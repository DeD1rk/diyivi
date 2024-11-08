<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import Title from '@/components/Title.vue'
import Header from '@/components/Header.vue'
import { Textarea } from '@/components/ui/textarea'
import { Button } from '@/components/ui/button'
import { useToast } from '@/components/ui/toast'
import { Loader2 } from 'lucide-vue-next'
import type { DisclosedValue } from '@/api/types'
import AttributeList from '@/components/AttributeList.vue'

const rawSignature = ref<string>('')
const isVerifying = ref<boolean>(false)
const validSignature = ref<{
  message: string
  disclosedValues: DisclosedValue[]
  signatureTime: string
} | null>(null)

const { toast } = useToast()

const verifyUrlPart = window.origin + '/signature/verify/#'
const placeholder =
  verifyUrlPart + 'eyJAY29udGV4dCI6Imh0dHBzOi8vaXJtYS5hcHAvbGQvc2lnbmF0dXJlL3YyI...'

const wellFormedSignature = computed(() => {
  const base64signature = rawSignature.value.trim()
  if (!base64signature) return null
  if (!base64signature.startsWith(verifyUrlPart)) return null
  try {
    const signature = window.atob(base64signature.slice(verifyUrlPart.length))
    return signature
  } catch (error) {
    return null
  }
})

onMounted(() => {
  const urlFragment = window.location.hash
  if (!urlFragment || urlFragment.length < 20 || urlFragment.length > 256000) return
  try {
    console.log('signature might be provided as url fragment:', urlFragment)
    // Fill in the signature in the text area for UX.
    rawSignature.value = verifyUrlPart + urlFragment.slice(1)
    const signature = window.atob(urlFragment.slice(1))
    verify(signature)
  } catch {
    return
  }
})

async function verify(signature: string) {
  isVerifying.value = true
  try {
    const signatureObject = JSON.parse(signature)
    if (signatureObject['@context'] !== 'https://irma.app/ld/signature/v2') {
      throw new Error('input does not appear to be a signature object')
    }
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
        validSignature.value = {
          message: signatureObject.message!,
          disclosedValues: responseBody.disclosed.flat(),
          signatureTime: new Date(signatureObject.timestamp.Time * 1000).toLocaleDateString('nl', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
          })
        }
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
        description: 'Er is iets misgegaan bij het controleren.',
        variant: 'destructive'
      })
      console.error('Signature is malformed:', error)
    }
  } catch (error) {
    toast({
      title: 'Geen handtekening gevonden',
      description: 'Dit ziet er niet uit als een bericht ondertekend met DIYivi.',
      variant: 'destructive'
    })
    console.error('Signature is malformed:', error)
  } finally {
    isVerifying.value = false
  }
}
</script>

<template>
  <div class="p-8">
    <Title>Handtekening controleren</Title>
    <p>
      Heb je een bericht dat ondertekend is met DIYivi? Hier kun je de handtekening controlen.
      Alleen als je dat gedaan hebt weet je of, door wie, en wanneer het bericht ondertekend is.
    </p>
    <div v-if="!validSignature">
      <Header>Plak het bericht</Header>
      <p>
        Plak hieronder het ondertekende bericht. Dit is een lange reeks tekens die begint zoals
        hieronder te zien is.
      </p>
      <Textarea
        v-model="rawSignature"
        :placeholder
        rows="8"
        class="mt-4 font-mono break-all text-sm"
        maxlength="256000"
      />
      <Button
        class="mt-4"
        :disabled="!wellFormedSignature"
        @click="() => verify(wellFormedSignature!)"
      >
        <Loader2 v-if="isVerifying" class="w-4 h-4 mr-2 animate-spin" />
        Controleer
      </Button>
    </div>
    <div v-else>
      <Header>Handtekening klopt!</Header>
      <p>Dit is het bericht dat ondertekend is:</p>
      <div class="text-sm whitespace-break-spaces bg-yivi-lightblue rounded-md p-4 my-4">
        {{ validSignature.message }}
      </div>
      <p>
        Het is ondertekend op
        <span class="font-semibold">{{ validSignature.signatureTime }}.</span>
        Dit zijn de gegevens waarmee het bericht ondertekend is:
      </p>
      <AttributeList :attributes="validSignature.disclosedValues" />
    </div>
  </div>
</template>
