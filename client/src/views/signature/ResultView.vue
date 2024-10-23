<script setup lang="ts">
import { computed } from 'vue'
import Header from '@/components/Header.vue'
import type { DisclosedValue } from '@/api/types'
import AttributeList from '@/components/AttributeList.vue'

const props = defineProps<{
  message: string
  signature: string
  disclosed: DisclosedValue[]
}>()

const signatureLines = computed(() => {
  const base64 = window.btoa(props.signature)
  const numLines = Math.ceil(base64.length / 64)
  const lines = new Array(numLines)
  for (let i = 0; i < numLines; ++i) {
    lines[i] = base64.slice(64 * i, 64 * i + 64)
  }
  return lines
})
const verifyUrl = window.origin + '/verify/'
</script>

<template>
  <Header>Gelukt!</Header>
  <p>Je hebt het bericht ondertekend met de volgende gegevens:</p>
  <AttributeList class="mt-4" :attributes="disclosed" />
  <p>Hier is het ondertekende bericht:</p>
  <div
    class="font-mono select-all break-normal bg-yivi-lightblue rounded-md p-4 text-sm overflow-x-scroll"
  >
    Onderstaande bericht is ondertekend met Yivi. Yivi is een identiteitsapp waarmee je makkelijk en
    veilig inlogt, gegevens deelt en bewijst wie je bent.
    <br />
    Controleer de handtekening op {{ verifyUrl }}. Alleen dan weet je zeker of het bericht echt
    ondertekend is. Je ziet daar ook door wie en wanneer de handtekening gemaakt is.
    <br />
    <br />
    ----- MESSAGE -----
    <br />
    <br />
    <div class="whitespace-break-spaces">{{ message }}</div>
    <br />
    <br />
    ----- BEGIN YIVI SIGNATURE -----
    <br />
    <div class="text-xs">
      <template v-for="(line, index) in signatureLines" :key="index"><br />{{ line }}</template>
    </div>
    <br />
    ----- END YIVI SIGNATURE -----
  </div>
</template>
