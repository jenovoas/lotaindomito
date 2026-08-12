<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { Map, NavigationControl, Popup, Marker, type LngLatLike } from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'
import booleanPointInPolygon from '@turf/boolean-point-in-polygon'
import { point as turfPoint, polygon as turfPolygon } from '@turf/turf'
import zonasData from '../data/zonas-lota.json'
import { useGeofenceStore } from '@/stores/geofence'
import { useGeolocation } from '@/composables/useGeolocation'
import { useWalletStore } from '@/stores/wallet'
import { useMobsStore } from '@/stores/mobs'
import { useLatticeStore } from '@/stores/lattice'
import { useAnalyticsStore } from '@/stores/analytics'
import { useWorldEventsStore } from '@/stores/worldEvents'
import { s60ToDegrees } from '@/utils/s60-to-degrees'
import MicroSesionChiflon from './MicroSesionChiflon.vue'
import MicroSesionIsidora from './MicroSesionIsidora.vue'
import MicroSesionPabellon from './MicroSesionPabellon.vue'
import WorldEventBanner from './WorldEventBanner.vue'

interface ZonaOSM {
  id: number
  name: string
  tags: { historic?: string; tourism?: string; leisure?: string; natural?: string }
  coords: Array<{ lat: number; lon: number }>
}

const zonas = (zonasData as { zonas: ZonaOSM[]; count: number; fuente: string }).zonas

const mapContainer = ref<HTMLElement | null>(null)
const geofence = useGeofenceStore()
const walletStore = useWalletStore()
const mobsStore = useMobsStore()
const latticeStore = useLatticeStore()
const analytics = useAnalyticsStore()
const worldEvents = useWorldEventsStore()
const { lat, lon, gpsAvailable, isWatching, teleport } = useGeolocation()
let map: Map | null = null
let npcMarkers: Marker[] = []
let npcEventMarker: Marker | null = null
let npcEventInterval: ReturnType<typeof setInterval> | null = null

const showChiflonModal = ref(false)
const showIsidoraModal = ref(false)
const showPabellonModal = ref(false)

function onMissionComplete(reward: { cobre: number; oro?: number }, zonaId?: number | null) {
  walletStore.balance.cobre += reward.cobre
  if (reward.oro) walletStore.balance.oro += reward.oro
  analytics.trackMissionComplete(
    zonaId ? String(zonaId) : 'unknown',
    true,
    { cobre: reward.cobre, oro: reward.oro }
  )
  if (worldEvents.eventosActivos.length > 0 && zonaId) {
    const evento = worldEvents.eventosActivos[0]
    if (evento.npc_exclusiva.zona_id === zonaId && evento.misiones[0]) {
      const m = evento.misiones[0]
      if (m.recompensa_insignia) {
        const insignia = evento.insignias.find(i => i.id === m.recompensa_insignia)
        if (insignia) worldEvents.desbloquearInsignia(insignia)
      }
      if (m.recompensa_cupon) {
        worldEvents.desbloquearCupon(m.recompensa_cupon)
      }
    }
  }
}

function updateNpcMarkers() {
  if (!map) return
  npcMarkers.forEach((m) => m.remove())
  npcMarkers = []

  for (const npc of mobsStore.mobsActivos) {
    try {
      const npcLat = s60ToDegrees(npc.lat_s60)
      const npcLon = s60ToDegrees(npc.lon_s60)
      const el = document.createElement('div')
      el.className = 'npc-marker'
      el.innerText = '👤 ' + npc.name
      el.style.backgroundColor = '#161b22'
      el.style.color = '#3FE6C0'
      el.style.border = '2px solid #3FE6C0'
      el.style.borderRadius = '12px'
      el.style.padding = '4px 8px'
      el.style.fontSize = '0.8rem'
      el.style.fontWeight = 'bold'
      el.style.boxShadow = '0 2px 8px rgba(0,0,0,0.5)'
      el.style.cursor = 'pointer'

      const marker = new Marker({ element: el })
        .setLngLat([npcLon, npcLat])
        .addTo(map)

      npcMarkers.push(marker)
    } catch (e) {
      console.warn('Coordenadas S60 inválidas para NPC', npc, e)
    }
  }
}

