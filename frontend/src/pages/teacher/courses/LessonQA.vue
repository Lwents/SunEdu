<template>
  <div class="lesson-qa mx-auto max-w-6xl p-6" :class="isDark ? 'lesson-qa--dark' : ''">
    <!-- Header -->
    <div class="mb-6 rounded-2xl border border-slate-200 bg-gradient-to-br from-white to-slate-50 p-6 shadow-sm">
      <div class="flex items-start gap-4">
        <div class="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-500 to-blue-600 shadow-lg">
          <svg class="h-8 w-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        </div>
        <div class="flex-1">
          <p class="text-xs font-bold uppercase tracking-wider text-blue-600">HỎI ĐÁP BÀI HỌC</p>
          <h1 class="mt-1 text-2xl font-bold text-slate-900">{{ lessonTitle || 'Chọn bài học' }}</h1>
          <p class="mt-2 flex items-center gap-2 text-sm text-slate-600">
            <svg class="h-4 w-4 text-green-500" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
            Trả lời thắc mắc của học sinh, phản hồi sẽ gửi thông báo ngay.
          </p>
        </div>
      </div>
    </div>

    <!-- Selector -->
    <div class="mb-6 flex flex-col gap-4 rounded-2xl border-2 border-slate-200 bg-white p-5 shadow-sm sm:flex-row sm:items-end">
      <div class="flex-1">
        <label class="mb-2 block text-sm font-bold text-slate-700">
          <span class="flex items-center gap-2">
            <svg class="h-4 w-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
            Chọn khoá học
          </span>
        </label>
        <select
          v-model="selectedCourseId"
          @change="onSelectCourse"
          class="w-full rounded-xl border-2 border-slate-200 bg-slate-50 px-4 py-3 text-sm font-medium text-slate-900 transition-all focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-4 focus:ring-blue-100"
        >
          <option value="">— Chọn khoá —</option>
          <option v-for="c in courses" :key="c.id" :value="c.id">
            {{ c.title }}
          </option>
        </select>
      </div>
      <div class="flex-1">
        <label class="mb-2 block text-sm font-bold text-slate-700">
          <span class="flex items-center gap-2">
            <svg class="h-4 w-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Chọn bài học
          </span>
        </label>
        <select
          v-model="selectedLessonId"
          class="w-full rounded-xl border-2 border-slate-200 bg-slate-50 px-4 py-3 text-sm font-medium text-slate-900 transition-all focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-4 focus:ring-blue-100"
        >
          <option value="">— Chọn bài học —</option>
          <option v-for="l in lessons" :key="l.id" :value="l.id">
            {{ l.title }}
          </option>
        </select>
      </div>
    </div>

    <!-- Lesson Video Preview -->
    <div v-if="lessonVideoSrc" class="mb-6 overflow-hidden rounded-2xl border-2 border-slate-200 bg-white shadow-lg">
      <div class="relative">
      <video
        v-if="lessonVideoSrc && !(lessonVideoSrc.includes('youtube.com') || lessonVideoSrc.includes('youtu.be'))"
        :key="lessonVideoSrc"
          class="w-full bg-black"
        controls
        controlsList="nodownload"
        preload="metadata"
        playsinline
      >
        <source :src="lessonVideoSrc" type="video/mp4" />
        Trình duyệt không hỗ trợ phát video.
      </video>
      <iframe
        v-else
        :src="lessonVideoSrc"
        class="aspect-video w-full"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
      ></iframe>
      </div>
      <div class="border-t border-slate-200 bg-gradient-to-br from-slate-50 to-white p-5">
        <div class="flex items-center gap-2">
          <svg class="h-5 w-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
          <h3 class="text-lg font-bold text-slate-900">{{ lessonTitle }}</h3>
        </div>
        <p class="mt-1 text-sm text-slate-600">Xem nhanh nội dung bài học trước khi trả lời.</p>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="space-y-4">
      <div v-for="i in 3" :key="i" class="h-40 rounded-2xl bg-gradient-to-br from-slate-100 to-slate-200 animate-pulse"></div>
    </div>

    <!-- Empty State -->
    <div v-else-if="questions.length === 0" class="flex flex-col items-center justify-center rounded-2xl border-2 border-dashed border-slate-200 bg-gradient-to-br from-slate-50 to-white p-12">
      <div class="flex h-20 w-20 items-center justify-center rounded-full bg-slate-100">
        <svg class="h-10 w-10 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
      </div>
      <p class="mt-4 text-lg font-semibold text-slate-700">Chưa có câu hỏi nào</p>
      <p class="mt-1 text-sm text-slate-500">Học sinh sẽ gửi câu hỏi ở đây khi có thắc mắc về bài học.</p>
      </div>

    <!-- Questions List -->
    <div v-else class="space-y-5">
      <div
        v-for="q in questions"
        :key="q.id"
        class="group rounded-2xl border-2 border-slate-200 bg-white p-6 shadow-sm transition-all hover:border-blue-300 hover:shadow-md"
      >
        <div class="flex items-start gap-4">
          <!-- Student Avatar -->
          <div class="relative flex-shrink-0">
            <div class="relative flex h-14 w-14 items-center justify-center overflow-hidden rounded-full bg-gradient-to-br from-green-200 to-green-300 text-base font-bold text-green-700 shadow-md ring-2 ring-white transition-all group-hover:ring-green-200">
              <img
                v-if="!avatarErrors[`q-${q.id}`]"
                :src="avatarUrlForQuestion(q)"
                :alt="q.student || 'Học sinh'"
                class="absolute inset-0 h-full w-full object-cover"
                @error="handleAvatarError(`q-${q.id}`)"
                @load="handleAvatarLoad(`q-${q.id}`)"
              />
              <span 
                v-if="avatarErrors[`q-${q.id}`]"
                class="text-base"
              >
                {{ getInitials(q.student) || 'HS' }}
              </span>
            </div>
            <div class="absolute -bottom-1 -right-1 flex h-6 w-6 items-center justify-center rounded-full bg-green-500 ring-2 ring-white shadow-md">
              <svg class="h-3.5 w-3.5 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                <path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clip-rule="evenodd" />
              </svg>
            </div>
          </div>
          
          <!-- Question Content -->
          <div class="flex-1 min-w-0">
            <div class="flex items-start justify-between gap-3">
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2">
                  <p class="font-bold text-slate-900">{{ q.student || 'Học sinh' }}</p>
                  <span class="rounded-full bg-green-100 px-2 py-0.5 text-xs font-semibold text-green-700">Học sinh</span>
                </div>
                <p class="mt-0.5 text-xs text-slate-500">{{ formatDateTimeShort(q.created_at) }}</p>
              </div>
            </div>
            <div class="mt-3 rounded-xl bg-slate-50 p-4">
              <p class="text-sm leading-relaxed text-slate-800 whitespace-pre-line">{{ q.content }}</p>
            </div>

            <!-- Replies Section -->
            <div v-if="q.replies && q.replies.length > 0" class="mt-4 space-y-3 border-t border-slate-200 pt-4">
              <div
                v-for="rep in q.replies"
                :key="rep.id"
                class="group/reply rounded-xl border border-slate-100 bg-gradient-to-br from-blue-50 to-white p-4 shadow-sm transition-all hover:border-blue-200 hover:shadow-md"
              >
                <div class="flex items-start gap-3">
                  <!-- Reply Avatar -->
                  <div class="relative flex-shrink-0">
                    <div 
                      class="relative flex h-10 w-10 items-center justify-center overflow-hidden rounded-full text-xs font-bold shadow-sm ring-2 ring-white transition-all"
                      :class="rep.is_teacher 
                        ? 'bg-gradient-to-br from-blue-500 to-blue-600 text-white' 
                        : (isAIReply(rep) ? 'bg-gradient-to-br from-purple-500 to-indigo-500 text-white' : 'bg-gradient-to-br from-slate-200 to-slate-300 text-slate-700')"
                    >
                      <!-- AI icon -->
                      <span v-if="isAIReply(rep)" class="text-sm">🤖</span>
                      <!-- Avatar image -->
                      <img
                        v-else-if="!avatarErrors[`r-${rep.id}`]"
                        :src="avatarUrlForReply(rep)"
                        :alt="rep.is_teacher ? 'Giáo viên' : (rep.user || 'Học sinh')"
                        class="absolute inset-0 h-full w-full object-cover"
                        @error="handleAvatarError(`r-${rep.id}`)"
                        @load="handleAvatarLoad(`r-${rep.id}`)"
                      />
                      <!-- Fallback initials -->
                      <span 
                        v-else
                        class="text-xs font-bold"
                      >
                        {{ rep.is_teacher ? 'GV' : getInitials(rep.user) || 'HS' }}
                      </span>
                    </div>
                    <div v-if="isAIReply(rep)" class="absolute -bottom-0.5 -right-0.5 flex h-5 w-5 items-center justify-center rounded-full bg-gradient-to-r from-purple-500 to-indigo-500 ring-2 ring-white shadow-sm">
                      <svg class="h-3 w-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                      </svg>
                    </div>
                    <div v-else-if="rep.is_teacher" class="absolute -bottom-0.5 -right-0.5 flex h-5 w-5 items-center justify-center rounded-full bg-blue-500 ring-2 ring-white shadow-sm">
                      <svg class="h-3 w-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                      </svg>
                    </div>
                  </div>
                  
                  <!-- Reply Content -->
                  <div class="flex-1 min-w-0">
                    <div class="flex items-center justify-between gap-2">
                      <div class="flex items-center gap-2">
                        <span class="text-sm font-bold" :class="rep.is_teacher ? 'text-blue-700' : (isAIReply(rep) ? 'text-purple-700' : 'text-slate-700')">
                          {{ rep.is_teacher ? '👨‍🏫 Giáo viên' : (isAIReply(rep) ? '🤖 Trợ lý AI' : rep.user || 'Học sinh') }}
                        </span>
                        <span v-if="isAIReply(rep)" class="rounded-full bg-gradient-to-r from-purple-100 to-indigo-100 px-2 py-0.5 text-xs font-semibold text-purple-700">AI</span>
                        <span v-else-if="rep.is_owner" class="rounded-full bg-orange-100 px-2 py-0.5 text-xs font-semibold text-orange-700">Bạn</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="text-xs text-slate-400">{{ formatDateTimeShort(rep.created_at) }}</span>
                    <div v-if="rep.is_owner" class="relative">
                      <button
                            class="flex h-7 w-7 items-center justify-center rounded-lg text-slate-400 transition-all hover:bg-slate-100 hover:text-slate-600"
                        @click="toggleMenu(rep.id)"
                      >
                            <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                              <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
                            </svg>
                      </button>
                          <transition name="fade">
                      <div
                        v-if="menus[rep.id]"
                              class="absolute right-0 top-full z-10 mt-2 min-w-[140px] rounded-xl border border-slate-200 bg-white py-2 shadow-xl"
                              @click.stop
                      >
                              <button class="w-full px-4 py-2 text-left text-sm text-slate-700 hover:bg-slate-50" @click="startEdit(rep); menus[rep.id]=false">✏️ Sửa</button>
                              <button class="w-full px-4 py-2 text-left text-sm text-rose-600 hover:bg-rose-50" @click="deleteReply(rep.id); menus[rep.id]=false">🗑️ Xóa</button>
                            </div>
                          </transition>
                        </div>
                      </div>
                    </div>
                    
                    <!-- Edit Mode -->
                    <div v-if="editing.id === rep.id" class="mt-3 space-y-2">
                  <textarea
                    v-model="editing.draft"
                        rows="3"
                        class="w-full rounded-xl border-2 border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 transition-all focus:border-blue-400 focus:outline-none focus:ring-4 focus:ring-blue-100"
                  ></textarea>
                  <div class="flex gap-2">
                        <button 
                          class="rounded-xl bg-gradient-to-r from-blue-500 to-blue-600 px-4 py-2 text-sm font-bold text-white shadow-md transition-all hover:from-blue-600 hover:to-blue-700 hover:shadow-lg active:scale-95" 
                          @click="saveEdit(rep.id)"
                        >
                      Lưu
                    </button>
                        <button 
                          class="rounded-xl border-2 border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition-all hover:bg-slate-50 active:scale-95" 
                          @click="cancelEdit"
                        >
                      Hủy
                    </button>
                      </div>
                    </div>
                    
                    <!-- Reply Text -->
                    <p v-else class="mt-2 text-sm leading-relaxed text-slate-800 whitespace-pre-line">{{ rep.content }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Reply Input Area -->
            <div class="mt-4 rounded-xl border-2 border-dashed border-blue-200 bg-gradient-to-br from-blue-50 to-white p-4 transition-all hover:border-blue-300">
              <div class="mb-2 flex items-center gap-2">
                <svg class="h-4 w-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                <span class="text-sm font-semibold text-blue-700">Phản hồi cho học sinh</span>
              </div>
              <textarea
                v-model="replyDrafts[q.id]"
                rows="3"
                class="w-full rounded-xl border-2 border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 placeholder:text-slate-400 transition-all focus:border-blue-400 focus:outline-none focus:ring-4 focus:ring-blue-100"
                placeholder="Nhập phản hồi của bạn cho học sinh..."
              ></textarea>
              <div class="mt-3 flex items-center justify-between">
                <span v-if="replyDrafts[q.id]?.length" class="text-xs text-slate-500">{{ replyDrafts[q.id].length }} ký tự</span>
                <span v-else></span>
                <button
                  class="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-blue-500 to-blue-600 px-6 py-2.5 text-sm font-bold text-white shadow-lg shadow-blue-200 transition-all hover:from-blue-600 hover:to-blue-700 hover:shadow-xl hover:-translate-y-0.5 active:translate-y-0 disabled:cursor-not-allowed disabled:from-slate-300 disabled:to-slate-400 disabled:shadow-none disabled:hover:translate-y-0"
                  :disabled="replying[q.id] || !(replyDrafts[q.id]?.trim())"
                  @click="sendReply(q.id)"
                >
                  <span v-if="replying[q.id]" class="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white"></span>
                  <span v-else>
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                    </svg>
                  </span>
                  Gửi phản hồi
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/config/axios'
import { showToast } from '@/utils/toast'
import { courseService, type CourseDetail } from '@/services/course.service'
import { contentService } from '@/services/content.service'
import { getAvatarSrc } from '@/utils/avatar'
import { useThemeStore } from '@/store/theme.store'

const route = useRoute()
const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)
const initialLessonId = (route.params as any).lessonId || route.query.lessonId || ''
const questions = ref<any[]>([])
const loading = ref(false)
const replyDrafts = reactive<Record<string, string>>({})
const replying = reactive<Record<string, boolean>>({})
const menus = reactive<Record<string, boolean>>({})
const editing = reactive<{ id: string | null; draft: string }>({ id: null, draft: '' })
const lessonTitle = ref('')
const courses = ref<any[]>([])
const lessons = ref<{ id: string; title: string }[]>([])
const selectedCourseId = ref<string>('')
const selectedLessonId = ref<string>(String(initialLessonId || ''))
const lessonDetail = ref<any>(null)
const lessonVideoSrc = ref<string>('')
const avatarErrors = reactive<Record<string, boolean>>({})

