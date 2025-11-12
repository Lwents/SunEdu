<template>
  <button
    @click="toggleDarkMode"
    class="relative inline-flex h-10 w-10 items-center justify-center rounded-xl border border-cyan-200 bg-white shadow-sm transition-all duration-300 hover:shadow-ocean-glow dark:border-cyan-800 dark:bg-gray-800 dark:hover:shadow-dark-ocean"
    :title="isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
  >
    <!-- Sun Icon (Light Mode) -->
    <svg
      v-if="!isDark"
      class="h-5 w-5 text-amber-500 animate-scale-in"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
      />
    </svg>

    <!-- Moon Icon with waves (Dark Mode) -->
    <svg
      v-else
      class="h-5 w-5 text-cyan-400 animate-scale-in"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
      />
    </svg>

    <!-- Ocean ripple effect on click -->
    <span
      v-if="showRipple"
      class="absolute inset-0 rounded-xl bg-cyan-500/30 animate-ripple-out"
    ></span>
  </button>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const isDark = ref(false)
const showRipple = ref(false)

// Initialize dark mode from localStorage or system preference
onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches

  if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
    isDark.value = true
    document.documentElement.classList.add('dark')
  } else {
    isDark.value = false
    document.documentElement.classList.remove('dark')
  }
})

function toggleDarkMode() {
  isDark.value = !isDark.value

  if (isDark.value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }

  // Show ripple effect
  showRipple.value = true
  setTimeout(() => {
    showRipple.value = false
  }, 800)
}
</script>

<style scoped>
@keyframes ripple-out {
  0% {
    transform: scale(0);
    opacity: 1;
  }
  100% {
    transform: scale(2.5);
    opacity: 0;
  }
}

.animate-ripple-out {
  animation: ripple-out 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
}
</style>
