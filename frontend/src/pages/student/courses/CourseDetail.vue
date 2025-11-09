<!-- src/pages/student/learn/LessonPlayer.vue -->
<template>
  <div class="student-shell" v-if="course">
    <div class="student-container max-w-6xl">
      <div
        class="mb-4 flex flex-col gap-2 text-sm font-semibold text-brand-muted sm:flex-row sm:items-center sm:justify-between"
      >
        <button
          type="button"
          class="inline-flex w-full items-center justify-center gap-2 rounded-2xl border border-slate-200 px-4 py-2 text-sm font-semibold text-brand-deep transition hover:bg-slate-50 sm:w-auto"
          @click="goBack"
        >
          ‹ Rời khỏi đây
        </button>
        <span class="text-center sm:text-right">{{ course.sections?.length || 0 }} chương</span>
      </div>

      <div class="grid gap-6 lg:grid-cols-[minmax(0,2fr)_minmax(320px,1fr)]">
        <div class="order-1 overflow-hidden rounded-3xl border border-slate-200 bg-slate-900/5 shadow-lg shadow-slate-200">
          <video
            ref="videoRef"
            class="aspect-video w-full rounded-3xl bg-black object-contain"
            :src="currentSrc"
            controls
            playsinline
            @ended="markDone(currentLesson?.id)"
          ></video>
          <div class="space-y-1 px-6 py-5">
            <p class="student-section-title text-xs text-brand-muted">Bài học hiện tại</p>
            <h2 class="text-2xl font-bold text-brand-deep">{{ course.title }}</h2>
            <p class="text-sm text-brand-muted">
              {{ currentFlatIndex + 1 }}. {{ currentLesson?.title }}
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
                  d="M18 2a16 16 0 1 1 0 32a16 16 0 1 1 0-32"
                />
                <path
                  class="text-brand-500"
                  stroke="currentColor"
                  stroke-width="3"
                  stroke-linecap="round"
                  fill="none"
                  :style="{ strokeDasharray: dash + ', 100' }"
                  d="M18 2a16 16 0 1 1 0 32a16 16 0 1 1 0-32"
                />
              </svg>
              <span class="absolute text-lg font-black text-brand-deep">{{ progressPct }}%</span>
            </div>
            <div>
              <p class="text-sm font-semibold uppercase tracking-[0.3em] text-brand-muted">
                Nội dung khóa học
              </p>
              <p class="text-base font-bold text-brand-deep">{{ doneCount }}/{{ totalCount }} bài học</p>
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
                class="flex w-full items-center justify-between gap-3 px-4 py-3 text-left font-semibold text-brand-deep"
                @click="toggle(si)"
              >
                <span class="flex-1 text-sm">{{ si + 1 }}. {{ sec.title }}</span>
                <span class="text-xs text-brand-muted">{{ sec.items.length }}</span>
                <svg
                  class="h-4 w-4 text-brand-muted transition"
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
                        ? 'bg-brand-50 text-brand-700'
                        : 'bg-white text-brand-deep hover:bg-slate-50',
                      it.done ? 'font-semibold' : '',
                    ]"
                    @click="goToLesson(si, li)"
                  >
                    <div class="flex items-center gap-2">
                      <span class="text-xs font-semibold text-brand-muted">{{ li + 1 }}</span>
                      <span>{{ it.title }}</span>
                    </div>
                    <div class="flex items-center gap-3 text-xs text-brand-muted">
                      <span>{{ formatDuration(it.durationMinutes) }}</span>
                      <svg
                        v-if="it.done"
                        class="h-4 w-4 text-brand-500"
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
            class="inline-flex items-center justify-center rounded-2xl border border-slate-200 px-4 py-2 text-sm font-semibold text-brand-deep transition hover:bg-slate-50 disabled:opacity-50"
            :disabled="!prevLesson"
            @click="goPrev"
          >
            ‹ Bài trước
          </button>
          <div class="text-center text-xs font-semibold uppercase tracking-[0.3em] text-brand-muted">
            {{ doneCount }}/{{ totalCount }} bài hoàn thành
          </div>
          <button
            type="button"
            class="inline-flex items-center justify-center rounded-2xl border border-brand-200 bg-brand-500 px-4 py-2 text-sm font-semibold text-white shadow-lg shadow-emerald-200 transition hover:bg-brand-600 disabled:opacity-50"
            :disabled="!nextLesson"
            @click="goNext"
          >
            Bài tiếp theo ›
          </button>
        </div>
      </div>
    </div>
  </div>

  <div v-else class="grid min-h-screen place-items-center text-brand-muted">Đang tải…</div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watchEffect } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { courseService, type CourseDetail, type Lesson as ApiLesson } from '@/services/course.service'

const router = useRouter()
const route = useRoute()

/* ====== STATE ====== */
const course = ref<CourseDetail | null>(null)
const videoRef = ref<HTMLVideoElement|null>(null)
const doneSet = reactive(new Set<string>())               // local progress
const showNonVideoInOutline = true                       // ẩn/hiện PDF/Quiz
const openIndex = ref<number>(0)
const cur = ref<{ si: number; li: number }>({ si: 0, li: 0 })

