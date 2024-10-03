<script setup lang="ts">
import client from '@/api'
import type { InitiatorExchangeResponse, ExchangeReply } from '@/api/types'
import Title from '@/components/Title.vue'
import Header from '@/components/Header.vue'
import { Copy, Mail } from 'lucide-vue-next'
import { useToast } from '@/components/ui/toast'
import WhatsApp from '@/components/icons/WhatsApp.vue'
import { Button } from '@/components/ui/button'
import { useTimeoutPoll } from '@vueuse/core'
import { computed } from 'vue'

const emit = defineEmits<{
  replied: [reply: ExchangeReply]
}>()

const props = defineProps<{
  exchange: InitiatorExchangeResponse
  publicAttribute: string
}>()

const { toast } = useToast()
const respondUrl = computed(() => `${window.origin}/exchange/respond/${props.exchange.id}/`)

const mailtoUrl = computed(() => {
  const subject = 'Elkaar leren kennen met DIYivi'
  const body =
    'Ik wil je graag met zekerheid leren kennen met DIYivi.\n' +
    'Open deze link om privacy-vriendelijk persoonlijke gegevens met me uit te wisselen:\n\n'

  return `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body + respondUrl.value)}`
})
const whatsappUrl = computed(() => {
  const content =
    'Ik wil je graag met zekerheid leren kennen met DIYivi.\n' +
    'Open deze link om privacy-vriendelijk persoonlijke gegevens met me uit te wisselen:\n\n'

  return `whatsapp://send?text=${encodeURIComponent(content + respondUrl.value)}`
})
async function copyLink() {
  await navigator.clipboard.writeText(respondUrl.value)
  toast({
    description: 'Je uitnodiging is gekopieerd.'
  })
}

async function getResult() {
  try {
    const { data } = await client.GET('/api/exchanges/{exchange_id}/result/', {
      params: {
        path: {
          exchange_id: props.exchange.id
        },
        query: {
          secret: props.exchange.initiator_secret
        }
      }
    })
    if (data) {
      if (data.replies.length === 1) {
        emit('replied', data.replies[0]!)
      } else if (data.replies.length > 1) {
        // TODO: distinguish between 1-to-1, 1-to-many and many-to-many exchanges.
        toast({
          title: 'Oeps! Er ging iets mis',
          description: 'Er is iets misgegaan bij het ophalen van de status van je uitwisseling.'
        })
      }
    } else {
      toast({
        title: 'Oeps! Er ging iets mis',
        description: 'Er is iets misgegaan bij het ophalen van de status van je uitwisseling.'
      })
    }
  } catch (error) {
    toast({
      title: 'Oeps! Er ging iets mis',
      description: 'Er is iets misgegaan bij het ophalen van de status van je uitwisseling.'
    })
  }
}

useTimeoutPoll(getResult, 3000, { immediate: true })
</script>
<template>
  <div class="p-8">
    <Title>Elkaar leren kennen </Title>
    <p>
      Jij neemt het initiatief. Jij kiest welke persoonlijke details je met een andere persoon uit
      wil wisselen. Je toont eerst jouw eigen persoonlijke gegevens aan deze website. Daarna krijg
      je een link om naar de ander te sturen. Pas als die andere persoon ook dezelfde gegevens aan
      deze website onthult, krijgen jullie allebei elkaars gegevens te zien.
    </p>
    <Header>Stap 4: Verstuur de link</Header>
    <p>
      Dankjewel! Je kunt nu een uitnodiging voor deze uitwisseling versturen. Laat de ontvanger de
      onderstaande link openen en de instructies volgen. Als de ontvanger dat gedaan heeft, krijgen
      jullie elkaars gegevens te zien. Je ziet de gegevens dan hieronder, en krijgt ze per e-mail
      toegestuurd.
    </p>
    <div class="font-mono bg-yivi-lightblue py-2 px-4 mt-4 break-all select-all">
      {{ respondUrl
      }}<button @click="copyLink">
        <Copy class="inline ms-2 w-4 h-4 hover:scale-110 transition" />
      </button>
    </div>
    <div id="share-buttons" class="mt-4 flex gap-2">
      <Button as-child v-if="publicAttribute === 'mobilenumber'"
        ><a :href="whatsappUrl"><WhatsApp class="w-4 h-4 me-2" />Verstuur met WhatsApp</a></Button
      >
      <Button as-child v-else-if="publicAttribute === 'email'"
        ><a :href="mailtoUrl"><Mail class="w-4 h-4 me-2" />Stuur e-mail</a></Button
      >
    </div>
    <div class="mt-4">
      De ontvanger heeft nog niet op je uitnodiging gereageerd<span class="animate-pulse">.</span
      ><span class="animate-pulse delay-150">.</span><span class="animate-pulse delay-300">.</span>
    </div>
  </div>
</template>
