<script setup lang="ts">
import { RouterView } from 'vue-router'
import Navbar from './components/navbar/Navbar.vue'
</script>

<template>
  <Navbar />
  <div class="max-w-screen-sm mx-auto">
    <RouterView />
  </div>
</template>
