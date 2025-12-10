<template>
  <div class="min-h-screen bg-gradient-to-br from-sky-50 via-white to-cyan-50">
    <div class="mx-auto max-w-6xl px-4 py-8">
      <!-- Header -->
      <div class="mb-6 flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-extrabold bg-gradient-to-r from-cyan-600 to-sky-600 bg-clip-text text-transparent">Lộ trình học tập</h1>
          <p class="mt-1 text-slate-600">AI đồng hành cùng con trên hành trình học tập!</p>
        </div>
        <router-link
          class="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50 shadow-sm"
          :to="{ name: 'MyCourses' }"
        >
          Khóa học của tôi
        </router-link>
      </div>

      <!-- AI Greeting Banner -->
      <div v-if="!loading" class="mb-6 rounded-2xl bg-gradient-to-r from-cyan-500 via-sky-500 to-blue-500 p-6 text-white shadow-xl">
        <div class="flex items-start gap-4">
          <div class="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl bg-white/20 backdrop-blur">
            <svg class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          </div>
          <div class="flex-1">
            <h2 class="text-xl font-bold">{{ getGreeting() }}</h2>
            <p class="mt-1 text-cyan-100">{{ aiMessage }}</p>
            <div class="mt-3 flex flex-wrap gap-2">
              <span class="inline-flex items-center gap-1 rounded-full bg-white/20 px-3 py-1 text-sm">
                {{ overall.courses }} khóa học
              </span>
              <span class="inline-flex items-center gap-1 rounded-full bg-white/20 px-3 py-1 text-sm">
                {{ overall.completed }}/{{ overall.total }} bài
              </span>
              <span class="inline-flex items-center gap-1 rounded-full bg-white/20 px-3 py-1 text-sm">
                {{ overall.progress }}% hoàn thành
              </span>
            </div>
          </div>
          <button
            v-if="todayTasks.length > 0"
            class="shrink-0 rounded-xl bg-white px-5 py-3 text-sm font-bold text-sky-600 shadow-lg hover:bg-sky-50 transition-all"
            @click="startFirstStep"
          >
            Học ngay!
          </button>
        </div>
      </div>

      <!-- Progress Overview -->
      <div v-if="!loading" class="mb-6 grid gap-4 sm:grid-cols-4">
        <div class="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm text-center">
          <div class="flex h-12 w-12 mx-auto mb-2 items-center justify-center rounded-2xl bg-sky-100">
            <svg class="h-6 w-6 text-sky-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
          </div>
          <p class="text-2xl font-bold text-slate-900">{{ overall.courses }}</p>
          <p class="text-xs text-slate-500">Khóa học</p>
        </div>
        <div class="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm text-center">
          <div class="flex h-12 w-12 mx-auto mb-2 items-center justify-center rounded-2xl bg-emerald-100">
            <svg class="h-6 w-6 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <p class="text-2xl font-bold text-emerald-600">{{ overall.completed }}</p>
          <p class="text-xs text-slate-500">Đã hoàn thành</p>
        </div>
        <div class="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm text-center">
          <div class="flex h-12 w-12 mx-auto mb-2 items-center justify-center rounded-2xl bg-orange-100">
            <svg class="h-6 w-6 text-orange-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <p class="text-2xl font-bold text-sky-600">{{ overall.total - overall.completed }}</p>
          <p class="text-xs text-slate-500">Bài còn lại</p>
        </div>
        <div class="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm text-center">
          <div class="flex h-12 w-12 mx-auto mb-2 items-center justify-center rounded-2xl bg-amber-100">
            <svg class="h-6 w-6 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
          </div>
          <p class="text-2xl font-bold text-amber-600">{{ overall.progress }}%</p>
          <p class="text-xs text-slate-500">Tiến độ</p>
        </div>
      </div>

      <!-- AI Gợi ý hôm nay -->
      <div v-if="!loading && todayTasks.length" class="mb-6 rounded-2xl border border-amber-200 bg-gradient-to-r from-amber-50 to-orange-50 p-5 shadow-sm">
        <div class="flex items-center gap-2 mb-4">
          <span class="text-2xl">🤖</span>
          <h3 class="text-lg font-bold text-amber-800">AI gợi ý cho hôm nay</h3>
          <span class="ml-auto rounded-full bg-amber-200 px-3 py-1 text-xs font-semibold text-amber-800">
            {{ todayTasks.length }} bài học
          </span>
        </div>
        <div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          <div
            v-for="(task, idx) in todayTasks"
            :key="task.key"
            class="flex items-center gap-3 rounded-xl bg-white p-4 border border-amber-100 shadow-sm hover:shadow-md transition-all cursor-pointer"
            @click="startStep(task.path, task.step)"
          >
            <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl text-xl"
              :class="idx === 0 ? 'bg-amber-500 text-white' : 'bg-slate-100'"
            >
              {{ idx === 0 ? '🔥' : '📖' }}
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-semibold text-slate-900 truncate">{{ task.title }}</p>
              <p class="text-xs text-slate-500 truncate">{{ task.course }}</p>
            </div>
            <span class="shrink-0 rounded-lg bg-amber-500 px-3 py-1.5 text-xs font-bold text-white">
              {{ idx === 0 ? 'Bắt đầu' : 'Học' }}
            </span>
          </div>
        </div>
      </div>

      <!-- Daily Goal & Streak -->
      <div v-if="!loading && dailyGoal.target > 0" class="mb-6 grid gap-4 sm:grid-cols-2">
        <div class="rounded-2xl border border-emerald-200 bg-gradient-to-r from-emerald-50 to-green-50 p-5 shadow-sm">
          <div class="flex items-center justify-between mb-3">
            <h3 class="text-lg font-bold text-emerald-800 flex items-center gap-2">
              <span>🎯</span> Mục tiêu hôm nay
            </h3>
            <span class="text-2xl">{{ dailyGoal.completed >= dailyGoal.target ? '🎉' : '💪' }}</span>
          </div>
          <div class="flex items-center gap-3 mb-2">
            <div class="flex-1 h-3 rounded-full bg-emerald-100 overflow-hidden">
              <div 
                class="h-full bg-gradient-to-r from-emerald-400 to-green-500 transition-all duration-500"
                :style="{ width: `${Math.min(100, (dailyGoal.completed / dailyGoal.target) * 100)}%` }"
              ></div>
            </div>
            <span class="text-sm font-bold text-emerald-700">{{ dailyGoal.completed }}/{{ dailyGoal.target }}</span>
          </div>
          <p class="text-sm text-emerald-600">
            {{ dailyGoal.completed >= dailyGoal.target 
              ? 'Tuyệt vời! Con đã hoàn thành mục tiêu hôm nay! 🌟' 
              : `Còn ${dailyGoal.target - dailyGoal.completed} bài nữa để đạt mục tiêu!` }}
          </p>
        </div>
        
        <div class="rounded-2xl border border-orange-200 bg-gradient-to-r from-orange-50 to-amber-50 p-5 shadow-sm relative overflow-hidden">
          <!-- Fire particles background -->
          <div v-if="dailyGoal.streak > 0" class="fire-particles">
            <div v-for="i in 12" :key="i" class="fire-particle" :style="{ '--delay': `${i * 0.15}s`, '--x': `${10 + (i * 7) % 80}%` }"></div>
          </div>
          
          <div class="flex items-center justify-between mb-3 relative z-10">
            <h3 class="text-lg font-bold text-orange-800 flex items-center gap-2">
              <span class="fire-icon">🔥</span> Streak
            </h3>
            <span class="text-3xl font-bold text-orange-600">{{ dailyGoal.streak }}</span>
          </div>
          <p class="text-sm text-orange-600 relative z-10">
            {{ dailyGoal.streak > 0 
              ? `${dailyGoal.streak} ngày học liên tiếp! Cố gắng duy trì nhé!` 
              : 'Hãy bắt đầu streak mới hôm nay!' }}
          </p>
          <div class="mt-2 flex gap-1 relative z-10">
            <span v-for="i in 7" :key="i" 
              class="w-8 h-8 rounded-full flex items-center justify-center text-sm transition-all duration-300"
              :class="i <= dailyGoal.streak ? 'bg-gradient-to-t from-orange-600 to-amber-400 text-white shadow-lg fire-day' : 'bg-orange-100 text-orange-300'"
            >
              {{ i <= dailyGoal.streak ? '🔥' : '○' }}
            </span>
          </div>
        </div>
      </div>
      
      <!-- Streak Celebration Modal - Hiệu ứng lửa cháy như thật -->
      <Teleport to="body">
        <Transition name="streak-fade">
          <div v-if="showStreakCelebration" class="streak-overlay" @click="closeStreakCelebration">
            <!-- Realistic Fire Effect -->
            <div class="realistic-fire-container">
              <!-- Fire base glow -->
              <div class="fire-base-glow"></div>
              
              <!-- Main fire -->
              <div class="realistic-fire">
                <div class="fire-flame flame-main"></div>
                <div class="fire-flame flame-left"></div>
                <div class="fire-flame flame-right"></div>
                <div class="fire-flame flame-center"></div>
                <div class="fire-flame flame-inner"></div>
              </div>
              
              <!-- Sparks -->
              <div class="fire-sparks">
                <div v-for="i in 15" :key="'sp-'+i" class="spark" :style="{ '--i': i }"></div>
              </div>
              
              <!-- Heat distortion -->
              <div class="heat-wave"></div>
            </div>
            
            <!-- Content -->
            <div class="streak-modal-content" @click.stop>
              <h2 class="streak-title-text">🔥 Streak!</h2>
              
              <div class="streak-number-display">
                <span class="streak-num">{{ celebratedStreak }}</span>
                <span class="streak-label">ngày liên tiếp</span>
              </div>
              
              <p class="streak-msg">{{ getStreakMessage(celebratedStreak) }}</p>
              
              <button class="streak-btn" @click="closeStreakCelebration">
                Tiếp tục học →
              </button>
            </div>
          </div>
        </Transition>
      </Teleport>

      <!-- AI Weaknesses (Điểm yếu cần cải thiện) -->
      <div v-if="!loading && aiWeaknesses.length" class="mb-6 rounded-2xl border border-red-200 bg-gradient-to-r from-red-50 to-pink-50 p-5 shadow-sm">
        <div class="flex items-center gap-2 mb-4">
          <span class="text-2xl">📉</span>
          <h3 class="text-lg font-bold text-red-800">Điểm cần cải thiện</h3>
          <span class="ml-auto rounded-full bg-red-200 px-3 py-1 text-xs font-semibold text-red-800">
            {{ aiWeaknesses.length }} chủ đề
          </span>
        </div>
        <div class="grid gap-3 sm:grid-cols-2">
          <div
            v-for="(weakness, idx) in aiWeaknesses.slice(0, 4)"
            :key="idx"
            class="flex items-center gap-3 rounded-xl bg-white p-4 border border-red-100 shadow-sm hover:shadow-md transition-all cursor-pointer"
            @click="router.push({ name: 'student-course-player', params: { id: weakness.course_id, lessonId: weakness.lesson_id } })"
          >
            <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-red-100 text-xl">
              📖
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-semibold text-slate-900 truncate">{{ weakness.topic }}</p>
              <p class="text-xs text-slate-500">Điểm: {{ weakness.score }}% · {{ weakness.course }}</p>
            </div>
            <span class="shrink-0 rounded-lg bg-red-500 px-3 py-1.5 text-xs font-bold text-white">
              Ôn lại
            </span>
          </div>
        </div>
      </div>

      <!-- AI Practice (Bài luyện tập AI) -->
      <div v-if="!loading && showPracticeSection" class="mb-6 rounded-2xl border border-purple-200 bg-gradient-to-r from-purple-50 to-pink-50 p-5 shadow-sm">
        <div class="flex items-center gap-2 mb-4">
          <span class="text-2xl">📝</span>
          <h3 class="text-lg font-bold text-purple-800">Bài luyện tập hôm nay</h3>
          <span class="ml-auto">
            <button
              v-if="!showPractice"
              @click="showPractice = true"
              class="rounded-full bg-purple-500 px-4 py-1.5 text-xs font-bold text-white hover:bg-purple-600 transition-colors"
            >
              🚀 Bắt đầu
            </button>
            <button
              v-else
              @click="showPractice = false"
              class="rounded-full bg-gray-200 px-4 py-1.5 text-xs font-bold text-gray-600 hover:bg-gray-300 transition-colors"
            >
              Thu gọn
            </button>
          </span>
        </div>
        <p v-if="!showPractice" class="text-sm text-purple-600 mb-3">
          SmartEdu AI đã chuẩn bị bài tập phù hợp với bạn dựa trên kết quả học tập! 🌟
        </p>
        <AIPractice 
          v-if="showPractice"
          ref="practiceRef"
          :auto-load="true"
          @completed="onPracticeCompleted"
          @exercise-answered="onExerciseAnswered"
        />
      </div>

      <!-- AI Achievements (Huy hiệu) -->
      <div v-if="!loading && aiAchievements.length" class="mb-6 rounded-2xl border border-purple-200 bg-gradient-to-r from-purple-50 to-indigo-50 p-5 shadow-sm">
        <div class="flex items-center gap-2 mb-4">
          <span class="text-2xl">🏆</span>
          <h3 class="text-lg font-bold text-purple-800">Huy hiệu của con</h3>
          <span class="ml-auto rounded-full bg-purple-200 px-3 py-1 text-xs font-semibold text-purple-800">
            {{ aiAchievements.filter(a => a.unlocked).length }} huy hiệu
          </span>
        </div>
        <div class="flex flex-wrap gap-3">
          <div
            v-for="achievement in aiAchievements"
            :key="achievement.id"
            class="flex items-center gap-2 rounded-xl px-4 py-2 border transition-all"
            :class="achievement.unlocked 
              ? 'bg-white border-purple-200 shadow-sm' 
              : 'bg-slate-100 border-slate-200 opacity-50'"
          >
            <span class="text-2xl">{{ achievement.icon }}</span>
            <span class="text-sm font-semibold" :class="achievement.unlocked ? 'text-purple-700' : 'text-slate-400'">
              {{ achievement.name }}
            </span>
          </div>
        </div>
      </div>

      <!-- Personalized Paths -->
      <div v-if="loading" class="space-y-4">
        <div v-for="i in 3" :key="i" class="h-48 animate-pulse rounded-2xl border border-slate-200 bg-white"></div>
      </div>

      <div v-else-if="personalizedPaths.length" class="space-y-6">
        <h3 class="text-lg font-bold text-slate-900 flex items-center gap-2">
          Khóa học của bạn
        </h3>
        <section
          v-for="path in personalizedPaths"
          :key="path.id"
          class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm hover:shadow-md transition-all"
        >
          <div class="mb-4 flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="flex h-12 w-12 items-center justify-center rounded-xl"
                :class="getCourseIconBg(path.progress)"
              >
                <svg class="h-6 w-6" :class="path.progress >= 100 ? 'text-emerald-600' : path.progress > 0 ? 'text-sky-600' : 'text-slate-400'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <div>
                <h2 class="text-xl font-bold text-slate-900">{{ path.courseTitle }}</h2>
                <p class="text-sm text-slate-500">
                  {{ path.completedSteps }}/{{ path.totalSteps }} bài · {{ getTimeEstimate(path.totalSteps - path.completedSteps) }}
                </p>
              </div>
            </div>
            <span
              class="rounded-full border px-3 py-1.5 text-xs font-bold"
              :class="getStatusClass(path.progress)"
            >
              {{ getStatusText(path.progress) }}
            </span>
          </div>

          <!-- Progress bar with milestones -->
          <div class="mb-4">
            <div class="relative h-3 overflow-hidden rounded-full bg-slate-100">
              <div
                class="h-full rounded-full transition-all duration-500"
                :class="getProgressBarClass(path.progress)"
                :style="{ width: `${path.progress}%` }"
              ></div>
              <!-- Milestones -->
              <div class="absolute inset-0 flex justify-between px-1">
                <div v-for="m in [25, 50, 75]" :key="m" 
                  class="w-0.5 h-full"
                  :class="path.progress >= m ? 'bg-white/50' : 'bg-slate-300'"
                  :style="{ marginLeft: `${m}%` }"
                ></div>
              </div>
            </div>
            <div class="mt-1 flex justify-between text-xs text-slate-500">
              <span>Bắt đầu</span>
              <span>{{ path.progress }}%</span>
            </div>
          </div>

          <!-- Next steps with better UI -->
          <div v-if="path.nextSteps.length" class="mb-4 rounded-xl bg-gradient-to-r from-slate-50 to-sky-50 p-4">
            <h3 class="mb-3 text-sm font-bold text-slate-700 flex items-center gap-2">
              <span>🎯</span> Bước tiếp theo
            </h3>
            <div class="space-y-2">
              <div
                v-for="(step, idx) in path.nextSteps"
                :key="idx"
                class="flex items-center gap-3 rounded-lg bg-white p-3 border border-slate-100 hover:border-cyan-200 transition-all cursor-pointer"
                @click="startStep(path, step)"
              >
                <div
                  class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg text-sm font-bold"
                  :class="step.current ? 'bg-cyan-500 text-white' : 'bg-slate-200 text-slate-600'"
                >
                  {{ idx + 1 }}
                </div>
                <span class="flex-1 text-sm font-medium text-slate-900">{{ step.title }}</span>
                <span v-if="step.current" class="rounded-lg bg-cyan-500 px-3 py-1 text-xs font-bold text-white">
                  ▶ Học ngay
                </span>
                <span v-else class="text-xs text-slate-400">Sắp tới</span>
              </div>
            </div>
          </div>

          <!-- Achievement badges -->
          <div class="flex items-center justify-between">
            <div class="flex gap-2">
              <span v-if="path.progress >= 25" class="rounded-full bg-amber-100 px-2 py-1 text-xs">🌟 Mới bắt đầu</span>
              <span v-if="path.progress >= 50" class="rounded-full bg-sky-100 px-2 py-1 text-xs">💪 Đang tiến bộ</span>
              <span v-if="path.progress >= 75" class="rounded-full bg-emerald-100 px-2 py-1 text-xs">🔥 Sắp xong</span>
              <span v-if="path.progress >= 100" class="rounded-full bg-purple-100 px-2 py-1 text-xs">🏆 Xuất sắc</span>
            </div>
            <div class="flex gap-2">
              <!-- Đánh giá theo mức độ tiến độ -->
              <button
                v-if="path.progress === 0"
                class="rounded-xl bg-gradient-to-r from-purple-500 to-indigo-500 px-4 py-2 text-sm font-bold text-white hover:from-purple-600 hover:to-indigo-600 shadow-sm"
                @click="startAssessment(path)"
              >
                🎯 Đánh giá đầu vào
              </button>
              <button
                v-else-if="path.progress > 0 && path.progress < 30"
                class="rounded-xl bg-gradient-to-r from-amber-500 to-orange-500 px-4 py-2 text-sm font-bold text-white hover:from-amber-600 hover:to-orange-600 shadow-sm"
                @click="startAssessment(path)"
              >
                📝 Kiểm tra cơ bản
              </button>
              <button
                v-else-if="path.progress >= 30 && path.progress < 60"
                class="rounded-xl bg-gradient-to-r from-cyan-500 to-blue-500 px-4 py-2 text-sm font-bold text-white hover:from-cyan-600 hover:to-blue-600 shadow-sm"
                @click="startAssessment(path)"
              >
                📊 Đánh giá giữa kỳ
              </button>
              <button
                v-else-if="path.progress >= 60 && path.progress < 90"
                class="rounded-xl bg-gradient-to-r from-emerald-500 to-green-500 px-4 py-2 text-sm font-bold text-white hover:from-emerald-600 hover:to-green-600 shadow-sm"
                @click="startAssessment(path)"
              >
                🎓 Kiểm tra nâng cao
              </button>
              <button
                v-else-if="path.progress >= 90"
                class="rounded-xl bg-gradient-to-r from-violet-500 to-purple-500 px-4 py-2 text-sm font-bold text-white hover:from-violet-600 hover:to-purple-600 shadow-sm"
                @click="startAssessment(path)"
              >
                🏆 Đánh giá tổng kết
              </button>
              <button
                class="rounded-xl border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50"
                @click="viewFullPath(path)"
              >
                Xem chi tiết →
              </button>
            </div>
          </div>
        </section>
      </div>

      <!-- Default Paths -->
      <div v-else class="mt-5 grid gap-4 sm:grid-cols-2">
        <!-- basic -->
        <section class="rounded-2xl border border-slate-200 bg-white p-5">
          <div class="flex items-center justify-between">
            <h2 class="text-lg font-extrabold text-slate-900">Khối 1–2 (Cơ bản)</h2>
            <span class="rounded-full border border-cyan-200 dark:border-cyan-700 bg-cyan-50 dark:bg-cyan-900/20 px-3 py-1 text-xs font-bold text-cyan-700 dark:text-cyan-300">Nền tảng</span>
          </div>
          <p class="mt-2 text-slate-700">Củng cố Toán, Tiếng Việt, Tiếng Anh với các bài ngắn dễ tiếp thu.</p>
          <ol class="mt-3 space-y-1 text-sm text-slate-700 list-decimal list-inside">
            <li>Bước 1: Ôn từ vựng & đọc hiểu</li>
            <li>Bước 2: Luyện toán cơ bản</li>
            <li>Bước 3: Làm bài kiểm tra mini (10 phút)</li>
          </ol>
          <div class="mt-4">
            <router-link
              class="inline-flex items-center rounded-xl bg-slate-900 px-4 py-2 text-sm font-extrabold text-white hover:bg-slate-800"
              :to="{ name: 'student-catalog', query: { grade: 1 } }"
            >
              Bắt đầu ngay
            </router-link>
          </div>
        </section>

        <!-- advanced -->
        <section class="rounded-2xl border border-slate-200 bg-white p-5">
          <div class="flex items-center justify-between">
            <h2 class="text-lg font-extrabold text-slate-900">Khối 3–5 (Nâng cao)</h2>
            <span class="rounded-full border border-sky-200 bg-sky-50 px-3 py-1 text-xs font-bold text-sky-700">Mở rộng</span>
          </div>
          <p class="mt-2 text-slate-700">Hệ thống hoá & luyện thi: Toán, TV, Anh + Khoa học/Lịch sử.</p>
          <ol class="mt-3 space-y-1 text-sm text-slate-700 list-decimal list-inside">
            <li>Bước 1: Ôn kỹ năng đọc & ngữ pháp</li>
            <li>Bước 2: Luyện đề Toán & Khoa học</li>
            <li>Bước 3: Kiểm tra đánh giá, nhận phản hồi</li>
          </ol>
          <div class="mt-4">
            <router-link
              class="inline-flex items-center rounded-xl bg-slate-900 px-4 py-2 text-sm font-extrabold text-white hover:bg-slate-800"
              :to="{ name: 'student-catalog', query: { grade: 3 } }"
            >
              Chọn khóa
            </router-link>
          </div>
        </section>
      </div>

    </div>

    <!-- Assessment Modal -->
    <Teleport to="body">
      <div v-if="showAssessmentModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
        <div class="w-full max-w-2xl rounded-2xl bg-white shadow-2xl max-h-[90vh] overflow-y-auto">
          
          <!-- Intro Step -->
          <div v-if="assessmentStep === 'intro'" class="p-6">
            <div class="text-center mb-6">
              <div class="text-6xl mb-4">🎯</div>
              <h2 class="text-2xl font-bold text-slate-900">Đánh giá đầu vào</h2>
              <p class="mt-2 text-slate-600">{{ assessmentCourse?.courseTitle }}</p>
            </div>
            
            <div class="bg-gradient-to-r from-purple-50 to-indigo-50 rounded-xl p-5 mb-6">
              <h3 class="font-bold text-purple-800 mb-2">🤖 AI sẽ giúp con:</h3>
              <ul class="space-y-2 text-sm text-purple-700">
                <li class="flex items-center gap-2">
                  <span>✅</span> Đánh giá kiến thức hiện tại
                </li>
                <li class="flex items-center gap-2">
                  <span>✅</span> Tìm ra điểm mạnh và điểm yếu
                </li>
                <li class="flex items-center gap-2">
                  <span>✅</span> Đề xuất lộ trình học phù hợp
                </li>
              </ul>
            </div>
            
            <div class="bg-amber-50 rounded-xl p-4 mb-6">
              <p class="text-sm text-amber-800">
                ⏱️ Bài đánh giá gồm <strong>10-15 câu hỏi</strong>, mất khoảng <strong>10-15 phút</strong>.
                Hãy trả lời thật lòng để AI đề xuất chính xác nhé!
              </p>
            </div>
            
            <div class="flex gap-3">
              <button
                class="flex-1 rounded-xl border border-slate-200 px-4 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-50"
                @click="closeAssessment"
              >
                Để sau
              </button>
              <button
                class="flex-1 rounded-xl bg-gradient-to-r from-purple-500 to-indigo-500 px-4 py-3 text-sm font-bold text-white hover:from-purple-600 hover:to-indigo-600"
                :disabled="assessmentLoading"
                @click="loadAssessmentQuestions"
              >
                {{ assessmentLoading ? '⏳ Đang tải...' : '🚀 Bắt đầu ngay!' }}
              </button>
            </div>
          </div>
          
          <!-- Questions Step -->
          <div v-else-if="assessmentStep === 'questions'" class="p-6">
            <!-- Progress -->
            <div class="mb-6">
              <div class="flex items-center justify-between mb-2">
                <span class="text-sm font-semibold text-slate-600">
                  Câu {{ currentQuestionIndex + 1 }}/{{ assessmentQuestions.length }}
                </span>
                <span class="text-sm text-slate-500">{{ assessmentProgress }}% hoàn thành</span>
              </div>
              <div class="h-2 rounded-full bg-slate-100 overflow-hidden">
                <div 
                  class="h-full bg-gradient-to-r from-purple-500 to-indigo-500 transition-all duration-300"
                  :style="{ width: `${assessmentProgress}%` }"
                ></div>
              </div>
            </div>
            
            <!-- Question -->
            <div v-if="currentQuestion" class="mb-6">
              <div class="bg-slate-50 rounded-xl p-4 mb-4">
                <p class="text-xs text-slate-500 mb-1">{{ currentQuestion.module }}</p>
                <p class="text-lg font-semibold text-slate-900">{{ currentQuestion.text }}</p>
              </div>
              
              <div class="space-y-3">
                <button
                  v-for="(choice, idx) in currentQuestion.choices"
                  :key="idx"
                  class="w-full text-left rounded-xl border-2 p-4 transition-all"
                  :class="assessmentAnswers[currentQuestion.id] === idx 
                    ? 'border-purple-500 bg-purple-50' 
                    : 'border-slate-200 hover:border-purple-300 hover:bg-purple-50/50'"
                  @click="selectAnswer(currentQuestion.id, idx)"
                >
                  <div class="flex items-center gap-3">
                    <div 
                      class="w-6 h-6 rounded-full border-2 flex items-center justify-center text-xs font-bold"
                      :class="assessmentAnswers[currentQuestion.id] === idx 
                        ? 'border-purple-500 bg-purple-500 text-white' 
                        : 'border-slate-300'"
                    >
                      {{ assessmentAnswers[currentQuestion.id] === idx ? '✓' : String.fromCharCode(65 + idx) }}
                    </div>
                    <span class="text-slate-700">{{ choice }}</span>
                  </div>
                </button>
              </div>
            </div>
            
            <!-- Navigation -->
            <div class="flex gap-3">
              <button
                v-if="currentQuestionIndex > 0"
                class="rounded-xl border border-slate-200 px-4 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-50"
                @click="prevQuestion"
              >
                ← Câu trước
              </button>
              <div class="flex-1"></div>
              <button
                v-if="currentQuestionIndex < assessmentQuestions.length - 1"
                class="rounded-xl bg-slate-900 px-6 py-3 text-sm font-bold text-white hover:bg-slate-800"
                @click="nextQuestion"
              >
                Câu tiếp →
              </button>
              <button
                v-else
                class="rounded-xl bg-gradient-to-r from-purple-500 to-indigo-500 px-6 py-3 text-sm font-bold text-white hover:from-purple-600 hover:to-indigo-600"
                :disabled="!canSubmitAssessment || assessmentLoading"
                @click="submitAssessment"
              >
                {{ assessmentLoading ? '⏳ Đang xử lý...' : '✅ Hoàn thành' }}
              </button>
            </div>
          </div>
          
          <!-- Result Step -->
          <div v-else-if="assessmentStep === 'result'" class="p-6">
            <div class="text-center mb-6">
              <div class="text-6xl mb-4">
                {{ assessmentResult?.level === 'advanced' ? '🏆' : 
                   assessmentResult?.level === 'intermediate' ? '⭐' : 
                   assessmentResult?.level === 'elementary' ? '📚' : '🌱' }}
              </div>
              <h2 class="text-2xl font-bold text-slate-900">Kết quả đánh giá</h2>
              <p class="mt-2 text-slate-600">{{ assessmentCourse?.courseTitle }}</p>
            </div>
            
            <!-- Level Badge -->
            <div class="bg-gradient-to-r from-purple-100 to-indigo-100 rounded-xl p-5 mb-6 text-center">
              <p class="text-sm text-purple-600 mb-1">Trình độ của con</p>
              <p class="text-2xl font-bold text-purple-800">{{ assessmentResult?.level_text }}</p>
              <p class="text-sm text-purple-600 mt-1">
                Điểm: {{ assessmentResult?.score }}/{{ assessmentResult?.max_score }}
              </p>
            </div>
            
            <!-- AI Recommendation -->
            <div class="bg-gradient-to-r from-cyan-50 to-sky-50 rounded-xl p-5 mb-6">
              <div class="flex items-start gap-3">
                <span class="text-2xl">🤖</span>
                <div>
                  <p class="font-bold text-cyan-800 mb-1">Lời khuyên từ AI</p>
                  <p class="text-sm text-cyan-700">{{ assessmentResult?.recommendation }}</p>
                </div>
              </div>
            </div>
            
            <!-- Suggested Lessons -->
            <div v-if="assessmentResult?.suggested_lessons?.length" class="mb-6">
              <p class="font-bold text-slate-900 mb-3">📖 Bài học đề xuất bắt đầu:</p>
              <div class="space-y-2">
                <div
                  v-for="(lesson, idx) in assessmentResult.suggested_lessons"
                  :key="lesson.id"
                  class="flex items-center gap-3 rounded-xl bg-slate-50 p-3"
                >
                  <div class="w-8 h-8 rounded-lg bg-purple-500 text-white flex items-center justify-center font-bold text-sm">
                    {{ idx + 1 }}
                  </div>
                  <div>
                    <p class="font-semibold text-slate-900">{{ lesson.title }}</p>
                    <p class="text-xs text-slate-500">{{ lesson.module }}</p>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Actions -->
            <div class="flex gap-3">
              <button
                class="flex-1 rounded-xl border border-slate-200 px-4 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-50"
                @click="closeAssessment"
              >
                Đóng
              </button>
              <button
                class="flex-1 rounded-xl bg-gradient-to-r from-purple-500 to-indigo-500 px-4 py-3 text-sm font-bold text-white hover:from-purple-600 hover:to-indigo-600"
                @click="startFromRecommendation"
              >
                🚀 Bắt đầu học ngay!
              </button>
            </div>
          </div>
          
        </div>
      </div>
    </Teleport>
    
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { courseService } from '@/services/course.service'
import { aiLearningService, type AISuggestion, type AIWeakness, type AIAchievement, type DailyGoal } from '@/services/ai-learning.service'
import AIPractice from '@/components/ai/AIPractice.vue'

