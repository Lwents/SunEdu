// import { createApp } from 'vue'
// import { createPinia } from 'pinia'
// import ElementPlus from 'element-plus'


// import App from './App.vue'
// import router from './router'
// import "@/styles/tailwind.css"

// const app = createApp(App)

// app.use(createPinia())
// app.use(router)
// app.use(ElementPlus)


// app.mount('#app')


import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from '@/router'
import 'element-plus/dist/index.css'
import '@/styles/tailwind.css'
import { useAuthStore } from '@/store/auth.store'
import { useUiStore } from '@/stores/ui.store'
import { useIdleLogout } from '@/composables/useIdleLogout'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'


const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(ElementPlus)
const authStore = useAuthStore()
authStore.hydrateFromStorage()
const uiStore = useUiStore()

useIdleLogout({
  timeout: 15 * 60 * 1000,
  warningTime: 5 * 60 * 1000,
  onWarn(remaining) {
    uiStore.openIdleWarning(remaining, () => {
      localStorage.setItem('app-last-activity', String(Date.now()))
    })
  },
  async onLogout() {
    uiStore.closeIdleWarning()
    await authStore.logout().catch(() => {})
  },
})

app.use(router).mount('#app')
