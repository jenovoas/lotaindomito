<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'complete', reward: { cobre: number; oro: number }): void
}>()

const step = ref<'intro' | 'game' | 'reward'>('intro')
const score = ref(0)
const timeLeft = ref(90)
let timer: number | null = null

interface FloraQuestion {
  id: number
  species: string
  origin: 'Nativa' | 'Introducida'
  hint: string
}

const questions: FloraQuestion[] = [
  { id: 1, species: 'Araucaria (Araucaria araucana)', origin: 'Nativa', hint: 'Árbol sagrado del sur de Chile.' },
  { id: 2, species: 'Roble (Nothofagus obliqua)', origin: 'Nativa', hint: 'Dominante en los bosques valdivianos.' },
  { id: 3, species: 'Eucalipto (Eucalyptus globulus)', origin: 'Introducida', hint: 'Traída de Australia para minería.' },
  { id: 4, species: 'Pino Radiata (Pinus radiata)', origin: 'Introducida', hint: 'Llegó desde California, siglo XIX.' },
  { id: 5, species: 'Canelo (Drimys winteri)', origin: 'Nativa', hint: 'Medicina mapuche y lenga.' },
  { id: 6, species: 'Palma Chilena (Jubaea chilensis)', origin: 'Nativa', hint: 'Endémica y centenaria.' },
]

const currentQIndex = ref(0)
const feedback = ref<string | null>(null)
const hasSunsetBonus = ref(false)

function startGame() {
  step.value = 'game'
  score.value = 0
  currentQIndex.value = 0
  timeLeft.value = 90
  // Simular evento de atardecer (en el piloto real: ENV lat_s60 o evento del servidor)
  // Evento del cielo entre 18:30 y 20:00 hora local de Chile
  const now = new Date()
  const hour = now.getHours()
  hasSunsetBonus.value = hour >= 18 && hour <= 20
  timer = window.setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--
    } else {
      finishGame()
    }
  }, 1000)
}

function selectOrigin(origin: FloraQuestion['origin']) {
  const currentQ = questions[currentQIndex.value]
  if (currentQ?.origin === origin) {
    score.value++
    feedback.value = '¡Correcto! Clasificación botánica exacta.'
  } else {
    feedback.value = `Incorrecto. La ${currentQ?.species} es ${currentQ?.origin}.`
  }

  setTimeout(() => {
    feedback.value = null
    if (currentQIndex.value < questions.length - 1) {
      currentQIndex.value++
    } else {
      finishGame()
    }
  }, 800)
}

function finishGame() {
  if (timer) clearInterval(timer)
  step.value = 'reward'
  const oro = hasSunsetBonus.value ? 5 : 0
  emit('complete', { cobre: 30, oro })
}

onMounted(() => {
  return () => {
    if (timer) clearInterval(timer)
  }
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<template>
  <div class="modal-overlay">
    <div class="modal-card">
      <button class="btn-cerrar" @click="emit('close')">✕</button>

      <!-- TRAMO 2: CONTEXTO -->
      <div v-if="step === 'intro'" class="intro-step">
        <div class="avatar-header">
          <div class="avatar-circle">🌹</div>
          <div>
            <h3>Isidora Goyenechea</h3>
            <p class="role">Patrona y Visión del Desarrollo</p>
          </div>
        </div>
        <p class="dialogo">
          "Bienvenida al Parque que llevo mi nombre, Explorador. Aquí la naturaleza y la historia conviven. Demuestra que conoces las especies que cuidé —nativas y traídas— para honrar la memoria botánica de Lota."
        </p>
        <button class="btn-primary" @click="startGame">Comenzar Misión (90s)</button>
      </div>

      <!-- TRAMO 3: ACCIÓN (MINIJUEGO) -->
      <div v-else-if="step === 'game'" class="game-step">
        <div class="game-header">
          <span>Tiempo: <strong>{{ timeLeft }}s</strong></span>
          <span>Aciertos: <strong>{{ score }}/{{ questions.length }}</strong></span>
        </div>

        <div class="card-display">
          <h4>{{ questions[currentQIndex]?.species }}</h4>
          <p class="card-hint">{{ questions[currentQIndex]?.hint }}</p>
          <p class="card-prompt">¿Es nativa de Chile o introducida?</p>
        </div>

        <div v-if="feedback" class="feedback-msg">
          {{ feedback }}
        </div>

        <div class="era-buttons">
          <button @click="selectOrigin('Nativa')">Nativa 🌿</button>
          <button @click="selectOrigin('Introducida')">Introducida 🌍</button>
        </div>
      </div>

      <!-- TRAMO 4 Y 5: RECOMPENSA Y DIRECCIÓN -->
      <div v-else-if="step === 'reward'" class="reward-step">
        <div class="reward-icon">🌳</div>
        <h3>¡Misión Completada!</h3>
        <p>Has identificado las especies botánicas del Parque Isidora Cousiño.</p>

        <div class="reward-box">
          <span class="mineral">+30 Cobre (Cu) 🟠</span>
          <span v-if="hasSunsetBonus" class="mineral oro">+5 Oro (Au) 🟡</span>
          <span class="badge">Insignia: Guardián de la Flora 🏅</span>
        </div>

        <div v-if="hasSunsetBonus" class="sunset-note">
          ✨ Evento del cielo: Atardecer detectado. El oro reverbera en el parque.
        </div>

        <div class="next-poi-box">
          <p class="next-title">📍 Próximo Destino Recomendado:</p>
          <p class="next-desc">Pabellón 81 (a 280m). El Palanquero y la Chinchorrera te esperan para la memoria social de la mina.</p>
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
  border: 1px solid #D4A547;
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
  background: #D4A547;
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

.card-prompt {
  font-size: 0.9rem;
  color: #D4A547;
  margin-top: 0.75rem;
  font-weight: 600;
}

.feedback-msg {
  text-align: center;
  font-size: 0.85rem;
  color: #D4A547;
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
  border-color: #D4A547;
  color: #D4A547;
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

.mineral.oro {
  color: #D4A547;
}

.badge {
  color: #D4A547;
  font-size: 0.9rem;
}

.sunset-note {
  background: rgba(212, 165, 71, 0.15);
  border: 1px dashed #D4A547;
  padding: 0.6rem;
  border-radius: 6px;
  font-size: 0.8rem;
  color: #D4A547;
  margin-bottom: 1rem;
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
