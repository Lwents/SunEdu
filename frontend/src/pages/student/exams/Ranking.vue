<template>
  <div class="min-h-screen bg-slate-50 py-8 relative overflow-hidden">
    <!-- 🎆 Pháo hoa cho bảng xếp hạng -->
    <RankingFireworks :active="showFireworks" :intensity="fireworkIntensity" />
    
    <div class="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 relative z-10">
      <header class="mb-6 flex flex-col gap-4 rounded-lg border border-slate-200 bg-white px-5 py-4 shadow-sm sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 class="text-3xl font-bold text-slate-900">🏆 Bảng Xếp Hạng</h1>
          <p class="mt-1 text-sm text-slate-600">
            Vinh danh những học viên có thành tích xuất sắc nhất trong mỗi kỳ thi.
          </p>
        </div>
        <div></div>
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

      <div v-else class="space-y-8">
        <section class="rounded-3xl border border-slate-200 bg-white p-8 shadow-xl shadow-slate-200/70">
          <div class="grid gap-5 items-end lg:grid-cols-3">
            <!-- Hạng 2 -->
            <div class="flex flex-col items-center rounded-2xl border-2 border-slate-200 bg-gradient-to-b from-slate-50 to-white px-6 py-8 text-center shadow min-h-[280px]">
              <div class="flex items-center gap-2 text-sm font-semibold text-slate-500">
                <span class="text-lg">🥈</span>
                <span>Hạng 2</span>
              </div>
              <div class="mt-4 flex h-28 w-28 items-center justify-center rounded-full border-2 border-slate-300 bg-slate-100 shadow-inner overflow-hidden">
                <template v-if="top2">
                  <img :src="avatarOf(top2.name, top2.avatar, top2.gender)" alt="avatar" class="h-full w-full object-cover" />
                </template>
                <span v-else class="text-4xl font-bold text-slate-300">?</span>
              </div>
              <div class="mt-5 space-y-1">
                <p class="text-lg font-bold text-slate-900 line-clamp-1">{{ top2?.name || 'Chưa có' }}</p>
                <p class="text-sm text-slate-500">{{ top2 ? top2.time : 'Đang chờ...' }}</p>
                <p class="text-2xl font-bold text-slate-800">{{ top2 ? `${top2.score} điểm` : '--' }}</p>
              </div>
            </div>

            <!-- Hạng 1 -->
            <div class="relative flex flex-col items-center rounded-[28px] border-4 border-amber-300 bg-gradient-to-b from-amber-50 via-amber-100 to-white px-8 py-10 text-center shadow-2xl shadow-amber-100 min-h-[320px]">
              <span class="absolute -top-3 rounded-full bg-amber-400 px-3 py-1 text-xs font-bold text-white shadow">TOP 1</span>
              <div class="flex items-center gap-2 text-sm font-semibold text-amber-700">
                <span class="text-xl">🥇</span>
                <span>Hạng 1</span>
              </div>
              <div class="mt-5 flex h-36 w-36 items-center justify-center rounded-full border-4 border-amber-300 bg-white shadow-[0_18px_40px_rgba(251,191,36,0.35)] overflow-hidden">
                <template v-if="top1">
                  <img :src="avatarOf(top1.name, top1.avatar, top1.gender)" alt="avatar" class="h-full w-full object-cover" />
                </template>
                <span v-else class="text-5xl font-black text-amber-200">?</span>
              </div>
              <div class="mt-5 space-y-1.5">
                <p class="text-xl font-extrabold text-slate-900 line-clamp-1">{{ top1?.name || 'Đang chờ' }}</p>
                <p class="text-sm text-slate-600">{{ top1 ? top1.time : 'Chưa có ai hoàn thành' }}</p>
                <p class="text-3xl font-black text-amber-700">{{ top1 ? `${top1.score} điểm` : '--' }}</p>
              </div>
            </div>

            <!-- Hạng 3 -->
            <div class="flex flex-col items-center rounded-2xl border-2 border-orange-200 bg-gradient-to-b from-orange-50 to-white px-6 py-8 text-center shadow min-h-[280px]">
              <div class="flex items-center gap-2 text-sm font-semibold text-amber-600">
                <span class="text-lg">🥉</span>
                <span>Hạng 3</span>
              </div>
              <div class="mt-4 flex h-24 w-24 items-center justify-center rounded-full border-2 border-orange-200 bg-orange-50 shadow-inner overflow-hidden">
                <template v-if="top3">
                  <img :src="avatarOf(top3.name, top3.avatar, top3.gender)" alt="avatar" class="h-full w-full object-cover" />
                </template>
                <span v-else class="text-4xl font-bold text-orange-200">?</span>
              </div>
              <div class="mt-5 space-y-1">
                <p class="text-lg font-bold text-slate-900 line-clamp-1">{{ top3?.name || 'Chưa có' }}</p>
                <p class="text-sm text-slate-500">{{ top3 ? top3.time : 'Đang chờ...' }}</p>
                <p class="text-2xl font-bold text-amber-700">{{ top3 ? `${top3.score} điểm` : '--' }}</p>
              </div>
            </div>
          </div>

          <div class="mt-8 rounded-[22px] border border-amber-100 bg-gradient-to-r from-amber-50 via-white to-sky-50 p-5 shadow">
            <div v-if="me" class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
              <div class="flex items-center gap-4">
                <div class="flex h-14 w-14 items-center justify-center rounded-full bg-white text-lg font-bold text-amber-700 shadow-inner border border-amber-100">#{{ me.rank }}</div>
                <div class="flex items-center gap-3">
                  <img :src="meAvatarSrc" alt="avatar" class="h-12 w-12 rounded-full object-cover border border-white shadow" />
                  <div>
                    <p class="text-sm font-semibold text-slate-500">Vị trí của bạn</p>
                    <p class="text-xl font-bold text-slate-900">Top {{ me.rank }}</p>
                  </div>
                </div>
              </div>
              <div class="grid flex-1 grid-cols-3 gap-3 text-center text-sm text-slate-600">
                <div class="rounded-lg bg-white/70 px-3 py-3 shadow-sm border border-amber-50">
                  <p class="text-lg font-bold text-amber-700">{{ me.correct }}/{{ me.total }}</p>
                  <p>Câu đúng</p>
                </div>
                <div class="rounded-lg bg-white/70 px-3 py-3 shadow-sm border border-amber-50">
                  <p class="text-lg font-bold text-slate-900">{{ meTime }}</p>
                  <p>Thời gian</p>
                </div>
                <div class="rounded-lg bg-white/70 px-3 py-3 shadow-sm border border-amber-50">
                  <p class="text-lg font-bold text-emerald-700">{{ me.score }}</p>
                  <p>Điểm</p>
                </div>
              </div>
            </div>
            <div v-else class="flex flex-col items-start gap-2 text-sm text-slate-600 sm:flex-row sm:items-center sm:justify-between">
              <div class="flex items-center gap-3">
                <div class="h-10 w-10 rounded-full bg-white text-slate-400 grid place-items-center border border-dashed border-slate-200">?</div>
                <div>
                  <p class="text-base font-semibold text-slate-900">Chưa có vị trí của bạn</p>
                  <p class="text-sm text-slate-600">Hoàn thành bài thi để xuất hiện trên bảng xếp hạng.</p>
                </div>
              </div>
              <router-link
                v-if="examId"
                :to="{ name: 'student-exam-detail', params: { id: examId } }"
                class="inline-flex items-center justify-center rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50 transition"
              >
                Bắt đầu làm bài
              </router-link>
            </div>
          </div>
        </section>

        <!-- Danh sách từ hạng 4 trở đi -->
        <section v-if="restRows.length > 0" class="rounded-2xl border border-slate-200 bg-white p-6 shadow-lg shadow-slate-200/60">
          <div class="mb-4 flex items-center justify-between border-b border-slate-100 pb-3">
            <div>
              <h3 class="text-lg font-bold text-slate-900">Bảng xếp hạng đầy đủ</h3>
              <p class="text-sm text-slate-600 mt-1">Tổng cộng {{ rows.length }} học viên đã hoàn thành</p>
            </div>
          </div>
          <div
            v-for="(row, index) in paginatedRestRows"
            :key="row.id || row.name + '-' + getRestRank(index)"
            class="mb-3 flex flex-col gap-3 rounded-xl border border-slate-100 bg-slate-50/60 px-4 py-3 shadow-sm last:mb-0 sm:flex-row sm:items-center sm:justify-between hover:border-amber-100 hover:bg-amber-50/40 transition"
          >
            <div class="flex items-center gap-4">
              <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-white text-base font-bold text-slate-700 shadow-inner border border-slate-200">#{{ getRestRank(index) }}</div>
              <div class="flex items-center gap-3">
                <img :src="avatarOf(row.name, row.avatar, row.gender)" alt="avatar" class="h-11 w-11 rounded-full object-cover border border-white shadow" />
                <span class="text-base font-semibold text-slate-900">{{ row.name }}</span>
              </div>
            </div>
            <div class="grid flex-1 grid-cols-3 gap-3 text-center text-sm text-slate-600">
              <div class="rounded-lg bg-white px-3 py-2 shadow-sm border border-slate-100">
                <p class="text-lg font-bold text-slate-900">{{ row.correct }}/{{ row.total }}</p>
                <p>Câu đúng</p>
              </div>
              <div class="rounded-lg bg-white px-3 py-2 shadow-sm border border-slate-100">
                <p class="text-lg font-bold text-slate-900">{{ row.time }}</p>
                <p>Thời gian</p>
              </div>
              <div class="rounded-lg bg-white px-3 py-2 shadow-sm border border-slate-100">
                <p class="text-lg font-bold text-emerald-700">{{ row.score }}</p>
                <p>Điểm</p>
              </div>
            </div>
          </div>
        </section>
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
import { examService } from '@/services/exam.service'
import { getAvatarSrc } from '@/utils/avatar'
import { useAuthStore } from '@/store/auth.store'
import { useRoute } from 'vue-router'
import RankingFireworks from '@/components/ui/RankingFireworks.vue'

