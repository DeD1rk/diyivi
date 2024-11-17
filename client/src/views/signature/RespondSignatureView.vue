<script setup lang="ts">
import { ref } from 'vue'
import client from '@/api'
import type { DisclosedValue, RecipientSignatureRequestResponse } from '@/api/types'
import { useToast } from '@/components/ui/toast'
import { Button } from '@/components/ui/button'
import router from '@/router'

import ConfirmationDialog from '@/components/ConfirmationDialog.vue'
import RequestedAttributeList from '@/components/RequestedAttributeList.vue'
import Title from '@/components/Title.vue'
import SignView from './respond/SignView.vue'
import ResultView from './respond/ResultView.vue'
import PlainMessageDisplay from '@/components/PlainMessageDisplay.vue'

const props = defineProps<{
  requestId: string
}>()

const { toast } = useToast()

const isLoading = ref(true)
const notFound = ref(false)
const confirmed = ref(false)
const request = ref<RecipientSignatureRequestResponse | null>(null)
const result = ref<{
  signature: string
  disclosed: DisclosedValue[]
} | null>(null)

async function loadRequest() {
  try {
    const { data } = await client.GET('/api/signatures/requests/{request_id}/', {
      params: {
        path: {
          request_id: props.requestId
        }
      }
    })
    if (data) {
      request.value = data
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

loadRequest()
</script>
<template>
  <div class="p-8">
    <div v-if="isLoading" class="flex justify-center">Aan het laden...</div>
    <template v-else-if="notFound">
      <Title>Verzoek niet gevonden</Title>
      <p>
        Het verzoek om te ondertekenen dat je probeert te openen bestaat niet meer of is al
        voltooid.
      </p>
    </template>
    <template v-else-if="!result">
      <Title>Afspraken vastleggen: verzoek</Title>
      <p>
        Iemand met e-mailadres
        <span class="font-semibold">{{ request!.initiator_email_value }}</span> wil graag dat je de
        volgende afspraak ondertekent met Yivi. Als je besluit te ondertekenen, wordt je
        handtekening naar dat e-mailadres opgestuurd.
      </p>
      <PlainMessageDisplay>
        {{ request!.message }}
      </PlainMessageDisplay>
      <p>Dit zijn de gegevens waarmee je verzocht wordt te ondertekenen:</p>
      <RequestedAttributeList :attributes="request!.attributes" />

      <template v-if="!confirmed">
        <p class="mt-4 font-semibold">Wil je de afspraak ondertekenen?</p>
        <div class="flex gap-4 mt-4">
          <Button variant="outline" @click="() => (cancelDialogOpen = true)"
            >Nee, liever niet</Button
          >
          <Button @click="() => (confirmed = true)">Ja, ga door</Button>
        </div>
      </template>
      <SignView
        v-else
        :requestId
        :request="request!"
        @signed="(s, attrs) => (result = { signature: s, disclosed: attrs })"
      ></SignView>
    </template>
    <ResultView
      v-else
      :signature="result.signature"
      :disclosed="result.disclosed"
      :initiatorEmail="request!.initiator_email_value"
    />
  </div>
  <ConfirmationDialog
    title="Niet ondertekenen?"
    v-model="cancelDialogOpen"
    @confirm="() => router.push('/')"
  >
    <template #description>
      Je hoeft de afspraak niet te ondertekenen als je dat niet wil, of als je de gevraagde gegevens
      niet wil delen.
    </template>
    <template #confirm>Onderteken niet</template>
  </ConfirmationDialog>
</template>