function formatDateTimeShort(iso?: string) {
  if (!iso) return ''
  try {
    const d = new Date(iso)
    return d.toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit' }) + ' ' + d.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
  } catch {
    return iso
  }
}

function getInitials(name?: string | null): string {
  if (!name || !name.trim()) return ''
  const parts = name.trim().split(/\s+/)
  if (parts.length === 1) {
    return name.slice(0, 2).toUpperCase()
  }
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
}

function handleAvatarError(key: string) {
  avatarErrors[key] = true
}

function handleAvatarLoad(key: string) {
  if (avatarErrors[key]) {
    delete avatarErrors[key]
  }
}

function normalizeAvatar(input: any) {
  if (!input) return ''
  const str = String(input).trim()
  if (!str) return ''
  const lower = str.toLowerCase()
  if (lower === 'avatar' || lower === 'null' || lower === 'undefined' || lower === 'none') return ''
  return str
}

function avatarUrlForQuestion(q: any) {
  const source =
    normalizeAvatar(q?.avatar) ||
    normalizeAvatar(q?.avatar_url) ||
    normalizeAvatar(q?.student_avatar)
  return getAvatarSrc(source, (q?.gender as any) || 'male', 'student')
}

function avatarUrlForReply(rep: any) {
  if (isAIReply(rep)) return ''
  const source =
    normalizeAvatar(rep?.avatar) ||
    normalizeAvatar(rep?.avatar_url) ||
    normalizeAvatar(rep?.user_avatar)
  return getAvatarSrc(source, (rep?.gender as any) || 'male', rep?.is_teacher ? 'instructor' : 'student')
}

