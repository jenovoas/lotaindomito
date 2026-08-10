<script setup lang="ts">
import WalletHUD from '@/components/WalletHUD.vue'
</script>

<template>
  <div class="home">
    <header class="home-header">
      <WalletHUD />
    </header>
    <main class="home-content">
      <h1>Lota Indómito</h1>
      <p class="tagline">Guardianes de la Cuenca</p>
    </main>
  </div>
</template>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.home-header {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 12px 16px;
  background: #0f1216;
  border-bottom: 1px solid #21262d;
}

.home-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex: 1;
  text-align: center;
  padding: 16px;
}

.home h1 {
  font-size: 2.5rem;
  color: #3fe6c0;
}

.home .tagline {
  color: #8b949e;
  font-size: 1.2rem;
}
</style>
