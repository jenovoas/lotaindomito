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
import VisorRA from './VisorRA.vue'
import WorldEventBanner from './WorldEventBanner.vue'
import type { NpcWire } from '@/stores/mobs'

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
const showVisorRaModal = ref(false)
const activeNpcForRa = ref<NpcWire | null>(null)

function openVisorRa(npc: NpcWire) {
  activeNpcForRa.value = npc
  showVisorRaModal.value = true
}

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
    if (evento && evento.npc_exclusiva.zona_id === zonaId && evento.misiones[0]) {
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
      el.innerText = `${npc.avatar || '👤'} ${npc.name} [RA]`
      el.style.backgroundColor = '#161b22'
      el.style.color = '#3FE6C0'
      el.style.border = '2px solid #3FE6C0'
      el.style.borderRadius = '12px'
      el.style.padding = '4px 8px'
      el.style.fontSize = '0.8rem'
      el.style.fontWeight = 'bold'
      el.style.boxShadow = '0 2px 10px rgba(63, 230, 192, 0.4)'
      el.style.cursor = 'pointer'
      el.style.transition = 'transform 0.2s'

      el.addEventListener('click', () => {
        openVisorRa(npc)
      })

      const marker = new Marker({ element: el })
        .setLngLat([npcLon, npcLat])
        .addTo(map)

      npcMarkers.push(marker)
    } catch (e) {
      console.warn('Coordenadas S60 inválidas para NPC', npc, e)
    }
  }

  // Verificar proximidad para activar el banner de intercepción
  if (lat.value && lon.value) {
    mobsStore.checkProximity(lat.value, lon.value)
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

function zoomIn() {
  if (map) map.zoomIn({ duration: 300 })
}

function zoomOut() {
  if (map) map.zoomOut({ duration: 300 })
}

function centrarEnJugador() {
  if (map && lat.value && lon.value) {
    map.flyTo({
      center: [lon.value, lat.value],
      zoom: 17,
      pitch: 55,
      bearing: -15,
      speed: 1.3,
      essential: true
    })
  } else if (map) {
    map.flyTo({
      center: [-73.165, -37.089],
      zoom: 16.5,
      pitch: 55,
      speed: 1.2,
      essential: true
    })
  }
}

function teleportAZona(zona: ZonaOSM) {
  console.log('[teleportAZona] Teletransportando a:', zona.name)
  if (!zona.coords || !zona.coords.length) return
  const avgLng = zona.coords.reduce((s, c) => s + c.lon, 0) / zona.coords.length
  const avgLat = zona.coords.reduce((s, c) => s + c.lat, 0) / zona.coords.length

  if (map) {
    map.flyTo({
      center: [avgLng, avgLat],
      zoom: 17,
      pitch: 55,
      bearing: -15,
      speed: 1.4,
      curve: 1.4,
      essential: true
    })
  }
  teleport(avgLat, avgLng)
  geofence.zonaActiva = {
    entered: true,
    zona_id: zona.id,
    zona_name: zona.name
  }
}

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
  mobsStore.startPatrolTicker()
  updateNpcMarkers()

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
        carto: {
          type: 'raster',
          tiles: ['https://basemaps.cartocdn.com/rastertiles/dark_all/{z}/{x}/{y}.png'],
          tileSize: 256,
          maxzoom: 19,
          attribution: '© CARTO / OpenStreetMap',
        },
      },
      layers: [{ id: 'carto-tiles', type: 'raster', source: 'carto', maxzoom: 22 }],
    },
    center: [-73.165, -37.089],
    zoom: 16.2,
    minZoom: 13,
    maxZoom: 19.5,
    maxBounds: [
      [-73.22, -37.14],
      [-73.10, -37.05]
    ],
    pitch: 52,
    maxPitch: 68,
    bearing: -15,
    dragRotate: true,
    touchZoomRotate: true,
    touchPitch: true,
    scrollZoom: true,
    doubleClickZoom: true,
  })

  map.addControl(new NavigationControl({ visualizePitch: true, showCompass: true, showZoom: false }), 'top-right')

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

let npcEventMarker: any = null

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
        if (!evt) return
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

    // Marcador del jugador
    const playerEl = document.createElement('div')
    playerEl.className = 'player-marker'
    playerEl.innerHTML = '🚶'
    playerEl.style.fontSize = '1.8rem'
    playerEl.style.filter = 'drop-shadow(0 0 8px #3FE6C0)'

    const playerMarker = new Marker({ element: playerEl })
      .setLngLat([lon.value || -73.165, lat.value || -37.089])
      .addTo(map)

    // Actualizar posición del jugador al cambiar GPS
    watch([lat, lon], ([newLat, newLon]) => {
      if (newLat && newLon && playerMarker) {
        playerMarker.setLngLat([newLon, newLat])
      }
    })

    // Forzar resize tras layout estable
    setTimeout(() => map?.resize(), 100)
  })
})

onUnmounted(() => {
  mobsStore.stopPatrolTicker()
  latticeStore.disconnect()
  npcMarkers.forEach((m) => m.remove())
  if (npcEventInterval) clearInterval(npcEventInterval)
  if (npcEventMarker) (npcEventMarker as any).remove()
  map?.remove()
})
</script>

