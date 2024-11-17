<script setup lang="ts">
import { onMounted } from 'vue'
import { attributeOptions } from '@/lib/attributes'
import { useToast } from '@/components/ui/toast'
import Header from '@/components/Header.vue'
import * as jose from 'jose'

// @ts-ignore
import yivi from '@privacybydesign/yivi-frontend'
import type { DisclosedValue, RecipientSignatureRequestResponse } from '@/api/types'
import { createConDisCon } from '@/lib/utils'
import client from '@/api'

const props = defineProps<{
  requestId: string
  request: RecipientSignatureRequestResponse
}>()

const emit = defineEmits<{
  signed: [signature: string, attributes: DisclosedValue[]]
}>()

const { toast } = useToast()

// Secret for requestor authentication. This secret is hardcoded and public, so it
// doesn't really do anything. However, because we want to require requestor authentication
// for *disclosure* sessions (with a proper secret), we need to also enable it for *signature*
// sessions. So here we are, making a session request JWT with a not-secret secret.
const jwtSecret = new TextEncoder().encode('signatures-can-be-created-by-anyone')

onMounted(async () => {
  const attributes = createConDisCon(props.request.attributes)
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
              message: props.request.message
            }
          }
        })
          .setIssuedAt()
          .setProtectedHeader({ alg: 'HS256' })
          .sign(jwtSecret)
      },
      result: {
        // @ts-ignore
        url: (o, { sessionPtr, sessionToken }) => `${o.url}/session/${sessionToken}/result-jwt`,
        // @ts-ignore
        parseResponse: (r) => r.text()
      }
    }
  })

  try {
    const resultJwt: string = await signatureSession.start()
    const result: {
      proofStatus: string
      disclosed: DisclosedValue[][]
      signature: {
        message: string
        timestamp: { Time: number }
      }
    } = await jose.decodeJwt(resultJwt)
    if (result.proofStatus !== 'VALID' || result.signature.message !== props.request.message) {
      throw new Error('Invalid signature')
    }
    const validSignature = {
      message: result.signature.message!,
      disclosedValues: result.disclosed.flat(),
      signatureTime: new Date(result.signature.timestamp.Time * 1000).toLocaleDateString('nl', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
    const { error } = await client.POST('/api/signatures/requests/{request_id}/respond/', {
      params: {
        path: {
          request_id: props.requestId
        }
      },
      body: {
        signature_result: resultJwt
      }
    })
    if (error) {
      toast({
        title: 'Oeps! Er ging iets mis',
        description: 'Er is iets misgegaan bij het ondertekenen.'
      })
      console.error(error)
    } else {
      emit('signed', JSON.stringify(result.signature), validSignature.disclosedValues)
    }
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
  <div class="flex justify-center mt-16">
    <div id="yivi-web-form"></div>
  </div>
</template>
