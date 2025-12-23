<template>
  <div class="space-y-6">
    <div class="text-center">
      <div
        class="mx-auto w-16 h-16 bg-gradient-to-br from-cyan-500/20 to-purple-500/20 rounded-full flex items-center justify-center mb-4 animate-bounce-slow border border-cyan-500/30"
      >
        <svg class="w-8 h-8 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
          />
        </svg>
      </div>
      <h3 class="text-xl font-bold text-white mb-2">Quên mật khẩu?</h3>
      <p class="text-sm text-gray-400">Nhập email của bạn để nhận link đặt lại mật khẩu</p>
    </div>

    <form v-if="status !== 'success'" @submit.prevent="submit" class="space-y-5" autocomplete="off">
      <!-- Email -->
      <div class="form-group">
        <label for="email" class="form-label">
          Email
          <span class="text-red-400">*</span>
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
        class="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-sm font-medium text-gray-300 hover:bg-white/10 transition"
      >
        Gửi lại email
      </button>
      <RouterLink
        to="/auth/login"
        class="block w-full rounded-xl border border-cyan-500/30 bg-cyan-500/10 px-4 py-2.5 text-center text-sm font-medium text-cyan-400 hover:bg-cyan-500/20 transition"
      >
        Quay lại đăng nhập
      </RouterLink>
    </div>

    <!-- Footer links -->
    <div v-if="status !== 'success'" class="text-center text-sm space-y-2">
      <RouterLink
        to="/auth/login"
        class="inline-flex items-center gap-1.5 text-gray-400 hover:text-white transition group"
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
  @apply block text-sm font-medium text-gray-300;
}

.form-input {
  @apply w-full pl-11 pr-4 py-3 rounded-xl text-white placeholder-gray-500;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  @apply focus:outline-none focus:ring-2 focus:ring-cyan-500/30 focus:border-cyan-500/50;
  @apply transition duration-200;
  @apply disabled:opacity-50 disabled:cursor-not-allowed;
}

.form-input:hover:not(:disabled) {
  border-color: rgba(255, 255, 255, 0.2);
}

.input-icon {
  @apply absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none z-10;
}

.input-icon svg {
  @apply text-gray-500;
}

.form-error {
  @apply text-xs text-red-400 mt-1.5 flex items-start gap-1.5;
}

/* Primary Button — Cyan to Purple gradient */
.btn-primary {
  width: 100% !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 0.875rem 1.5rem !important;
  border-radius: 0.875rem !important;
  background: linear-gradient(135deg, #06b6d4 0%, #8b5cf6 100%) !important;
  color: white !important;
  font-weight: 700 !important;
  transition: all 0.3s !important;
  box-shadow: 0 10px 30px -5px rgba(6, 182, 212, 0.4) !important;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px) !important;
  box-shadow: 0 15px 40px -5px rgba(6, 182, 212, 0.5) !important;
}

.btn-primary:focus {
  outline: none !important;
  box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.3), 0 10px 30px -5px rgba(6, 182, 212, 0.4) !important;
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
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
.animate-bounce-slow {
  animation: bounce-slow 3s ease-in-out infinite;
}
</style>
