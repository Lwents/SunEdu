<template>
  <div class="student-shell">
    <div class="student-container">
      <header class="mb-6">
        <p class="student-section-title">Chứng chỉ</p>
        <h1 class="text-3xl font-black text-gray-900 dark:text-gray-100">Chứng chỉ của tôi</h1>
        <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
          Các chứng chỉ bạn đã đạt được sau khi hoàn thành bài thi.
        </p>
      </header>

      <div
        v-if="items.length"
        class="grid gap-4 sm:grid-cols-2 xl:grid-cols-3"
      >
        <article
          v-for="c in items"
          :key="c.id"
          class="flex flex-col overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm shadow-slate-100 transition hover:-translate-y-1 hover:shadow-xl"
        >
          <img :src="c.thumbnail" :alt="c.title" class="h-40 w-full object-cover" />
          <div class="flex flex-1 flex-col space-y-2 p-4">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">{{ c.title }}</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400">
              Điểm {{ c.score }}/{{ c.total }} · Ngày cấp {{ c.issuedAt }}
            </p>
            <div class="mt-auto flex items-center justify-end gap-2">
              <el-button size="small" @click="view(c)">Xem</el-button>
              <el-button size="small" type="primary" @click="download(c)">Tải PDF</el-button>
            </div>
          </div>
        </article>
      </div>

      <div
        v-else
        class="mt-6 rounded-3xl border border-dashed border-slate-200 bg-white/80 px-6 py-10 text-center text-sm text-gray-600 dark:text-gray-400"
      >
        Bạn chưa có chứng chỉ nào.
      </div>
      <div
        v-if="err"
        class="mt-4 rounded-3xl border border-rose-200 bg-rose-50/80 px-4 py-3 text-center text-sm text-rose-600"
      >
        {{ err }}
      </div>
    </div>

    <el-dialog v-model="show" title="Xem chứng chỉ" width="720px">
      <img :src="viewing?.image" alt="" class="w-full rounded-lg border border-slate-200" />
      <template #footer>
        <el-button @click="show = false">Đóng</el-button>
        <el-button type="primary" @click="download(viewing!)">Tải PDF</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'

let examService: any
try { examService = (await import('@/services/exam.service')).examService } catch {}

const items = ref<any[]>([])
const err = ref('')
const show = ref(false)
const viewing = ref<any>(null)

onMounted(async () => {
  try {
    items.value = examService?.certificates ? await examService.certificates() : mockCerts()
  } catch (e:any) {
    err.value = e?.message || String(e)
    items.value = mockCerts()
  }
})

function view(c:any){ viewing.value = c; show.value = true }
function download(c:any){
  // demo: tải ảnh; thực tế trả file pdf từ server
  const a = document.createElement('a')
  a.href = c.pdf || c.image || c.thumbnail
  a.download = (c.title || 'certificate') + '.pdf'
  a.click()
}

/* ------- MOCK ------- */
function mockCerts(){
  return Array.from({length:4}).map((_,i)=>({
    id: i+1,
    title: `Chứng chỉ Đề #${i+1}`,
    score: 90 - i*5,
    total: 100,
    issuedAt: '2025-03-1' + i,
    thumbnail: `https://picsum.photos/seed/cert-${i}/640/360`,
    image: `https://picsum.photos/seed/cert-${i}/960/540`,
    pdf: ''
  }))
}
</script>
