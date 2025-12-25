<!-- src/components/shared/AdminNavbar.vue -->
<template>
  <header class="navbar" :class="isDark ? 'dark' : 'light'">
    <!-- Left: Hamburger + title -->
    <div class="navbar-left">
      <button class="menu-btn" aria-label="Mở menu" @click="$emit('toggle-sidebar')">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
      <h1 class="page-title">{{ pageTitle }}</h1>
    </div>

    <!-- Right: actions -->
    <div class="navbar-right">
      <!-- Theme Toggle -->
      <button class="theme-btn" @click="toggleTheme" :title="isDark ? 'Chế độ sáng' : 'Chế độ tối'">
        <svg v-if="isDark" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
        <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
        </svg>
      </button>

      <!-- Notifications -->
      <NotificationBell :user-id="auth.user?.id" role="admin" />

      <!-- User Info -->
      <div class="user-info">
        <span class="user-name">{{ user?.name || 'Admin' }}</span>
        <span class="user-email">{{ user?.email || 'admin@example.com' }}</span>
      </div>

      <!-- Avatar -->
      <img
        class="avatar"
        :src="avatarSrc"
        alt="avatar"
        @error="handleAvatarError"
        @mousedown="startSecretHold"
        @mouseup="cancelSecretHold"
        @mouseleave="cancelSecretHold"
        @touchstart.prevent="startSecretHold"
        @touchend="cancelSecretHold"
      />

      <!-- Logout -->
      <button class="logout-btn" @click="showConfirm = true">
        <LogOut class="h-4 w-4" />
        <span class="logout-text">Đăng xuất</span>
      </button>
    </div>

    <ConfirmLogout :open="showConfirm" @update:open="showConfirm = $event" @confirm="handleLogout" />

    <!-- Secret AI Settings Popup -->
    <Teleport to="body">
      <div v-if="showSecretPopup" class="secret-overlay">
        <div class="secret-popup" :class="isDark ? 'dark' : 'light'">
          <div class="popup-header">
            <h3>🔐 Cài đặt AI (Ẩn)</h3>
            <button type="button" class="close-popup" @click="showSecretPopup = false">
              <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div class="popup-content">
            <!-- AI Toggle -->
            <div class="setting-item">
              <div>
                <div class="setting-title">Bật/Tắt AI</div>
                <div class="setting-desc">Cho phép sử dụng tính năng AI trong hệ thống</div>
              </div>
              <el-switch v-model="aiSettings.enabled" size="large" />
            </div>

            <!-- OpenRouter API Key -->
            <div class="setting-item vertical">
              <label class="setting-title">OPENROUTER_API_KEY</label>
              <div class="key-input">
                <el-input
                  v-model="aiSettings.openrouterKey"
                  :type="showOpenrouterKey ? 'text' : 'password'"
                  placeholder="Nhập key mới hoặc để trống giữ nguyên..."
                  @focus="onKeyFocus('openrouter')"
                />
                <el-button @click="showOpenrouterKey = !showOpenrouterKey">
                  {{ showOpenrouterKey ? '🙈' : '👁️' }}
                </el-button>
              </div>
              <p class="setting-hint">Nhập key mới để thay đổi, hoặc để trống để giữ nguyên</p>
            </div>

            <!-- DeepSeek API Key -->
            <div class="setting-item vertical">
              <label class="setting-title">DEEPSEEK_API_KEY</label>
              <div class="key-input">
                <el-input
                  v-model="aiSettings.deepseekKey"
                  :type="showDeepseekKey ? 'text' : 'password'"
                  placeholder="Nhập key mới hoặc để trống giữ nguyên..."
                  @focus="onKeyFocus('deepseek')"
                />
                <el-button @click="showDeepseekKey = !showDeepseekKey">
                  {{ showDeepseekKey ? '🙈' : '👁️' }}
                </el-button>
              </div>
              <p class="setting-hint">Nhập key mới để thay đổi, hoặc để trống để giữ nguyên</p>
            </div>

            <!-- AI Model -->
            <div class="setting-item vertical">
              <label class="setting-title">Model mặc định</label>
              <el-select v-model="aiSettings.defaultModel" class="w-full">
                <el-option value="openai/gpt-4o" label="GPT-4o" />
                <el-option value="openai/gpt-4o-mini" label="GPT-4o Mini" />
                <el-option value="deepseek/deepseek-chat-v3-0324" label="DeepSeek Chat V3" />
              </el-select>
            </div>

            <div class="setting-warning">
              ⚠️ Giữ avatar 5 giây để mở popup này. Cài đặt sẽ được lưu vào hệ thống.
            </div>
          </div>

          <div class="popup-footer">
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
import { ref, reactive, computed, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth.store'
import { useThemeStore } from '@/store/theme.store'
import ConfirmLogout from '@/components/ui/ConfirmLogout.vue'
import { LogOut } from 'lucide-vue-next'
import { getAvatarSrc } from '@/utils/avatar'
import http from '@/config/axios'
import { showToast } from '@/utils/toast'
import NotificationBell from '@/components/shared/NotificationBell.vue'

const emit = defineEmits(['toggle-sidebar'])

const auth = useAuthStore()
const themeStore = useThemeStore()
const user = computed(() => auth.user)
const isDark = computed(() => themeStore.isDark)

const route = useRoute()
const router = useRouter()

function toggleTheme() {
  themeStore.toggleTheme()
}

const avatarSrc = computed(() => {
  return getAvatarSrc(
    auth.user?.avatar,
    auth.user?.gender as 'male' | 'female' | 'other' | null | undefined,
    'admin'
  )
})

const pageTitle = computed(() => {
  const matched = [...route.matched].reverse().find((r) => r.meta?.title) as any
  const raw = matched?.meta?.title
  const title = typeof raw === 'function' ? raw(route) : raw
  return title || 'Admin'
})

// Confirm popup
const showConfirm = ref(false)

// Secret AI Settings
const showSecretPopup = ref(false)
const savingAI = ref(false)
const showOpenrouterKey = ref(false)
const showDeepseekKey = ref(false)
let secretHoldTimer: ReturnType<typeof setTimeout> | null = null

const aiSettings = reactive({
  enabled: true,
  openrouterKey: '',
  deepseekKey: '',
  defaultModel: 'openai/gpt-4o'
})

function startSecretHold() {
  secretHoldTimer = setTimeout(() => {
    showSecretPopup.value = true
    loadAISettings()
  }, 5000)
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
    aiSettings.openrouterKey = data.openrouter_key || ''
    aiSettings.deepseekKey = data.deepseek_key || ''
    aiSettings.defaultModel = data.default_model || 'openai/gpt-4o'
  } catch {
    // Ignore
  }
}

