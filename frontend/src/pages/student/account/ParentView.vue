<!-- src/pages/student/account/ParentInfo.vue -->
<template>
  <div class="student-shell">
    <div class="student-container">
      <div class="student-tabs flex items-center gap-1 sm:gap-2">
        <button type="button" class="student-tab" @click="goProfile">CÁ NHÂN</button>
        <button type="button" class="student-tab" @click="goChangePwd">ĐỔI MẬT KHẨU</button>
        <button type="button" class="student-tab student-tab--active">PHỤ HUYNH</button>
      </div>

      <div class="student-card mt-4">
        <div class="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <h2 class="text-base font-extrabold uppercase tracking-wide text-slate-900 sm:text-lg">
            THÔNG TIN PHỤ HUYNH
          </h2>
        </div>

        <Transition
          enter-active-class="transition-opacity duration-200"
          leave-active-class="transition-opacity duration-200"
          enter-from-class="opacity-0"
          leave-to-class="opacity-0"
        >
          <div
            v-if="toast.msg"
            :class="[
              'fixed bottom-4 right-4 z-40 rounded-2xl border px-4 py-3 text-sm font-medium shadow-lg sm:text-base',
              toast.type === 'success'
                ? 'border-emerald-200 bg-emerald-50 text-emerald-700'
                : 'border-rose-200 bg-rose-50 text-rose-700',
            ]"
          >
            {{ toast.msg }}
          </div>
        </Transition>

        <form v-if="!loading" class="mt-6 space-y-6" @submit.prevent="save">
          <div class="grid gap-2 sm:gap-3 lg:grid-cols-[220px_1fr]">
            <label class="text-sm font-semibold text-slate-900 sm:text-base lg:pt-2">
              Họ tên phụ huynh <span class="text-rose-500">*</span>
            </label>
            <div class="space-y-2">
              <input
                v-model.trim="f.fullname"
                placeholder="Ví dụ: Nguyễn Văn B"
                @blur="touched.fullname = true"
                :class="[
                  'w-full rounded-2xl border px-4 py-2.5 text-sm text-slate-900 shadow-sm shadow-slate-100 transition focus-visible:outline-none focus:ring-4',
                  touched.fullname && errs.fullname
                    ? 'border-rose-300 focus:border-rose-400 focus:ring-rose-100'
                    : 'border-slate-200 focus:border-emerald-500 focus:ring-emerald-100',
                ]"
              />
              <p v-if="touched.fullname && errs.fullname" class="text-xs font-medium text-rose-600">
                {{ errs.fullname }}
              </p>
            </div>
          </div>

          <div class="grid gap-2 sm:gap-3 lg:grid-cols-[220px_1fr]">
            <label class="text-sm font-semibold text-slate-900 sm:text-base lg:pt-2">
              Số điện thoại <span class="text-rose-500">*</span>
            </label>
            <div class="space-y-2">
              <input
                v-model.trim="f.phone"
                type="tel"
                inputmode="tel"
                placeholder="09xxxxxxxx"
                @blur="touched.phone = true"
                :class="[
                  'w-full rounded-2xl border px-4 py-2.5 text-sm text-slate-900 shadow-sm shadow-slate-100 transition focus-visible:outline-none focus:ring-4',
                  touched.phone && errs.phone
                    ? 'border-rose-300 focus:border-rose-400 focus:ring-rose-100'
                    : 'border-slate-200 focus:border-emerald-500 focus:ring-emerald-100',
                ]"
              />
              <p v-if="touched.phone && errs.phone" class="text-xs font-medium text-rose-600">
                {{ errs.phone }}
              </p>
            </div>
          </div>

          <div class="grid gap-2 sm:gap-3 lg:grid-cols-[220px_1fr]">
            <label class="text-sm font-semibold text-slate-900 sm:text-base lg:pt-2">Email</label>
            <div class="space-y-2">
              <input
                v-model.trim="f.email"
                type="email"
                placeholder="parent@example.com"
                @blur="touched.email = true"
                :class="[
                  'w-full rounded-2xl border px-4 py-2.5 text-sm text-slate-900 shadow-sm shadow-slate-100 transition focus-visible:outline-none focus:ring-4',
                  touched.email && errs.email
                    ? 'border-rose-300 focus:border-rose-400 focus:ring-rose-100'
                    : 'border-slate-200 focus:border-emerald-500 focus:ring-emerald-100',
                ]"
              />
              <p v-if="touched.email && errs.email" class="text-xs font-medium text-rose-600">
                {{ errs.email }}
              </p>
            </div>
          </div>

          <div class="grid gap-2 sm:gap-3 lg:grid-cols-[220px_1fr]">
            <label class="text-sm font-semibold text-slate-900 sm:text-base lg:pt-2">Mối quan hệ</label>
            <div>
              <select
                v-model="f.relation"
                class="w-full rounded-2xl border border-slate-200 px-4 py-2.5 text-sm font-medium text-slate-900 shadow-sm shadow-slate-100 transition focus:border-emerald-500 focus-visible:outline-none focus:ring-4 focus:ring-emerald-100"
              >
                <option value="">Chọn</option>
                <option>Bố</option>
                <option>Mẹ</option>
                <option>Người giám hộ</option>
              </select>
            </div>
          </div>

          <div class="grid gap-2 sm:gap-3 lg:grid-cols-[220px_1fr]">
            <label class="text-sm font-semibold text-slate-900 sm:text-base lg:pt-2">Địa chỉ</label>
            <div>
              <textarea
                v-model.trim="f.address"
                rows="3"
                placeholder="Số nhà, đường, phường/xã, quận/huyện, tỉnh/thành"
                class="w-full rounded-2xl border border-slate-200 px-4 py-3 text-sm text-slate-900 shadow-sm shadow-slate-100 transition focus:border-emerald-500 focus-visible:outline-none focus:ring-4 focus:ring-emerald-100"
              ></textarea>
            </div>
          </div>

          <div class="flex flex-col gap-3 pt-2 sm:flex-row sm:items-center sm:justify-end">
            <button
              type="submit"
              class="inline-flex w-full items-center justify-center gap-2 rounded-2xl border border-transparent bg-emerald-500 px-4 py-3 text-xs font-extrabold uppercase tracking-wide text-white shadow-lg shadow-emerald-200 transition hover:bg-emerald-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-600 disabled:cursor-not-allowed disabled:border-slate-200 disabled:bg-slate-200 disabled:text-slate-500 sm:w-auto sm:text-sm"
              :disabled="saving || !isValid"
            >
              <span
                v-if="saving"
                class="h-4 w-4 animate-spin rounded-full border-2 border-white/60 border-t-white"
              ></span>
              {{ saving ? 'ĐANG LƯU...' : 'LƯU THÔNG TIN' }}
            </button>
            <p v-if="!isValid" class="text-center text-xs font-medium text-slate-500 sm:text-right">
              Vui lòng điền đầy đủ thông tin bắt buộc
            </p>
          </div>
        </form>

        <div v-else class="mt-6 text-sm font-medium text-slate-500">Đang tải thông tin…</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth.store'
import { authService, type ProfileUpdatePayload, type ProfileDetails } from '@/services/auth.service'

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

const toast = reactive<{ msg: string; type: 'success' | 'error' | '' }>({ msg: '', type: '' })
let toastTimer: number | undefined
function showToast(msg: string, type: 'success' | 'error') {
  toast.msg = msg
  toast.type = type
  clearTimeout(toastTimer)
  toastTimer = window.setTimeout(() => (toast.msg = ''), 2500)
}

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
