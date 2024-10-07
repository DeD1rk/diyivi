<script setup lang="ts">
import type { DisclosedValue, TranslatedString } from '@/api/types'
import { attributeDisplayOptions } from '@/lib/attributes'
import { computed } from 'vue'

const props = defineProps<{
  attributes: DisclosedValue[]
}>()

const attributeValueMap = computed(() => {
  const map: { [key: string]: TranslatedString } = {}
  for (const attribute of props.attributes) {
    map[attribute.id] = attribute.value
  }
  return map
})
</script>
<template>
  <ul class="mt-4">
    <template v-for="(option, index) of attributeDisplayOptions">
      <li v-if="option.requiredAttributes.every((id) => attributeValueMap[id])" :key="index">
        <span class="font-semibold">{{ option.label }}:</span>
        {{ option.display(attributeValueMap) }}
      </li>
    </template>
  </ul>
</template>
