<template>
  <div class="student-shell" v-if="course">
    <div class="student-container max-w-6xl">
      <div
        class="mb-4 flex flex-col gap-2 text-sm font-semibold text-gray-600 dark:text-gray-400 sm:flex-row sm:items-center sm:justify-between"
      >
        <button
          type="button"
          class="inline-flex w-full items-center justify-center gap-2 rounded-2xl border border-slate-200 px-4 py-2 text-sm font-semibold text-gray-900 dark:text-gray-100 transition hover:bg-slate-50 sm:w-auto"
          @click="goBack"
        >
          ‹ Rời khỏi đây
        </button>
        <span class="text-center sm:text-right">{{ course.sections?.length || 0 }} chương</span>
      </div>

      <div class="grid gap-6 lg:grid-cols-[minmax(0,2fr)_minmax(320px,1fr)]">
        <div class="order-1 space-y-4">
          <!-- Locked Lesson Warning -->
          <div v-if="lessonLocked" class="rounded-2xl border border-amber-200 bg-amber-50 p-6 text-center">
            <svg class="mx-auto h-12 w-12 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
            <h3 class="mt-4 text-lg font-semibold text-amber-900">Bài học bị khóa</h3>
            <p class="mt-2 text-sm text-amber-700">{{ unlockReason || 'Bạn cần hoàn thành bài học trước đó' }}</p>
          </div>

          <!-- Introduction -->
          <div v-if="currentLessonDetail?.introduction && !lessonLocked" class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <h3 class="mb-3 text-lg font-semibold text-gray-900">Giới thiệu</h3>
            <div class="text-gray-700 whitespace-pre-line">{{ currentLessonDetail.introduction }}</div>
          </div>

          <!-- Video Player -->
          <div v-if="!lessonLocked" class="overflow-hidden rounded-3xl border border-slate-200 bg-slate-900/5 shadow-lg shadow-slate-200">
            <!-- Video từ YouTube -->
            <iframe
              v-if="lessonVideoUrl && isYouTubeUrl(lessonVideoUrl)"
              ref="youtubeIframeRef"
              :src="getYouTubeEmbedUrl(lessonVideoUrl)"
              class="aspect-video w-full rounded-3xl"
              frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen
              @load="onYouTubeIframeLoad"
            ></iframe>
            <!-- Video từ URL hoặc file -->
            <video
              v-else-if="lessonVideoUrl || lessonVideoFile"
              ref="videoRef"
              class="aspect-video w-full rounded-3xl bg-black object-contain"
              :src="lessonVideoSrc"
              controls
              playsinline
              @ended="onVideoEnded"
              @play="onVideoWatched"
            ></video>
            <!-- Fallback: Course video -->
            <template v-else>
              <iframe
                v-if="course.video_url && isYouTubeUrl(course.video_url)"
                ref="youtubeIframeRef"
                :src="getYouTubeEmbedUrl(course.video_url)"
                class="aspect-video w-full rounded-3xl"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
                @load="onYouTubeIframeLoad"
              ></iframe>
              <video
                v-else
                ref="videoRef"
                class="aspect-video w-full rounded-3xl bg-black object-contain"
                :src="currentSrc"
                controls
                playsinline
                @ended="onVideoEnded"
                @play="onVideoWatched"
              ></video>
            </template>
            <div class="space-y-1 px-6 py-5">
              <p class="student-section-title text-xs text-gray-600 dark:text-gray-400">
                {{ currentLesson ? 'Bài học hiện tại' : 'Video khóa học' }}
              </p>
              <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100">
                {{ currentLesson?.title || course.title }}
              </h2>
            </div>
          </div>

          <!-- Exercise Section -->
          <div v-if="currentLessonExercises.length > 0 && !lessonLocked" class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div class="mb-4 flex items-center justify-between">
              <h3 class="text-lg font-semibold text-gray-900">Bài tập</h3>
              <span v-if="lessonProgress?.exercise_completed" class="rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-700">
                Đã hoàn thành
              </span>
            </div>
            <div v-for="(exercise, idx) in currentLessonExercises" :key="exercise.id" class="mb-4 last:mb-0">
              <div class="rounded-lg border border-gray-200 bg-gray-50 p-4">
                <h4 class="mb-2 font-semibold text-gray-900">{{ exercise.title }}</h4>
                <button
                  type="button"
                  class="rounded-lg bg-cyan-600 px-4 py-2 text-sm font-semibold text-white hover:bg-cyan-700"
                  @click="openExercise(exercise.id)"
                >
                  {{ lessonProgress?.exercise_completed ? 'Xem lại bài tập' : 'Làm bài tập' }}
                </button>
              </div>
            </div>
            <p v-if="currentLessonDetail?.requires_exercise_completion && !lessonProgress?.exercise_completed" class="mt-3 text-sm text-amber-600">
              ⚠️ Bạn cần hoàn thành bài tập này để tiếp tục bài học tiếp theo
            </p>
          </div>
        </div>

        <aside class="order-2 rounded-3xl border border-slate-200 bg-white/95 p-5 shadow-sm shadow-slate-100">
          <div class="flex items-center gap-4">
            <div class="relative flex h-20 w-20 items-center justify-center rounded-full bg-slate-100">
              <svg viewBox="0 0 36 36" class="h-16 w-16 text-brand-200">
                <path
                  class="text-slate-200"
                  stroke="currentColor"
                  stroke-width="3"
                  fill="none"
                  d="M18 2.0845 a 15.9155 15.9155 0 1 1 0 31.831 a 15.9155 15.9155 0 1 1 0 -31.831"
                />
                <path
                  class="text-cyan-500"
                  stroke="currentColor"
                  stroke-width="3"
                  stroke-linecap="round"
                  fill="none"
                  :style="{ strokeDasharray: dash + ', 100' }"
                  d="M18 2.0845 a 15.9155 15.9155 0 1 1 0 31.831 a 15.9155 15.9155 0 1 1 0 -31.831"
                />
              </svg>
              <span class="absolute text-lg font-black text-gray-900 dark:text-gray-100">{{ progressPct }}%</span>
            </div>
            <div>
              <p class="text-sm font-semibold uppercase tracking-[0.3em] text-gray-600 dark:text-gray-400">
                Nội dung khóa học
              </p>
              <p class="text-base font-bold text-gray-900 dark:text-gray-100">{{ doneCount }}/{{ totalCount }} bài học</p>
            </div>
          </div>

          <div ref="outlineRef" class="mt-5 space-y-4">
            <div
              v-for="(sec, si) in uiSections"
              :key="sec.id"
              class="rounded-2xl border border-slate-100 bg-white shadow-sm shadow-slate-100"
            >
              <button
                type="button"
                class="flex w-full items-center justify-between gap-3 px-4 py-3 text-left font-semibold text-gray-900 dark:text-gray-100"
                @click="toggle(si)"
              >
                <span class="flex-1 text-sm">{{ si + 1 }}. {{ sec.title }}</span>
                <span class="text-xs text-gray-600 dark:text-gray-400">{{ sec.items.length }}</span>
                <svg
                  class="h-4 w-4 text-gray-600 dark:text-gray-400 transition"
                  :class="{ 'rotate-180': openIndex === si }"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path d="M6 9l6 6 6-6" />
                </svg>
              </button>
              <transition
                enter-active-class="transition-all duration-200 ease-out"
                leave-active-class="transition-all duration-150 ease-in"
                enter-from-class="max-h-0 opacity-0"
                enter-to-class="max-h-[600px] opacity-100"
                leave-from-class="max-h-[600px] opacity-100"
                leave-to-class="max-h-0 opacity-0"
              >
                <ul v-show="openIndex === si" class="divide-y divide-slate-100 overflow-hidden">
                  <li
                    v-for="(it, li) in sec.items"
                    :key="it.id"
                    :class="[
                      'flex cursor-pointer items-center justify-between gap-3 px-4 py-3 text-sm transition',
                      String(it.id) === String(currentLesson?.id)
                        ? 'bg-cyan-50 dark:bg-cyan-900/20 text-cyan-700 dark:text-cyan-300'
                        : 'bg-white text-gray-900 dark:text-gray-100 hover:bg-slate-50',
                      it.done ? 'font-semibold' : '',
                    ]"
                    @click="goToLesson(si, li)"
                  >
                    <div class="flex items-center gap-2">
                      <span class="text-xs font-semibold text-gray-600 dark:text-gray-400">{{ li + 1 }}</span>
                      <span>{{ it.title }}</span>
                    </div>
                    <div class="flex items-center gap-3 text-xs text-gray-600 dark:text-gray-400">
                      <span>{{ formatDuration(it.durationMinutes) }}</span>
                      <svg
                        v-if="it.done"
                        class="h-4 w-4 text-cyan-500"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                      >
                        <path d="M20 6L9 17l-5-5" />
                      </svg>
                    </div>
                  </li>
                </ul>
              </transition>
            </div>
          </div>
        </aside>

        <div class="order-3 flex flex-col gap-3 rounded-3xl border border-slate-200 bg-white px-4 py-3 shadow-sm shadow-slate-100 sm:flex-row sm:items-center sm:justify-between">
          <button
            type="button"
            class="inline-flex items-center justify-center rounded-2xl border border-slate-200 px-4 py-2 text-sm font-semibold text-gray-900 dark:text-gray-100 transition hover:bg-slate-50 disabled:opacity-50"
            :disabled="!prevLesson"
            @click="goPrev"
          >
            ‹ Bài trước
          </button>
          <div class="text-center text-xs font-semibold uppercase tracking-[0.3em] text-gray-600 dark:text-gray-400">
            {{ doneCount }}/{{ totalCount }} bài hoàn thành
          </div>
          <button
            type="button"
            class="inline-flex items-center justify-center rounded-2xl border border-transparent bg-gradient-to-r from-cyan-500 to-cyan-600 px-4 py-2 text-sm font-semibold text-white shadow-lg shadow-cyan-500/40 transition hover:from-cyan-600 hover:to-cyan-700 hover:shadow-xl hover:-translate-y-0.5 disabled:opacity-50 disabled:hover:translate-y-0"
            :disabled="!nextLesson"
            @click="goNext"
          >
            Bài tiếp theo ›
          </button>
        </div>
      </div>
    </div>
  </div>
  <div v-else class="grid min-h-screen place-items-center text-gray-600 dark:text-gray-400">Đang tải…</div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watchEffect, watch, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { courseService, type CourseDetail } from '@/services/course.service'
