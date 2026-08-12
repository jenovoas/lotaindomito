import { ref } from 'vue'
import { defineStore } from 'pinia'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export interface Insignia {
  id: string
  nombre: string
  descripcion: string
  imagen: string
  caduca: boolean
}

export interface Cupon {
  id: string
  nombre: string
  comercio: string
  comercio_id: string
  descuento: string
  validez_dias: number
}

export interface Mission {
  id: string
  nombre: string
  descripcion: string
  pasos: number
  recompensa_minerales: { cobre?: number; oro?: number; estanio?: number }
  recompensa_insignia: string
  recompensa_cupon: Cupon | null
}

export interface WorldEvent {
  id: string
  nombre: string
  descripcion: string
  fecha_inicio: string
  fecha_fin: string
  npc_exclusiva: {
    nombre: string
    rol: string
    historia: string
    zona_nombre: string
    zona_id: number
    ruta_fija: Array<{ lat: number; lon: number }>
  }
  misiones: Mission[]
  insignias: Insignia[]
  tematica: string
  colores: { primario: string; secundario: string; fondo: string }
  activo: boolean
}

export const useWorldEventsStore = defineStore('worldEvents', () => {
  const eventos = ref<WorldEvent[]>([])
  const eventosActivos = ref<WorldEvent[]>([])
  const eventosProximos = ref<WorldEvent[]>([])
  const insigniasObtenidas = ref<Insignia[]>([])
  const cuponesObtenidos = ref<Cupon[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const INSIGNIAS_KEY = 'lota_insignias'
  const CUPONES_KEY = 'lota_cupones'

  async function fetchAll() {
    loading.value = true
    error.value = null
    try {
      const [all, activos, proximos] = await Promise.all([
        fetch(`${API_BASE}/api/world-events`),
        fetch(`${API_BASE}/api/world-events/activos`),
        fetch(`${API_BASE}/api/world-events/proximos`),
      ])
      const [allData, activosData, proximosData] = await Promise.all([
        all.json(),
        activos.json(),
        proximos.json(),
      ])
      eventos.value = allData
      eventosActivos.value = activosData
      eventosProximos.value = proximosData
    } catch (err) {
      error.value = String(err)
    } finally {
      loading.value = false
    }
  }

  function cargarInsignias() {
    try {
      const stored = localStorage.getItem(INSIGNIAS_KEY)
      if (stored) insigniasObtenidas.value = JSON.parse(stored)
    } catch { insigniasObtenidas.value = [] }
  }

  function cargarCupones() {
    try {
      const stored = localStorage.getItem(CUPONES_KEY)
      if (stored) cuponesObtenidos.value = JSON.parse(stored)
    } catch { cuponesObtenidos.value = [] }
  }

  function desbloquearInsignia(insignia: Insignia) {
    if (!insigniasObtenidas.value.find(i => i.id === insignia.id)) {
      insigniasObtenidas.value.push(insignia)
      localStorage.setItem(INSIGNIAS_KEY, JSON.stringify(insigniasObtenidas.value))
    }
  }

  function desbloquearCupon(cupon: Cupon) {
    if (!cuponesObtenidos.value.find(c => c.id === cupon.id)) {
      cuponesObtenidos.value.push(cupon)
      localStorage.setItem(CUPONES_KEY, JSON.stringify(cuponesObtenidos.value))
    }
  }

  function obtenerPosicionNpc(eventId: string, tick: number): Promise<{ lat: number; lon: number; npc: string } | null> {
    return fetch(`${API_BASE}/api/world-events/${eventId}/npc/posicion?tick=${tick}`)
      .then(r => r.json())
      .catch(() => null)
  }

  function init() {
    cargarInsignias()
    cargarCupones()
    fetchAll()
  }

  return {
    eventos,
    eventosActivos,
    eventosProximos,
    insigniasObtenidas,
    cuponesObtenidos,
    loading,
    error,
    init,
    fetchAll,
    desbloquearInsignia,
    desbloquearCupon,
    obtenerPosicionNpc,
  }
})
