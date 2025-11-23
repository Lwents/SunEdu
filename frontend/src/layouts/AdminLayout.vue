<template>
  <div class="h-screen w-screen overflow-hidden bg-gray-100">
    <div class="flex h-full">
      <!-- Sidebar desktop -->
      <aside class="hidden md:flex w-64 shrink-0 flex-col border-r bg-white">
        <AdminSidebar />
      </aside>

      <!-- Sidebar mobile overlay -->
      <transition name="slide">
        <div v-if="isSidebarOpen" class="fixed inset-0 z-40 flex md:hidden">
          <div class="fixed inset-0 bg-black/50" @click="isSidebarOpen = false"></div>
          <aside class="relative w-[280px] max-w-[85vw] flex flex-col border-r bg-white h-full z-50 shadow-xl">
            <AdminSidebar @close="isSidebarOpen = false" />
          </aside>
        </div>
      </transition>

      <!-- Main -->
      <div class="flex min-w-0 flex-1 flex-col">
        <header class="sticky top-0 z-20 h-14 border-b bg-white">
          <AdminNavbar @toggle-sidebar="isSidebarOpen = !isSidebarOpen" />
        </header>

        <main class="min-h-0 flex-1 overflow-y-auto bg-gray-50 p-3 sm:p-4">
          <router-view />
        </main>
      </div>
    </div>
  </div>
</template>

<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from aside {
  transform: translateX(-100%);
}

.slide-leave-to aside {
  transform: translateX(-100%);
}
</style>

<script setup lang="ts">
import { ref } from 'vue'
import AdminSidebar from '@/components/shared/AdminSidebar.vue'
import AdminNavbar from '@/components/shared/AdminNavbar.vue'

const isSidebarOpen = ref(false)
</script>
