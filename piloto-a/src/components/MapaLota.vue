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
import { useGameLoop } from '@/composables/useGameLoop'
import { useGraphicsProfile } from '@/composables/useGraphicsProfile'
import { RingBuffer, sampleAt } from '@/utils/interpolationBuffer'
import NpcAvatar from './NpcAvatar.vue'
import BrumaCostera from './BrumaCostera.vue'
import EncuentroPulso from './EncuentroPulso.vue'
import EncuentroSheet from './EncuentroSheet.vue'
import BannerIntercept from './BannerIntercept.vue'
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
const { value: graphics } = useGraphicsProfile()

let map: Map | null = null
let playerMarker: Marker | null = null
let npcMarkers: Map<string, Marker> = new Map()
let npcEventMarker: Marker | null = null
let npcEventInterval: ReturnType<typeof setInterval> | null = null
const playerBuffer = new RingBuffer<{ lat: number; lon: number }>(10)
const npcBuffers: Map<string, RingBuffer<{ lat: number; lon: number }>> = new Map()

const showChiflonModal = ref(false)
const showIsidoraModal = ref(false)
const showPabellonModal = ref(false)
const showVisorRaModal = ref(false)
const showEncuentroSheet = ref(false)
const activeNpcForRa = ref<NpcWire | null>(null)
const showPulso = ref(false)
let pulsoTimer: ReturnType<typeof setTimeout> | null = null

function openVisorRa(npc: NpcWire) {
  activeNpcForRa.value = npc
  showVisorRaModal.value = true
}

function openEncuentroSheet(npc: NpcWire) {
  activeNpcForRa.value = npc
  showEncuentroSheet.value = true
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

function ensureNpcMarker(npc: NpcWire): Marker {
  const existing = npcMarkers.get(npc.npcId || npc.id.toString())
  if (existing) return existing

  const el = document.createElement('div')
  el.className = 'npc-marker-wrapper'

  // El componente Vue se monta sobre el div vía createApp sería más limpio,
  // pero para mantener esta fase sin tocar el runtime de Vue,
  // renderizamos un fallback HTML con clases CSS que luego enriquezca NpcAvatar.
  el.innerHTML = `
    <div class="npc-hex" data-npc-id="${npc.npcId || npc.id}">
      <div class="npc-hex-inner">${npc.avatar || '◈'}</div>
      <div class="npc-name">${npc.name}</div>
    </div>
  `
  el.style.cursor = 'pointer'
  el.addEventListener('click', () => openEncuentroSheet(npc))

  const marker = new Marker({ element: el })
    .setLngLat([s60ToDegrees(npc.lon_s60), s60ToDegrees(npc.lat_s60)])
    .addTo(map!)

  npcMarkers.set(npc.npcId || npc.id.toString(), marker)
  // crea buffer por NPC
  if (!npcBuffers.has(npc.npcId || npc.id.toString())) {
    npcBuffers.set(npc.npcId || npc.id.toString(), new RingBuffer<{ lat: number; lon: number }>(10))
  }
  npcBuffers.get(npc.npcId || npc.id.toString())!.push(
    { lat: s60ToDegrees(npc.lat_s60), lon: s60ToDegrees(npc.lon_s60) },
    performance.now() / 1000
  )
  return marker
}

function rebuildNpcMarkers() {
  // Limpia markers huérfanos
  const keep = new Set(mobsStore.mobsActivos.map(n => n.npcId || n.id.toString()))
  for (const [key, marker] of npcMarkers.entries()) {
    if (!keep.has(key)) {
      marker.remove()
      npcMarkers.delete(key)
      npcBuffers.delete(key)
    }
  }
  for (const npc of mobsStore.mobsActivos) {
    ensureNpcMarker(npc)
  }
}

watch(
  () => mobsStore.mobsActivos,
  () => {
    rebuildNpcMarkers()
  },
  { deep: true }
)

watch(
  () => geofence.zonaActiva,
  (nuevaZona, prev) => {
    if (nuevaZona?.entered && nuevaZona.zona_id) {
      mobsStore.fetchNpcs(nuevaZona.zona_id)
      // Dispara pulso de encuentro solo si cambió de zona
      if (!prev || prev.zona_id !== nuevaZona.zona_id) {
        showPulso.value = true
        if (pulsoTimer) clearTimeout(pulsoTimer)
        pulsoTimer = setTimeout(() => {
          showPulso.value = false
        }, 2000)
      }
    } else {
      mobsStore.clearMobs()
      rebuildNpcMarkers()
    }
  }
)

// Push GPS al buffer cuando cambie
watch([lat, lon], ([newLat, newLon]) => {
  if (newLat && newLon) {
    playerBuffer.push({ lat: newLat, lon: newLon }, performance.now() / 1000)
  }
})

// Game loop: render interpolado de posiciones
useGameLoop(() => {
  const now = performance.now() / 1000
  // Player
  const p = sampleAt(playerBuffer, now, ['lat', 'lon'] as const, 0.15)
  if (p && playerMarker) {
    playerMarker.setLngLat([p.lon, p.lat])
  }
  // NPCs
  for (const [key, buf] of npcBuffers.entries()) {
    const marker = npcMarkers.get(key)
    if (!marker) continue
    const v = sampleAt(buf, now, ['lat', 'lon'] as const, 0.15)
    if (v) marker.setLngLat([v.lon, v.lat])
  }
  // proximidad
  if (lat.value && lon.value) {
    mobsStore.checkProximity(lat.value, lon.value)
  }
})

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

function abrirMision(zonaId: number | null, zonaName?: string | null) {
  const name = zonaName || ''
  if (zonaId) analytics.trackPoiVisit(zonaId, 0)
  if (zonaId === 480338029 || name.includes('Chiflón')) {
    showChiflonModal.value = true
    return
  }
  if (zonaId === 89121388 || name.includes('Isidora')) {
    showIsidoraModal.value = true
    return
  }
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

    map.on('mouseenter', 'zonas-fill', () => {
      if (map) map.getCanvas().style.cursor = 'pointer'
    })
    map.on('mouseleave', 'zonas-fill', () => {
      if (map) map.getCanvas().style.cursor = ''
    })

    const playerEl = document.createElement('div')
    playerEl.className = 'player-marker'
    playerEl.innerHTML = '🚶'
    playerEl.style.fontSize = '1.8rem'
    playerEl.style.filter = 'drop-shadow(0 0 8px #3FE6C0)'

    playerMarker = new Marker({ element: playerEl })
      .setLngLat([lon.value || -73.165, lat.value || -37.089])
      .addTo(map)

    setTimeout(() => map?.resize(), 100)
  })
})

