<!-- src/App.vue -->
<template>
  <!-- Element Plus config (tùy chọn, nhưng hữu ích) -->
  <el-config-provider namespace="el" :z-index="3000">
    <IdleWarning />
    <!-- Route outlet -->
    <RouterView v-slot="{ Component }">
      <Transition name="fade" mode="out-in">
        <component :is="Component" />
      </Transition>
    </RouterView>
  </el-config-provider>
</template>

<script setup lang="ts">
import { watch } from 'vue'
import IdleWarning from '@/components/ui/IdleWarning.vue'
import { RouterView } from 'vue-router'
import { ElConfigProvider } from 'element-plus'
import { useIdleLogout } from '@/composables/useIdleLogout'
import { useAuthStore } from '@/store/auth.store'
import { useUiStore } from '@/stores/ui.store'
import router from '@/router'

const authStore = useAuthStore()
const uiStore = useUiStore()

// Khởi tạo/làm tươi hồ sơ ngay khi app boot
authStore.init().catch(() => {
  /* ignore */
})

// Đăng xuất tự động khi người dùng không hoạt động
const idleControl = useIdleLogout({
  timeout: 15 * 60 * 1000, // 15 phút không tương tác
  warningTime: 5 * 60 * 1000, // cảnh báo trước 5 phút
  onWarn(remaining) {
    uiStore.openIdleWarning(remaining, () => {
      localStorage.setItem('app-last-activity', String(Date.now()))
    })
  },
  async onLogout() {
    uiStore.closeIdleWarning()
    await authStore.logout().catch(() => {})
    await router.push('/auth/login').catch(() => {})
  },
})

watch(
  () => authStore.isAuthenticated,
  (isAuth) => {
    if (isAuth) {
      idleControl.start()
    } else {
      idleControl.stop()
      uiStore.closeIdleWarning()
      localStorage.removeItem('app-last-activity')
    }
  },
  { immediate: true },
)
</script>

<style>
/* Transition nhẹ nhàng khi đổi page */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
