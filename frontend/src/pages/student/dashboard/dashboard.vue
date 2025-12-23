<template>
  <div class="dashboard-wrapper" :class="isDark ? 'dark-mode' : 'light-mode'">
    <!-- Floating Background Elements (Dark mode only) -->
    <div v-if="isDark" class="bg-elements">
      <div class="float-shape shape-1"></div>
      <div class="float-shape shape-2"></div>
      <div class="float-shape shape-3"></div>
      <div class="glow glow-1"></div>
      <div class="glow glow-2"></div>
    </div>

    <!-- Main Content -->
    <div class="dashboard-content">
      <!-- Welcome Section -->
      <div class="welcome-section">
        <div class="welcome-text">
          <div class="welcome-badge">
            <span class="badge-dot"></span>
            <span>{{ greetingText }}</span>
          </div>
          <h1>Chào mừng trở lại! 👋</h1>
          <p>Tiếp tục hành trình học tập của bạn</p>
        </div>
      </div>

      <!-- Error -->
      <div v-if="errMsg" class="error-alert">⚠️ {{ errMsg }}</div>

      <!-- Stats Grid -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon blue">
            <svg class="stat-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
          </div>
          <div class="stat-info">
            <span class="stat-num">{{ stats.courses }}</span>
            <span class="stat-label">Khóa học</span>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon green">
            <svg class="stat-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="stat-info">
            <span class="stat-num">{{ stats.completed }}</span>
            <span class="stat-label">Hoàn thành</span>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon purple">
            <svg class="stat-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
            </svg>
          </div>
          <div class="stat-info">
            <span class="stat-num">{{ stats.exams }}</span>
            <span class="stat-label">Bài kiểm tra</span>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon orange">
            <svg class="stat-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z" />
              <path d="M9.879 16.121A3 3 0 1012.015 11L11 14H9c0 .768.293 1.536.879 2.121z" />
            </svg>
          </div>
          <div class="stat-info">
            <span class="stat-num">{{ stats.streak }}</span>
            <span class="stat-label">Ngày streak</span>
          </div>
        </div>
      </div>

      <!-- Continue Learning -->
      <div v-if="currentCourse" class="continue-section">
        <div class="section-badge">
          <span>▶️ Tiếp tục học</span>
        </div>
        <div class="continue-card" @click="openCourse(currentCourse.id)">
          <div class="continue-content">
            <h3>{{ currentCourse.title }}</h3>
            <p>{{ currentCourse.grade || 'Khóa học' }}</p>
            <div class="continue-progress">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: currentCourse.progress + '%' }"></div>
              </div>
              <span>{{ currentCourse.progress }}%</span>
            </div>
          </div>
          <button class="continue-btn">
            Học tiếp
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- Two Column Layout -->
      <div class="two-columns">
        <!-- Courses Section -->
        <div class="glass-card courses-card">
          <div class="card-header">
            <h2>📖 Khóa học của tôi</h2>
            <button @click="goToCourses">Xem tất cả →</button>
          </div>
          <div v-if="courses.length" class="courses-list">
            <div v-for="c in courses.slice(0, 4)" :key="c.id" class="course-item" @click="openCourse(c.id)">
              <div class="course-icon">{{ c.done ? '✅' : '📖' }}</div>
              <div class="course-info">
                <h4>{{ c.title }}</h4>
                <div class="course-progress">
                  <div class="mini-bar">
                    <div class="mini-fill" :style="{ width: (c.done ? 100 : c.progress) + '%' }"></div>
                  </div>
                  <span>{{ c.done ? 100 : c.progress }}%</span>
                </div>
              </div>
              <span class="course-arrow">→</span>
            </div>
          </div>
          <div v-else class="empty-state">
            <span>📚</span>
            <p>Chưa có khóa học</p>
            <button @click="goToCourses">Khám phá ngay</button>
          </div>
        </div>

        <!-- Right Column -->
        <div class="right-widgets">
          <!-- Streak Widget -->
          <div class="glass-card streak-card">
            <h3>Chuỗi ngày học</h3>
            <div class="streak-display">
              <div class="streak-num-wrapper" :class="{ 'has-streak': stats.streak > 0 }">
                <span class="streak-num">{{ stats.streak }}</span>
              </div>
              <span class="streak-text">ngày liên tiếp</span>
            </div>
            <div class="streak-week">
              <span v-for="(d, i) in weekDays" :key="i" class="week-dot" :class="{ active: d }">
                <span v-if="d" class="flame-container">
                  <span class="flame-main">
                    <span class="flame-inner"></span>
                  </span>
                  <span class="flame-left"></span>
                  <span class="flame-right"></span>
                  <span class="flame-glow"></span>
                </span>
                <span v-else class="empty-dot">○</span>
              </span>
            </div>
          </div>

          <!-- Exams Widget -->
          <div class="glass-card exams-card">
            <div class="card-header">
              <h3>📝 Bài kiểm tra</h3>
              <button @click="openExamsList">Xem →</button>
            </div>
            <div v-if="exams.length" class="exams-list">
              <div v-for="e in exams.slice(0, 2)" :key="e.id" class="exam-item" @click="openExamDetail(e.id)">
                <span class="exam-icon">{{ e.done ? '🏆' : '📋' }}</span>
                <div class="exam-info">
                  <span class="exam-title">{{ e.title }}</span>
                  <span class="exam-meta">⏱ {{ toMin(e.duration) }} phút</span>
                </div>
              </div>
            </div>
            <div v-else class="empty-mini">Chưa có bài kiểm tra</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { courseService, type CourseSummary } from '@/services/course.service'
