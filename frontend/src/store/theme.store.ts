import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const isDark = ref(localStorage.getItem('theme') === 'dark' || !localStorage.getItem('theme'))

  function toggleTheme() {
    isDark.value = !isDark.value
  }

  function setTheme(dark: boolean) {
    isDark.value = dark
  }

  watch(isDark, (val) => {
    localStorage.setItem('theme', val ? 'dark' : 'light')
    // Add/remove 'dark' class on html for global CSS selectors (popups, etc.)
    if (val) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, { immediate: true })

  return { isDark, toggleTheme, setTheme }
})