import { contentService } from '@/services/content.service'
import api from '@/config/axios'

type Lesson = CourseDetail['sections'][0]['lessons'][0];

const router = useRouter()
const route = useRoute()

const course = ref<CourseDetail | null>(null)
const videoRef = ref<HTMLVideoElement|null>(null)
const youtubeIframeRef = ref<HTMLIFrameElement|null>(null)
const youtubePlayer = ref<any>(null)
const doneSet = reactive(new Set<string>())
const openIndex = ref<number>(0)
const cur = ref<{ si: number; li: number }>({ si: 0, li: 0 })

// Lesson detail and progress
const currentLessonDetail = ref<any>(null)
const currentLessonExercises = ref<any[]>([])
const lessonProgress = ref<any>(null)
const lessonLocked = ref(false)
const unlockReason = ref<string>('')

function normalizeRouteParam(param: any): string | number | undefined {
  if (Array.isArray(param)) return param[0]
  return param as string | number | undefined
}

const courseId = computed(() => {
  const raw = normalizeRouteParam(route.params.id)
  return raw != null ? String(raw) : ''
})

async function load() {
  const id = courseId.value
  const lessonParam = normalizeRouteParam(route.params.lessonId) as any
  if (!id) {
    console.warn('Missing course id in route params')
    return
  }
  
  // Sử dụng student API endpoint để lấy isEnrolled
  try {
    const { data } = await api.get(`/student/courses/${id}/`)
    course.value = data
    
    // Cập nhật doneSet từ course data (sync với backend progress)
    if (data && data.sections) {
      doneSet.clear() // Clear trước để tránh duplicate
      doneSetTrigger.value++ // Force reactivity
      data.sections.forEach((section: any) => {
        if (section.lessons && Array.isArray(section.lessons)) {
          section.lessons.forEach((lesson: any) => {
            // Check nhiều cách để đảm bảo nhận được completed status
            const isCompleted = lesson.completed === true || 
                               lesson.completed === 'true' || 
                               lesson.completed === 1 ||
                               lesson.completed === '1' ||
                               lesson.videoWatched === true ||
                               lesson.videoWatched === 'true'
            
            if (isCompleted) {
              doneSet.add(String(lesson.id))
              console.log('Loaded completed lesson:', lesson.id, lesson.title)
            }
          })
        }
      })
      // Force reactivity sau khi load
      doneSetTrigger.value++
      console.log('Loaded progress from backend:', doneSet.size, 'lessons completed, total sections:', data.sections?.length || 0)
      
      // Rebuild UI sau khi load
      await nextTick()
      rebuildAndKeepCursor(lessonParam ?? null)
    } else {
      console.warn('No sections found in course data:', data)
    }
  } catch (e: any) {
    // Fallback to regular endpoint nếu student endpoint không có
    const d = await courseService.detail(id)
    course.value = d
  }
  
  // Kiểm tra enrollment - nếu chưa enroll thì redirect về course detail
  // Chỉ redirect nếu thực sự chưa enroll (không phải do API chưa trả về)
  if (course.value && (course.value as any).isEnrolled === false) {
    console.log('Course not enrolled, redirecting to detail page')
    router.push({ name: 'student-course-detail', params: { id } })
    return
  }
  
  // Nếu isEnrolled không có trong response, giả sử đã enroll (để tránh redirect loop)
  if (course.value && (course.value as any).isEnrolled === undefined) {
    console.log('isEnrolled not in response, assuming enrolled')
  }
  
  rebuildAndKeepCursor(lessonParam ?? null)
  if (lessonParam) openIndex.value = findById(lessonParam)?.si ?? 0
}