import { useExamStore } from '@/store/exam.store'
import { useThemeStore } from '@/store/theme.store'

type CourseCard = CourseSummary & { progress: number; done: boolean }

const router = useRouter()
const errMsg = ref('')
const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)

// Greeting
const hour = new Date().getHours()
const greetingText = hour < 12 ? 'Chào buổi sáng' : hour < 18 ? 'Chào buổi chiều' : 'Chào buổi tối'

// Stats
const stats = reactive({ courses: 0, completed: 0, exams: 0, streak: 5, xp: 120 })
const now = new Date()
const weekDays = computed(() => {
  // Hiển thị 7 ô, với số ô có lửa = min(streak, 7)
  // Lửa hiển thị từ trái sang phải theo số streak
  const streakCount = Math.min(stats.streak, 7)
  return [0, 1, 2, 3, 4, 5, 6].map(i => i < streakCount)
})

// Courses
const courses = ref<CourseCard[]>([])
const currentCourse = computed(() => courses.value.find(c => c.progress > 0 && !c.done) || null)

async function fetchCourses() {
  try {
    const res = await courseService.myCourses({})
    courses.value = (res.all || []).slice(0, 10).map(c => ({
      ...c, progress: c.progress ?? 0, done: c.done ?? ((c.progress ?? 0) >= 100)
    })) as CourseCard[]
    stats.courses = courses.value.length
    stats.completed = courses.value.filter(c => c.done).length
    stats.xp = stats.completed * 50 + courses.value.reduce((s, c) => s + c.progress, 0)
  } catch (e: any) { errMsg.value = `Lỗi: ${e?.message || e}` }
}

// Exams
const examStore = useExamStore()
const exams = computed(() => ((examStore.exams as any[]) || []).slice(0, 3))
function toMin(s: number) { return Math.round((Number(s) || 0) / 60) }

// Navigation
const hasRoute = (n: string) => router.hasRoute(n as any)
function goToCourses() { hasRoute('MyCourses') ? router.push({ name: 'MyCourses' }) : router.push('/student/courses') }
function openCourse(id: number | string) {
  hasRoute('MyCourses') ? router.push({ name: 'MyCourses', query: { highlight: String(id) } }) : router.push({ path: '/student/courses', query: { highlight: String(id) } })
}
function openExamsList() { hasRoute('student-exams') ? router.push({ name: 'student-exams' }) : router.push('/student/exams') }
function openExamDetail(id: number | string) {
  hasRoute('student-exam-detail') ? router.push({ name: 'student-exam-detail', params: { id } }) : router.push(`/student/exams/${id}`)
}

onMounted(async () => {
  await fetchCourses()
  try { await examStore.fetchExams(); stats.exams = exams.value.length } catch {}
})
</script>

<style scoped>
/* Base Wrapper */
.dashboard-wrapper {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  transition: background-color 0.3s ease;
}

.dashboard-wrapper.dark-mode {
  background: #020617;
}

.dashboard-wrapper.light-mode {
  background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
}

