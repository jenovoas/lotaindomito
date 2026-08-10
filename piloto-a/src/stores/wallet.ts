import { ref } from 'vue'
import { defineStore } from 'pinia'

/** Tipos de moneda disponibles en la billetera del jugador. */
export type Currency = 'cobre' | 'oro' | 'estanio'

/** Balance actual de la billetera. */
export interface WalletBalance {
  cobre: number
  oro: number
  estanio: number
}

/** Representación de una transacción registrada en la billetera. */
export interface WalletTransaction {
  id: string
  currency: Currency
  amount: number
  tx_type: 'earn' | 'spend' | 'transfer'
  reason: string
  created_at: string
}

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

/** Store Pinia para gestionar la billetera del usuario. */
export const useWalletStore = defineStore('wallet', () => {
  const balance = ref<WalletBalance>({ cobre: 0, oro: 0, estanio: 0 })
  const transactions = ref<WalletTransaction[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchBalance(userId: string): Promise<void> {
    loading.value = true
    error.value = null
    try {
      const res = await fetch(`${API_BASE}/api/wallet/${userId}`)
      if (!res.ok) {
        throw new Error(`Error ${res.status}: ${res.statusText}`)
      }
      balance.value = (await res.json()) as WalletBalance
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'No se pudo cargar el balance'
    } finally {
      loading.value = false
    }
  }

  async function earn(
    userId: string,
    currency: Currency,
    amount: number,
    reason: string,
  ): Promise<boolean> {
    try {
      const res = await fetch(`${API_BASE}/api/wallet/earn`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, currency, amount, reason }),
      })
      if (res.ok) {
        balance.value = (await res.json()) as WalletBalance
        return true
      }
      return false
    } catch {
      return false
    }
  }

  async function spend(
    userId: string,
    currency: Currency,
    amount: number,
    reason: string,
  ): Promise<boolean> {
    try {
      const res = await fetch(`${API_BASE}/api/wallet/spend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, currency, amount, reason }),
      })
      if (res.ok) {
        balance.value = (await res.json()) as WalletBalance
        return true
      }
      return false
    } catch {
      return false
    }
  }

  async function transfer(
    fromId: string,
    toId: string,
    currency: Currency,
    amount: number,
  ): Promise<boolean> {
    try {
      const res = await fetch(`${API_BASE}/api/wallet/transfer`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ from_id: fromId, to_id: toId, currency, amount }),
      })
      if (res.ok) {
        balance.value = (await res.json()) as WalletBalance
        return true
      }
      return false
    } catch {
      return false
    }
  }

  return {
    balance,
    transactions,
    loading,
    error,
    fetchBalance,
    earn,
    spend,
    transfer,
  }
})
