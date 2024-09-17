<script setup lang="ts">
import { computed, ref } from 'vue'
import type { InitiatorExchangeResponse } from '@/api/types'
import ExchangeCreateView from './ExchangeCreateView.vue'
import ExchangeStartView from './ExchangeStartView.vue'

const exchange = ref<InitiatorExchangeResponse | null>(null)
const started = ref<boolean>(false)
const respondUrl = computed(() => {
  if (!exchange.value) return ''
  return `${window.origin}/exchange/respond/${exchange.value.id}/`
})
</script>

<template>
  <ExchangeCreateView v-if="!exchange" @created="(e) => (exchange = e)" />
  <ExchangeStartView v-else-if="!started" :exchange="exchange" @started="() => (started = true)" />
  <div class="p-8" v-else>
    <h1 class="text-xl font-bold mt-4 mb-2">Versturen</h1>
    <p>
      Dankjewel! Je kunt nu een uitnodiging voor deze uitwisseling versturen. Laat de ontvanger de
      onderstaande link openen en de instructies volgen. Als de ontvanger dat gedaan heeft, krijgen
      jullie elkaars gegevens te zien.
    </p>
    <div class="font-mono bg-muted py-2 px-4 mt-4">
      {{ respondUrl }}
    </div>
  </div>
</template>
