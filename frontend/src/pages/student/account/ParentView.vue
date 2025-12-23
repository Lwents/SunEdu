<template>
  <div :class="isDark ? 'dark-mode' : 'light-mode'">
    <!-- Background glow effects for dark mode -->
    <div v-if="isDark" class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 -left-32 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl"></div>
      <div class="absolute bottom-1/4 -right-32 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl"></div>
    </div>

    <div class="min-h-screen relative z-10">
      <div class="mx-auto max-w-4xl px-4 py-6 sm:px-6 lg:px-8">
        <!-- Tabs -->
        <div class="mb-6 flex items-center gap-2 border-b" :class="isDark ? 'border-slate-700' : 'border-slate-200'">
          <button
            type="button"
            class="px-4 py-3 text-sm font-medium transition"
            :class="isDark ? 'text-slate-400 hover:text-white' : 'text-slate-600 hover:text-slate-900'"
            @click="goProfile"
          >
            Cá nhân
          </button>
          <button
            type="button"
            class="px-4 py-3 text-sm font-medium transition"
            :class="isDark ? 'text-slate-400 hover:text-white' : 'text-slate-600 hover:text-slate-900'"
            @click="goChangePwd"
          >
            Đổi mật khẩu
          </button>
          <button
            type="button"
            class="border-b-2 px-4 py-3 text-sm font-semibold"
            :class="isDark ? 'border-cyan-400 text-cyan-400' : 'border-slate-900 text-slate-900'"
          >
            Phụ huynh
          </button>
        </div>

        <!-- Main Card -->
        <div 
          class="rounded-lg border shadow-sm"
          :class="isDark 
            ? 'border-slate-700/50 bg-slate-800/50 backdrop-blur-sm' 
            : 'border-slate-200 bg-white'"
        >
          <div class="border-b px-6 py-4" :class="isDark ? 'border-slate-700' : 'border-slate-200'">
            <h2 class="text-lg font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Thông tin phụ huynh</h2>
          </div>

          <form v-if="!loading" class="p-6 space-y-6" @submit.prevent="save">
            <!-- Full Name -->
            <div class="grid gap-3 lg:grid-cols-[180px_1fr]">
              <label class="text-sm font-medium lg:pt-2" :class="isDark ? 'text-slate-300' : 'text-slate-700'">
                Họ tên phụ huynh <span class="text-red-500">*</span>
              </label>
              <div class="space-y-1">
                <input
                  v-model.trim="f.fullname"
                  placeholder="Nhập họ tên phụ huynh"
                  @blur="touched.fullname = true"
                  :class="[
                    'w-full rounded-lg border px-3 py-2 text-sm transition focus:outline-none focus:ring-2',
                    touched.fullname && errs.fullname
                      ? 'border-red-300 focus:border-red-400 focus:ring-red-200'
                      : isDark 
                        ? 'border-slate-600 bg-slate-700/50 text-white placeholder-slate-400 focus:border-cyan-500 focus:ring-cyan-500/20'
                        : 'border-slate-300 text-slate-900 focus:border-slate-400 focus:ring-slate-200',
                  ]"
                />
                <p v-if="touched.fullname && errs.fullname" class="text-xs text-red-500">{{ errs.fullname }}</p>
              </div>
            </div>

            <!-- Phone -->
            <div class="grid gap-3 lg:grid-cols-[180px_1fr]">
              <label class="text-sm font-medium lg:pt-2" :class="isDark ? 'text-slate-300' : 'text-slate-700'">
                Số điện thoại <span class="text-red-500">*</span>
              </label>
              <div class="space-y-1">
                <input
                  v-model.trim="f.phone"
                  type="tel"
                  inputmode="tel"
                  placeholder="Nhập số điện thoại"
                  @blur="touched.phone = true"
                  :class="[
                    'w-full rounded-lg border px-3 py-2 text-sm transition focus:outline-none focus:ring-2',
                    touched.phone && errs.phone
                      ? 'border-red-300 focus:border-red-400 focus:ring-red-200'
                      : isDark 
                        ? 'border-slate-600 bg-slate-700/50 text-white placeholder-slate-400 focus:border-cyan-500 focus:ring-cyan-500/20'
                        : 'border-slate-300 text-slate-900 focus:border-slate-400 focus:ring-slate-200',
                  ]"
                />
                <p v-if="touched.phone && errs.phone" class="text-xs text-red-500">{{ errs.phone }}</p>
              </div>
            </div>

            <!-- Email -->
            <div class="grid gap-3 lg:grid-cols-[180px_1fr]">
              <label class="text-sm font-medium lg:pt-2" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Email</label>
              <div class="space-y-1">
                <input
                  v-model.trim="f.email"
                  type="email"
                  placeholder="parent@example.com"
                  @blur="touched.email = true"
                  :class="[
                    'w-full rounded-lg border px-3 py-2 text-sm transition focus:outline-none focus:ring-2',
                    touched.email && errs.email
                      ? 'border-red-300 focus:border-red-400 focus:ring-red-200'
                      : isDark 
                        ? 'border-slate-600 bg-slate-700/50 text-white placeholder-slate-400 focus:border-cyan-500 focus:ring-cyan-500/20'
                        : 'border-slate-300 text-slate-900 focus:border-slate-400 focus:ring-slate-200',
                  ]"
                />
                <p v-if="touched.email && errs.email" class="text-xs text-red-500">{{ errs.email }}</p>
              </div>
            </div>

            <!-- Relation -->
            <div class="grid gap-3 lg:grid-cols-[180px_1fr]">
              <label class="text-sm font-medium lg:pt-2" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Mối quan hệ</label>
              <div>
                <select
                  v-model="f.relation"
                  class="w-full rounded-lg border px-3 py-2 text-sm transition focus:outline-none focus:ring-2"
                  :class="isDark 
                    ? 'border-slate-600 bg-slate-700/50 text-white focus:border-cyan-500 focus:ring-cyan-500/20'
                    : 'border-slate-300 text-slate-900 focus:border-slate-400 focus:ring-slate-200'"
                >
                  <option value="">Chọn</option>
                  <option>Bố</option>
                  <option>Mẹ</option>
                  <option>Người giám hộ</option>
                </select>
              </div>
            </div>

            <!-- Address -->
            <div class="grid gap-3 lg:grid-cols-[180px_1fr]">
              <label class="text-sm font-medium lg:pt-2" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Địa chỉ</label>
              <div>
                <textarea
                  v-model.trim="f.address"
                  rows="3"
                  placeholder="Nhập địa chỉ"
                  class="w-full rounded-lg border px-3 py-2 text-sm transition focus:outline-none focus:ring-2"
                  :class="isDark 
                    ? 'border-slate-600 bg-slate-700/50 text-white placeholder-slate-400 focus:border-cyan-500 focus:ring-cyan-500/20'
                    : 'border-slate-300 text-slate-900 focus:border-slate-400 focus:ring-slate-200'"
                ></textarea>
              </div>
            </div>

            <!-- Submit Button -->
            <div class="flex flex-col gap-3 pt-4 border-t sm:flex-row sm:items-center sm:justify-end" :class="isDark ? 'border-slate-700' : 'border-slate-200'">
              <button
                type="submit"
                class="inline-flex items-center justify-center gap-2 rounded-lg border px-6 py-2.5 text-sm font-medium transition focus:outline-none focus:ring-2 disabled:cursor-not-allowed disabled:opacity-50"
                :class="isDark 
                  ? 'border-transparent bg-gradient-to-r from-cyan-500 to-purple-500 text-white hover:from-cyan-600 hover:to-purple-600 focus:ring-cyan-500/20'
                  : 'border-slate-300 bg-slate-900 text-white hover:bg-slate-800 focus:ring-slate-200'"
                :disabled="saving || !isValid"
              >
                <span v-if="saving" class="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white"></span>
                {{ saving ? 'Đang lưu...' : 'Lưu thông tin' }}
              </button>
            </div>
          </form>

          <div v-else class="p-6 text-sm" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Đang tải thông tin…</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth.store'
