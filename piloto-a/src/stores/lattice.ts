import { ref } from 'vue'
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

export const useLatticeStore = defineStore('lattice', () => {
  const lastTick = ref<number | null>(null)
  const lastWaveSample = ref<number[]>([])
  const lastPortales = ref<number[]>([])
  const portalCount = ref<number>(0)
  const connected = ref(false)
  const error = ref<string | null>(null)

  let socket: WebSocket | null = null
  let reconnectTimer: ReturnType<typeof setTimeout> | null = null
  let reconnectDelay = 1000
  let isIntentionallyClosed = false

  function connect(wsUrl?: string): void {
    if (socket && (socket.readyState === WebSocket.CONNECTING || socket.readyState === WebSocket.OPEN)) {
      return
    }

    isIntentionallyClosed = false
    const targetUrl = wsUrl || defaultWsUrl()

    try {
      socket = new WebSocket(targetUrl)

      socket.onopen = () => {
        connected.value = true
        error.value = null
        reconnectDelay = 1000
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
          scheduleReconnect(targetUrl)
        }
      }
    } catch (e) {
      error.value = 'No se pudo crear WebSocket'
      connected.value = false
      scheduleReconnect(targetUrl)
    }
  }

  function scheduleReconnect(targetUrl: string): void {
    if (reconnectTimer) clearTimeout(reconnectTimer)
    reconnectTimer = setTimeout(() => {
      reconnectDelay = Math.min(reconnectDelay * 2, 30000)
      connect(targetUrl)
    }, reconnectDelay)
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
  }

  return {
    lastTick,
    lastWaveSample,
    lastPortales,
    portalCount,
    connected,
    error,
    connect,
    disconnect,
  }
})