type UiLesson = { id: string|number; title: string; durationMinutes?: number; type: Lesson['type']; done?: boolean }
type UiSection = { id: string|number; title: string; items: UiLesson[] }
const uiSections = ref<UiSection[]>([])

function buildUiSections() {
  if (!course.value) { uiSections.value = []; return }
  uiSections.value = (course.value.sections || []).map(s => ({
    id: s.id,
    title: s.title,
    items: (s.lessons || []).map(l => ({
      id: l.id,
      title: l.title,
      durationMinutes: l.durationMinutes,
      type: l.type,
      done: doneSet.has(String(l.id))
    }))
  }))
}

function rebuildAndKeepCursor(preferredId: any) {
  const oldId = preferredId ?? currentLesson.value?.id ?? null
  buildUiSections()
  if (!uiSections.value.length) { cur.value = { si: 0, li: 0 }; return }
  const found = oldId != null ? findById(oldId) : null
  cur.value = found ?? { si: 0, li: 0 }
}

const flat = computed<UiLesson[]>(() => uiSections.value.flatMap(s => s.items))
const totalCount = computed(() => flat.value.length)
// [NOTE] SỬA LỖI LOGIC: Tính trực tiếp từ `doneSet.size` để đảm bảo reactivity
// Force reactivity bằng cách tạo computed từ reactive Set
const doneSetTrigger = ref(0) // Trigger để force reactivity
const doneCount = computed(() => {
  // Access trigger để force reactivity
  doneSetTrigger.value // Trigger reactivity
  // Access doneSet để track changes
  const size = doneSet.size
  return size
})
const progressPct = computed(() => {
  const total = totalCount.value
  const done = doneCount.value
  const pct = total > 0 ? Math.round((done / total) * 100) : 0
  console.log('Progress calculation:', done, '/', total, '=', pct + '%')
  return pct
})
const dash = computed(() => progressPct.value)