/* Background Elements (Dark mode) */
.bg-elements {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.float-shape {
  position: absolute;
  border-radius: 24px;
  opacity: 0.15;
}

.shape-1 {
  top: 10%;
  left: 5%;
  width: 120px;
  height: 120px;
  background: linear-gradient(135deg, #06b6d4, #3b82f6);
  transform: rotate(12deg);
  animation: float1 15s ease-in-out infinite;
}

.shape-2 {
  top: 30%;
  right: 10%;
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #8b5cf6, #ec4899);
  transform: rotate(-12deg);
  animation: float2 12s ease-in-out infinite;
}

.shape-3 {
  bottom: 20%;
  left: 20%;
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #f59e0b, #ef4444);
  transform: rotate(45deg);
  animation: float3 18s ease-in-out infinite;
}

.glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
}

.glow-1 {
  top: 20%;
  left: -10%;
  width: 400px;
  height: 400px;
  background: rgba(6, 182, 212, 0.15);
}

.glow-2 {
  bottom: 10%;
  right: -10%;
  width: 350px;
  height: 350px;
  background: rgba(139, 92, 246, 0.15);
}

@keyframes float1 {
  0%, 100% { transform: translateY(0) rotate(12deg); }
  50% { transform: translateY(-20px) rotate(12deg); }
}

@keyframes float2 {
  0%, 100% { transform: translateY(0) rotate(-12deg); }
  50% { transform: translateY(-15px) rotate(-12deg); }
}

@keyframes float3 {
  0%, 100% { transform: translateY(0) rotate(45deg); }
  50% { transform: translateY(-25px) rotate(45deg); }
}

/* Content */
.dashboard-content {
  position: relative;
  z-index: 10;
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 24px;
}

/* Welcome Section */
.welcome-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
}

.welcome-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 50px;
  margin-bottom: 12px;
}

.dark-mode .welcome-badge {
  background: rgba(6, 182, 212, 0.1);
  border: 1px solid rgba(6, 182, 212, 0.2);
}

.light-mode .welcome-badge {
  background: rgba(99, 102, 241, 0.1);
  border: 1px solid rgba(99, 102, 241, 0.2);
}

.badge-dot {
  width: 8px;
  height: 8px;
  background: #06b6d4;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.light-mode .badge-dot {
  background: #6366f1;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.welcome-badge span {
  font-size: 14px;
  font-weight: 500;
}

