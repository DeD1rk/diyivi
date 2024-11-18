<script setup lang="ts">
import type { InitiatorExchangeResponse, ExchangeReply, DisclosedValue } from '@/api/types'
import Title from '@/components/Title.vue'
import DisclosedAttributeList from '@/components/DisclosedAttributeList.vue'

const props = defineProps<{
  exchange: InitiatorExchangeResponse
  reply: ExchangeReply
  initiatorAttributes: DisclosedValue[]
}>()
</script>
<template>
  <div class="p-8">
    <Title>Elkaar leren kennen</Title>
    <p>
      Gefeliciteerd! Iemand heeft gereageerd op je verzoek om gegevens uit te wisselen. Dit zijn de
      gegevens die je hebt ontvangen:
    </p>
    <DisclosedAttributeList class="mt-4" :attributes="reply" />
    <p class="mt-4">Dit zijn de gegevens die de ander van jou heeft gekregen:</p>
    <DisclosedAttributeList class="mt-4" :attributes="initiatorAttributes" />
  </div>
</template>
