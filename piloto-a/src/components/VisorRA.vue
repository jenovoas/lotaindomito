<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import type { NpcWire } from '@/stores/mobs'
import { useAnalyticsStore } from '@/stores/analytics'

import { useInventoryStore } from '@/stores/inventory'

const props = defineProps<{
  npc: NpcWire
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'complete', reward: { cobre: number; oro?: number }): void
}>()

const analytics = useAnalyticsStore()
const inventory = useInventoryStore()
const videoElement = ref<HTMLVideoElement | null>(null)
const cameraActive = ref(false)
const cameraError = ref(false)

const dialogueIndex = ref(0)
const isWalking = ref(true)
const questAccepted = ref(false)

// Simulación de audio/pasos y giroscopio
const heading = ref(45)
const pitch = ref(0)

onMounted(async () => {
  analytics.trackWorldEventJoin(`intercepcion_ra_${props.npc.id}`)
  await startCamera()
  startOrientationListener()
})

onUnmounted(() => {
  stopCamera()
})

async function startCamera() {
  try {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } }
      })
      if (videoElement.value) {
        videoElement.value.srcObject = stream
        cameraActive.value = true
      }
    } else {
      cameraError.value = true
    }
  } catch (err) {
    console.warn('Cámara no disponible, usando simulador de visor espectral', err)
    cameraError.value = true
  }
}

function stopCamera() {
  if (videoElement.value && videoElement.value.srcObject) {
    const stream = videoElement.value.srcObject as MediaStream
    stream.getTracks().forEach((track) => track.stop())
  }
}

function startOrientationListener() {
  if (window.DeviceOrientationEvent) {
    window.addEventListener('deviceorientation', (e) => {
      if (e.alpha !== null) heading.value = Math.round(e.alpha)
      if (e.beta !== null) pitch.value = Math.round(e.beta)
    })
  }
}

function nextDialogue() {
  if (dialogueIndex.value < props.npc.dialogueLines.length - 1) {
    dialogueIndex.value++
  } else {
    finishEncounter()
  }
}

function finishEncounter() {
  questAccepted.value = true
  isWalking.value = false

  // Registrar ítem histórico en la mochila
  if (props.npc.id === 2) {
    // El Palanquero
    inventory.addItem({
      id: 'despacho_palanquero',
      name: 'Orden de Despacho Ferroviario',
      category: 'reliquia',
      rarity: 'raro',
      icon: '📜',
      description: 'Orden firmada para autorizar el cambio de agujas del tren de carbón.',
      lore: 'Los trenes de Lota transportaban miles de toneladas al puerto. El palanquero era el árbitro de la vida y la muerte en las vías.'
    }, 1)

    inventory.acceptQuest({
      id: `quest_palanquero_${Date.now()}`,
      npcId: 2,
      npcName: 'El Palanquero',
      npcAvatar: '⛏️',
      title: 'El Tren de la Maestranza',
      description: 'Lleva la orden de cambio de agujas al sector de Pabellones y Chiflón.',
      objective: 'Caminar 200m hacia el Chiflón del Diablo',
      targetZoneId: 480338029,
      targetZoneName: 'Chiflón del Diablo',
      status: 'lista_para_entrega',
      reward: { cobre: 75, oro: 5 },
      progress: 100,
      createdAt: Date.now()
    })
  } else if (props.npc.id === 1) {
    // Doña Isidora
    inventory.addItem({
      id: 'carta_isidora',
      name: 'Carta Lacrada de Doña Isidora',
      category: 'reliquia',
      rarity: 'epico',
      icon: '👑',
      description: 'Documento sellado con cera y la corona de la familia Cousiño.',
      lore: 'Contiene planos de la primera planta hidroeléctrica de Chivilingo que iluminó Lota.'
    }, 1)
  } else {
    // El Ciego de la Mina
    inventory.addItem({
      id: 'carbon_grasa',
      name: 'Carbón Grasa de Lota',
      category: 'mineral',
      rarity: 'comun',
      icon: '⬛',
      description: 'Carbón sub-bituminoso extraído a 500 metros bajo el nivel del mar.',
      lore: 'La memoria viva de las galerías submarinas del Chiflón.'
    }, 3)
  }

  emit('complete', props.npc.reward)
}
</script>