import { useThemeStore } from '@/store/theme.store'
import { authService, type ProfileUpdatePayload, type ProfileDetails } from '@/services/auth.service'
import { showToast } from '@/utils/toast'

const router = useRouter()
const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)

const goProfile = () => router.push({ name: 'student-profile' })
const goChangePwd = () => router.push({ name: 'student-change-password' })
const auth = useAuthStore()

type ParentForm = {
  fullname: string
  phone: string
  email: string
  relation: string
  address: string
}
const f = reactive<ParentForm>({ fullname: '', phone: '', email: '', relation: '', address: '' })
const touched = reactive({ fullname: false, phone: false, email: false })
const errs = reactive<{ fullname?: string; phone?: string; email?: string }>({})

const isEmail = (v: string) => /^\S+@\S+\.\S+$/.test(v)

watch(
  () => ({ ...f }),
  () => {
    errs.fullname = f.fullname ? '' : 'Vui lòng nhập họ tên phụ huynh.'
    errs.phone = f.phone ? '' : 'Vui lòng nhập số điện thoại.'
    errs.email = f.email && !isEmail(f.email) ? 'Email không hợp lệ.' : ''
  },
  { deep: true, immediate: true },
)

const isValid = computed(() => {
  const phoneOk = !!f.phone
  const nameOk = !!f.fullname
  const emailOk = !f.email || isEmail(f.email)
  return phoneOk && nameOk && emailOk
})

const saving = ref(false)
const loading = ref(false)
let profileDetails: ProfileDetails | null = null

async function save() {
  touched.fullname = touched.phone = true
  if (f.email) touched.email = true
  if (!isValid.value) return

  saving.value = true
  try {
    const payload: ProfileUpdatePayload = {
      parent_name: f.fullname,
      parent_phone: f.phone,
      parent_email: f.email || undefined,
      parent_relation: f.relation || undefined,
      parent_address: f.address || undefined,
    }
    profileDetails = await auth.updateProfile(payload)
    showToast('Đã lưu thông tin phụ huynh!', 'success')
  } catch (e) {
    showToast('Lưu thất bại, thử lại sau.', 'error')
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  auth.init?.()
  loading.value = true
  try {
    profileDetails = await authService.getProfile()
    f.fullname = profileDetails.parent_name || ''
    f.phone = profileDetails.parent_phone || ''
    f.email = profileDetails.parent_email || ''
    f.relation = profileDetails.parent_relation || ''
    f.address = profileDetails.parent_address || ''
  } catch (error) {
    console.error('Không thể tải thông tin phụ huynh:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.dark-mode {
  @apply bg-slate-950;
}
.light-mode {
  @apply bg-slate-50;
}

/* Fix dark mode for select options */
.dark-mode select option {
  background: #1e293b;
  color: white;
}
</style>