.dark-mode .welcome-badge span { color: #06b6d4; }
.light-mode .welcome-badge span { color: #6366f1; }

.welcome-text h1 {
  font-size: 36px;
  font-weight: 800;
  margin: 0 0 8px;
}

.dark-mode .welcome-text h1 { color: white; }
.light-mode .welcome-text h1 { color: #1e293b; }

.welcome-text p {
  font-size: 16px;
  margin: 0;
}

.dark-mode .welcome-text p { color: #94a3b8; }
.light-mode .welcome-text p { color: #64748b; }

.welcome-stats {
  display: flex;
  gap: 24px;
}

.mini-stat {
  text-align: center;
}

.mini-value {
  display: block;
  font-size: 24px;
  font-weight: 800;
}

.dark-mode .mini-value { color: white; }
.light-mode .mini-value { color: #1e293b; }

.mini-label {
  font-size: 12px;
  color: #64748b;
}

/* Error */
.error-alert {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #f87171;
  padding: 12px 20px;
  border-radius: 12px;
  margin-bottom: 24px;
  font-size: 14px;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}

.stat-card {
  border-radius: 20px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.dark-mode .stat-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.light-mode .stat-card {
  background: white;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.stat-card:hover {
  transform: translateY(-4px);
}

.dark-mode .stat-card:hover { border-color: rgba(6, 182, 212, 0.3); }
.light-mode .stat-card:hover { box-shadow: 0 8px 24px rgba(0,0,0,0.1); }

.stat-icon {
  width: 52px;
  height: 52px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
}

.stat-svg {
  width: 28px;
  height: 28px;
}

.stat-icon.blue { background: rgba(59, 130, 246, 0.2); color: #3b82f6; }
.stat-icon.green { background: rgba(34, 197, 94, 0.2); color: #22c55e; }
.stat-icon.purple { background: rgba(139, 92, 246, 0.2); color: #8b5cf6; }
.stat-icon.orange { background: rgba(249, 115, 22, 0.2); color: #f97316; }

.stat-num {
  display: block;
  font-size: 28px;
  font-weight: 800;
  line-height: 1;
}

.dark-mode .stat-num { color: white; }
.light-mode .stat-num { color: #1e293b; }

.stat-label {
  font-size: 13px;
  color: #64748b;
}

/* Section Badge */
.section-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 50px;
  margin-bottom: 16px;
}

.section-badge span {
  color: #a78bfa;
  font-size: 14px;
  font-weight: 600;
}

/* Continue Card */
.continue-card {
  border-radius: 24px;
  padding: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 32px;
}

.dark-mode .continue-card {
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(139, 92, 246, 0.2));
  border: 1px solid rgba(6, 182, 212, 0.3);
}

.light-mode .continue-card {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border: none;
  box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);
}

.continue-card:hover {
  transform: translateY(-4px);
}

.dark-mode .continue-card:hover {
  border-color: rgba(6, 182, 212, 0.5);
  box-shadow: 0 0 40px rgba(6, 182, 212, 0.2);
}

.light-mode .continue-card:hover {
  box-shadow: 0 8px 30px rgba(99, 102, 241, 0.4);
}

.continue-content h3 {
  font-size: 20px;
  font-weight: 700;
  color: white;
  margin: 0 0 4px;
}

.continue-content p {
  font-size: 14px;
  margin: 0 0 16px;
}

.dark-mode .continue-content p { color: #94a3b8; }
.light-mode .continue-content p { color: rgba(255,255,255,0.8); }

.continue-progress {
  display: flex;
  align-items: center;
  gap: 12px;
}

.progress-bar {
  width: 200px;
  height: 8px;
  border-radius: 4px;
  overflow: hidden;
}

.dark-mode .progress-bar { background: rgba(255, 255, 255, 0.1); }
.light-mode .progress-bar { background: rgba(255, 255, 255, 0.3); }

.progress-fill {
  height: 100%;
  border-radius: 4px;
}

.dark-mode .progress-fill { background: linear-gradient(90deg, #06b6d4, #8b5cf6); }
.light-mode .progress-fill { background: white; }

.continue-progress span {
  font-size: 14px;
  font-weight: 600;
}

.dark-mode .continue-progress span { color: #06b6d4; }
.light-mode .continue-progress span { color: white; }

.continue-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 28px;
  border: none;
  border-radius: 14px;
  color: white;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
}

.dark-mode .continue-btn { background: linear-gradient(135deg, #06b6d4, #8b5cf6); }
.light-mode .continue-btn { background: white; color: #6366f1; }

.continue-btn:hover {
  transform: scale(1.05);
}

.dark-mode .continue-btn:hover { box-shadow: 0 0 30px rgba(6, 182, 212, 0.4); }
.light-mode .continue-btn:hover { box-shadow: 0 4px 20px rgba(0,0,0,0.15); }

/* Two Columns */
.two-columns {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 24px;
}

/* Glass Card */
.glass-card {
  border-radius: 24px;
  padding: 24px;
  backdrop-filter: blur(10px);
}

.dark-mode .glass-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.light-mode .glass-card {
  background: white;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-header h2, .card-header h3 {
  font-size: 18px;
  font-weight: 700;
  margin: 0;
}

.dark-mode .card-header h2, .dark-mode .card-header h3 { color: white; }
.light-mode .card-header h2, .light-mode .card-header h3 { color: #1e293b; }

.card-header button {
  background: none;
  border: none;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.dark-mode .card-header button { color: #06b6d4; }
.light-mode .card-header button { color: #6366f1; }

.card-header button:hover {
  text-decoration: underline;
}

/* Courses List */
.courses-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.course-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.dark-mode .course-item {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.light-mode .course-item {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
}

.course-item:hover {
  transform: translateX(4px);
}

.dark-mode .course-item:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(6, 182, 212, 0.3);
}

.light-mode .course-item:hover {
  background: #f1f5f9;
  border-color: #6366f1;
}

.course-icon {
  font-size: 28px;
}

.course-info {
  flex: 1;
  min-width: 0;
}

.course-info h4 {
  font-size: 15px;
  font-weight: 600;
  margin: 0 0 8px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dark-mode .course-info h4 { color: white; }
.light-mode .course-info h4 { color: #1e293b; }

.course-progress {
  display: flex;
  align-items: center;
  gap: 10px;
}

.mini-bar {
  width: 120px;
  height: 4px;
  border-radius: 2px;
  overflow: hidden;
}

.dark-mode .mini-bar { background: rgba(255, 255, 255, 0.1); }
.light-mode .mini-bar { background: #e2e8f0; }

.mini-fill {
  height: 100%;
  background: linear-gradient(90deg, #06b6d4, #8b5cf6);
  border-radius: 2px;
}

.light-mode .mini-fill {
  background: linear-gradient(90deg, #6366f1, #8b5cf6);
}

.course-progress span {
  font-size: 12px;
  color: #64748b;
}

.course-arrow {
  color: #475569;
  font-size: 18px;
}

/* Right Widgets */
.right-widgets {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Streak Card */
.streak-card h3 {
  font-size: 16px;
  font-weight: 700;
  margin: 0 0 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.dark-mode .streak-card h3 { color: white; }
.light-mode .streak-card h3 { color: #1e293b; }

/* Fire Icon Animation */
.fire-icon {
  position: relative;
  width: 24px;
  height: 28px;
  display: inline-block;
}

.fire-icon .flame {
  position: absolute;
  bottom: 0;
  border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
  animation: flicker 0.3s ease-in-out infinite alternate;
}

.fire-icon .f1 {
  left: 2px;
  width: 10px;
  height: 16px;
  background: linear-gradient(to top, #ff6b35, #f7931e);
  animation-delay: 0s;
}

.fire-icon .f2 {
  left: 7px;
  width: 12px;
  height: 20px;
  background: linear-gradient(to top, #ff4500, #ff6b35);
  animation-delay: 0.1s;
}

.fire-icon .f3 {
  right: 2px;
  width: 10px;
  height: 14px;
  background: linear-gradient(to top, #ff6b35, #ffa500);
  animation-delay: 0.2s;
}

.fire-icon .core {
  left: 50%;
  transform: translateX(-50%);
  width: 8px;
  height: 12px;
  background: linear-gradient(to top, #ffeb3b, #fff176);
  animation-delay: 0.15s;
}

@keyframes flicker {
  0% { transform: scaleY(1) scaleX(1); opacity: 1; }
  100% { transform: scaleY(1.1) scaleX(0.9); opacity: 0.9; }
}

/* ========== HEADER FLAME (next to title) ========== */
.header-flame {
  position: relative;
  display: inline-block;
  width: 24px;
  height: 28px;
  vertical-align: middle;
  margin-right: 6px;
}

.hf-main {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 14px;
  height: 20px;
  background: linear-gradient(to top, #ff6b08 0%, #ff9500 30%, #ffcc00 60%, #ffeb3b 100%);
  border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
  animation: hf-dance 0.3s ease-in-out infinite alternate;
}

.hf-inner {
  position: absolute;
  bottom: 2px;
  left: 50%;
  transform: translateX(-50%);
  width: 5px;
  height: 9px;
  background: linear-gradient(to top, #fff9c4, #ffffff);
  border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
  animation: hf-inner 0.25s ease-in-out infinite alternate;
}

.hf-left {
  position: absolute;
  bottom: 2px;
  left: 2px;
  width: 8px;
  height: 12px;
  background: linear-gradient(to top, #ff5722 0%, #ff9800 50%, #ffc107 100%);
  border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
  transform: rotate(-15deg);
  animation: hf-left 0.35s ease-in-out infinite alternate;
}

.hf-right {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 8px;
  height: 12px;
  background: linear-gradient(to top, #ff5722 0%, #ff9800 50%, #ffc107 100%);
  border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
  transform: rotate(15deg);
  animation: hf-right 0.4s ease-in-out infinite alternate;
}

@keyframes hf-dance {
  0% { height: 18px; transform: translateX(-50%) scaleX(1) rotate(-2deg); }
  100% { height: 22px; transform: translateX(-50%) scaleX(0.9) rotate(2deg); }
}

@keyframes hf-inner {
  0% { height: 7px; opacity: 0.9; }
  100% { height: 11px; opacity: 1; }
}

@keyframes hf-left {
  0% { height: 10px; transform: rotate(-10deg); }
  100% { height: 14px; transform: rotate(-20deg) translateY(-2px); }
}

@keyframes hf-right {
  0% { height: 10px; transform: rotate(10deg); }
  100% { height: 14px; transform: rotate(20deg) translateY(-2px); }
}

/* ========== STREAK FIRE (behind number) ========== */
.streak-fire {
  position: absolute;
  bottom: -5px;
  left: 50%;
  transform: translateX(-50%);
  width: 70px;
  height: 85px;
  pointer-events: none;
  z-index: 0;
}

.sf-main {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 70px;
  background: linear-gradient(to top, #ff6b08 0%, #ff9500 25%, #ffcc00 50%, #ffeb3b 75%, #fff9c4 100%);
  border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
  animation: sf-dance 0.35s ease-in-out infinite alternate;
  z-index: 2;
}

.sf-inner {
  position: absolute;
  bottom: 5px;
  left: 50%;
  transform: translateX(-50%);
  width: 14px;
  height: 30px;
  background: linear-gradient(to top, #fff9c4, #ffffff);
  border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
  animation: sf-inner 0.3s ease-in-out infinite alternate;
}

.sf-left {
  position: absolute;
  bottom: 0;
  left: 5px;
  width: 22px;
  height: 45px;
  background: linear-gradient(to top, #ff5722 0%, #ff9800 40%, #ffc107 80%, #ffeb3b 100%);
  border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
  transform: rotate(-18deg);
  animation: sf-left 0.4s ease-in-out infinite alternate;
  z-index: 1;
}

.sf-right {
  position: absolute;
  bottom: 0;
  right: 5px;
  width: 22px;
  height: 45px;
  background: linear-gradient(to top, #ff5722 0%, #ff9800 40%, #ffc107 80%, #ffeb3b 100%);
  border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
  transform: rotate(18deg);
  animation: sf-right 0.45s ease-in-out infinite alternate;
  z-index: 1;
}

.sf-glow {
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 90px;
  height: 45px;
  background: radial-gradient(ellipse at center bottom, rgba(255, 152, 0, 0.6) 0%, rgba(255, 87, 34, 0.3) 40%, transparent 70%);
  border-radius: 50%;
  animation: sf-glow 0.5s ease-in-out infinite alternate;
  z-index: 0;
}

@keyframes sf-dance {
  0% { height: 65px; transform: translateX(-50%) scaleX(1) rotate(-2deg); }
  100% { height: 75px; transform: translateX(-50%) scaleX(0.92) rotate(2deg); }
}

@keyframes sf-inner {
  0% { height: 25px; opacity: 0.9; }
  100% { height: 35px; opacity: 1; }
}

@keyframes sf-left {
  0% { height: 40px; transform: rotate(-15deg); }
  100% { height: 50px; transform: rotate(-22deg) translateY(-3px); }
}

@keyframes sf-right {
  0% { height: 40px; transform: rotate(15deg); }
  100% { height: 50px; transform: rotate(22deg) translateY(-3px); }
}

@keyframes sf-glow {
  0% { opacity: 0.5; transform: translateX(-50%) scale(0.95); }
  100% { opacity: 0.8; transform: translateX(-50%) scale(1.05); }
}

/* ========== WEEK DOT FLAME ========== */
.flame-container {
  position: relative;
  width: 20px;
  height: 26px;
  display: inline-block;
}

.flame-main {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 14px;
  height: 20px;
  background: linear-gradient(to top, #ff6b08 0%, #ff9500 30%, #ffcc00 60%, #ffeb3b 100%);
  border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
  animation: flame-dance 0.3s ease-in-out infinite alternate;
}

.flame-inner {
  position: absolute;
  bottom: 2px;
  left: 50%;
  transform: translateX(-50%);
  width: 6px;
  height: 10px;
  background: linear-gradient(to top, #fff9c4, #ffffff);
  border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
  animation: flame-inner-dance 0.25s ease-in-out infinite alternate;
}

.flame-left {
  position: absolute;
  bottom: 2px;
  left: 0;
  width: 8px;
  height: 12px;
  background: linear-gradient(to top, #ff5722 0%, #ff9800 50%, #ffc107 100%);
  border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
  transform: rotate(-15deg);
  animation: flame-side-left 0.35s ease-in-out infinite alternate;
}

.flame-right {
  position: absolute;
  bottom: 2px;
  right: 0;
  width: 8px;
  height: 12px;
  background: linear-gradient(to top, #ff5722 0%, #ff9800 50%, #ffc107 100%);
  border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
  transform: rotate(15deg);
  animation: flame-side-right 0.4s ease-in-out infinite alternate;
}

.flame-glow {
  position: absolute;
  bottom: -4px;
  left: 50%;
  transform: translateX(-50%);
  width: 24px;
  height: 16px;
  background: radial-gradient(ellipse at center, rgba(255, 152, 0, 0.6) 0%, rgba(255, 87, 34, 0.3) 40%, transparent 70%);
  border-radius: 50%;
  animation: glow-pulse 0.5s ease-in-out infinite alternate;
}

@keyframes flame-dance {
  0% { height: 18px; transform: translateX(-50%) scaleX(1) rotate(-2deg); }
  100% { height: 22px; transform: translateX(-50%) scaleX(0.9) rotate(2deg); }
}

@keyframes flame-inner-dance {
  0% { height: 8px; opacity: 0.9; }
  100% { height: 12px; opacity: 1; }
}

@keyframes flame-side-left {
  0% { height: 10px; transform: rotate(-10deg); }
  100% { height: 14px; transform: rotate(-20deg) translateY(-2px); }
}

@keyframes flame-side-right {
  0% { height: 10px; transform: rotate(10deg); }
  100% { height: 14px; transform: rotate(20deg) translateY(-2px); }
}

@keyframes glow-pulse {
  0% { opacity: 0.5; transform: translateX(-50%) scale(0.9); }
  100% { opacity: 0.8; transform: translateX(-50%) scale(1.1); }
}

.empty-dot {
  color: #475569;
  font-size: 16px;
  opacity: 0.4;
}

.streak-display {
  text-align: center;
  padding: 24px;
  background: linear-gradient(135deg, rgba(249, 115, 22, 0.15), rgba(239, 68, 68, 0.15));
  border-radius: 16px;
  margin-bottom: 16px;
  position: relative;
  overflow: visible;
}

.streak-num-wrapper {
  position: relative;
  display: inline-block;
  z-index: 1;
}

.streak-num-wrapper.has-streak::before {
  content: '';
  position: absolute;
  inset: -20px;
  background: radial-gradient(circle, rgba(255, 152, 0, 0.4) 0%, rgba(255, 87, 34, 0.2) 40%, transparent 70%);
  border-radius: 50%;
  animation: pulse-glow 2s ease-in-out infinite;
  z-index: -1;
}

@keyframes pulse-glow {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.1); opacity: 0.8; }
}

.streak-num {
  position: relative;
  display: block;
  font-size: 56px;
  font-weight: 900;
  background: linear-gradient(135deg, #f97316, #ef4444);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
}

.streak-text {
  color: #94a3b8;
  font-size: 14px;
}

.streak-week {
  display: flex;
  justify-content: space-between;
  padding: 8px 8px 0;
}

.week-dot {
  transition: all 0.3s ease;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  position: relative;
}

.week-dot.active {
  animation: bounce-fire 0.5s ease-in-out;
}

@keyframes bounce-fire {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}

/* Exams Card */
.exams-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.exam-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.dark-mode .exam-item { background: rgba(255, 255, 255, 0.03); }
.light-mode .exam-item { background: #f8fafc; }

.dark-mode .exam-item:hover { background: rgba(255, 255, 255, 0.06); }
.light-mode .exam-item:hover { background: #f1f5f9; }

.exam-icon {
  font-size: 24px;
}

.exam-info {
  flex: 1;
}

.exam-title {
  display: block;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 2px;
}

.dark-mode .exam-title { color: white; }
.light-mode .exam-title { color: #1e293b; }

.exam-meta {
  font-size: 12px;
  color: #64748b;
}

/* Empty States */
.empty-state {
  text-align: center;
  padding: 40px 20px;
}

.empty-state span {
  font-size: 48px;
  display: block;
  margin-bottom: 12px;
}

.empty-state p {
  color: #64748b;
  margin: 0 0 16px;
}

.empty-state button {
  padding: 10px 24px;
  background: linear-gradient(135deg, #06b6d4, #8b5cf6);
  border: none;
  border-radius: 12px;
  color: white;
  font-weight: 600;
  cursor: pointer;
}

.empty-mini {
  text-align: center;
  padding: 24px;
  color: #64748b;
  font-size: 14px;
}

/* Responsive */
@media (max-width: 1024px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .two-columns { grid-template-columns: 1fr; }
  .right-widgets { display: grid; grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 640px) {
  .dashboard-content { padding: 20px 16px; }
  .welcome-section { flex-direction: column; gap: 16px; }
  .welcome-text h1 { font-size: 28px; }
  .stats-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
  .stat-card { padding: 16px; }
  .stat-num { font-size: 22px; }
  .continue-card { flex-direction: column; gap: 16px; text-align: center; }
  .progress-bar { width: 100%; }
  .right-widgets { grid-template-columns: 1fr; }
}
</style>
