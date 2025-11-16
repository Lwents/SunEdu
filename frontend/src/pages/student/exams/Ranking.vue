<template>
  <div class="min-h-screen bg-slate-50 py-8">
    <div class="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
      <header class="mb-6 flex flex-col gap-4 rounded-lg border border-slate-200 bg-white px-5 py-4 shadow-sm sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 class="text-3xl font-bold text-slate-900">🏆 Bảng Xếp Hạng</h1>
          <p class="mt-1 text-sm text-slate-600">
            Vinh danh những học viên có thành tích xuất sắc nhất trong mỗi kỳ thi.
          </p>
        </div>
        <div class="relative w-full max-w-sm" @mouseleave="openSelect = false">
          <button
            type="button"
            class="flex w-full items-center justify-between gap-2 rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-900 hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-slate-200 transition"
            :disabled="loadingExams"
            @click="openSelect = !openSelect"
          >
            <span v-if="loadingExams">Đang tải đề...</span>
            <span v-else>{{ selectedExamTitle || 'Vui lòng chọn đề thi' }}</span>
            <svg class="h-4 w-4 text-slate-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25 12 15.75 4.5 8.25" />
            </svg>
          </button>
          <ul
            v-show="openSelect"
            class="absolute right-0 z-20 mt-2 w-full rounded-lg border border-slate-200 bg-white p-2 shadow-lg"
          >
            <li
              v-for="e in exams"
              :key="e.id"
              class="cursor-pointer rounded-lg px-3 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50 transition"
              @click="selectExam(e.id)"
            >
              {{ e.title }}
            </li>
          </ul>
        </div>
      </header>

      <div v-if="loading" class="space-y-4">
        <div class="grid gap-4 md:grid-cols-3">
          <div class="h-48 animate-pulse rounded-lg bg-slate-100"></div>
          <div class="h-48 animate-pulse rounded-lg bg-slate-100"></div>
          <div class="h-48 animate-pulse rounded-lg bg-slate-100"></div>
        </div>
        <div class="space-y-3 rounded-lg border border-slate-200 bg-white px-4 py-4 shadow-sm">
          <div v-for="i in 7" :key="i" class="h-14 animate-pulse rounded-lg bg-slate-100"></div>
        </div>
      </div>

      <div
        v-else-if="rows.length === 0"
        class="flex flex-col items-center rounded-lg border border-dashed border-slate-300 bg-white px-6 py-12 text-center text-sm text-slate-600"
      >
        <img
          src="https://res.cloudinary.com/dapvicdpm/image/upload/v1727116801/temp/leaderboard-empty_u5o8fg.svg"
          alt="No data"
          class="h-32 w-32"
        />
        <h3 class="mt-4 text-xl font-bold text-slate-900">Chưa có dữ liệu xếp hạng</h3>
        <p class="mt-2 max-w-md">
          Hiện chưa có ai hoàn thành đề thi này. Hãy là người đầu tiên!
        </p>
      </div>

      <div v-else class="space-y-6">
        <div class="grid gap-4 md:grid-cols-3">
          <div
            v-if="rows[1]"
            class="flex flex-col items-center rounded-lg border border-slate-200 bg-white px-4 py-6 text-center shadow-sm"
          >
            <div class="text-sm font-semibold text-slate-600">🥈 Hạng 2</div>
            <img :src="avatarOf(rows[1].name)" alt="avatar" class="mt-3 h-16 w-16 rounded-full object-cover border-2 border-slate-200" />
            <h3 class="mt-3 text-lg font-bold text-slate-900">{{ rows[1].name }}</h3>
            <p class="text-sm text-slate-600">{{ rows[1].time }}</p>
            <p class="text-xl font-bold text-slate-900">{{ rows[1].score }} điểm</p>
          </div>
          <div
            v-if="rows[0]"
            class="flex flex-col items-center rounded-lg border-2 border-amber-300 bg-amber-50 px-4 py-6 text-center shadow-sm"
          >
            <div class="text-sm font-semibold text-amber-700">🥇 Hạng 1</div>
            <img :src="avatarOf(rows[0].name)" alt="avatar" class="mt-3 h-18 w-18 rounded-full border-4 border-amber-200 object-cover" />
            <h3 class="mt-3 text-lg font-bold text-slate-900">{{ rows[0].name }}</h3>
            <p class="text-sm text-slate-600">{{ rows[0].time }}</p>
            <p class="text-2xl font-bold text-slate-900">{{ rows[0].score }} điểm</p>
          </div>
          <div
            v-if="rows[2]"
            class="flex flex-col items-center rounded-lg border border-slate-200 bg-white px-4 py-6 text-center shadow-sm"
          >
            <div class="text-sm font-semibold text-slate-600">🥉 Hạng 3</div>
            <img :src="avatarOf(rows[2].name)" alt="avatar" class="mt-3 h-16 w-16 rounded-full object-cover border-2 border-slate-200" />
            <h3 class="mt-3 text-lg font-bold text-slate-900">{{ rows[2].name }}</h3>
            <p class="text-sm text-slate-600">{{ rows[2].time }}</p>
            <p class="text-xl font-bold text-slate-900">{{ rows[2].score }} điểm</p>
          </div>
        </div>

        <div class="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
          <div
            v-for="(row, index) in paginatedRestRows"
            :key="row.id || row.name + '-' + getRestRank(index)"
            class="flex flex-col gap-3 border-b border-slate-100 py-4 last:border-b-0 sm:flex-row sm:items-center sm:justify-between"
          >
            <div class="flex items-center gap-4">
              <div class="text-xl font-bold text-slate-600">#{{ getRestRank(index) }}</div>
              <div class="flex items-center gap-3">
                <img :src="avatarOf(row.name)" alt="avatar" class="h-12 w-12 rounded-full object-cover border border-slate-200" />
                <span class="text-base font-semibold text-slate-900">{{ row.name }}</span>
              </div>
            </div>
            <div class="grid flex-1 grid-cols-3 gap-3 text-center text-sm text-slate-600">
              <div>
                <p class="text-lg font-bold text-slate-900">{{ row.correct }}/{{ row.total }}</p>
                <p>Câu đúng</p>
              </div>
              <div>
                <p class="text-lg font-bold text-slate-900">{{ row.time }}</p>
                <p>Thời gian</p>
              </div>
              <div>
                <p class="text-lg font-bold text-slate-900">{{ row.score }}</p>
                <p>Điểm</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="totalPages > 1" class="mt-6 flex items-center justify-center gap-2">
        <button
          class="inline-flex h-10 w-10 items-center justify-center rounded-lg border border-slate-300 bg-white text-sm font-semibold text-slate-700 hover:bg-slate-50 transition disabled:cursor-not-allowed disabled:opacity-40"
          :disabled="currentPage <= 1"
          @click="handlePageChange(currentPage - 1)"
        >
          ‹
        </button>
        <button
          v-for="p in pagesToShow"
          :key="p.key"
          class="inline-flex h-10 min-w-[40px] items-center justify-center rounded-lg border text-sm font-semibold transition"
          :class="p.sep
            ? 'border-transparent bg-transparent text-slate-400'
            : p.num === currentPage
              ? 'border-slate-900 bg-slate-900 text-white'
              : 'border-slate-300 bg-white text-slate-700 hover:bg-slate-50'"
          :disabled="p.sep"
          @click="!p.sep && handlePageChange(p.num!)"
        >
          {{ p.text }}
        </button>
        <button
          class="inline-flex h-10 w-10 items-center justify-center rounded-lg border border-slate-300 bg-white text-sm font-semibold text-slate-700 hover:bg-slate-50 transition disabled:cursor-not-allowed disabled:opacity-40"
          :disabled="currentPage >= totalPages"
          @click="handlePageChange(currentPage + 1)"
        >
          ›
        </button>
      </div>

      <div
        v-if="me"
        class="mt-8 rounded-lg border border-slate-200 bg-slate-50 px-5 py-4 shadow-sm"
      >
        <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div class="flex items-center gap-4">
            <div class="text-2xl font-bold text-slate-700">#{{ me.rank }}</div>
            <div class="flex items-center gap-3">
              <img :src="avatarOf('Bạn')" alt="avatar" class="h-12 w-12 rounded-full object-cover border border-slate-200" />
              <span class="text-base font-semibold text-slate-900">Vị trí của bạn</span>
            </div>
          </div>
          <div class="grid flex-1 grid-cols-3 gap-3 text-center text-sm text-slate-600">
            <div>
              <p class="text-lg font-bold text-slate-900">{{ me.correct }}/{{ me.total }}</p>
              <p>Câu đúng</p>
            </div>
            <div>
              <p class="text-lg font-bold text-slate-900">{{ me.time }}</p>
              <p>Thời gian</p>
            </div>
            <div>
              <p class="text-lg font-bold text-slate-900">{{ me.score }}</p>
              <p>Điểm</p>
            </div>
          </div>
        </div>
      </div>

      <div
        v-if="err"
        class="mt-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-center text-sm text-red-600"
      >
        {{ err }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch, computed } from 'vue'