function isAIReply(rep: any) {
  const name = (rep?.user || '').toString().trim()
  return name === 'AI_Assistant'
}

async function loadQuestions() {
  if (!selectedLessonId.value) return
  loading.value = true
  try {
    const { data } = await api.get('/teacher/lesson-questions/', {
      params: { lesson_id: selectedLessonId.value },
    })
    questions.value = data?.items || []
    if (questions.value.length) {
      lessonTitle.value = questions.value[0].lesson_title || lessonTitle.value
    }
  } catch (e: any) {
    showToast(e?.message || 'Không tải được hỏi đáp', 'error')
  } finally {
    loading.value = false
  }
}

async function sendReply(questionId: string) {
  const content = (replyDrafts[questionId] || '').trim()
  if (!content) return
  replying[questionId] = true
  try {
    await api.post(`/teacher/lesson-questions/${questionId}/reply/`, { content })
    replyDrafts[questionId] = ''
    showToast('Đã gửi phản hồi', 'success')
    await loadQuestions()
  } catch (e: any) {
    showToast(e?.response?.data?.detail || 'Không gửi được phản hồi', 'error')
  } finally {
    replying[questionId] = false
  }
}

function toggleMenu(id: string) {
  menus[id] = !menus[id]
}

function startEdit(rep: any) {
  editing.id = rep.id
  editing.draft = rep.content
}
function cancelEdit() {
  editing.id = null
  editing.draft = ''
}
async function saveEdit(replyId: string) {
  if (!editing.draft.trim()) return
  try {
    await api.patch(`/teacher/lesson-question-replies/${replyId}/`, { content: editing.draft })
    showToast('Đã cập nhật phản hồi', 'success')
    cancelEdit()
    await loadQuestions()
  } catch (e: any) {
    showToast(e?.response?.data?.detail || 'Không sửa được phản hồi', 'error')
  }
}

