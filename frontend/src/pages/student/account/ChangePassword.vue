<!-- src/pages/student/account/ChangePassword.vue -->
<template>
  <div class="student-shell">
    <div class="student-container">
      <div class="student-tabs flex items-center gap-1 sm:gap-2">
        <button type="button" class="student-tab" @click="goProfile">CÁ NHÂN</button>
        <button type="button" class="student-tab student-tab--active">ĐỔI MẬT KHẨU</button>
        <button type="button" class="student-tab" @click="goParent">PHỤ HUYNH</button>
      </div>

      <div class="student-card mt-4">
        <div class="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <h2 class="text-base font-extrabold uppercase tracking-wide text-slate-900 sm:text-lg">
            ĐỔI MẬT KHẨU
          </h2>
        </div>

        <form class="mt-6 space-y-6" @submit.prevent="changePassword">
          <div class="grid gap-2 sm:gap-3 lg:grid-cols-[220px_1fr]">
            <label class="text-sm font-semibold text-slate-900 sm:text-base lg:pt-2">
              Mật khẩu hiện tại <span class="text-rose-500">*</span>
            </label>
            <div class="space-y-2">
              <div class="relative">
                <input
                  :type="show.current ? 'text' : 'password'"
                  v-model.trim="pwd.current"
                  autocomplete="current-password"
                  @blur="touched.current = true"
                  :class="[
                    'w-full rounded-2xl border px-4 py-2.5 text-sm text-slate-900 shadow-sm shadow-slate-100 transition focus-visible:outline-none focus:ring-4',
                    touched.current && errs.current
                      ? 'border-rose-300 focus:border-rose-400 focus:ring-rose-100'
                      : 'border-slate-200 focus:border-cyan-500 dark:border-cyan-600 focus:ring-cyan-500/30',
                  ]"
                />
                <button
                  type="button"
                  class="absolute inset-y-1 right-1 inline-flex h-10 w-10 items-center justify-center rounded-xl text-slate-400 transition hover:bg-slate-50 hover:text-slate-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-cyan-500"
                  :aria-label="show.current ? 'Ẩn mật khẩu cũ' : 'Hiện mật khẩu cũ'"
                  @click="show.current = !show.current"
                >
                  <svg
                    v-if="show.current"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                    class="h-5 w-5"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88"
                    />
                  </svg>
                  <svg
                    v-else
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                    class="h-5 w-5"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M2.036 12.322a1.012 1.012 0 010-.644C3.423 7.51 7.36 4.5 12 4.5c4.66 0 8.597 3.01 9.964 7.178a1.012 1.012 0 010 .644C20.597 16.49 16.66 19.5 12 19.5c-4.66 0-8.597-3.01-9.964-7.178z"
                    />
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                    />
                  </svg>
                </button>
              </div>
              <p v-if="touched.current && errs.current" class="text-xs font-medium text-rose-600">
                {{ errs.current }}
              </p>
            </div>
          </div>

          <div class="grid gap-2 sm:gap-3 lg:grid-cols-[220px_1fr]">
            <label class="text-sm font-semibold text-slate-900 sm:text-base lg:pt-2">
              Mật khẩu mới <span class="text-rose-500">*</span>
            </label>
            <div class="space-y-2">
              <div class="relative">
                <input
                  :type="show.new1 ? 'text' : 'password'"
                  v-model.trim="pwd.new1"
                  autocomplete="new-password"
                  @blur="touched.new1 = true"
                  :class="[
                    'w-full rounded-2xl border px-4 py-2.5 text-sm text-slate-900 shadow-sm shadow-slate-100 transition focus-visible:outline-none focus:ring-4',
                    touched.new1 && errs.new1
                      ? 'border-rose-300 focus:border-rose-400 focus:ring-rose-100'
                      : 'border-slate-200 focus:border-cyan-500 dark:border-cyan-600 focus:ring-cyan-500/30',
                  ]"
                />
                <button
                  type="button"
                  class="absolute inset-y-1 right-1 inline-flex h-10 w-10 items-center justify-center rounded-xl text-slate-400 transition hover:bg-slate-50 hover:text-slate-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-cyan-500"
                  :aria-label="show.new1 ? 'Ẩn' : 'Hiện'"
                  @click="show.new1 = !show.new1"
                >
                  <svg
                    v-if="show.new1"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                    class="h-5 w-5"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88"
                    />
                  </svg>
                  <svg
                    v-else
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                    class="h-5 w-5"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M2.036 12.322a1.012 1.012 0 010-.644C3.423 7.51 7.36 4.5 12 4.5c4.66 0 8.597 3.01 9.964 7.178a1.012 1.012 0 010 .644C20.597 16.49 16.66 19.5 12 19.5c-4.66 0-8.597-3.01-9.964-7.178z"
                    />
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                    />
                  </svg>
                </button>
              </div>
              <p v-if="touched.new1 && errs.new1" class="text-xs font-medium text-rose-600">
                {{ errs.new1 }}
              </p>
            </div>
          </div>

          <div class="grid gap-2 sm:gap-3 lg:grid-cols-[220px_1fr]">
            <label class="text-sm font-semibold text-slate-900 sm:text-base lg:pt-2">
              Nhập lại mật khẩu mới <span class="text-rose-500">*</span>
            </label>
            <div class="space-y-2">
              <div class="relative">
                <input
                  :type="show.new2 ? 'text' : 'password'"
                  v-model.trim="pwd.new2"
                  autocomplete="new-password"
                  @blur="touched.new2 = true"
                  :class="[
                    'w-full rounded-2xl border px-4 py-2.5 text-sm text-slate-900 shadow-sm shadow-slate-100 transition focus-visible:outline-none focus:ring-4',
                    touched.new2 && errs.new2
                      ? 'border-rose-300 focus:border-rose-400 focus:ring-rose-100'
                      : 'border-slate-200 focus:border-cyan-500 dark:border-cyan-600 focus:ring-cyan-500/30',
                  ]"
                />
                <button
                  type="button"
                  class="absolute inset-y-1 right-1 inline-flex h-10 w-10 items-center justify-center rounded-xl text-slate-400 transition hover:bg-slate-50 hover:text-slate-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-cyan-500"
                  :aria-label="show.new2 ? 'Ẩn' : 'Hiện'"
                  @click="show.new2 = !show.new2"
                >
                  <svg
                    v-if="show.new2"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                    class="h-5 w-5"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88"
                    />
                  </svg>
                  <svg
                    v-else
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                    class="h-5 w-5"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M2.036 12.322a1.012 1.012 0 010-.644C3.423 7.51 7.36 4.5 12 4.5c4.66 0 8.597 3.01 9.964 7.178a1.012 1.012 0 010 .644C20.597 16.49 16.66 19.5 12 19.5c-4.66 0-8.597-3.01-9.964-7.178z"
                    />
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                    />
                  </svg>
                </button>
              </div>
              <p v-if="touched.new2 && errs.new2" class="text-xs font-medium text-rose-600">
                {{ errs.new2 }}
              </p>
            </div>
          </div>

          <div class="flex flex-col gap-3 pt-2 sm:flex-row sm:items-center sm:justify-end">
            <button
              type="submit"
              class="inline-flex w-full items-center justify-center gap-2 rounded-2xl border border-transparent bg-gradient-to-r from-cyan-500 to-cyan-600 px-4 py-3 text-xs font-extrabold uppercase tracking-wide text-white shadow-lg shadow-cyan-500/40 transition hover:from-cyan-600 hover:to-cyan-700 hover:shadow-xl hover:-translate-y-0.5 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-cyan-600 disabled:cursor-not-allowed disabled:opacity-60 disabled:hover:translate-y-0 sm:w-auto sm:text-sm"
              :disabled="isSubmitDisabled"
            >
              <span
                v-if="saving || otp.sending"
                class="h-4 w-4 animate-spin rounded-full border-2 border-white/60 border-t-white"
              ></span>
              CẬP NHẬT MẬT KHẨU
            </button>
          </div>
        </form>

        <Transition
          enter-active-class="transition-opacity duration-200"
          leave-active-class="transition-opacity duration-150"
          enter-from-class="opacity-0"
          leave-to-class="opacity-0"
        >
          <div
            v-if="otpModalVisible"
            class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 px-4 py-10 backdrop-blur-sm"
            @click.self="closeOtpModal"
          >
            <div
              class="w-full max-w-md rounded-3xl border border-slate-200 bg-white p-6 shadow-2xl shadow-slate-200"
            >
              <div class="flex items-start justify-between">
                <div>
                  <h3 class="mt-1 text-xl font-bold text-slate-900">Nhập mã OTP xác thực</h3>
                  <p class="text-sm text-slate-500">
                    OTP đã gửi tới {{ otp.sentTo || maskedEmail || 'email của bạn' }}.
                  </p>
                </div>
                <button
                  type="button"
                  class="rounded-full p-2 text-slate-400 transition hover:bg-slate-100 hover:text-slate-600"
                  aria-label="Đóng"
                  @click="closeOtpModal"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="1.5"
                    class="h-5 w-5"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <div class="mt-6 space-y-2">
                <input
                  v-model.trim="otp.code"
                  maxlength="6"
                  inputmode="numeric"
                  @blur="touched.otp = true"
                  :class="[
                    'w-full rounded-2xl border px-4 py-3 text-center text-lg font-bold tracking-[0.4em] text-slate-900 shadow-sm transition focus-visible:outline-none focus:ring-4',
                    touched.otp && errs.otp
                      ? 'border-rose-300 focus:border-rose-400 focus:ring-rose-100'
                      : 'border-slate-200 focus:border-cyan-500 dark:border-cyan-600 focus:ring-cyan-500/30',
                  ]"
                />
                <p v-if="touched.otp && errs.otp" class="text-xs font-medium text-rose-600">
                  {{ errs.otp }}
                </p>
              </div>

              <div class="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <button
                  type="button"
                  class="inline-flex w-full items-center justify-center gap-2 rounded-2xl border border-transparent bg-gradient-to-r from-cyan-500 to-cyan-600 px-4 py-3 text-sm font-bold uppercase tracking-wide text-white shadow-lg shadow-cyan-500/40 transition hover:from-cyan-600 hover:to-cyan-700 hover:shadow-xl hover:-translate-y-0.5 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-cyan-600 disabled:cursor-not-allowed disabled:opacity-60 disabled:hover:translate-y-0"
                  :disabled="saving"
                  @click="submitOtp"
                >
                  <span
                    v-if="saving"
                    class="h-4 w-4 animate-spin rounded-full border-2 border-white/60 border-t-white"
                  ></span>
                  XÁC NHẬN
                </button>
                <button
                  type="button"
                  class="inline-flex w-full items-center justify-center rounded-2xl border border-slate-200 px-4 py-3 text-xs font-bold uppercase tracking-wide text-slate-600 transition hover:bg-slate-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-slate-300 disabled:cursor-not-allowed disabled:border-slate-100 disabled:text-slate-400 sm:w-auto"
                  :disabled="otp.countdown > 0 || otp.sending"
                  @click="sendOtp()"
                >
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
import { showToast } from '@/utils/toast'

