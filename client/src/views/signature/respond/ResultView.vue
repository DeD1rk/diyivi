<script setup lang="ts">
import { computed } from 'vue'
import Header from '@/components/Header.vue'
import type { DisclosedValue } from '@/api/types'
import DisclosedAttributeList from '@/components/DisclosedAttributeList.vue'
import RawLinkDisplay from '@/components/RawLinkDisplay.vue'
import PlainMessageDisplay from '@/components/PlainMessageDisplay.vue'

const props = defineProps<{
  signature: string
  disclosed: DisclosedValue[]
  initiatorEmail: string | null
}>()
const verifyUrl = window.origin + '/signature/verify/'

const signatureText = computed(() => {
  return verifyUrl + '#' + window.btoa(props.signature)
})
</script>

<template>
  <Header>Afspraak vastleggen: verzoek</Header>
  <p>
    Gelukt! Je hebt het bericht ondertekend. Je handtekening is naar
    <span class="font-semibold">{{ initiatorEmail }}</span> gestuurd.
  </p>
  <p>Dit zijn de gegevens van jou waarmee je getekend hebt:</p>
  <DisclosedAttributeList class="mt-4" :attributes="disclosed" />
  <p class="my-4">
    Hieronder vind je het ondertekende bericht. Om het te lezen en te zien door wie de afspraak
    ondertekend is, kan iemand hem invullen op
    <a :href="verifyUrl" class="font-mono" target="_blank">{{ verifyUrl }}</a
    >. Het ondertekende bericht zelf is ook een link naar deze pagina, dus men kan deze link
    simpelweg openen. Geef deze instructie mee aan de ontvanger van het ondertekende bericht, zodat
    die weet hoe hij het bericht kan lezen en de handtekening kan controleren.
  </p>
  <RawLinkDisplay
    :link="signatureText"
    copyMessage="Je ondertekende bericht is gekopieerd."
    class="text-xs"
  />
</template>
