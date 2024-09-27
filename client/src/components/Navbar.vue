<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <nav class="bg-background shadow-lg w-full sticky top-0">
    <div
      class="max-w-screen-sm lg:max-w-screen-md flex flex-wrap items-center justify-between mx-auto px-8 py-3"
    >
      <div class="flex items-baseline">
        <RouterLink to="/">
          <div class="font-extrabold text-2xl tracking-tighter text-yivi-red">
            <span class="text-black">diy</span>ivi
          </div>
        </RouterLink>
        <div class="text-2xl ms-6 text-muted-foreground font-semibold hidden min-[480px]:inline">
          weet met wie je praat!
        </div>
      </div>
      <div>
        <div>...</div>
      </div>
    </div>
  </nav>
</template>
