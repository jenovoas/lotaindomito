import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export type ItemCategory = 'mineral' | 'ficha' | 'reliquia' | 'consumible'
export type ItemRarity = 'comun' | 'raro' | 'epico' | 'legendario'

export interface InventoryItem {
  id: string
  name: string
  category: ItemCategory
  rarity: ItemRarity
  icon: string
  quantity: number
  description: string
  lore: string
}

export type QuestStatus = 'en_marcha' | 'lista_para_entrega' | 'completada'

export interface Quest {
  id: string
  npcId: number
  npcName: string
  npcAvatar: string
  title: string
  description: string
  objective: string
  targetZoneId: number
  targetZoneName: string
  status: QuestStatus
  reward: {
    cobre: number
    oro?: number
    itemReward?: { id: string; name: string; icon: string; quantity: number }
  }
  progress: number // 0 - 100
  createdAt: number
}

const STORAGE_KEY_ITEMS = 'lota_inventory_items'
const STORAGE_KEY_QUESTS = 'lota_inventory_quests'

// Ítems iniciales del explorador al llegar a Lota
const ITEMS_DEFAULT: InventoryItem[] = [
  {
    id: 'carbon_grasa',
    name: 'Carbón Grasa de Lota',
    category: 'mineral',
    rarity: 'comun',
    icon: '⬛',
    quantity: 5,
    description: 'Carbón sub-bituminoso de alto poder calórico extraído bajo el mar.',
    lore: 'El combustible que forjó la revolución industrial en Chile y alimentó los vapores del Pacífico.'
  },
  {
    id: 'ficha_cobre_1895',
    name: 'Ficha Pulpería Cousiño (1895)',
    category: 'ficha',
    rarity: 'raro',
    icon: '🪙',
    quantity: 2,
    description: 'Moneda de cuño propio válida en la Pulpería del Pabellón 83.',
    lore: 'Grabada con la corona de Doña Isidora. Con ella los mineros compraban harina y velas.'
  },
  {
    id: 'candil_davy',
    name: 'Candil de Seguridad Davy',
    category: 'reliquia',
    rarity: 'epico',
    icon: '🕯️',
    quantity: 1,
    description: 'Lámpara con malla de alambre que delata la presencia de gas grisú.',
    lore: 'Si la llama se vuelve azul, corre hacia el pique principal antes de que estalle la galería.'
  }
]

export const useInventoryStore = defineStore('inventory', () => {
  const items = ref<InventoryItem[]>(loadItemsFromStorage())
  const quests = ref<Quest[]>(loadQuestsFromStorage())
  const lastAcquiredItem = ref<{ name: string; icon: string } | null>(null)

  function loadItemsFromStorage(): InventoryItem[] {
    try {
      const raw = localStorage.getItem(STORAGE_KEY_ITEMS)
      if (raw) return JSON.parse(raw)
    } catch {
      // Fallback
    }
    return [...ITEMS_DEFAULT]
  }

  function loadQuestsFromStorage(): Quest[] {
    try {
      const raw = localStorage.getItem(STORAGE_KEY_QUESTS)
      if (raw) return JSON.parse(raw)
    } catch {
      // Fallback
    }
    return []
  }

  function persist() {
    try {
      localStorage.setItem(STORAGE_KEY_ITEMS, JSON.stringify(items.value))
      localStorage.setItem(STORAGE_KEY_QUESTS, JSON.stringify(quests.value))
    } catch {
      // Storage error
    }
  }

  function addItem(itemData: Omit<InventoryItem, 'quantity'>, quantity = 1) {
    const existing = items.value.find(i => i.id === itemData.id)
    if (existing) {
      existing.quantity += quantity
    } else {
      items.value.push({ ...itemData, quantity })
    }
    lastAcquiredItem.value = { name: itemData.name, icon: itemData.icon }
    persist()

    // Limpiar toast tras 3 segundos
    setTimeout(() => {
      if (lastAcquiredItem.value?.name === itemData.name) {
        lastAcquiredItem.value = null
      }
    }, 3500)
  }

  function removeItem(itemId: string, quantity = 1): boolean {
    const existing = items.value.find(i => i.id === itemId)
    if (!existing || existing.quantity < quantity) return false
    existing.quantity -= quantity
    if (existing.quantity <= 0) {
      items.value = items.value.filter(i => i.id !== itemId)
    }
    persist()
    return true
  }

  function acceptQuest(quest: Quest) {
    const exists = quests.value.some(q => q.id === quest.id)
    if (!exists) {
      quests.value.push(quest)
      persist()
    }
  }

  function updateQuestProgress(questId: string, progress: number) {
    const q = quests.value.find(q => q.id === questId)
    if (q) {
      q.progress = Math.min(100, Math.max(0, progress))
      if (q.progress >= 100 && q.status === 'en_marcha') {
        q.status = 'lista_para_entrega'
      }
      persist()
    }
  }

  function completeQuest(questId: string): Quest | null {
    const q = quests.value.find(q => q.id === questId)
    if (q) {
      q.status = 'completada'
      if (q.reward.itemReward) {
        addItem({
          id: q.reward.itemReward.id,
          name: q.reward.itemReward.name,
          category: 'reliquia',
          rarity: 'epico',
          icon: q.reward.itemReward.icon,
          description: 'Recompensa obtenida al culminar el despacho con éxito.',
          lore: `Otorgado por ${q.npcName} tras tu servicio en la cuenca carbonífera.`
        }, q.reward.itemReward.quantity)
      }
      persist()
      return q
    }
    return null
  }

  const totalItemsCount = computed(() => items.value.reduce((s, i) => s + i.quantity, 0))
  const activeQuests = computed(() => quests.value.filter(q => q.status !== 'completada'))
  const completedQuests = computed(() => quests.value.filter(q => q.status === 'completada'))

  return {
    items,
    quests,
    lastAcquiredItem,
    totalItemsCount,
    activeQuests,
    completedQuests,
    addItem,
    removeItem,
    acceptQuest,
    updateQuestProgress,
    completeQuest,
  }
})
