<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { Map, NavigationControl, Popup, type LngLatLike } from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'
import booleanPointInPolygon from '@turf/boolean-point-in-polygon'
import { point as turfPoint, polygon as turfPolygon } from '@turf/turf'
import zonasData from '../data/zonas-lota.json'
import { useGeofenceStore } from '@/stores/geofence'
import { useGeolocation } from '@/composables/useGeolocation'

interface ZonaOSM {
  id: number
  name: string
  tags: { historic?: string; tourism?: string; leisure?: string; natural?: string }
  coords: Array<{ lat: number; lon: number }>
}

const zonas = (zonasData as { zonas: ZonaOSM[]; count: number; fuente: string }).zonas

const mapContainer = ref<HTMLElement | null>(null)
const geofence = useGeofenceStore()
const { lat, lon, gpsAvailable, isWatching, teleport } = useGeolocation()
let map: Map | null = null

onMounted(() => {
  if (!mapContainer.value) return

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
    center: [-73.16, -37.08],
    zoom: 13,
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

    // Demo de geofencing: promedio de vértices cae dentro del polígono de Chiflón
    const chiflon = zonas.find((z) => z.name.includes('Chiflón'))
    if (chiflon && chiflon.coords.length >= 3) {
      const coords: [number, number][] = chiflon.coords.map((c) => [c.lon, c.lat])
      const poly = turfPolygon([[...coords, coords[0]!]])
      const avgLng = coords.reduce((s, c) => s + c[0], 0) / coords.length
      const avgLat = coords.reduce((s, c) => s + c[1], 0) / coords.length
      const pt = turfPoint([avgLng, avgLat])
      const inside = booleanPointInPolygon(pt, poly)
      console.log(`[geofencing] ${chiflon.name}: promedio de vértices dentro = ${inside}`)
    }

    // Forzar resize tras layout estable
    setTimeout(() => map?.resize(), 100)
  })
})

onUnmounted(() => {
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

    <aside v-if="geofence.zonaActiva" class="panel-zona">
      <button class="cerrar" @click="geofence.zonaActiva = null">✕</button>
      <h2>{{ geofence.zonaActiva.zona_name }}</h2>
      <p class="origen">Origen: OpenStreetMap (Overpass API, 2026-08-10)</p>
      <p class="hint">Geofencing listo — entrando a esta zona se activa la misión.</p>
    </aside>
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