<template>
  <div class="visor-ra-overlay">
    <!-- Capa de Cámara Real o Filtro Espectral -->
    <div class="camera-container">
      <video
        ref="videoElement"
        autoplay
        playsinline
        muted
        class="camera-stream"
        :class="{ hidden: cameraError || !cameraActive }"
      ></video>

      <!-- Fondo alternativo si la cámara no tiene permiso -->
      <div v-if="cameraError || !cameraActive" class="spectral-environment">
        <div class="grid-overlay"></div>
        <div class="fog-layer"></div>
        <div class="coal-particles">
          <span v-for="i in 15" :key="i" class="ember" :style="{ left: `${(i * 7) % 100}%`, animationDelay: `${i * 0.4}s` }"></span>
        </div>
      </div>
    </div>

    <!-- HUD Holográfico de Realidad Aumentada -->
    <div class="ar-hud">
      <!-- Barra Superior: Datos de Sincronización y Giroscopio -->
      <div class="hud-top">
        <div class="sync-badge">
          <span class="pulse-dot"></span>
          <span>SINCRONIZACIÓN S60: 100%</span>
        </div>
        <div class="compass-badge">
          <span>🧭 {{ heading }}° | RUMBO CALLE</span>
        </div>
        <button class="btn-close" @click="emit('close')">✕ SALIR</button>
      </div>

      <!-- Espacio Central: Modelo Espectral en Marcha -->
      <div class="npc-projection-area">
        <div class="npc-spatial-wrapper" :class="{ 'in-motion': isWalking }">
          <div class="hologram-glow"></div>
          
          <!-- Avatar Espectral a Escala 1:1 -->
          <div class="npc-character-card">
            <div class="npc-avatar-big">{{ npc.avatar }}</div>
            <div class="faction-tag">{{ npc.faction }}</div>
            <h2 class="npc-name-ar">{{ npc.name }}</h2>
            <p class="npc-title-ar">{{ npc.title }}</p>
          </div>

          <!-- Indicador de Marcha Hombro a Hombro -->
          <div class="walk-status" v-if="isWalking">
            <span class="boot-step">👞</span>
            <span>Caminando a 3.5 km/h a tu lado</span>
          </div>
        </div>
      </div>

      <!-- Barra Inferior: Diálogo en Marcha y Acción -->
      <div class="dialogue-box">
        <div class="speaker-header">
          <span class="speaker-name">{{ npc.name }}</span>
          <span class="dialogue-step">{{ dialogueIndex + 1 }} / {{ npc.dialogueLines.length }}</span>
        </div>

        <p class="dialogue-text">
          "{{ npc.dialogueLines[dialogueIndex] }}"
        </p>

        <div class="dialogue-actions">
          <button v-if="!questAccepted && dialogueIndex < npc.dialogueLines.length - 1" class="btn-ar-primary" @click="nextDialogue">
            CONTINUAR CAMINANDO ──►
          </button>
          <button v-else-if="!questAccepted" class="btn-ar-action" @click="finishEncounter">
            ⛏️ ACEPTAR DESPACHO (+{{ npc.reward.cobre }} Cu)
          </button>
          <div v-else class="reward-success">
            <span>✨ ¡Despacho aceptado! Guardado en la mochila.</span>
            <button class="btn-ar-primary" @click="emit('close')">VOLVER AL MAPA</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.visor-ra-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background-color: #0f1216;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  font-family: 'Segoe UI', system-ui, sans-serif;
}

.camera-container {
  position: absolute;
  inset: 0;
  z-index: 1;
}

