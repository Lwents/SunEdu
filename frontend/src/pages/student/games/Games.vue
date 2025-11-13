<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-cyan-50/30 to-slate-50">
    <!-- Header -->
    <div class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <div class="mb-8">
        <div class="flex items-center gap-3 mb-3">
          <div
            class="flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-cyan-500 to-cyan-600 shadow-lg shadow-cyan-500/30"
          >
            <svg class="h-7 w-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"
              />
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>
          <div>
            <h1 class="text-3xl font-black text-slate-900 sm:text-4xl">Trò chơi giáo dục</h1>
            <p class="mt-1 text-sm text-slate-600">Học mà chơi, chơi mà học</p>
          </div>
        </div>
      </div>

      <!-- Game Grid -->
      <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <!-- Game Card 1 -->
        <div
          class="group relative overflow-hidden rounded-3xl border border-slate-200/80 bg-white/95 p-6 shadow-xl shadow-slate-100 transition-all duration-300 hover:scale-[1.02] hover:shadow-2xl hover:shadow-cyan-500/20"
        >
          <div
            class="absolute -right-8 -top-8 h-32 w-32 rounded-full bg-gradient-to-br from-cyan-400/20 to-sky-400/20 blur-2xl transition-all duration-500 group-hover:scale-150"
          ></div>
          <div class="relative">
            <div
              class="mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-cyan-500 to-cyan-600 shadow-lg shadow-cyan-500/30"
            >
              <svg class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-slate-900">Trắc nghiệm nhanh</h3>
            <p class="mt-2 text-sm text-slate-600">
              Thử thách kiến thức của bạn với các câu hỏi trắc nghiệm vui nhộn
            </p>
            <button
              class="mt-4 inline-flex w-full items-center justify-center gap-2 rounded-2xl border border-transparent bg-gradient-to-r from-cyan-500 to-cyan-600 px-4 py-3 text-sm font-bold text-white shadow-lg shadow-cyan-500/30 transition-all duration-300 hover:shadow-xl hover:shadow-cyan-500/40"
            >
              <span>Chơi ngay</span>
              <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M14 5l7 7m0 0l-7 7m7-7H3"
                />
              </svg>
            </button>
          </div>
        </div>

        <!-- Game Card 2 -->
        <div
          class="group relative overflow-hidden rounded-3xl border border-slate-200/80 bg-white/95 p-6 shadow-xl shadow-slate-100 transition-all duration-300 hover:scale-[1.02] hover:shadow-2xl hover:shadow-sky-500/20"
        >
          <div
            class="absolute -right-8 -top-8 h-32 w-32 rounded-full bg-gradient-to-br from-sky-400/20 to-blue-400/20 blur-2xl transition-all duration-500 group-hover:scale-150"
          ></div>
          <div class="relative">
            <div
              class="mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-sky-500 to-sky-600 shadow-lg shadow-sky-500/30"
            >
              <svg class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
                />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-slate-900">Ghép từ</h3>
            <p class="mt-2 text-sm text-slate-600">
              Luyện tập từ vựng và kiến thức qua trò chơi ghép từ
            </p>
            <button
              class="mt-4 inline-flex w-full items-center justify-center gap-2 rounded-2xl border border-transparent bg-gradient-to-r from-sky-500 to-sky-600 px-4 py-3 text-sm font-bold text-white shadow-lg shadow-sky-500/30 transition-all duration-300 hover:shadow-xl hover:shadow-sky-500/40"
            >
              <span>Chơi ngay</span>
              <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M14 5l7 7m0 0l-7 7m7-7H3"
                />
              </svg>
            </button>
          </div>
        </div>

        <!-- Game Card 3 -->
        <div
          class="group relative overflow-hidden rounded-3xl border border-slate-200/80 bg-white/95 p-6 shadow-xl shadow-slate-100 transition-all duration-300 hover:scale-[1.02] hover:shadow-2xl hover:shadow-blue-500/20"
        >
          <div
            class="absolute -right-8 -top-8 h-32 w-32 rounded-full bg-gradient-to-br from-blue-400/20 to-indigo-400/20 blur-2xl transition-all duration-500 group-hover:scale-150"
          ></div>
          <div class="relative">
            <div
              class="mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-500 to-blue-600 shadow-lg shadow-blue-500/30"
            >
              <svg class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-slate-900">Đố vui</h3>
            <p class="mt-2 text-sm text-slate-600">
              Giải đố và thử thách bản thân với các câu hỏi khó
            </p>
            <button
              class="mt-4 inline-flex w-full items-center justify-center gap-2 rounded-2xl border border-transparent bg-gradient-to-r from-blue-500 to-blue-600 px-4 py-3 text-sm font-bold text-white shadow-lg shadow-blue-500/30 transition-all duration-300 hover:shadow-xl hover:shadow-blue-500/40"
            >
              <span>Chơi ngay</span>
              <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M14 5l7 7m0 0l-7 7m7-7H3"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Coming Soon Section -->
      <div class="mt-12">
        <div
          class="rounded-3xl border border-slate-200/80 bg-white/95 p-8 text-center shadow-xl shadow-slate-100"
        >
          <div class="mx-auto mb-4 flex h-20 w-20 items-center justify-center">
            <svg
              class="h-20 w-20 text-slate-300"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-slate-900">Sắp có thêm nhiều trò chơi mới</h3>
          <p class="mt-2 text-slate-600">
            Chúng tôi đang phát triển thêm nhiều trò chơi giáo dục thú vị. Hãy quay lại sau nhé!
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Game page component
</script>
