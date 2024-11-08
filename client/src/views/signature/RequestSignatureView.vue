<script setup lang="ts">
import { ref } from 'vue'
import type { SignatureRequestResponse } from '@/api/types'
import CreateView from './request/CreateView.vue'
import StartView from './request/StartView.vue'
import SendView from './request/SendView.vue'
import Title from '@/components/Title.vue'

const request = ref<SignatureRequestResponse | null>(null)
const started = ref<boolean>(false)
</script>

<template>
  <div class="p-8">
    <Title>Afspraken vastleggen: vraag iemand anders</Title>
    <p>
      Stel een afspraak voor, om door iemand anders te laten ondertekenen. Jij kiest eerst de tekst
      van de afspraak, en de gegevens waarmee de afspraak ondertekend moet worden. Dan deel je je
      e-mailadres met de Yivi app, en verstuur je een verzoek naar degene die de afspraak gaat
      ondertekenen. Ten slotte krijg je een e-mail met de ondertekende afspraak.
    </p>
    <CreateView v-if="!request" @created="(r) => (request = r)" />
    <StartView v-else-if="!started" :request @started="() => (started = true)" />
    <SendView v-else :request />
  </div>
</template>