const router = useRouter()
const route = useRoute()

const loading = ref(false)
const personalizedPaths = ref<any[]>([])
const todayTasks = ref<any[]>([])
const overall = ref({ courses: 0, completed: 0, total: 0, progress: 0 })

// AI Practice
const showPractice = ref(false)
const showPracticeSection = ref(true)
const practiceRef = ref<InstanceType<typeof AIPractice> | null>(null)

function onPracticeCompleted(score: number) {
  console.log('Practice completed with score:', score)
  // Có thể cập nhật daily goal hoặc hiển thị thông báo
  if (score >= 80) {
    dailyGoal.value.completed++
  }
}

function onExerciseAnswered(correct: boolean) {
  console.log('Exercise answered:', correct ? 'correct' : 'incorrect')
}

// AI Data
const aiSuggestions = ref<AISuggestion[]>([])
const aiWeaknesses = ref<AIWeakness[]>([])
const aiAchievements = ref<AIAchievement[]>([])
const dailyGoal = ref<DailyGoal>({ target: 2, completed: 0, streak: 0 })
const serverAiMessage = ref('')

// Streak Celebration - Lưu vào localStorage để chỉ hiện 1 lần khi streak tăng
const showStreakCelebration = ref(false)
const celebratedStreak = ref(0) // Streak đang celebrate (để hiển thị trong modal)
const STREAK_STORAGE_KEY = 'smartedu_last_celebrated_streak'