// --- MOCK SERVICE (thay thế bằng service thật của bạn) ---
const examService = createMockService();

// --- TYPES ---
type Exam = { id: number | string; title: string };
type RankRow = { id?: string | number; name: string; score: number; correct: number; total: number; time: string };
type RankMe = { rank: number; score: number; correct: number; total: number; time: string };

// --- STATE ---
const exams = ref<Exam[]>([]);
const examId = ref<Exam['id'] | undefined>();
const openSelect = ref(false);

const rows = ref<RankRow[]>([]);
const me = ref<RankMe | null>(null);

const loading = ref(true);
const loadingExams = ref(true);
const err = ref('');

const selectedExamTitle = computed(() => exams.value.find(e => e.id === examId.value)?.title);

function selectExam(id: Exam['id']) {
  examId.value = id;
  openSelect.value = false;
}

// --- PAGINATION (cho danh sách từ hạng 4) ---
const currentPage = ref(1);
const pageSize = 10;
const restRows = computed(() => rows.value.slice(3)); // Bỏ qua top 3

const paginatedRestRows = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  return restRows.value.slice(start, start + pageSize);
});

const totalPages = computed(() => Math.max(1, Math.ceil(restRows.value.length / pageSize)));

function handlePageChange(page: number) {
  if (page < 1 || page > totalPages.value) return;
  currentPage.value = page;
}

