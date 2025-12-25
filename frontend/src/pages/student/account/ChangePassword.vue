<template>
  <div class="page-wrapper" :class="isDark ? 'dark-mode' : 'light-mode'">
    <!-- Background Elements -->
    <div v-if="isDark" class="bg-elements">
      <div class="glow glow-1"></div>
      <div class="glow glow-2"></div>
    </div>

    <div class="page-content">
      <!-- Tabs -->
      <div class="tabs-nav">
        <button type="button" class="tab-btn" @click="goProfile">Cá nhân</button>
        <button type="button" class="tab-btn active">Đổi mật khẩu</button>
        <button type="button" class="tab-btn" @click="goParent">Phụ huynh</button>
      </div>

      <!-- Main Card -->
      <div class="main-card">
        <div class="card-header">
          <h2>Đổi mật khẩu</h2>
        </div>

        <form class="card-body" @submit.prevent="changePassword">
          <!-- Current Password -->
          <div class="form-row">
            <label class="form-label">Mật khẩu hiện tại <span class="required">*</span></label>
            <div class="form-field">
              <div class="input-wrapper">
                <input
                  :type="show.current ? 'text' : 'password'"
                  v-model="currentPasswordModel"
                  autocomplete="current-password"
                  placeholder="Nhập mật khẩu hiện tại"
                  @blur="touched.current = true"
                  class="form-input"
                  :class="{ 'has-error': touched.current && errs.current }"
                  :maxlength="MAX_PASSWORD_LENGTH"
                />
                <button type="button" class="toggle-btn" @click="show.current = !show.current">
                  <svg v-if="show.current" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
                  </svg>
                  <svg v-else class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.644C3.423 7.51 7.36 4.5 12 4.5c4.66 0 8.597 3.01 9.964 7.178a1.012 1.012 0 010 .644C20.597 16.49 16.66 19.5 12 19.5c-4.66 0-8.597-3.01-9.964-7.178z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </button>
              </div>
              <p v-if="touched.current && errs.current" class="error-text">{{ errs.current }}</p>
            </div>
          </div>

          <!-- New Password -->
          <div class="form-row">
            <label class="form-label">Mật khẩu mới <span class="required">*</span></label>
            <div class="form-field">
              <div class="input-wrapper">
                <input
                  :type="show.new1 ? 'text' : 'password'"
                  v-model="newPasswordModel"
                  autocomplete="new-password"
                  placeholder="Nhập mật khẩu mới (6-12 ký tự)"
                  @blur="touched.new1 = true"
                  class="form-input"
                  :class="{ 'has-error': touched.new1 && errs.new1 }"
                  :maxlength="MAX_PASSWORD_LENGTH"
                />
                <button type="button" class="toggle-btn" @click="show.new1 = !show.new1">
                  <svg v-if="show.new1" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
                  </svg>
                  <svg v-else class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.644C3.423 7.51 7.36 4.5 12 4.5c4.66 0 8.597 3.01 9.964 7.178a1.012 1.012 0 010 .644C20.597 16.49 16.66 19.5 12 19.5c-4.66 0-8.597-3.01-9.964-7.178z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </button>
              </div>
              <p v-if="touched.new1 && errs.new1" class="error-text">{{ errs.new1 }}</p>
            </div>
          </div>

          <!-- Confirm New Password -->
          <div class="form-row">
            <label class="form-label">Nhập lại mật khẩu mới <span class="required">*</span></label>
            <div class="form-field">
              <div class="input-wrapper">
                <input
                  :type="show.new2 ? 'text' : 'password'"
                  v-model="confirmPasswordModel"
                  autocomplete="new-password"
                  placeholder="Nhập lại mật khẩu mới"
                  @blur="touched.new2 = true"
                  class="form-input"
                  :class="{ 'has-error': touched.new2 && errs.new2 }"
                  :maxlength="MAX_PASSWORD_LENGTH"
                />
                <button type="button" class="toggle-btn" @click="show.new2 = !show.new2">
                  <svg v-if="show.new2" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
                  </svg>
                  <svg v-else class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.644C3.423 7.51 7.36 4.5 12 4.5c4.66 0 8.597 3.01 9.964 7.178a1.012 1.012 0 010 .644C20.597 16.49 16.66 19.5 12 19.5c-4.66 0-8.597-3.01-9.964-7.178z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </button>
              </div>
              <p v-if="touched.new2 && errs.new2" class="error-text">{{ errs.new2 }}</p>
            </div>
          </div>

          <!-- Submit Button -->
          <div class="form-actions">
            <button type="submit" class="btn-primary" :disabled="isSubmitDisabled">
              <span v-if="saving || otp.sending" class="spinner"></span>
              {{ saving || otp.sending ? 'Đang xử lý...' : 'Cập nhật mật khẩu' }}
            </button>
          </div>
        </form>

        <!-- OTP Modal -->
        <Transition enter-active-class="transition-opacity duration-200" leave-active-class="transition-opacity duration-150" enter-from-class="opacity-0" leave-to-class="opacity-0">
          <div v-if="otpModalVisible" class="modal-overlay" @click.self="closeOtpModal">
            <div class="modal-content">
              <div class="modal-header">
                <div>
                  <h3>Nhập mã OTP xác thực</h3>
                  <p>OTP đã gửi tới {{ otp.sentTo || maskedEmail || 'email của bạn' }}.</p>
                </div>
                <button type="button" class="modal-close" @click="closeOtpModal">
                  <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <div class="otp-input-wrapper">
                <input
                  v-model.trim="otp.code"
                  maxlength="6"
                  inputmode="numeric"
                  placeholder="000000"
                  @blur="touched.otp = true"
                  class="otp-input"
                  :class="{ 'has-error': touched.otp && errs.otp }"
                />
                <p v-if="touched.otp && errs.otp" class="error-text">{{ errs.otp }}</p>
              </div>

              <div class="modal-actions">
                <button type="button" class="btn-primary" :disabled="saving" @click="submitOtp">
                  <span v-if="saving" class="spinner"></span>
                  Xác nhận
                </button>
                <button type="button" class="btn-outline" :disabled="otp.countdown > 0 || otp.sending" @click="sendOtp()">
                  <span v-if="otp.sending">Đang gửi…</span>
                  <span v-else-if="otp.countdown > 0">Gửi lại ({{ otp.countdown }}s)</span>
                  <span v-else>Gửi lại OTP</span>
                </button>
              </div>
            </div>
          </div>
        </Transition>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, watch, computed, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth.store'
