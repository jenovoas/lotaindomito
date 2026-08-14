<script setup lang="ts">
import { ref } from 'vue'
import { useInventoryStore, type InventoryItem, type Quest } from '@/stores/inventory'
import { useWalletStore } from '@/stores/wallet'

const emit = defineEmits<{
  (e: 'close'): void
}>()

const inventory = useInventoryStore()
const wallet = useWalletStore()

const activeTab = ref<'mochila' | 'bitacora'>('mochila')
const selectedItem = ref<InventoryItem | null>(null)
const selectedQuest = ref<Quest | null>(null)

function selectItem(item: InventoryItem) {
  selectedItem.value = item
}

function selectQuest(quest: Quest) {
  selectedQuest.value = quest
}

function claimQuestReward(quest: Quest) {
  const finished = inventory.completeQuest(quest.id)
  if (finished) {
    wallet.balance.cobre += finished.reward.cobre
    if (finished.reward.oro) wallet.balance.oro += finished.reward.oro
  }
}
</script>

<template>
  <div class="mochila-overlay" @click.self="emit('close')">
    <div class="mochila-modal">
      <!-- Encabezado Diegético -->
      <div class="modal-header">
        <div class="header-title">
          <span class="icon-pack">🎒</span>
          <div>
            <h2>Mochila de Barretero</h2>
            <span class="subtitle">Equipamiento & Registro de la Cuenca</span>
          </div>
        </div>
        <button class="btn-close" @click="emit('close')">✕</button>
      </div>

      <!-- Pestañas de Navegación -->
      <div class="tab-nav">
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'mochila' }"
          @click="activeTab = 'mochila'"
        >
          ⛏️ Minerales & Fichas ({{ inventory.items.length }})
        </button>
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'bitacora' }"
          @click="activeTab = 'bitacora'"
        >
          📜 Bitácora de Misiones ({{ inventory.activeQuests.length }})
        </button>
      </div>

      <!-- Contenido de la Pestaña Mochila -->
      <div v-if="activeTab === 'mochila'" class="tab-content mochila-grid-layout">
        <div class="items-grid">
          <div
            v-for="item in inventory.items"
            :key="item.id"
            class="item-card"
            :class="[item.rarity, { selected: selectedItem?.id === item.id }]"
            @click="selectItem(item)"
          >
            <div class="item-icon-wrapper">
              <span class="item-icon">{{ item.icon }}</span>
              <span class="item-qty">x{{ item.quantity }}</span>
            </div>
            <span class="item-name">{{ item.name }}</span>
            <span class="item-rarity-tag">{{ item.rarity }}</span>
          </div>

          <div v-if="inventory.items.length === 0" class="empty-state">
            <span class="empty-icon">🪹</span>
            <p>Tu morral está vacío. Camina por las zonas de Lota y habla con los personajes para recolectar minerales.</p>
          </div>
        </div>

        <!-- Inspector de Ítem Seleccionado -->
        <aside v-if="selectedItem" class="item-inspector">
          <div class="inspector-header">
            <span class="inspector-icon">{{ selectedItem.icon }}</span>
            <div>
              <h3>{{ selectedItem.name }}</h3>
              <span class="inspector-cat">{{ selectedItem.category }} • {{ selectedItem.rarity }}</span>
            </div>
          </div>
          <p class="inspector-desc">{{ selectedItem.description }}</p>
          <div class="inspector-lore">
            <span class="lore-label">📜 MEMORIA HISTÓRICA:</span>
            <p>"{{ selectedItem.lore }}"</p>
          </div>
          <div class="inspector-footer">
            <span>En inventario: <strong>{{ selectedItem.quantity }} unidades</strong></span>
          </div>
        </aside>
      </div>

      <!-- Contenido de la Pestaña Bitácora -->
      <div v-else-if="activeTab === 'bitacora'" class="tab-content bitacora-layout">
        <div class="quests-list">
          <div
            v-for="quest in inventory.quests"
            :key="quest.id"
            class="quest-card"
            :class="[quest.status, { selected: selectedQuest?.id === quest.id }]"
            @click="selectQuest(quest)"
          >
            <div class="quest-card-header">
              <div class="npc-badge">
                <span>{{ quest.npcAvatar }}</span>
                <span class="npc-name">{{ quest.npcName }}</span>
              </div>
              <span class="quest-status-badge" :class="quest.status">
                {{ quest.status === 'completada' ? '✓ CUMPLIDA' : quest.status === 'lista_para_entrega' ? '⚡ LISTA' : '⏳ EN MARCHA' }}
              </span>
            </div>

            <h4 class="quest-title">{{ quest.title }}</h4>
            <p class="quest-objective">📍 {{ quest.objective }}</p>

            <!-- Barra de Progreso -->
            <div class="progress-bar-container">
              <div class="progress-bar-fill" :style="{ width: `${quest.progress}%` }"></div>
            </div>

            <div class="quest-card-footer">
              <span class="reward-preview">Recompensa: +{{ quest.reward.cobre }} Cu</span>
              <button
                v-if="quest.status === 'lista_para_entrega'"
                class="btn-claim"
                @click.stop="claimQuestReward(quest)"
              >
                ENTREGAR 🎁
              </button>
            </div>
          </div>

          <div v-if="inventory.quests.length === 0" class="empty-state">
            <span class="empty-icon">🧭</span>
            <p>No tienes misiones activas. Intercepta a <strong>El Palanquero</strong> o a <strong>Doña Isidora</strong> en las calles para recibir despachos.</p>
          </div>
        </div>

        <!-- Detalle de Misión Seleccionada -->
        <aside v-if="selectedQuest" class="quest-detail-inspector">
          <h3>{{ selectedQuest.title }}</h3>
          <p class="quest-desc">{{ selectedQuest.description }}</p>
          <div class="target-zone-box">
            <span>ZONA DE DESTINO:</span>
            <strong>🏛️ {{ selectedQuest.targetZoneName }}</strong>
          </div>
          <div class="rewards-breakdown">
            <h4>Recompensas al entregar:</h4>
            <ul>
              <li>🪙 {{ selectedQuest.reward.cobre }} Fichas de Cobre</li>
              <li v-if="selectedQuest.reward.oro">✨ {{ selectedQuest.reward.oro }} Fichas de Oro</li>
              <li v-if="selectedQuest.reward.itemReward">
                🎁 {{ selectedQuest.reward.itemReward.icon }} {{ selectedQuest.reward.itemReward.name }} (x{{ selectedQuest.reward.itemReward.quantity }})
              </li>
            </ul>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<style scoped>
