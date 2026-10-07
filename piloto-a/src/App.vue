<script setup lang="ts">
import { ref } from 'vue'
import MicroSesionIsidora from './components/MicroSesionIsidora.vue'

const show = ref(true)
</script>

<template>
  <MicroSesionIsidora v-if="show" @close="show = false" @complete="show = false" />
</template>
