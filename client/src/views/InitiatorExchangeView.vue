<script setup lang="ts">
import { provide, ref } from 'vue'
import { RouterView } from 'vue-router'
import { initiatorExchangeKey } from '@/lib/keys'
import type { InitiatorExchangeResponse } from '@/api/types'

const exchange = ref<InitiatorExchangeResponse | null>(null)

provide(initiatorExchangeKey, exchange)
</script>

<template>
  <RouterView />
</template>
