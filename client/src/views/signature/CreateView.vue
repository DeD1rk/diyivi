<script setup lang="ts">
import { computed, ref } from 'vue'
import client from '@/api'
import { Checkbox } from '@/components/ui/checkbox'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { attributeOptions } from '@/lib/attributes'
import { Loader2 } from 'lucide-vue-next'
import { useToast } from '@/components/ui/toast'
import { Textarea } from '@/components/ui/textarea'
import Title from '@/components/Title.vue'
import Header from '@/components/Header.vue'

const emit = defineEmits<{
  created: [message: string, attributes: Set<string>]
}>()

const message = ref('')
const selectedAttributes = ref(new Set<string>())

const noAttributesSelected = computed(() => selectedAttributes.value.size === 0)
const emptyMessage = computed(() => message.value.trim().length === 0)

function setSelectedAttribute(attribute: string, checked: boolean) {
  if (checked) selectedAttributes.value.add(attribute)
  else selectedAttributes.value.delete(attribute)
}
</script>

<template>
  <Header>Stap 1: Wat wil je ondertekenen?</Header>
  <!--
    Ideally, this textarea would be a <div contenteditable> that grows to fit the content.
    That way, it cannot happen that part of the 'contract' is not visible to the user.
    It's a bit harder to implement while keeping the accessibility and styling consistent.
    The Yivi app should already protect the user from this, as well as from an evil client.
  -->
  <Textarea v-model="message" placeholder="Typ hier je bericht of afspraak." rows="6" />

  <Header>Stap 2: Met welke gegevens wil je tekenen?</Header>
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

  <Header>Stap 3: Onderteken</Header>
  <p class="text-sm">Klopt alles? Dan kun je je bericht nu ondertekenen met Yivi.</p>
  <Button
    class="mt-4"
    :disabled="noAttributesSelected || emptyMessage"
    @click="() => emit('created', message.trim(), selectedAttributes)"
  >
    Onderteken
  </Button>
</template>
