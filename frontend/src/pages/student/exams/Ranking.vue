<template>
  <div class="ranking-page" :class="isDark ? 'dark-mode' : 'light-mode'">
    <!-- Cosmic Background Effects -->
    <div class="cosmic-bg">
      <!-- Deep Space Background -->
      <div class="space-gradient"></div>
      
      <!-- Nebula Clouds -->
      <div class="nebula nebula-1"></div>
      <div class="nebula nebula-2"></div>
      <div class="nebula nebula-3"></div>
      
      <!-- Twinkling Stars Field -->
      <div class="star-field">
        <div v-for="i in 100" :key="'star'+i" class="cosmic-star" 
          :style="{ 
            '--x': `${Math.random() * 100}%`, 
            '--y': `${Math.random() * 100}%`, 
            '--size': `${1 + Math.random() * 2}px`,
            '--duration': `${2 + Math.random() * 3}s`,
            '--delay': `${Math.random() * 3}s`
          }"></div>
      </div>
      
      <!-- Shooting Stars -->
      <div class="shooting-stars">
        <div v-for="i in 5" :key="'shoot'+i" class="shooting-star"
          :style="{ '--delay': `${i * 3}s`, '--top': `${10 + Math.random() * 40}%` }"></div>
      </div>
      
      <!-- Floating Planets -->
      <div class="planets">
        <div class="planet planet-1">🪐</div>
        <div class="planet planet-2">🌙</div>
        <div class="planet planet-3">✨</div>
      </div>
      
      <!-- Galaxy Spiral -->
      <div class="galaxy"></div>
      
      <!-- Aurora Effect -->
      <div class="aurora">
        <div class="aurora-band aurora-1"></div>
        <div class="aurora-band aurora-2"></div>
        <div class="aurora-band aurora-3"></div>
      </div>
      
      <!-- Cosmic Dust -->
      <div class="cosmic-dust">
        <div v-for="i in 30" :key="'dust'+i" class="dust-particle"
          :style="{ 
            '--x': `${Math.random() * 100}%`, 
            '--delay': `${Math.random() * 10}s`,
            '--size': `${2 + Math.random() * 4}px`
          }"></div>
      </div>
      
      <!-- Constellation Lines -->
      <svg class="constellations" viewBox="0 0 100 100" preserveAspectRatio="none">
        <line x1="10" y1="20" x2="25" y2="15" class="constellation-line" />
        <line x1="25" y1="15" x2="35" y2="25" class="constellation-line" />
        <line x1="35" y1="25" x2="30" y2="40" class="constellation-line" />
        <line x1="70" y1="60" x2="85" y2="55" class="constellation-line" />
        <line x1="85" y1="55" x2="90" y2="70" class="constellation-line" />
      </svg>
    </div>

    <!-- Fireworks -->
    <RankingFireworks :active="showFireworks" :intensity="fireworkIntensity" />

    <div class="page-content">
      <!-- Header with cosmic effect -->
      <header class="page-header cosmic-card">
        <div class="header-shine"></div>
        <div class="cosmic-border"></div>
        <div class="header-content">
          <div class="trophy-icon">
            <span class="trophy-glow">🏆</span>
            <div class="trophy-rays"></div>
            <div class="trophy-orbit">
              <span class="orbit-star">⭐</span>
            </div>
          </div>
          <div>
            <h1 class="title-gradient cosmic-title">Bảng Xếp Hạng</h1>
            <p>Vinh danh những học viên có thành tích xuất sắc nhất trong mỗi kỳ thi.</p>
          </div>
        </div>
      </header>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="cosmic-loader">
          <div class="loader-planet"></div>
          <div class="loader-ring"></div>
          <div class="loader-ring ring-2"></div>
        </div>
        <p>Đang tải bảng xếp hạng...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="rows.length === 0" class="empty-state cosmic-card">
        <div class="empty-icon pulse-icon">🚀</div>
        <h3>Chưa có dữ liệu xếp hạng</h3>
        <p>Hiện chưa có ai hoàn thành đề thi này. Hãy là người đầu tiên!</p>
        <router-link v-if="examId" :to="{ name: 'student-exam-detail', params: { id: examId } }" class="start-btn cosmic-btn">
          <span>🚀 Bắt đầu khám phá</span>
          <div class="btn-shine"></div>
        </router-link>
      </div>

      <!-- Main Content -->
      <div v-else class="main-content">
        <!-- Podium Section -->
        <section class="podium-section cosmic-card">
          <div class="section-glow"></div>
          <div class="podium-stars"></div>
          <div class="podium-container">
            <!-- Rank 2 -->
            <div class="podium-item rank-2 slide-up" :class="{ 'has-data': top2 }">
              <div class="podium-card">
                <div class="card-shine"></div>
                <div class="rank-badge silver shimmer">
                  <span class="medal bounce-medal">🥈</span>
                  <span>Hạng 2</span>
                </div>
                <div class="avatar-wrapper silver">
                  <div class="avatar-ring"></div>
                  <div class="avatar-orbit">
                    <span v-for="i in 3" :key="i" class="orbit-dot"></span>
                  </div>
                  <div class="avatar">
                    <img v-if="top2" :src="avatarOf(top2.name, top2.avatar, top2.gender)" alt="avatar" />
                    <span v-else class="placeholder">?</span>
                  </div>
                </div>
                <div class="user-info">
                  <h3>{{ top2?.name || 'Chưa có' }}</h3>
                  <p class="time">{{ top2 ? top2.time : 'Đang chờ...' }}</p>
                  <div class="score silver counter-animate">{{ top2 ? `${top2.score} điểm` : '--' }}</div>
                </div>
              </div>
              <div class="podium-stand silver">
                <div class="stand-shine"></div>
                <span>2</span>
              </div>
            </div>

            <!-- Rank 1 - Champion -->
            <div class="podium-item rank-1 slide-up" :class="{ 'has-data': top1 }">
              <div class="champion-effects">
                <div class="crown-wrapper">
                  <span class="crown">👑</span>
                  <div class="crown-sparkles">
                    <span v-for="i in 5" :key="i" class="crown-spark">✨</span>
                  </div>
                </div>
                <div class="light-rays">
                  <div v-for="i in 12" :key="i" class="ray" :style="{ '--rotation': `${i * 30}deg` }"></div>
                </div>
              </div>
              <div class="podium-card champion">
                <div class="card-shine gold-shine"></div>
                <div class="champion-border"></div>
                <div class="rank-badge gold shimmer">
                  <span class="medal bounce-medal">🥇</span>
                  <span>Hạng 1</span>
                </div>
                <div class="avatar-wrapper gold">
                  <div class="avatar-ring"></div>
                  <div class="avatar-glow"></div>
                  <div class="avatar-pulse"></div>
                  <div class="avatar-orbit gold-orbit">
                    <span v-for="i in 5" :key="i" class="orbit-dot"></span>
                  </div>
                  <div class="avatar">
                    <img v-if="top1" :src="avatarOf(top1.name, top1.avatar, top1.gender)" alt="avatar" />
                    <span v-else class="placeholder">?</span>
                  </div>
                </div>
                <div class="user-info">
                  <h3 class="champion-name">{{ top1?.name || 'Đang chờ' }}</h3>
                  <p class="time">{{ top1 ? top1.time : 'Chưa có ai hoàn thành' }}</p>
                  <div class="score gold counter-animate glow-text">{{ top1 ? `${top1.score} điểm` : '--' }}</div>
                </div>
              </div>
              <div class="podium-stand gold">
                <div class="stand-shine gold-stand-shine"></div>
                <div class="stand-glow"></div>
                <span>1</span>
              </div>
            </div>

            <!-- Rank 3 -->
            <div class="podium-item rank-3 slide-up" :class="{ 'has-data': top3 }">
              <div class="podium-card">
                <div class="card-shine"></div>
                <div class="rank-badge bronze shimmer">
                  <span class="medal bounce-medal">🥉</span>
                  <span>Hạng 3</span>
                </div>
                <div class="avatar-wrapper bronze">
                  <div class="avatar-ring"></div>
                  <div class="avatar-orbit">
                    <span v-for="i in 3" :key="i" class="orbit-dot"></span>
                  </div>
                  <div class="avatar">
                    <img v-if="top3" :src="avatarOf(top3.name, top3.avatar, top3.gender)" alt="avatar" />
                    <span v-else class="placeholder">?</span>
                  </div>
                </div>
                <div class="user-info">
                  <h3>{{ top3?.name || 'Chưa có' }}</h3>
                  <p class="time">{{ top3 ? top3.time : 'Đang chờ...' }}</p>
                  <div class="score bronze counter-animate">{{ top3 ? `${top3.score} điểm` : '--' }}</div>
                </div>
              </div>
              <div class="podium-stand bronze">
                <div class="stand-shine"></div>
                <span>3</span>
              </div>
            </div>
          </div>
        </section>

        <!-- My Position Card -->
        <section class="my-position-section">
          <div class="my-position-card cosmic-card" :class="{ 'has-rank': me }">
            <div class="cosmic-border"></div>
            <div v-if="me" class="position-content">
              <div class="rank-display">
                <div class="rank-number pulse-rank">
                  <span>#{{ me.rank }}</span>
                  <div class="rank-glow"></div>
                </div>
                <div class="rank-info">
                  <div class="avatar-mini-wrapper">
                    <img :src="meAvatarSrc" alt="avatar" class="my-avatar" />
                    <div class="avatar-mini-ring"></div>
                  </div>
                  <div>
                    <span class="label">Vị trí của bạn</span>
                    <span class="value">Top {{ me.rank }}</span>
                  </div>
                </div>
              </div>
              <div class="stats-grid">
                <div class="stat-item hover-lift">
                  <div class="stat-value correct">{{ me.correct }}/{{ me.total }}</div>
                  <div class="stat-label">Câu đúng</div>
                </div>
                <div class="stat-item hover-lift">
                  <div class="stat-value">{{ meTime }}</div>
                  <div class="stat-label">Thời gian</div>
                </div>
                <div class="stat-item hover-lift highlight-stat">
                  <div class="stat-value score">{{ me.score }}</div>
                  <div class="stat-label">Điểm</div>
                </div>
              </div>
            </div>
            <div v-else class="no-position">
              <div class="no-rank-icon pulse-icon">?</div>
              <div class="no-rank-text">
                <h4>Chưa có vị trí của bạn</h4>
                <p>Hoàn thành bài thi để xuất hiện trên bảng xếp hạng.</p>
              </div>
              <router-link v-if="examId" :to="{ name: 'student-exam-detail', params: { id: examId } }" class="start-btn glow-btn">
                <span>Bắt đầu làm bài</span>
                <div class="btn-shine"></div>
              </router-link>
            </div>
          </div>
        </section>

        <!-- Full Rankings List -->
        <section v-if="restRows.length > 0" class="rankings-list-section">
          <div class="section-header">
            <h2>📋 Bảng xếp hạng đầy đủ</h2>
            <p>Tổng cộng <strong>{{ rows.length }}</strong> học viên đã hoàn thành</p>
          </div>
          
          <div class="rankings-list">
            <div v-for="(row, index) in paginatedRestRows" :key="row.id || row.name + '-' + getRestRank(index)" class="ranking-row hover-row" :style="{ '--delay': `${index * 0.05}s` }">
              <div class="row-left">
                <div class="row-rank">#{{ getRestRank(index) }}</div>
                <div class="row-avatar-wrapper">
                  <img :src="avatarOf(row.name, row.avatar, row.gender)" alt="avatar" class="row-avatar" />
                </div>
                <span class="row-name">{{ row.name }}</span>
              </div>
              <div class="row-stats">
                <div class="row-stat">
                  <span class="stat-num">{{ row.correct }}/{{ row.total }}</span>
                  <span class="stat-text">Câu đúng</span>
                </div>
                <div class="row-stat">
                  <span class="stat-num">{{ row.time }}</span>
                  <span class="stat-text">Thời gian</span>
                </div>
                <div class="row-stat highlight">
                  <span class="stat-num">{{ row.score }}</span>
                  <span class="stat-text">Điểm</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Pagination -->
          <div v-if="totalPages > 1" class="pagination">
            <button class="page-btn" :disabled="currentPage <= 1" @click="handlePageChange(currentPage - 1)">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg>
            </button>
            <button v-for="p in pagesToShow" :key="p.key" class="page-btn" :class="{ active: p.num === currentPage, sep: p.sep }" :disabled="p.sep" @click="!p.sep && handlePageChange(p.num!)">
              {{ p.text }}
            </button>
            <button class="page-btn" :disabled="currentPage >= totalPages" @click="handlePageChange(currentPage + 1)">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>
            </button>
          </div>
        </section>
      </div>

      <!-- Error -->
      <div v-if="err" class="error-message">{{ err }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch, computed } from 'vue'
