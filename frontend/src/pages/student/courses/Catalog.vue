<template>
  <div class="min-h-screen bg-slate-50">
    <div class="mx-auto max-w-6xl px-4 py-6">
      <!-- header -->
      <div class="flex items-start justify-between gap-3">
        <div>
          <h1 class="text-2xl font-extrabold tracking-tight text-slate-900">Catalog</h1>
          <p class="mt-1 text-slate-600">Khám phá các khoá học đã phát hành theo khối & môn học.</p>
        </div>
        <router-link
          class="inline-flex items-center rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50"
          :to="{ name: 'student-learning-path' }"
        >
          Lộ trình học ›
        </router-link>
      </div>

      <!-- filters -->
      <div class="mt-5 space-y-4">
        <div class="flex flex-col gap-3 sm:flex-row sm:items-center">
          <div class="relative flex-1">
            <input
              v-model.trim="q"
              @keyup.enter="load"
              placeholder="Tìm khóa học…"
              class="w-full rounded-xl border border-slate-200 bg-white px-4 py-2.5 pr-10 text-slate-800 outline-none ring-sky-100 focus:ring-4"
            />
            <svg class="pointer-events-none absolute right-3 top-2.5 h-5 w-5 stroke-slate-400" viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M21 21l-4.3-4.3"/><circle cx="11" cy="11" r="7"/></svg>
          </div>

          <select v-model="grade" class="rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm" @change="load">
            <option :value="undefined">Tất cả khối</option>
            <option v-for="g in [1,2,3,4,5]" :key="g" :value="g">Khối {{ g }}</option>
          </select>

          <select v-model="subject" class="rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm" @change="load">
            <option :value="undefined">Tất cả môn</option>
            <option v-for="s in subjects" :key="s.value" :value="s.value">{{ s.label }}</option>
          </select>

          <select v-model="sortBy" class="rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm" @change="load">
            <option value="updatedAt">Mới nhất</option>
            <option value="createdAt">Cũ nhất</option>
            <option value="title">Tên A-Z</option>
            <option value="enrollments">Nhiều học viên</option>
          </select>
        </div>

        <div class="flex items-center justify-between text-sm text-slate-600">
          <span>Tìm thấy {{ total }} khóa học</span>
          <button
            v-if="q || grade || subject"
            class="text-cyan-600 hover:text-cyan-700"
            @click="clearFilters"
          >
            Xóa bộ lọc
          </button>
        </div>
      </div>

      <!-- grid -->
      <div class="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        <!-- skeleton -->
        <template v-if="loading">
          <div v-for="i in 8" :key="i" class="animate-pulse rounded-2xl border border-slate-200 bg-white">
            <div class="h-36 w-full rounded-t-2xl bg-slate-100"></div>
            <div class="p-4">
              <div class="h-4 w-3/4 rounded bg-slate-100"></div>
              <div class="mt-2 h-3 w-1/2 rounded bg-slate-100"></div>
            </div>
          </div>
        </template>

        <article
          v-else
          v-for="c in items"
          :key="String(c.id)"
          class="group relative overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm transition hover:-translate-y-0.5 hover:shadow-md"
          @click="open(c.id)"
        >
          <img 
            v-if="c.thumbnail" 
            :src="getThumbnailUrl(c.thumbnail)" 
            :alt="c.title" 
            class="h-36 w-full object-cover"
            @error="handleImageError"
          />
          <div v-else class="flex h-36 w-full items-center justify-center bg-slate-200">
            <span class="text-slate-400 text-sm">Chưa có ảnh</span>
          </div>
          <div class="p-4">
            <div class="line-clamp-2 text-sm font-extrabold leading-snug text-slate-900">{{ c.title }}</div>
            <div class="mt-2 flex items-center gap-2 text-xs text-slate-600">
              <span class="inline-flex items-center rounded-full border border-slate-200 px-2 py-0.5">Khối {{ c.grade }}</span>
              <span class="inline-flex items-center rounded-full border border-slate-200 px-2 py-0.5">{{ subjectLabel(c.subject) }}</span>
            </div>
            <div class="mt-2 text-sm font-semibold" :class="(c.price || 0) === 0 ? 'text-green-600' : 'text-amber-600'">
              {{ (c.price || 0) === 0 ? 'Miễn phí' : formatPrice(c.price) }}
            </div>
          </div>
          <div class="absolute right-3 top-3 rounded-full bg-white/90 px-2 py-1 text-[10px] font-bold text-slate-600 ring-1 ring-slate-200">PUBLISHED</div>
        </article>
      </div>

      <!-- pager & empty -->
      <div v-if="totalPages > 1" class="mt-6 flex items-center justify-center gap-2">
        <button
          :disabled="page <= 1"
          @click="goToPage(page - 1)"
          class="rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm font-semibold text-slate-700 disabled:opacity-40 hover:bg-slate-50"
        >
          ‹ Trước
        </button>
        <div class="flex gap-1">
          <button
            v-for="p in visiblePages"
            :key="p"
            class="rounded-xl border px-3 py-2 text-sm font-semibold transition"
            :class="
              p === page
                ? 'border-cyan-500 bg-cyan-50 text-cyan-700'
                : 'border-slate-200 bg-white text-slate-700 hover:bg-slate-50'
            "
            @click="goToPage(p)"
          >
            {{ p }}
          </button>
        </div>
        <button
          :disabled="page >= totalPages"
          @click="goToPage(page + 1)"
          class="rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm font-semibold text-slate-700 disabled:opacity-40 hover:bg-slate-50"
        >
          Sau ›
        </button>
      </div>

      <div v-if="!loading && !items.length" class="mt-8 rounded-2xl border border-dashed border-slate-300 bg-white p-10 text-center text-slate-600">
        Không có khoá học phù hợp.
      </div>

      <div v-if="err" class="mt-4 text-center font-semibold text-rose-600">{{ err }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { courseService, type Subject } from '@/services/course.service'

const router = useRouter()
const route = useRoute()

const items = ref<any[]>([])
const err = ref('')
const loading = ref(false)
const total = ref(0)

const q = ref('')
const grade = ref<number | undefined>()
const subject = ref<Subject | undefined>()
const sortBy = ref<'updatedAt' | 'title' | 'enrollments' | 'createdAt'>('updatedAt')
const page = ref(1)
const pageSize = 20
const subjects = courseService.subjects()

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize)))

