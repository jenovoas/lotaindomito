<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'complete', reward: { cobre: number; oro?: number }): void
}>()

const step = ref<'intro' | 'game' | 'reward'>('intro')
const score = ref(0)
const targetRounds = 6
const timeLeft = ref(90)
const beatIndex = ref(0)
let timer: number | null = null

/** Secuencia de QTE de ritmo: cada paso exige una acción en el momento justo. */
const beatPattern: Array<'press' | 'hold' | 'tap'> = [
  'press', 'hold', 'tap', 'press', 'hold', 'tap',
]

function startGame() {
  step.value = 'game'
  score.value = 0
  beatIndex.value = 0
  timeLeft.value = 90
  qtePhase.value = 'press'
  timer = window.setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--
    } else {
      finishGame()
    }
  }, 1000)
}

// Estado del QTE
const qtePhase = ref<'press' | 'hold' | 'tap'>('press')
const holdProgress = ref(0)
const showSuccess = ref(false)
const showMiss = ref(false)
let holdInterval: number | null = null

function advanceBeat() {
  if (holdInterval) clearInterval(holdInterval)
  holdInterval = null
  showSuccess.value = false
  showMiss.value = false
  holdProgress.value = 0

  if (beatIndex.value < targetRounds - 1) {
    beatIndex.value++
    qtePhase.value = beatPattern[beatIndex.value]!
  } else {
    finishGame()
  }
}

function onPress() {
  if (qtePhase.value !== 'press') return
  score.value++
  showSuccess.value = true
  setTimeout(() => advanceBeat(), 500)
}

function onHoldStart() {
  if (qtePhase.value !== 'hold') {
    onMiss()
    return
  }
  clearInterval(holdInterval as number)
  holdInterval = window.setInterval(() => {
    holdProgress.value += 8
    if (holdProgress.value >= 100) {
      score.value++
      showSuccess.value = true
      setTimeout(() => advanceBeat(), 400)
    }
  }, 60)
}

function onTap() {
  if (qtePhase.value !== 'tap') {
    onMiss()
    return
  }
  score.value++
  showSuccess.value = true
  setTimeout(() => advanceBeat(), 400)
}

function onMiss() {
  if (holdInterval) clearInterval(holdInterval)
  holdInterval = null
  showMiss.value = true
  setTimeout(() => advanceBeat(), 400)
}

function finishGame() {
  if (timer) clearInterval(timer)
  if (holdInterval) clearInterval(holdInterval)
  step.value = 'reward'
  emit('complete', { cobre: 40 })
}

onMounted(() => {
  return () => {
    if (timer) clearInterval(timer)
    if (holdInterval) clearInterval(holdInterval)
  }
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
  if (holdInterval) clearInterval(holdInterval)
})
</script>

<template>
  <div class="modal-overlay">
    <div class="modal-card">
      <button class="btn-cerrar" @click="emit('close')">✕</button>

      <!-- TRAMO 2: CONTEXTO -->
      <div v-if="step === 'intro'" class="intro-step">
        <div class="avatar-header">
          <div class="avatar-circle">🥖</div>
          <div>
            <h3>La Chinchorrera y El Palanquero</h3>
            <p class="role">Memoria Social de Lota</p>
          </div>
        </div>
        <p class="dialogo">
          "En estos pabellones se levantó la comunidad carbonera, Explorador. Aquí, amasar pan era el pulso de cada familia. Sigue el ritmo de la mesa para revivir la memoria colectiva del barrio."
        </p>
        <button class="btn-primary" @click="startGame">Comenzar Misión (90s)</button>
      </div>

      <!-- TRAMO 3: ACCIÓN (MINIJUEGO QTE) -->
      <div v-else-if="step === 'game'" class="game-step">
        <div class="game-header">
          <span>Tiempo: <strong>{{ timeLeft }}s</strong></span>
          <span>Pan amasado: <strong>{{ score }}/{{ targetRounds }}</strong></span>
        </div>

        <div class="qte-card" :class="{ pressed: showSuccess, missed: showMiss }">
          <div v-if="qtePhase === 'press'" class="qte-prompt">
            <strong>¡Aprieta!</strong>
            <p>Golpea la masa para el primer pliegue.</p>
          </div>
          <div v-else-if="qtePhase === 'hold'" class="qte-prompt">
            <strong>¡Mantén presionado!</strong>
            <p>Amasa firmemente para integrar la harina.</p>
            <div class="hold-bar"><div class="hold-fill" :style="{ width: holdProgress + '%' }"></div></div>
          </div>
          <div v-else class="qte-prompt">
            <strong>¡Toca rápido!</strong>
            <p>Da palmadas al pan para darle forma.</p>
          </div>

          <div v-if="showSuccess" class="qte-feedback success">✓ ¡Buen ritmo!</div>
          <div v-if="showMiss" class="qte-feedback miss">✕ ¡Se te cayó la masa!</div>
        </div>

        <div class="action-zone">
          <button
            class="btn-qte"
            :class="{ 'is-current': qtePhase === 'press' }"
            @pointerdown="onPress"
            @click="qtePhase === 'press' ? onPress() : null"
          >👊</button>
          <button
            class="btn-qte"
            :class="{ 'is-current': qtePhase === 'hold' }"
            @pointerdown="qtePhase === 'hold' ? onHoldStart() : onMiss()"
          >🖐️</button>
          <button
            class="btn-qte"
            :class="{ 'is-current': qtePhase === 'tap' }"
            @pointerdown="onTap"
          >👏</button>
        </div>
      </div>

      <!-- TRAMO 4 Y 5: RECOMPENSA Y DIRECCIÓN -->
      <div v-else-if="step === 'reward'" class="reward-step">
        <div class="reward-icon">🍞</div>
        <h3>¡Memoria Viva!</h3>
        <p>Has amasado pan como las familias mineras del Pabellón 81.</p>

        <div class="reward-box">
          <span class="mineral">+40 Cobre (Cu) 🟠</span>
          <span class="badge">Insignia: Corazón de Barrio 🏅</span>
          <span class="coupon">🎟️ Cupón QR: 15% desc. en Panadería "El Minero"</span>
        </div>

        <div class="next-poi-box">
          <p class="next-title">📍 Próximo Destino Recomendado:</p>
          <p class="next-desc">Centro Histórico Isidora Cousiño. Tu Cobre ya vale en el comercio local de Lota Alto.</p>
        </div>

        <button class="btn-primary" @click="emit('close')">Volver al Mapa</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  padding: 1rem;
}

