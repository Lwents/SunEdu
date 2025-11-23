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
import IdleWarning from '@/components/ui/IdleWarning.vue'
import { RouterView } from 'vue-router'
import { ElConfigProvider } from 'element-plus'
import { useIdleLogout } from '@/composables/useIdleLogout'
import { useAuthStore } from '@/store/auth.store'
import { useUiStore } from '@/stores/ui.store'
import router from '@/router'

const authStore = useAuthStore()
const uiStore = useUiStore()

// Khởi tạo token/user từ localStorage trước khi mount
authStore.hydrateFromStorage()
// Làm tươi hồ sơ nếu đã có token (tránh hiển thị avatar cũ)
if (localStorage.getItem('accessToken') || authStore.token) {
  authStore.fetchCurrentUser().catch(() => {
    /* ignore, sẽ dùng dữ liệu cache nếu fetch lỗi */
  })
}

// Đăng xuất tự động khi người dùng không hoạt động
useIdleLogout({
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
