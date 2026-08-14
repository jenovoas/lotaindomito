<script setup lang="ts">
/**
 * EncuentroSheet — Modal "ficha de colección" del NPC.
 * Sustituye al flujo "tap marker → Visor RA" cuando el jugador aún no
 * ha decidido iniciar el encuentro.
 */
import NpcAvatar from './NpcAvatar.vue'

defineProps<{
  npc: {
    npcId: string
    name: string
    avatar?: string
    historia?: string
    estado?: string
  }
  /** epíteto histórico mostrado bajo el nombre */
  epiteto?: string
  /** texto del CTA principal */
  ctaLabel?: string
  /** progreso de la micro-sesión 0..1 */
  progress?: number
}>()

defineEmits<{
  (e: 'close'): void
  (e: 'iniciar'): void
}>()
</script>

<template>
  <div class="sheet-backdrop" @click.self="$emit('close')">
    <div class="sheet" role="dialog" aria-modal="true">
      <button class="cerrar" @click="$emit('close')" aria-label="Cerrar ficha">✕</button>

      <div class="portrait">
        <NpcAvatar :npc-id="npc.npcId" :size="120" :halo="true" />
      </div>

      <div class="meta">
        <span class="tag">PERSONAJE HISTÓRICO</span>
        <h2 class="name">{{ npc.name }}</h2>
        <span v-if="epiteto" class="epiteto">{{ epiteto }}</span>

        <p class="historia">
          {{ npc.historia || 'Fragmento narrativo en preparación.' }}
        </p>

        <div v-if="typeof progress === 'number'" class="progress-bar" :aria-valuenow="Math.round(progress * 100)">
          <span class="progress-fill" :style="{ width: Math.round(progress * 100) + '%' }"></span>
        </div>

        <div class="actions">
          <button class="btn btn-ghost" @click="$emit('close')">Más tarde</button>
          <button class="btn btn-primary" @click="$emit('iniciar')">{{ ctaLabel || 'Iniciar Encuentro' }} ▶</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sheet-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(7, 8, 11, 0.65);
  backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fade 0.25s var(--lota-ease-out, ease-out);
}

.sheet {
  position: relative;
  width: min(540px, 92vw);
  background: var(--lota-glass-bg-strong, rgba(10,12,16,0.92));
  border: 2px solid var(--lota-copper, #c87d55);
  border-radius: var(--lota-radius-lg, 16px);
  padding: 28px;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.7),
              inset 0 1px 0 rgba(255, 255, 255, 0.04);
  display: grid;
  grid-template-columns: 140px 1fr;
  gap: 22px;
  animation: slide-down 0.3s var(--lota-ease-out, ease-out);
}

@media (max-width: 540px) {
  .sheet {
    grid-template-columns: 1fr;
    text-align: center;
    padding: 22px;
  }
  .portrait {
    display: flex;
    justify-content: center;
  }
}

.cerrar {
  position: absolute;
  top: 12px;
  right: 12px;
  background: transparent;
  border: 1px solid var(--lota-line, #1e2634);
  color: var(--lota-text-muted, #a0aec0);
  width: 32px;
  height: 32px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}

.cerrar:hover {
  color: var(--lota-gold, #D4AF37);
  border-color: var(--lota-gold, #D4AF37);
}

.portrait {
  display: flex;
  align-items: flex-start;
  justify-content: center;
}

.meta {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.tag {
  font-family: var(--lota-font-mono, "JetBrains Mono", monospace);
  font-size: 10px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--lota-gold, #D4AF37);
  border: 1px solid rgba(212, 175, 55, 0.3);
  padding: 4px 8px;
  border-radius: 4px;
  align-self: flex-start;
}

.name {
  font-family: var(--lota-font-sans, "Space Grotesk", sans-serif);
  font-size: 24px;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: var(--lota-text, #f0f4f9);
  margin: 0;
  line-height: 1.1;
}

.epiteto {
  font-family: var(--lota-font-sans, "Space Grotesk", sans-serif);
  font-size: 12px;
  letter-spacing: 2px;
  color: var(--lota-teal, #65dabc);
  text-transform: uppercase;
}

.historia {
  font-family: var(--lota-font-sans, "Space Grotesk", sans-serif);
  font-size: 14px;
  line-height: 1.5;
  color: var(--lota-text-muted, #a0aec0);
}

.progress-bar {
  height: 6px;
  background: var(--lota-bg-3, #161c26);
  border: 1px solid var(--lota-line, #1e2634);
  border-radius: 3px;
  overflow: hidden;
  margin-top: 6px;
}

.progress-fill {
  display: block;
  height: 100%;
  background: linear-gradient(90deg, var(--lota-teal, #65dabc), var(--lota-gold, #D4AF37));
  transition: width 0.3s var(--lota-ease-out, ease-out);
}

.actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
  justify-content: flex-end;
  flex-wrap: wrap;
}

.btn {
  font-family: var(--lota-font-sans, "Space Grotesk", sans-serif);
  font-weight: 700;
  font-size: 13px;
  letter-spacing: 1px;
  text-transform: uppercase;
  padding: 10px 18px;
  border-radius: 8px;
  cursor: pointer;
  border: none;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.btn:hover {
  transform: translateY(-2px);
}

.btn-primary {
  background: var(--lota-gold, #D4AF37);
  color: #10131a;
  box-shadow: 0 6px 22px rgba(212, 175, 55, 0.3);
}

.btn-primary:hover {
  box-shadow: 0 10px 30px rgba(212, 175, 55, 0.45);
}

.btn-ghost {
  background: transparent;
  color: var(--lota-text-muted, #a0aec0);
  border: 1px solid var(--lota-line, #1e2634);
}

.btn-ghost:hover {
  color: var(--lota-teal, #65dabc);
  border-color: var(--lota-teal, #65dabc);
}

@keyframes fade {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slide-down {
  from { opacity: 0; transform: translateY(-30px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (prefers-reduced-motion: reduce) {
  .sheet-backdrop, .sheet {
    animation: none;
  }
}
</style>
