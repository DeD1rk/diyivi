<script setup lang="ts">
import client from '@/api'
import type { InitiatorExchangeResponse, ExchangeReply } from '@/api/types'
import Title from '@/components/Title.vue'
import Header from '@/components/Header.vue'
import { useToast } from '@/components/ui/toast'
import { useTimeoutPoll } from '@vueuse/core'
import { computed } from 'vue'

const emit = defineEmits<{
  replied: [reply: ExchangeReply]
}>()

const props = defineProps<{
  exchange: InitiatorExchangeResponse
}>()

const { toast } = useToast()
const respondUrl = computed(() => {
  return `${window.origin}/exchange/respond/${props.exchange.id}/`
})

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

const { isActive, pause, resume } = useTimeoutPoll(getResult, 3000, { immediate: true })
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
    <div class="font-mono bg-muted py-2 px-4 mt-4">
      {{ respondUrl }}
    </div>
    <div>De ontvanger heeft nog niet op je uitnodiging gereageerd...</div>
  </div>
</template>
