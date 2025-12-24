<template>
  <div class="min-h-screen w-full" :class="isDark ? 'bg-slate-950' : 'bg-gray-50'">
    <header class="sticky top-0 z-20">
      <StudentNavbar />
    </header>
    <main class="w-full" :class="isDark ? 'bg-slate-950' : 'bg-gray-50'">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import StudentNavbar from '@/components/shared/StudentNavbar.vue'
import { useThemeStore } from '@/store/theme.store'

const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)
</script>