// --- TYPES ---
type Exam = { id: number | string; title: string };
type RankRow = { id?: string | number; name: string; avatar?: string; gender?: string; score: number; correct: number; total: number; time: string; attemptId?: string };
type RankMe = { id?: string | number; name?: string; rank: number; score: number; correct: number; total: number; time: string; avatar?: string; gender?: string; attemptId?: string };

// --- STATE ---
const exams = ref<Exam[]>([]);
const examId = ref<Exam['id'] | undefined>();
const route = useRoute()
const auth = useAuthStore()

// 🎆 Fireworks state
const showFireworks = ref(false)
const fireworkIntensity = computed<'low' | 'medium' | 'high'>(() => {
  // Nếu user nằm trong top 3, pháo hoa mạnh hơn
  if (me.value && me.value.rank <= 3) return 'high'
  if (rows.value.length > 0) return 'medium'
  return 'low'
})

const rows = ref<RankRow[]>([]);
const limitedRows = computed(() => rows.value.slice(0, 100)); // Hiển thị tối đa 100 học viên
const me = ref<RankMe | null>(null);
const top1 = computed(() => limitedRows.value[0]);
const top2 = computed(() => limitedRows.value[1]);
const top3 = computed(() => limitedRows.value[2]);
const meTime = computed(() => {
  if (!me.value) return '00:00'
  if (me.value.time) return me.value.time
  const fallback = rows.value.find(r =>
    (r.attemptId && me.value?.attemptId && r.attemptId === me.value.attemptId) ||
    (me.value?.id && r.id && String(r.id) === String(me.value.id))
  )
  return fallback?.time || '00:00'
});

