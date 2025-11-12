<template>
  <div class="space-y-6">
    <div class="text-center">
      <div
        class="mx-auto w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mb-4 animate-bounce-slow"
      >
        <svg class="w-8 h-8 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
          />
        </svg>
      </div>
      <h3 class="text-xl font-bold text-gray-900 mb-2">Quên mật khẩu?</h3>
      <p class="text-sm text-gray-600">Nhập email của bạn để nhận link đặt lại mật khẩu</p>
    </div>

    <form v-if="status !== 'success'" @submit.prevent="submit" class="space-y-5" autocomplete="off">
      <!-- Email -->
      <div class="form-group">
        <label for="email" class="form-label">
          Email
          <span class="text-red-500">*</span>
        </label>
        <div class="relative">
          <div class="input-icon">
            <svg
              class="w-5 h-5 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
              />
            </svg>
          </div>
          <input
            id="email"
            v-model.trim="email"
            type="email"
            name="email-forgot"
            placeholder="you@example.com"
            autocomplete="off"
            class="form-input"
            :class="{ 'border-red-300': touched && !validEmail }"
            :disabled="loading"
            @blur="touched = true"
            @input="touched = false"
            required
          />
        </div>
        <div class="min-h-[20px]">
          <p v-if="touched && !validEmail" class="form-error">
            <svg class="w-3.5 h-3.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
                clip-rule="evenodd"
              />
            </svg>
            <span>Vui lòng nhập email hợp lệ</span>
          </p>
        </div>
      </div>

      <button
        type="submit"
        class="btn-primary"
        :disabled="!validEmail || loading"
        :class="{ 'opacity-60 cursor-not-allowed': !validEmail || loading }"
      >
        <svg
          v-if="loading"
          class="animate-spin -ml-1 mr-2 h-5 w-5 text-white"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            class="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            stroke-width="4"
          ></circle>
          <path
            class="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          ></path>
        </svg>
        <span v-if="!loading">Gửi link đặt lại</span>
        <span v-else>Đang gửi...</span>
      </button>
    </form>

    <!-- Success state actions -->
    <div v-else class="space-y-3">
      <button
        @click="() => {
          status = 'idle';
          email = '';
          touched = false;
        }"
        class="w-full rounded-xl border border-gray-200 px-4 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50 transition"
      >
        Gửi lại email
      </button>
      <RouterLink
        to="/auth/login"
        class="block w-full rounded-xl border border-indigo-200 bg-indigo-50 px-4 py-2.5 text-center text-sm font-medium text-indigo-700 hover:bg-indigo-100 transition"
      >
        Quay lại đăng nhập
      </RouterLink>
    </div>

    <!-- Footer links -->
    <div v-if="status !== 'success'" class="text-center text-sm space-y-2">
      <RouterLink
        to="/auth/login"
        class="inline-flex items-center gap-1.5 text-gray-600 hover:text-gray-900 transition group"
      >
        <svg
          class="w-4 h-4 transition-transform group-hover:-translate-x-0.5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M15 19l-7-7 7-7"
          />
        </svg>
        <span class="font-medium">Quay lại đăng nhập</span>
      </RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuthStore } from '@/store/auth.store'
import { showToast } from '@/utils/toast'

const auth = useAuthStore()

const email = ref('')
const touched = ref(false)
const loading = ref(false)
const status = ref<'idle' | 'success' | 'error'>('idle')

const validEmail = computed(() => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value))

async function submit() {
  touched.value = true
  if (!validEmail.value || loading.value) return

  loading.value = true
  status.value = 'idle'

  try {
    await auth.forgotPassword(email.value)
    status.value = 'success'
    showToast('Đã gửi link đặt lại mật khẩu đến email của bạn!', 'success')
  } catch (e: any) {
    status.value = 'error'
    showToast(e?.message || 'Gửi email thất bại. Vui lòng thử lại.', 'error')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.form-group {
  @apply space-y-2;
}

.form-label {
  @apply block text-sm font-medium text-gray-700;
}

.form-input {
  @apply w-full pl-11 pr-4 py-3 bg-white border border-gray-200 rounded-xl text-gray-900 placeholder-gray-400;
  @apply focus:outline-none focus:ring-2 focus:ring-indigo-500/30 focus:border-indigo-500;
  @apply transition duration-200;
  @apply disabled:bg-gray-50 disabled:cursor-not-allowed;
}

.form-input:hover:not(:disabled) {
  @apply border-gray-300;
}

.input-icon {
  @apply absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none z-10;
}

.form-error {
  @apply text-xs text-red-600 mt-1.5 flex items-start gap-1.5;
}

/* Primary Button — Purple gradient */
.btn-primary {
  width: 100% !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 0.75rem 1.5rem !important;
  border-radius: 0.75rem !important;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  color: white !important;
  font-weight: 600 !important;
  transition: all 0.2s !important;
  transform-origin: center !important;
  box-shadow: 0 10px 15px -3px rgba(102, 126, 234, 0.25) !important;
}

.btn-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #5568d3 0%, #663d8f 100%) !important;
}

.btn-primary:focus {
  outline: none !important;
  box-shadow:
    0 0 0 2px rgba(102, 126, 234, 0.5),
    0 10px 15px -3px rgba(102, 126, 234, 0.25) !important;
}

.btn-primary:active:not(:disabled) {
  transform: scale(0.98) !important;
}

.btn-primary:disabled {
  opacity: 0.6 !important;
  cursor: not-allowed !important;
}

/* Animations */
@keyframes bounce-slow {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}
.animate-bounce-slow {
  animation: bounce-slow 3s ease-in-out infinite;
}
</style>