async function deleteReply(replyId: string) {
  try {
    await api.delete(`/teacher/lesson-question-replies/${replyId}/`)
    showToast('Đã xóa phản hồi', 'success')
    await loadQuestions()
  } catch (e: any) {
    showToast(e?.response?.data?.detail || 'Không xóa được phản hồi', 'error')
  }
}

onMounted(loadQuestions)
watch(selectedLessonId, () => {
  loadQuestions()
  loadLessonDetail()
})

async function loadCourses() {
  try {
    const { items } = await courseService.list({ page: 1, pageSize: 50, status: 'published' })
    courses.value = items || []
  } catch (e) {
    console.error(e)
  }
}

async function onSelectCourse() {
  lessons.value = []
  selectedLessonId.value = ''
  lessonTitle.value = ''
  lessonDetail.value = null
  lessonVideoSrc.value = ''
  if (!selectedCourseId.value) return
  try {
    const modules = await contentService.listModules(selectedCourseId.value)
    const allLessons: { id: string; title: string }[] = []
    for (const mod of modules) {
      const modLessons = await contentService.listLessons(mod.id)
      modLessons.forEach((l: any) => {
        allLessons.push({
          id: String(l.id),
          title: `${mod.title}: ${l.title}`,
        })
      })
    }
    lessons.value = allLessons
    if (!lessons.value.length) {
      showToast('Khoá chưa có bài học', 'warning')
    }
  } catch (e: any) {
    showToast(e?.message || 'Không tải được bài học', 'error')
  }
}

