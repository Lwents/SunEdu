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
  }, { immediate: true })

  return { isDark, toggleTheme, setTheme }
})