import { examService } from '@/services/exam.service'
import { getAvatarSrc } from '@/utils/avatar'
import { useAuthStore } from '@/store/auth.store'
import { useThemeStore } from '@/store/theme.store'
import { useRoute } from 'vue-router'
import RankingFireworks from '@/components/ui/RankingFireworks.vue'

const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)

const confettiColors = ['#fbbf24', '#f59e0b', '#06b6d4', '#8b5cf6', '#22c55e', '#ef4444', '#ec4899']
const showConfetti = ref(false)

type Exam = { id: number | string; title: string }
type RankRow = { id?: string | number; name: string; avatar?: string; gender?: string; score: number; correct: number; total: number; time: string; attemptId?: string }
type RankMe = { id?: string | number; name?: string; rank: number; score: number; correct: number; total: number; time: string; avatar?: string; gender?: string; attemptId?: string }

const exams = ref<Exam[]>([])
const examId = ref<Exam['id'] | undefined>()
const route = useRoute()
const auth = useAuthStore()

const showFireworks = ref(false)
const fireworkIntensity = computed<'low' | 'medium' | 'high'>(() => {
  if (me.value && me.value.rank <= 3) return 'high'
  if (rows.value.length > 0) return 'medium'
  return 'low'
})

const rows = ref<RankRow[]>([])
const limitedRows = computed(() => rows.value.slice(0, 100))
const me = ref<RankMe | null>(null)
const top1 = computed(() => limitedRows.value[0])
const top2 = computed(() => limitedRows.value[1])
const top3 = computed(() => limitedRows.value[2])
const meTime = computed(() => {
  if (!me.value) return '00:00'
  if (me.value.time) return me.value.time
  const fallback = rows.value.find(r =>
    (r.attemptId && me.value?.attemptId && r.attemptId === me.value.attemptId) ||
    (me.value?.id && r.id && String(r.id) === String(me.value.id))
  )
  return fallback?.time || '00:00'
})

