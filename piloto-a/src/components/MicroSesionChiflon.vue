<script setup lang="ts">
import { ref, onMounted } from 'vue'

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'complete', reward: { cobre: number; oro: number }): void
}>()

const step = ref<'intro' | 'game' | 'reward'>('intro')
const score = ref(0)
const targetScore = 5
const timeLeft = ref(90)
let timer: number | null = null

interface Card {
  id: number
  name: string
  era: 'Carbonífero (300 Ma)' | 'Terciario (50 Ma)' | 'Cuaternario (Reciente)'
  type: 'carbon' | 'fosil' | 'roca'
}

const cards: Card[] = [
  { id: 1, name: 'Manto Estéril / Lutita', era: 'Carbonífero (300 Ma)', type: 'roca' },
  { id: 2, name: 'Sigillaria (Fósil)', era: 'Carbonífero (300 Ma)', type: 'fosil' },
  { id: 3, name: 'Carbón Bituminoso', era: 'Carbonífero (300 Ma)', type: 'carbon' },
  { id: 4, name: 'Impresión de Helecho Giant', era: 'Carbonífero (300 Ma)', type: 'fosil' },
  { id: 5, name: 'Arcilla Terciaria', era: 'Terciario (50 Ma)', type: 'roca' },
  { id: 6, name: 'Sedimento Reciente', era: 'Cuaternario (Reciente)', type: 'roca' },
]

const currentCardIndex = ref(0)
const feedback = ref<string | null>(null)

function startGame() {
  step.value = 'game'
  score.value = 0
  currentCardIndex.value = 0
  timeLeft.value = 90
  timer = window.setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--
    } else {
      finishGame()
    }
  }, 1000)
}

function selectEra(era: Card['era']) {
  const currentCard = cards[currentCardIndex.value]
  if (currentCard.era === era) {
    score.value++
    feedback.value = '¡Correcto! Clasificación geológica exacta.'
  } else {
    feedback.value = 'Incorrecto, esa capa pertenece a otra era.'
  }

  setTimeout(() => {
    feedback.value = null
    if (currentCardIndex.value < cards.length - 1) {
      currentCardIndex.value++
    } else {
      finishGame()
    }
  }, 800)
}

function finishGame() {
  if (timer) clearInterval(timer)
  step.value = 'reward'
  emit('complete', { cobre: 50, oro: 0 })
}

onMounted(() => {
  return () => {
    if (timer) clearInterval(timer)
  }
})
</script>

<template>
  <div class="modal-overlay">
    <div class="modal-card">
      <button class="btn-cerrar" @click="emit('close')">✕</button>

      <!-- TRAMO 2: CONTEXTO -->
      <div v-if="step === 'intro'" class="intro-step">
        <div class="avatar-header">
          <div class="avatar-circle">⛏️</div>
          <div>
            <h3>El Ciego de la Mina</h3>
            <p class="role">Guía Histórico del Pique</p>
          </div>
        </div>
        <p class="dialogo">
          "Bienvenido al Chiflón del Diablo, Explorador. Abajo en la galería, las capas de la tierra cuentan la historia de 300 millones de años. Clasifica las capas geológicas para rescatar la memoria del mineral."
        </p>
        <button class="btn-primary" @click="startGame">Comenzar Misión (90s)</button>
      </div>

      <!-- TRAMO 3: ACCIÓN (MINIJUEGO) -->
      <div v-else-if="step === 'game'" class="game-step">
        <div class="game-header">
          <span>Tiempo: <strong>{{ timeLeft }}s</strong></span>
          <span>Aciertos: <strong>{{ score }}/{{ cards.length }}</strong></span>
        </div>

        <div class="card-display">
          <h4>{{ cards[currentCardIndex].name }}</h4>
          <p class="card-hint">¿A qué era geológica pertenece este hallazgo?</p>
        </div>

        <div v-if="feedback" class="feedback-msg">
          {{ feedback }}
        </div>

        <div class="era-buttons">
          <button @click="selectEra('Carbonífero (300 Ma)')">Carbonífero (300 Ma)</button>
          <button @click="selectEra('Terciario (50 Ma)')">Terciario (50 Ma)</button>
          <button @click="selectEra('Cuaternario (Reciente)')">Cuaternario (Reciente)</button>
        </div>
      </div>

      <!-- TRAMO 4 Y 5: RECOMPENSA Y DIRECCIÓN -->
      <div v-else-if="step === 'reward'" class="reward-step">
        <div class="reward-icon">🏆</div>
        <h3>¡Misión Completada!</h3>
        <p>Has clasificado las muestras geológicas del Chiflón del Diablo.</p>
        
        <div class="reward-box">
          <span class="mineral">+50 Cobre (Cu) 🟠</span>
          <span class="badge">Insignia: Explorador de las Profundidades 🏅</span>
        </div>

        <div class="next-poi-box">
          <p class="next-title">📍 Próximo Destino Recomendado:</p>
          <p class="next-desc">Parque Isidora Cousiño (a 320m). Isidora te espera con misiones botánicas.</p>
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
  border: 1px solid #3FE6C0;
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
  background: #3FE6C0;
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

.card-display {
  background: #21262d;
  padding: 1.25rem;
  border-radius: 8px;
  text-align: center;
  margin-bottom: 1rem;
  border: 1px solid #30363d;
}

.card-hint {
  font-size: 0.85rem;
  color: #8b949e;
  margin-top: 0.5rem;
}

.feedback-msg {
  text-align: center;
  font-size: 0.85rem;
  color: #3FE6C0;
  margin-bottom: 0.5rem;
}

.era-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.era-buttons button {
  padding: 0.65rem;
  background: #21262d;
  border: 1px solid #30363d;
  color: #e6edf3;
  border-radius: 6px;
  cursor: pointer;
}

.era-buttons button:hover {
  border-color: #3FE6C0;
  color: #3FE6C0;
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