import { useThemeStore } from '@/store/theme.store'
import { showToast } from '@/utils/toast'

const router = useRouter()
const auth = useAuthStore()
const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)

const MAX_PASSWORD_LENGTH = 12
const clampPassword = (value: string) => String(value ?? '').trim().slice(0, MAX_PASSWORD_LENGTH)

const goProfile = () => router.push({ name: 'student-profile' })
const goParent = () => router.push({ name: 'student-parent' })

const pwd = reactive({ current: '', new1: '', new2: '' })
const currentPasswordModel = computed({
  get: () => pwd.current,
  set: (value) => {
    pwd.current = clampPassword(value)
  },
})
const newPasswordModel = computed({
  get: () => pwd.new1,
  set: (value) => {
    pwd.new1 = clampPassword(value)
  },
})
const confirmPasswordModel = computed({
  get: () => pwd.new2,
  set: (value) => {
    pwd.new2 = clampPassword(value)
  },
})
const show = reactive({ current: false, new1: false, new2: false })
const touched = reactive({ current: false, new1: false, new2: false, otp: false })
const errs = reactive<{ current: string; new1: string; new2: string; otp: string }>({ current: '', new1: '', new2: '', otp: '' })

const otp = reactive({ code: '', countdown: 0, sending: false, sentTo: '', requested: false })
const otpModalVisible = ref(false)
const OTP_COUNTDOWN = 60
let countdownTimer: number | undefined