.modal-card {
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 12px;
  width: 100%;
  max-width: 440px;
  padding: 1.5rem;
  position: relative;
  color: #e6edf3;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
}

.btn-cerrar {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: transparent;
  border: none;
  color: #8b949e;
  font-size: 1.2rem;
  cursor: pointer;
}

.avatar-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.avatar-circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #21262d;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  border: 1px solid #E8B86D;
}

.role {
  font-size: 0.85rem;
  color: #8b949e;
}

.dialogo {
  font-size: 0.95rem;
  line-height: 1.4;
  margin-bottom: 1.5rem;
  color: #c9d1d9;
}

.btn-primary {
  width: 100%;
  padding: 0.75rem;
  background: #E8B86D;
  color: #0f1216;
  font-weight: 700;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.game-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.qte-card {
  background: #21262d;
  padding: 1.5rem 1.25rem;
  border-radius: 8px;
  text-align: center;
  margin-bottom: 1rem;
  border: 1px solid #30363d;
  min-height: 160px;
  transition: border-color 0.2s;
}

.qte-card.pressed {
  border-color: #3FE6C0;
}

.qte-card.missed {
  border-color: #f85149;
}

.qte-prompt strong {
  font-size: 1.2rem;
  color: #E8B86D;
  display: block;
  margin-bottom: 0.5rem;
}

.qte-prompt p {
  font-size: 0.85rem;
  color: #c9d1d9;
}

.hold-bar {
  background: #161b22;
  height: 10px;
  border-radius: 6px;
  margin-top: 0.75rem;
  overflow: hidden;
}

.hold-fill {
  height: 100%;
  background: #E8B86D;
  width: 0%;
  transition: width 0.1s linear;
}

.qte-feedback {
  margin-top: 0.75rem;
  font-weight: 700;
  font-size: 0.9rem;
}

.qte-feedback.success {
  color: #3FE6C0;
}

.qte-feedback.miss {
  color: #f85149;
}

.action-zone {
  display: flex;
  justify-content: space-around;
  gap: 0.5rem;
}

.btn-qte {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  font-size: 1.8rem;
  background: #21262d;
  border: 2px solid #30363d;
  color: #e6edf3;
  cursor: pointer;
  transition: transform 0.05s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-qte:hover {
  border-color: #E8B86D;
}

.btn-qte.is-current {
  border-color: #E8B86D;
  box-shadow: 0 0 10px rgba(232, 184, 109, 0.4);
}

.reward-step {
  text-align: center;
}

.reward-icon {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.reward-box {
  background: #21262d;
  padding: 1rem;
  border-radius: 8px;
  margin: 1rem 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.mineral {
  color: #D17A4F;
  font-weight: 700;
}

.badge {
  color: #E8B86D;
  font-size: 0.9rem;
}

.coupon {
  color: #3FE6C0;
  font-size: 0.9rem;
}

.next-poi-box {
  background: #161b22;
  border: 1px dashed #30363d;
  padding: 0.75rem;
  border-radius: 6px;
  font-size: 0.85rem;
  text-align: left;
  margin-bottom: 1rem;
}

.next-title {
  font-weight: 600;
  color: #e6edf3;
}

.next-desc {
  color: #8b949e;
}
</style>