<script setup lang="ts">
import { computed, ref } from 'vue'
import Title from '@/components/Title.vue'
import Header from '@/components/Header.vue'
import { Textarea } from '@/components/ui/textarea'
import { Button } from '@/components/ui/button'
import { useToast } from '@/components/ui/toast'
import { Loader2 } from 'lucide-vue-next'
import type { DisclosedValue } from '@/api/types'
import AttributeList from '@/components/AttributeList.vue'

const rawMessage = ref<string>('')
const isVerifying = ref<boolean>(false)
const disclosedValues = ref<DisclosedValue[] | null>(null)
const signatureTime = ref<string | null>(null)

const { toast } = useToast()

const placeholder =
  '----- MESSAGE -----\n\n...\n\n\
  ----- BEGIN YIVI SIGNATURE -----\n\n...\n\n----- END YIVI SIGNATURE -----'
const messageRegExp =
  /----- MESSAGE -----\n\n(?<message>[^]*)\n\n----- BEGIN YIVI SIGNATURE -----\n\n(?<signature>([-A-Za-z0-9+/]{64}\n)*[-A-Za-z0-9+/]+={0,3}\n?)\n----- END YIVI SIGNATURE -----/

const wellFormedMessage = computed(() => {
  if (!rawMessage.value.trim()) return null
  const matches = messageRegExp.exec(rawMessage.value.trim())
  if (!matches?.groups?.message || !matches.groups?.signature) return null

  return {
    message: matches.groups.message,
    signature: matches.groups.signature
  }
})

async function verify(message: string, signature: string) {
  try {
    const signatureObject = JSON.parse(window.atob(signature))
    console.log(signatureObject)

    // TODO: Verify signatureObject schema.

    // Put the message back into the irmago SignedMessage.
    signatureObject['message'] = message

    try {
      const response = await fetch(
        (import.meta.env.VITE_YIVI_URL || `${window.origin}/yivi`) + '/verifysignature',
        {
          method: 'POST',
          body: JSON.stringify({
            '@context': 'https://irma.app/ld/request/signatureverification/v1',
            signature: signatureObject
          })
        }
      )
      if (!response.ok) {
        throw new Error('irma server did not respon successfully.')
      }
      const responseBody = await response.json()
      if (responseBody.proofStatus === 'VALID') {
        disclosedValues.value = responseBody.disclosed.flat()
        signatureTime.value = new Date(signatureObject.timestamp.Time * 1000).toLocaleDateString(
          'nl',
          { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }
        )
      } else {
        toast({
          title: 'Handtekening ongeldig!',
          description:
            'Misschien is er iets misgegaan bij het invullen van het bericht, of iemand probeert je voor de gek te houden.',
          variant: 'destructive'
        })
        console.warn('Signature is invalid, respons from irma server:', responseBody)
      }
    } catch (error) {
      toast({
        title: 'Oeps! Er ging iets mis',
        description: 'Er is iets misgegaan bij het controleren.'
      })
      console.error('Signature is malformed:', error)
    }
  } catch (error) {
    toast({
      title: 'AAAAaaaahh! Deze handtekening klopt niet!',
      description: 'Iemand probeert je voor de gek te houden!'
    })
    console.error('Signature is malformed:', error)
  }

  // verify on irmaserver
}
</script>

<template>
  <div class="p-8">
    <Title>Handtekening controleren</Title>
    <p>
      Heb je een bericht dat ondertekend is met DIYivi? Hier kun je de handtekening controlen.
      Alleen als je dat gedaan hebt weet je of, door wie, en wanneer het bericht ondertekend is.
    </p>
    <div v-if="!disclosedValues">
      <Header>Plak het bericht</Header>
      <p>
        Plak hieronder het hele ondertekende bericht. Let op dat je het gehele bericht inclusief
        handtekening plakt, zonder er iets aan te veranderen (ook geen spaties, witregels, etc.).
      </p>

      <Textarea v-model="rawMessage" :placeholder rows="20" class="mt-4" />
      <Button
        class="mt-4"
        :disabled="!wellFormedMessage"
        @click="() => verify(wellFormedMessage!.message, wellFormedMessage!.signature)"
      >
        <Loader2 v-if="isVerifying" class="w-4 h-4 mr-2 animate-spin" />
        Controleer
      </Button>
    </div>
    <div v-else>
      <Header>Handtekening klopt!</Header>
      <p>
        Het bericht is ondertekend op <span class="font-semibold">{{ signatureTime }}.</span>
        Dit zijn de gegevens waarmee het bericht ondertekend is:
      </p>
      <AttributeList :attributes="disclosedValues" />
    </div>
  </div>
</template>