watch(
  () => mobsStore.mobsActivos,
  () => {
    updateNpcMarkers()
  },
  { deep: true }
)

watch(
  () => geofence.zonaActiva,
  (nuevaZona) => {
    if (nuevaZona?.entered && nuevaZona.zona_id) {
      mobsStore.fetchNpcs(nuevaZona.zona_id)
    } else {
      mobsStore.clearMobs()
      updateNpcMarkers()
    }
  }
)

// Abre la micro-sesión correspondiente a una zona patrimonial.
function abrirMision(zonaId: number | null, zonaName?: string | null) {
  const name = zonaName || ''
  if (zonaId) {
    analytics.trackPoiVisit(zonaId, 0)
  }
  // Chiflón del Diablo (Museo de Sitio / Chiflón)
  if (zonaId === 480338029 || name.includes('Chiflón')) {
    showChiflonModal.value = true
    return
  }
  // Parque Isidora Cousiño
  if (zonaId === 89121388 || name.includes('Isidora')) {
    showIsidoraModal.value = true
    return
  }
  // Pabellón 81 (zona 3 — reemplaza al Pabellón 83 de la spec original)
  if ((zonaId && [12557447365].includes(zonaId)) || name.includes('Pabellón')) {
    showPabellonModal.value = true
    return
  }
}

