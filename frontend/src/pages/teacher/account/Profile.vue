<template>
  <div class="min-h-screen bg-slate-50 p-4 sm:p-6">
    <div class="mx-auto max-w-4xl">
      <section class="rounded-xl border border-slate-200 bg-white shadow-sm">
        <div class="flex items-center justify-between border-b border-slate-200 p-6">
          <div>
            <h2 class="text-xl font-bold text-slate-800">Hồ sơ giảng viên</h2>
            <p class="mt-1 text-sm text-slate-500">
              Cập nhật thông tin cá nhân và giới thiệu của bạn.
            </p>
          </div>
          <button
            class="shrink-0 whitespace-nowrap rounded-lg border border-slate-300 px-2.5 py-1 text-xs font-medium text-slate-600 transition-colors hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-50 sm:px-3 sm:py-1.5 sm:text-sm"
            @click="resetForm"
            :disabled="loading || !isDirty"
          >
            Hoàn tác
          </button>
        </div>

        <form class="space-y-6 p-6" @submit.prevent="onSave">
          <div class="flex flex-col gap-4 sm:flex-row sm:items-center">
            <!-- Avatar clickable -->
            <div class="flex items-center gap-4">
              <!-- Hidden input -->
              <input
                ref="avatarInputRef"
                id="avatarInput"
                type="file"
                class="hidden"
                accept="image/*"
                @change="onPick"
              />
              <!-- Label wraps avatar to trigger file picker -->
              <label
                for="avatarInput"
                class="relative inline-block cursor-pointer"
                aria-label="Đổi ảnh đại diện"
                title="Đổi ảnh đại diện"
              >
                <img
                  :src="preview || auth.user?.avatar || form.avatar || fallback120"
                  class="h-20 w-20 rounded-full object-cover ring-2 ring-slate-200 transition-all hover:ring-blue-300"
                  alt="avatar"
                />
                <!-- camera badge -->
                <span
                  class="absolute -right-1 -bottom-1 grid h-6 w-6 place-items-center rounded-full border border-white bg-slate-800 text-white shadow ring-1 ring-black/5"
                >
                  <svg viewBox="0 0 20 20" fill="currentColor" class="h-3.5 w-3.5">
                    <path
                      d="M4 6.5A1.5 1.5 0 0 1 5.5 5h1.172a2 2 0 0 0 1.414-.586l.328-.328A2 2 0 0 1 9.828 3h.344a2 2 0 0 1 1.414.586l.328.328A2 2 0 0 0 13.328 5H14.5A1.5 1.5 0 0 1 16 6.5v6A1.5 1.5 0 0 1 14.5 14h-9A1.5 1.5 0 0 1 4 12.5v-6Zm6 6a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z"
                    />
                  </svg>
                </span>
              </label>
            </div>

            <div class="space-y-2">
              <p class="text-xs text-slate-500">Chấp nhận PNG, JPG, WebP. Kích thước tối đa 10MB.</p>
              <p v-if="errors.avatar" class="text-xs text-red-600" aria-live="polite">
                {{ errors.avatar }}
              </p>
            </div>
          </div>

          <hr class="border-slate-200" />

          <div class="grid grid-cols-1 gap-x-6 gap-y-5 sm:grid-cols-2">
            <div class="space-y-1.5">
              <label for="name" class="text-sm font-medium text-slate-700">Họ tên</label>
              <input
                id="name"
                v-model.trim="form.name"
                class="w-full rounded-lg border border-slate-300 bg-slate-50 px-3 py-2 text-slate-800 transition-colors focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                placeholder="Nguyễn Văn A"
              />
              <p v-if="errors.name" class="mt-1 text-xs text-red-600" aria-live="polite">
                {{ errors.name }}
              </p>
            </div>

            <div class="space-y-1.5">
              <label for="email" class="text-sm font-medium text-slate-700">Email</label>
              <input
                id="email"
                v-model.trim="form.email"
                type="email"
                class="w-full rounded-lg border border-slate-300 bg-slate-50 px-3 py-2 text-slate-800 transition-colors focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                placeholder="teacher@example.com"
              />
              <p v-if="errors.email" class="mt-1 text-xs text-red-600" aria-live="polite">
                {{ errors.email }}
              </p>
            </div>

            <div class="space-y-1.5">
              <label for="phone" class="text-sm font-medium text-slate-700">Số điện thoại</label>
              <input
                id="phone"
                v-model.trim="form.phone"
                class="w-full rounded-lg border border-slate-300 bg-slate-50 px-3 py-2 text-slate-800 transition-colors focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                placeholder="09xx xxx xxx"
              />
            </div>

            <div class="space-y-1.5">
              <label for="title" class="text-sm font-medium text-slate-700">Chức danh</label>
              <input
                id="title"
                v-model.trim="form.title"
                class="w-full rounded-lg border border-slate-300 bg-slate-50 px-3 py-2 text-slate-800 transition-colors focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                placeholder="Giảng viên / Mentor"
              />
            </div>

            <div class="space-y-1.5">
              <label for="gender" class="text-sm font-medium text-slate-700">Giới tính</label>
              <select
                id="gender"
                v-model="form.gender"
                class="w-full rounded-lg border border-slate-300 bg-slate-50 px-3 py-2 text-slate-800 transition-colors focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              >
                <option value="">Chọn giới tính</option>
                <option value="male">Nam</option>
                <option value="female">Nữ</option>
                <option value="other">Khác</option>
              </select>
            </div>
          </div>

          <div class="space-y-1.5">
            <label for="bio" class="text-sm font-medium text-slate-700">Giới thiệu</label>
            <textarea
              id="bio"
              v-model.trim="form.bio"
              rows="4"
              class="w-full rounded-lg border border-slate-300 bg-slate-50 px-3 py-2 text-slate-800 transition-colors focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              placeholder="Mô tả ngắn về kinh nghiệm, thế mạnh giảng dạy…"
            ></textarea>
          </div>

          <hr class="border-slate-200" />

          <div class="flex flex-wrap items-center gap-3 sm:gap-4">
            <button
              type="submit"
              class="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white transition-colors hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-blue-400"
              :disabled="loading || !isDirty"
            >
              <span v-if="loading">Đang lưu...</span>
              <span v-else>Lưu thay đổi</span>
            </button>

            <RouterLink
              to="/teacher/account/change-password"
              class="text-sm font-medium text-blue-600 transition-colors hover:underline"
            >
              Đổi mật khẩu
            </RouterLink>

            <transition
              enter-active-class="transition ease-out duration-300"
              enter-from-class="transform opacity-0 scale-95"
              enter-to-class="transform opacity-100 scale-100"
              leave-active-class="transition ease-in duration-200"
              leave-from-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95"
            >
              <span
                v-if="saved"
                class="flex items-center gap-2 text-sm text-green-600"
                role="status"
                aria-live="polite"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  class="h-5 w-5"
                >
                  <path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
                    clip-rule="evenodd"
                  />
                </svg>
                Đã lưu thành công!
              </span>
            </transition>
          </div>
        </form>
      </section>
    </div>

    <!-- ===== Modal thông báo dung lượng ảnh (giống student) ===== -->
    <transition
      enter-active-class="transition-opacity duration-150 ease-out"
      leave-active-class="transition-opacity duration-150 ease-in"
      enter-from-class="opacity-0"
      leave-to-class="opacity-0"
    >
      <div
        v-if="limitModal.open"
        class="fixed inset-0 z-50 grid place-items-center bg-slate-900/50 p-4"
        role="dialog"
        aria-modal="true"
        aria-labelledby="limit-title"
        @click.self="closeLimitModal"
      >
        <div
          ref="limitCard"
          tabindex="-1"
          class="w-full max-w-md rounded-xl border border-slate-200 bg-white p-4 shadow-2xl outline-none"
        >
          <div class="mb-2 flex items-center gap-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5 text-amber-500"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M12 9v3m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"
              />
            </svg>
            <h3 id="limit-title" class="text-base font-bold text-slate-800">Không thể tải ảnh</h3>
          </div>
          <div class="mb-3 text-sm text-slate-800">
            <p>{{ limitModal.message }}</p>
            <small class="mt-1 block text-slate-500">Vui lòng chọn tệp PNG/JPG ≤ 10MB.</small>
          </div>
          <div class="flex justify-end">
            <button
              type="button"
              class="rounded-lg bg-blue-600 px-3 py-2 text-sm font-semibold text-white hover:bg-blue-700"
              @click="closeLimitModal"
            >
              ĐÃ HIỂU
            </button>
          </div>
        </div>
      </div>
    </transition>
    <!-- ===== /Modal ===== -->
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref, watch, onMounted, onBeforeUnmount } from 'vue'
import { useAuthStore } from '@/store/auth.store'
import { authService, type AuthUser } from '@/services/auth.service'
import { getAvatarSrc } from '@/utils/avatar'
import { showToast } from '@/utils/toast'