function getLastCelebratedStreak(): { streak: number; date: string } | null {
  try {
    const stored = localStorage.getItem(STREAK_STORAGE_KEY)
    if (stored) {
      return JSON.parse(stored)
    }
  } catch (e) {
    console.error('Error reading streak from localStorage:', e)
  }
  return null
}

function saveLastCelebratedStreak(streak: number) {
  try {
    const today = new Date().toDateString()
    localStorage.setItem(STREAK_STORAGE_KEY, JSON.stringify({ streak, date: today }))
  } catch (e) {
    console.error('Error saving streak to localStorage:', e)
  }
}

function checkStreakCelebration(newStreak: number) {
  if (newStreak <= 0) return
  
  const stored = getLastCelebratedStreak()
  const today = new Date().toDateString()
  
  // Hiện celebration nếu:
  // 1. Chưa bao giờ celebrate (stored = null)
  // 2. Ngày mới và streak > 0 (reset mỗi ngày)
  // 3. Streak tăng trong cùng ngày
  const shouldCelebrate = 
    !stored || 
    stored.date !== today || 
    newStreak > stored.streak
  
  if (shouldCelebrate) {
    celebratedStreak.value = newStreak
    showStreakCelebration.value = true
    saveLastCelebratedStreak(newStreak)
  }
}