const meAvatarSrc = computed(() => {
  const preferred = (me.value?.avatar && me.value.avatar.toLowerCase() !== 'avatar')
    ? me.value.avatar
    : (auth.user?.avatar || '')
  const gender = (me.value?.gender || auth.user?.gender) as any
  return getAvatarSrc(preferred, gender, 'student')
})

const loading = ref(true)
const err = ref('')
const currentPage = ref(1)
const pageSize = 20
const restRows = computed(() => limitedRows.value.slice(3))
const paginatedRestRows = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return restRows.value.slice(start, start + pageSize)
})
const totalPages = computed(() => Math.max(1, Math.ceil(restRows.value.length / pageSize)))

function handlePageChange(page: number) {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
}

function getRestRank(indexOnPage: number) {
  return (currentPage.value - 1) * pageSize + indexOnPage + 4
}

const pagesToShow = computed(() => {
  const max = totalPages.value
  const cur = currentPage.value
  const arr: { key: string; num?: number; text: string; sep?: boolean }[] = []
  const push = (n: number) => arr.push({ key: 'p' + n, num: n, text: String(n) })
  const sep = (k: string) => arr.push({ key: k, text: '…', sep: true })
  if (max <= 7) { for (let i = 1; i <= max; i++) push(i) }
  else {
    push(1)
    const start = Math.max(2, cur - 1), end = Math.min(max - 1, cur + 1)
    if (start > 2) sep('s')
    for (let i = start; i <= end; i++) push(i)
    if (end < max - 1) sep('e')
    push(max)
  }
  return arr
})

function avatarOf(name: string, avatarUrl?: string, gender?: string) {
  const src = getAvatarSrc(avatarUrl || '', (gender as any) || undefined, 'student')
  if (src) return src
  return `https://api.dicebear.com/7.x/initials/svg?seed=${encodeURIComponent(name || 'User')}&backgroundColor=e2e8f0&textColor=64748b`
}

async function loadExams() {
  err.value = ''
  try {
    const result = await examService.list({ status: 'published', pageSize: 1 })
    exams.value = result.items?.map((ex: any) => ({ id: ex.id, title: ex.title })) || []
    const firstId = result.items?.[0]?.id
    if (firstId !== undefined) { examId.value = firstId; await loadRanking(firstId) }
    else { loading.value = false }
  } catch (e: any) { err.value = e?.message || String(e); loading.value = false }
}

async function loadRanking(id: Exam['id']) {
  if (!id && id !== 0) { rows.value = []; me.value = null; return }
  loading.value = true; rows.value = []; me.value = null; err.value = ''; currentPage.value = 1
  try {
    const r = await examService.ranking(id)
    rows.value = (r.top || []).map((item: any) => ({
      id: item.id, name: item.name || 'Học viên', attemptId: item.attemptId || item.attempt_id,
      avatar: item.avatar || item.avatar_url || item.photo || '', gender: item.gender || '',
      score: item.score || 0, correct: item.correct || 0, total: item.total || 0, time: formatTime(item.time) || '00:00',
    })).sort((a, b) => b.score !== a.score ? b.score - a.score : a.time.localeCompare(b.time))
    if (r.me) {
      me.value = {
        id: r.me.id || r.me.student_id, name: r.me.name || r.me.student_name, rank: r.me.rank || 0,
        score: r.me.score || 0, correct: r.me.correct || 0, total: r.me.total || 0,
        time: formatTime(r.me.time) || '00:00', attemptId: r.me.attemptId || r.me.attempt_id,
        avatar: r.me.avatar || r.me.avatar_url || r.me.photo || '', gender: r.me.gender || '',
      }
    }
    if (rows.value.length > 0) {
      setTimeout(() => { showFireworks.value = true; showConfetti.value = true
        setTimeout(() => { showFireworks.value = false; showConfetti.value = false }, 8000)
      }, 500)
    }
  } catch (e: any) { err.value = e?.message || String(e) }
  finally { loading.value = false }
}

function formatTime(time: string | number | undefined): string {
  if (!time) return '00:00'
  if (typeof time === 'number') { const m = Math.floor(Math.abs(time) / 60), s = Math.floor(Math.abs(time) % 60); return `${m.toString().padStart(2,'0')}:${s.toString().padStart(2,'0')}` }
  if (typeof time === 'string' && time.includes(':')) { const [m, s] = time.split(':').map(x => parseInt(x, 10)); if (!isNaN(m) && !isNaN(s)) return `${Math.abs(m).toString().padStart(2,'0')}:${Math.abs(s).toString().padStart(2,'0')}`; return '00:00' }
  const sec = parseInt(String(time), 10); if (!isNaN(sec)) { const m = Math.floor(Math.abs(sec) / 60), s = Math.floor(Math.abs(sec) % 60); return `${m.toString().padStart(2,'0')}:${s.toString().padStart(2,'0')}` }
  return '00:00'
}

onMounted(() => {
  const idFromRoute = (route.query?.examId || route.query?.id || (window.history.state as any)?.current?.params?.id) as string | undefined
  if (idFromRoute) { examId.value = idFromRoute; loadRanking(idFromRoute) } else { loadExams() }
})
watch(examId, (id, prev) => { if (id !== undefined && id !== prev) loadRanking(id) })
</script>

