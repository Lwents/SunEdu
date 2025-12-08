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
        class="h-7 w-7 sm:h-8 sm:w-8 rounded-full object-cover aspect-square cursor-pointer"
        :src="avatarSrc"
        alt="avatar"
        @error="handleAvatarError"
        @mousedown="startSecretHold"
        @mouseup="cancelSecretHold"
        @mouseleave="cancelSecretHold"
        @touchstart.prevent="startSecretHold"
        @touchend="cancelSecretHold"
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

    <!-- Secret AI Settings Popup -->
    <Teleport to="body">
      <div v-if="showSecretPopup" class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/60">
        <div class="w-full max-w-lg rounded-2xl bg-white p-6 shadow-2xl">
          <div class="mb-4 flex items-center justify-between">
            <h3 class="text-lg font-bold text-gray-900">🔐 Cài đặt AI (Ẩn)</h3>
            <button
              type="button"
              class="rounded-lg p-1 text-gray-400 hover:bg-gray-100 hover:text-gray-600"
              @click="showSecretPopup = false"
            >
              <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div class="space-y-4">
            <!-- AI Toggle -->
            <div class="flex items-center justify-between rounded-lg border border-gray-200 p-4">
              <div>
                <div class="font-medium text-gray-900">Bật/Tắt AI</div>
                <div class="text-sm text-gray-500">Cho phép sử dụng tính năng AI trong hệ thống</div>
              </div>
              <el-switch v-model="aiSettings.enabled" size="large" />
            </div>

            <!-- Gemini API Key -->
            <div class="rounded-lg border border-gray-200 p-4">
              <label class="mb-2 block font-medium text-gray-900">GEMINI_API_KEY</label>
              <div class="flex gap-2">
                <el-input
                  v-model="aiSettings.geminiKey"
                  :type="showGeminiKey ? 'text' : 'password'"
                  placeholder="Nhập key mới hoặc để trống giữ nguyên..."
                  class="flex-1"
                  @focus="onKeyFocus('gemini')"
                />
                <el-button @click="showGeminiKey = !showGeminiKey">
                  {{ showGeminiKey ? '🙈' : '👁️' }}
                </el-button>
              </div>
              <p class="mt-1 text-xs text-gray-500">Nhập key mới để thay đổi, hoặc để trống để giữ nguyên</p>
            </div>

            <!-- DeepSeek API Key -->
            <div class="rounded-lg border border-gray-200 p-4">
              <label class="mb-2 block font-medium text-gray-900">DEEPSEEK_API_KEY</label>
              <div class="flex gap-2">
                <el-input
                  v-model="aiSettings.deepseekKey"
                  :type="showDeepseekKey ? 'text' : 'password'"
                  placeholder="Nhập key mới hoặc để trống giữ nguyên..."
                  class="flex-1"
                  @focus="onKeyFocus('deepseek')"
                />
                <el-button @click="showDeepseekKey = !showDeepseekKey">
                  {{ showDeepseekKey ? '🙈' : '👁️' }}
                </el-button>
              </div>
              <p class="mt-1 text-xs text-gray-500">Nhập key mới để thay đổi, hoặc để trống để giữ nguyên</p>
            </div>

            <!-- AI Model -->
            <div class="rounded-lg border border-gray-200 p-4">
              <label class="mb-2 block font-medium text-gray-900">Model mặc định</label>
              <el-select v-model="aiSettings.defaultModel" class="w-full">
                <el-option value="gemini-2.5-flash" label="Gemini 2.5 Flash" />
                <el-option value="gemini-2.0-flash" label="Gemini 2.0 Flash" />
                <el-option value="gemini-1.5-pro" label="Gemini 1.5 Pro" />
                <el-option value="deepseek-chat" label="DeepSeek Chat" />
              </el-select>
            </div>

            <div class="rounded-lg border border-amber-200 bg-amber-50 p-3">
              <p class="text-xs text-amber-700">
                ⚠️ Giữ avatar 5 giây để mở popup này. Cài đặt sẽ được lưu vào hệ thống.
              </p>
            </div>
          </div>

          <div class="mt-6 flex justify-end gap-3">
            <el-button @click="showSecretPopup = false">Đóng</el-button>
            <el-button type="primary" :loading="savingAI" @click="saveAISettings">
              Lưu cài đặt
            </el-button>
          </div>
        </div>
      </div>
    </Teleport>
  </header>
</template>

<script setup lang="ts">
import { ref, reactive, computed, defineEmits, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth.store'
import ConfirmLogout from '@/components/ui/ConfirmLogout.vue'
import { LogOut } from 'lucide-vue-next'
import { getAvatarSrc } from '@/utils/avatar'
import http from '@/config/axios'
import { showToast } from '@/utils/toast'
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

// Secret AI Settings
const showSecretPopup = ref(false)
const savingAI = ref(false)
const showGeminiKey = ref(false)
const showDeepseekKey = ref(false)
let secretHoldTimer: ReturnType<typeof setTimeout> | null = null

const aiSettings = reactive({
  enabled: true,
  geminiKey: '',
  deepseekKey: '',
  defaultModel: 'gemini-2.5-flash'
})

function startSecretHold() {
  secretHoldTimer = setTimeout(() => {
    showSecretPopup.value = true
    loadAISettings()
  }, 5000) // 5 seconds
}

function cancelSecretHold() {
  if (secretHoldTimer) {
    clearTimeout(secretHoldTimer)
    secretHoldTimer = null
  }
}

async function loadAISettings() {
  try {
    const { data } = await http.get('/admin/system/ai-settings/')
    aiSettings.enabled = data.enabled ?? true
    aiSettings.geminiKey = data.gemini_key || ''
    aiSettings.deepseekKey = data.deepseek_key || ''
    aiSettings.defaultModel = data.default_model || 'gemini-2.5-flash'
  } catch (e) {
    // Ignore - settings might not exist yet
  }
}

function onKeyFocus(type: 'gemini' | 'deepseek') {
  // Xóa key masked khi focus để nhập key mới
  if (type === 'gemini' && aiSettings.geminiKey.includes('***')) {
    aiSettings.geminiKey = ''
  }
  if (type === 'deepseek' && aiSettings.deepseekKey.includes('***')) {
    aiSettings.deepseekKey = ''
  }
}

async function saveAISettings() {
  savingAI.value = true
  try {
    await http.post('/admin/system/ai-settings/', {
      enabled: aiSettings.enabled,
      gemini_key: aiSettings.geminiKey,
      deepseek_key: aiSettings.deepseekKey,
      default_model: aiSettings.defaultModel
    })
    showToast('Đã lưu cài đặt AI', 'success')
    showSecretPopup.value = false
  } catch (e: any) {
    showToast(e.response?.data?.detail || 'Không thể lưu cài đặt', 'error')
  } finally {
    savingAI.value = false
  }
}

onBeforeUnmount(() => {
  cancelSecretHold()
})

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
