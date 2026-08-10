<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { Map, NavigationControl, Marker, Popup } from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'

// Coordenadas de las 5 zonas patrimoniales del piloto
const ZONAS = [
  { id: 1, nombre: 'Chiflón del Diablo', lng: -72.99, lat: -37.15, desc: 'Mina de carbón, Monumento Nacional' },
  { id: 2, nombre: 'Parque de Lota', lng: -73.01, lat: -37.09, desc: 'Parque Isidora Cousiño' },
  { id: 3, nombre: 'Pabellón 83', lng: -73.00, lat: -37.14, desc: 'Arquitectura industrial obrera' },
  { id: 4, nombre: 'Teatro de Lota', lng: -73.01, lat: -37.10, desc: 'Patrimonio cultural urbano' },
  { id: 5, nombre: 'Costa / Oficios de Mar', lng: -73.02, lat: -37.11, desc: 'Patrimonio inmaterial del borde mar' },
]

const mapContainer = ref<HTMLElement | null>(null)
const zonaSeleccionada = ref<number | null>(null)
let map: Map | null = null

onMounted(() => {
  if (!mapContainer.value) return

  map = new Map({
    container: mapContainer.value,
    // Estilo básico sin necesidad de API key (OSM raster)
    style: {
      version: 8,
      sources: {
        osm: {
          type: 'raster',
          tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
          tileSize: 256,
          attribution: '© OpenStreetMap',
        },
      },
      layers: [
        {
          id: 'osm-tiles',
          type: 'raster',
          source: 'osm',
        },
      ],
    },
    center: [-73.01, -37.12], // Centro de Lota
    zoom: 13,
  })

  map.addControl(new NavigationControl(), 'top-right')

  map.on('load', () => {
    // Agregar marcadores por cada zona
    ZONAS.forEach((zona) => {
      const marker = new Marker({ color: '#3FE6C0' })
        .setLngLat([zona.lng, zona.lat])
        .setPopup(
          new Popup({ offset: 25 }).setHTML(
            `<h3>${zona.nombre}</h3><p>${zona.desc}</p>`
          )
        )
        .addTo(map!)

      marker.getElement().addEventListener('click', () => {
        zonaSeleccionada.value = zona.id
      })
    })
  })
})

onUnmounted(() => {
  map?.remove()
})
</script>

<template>
  <div class="mapa-container">
    <div ref="mapContainer" class="mapa"></div>
    <aside v-if="zonaSeleccionada" class="panel-zona">
      <button class="cerrar" @click="zonaSeleccionada = null">✕</button>
      <h2>{{ ZONAS.find(z => z.id === zonaSeleccionada)?.nombre }}</h2>
      <p>{{ ZONAS.find(z => z.id === zonaSeleccionada)?.desc }}</p>
      <p class="hint">Misión del piloto: próximamente</p>
    </aside>
  </div>
</template>

<style scoped>
.mapa-container {
  flex: 1;
  position: relative;
  display: flex;
}

.mapa {
  flex: 1;
  height: 100%;
}

.panel-zona {
  position: absolute;
  right: 1rem;
  bottom: 2rem;
  width: 280px;
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}

.panel-zona h2 {
  font-size: 1.1rem;
  color: #3FE6C0;
  margin-bottom: 0.5rem;
}

.panel-zona p {
  font-size: 0.85rem;
  color: #8b949e;
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
