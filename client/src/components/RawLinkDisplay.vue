<script setup lang="ts">
import { Copy } from 'lucide-vue-next'
import { useToast } from '@/components/ui/toast'

const props = defineProps<{
  link: string
  copyMessage: string
}>()

const { toast } = useToast()

async function copyLink() {
  await navigator.clipboard.writeText(props.link)
  toast({
    description: props.copyMessage
  })
}
</script>
<template>
  <div class="font-mono break-all select-all bg-yivi-lightblue py-2 px-4">
    <button @click="copyLink">
      <Copy class="inline me-2 w-4 h-4 hover:scale-110 transition" /></button
    >{{ link }}
  </div>
</template>
