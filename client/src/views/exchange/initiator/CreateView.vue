<script setup lang="ts">
import { computed, ref } from 'vue'
import client from '@/api'
import { Checkbox } from '@/components/ui/checkbox'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { attributeOptions, publicAttributeOptions } from '@/lib/attributes'
import { Loader2 } from 'lucide-vue-next'
import { useToast } from '@/components/ui/toast'
import type { InitiatorExchangeResponse } from '@/api/types'
import Title from '@/components/Title.vue'
import Header from '@/components/Header.vue'

const emit = defineEmits<{
  created: [exchange: InitiatorExchangeResponse, publicAttribute: string]
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
        type: '1-to-1',
        send_email: true,
        attributes: [...selectedAttributes.value].flatMap(
          (attribute) => attributeOptions[attribute]!.attributes
        ),
        public_initiator_attributes: [publicAttributeOptions[publicAttribute.value]!.attributeId]
      }
    })

    if (data) {
      emit('created', data, publicAttribute.value)
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

const noAttributesSelected = computed(() => selectedAttributes.value.size === 0)
</script>
<template>
  <div class="p-8">
    <Title>Elkaar leren kennen</Title>
    <p>
      Jij neemt het initiatief. Jij kiest welke persoonlijke details je met een andere persoon uit
      wil wisselen. Je toont eerst jouw eigen persoonlijke gegevens aan deze website. Daarna krijg
      je een link om naar de ander te sturen. Pas als die andere persoon ook dezelfde gegevens aan
      deze website onthult, krijgen jullie allebei elkaars gegevens te zien.
    </p>
    <Header>Stap 1: Hoe hebben jij en de ander contact?</Header>
    <p class="text-sm">
      Deze informatie krijgt de ander al te zien voordat diegene besluit gegevens te delen. Zo weet
      die persoon zeker dat jij degene bent die de link heeft gestuurd. Je krijgt sowieso een e-mail
      als jullie gegevens hebben uitgewisseld.
    </p>
    <div>
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

    <Header>Stap 2: Welke details wil je uitwisselen?</Header>
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

    <Button @click="createExchange" :disabled="isCreating || noAttributesSelected" class="mt-4">
      <Loader2 v-if="isCreating" class="w-4 h-4 mr-2 animate-spin" />
      Ga door naar stap 3
    </Button>
  </div>
</template>
