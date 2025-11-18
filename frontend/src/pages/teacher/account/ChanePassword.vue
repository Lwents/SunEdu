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
        <!-- Current password -->
        <div>
          <label class="text-sm text-gray-600">Mật khẩu hiện tại</label>
          <div class="relative mt-1">
            <input
              :type="show.current ? 'text' : 'password'"
              v-model.trim="form.currentPassword"
              class="w-full rounded-lg border px-3 py-2 pr-12 focus:ring-2 focus:ring-blue-500"
              autocomplete="current-password"
              placeholder="Nhập mật khẩu đang dùng"
            />
            <button
              type="button"
              class="absolute inset-y-0 right-2 my-auto text-sm text-gray-500"
              @click="show.current = !show.current"
            >
              {{ show.current ? 'Ẩn' : 'Hiện' }}
            </button>
          </div>
          <p v-if="errors.currentPassword" class="mt-1 text-xs text-red-600">{{ errors.currentPassword }}</p>
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

  <!-- OTP Modal -->
  <Transition name="fade">
    <div
      v-if="otp.open"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4"
      @click.self="closeOtpModal"
    >
      <div class="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl">
        <div class="mb-4">
          <h3 class="text-lg font-semibold text-gray-900">Nhập mã OTP</h3>
          <p class="text-sm text-gray-600">OTP đã gửi tới {{ otp.sentTo || maskedEmail }}</p>
        </div>

        <div class="space-y-3">
          <input
            v-model.trim="otp.code"
            maxlength="6"
            inputmode="numeric"
            class="w-full rounded-xl border px-4 py-3 text-center text-xl tracking-[0.4em] focus:ring-2 focus:ring-blue-500"
            placeholder="••••••"
          />
          <p v-if="otp.error" class="text-sm text-red-600">{{ otp.error }}</p>
          <button
            type="button"
            class="text-sm text-blue-600 hover:underline"
            :disabled="otp.sending"
            @click="resendOtp"
          >
            {{ otp.sending ? 'Đang gửi lại...' : 'Chưa nhận được mã? Gửi lại OTP' }}
          </button>
        </div>

        <div class="mt-6 flex justify-end gap-3">
          <button
            type="button"
            class="rounded-lg border px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
            @click="closeOtpModal"
          >
            Hủy
          </button>
          <button
            type="button"
            class="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700 disabled:opacity-60"
            :disabled="otp.verifying || otp.code.length !== 6"
            @click="verifyOtp"
          >
            <span v-if="otp.verifying">Đang xác nhận…</span>
            <span v-else>Xác nhận</span>
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { reactive, ref, computed } from 'vue'
import { useAuthStore } from '@/store/auth.store'

const auth = useAuthStore()

const form = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
})
const errors = reactive<{ [k: string]: string }>({
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
})
const loading = ref(false)
const done = ref(false)
const show = reactive({ current: false, new: false, confirm: false })
const otp = reactive({
  open: false,
  code: '',
  sentTo: '',
  sending: false,
  verifying: false,
  error: '',
})

const maskedEmail = computed(() => {
  const email = auth.user?.email || ''
  if (!email || !email.includes('@')) return ''
  const [local, domain] = email.split('@')
  if (local.length <= 2) return `${local[0]}***@${domain}`
  return `${local[0]}***${local[local.length - 1]}@${domain}`
})

const validateForm = () => {
  errors.currentPassword = ''
  errors.newPassword = ''
  errors.confirmPassword = ''
  let ok = true

  if (!form.currentPassword) {
    errors.currentPassword = 'Vui lòng nhập mật khẩu hiện tại.'
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
  otp.error = ''
  otp.code = ''
  if (!validateForm()) return
  loading.value = true
  try {
    const ok = await requestOtp()
    if (ok) {
      otp.open = true
    }
  } finally {
    loading.value = false
  }
}

const requestOtp = async () => {
  otp.error = ''
  otp.sending = true
  try {
    const res = await auth.requestPasswordOtp(form.currentPassword)
    otp.sentTo = res?.email || maskedEmail.value || ''
    errors.currentPassword = ''
    return true
  } catch (error: any) {
    const message = error?.message || 'Không thể gửi OTP. Vui lòng thử lại.'
    otp.error = message
    if (message.toLowerCase().includes('mật khẩu') && message.toLowerCase().includes('không chính xác')) {
      errors.currentPassword = message
    }
    return false
  } finally {
    otp.sending = false
  }
}

const verifyOtp = async () => {
  otp.error = ''
  if (otp.code.length !== 6) {
    otp.error = 'OTP gồm 6 chữ số.'
    return
  }
  otp.verifying = true
  try {
    await auth.changePasswordWithOtp(otp.code, form.newPassword)
    done.value = true
    otp.open = false
    form.currentPassword = ''
    form.newPassword = ''
    form.confirmPassword = ''
    otp.code = ''
    setTimeout(() => (done.value = false), 2000)
  } catch (error: any) {
    otp.error = error?.message || 'OTP không hợp lệ hoặc đã hết hạn.'
  } finally {
    otp.verifying = false
  }
}

const closeOtpModal = () => {
  otp.open = false
  otp.code = ''
  otp.error = ''
}

const resendOtp = async () => {
  if (otp.sending) return
  await requestOtp()
}
</script>