const currentLesson = computed<UiLesson | null>(() => uiSections.value[cur.value.si]?.items[cur.value.li] || null);

const currentFlatIndex = computed<number>(() => {
  const id = currentLesson.value?.id
  return id != null ? flat.value.findIndex(l => String(l.id) === String(id)) : -1;
})

const prevLesson = computed<UiLesson | null>(() => {
  const idx = currentFlatIndex.value
  return idx > 0 ? flat.value[idx - 1] : null
})

const nextLesson = computed<UiLesson | null>(() => {
  const idx = currentFlatIndex.value
  return (idx >= 0 && idx < flat.value.length - 1) ? flat.value[idx + 1] : null
})

const lessonVideoUrl = computed(() => currentLessonDetail.value?.video_url)
const lessonVideoFile = computed(() => currentLessonDetail.value?.video_file)
const lessonVideoSrc = computed(() => {
  if (lessonVideoUrl.value) {
    if (isYouTubeUrl(lessonVideoUrl.value)) {
      return getYouTubeEmbedUrl(lessonVideoUrl.value)
    }
    return lessonVideoUrl.value
  }
  if (lessonVideoFile.value) {
    return getVideoFileUrl(lessonVideoFile.value)
  }
  return null
})

const currentSrc = computed(() => {
  // Ưu tiên video từ lesson
  if (lessonVideoSrc.value) return lessonVideoSrc.value
  // Nếu có video_url hoặc video_file từ course, dùng nó
  if (course.value?.video_url) {
    if (isYouTubeUrl(course.value.video_url)) {
      return getYouTubeEmbedUrl(course.value.video_url)
    }
    return course.value.video_url
  }
  if (course.value?.video_file) {
    return getVideoFileUrl(course.value.video_file)
  }
  // Fallback: mock video
  return 'https://pub-52a4bc53687a4601ac29f7d454bef601.r2.dev/test'
})

