<script setup lang="ts">
import MapaLota from './components/MapaLota.vue'
</script>

<template>
  <main class="app">
    <h1 class="titulo">Lota Indómito</h1>
    <p class="subtitulo">Guardianes de la Cuenca — Piloto A</p>
    <MapaLota />
  </main>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: system-ui, sans-serif;
  background: #0d1117;
  color: #e6edf3;
}

.app {
  display: flex;
  flex-direction: column;
  height: 100vh;
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