function closeStreakCelebration() {
  showStreakCelebration.value = false
}

// Expose để test trong console: window.testStreakCelebration()
if (typeof window !== 'undefined') {
  (window as any).testStreakCelebration = () => {
    localStorage.removeItem(STREAK_STORAGE_KEY)
    celebratedStreak.value = dailyGoal.value.streak || 1
    showStreakCelebration.value = true
  }
}

function getStreakMessage(streak: number): string {
  if (streak >= 30) return '🏆 Huyền thoại! Một tháng học liên tục!'
  if (streak >= 14) return '🌟 Siêu sao! 2 tuần không nghỉ!'
  if (streak >= 7) return '💪 Tuyệt vời! Cả tuần kiên trì!'
  if (streak >= 3) return '🔥 Đang cháy! Giữ vững nhịp độ nhé!'
  return '✨ Khởi đầu tốt! Tiếp tục phát huy!'
}

// Particle styles for animation
function getSparkStyle(index: number) {
  const angle = (index * 12) + Math.random() * 10
  const distance = 100 + Math.random() * 150
  const delay = Math.random() * 0.5
  const duration = 1 + Math.random() * 0.5
  const size = 4 + Math.random() * 4
  return {
    '--angle': `${angle}deg`,
    '--distance': `${distance}px`,
    '--delay': `${delay}s`,
    '--duration': `${duration}s`,
    '--size': `${size}px`,
  }
}