const auth = useAuthStore()
const user = computed<AuthUser | null>(() => auth.user)

/** constants */
const MAX_AVATAR_SIZE = 10 * 1024 * 1024 // 10MB
const OVER_LIMIT_MSG = 'File ảnh vượt quá dung lượng cho phép (10MB)'

/** fallback - dựa vào gender và role */
const fallback120 = computed(() => {
  return getAvatarSrc(
    user.value?.avatar,
    user.value?.gender as 'male' | 'female' | 'other' | null | undefined,
    'instructor'
  )
})

/** form state */
const original = reactive({
  name: user.value?.name ?? '',
  email: user.value?.email ?? '',
  phone: user.value?.phone ?? '',
  title: (user.value as any)?.title ?? '',
  bio: (user.value as any)?.bio ?? '',
  gender: user.value?.gender ?? '',
  avatar: user.value?.avatar ?? '',
})
const form = reactive({ ...original })
const errors = reactive<{ [k: string]: string }>({})
const loading = ref(false)
const saved = ref(false)

/** dirty */
const isDirty = computed(() => {
  // Kiểm tra thay đổi trong form
  const formChanged = JSON.stringify(form) !== JSON.stringify(original)
  // Kiểm tra có avatar mới được chọn chưa
  const hasNewAvatar = preview.value !== null
  return formChanged || hasNewAvatar
})

