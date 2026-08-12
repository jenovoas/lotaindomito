import { ref } from 'vue'
import { defineStore } from 'pinia'
import type { S60Components } from '@/utils/s60-to-degrees'

export interface NpcWire {
  id: number
  name: string
  state: string
  lat_s60: S60Components
  lon_s60: S60Components
  zona_id: number
  mission_id: number
  active: boolean
}

export interface NpcsResponseWire {
  zona_id: number
  count: number
  npcs: NpcWire[]
}

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8080'

export const useMobsStore = defineStore('mobs', () => {
  const mobsActivos = ref<NpcWire[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchNpcs(zonaId: number): Promise<void> {
    loading.value = true
    error.value = null
    try {
      const res = await fetch(`${API_BASE}/npcs?zona_id=${zonaId}`)
      if (!res.ok) {
        throw new Error(`Error ${res.status}: ${res.statusText}`)
      }
      const data = (await res.json()) as NpcsResponseWire
      mobsActivos.value = data.npcs || []
    } catch (e) {
      error.value = 'No se pudo cargar la lista de NPCs desde el servidor'
    } finally {
      loading.value = false
    }
  }

  function clearMobs(): void {
    mobsActivos.value = []
  }

  return {
    mobsActivos,
    loading,
    error,
    fetchNpcs,
    clearMobs,
  }
})
