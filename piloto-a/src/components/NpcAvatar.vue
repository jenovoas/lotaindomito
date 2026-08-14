<script setup lang="ts">
/**
 * NpcAvatar — Retrato SVG 2.5D estilizado para los NPCs del enjambre SOMA.
 *
 * Tres capas: silueta (path), iluminación (gradiente) y detalle vestimenta.
 * Determinístico: dado el mismo `npcId`, siempre se pinta el mismo retrato.
 * Cero dependencia de red, cero costo de batería en móvil.
 */
import { computed } from 'vue'

type NpcId = 'isidora' | 'ciego' | 'chinchorrera' | 'palanquero'

const props = withDefaults(
  defineProps<{
    npcId: string
    size?: number
    /** muestra halo animado (false en perfil lite) */
    halo?: boolean
    /** anillo "EN EL RANGO" para intercepción */
    intercept?: boolean
    name?: string
  }>(),
  {
    size: 64,
    halo: true,
    intercept: false,
    name: '',
  }
)

const isKnown = computed<NpcId | null>(() => {
  const id = props.npcId.toLowerCase()
  if (['isidora', 'isidora_goyenechea', 'dama_carbon'].includes(id)) return 'isidora'
  if (['ciego', 'ciego_mina'].includes(id)) return 'ciego'
  if (['chinchorrera', 'chinchorrera_mayor'].includes(id)) return 'chinchorrera'
  if (['palanquero'].includes(id)) return 'palanquero'
  return null
})
</script>

<template>
  <div
    class="npc-avatar"
    :class="{ 'with-halo': halo, intercept, lite: !halo }"
    :style="{ width: size + 'px', height: size + 'px' }"
    :title="name || npcId"
  >
    <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <defs>
        <radialGradient :id="`g-bg-${npcId}`" cx="50%" cy="40%" r="65%">
          <stop offset="0%" stop-color="rgba(212, 175, 55, 0.35)" />
          <stop offset="60%" stop-color="rgba(101, 218, 188, 0.15)" />
          <stop offset="100%" stop-color="rgba(7, 8, 11, 0.85)" />
        </radialGradient>
        <linearGradient :id="`g-skin-${npcId}`" x1="0" x2="1" y1="0" y2="1">
          <stop offset="0%" stop-color="#f6d6a0" />
          <stop offset="100%" stop-color="#a06d3f" />
        </linearGradient>
        <linearGradient :id="`g-cloth-${npcId}`" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stop-color="#65dabc" />
          <stop offset="100%" stop-color="#2A9D8F" />
        </linearGradient>
      </defs>

      <!-- Marco hexagonal (ficha de colección) -->
      <polygon
        points="50,4 92,28 92,72 50,96 8,72 8,28"
        :fill="`url(#g-bg-${npcId})`"
        stroke="rgba(212,175,55,0.6)"
        stroke-width="2"
      />

      <!-- ISIDORA: dama del carbón, peinado alto, vestido turquesa -->
      <g v-if="isKnown === 'isidora'">
        <ellipse cx="50" cy="78" rx="22" ry="6" fill="#0f131a" />
        <path d="M28 78 Q30 56 50 54 Q70 56 72 78 Z" :fill="`url(#g-cloth-${npcId})`" />
        <path d="M30 78 Q34 70 50 68 Q66 70 70 78" fill="rgba(212,175,55,0.4)" />
        <circle cx="50" cy="42" r="13" :fill="`url(#g-skin-${npcId})`" />
        <path d="M37 38 Q40 26 50 26 Q60 26 63 38 L60 42 Q50 36 40 42 Z" fill="#1e2634" />
        <circle cx="45" cy="42" r="1.5" fill="#0f131a" />
        <circle cx="55" cy="42" r="1.5" fill="#0f131a" />
        <path d="M44 50 Q50 53 56 50" stroke="#1e2634" stroke-width="1.5" fill="none" />
        <path d="M50 54 L50 62" stroke="rgba(212,175,55,0.55)" stroke-width="1.2" />
      </g>

      <!-- CIEGO: lámpara Davy, silueta en sombra -->
      <g v-else-if="isKnown === 'ciego'">
        <ellipse cx="50" cy="80" rx="22" ry="6" fill="#0f131a" />
        <path d="M28 80 Q30 56 50 54 Q70 56 72 80 Z" fill="#1e2634" />
        <circle cx="50" cy="42" r="13" fill="#0f131a" />
        <!-- lámpara en la frente -->
        <rect x="42" y="32" width="16" height="6" rx="1.5" fill="rgba(212,175,55,0.7)" />
        <circle cx="50" cy="46" r="3" fill="rgba(244,162,97,0.9)" />
        <!-- ojos vendados -->
        <rect x="40" y="40" width="20" height="3" fill="#0f131a" />
        <path d="M30 64 L70 64" stroke="rgba(212,175,55,0.4)" stroke-width="1" />
      </g>

      <!-- CHINCHORRERA: chaleco colorido, aretes -->
      <g v-else-if="isKnown === 'chinchorrera'">
        <ellipse cx="50" cy="80" rx="22" ry="6" fill="#0f131a" />
        <path d="M28 80 Q30 54 50 52 Q70 54 72 80 Z" fill="#E76F51" />
        <!-- delantal turquesa -->
        <path d="M34 80 Q38 64 50 62 Q62 64 66 80 Z" fill="#65dabc" opacity="0.85" />
        <circle cx="50" cy="42" r="13" :fill="`url(#g-skin-${npcId})`" />
        <!-- pelo recogido con pañuelo -->
        <path d="M37 38 Q40 24 50 24 Q60 24 63 38 L60 40 Q50 32 40 40 Z" fill="#F4A261" />
        <circle cx="44" cy="44" r="1.5" fill="#0f131a" />
        <circle cx="56" cy="44" r="1.5" fill="#0f131a" />
        <circle cx="38" cy="50" r="2" fill="#D4AF37" />
        <circle cx="62" cy="50" r="2" fill="#D4AF37" />
        <!-- flores en el pelo -->
        <circle cx="42" cy="30" r="2.5" fill="#F4A261" />
        <circle cx="58" cy="30" r="2.5" fill="#E76F51" />
      </g>

      <!-- PALANQUERO: silueta robusta, garrucha -->
      <g v-else-if="isKnown === 'palanquero'">
        <ellipse cx="50" cy="80" rx="24" ry="6" fill="#0f131a" />
        <path d="M26 80 Q28 52 50 50 Q72 52 74 80 Z" fill="#1e2634" />
        <circle cx="50" cy="40" r="14" :fill="`url(#g-skin-${npcId})`" />
        <!-- casco -->
        <path d="M34 34 Q40 22 50 22 Q60 22 66 34 L62 36 Q50 30 38 36 Z" fill="#2c3546" />
        <rect x="34" y="34" width="32" height="3" fill="rgba(212,175,55,0.6)" />
        <circle cx="45" cy="42" r="1.5" fill="#0f131a" />
        <circle cx="55" cy="42" r="1.5" fill="#0f131a" />
        <!-- garrucha al hombro -->
        <rect x="68" y="38" width="6" height="22" fill="#0f131a" stroke="rgba(212,175,55,0.5)" stroke-width="1" />
        <circle cx="71" cy="36" r="3" fill="rgba(244,162,97,0.8)" />
      </g>

      <!-- Fallback genérico (NPC desconocido) -->
      <g v-else>
        <circle cx="50" cy="42" r="13" :fill="`url(#g-skin-${npcId})`" />
        <path d="M28 80 Q30 56 50 54 Q70 56 72 80 Z" fill="#556072" />
        <circle cx="45" cy="42" r="1.5" fill="#0f131a" />
        <circle cx="55" cy="42" r="1.5" fill="#0f131a" />
        <text x="50" y="68" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="9" fill="rgba(212,175,55,0.7)">NPC</text>
      </g>

      <!-- Bisel interior carbón -->
      <polygon
        points="50,4 92,28 92,72 50,96 8,72 8,28"
        fill="none"
        stroke="rgba(0,0,0,0.55)"
        stroke-width="1"
        stroke-dasharray="2 4"
        opacity="0.5"
      />
    </svg>

    <span v-if="intercept" class="ring intercept-ring" aria-hidden="true"></span>
    <span v-if="name && !intercept" class="caption">{{ name }}</span>
    <span v-if="intercept && name" class="caption intercept-caption">EN EL RANGO · {{ name }}</span>
  </div>
