<template>
  <div class="h-screen w-screen overflow-hidden transition-colors duration-300" :class="isDark ? 'bg-slate-950' : 'bg-gray-50'">
    <div class="flex h-full flex-col">
      <header class="sticky top-0 z-20">
        <StudentNavbar />
      </header>
      <main class="min-h-0 flex-1 overflow-y-auto">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import StudentNavbar from '@/components/shared/StudentNavbar.vue'
import { useThemeStore } from '@/store/theme.store'

const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)
</script>
