<script setup lang="ts">
import { ref, inject, defineEmits } from 'vue' // Import defineEmits from vue

import client from '@/api'
import { Checkbox } from '@/components/ui/checkbox'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { initiatorExchangeKey } from '@/lib/keys'
import { attributeOptions, publicAttributeOptions } from '@/lib/attributes'
import router from '@/router'
import { Loader2 } from 'lucide-vue-next'
import { useToast } from '@/components/ui/toast'
import type { InitiatorExchangeResponse } from '@/api/types'

const emit = defineEmits<{
  created: [exchange: InitiatorExchangeResponse]
}>()

const { toast } = useToast()

const publicAttribute = ref('mobilenumber')
const selectedAttributes = ref(new Set<string>())
const isCreating = ref(false)

function setSelectedAttribute(attribute: string, checked: boolean) {
  if (checked) selectedAttributes.value.add(attribute)
  else selectedAttributes.value.delete(attribute)
}

async function createExchange() {
  isCreating.value = true
  try {
    await new Promise((resolve) => setTimeout(resolve, 1000))
    const { data, error } = await client.POST('/api/exchanges/create/', {
      body: {
        attributes: [
          [
            [...selectedAttributes.value].map(
              (attribute) => attributeOptions[attribute]!.attributeId
            )
          ]
        ],
        public_initiator_attributes: [[publicAttributeOptions[publicAttribute.value]!.attributeId]]
      }
    })

    if (data) {
      emit('created', data)
    } else {
      toast({
        title: 'Oeps! Er ging iets mis',
        description: 'Er is iets misgegaan bij het aanmaken van de uitwisseling.'
      })
      console.error(error)
    }
  } catch (error) {
    toast({
      title: 'Oeps! Er ging iets mis',
      description: 'Er is iets misgegaan bij het aanmaken van de uitwisseling.'
    })
    console.error("Couldn't do what you asked 😢", error)
  } finally {
    isCreating.value = false
  }
}
</script>
<template>
  <div class="p-8">
    <h1 class="text-xl font-bold mt-4 mb-2">Uitwisseling aanmaken</h1>
    <p>
      Je maakt een verzoek om gegevens uit te wisselen. Jij kiest welke gegevens uitgewisseld
      worden. Je toont eerst zelf je gegevens. Daarna krijg je een link om naar iemand anders te
      sturen. Als diegene ook diens gegevens deelt, krijgen jullie allebei elkaars gegevens te zien.
    </p>
    <h2 class="text-lg font-bold mt-4 mb-2">Hoe kent de ontvanger je?</h2>
    <div>
      <p class="text-sm">
        Deze informatie krijgt de ontvanger al te zien voordat diegene besluit gegevens te delen. Zo
        weet de ontvanger zeker dat jij degene bent die de link heeft gestuurd.
      </p>
      <RadioGroup v-model="publicAttribute" class="mt-4 mb-2">
        <div
          v-for="({ label, description }, attribute) in publicAttributeOptions"
          class="flex items-start space-x-2"
          :key="attribute"
        >
          <RadioGroupItem :id="`public-attribute-${attribute}`" :value="attribute as string" />
          <Label :for="`public-attribute-${attribute}`">
            {{ label }}
            <p v-if="description" class="font-normal text-xs text-muted-foreground py-1">
              {{ description }}
            </p>
          </Label>
        </div>
      </RadioGroup>
    </div>

    <h2 class="text-lg font-bold mt-4 mb-2">Welke gegevens wil je uitwisselen?</h2>
    <div>
      <p class="text-sm">
        Deze informatie krijgen jullie allebei pas te zien nadat jullie allebei hebben besloten
        gegevens te delen.
      </p>
      <div class="grid gap-2 mt-4 mb-2">
        <div
          v-for="({ label }, attribute) of attributeOptions"
          :key="attribute"
          class="flex items-start space-x-2"
        >
          <Checkbox
            :id="`attribute-${attribute}`"
            @update:checked="(checked) => setSelectedAttribute(attribute as string, checked)"
          />
          <Label :for="`attribute-${attribute}`">
            {{ label }}
          </Label>
        </div>
      </div>
    </div>

    <Button @click="createExchange" class="mt-4" :disabled="isCreating">
      <Loader2 v-if="isCreating" class="w-4 h-4 mr-2 animate-spin" />
      Aanmaken
    </Button>
  </div>
</template>
