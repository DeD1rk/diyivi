<script setup lang="ts">
import Header from '@/components/Header.vue'
import { Mail } from 'lucide-vue-next'
import { useToast } from '@/components/ui/toast'
import WhatsApp from '@/components/icons/WhatsApp.vue'
import { Button } from '@/components/ui/button'
import { computed } from 'vue'
import type { SignatureRequestResponse } from '@/api/types'
import RawLinkDisplay from '@/components/RawLinkDisplay.vue'

const props = defineProps<{
  request: SignatureRequestResponse
}>()

const respondUrl = computed(() => `${window.origin}/signature/request/respond/${props.request.id}/`)

const mailtoUrl = computed(() => {
  const subject = 'Afspraak ondertekenen met DIYivi'
  const body =
    'Ik wil graag dat je een afspraak ondertekent met DIYivi.\n' +
    'Open deze link om de afspraak te bekijken, en eventueel te ondertekenen:\n\n'

  return `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body + respondUrl.value)}`
})
const whatsappUrl = computed(() => {
  const content =
    'Ik wil graag dat je een afspraak ondertekent met DIYivi.\n' +
    'Open deze link om de afspraak te bekijken, en eventueel te ondertekenen:\n\n'

  return `whatsapp://send?text=${encodeURIComponent(content + respondUrl.value)}`
})
</script>
<template>
  <Header>Stap 4: Verstuur de link</Header>
  <p>
    Dankjewel! Je kunt nu een verzoek sturen om de afspraak te ondertekenen. Laat de andere partij
    de onderstaande link openen en de instructies volgen. Als de ontvanger de afspraak ondertekend
    heeft ontvang je een e-mail met de handtekening.
  </p>
  <RawLinkDisplay :link="respondUrl" copyMessage="Je uitnodiging is gekopieerd." class="mt-4" />
  <div id="share-buttons" class="mt-4 flex gap-2">
    <Button as-child>
      <a :href="whatsappUrl"><WhatsApp class="w-4 h-4 me-2" />Verstuur met WhatsApp</a>
    </Button>
    <Button as-child>
      <a :href="mailtoUrl"><Mail class="w-4 h-4 me-2" />Stuur e-mail</a>
    </Button>
  </div>
</template>
