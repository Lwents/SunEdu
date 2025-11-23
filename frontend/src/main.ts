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
import { Toaster } from 'vue-sonner'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// Force HTTPS in production to keep origin consistent with the backend (avoids CORS).
if (
  typeof window !== 'undefined' &&
  window.location.hostname.endsWith('smartedu.click') &&
  window.location.protocol !== 'https:'
) {
  const { host, pathname, search, hash } = window.location
  window.location.replace(`https://${host}${pathname}${search}${hash}`)
}

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(ElementPlus)

// Register Sonner Toaster component globally
app.component('Toaster', Toaster)

app.use(router).mount('#app')
