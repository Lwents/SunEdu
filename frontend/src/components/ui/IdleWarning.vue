<template>
  <div v-if="ui.showIdleWarning" class="fixed inset-0 z-[9999] flex items-center justify-center">
    <div class="absolute inset-0 bg-black/50" />
    <div class="bg-white rounded-lg shadow-lg p-6 z-10 w-full max-w-sm text-center">
      <h3 class="text-lg font-semibold mb-2">Bạn còn hoạt động không?</h3>
      <p class="text-sm text-gray-600 mb-4">
        Đã 15 phút không có thao tác, hệ thống sẽ tự đăng xuất sau
        <strong>{{ secondsLeft }}</strong> giây nếu bạn không bấm "Em vẫn ở đây".
      </p>
      <div class="text-center mb-4">
        <span class="text-3xl font-medium text-red-600">{{ secondsLeft }}</span>
        <span class="text-sm text-gray-500 ml-1">giây</span>
      </div>
      <button @click="stay" class="px-5 py-2.5 rounded bg-green-600 text-white font-medium w-full">
        Em vẫn ở đây
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onBeforeUnmount } from 'vue'
import { useUiStore } from '@/stores/ui.store'
import { useAuthStore } from '@/store/auth.store'
import router from '@/router'

const ui = useUiStore()
const auth = useAuthStore()

const secondsLeft = computed(() => Math.max(0, Math.ceil((ui.idleRemaining ?? 0) / 1000)))

let countdown: ReturnType<typeof setInterval> | null = null

onMounted(() => {
  countdown = setInterval(() => {
    if (ui.showIdleWarning && ui.idleRemaining > 0) {
      ui.idleRemaining = Math.max(0, ui.idleRemaining - 1000)
      if (ui.idleRemaining <= 0) {
        logoutNow()
      }
    }
  }, 1000)
})

onBeforeUnmount(() => {
  if (countdown) clearInterval(countdown)
})

function stay() {
  ui.keepAlive() // gọi reset function thiết lập trong store
}

async function logoutNow() {
  ui.closeIdleWarning()
  try {
    if (typeof auth.logout === 'function') {
      await auth.logout()
    } else {
      localStorage.removeItem('access')
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refresh')
    }
  } finally {
    router.push({ name: 'Login' }).catch(() => {})
  }
}
</script>

<style scoped>
/* tuỳ chỉnh nếu cần */
</style>
