<script setup lang="ts">
import { onMounted } from 'vue'
import { useWorldEventsStore } from '@/stores/worldEvents'

const store = useWorldEventsStore()

onMounted(() => {
  store.init()
})
</script>

<template>
  <div
    v-if="store.eventosActivos.length > 0 || store.eventosProximos.length > 0"
    class="we-banner"
    :style="{
      '--color-primary': (store.eventosActivos[0] || store.eventosProximos[0])?.colores?.primario || '#E63946',
      '--color-secondary': (store.eventosActivos[0] || store.eventosProximos[0])?.colores?.secundario || '#FFD166',
      '--color-bg': (store.eventosActivos[0] || store.eventosProximos[0])?.colores?.fondo || '#1A1A2E',
    }"
  >
    <template v-if="store.eventosActivos.length > 0">
      <div class="we-evento-activo">
        <span class="we-badge-live">EN VIVO</span>
        <div v-for="evt in store.eventosActivos" :key="evt.id" class="we-evento">
          <div class="we-header">
            <h3 class="we-nombre">{{ evt.nombre }}</h3>
            <p class="we-fecha">{{ evt.fecha_inicio }} — {{ evt.fecha_fin }}</p>
          </div>
          <p class="we-desc">{{ evt.descripcion }}</p>
          <div class="we-info-row">
            <span class="we-npc-tag">NPC: {{ evt.npc_exclusiva.nombre }}</span>
            <span
              v-if="evt.misiones[0]?.recompensa_cupon"
              class="we-cupon-tag"
            >
              Cupón: {{ evt.misiones[0].recompensa_cupon.descuento }} en
              {{ evt.misiones[0].recompensa_cupon.comercio }}
            </span>
          </div>
          <div v-if="evt.insignias.length" class="we-insignias-row">
            <span
              v-for="ins in evt.insignias"
              :key="ins.id"
              class="we-insignia"
              :title="ins.descripcion"
            >
              {{ ins.imagen }} {{ ins.nombre }}
            </span>
          </div>
        </div>
      </div>
    </template>

    <template v-else-if="store.eventosProximos.length > 0">
      <div
        v-for="evt in store.eventosProximos.slice(0, 2)"
        :key="evt.id"
        class="we-evento-proximo"
      >
        <span class="we-badge-prox">PRÓXIMO</span>
        <div class="we-header">
          <h3 class="we-nombre">{{ evt.nombre }}</h3>
          <p class="we-fecha">{{ evt.fecha_inicio }} — {{ evt.fecha_fin }}</p>
        </div>
        <p class="we-desc">{{ evt.descripcion }}</p>
        <div class="we-info-row">
          <span class="we-npc-tag">NPC: {{ evt.npc_exclusiva.nombre }}</span>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.we-banner {
  background: var(--color-bg, #1A1A2E);
  border-left: 4px solid var(--color-primary, #E63946);
  padding: 0.5rem 1rem;
  margin: 0.25rem 0;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.we-evento-activo {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.we-evento,
.we-evento-proximo {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.we-header {
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.we-nombre {
  font-size: 1rem;
  font-weight: 700;
  color: var(--color-secondary, #FFD166);
  margin: 0;
}

.we-fecha {
  font-size: 0.75rem;
  color: #8b949e;
  margin: 0;
}

.we-desc {
  font-size: 0.8rem;
  color: #c9d1d9;
  margin: 0;
}

.we-info-row {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.we-npc-tag,
.we-cupon-tag {
  font-size: 0.7rem;
  padding: 0.15rem 0.4rem;
  border-radius: 4px;
  background: rgba(255,255,255,0.08);
}

.we-cupon-tag {
  color: #3FE6C0;
}

.we-insignias-row {
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
  margin-top: 0.2rem;
}

.we-insignia {
  font-size: 0.7rem;
  background: rgba(255,255,255,0.06);
  padding: 0.1rem 0.35rem;
  border-radius: 4px;
  cursor: default;
}

.we-badge-live {
  font-size: 0.6rem;
  font-weight: 700;
  background: #E63946;
  color: white;
  padding: 0.1rem 0.35rem;
  border-radius: 3px;
  align-self: flex-start;
  letter-spacing: 0.05em;
}

.we-badge-prox {
  font-size: 0.6rem;
  font-weight: 700;
  background: var(--color-primary, #E63946);
  color: white;
  padding: 0.1rem 0.35rem;
  border-radius: 3px;
  align-self: flex-start;
  letter-spacing: 0.05em;
}
</style>