const router = useRouter()
const auth = useAuthStore()
const goProfile = () => router.push({ name: 'student-profile' })
const goParent = () => router.push({ name: 'student-parent' })

const pwd = reactive({ current: '', new1: '', new2: '' })
const show = reactive({ current: false, new1: false, new2: false })
const touched = reactive({ current: false, new1: false, new2: false, otp: false })
const errs = reactive<{ current: string; new1: string; new2: string; otp: string }>({
  current: '',
  new1: '',
  new2: '',
  otp: '',
})

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

watch(
  () => otp.code,
  () => {
    if (!otp.requested) {
      errs.otp = ''
      return
    }
    if (!otp.code) errs.otp = 'Vui lòng nhập OTP.'
    else if (otp.code.length !== 6) errs.otp = 'OTP gồm 6 chữ số.'
    else errs.otp = ''
  },
  { immediate: true },
)

watch(
  () => pwd.current,
  () => {
    errs.current = pwd.current ? '' : 'Vui lòng nhập mật khẩu hiện tại.'
  },
  { immediate: true },
)

watch(
  () => pwd.new1,
  () => {
    errs.new1 = pwd.new1.length >= 6 ? '' : 'Mật khẩu mới tối thiểu 6 ký tự.'
    errs.new2 = pwd.new2 === pwd.new1 ? '' : 'Xác nhận mật khẩu chưa khớp.'
  },
  { immediate: true },
)