</template>

<style scoped>
.npc-avatar {
  position: relative;
  display: inline-block;
  filter: drop-shadow(0 6px 14px rgba(0, 0, 0, 0.7));
}

.npc-avatar svg {
  width: 100%;
  height: 100%;
  display: block;
}

.npc-avatar.with-halo::before {
  content: "";
  position: absolute;
  inset: -8%;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.35) 0%, transparent 70%);
  animation: halo-pulse 1.5s ease-in-out infinite;
  pointer-events: none;
  z-index: -1;
}

.npc-avatar.lite::before {
  display: none;
}

@keyframes halo-pulse {
  0%, 100% { opacity: 0.7; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.06); }
}

.ring {
  position: absolute;
  inset: -4px;
  border: 2px solid rgba(212, 175, 55, 0.85);
  border-radius: 18%;
  pointer-events: none;
}

.intercept-ring {
  animation: intercept-pulse 1.2s ease-in-out infinite;
}

@keyframes intercept-pulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 0 12px rgba(212, 175, 55, 0.6);
  }
  50% {
    transform: scale(1.08);
    box-shadow: 0 0 28px rgba(212, 175, 55, 0.95);
  }
}

.caption {
  position: absolute;
  left: 50%;
  bottom: -22px;
  transform: translateX(-50%);
  font-family: var(--lota-font-mono, "JetBrains Mono", monospace);
  font-size: 10px;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: var(--lota-teal, #65dabc);
  white-space: nowrap;
  text-shadow: 0 1px 4px rgba(0, 0, 0, 0.85);
}

.intercept-caption {
  color: var(--lota-gold, #D4AF37);
  font-weight: 700;
  bottom: -22px;
}

@media (prefers-reduced-motion: reduce) {
  .npc-avatar.with-halo::before,
  .intercept-ring {
    animation: none;
  }
}
</style>