function getEmberStyle(index: number) {
  const x = -50 + Math.random() * 100
  const delay = Math.random() * 2
  const duration = 2 + Math.random() * 2
  const size = 6 + Math.random() * 8
  return {
    '--x': `${x}px`,
    '--delay': `${delay}s`,
    '--duration': `${duration}s`,
    '--size': `${size}px`,
  }
}

// Assessment Modal
const showAssessmentModal = ref(false)
const assessmentLoading = ref(false)
const assessmentCourse = ref<any>(null)
const assessmentQuestions = ref<any[]>([])
const assessmentAnswers = ref<Record<number, number>>({})
const currentQuestionIndex = ref(0)
const assessmentResult = ref<any>(null)
const assessmentStep = ref<'intro' | 'questions' | 'result'>('intro')

// AI Messages based on progress - ưu tiên tin nhắn từ AI API
const aiMessage = computed(() => {
  // Nếu có tin nhắn từ AI API, dùng nó
  if (serverAiMessage.value) {
    return serverAiMessage.value
  }
  
  // Fallback: tin nhắn mặc định
  const p = overall.value.progress
  const remaining = overall.value.total - overall.value.completed
  
  if (overall.value.courses === 0) {
    return 'Chào con! Hãy chọn một khóa học để bắt đầu hành trình học tập nhé! 🚀'
  }
  if (p === 0) {
    return 'Hãy bắt đầu bài học đầu tiên nào! AI sẽ đồng hành cùng con! 🌟'
  }
  if (p < 25) {
    return `Tuyệt vời! Con đã bắt đầu rồi. Còn ${remaining} bài nữa thôi, cố lên nhé! 💪`
  }
  if (p < 50) {
    return `Giỏi lắm! Con đã hoàn thành ${overall.value.completed} bài. Tiếp tục phát huy nhé! 🌟`
  }
  if (p < 75) {
    return `Xuất sắc! Đã đi được nửa chặng đường rồi. Còn ${remaining} bài nữa thôi! 🔥`
  }
  if (p < 100) {
    return `Sắp hoàn thành rồi! Chỉ còn ${remaining} bài nữa. Con làm được mà! 🏆`
  }
  return 'Chúc mừng con đã hoàn thành tất cả! Con thật giỏi! 🎉🏆'
})

