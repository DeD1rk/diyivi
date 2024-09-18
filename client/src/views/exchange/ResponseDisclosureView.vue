<script setup lang="ts">
import { onMounted } from 'vue'

// @ts-ignore
import yivi from '@privacybydesign/yivi-frontend'
import type { RecipientExchangeResponse, RecipientResponseResponse } from '@/api/types'
import client from '@/api'
import { useToast } from '@/components/ui/toast'

const props = defineProps<{
  exchangeId: string
  exchange: RecipientExchangeResponse
}>()

const emit = defineEmits<{
  result: [result: RecipientResponseResponse]
}>()

const { toast } = useToast()

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
    const disclosure_result: string = await disclosure.start()
    const { data, error } = await client.POST('/api/exchanges/{exchange_id}/respond/', {
      params: {
        path: {
          exchange_id: props.exchangeId
        }
      },
      body: {
        disclosure_result: disclosure_result
      }
    })
    if (data) {
      emit('result', data)
    } else {
      toast({
        title: 'Oeps! Er ging iets mis',
        description: 'Er is iets misgegaan bij het reageren op de uitwisseling.'
      })
      console.error(error)
    }
  } catch (error) {
    toast({
      title: 'Oeps! Er ging iets mis',
      description: 'Er is iets misgegaan bij het reageren op de uitwisseling.'
    })
    console.error(error)
  }
})
</script>

<template>
  <div class="flex justify-center mt-16">
    <div id="yivi-web-form"></div>
  </div>
</template>
