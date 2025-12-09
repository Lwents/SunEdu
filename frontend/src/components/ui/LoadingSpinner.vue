<template>
  <div
    class="flex items-center justify-center"
    :class="wrapperClass"
    role="status"
    aria-live="polite"
  >
    <img
      src="/loading.gif"
      :alt="resolvedAlt"
      class="object-contain drop-shadow-sm"
      :style="{ width: resolvedSize, height: resolvedSize }"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  size?: number | string
  alt?: string
  wrapperClass?: string
}>()

const resolvedSize = computed(() => {
  if (typeof props.size === 'number') return `${props.size}px`
  if (typeof props.size === 'string') {
    return props.size.match(/(px|rem|em|vh|vw|%)$/) ? props.size : `${props.size}px`
  }
  return '80px'
})

const resolvedAlt = computed(() => props.alt || 'Đang tải...')
const wrapperClass = computed(() => props.wrapperClass || 'py-10')
</script>