const meAvatarSrc = computed(() => {
  const preferred = (me.value?.avatar && me.value.avatar.toLowerCase() !== 'avatar')
    ? me.value.avatar
    : (auth.user?.avatar || '')
  const gender = (me.value?.gender || auth.user?.gender) as any
  return getAvatarSrc(preferred, gender, 'student')
})

const loading = ref(true);
const err = ref('');

// --- PAGINATION (cho danh sách từ hạng 4) ---
const currentPage = ref(1);
const pageSize = 20; // Tăng số lượng hiển thị mỗi trang
const restRows = computed(() => limitedRows.value.slice(3)); // Bỏ qua top 3, hiển thị từ hạng 4 trở đi

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
function avatarOf(name: string, avatarUrl?: string, gender?: string) {
  // Use provided avatar; otherwise fallback to default avatar (student role)
  const src = getAvatarSrc(avatarUrl || '', (gender as any) || undefined, 'student')
  if (src) return src
  const safe = encodeURIComponent(name || 'User')
  return `https://api.dicebear.com/7.x/initials/svg?seed=${safe}&backgroundColor=e2e8f0&textColor=64748b`
}

// --- DATA LOADERS ---
async function loadExams() {
  err.value = '';
  try {
    const result = await examService.list({ status: 'published', pageSize: 1 });
    exams.value = result.items?.map((ex: any) => ({ id: ex.id, title: ex.title })) || []
    const firstId = result.items?.[0]?.id;
    if (firstId !== undefined) {
      examId.value = firstId;
      await loadRanking(firstId);
    } else {
      loading.value = false;
    }
  } catch (e: any) {
    err.value = e?.message || String(e);
    console.error('Load exams error:', e);
    loading.value = false;
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
    // Map API response to component format and sort by score (descending)
    const mappedRows = (r.top || []).map((item: any) => ({
      id: item.id,
      name: item.name || 'Học viên',
      attemptId: item.attemptId || item.attempt_id,
      avatar: item.avatar || item.avatar_url || item.photo || '',
      gender: item.gender || '',
      score: item.score || 0,
      correct: item.correct || 0,
      total: item.total || 0,
      time: formatTime(item.time) || '00:00',
    }));
    // Sort by score descending (highest first), then by time ascending (faster first)
    rows.value = mappedRows.sort((a, b) => {
      if (b.score !== a.score) return b.score - a.score;
      // If scores are equal, sort by time (faster time first)
      return a.time.localeCompare(b.time);
    });
    
    // Map my stats
    if (r.me) {
      me.value = {
        id: r.me.id || r.me.student_id,
        name: r.me.name || r.me.student_name,
        rank: r.me.rank || 0,
        score: r.me.score || 0,
        correct: r.me.correct || 0,
        total: r.me.total || 0,
        time: formatTime(r.me.time) || '00:00',
        attemptId: r.me.attemptId || r.me.attempt_id,
        avatar: r.me.avatar || r.me.avatar_url || r.me.photo || '',
        gender: r.me.gender || '',
      };
    } else {
      me.value = null;
    }
    // 🎆 Bật pháo hoa khi có dữ liệu ranking
    if (rows.value.length > 0) {
      setTimeout(() => {
        showFireworks.value = true
        // Tắt pháo hoa sau 8 giây
        setTimeout(() => {
          showFireworks.value = false
        }, 8000)
      }, 500)
    }
  } catch (e: any) {
    err.value = e?.message || String(e);
    console.error('Load ranking error:', e);
  } finally {
    loading.value = false;
  }
}