onMounted(async () => {
  await loadCourses()
  if (initialLessonId) {
    selectedLessonId.value = String(initialLessonId)
    await loadQuestions()
    await loadLessonDetail()
  }
})

async function loadLessonDetail() {
  lessonDetail.value = null
  lessonVideoSrc.value = ''
  if (!selectedLessonId.value) return
  try {
    const { data } = await api.get(`/content/lessons/${selectedLessonId.value}/`)
    lessonDetail.value = data
    lessonTitle.value = data?.title || lessonTitle.value
    lessonVideoSrc.value = resolveVideoSrc(data)
  } catch (e: any) {
    console.error(e)
  }
}

function resolveVideoSrc(detail: any): string {
  const url = detail?.video_url
  const file = detail?.video_file
  if (url) {
    if (url.includes('youtube.com') || url.includes('youtu.be')) {
      return getYouTubeEmbedUrl(url)
    }
    return url
  }
  if (file) {
    // Nếu đã là URL tuyệt đối thì dùng luôn
    if (/^https?:\/\//i.test(file)) return file
    const base = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/+$/, '')
    const safe = encodeURI(String(file).replace(/^\/+/, ''))
    return `${base}/api/media/stream/${safe}`
  }
  return ''
}

function getYouTubeEmbedUrl(url: string): string {
  if (!url) return ''
  let videoId = ''
  if (url.includes('watch?v=')) {
    videoId = url.split('v=')[1]?.split('&')[0] || ''
  } else if (url.includes('youtu.be/')) {
    videoId = url.split('youtu.be/')[1]?.split('?')[0] || ''
  } else if (url.includes('/embed/')) {
    videoId = url.split('/embed/')[1]?.split('?')[0] || ''
  }
  const params = new URLSearchParams({
    rel: '0',
    modestbranding: '1',
    enablejsapi: '1',
  })
  return videoId ? `https://www.youtube.com/embed/${videoId}?${params.toString()}` : url
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.lesson-qa--dark .from-white,
.lesson-qa--dark .from-slate-50,
.lesson-qa--dark .from-slate-100,
.lesson-qa--dark .from-blue-50 {
  --tw-gradient-from: rgba(15, 23, 42, 0.95) !important;
  --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to) !important;
}

.lesson-qa--dark .to-white,
.lesson-qa--dark .to-slate-50,
.lesson-qa--dark .to-slate-200,
.lesson-qa--dark .to-blue-50 {
  --tw-gradient-to: rgba(15, 23, 42, 0.75) !important;
}
</style>
