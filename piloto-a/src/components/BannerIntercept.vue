<script setup lang="ts">
/**
 * BannerIntercept — Banner persistente que anuncia cuando un NPC está
 * "EN EL RANGO". Emite vibración háptica opcional (navigator.vibrate).
 */
import { onMounted } from 'vue'

const props = withDefaults(
  defineProps<{
    npcName: string
    distanceMeters?: number
  }>(),
  { distanceMeters: 0 }
)

defineEmits<{
  (e: 'open'): void
}>()

function tryVibrate() {
  if (typeof navigator !== 'undefined' && typeof navigator.vibrate === 'function') {
    try {
      navigator.vibrate(120)
    } catch {
      // ignore
    }
  }
}

onMounted(() => {
  tryVibrate()
})
</script>

<template>
  <button
    class="banner-intercept"
    type="button"
    @click="$emit('open')"
    :aria-label="`NPC ${npcName} en rango, abrir encuentro`"
  >
    <span class="halo" aria-hidden="true"></span>
    <span class="content">
      <span class="dot"></span>
      <span class="title">EN EL RANGO · {{ npcName }}</span>
      <span v-if="distanceMeters > 0" class="dist">{{ Math.round(distanceMeters) }} m</span>
      <span class="cta">ABRIR ENCUENTRO ▶</span>
    </span>
  </button>
</template>

<style scoped>
.banner-intercept {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 10px 18px;
  background: linear-gradient(135deg, var(--lota-copper, #c87d55) 0%, var(--lota-gold, #D4AF37) 100%);
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-radius: var(--lota-radius-pill, 999px);
  color: #10131a;
  font-family: var(--lota-font-sans, "Space Grotesk", sans-serif);
  font-size: 12px;
  letter-spacing: 1.2px;
  text-transform: uppercase;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 8px 28px rgba(212, 175, 55, 0.45);
  overflow: hidden;
}

.halo {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 30% 50%, rgba(255, 255, 255, 0.4), transparent 60%);
  animation: halo-shimmer 2s ease-in-out infinite;
  pointer-events: none;
}

@keyframes halo-shimmer {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}

.content {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10131a;
  animation: blink 1.1s infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.title {
  font-weight: 800;
}

.dist {
  font-family: var(--lota-font-mono, "JetBrains Mono", monospace);
  font-size: 11px;
  opacity: 0.85;
}

.cta {
  font-size: 11px;
  letter-spacing: 1.5px;
  background: #10131a;
  color: var(--lota-gold, #D4AF37);
  padding: 4px 8px;
  border-radius: 4px;
}

@media (prefers-reduced-motion: reduce) {
  .halo, .dot {
    animation: none;
  }
}
</style>