function isYouTubeUrl(url?: string): boolean {
  if (!url) return false
  return url.includes('youtube.com') || url.includes('youtu.be')
}

function getYouTubeEmbedUrl(url: string): string {
  if (!url) return ''
  let videoId = ''
  if (url.includes('youtube.com/watch?v=')) {
    videoId = url.split('v=')[1]?.split('&')[0] || ''
  } else if (url.includes('youtu.be/')) {
    videoId = url.split('youtu.be/')[1]?.split('?')[0] || ''
  } else if (url.includes('youtube.com/embed/')) {
    videoId = url.split('embed/')[1]?.split('?')[0] || ''
  }
  
  if (!videoId) return url
  
  // Thêm các tham số để cho phép controls và tua video
  const params = new URLSearchParams({
    'enablejsapi': '1',
    'controls': '1', // Cho phép controls
    'rel': '0', // Không hiển thị video liên quan
    'modestbranding': '1', // Giảm branding
    'fs': '1', // Cho phép fullscreen
    'iv_load_policy': '3', // Không hiển thị annotations
  })
  
  return `https://www.youtube.com/embed/${videoId}?${params.toString()}`
}

function getYouTubeVideoId(url: string): string {
  if (!url) return ''
  if (url.includes('youtube.com/watch?v=')) {
    return url.split('v=')[1]?.split('&')[0] || ''
  } else if (url.includes('youtu.be/')) {
    return url.split('youtu.be/')[1]?.split('?')[0] || ''
  } else if (url.includes('youtube.com/embed/')) {
    return url.split('embed/')[1]?.split('?')[0] || ''
  }
  return ''
}

