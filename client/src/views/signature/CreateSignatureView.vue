<script setup lang="ts">
import { ref } from 'vue'
import CreateView from './CreateView.vue'
import SignView from './SignView.vue'
import Title from '@/components/Title.vue'
import ResultView from './ResultView.vue'
import type { DisclosedValue } from '@/api/types'

const message = ref<string | null>(null)
const selectedAttributes = ref(new Set<string>())
const signature = ref<string | null>(null)
const disclosed = ref<DisclosedValue[] | null>(null)
</script>

<template>
  <div class="p-8">
    <Title>Afspraken vastleggen</Title>
    <p>
      Onderteken een afspraak. Stel de afspraak op, kies de gegevens waarmee je wilt onderteken, en
      zet je handtekening met je Yivi app.
    </p>
    <CreateView
      v-if="!message"
      @created="
        (m, attributes) => {
          message = m
          selectedAttributes = attributes
        }
      "
    />
    <SignView
      v-else-if="!signature || !disclosed"
      :message
      :selectedAttributes
      @signed="
        (_, s, d) => {
          signature = s
          disclosed = d
        }
      "
    />
    <ResultView v-else :signature :message :disclosed />
  </div>
</template>
