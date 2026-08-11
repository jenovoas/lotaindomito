import { ref } from 'vue'
import { defineStore } from 'pinia'

export interface ZonaInfo {
  zona_id: number | null
  zona_name: string | null
  entered: boolean
}

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export const useGeofenceStore = defineStore('geofence', () => {
  const zonaActiva = ref<ZonaInfo | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const isVirtualMode = ref(false)

  // Event listener for zona-entered
  const zonaEnteredListeners = ref<((zona: ZonaInfo) => void)[]>([])

  function onZonaEntered(callback: (zona: ZonaInfo) => void): void {
    zonaEnteredListeners.value.push(callback)
  }

  function emitZonaEntered(zona: ZonaInfo): void {
    if (zona.entered) {
      zonaEnteredListeners.value.forEach((cb) => cb(zona))
    }
  }

  async function checkPosition(lat: number, lon: number, userId: string): Promise<void> {
    loading.value = true
    error.value = null
    try {
      const res = await fetch(`${API_BASE}/api/geofence/check`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lat, lon, user_id: userId }),
      })
      if (res.ok) {
        const zona = (await res.json()) as ZonaInfo
        // Detectar cambio de zona
        const prevName = zonaActiva.value?.zona_name
        zonaActiva.value = zona
        if (zona.zona_name && zona.zona_name !== prevName) {
          zona.entered = true
          emitZonaEntered(zona)
        }
      }
    } catch (e) {
      error.value = 'No se pudo verificar posición'
    } finally {
      loading.value = false
    }
  }

  function setVirtualMode(enabled: boolean): void {
    isVirtualMode.value = enabled
  }

  return {
    zonaActiva,
    loading,
    error,
    isVirtualMode,
    checkPosition,
    onZonaEntered,
    setVirtualMode,
  }
})
