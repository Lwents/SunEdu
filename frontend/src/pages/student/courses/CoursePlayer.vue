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
            <p class="student-section-title text-xs text-gray-600 dark:text-gray-400">Bài học hiện tại</p>
            <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100">{{ course.title }}</h2>
            <p class="text-sm text-gray-600 dark:text-gray-400">
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
            class="inline-flex items-center justify-center rounded-2xl border border-cyan-200 dark:border-cyan-700 bg-cyan-50 dark:bg-cyan-900/200 px-4 py-2 text-sm font-semibold text-white shadow-lg shadow-ocean-glow transition hover:bg-cyan-600 disabled:opacity-50"
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
import { computed, onMounted, reactive, ref, watchEffect } from 'vue'
import { useRouter, useRoute } from 'vue-router'

// Giả lập service nếu bạn chưa có
const courseService = {
  detail: async (id: string) => {
    await new Promise(r => setTimeout(r, 500));
    return mockCourseData;
  }
};
type CourseDetail = typeof mockCourseData;
type Lesson = CourseDetail['sections'][0]['lessons'][0];
// ---

const router = useRouter()
const route = useRoute()

const course = ref<CourseDetail | null>(null)
const videoRef = ref<HTMLVideoElement|null>(null)
const doneSet = reactive(new Set<string>())
const openIndex = ref<number>(0)
const cur = ref<{ si: number; li: number }>({ si: 0, li: 0 })

async function load() {
  const id = route.params.id as any
  const lessonParam = route.params.lessonId as any
  const d = await courseService.detail(id)
  course.value = d
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
const doneCount = computed(() => doneSet.size)
const progressPct = computed(() => Math.round((doneCount.value / Math.max(1, totalCount.value)) * 100))
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

const currentSrc = computed(() => 'https://pub-52a4bc53687a4601ac29f7d454bef601.r2.dev/test')

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
  if (!doneSet.has(String(id))) {
    doneSet.add(String(id));
    // Rebuild UI để cập nhật trạng thái 'done' cho các bài học
    rebuildAndKeepCursor(id);
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

onMounted(load)

// --- MOCK DATA ---
const mockCourseData = {
  id: "1",
  title: "Khóa học Vue.js Toàn Tập",
  sections: Array.from({ length: 5 }, (_, si) => ({
    id: `s${si + 1}`,
    title: `Chương ${si + 1}: Bắt đầu với Vue`,
    lessons: Array.from({ length: 4 }, (_, li) => ({
      id: `l${si * 4 + li + 1}`,
      title: `Bài học ${si * 4 + li + 1}`,
      durationMinutes: 5,
      type: 'video' as const,
    })),
  })),
};
</script>
