<script setup lang="ts">
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle
} from '@/components/ui/alert-dialog'

const model = defineModel<boolean>({ required: true })
const props = defineProps<{ title: string }>()
const emit = defineEmits<{
  confirm: []
  cancel: []
}>()

function cancel() {
  model.value = false
  emit('cancel')
}

function confirm() {
  model.value = false
  emit('confirm')
}
</script>

<template>
  <AlertDialog :open="model">
    <AlertDialogContent>
      <AlertDialogHeader>
        <AlertDialogTitle>{{ title }}</AlertDialogTitle>
      </AlertDialogHeader>
      <AlertDialogDescription v-if="$slots.description">
        <slot name="description"></slot>
      </AlertDialogDescription>
      <AlertDialogFooter>
        <AlertDialogCancel @click="cancel">
          <slot name="cancel">Terug</slot>
        </AlertDialogCancel>
        <AlertDialogAction @click="confirm">
          <slot name="confirm">Ja</slot>
        </AlertDialogAction>
      </AlertDialogFooter>
    </AlertDialogContent>
  </AlertDialog>
</template>
