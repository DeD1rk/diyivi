<script setup lang="ts">
import { inject } from 'vue'
import { RouterLink } from 'vue-router'
import { initiatorExchangeKey } from '@/lib/keys'
import { Button } from '@/components/ui/button'
import { AlertCircle } from 'lucide-vue-next'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'

// @ts-ignore
import yivi from '@privacybydesign/yivi-frontend'
import client from '@/api'

async function startExchange() {
  const disclosure = yivi.newWeb({
    debugging: true,
    session: {
      url: import.meta.env.VITE_YIVI_URL || `${window.origin}/yivi`,
      start: {
        method: 'POST',
        headers: {
          'Content-Type': 'text/plain'
        },
        body: exchange.value?.request_jwt
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
    console.info('Successful disclosure! 🎉', result)
    const { error } = await client.POST('/api/exchanges/{exchange_id}/start/', {
      params: {
        path: {
          exchange_id: exchange.value!.id
        }
      },
      body: {
        initiator_secret: exchange.value!.initiator_secret,
        disclosure_result: result
      }
    })
    if (error) {
      console.error('Error starting exchange', error)
    }
  } catch (error) {
    console.error("Couldn't do what you asked 😢", error)
  }
}

const exchange = inject(initiatorExchangeKey)!
</script>
<template>
  <Alert v-if="!exchange" variant="destructive" class="m-5">
    <AlertCircle class="w-4 h-4" />
    <AlertTitle>Error</AlertTitle>
    <AlertDescription
      >Er is geen uitwisseling gestart.
      <RouterLink class="underline" to="/exchange/create/">
        Begin een nieuwe uitwisseling.
      </RouterLink>
    </AlertDescription>
  </Alert>
  <div class="p-5" v-else>
    <h1 class="text-xl font-bold pt-4 pb-2">Uitwisseling beginnen</h1>
    <p class="">Open in yivi</p>
    <div>
      <Button @click="startExchange"> Start </Button>
    </div>

    <div id="yivi-web-form"></div>
  </div>
</template>
