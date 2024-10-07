<script setup lang="ts">
import { computed, ref } from 'vue'
import client from '@/api'
import type { RecipientExchangeResponse, RecipientResponseResponse } from '@/api/types'
import { useToast } from '@/components/ui/toast'
import { Button } from '@/components/ui/button'
import router from '@/router'

import ConfirmationDialog from '@/components/ConfirmationDialog.vue'
import ResponseDisclosureView from './ResponseDisclosureView.vue'
import { attributeDisplayOptions, publicAttributeDisplayOptions } from '@/lib/attributes'
import Title from '@/components/Title.vue'
import AttributeList from '@/components/AttributeList.vue'

const props = defineProps<{
  exchangeId: string
}>()

const { toast } = useToast()

const isLoading = ref(true)
const notFound = ref(false)
const exchange = ref<RecipientExchangeResponse | null>(null)
const confirmed = ref(false)
const result = ref<RecipientResponseResponse | null>(null)

async function loadExchange() {
  try {
    const { data } = await client.GET('/api/exchanges/{exchange_id}/', {
      params: {
        path: {
          exchange_id: props.exchangeId
        }
      }
    })
    if (data) {
      exchange.value = data
    } else {
      notFound.value = true
    }
  } catch (error) {
    toast({
      title: 'Oeps! Er ging iets mis',
      description: 'Er is iets misgegaan bij het aanmaken van de uitwisseling.'
    })
  } finally {
    isLoading.value = false
  }
}

const cancelDialogOpen = ref(false)
const continueDialogOpen = ref(false)

const firstAttribute = computed(() => {
  if (!exchange.value) return null
  for (let [id, label] of Object.entries(publicAttributeDisplayOptions)) {
    let disclosedValue = exchange.value.public_initiator_attribute_values.find((v) => v.id === id)
    if (disclosedValue) return { ...label, value: disclosedValue.value }
  }
  return null
})

loadExchange()
</script>
<template>
  <div class="p-8">
    <div v-if="isLoading" class="flex justify-center">Aan het laden...</div>
    <template v-else-if="notFound">
      <Title>Uitnodiging niet gevonden</Title>
      <p>De uitnodiging die je probeert te openen bestaat niet meer of is al voltooid.</p>
    </template>
    <template v-else-if="!result">
      <Title>Elkaar leren kennen</Title>
      <p>
        Iemand
        <template v-if="firstAttribute"
          >met {{ firstAttribute.label }}
          <span class="font-semibold">{{ firstAttribute.value.nl }}</span></template
        >
        wil graag gegevens met je uitwisselen. Als je hiermee akkoord gaat krijgen jullie de
        volgende gegevens van elkaar te zien:
      </p>
      <ul class="list-disc list-inside mt-4 ps-2 font-semibold">
        <template v-for="(option, index) of attributeDisplayOptions">
          <li
            v-if="option.requiredAttributes.every((id) => exchange!.attributes.includes(id))"
            :key="index"
          >
            {{ option.label }}
          </li>
        </template>
      </ul>
      <template v-if="!confirmed">
        <p class="mt-4 font-semibold">Wil je deze gegevens delen?</p>
        <div class="flex gap-4 mt-4">
          <Button variant="outline" @click="() => (cancelDialogOpen = true)"
            >Nee, liever niet</Button
          >
          <Button @click="() => (continueDialogOpen = true)">Ja, ga door</Button>
        </div>
      </template>
      <ResponseDisclosureView
        v-else
        :exchangeId
        :exchange="exchange!"
        @result="(r) => (result = r)"
      ></ResponseDisclosureView>
    </template>
    <template v-else>
      <Title>Elkaar leren kennen</Title>
      <p>
        Gefeliciteerd! Je hebt gegevens uitgewisseld. Dit zijn de gegevens die je van de ander hebt
        ontvangen:
      </p>
      <AttributeList class="mt-4" :attributes="result!.initiator_attribute_values" />
      <p class="mt-4">Dit zijn de gegevens die de ander van jou heeft gekregen:</p>
      <AttributeList class="mt-4" :attributes="result!.response_attribute_values" />
    </template>
  </div>
  <ConfirmationDialog
    title="Geen gegevens delen?"
    v-model="cancelDialogOpen"
    @confirm="() => router.push('/')"
  >
    <template #description>
      Je hoeft je gegevens niet te delen als je dat niet wil. Als je niets deelt, krijgen jij en
      degene die de uitnodiging heeft gemaakt elkaars gegevens niet te zien.
    </template>
    <template #confirm>Deel niets</template>
  </ConfirmationDialog>
  <ConfirmationDialog
    :title="`Herken je ${firstAttribute?.value.nl}?`"
    v-model="continueDialogOpen"
    @confirm="() => (confirmed = true)"
  >
    <template #description>
      <p>
        Heb je de link naar deze pagina gekregen van iemand
        <template v-if="firstAttribute"
          >met {{ firstAttribute.label }}
          <span class="font-semibold">{{ firstAttribute.value.nl }}</span></template
        >?
      </p>
      <p class="mt-2">
        Als je de uitnodiging
        <i>niet</i> via dat {{ firstAttribute?.label }} hebt gekregen, dan probeert iemand zich
        misschien voor te doen als een ander. Deel dan je gegevens niet!
      </p>
    </template>
  </ConfirmationDialog>
</template>
