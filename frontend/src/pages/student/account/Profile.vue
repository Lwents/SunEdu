<!-- src/pages/student/account/Profile.vue -->
<template>
  <div class="min-h-screen bg-slate-50">
    <div class="mx-auto max-w-4xl px-4 py-6 sm:px-6 lg:px-8">
      <!-- Tabs -->
      <div class="mb-6 flex items-center gap-2 border-b border-slate-200">
        <button
          type="button"
          class="border-b-2 border-slate-900 px-4 py-3 text-sm font-semibold text-slate-900"
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
          class="px-4 py-3 text-sm font-medium text-slate-600 transition hover:text-slate-900"
          @click="goParent"
        >
          Phụ huynh
        </button>
      </div>

      <!-- Main Card -->
      <div class="rounded-lg border border-slate-200 bg-white shadow-sm">
        <div class="border-b border-slate-200 px-6 py-4">
        <div class="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
            <h2 class="text-lg font-semibold text-slate-900">Thông tin cá nhân</h2>
            <p class="text-xs text-slate-500">
              Cập nhật lần cuối: <span class="text-slate-700">{{ lastUpdated }}</span>
          </p>
          </div>
        </div>

        <form v-if="ready" class="p-6 space-y-6" @submit.prevent="saveProfile">
          <!-- Avatar -->
          <div class="grid gap-3 lg:grid-cols-[180px_1fr]">
            <label class="text-sm font-medium text-slate-700 lg:pt-2">Ảnh đại diện</label>
            <div class="space-y-2">
                <button
                  type="button"
                class="group relative inline-flex h-24 w-24 items-center justify-center rounded-lg border border-slate-300 bg-white overflow-hidden transition hover:border-slate-400"
                  @click="openFile"
                >
                  <img
                    :src="avatarPreview || currentAvatar"
                    alt="Ảnh đại diện"
                  class="h-full w-full object-cover"
                  />
                  <div
                  class="absolute inset-0 flex items-center justify-center bg-slate-900/60 opacity-0 transition group-hover:opacity-100"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                    class="h-5 w-5 text-white"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                      d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                      />
                    </svg>
                  </div>
                </button>
              <p class="text-xs text-slate-500">Nhấn để đổi ảnh (tối đa 2MB)</p>
              <input
                ref="fileInput"
                type="file"
                accept="image/*"
                class="hidden"
                @change="onPickFile"
              />
            </div>
          </div>

          <!-- Username -->
          <div class="grid gap-3 lg:grid-cols-[180px_1fr]">
            <label class="text-sm font-medium text-slate-700 lg:pt-2">Tên đăng nhập</label>
            <div class="space-y-1">
              <input
                v-model.trim="form.username"
                type="text"
                readonly
                class="w-full rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-600"
              />
              <p class="text-xs text-slate-500">Không thể thay đổi</p>
            </div>
          </div>

          <!-- Full Name -->
          <div class="grid gap-3 lg:grid-cols-[180px_1fr]">
            <label class="text-sm font-medium text-slate-700 lg:pt-2">
              Họ và tên <span class="text-red-500">*</span>
            </label>
            <div class="space-y-1">
              <input
                v-model.trim="form.fullname"
                type="text"
                placeholder="Nhập họ và tên"
                :class="[
                  'w-full rounded-lg border px-3 py-2 text-sm text-slate-900 transition focus:outline-none focus:ring-2',
                  errors.fullname
                    ? 'border-red-300 focus:border-red-400 focus:ring-red-200'
                    : 'border-slate-300 focus:border-slate-400 focus:ring-slate-200',
                ]"
              />
              <p v-if="errors.fullname" class="text-xs text-red-600">
                {{ errors.fullname }}
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
                v-model.trim="form.phone"
                type="tel"
                placeholder="Nhập số điện thoại"
                :class="[
                  'w-full rounded-lg border px-3 py-2 text-sm text-slate-900 transition focus:outline-none focus:ring-2',
                  errors.phone
                    ? 'border-red-300 focus:border-red-400 focus:ring-red-200'
                    : 'border-slate-300 focus:border-slate-400 focus:ring-slate-200',
                ]"
              />
              <p v-if="errors.phone" class="text-xs text-red-600">
                {{ errors.phone }}
              </p>
            </div>
          </div>

          <!-- Date of Birth -->
          <div class="grid gap-3 lg:grid-cols-[180px_1fr]">
            <label class="text-sm font-medium text-slate-700 lg:pt-2">Ngày sinh</label>
            <div class="space-y-1">
              <div class="flex gap-2">
                <select
                  v-model.number="dob.day"
                  class="flex-1 rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-200 focus:border-slate-400"
                >
                  <option v-for="d in days" :key="d" :value="d">Ngày {{ d }}</option>
                </select>
                <select
                  v-model.number="dob.month"
                  class="flex-1 rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-200 focus:border-slate-400"
                >
                  <option v-for="m in months" :key="m" :value="m">Tháng {{ m }}</option>
                </select>
                <select
                  v-model.number="dob.year"
                  class="flex-1 rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-200 focus:border-slate-400"
                >
                  <option v-for="y in years" :key="y" :value="y">Năm {{ y }}</option>
                </select>
              </div>
              <p class="text-xs text-slate-500">Có thể để trống</p>
            </div>
          </div>

          <!-- Gender -->
          <div class="grid gap-3 lg:grid-cols-[180px_1fr]">
            <label class="text-sm font-medium text-slate-700 lg:pt-2">Giới tính</label>
            <div class="flex gap-3">
              <label
                class="flex items-center gap-2 rounded-lg border px-4 py-2 text-sm transition cursor-pointer"
                :class="
                  form.gender === 'male'
                    ? 'border-slate-400 bg-slate-50 text-slate-900'
                    : 'border-slate-300 text-slate-600 hover:border-slate-400'
                "
              >
                <input
                  type="radio"
                  class="h-4 w-4 text-slate-600 focus:ring-slate-200"
                  value="male"
                  v-model="form.gender"
                />
                Nam
              </label>
              <label
                class="flex items-center gap-2 rounded-lg border px-4 py-2 text-sm transition cursor-pointer"
                :class="
                  form.gender === 'female'
                    ? 'border-slate-400 bg-slate-50 text-slate-900'
                    : 'border-slate-300 text-slate-600 hover:border-slate-400'
                "
              >
                <input
                  type="radio"
                  class="h-4 w-4 text-slate-600 focus:ring-slate-200"
                  value="female"
                  v-model="form.gender"
                />
                Nữ
              </label>
            </div>
          </div>

          <!-- Email -->
          <div class="grid gap-3 lg:grid-cols-[180px_1fr]">
            <label class="text-sm font-medium text-slate-700 lg:pt-2">Email</label>
            <div class="space-y-1">
                <input
                  v-model.trim="form.email"
                  type="email"
                  placeholder="you@example.com"
                  :class="[
                  'w-full rounded-lg border px-3 py-2 text-sm text-slate-900 transition focus:outline-none focus:ring-2',
                    errors.email
                    ? 'border-red-300 focus:border-red-400 focus:ring-red-200'
                    : 'border-slate-300 focus:border-slate-400 focus:ring-slate-200',
                  ]"
                />
              <p v-if="errors.email" class="text-xs text-red-600">
                  {{ errors.email }}
                </p>
            </div>
          </div>

          <!-- Address -->
          <div class="grid gap-3 lg:grid-cols-[180px_1fr]">
            <label class="text-sm font-medium text-slate-700 lg:pt-2">Địa chỉ</label>
            <div>
              <textarea
                v-model.trim="form.address"
                rows="3"
                placeholder="Nhập địa chỉ"
                class="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-900 transition focus:outline-none focus:ring-2 focus:ring-slate-200 focus:border-slate-400"
              ></textarea>
            </div>
          </div>

          <!-- Province -->
          <div class="grid gap-3 lg:grid-cols-[180px_1fr]">
            <label class="text-sm font-medium text-slate-700 lg:pt-2">Tỉnh/Thành phố</label>
            <div>
              <select
                v-model.number="selectedProvinceCode"
                :disabled="provincesLoading"
                class="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-900 transition focus:outline-none focus:ring-2 focus:ring-slate-200 focus:border-slate-400 disabled:cursor-not-allowed disabled:bg-slate-100"
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

          <!-- District -->
          <div class="grid gap-3 lg:grid-cols-[180px_1fr]">
            <label class="text-sm font-medium text-slate-700 lg:pt-2">Quận/Huyện</label>
            <div>
              <select
                v-model.number="selectedDistrictCode"
                :disabled="!selectedProvinceCode || districtsLoading"
                class="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-900 transition focus:outline-none focus:ring-2 focus:ring-slate-200 focus:border-slate-400 disabled:cursor-not-allowed disabled:bg-slate-100"
              >
                <option value="">
                  {{
                    !selectedProvinceCode
                      ? 'Chọn tỉnh/thành phố trước'
                      : districtsLoading
                        ? 'Đang tải...'
                        : 'Chọn quận/huyện'
                  }}
                </option>
                <option v-for="district in districts" :key="district.code" :value="district.code">
                  {{ district.name }}
                </option>
              </select>
            </div>
          </div>

          <!-- Ward -->
          <div class="grid gap-3 lg:grid-cols-[180px_1fr]">
            <label class="text-sm font-medium text-slate-700 lg:pt-2">Phường/Xã</label>
            <div>
              <select
                v-model.number="selectedWardCode"
                :disabled="!selectedDistrictCode || wardsLoading"
                class="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-900 transition focus:outline-none focus:ring-2 focus:ring-slate-200 focus:border-slate-400 disabled:cursor-not-allowed disabled:bg-slate-100"
              >
                <option value="">
                  {{
                    !selectedDistrictCode
                      ? 'Chọn quận/huyện trước'
                      : wardsLoading
                        ? 'Đang tải...'
                        : 'Chọn phường/xã'
                  }}
                </option>
                <option v-for="ward in wards" :key="ward.code" :value="ward.code">
                  {{ ward.name }}
                </option>
              </select>
            </div>
          </div>

          <!-- Submit Button -->
          <div class="flex flex-col gap-3 pt-4 border-t border-slate-200 sm:flex-row sm:items-center sm:justify-end">
            <p
              v-if="!isValidInfo"
              class="text-xs text-slate-500 sm:mr-auto"
            >
              Vui lòng điền đầy đủ thông tin bắt buộc
            </p>
            <button
              type="submit"
              class="inline-flex items-center justify-center gap-2 rounded-lg border border-slate-300 bg-slate-900 px-6 py-2.5 text-sm font-medium text-white transition hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-slate-200 disabled:cursor-not-allowed disabled:opacity-50"
              :disabled="saving || !isValidInfo || !isDirty"
            >
              <span
                v-if="saving"
                class="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white"
              ></span>
              {{ saving ? 'Đang cập nhật...' : 'Cập nhật' }}
            </button>
          </div>
        </form>

        <div v-else class="p-6 text-sm text-slate-500">Đang tải thông tin…</div>
      </div>
    </div>
  </div>

  <!-- Error Modal -->
  <Transition
    enter-active-class="transition-opacity duration-200"
    leave-active-class="transition-opacity duration-200"
    enter-from-class="opacity-0"
    leave-to-class="opacity-0"
  >
    <div
      v-if="limitModal.open"
      class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 px-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby="limit-title"
      @click.self="closeLimitModal"
    >
      <div
        class="w-full max-w-sm rounded-lg border border-slate-200 bg-white p-6 shadow-lg outline-none"
        ref="limitCard"
        tabindex="-1"
      >
        <div class="mb-4 flex flex-col items-center gap-3">
          <div class="flex h-12 w-12 items-center justify-center rounded-full bg-red-50 text-red-600">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 9v3m0 4h.01M10.29 3.86 1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"
              />
            </svg>
          </div>
          <h3 id="limit-title" class="text-lg font-semibold text-slate-900">Không thể tải ảnh</h3>
        </div>
        <p class="text-sm text-slate-600">{{ limitModal.message }}</p>
        <p class="mt-2 text-xs text-slate-500">Vui lòng chọn tệp PNG/JPG ≤ 2MB.</p>
        <div class="mt-6">
          <button
            type="button"
            class="w-full rounded-lg border border-slate-300 bg-slate-900 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-slate-200"
            @click="closeLimitModal"
          >
            Đã hiểu
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
