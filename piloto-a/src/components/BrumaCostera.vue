<script setup lang="ts">
/**
 * BrumaCostera — capa sutil de niebla animada sobre el mapa MapLibre.
 * Implementación 100% CSS: el navegador delega al hilo del compositor
 * sin intervención JS → no roba FPS al render loop.
 *
 * - En perfil 'lite' o 'css-only' se desactiva automáticamente.
 * - En `prefers-reduced-motion` se muestra niebla estática.
 */
import { computed } from 'vue'
import { useGraphicsProfile } from '@/composables/useGraphicsProfile'

const props = withDefaults(
  defineProps<{
    /** densidad relativa (0..1); default 0.6 */
    density?: number
    /** forzar activación ignorando perfil */
    force?: boolean
  }>(),
  { density: 0.6, force: false }
)

const { value: graphics } = useGraphicsProfile()
const enabled = computed(() => props.force || graphics.value.profile === 'full')
const count = computed(() => Math.max(4, Math.floor(14 * props.density)))
</script>

<template>
  <div v-if="enabled" class="bruma-costera" aria-hidden="true">
    <span
      v-for="i in count"
      :key="i"
      class="particle"
      :style="{
        top: (10 + ((i * 13) % 70)) + '%',
        animationDuration: (18 + (i % 5) * 3) + 's',
        animationDelay: -(i * 1.7) + 's',
        width: 120 + (i % 3) * 50 + 'px',
        height: 60 + (i % 4) * 20 + 'px',
        opacity: 0.18 + (i % 3) * 0.05,
      }"
    ></span>
  </div>
</template>

<style scoped>
.bruma-costera {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
  z-index: 5;
  mix-blend-mode: screen;
}

.particle {
  position: absolute;
  left: -200px;
  background: radial-gradient(ellipse at center, rgba(101, 218, 188, 0.5) 0%, transparent 70%);
  border-radius: 50%;
  filter: blur(8px);
  animation: drift linear infinite;
  will-change: transform;
}

@keyframes drift {
  0% { transform: translate3d(0, 0, 0); }
  50% { transform: translate3d(60vw, -12px, 0); }
  100% { transform: translate3d(110vw, 8px, 0); }
}

@media (prefers-reduced-motion: reduce) {
  .particle {
    animation: none;
    left: 30%;
  }
}
</style>