<template>
  <div class="mapa-container">
    <div ref="mapContainer" class="mapa"></div>

    <!-- Banner: Intercepción en Movimiento / Proximidad RA -->
    <div
      v-if="mobsStore.interceptedNpc && !showVisorRaModal"
      class="banner banner-intercepcion"
      @click="openVisorRa(mobsStore.interceptedNpc)"
    >
      🚨 ¡{{ mobsStore.interceptedNpc.name }} camina a tu lado! Toca para Visor RA 👁️
    </div>

    <!-- Banner: GPS no disponible -->
    <div v-else-if="!gpsAvailable" class="banner banner-gps">
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
        {{ mobsStore.mobsActivos.length > 0 ? `Patrullas vivas activas en la comuna.` : 'Geofencing listo — entra a una zona patrimonial para encontrar personajes históricos.' }}
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

    <!-- Visor de Realidad Aumentada (RA) y Encuentro en Marcha -->
    <VisorRA
      v-if="showVisorRaModal && activeNpcForRa"
      :npc="activeNpcForRa"
      @close="showVisorRaModal = false"
      @complete="(r: { cobre: number; oro?: number }) => { onMissionComplete(r, activeNpcForRa?.zona_id); showVisorRaModal = false }"
    />

    <aside class="panel-zonas">
      <div class="panel-header-gaming">
        <span class="icon">📍</span>
        <div>
          <h3>LotaStops Patrimoniales</h3>
          <span class="subtext">{{ zonas.length }} Lugares de Interés Histórico</span>
        </div>
      </div>
      <div class="zonas-list-scroll">
        <div
          v-for="z in zonas"
          :key="z.id"
          class="zona-card-gaming"
          @click="teleportAZona(z)"
        >
          <div class="zona-info">
            <span class="zona-badge">LotaStop</span>
            <h4 class="zona-title">{{ z.name }}</h4>
          </div>
          <button class="btn-play-zona">EXPLORAR ▶</button>
        </div>
      </div>
    </aside>

    <!-- Controles Flotantes de Zoom y Cámara -->
    <div class="map-controls-floating">
      <button class="btn-map-control" title="Acercar Cámara (+)" @click="zoomIn">➕</button>
      <button class="btn-map-control" title="Alejar Cámara (-)" @click="zoomOut">➖</button>
      <button class="btn-map-control btn-center-player" title="Centrar en Jugador" @click="centrarEnJugador">🎯</button>
    </div>
  </div>
</template>

<style scoped>
.map-controls-floating {
  position: absolute;
  top: 4.5rem;
  right: 1rem;
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 15;
}

.btn-map-control {
  width: 38px;
  height: 38px;
  background: rgba(22, 27, 34, 0.92);
  border: 1.5px solid #30363d;
  color: #3fe6c0;
  border-radius: 8px;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(8px);
  transition: all 0.2s ease;
}

.btn-map-control:hover {
  background: #3fe6c0;
  color: #0f1216;
  border-color: #3fe6c0;
  transform: scale(1.08);
}

.btn-center-player {
  border-color: #f5a285;
  color: #f5a285;
}

.btn-center-player:hover {
  background: #f5a285;
  color: #0f1216;
  border-color: #f5a285;
}

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

.banner-intercepcion {
  background: linear-gradient(135deg, #d17a4f 0%, #f5a285 100%);
  color: #0f1216;
  border: 2px solid #fff;
  cursor: pointer;
  pointer-events: auto;
  font-weight: 800;
  animation: pulseGlow 1.8s infinite alternate ease-in-out;
  box-shadow: 0 4px 20px rgba(209, 122, 79, 0.7);
}

@keyframes pulseGlow {
  0% { transform: translateX(-50%) scale(1); }
  100% { transform: translateX(-50%) scale(1.04); }
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
  background: rgba(13, 17, 23, 0.92);
  backdrop-filter: blur(12px);
  border: 2px solid #c87d55;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.8);
  color: #c9d1d9;
}

.panel-zona {
  right: 1rem;
  bottom: 2rem;
  width: 300px;
}

.panel-zonas {
  left: 1rem;
  top: 5rem;
  width: 295px;
  max-height: calc(100vh - 7rem);
  display: flex;
  flex-direction: column;
}

.panel-header-gaming {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #30363d;
}

.panel-header-gaming .icon {
  font-size: 20px;
}

.panel-header-gaming h3 {
  font-size: 0.95rem;
  color: #3FE6C0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.panel-header-gaming .subtext {
  font-size: 0.7rem;
  color: #8b949e;
  display: block;
}

.zonas-list-scroll {
  overflow-y: auto;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-right: 4px;
}

.zona-card-gaming {
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 8px;
  padding: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  transition: all 0.2s ease;
}

.zona-card-gaming:hover {
  border-color: #3FE6C0;
  background: rgba(63, 230, 192, 0.08);
  transform: translateX(3px);
}

.zona-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.zona-badge {
  font-size: 0.65rem;
  font-family: monospace;
  color: #d4af37;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.zona-title {
  font-size: 0.82rem;
  color: #f0f4f9;
  font-weight: 600;
}

.btn-play-zona {
  background: #c87d55;
  color: #000;
  border: none;
  font-family: monospace;
  font-size: 0.7rem;
  font-weight: bold;
  padding: 6px 10px;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.15s;
  white-space: nowrap;
}

.zona-card-gaming:hover .btn-play-zona {
  background: #3FE6C0;
  color: #000;
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
