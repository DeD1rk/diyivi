<script setup lang="ts">
import { inject } from 'vue'
import { RouterLink } from 'vue-router'
import { initiatorExchangeKey } from '@/lib/keys'
import { Button } from '@/components/ui/button'
import { AlertCircle } from 'lucide-vue-next'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
async function startExchange() {
  // yivi.use(YiviClient)
}

const exchange = inject(initiatorExchangeKey)!

// TODO: use yivi frontend packages to manage the disclosure?
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
