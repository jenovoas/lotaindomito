<script setup lang="ts">
/**
 * EncuentroPulso — Anillo de pulso luminoso en el centroide de la zona.
 * Tres anillos concéntricos que se expanden desde r=0 hasta ~80 m en 2s.
 * Se dispara una sola vez por entrada (controlado por prop visible).
 *
 * En perfil 'lite' se renderiza un único anillo para mantener FPS.
 */
import { computed } from 'vue'
import { useGraphicsProfile } from '@/composables/useGraphicsProfile'

const props = withDefaults(
  defineProps<{
    visible: boolean
  }>(),
  { visible: false }
)

const graphics = useGraphicsProfile()
const ringCount = computed(() => (graphics.profile === 'lite' ? 1 : 3))
</script>

<template>
  <div v-if="visible" class="pulso-overlay" aria-hidden="true">
    <span
      v-for="i in ringCount"
      :key="i"
      class="ring"
      :style="{ animationDelay: (i - 1) * 0.3 + 's' }"
    ></span>
  </div>
</template>

<style scoped>
.pulso-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  z-index: 8;
}

.ring {
  position: absolute;
  width: 80px;
  height: 80px;
  border: 2px solid rgba(212, 175, 55, 0.85);
  border-radius: 50%;
  animation: ring-expand 2s ease-out forwards;
  box-shadow: 0 0 24px rgba(212, 175, 55, 0.45);
}

@keyframes ring-expand {
  0% {
    width: 80px;
    height: 80px;
    opacity: 0.9;
    border-width: 3px;
  }
  100% {
    width: 280px;
    height: 280px;
    opacity: 0;
    border-width: 1px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .ring {
    animation: none;
    width: 200px;
    height: 200px;
    opacity: 0.3;
  }
}
</style>