/** file input ref + preview */
const avatarInputRef = ref<HTMLInputElement | null>(null)
const preview = ref<string | null>(null)

/** ===== Modal state & handlers (giống student) ===== */
const limitModal = reactive<{ open: boolean; message: string }>({ open: false, message: '' })
const limitCard = ref<HTMLElement | null>(null)
function showLimitModal(msg = OVER_LIMIT_MSG) {
  limitModal.message = msg
  limitModal.open = true
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
onMounted(() => {
  window.addEventListener('keydown', handleEsc)
  loadProfile()
})
onBeforeUnmount(() => window.removeEventListener('keydown', handleEsc))

/** helpers */
function resetFile() {
  if (avatarInputRef.value) avatarInputRef.value.value = ''
  preview.value = null
  // không set errors.avatar ở đây vì oversize dùng modal thông báo
}

/** Load profile fresh from backend so F5 shows latest data */
async function loadProfile() {
  try {
    const profile = await authService.getProfile()
    const updatedUser: AuthUser = {
      ...(auth.user ?? {}),
      id: (auth.user as AuthUser | null)?.id ?? profile.id ?? 0,
      name: profile.fullName || profile.name || auth.user?.name || '',
      email: profile.email || auth.user?.email || '',
      phone: profile.phone || auth.user?.phone,
      role: (auth.user as AuthUser | null)?.role ?? 'instructor',
      avatar: profile.avatar || profile.avatar_url || auth.user?.avatar,
      gender: profile.gender ?? auth.user?.gender,
      title: profile.title ?? (profile as any)?.metadata?.title ?? (auth.user as any)?.title,
      bio: profile.bio ?? (profile as any)?.metadata?.bio ?? (auth.user as any)?.bio,
    }
    auth.user = updatedUser
    auth.persist()
    Object.assign(original, {
      name: updatedUser.name ?? '',
      email: updatedUser.email ?? '',
      phone: updatedUser.phone ?? '',
      title: (updatedUser as any)?.title ?? '',
      bio: (updatedUser as any)?.bio ?? '',
      gender: (updatedUser as any)?.gender ?? '',
      avatar: updatedUser.avatar ?? '',
    })
    resetForm()
  } catch (e) {
    console.warn('Không thể tải hồ sơ giáo viên:', e)
  }
}

const onPick = (e: Event) => {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return

  // type check (vẫn giữ PNG/JPG/WebP như bản teacher)
  if (!/^image\/(png|jpe?g|webp)$/.test(file.type)) {
    errors.avatar = 'Chỉ nhận PNG/JPG/WebP'
    resetFile()
    return
  }

  // size check -> MỞ MODAL giống student
  if (file.size > MAX_AVATAR_SIZE) {
    showLimitModal() // Hiển thị hộp thoại
    resetFile() // Reset input file & preview
    return
  }

  errors.avatar = ''
  const reader = new FileReader()
  reader.onload = () => (preview.value = reader.result as string)
  reader.readAsDataURL(file)
}

/** validate */
const isEmail = (v: string) => !v || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)
const validate = () => {
  errors.name = form.name ? '' : 'Vui lòng nhập họ tên'
  errors.email = isEmail(form.email) ? '' : 'Email không hợp lệ'
  return !errors.name && !errors.email
}

