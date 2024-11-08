<script setup lang="ts">
import { onMounted, ref } from 'vue'
import type { InitiatorExchangeResponse, SignatureRequestResponse } from '@/api/types'
import { useToast } from '@/components/ui/toast'
import Title from '@/components/Title.vue'
import Header from '@/components/Title.vue'
import client from '@/api'

// @ts-ignore
import yivi from '@privacybydesign/yivi-frontend'

const props = defineProps<{
  request: SignatureRequestResponse
}>()
const emit = defineEmits<{
  started: []
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
        body: props.request.request_jwt
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
    const { error } = await client.POST('/api/signatures/requests/{request_id}/start/', {
      params: {
        path: {
          request_id: props.request.id
        }
      },
      body: {
        disclosure_result: result
      }
    })
    if (error) {
      toast({
        title: 'Oeps! Er ging iets mis',
        description: 'Er is iets misgegaan bij het tonen van je e-mail.'
      })
      console.error(error)
    } else {
      emit('started')
      console.log(
        'Send this to the other party:',
        `${window.origin}/signature/request/respond/${props.request.id}/`
      )
    }
  } catch (error) {
    toast({
      title: 'Oeps! Er ging iets mis',
      description: 'Er is iets misgegaan bij het tonen van je e-mail.'
    })
    console.error(error)
  }
})
</script>

<template>
  <Header>Stap 3: Deel je eigen e-mailadres</Header>
  <p>Toon je eigen e-mailadres met Yivi. Daar wordt het ondertekende bericht naar opgestuurd.</p>
  <div class="flex justify-center mt-16">
    <div id="yivi-web-form"></div>
  </div>
</template>
