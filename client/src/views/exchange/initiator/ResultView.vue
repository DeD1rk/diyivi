<script setup lang="ts">
import type { InitiatorExchangeResponse, ExchangeReply } from '@/api/types'
import Title from '@/components/Title.vue'
import { attributeDisplayOptions } from '@/lib/attributes'

const props = defineProps<{
  exchange: InitiatorExchangeResponse
  reply: ExchangeReply
}>()
</script>
<template>
  <div class="p-8">
    <Title>Uitwisseling gelukt</Title>
    <p>
      Gefeliciteerd! Iemand heeft gereageerd op je verzoek om gegevens uit te wisselen. Dit zijn de
      gegevens die je hebt ontvangen:
    </p>
    <ul class="mt-4">
      <li v-for="(attribute, index) of reply" :key="index">
        <span class="font-semibold">{{ attributeDisplayOptions[attribute.id]?.label }}:</span>
        {{ attribute.value.nl }}
      </li>
    </ul>
    <!-- <p class="mt-4">Dit zijn de gegevens die de ander van jou heeft gekregen:</p> -->
    <!-- <ul class="mt-4">
      <li v-for="(attribute, index) of exchange!." :key="index">
        <span class="font-semibold">{{ attributeDisplayOptions[attribute.id]?.label }}:</span>
        {{ attribute.value.nl }}
      </li>
    </ul> -->
  </div>
</template>