async function onYouTubeIframeLoad() {
  try {
    const videoUrl = lessonVideoUrl.value || course.value?.video_url
    if (!videoUrl || !isYouTubeUrl(videoUrl)) {
      console.log('Not a YouTube URL, skipping YouTube API initialization')
      return
    }
    
    // Load YouTube IFrame API nếu chưa có
    if (!(window as any).YT) {
      // Kiểm tra xem script đã được thêm chưa
      const existingScript = document.querySelector('script[src="https://www.youtube.com/iframe_api"]')
      if (!existingScript) {
        const tag = document.createElement('script')
        tag.src = 'https://www.youtube.com/iframe_api'
        const firstScriptTag = document.getElementsByTagName('script')[0]
        firstScriptTag.parentNode?.insertBefore(tag, firstScriptTag)
      }
      
      // Đợi YouTube API load (với timeout)
      await new Promise((resolve, reject) => {
        const timeout = setTimeout(() => {
          reject(new Error('YouTube API load timeout'))
        }, 10000) // 10 seconds timeout
        
        if ((window as any).YT && (window as any).YT.Player) {
          clearTimeout(timeout)
          resolve(true)
          return
        }
        
        ;(window as any).onYouTubeIframeAPIReady = () => {
          clearTimeout(timeout)
          resolve(true)
        }
      })
    }
    
    // Khởi tạo YouTube player
    const videoId = getYouTubeVideoId(videoUrl)
    if (!videoId || !youtubeIframeRef.value) {
      console.log('Missing videoId or iframe ref')
      return
    }
    
    // Chỉ khởi tạo nếu chưa có player
    if (!youtubePlayer.value) {
      youtubePlayer.value = new (window as any).YT.Player(youtubeIframeRef.value, {
        events: {
          'onStateChange': onYouTubeStateChange,
          'onReady': () => {
            console.log('YouTube player ready')
            // Đánh dấu đã xem khi video bắt đầu phát
            onVideoWatched()
          },
          'onError': (event: any) => {
            console.error('YouTube player error:', event.data)
          }
        }
      })
    }
  } catch (e) {
    console.error('Error initializing YouTube player:', e)
    // Không throw error, chỉ log để video vẫn có thể hiển thị
  }
}

function onYouTubeStateChange(event: any) {
  // YouTube player states:
  // -1 (unstarted), 0 (ended), 1 (playing), 2 (paused), 3 (buffering), 5 (cued)
  if (event.data === 0) { // Video ended
    onVideoEnded()
  } else if (event.data === 1) { // Video playing
    onVideoWatched()
  }
}

function getVideoFileUrl(videoFile?: string): string {
  if (!videoFile) return ''
  if (videoFile.startsWith('http://') || videoFile.startsWith('https://')) {
    return videoFile
  }
  const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  return `${apiBase}/media/${videoFile}`
}

function formatDuration(min?: number){
  if (!min || min <= 0) return '—'
  const total = Math.round(min * 60)
  const mm = Math.floor(total / 60).toString().padStart(2,'0')
  const ss = (total % 60).toString().padStart(2,'0')
  return `${mm}:${ss}`
}

function goBack() {
  const courseId = normalizeRouteParam(route.params.id)
  // Navigate về course detail để trigger reload
  if (courseId) {
    router.push({ name: 'student-course-detail', params: { id: String(courseId) } }).catch(() => {
      window.history.length > 1 ? window.history.back() : router.push('/student/courses')
    })
    return
  }
  router.push('/student/courses').catch(() => {
    // Fallback nếu route không tồn tại
    window.history.length > 1 ? window.history.back() : router.push('/student/courses')
  })
}

