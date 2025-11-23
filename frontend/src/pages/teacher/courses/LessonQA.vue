<template>
  <div class="mx-auto max-w-5xl p-6">
    <div class="mb-6 flex items-center justify-between gap-3">
      <div>
        <p class="text-xs font-semibold uppercase tracking-[0.2em] text-slate-700">Hỏi đáp bài học</p>
        <h1 class="text-2xl font-bold text-slate-900">Bài học: {{ lessonTitle || 'Chọn bài học' }}</h1>
        <p class="text-sm text-slate-500">Trả lời thắc mắc của học sinh, phản hồi sẽ gửi thông báo ngay.</p>
      </div>
    </div>

    <!-- Selector -->
    <div class="mb-4 flex flex-col gap-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:flex-row sm:items-center">
      <div class="flex-1">
        <label class="text-sm font-semibold text-slate-700">Chọn khoá học</label>
        <select
          v-model="selectedCourseId"
          @change="onSelectCourse"
          class="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:border-slate-500 focus:outline-none focus:ring-2 focus:ring-slate-200"
        >
          <option value="">— Chọn khoá —</option>
          <option v-for="c in courses" :key="c.id" :value="c.id">
            {{ c.title }}
          </option>
        </select>
      </div>
      <div class="flex-1">
        <label class="text-sm font-semibold text-slate-700">Chọn bài học</label>
        <select
          v-model="selectedLessonId"
          class="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:border-slate-500 focus:outline-none focus:ring-2 focus:ring-slate-200"
        >
          <option value="">— Chọn bài học —</option>
          <option v-for="l in lessons" :key="l.id" :value="l.id">
            {{ l.title }}
          </option>
        </select>
      </div>
    </div>

    <div v-if="lessonVideoSrc" class="mb-4 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      <video
        v-if="lessonVideoSrc && !(lessonVideoSrc.includes('youtube.com') || lessonVideoSrc.includes('youtu.be'))"
        :key="lessonVideoSrc"
        class="w-full"
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
      <div class="p-4">
        <h3 class="text-lg font-semibold text-slate-900">{{ lessonTitle }}</h3>
        <p class="text-sm text-slate-500">Xem nhanh nội dung bài học trước khi trả lời.</p>
      </div>
    </div>

    <div v-if="loading" class="space-y-3">
      <div v-for="i in 3" :key="i" class="h-28 rounded-2xl bg-slate-100 animate-pulse"></div>
    </div>

    <div v-else class="space-y-4">
      <div v-if="questions.length === 0" class="rounded-xl border border-slate-200 bg-white p-5 text-sm text-slate-600">
        Chưa có bình luận nào cho bài học này.
      </div>

      <div
        v-for="q in questions"
        :key="q.id"
        class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"
      >
        <div class="flex items-start gap-3">
          <div class="flex h-10 w-10 items-center justify-center rounded-full bg-slate-100 text-sm font-bold text-slate-700">
            <img
              v-if="q.avatar"
              :src="q.avatar"
              alt="avatar"
              class="h-10 w-10 rounded-full object-cover"
            />
            <span v-else>{{ q.student?.slice(0, 2)?.toUpperCase() || 'HS' }}</span>
          </div>
          <div class="flex-1">
            <div class="flex items-center justify-between">
              <p class="font-semibold text-slate-900">{{ q.student || 'Học sinh' }}</p>
              <span class="text-xs text-slate-400">{{ formatDateTimeShort(q.created_at) }}</span>
            </div>
            <p class="mt-1 text-sm text-slate-800 whitespace-pre-line">{{ q.content }}</p>

            <div class="mt-3 space-y-3">
              <div
                v-for="rep in q.replies"
                :key="rep.id"
                class="rounded-lg border border-slate-100 bg-slate-50 p-2"
              >
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2">
                    <img
                      v-if="rep.avatar"
                      :src="rep.avatar"
                      alt="avatar"
                      class="h-6 w-6 rounded-full object-cover"
                    />
                    <span class="text-xs font-semibold" :class="rep.is_teacher ? 'text-blue-700' : 'text-slate-700'">
                      {{ rep.is_teacher ? 'Giáo viên' : rep.user || 'Học sinh' }}
                    </span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="text-xs text-slate-400">{{ formatDateTimeShort(rep.created_at) }}</span>
                    <div v-if="rep.is_owner" class="relative">
                      <button
                        class="rounded-full border px-2 py-1 text-xs font-semibold text-slate-500 hover:bg-slate-100"
                        @click="toggleMenu(rep.id)"
                      >
                        •••
                      </button>
                      <div
                        v-if="menus[rep.id]"
                        class="absolute right-0 top-6 min-w-[120px] rounded-lg border border-slate-200 bg-white shadow-lg"
                      >
                        <button class="block w-full px-3 py-2 text-left text-sm hover:bg-slate-50" @click="startEdit(rep)">Sửa</button>
                        <button class="block w-full px-3 py-2 text-left text-sm text-rose-600 hover:bg-slate-50" @click="deleteReply(rep.id)">Xóa</button>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-if="editing.id === rep.id" class="space-y-2">
                  <textarea
                    v-model="editing.draft"
                    rows="2"
                    class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-100"
                  ></textarea>
                  <div class="flex gap-2">
                    <button class="rounded-lg bg-orange-500 px-3 py-1.5 text-sm font-semibold text-white hover:bg-orange-600" @click="saveEdit(rep.id)">
                      Lưu
                    </button>
                    <button class="rounded-lg border px-3 py-1.5 text-sm font-semibold text-slate-600 hover:bg-slate-50" @click="cancelEdit">
                      Hủy
                    </button>
                  </div>
                </div>
                <p v-else class="text-sm text-slate-800 whitespace-pre-line">{{ rep.content }}</p>
              </div>
            </div>

            <div class="mt-3 rounded-xl border border-slate-200 bg-slate-50 p-3">
              <textarea
                v-model="replyDrafts[q.id]"
                rows="2"
                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-100"
                placeholder="Phản hồi cho học sinh..."
              ></textarea>
              <div class="mt-2 flex justify-end">
                <button
                  class="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-300"
                  :disabled="replying[q.id] || !(replyDrafts[q.id]?.trim())"
                  @click="sendReply(q.id)"
                >
                  <span v-if="replying[q.id]" class="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white inline-block"></span>
                  <span v-else>Gửi phản hồi</span>
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
import { onMounted, reactive, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/config/axios'
import { showToast } from '@/utils/toast'
import { courseService, type CourseDetail } from '@/services/course.service'
import { contentService } from '@/services/content.service'

const route = useRoute()
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

function formatDateTimeShort(iso?: string) {
  if (!iso) return ''
  try {
    const d = new Date(iso)
    return d.toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit' }) + ' ' + d.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
  } catch {
    return iso
  }
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
.rounded-full.border.px-2.py-1 {
  line-height: 1;
}
</style>