function getGreeting() {
  const hour = new Date().getHours()
  if (hour < 12) return 'Chào buổi sáng! ☀️'
  if (hour < 18) return 'Chào buổi chiều! 🌤️'
  return 'Chào buổi tối! 🌙'
}

function getGreetingEmoji() {
  const hour = new Date().getHours()
  if (hour < 12) return '🌞'
  if (hour < 18) return '☀️'
  return '🌙'
}

function getProgressEmoji() {
  const p = overall.value.progress
  if (p === 0) return '🎯'
  if (p < 25) return '🌱'
  if (p < 50) return '💪'
  if (p < 75) return '🔥'
  if (p < 100) return '🌟'
  return '🏆'
}

function getCourseIcon(title: string) {
  const t = title.toLowerCase()
  if (t.includes('toán') || t.includes('math')) return '📊'
  if (t.includes('việt') || t.includes('văn')) return '📖'
  if (t.includes('anh') || t.includes('english')) return '🌍'
  if (t.includes('khoa')) return '🔬'
  if (t.includes('sử')) return '🏛️'
  return '📚'
}

function getCourseIconBg(progress: number) {
  if (progress >= 100) return 'bg-emerald-100'
  if (progress >= 50) return 'bg-sky-100'
  return 'bg-amber-100'
}

function getStatusClass(progress: number) {
  if (progress >= 100) return 'border-emerald-200 bg-emerald-50 text-emerald-700'
  if (progress >= 50) return 'border-sky-200 bg-sky-50 text-sky-700'
  return 'border-amber-200 bg-amber-50 text-amber-700'
}

function getStatusText(progress: number) {
  if (progress >= 100) return '🏆 Hoàn thành'
  if (progress >= 75) return '🔥 Sắp xong'
  if (progress >= 50) return '💪 Đang tiến bộ'
  if (progress > 0) return '🌱 Mới bắt đầu'
  return '🎯 Chưa học'
}

function getProgressBarClass(progress: number) {
  if (progress >= 100) return 'bg-gradient-to-r from-emerald-400 to-emerald-500'
  if (progress >= 50) return 'bg-gradient-to-r from-sky-400 to-cyan-500'
  return 'bg-gradient-to-r from-amber-400 to-orange-500'
}

function getTimeEstimate(lessons: number) {
  const mins = lessons * 15 // 15 mins per lesson
  if (mins < 60) return `~${mins} phút`
  const hours = Math.floor(mins / 60)
  const remainMins = mins % 60
  return remainMins > 0 ? `~${hours}h ${remainMins}p` : `~${hours} giờ`
}

function formatDate(iso?: string) {
  if (!iso) return ''
  try {
    return new Date(iso).toLocaleDateString('vi-VN')
  } catch {
    return iso
  }
}

async function loadPaths() {
  loading.value = true
  try {
    // Load enrolled courses với progress từ API
    const myCoursesData = await courseService.myCourses()
    const courses = myCoursesData.all || [...(myCoursesData.base || []), ...(myCoursesData.supp || [])]
    
    // Map courses to personalized paths - progress đã có sẵn từ API
    personalizedPaths.value = courses.map((course: any) => {
      const progress = course.progress || 0
      const totalLessons = course.lessonsCount || 0
      const completedLessons = Math.round((progress / 100) * totalLessons)
      
      // Determine difficulty level based on progress
      let difficulty = 'easy'
      if (progress >= 80) difficulty = 'hard'
      else if (progress >= 50) difficulty = 'medium'
      
      return {
        id: course.id,
        courseId: course.id,
        courseTitle: course.title,
        progress,
        completedSteps: completedLessons,
        totalSteps: totalLessons,
        difficulty,
        createdAt: course.createdAt || new Date().toISOString(),
        done: course.done || progress >= 100,
        nextSteps: [], // Sẽ load riêng nếu cần
      }
    })
    
    // Filter out null values
    personalizedPaths.value = personalizedPaths.value.filter(p => p !== null)
    
    // Sort by progress (descending)
    personalizedPaths.value.sort((a, b) => b.progress - a.progress)

    // Build summary + tasks
    const totalSteps = personalizedPaths.value.reduce((s, p) => s + (p.totalSteps || 0), 0)
    const completed = personalizedPaths.value.reduce((s, p) => s + (p.completedSteps || 0), 0)
    overall.value = {
      courses: personalizedPaths.value.length,
      completed,
      total: totalSteps,
      progress: totalSteps > 0 ? Math.round((completed / totalSteps) * 100) : 0,
    }

    // Pick up to 3 courses chưa hoàn thành for today
    todayTasks.value = personalizedPaths.value
      .filter((p) => p.progress < 100)
      .slice(0, 3)
      .map((p, idx) => ({
        key: `${p.id}-${idx}`,
        title: `Tiếp tục học ${p.courseTitle}`,
        course: p.courseTitle,
        path: p,
        step: { lessonId: null },
      }))
    
    // Load AI analysis
    await loadAIAnalysis()
  } catch (e: any) {
    console.error('Load paths error:', e)
  } finally {
    loading.value = false
  }
}

async function loadAIAnalysis() {
  try {
    const data = await aiLearningService.getAnalysis()
    if (data.suggestions) {
      aiSuggestions.value = data.suggestions
    }
    if (data.weaknesses) {
      aiWeaknesses.value = data.weaknesses
    }
    if (data.achievements) {
      aiAchievements.value = data.achievements
    }
    if (data.daily_goal) {
      dailyGoal.value = data.daily_goal
      // Check if streak increased to show celebration
      checkStreakCelebration(data.daily_goal.streak || 0)
    }
    if (data.ai_message) {
      serverAiMessage.value = data.ai_message
    }
  } catch (e) {
    console.error('Load AI analysis error:', e)
  }
}

function startStep(path: any, step: any) {
  router.push({
    name: 'student-course-player',
    params: { id: path.courseId, lessonId: step.lessonId || '1' },
  })
}

function startFirstStep() {
  // Go to the first upcoming step in any path
  if (todayTasks.value.length > 0) {
    const first = todayTasks.value[0]
    startStep(first.path, first.step)
  } else if (personalizedPaths.value.length > 0) {
    const p = personalizedPaths.value[0]
    const step = (p.nextSteps && p.nextSteps[0]) || { lessonId: '1' }
    startStep(p, step)
  }
}

function viewFullPath(path: any) {
  router.push({ name: 'student-course-detail', params: { id: path.courseId } })
}

