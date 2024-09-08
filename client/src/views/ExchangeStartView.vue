<script setup lang="ts">
import client from '@/api'
import { Checkbox } from '@/components/ui/checkbox'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { ref } from 'vue'

const publicAttributeOptions: {
  [key: string]: { label: string; description: string | null; attributeId: string }
} = {
  mobilenumber: {
    label: 'Mobiel telefoonnumer',
    description: 'Bijvoorbeeld via WhatsApp of Signal.',
    attributeId: 'irma-demo.sidn-pbdf.mobilenumber.mobilenumber'
  },
  email: {
    label: 'E-mailadres',
    description: null,
    attributeId: 'irma-demo.sidn-pbdf.email.email'
  }
}

const attributeOptions: {
  [key: string]: { label: string; attributeId: string }
} = {
  name: {
    label: 'Naam',
    attributeId: 'irma-demo.gemeente.personalData.fullname'
  },
  birthdate: {
    label: 'Geboortedatum',
    attributeId: 'irma-demo.sidn-pbdf.personalData.dateofbirth'
  },
  mobilenumber: {
    label: 'Mobiel telefoonnumer',
    attributeId: 'irma-demo.sidn-pbdf.mobilenumber.mobilenumber'
  },
  email: {
    label: 'E-mailadres',
    attributeId: 'irma-demo.sidn-pbdf.email.email'
  }
}

const publicAttribute = ref('mobilenumber')
const selectedAttributes = ref(new Set<string>())

function setSelectedAttribute(attribute: string, checked: boolean) {
  console.log(attribute, checked)
  if (checked) selectedAttributes.value.add(attribute)
  else selectedAttributes.value.delete(attribute)
}

async function createExchange() {
  console.log(publicAttribute.value)

  const response = await client.POST('/api/exchanges/create/', {
    body: {
      attributes: [
        [[...selectedAttributes.value].map((attribute) => attributeOptions[attribute]!.attributeId)]
      ],
      public_initiator_attributes: [[publicAttributeOptions[publicAttribute.value]!.attributeId]]
    }
  })

  console.log(response)
}
</script>
<template>
  <div class="px-5">
    <h1 class="text-xl font-bold pt-4 pb-2">Uitwisseling aanmaken</h1>
    <p class="">
      Je maakt een verzoek om gegevens uit te wisselen. Jij kiest welke gegevens uitgewisseld
      worden. Je toont eerst zelf je gegevens. Daarna krijg je een link om naar iemand anders te
      sturen. Als diegene ook diens gegevens deelt, krijgen jullie allebei elkaars gegevens te zien.
    </p>
    <h2 class="text-lg font-bold pt-4 pb-2">Hoe kent de ontvanger je?</h2>
    <div>
      <p class="text-sm">
        Deze informatie krijgt de ontvanger al te zien voordat diegene besluit gegevens te delen. Zo
        weet de ontvanger zeker dat jij degene bent die de link heeft gestuurd.
      </p>
      <RadioGroup v-model="publicAttribute" class="pt-4 pb-2">
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

    <h2 class="text-lg font-bold pt-4 pb-2">Welke gegevens wil je uitwisselen?</h2>
    <div>
      <p class="text-sm">
        Deze informatie krijgen jullie allebei pas te zien nadat jullie allebei hebben besloten
        gegevens te delen.
      </p>
      <div class="grid gap-2 pt-4 pb-2">
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

    <Button @click="createExchange" class="pt-4"> Aanmaken </Button>
  </div>
</template>