onUnmounted(() => {
  mobsStore.stopPatrolTicker()
  latticeStore.disconnect()
  npcMarkers.forEach((m) => m.remove())
  npcMarkers.clear()
  if (npcEventInterval) clearInterval(npcEventInterval)
  if (npcEventMarker) npcEventMarker.remove()
  if (pulsoTimer) clearTimeout(pulsoTimer)
  map?.remove()
})
</script>

<template>
  <div class="mapa-container">
    <div ref="mapContainer" class="mapa"></div>

    <!-- Bruma costera (full / lite). Desactivada en css-only y prefers-reduced-motion -->
    <BrumaCostera :density="graphics.profile === 'full' ? 0.7 : 0.3" />

    <!-- Pulso de encuentro al entrar a una zona -->
    <EncuentroPulso :visible="showPulso" />

    <!-- Banner NPC interceptado (usa el nuevo BannerIntercept) -->
    <div
      v-if="mobsStore.interceptedNpc && !showVisorRaModal && !showEncuentroSheet"
      class="intercept-anchor"
    >
      <BannerIntercept
        :npc-name="mobsStore.interceptedNpc.name"
        @open="openEncuentroSheet(mobsStore.interceptedNpc!)"
      />
    </div>

    <!-- Banner: GPS no disponible -->
    <div v-else-if="!gpsAvailable" class="banner banner-gps">
      <span class="banner-dot"></span> GPS no disponible, modo manual activado
    </div>

    <!-- Banner: dentro de una zona -->
    <div v-if="geofence.zonaActiva?.entered" class="banner banner-zona">
      Estás en {{ geofence.zonaActiva.zona_name }}
    </div>

    <WorldEventBanner />

    <!-- Indicador de WebSocket Lattice -->
    <div class="status-ws" :class="{ conectado: latticeStore.connected, 'lattice-pausa': latticeStore.isLatticePaused }">
      <span class="lattice-dot"></span>
      LATTICE WS:
      <span v-if="latticeStore.connected">TICK #{{ latticeStore.lastTick ?? '-' }}</span>
      <span v-else-if="latticeStore.connectionStatus === 'reconnecting'">RECONECTANDO…</span>
      <span v-else>LATTICE EN PAUSA</span>
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

    <!-- Ficha coleccionable -->
    <EncuentroSheet
      v-if="showEncuentroSheet && activeNpcForRa"
      :npc="activeNpcForRa"
      :epiteto="activeNpcForRa.estado === 'Approach' ? 'En el rango' : 'A la espera'"
      @close="showEncuentroSheet = false"
      @iniciar="() => { showEncuentroSheet = false; openVisorRa(activeNpcForRa!) }"
    />

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

    <div class="map-controls-floating">
      <button class="btn-map-control" title="Acercar Cámara (+)" @click="zoomIn">➕</button>
      <button class="btn-map-control" title="Alejar Cámara (-)" @click="zoomOut">➖</button>
      <button class="btn-map-control btn-center-player" title="Centrar en Jugador" @click="centrarEnJugador">🎯</button>
    </div>
  </div>
