<script setup lang="ts">
import { onUpdated, ref } from 'vue'
import client from '@/api'
import type { RecipientExchangeResponse, RecipientResponseResponse } from '@/api/types'
import { useToast } from '@/components/ui/toast'
import { Button } from '@/components/ui/button'
import router from '@/router'

import ConfirmationDialog from '@/components/confirmation/ConfirmationDialog.vue'
import ResponseDisclosureView from './exchange/ResponseDisclosureView.vue'

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

loadExchange()
</script>
<template>
  <div class="p-8">
    <div v-if="isLoading" class="flex justify-center">Aan het laden...</div>
    <template v-else-if="notFound">
      <h1 class="text-xl font-bold mt-4 mb-2">Uitwisseling niet gevonden</h1>
      <p>De uitwisseling die je probeert te openen bestaat niet meer of is al voltooid.</p>
    </template>
    <template v-else>
      <h1 class="text-xl font-bold mt-4 mb-2">Gegevens uitwisselen</h1>
      <p>
        ... wil graag gegevens met je uitwisselen. Als je hiermee akkoord gaat krijgen jullie de
        volgende gegevens van elkaar te zien:
      </p>
      <ul class="list-disc list-inside mt-4 ps-2 font-semibold">
        <li v-for="(attribute, index) of exchange!.attributes[0]![0]" :key="index">
          {{ attribute }}
        </li>
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
      <ResponseDisclosureView v-else :exchangeId :exchange="exchange!"></ResponseDisclosureView>
    </template>
  </div>
  <ConfirmationDialog
    title="Weet je zeker dat je je gegevens niet wil delen?"
    v-model="cancelDialogOpen"
    @confirm="() => router.push('/')"
  >
    <template #description>
      Je hoeft je gegevens niet te delen als je dat niet wil. Als je niets deelt, krijgen jij en
      degene die de uitnodiging heeft gemaakt elkaars gegevens niet te zien.
    </template>
    <template #confirm>Ja, ik deel niets</template>
  </ConfirmationDialog>
  <ConfirmationDialog
    title="Weet je zeker dat je je gegevens niet wil delen?"
    v-model="continueDialogOpen"
    @confirm="() => (confirmed = true)"
  >
    <template #description>
      <p>Heb je de link naar deze pagina gekregen van iemand met ...?</p>
      <p class="mt-2">
        Als je de uitnodiging
        <i>niet</i> van ... hebt gekregen, dan probeert iemand zich misschien voor te doen als een
        ander. Deel dan je gegevens niet!
      </p>
    </template>
  </ConfirmationDialog>
</template>
