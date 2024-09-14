<script setup lang="ts">
import { inject } from 'vue'
import { RouterLink } from 'vue-router'
import { initiatorExchangeKey } from '@/lib/keys'
import { Button } from '@/components/ui/button'
import { AlertCircle } from 'lucide-vue-next'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'

// @ts-ignore
import yivi from '@privacybydesign/yivi-frontend'

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
      }
    }
  })

  try {
    const result = await disclosure.start()
    console.log('Successful disclosure! 🎉', result)
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
