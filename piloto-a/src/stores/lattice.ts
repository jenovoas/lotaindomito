import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export interface LatticeTickEvent {
  event: 'lattice_tick'
  tick: number
  node_count: number
  wave_value_sample: number[]
}

export interface PortalOpenedEvent {
  event: 'portal_opened'
  indices: number[]
  count: number
  tick: number
}

export type ServerWsEvent = LatticeTickEvent | PortalOpenedEvent

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8080'

function defaultWsUrl(): string {
  const url = new URL(API_BASE)
  const protocol = url.protocol === 'https:' ? 'wss:' : 'ws:'
  return `${protocol}//${url.host}/ws/events`
}

export type ConnectionStatus = 'connected' | 'reconnecting' | 'offline'

/**
 * Backoff exponencial con jitter ± 20%.
 * Backoff inicial 1s, máximo 30s.
 */
function backoffMs(retries: number): number {
  const base = Math.min(30_000, 1_000 * Math.pow(2, retries))
  const jitter = 1 + (Math.random() - 0.5) * 0.4
  return Math.max(500, Math.floor(base * jitter))
}

export const useLatticeStore = defineStore('lattice', () => {
  const lastTick = ref<number | null>(null)
  const lastWaveSample = ref<number[]>([])
  const lastPortales = ref<number[]>([])
  const portalCount = ref<number>(0)
  const connected = ref(false)
  const error = ref<string | null>(null)
  const reconnectAttempts = ref(0)
  const connectionStatus = ref<ConnectionStatus>('offline')

  let socket: WebSocket | null = null
  let reconnectTimer: ReturnType<typeof setTimeout> | null = null
  let isIntentionallyClosed = false

  function connect(wsUrl?: string): void {
    if (socket && (socket.readyState === WebSocket.CONNECTING || socket.readyState === WebSocket.OPEN)) {
      return
    }

    isIntentionallyClosed = false
    const targetUrl = wsUrl || defaultWsUrl()

    if (reconnectAttempts.value > 0) {
      connectionStatus.value = 'reconnecting'
    }

    try {
      socket = new WebSocket(targetUrl)

      socket.onopen = () => {
        connected.value = true
        error.value = null
        connectionStatus.value = 'connected'
        reconnectAttempts.value = 0
      }

      socket.onmessage = (msg) => {
        try {
          const data = JSON.parse(msg.data) as ServerWsEvent
          if (data.event === 'lattice_tick') {
            lastTick.value = data.tick
            lastWaveSample.value = data.wave_value_sample || []
          } else if (data.event === 'portal_opened') {
            lastPortales.value = data.indices || []
            portalCount.value = data.count || 0
          }
        } catch {
          // Ignore malformed messages
        }
      }

      socket.onerror = () => {
        error.value = 'Error en conexión WebSocket con lota-server'
      }

      socket.onclose = () => {
        connected.value = false
        socket = null
        if (!isIntentionallyClosed) {
          connectionStatus.value = reconnectAttempts.value === 0 ? 'reconnecting' : 'reconnecting'
          scheduleReconnect(targetUrl)
        } else {
          connectionStatus.value = 'offline'
        }
      }
    } catch (e) {
      error.value = 'No se pudo crear WebSocket'
      connected.value = false
      connectionStatus.value = 'reconnecting'
      scheduleReconnect(targetUrl)
    }
  }

  function scheduleReconnect(targetUrl: string): void {
    if (reconnectTimer) clearTimeout(reconnectTimer)
    const delay = backoffMs(reconnectAttempts.value)
    reconnectAttempts.value += 1
    connectionStatus.value = 'reconnecting'
    reconnectTimer = setTimeout(() => {
      connect(targetUrl)
    }, delay)
  }

  function disconnect(): void {
    isIntentionallyClosed = true
    if (reconnectTimer) {
      clearTimeout(reconnectTimer)
      reconnectTimer = null
    }
    if (socket) {
      socket.close()
      socket = null
    }
    connected.value = false
    connectionStatus.value = 'offline'
    reconnectAttempts.value = 0
  }

  const isLatticePaused = computed(() => connectionStatus.value !== 'connected')

  return {
    lastTick,
    lastWaveSample,
    lastPortales,
    portalCount,
    connected,
    error,
    reconnectAttempts,
    connectionStatus,
    isLatticePaused,
    connect,
    disconnect,
  }
})