.mochila-overlay {
  position: fixed;
  inset: 0;
  z-index: 9998;
  background: rgba(7, 9, 13, 0.85);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
}

.mochila-modal {
  width: 100%;
  max-width: 820px;
  max-height: 90vh;
  background: #121720;
  border: 2px solid #303a4b;
  border-radius: 20px;
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.8), 0 0 20px rgba(63, 230, 192, 0.15);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.modal-header {
  padding: 18px 24px;
  background: #171f2c;
  border-bottom: 1px solid #283344;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.icon-pack {
  font-size: 2rem;
}

.header-title h2 {
  font-size: 1.3rem;
  color: #3fe6c0;
  margin: 0;
  font-weight: 800;
}

.header-title .subtitle {
  font-size: 0.8rem;
  color: #8b99ad;
}

.btn-close {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #303a4b;
  color: #8b99ad;
  font-size: 1.1rem;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-close:hover {
  background: #e76f51;
  color: #fff;
  border-color: #e76f51;
}

.tab-nav {
  display: flex;
  background: #0e1219;
  border-bottom: 1px solid #283344;
}

.tab-btn {
  flex: 1;
  padding: 12px 16px;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  color: #8b99ad;
  font-weight: 700;
  font-size: 0.88rem;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-btn.active {
  color: #3fe6c0;
  border-bottom-color: #3fe6c0;
  background: rgba(63, 230, 192, 0.04);
}

.tab-content {
  padding: 20px;
  overflow-y: auto;
  flex: 1;
}

.mochila-grid-layout, .bitacora-layout {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 20px;
}

@media (max-width: 720px) {
  .mochila-grid-layout, .bitacora-layout {
    grid-template-columns: 1fr;
  }
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  gap: 12px;
}

.item-card {
  background: #171e2a;
  border: 1.5px solid #283344;
  border-radius: 12px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
}

.item-card:hover, .item-card.selected {
  transform: translateY(-2px);
  border-color: #3fe6c0;
  box-shadow: 0 4px 16px rgba(63, 230, 192, 0.2);
}

.item-card.comun { border-left: 3px solid #8b99ad; }
.item-card.raro { border-left: 3px solid #ffd700; }
.item-card.epico { border-left: 3px solid #3fe6c0; }
.item-card.legendario { border-left: 3px solid #e76f51; }

.item-icon-wrapper {
  position: relative;
  margin-bottom: 8px;
}

.item-icon {
  font-size: 2.2rem;
}

.item-qty {
  position: absolute;
  bottom: -4px;
  right: -8px;
  background: #0f1216;
  border: 1px solid #303a4b;
  color: #3fe6c0;
  font-size: 0.7rem;
  font-weight: 800;
  padding: 1px 5px;
  border-radius: 10px;
}

.item-name {
  font-size: 0.8rem;
  font-weight: 700;
  color: #f1f5f9;
  margin-bottom: 4px;
}

.item-rarity-tag {
  font-size: 0.65rem;
  text-transform: uppercase;
  color: #64748b;
  font-weight: 600;
}

.item-inspector, .quest-detail-inspector {
  background: #18202d;
  border: 1px solid #2d3a4d;
  border-radius: 14px;
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.inspector-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.inspector-icon {
  font-size: 2.5rem;
}

.inspector-header h3 {
  font-size: 1.1rem;
  color: #f1f5f9;
  margin: 0;
}

.inspector-cat {
  font-size: 0.75rem;
  color: #3fe6c0;
  text-transform: uppercase;
  font-weight: bold;
}

.inspector-desc {
  font-size: 0.88rem;
  color: #94a3b8;
  line-height: 1.4;
}

.inspector-lore {
  background: rgba(15, 23, 42, 0.6);
  border-left: 3px solid #d4af37;
  padding: 10px 12px;
  border-radius: 0 8px 8px 0;
}

.lore-label {
  font-size: 0.65rem;
  color: #d4af37;
  font-weight: bold;
  letter-spacing: 1px;
}

.inspector-lore p {
  font-size: 0.8rem;
  color: #cbd5e1;
  font-style: italic;
  margin-top: 4px;
}

.inspector-footer {
  margin-top: auto;
  border-top: 1px solid #283344;
  padding-top: 10px;
  font-size: 0.8rem;
  color: #64748b;
}

/* Bitácora */
.quests-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.quest-card {
  background: #171e2a;
  border: 1.5px solid #283344;
  border-radius: 12px;
  padding: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.quest-card:hover, .quest-card.selected {
  border-color: #3fe6c0;
  background: #1b2332;
}

.quest-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.npc-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8rem;
  font-weight: 700;
  color: #3fe6c0;
}

.quest-status-badge {
  font-size: 0.68rem;
  font-weight: 800;
  padding: 2px 8px;
  border-radius: 12px;
}

.quest-status-badge.en_marcha {
  background: rgba(245, 162, 133, 0.15);
  color: #f5a285;
}

.quest-status-badge.lista_para_entrega {
  background: rgba(63, 230, 192, 0.2);
  color: #3fe6c0;
}

.quest-status-badge.completada {
  background: rgba(100, 116, 139, 0.2);
  color: #64748b;
}

.quest-title {
  color: #f1f5f9;
  font-size: 0.95rem;
  margin-bottom: 4px;
}

.quest-objective {
  font-size: 0.8rem;
  color: #94a3b8;
  margin-bottom: 8px;
}

.progress-bar-container {
  height: 6px;
  background: #0f1216;
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 10px;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #d17a4f, #3fe6c0);
  transition: width 0.3s ease;
}

.quest-card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.reward-preview {
  font-size: 0.75rem;
  color: #d4af37;
  font-weight: 700;
}

.btn-claim {
  background: #3fe6c0;
  color: #0f1216;
  border: none;
  font-size: 0.75rem;
  font-weight: 800;
  padding: 4px 10px;
  border-radius: 6px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(63, 230, 192, 0.4);
}

.target-zone-box {
  background: #0f1216;
  padding: 10px;
  border-radius: 8px;
  font-size: 0.8rem;
  color: #94a3b8;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.target-zone-box strong {
  color: #3fe6c0;
}

.rewards-breakdown ul {
  list-style: none;
  padding: 0;
  margin-top: 8px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 0.85rem;
  color: #e2e8f0;
}

.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 30px;
  color: #64748b;
}

.empty-icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 10px;
}
</style>
