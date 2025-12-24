<template>
  <!-- Brand tone: indigo -->
  <div class="teacher-page h-screen w-screen overflow-hidden" :class="[isDark ? 'bg-slate-950' : 'bg-gray-100']">
    <div class="flex h-full">
      <!-- Sidebar (ẩn trên mobile) -->
      <!-- <aside class="hidden md:flex w-64 shrink-0 flex-col border-r bg-white">
        <TeacherSidebar />
      </aside> -->

      <!-- Cột phải -->
      <div class="flex min-w-0 flex-1 flex-col">
        <!-- Navbar dính trên -->
        <header class="sticky top-0 z-20">
          <TeacherNavbar />
        </header>

        <!-- Nội dung: chỉ phần này được cuộn -->
        <main class="min-h-0 flex-1 overflow-y-auto p-4" :class="isDark ? 'bg-slate-950' : 'bg-gray-50'">
          <router-view />
        </main>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
// import TeacherSidebar from '@/components/shared/TeacherSidebar.vue'
import TeacherNavbar from '@/components/shared/TeacherNavbar.vue'
import { useThemeStore } from '@/store/theme.store'

const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)
</script>