const visiblePages = computed(() => {
  const max = totalPages.value
  const current = page.value
  const pages: number[] = []
  
  if (max <= 7) {
    for (let i = 1; i <= max; i++) pages.push(i)
  } else {
    if (current <= 3) {
      for (let i = 1; i <= 5; i++) pages.push(i)
    } else if (current >= max - 2) {
      for (let i = max - 4; i <= max; i++) pages.push(i)
    } else {
      for (let i = current - 2; i <= current + 2; i++) pages.push(i)
    }
  }
  return pages
})

function subjectLabel(s: Subject){
  for (let i = 0; i < subjects.length; i++) {
    if (subjects[i].value === s) {
      return subjects[i].label
    }
  }
  return s
}

function clearFilters() {
  q.value = ''
  grade.value = undefined
  subject.value = undefined
  page.value = 1
  load()
}

function goToPage(p: number) {
  if (p >= 1 && p <= totalPages.value) {
    page.value = p
    load()
  }
}

async function load(){
  try{
    loading.value = true
    const res = await courseService.list({
      q: q.value || undefined,
      grade: grade.value as any,
      subject: subject.value as any,
      status: 'published',
      page: page.value,
      pageSize,
      sortBy: sortBy.value,
      sortDir: sortBy.value === 'title' ? 'ascending' : 'descending',
    })
    items.value = res.items
    total.value = res.total || res.items.length
    err.value = ''
  }catch(e:any){ err.value = e?.message || String(e)}
  finally{ loading.value = false }
}
function open(id: number | string){
  router.push({ name: 'student-course-detail', params: { id } })
}

function getThumbnailUrl(thumbnail?: string): string {
  if (!thumbnail) return ''
  if (thumbnail.startsWith('http://') || thumbnail.startsWith('https://')) {
    return thumbnail
  }
  const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  return `${apiBase}/media/${thumbnail}`
}

function handleImageError(event: Event) {
  const img = event.target as HTMLImageElement
  img.src = 'https://via.placeholder.com/400x300?text=No+Image'
}

function formatPrice(price?: number | string): string {
  if (!price || price === 0 || price === '0') return 'Miễn phí'
  const numPrice = typeof price === 'string' ? parseFloat(price) : price
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(numPrice)
}

onMounted(() => {
  // nhận filter từ LearningPath (query.grade)
  const g = Number(route.query.grade || '')
  if (!isNaN(g) && g >= 1 && g <= 5) grade.value = g
  load()
})
</script>