.camera-stream {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.camera-stream.hidden {
  display: none;
}

.spectral-environment {
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, #1b2838 0%, #0a0d12 100%);
  position: relative;
  overflow: hidden;
}

.grid-overlay {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(rgba(63, 230, 192, 0.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(63, 230, 192, 0.08) 1px, transparent 1px);
  background-size: 40px 40px;
}

.coal-particles .ember {
  position: absolute;
  bottom: -10px;
  width: 6px;
  height: 6px;
  background: #f5a285;
  box-shadow: 0 0 10px #f5a285;
  border-radius: 50%;
  animation: floatUp 4s infinite linear;
}

@keyframes floatUp {
  0% { transform: translateY(0) scale(1); opacity: 0; }
  30% { opacity: 0.8; }
  100% { transform: translateY(-100vh) scale(0.3); opacity: 0; }
}

.ar-hud {
  position: relative;
  z-index: 2;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 16px;
  pointer-events: none;
}

.ar-hud button {
  pointer-events: auto;
}

.hud-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.sync-badge, .compass-badge {
  background: rgba(15, 18, 22, 0.85);
  border: 1px solid #3fe6c0;
  color: #3fe6c0;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 6px;
  backdrop-filter: blur(8px);
}

.pulse-dot {
  width: 8px;
  height: 8px;
  background-color: #3fe6c0;
  border-radius: 50%;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(1.3); }
}

.btn-close {
  background: rgba(220, 53, 69, 0.8);
  border: 1px solid #ff4d4f;
  color: #fff;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: bold;
  cursor: pointer;
}

.npc-projection-area {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.npc-spatial-wrapper {
  text-align: center;
  background: rgba(15, 23, 42, 0.75);
  border: 2px solid rgba(63, 230, 192, 0.6);
  padding: 24px 32px;
  border-radius: 24px;
  backdrop-filter: blur(12px);
  box-shadow: 0 0 30px rgba(63, 230, 192, 0.3);
  transition: transform 0.5s ease;
}

.npc-spatial-wrapper.in-motion {
  animation: gentleWalk 2s infinite ease-in-out;
}

@keyframes gentleWalk {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

.npc-avatar-big {
  font-size: 4rem;
  margin-bottom: 8px;
  filter: drop-shadow(0 0 16px #3fe6c0);
}

.faction-tag {
  display: inline-block;
  background: #d17a4f;
  color: #fff;
  font-size: 0.75rem;
  font-weight: bold;
  padding: 2px 10px;
  border-radius: 12px;
  margin-bottom: 6px;
}

.npc-name-ar {
  color: #3fe6c0;
  font-size: 1.5rem;
  margin: 0;
  font-weight: 800;
}

.npc-title-ar {
  color: #94a3b8;
  font-size: 0.85rem;
  margin: 4px 0 12px 0;
}

.walk-status {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #f5a285;
  font-size: 0.8rem;
  font-weight: bold;
}

.dialogue-box {
  pointer-events: auto;
  background: rgba(15, 18, 22, 0.92);
  border: 2px solid #3fe6c0;
  border-radius: 16px;
  padding: 18px;
  backdrop-filter: blur(16px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.7);
}

.speaker-header {
  display: flex;
  justify-content: space-between;
  color: #3fe6c0;
  font-size: 0.85rem;
  font-weight: bold;
  margin-bottom: 8px;
  border-bottom: 1px solid rgba(63, 230, 192, 0.2);
  padding-bottom: 4px;
}

.dialogue-text {
  color: #f1f5f9;
  font-size: 1.05rem;
  line-height: 1.5;
  margin: 10px 0 16px 0;
  font-style: italic;
}

.dialogue-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.btn-ar-primary {
  background: #3fe6c0;
  color: #0f1216;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: bold;
  font-size: 0.9rem;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(63, 230, 192, 0.4);
}

.btn-ar-action {
  background: linear-gradient(135deg, #d17a4f 0%, #f5a285 100%);
  color: #0f1216;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 900;
  font-size: 0.95rem;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(209, 122, 79, 0.5);
}

.reward-success {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  color: #3fe6c0;
  font-weight: bold;
}
</style>