watch(
  () => pwd.new2,
  () => {
    errs.new2 = pwd.new2 === pwd.new1 ? '' : 'Xác nhận mật khẩu chưa khớp.'
  },
  { immediate: true },
)

const credentialsValid = computed(
  () =>
    !!pwd.current &&
    pwd.new1.length >= 6 &&
    pwd.new2 === pwd.new1 &&
    !errs.current &&
    !errs.new1 &&
    !errs.new2,
)

const otpValid = computed(() => otp.requested && otp.code.length === 6 && !errs.otp)

const isSubmitDisabled = computed(() => {
  if (saving.value) return true
  if (!otp.requested) return !credentialsValid.value || otp.sending
  return false
})

const saving = ref(false)

async function changePassword() {
  touched.current = touched.new1 = touched.new2 = true
  if (!credentialsValid.value) return

  if (!otp.requested) {
    const requested = await sendOtp()
    if (requested) otpModalVisible.value = true
    return
  }

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
  } finally {
    saving.value = false
  }
}

function resetForm() {
  pwd.current = ''
  pwd.new1 = ''
  pwd.new2 = ''
  otp.code = ''
  otp.sentTo = ''
  otp.requested = false
  otp.countdown = 0
  touched.current = touched.new1 = touched.new2 = touched.otp = false
  errs.otp = ''
  clearCountdown()
  closeOtpModal()
}