/** save */
const onSave = async () => {
  saved.value = false
  if (!validate()) return
  loading.value = true
  try {
    const payload: any = {
      full_name: form.name,
      email: form.email,
      phone: form.phone,
      title: form.title,
      bio: form.bio,
      gender: form.gender || undefined,
    }
    if (preview.value) {
      payload.avatar_url = preview.value
    }
    // updateProfile sẽ tự động cập nhật auth.user.avatar và persist
    const updated = await auth.updateProfile(payload)
    // Đảm bảo avatar được cập nhật trong original và form từ store
    const updatedAvatar = updated?.avatar || updated?.avatar_url || auth.user?.avatar || preview.value || form.avatar
    Object.assign(original, { ...form, avatar: updatedAvatar })
    form.avatar = updatedAvatar
    // Clear preview sau khi lưu thành công
    preview.value = null
    saved.value = true
    showToast('Cập nhật hồ sơ thành công!', 'success')
    setTimeout(() => (saved.value = false), 2000)
  } catch (e: any) {
    console.error('Profile update error:', e)
    // Kiểm tra xem có phải lỗi network/timeout không, nhưng backend đã lưu thành công
    // Nếu có response và status code là 200, coi như thành công
    if (e?.response?.status === 200 || e?.response?.status === 201) {
      const updatedAvatar = auth.user?.avatar || preview.value || form.avatar
      Object.assign(original, { ...form, avatar: updatedAvatar })
      form.avatar = updatedAvatar
      preview.value = null
      saved.value = true
      setTimeout(() => (saved.value = false), 2000)
    } else {
      // Hiển thị lỗi thực sự
      const errorMsg = e?.response?.data?.detail || e?.message || 'Cập nhật thất bại. Thử lại sau.'
      showToast(errorMsg, 'error')
    }
  } finally {
    loading.value = false
  }
}

/** reset */
const resetForm = () => {
  Object.assign(form, original)
  resetFile()
  Object.keys(errors).forEach((k) => (errors[k] = ''))
}

/** sync when user changes */
watch(user, (u) => {
  if (!u) return
  Object.assign(original, {
    name: u.name ?? '',
    email: u.email ?? '',
    phone: u.phone ?? '',
    title: (u as any)?.title ?? '',
    bio: (u as any)?.bio ?? '',
    gender: (u as any)?.gender ?? '',
    avatar: u.avatar ?? '',
  })
  resetForm()
})
</script>

<style scoped></style>
