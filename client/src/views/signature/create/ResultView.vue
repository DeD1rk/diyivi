<script setup lang="ts">
import { computed } from 'vue'
import Header from '@/components/Header.vue'
import type { DisclosedValue } from '@/api/types'
import AttributeList from '@/components/AttributeList.vue'
import RawLinkDisplay from '@/components/RawLinkDisplay.vue'

const props = defineProps<{
  message: string
  signature: string
  disclosed: DisclosedValue[]
}>()
const verifyUrl = window.origin + '/signature/verify/'

const signatureText = computed(() => {
  return verifyUrl + '#' + window.btoa(props.signature)
})
</script>

<template>
  <Header>Gelukt!</Header>
  <p>Je hebt het bericht ondertekend met de volgende gegevens van jou:</p>
  <AttributeList class="mt-4" :attributes="disclosed" />
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
