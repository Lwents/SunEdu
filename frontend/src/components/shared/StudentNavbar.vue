<!-- src/components/navbar/StudentNavbar.vue -->
<template>
  <nav 
    class="sticky top-0 z-50 h-14 sm:h-16 backdrop-blur-xl border-b transition-colors duration-300"
    :class="isDark ? 'bg-slate-950/80 border-white/10' : 'bg-white/90 border-gray-200'"
  >
    <div class="mx-auto flex h-full max-w-7xl items-center justify-between px-3 sm:px-4 lg:px-8">
      <!-- Logo -->
      <div class="flex items-center gap-3">
        <RouterLink 
          to="/student/dashboard" 
          class="inline-block transition hover:opacity-80"
        >
          <LogoSmartEdu :size="90" />
        </RouterLink>
      </div>

      <!-- Desktop Menu -->
      <ul class="hidden items-center gap-1 md:flex">
        <li v-for="item in menu" :key="item.path">
          <RouterLink
            :to="item.path"
            class="rounded-xl px-4 py-2.5 text-sm font-medium transition-all duration-300"
            :class="getMenuClass(item.path)"
          >
            {{ item.label }}
          </RouterLink>
        </li>
      </ul>

      <!-- Right side actions -->
      <div class="flex items-center gap-3">
        <!-- Theme Toggle -->
        <button
          @click="toggleTheme"
          class="p-2 rounded-xl transition-all duration-300"
          :class="isDark ? 'hover:bg-white/10 text-gray-300' : 'hover:bg-gray-100 text-gray-700'"
          :title="isDark ? 'Chuyển sang Light Mode' : 'Chuyển sang Dark Mode'"
        >
          <!-- Sun icon (show in dark mode) -->
          <svg v-if="isDark" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
          </svg>
          <!-- Moon icon (show in light mode) -->
          <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
          </svg>
        </button>

        <!-- Notification Bell Component -->
        <NotificationBell :user-id="auth.user?.id" role="student" />

        <!-- Avatar Dropdown -->
        <div class="relative" ref="avatarWrapper">
          <button
            @click="avatarOpen = !avatarOpen"
            class="flex items-center gap-2 transition hover:opacity-80 focus:outline-none focus:ring-2 rounded-full"
            :class="isDark ? 'focus:ring-cyan-500/50' : 'focus:ring-slate-300'"
          >
            <img
              class="h-10 w-10 rounded-full object-cover border-2 aspect-square"
              :class="isDark ? 'border-cyan-500/50' : 'border-slate-300'"
              :src="avatarSrc"
              alt="avatar"
              @error="handleAvatarError"
            />
          </button>

          <!-- Dropdown Menu -->
          <Transition
            enter-active-class="transition ease-out duration-200"
            enter-from-class="transform opacity-0 scale-95"
            enter-to-class="transform opacity-100 scale-100"
            leave-active-class="transition ease-in duration-150"
            leave-from-class="transform opacity-100 scale-100"
            leave-to-class="opacity-0 scale-95"
          >
            <div
              v-if="avatarOpen"
              class="absolute right-0 z-30 mt-2 w-56 rounded-xl border backdrop-blur-xl shadow-xl p-2"
              :class="isDark ? 'border-white/10 bg-slate-900/95' : 'border-slate-200 bg-white'"
            >
              <!-- User info -->
              <div class="px-3 py-3 border-b mb-2" :class="isDark ? 'border-white/10' : 'border-slate-200'">
                <p class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ displayName }}</p>
                <p class="text-xs truncate mt-0.5" :class="isDark ? 'text-gray-400' : 'text-slate-500'">{{ displayEmail }}</p>
              </div>

              <!-- Menu items -->
              <div class="py-1 space-y-1">
                <RouterLink
                  to="/student/account/profile"
                  class="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm transition"
                  :class="isDark ? 'text-gray-300 hover:bg-white/10 hover:text-white' : 'text-slate-700 hover:bg-slate-100'"
                  @click="avatarOpen = false"
                >
                  <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                  </svg>
                  <span>Tài khoản</span>
                </RouterLink>

                <RouterLink
                  to="/student/payments/history"
                  class="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm transition"
                  :class="isDark ? 'text-gray-300 hover:bg-white/10 hover:text-white' : 'text-slate-700 hover:bg-slate-100'"
                  @click="avatarOpen = false"
                >
                  <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/>
                  </svg>
                  <span>Lịch sử thanh toán</span>
                </RouterLink>

                <button
                  @click="showConfirm = true"
                  class="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm transition"
                  :class="isDark ? 'text-red-400 hover:bg-red-500/10' : 'text-red-600 hover:bg-red-50'"
                >
                  <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
                  </svg>
                  <span>Đăng xuất</span>
                </button>
              </div>
            </div>
          </Transition>
        </div>

        <!-- Mobile Menu Button -->
        <div class="md:hidden">
          <button
            @click="open = !open"
            class="p-2 rounded-lg transition"
            :class="isDark ? 'hover:bg-white/10' : 'hover:bg-slate-100'"
            aria-label="Mở menu"
          >
            <svg class="h-6 w-6" :class="isDark ? 'text-gray-300' : 'text-slate-700'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path v-if="!open" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Menu -->
    <Transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="opacity-0 -translate-y-2"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 -translate-y-2"
    >
      <div
        v-if="open"
        ref="mobileMenuWrapper"
        class="md:hidden border-t backdrop-blur-xl"
        :class="isDark ? 'border-white/10 bg-slate-950/95' : 'border-slate-200 bg-white/95'"
      >
        <div class="space-y-1 px-3 py-3">
          <RouterLink
            v-for="item in menu"
            :key="item.path"
            :to="item.path"
            class="block rounded-xl px-4 py-3 text-base font-medium transition"
            :class="getMenuClass(item.path)"
            @click="open = false"
          >
            {{ item.label }}
          </RouterLink>
        </div>
      </div>
    </Transition>
  </nav>

  <ConfirmLogout
    :open="showConfirm"
    :loading="isLoggingOut"
    @update:open="showConfirm = $event"
    @confirm="handleLogout"
  />
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth.store'
import { useThemeStore } from '@/store/theme.store'
import { onClickOutside } from '@vueuse/core'
import LogoSmartEdu from '@/components/ui/LogoSmartEdu.vue'
import ConfirmLogout from '@/components/ui/ConfirmLogout.vue'
import NotificationBell from '@/components/shared/NotificationBell.vue'
import { getAvatarSrc } from '@/utils/avatar'