/* ====== LOAD ====== */
async function load() {
  const id = route.params.id as any
  const lessonParam = route.params.lessonId as any

  const d = await courseService.detail(id)
  course.value = d

  // build và trỏ đúng bài
  rebuildAndKeepCursor(lessonParam ?? null)
  if (lessonParam) openIndex.value = findById(lessonParam)?.si ?? 0
}

/* ====== UI sections ====== */
type UiLesson = { id: string|number; title: string; durationMinutes?: number; type: ApiLesson['type']; done?: boolean }
type UiSection = { id: string|number; title: string; items: UiLesson[] }
const uiSections = ref<UiSection[]>([])

function buildUiSections() {
  if (!course.value) { uiSections.value = []; return }
  uiSections.value = (course.value.sections || []).map(s => ({
    id: s.id,
    title: s.title,
    items: (s.lessons || [])
      .filter(l => showNonVideoInOutline ? true : l.type === 'video')
      .map(l => ({
        id: l.id,
        title: l.title,
        durationMinutes: l.durationMinutes,
        type: l.type,
        done: doneSet.has(String(l.id))
      }))
  }))
}

/** Rebuild nhưng vẫn giữ nguyên con trỏ theo id cũ (nếu còn). */
function rebuildAndKeepCursor(preferredId: any) {
  const oldId = preferredId ?? currentLesson.value?.id ?? null
  buildUiSections()
  if (!uiSections.value.length) { cur.value = { si: 0, li: 0 }; return }

  // nếu còn id cũ thì trỏ lại, không thì snap về 0
  const found = oldId != null ? findById(oldId) : null
  cur.value = found ?? { si: 0, li: 0 }
}

/* ====== DERIVED (dựa theo chỉ số phẳng) ====== */
const flat = computed<UiLesson[]>(() => uiSections.value.flatMap(s => s.items))
const totalCount = computed(() => flat.value.length)
const doneCount = computed(() => flat.value.filter(l => l.done).length)
const progressPct = computed(() => Math.round((doneCount.value / Math.max(1, totalCount.value)) * 100))
const dash = computed(() => (progressPct.value/100)*100)

const currentLesson = computed<UiLesson | null>(() => {
  const sec = uiSections.value[cur.value.si]; if (!sec) return null
  return sec.items[cur.value.li] || null
})

/** Trả về index trong mảng phẳng ứng với cur; an toàn khi rebuild */
const currentFlatIndex = computed<number>(() => {
  const id = currentLesson.value?.id
  if (id == null) return -1
  return flat.value.findIndex(l => String(l.id) === String(id))
})

const prevLesson = computed<UiLesson | null>(() => {
  const idx = currentFlatIndex.value
  return idx > 0 ? flat.value[idx - 1] : null
})

const nextLesson = computed<UiLesson | null>(() => {
  const idx = currentFlatIndex.value
  return (idx >= 0 && idx < flat.value.length - 1) ? flat.value[idx + 1] : null
})

/* Demo src: thay bằng URL thật của bạn */
const currentSrc = computed(() =>
  'https://pub-52a4bc53687a4601ac29f7d454bef601.r2.dev/test2.mp4'
)

/* ====== METHODS ====== */
function formatDuration(min?: number){
  if (!min || min <= 0) return '—'
  const total = Math.round(min * 60)
  const mm = Math.floor(total / 60).toString().padStart(2,'0')
  const ss = (total % 60).toString().padStart(2,'0')
  return `${mm}:${ss}`
}

function goBack(){ window.history.length > 1 ? window.history.back() : router.push('/student/courses') }

function goToLesson(si: number, li: number){
  cur.value = { si, li }
  openIndex.value = si
  const id = uiSections.value[si]?.items[li]?.id
  if (id != null) router.replace({ params: { ...route.params, lessonId: String(id) } })
  videoRef.value?.play?.()
}

function goPrev(){
  if (!prevLesson.value) return
  const found = findById(prevLesson.value.id)
  if (found) goToLesson(found.si, found.li)
}

function goNext(){
  if (!nextLesson.value) return
  const found = findById(nextLesson.value.id)
  if (found) goToLesson(found.si, found.li)
}

function toggle(i: number){ openIndex.value = openIndex.value===i ? -1 : i }

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
  doneSet.add(String(id))
  // rebuild nhưng vẫn giữ bài hiện tại => không bị -1 làm mất nút "tiếp theo"
  rebuildAndKeepCursor(id)
}

/* Nếu dữ liệu/sections đổi bất chợt (reset), vẫn đảm bảo con trỏ hợp lệ */
watchEffect(() => {
  if (!uiSections.value.length) return
  const id = currentLesson.value?.id
  const found = id != null ? findById(id) : null
  if (!found) {
    // snap về 0 an toàn
    cur.value = { si: 0, li: 0 }
  }
})

/* ====== MOUNT ====== */
onMounted(load)
</script>