async function loadLessonDetail(lessonId: string | number | null) {
  const cid = courseId.value
  if (!cid) return
  try {
    const endpoint = lessonId
      ? `/student/courses/${cid}/player/${lessonId}/`
      : `/student/courses/${cid}/player/`
    const { data } = await api.get(endpoint)
    currentLessonDetail.value = data
    lessonProgress.value = data.progress || null
    const activeLessonId = String(data.id || lessonId || '')
    
    // Load exercises
    try {
      const { data: exercisesData } = await api.get(`/activities/exercises/?lesson=${activeLessonId}`)
      currentLessonExercises.value = Array.isArray(exercisesData) ? exercisesData : exercisesData.results || []
    } catch (e) {
      currentLessonExercises.value = []
    }
    
    // Check unlock
    try {
      const unlockCheck = await contentService.checkLessonUnlock(activeLessonId)
      lessonLocked.value = !unlockCheck.can_unlock
      unlockReason.value = unlockCheck.reason || ''
    } catch {
      lessonLocked.value = false
    }
  } catch (e) {
    console.error('Error loading lesson detail:', e)
    currentLessonDetail.value = null
    currentLessonExercises.value = []
    lessonProgress.value = null
    lessonLocked.value = false
  }
}

async function goToLesson(si: number, li: number){
  cur.value = { si, li }
  openIndex.value = si
  const id = uiSections.value[si]?.items[li]?.id
  if (id != null) {
    await loadLessonDetail(id)
    router.replace({ params: { ...route.params, lessonId: String(id) } })
    videoRef.value?.play?.()
  }
}

async function goPrev(){
  if (!prevLesson.value) return
  const found = findById(prevLesson.value.id)
  if (found) await goToLesson(found.si, found.li)
}

async function goNext(){
  if (!nextLesson.value) return
  // Check if current lesson requires exercise completion
  if (currentLessonDetail.value?.requires_exercise_completion && !lessonProgress.value?.exercise_completed) {
    alert('Bạn cần hoàn thành bài tập trước khi tiếp tục!')
    return
  }
  const found = findById(nextLesson.value.id)
  if (found) await goToLesson(found.si, found.li)
}

async function onVideoWatched() {
  if (!currentLesson.value?.id) return
  try {
    await contentService.updateLessonProgress(currentLesson.value.id, { video_watched: true })
    if (lessonProgress.value) {
      lessonProgress.value.video_watched = true
    }
  } catch (e) {
    console.error('Error updating video watched:', e)
  }
}

async function onVideoEnded() {
  if (!currentLesson.value?.id) return
  
  const lessonId = String(currentLesson.value.id)
  console.log('Video ended for lesson:', lessonId)
  
  // Đánh dấu video đã xem xong
  await onVideoWatched()
  
  // Cập nhật progress: video completed
  try {
    const progressResponse = await contentService.updateLessonProgress(lessonId, { 
      video_watched: true
    })
    console.log('Progress updated:', progressResponse)
    
    if (lessonProgress.value) {
      lessonProgress.value.video_watched = true
      lessonProgress.value.completed = true
    }
    
    // Đánh dấu lesson đã hoàn thành trong local state NGAY LẬP TỨC
    markDone(lessonId)
    console.log('Lesson marked as done in local state. Current progress:', doneCount.value, '/', totalCount.value)
    
    // Reload course data để lấy progress mới từ backend và sync
    const courseId = normalizeRouteParam(route.params.id) as any
    const { data } = await api.get(`/student/courses/${courseId}/`, {
      params: { _t: Date.now() } // Cache busting
    })
    
    if (data && data.sections) {
      course.value = data
      
      // CLEAR doneSet trước khi repopulate để tránh duplicate
      doneSet.clear()
      doneSetTrigger.value++ // Force reactivity
      
      // Repopulate doneSet từ backend data
      let totalLessonsFromBackend = 0
      data.sections.forEach((section: any) => {
        if (section.lessons && Array.isArray(section.lessons)) {
          totalLessonsFromBackend += section.lessons.length
          section.lessons.forEach((lesson: any) => {
            // Check nhiều cách để đảm bảo nhận được completed status
            const isCompleted = lesson.completed === true || 
                               lesson.completed === 'true' || 
                               lesson.completed === 1 ||
                               lesson.completed === '1' ||
                               lesson.videoWatched === true ||
                               lesson.videoWatched === 'true' ||
                               (lesson.videoWatched && !lesson.requires_exercise_completion) ||
                               (lesson.videoWatched && lesson.exerciseCompleted)
            
            if (isCompleted) {
              doneSet.add(String(lesson.id))
              console.log('Added lesson to doneSet:', lesson.id, lesson.title, 'completed:', lesson.completed, 'videoWatched:', lesson.videoWatched)
            }
          })
        }
      })
      
      // Force reactivity sau khi repopulate
      doneSetTrigger.value++
      
      console.log('After reload - doneSet size:', doneSet.size, 'total lessons from backend:', totalLessonsFromBackend, 'UI totalCount:', totalCount.value)
      
      // Force UI update với nextTick
      await nextTick()
      
      // Rebuild UI với progress mới - QUAN TRỌNG: phải rebuild để totalCount được tính lại
      rebuildAndKeepCursor(lessonId)
      
      // Force reactivity update - đợi UI rebuild xong
      await nextTick()
      doneSetTrigger.value++ // Force reactivity one more time
      
      // Log final state
      const finalDone = doneCount.value
      const finalTotal = totalCount.value
      const finalPct = progressPct.value
      console.log('Final progress after rebuild:', finalDone, '/', finalTotal, '=', finalPct + '%')
      
      // Nếu vẫn 0%, log warning
      if (finalTotal > 0 && finalDone === 0) {
        console.warn('⚠️ Progress is 0% but should be updated! doneSet:', Array.from(doneSet), 'sections:', data.sections)
      }
    }
  } catch (e) {
    console.error('Error updating lesson progress:', e)
    // Vẫn mark done trong local state nếu API fail
    markDone(lessonId)
  }
  
  // Final log
  await nextTick()
  console.log('Video ended - Final progress:', doneCount.value, '/', totalCount.value, '=', progressPct.value + '%')
}