function getRestRank(indexOnPage: number) {
  return (currentPage.value - 1) * pageSize + indexOnPage + 4; // Bắt đầu từ hạng 4
}

const pagesToShow = computed(() => {
  const max = totalPages.value
  const cur = currentPage.value
  const windowSize = 5
  const arr: { key: string; num?: number; text: string; sep?: boolean }[] = []

  const push = (n: number) => arr.push({ key: 'p' + n, num: n, text: String(n) })
  const sep = (k: string) => arr.push({ key: k, text: '…', sep: true })

  if (max <= windowSize + 2) {
    for (let i = 1; i <= max; i++) push(i)
  } else {
    push(1)
    const start = Math.max(2, cur - 1)
    const end = Math.min(max - 1, cur + 1)
    if (start > 2) sep('s')
    for (let i = start; i <= end; i++) push(i)
    if (end < max - 1) sep('e')
    push(max)
  }
  return arr
})


// --- HELPERS ---
function avatarOf(name: string) {
  const safe = encodeURIComponent(name || 'User');
  return `https://api.dicebear.com/7.x/initials/svg?seed=${safe}&backgroundColor=e2e8f0&textColor=64748b`;
}

// --- DATA LOADERS ---
async function loadExams() {
  loadingExams.value = true;
  err.value = '';
  try {
    const list = await examService.list();
    exams.value = list;
    if (list.length > 0) {
      examId.value = list[0].id;
    }
  } catch (e: any) {
    err.value = e?.message || String(e);
  } finally {
    loadingExams.value = false;
  }
}

async function loadRanking(id: Exam['id']) {
  if (!id && id !== 0) {
    rows.value = [];
    me.value = null;
    return;
  };
  loading.value = true;
  rows.value = [];
  me.value = null;
  err.value = '';
  currentPage.value = 1;

  try {
    const r = await examService.ranking(id);
    rows.value = r.top;
    me.value = r.me;
  } catch (e: any) {
    err.value = e?.message || String(e);
  } finally {
    loading.value = false;
  }
}

// --- LIFECYCLE ---
onMounted(loadExams);
watch(examId, (id) => { if (id !== undefined) loadRanking(id) });

// --- MOCK SERVICE ---
function createMockService() {
  const delay = (ms: number) => new Promise(r => setTimeout(r, ms));
  return {
    async list(): Promise<Exam[]> {
      await delay(500);
      return Array.from({ length: 8 }).map((_, i) => ({
        id: i + 1,
        title: `Đề thi Thử Năng Lực #${i + 1}`
      }));
    },
    async ranking(_examId: Exam['id']): Promise<{ top: RankRow[]; me: RankMe }> {
      await delay(800);
      const N = 73;
      const top: RankRow[] = Array.from({ length: N }).map((_, i) => {
        const correct = 50 - Math.floor(i / 2);
        const score = Math.max(0, correct * 20);
        const mm = (15 + (i % 20)).toString().padStart(2, '0');
        const ss = ((i * 7) % 60).toString().padStart(2, '0');
        return { id: i + 1, name: `Học viên ${String.fromCharCode(65 + i)}`, score, correct, total: 50, time: `${mm}:${ss}` };
      });
      return { top, me: { rank: 88, score: 720, correct: 36, total: 50, time: '22:31' } };
    }
  };
}
</script>