</template>

<style scoped>
/* Sistema de tokens — todos los colores / radios / sombras vienen de design-tokens */
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
  background: var(--lota-glass-bg-strong, rgba(22, 27, 34, 0.92));
  border: 1.5px solid var(--lota-line-strong, #30363d);
  color: var(--lota-teal, #3fe6c0);
  border-radius: var(--lota-radius-sm, 8px);
  font-family: var(--lota-font-sans, "Space Grotesk", sans-serif);
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: var(--lota-shadow-sm, 0 4px 12px rgba(0, 0, 0, 0.5));
  backdrop-filter: var(--lota-glass-blur, blur(8px));
  transition: transform var(--lota-duration-fast, 150ms) var(--lota-ease-out, ease),
              background var(--lota-duration-fast, 150ms) var(--lota-ease-out, ease),
              color var(--lota-duration-fast, 150ms) var(--lota-ease-out, ease);
}

.btn-map-control:hover {
  background: var(--lota-teal, #3fe6c0);
  color: var(--lota-bg, #0f1216);
  border-color: var(--lota-teal, #3fe6c0);
  transform: scale(1.08);
}

.btn-center-player {
  border-color: var(--lota-peach, #f5a285);
  color: var(--lota-peach, #f5a285);
}

.btn-center-player:hover {
  background: var(--lota-peach, #f5a285);
  color: var(--lota-bg, #0f1216);
  border-color: var(--lota-peach, #f5a285);
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
  border-radius: var(--lota-radius-pill, 999px);
  font-family: var(--lota-font-sans, "Space Grotesk", sans-serif);
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 0.6px;
  text-transform: uppercase;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: var(--lota-shadow-sm, 0 4px 12px rgba(0, 0, 0, 0.4));
  z-index: 10;
  pointer-events: none;
}

.banner-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--lota-gold, #D4AF37);
}

.banner-gps {
  background: var(--lota-glass-bg-strong, #161b22);
  border: 1px solid var(--lota-line-strong, #30363d);
  color: var(--lota-text, #e6e9ef);
}

.banner-zona {
  background: var(--lota-teal, #3fe6c0);
  color: var(--lota-bg, #0f1216);
}

.intercept-anchor {
  position: absolute;
  top: 1rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 12;
}

.status-ws {
  position: absolute;
  top: 1rem;
  right: 4rem;
  background: var(--lota-bg-2, #161b22);
  border: 1px solid var(--lota-line-strong, #30363d);
  padding: 0.4rem 0.8rem;
  border-radius: var(--lota-radius-sm, 6px);
  font-family: var(--lota-font-mono, "JetBrains Mono", monospace);
  font-size: 0.72rem;
  letter-spacing: 1px;
  color: var(--lota-text-muted, #8b949e);
  z-index: 10;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.status-ws .lattice-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--lota-coral, #E76F51);
}

.status-ws.conectado {
  color: var(--lota-teal, #3fe6c0);
  border-color: var(--lota-teal, #3fe6c0);
}

.status-ws.conectado .lattice-dot {
  background: var(--lota-teal, #3fe6c0);
  box-shadow: 0 0 8px var(--lota-teal, #3fe6c0);
}

.status-ws.lattice-pausa {
  color: var(--lota-gold, #D4AF37);
  border-color: rgba(212, 175, 55, 0.45);
}

.status-ws.lattice-pausa .lattice-dot {
  background: var(--lota-gold, #D4AF37);
  animation: blink 1.4s infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.35; }
}

.panel-zona,
.panel-zonas {
  position: absolute;
  background: var(--lota-glass-bg-strong, rgba(13, 17, 23, 0.92));
  backdrop-filter: var(--lota-glass-blur, blur(12px));
  border: var(--lota-bisel-border, 2px) solid var(--lota-copper, #c87d55);
  border-radius: var(--lota-radius-lg, 12px);
  padding: 1rem;
  box-shadow: var(--lota-shadow-md, 0 12px 32px rgba(0, 0, 0, 0.8)),
              var(--lota-bisel-inset, inset 0 1px 0 rgba(255, 255, 255, 0.04));
  color: var(--lota-text-muted, #c9d1d9);
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
  border-bottom: 1px solid var(--lota-line-strong, #30363d);
}

.panel-header-gaming .icon {
  font-size: 20px;
}

.panel-header-gaming h3 {
  font-family: var(--lota-font-sans, "Space Grotesk", sans-serif);
  font-size: 0.95rem;
  font-weight: 700;
  letter-spacing: var(--lota-tracking-title, 1.5px);
  text-transform: uppercase;
  color: var(--lota-teal, #3FE6C0);
  margin: 0;
}

.panel-header-gaming .subtext {
  font-family: var(--lota-font-mono, "JetBrains Mono", monospace);
  font-size: 0.7rem;
  color: var(--lota-text-muted, #8b949e);
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
  background: var(--lota-bg-2, #161b22);
  border: 1px solid var(--lota-line-strong, #30363d);
  border-radius: var(--lota-radius-sm, 8px);
  padding: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  transition: transform var(--lota-duration-fast, 150ms) var(--lota-ease-out, ease),
              border-color var(--lota-duration-fast, 150ms) var(--lota-ease-out, ease);
}

.zona-card-gaming:hover {
  border-color: var(--lota-teal, #3FE6C0);
  transform: translateX(3px);
}

.zona-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.zona-badge {
  font-family: var(--lota-font-mono, "JetBrains Mono", monospace);
  font-size: 0.65rem;
  color: var(--lota-gold, #d4af37);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.zona-title {
  font-family: var(--lota-font-sans, "Space Grotesk", sans-serif);
  font-size: 0.82rem;
  color: var(--lota-text, #f0f4f9);
  font-weight: 600;
}

.btn-play-zona {
  background: var(--lota-copper, #c87d55);
  color: var(--lota-bg, #000);
  border: none;
  font-family: var(--lota-font-mono, "JetBrains Mono", monospace);
  font-size: 0.7rem;
  font-weight: bold;
  padding: 6px 10px;
  border-radius: var(--lota-radius-sm, 4px);
  cursor: pointer;
  letter-spacing: 0.5px;
  transition: background var(--lota-duration-fast, 150ms) var(--lota-ease-out, ease);
}

.zona-card-gaming:hover .btn-play-zona {
  background: var(--lota-teal, #3FE6C0);
  color: var(--lota-bg, #000);
}

.panel-zona h2 {
  font-family: var(--lota-font-sans, "Space Grotesk", sans-serif);
  font-size: 1.1rem;
  font-weight: 700;
  letter-spacing: var(--lota-tracking-title, 1.5px);
  text-transform: uppercase;
  color: var(--lota-teal, #3FE6C0);
  margin-bottom: 0.3rem;
}

.panel-zona p {
  font-family: var(--lota-font-sans, "Space Grotesk", sans-serif);
  font-size: 0.85rem;
  color: var(--lota-text-muted, #8b949e);
}

.panel-zona .origen {
  font-size: 0.7rem;
  color: var(--lota-text-dim, #6e7681);
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
  border: 1px solid var(--lota-line, #1e2634);
  color: var(--lota-text-muted, #8b949e);
  cursor: pointer;
  font-size: 1rem;
  width: 28px;
  height: 28px;
  border-radius: var(--lota-radius-sm, 6px);
  transition: color var(--lota-duration-fast, 150ms) var(--lota-ease-out, ease);
}

.cerrar:hover {
  color: var(--lota-gold, #D4AF37);
}

/* Marker NPC fallback (mientras se migra a NpcAvatar real) */
.npc-marker-wrapper .npc-hex {
  width: 56px;
  height: 56px;
  background: linear-gradient(160deg, rgba(212, 175, 55, 0.18), rgba(101, 218, 188, 0.08));
  border: 2px solid var(--lota-gold, #D4AF37);
  clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--lota-teal, #65dabc);
  font-size: 22px;
  font-weight: 700;
  filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.7));
}

.npc-marker-wrapper .npc-name {
  position: absolute;
  bottom: -18px;
  left: 50%;
  transform: translateX(-50%);
  font-family: var(--lota-font-mono, "JetBrains Mono", monospace);
  font-size: 10px;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: var(--lota-teal, #65dabc);
  white-space: nowrap;
  text-shadow: 0 1px 4px rgba(0, 0, 0, 0.85);
}

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.001ms !important;
    transition-duration: 0.001ms !important;
  }
}
</style>