function openExercise(exerciseId: string | number) {
  // TODO: Open exercise modal or navigate to exercise page
  alert(`Mở bài tập ${exerciseId}. Tính năng này sẽ được implement sau.`)
}

function toggle(i: number){ openIndex.value = openIndex.value === i ? -1 : i }

function findById(id: any){
  if (id == null) return null
  for (let si=0; si<uiSections.value.length; si++){
    const li = uiSections.value[si].items.findIndex(x => String(x.id) === String(id))
    if (li >= 0) return { si, li }
  }
  return null
}

function markDone(id?: string|number|null){
  if (id == null) return
  const idStr = String(id)
  if (!doneSet.has(idStr)) {
    doneSet.add(idStr)
    // Force reactivity trigger
    doneSetTrigger.value++
    console.log('markDone: Added lesson', idStr, 'to doneSet. New size:', doneSet.size, 'total:', totalCount.value)
    // Rebuild UI để cập nhật trạng thái 'done' cho các bài học
    nextTick(() => {
      rebuildAndKeepCursor(idStr)
      // Force reactivity update
      doneSetTrigger.value++
      console.log('UI rebuilt after markDone. Progress:', doneCount.value, '/', totalCount.value, '=', progressPct.value + '%')
    })
  } else {
    console.log('markDone: Lesson', idStr, 'already in doneSet')
  }
}

watchEffect(() => {
  if (!uiSections.value.length) return
  const id = currentLesson.value?.id
  const found = id != null ? findById(id) : null
  if (!found) {
    cur.value = { si: 0, li: 0 }
  }
})

// Watch for lesson changes
watch(() => currentLesson.value?.id, async (newId) => {
  if (newId) {
    await loadLessonDetail(newId)
  }
}, { immediate: true })

// Watch route params for lessonId changes
watch(() => route.params.lessonId, async (newLessonId) => {
  const normalized = normalizeRouteParam(newLessonId)
  if (normalized) {
    await loadLessonDetail(normalized)
  }
})

onMounted(async () => {
  await load()
  const lessonParam = normalizeRouteParam(route.params.lessonId)
  if (lessonParam) {
    await loadLessonDetail(lessonParam)
  }
})
</script>
