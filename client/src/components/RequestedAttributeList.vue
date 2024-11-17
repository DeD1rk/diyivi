<script setup lang="ts">
import { attributeDisplayOptions } from '@/lib/attributes'

const props = defineProps<{
  attributes: string[]
}>()
</script>
<template>
  <ul class="list-disc list-inside mt-4 ps-2 font-semibold">
    <template v-for="(option, index) of attributeDisplayOptions">
      <li v-if="option.requiredAttributes.every((id) => attributes.includes(id))" :key="index">
        {{ option.label }}
      </li>
    </template>
  </ul>
</template>