// ============ ASSESSMENT FUNCTIONS ============
async function startAssessment(path: any) {
  assessmentCourse.value = path
  assessmentStep.value = 'intro'
  assessmentQuestions.value = []
  assessmentAnswers.value = {}
  currentQuestionIndex.value = 0
  assessmentResult.value = null
  showAssessmentModal.value = true
}

async function loadAssessmentQuestions() {
  if (!assessmentCourse.value) return
  
  assessmentLoading.value = true
  try {
    const data = await aiLearningService.getAssessment(assessmentCourse.value.courseId)
    assessmentQuestions.value = data.questions || []
    assessmentStep.value = 'questions'
    currentQuestionIndex.value = 0
  } catch (e) {
    console.error('Load assessment error:', e)
    alert('Không thể tải câu hỏi đánh giá. Vui lòng thử lại!')
  } finally {
    assessmentLoading.value = false
  }
}

function selectAnswer(questionId: number, choiceIndex: number) {
  assessmentAnswers.value[questionId] = choiceIndex
}

function nextQuestion() {
  if (currentQuestionIndex.value < assessmentQuestions.value.length - 1) {
    currentQuestionIndex.value++
  }
}

function prevQuestion() {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
  }
}

async function submitAssessment() {
  if (!assessmentCourse.value) return
  
  assessmentLoading.value = true
  try {
    const answers = assessmentQuestions.value.map(q => ({
      question_id: q.id,
      choice: assessmentAnswers.value[q.id] || 0,
      lesson_id: q.lesson_id,
    }))
    
    const result = await aiLearningService.submitAssessment(
      assessmentCourse.value.courseId,
      answers
    )
    assessmentResult.value = result
    assessmentStep.value = 'result'
  } catch (e) {
    console.error('Submit assessment error:', e)
    alert('Không thể gửi kết quả. Vui lòng thử lại!')
  } finally {
    assessmentLoading.value = false
  }
}

function closeAssessment() {
  showAssessmentModal.value = false
}

function startFromRecommendation() {
  if (assessmentResult.value?.suggested_lessons?.length > 0) {
    const lesson = assessmentResult.value.suggested_lessons[0]
    router.push({
      name: 'student-course-player',
      params: { id: assessmentCourse.value.courseId, lessonId: lesson.id },
    })
  }
  closeAssessment()
}

const currentQuestion = computed(() => {
  return assessmentQuestions.value[currentQuestionIndex.value] || null
})

const assessmentProgress = computed(() => {
  const answered = Object.keys(assessmentAnswers.value).length
  const total = assessmentQuestions.value.length
  return total > 0 ? Math.round((answered / total) * 100) : 0
})

const canSubmitAssessment = computed(() => {
  return Object.keys(assessmentAnswers.value).length === assessmentQuestions.value.length
})

onMounted(async () => {
  await loadPaths()
})

// Refresh khi quay lại trang (từ CoursePlayer) - dùng watch route
watch(() => route.path, async (newPath) => {
  if (newPath === '/student/learning-path' || newPath === '/student/learning_path') {
    await loadPaths()
  }
})
</script>

<style scoped>
/* Fire icon animation in streak card */
.fire-icon {
  display: inline-block;
  animation: fireWobble 0.3s ease-in-out infinite alternate;
  filter: drop-shadow(0 0 8px rgba(251, 146, 60, 0.8));
}

@keyframes fireWobble {
  0% { transform: scale(1) rotate(-5deg); }
  100% { transform: scale(1.15) rotate(5deg); }
}