onMounted(() => {
  if (!mapContainer.value) return

  worldEvents.init()
  latticeStore.connect()

  // Construir GeoJSON con polígonos de las zonas patrimoniales
  const features = zonas
    .filter((z) => z.coords.length >= 3)
    .map((z) => ({
      type: 'Feature' as const,
      id: z.id,
      properties: { name: z.name, tags: z.tags },
      geometry: {
        type: 'Polygon' as const,
        coordinates: [[...z.coords.map((c): [number, number] => [c.lon, c.lat]), [z.coords[0]!.lon, z.coords[0]!.lat]]],
      },
    }))

  const zonasGeoJSON = {
    type: 'FeatureCollection' as const,
    features,
  }

  map = new Map({
    container: mapContainer.value,
    style: {
      version: 8,
      sources: {
        osm: {
          type: 'raster',
          tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
          tileSize: 256,
          attribution: '© OpenStreetMap contributors',
        },
      },
      layers: [{ id: 'osm-tiles', type: 'raster', source: 'osm' }],
    },
    center: [-73.165, -37.089],
    zoom: 15,
  })

  map.addControl(new NavigationControl(), 'top-right')

  map.on('load', () => {
    if (!map) return

    // Capa de polígonos patrimoniales (verde translúcido)
    map.addSource('zonas-patrimoniales', { type: 'geojson', data: zonasGeoJSON })

    map.addLayer({
      id: 'zonas-fill',
      type: 'fill',
      source: 'zonas-patrimoniales',
      paint: {
        'fill-color': '#3FE6C0',
        'fill-opacity': 0.25,
      },
    })

    map.addLayer({
      id: 'zonas-outline',
      type: 'line',
      source: 'zonas-patrimoniales',
      paint: {
        'line-color': '#3FE6C0',
        'line-width': 2,
      },
    })

    let npcEventMarker: Marker | null = null

    watch(
      () => worldEvents.eventosActivos,
      (activos) => {
        if (!map) return
        if (activos.length === 0) {
          if (npcEventMarker) {
            npcEventMarker.remove()
            npcEventMarker = null
          }
          return
        }
        const evt = activos[0]
        const ruta = evt.npc_exclusiva.ruta_fija
        if (ruta.length === 0) return
        const pos = ruta[0]!
        if (npcEventMarker) npcEventMarker.remove()
        const el = document.createElement('div')
        el.className = 'npc-event-marker'
        el.innerText = `👒 ${evt.npc_exclusiva.nombre}`
        el.style.cssText = `
          background: ${evt.colores.primario};
          color: white;
          border: 2px solid ${evt.colores.secundario};
          border-radius: 16px;
          padding: 4px 10px;
          font-size: 0.8rem;
          font-weight: bold;
          box-shadow: 0 2px 8px rgba(0,0,0,0.5);
          cursor: pointer;
          white-space: nowrap;
        `
        npcEventMarker = new Marker({ element: el })
          .setLngLat([pos.lon, pos.lat])
          .addTo(map)
        el.addEventListener('click', () => {
          alert(`${evt.npc_exclusiva.nombre}: ${evt.npc_exclusiva.historia}`)
        })
        let tick = 0
        if (npcEventInterval) clearInterval(npcEventInterval)
        npcEventInterval = setInterval(() => {
          if (!map || !npcEventMarker) { clearInterval(npcEventInterval!); return }
          tick++
          const idx = tick % ruta.length
          npcEventMarker.setLngLat([ruta[idx]!.lon, ruta[idx]!.lat])
        }, 5000)
      },
      { immediate: true }
    )

    // Popup al hacer click en una zona
    map.on('click', 'zonas-fill', (e) => {
      if (!map || !e.features?.[0]) return
      const feature = e.features[0]
      const name = feature.properties?.name ?? 'Sin nombre'
      const tags = JSON.stringify(feature.properties?.tags ?? {})
      new Popup({ offset: 12, closeButton: true })
        .setLngLat(e.lngLat as LngLatLike)
        .setHTML(`<h3>${name}</h3><p style="font-size:0.8em;color:#8b949e">${tags}</p>`)
        .addTo(map)
    })

    // Cambiar cursor al pasar sobre una zona
    map.on('mouseenter', 'zonas-fill', () => {
      if (map) map.getCanvas().style.cursor = 'pointer'
    })
    map.on('mouseleave', 'zonas-fill', () => {
      if (map) map.getCanvas().style.cursor = ''
    })

    // Teletransporte virtual al hacer click en el mapa
    map.on('click', (e) => {
      if (geofence.isVirtualMode) {
        teleport(e.lngLat.lat, e.lngLat.lng)
      }
    })

    // Demo de geofencing: promedio de vértices cae dentro del polígono del Parque Isidora
    const isidora = zonas.find((z) => z.id === 89121388 || z.name.includes('Isidora'))
    if (isidora && isidora.coords.length >= 3) {
      const coords: [number, number][] = isidora.coords.map((c) => [c.lon, c.lat])
      const poly = turfPolygon([[...coords, coords[0]!]])
      const avgLng = coords.reduce((s, c) => s + c[0], 0) / coords.length
      const avgLat = coords.reduce((s, c) => s + c[1], 0) / coords.length
      const pt = turfPoint([avgLng, avgLat])
      const inside = booleanPointInPolygon(pt, poly)
      console.log(`[geofencing] ${isidora.name}: promedio de vértices dentro = ${inside}`)
    }

    // Forzar resize tras layout estable
    setTimeout(() => map?.resize(), 100)
  })
})

onUnmounted(() => {
  latticeStore.disconnect()
  npcMarkers.forEach((m) => m.remove())
  if (npcEventInterval) clearInterval(npcEventInterval)
  if (npcEventMarker) npcEventMarker.remove()
  map?.remove()
})
</script>