<style scoped>
.ranking-page { min-height: 100vh; position: relative; padding: 24px; padding-bottom: 80px; transition: all 0.3s ease; overflow-x: hidden; }
.ranking-page.dark-mode { background: #020617; }
.ranking-page.light-mode { background: linear-gradient(180deg, #f0f4ff 0%, #e8f0fe 100%); }

/* ========== COSMIC BACKGROUND ========== */
.cosmic-bg { position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden; }

/* Deep Space Gradient */
.space-gradient { position: absolute; inset: 0; background: radial-gradient(ellipse at 20% 20%, rgba(88, 28, 135, 0.3) 0%, transparent 50%), radial-gradient(ellipse at 80% 80%, rgba(30, 58, 138, 0.3) 0%, transparent 50%), radial-gradient(ellipse at 50% 50%, rgba(6, 78, 59, 0.15) 0%, transparent 60%); }
.light-mode .space-gradient { display: none; }

/* Nebula Clouds */
.nebula { position: absolute; border-radius: 50%; filter: blur(80px); animation: nebula-drift 20s ease-in-out infinite; }
.dark-mode .nebula-1 { top: 5%; left: -10%; width: 500px; height: 400px; background: linear-gradient(135deg, rgba(139, 92, 246, 0.25), rgba(236, 72, 153, 0.15)); }
.dark-mode .nebula-2 { bottom: 10%; right: -15%; width: 600px; height: 500px; background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(34, 197, 94, 0.1)); animation-delay: -7s; }
.dark-mode .nebula-3 { top: 40%; left: 30%; width: 400px; height: 350px; background: linear-gradient(135deg, rgba(251, 191, 36, 0.15), rgba(249, 115, 22, 0.1)); animation-delay: -12s; }
.light-mode .nebula { display: none; }
@keyframes nebula-drift { 0%, 100% { transform: translate(0, 0) scale(1) rotate(0deg); } 33% { transform: translate(30px, -20px) scale(1.1) rotate(5deg); } 66% { transform: translate(-20px, 30px) scale(0.95) rotate(-5deg); } }

/* Twinkling Stars */
.star-field { position: absolute; inset: 0; }
.cosmic-star { position: absolute; left: var(--x); top: var(--y); width: var(--size); height: var(--size); border-radius: 50%; animation: twinkle var(--duration) ease-in-out infinite; animation-delay: var(--delay); }
.dark-mode .cosmic-star { background: white; box-shadow: 0 0 4px white, 0 0 8px rgba(255,255,255,0.5); }
.light-mode .cosmic-star { display: none; }
@keyframes twinkle { 0%, 100% { opacity: 0.3; transform: scale(0.8); } 50% { opacity: 1; transform: scale(1.2); } }

/* Shooting Stars */
.shooting-stars { position: absolute; inset: 0; }
.shooting-star { position: absolute; top: var(--top); left: -100px; width: 100px; height: 2px; background: linear-gradient(90deg, transparent, white, transparent); animation: shoot 6s linear infinite; animation-delay: var(--delay); opacity: 0; }
.shooting-star::before { content: ''; position: absolute; right: 0; top: -2px; width: 6px; height: 6px; border-radius: 50%; background: white; box-shadow: 0 0 10px white, 0 0 20px #06b6d4; }
.light-mode .shooting-star { display: none; }
@keyframes shoot { 0% { left: -100px; opacity: 0; } 5% { opacity: 1; } 30% { left: 110%; opacity: 1; } 31%, 100% { opacity: 0; left: 110%; } }

/* Floating Planets */
.planets { position: absolute; inset: 0; }
.planet { position: absolute; font-size: 30px; animation: planet-float 15s ease-in-out infinite; filter: drop-shadow(0 0 20px rgba(139, 92, 246, 0.5)); }
.planet-1 { top: 15%; right: 10%; animation-delay: 0s; }
.planet-2 { bottom: 20%; left: 8%; font-size: 24px; animation-delay: -5s; }
.planet-3 { top: 50%; right: 20%; font-size: 18px; animation-delay: -10s; }
.light-mode .planet { opacity: 0.3; }
@keyframes planet-float { 0%, 100% { transform: translateY(0) rotate(0deg); } 50% { transform: translateY(-30px) rotate(10deg); } }

/* Galaxy Spiral */
.galaxy { position: absolute; top: 60%; left: 5%; width: 200px; height: 200px; background: conic-gradient(from 0deg, transparent, rgba(139, 92, 246, 0.1), transparent, rgba(6, 182, 212, 0.1), transparent); border-radius: 50%; animation: galaxy-spin 60s linear infinite; filter: blur(20px); }
.light-mode .galaxy { display: none; }
@keyframes galaxy-spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

/* Aurora Effect */
.aurora { position: absolute; top: 0; left: 0; right: 0; height: 40%; pointer-events: none; }
.aurora-band { position: absolute; width: 100%; height: 100%; opacity: 0.3; filter: blur(60px); }
.aurora-1 { background: linear-gradient(180deg, transparent, rgba(34, 197, 94, 0.2), transparent); animation: aurora-wave 8s ease-in-out infinite; }
.aurora-2 { background: linear-gradient(180deg, transparent, rgba(6, 182, 212, 0.15), transparent); animation: aurora-wave 10s ease-in-out infinite; animation-delay: -3s; }
.aurora-3 { background: linear-gradient(180deg, transparent, rgba(139, 92, 246, 0.15), transparent); animation: aurora-wave 12s ease-in-out infinite; animation-delay: -6s; }
.light-mode .aurora { display: none; }
@keyframes aurora-wave { 0%, 100% { transform: translateX(-20%) scaleY(1); } 50% { transform: translateX(20%) scaleY(1.3); } }

/* Cosmic Dust */
.cosmic-dust { position: absolute; inset: 0; }
.dust-particle { position: absolute; left: var(--x); width: var(--size); height: var(--size); border-radius: 50%; animation: dust-float 20s linear infinite; animation-delay: var(--delay); }
.dark-mode .dust-particle { background: rgba(251, 191, 36, 0.4); box-shadow: 0 0 6px rgba(251, 191, 36, 0.6); }
.light-mode .dust-particle { display: none; }
@keyframes dust-float { 0% { transform: translateY(100vh) rotate(0deg); opacity: 0; } 10% { opacity: 0.8; } 90% { opacity: 0.8; } 100% { transform: translateY(-100px) rotate(360deg); opacity: 0; } }

/* Constellation Lines */
.constellations { position: absolute; inset: 0; width: 100%; height: 100%; }
.constellation-line { stroke: rgba(255, 255, 255, 0.1); stroke-width: 0.1; stroke-dasharray: 2 2; animation: constellation-glow 4s ease-in-out infinite; }
.light-mode .constellations { display: none; }
@keyframes constellation-glow { 0%, 100% { opacity: 0.3; } 50% { opacity: 0.8; } }

.page-content { position: relative; z-index: 10; max-width: 1100px; margin: 0 auto; }

/* Cosmic Card Style */
.cosmic-card { position: relative; overflow: hidden; }
.cosmic-border { position: absolute; inset: 0; border-radius: inherit; padding: 2px; background: linear-gradient(135deg, rgba(139, 92, 246, 0.5), rgba(6, 182, 212, 0.5), rgba(251, 191, 36, 0.5)); mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0); mask-composite: exclude; animation: border-shimmer 4s linear infinite; pointer-events: none; }
@keyframes border-shimmer { 0% { filter: hue-rotate(0deg); } 100% { filter: hue-rotate(360deg); } }
.light-mode .cosmic-border { opacity: 0.5; }

/* Header */
.page-header { margin-bottom: 32px; padding: 28px 32px; border-radius: 24px; position: relative; }
.dark-mode .page-header { background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.8) 100%); border: 1px solid rgba(139, 92, 246, 0.2); box-shadow: 0 8px 32px rgba(139, 92, 246, 0.15), inset 0 1px 0 rgba(255,255,255,0.05); }
.light-mode .page-header { background: rgba(255,255,255,0.9); border: 1px solid #e2e8f0; box-shadow: 0 8px 32px rgba(0,0,0,0.08); backdrop-filter: blur(10px); }

.header-shine { position: absolute; top: 0; left: -100%; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.1), rgba(6, 182, 212, 0.1), transparent); animation: shine-move 4s ease-in-out infinite; }
@keyframes shine-move { 0% { left: -100%; } 100% { left: 100%; } }

.header-content { display: flex; align-items: center; gap: 20px; position: relative; z-index: 1; }
.trophy-icon { position: relative; }
.trophy-glow { font-size: 52px; display: block; animation: trophy-bounce 2s ease-in-out infinite; filter: drop-shadow(0 0 25px rgba(251, 191, 36, 0.6)) drop-shadow(0 0 50px rgba(251, 191, 36, 0.3)); }
@keyframes trophy-bounce { 0%, 100% { transform: translateY(0) scale(1) rotate(-3deg); } 50% { transform: translateY(-8px) scale(1.05) rotate(3deg); } }
.trophy-rays { position: absolute; inset: -25px; background: radial-gradient(circle, rgba(251, 191, 36, 0.4) 0%, transparent 70%); animation: rays-pulse 2s ease-in-out infinite; border-radius: 50%; }
@keyframes rays-pulse { 0%, 100% { opacity: 0.5; transform: scale(1); } 50% { opacity: 1; transform: scale(1.3); } }
.trophy-orbit { position: absolute; inset: -30px; animation: orbit-spin 8s linear infinite; }
.orbit-star { position: absolute; top: 0; left: 50%; font-size: 12px; transform: translateX(-50%); }
@keyframes orbit-spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

