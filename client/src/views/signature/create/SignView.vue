<script setup lang="ts">
import { onMounted } from 'vue'
import { attributeOptions } from '@/lib/attributes'
import { useToast } from '@/components/ui/toast'
import Header from '@/components/Header.vue'
import * as jose from 'jose'

// @ts-ignore
import yivi from '@privacybydesign/yivi-frontend'
import type { DisclosedValue } from '@/api/types'
import { createConDisCon } from '@/lib/utils'

const props = defineProps<{
  message: string
  selectedAttributes: Set<string>
}>()

const emit = defineEmits<{
  signed: [message: string, signature: string, attributes: DisclosedValue[]]
}>()

const { toast } = useToast()

// Secret for requestor authentication. This secret is hardcoded and public, so it
// doesn't really do anything. However, because we want to require requestor authentication
// for *disclosure* sessions (with a proper secret), we need to also enable it for *signature*
// sessions. So here we are, making a session request JWT with a not-secret secret.
const jwtSecret = new TextEncoder().encode('signatures-can-be-created-by-anyone')

onMounted(async () => {
  const attributes = createConDisCon(
    [...props.selectedAttributes].flatMap((attribute) => attributeOptions[attribute]!.attributes)
  )
  const signatureSession = yivi.newWeb({
    debugging: true,
    session: {
      url: import.meta.env.VITE_YIVI_URL || `${window.origin}/yivi`,
      start: {
        method: 'POST',
        headers: {
          'Content-Type': 'text/plain'
        },
        body: await new jose.SignJWT({
          iss: 'client',
          sub: 'signature_request',
          absrequest: {
            request: {
              '@context': 'https://irma.app/ld/request/signature/v2',
              disclose: attributes,
              message: props.message
            }
          }
        })
          .setIssuedAt()
          .setProtectedHeader({ alg: 'HS256' })
          .sign(jwtSecret)
      }
    }
  })

  try {
    const result: {
      proofStatus: string
      signature: { message: string; [key: symbol]: any }
      disclosed: DisclosedValue[][]
    } = await signatureSession.start()
    if (result.proofStatus !== 'VALID' || !result.signature) {
      toast({
        title: 'Oeps! Er ging iets mis',
        description: 'Er is iets misgegaan bij het ondertekenen.'
      })
      console.error('Session result: ', result)
      return
    }
    emit(
      'signed',
      result.signature.message,
      JSON.stringify(result.signature),
      result.disclosed.flat()
    )
  } catch (error) {
    toast({
      title: 'Oeps! Er ging iets mis',
      description: 'Er is iets misgegaan bij het ondertekenen.'
    })
    console.error(error)
  }
})
</script>

<template>
  <Header>Stap 3: Onderteken</Header>
  <p>Bijna klaar! Ga nu verder met Yivi.</p>
  <div class="flex justify-center mt-16">
    <div id="yivi-web-form"></div>
  </div>
</template>
