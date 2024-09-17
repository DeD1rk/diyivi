<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { Button } from '@/components/ui/button'
</script>

<template>
  <div class="p-8">
    Hallo!
    <Button as-child>
      <RouterLink to="/exchange/start/">Begin een uitwisseling</RouterLink>
    </Button>
  </div>
</template>