/* Fire particles in streak card */
.fire-particles {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.fire-particle {
  position: absolute;
  bottom: 0;
  left: var(--x, 50%);
  width: 8px;
  height: 8px;
  background: radial-gradient(circle, #fbbf24 0%, #f97316 50%, #ef4444 100%);
  border-radius: 50%;
  animation: fireRise 2s ease-out infinite;
  animation-delay: var(--delay, 0s);
  opacity: 0;
}

@keyframes fireRise {
  0% { transform: translateY(0) scale(1); opacity: 0.8; }
  50% { opacity: 0.6; }
  100% { transform: translateY(-100px) scale(0.3); opacity: 0; }
}

/* Fire day glow */
.fire-day {
  animation: dayGlow 1s ease-in-out infinite alternate;
  box-shadow: 0 0 15px rgba(251, 146, 60, 0.6);
}

@keyframes dayGlow {
  0% { box-shadow: 0 0 10px rgba(251, 146, 60, 0.4); }
  100% { box-shadow: 0 0 20px rgba(239, 68, 68, 0.8); }
}

/* ============ REALISTIC FIRE CELEBRATION ============ */

.streak-fade-enter-active { animation: fadeIn 0.4s ease-out; }
.streak-fade-leave-active { animation: fadeOut 0.3s ease-in; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes fadeOut { from { opacity: 1; } to { opacity: 0; } }

/* Overlay */
.streak-overlay {
  position: fixed;
  inset: 0;
  z-index: 100;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: 
    radial-gradient(ellipse at center bottom, rgba(80, 30, 0, 0.4) 0%, transparent 50%),
    radial-gradient(ellipse at center, #0a0500 0%, #000000 100%);
  overflow: hidden;
}

/* ===== REALISTIC FIRE - TO VÀ ĐẸP ===== */
.realistic-fire-container {
  position: relative;
  width: 320px;
  height: 380px;
  margin-bottom: 0;
}

/* Base glow on ground - ánh sáng phản chiếu */
.fire-base-glow {
  position: absolute;
  bottom: -30px;
  left: 50%;
  transform: translateX(-50%);
  width: 350px;
  height: 100px;
  background: radial-gradient(ellipse, 
    rgba(255, 120, 0, 0.8) 0%, 
    rgba(255, 80, 0, 0.5) 30%, 
    rgba(255, 50, 0, 0.2) 60%, 
    transparent 80%
  );
  filter: blur(20px);
  animation: baseGlow 0.4s ease-in-out infinite alternate;
}

@keyframes baseGlow {
  0% { opacity: 0.7; transform: translateX(-50%) scaleX(0.95); }
  100% { opacity: 1; transform: translateX(-50%) scaleX(1.05); }
}

/* Main fire container */
.realistic-fire {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 180px;
  height: 300px;
}

/* Individual flames - rõ nét hơn */
.fire-flame {
  position: absolute;
  bottom: 0;
  border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
}

/* Main large flame - ngọn lửa chính TO */
.flame-main {
  left: 50%;
  transform: translateX(-50%);
  width: 140px;
  height: 280px;
  background: linear-gradient(to top, 
    #cc2200 0%,
    #ff3300 10%, 
    #ff5500 25%, 
    #ff7700 40%, 
    #ff9900 55%, 
    #ffbb00 70%, 
    #ffdd00 85%,
    #ffff44 95%,
    transparent 100%
  );
  filter: blur(1px);
  animation: flameMain 0.15s ease-in-out infinite alternate;
  box-shadow: 
    0 0 60px 30px rgba(255, 100, 0, 0.5),
    0 0 100px 60px rgba(255, 50, 0, 0.3),
    0 0 140px 90px rgba(255, 30, 0, 0.2);
}

@keyframes flameMain {
  0% { 
    height: 270px; 
    width: 135px;
    transform: translateX(-50%) skewX(-3deg);
  }
  100% { 
    height: 290px; 
    width: 145px;
    transform: translateX(-50%) skewX(3deg);
  }
}

/* Left flame - ngọn lửa trái */
.flame-left {
  left: -10px;
  width: 90px;
  height: 200px;
  background: linear-gradient(to top, 
    #dd2200 0%,
    #ff4400 20%, 
    #ff6600 45%, 
    #ff8800 70%, 
    #ffaa00 90%,
    transparent 100%
  );
  filter: blur(1px);
  animation: flameLeft 0.2s ease-in-out infinite alternate;
  box-shadow: 0 0 40px 15px rgba(255, 80, 0, 0.4);
}

@keyframes flameLeft {
  0% { 
    height: 190px;
    transform: skewX(8deg) rotate(-8deg);
  }
  100% { 
    height: 210px;
    transform: skewX(-4deg) rotate(4deg);
  }
}

/* Right flame - ngọn lửa phải */
.flame-right {
  right: -10px;
  width: 90px;
  height: 200px;
  background: linear-gradient(to top, 
    #dd2200 0%,
    #ff4400 20%, 
    #ff6600 45%, 
    #ff8800 70%, 
    #ffaa00 90%,
    transparent 100%
  );
  filter: blur(1px);
  animation: flameRight 0.18s ease-in-out infinite alternate;
  box-shadow: 0 0 40px 15px rgba(255, 80, 0, 0.4);
}

@keyframes flameRight {
  0% { 
    height: 195px;
    transform: skewX(-8deg) rotate(8deg);
  }
  100% { 
    height: 215px;
    transform: skewX(4deg) rotate(-4deg);
  }
}

/* Center bright flame - lõi sáng */
.flame-center {
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 220px;
  background: linear-gradient(to top, 
    #ff5500 0%, 
    #ff8800 20%, 
    #ffaa00 40%, 
    #ffcc00 60%, 
    #ffee00 80%,
    #ffff88 95%,
    transparent 100%
  );
  animation: flameCenter 0.12s ease-in-out infinite alternate;
  filter: blur(2px);
  box-shadow: 0 0 30px 10px rgba(255, 200, 0, 0.5);
}

@keyframes flameCenter {
  0% { height: 210px; opacity: 0.9; }
  100% { height: 230px; opacity: 1; }
}

/* Inner hottest part - phần nóng nhất */
.flame-inner {
  left: 50%;
  transform: translateX(-50%);
  bottom: 10px;
  width: 50px;
  height: 150px;
  background: linear-gradient(to top, 
    #ffbb00 0%, 
    #ffdd00 30%, 
    #ffff00 60%,
    #ffffaa 85%,
    #ffffff 95%,
    transparent 100%
  );
  animation: flameInner 0.1s ease-in-out infinite alternate;
  filter: blur(3px);
  box-shadow: 0 0 40px 15px rgba(255, 255, 200, 0.6);
}

@keyframes flameInner {
  0% { height: 140px; }
  100% { height: 160px; }
}

/* Sparks - tia lửa bay lên */
.fire-sparks {
  position: absolute;
  bottom: 100px;
  left: 50%;
  transform: translateX(-50%);
  width: 180px;
  height: 250px;
  pointer-events: none;
}

.spark {
  position: absolute;
  width: 6px;
  height: 6px;
  background: radial-gradient(circle, #fff 0%, #ffdd00 50%, #ff8800 100%);
  border-radius: 50%;
  box-shadow: 0 0 10px 4px rgba(255, 200, 0, 0.9);
  animation: sparkFly 1.5s ease-out infinite;
  animation-delay: calc(var(--i) * 0.1s);
  left: calc(15% + var(--i) * 5%);
}

@keyframes sparkFly {
  0% {
    transform: translateY(0) scale(1);
    opacity: 1;
  }
  100% {
    transform: translateY(-300px) translateX(calc((var(--i) - 7) * 25px)) scale(0);
    opacity: 0;
  }
}

/* Heat distortion wave - bỏ */
.heat-wave {
  display: none;
}

/* ===== CONTENT ===== */
.streak-modal-content {
  position: relative;
  z-index: 10;
  text-align: center;
  margin-top: -60px;
  animation: contentSlideUp 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

@keyframes contentSlideUp {
  0% { transform: translateY(50px); opacity: 0; }
  100% { transform: translateY(0); opacity: 1; }
}

.streak-title-text {
  font-size: 3.5rem;
  font-weight: 900;
  color: #fff;
  text-shadow: 
    0 0 20px rgba(255, 150, 0, 1),
    0 0 40px rgba(255, 100, 0, 0.8),
    0 0 60px rgba(255, 50, 0, 0.6),
    0 0 80px rgba(255, 30, 0, 0.4);
  margin-bottom: 0.5rem;
  letter-spacing: 2px;
  animation: titlePulse 0.8s ease-in-out infinite alternate;
}

@keyframes titlePulse {
  0% { 
    text-shadow: 0 0 20px rgba(255, 150, 0, 1), 0 0 40px rgba(255, 100, 0, 0.8); 
    transform: scale(1);
  }
  100% { 
    text-shadow: 0 0 30px rgba(255, 200, 0, 1), 0 0 60px rgba(255, 120, 0, 1), 0 0 100px rgba(255, 80, 0, 0.8); 
    transform: scale(1.02);
  }
}

.streak-number-display {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1.5rem;
}

.streak-num {
  font-size: 9rem;
  font-weight: 900;
  line-height: 1;
  background: linear-gradient(180deg, 
    #ffffff 0%, 
    #fff8e0 20%,
    #ffdd00 40%, 
    #ffaa00 60%, 
    #ff6600 80%, 
    #ff3300 100%
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  filter: drop-shadow(0 0 20px rgba(255, 150, 0, 0.8)) drop-shadow(0 6px 12px rgba(0, 0, 0, 0.5));
  animation: numBounce 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 0.3s both;
}

@keyframes numBounce {
  0% { transform: scale(0) rotate(-10deg); }
  60% { transform: scale(1.3) rotate(5deg); }
  100% { transform: scale(1) rotate(0deg); }
}

.streak-label {
  font-size: 1.5rem;
  color: rgba(255, 220, 180, 1);
  font-weight: 700;
  text-shadow: 0 2px 10px rgba(0,0,0,0.5);
  letter-spacing: 3px;
  text-transform: uppercase;
}

.streak-msg {
  font-size: 1.25rem;
  color: rgba(255, 230, 200, 1);
  margin-bottom: 2rem;
  font-weight: 500;
  text-shadow: 0 2px 10px rgba(0,0,0,0.5);
  animation: msgFade 0.5s ease-out 0.5s both;
}

@keyframes msgFade {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.streak-btn {
  padding: 1.25rem 3rem;
  font-size: 1.25rem;
  font-weight: 800;
  color: #fff;
  background: linear-gradient(135deg, #ff7700 0%, #ff5500 50%, #dd3300 100%);
  border: none;
  border-radius: 60px;
  cursor: pointer;
  box-shadow: 
    0 6px 20px rgba(255, 100, 0, 0.6),
    0 0 40px rgba(255, 100, 0, 0.4),
    inset 0 2px 0 rgba(255, 255, 255, 0.3),
    inset 0 -2px 0 rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  animation: btnAppear 0.5s ease-out 0.6s both;
  text-transform: uppercase;
  letter-spacing: 1px;
}

@keyframes btnAppear {
  from { opacity: 0; transform: translateY(30px) scale(0.8); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

.streak-btn:hover {
  transform: scale(1.08) translateY(-3px);
  box-shadow: 
    0 10px 35px rgba(255, 100, 0, 0.7),
    0 0 60px rgba(255, 100, 0, 0.5);
}

.streak-btn:active {
  transform: scale(0.98);
}
</style>
