<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { Button } from '@/components/ui/button'
</script>

<template>
  <div class="p-5">
    Hallo!
    <Button as-child>
      <RouterLink to="/exchange/create/">Begin een uitwisseling</RouterLink>
    </Button>
  </div>
</template>
