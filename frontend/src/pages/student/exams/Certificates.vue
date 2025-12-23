<template>
  <div :class="isDark ? 'dark-mode' : 'light-mode'">
    <!-- Background glow effects for dark mode -->
    <div v-if="isDark" class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 -left-32 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl"></div>
      <div class="absolute bottom-1/4 -right-32 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl"></div>
    </div>

    <div class="student-shell relative z-10">
      <div class="student-container">
        <header class="mb-6">
          <p class="student-section-title" :class="isDark ? 'text-cyan-400' : 'text-indigo-600'">Chứng chỉ</p>
          <h1 class="text-3xl font-black" :class="isDark ? 'text-white' : 'text-gray-900'">Chứng chỉ của tôi</h1>
          <p class="mt-2 text-sm" :class="isDark ? 'text-slate-400' : 'text-gray-600'">
            Các chứng chỉ bạn đã đạt được sau khi hoàn thành bài thi.
          </p>
        </header>

        <div v-if="items.length" class="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          <article
            v-for="c in items"
            :key="c.id"
            class="flex flex-col overflow-hidden rounded-3xl border shadow-sm transition hover:-translate-y-1 hover:shadow-xl"
            :class="isDark 
              ? 'border-slate-700/50 bg-slate-800/50 backdrop-blur-sm' 
              : 'border-slate-200 bg-white'"
          >
            <img :src="c.thumbnail" :alt="c.title" class="h-40 w-full object-cover" />
            <div class="flex flex-1 flex-col space-y-2 p-4">
              <h3 class="text-lg font-semibold" :class="isDark ? 'text-white' : 'text-gray-900'">{{ c.title }}</h3>
              <p class="text-sm" :class="isDark ? 'text-slate-400' : 'text-gray-600'">
                Điểm {{ c.score }}/{{ c.total }} · Ngày cấp {{ c.issuedAt }}
              </p>
              <div class="mt-auto flex items-center justify-end gap-2">
                <button
                  @click="view(c)"
                  class="px-3 py-1.5 text-sm font-medium rounded-lg border transition"
                  :class="isDark 
                    ? 'border-slate-600 text-slate-300 hover:bg-slate-700' 
                    : 'border-slate-300 text-slate-700 hover:bg-slate-50'"
                >
                  Xem
                </button>
                <button
                  @click="download(c)"
                  class="px-3 py-1.5 text-sm font-medium rounded-lg transition"
                  :class="isDark 
                    ? 'bg-gradient-to-r from-cyan-500 to-purple-500 text-white hover:from-cyan-600 hover:to-purple-600' 
                    : 'bg-indigo-600 text-white hover:bg-indigo-700'"
                >
                  Tải PDF
                </button>
              </div>
            </div>
          </article>
        </div>

        <div
          v-else
          class="mt-6 rounded-3xl border border-dashed px-6 py-10 text-center text-sm"
          :class="isDark 
            ? 'border-slate-700 bg-slate-800/30 text-slate-400' 
            : 'border-slate-200 bg-white/80 text-gray-600'"
        >
          Bạn chưa có chứng chỉ nào.
        </div>

        <div
          v-if="err"
          class="mt-4 rounded-3xl border px-4 py-3 text-center text-sm"
          :class="isDark 
            ? 'border-rose-500/30 bg-rose-500/10 text-rose-400' 
            : 'border-rose-200 bg-rose-50/80 text-rose-600'"
        >
          {{ err }}
        </div>
      </div>

      <!-- View Certificate Modal -->
      <Teleport to="body">
        <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="show = false"></div>
          <div 
            class="relative w-full max-w-3xl rounded-2xl p-6 shadow-2xl"
            :class="isDark ? 'bg-slate-800' : 'bg-white'"
          >
            <h3 class="text-lg font-semibold mb-4" :class="isDark ? 'text-white' : 'text-gray-900'">
              Xem chứng chỉ
            </h3>
            <img :src="viewing?.image" alt="" class="w-full rounded-lg border" :class="isDark ? 'border-slate-700' : 'border-slate-200'" />
            <div class="mt-4 flex justify-end gap-3">
              <button
                @click="show = false"
                class="px-4 py-2 text-sm font-medium rounded-lg border transition"
                :class="isDark 
                  ? 'border-slate-600 text-slate-300 hover:bg-slate-700' 
                  : 'border-slate-300 text-slate-700 hover:bg-slate-50'"
              >
                Đóng
              </button>
              <button
                @click="download(viewing!)"
                class="px-4 py-2 text-sm font-medium rounded-lg transition"
                :class="isDark 
                  ? 'bg-gradient-to-r from-cyan-500 to-purple-500 text-white hover:from-cyan-600 hover:to-purple-600' 
                  : 'bg-indigo-600 text-white hover:bg-indigo-700'"
              >
                Tải PDF
              </button>
            </div>
          </div>
        </div>
      </Teleport>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useThemeStore } from '@/store/theme.store'

const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)

const items = ref<any[]>([])
const err = ref('')
const show = ref(false)
const viewing = ref<any>(null)

onMounted(async () => {
  try {
    const examServiceModule = await import('@/services/exam.service')
    const examService = examServiceModule.examService
    if (examService && typeof (examService as any).certificates === 'function') {
      items.value = await (examService as any).certificates()
    } else {
      items.value = mockCerts()
    }
  } catch (e:any) {
    err.value = e?.message || String(e)
    items.value = mockCerts()
  }
})

function view(c:any){ viewing.value = c; show.value = true }

async function download(c:any){
  try {
    if (c.pdf) {
      const response = await fetch(c.pdf)
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = (c.title || 'certificate') + '.pdf'
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)
    } else if (c.image || c.thumbnail) {
      const a = document.createElement('a')
      a.href = c.image || c.thumbnail
      a.download = (c.title || 'certificate') + '.png'
      a.click()
    }
  } catch (e: any) {
    console.error('Download error:', e)
    alert('Không thể tải chứng chỉ. Vui lòng thử lại sau.')
  }
}

function mockCerts(){
  const result = []
  for (let i = 0; i < 4; i++) {
    result.push({
      id: i+1,
      title: `Chứng chỉ Đề #${i+1}`,
      score: 90 - i*5,
      total: 100,
      issuedAt: '2025-03-1' + i,
      thumbnail: `https://picsum.photos/seed/cert-${i}/640/360`,
      image: `https://picsum.photos/seed/cert-${i}/960/540`,
      pdf: ''
    })
  }
  return result
}
</script>

<style scoped>
.dark-mode {
  @apply min-h-screen bg-slate-950;
}
.light-mode {
  @apply min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50;
}
</style>