function onKeyFocus(type: 'openrouter' | 'deepseek') {
  if (type === 'openrouter' && aiSettings.openrouterKey.includes('***')) {
    aiSettings.openrouterKey = ''
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
      openrouter_key: aiSettings.openrouterKey,
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
  const defaultAvatar = getAvatarSrc(null, auth.user?.gender as 'male' | 'female' | 'other' | null | undefined, 'admin')
  img.src = defaultAvatar
}

async function handleLogout() {
  try {
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
  } catch {
    await router.push('/auth/login')
  }
}
</script>

<style scoped>
.navbar {
  display: flex;
  height: 100%;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  transition: all 0.3s ease;
}

.navbar.dark {
  background: rgba(15, 23, 42, 0.95);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.navbar.light {
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
}

/* Left */
.navbar-left {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
  flex: 1;
}

.menu-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px;
  border-radius: 8px;
  transition: all 0.2s;
}

@media (min-width: 768px) {
  .menu-btn {
    display: none;
  }
}

.navbar.dark .menu-btn {
  color: #94a3b8;
}

.navbar.dark .menu-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.navbar.light .menu-btn {
  color: #64748b;
}

.navbar.light .menu-btn:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.page-title {
  font-size: 16px;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.navbar.dark .page-title {
  color: white;
}

.navbar.light .page-title {
  color: #1e293b;
}

/* Right */
.navbar-right {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.theme-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px;
  border-radius: 8px;
  transition: all 0.2s;
}

.navbar.dark .theme-btn {
  color: #fbbf24;
}

.navbar.dark .theme-btn:hover {
  background: rgba(251, 191, 36, 0.1);
}

.navbar.light .theme-btn {
  color: #6366f1;
}

.navbar.light .theme-btn:hover {
  background: #eff6ff;
}

.user-info {
  display: none;
  flex-direction: column;
  align-items: flex-end;
}

@media (min-width: 1024px) {
  .user-info {
    display: flex;
  }
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  line-height: 1.2;
}

.navbar.dark .user-name {
  color: white;
}

.navbar.light .user-name {
  color: #1e293b;
}

.user-email {
  font-size: 12px;
  line-height: 1.2;
}

.navbar.dark .user-email {
  color: #64748b;
}

.navbar.light .user-email {
  color: #94a3b8;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  cursor: pointer;
  transition: all 0.2s;
}

.navbar.dark .avatar {
  border: 2px solid rgba(255, 255, 255, 0.1);
}

.navbar.light .avatar {
  border: 2px solid #e2e8f0;
}

.avatar:hover {
  transform: scale(1.05);
}

.logout-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  color: white;
  background: #ef4444;
  transition: all 0.2s;
}

.logout-btn:hover {
  background: #dc2626;
  transform: translateY(-1px);
}

.logout-text {
  display: none;
}

@media (min-width: 640px) {
  .logout-text {
    display: inline;
  }
}

/* Secret Popup */
.secret-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
}