const auth = useAuthStore()
const themeStore = useThemeStore()
const route = useRoute()
const router = useRouter()

const isDark = computed(() => themeStore.isDark)
const toggleTheme = () => themeStore.toggleTheme()

const open = ref(false)
const avatarOpen = ref(false)
const showConfirm = ref(false)
const isLoggingOut = ref(false)

const avatarSrc = computed(() => {
  return getAvatarSrc(
    auth.user?.avatar,
    auth.user?.gender as 'male' | 'female' | 'other' | null | undefined,
    'student'
  )
})
const displayName = computed(() => auth.user?.name || 'Học sinh')
const displayEmail = computed(() => auth.user?.email || 'student@example.com')

const menu = [
  { path: '/student/dashboard', label: 'Trang chủ' },
  { path: '/student/courses', label: 'Khóa học' },
  { path: '/student/exams', label: 'Bài kiểm tra' },
  { path: '/student/games', label: 'Trò chơi' },
]

// Click outside handlers
const avatarWrapper = ref<HTMLElement | null>(null)
onClickOutside(avatarWrapper, () => {
  avatarOpen.value = false
})

const mobileMenuWrapper = ref<HTMLElement | null>(null)
onClickOutside(mobileMenuWrapper, (event) => {
  const target = event.target as HTMLElement
  const isHamburgerClick = target.closest('button[aria-label="Mở menu"]')
  if (!isHamburgerClick) {
    open.value = false
  }
})

function isActive(path: string) {
  if (path === '/student/dashboard') return route.path === path
  return route.path.startsWith(path)
}

function getMenuClass(path: string) {
  if (isActive(path)) {
    return isDark.value
      ? 'bg-gradient-to-r from-cyan-500 to-purple-500 text-white'
      : 'bg-slate-800 text-white shadow-sm'
  }
  return isDark.value 
    ? 'text-gray-300 hover:text-white hover:bg-white/10' 
    : 'text-gray-700 hover:text-gray-900 hover:bg-gray-100'
}

function handleAvatarError(event: Event) {
  const img = event.target as HTMLImageElement
  const defaultAvatar = getAvatarSrc(null, auth.user?.gender as 'male' | 'female' | 'other' | null | undefined, 'student')
  img.src = defaultAvatar
}

async function handleLogout() {
  try {
    isLoggingOut.value = true
    avatarOpen.value = false
    open.value = false

    if (typeof auth.logout === 'function') {
      await auth.logout()
    } else {
      auth.token = null
      auth.user = null
      localStorage.removeItem('auth')
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      sessionStorage.removeItem('accessToken')
      sessionStorage.removeItem('refreshToken')
    }
    
    await new Promise(resolve => setTimeout(resolve, 100))
    await router.push('/auth/login')
  } catch (error) {
    console.error('Logout error:', error)
    await router.push('/auth/login')
  } finally {
    isLoggingOut.value = false
  }
}

onMounted(() => {
  if (typeof auth.refreshProfile === 'function') {
    auth.refreshProfile().catch(() => {})
  }
})
</script>
