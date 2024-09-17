<script setup lang="ts">
import { defineEmits, onMounted, ref } from 'vue'
import type { InitiatorExchangeResponse } from '@/api/types'
import { useToast } from '@/components/ui/toast'

// @ts-ignore
import yivi from '@privacybydesign/yivi-frontend'
import client from '@/api'

const props = defineProps<{
  exchange: InitiatorExchangeResponse
}>()
const emit = defineEmits<{
  started: []
}>()

const { toast } = useToast()

const exchangeStarted = ref(false)

onMounted(async () => {
  const disclosure = yivi.newWeb({
    debugging: true,
    session: {
      url: import.meta.env.VITE_YIVI_URL || `${window.origin}/yivi`,
      start: {
        method: 'POST',
        headers: {
          'Content-Type': 'text/plain'
        },
        body: props.exchange.request_jwt
      },
      result: {
        // @ts-ignore
        url: (o, { sessionPtr, sessionToken }) => `${o.url}/session/${sessionToken}/result-jwt`,
        // @ts-ignore
        parseResponse: (r) => r.text()
      }
    }
  })

  try {
    const result: string = await disclosure.start()
    const { error } = await client.POST('/api/exchanges/{exchange_id}/start/', {
      params: {
        path: {
          exchange_id: props.exchange.id
        }
      },
      body: {
        initiator_secret: props.exchange.initiator_secret,
        disclosure_result: result
      }
    })
    if (error) {
      toast({
        title: 'Oeps! Er ging iets mis',
        description: 'Er is iets misgegaan bij het beginnen van de uitwisseling.'
      })
      console.error(error)
    } else {
      exchangeStarted.value = true
      emit('started')
      console.log(
        'Send this to the other party:',
        `${window.origin}/exchange/respond/${props.exchange.id}/`
      )
    }
  } catch (error) {
    toast({
      title: 'Oeps! Er ging iets mis',
      description: 'Er is iets misgegaan bij het beginnen van de uitwisseling.'
    })
    console.error(error)
  }
})
</script>

<template>
  <div class="p-8">
    <h1 class="text-xl font-bold mt-4 mb-2">Uitwisseling beginnen</h1>
    <p>Toon nu je eigen gegevens met Yivi.</p>
    <div class="flex justify-center mt-16">
      <div id="yivi-web-form"></div>
    </div>
  </div>
</template>
