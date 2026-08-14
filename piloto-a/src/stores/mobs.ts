import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { s60ToDegrees, degreesToS60, type S60Components } from '@/utils/s60-to-degrees'

export interface NpcWire {
  id: number
  name: string
  title: string
  faction: string
  avatar: string
  state: 'idle' | 'wander' | 'approach' | 'deliver'
  lat_s60: S60Components
  lon_s60: S60Components
  zona_id: number
  mission_id: number
  active: boolean
  waypoints?: Array<{ lat: number; lon: number }>
  currentWaypointIdx?: number
  dialogueLines: string[]
  reward: { cobre: number; oro?: number }
}

export interface NpcsResponseWire {
  zona_id: number
  count: number
  npcs: NpcWire[]
}

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8080'

// NPCs deterministas iniciales con rutas reales de patrulla en Lota
const PATRULLAS_INICIALES: NpcWire[] = [
  {
    id: 1,
    name: 'Isidora Goyenechea',
    title: 'Matriarca del Carbón & Visión de la Luz',
    faction: 'Linaje de la Luz',
    avatar: '👑',
    state: 'wander',
    lat_s60: degreesToS60(-37.08834),
    lon_s60: degreesToS60(-73.16527),
    zona_id: 89121388, // Parque de Lota
    mission_id: 1,
    active: true,
    waypoints: [
      { lat: -37.08834, lon: -73.16527 },
      { lat: -37.08910, lon: -73.16480 },
      { lat: -37.08980, lon: -73.16550 },
      { lat: -37.08834, lon: -73.16527 }
    ],
    currentWaypointIdx: 0,
    dialogueLines: [
      "Camina conmigo por la alameda... Mis ingenieros decían que era imposible iluminar una mina bajo el mar.",
      "Lota fue la primera ciudad de Chile con luz eléctrica antes que Santiago. No dejes que olviden ese orgullo.",
      "Toma este despacho sellado y llévalo a la maestranza antes del atardecer."
    ],
    reward: { cobre: 50, oro: 10 }
  },
  {
    id: 2,
    name: 'El Palanquero',
    title: 'Guardián de los Desvíos & Fogonero Mayor',
    faction: 'Hermandad del Carbón',
    avatar: '⛏️',
    state: 'wander',
    lat_s60: degreesToS60(-37.09275),
    lon_s60: degreesToS60(-73.16300),
    zona_id: 12557447365, // Pabellón 81 / Corredor
    mission_id: 2,
    active: true,
    waypoints: [
      { lat: -37.09275, lon: -73.16300 },
      { lat: -37.09380, lon: -73.16450 },
      { lat: -37.09450, lon: -73.16700 },
      { lat: -37.09500, lon: -73.17000 },
      { lat: -37.09275, lon: -73.16300 }
    ],
    currentWaypointIdx: 0,
    dialogueLines: [
      "¡Apura el paso, forastero! Si no llego a tiempo a la aguja del desvío, el tren de carros se descarrila.",
      "¿Ves ese pabellón de madera? Cada tabla la pagamos con sudor. Escucha el crujido... la mina nunca duerme.",
      "Toma este pedazo de carbón de piedra grasa y llévalo al horno de barro. Te pagarán con pan recién salido."
    ],
    reward: { cobre: 75, oro: 5 }
  },
  {
    id: 3,
    name: 'El Ciego de la Mina',
    title: 'Voz de las Galerías Submarinas',
    faction: 'Hermandad del Carbón',
    avatar: '🕯️',
    state: 'idle',
    lat_s60: degreesToS60(-37.09500),
    lon_s60: degreesToS60(-73.17100),
    zona_id: 480338029, // Chiflón del Diablo
    mission_id: 3,
    active: true,
    waypoints: [
      { lat: -37.09500, lon: -73.17100 },
      { lat: -37.09460, lon: -73.17050 },
      { lat: -37.09500, lon: -73.17100 }
    ],
    currentWaypointIdx: 0,
    dialogueLines: [
      "No necesito ojos para saber que estás parado sobre la veta más profunda del Pacífico.",
      "Siente el aire frío que sube del pique... Cuando el mar ruge arriba, aquí abajo rezamos en silencio.",
      "Toma esta ficha minera de 1895. Canjéala en la pulpería por algo caliente."
    ],
    reward: { cobre: 100, oro: 15 }
  }
]

