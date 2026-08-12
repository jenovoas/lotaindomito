<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import MapaLota from './components/MapaLota.vue'
import WalletHUD from './components/WalletHUD.vue'
import { useAnalyticsStore } from './stores/analytics'

const analytics = useAnalyticsStore()

function getOrCreateUserId(): string {
  const key = 'lota_user_id'
  let id = localStorage.getItem(key)
  if (!id) {
    id = crypto.randomUUID()
    localStorage.setItem(key, id)
  }
  return id
}

onMounted(() => {
  analytics.init(getOrCreateUserId())
})

onUnmounted(() => {
  analytics.endSession()
})
</script>

<template>
  <main class="app">
    <header class="cabecera">
      <div class="header-main">
        <div>
          <h1 class="titulo">Lota Indómito</h1>
          <p class="subtitulo">Guardianes de la Cuenca — Piloto A</p>
        </div>
        <WalletHUD />
      </div>
    </header>
    <div class="mapa-wrapper">
      <MapaLota />
    </div>
  </main>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  font-family: system-ui, sans-serif;
  background: #0d1117;
  color: #e6edf3;
}

#app {
  height: 100%;
}

.app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100vw;
}

.mapa-wrapper {
  flex: 1;
  position: relative;
  min-height: 0;
  width: 100%;
}

.cabecera {
  flex-shrink: 0;
}

.titulo {
  font-size: 1.5rem;
  font-weight: 700;
  padding: 0.5rem 1rem;
  color: #3FE6C0;
}

.subtitulo {
  font-size: 0.85rem;
  padding: 0 1rem 0.5rem;
  color: #8b949e;
}
</style>