const maskedEmail = computed(() => {
  const email = auth.user?.email || ''
  if (!email || !email.includes('@')) return ''
  const [local, domain] = email.split('@')
  if (local.length <= 2) return `${local[0]}***@${domain}`
  return `${local[0]}***${local[local.length - 1]}@${domain}`
})

watch(() => otp.code, () => {
  if (!otp.requested) { errs.otp = ''; return }
  if (!otp.code) errs.otp = 'Vui lòng nhập OTP.'
  else if (otp.code.length !== 6) errs.otp = 'OTP gồm 6 chữ số.'
  else errs.otp = ''
}, { immediate: true })

watch(() => pwd.current, () => { errs.current = pwd.current ? '' : 'Vui lòng nhập mật khẩu hiện tại.' }, { immediate: true })

watch(() => [pwd.new1, pwd.current], ([newPassword, currentPassword]) => {
  if (!newPassword || newPassword.length < 6) errs.new1 = 'Mật khẩu mới tối thiểu 6 ký tự.'
  else if (currentPassword && newPassword === currentPassword) errs.new1 = 'Mật khẩu mới trùng mật khẩu cũ.'
  else errs.new1 = ''
  errs.new2 = pwd.new2 === newPassword ? '' : 'Xác nhận mật khẩu chưa khớp.'
}, { immediate: true })

watch(() => pwd.new2, () => { errs.new2 = pwd.new2 === pwd.new1 ? '' : 'Xác nhận mật khẩu chưa khớp.' }, { immediate: true })

const credentialsValid = computed(() => !!pwd.current && pwd.new1.length >= 6 && pwd.new1 !== pwd.current && pwd.new2 === pwd.new1 && !errs.current && !errs.new1 && !errs.new2)
const otpValid = computed(() => otp.requested && otp.code.length === 6 && !errs.otp)
const isSubmitDisabled = computed(() => { if (saving.value) return true; if (!otp.requested) return !credentialsValid.value || otp.sending; return false })

const saving = ref(false)

async function changePassword() {
  touched.current = touched.new1 = touched.new2 = true
  if (!credentialsValid.value) return
  if (!otp.requested) { const requested = await sendOtp(); if (requested) otpModalVisible.value = true; return }
  otpModalVisible.value = true
}

async function submitOtp() {
  touched.otp = true
  if (!otpValid.value) return
  saving.value = true
  try {
    await auth.changePasswordWithOtp(otp.code, pwd.new1)
    showToast('Đổi mật khẩu thành công!', 'success')
    resetForm()
  } catch (e) {
    const message = e instanceof Error ? e.message : 'Có lỗi xảy ra, vui lòng thử lại.'
    showToast(message, 'error')
  } finally { saving.value = false }
}

function resetForm() {
  pwd.current = ''; pwd.new1 = ''; pwd.new2 = ''
  otp.code = ''; otp.sentTo = ''; otp.requested = false; otp.countdown = 0
  touched.current = touched.new1 = touched.new2 = touched.otp = false
  errs.otp = ''
  clearCountdown()
  closeOtpModal()
}

function clearCountdown() { if (countdownTimer) { window.clearInterval(countdownTimer); countdownTimer = undefined } }

async function sendOtp(showSuccess = true) {
  if (otp.sending || otp.countdown > 0) return false
  if (!pwd.current) { touched.current = true; errs.current = 'Vui lòng nhập mật khẩu hiện tại.'; return false }
  otp.sending = true
  try {
    const res = await auth.requestPasswordOtp(pwd.current)
    otp.sentTo = res?.email || maskedEmail.value || ''
    otp.requested = true; otp.code = ''; touched.otp = false; errs.otp = ''
    if (showSuccess) showToast('Đã gửi OTP đến email của bạn.', 'success')
    otp.countdown = OTP_COUNTDOWN
    clearCountdown()
    countdownTimer = window.setInterval(() => { if (otp.countdown > 0) otp.countdown -= 1; else clearCountdown() }, 1000)
    return true
  } catch (e) {
    const message = e instanceof Error ? e.message : 'Không gửi được OTP. Thử lại sau.'
    if (message.toLowerCase().includes('mật khẩu') && message.toLowerCase().includes('không chính xác')) { errs.current = message; touched.current = true }
    showToast(message, 'error')
    return false
  } finally { otp.sending = false }
}

