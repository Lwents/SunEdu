<!-- src/components/shared/AdminNavbar.vue -->
<template>
  <header class="flex h-full items-center justify-between px-2 sm:px-4">
    <!-- Left: Hamburger + dynamic title -->
    <div class="flex items-center min-w-0 gap-2 flex-1">
      <!-- Hamburger menu, chỉ hiện trên mobile -->
      <button
        class="mr-1 sm:mr-2 flex md:hidden items-center justify-center rounded p-2 hover:bg-gray-100 transition-colors"
        aria-label="Mở menu"
        @click="$emit('toggle-sidebar')"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5 sm:h-6 sm:w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M4 6h16M4 12h16M4 18h16"
          />
        </svg>
      </button>
      <h1 class="truncate text-sm sm:text-base font-semibold text-gray-800">
        {{ pageTitle }}
      </h1>
    </div>

    <!-- Right: actions -->
    <div class="flex items-center gap-1 sm:gap-2 shrink-0">
      <!-- Notification Bell Component for Admin -->
      <NotificationBell :user-id="auth.user?.id" role="admin" />

      <div class="hidden lg:flex flex-col items-end">
        <span class="text-sm font-medium leading-4">{{ user?.name || 'Admin' }}</span>
        <span class="text-xs text-gray-500 leading-4">{{
          user?.email || 'admin@example.com'
        }}</span>
      </div>

      <img
        class="h-7 w-7 sm:h-8 sm:w-8 rounded-full object-cover aspect-square"
        :src="avatarSrc"
        alt="avatar"
        @error="handleAvatarError"
      />

      <button
        class="inline-flex items-center gap-1 sm:gap-2 rounded bg-red-500 px-2 sm:px-3 py-1 text-xs sm:text-sm text-white hover:bg-red-600 transition-colors"
        @click="showConfirm = true"
      >
        <LogOut class="h-3 w-3 sm:h-4 sm:w-4" />
        <span class="hidden sm:inline">Đăng xuất</span>
      </button>
    </div>
    <ConfirmLogout
      :open="showConfirm"
      @update:open="showConfirm = $event"
      @confirm="handleLogout"
    />
  </header>
</template>

<script setup lang="ts">
import { ref, computed, defineEmits } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth.store'
import ConfirmLogout from '@/components/ui/ConfirmLogout.vue'
import { LogOut } from 'lucide-vue-next'
import { getAvatarSrc } from '@/utils/avatar'
import NotificationBell from '@/components/shared/NotificationBell.vue'

const emit = defineEmits(['toggle-sidebar'])

const auth = useAuthStore()
const user = computed(() => auth.user)

const route = useRoute()
const router = useRouter()

const avatarSrc = computed(() => {
  return getAvatarSrc(
    auth.user?.avatar,
    auth.user?.gender as 'male' | 'female' | 'other' | null | undefined,
    'admin'
  )
})

const pageTitle = computed(() => {
  const matched = [...route.matched].reverse().find((r) => r.meta?.title) as any
  return matched?.meta?.title || 'Admin'
})

// Confirm popup
const showConfirm = ref(false)

function handleAvatarError(event: Event) {
  const img = event.target as HTMLImageElement
  // Fallback to default avatar
  const defaultAvatar = getAvatarSrc(null, auth.user?.gender as 'male' | 'female' | 'other' | null | undefined, 'admin')
  img.src = defaultAvatar
}

async function handleLogout() {
  try {
    // Gọi logout và đợi hoàn tất
    if (typeof auth.logout === 'function') {
      await auth.logout()
    } else {
      // Fallback nếu logout không phải function
      auth.token = null
      auth.user = null
      localStorage.removeItem('auth')
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      sessionStorage.removeItem('accessToken')
      sessionStorage.removeItem('refreshToken')
    }
    
    // Đợi một chút để đảm bảo state đã được cập nhật hoàn toàn
    await new Promise(resolve => setTimeout(resolve, 100))
    
    // Redirect trực tiếp về login để tránh router guard xử lý phức tạp
    await router.push('/auth/login')
  } catch (error) {
    console.error('Logout error:', error)
    // Nếu có lỗi, vẫn redirect về login
    await router.push('/auth/login')
  }
}
</script>