function clearCountdown() {
  if (countdownTimer) {
    window.clearInterval(countdownTimer)
    countdownTimer = undefined
  }
}

async function sendOtp(showSuccess = true) {
  if (otp.sending || otp.countdown > 0) return false
  if (!pwd.current) {
    touched.current = true
    errs.current = 'Vui lòng nhập mật khẩu hiện tại.'
    return false
  }
  otp.sending = true
  try {
    const res = await auth.requestPasswordOtp(pwd.current)
    otp.sentTo = res?.email || maskedEmail.value || ''
    otp.requested = true
    otp.code = ''
    touched.otp = false
    errs.otp = ''
    if (showSuccess) showToast('Đã gửi OTP đến email của bạn.', 'success')
    otp.countdown = OTP_COUNTDOWN
    clearCountdown()
    countdownTimer = window.setInterval(() => {
      if (otp.countdown > 0) otp.countdown -= 1
      else clearCountdown()
    }, 1000)
    return true
  } catch (e) {
    const message = e instanceof Error ? e.message : 'Không gửi được OTP. Thử lại sau.'
    if (
      message.toLowerCase().includes('mật khẩu') &&
      message.toLowerCase().includes('không chính xác')
    ) {
      errs.current = message
      touched.current = true
    }
    showToast(message, 'error')
    return false
  } finally {
    otp.sending = false
  }
}

function closeOtpModal() {
  otpModalVisible.value = false
}

onUnmounted(() => clearCountdown())
</script>