export const useMobsStore = defineStore('mobs', () => {
  const mobsActivos = ref<NpcWire[]>([...PATRULLAS_INICIALES])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const interceptedNpc = ref<NpcWire | null>(null)
  let tickerInterval: number | null = null

  // Inicia la simulación de movimiento de patrullas
  function startPatrolTicker() {
    if (tickerInterval) return
    tickerInterval = window.setInterval(() => {
      advancePatrolStep()
    }, 1500)
  }

  function stopPatrolTicker() {
    if (tickerInterval) {
      clearInterval(tickerInterval)
      tickerInterval = null
    }
  }

  // Avanza deterministamente la posición de cada NPC según sus waypoints
  function advancePatrolStep() {
    mobsActivos.value = mobsActivos.value.map((npc) => {
      if (!npc.waypoints || npc.waypoints.length < 2) return npc

      const currentLat = s60ToDegrees(npc.lat_s60)
      const currentLon = s60ToDegrees(npc.lon_s60)
      const currentIdx = npc.currentWaypointIdx || 0
      const target = npc.waypoints[currentIdx]!

      const dLat = target.lat - currentLat
      const dLon = target.lon - currentLon
      const dist = Math.sqrt(dLat * dLat + dLon * dLon)

      // Si llegó al waypoint, pasar al siguiente
      if (dist < 0.00015) {
        const nextIdx = (currentIdx + 1) % npc.waypoints.length
        return {
          ...npc,
          currentWaypointIdx: nextIdx,
        }
      }

      // Paso de avance suave (velocidad de caminata humana)
      const stepSize = 0.00008
      const nextLat = currentLat + (dLat / dist) * stepSize
      const nextLon = currentLon + (dLon / dist) * stepSize

      return {
        ...npc,
        lat_s60: degreesToS60(nextLat),
        lon_s60: degreesToS60(nextLon),
      }
    })
  }

  // Comprueba si el jugador está a corta distancia (< 35 metros) de algún NPC
  function checkProximity(playerLat: number, playerLon: number): NpcWire | null {
    const PROXIMITY_THRESHOLD_DEG = 0.00035 // aprox 35 metros

    for (const npc of mobsActivos.value) {
      try {
        const npcLat = s60ToDegrees(npc.lat_s60)
        const npcLon = s60ToDegrees(npc.lon_s60)
        const dLat = playerLat - npcLat
        const dLon = playerLon - npcLon
        const dist = Math.sqrt(dLat * dLat + dLon * dLon)

        if (dist <= PROXIMITY_THRESHOLD_DEG) {
          interceptedNpc.value = npc
          return npc
        }
      } catch (e) {
        // Coordenadas en cálculo
      }
    }

    interceptedNpc.value = null
    return null
  }

  async function fetchNpcs(zonaId: number): Promise<void> {
    loading.value = true
    error.value = null
    try {
      const res = await fetch(`${API_BASE}/npcs?zona_id=${zonaId}`)
      if (res.ok) {
        const data = (await res.json()) as NpcsResponseWire
        if (data.npcs && data.npcs.length > 0) {
          // Fusionar con datos narrativos locales
          mobsActivos.value = data.npcs.map(wire => {
            const local = PATRULLAS_INICIALES.find(p => p.id === wire.id)
            return {
              ...wire,
              title: local?.title || 'Habitante del Carbón',
              faction: local?.faction || 'Hermandad del Carbón',
              avatar: local?.avatar || '👤',
              dialogueLines: local?.dialogueLines || ['La historia de Lota sigue viva.'],
              reward: local?.reward || { cobre: 30 },
              waypoints: local?.waypoints
            }
          })
          return
        }
      }
    } catch (e) {
      // Fallback determinista local activo
    } finally {
      loading.value = false
    }
  }

  function clearMobs(): void {
    // Mantiene las patrullas activas para que siempre haya vida en el mapa
  }

  return {
    mobsActivos,
    loading,
    error,
    interceptedNpc,
    startPatrolTicker,
    stopPatrolTicker,
    advancePatrolStep,
    checkProximity,
    fetchNpcs,
    clearMobs,
  }
})
