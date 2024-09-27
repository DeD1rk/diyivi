<script setup lang="ts">
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
import Toaster from '@/components/ui/toast/Toaster.vue'
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <Navbar />
    <div class="max-w-screen-sm lg:max-w-screen-md mx-auto bg-background grow w-full">
      <RouterView />
    </div>
  </div>
  <Toaster />
</template>
