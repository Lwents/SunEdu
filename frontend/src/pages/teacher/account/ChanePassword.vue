<template>
  <div class="p-6">
    <section class="mx-auto w-full max-w-3xl rounded-2xl border bg-white p-6 shadow-sm">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-lg font-semibold text-gray-800">Đổi mật khẩu</h2>
          <p class="text-sm text-gray-500">Nhận OTP qua email và thiết lập mật khẩu mới.</p>
        </div>
      </div>

      <!-- Form -->
      <form class="mt-6 space-y-5" @submit.prevent="onSubmit">
        <!-- OTP row -->
        <div>
          <label class="text-sm text-gray-600">Mã OTP xác nhận</label>
          <div class="mt-1 flex gap-3">
            <input
              v-model.trim="otp.code"
              maxlength="6"
              inputmode="numeric"
              class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-blue-500"
              placeholder="Nhập 6 số"
            />
            <button
              type="button"
              class="rounded-lg border px-4 py-2 text-sm font-semibold"
              :disabled="otp.countdown > 0 || otp.sending"
              @click="sendOtp"
            >
              <span v-if="otp.sending">Đang gửi…</span>
              <span v-else-if="otp.countdown > 0">Gửi lại ({{ otp.countdown }}s)</span>
              <span v-else>Gửi OTP</span>
            </button>
          </div>
          <p v-if="errors.otp" class="mt-1 text-xs text-red-600">{{ errors.otp }}</p>
          <p class="mt-1 text-xs text-gray-500">OTP sẽ gửi tới {{ otp.sentTo || maskedEmail }}</p>
        </div>

        <!-- New password -->
        <div class="grid gap-4 sm:grid-cols-2">
          <div>
            <label class="text-sm text-gray-600">Mật khẩu mới</label>
            <div class="relative mt-1">
              <input
                :type="show.new ? 'text' : 'password'"
                v-model.trim="form.newPassword"
                class="w-full rounded-lg border px-3 py-2 pr-12 focus:ring-2 focus:ring-blue-500"
                autocomplete="new-password"
                placeholder="Ít nhất 8 ký tự"
              />
              <button
                type="button"
                class="absolute inset-y-0 right-2 my-auto text-sm text-gray-500"
                @click="show.new = !show.new"
              >
                {{ show.new ? 'Ẩn' : 'Hiện' }}
              </button>
            </div>
            <p v-if="errors.newPassword" class="mt-1 text-xs text-red-600">
              {{ errors.newPassword }}
            </p>
          </div>

          <div>
            <label class="text-sm text-gray-600">Xác nhận mật khẩu mới</label>
            <div class="relative mt-1">
              <input
                :type="show.confirm ? 'text' : 'password'"
                v-model.trim="form.confirmPassword"
                class="w-full rounded-lg border px-3 py-2 pr-12 focus:ring-2 focus:ring-blue-500"
                autocomplete="new-password"
                placeholder="Nhập lại mật khẩu mới"
              />
              <button
                type="button"
                class="absolute inset-y-0 right-2 my-auto text-sm text-gray-500"
                @click="show.confirm = !show.confirm"
              >
                {{ show.confirm ? 'Ẩn' : 'Hiện' }}
              </button>
            </div>
            <p v-if="errors.confirmPassword" class="mt-1 text-xs text-red-600">
              {{ errors.confirmPassword }}
            </p>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex items-center gap-3 pt-1">
          <button
            type="submit"
            class="rounded-xl bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-60"
            :disabled="loading"
          >
            <span v-if="loading">Đang đổi…</span>
            <span v-else>Đổi mật khẩu</span>
          </button>

          <RouterLink to="/teacher/account/profile" class="text-sm text-blue-600 hover:underline">
            Quay lại hồ sơ
          </RouterLink>

          <span v-if="done" class="text-sm text-green-600">Đổi mật khẩu thành công!</span>
        </div>
      </form>
    </section>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed, onUnmounted } from 'vue'
import { useAuthStore } from '@/store/auth.store'

const auth = useAuthStore()

const form = reactive({
  newPassword: '',
  confirmPassword: '',
})
const errors = reactive<{ [k: string]: string }>({ otp: '', newPassword: '', confirmPassword: '' })
const loading = ref(false)
const done = ref(false)
const show = reactive({ new: false, confirm: false })
const otp = reactive({ code: '', countdown: 0, sending: false, sentTo: '' })
const OTP_COUNTDOWN = 60
let timer: number | undefined

const maskedEmail = computed(() => {
  const email = auth.user?.email || ''
  if (!email || !email.includes('@')) return ''
  const [local, domain] = email.split('@')
  if (local.length <= 2) return `${local[0]}***@${domain}`
  return `${local[0]}***${local[local.length - 1]}@${domain}`
})

const validate = () => {
  errors.newPassword = ''
  errors.confirmPassword = ''
  errors.otp = ''
  let ok = true

  if (otp.code.length !== 6) {
    errors.otp = 'OTP gồm 6 chữ số.'
    ok = false
  }
  if (form.newPassword.length < 8) {
    errors.newPassword = 'Mật khẩu mới phải có ít nhất 8 ký tự.'
    ok = false
  }
  if (form.confirmPassword !== form.newPassword) {
    errors.confirmPassword = 'Xác nhận mật khẩu mới không khớp.'
    ok = false
  }
  return ok
}
const onSubmit = async () => {
  done.value = false
  if (!validate()) return
  loading.value = true
  try {
    await auth.changePasswordWithOtp(otp.code, form.newPassword)

    done.value = true
    form.newPassword = ''
    form.confirmPassword = ''
    otp.code = ''
    setTimeout(() => (done.value = false), 1800)
  } finally {
    loading.value = false
  }
}

const sendOtp = async () => {
  if (otp.sending || otp.countdown > 0) return
  otp.sending = true
  try {
    const res = await auth.requestPasswordOtp()
    otp.sentTo = res?.email || maskedEmail.value || ''
    otp.countdown = OTP_COUNTDOWN
    clearTimer()
    timer = window.setInterval(() => {
      if (otp.countdown > 0) otp.countdown -= 1
      else clearTimer()
    }, 1000)
  } catch (error: any) {
    errors.otp = error?.message || 'Không thể gửi OTP. Vui lòng thử lại.'
  } finally {
    otp.sending = false
  }
}

function clearTimer() {
  if (timer) {
    window.clearInterval(timer)
    timer = undefined
  }
}

onUnmounted(() => clearTimer())
</script>
