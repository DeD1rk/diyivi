<script setup lang="ts">
import { Checkbox } from '@/components/ui/checkbox'
import { Label } from '@/components/ui/label'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'

const publicAttributeOptions = {
  mobilenumber: {
    label: 'Mobiel telefoonnumer',
    description: 'Bijvoorbeeld via WhatsApp of Signal.'
  },
  email: {
    label: 'E-mailadres',
    description: null
  }
}

const attributeOptions = {
  name: {
    label: 'Naam',
    description: null
  },
  birthdate: {
    label: 'Geboortedatum',
    description: null
  },
  mobilenumber: {
    label: 'Mobiel telefoonnumer',
    description: null
  },
  email: {
    label: 'E-mailadres',
    description: null
  }
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
      <RadioGroup class="pt-4 pb-2">
        <div
          v-for="({ label, description }, attribute) in publicAttributeOptions"
          class="flex items-start space-x-2"
          :key="attribute"
        >
          <RadioGroupItem :id="`public-attribute-${attribute}`" :value="attribute" />
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
          v-for="({ label, description }, attribute) in attributeOptions"
          :key="attribute"
          class="flex items-start space-x-2"
        >
          <Checkbox :id="`attribute-${attribute}`" />
          <Label :for="`attribute-${attribute}`">
            {{ label }}
            <p v-if="description" class="font-normal text-xs text-muted-foreground py-1">
              {{ description }}
            </p>
          </Label>
        </div>
      </div>
    </div>
  </div>
</template>
