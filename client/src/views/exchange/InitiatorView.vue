<script setup lang="ts">
import { ref } from 'vue'
import type { InitiatorExchangeResponse, ExchangeReply } from '@/api/types'
import ExchangeCreateView from './initiator/CreateView.vue'
import ExchangeStartView from './initiator/StartView.vue'
import SendView from './initiator/SendView.vue'
import ResultView from './initiator/ResultView.vue'

const exchange = ref<InitiatorExchangeResponse | null>(null)
const publicAttribute = ref<string | null>(null)
const started = ref<boolean>(false)
const reply = ref<ExchangeReply | null>(null)
</script>

<template>
  <ExchangeCreateView
    v-if="!exchange || !publicAttribute"
    @created="
      (e, attribute) => {
        exchange = e
        publicAttribute = attribute
      }
    "
  />
  <ExchangeStartView v-else-if="!started" :exchange @started="() => (started = true)" />
  <SendView v-else-if="reply === null" :exchange :publicAttribute @replied="(r) => (reply = r)" />
  <ResultView v-else :exchange :reply />
</template>
