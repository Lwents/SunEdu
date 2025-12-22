<template>
  <div class="rounded-lg bg-white p-4 ring-1 ring-black/5">
    <div class="flex items-center justify-between gap-3">
      <div class="min-w-0">
        <div class="text-xs text-gray-500">{{ title }}</div>
        <div class="mt-1 truncate text-2xl font-semibold text-gray-900">{{ value }}</div>
      </div>
      <div class="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-indigo-50 text-indigo-600">
        <component :is="iconComponent" class="h-4 w-4" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Activity, ClipboardCheck, CreditCard, RotateCcw, UserPlus, Users } from 'lucide-vue-next'

const props = defineProps<{
  title: string
  value: string | number
  icon?: string
}>()

const iconComponent = computed(() => {
  const mapping: Record<string, any> = {
    users: Users,
    'user-plus': UserPlus,
    'credit-card': CreditCard,
    activity: Activity,
    'rotate-ccw': RotateCcw,
    'clipboard-check': ClipboardCheck,
  }
  return mapping[props.icon ?? ''] || Activity
})
</script>