<template>
  <div class="mapa-container">
    <div ref="mapContainer" class="mapa"></div>

    <!-- Banner: GPS no disponible -->
    <div v-if="!gpsAvailable" class="banner banner-gps">
      GPS no disponible, modo manual activado
    </div>

    <!-- Banner: dentro de una zona -->
    <div v-if="geofence.zonaActiva?.entered" class="banner banner-zona">
      Estás en {{ geofence.zonaActiva.zona_name }}
    </div>

    <!-- Banner: World Events activos y próximos -->
    <WorldEventBanner />

    <!-- Indicador de WebSocket Lattice -->
    <div class="status-ws" :class="{ conectado: latticeStore.connected }">
      Lattice WS: {{ latticeStore.connected ? `🟢 Tick #${latticeStore.lastTick ?? '-'}` : '🔴 Desconectado' }}
    </div>

    <aside v-if="geofence.zonaActiva" class="panel-zona">
      <button class="cerrar" @click="geofence.zonaActiva = null">✕</button>
      <h2>{{ geofence.zonaActiva.zona_name }}</h2>
      <p class="origen">Origen: OpenStreetMap (Overpass API, 2026-08-12)</p>
      <p class="hint">
        {{ mobsStore.mobsActivos.length > 0 ? `NPC ${mobsStore.mobsActivos[0]?.name} detectada en la zona.` : 'Geofencing listo — entra a una zona patrimonial para encontrar personajes históricos.' }}
      </p>
      <button class="btn-mision" @click="abrirMision(geofence.zonaActiva.zona_id, geofence.zonaActiva.zona_name)">
        Iniciar Misión: {{ geofence.zonaActiva.zona_name }}
      </button>
    </aside>

    <MicroSesionChiflon
      v-if="showChiflonModal"
      @close="showChiflonModal = false"
      @complete="(r: { cobre: number; oro?: number }) => onMissionComplete(r, 480338029)"
    />
    <MicroSesionIsidora
      v-if="showIsidoraModal"
      @close="showIsidoraModal = false"
      @complete="(r: { cobre: number; oro?: number }) => onMissionComplete(r, 89121388)"
    />
    <MicroSesionPabellon
      v-if="showPabellonModal"
      @close="showPabellonModal = false"
      @complete="(r: { cobre: number; oro?: number }) => onMissionComplete(r, 12557447365)"
    />
    <aside class="panel-zonas">
      <h3>Zonas patrimoniales</h3>
      <ul>
        <li v-for="z in zonas" :key="z.id">
          {{ z.name }}
        </li>
      </ul>
      <p class="count">{{ zonas.length }} zonas · fuente OSM</p>
    </aside>
  </div>
</template>

<style scoped>
.mapa-container {
  flex: 1;
  position: relative;
  min-width: 0;
  min-height: 0;
  width: 100%;
  height: 100%;
}

.mapa {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.banner {
  position: absolute;
  top: 1rem;
  left: 50%;
  transform: translateX(-50%);
  padding: 0.6rem 1rem;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
  z-index: 10;
  pointer-events: none;
}

.banner-gps {
  background: #161b22;
  border: 1px solid #30363d;
  color: #e6e9ef;
}

.banner-zona {
  background: #3fe6c0;
  color: #0f1216;
}

.status-ws {
  position: absolute;
  top: 1rem;
  right: 4rem;
  background: #161b22;
  border: 1px solid #30363d;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  font-size: 0.75rem;
  color: #8b949e;
  z-index: 10;
}

.status-ws.conectado {
  color: #3fe6c0;
  border-color: #3fe6c0;
}

.panel-zona,
.panel-zonas {
  position: absolute;
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
  color: #c9d1d9;
}

.panel-zona {
  right: 1rem;
  bottom: 2rem;
  width: 280px;
}

.panel-zonas {
  left: 1rem;
  top: 6rem;
  width: 260px;
  max-height: calc(100vh - 8rem);
  overflow-y: auto;
}

.panel-zonas h3 {
  font-size: 1rem;
  color: #3FE6C0;
  margin-bottom: 0.5rem;
}

.panel-zonas ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.panel-zonas li {
  padding: 0.4rem 0.6rem;
  margin: 2px 0;
  border-radius: 4px;
  font-size: 0.85rem;
}

.panel-zonas li:hover {
  background: #21262d;
  color: #3FE6C0;
}

.panel-zonas .count {
  margin-top: 0.5rem;
  font-size: 0.7rem;
  color: #6e7681;
}

.panel-zona h2 {
  font-size: 1.1rem;
  color: #3FE6C0;
  margin-bottom: 0.3rem;
}

.panel-zona p {
  font-size: 0.85rem;
  color: #8b949e;
}

.panel-zona .origen {
  font-size: 0.7rem;
  color: #6e7681;
}

.panel-zona .hint {
  margin-top: 0.5rem;
  font-style: italic;
}

.cerrar {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: none;
  border: none;
  color: #8b949e;
  cursor: pointer;
  font-size: 1rem;
}
</style>
