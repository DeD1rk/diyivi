<script setup lang="ts">
import client from '@/api'
import type { InitiatorExchangeResponse, ExchangeReply } from '@/api/types'
import Title from '@/components/Title.vue'
import { useToast } from '@/components/ui/toast'
import { useTimeoutPoll } from '@vueuse/core'
import { computed } from 'vue'
import { Loader2 } from 'lucide-vue-next'

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
    <Title>Versturen</Title>
    <p>
      Dankjewel! Je kunt nu een uitnodiging voor deze uitwisseling versturen. Laat de ontvanger de
      onderstaande link openen en de instructies volgen. Als de ontvanger dat gedaan heeft, krijgen
      jullie elkaars gegevens te zien.
    </p>
    <div class="font-mono bg-muted py-2 px-4 mt-4">
      {{ respondUrl }}
    </div>
    <div>De ontvanger heeft nog niet op je uitnodiging gereageerd...</div>
  </div>
</template>
