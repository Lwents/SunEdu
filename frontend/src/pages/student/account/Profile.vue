<!-- src/pages/student/account/Profile.vue -->
<template>
  <div class="student-shell">
    <div class="student-container">
      <div class="student-tabs flex items-center gap-1 sm:gap-2">
        <button type="button" class="student-tab student-tab--active">CÁ NHÂN</button>
        <button type="button" class="student-tab" @click="goChangePwd">ĐỔI MẬT KHẨU</button>
        <button type="button" class="student-tab" @click="goParent">PHỤ HUYNH</button>
      </div>

      <div class="student-card mt-4">
        <div class="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <h2 class="text-base font-extrabold uppercase tracking-wide text-slate-900 sm:text-lg">
            THÔNG TIN CÁ NHÂN
          </h2>
          <p class="text-xs font-semibold text-slate-500 sm:text-sm">
            Lần cập nhật gần nhất: <span class="text-slate-900">{{ lastUpdated }}</span>
          </p>
        </div>

        <form v-if="ready" class="mt-6 space-y-6" @submit.prevent="saveProfile">
          <div class="grid gap-2 sm:gap-3 lg:grid-cols-[220px_1fr]">
            <label class="text-sm font-semibold text-slate-900 sm:text-base lg:pt-2"
              >Ảnh đại diện</label
            >
            <div class="space-y-2">
              <div class="flex flex-col gap-4 sm:flex-row sm:items-center">
                <button
                  type="button"
                  class="group relative inline-flex h-28 w-28 items-center justify-center rounded-3xl border-2 border-dashed border-cyan-200 dark:border-cyan-700 bg-white/70 p-1 shadow-sm shadow-slate-100 transition hover:border-cyan-500 dark:border-cyan-600 hover:bg-cyan-50 dark:bg-cyan-900/20"
                  @click="openFile"
                >
                  <img
                    :src="avatarPreview || currentAvatar"
                    alt="Ảnh đại diện"
                    class="h-full w-full rounded-2xl object-cover object-center"
                  />
                  <div
                    class="absolute inset-0 flex flex-col items-center justify-center gap-1 rounded-3xl bg-slate-900/10 text-[11px] font-semibold text-slate-700 opacity-0 transition group-hover:opacity-100"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-5 w-5"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z"
                      />
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M16.5 12.75a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0zM18.75 10.5h.008v.008h-.008V10.5z"
                      />
                    </svg>
                    <span>Đổi ảnh</span>
                  </div>
                </button>
              </div>
              <input
                ref="fileInput"
                type="file"
                accept="image/*"
                class="hidden"
                @change="onPickFile"
              />
            </div>
          </div>

          <div class="grid gap-2 sm:gap-3 lg:grid-cols-[220px_1fr]">
            <label class="text-sm font-semibold text-slate-900 sm:text-base lg:pt-2"
              >Tên đăng nhập</label
            >
            <div class="space-y-2">
              <input
                v-model.trim="form.username"
                type="text"
                readonly
                class="w-full rounded-2xl border border-slate-200 bg-slate-100/80 px-4 py-2.5 text-sm font-semibold text-slate-500 shadow-sm shadow-slate-100"
              />
              <p class="text-xs text-slate-500">
                Tên đăng nhập do hệ thống quản lý, không thể đổi.
              </p>
            </div>
          </div>

          <div class="grid gap-2 sm:gap-3 lg:grid-cols-[220px_1fr]">
            <label class="text-sm font-semibold text-slate-900 sm:text-base lg:pt-2">
              Họ và tên <span class="text-rose-500">*</span>
            </label>
            <div class="space-y-2">
              <input
                v-model.trim="form.fullname"
                type="text"
                placeholder="Họ và tên"
                :class="[
                  'w-full rounded-2xl border px-4 py-2.5 text-sm text-slate-900 shadow-sm shadow-slate-100 transition focus-visible:outline-none focus:ring-4',
                  errors.fullname
                    ? 'border-rose-300 focus:border-rose-400 focus:ring-rose-100'
                    : 'border-slate-200 focus:border-cyan-500 dark:border-cyan-600 focus:ring-cyan-500/30',
                ]"
              />
              <p v-if="errors.fullname" class="text-xs font-medium text-rose-600">
                {{ errors.fullname }}
              </p>
            </div>
          </div>

          <div class="grid gap-2 sm:gap-3 lg:grid-cols-[220px_1fr]">
            <label class="text-sm font-semibold text-slate-900 sm:text-base lg:pt-2">
              Số điện thoại <span class="text-rose-500">*</span>
            </label>
            <div class="space-y-2">
              <input
                v-model.trim="form.phone"
                type="tel"
                :class="[
                  'w-full rounded-2xl border px-4 py-2.5 text-sm text-slate-900 shadow-sm shadow-slate-100 transition focus-visible:outline-none focus:ring-4',
                  errors.phone
                    ? 'border-rose-300 focus:border-rose-400 focus:ring-rose-100'
                    : 'border-slate-200 focus:border-cyan-500 dark:border-cyan-600 focus:ring-cyan-500/30',
                ]"
              />
              <p v-if="errors.phone" class="text-xs font-medium text-rose-600">
                {{ errors.phone }}
              </p>
            </div>
          </div>

          <div class="grid gap-2 sm:gap-3 lg:grid-cols-[220px_1fr]">
            <label class="text-sm font-semibold text-slate-900 sm:text-base lg:pt-2"
              >Ngày sinh</label
            >
            <div class="space-y-2">
              <div class="flex flex-col gap-3 sm:flex-row">
                <select
                  v-model.number="dob.day"
                  class="w-full rounded-2xl border border-slate-200 px-4 py-2.5 text-sm font-medium text-slate-900 shadow-sm shadow-slate-100 transition focus:border-cyan-500 dark:border-cyan-600 focus:outline-none focus:ring-4 focus:ring-cyan-500/30 sm:max-w-[180px]"
                >
                  <option v-for="d in days" :key="d" :value="d">Ngày {{ d }}</option>
                </select>
                <select
                  v-model.number="dob.month"
                  class="w-full rounded-2xl border border-slate-200 px-4 py-2.5 text-sm font-medium text-slate-900 shadow-sm shadow-slate-100 transition focus:border-cyan-500 dark:border-cyan-600 focus:outline-none focus:ring-4 focus:ring-cyan-500/30 sm:max-w-[180px]"
                >
                  <option v-for="m in months" :key="m" :value="m">Tháng {{ m }}</option>
                </select>
                <select
                  v-model.number="dob.year"
                  class="w-full rounded-2xl border border-slate-200 px-4 py-2.5 text-sm font-medium text-slate-900 shadow-sm shadow-slate-100 transition focus:border-cyan-500 dark:border-cyan-600 focus:outline-none focus:ring-4 focus:ring-cyan-500/30 sm:max-w-[200px]"
                >
                  <option v-for="y in years" :key="y" :value="y">Năm {{ y }}</option>
                </select>
              </div>
              <p class="text-xs text-slate-500">Có thể để trống.</p>
            </div>
          </div>

          <div class="grid gap-2 sm:gap-3 lg:grid-cols-[220px_1fr]">
            <label class="text-sm font-semibold text-slate-900 sm:text-base lg:pt-2"
              >Giới tính</label
            >
            <div class="flex flex-wrap gap-3">
              <label
                class="flex flex-1 min-w-[140px] items-center gap-3 rounded-2xl border px-4 py-2 text-sm font-semibold shadow-sm shadow-slate-100 transition"
                :class="
                  form.gender === 'male'
                    ? 'border-cyan-400 dark:border-cyan-500 bg-cyan-50 dark:bg-cyan-900/20 text-cyan-700 dark:text-cyan-300'
                    : 'border-slate-200 text-slate-600'
                "
              >
                <input
                  type="radio"
                  class="h-4 w-4 border-slate-300 text-cyan-600 dark:text-cyan-400 focus:ring-cyan-500/50"
                  value="male"
                  v-model="form.gender"
                />
                Nam
              </label>
              <label
                class="flex flex-1 min-w-[140px] items-center gap-3 rounded-2xl border px-4 py-2 text-sm font-semibold shadow-sm shadow-slate-100 transition"
                :class="
                  form.gender === 'female'
                    ? 'border-cyan-400 dark:border-cyan-500 bg-cyan-50 dark:bg-cyan-900/20 text-cyan-700 dark:text-cyan-300'
                    : 'border-slate-200 text-slate-600'
                "
              >
                <input
                  type="radio"
                  class="h-4 w-4 border-slate-300 text-cyan-600 dark:text-cyan-400 focus:ring-cyan-500/50"
                  value="female"
                  v-model="form.gender"
                />
                Nữ
              </label>
            </div>
          </div>

          <div class="grid gap-2 sm:gap-3 lg:grid-cols-[220px_1fr]">
            <label class="text-sm font-semibold text-slate-900 sm:text-base lg:pt-2">Email</label>
            <div class="space-y-3">
              <div class="space-y-2">
                <input
                  v-model.trim="form.email"
                  type="email"
                  placeholder="you@example.com"
                  :class="[
                    'w-full rounded-2xl border px-4 py-2.5 text-sm text-slate-900 shadow-sm shadow-slate-100 transition focus-visible:outline-none focus:ring-4',
                    errors.email
                      ? 'border-rose-300 focus:border-rose-400 focus:ring-rose-100'
                      : 'border-slate-200 focus:border-cyan-500 dark:border-cyan-600 focus:ring-cyan-500/30',
                  ]"
                />
                <p v-if="errors.email" class="text-xs font-medium text-rose-600">
                  {{ errors.email }}
                </p>
              </div>
            </div>
          </div>

          <div class="grid gap-2 sm:gap-3 lg:grid-cols-[220px_1fr]">
            <label class="text-sm font-semibold text-slate-900 sm:text-base lg:pt-2">Địa chỉ</label>
            <div>
              <textarea
                v-model.trim="form.address"
                rows="3"
                placeholder="Có thể để trống"
                class="w-full rounded-2xl border border-slate-200 px-4 py-3 text-sm text-slate-900 shadow-sm shadow-slate-100 transition focus:border-cyan-500 dark:border-cyan-600 focus-visible:outline-none focus:ring-4 focus:ring-cyan-500/30"
              ></textarea>
            </div>
          </div>

          <div class="grid gap-2 sm:gap-3 lg:grid-cols-[220px_1fr]">
            <label class="text-sm font-semibold text-slate-900 sm:text-base lg:pt-2">
              Tỉnh/Thành phố
            </label>
            <div>
              <select
                v-model.number="selectedProvinceCode"
                :disabled="provincesLoading"
                class="w-full rounded-2xl border border-slate-200 px-4 py-2.5 text-sm font-medium text-slate-900 shadow-sm shadow-slate-100 transition focus:border-cyan-500 dark:border-cyan-600 focus-visible:outline-none focus:ring-4 focus:ring-cyan-500/30 disabled:cursor-not-allowed disabled:bg-slate-100"
              >
                <option value="">
                  {{ provincesLoading ? 'Đang tải...' : 'Chọn tỉnh/thành phố' }}
                </option>
                <option v-for="province in provinces" :key="province.code" :value="province.code">
                  {{ province.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="grid gap-2 sm:gap-3 lg:grid-cols-[220px_1fr]">
            <label class="text-sm font-semibold text-slate-900 sm:text-base lg:pt-2"
              >Quận/Huyện</label
            >
            <div>
              <select
                v-model.number="selectedDistrictCode"
                :disabled="!selectedProvinceCode || districtsLoading"
                class="w-full rounded-2xl border border-slate-200 px-4 py-2.5 text-sm font-medium text-slate-900 shadow-sm shadow-slate-100 transition focus:border-cyan-500 dark:border-cyan-600 focus-visible:outline-none focus:ring-4 focus:ring-cyan-500/30 disabled:cursor-not-allowed disabled:bg-slate-100"
              >
                <option value="">
                  {{
                    !selectedProvinceCode
                      ? 'Chọn tỉnh/thành phố trước'
                      : districtsLoading
                        ? 'Đang tải...'
                        : 'Chọn quận/huyện (có thể để trống)'
                  }}
                </option>
                <option v-for="district in districts" :key="district.code" :value="district.code">
                  {{ district.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="grid gap-2 sm:gap-3 lg:grid-cols-[220px_1fr]">
            <label class="text-sm font-semibold text-slate-900 sm:text-base lg:pt-2"
              >Phường/Xã</label
            >
            <div>
              <select
                v-model.number="selectedWardCode"
                :disabled="!selectedDistrictCode || wardsLoading"
                class="w-full rounded-2xl border border-slate-200 px-4 py-2.5 text-sm font-medium text-slate-900 shadow-sm shadow-slate-100 transition focus:border-cyan-500 dark:border-cyan-600 focus-visible:outline-none focus:ring-4 focus:ring-cyan-500/30 disabled:cursor-not-allowed disabled:bg-slate-100"
              >
                <option value="">
                  {{
                    !selectedDistrictCode
                      ? 'Chọn quận/huyện trước'
                      : wardsLoading
                        ? 'Đang tải...'
                        : 'Chọn phường/xã (có thể để trống)'
                  }}
                </option>
                <option v-for="ward in wards" :key="ward.code" :value="ward.code">
                  {{ ward.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="flex flex-col gap-3 pt-2 sm:flex-row sm:items-center sm:justify-end">
            <button
              type="submit"
              class="inline-flex w-full items-center justify-center gap-2 rounded-2xl border border-transparent bg-gradient-to-r from-cyan-500 to-cyan-600 px-4 py-3 text-xs font-extrabold uppercase tracking-wide text-white shadow-lg shadow-cyan-500/40 transition hover:from-cyan-600 hover:to-cyan-700 hover:shadow-xl hover:-translate-y-0.5 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-cyan-600 disabled:cursor-not-allowed disabled:opacity-60 disabled:hover:translate-y-0 sm:w-auto sm:text-sm"
              :disabled="saving || !isValidInfo || !isDirty"
              :class="{ 'opacity-80': saving }"
            >
              <span
                v-if="saving"
                class="h-4 w-4 animate-spin rounded-full border-2 border-white/60 border-t-white"
              ></span>
              {{ saving ? 'ĐANG CẬP NHẬT...' : 'CẬP NHẬT' }}
            </button>
            <p
              v-if="!isValidInfo"
              class="text-center text-xs font-medium text-slate-500 sm:text-right"
            >
              Vui lòng điền đầy đủ thông tin bắt buộc
            </p>
          </div>
        </form>

        <div v-else class="mt-6 text-sm font-medium text-slate-500">Đang tải thông tin…</div>
      </div>
    </div>
  </div>

  <Transition
    enter-active-class="transition-opacity duration-200"
    leave-active-class="transition-opacity duration-200"
    enter-from-class="opacity-0"
    leave-to-class="opacity-0"
  >
    <div
      v-if="limitModal.open"
      class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 px-4 py-10 backdrop-blur-sm"
      role="dialog"
      aria-modal="true"
      aria-labelledby="limit-title"
      @click.self="closeLimitModal"
    >
      <div
        class="w-full max-w-sm rounded-3xl border border-slate-200 bg-white p-6 text-center shadow-2xl shadow-slate-200 outline-none"
        ref="limitCard"
        tabindex="-1"
      >
        <div class="mb-4 flex flex-col items-center gap-3">
          <div
            class="flex h-14 w-14 items-center justify-center rounded-2xl bg-rose-50 text-rose-500"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-7 w-7"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="1.8"
                d="M12 9v3m0 4h.01M10.29 3.86 1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"
              />
            </svg>
          </div>
          <h3 id="limit-title" class="text-lg font-bold text-slate-900">Không thể tải ảnh</h3>
        </div>
        <p class="text-sm text-slate-600">{{ limitModal.message }}</p>
        <p class="mt-2 text-xs text-slate-500">Vui lòng chọn tệp PNG/JPG ≤ 2MB.</p>
        <div class="mt-6">
          <button
            type="button"
            class="inline-flex w-full items-center justify-center rounded-2xl bg-gradient-to-r from-cyan-500 to-cyan-600 px-4 py-3 text-sm font-bold uppercase tracking-wide text-white shadow-lg shadow-cyan-500/40 transition hover:from-cyan-600 hover:to-cyan-700 hover:shadow-xl hover:-translate-y-0.5 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-cyan-600"
            @click="closeLimitModal"
          >
            ĐÃ HIỂU
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth.store'
import {
  authService,
  type ProfileUpdatePayload,
  type ProfileDetails,
} from '@/services/auth.service'
import {
  locationService,
  type DistrictOption,
  type ProvinceOption,
  type WardOption,
} from '@/services/location.service'
import { showToast } from '@/utils/toast'

const router = useRouter()
const auth = useAuthStore()
const ready = ref(false)

const MAX_AVATAR_SIZE = 2 * 1024 * 1024 // 2MB
const OVER_LIMIT_MSG = 'File ảnh vượt quá dung lượng cho phép (2MB)'

function goChangePwd() {
  router.push({ name: 'student-change-password' })
}
function goParent() {
  router.push({ name: 'student-parent' })
}

const defaultAvatar = 'https://i.pravatar.cc/80?img=10'
const profileDetails = ref<ProfileDetails | null>(null)
const currentAvatar = computed(
  () =>
    auth.user?.avatar ||
    profileDetails.value?.avatar ||
    profileDetails.value?.avatar_url ||
    defaultAvatar,
)

const fileInput = ref<HTMLInputElement | null>(null)
const avatarFile = ref<File | null>(null)
const avatarPreview = ref<string>('')

function openFile() {
  fileInput.value?.click()
}

/** MODAL: thông báo giới hạn dung lượng */
const limitModal = reactive<{ open: boolean; message: string }>({ open: false, message: '' })
const limitCard = ref<HTMLElement | null>(null)

function showLimitModal(msg = OVER_LIMIT_MSG) {
  limitModal.message = msg
  limitModal.open = true
  // focus bẫy trong modal
  queueMicrotask(() => limitCard.value?.focus())
}
function closeLimitModal() {
  limitModal.open = false
}

function handleEsc(e: KeyboardEvent) {
  if (e.key === 'Escape' && limitModal.open) {
    e.stopPropagation()
    closeLimitModal()
  }
}
window.addEventListener('keydown', handleEsc)
onBeforeUnmount(() => window.removeEventListener('keydown', handleEsc))

function onPickFile(e: Event) {
  const input = e.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return

  if (file.size > MAX_AVATAR_SIZE) {
    // Hiển thị HỘP THOẠI
    showLimitModal()
    // reset lựa chọn file
    input.value = ''
    avatarFile.value = null
    avatarPreview.value = ''
    return
  }

  avatarFile.value = file
  const reader = new FileReader()
  reader.onload = () => (avatarPreview.value = String(reader.result || ''))
  reader.readAsDataURL(file)
}

/** FORM DATA */
const form = reactive({
  username: '',
  fullname: '',
  phone: '',
  email: '',
  emailUpdates: false,
  gender: 'male',
  address: '',
  city: '',
  district: '',
  ward: '',
})

const provinces = ref<ProvinceOption[]>([])
const districts = ref<DistrictOption[]>([])
const wards = ref<WardOption[]>([])
const provincesLoading = ref(false)
const districtsLoading = ref(false)
const wardsLoading = ref(false)

const selectedProvinceCode = ref<number | null>(null)
const selectedDistrictCode = ref<number | null>(null)
const selectedWardCode = ref<number | null>(null)
const pendingDistrictName = ref<string | null>(null)
const pendingWardName = ref<string | null>(null)

const dob = reactive({ day: 1, month: 1, year: 2000 })
const days = Array.from({ length: 31 }, (_, i) => i + 1)
const months = Array.from({ length: 12 }, (_, i) => i + 1)
const years = Array.from({ length: 60 }, (_, i) => 1980 + i)

const initialJSON = ref<string>('')

function snapshot() {
  initialJSON.value = JSON.stringify({
    ...form,
    dob: { ...dob },
    avatarPreview: avatarPreview.value,
  })
}

function formatDateTime(value?: string | Date) {
  if (!value) return 'chưa có'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return 'chưa có'
  return new Intl.DateTimeFormat('vi-VN', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  }).format(date)
}

const normalizeName = (value?: string | null) =>
  (value || '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .trim()

function findByName<T extends { name: string }>(list: T[], name?: string | null) {
  if (!name) return undefined
  const target = normalizeName(name)
  return list.find((item) => normalizeName(item.name) === target)
}

async function loadProvinces() {
  provincesLoading.value = true
  try {
    provinces.value = await locationService.listProvinces()
  } catch (error) {
    console.error('Không thể tải danh sách tỉnh/thành phố:', error)
    provinces.value = []
  } finally {
    provincesLoading.value = false
  }
}

async function handleProvinceChanged(code: number | null) {
  form.city = ''
  form.district = ''
  form.ward = ''
  districts.value = []
  wards.value = []
  selectedDistrictCode.value = null
  selectedWardCode.value = null

  if (typeof code !== 'number' || Number.isNaN(code)) {
    return
  }

  const province = provinces.value.find((p) => p.code === code)
  form.city = province?.name || ''

  districtsLoading.value = true
  try {
    districts.value = await locationService.listDistricts(code)
  } catch (error) {
    console.error('Không thể tải danh sách quận/huyện:', error)
    districts.value = []
  } finally {
    districtsLoading.value = false
  }

  if (pendingDistrictName.value) {
    const matchDistrict = findByName(districts.value, pendingDistrictName.value)
    pendingDistrictName.value = null
    if (matchDistrict) {
      selectedDistrictCode.value = matchDistrict.code
      return
    }
  }
}

async function handleDistrictChanged(code: number | null) {
  form.district = ''
  form.ward = ''
  wards.value = []
  selectedWardCode.value = null

  if (typeof code !== 'number' || Number.isNaN(code)) {
    return
  }
  const district = districts.value.find((d) => d.code === code)
  form.district = district?.name || ''

  wardsLoading.value = true
  try {
    wards.value = await locationService.listWards(code)
  } catch (error) {
    console.error('Không thể tải danh sách phường/xã:', error)
    wards.value = []
  } finally {
    wardsLoading.value = false
  }

  if (pendingWardName.value) {
    const matchWard = findByName(wards.value, pendingWardName.value)
    pendingWardName.value = null
    if (matchWard) {
      selectedWardCode.value = matchWard.code
    }
  }
}

function applyProfileToForm(profile?: ProfileDetails | null) {
  if (!profile) return
  form.username = profile.username || profile.name || ''
  form.fullname = profile.fullName || profile.name || ''
  form.phone = profile.phone || ''
  form.email = profile.email || ''
  form.gender = (profile.gender as any) || form.gender
  form.emailUpdates = profile.email_updates ?? false
  form.address = profile.address || ''
  form.city = profile.city || ''
  form.district = profile.district || ''
  form.ward = profile.ward || ''

  if (profile.dob) {
    const [year, month, day] = profile.dob.split('-').map(Number)
    if (year && month && day) {
      dob.year = year
      dob.month = month
      dob.day = day
    }
  }

  avatarPreview.value = profile.avatar || profile.avatar_url || ''
  if (profile.updatedAt || profile.createdAt) {
    lastUpdated.value = formatDateTime(profile.updatedAt || (profile.createdAt as string))
  }
  snapshot()
}

async function hydrateLocationSelections(profile?: ProfileDetails | null) {
  if (!profile) {
    selectedProvinceCode.value = null
    return
  }
  pendingDistrictName.value = profile.district || null
  pendingWardName.value = profile.ward || null
  const provinceMatch = findByName(provinces.value, profile.city || '')
  if (provinceMatch) {
    selectedProvinceCode.value = provinceMatch.code
  } else {
    selectedProvinceCode.value = null
  }
}

onMounted(async () => {
  auth.init?.()
  await loadProvinces()
  try {
    await auth.fetchCurrentUser()
    const profile = await authService.getProfile()
    profileDetails.value = profile
    applyProfileToForm(profile)
    await hydrateLocationSelections(profile)
    const avatarUrl = profile.avatar || profile.avatar_url
    if (avatarUrl) {
      auth.setAvatar(avatarUrl)
    }
  } catch (error) {
    console.error('Không thể tải thông tin hồ sơ:', error)
  } finally {
    ready.value = true
  }
})

/** VALIDATION */
const errors = reactive<{ fullname?: string; phone?: string; email?: string }>({})
const isEmail = (v: string) => /^\S+@\S+\.\S+$/.test(v)

watch(
  () => ({ ...form }),
  () => {
    if (!ready.value) return
    errors.fullname = form.fullname ? '' : 'Vui lòng nhập họ và tên.'
    errors.phone = form.phone ? '' : 'Vui lòng nhập số điện thoại.'
    errors.email = form.email && !isEmail(form.email) ? 'Email không hợp lệ.' : ''
  },
  { deep: true },
)

watch(selectedProvinceCode, (code) => {
  const normalized = typeof code === 'number' && !Number.isNaN(code) ? code : null
  handleProvinceChanged(normalized)
})

watch(selectedDistrictCode, (code) => {
  const normalized = typeof code === 'number' && !Number.isNaN(code) ? code : null
  handleDistrictChanged(normalized)
})

watch(selectedWardCode, (code) => {
  const normalized = typeof code === 'number' && !Number.isNaN(code) ? code : null
  if (!normalized) {
    form.ward = ''
    return
  }
  const ward = wards.value.find((w) => w.code === normalized)
  form.ward = ward?.name || ''
})

const isValidInfo = computed(() => !errors.fullname && !errors.phone && !errors.email)
const isDirty = computed(() => {
  const now = JSON.stringify({ ...form, dob: { ...dob }, avatarPreview: avatarPreview.value })
  return now !== initialJSON.value
})

/** SAVE */
const saving = ref(false)
const lastUpdated = ref('chưa có')

async function saveProfile() {
  if (!isValidInfo.value) {
    showToast('Vui lòng kiểm tra lại các trường bắt buộc.', 'error')
    return
  }
  if (!isDirty.value) return

  saving.value = true
  try {
    const payload: ProfileUpdatePayload = {
      full_name: form.fullname || undefined,
      phone: form.phone || undefined,
      email: form.email || undefined,
      gender: form.gender || undefined,
      avatar_url:
        avatarPreview.value || profileDetails.value?.avatar || profileDetails.value?.avatar_url,
      email_updates: form.emailUpdates,
      address: form.address || undefined,
      city: form.city || undefined,
      district: form.district || undefined,
      ward: form.ward || undefined,
    }

    if (dob.year && dob.month && dob.day) {
      payload.dob = `${dob.year}-${String(dob.month).padStart(2, '0')}-${String(dob.day).padStart(2, '0')}`
    }

    const updated = await auth.updateProfile(payload)
    profileDetails.value = updated
    applyProfileToForm(updated)
    lastUpdated.value = formatDateTime(updated.updatedAt || updated.createdAt || new Date())
    snapshot()
    avatarFile.value = null
    avatarPreview.value = ''
    if (fileInput.value) fileInput.value.value = ''
    showToast('Cập nhật hồ sơ thành công!', 'success')
  } catch (e) {
    showToast('Cập nhật thất bại. Thử lại sau.', 'error')
  } finally {
    saving.value = false
  }
}
</script>
