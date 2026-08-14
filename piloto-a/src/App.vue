<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import MapaLota from './components/MapaLota.vue'
import WalletHUD from './components/WalletHUD.vue'
import MochilaMinera from './components/MochilaMinera.vue'
import { useAnalyticsStore } from './stores/analytics'
import { useInventoryStore } from './stores/inventory'

const analytics = useAnalyticsStore()
const inventory = useInventoryStore()
const showMochilaModal = ref(false)

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
        <div class="brand-group">
          <h1 class="titulo">Lota Indómito</h1>
          <p class="subtitulo">Guardianes de la Cuenca — Piloto A</p>
        </div>

        <div class="hud-actions">
          <WalletHUD />
          <button class="btn-mochila" @click="showMochilaModal = true">
            <span>🎒 Mochila</span>
            <span class="badge-count">{{ inventory.items.length }}</span>
          </button>
        </div>
      </div>

      <!-- Toast Flotante de Ítems Obtenidos -->
      <transition name="toast-slide">
        <div v-if="inventory.lastAcquiredItem" class="item-toast">
          <span class="toast-sparkle">✨</span>
          <span>¡Nuevo ítem: <strong>{{ inventory.lastAcquiredItem.icon }} {{ inventory.lastAcquiredItem.name }}</strong>!</span>
        </div>
      </transition>
    </header>

    <div class="mapa-wrapper">
      <MapaLota />
    </div>

    <!-- Modal de Mochila Minera & Bitácora -->
    <MochilaMinera
      v-if="showMochilaModal"
      @close="showMochilaModal = false"
    />

    <footer class="pie-pagina">
      <div class="pie-content">
        <span class="pie-tech">
          Impulsado por tecnología
          <a href="https://www.pinguinoseguro.cl" target="_blank" rel="noopener noreferrer" class="pie-link">Sentinel®</a>
          y
          <a href="https://www.pinguinoseguro.cl" target="_blank" rel="noopener noreferrer" class="pie-link">Sentinel-Cortex®</a>
        </span>
        <span class="pie-sep">•</span>
        <span class="pie-copy">
          © 2026 <strong>Pinguino Seguro SpA</strong>. Todos los derechos reservados.
        </span>
        <span class="pie-sep">•</span>
        <a href="https://www.pinguinoseguro.cl" target="_blank" rel="noopener noreferrer" class="pie-web">www.pinguinoseguro.cl</a>
      </div>
    </footer>
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
  font-family: var(--lota-font-sans, system-ui, sans-serif);
  background: var(--lota-bg, #0d1117);
  color: var(--lota-text, #e6edf3);
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
  background: var(--lota-bg-2, #161b22);
  border-bottom: 1px solid var(--lota-line-strong, #30363d);
  position: relative;
}

.header-main {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.4rem 1rem;
  flex-wrap: wrap;
  gap: 10px;
}

.brand-group {
  display: flex;
  flex-direction: column;
}

.titulo {
  font-family: var(--lota-font-sans, "Space Grotesk", sans-serif);
  font-size: 1.3rem;
  font-weight: 700;
  letter-spacing: var(--lota-tracking-title, 1.5px);
  text-transform: uppercase;
  color: var(--lota-teal, #3fe6c0);
  padding: 0;
  line-height: 1.1;
}

.subtitulo {
  font-family: var(--lota-font-mono, "JetBrains Mono", monospace);
  font-size: 0.75rem;
  letter-spacing: var(--lota-tracking-mono, 2.5px);
  color: var(--lota-text-muted, #8b949e);
  padding: 0;
  margin-top: 2px;
}

.hud-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn-mochila {
  background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
  border: 1.5px solid var(--lota-copper, #d17a4f);
  color: var(--lota-text, #f1f5f9);
  padding: 6px 14px;
  border-radius: var(--lota-radius-pill, 20px);
  font-family: var(--lota-font-sans, "Space Grotesk", sans-serif);
  font-weight: 700;
  font-size: 0.85rem;
  letter-spacing: var(--lota-tracking-cta, 1px);
  text-transform: uppercase;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 2px 10px rgba(209, 122, 79, 0.25);
  transition: transform var(--lota-duration-fast, 150ms) var(--lota-ease-out, ease),
              box-shadow var(--lota-duration-fast, 150ms) var(--lota-ease-out, ease);
}

.btn-mochila:hover {
  border-color: var(--lota-teal, #3fe6c0);
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(63, 230, 192, 0.3);
}

.badge-count {
  background: var(--lota-copper, #d17a4f);
  color: var(--lota-bg, #0f1216);
  font-family: var(--lota-font-mono, "JetBrains Mono", monospace);
  font-size: 0.7rem;
  font-weight: 800;
  padding: 1px 6px;
  border-radius: 10px;
}

.item-toast {
  position: absolute;
  top: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%);
  background: rgba(15, 23, 42, 0.95);
  border: 1.5px solid var(--lota-gold, #ffd700);
  color: var(--lota-gold, #ffd700);
  padding: 8px 18px;
  border-radius: var(--lota-radius-pill, 20px);
  font-family: var(--lota-font-sans, "Space Grotesk", sans-serif);
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: var(--lota-tracking-cta, 1px);
  text-transform: uppercase;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
  z-index: 999;
  backdrop-filter: var(--lota-glass-blur, blur(10px));
}

.toast-slide-enter-active, .toast-slide-leave-active {
  transition: opacity var(--lota-duration-base, 250ms) ease,
              transform var(--lota-duration-base, 250ms) ease;
}
.toast-slide-enter-from, .toast-slide-leave-to {
  opacity: 0;
  transform: translate(-50%, -10px);
}

.pie-pagina {
  flex-shrink: 0;
  background: var(--lota-bg, #0d1117);
  border-top: 1px solid var(--lota-line, #21262d);
  padding: 0.55rem 1rem;
  font-size: 0.72rem;
  color: var(--lota-text-muted, #8b949e);
  z-index: 10;
}

.pie-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  flex-wrap: wrap;
  text-align: center;
  max-width: 1200px;
  margin: 0 auto;
}

.pie-link {
  color: var(--lota-teal, #3FE6C0);
  text-decoration: none;
  font-weight: 600;
  transition: color var(--lota-duration-fast, 150ms) ease;
}

.pie-link:hover {
  color: var(--lota-teal-bright, #58a6ff);
  text-decoration: underline;
}

.pie-web {
  color: #d2a8ff;
  text-decoration: none;
  font-weight: 500;
}

.pie-web:hover {
  text-decoration: underline;
}

.pie-sep {
  color: var(--lota-line-strong, #30363d);
}

@media (prefers-reduced-motion: reduce) {
  .btn-mochila,
  .item-toast,
  .toast-slide-enter-active,
  .toast-slide-leave-active {
    transition: none;
  }
}
</style>