.secret-popup {
  width: 100%;
  max-width: 500px;
  margin: 16px;
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.secret-popup.dark {
  background: #1e293b;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.secret-popup.light {
  background: white;
  border: 1px solid #e2e8f0;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.popup-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid;
}

.secret-popup.dark .popup-header {
  border-color: rgba(255, 255, 255, 0.1);
}

.secret-popup.light .popup-header {
  border-color: #e2e8f0;
}

.popup-header h3 {
  font-size: 18px;
  font-weight: 700;
  margin: 0;
}

.secret-popup.dark .popup-header h3 {
  color: white;
}

.secret-popup.light .popup-header h3 {
  color: #1e293b;
}

.close-popup {
  padding: 6px;
  border-radius: 8px;
  transition: all 0.2s;
}

.secret-popup.dark .close-popup {
  color: #64748b;
}

.secret-popup.dark .close-popup:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.secret-popup.light .close-popup {
  color: #94a3b8;
}

.secret-popup.light .close-popup:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.popup-content {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.setting-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  border-radius: 12px;
}

.setting-item.vertical {
  flex-direction: column;
  align-items: stretch;
  gap: 8px;
}

.secret-popup.dark .setting-item {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.secret-popup.light .setting-item {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
}

.setting-title {
  font-size: 14px;
  font-weight: 600;
}

.secret-popup.dark .setting-title {
  color: white;
}

.secret-popup.light .setting-title {
  color: #1e293b;
}

.setting-desc {
  font-size: 13px;
  margin-top: 2px;
}

.secret-popup.dark .setting-desc {
  color: #64748b;
}

.secret-popup.light .setting-desc {
  color: #94a3b8;
}

.key-input {
  display: flex;
  gap: 8px;
}

.setting-hint {
  font-size: 12px;
  margin: 0;
}

.secret-popup.dark .setting-hint {
  color: #64748b;
}

.secret-popup.light .setting-hint {
  color: #94a3b8;
}

.setting-warning {
  padding: 12px;
  border-radius: 8px;
  font-size: 13px;
  background: rgba(251, 191, 36, 0.1);
  border: 1px solid rgba(251, 191, 36, 0.3);
  color: #fbbf24;
}

.popup-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 20px;
  border-top: 1px solid;
}

.secret-popup.dark .popup-footer {
  border-color: rgba(255, 255, 255, 0.1);
}

.secret-popup.light .popup-footer {
  border-color: #e2e8f0;
}
</style>