.title-gradient { font-size: 32px; font-weight: 900; margin: 0 0 6px; }
.cosmic-title { background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 25%, #ec4899 50%, #8b5cf6 75%, #06b6d4 100%); background-size: 300% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; animation: cosmic-gradient 5s linear infinite; }
@keyframes cosmic-gradient { 0% { background-position: 0% center; } 100% { background-position: 300% center; } }
.page-header p { font-size: 14px; margin: 0; }
.dark-mode .page-header p { color: #94a3b8; }
.light-mode .page-header p { color: #64748b; }

/* Cosmic Loading */
.loading-state { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 20px; gap: 24px; }
.cosmic-loader { position: relative; width: 80px; height: 80px; }
.loader-planet { position: absolute; inset: 20px; border-radius: 50%; background: linear-gradient(135deg, #fbbf24, #f59e0b); box-shadow: 0 0 30px rgba(251, 191, 36, 0.5), inset -5px -5px 10px rgba(0,0,0,0.3); animation: planet-rotate 4s linear infinite; }
@keyframes planet-rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
.loader-ring { position: absolute; inset: 0; border: 3px solid transparent; border-top-color: #8b5cf6; border-radius: 50%; animation: ring-orbit 2s linear infinite; }
.loader-ring.ring-2 { inset: 8px; border-top-color: #06b6d4; animation-duration: 1.5s; animation-direction: reverse; }
@keyframes ring-orbit { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
.loading-state p { font-size: 14px; }
.dark-mode .loading-state p { color: #94a3b8; }
.light-mode .loading-state p { color: #64748b; }

/* Empty State */
.empty-state { text-align: center; padding: 80px 20px; border-radius: 28px; }
.dark-mode .empty-state { background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(30, 41, 59, 0.8)); border: 1px solid rgba(139, 92, 246, 0.2); }
.light-mode .empty-state { background: rgba(255,255,255,0.9); border: 1px solid #e2e8f0; backdrop-filter: blur(10px); }
.empty-icon { font-size: 80px; margin-bottom: 20px; display: inline-block; }
.pulse-icon { animation: rocket-float 3s ease-in-out infinite; }
@keyframes rocket-float { 0%, 100% { transform: translateY(0) rotate(-10deg); } 50% { transform: translateY(-15px) rotate(10deg); } }
.empty-state h3 { font-size: 22px; font-weight: 700; margin: 0 0 10px; }
.dark-mode .empty-state h3 { color: white; }
.light-mode .empty-state h3 { color: #1e293b; }
.empty-state > p { font-size: 15px; margin: 0 0 28px; }
.dark-mode .empty-state > p { color: #94a3b8; }
.light-mode .empty-state > p { color: #64748b; }

/* Cosmic Button */
.start-btn { display: inline-flex; align-items: center; gap: 8px; padding: 14px 28px; border-radius: 14px; font-size: 15px; font-weight: 600; text-decoration: none; position: relative; overflow: hidden; transition: all 0.3s; }
.cosmic-btn { background: linear-gradient(135deg, #8b5cf6, #06b6d4, #22c55e); background-size: 200% auto; animation: cosmic-btn-bg 3s linear infinite; }
@keyframes cosmic-btn-bg { 0% { background-position: 0% center; } 100% { background-position: 200% center; } }
.dark-mode .start-btn { color: white; box-shadow: 0 4px 20px rgba(139, 92, 246, 0.4); }
.light-mode .start-btn { background: linear-gradient(135deg, #1e293b, #334155); color: white; box-shadow: 0 4px 20px rgba(30, 41, 59, 0.3); }
.start-btn:hover { transform: translateY(-3px) scale(1.02); box-shadow: 0 8px 30px rgba(139, 92, 246, 0.5); }
.btn-shine { position: absolute; top: 0; left: -100%; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent); animation: btn-shine 2s ease-in-out infinite; }
@keyframes btn-shine { 0% { left: -100%; } 100% { left: 100%; } }

/* Podium Section */
.podium-section { margin-bottom: 36px; padding: 50px 28px 0; border-radius: 32px; position: relative; overflow: hidden; }
.dark-mode .podium-section { background: linear-gradient(180deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.9) 100%); border: 1px solid rgba(139, 92, 246, 0.2); box-shadow: 0 12px 40px rgba(139, 92, 246, 0.15), inset 0 1px 0 rgba(255,255,255,0.05); }
.light-mode .podium-section { background: linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(248,250,252,0.9) 100%); border: 1px solid #e2e8f0; box-shadow: 0 12px 40px rgba(0,0,0,0.1); backdrop-filter: blur(10px); }
.section-glow { position: absolute; top: -50%; left: 50%; transform: translateX(-50%); width: 700px; height: 500px; background: radial-gradient(ellipse, rgba(139, 92, 246, 0.15) 0%, rgba(251, 191, 36, 0.1) 30%, transparent 70%); pointer-events: none; animation: section-glow-pulse 4s ease-in-out infinite; }
@keyframes section-glow-pulse { 0%, 100% { opacity: 0.5; transform: translateX(-50%) scale(1); } 50% { opacity: 0.8; transform: translateX(-50%) scale(1.1); } }
.light-mode .section-glow { display: none; }
.podium-stars { position: absolute; inset: 0; background-image: radial-gradient(2px 2px at 20px 30px, rgba(255,255,255,0.3), transparent), radial-gradient(2px 2px at 40px 70px, rgba(255,255,255,0.2), transparent), radial-gradient(1px 1px at 90px 40px, rgba(255,255,255,0.3), transparent), radial-gradient(2px 2px at 130px 80px, rgba(255,255,255,0.2), transparent), radial-gradient(1px 1px at 160px 30px, rgba(255,255,255,0.4), transparent); background-size: 200px 100px; animation: stars-twinkle 4s ease-in-out infinite; }
@keyframes stars-twinkle { 0%, 100% { opacity: 0.5; } 50% { opacity: 1; } }
.light-mode .podium-stars { display: none; }

.podium-container { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; align-items: flex-end; max-width: 950px; margin: 0 auto; position: relative; z-index: 1; }
.podium-item { display: flex; flex-direction: column; align-items: center; }
.podium-item.rank-1 { order: 2; }
.podium-item.rank-2 { order: 1; }
.podium-item.rank-3 { order: 3; }

.slide-up { animation: slide-up 0.8s ease-out forwards; opacity: 0; }
.rank-2 { animation-delay: 0.2s; }
.rank-1 { animation-delay: 0.4s; }
.rank-3 { animation-delay: 0.3s; }
@keyframes slide-up { from { opacity: 0; transform: translateY(40px); } to { opacity: 1; transform: translateY(0); } }

/* Champion Effects */
.champion-effects { position: relative; width: 100%; display: flex; justify-content: center; margin-bottom: -10px; }
.crown-wrapper { position: relative; z-index: 10; }
.crown { font-size: 44px; display: block; animation: crown-float 2.5s ease-in-out infinite; filter: drop-shadow(0 0 15px rgba(251, 191, 36, 0.6)); }
@keyframes crown-float { 0%, 100% { transform: translateY(0) rotate(-5deg); } 50% { transform: translateY(-10px) rotate(5deg); } }
.crown-sparkles { position: absolute; inset: -15px; }
.crown-spark { position: absolute; font-size: 10px; animation: spark-twinkle 1.5s ease-in-out infinite; }
.crown-spark:nth-child(1) { top: 0; left: 20%; animation-delay: 0s; }
.crown-spark:nth-child(2) { top: 10%; right: 15%; animation-delay: 0.3s; }
.crown-spark:nth-child(3) { bottom: 20%; left: 10%; animation-delay: 0.6s; }
.crown-spark:nth-child(4) { bottom: 10%; right: 20%; animation-delay: 0.9s; }
.crown-spark:nth-child(5) { top: 30%; left: 50%; animation-delay: 1.2s; }
@keyframes spark-twinkle { 0%, 100% { opacity: 0; transform: scale(0); } 50% { opacity: 1; transform: scale(1.2); } }

.light-rays { position: absolute; inset: -30px; pointer-events: none; }
.ray { position: absolute; top: 50%; left: 50%; width: 3px; height: 60px; background: linear-gradient(to top, rgba(251, 191, 36, 0.4), transparent); transform-origin: bottom center; transform: rotate(var(--rotation)) translateY(-30px); animation: ray-pulse 2s ease-in-out infinite; }
@keyframes ray-pulse { 0%, 100% { opacity: 0.3; height: 60px; } 50% { opacity: 0.8; height: 80px; } }
.light-mode .light-rays { display: none; }

/* Podium Card */
.podium-card { width: 100%; padding: 28px 18px; border-radius: 24px; text-align: center; position: relative; overflow: hidden; transition: all 0.3s; }
.dark-mode .podium-card { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1); }
.light-mode .podium-card { background: white; border: 1px solid #e2e8f0; box-shadow: 0 4px 20px rgba(0,0,0,0.05); }
.podium-card:hover { transform: translateY(-5px); }

.card-shine { position: absolute; top: 0; left: -100%; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent); animation: card-shine 4s ease-in-out infinite; }
@keyframes card-shine { 0%, 100% { left: -100%; } 50% { left: 100%; } }
.gold-shine { background: linear-gradient(90deg, transparent, rgba(251, 191, 36, 0.15), transparent); }

.podium-card.champion { padding: 36px 22px; }
.dark-mode .podium-card.champion { background: linear-gradient(180deg, rgba(251, 191, 36, 0.12) 0%, rgba(251, 191, 36, 0.03) 100%); border-color: rgba(251, 191, 36, 0.4); }
.light-mode .podium-card.champion { background: linear-gradient(180deg, #fffbeb 0%, #ffffff 100%); border-color: #fcd34d; }
.champion-border { position: absolute; inset: 0; border-radius: 24px; border: 2px solid transparent; background: linear-gradient(135deg, rgba(251, 191, 36, 0.5), rgba(251, 191, 36, 0.1), rgba(251, 191, 36, 0.5)) border-box; mask: linear-gradient(#fff 0 0) padding-box, linear-gradient(#fff 0 0); mask-composite: exclude; animation: border-rotate 4s linear infinite; }
@keyframes border-rotate { from { filter: hue-rotate(0deg); } to { filter: hue-rotate(360deg); } }

/* Rank Badge */
.rank-badge { display: inline-flex; align-items: center; gap: 8px; padding: 8px 16px; border-radius: 24px; font-size: 13px; font-weight: 700; margin-bottom: 18px; position: relative; overflow: hidden; }
.rank-badge.gold { background: linear-gradient(135deg, rgba(251, 191, 36, 0.2), rgba(245, 158, 11, 0.15)); color: #fbbf24; border: 1px solid rgba(251, 191, 36, 0.3); }
.rank-badge.silver { background: rgba(148, 163, 184, 0.15); color: #94a3b8; border: 1px solid rgba(148, 163, 184, 0.2); }
.rank-badge.bronze { background: rgba(251, 146, 60, 0.15); color: #fb923c; border: 1px solid rgba(251, 146, 60, 0.2); }
.shimmer::after { content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent); animation: shimmer 2s infinite; }
@keyframes shimmer { 100% { left: 150%; } }
.medal { font-size: 18px; }
.bounce-medal { animation: medal-bounce 2s ease-in-out infinite; display: inline-block; }
@keyframes medal-bounce { 0%, 100% { transform: translateY(0) rotate(0deg); } 25% { transform: translateY(-3px) rotate(-5deg); } 75% { transform: translateY(-3px) rotate(5deg); } }

/* Avatar */
.avatar-wrapper { position: relative; margin-bottom: 18px; }
.avatar-wrapper.gold .avatar { width: 110px; height: 110px; }
.avatar-wrapper.silver .avatar, .avatar-wrapper.bronze .avatar { width: 88px; height: 88px; }
.avatar { border-radius: 50%; overflow: hidden; display: flex; align-items: center; justify-content: center; margin: 0 auto; position: relative; z-index: 3; transition: transform 0.3s; }
.avatar:hover { transform: scale(1.05); }
.dark-mode .avatar { background: #1e293b; border: 4px solid rgba(255,255,255,0.15); }
.light-mode .avatar { background: #f1f5f9; border: 4px solid #e2e8f0; }
.avatar-wrapper.gold .avatar { border-color: #fbbf24; box-shadow: 0 0 30px rgba(251, 191, 36, 0.4); }
.avatar-wrapper.silver .avatar { border-color: #94a3b8; }
.avatar-wrapper.bronze .avatar { border-color: #fb923c; }
.avatar img { width: 100%; height: 100%; object-fit: cover; }
.avatar .placeholder { font-size: 36px; font-weight: 900; }
.dark-mode .avatar .placeholder { color: #475569; }
.light-mode .avatar .placeholder { color: #cbd5e1; }

.avatar-ring { position: absolute; inset: -8px; border-radius: 50%; border: 2px dashed; animation: ring-spin 15s linear infinite; z-index: 1; }
.avatar-wrapper.gold .avatar-ring { border-color: rgba(251, 191, 36, 0.4); }
.avatar-wrapper.silver .avatar-ring { border-color: rgba(148, 163, 184, 0.3); }
.avatar-wrapper.bronze .avatar-ring { border-color: rgba(251, 146, 60, 0.3); }
@keyframes ring-spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

.avatar-glow { position: absolute; inset: -25px; border-radius: 50%; background: radial-gradient(circle, rgba(251, 191, 36, 0.4) 0%, transparent 70%); animation: avatar-glow-pulse 2s ease-in-out infinite; z-index: 0; }
.avatar-pulse { position: absolute; inset: -15px; border-radius: 50%; border: 2px solid rgba(251, 191, 36, 0.3); animation: avatar-pulse-anim 2s ease-out infinite; z-index: 0; }
@keyframes avatar-glow-pulse { 0%, 100% { opacity: 0.6; transform: scale(1); } 50% { opacity: 1; transform: scale(1.15); } }
@keyframes avatar-pulse-anim { 0% { transform: scale(1); opacity: 1; } 100% { transform: scale(1.5); opacity: 0; } }

/* Avatar Orbit - Cosmic Planet Effect */
.avatar-orbit { position: absolute; inset: -15px; animation: orbit-container 10s linear infinite; z-index: 1; }
.gold-orbit { inset: -20px; animation-duration: 8s; }
.orbit-dot { position: absolute; width: 6px; height: 6px; border-radius: 50%; top: 50%; left: 0; transform: translateY(-50%); }
.avatar-wrapper.gold .orbit-dot { background: #fbbf24; box-shadow: 0 0 10px #fbbf24, 0 0 20px rgba(251, 191, 36, 0.5); }
.avatar-wrapper.silver .orbit-dot { background: #94a3b8; box-shadow: 0 0 8px #94a3b8; }
.avatar-wrapper.bronze .orbit-dot { background: #fb923c; box-shadow: 0 0 8px #fb923c; }
.orbit-dot:nth-child(1) { animation: orbit-dot 10s linear infinite; }
.orbit-dot:nth-child(2) { animation: orbit-dot 10s linear infinite; animation-delay: -3.33s; }
.orbit-dot:nth-child(3) { animation: orbit-dot 10s linear infinite; animation-delay: -6.66s; }
.orbit-dot:nth-child(4) { animation: orbit-dot 10s linear infinite; animation-delay: -2.5s; }
.orbit-dot:nth-child(5) { animation: orbit-dot 10s linear infinite; animation-delay: -5s; }
.gold-orbit .orbit-dot:nth-child(1) { animation-duration: 8s; }
.gold-orbit .orbit-dot:nth-child(2) { animation-duration: 8s; animation-delay: -1.6s; }
.gold-orbit .orbit-dot:nth-child(3) { animation-duration: 8s; animation-delay: -3.2s; }
.gold-orbit .orbit-dot:nth-child(4) { animation-duration: 8s; animation-delay: -4.8s; }
.gold-orbit .orbit-dot:nth-child(5) { animation-duration: 8s; animation-delay: -6.4s; }
@keyframes orbit-container { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes orbit-dot { 0%, 100% { opacity: 1; transform: translateY(-50%) scale(1); } 50% { opacity: 0.5; transform: translateY(-50%) scale(0.6); } }

/* User Info */
.user-info h3 { font-size: 17px; font-weight: 700; margin: 0 0 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 160px; margin-left: auto; margin-right: auto; }
.rank-1 .user-info h3 { font-size: 20px; max-width: 200px; }
.champion-name { background: linear-gradient(135deg, #fbbf24, #f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.dark-mode .user-info h3 { color: white; }
.light-mode .user-info h3 { color: #1e293b; }
.user-info .time { font-size: 13px; margin: 0 0 10px; }
.dark-mode .user-info .time { color: #64748b; }
.light-mode .user-info .time { color: #94a3b8; }
.user-info .score { font-size: 26px; font-weight: 900; }
.rank-1 .user-info .score { font-size: 32px; }
.score.gold { color: #fbbf24; text-shadow: 0 0 20px rgba(251, 191, 36, 0.5); }
.score.silver { color: #94a3b8; }
.score.bronze { color: #fb923c; }
.glow-text { animation: text-glow 2s ease-in-out infinite; }
@keyframes text-glow { 0%, 100% { text-shadow: 0 0 20px rgba(251, 191, 36, 0.5); } 50% { text-shadow: 0 0 30px rgba(251, 191, 36, 0.8), 0 0 40px rgba(251, 191, 36, 0.4); } }
.counter-animate { animation: counter-pop 0.5s ease-out; }
@keyframes counter-pop { 0% { transform: scale(0.5); opacity: 0; } 70% { transform: scale(1.1); } 100% { transform: scale(1); opacity: 1; } }

/* Podium Stand */
.podium-stand { width: 100%; display: flex; align-items: center; justify-content: center; font-size: 36px; font-weight: 900; margin-top: 18px; border-radius: 16px 16px 0 0; position: relative; overflow: hidden; }
.podium-stand.gold { height: 110px; background: linear-gradient(180deg, #fbbf24 0%, #f59e0b 100%); color: white; box-shadow: 0 -5px 30px rgba(251, 191, 36, 0.4); }
.podium-stand.silver { height: 80px; background: linear-gradient(180deg, #94a3b8 0%, #64748b 100%); color: white; }
.podium-stand.bronze { height: 55px; background: linear-gradient(180deg, #fb923c 0%, #ea580c 100%); color: white; }
.stand-shine { position: absolute; top: 0; left: -100%; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent); animation: stand-shine 3s ease-in-out infinite; }
@keyframes stand-shine { 0%, 100% { left: -100%; } 50% { left: 100%; } }
.gold-stand-shine { animation-duration: 2s; }
.stand-glow { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(255,255,255,0.2) 0%, transparent 50%); }

/* My Position Section */
.my-position-section { margin-bottom: 36px; }
.my-position-card { padding: 28px; border-radius: 24px; position: relative; overflow: hidden; }
.dark-mode .my-position-card { background: linear-gradient(135deg, rgba(251, 191, 36, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%); border: 1px solid rgba(251, 191, 36, 0.25); }
.light-mode .my-position-card { background: linear-gradient(135deg, #fffbeb 0%, #f0fdfa 100%); border: 1px solid #fde68a; box-shadow: 0 8px 30px rgba(251, 191, 36, 0.15); }
.card-border-glow { position: absolute; inset: -2px; border-radius: 26px; background: linear-gradient(135deg, rgba(251, 191, 36, 0.4), rgba(6, 182, 212, 0.4)); z-index: -1; animation: border-glow 3s ease-in-out infinite; }
@keyframes border-glow { 0%, 100% { opacity: 0.5; } 50% { opacity: 1; } }
.light-mode .card-border-glow { display: none; }

.position-content { display: flex; align-items: center; justify-content: space-between; gap: 28px; flex-wrap: wrap; }
.rank-display { display: flex; align-items: center; gap: 18px; }
.rank-number { width: 64px; height: 64px; border-radius: 18px; display: flex; align-items: center; justify-content: center; font-size: 22px; font-weight: 900; position: relative; overflow: hidden; }
.dark-mode .rank-number { background: linear-gradient(135deg, rgba(251, 191, 36, 0.2), rgba(251, 191, 36, 0.1)); color: #fbbf24; border: 2px solid rgba(251, 191, 36, 0.4); }
.light-mode .rank-number { background: linear-gradient(135deg, #fef3c7, #fde68a); color: #b45309; border: 2px solid #fcd34d; }
.pulse-rank { animation: rank-pulse 2s ease-in-out infinite; }
@keyframes rank-pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
.rank-glow { position: absolute; inset: 0; background: radial-gradient(circle, rgba(251, 191, 36, 0.3) 0%, transparent 70%); animation: rank-glow-pulse 2s ease-in-out infinite; }
@keyframes rank-glow-pulse { 0%, 100% { opacity: 0.3; } 50% { opacity: 0.8; } }

.rank-info { display: flex; align-items: center; gap: 14px; }
.avatar-mini-wrapper { position: relative; }
.my-avatar { width: 52px; height: 52px; border-radius: 50%; object-fit: cover; }
.dark-mode .my-avatar { border: 3px solid rgba(255,255,255,0.15); }
.light-mode .my-avatar { border: 3px solid white; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.avatar-mini-ring { position: absolute; inset: -4px; border-radius: 50%; border: 2px dashed rgba(251, 191, 36, 0.4); animation: ring-spin 10s linear infinite; }
.rank-info .label { display: block; font-size: 13px; }
.dark-mode .rank-info .label { color: #94a3b8; }
.light-mode .rank-info .label { color: #64748b; }
.rank-info .value { display: block; font-size: 20px; font-weight: 800; }
.dark-mode .rank-info .value { color: white; }
.light-mode .rank-info .value { color: #1e293b; }

.stats-grid { display: flex; gap: 14px; flex: 1; justify-content: flex-end; }
.stat-item { padding: 14px 22px; border-radius: 16px; text-align: center; min-width: 110px; transition: all 0.3s; }
.dark-mode .stat-item { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); }
.light-mode .stat-item { background: white; border: 1px solid #e2e8f0; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
.hover-lift:hover { transform: translateY(-3px); }
.dark-mode .hover-lift:hover { box-shadow: 0 8px 20px rgba(0,0,0,0.3); }
.light-mode .hover-lift:hover { box-shadow: 0 8px 20px rgba(0,0,0,0.1); }
.highlight-stat { position: relative; overflow: hidden; }
.dark-mode .highlight-stat { background: linear-gradient(135deg, rgba(34, 197, 94, 0.15), rgba(34, 197, 94, 0.05)); border-color: rgba(34, 197, 94, 0.3); }
.light-mode .highlight-stat { background: linear-gradient(135deg, #dcfce7, #f0fdf4); border-color: #86efac; }

.stat-value { font-size: 20px; font-weight: 800; margin-bottom: 4px; }
.dark-mode .stat-value { color: white; }
.light-mode .stat-value { color: #1e293b; }
.stat-value.correct { color: #fbbf24; }
.stat-value.score { color: #22c55e; }
.stat-label { font-size: 12px; }
.dark-mode .stat-label { color: #64748b; }
.light-mode .stat-label { color: #94a3b8; }

.no-position { display: flex; align-items: center; gap: 18px; flex-wrap: wrap; }
.no-rank-icon { width: 56px; height: 56px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: 800; border: 2px dashed; }
.dark-mode .no-rank-icon { background: rgba(255,255,255,0.05); color: #64748b; border-color: #475569; }
.light-mode .no-rank-icon { background: #f8fafc; color: #94a3b8; border-color: #cbd5e1; }
.no-rank-text { flex: 1; }
.no-rank-text h4 { font-size: 17px; font-weight: 700; margin: 0 0 6px; }
.dark-mode .no-rank-text h4 { color: white; }
.light-mode .no-rank-text h4 { color: #1e293b; }
.no-rank-text p { font-size: 14px; margin: 0; }
.dark-mode .no-rank-text p { color: #94a3b8; }
.light-mode .no-rank-text p { color: #64748b; }

/* Rankings List */
.rankings-list-section { padding: 28px; border-radius: 24px; }
.dark-mode .rankings-list-section { background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(255,255,255,0.1); }
.light-mode .rankings-list-section { background: white; border: 1px solid #e2e8f0; box-shadow: 0 8px 30px rgba(0,0,0,0.08); }
.section-header { margin-bottom: 24px; padding-bottom: 18px; border-bottom: 1px solid; }
.dark-mode .section-header { border-color: rgba(255,255,255,0.1); }
.light-mode .section-header { border-color: #e2e8f0; }
.section-header h2 { font-size: 20px; font-weight: 800; margin: 0 0 6px; }
.dark-mode .section-header h2 { color: white; }
.light-mode .section-header h2 { color: #1e293b; }
.section-header p { font-size: 14px; margin: 0; }
.dark-mode .section-header p { color: #64748b; }
.light-mode .section-header p { color: #94a3b8; }
.section-header strong { color: #fbbf24; }

.rankings-list { display: flex; flex-direction: column; gap: 12px; }
.ranking-row { display: flex; align-items: center; justify-content: space-between; padding: 16px 18px; border-radius: 16px; transition: all 0.3s; animation: row-fade-in 0.5s ease-out forwards; animation-delay: var(--delay); opacity: 0; }
@keyframes row-fade-in { from { opacity: 0; transform: translateX(-20px); } to { opacity: 1; transform: translateX(0); } }
.dark-mode .ranking-row { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); }
.light-mode .ranking-row { background: #f8fafc; border: 1px solid #f1f5f9; }
.hover-row:hover { transform: translateX(8px); }
.dark-mode .hover-row:hover { background: rgba(251, 191, 36, 0.08); border-color: rgba(251, 191, 36, 0.25); }
.light-mode .hover-row:hover { background: #fffbeb; border-color: #fde68a; }

.row-left { display: flex; align-items: center; gap: 14px; }
.row-rank { width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 15px; font-weight: 800; }
.dark-mode .row-rank { background: rgba(255,255,255,0.06); color: #94a3b8; }
.light-mode .row-rank { background: white; color: #64748b; border: 1px solid #e2e8f0; }
.row-avatar-wrapper { position: relative; }
.row-avatar { width: 44px; height: 44px; border-radius: 50%; object-fit: cover; transition: transform 0.3s; }
.row-avatar:hover { transform: scale(1.1); }
.dark-mode .row-avatar { border: 2px solid rgba(255,255,255,0.1); }
.light-mode .row-avatar { border: 2px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.row-name { font-size: 15px; font-weight: 700; }
.dark-mode .row-name { color: white; }
.light-mode .row-name { color: #1e293b; }

.row-stats { display: flex; gap: 10px; }
.row-stat { padding: 10px 16px; border-radius: 12px; text-align: center; min-width: 85px; }
.dark-mode .row-stat { background: rgba(255,255,255,0.04); }
.light-mode .row-stat { background: white; border: 1px solid #f1f5f9; }
.stat-num { display: block; font-size: 15px; font-weight: 800; }
.dark-mode .stat-num { color: white; }
.light-mode .stat-num { color: #1e293b; }
.row-stat.highlight .stat-num { color: #22c55e; }
.stat-text { display: block; font-size: 11px; margin-top: 2px; }
.dark-mode .stat-text { color: #64748b; }
.light-mode .stat-text { color: #94a3b8; }

/* Pagination */
.pagination { display: flex; justify-content: center; gap: 8px; margin-top: 28px; }
.page-btn { min-width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 15px; font-weight: 700; cursor: pointer; transition: all 0.3s; }
.dark-mode .page-btn { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; }
.light-mode .page-btn { background: white; border: 1px solid #e2e8f0; color: #64748b; }
.page-btn:hover:not(:disabled):not(.sep) { transform: translateY(-2px); }
.dark-mode .page-btn:hover:not(:disabled):not(.sep) { background: rgba(255,255,255,0.12); color: white; }
.light-mode .page-btn:hover:not(:disabled):not(.sep) { background: #f8fafc; color: #1e293b; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.page-btn.active { color: white; }
.dark-mode .page-btn.active { background: linear-gradient(135deg, #06b6d4, #8b5cf6); border-color: transparent; box-shadow: 0 4px 15px rgba(6, 182, 212, 0.4); }
.light-mode .page-btn.active { background: linear-gradient(135deg, #1e293b, #334155); border-color: transparent; }
.page-btn.sep { cursor: default; border: none; background: transparent; }
.page-btn:disabled { opacity: 0.4; cursor: not-allowed; }

/* Error */
.error-message { margin-top: 24px; padding: 16px 24px; border-radius: 16px; text-align: center; font-size: 15px; }
.dark-mode .error-message { background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.3); color: #f87171; }
.light-mode .error-message { background: #fef2f2; border: 1px solid #fecaca; color: #dc2626; }

/* Responsive */
@media (max-width: 768px) {
  .ranking-page { padding: 16px; }
  .podium-container { grid-template-columns: 1fr; gap: 20px; }
  .podium-item.rank-1, .podium-item.rank-2, .podium-item.rank-3 { order: unset; }
  .podium-item.rank-1 { order: -1; }
  .podium-stand { height: 50px !important; font-size: 24px; }
  .position-content { flex-direction: column; align-items: stretch; }
  .stats-grid { justify-content: center; }
  .ranking-row { flex-direction: column; gap: 14px; align-items: stretch; }
  .row-stats { justify-content: space-between; }
  .title-gradient { font-size: 24px; }
}
</style>
