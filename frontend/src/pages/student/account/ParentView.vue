<!-- src/pages/student/account/ParentInfo.vue -->
<template>
  <div class="min-h-screen bg-slate-50">
    <div class="mx-auto max-w-4xl px-4 py-6 sm:px-6 lg:px-8">
      <!-- Tabs -->
      <div class="mb-6 flex items-center gap-2 border-b border-slate-200">
        <button
          type="button"
          class="px-4 py-3 text-sm font-medium text-slate-600 transition hover:text-slate-900"
          @click="goProfile"
        >
          Cá nhân
        </button>
        <button
          type="button"
          class="px-4 py-3 text-sm font-medium text-slate-600 transition hover:text-slate-900"
          @click="goChangePwd"
        >
          Đổi mật khẩu
        </button>
        <button
          type="button"
          class="border-b-2 border-slate-900 px-4 py-3 text-sm font-semibold text-slate-900"
        >
          Phụ huynh
        </button>
      </div>

      <!-- Main Card -->
      <div class="rounded-lg border border-slate-200 bg-white shadow-sm">
        <div class="border-b border-slate-200 px-6 py-4">
          <h2 class="text-lg font-semibold text-slate-900">Thông tin phụ huynh</h2>
        </div>

        <form v-if="!loading" class="p-6 space-y-6" @submit.prevent="save">
          <!-- Full Name -->
          <div class="grid gap-3 lg:grid-cols-[180px_1fr]">
            <label class="text-sm font-medium text-slate-700 lg:pt-2">
              Họ tên phụ huynh <span class="text-red-500">*</span>
            </label>
            <div class="space-y-1">
              <input
                v-model.trim="f.fullname"
                placeholder="Nhập họ tên phụ huynh"
                @blur="touched.fullname = true"
                :class="[
                  'w-full rounded-lg border px-3 py-2 text-sm text-slate-900 transition focus:outline-none focus:ring-2',
                  touched.fullname && errs.fullname
                    ? 'border-red-300 focus:border-red-400 focus:ring-red-200'
                    : 'border-slate-300 focus:border-slate-400 focus:ring-slate-200',
                ]"
              />
              <p v-if="touched.fullname && errs.fullname" class="text-xs text-red-600">
                {{ errs.fullname }}
              </p>
            </div>
          </div>

          <!-- Phone -->
          <div class="grid gap-3 lg:grid-cols-[180px_1fr]">
            <label class="text-sm font-medium text-slate-700 lg:pt-2">
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
                  'w-full rounded-lg border px-3 py-2 text-sm text-slate-900 transition focus:outline-none focus:ring-2',
                  touched.phone && errs.phone
                    ? 'border-red-300 focus:border-red-400 focus:ring-red-200'
                    : 'border-slate-300 focus:border-slate-400 focus:ring-slate-200',
                ]"
              />
              <p v-if="touched.phone && errs.phone" class="text-xs text-red-600">
                {{ errs.phone }}
              </p>
            </div>
          </div>

          <!-- Email -->
          <div class="grid gap-3 lg:grid-cols-[180px_1fr]">
            <label class="text-sm font-medium text-slate-700 lg:pt-2">Email</label>
            <div class="space-y-1">
              <input
                v-model.trim="f.email"
                type="email"
                placeholder="parent@example.com"
                @blur="touched.email = true"
                :class="[
                  'w-full rounded-lg border px-3 py-2 text-sm text-slate-900 transition focus:outline-none focus:ring-2',
                  touched.email && errs.email
                    ? 'border-red-300 focus:border-red-400 focus:ring-red-200'
                    : 'border-slate-300 focus:border-slate-400 focus:ring-slate-200',
                ]"
              />
              <p v-if="touched.email && errs.email" class="text-xs text-red-600">
                {{ errs.email }}
              </p>
            </div>
          </div>

          <!-- Relation -->
          <div class="grid gap-3 lg:grid-cols-[180px_1fr]">
            <label class="text-sm font-medium text-slate-700 lg:pt-2">Mối quan hệ</label>
            <div>
              <select
                v-model="f.relation"
                class="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-900 transition focus:outline-none focus:ring-2 focus:ring-slate-200 focus:border-slate-400"
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
            <label class="text-sm font-medium text-slate-700 lg:pt-2">Địa chỉ</label>
            <div>
              <textarea
                v-model.trim="f.address"
                rows="3"
                placeholder="Nhập địa chỉ"
                class="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-900 transition focus:outline-none focus:ring-2 focus:ring-slate-200 focus:border-slate-400"
              ></textarea>
            </div>
          </div>

          <!-- Submit Button -->
          <div class="flex flex-col gap-3 pt-4 border-t border-slate-200 sm:flex-row sm:items-center sm:justify-end">
            <button
              type="submit"
              class="inline-flex items-center justify-center gap-2 rounded-lg border border-slate-300 bg-slate-900 px-6 py-2.5 text-sm font-medium text-white transition hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-slate-200 disabled:cursor-not-allowed disabled:opacity-50"
              :disabled="saving || !isValid"
            >
              <span
                v-if="saving"
                class="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white"
              ></span>
              {{ saving ? 'Đang lưu...' : 'Lưu thông tin' }}
            </button>
          </div>
        </form>

        <div v-else class="p-6 text-sm text-slate-500">Đang tải thông tin…</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth.store'
import {
  authService,
  type ProfileUpdatePayload,
  type ProfileDetails,
} from '@/services/auth.service'
import { showToast } from '@/utils/toast'

const router = useRouter()
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

// trạng thái đã tương tác từng ô
const touched = reactive({ fullname: false, phone: false, email: false })

// lỗi (chỉ hiển thị khi đã "touched" hoặc khi submit mà còn lỗi)
const errs = reactive<{ fullname?: string; phone?: string; email?: string }>({})

const isEmail = (v: string) => /^\S+@\S+\.\S+$/.test(v)

// cập nhật thông báo lỗi theo dữ liệu
watch(
  () => ({ ...f }),
  () => {
    errs.fullname = f.fullname ? '' : 'Vui lòng nhập họ tên phụ huynh.'
    errs.phone = f.phone ? '' : 'Vui lòng nhập số điện thoại.'
    errs.email = f.email && !isEmail(f.email) ? 'Email không hợp lệ.' : ''
  },
  { deep: true, immediate: true },
)

// điều kiện hợp lệ để bật nút (độc lập với "touched")
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
  // khi bấm lưu, hiển thị lỗi cho các trường bắt buộc nếu còn thiếu
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