function closeOtpModal() { otpModalVisible.value = false }
onUnmounted(() => clearCountdown())
</script>

<style scoped>
.page-wrapper { min-height: 100vh; position: relative; transition: background-color 0.3s ease; }
.page-wrapper.dark-mode { background: #020617; }
.page-wrapper.light-mode { background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%); }

.bg-elements { position: fixed; inset: 0; pointer-events: none; z-index: 0; }
.glow { position: absolute; border-radius: 50%; filter: blur(100px); }
.glow-1 { top: 10%; left: -5%; width: 300px; height: 300px; background: rgba(6, 182, 212, 0.1); }
.glow-2 { bottom: 10%; right: -5%; width: 250px; height: 250px; background: rgba(139, 92, 246, 0.1); }

.page-content { position: relative; z-index: 10; max-width: 800px; margin: 0 auto; padding: 24px 16px; }

.tabs-nav { display: flex; align-items: center; gap: 8px; margin-bottom: 24px; border-bottom: 1px solid; padding-bottom: 0; }
.dark-mode .tabs-nav { border-color: rgba(255,255,255,0.08); }
.light-mode .tabs-nav { border-color: #e2e8f0; }

.tab-btn { padding: 12px 16px; font-size: 14px; font-weight: 500; border: none; background: transparent; cursor: pointer; transition: all 0.3s; border-bottom: 2px solid transparent; margin-bottom: -1px; }
.dark-mode .tab-btn { color: #64748b; }
.light-mode .tab-btn { color: #64748b; }
.tab-btn:hover { }
.dark-mode .tab-btn:hover { color: white; }
.light-mode .tab-btn:hover { color: #1e293b; }
.tab-btn.active { font-weight: 600; }
.dark-mode .tab-btn.active { color: #06b6d4; border-color: #06b6d4; }
.light-mode .tab-btn.active { color: #1e293b; border-color: #1e293b; }

.main-card { border-radius: 16px; overflow: hidden; }
.dark-mode .main-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); }
.light-mode .main-card { background: white; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }

.card-header { padding: 16px 24px; border-bottom: 1px solid; }
.dark-mode .card-header { border-color: rgba(255,255,255,0.08); }
.light-mode .card-header { border-color: #e2e8f0; }
.card-header h2 { font-size: 18px; font-weight: 600; margin: 0; }
.dark-mode .card-header h2 { color: white; }
.light-mode .card-header h2 { color: #1e293b; }

.card-body { padding: 24px; display: flex; flex-direction: column; gap: 24px; }

.form-row { display: grid; gap: 12px; }
@media (min-width: 1024px) { .form-row { grid-template-columns: 180px 1fr; } }

.form-label { font-size: 14px; font-weight: 500; padding-top: 8px; }
.dark-mode .form-label { color: #94a3b8; }
.light-mode .form-label { color: #64748b; }
.required { color: #ef4444; }

.form-field { display: flex; flex-direction: column; gap: 4px; }
.input-wrapper { position: relative; }

.form-input { width: 100%; padding: 10px 40px 10px 12px; border-radius: 10px; font-size: 14px; outline: none; transition: all 0.3s; }
.dark-mode .form-input { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: white; }
.light-mode .form-input { background: #f8fafc; border: 1px solid #e2e8f0; color: #1e293b; }
.form-input:focus { }
.dark-mode .form-input:focus { border-color: #06b6d4; }
.light-mode .form-input:focus { border-color: #6366f1; }
.form-input.has-error { }
.dark-mode .form-input.has-error { border-color: #ef4444; }
.light-mode .form-input.has-error { border-color: #ef4444; }

.toggle-btn { position: absolute; inset-y: 0; right: 0; width: 40px; display: flex; align-items: center; justify-content: center; border: none; background: transparent; cursor: pointer; transition: all 0.3s; }
.dark-mode .toggle-btn { color: #64748b; }
.light-mode .toggle-btn { color: #94a3b8; }
.toggle-btn:hover { }
.dark-mode .toggle-btn:hover { color: white; }
.light-mode .toggle-btn:hover { color: #1e293b; }
.icon { width: 20px; height: 20px; }

.error-text { font-size: 12px; color: #ef4444; }

.form-actions { display: flex; flex-direction: column; gap: 12px; padding-top: 16px; border-top: 1px solid; }
@media (min-width: 640px) { .form-actions { flex-direction: row; align-items: center; justify-content: flex-end; } }
.dark-mode .form-actions { border-color: rgba(255,255,255,0.08); }
.light-mode .form-actions { border-color: #e2e8f0; }

.btn-primary { display: inline-flex; align-items: center; justify-content: center; gap: 8px; padding: 10px 24px; border-radius: 10px; font-size: 14px; font-weight: 600; border: none; cursor: pointer; transition: all 0.3s; }
.dark-mode .btn-primary { background: linear-gradient(135deg, #06b6d4, #8b5cf6); color: white; }
.light-mode .btn-primary { background: #1e293b; color: white; }
.btn-primary:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

.btn-outline { display: inline-flex; align-items: center; justify-content: center; gap: 8px; padding: 10px 24px; border-radius: 10px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.3s; }
.dark-mode .btn-outline { background: transparent; border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; }
.light-mode .btn-outline { background: white; border: 1px solid #e2e8f0; color: #64748b; }
.btn-outline:hover { transform: translateY(-1px); }
.dark-mode .btn-outline:hover { border-color: #06b6d4; color: #06b6d4; }
.light-mode .btn-outline:hover { border-color: #6366f1; color: #6366f1; }
.btn-outline:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

.spinner { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.modal-overlay { position: fixed; inset: 0; z-index: 50; display: flex; align-items: center; justify-content: center; padding: 16px; }
.dark-mode .modal-overlay { background: rgba(0,0,0,0.7); }
.light-mode .modal-overlay { background: rgba(15,23,42,0.5); }

.modal-content { width: 100%; max-width: 400px; border-radius: 16px; padding: 24px; }
.dark-mode .modal-content { background: #0f172a; border: 1px solid rgba(255,255,255,0.1); }
.light-mode .modal-content { background: white; border: 1px solid #e2e8f0; box-shadow: 0 20px 40px rgba(0,0,0,0.15); }

.modal-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; }
.modal-header h3 { font-size: 18px; font-weight: 600; margin: 0; }
.dark-mode .modal-header h3 { color: white; }
.light-mode .modal-header h3 { color: #1e293b; }
.modal-header p { font-size: 14px; margin: 4px 0 0; }
.dark-mode .modal-header p { color: #64748b; }
.light-mode .modal-header p { color: #64748b; }

.modal-close { padding: 4px; border-radius: 6px; border: none; background: transparent; cursor: pointer; transition: all 0.3s; }
.dark-mode .modal-close { color: #64748b; }
.light-mode .modal-close { color: #94a3b8; }
.modal-close:hover { }
.dark-mode .modal-close:hover { background: rgba(255,255,255,0.05); color: white; }
.light-mode .modal-close:hover { background: #f1f5f9; color: #1e293b; }

.otp-input-wrapper { margin-top: 24px; display: flex; flex-direction: column; gap: 4px; }
.otp-input { width: 100%; padding: 12px 16px; border-radius: 10px; font-size: 18px; font-weight: 600; text-align: center; letter-spacing: 0.4em; outline: none; transition: all 0.3s; }
.dark-mode .otp-input { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: white; }
.light-mode .otp-input { background: #f8fafc; border: 1px solid #e2e8f0; color: #1e293b; }
.otp-input:focus { }
.dark-mode .otp-input:focus { border-color: #06b6d4; }
.light-mode .otp-input:focus { border-color: #6366f1; }
.otp-input.has-error { border-color: #ef4444; }

.modal-actions { margin-top: 16px; display: flex; flex-direction: column; gap: 12px; }
@media (min-width: 640px) { .modal-actions { flex-direction: row; align-items: center; justify-content: space-between; } }
</style>