// Format time from seconds or MM:SS string
function formatTime(time: string | number | undefined): string {
  if (!time) return '00:00';
  
  // Handle number (seconds)
  if (typeof time === 'number') {
    // Ensure non-negative
    const absTime = Math.abs(time);
    const minutes = Math.floor(absTime / 60);
    const seconds = Math.floor(absTime % 60);
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  }
  
  // If already in MM:SS format, validate and return
  if (typeof time === 'string' && time.includes(':')) {
    const parts = time.split(':');
    if (parts.length === 2) {
      const minutes = parseInt(parts[0], 10);
      const seconds = parseInt(parts[1], 10);
      // If negative, return 00:00
      if (!isNaN(minutes) && !isNaN(seconds) && minutes >= 0 && seconds >= 0) {
        return `${Math.abs(minutes).toString().padStart(2, '0')}:${Math.abs(seconds).toString().padStart(2, '0')}`;
      }
    }
    // If format is invalid or negative, return 00:00
    return '00:00';
  }
  
  // Try to parse as seconds
  const seconds = parseInt(String(time), 10);
  if (!isNaN(seconds)) {
    // Ensure non-negative
    const absSeconds = Math.abs(seconds);
    const minutes = Math.floor(absSeconds / 60);
    const secs = Math.floor(absSeconds % 60);
    return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }
  
  return '00:00';
}

// --- LIFECYCLE ---
onMounted(() => {
  const idFromRoute = (route.query?.examId || route.query?.id || (window.history.state && (window.history.state as any).current?.params?.id)) as string | undefined
  if (idFromRoute) {
    examId.value = idFromRoute
    loadRanking(idFromRoute)
  } else {
    loadExams()
  }
});

watch(examId, (id, prev) => { 
  if (id !== undefined && id !== prev) loadRanking(id) 
});
</script>
