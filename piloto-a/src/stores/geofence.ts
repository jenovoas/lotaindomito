import { ref } from 'vue'
import { defineStore } from 'pinia'
import booleanPointInPolygon from '@turf/boolean-point-in-polygon'
import { point as turfPoint, polygon as turfPolygon } from '@turf/turf'
import zonasData from '../data/zonas-lota.json'

export interface ZonaInfo {
  zona_id: number | null
  zona_name: string | null
  entered: boolean
}

interface ZonaOSM {
  id: number
  name: string
  tags: Record<string, string>
  coords: Array<{ lat: number; lon: number }>
}

const zonas = (zonasData as unknown as { zonas: ZonaOSM[]; count: number; fuente: string }).zonas

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

  function checkPosition(lat: number, lon: number, _userId: string): void {
    loading.value = true
    error.value = null
    try {
      if (typeof lat !== 'number' || typeof lon !== 'number' || isNaN(lat) || isNaN(lon)) {
        error.value = 'Coordenadas inválidas'
        return
      }

      const pt = turfPoint([lon, lat])
      let found: ZonaOSM | null = null

      for (const z of zonas) {
        if (z.coords && z.coords.length >= 3) {
          const coords: [number, number][] = z.coords.map((c) => [c.lon, c.lat])
          const poly = turfPolygon([[...coords, coords[0]!]])
          if (booleanPointInPolygon(pt, poly)) {
            found = z
            break
          }
        }
      }

      const prevName = zonaActiva.value?.zona_name
      if (found) {
        const isNew = found.name !== prevName
        const newZona: ZonaInfo = {
          zona_id: found.id,
          zona_name: found.name,
          entered: true,
        }
        zonaActiva.value = newZona
        if (isNew) {
          emitZonaEntered(newZona)
        }
      } else {
        zonaActiva.value = {
          zona_id: null,
          zona_name: null,
          entered: false,
        }
      }
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'No se pudo verificar posición'
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
