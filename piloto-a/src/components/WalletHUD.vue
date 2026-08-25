<script setup lang="ts">
import { useWalletStore } from '@/stores/wallet'
import { onMounted } from 'vue'

const wallet = useWalletStore()

// Usuario de prueba para el piloto.
const TEST_USER = 'test-1'

onMounted(() => {
  wallet.fetchBalance(TEST_USER)
})
</script>

<template>
  <div class="wallet-hud">
    <span class="currency cobre" title="Cobre" :aria-label="`Cobre: ${wallet.balance.cobre.toLocaleString()} fichas`">
      <span class="icon" aria-hidden="true">Cu</span>
      <span class="amount">{{ wallet.balance.cobre.toLocaleString() }}</span>
    </span>
    <span class="currency oro" title="Oro" :aria-label="`Oro: ${wallet.balance.oro.toLocaleString()} fichas`">
      <span class="icon" aria-hidden="true">Au</span>
      <span class="amount">{{ wallet.balance.oro.toLocaleString() }}</span>
    </span>
    <span class="currency estanio" title="Estaño" :aria-label="`Estaño: ${wallet.balance.estanio.toLocaleString()} fichas`">
      <span class="icon" aria-hidden="true">Sn</span>
      <span class="amount">{{ wallet.balance.estanio.toLocaleString() }}</span>
    </span>
  </div>
</template>

<style scoped>
.wallet-hud {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
  font-size: 14px;
  font-weight: 600;
}

.currency {
  display: flex;
  align-items: center;
  gap: 4px;
}

.icon {
  font-size: 11px;
  font-weight: 700;
  padding: 2px 5px;
  border-radius: 4px;
  color: #0f1216;
}

.cobre .icon {
  background: #d17a4f;
}

.oro .icon {
  background: #ffd700;
}

.estanio .icon {
  background: #c0c0c0;
}

.amount {
  color: #e6e9ef;
}
</style>
