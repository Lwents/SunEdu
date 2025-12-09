<template>
  <div class="student-shell" v-if="course">
    <div class="student-container max-w-[1600px] px-4 lg:px-8">
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

      <div class="grid gap-6 lg:grid-cols-[minmax(0,3fr)_minmax(320px,1fr)]">
        <div class="order-1 space-y-4">
          <!-- Locked Lesson Warning -->
          <div v-if="lessonLocked" class="rounded-2xl border border-amber-200 bg-amber-50 p-6 text-center">
            <svg class="mx-auto h-12 w-12 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
            <h3 class="mt-4 text-lg font-semibold text-amber-900">Bài học bị khóa</h3>
            <p class="mt-2 text-sm text-amber-700">{{ unlockReason || 'Bạn cần hoàn thành bài học trước đó' }}</p>
          </div>

          <!-- Content from lessonContentPayload (from content library) - Chỉ hiển thị khi KHÔNG phải video -->
          <div v-if="!lessonLocked && lessonContentPayload && currentLessonKind !== 'video'" class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div v-if="lessonContentPayload.contentType === 'text'" class="space-y-3">
              <div class="flex items-center gap-3">
                <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-slate-100">
                  <span class="text-2xl">📝</span>
                </div>
                <h3 class="text-lg font-semibold text-gray-900">Nội dung bài học</h3>
              </div>
              <div class="prose max-w-none text-gray-800">
                <p class="whitespace-pre-line">{{ lessonContentPayload.payload?.content || lessonContentPayload.payload?.text || currentLessonDetail?.introduction || 'Chưa có nội dung văn bản' }}</p>
              </div>
            </div>
            <div v-else-if="lessonContentPayload.contentType === 'image'" class="space-y-3">
              <div class="flex items-center gap-3">
                <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-indigo-100">
                  <span class="text-2xl">🖼️</span>
                </div>
                <h3 class="text-lg font-semibold text-gray-900">Hình ảnh</h3>
              </div>
              <div class="space-y-2">
                <img
                  :src="lessonContentPayload.payload?.fileData || lessonContentPayload.payload?.url"
                  alt="Nội dung hình ảnh"
                  class="max-h-[480px] w-full rounded-2xl object-contain border border-slate-200"
                />
                <p class="text-xs text-gray-500" v-if="lessonContentPayload.payload?.fileName">
                  {{ lessonContentPayload.payload.fileName }}
                </p>
              </div>
            </div>
            <div v-else-if="lessonContentPayload.contentType === 'pdf'" class="space-y-3">
              <div class="flex items-center gap-3">
                <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-rose-100">
                  <span class="text-2xl">📄</span>
                </div>
                <div>
                  <h3 class="text-lg font-semibold text-gray-900">Tài liệu PDF</h3>
                  <p class="text-sm text-gray-500">Xem hoặc tải về tài liệu bài học</p>
                </div>
              </div>
              <div class="flex gap-3">
                <a
                  class="inline-flex items-center gap-2 rounded-lg bg-cyan-600 px-4 py-2 text-sm font-semibold text-white hover:bg-cyan-700"
                  :href="lessonContentPayload.payload?.fileData || lessonContentPayload.payload?.url || '#'"
                  target="_blank"
                  rel="noopener"
                >
                  📖 Xem tài liệu
                </a>
                <a
                  class="inline-flex items-center gap-2 rounded-lg border border-gray-300 px-4 py-2 text-sm font-semibold text-gray-700 hover:bg-gray-50"
                  :href="lessonContentPayload.payload?.fileData || lessonContentPayload.payload?.url || '#'"
                  download
                >
                  ⬇️ Tải về
                </a>
              </div>
              <div class="overflow-hidden rounded-xl border border-slate-200">
                <object
                  v-if="docUrlFromPayload"
                  :data="docUrlFromPayload"
                  type="application/pdf"
                  class="h-[520px] w-full"
                >
                  <iframe
                    :src="getDocViewerUrl(docUrlFromPayload, 'pdf')"
                    class="h-[520px] w-full"
                  ></iframe>
                </object>
              </div>
              <p class="text-xs text-gray-500" v-if="lessonContentPayload.payload?.fileName">
                {{ lessonContentPayload.payload.fileName }}
              </p>
            </div>
            <div v-else-if="lessonContentPayload.contentType === 'doc'" class="space-y-3">
              <div class="flex items-center gap-3">
                <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-blue-100">
                  <span class="text-2xl">📑</span>
                </div>
                <div>
                  <h3 class="text-lg font-semibold text-gray-900">Tài liệu</h3>
                  <p class="text-sm text-gray-500">Tải về tài liệu để xem chi tiết</p>
                </div>
              </div>
              <div class="overflow-hidden rounded-xl border border-slate-200">
                <iframe
                  v-if="docViewerFromPayload"
                  :src="docViewerFromPayload"
                  class="h-[520px] w-full"
                ></iframe>
              </div>
              <a
                class="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700"
                :href="lessonContentPayload.payload?.fileData || lessonContentPayload.payload?.url || '#'"
                download
              >
                ⬇️ Tải tài liệu
              </a>
              <p class="text-xs text-gray-500" v-if="lessonContentPayload.payload?.fileName">
                {{ lessonContentPayload.payload.fileName }}
              </p>
            </div>
          </div>

          <!-- Introduction (fallback if no lessonContentPayload but introduction exists) - Chỉ hiển thị khi KHÔNG phải video -->
          <div v-else-if="!lessonLocked && currentLessonDetail?.introduction && !lessonContentPayload && currentLessonKind !== 'video'" class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div class="flex items-center gap-3 mb-3">
              <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-slate-100">
                <span class="text-2xl">📝</span>
              </div>
              <h3 class="text-lg font-semibold text-gray-900">Nội dung bài học</h3>
            </div>
            <div class="prose max-w-none text-gray-800">
              <p class="whitespace-pre-line">{{ currentLessonDetail.introduction }}</p>
            </div>
          </div>

          <!-- PDF Content (fallback from document_file) - Chỉ hiển thị khi KHÔNG phải video -->
          <div v-if="!lessonLocked && !lessonContentPayload && currentLessonKind !== 'video' && currentLessonDetail?.content_type === 'pdf' && currentLessonDetail?.document_file" class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div class="flex items-center gap-3 mb-4">
              <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-rose-100">
                <span class="text-2xl">📄</span>
              </div>
              <div>
                <h3 class="text-lg font-semibold text-gray-900">Tài liệu PDF</h3>
                <p class="text-sm text-gray-500">Xem hoặc tải về tài liệu bài học</p>
              </div>
            </div>
            <div class="flex gap-3">
              <a
                :href="docUrlFromLesson"
                target="_blank"
                class="inline-flex items-center gap-2 rounded-lg bg-cyan-600 px-4 py-2 text-sm font-semibold text-white hover:bg-cyan-700"
              >
                📖 Xem tài liệu
              </a>
              <a
                :href="docUrlFromLesson"
                download
                class="inline-flex items-center gap-2 rounded-lg border border-gray-300 px-4 py-2 text-sm font-semibold text-gray-700 hover:bg-gray-50"
              >
                ⬇️ Tải về
              </a>
            </div>
            <div class="mt-4 overflow-hidden rounded-xl border border-slate-200">
              <object
                :data="docUrlFromLesson"
                type="application/pdf"
                class="h-[520px] w-full"
              >
                <iframe
                  :src="getDocViewerUrl(docUrlFromLesson, 'pdf')"
                  class="h-[520px] w-full"
                ></iframe>
              </object>
            </div>
          </div>

          <!-- Document (Word/Docx) Content (fallback) - Chỉ hiển thị khi KHÔNG phải video -->
          <div v-if="!lessonLocked && !lessonContentPayload && currentLessonKind !== 'video' && currentLessonDetail?.content_type === 'document' && currentLessonDetail?.document_file" class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div class="flex items-center gap-3 mb-4">
              <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-blue-100">
                <span class="text-2xl">📑</span>
              </div>
              <div>
                <h3 class="text-lg font-semibold text-gray-900">Tài liệu Word</h3>
                <p class="text-sm text-gray-500">Tải về tài liệu để xem chi tiết</p>
              </div>
            </div>
            <a
              :href="docUrlFromLesson"
              download
              class="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700"
            >
              ⬇️ Tải tài liệu Word
            </a>
            <div class="mt-4 overflow-hidden rounded-xl border border-slate-200">
              <iframe
                :src="docViewerFromLesson"
                class="h-[520px] w-full"
              ></iframe>
            </div>
          </div>

          <!-- Text Content (fallback from content_type) - Chỉ hiển thị khi KHÔNG phải video -->
          <div v-if="!lessonLocked && !lessonContentPayload && currentLessonKind !== 'video' && currentLessonDetail?.content_type === 'text'" class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div class="flex items-center gap-3 mb-4">
              <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-slate-100">
                <span class="text-2xl">📝</span>
              </div>
              <h3 class="text-lg font-semibold text-gray-900">Nội dung bài học</h3>
            </div>
            <div class="prose max-w-none text-gray-800">
              <p class="whitespace-pre-line">{{ currentLessonDetail.text_content || currentLessonDetail.introduction || 'Chưa có nội dung' }}</p>
            </div>
          </div>

          <!-- Video Player - CHỈ hiển thị khi là video -->
          <div v-if="!lessonLocked && currentLessonKind === 'video' && hasVideo" class="overflow-hidden rounded-3xl border border-slate-200 bg-slate-900/5 shadow-xl shadow-slate-300/50">
            <!-- Video từ YouTube -->
            <iframe
              v-if="lessonVideoUrl && isYouTubeUrl(lessonVideoUrl)"
              ref="youtubeIframeRef"
              :src="getYouTubeEmbedUrl(lessonVideoUrl)"
              class="aspect-video w-full min-h-[400px] lg:min-h-[500px] rounded-3xl"
              frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen
              @load="onYouTubeIframeLoad"
            ></iframe>
            <!-- Video từ URL hoặc file -->
            <video
              v-else-if="lessonVideoUrl || lessonVideoFile"
              ref="videoRef"
              class="aspect-video w-full min-h-[400px] lg:min-h-[500px] rounded-3xl bg-black object-contain"
              :src="lessonVideoSrc"
              controls
              playsinline
              @ended="onVideoEnded"
              @timeupdate="onVideoTimeUpdate"
            ></video>
            <!-- Fallback: Course video -->
            <template v-else>
              <iframe
                v-if="course.video_url && isYouTubeUrl(course.video_url)"
                ref="youtubeIframeRef"
                :src="getYouTubeEmbedUrl(course.video_url)"
                class="aspect-video w-full min-h-[400px] lg:min-h-[500px] rounded-3xl"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
                @load="onYouTubeIframeLoad"
              ></iframe>
              <video
                v-else
                ref="videoRef"
                class="aspect-video w-full min-h-[400px] lg:min-h-[500px] rounded-3xl bg-black object-contain"
                :src="currentSrc"
                controls
                playsinline
                @ended="onVideoEnded"
                @timeupdate="onVideoTimeUpdate"
              ></video>
            </template>
            <div class="flex items-start justify-between gap-4 px-6 py-5">
              <div class="space-y-1">
                <p class="student-section-title text-xs text-gray-600 dark:text-gray-400">
                  {{ currentLesson ? 'Bài học hiện tại' : 'Video khóa học' }}
                </p>
                <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100">
                  {{ currentLesson?.title || course.title }}
                </h2>
                <div class="mt-2">
                  <span class="inline-flex items-center gap-2 rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700">
                    <span v-if="currentLessonKind === 'video'">🎬</span>
                    <span v-else-if="currentLessonKind === 'quiz'">✏️</span>
                    <span v-else-if="currentLessonKind === 'pdf'">📄</span>
                    <span v-else-if="currentLessonKind === 'doc'">📑</span>
                    <span v-else-if="currentLessonKind === 'text'">📝</span>
                    <span v-else-if="currentLessonKind === 'image'">🖼️</span>
                    <span v-else>📚</span>
                    {{ lessonKindLabel(currentLessonKind) }}
                  </span>
                </div>
              </div>
              <!-- Nút Hỏi AI về video - bên phải -->
              <button
                v-if="currentLessonKind === 'video'"
                class="flex-shrink-0 inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-purple-500 to-indigo-600 px-4 py-2.5 text-sm font-bold text-white shadow-lg shadow-purple-200 transition hover:from-purple-600 hover:to-indigo-700 hover:shadow-xl hover:-translate-y-0.5 active:translate-y-0"
                @click="openAIVideoModal"
              >
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
                Hỏi AI
              </button>
            </div>
          </div>
          <!-- Chỉ hiển thị thông báo này khi thực sự là video nhưng thiếu video URL -->
          <div v-else-if="!lessonLocked && currentLessonKind === 'video' && !hasVideo" class="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <h3 class="text-lg font-semibold text-gray-900">Bài học</h3>
            <p class="text-sm text-gray-600">Bài này không có video, hãy xem nội dung bên dưới.</p>
          </div>

          <!-- Exercise Section -->
          <div v-if="currentLessonExercises.length > 0 && !lessonLocked" class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div class="mb-4 flex items-center justify-between">
              <h3 class="text-lg font-semibold text-gray-900">Bài tập</h3>
              <span v-if="lessonProgress?.exercise_completed" class="rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-700">
                Đã hoàn thành
              </span>
            </div>
            <div v-for="(exercise, idx) in currentLessonExercises" :key="exercise.id" class="mb-4 last:mb-0">
              <div class="rounded-lg border border-gray-200 bg-gray-50 p-4">
                <h4 class="mb-2 font-semibold text-gray-900">{{ exercise.title }}</h4>
                <button
                  type="button"
                  class="rounded-lg bg-cyan-600 px-4 py-2 text-sm font-semibold text-white hover:bg-cyan-700"
                  :disabled="lessonProgress?.exercise_completed"
                  :class="lessonProgress?.exercise_completed ? 'opacity-60 cursor-not-allowed' : ''"
                  @click="!lessonProgress?.exercise_completed && openExercise(exercise.id)"
                >
                  {{ lessonProgress?.exercise_completed ? 'Đã nộp' : 'Làm bài tập' }}
                </button>
              </div>
            </div>
            <p v-if="currentLessonDetail?.requires_exercise_completion && !lessonProgress?.exercise_completed" class="mt-3 text-sm text-amber-600">
              ⚠️ Bạn cần hoàn thành bài tập này để tiếp tục bài học tiếp theo
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
                        ? 'bg-cyan-50 dark:bg-cyan-900/20 text-cyan-700 dark:text-cyan-300 ring-1 ring-cyan-100'
                        : 'bg-white text-gray-900 dark:text-gray-100 hover:bg-slate-50',
                      lessonState(it) === 'next' ? 'ring-1 ring-cyan-50' : '',
                      it.done ? 'font-semibold' : '',
                    ]"
                    @click="goToLesson(si, li)"
                  >
                    <div class="flex items-center gap-3">
                      <span
                        :class="[
                          'flex h-9 w-9 items-center justify-center rounded-full text-xs font-semibold',
                          lessonStateClass(lessonState(it))
                        ]"
                      >
                        <svg v-if="lessonState(it) === 'done'" class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M20 6L9 17l-5-5" />
                        </svg>
                        <svg v-else-if="lessonKind(it) === 'video'" class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
                          <path d="M8 5v14l11-7z" />
                        </svg>
                        <svg v-else-if="lessonKind(it) === 'quiz'" class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2" />
                          <path d="M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                          <path d="M9 14l2 2 4-4" />
                        </svg>
                        <span v-else-if="lessonKind(it) === 'pdf'" class="text-sm">📄</span>
                        <span v-else-if="lessonKind(it) === 'doc'" class="text-sm">📑</span>
                        <span v-else-if="lessonKind(it) === 'text'" class="text-sm">📝</span>
                        <svg v-else-if="lessonKind(it) === 'image'" class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M3 5h18v14H3z" />
                          <path d="M21 15l-5-5-4 4-3-3-6 6" />
                        </svg>
                        <svg v-else class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
                          <path d="M14 2v6h6" />
                        </svg>
                      </span>
                      <div class="flex flex-col">
                        <span class="text-sm font-semibold leading-tight">{{ li + 1 }}. {{ it.title }}</span>
                        <span class="text-xs text-gray-500">{{ lessonStateLabel(lessonState(it)) }}</span>
                        <span class="mt-0.5 inline-flex w-fit items-center gap-1 rounded-full bg-slate-100 px-2 py-0.5 text-[11px] font-semibold text-slate-600">
                          <span v-if="lessonKind(it) === 'video'">🎬</span>
                          <span v-else-if="lessonKind(it) === 'quiz'">✏️</span>
                          <span v-else-if="lessonKind(it) === 'pdf'">📄</span>
                          <span v-else-if="lessonKind(it) === 'doc'">📑</span>
                          <span v-else-if="lessonKind(it) === 'text'">📝</span>
                          <span v-else-if="lessonKind(it) === 'image'">🖼️</span>
                          <span v-else>📚</span>
                          {{ lessonKindLabel(lessonKind(it)) }}
                        </span>
                      </div>
                    </div>
                    <div class="text-right text-xs font-semibold text-gray-500 dark:text-gray-400 min-w-[42px]">
                      {{ formatDuration(it.durationMinutes) }}
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
            class="inline-flex items-center justify-center rounded-2xl border border-transparent bg-gradient-to-r from-cyan-500 to-cyan-600 px-4 py-2 text-sm font-semibold text-white shadow-lg shadow-cyan-500/40 transition hover:from-cyan-600 hover:to-cyan-700 hover:shadow-xl hover:-translate-y-0.5 disabled:opacity-50 disabled:hover:translate-y-0"
            :disabled="!nextLesson"
            @click="goNext"
          >
            Bài tiếp theo ›
          </button>
        </div>
      </div>
    </div>

    <!-- Nút hỏi đáp nổi -->
    <button
      v-if="qaLessonId"
      class="fixed bottom-6 right-6 z-30 inline-flex items-center gap-2 rounded-full px-4 py-3 text-sm font-bold shadow-lg shadow-orange-200 transition"
      :class="lessonLocked
        ? 'bg-slate-300 text-white cursor-not-allowed'
        : 'bg-orange-500 text-white hover:bg-orange-600'"
      :disabled="lessonLocked"
      @click="toggleQA(true)"
    >
      <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h6m-3 8a9 9 0 110-18 9 9 0 010 18z" />
      </svg>
      <span>{{ lessonLocked ? 'Hỏi đáp bị khoá' : 'Hỏi đáp' }}</span>
    </button>

    <!-- Drawer hỏi đáp -->
    <transition name="fade">
      <div
        v-if="qaOpen"
        class="fixed inset-0 z-40 bg-black/50 backdrop-blur-sm"
        @click.self="toggleQA(false)"
      ></div>
    </transition>
    <transition name="slide">
      <div
        v-if="qaOpen"
        class="fixed inset-y-0 right-0 z-50 flex w-full max-w-2xl flex-col bg-gradient-to-b from-white to-slate-50 shadow-2xl"
      >
        <!-- Header -->
        <div class="flex items-center justify-between border-b border-slate-200 bg-white px-6 py-5 shadow-sm">
          <div class="flex items-center gap-3">
            <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-orange-500 to-orange-600 shadow-lg">
              <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
          <div>
              <p class="text-xs font-bold uppercase tracking-wider text-orange-600">HỎI ĐÁP BÀI HỌC</p>
              <h3 class="mt-0.5 text-lg font-bold text-slate-900 line-clamp-1">{{ currentLesson?.title || '—' }}</h3>
            </div>
          </div>
          <button
            class="flex h-10 w-10 items-center justify-center rounded-full text-slate-400 transition-all hover:bg-slate-100 hover:text-slate-600 active:scale-95"
            @click="toggleQA(false)"
          >
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Input Area -->
        <div class="border-b border-slate-200 bg-white px-6 py-5 shadow-sm">
          <div class="relative">
          <textarea
            v-model="questionText"
            rows="3"
              class="w-full rounded-2xl border-2 border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 placeholder:text-slate-400 transition-all focus:border-orange-400 focus:bg-white focus:outline-none focus:ring-4 focus:ring-orange-100"
            placeholder="Nhập bình luận mới..."
          ></textarea>
            <div class="absolute bottom-3 right-3 flex items-center gap-2">
              <span v-if="questionText.length > 0" class="text-xs text-slate-400">{{ questionText.length }} ký tự</span>
            </div>
          </div>
          <div class="mt-3 flex justify-end">
            <button
              class="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-orange-500 to-orange-600 px-6 py-2.5 text-sm font-bold text-white shadow-lg shadow-orange-200 transition-all hover:from-orange-600 hover:to-orange-700 hover:shadow-xl hover:-translate-y-0.5 active:translate-y-0 disabled:cursor-not-allowed disabled:from-slate-300 disabled:to-slate-400 disabled:shadow-none disabled:hover:translate-y-0"
              :disabled="sendingQuestion || !canSendQuestion"
              @click="submitQuestion()"
            >
              <span v-if="sendingQuestion" class="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white"></span>
              <span v-else>
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </span>
              Đăng bình luận
            </button>
          </div>
        </div>

        <!-- Comments List -->
        <div class="flex-1 space-y-4 overflow-y-auto px-6 py-6">
          <!-- Loading State -->
          <div v-if="qaLoading" class="flex flex-col items-center justify-center py-12">
            <div class="h-8 w-8 animate-spin rounded-full border-4 border-orange-200 border-t-orange-500"></div>
            <p class="mt-4 text-sm font-medium text-slate-500">Đang tải bình luận…</p>
          </div>
          
          <!-- Empty State -->
          <div v-else-if="qaItems.length === 0" class="flex flex-col items-center justify-center py-12">
            <div class="flex h-16 w-16 items-center justify-center rounded-full bg-slate-100">
              <svg class="h-8 w-8 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <p class="mt-4 text-sm font-semibold text-slate-600">Chưa có bình luận nào</p>
            <p class="mt-1 text-xs text-slate-400">Hãy mở lời trước!</p>
          </div>
          
          <!-- Comments -->
          <div v-else class="space-y-5">
            <div
              v-for="q in qaItems"
              :key="q.id"
              class="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition-all hover:border-slate-300 hover:shadow-md"
            >
              <div class="flex items-start gap-4">
                <!-- Avatar -->
                <div class="relative flex-shrink-0">
                  <div class="relative flex h-12 w-12 items-center justify-center overflow-hidden rounded-full bg-gradient-to-br from-slate-200 to-slate-300 text-sm font-bold text-slate-700 shadow-md ring-2 ring-white transition-all group-hover:ring-orange-200">
                    <!-- Avatar Image -->
                    <img
                      v-if="!avatarErrors[`q-${q.id}`]"
                      :src="avatarUrlForQuestion(q)"
                      :alt="q.student || 'Học sinh'"
                      class="absolute inset-0 h-full w-full object-cover"
                      @error="handleAvatarError(`q-${q.id}`)"
                      @load="handleAvatarLoad(`q-${q.id}`)"
                    />
                    <!-- Fallback Initials -->
                    <span 
                      v-if="avatarErrors[`q-${q.id}`]"
                      class="text-base"
                    >
                      {{ getInitials(q.student) || 'HS' }}
                    </span>
                </div>
                  <div v-if="q.is_owner" class="absolute -bottom-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-orange-500 ring-2 ring-white shadow-md">
                    <svg class="h-3 w-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                  </div>
                </div>
                
                <!-- Content -->
                <div class="flex-1 min-w-0">
                  <!-- Header -->
                  <div class="flex items-start justify-between gap-3">
                    <div class="flex-1 min-w-0">
                    <div class="flex items-center gap-2">
                        <p class="font-bold text-slate-900">{{ q.student || 'Học sinh' }}</p>
                        <span v-if="q.is_owner" class="rounded-full bg-orange-100 px-2 py-0.5 text-xs font-semibold text-orange-700">Bạn</span>
                      </div>
                      <p class="mt-0.5 text-xs text-slate-500">{{ formatDateTimeShort(q.created_at) }}</p>
                    </div>
                    <div class="relative flex-shrink-0">
                        <button
                        class="flex h-8 w-8 items-center justify-center rounded-lg text-slate-400 transition-all hover:bg-slate-100 hover:text-slate-600"
                          @click="toggleQuestionMenu(q.id)"
                      >
                        <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                          <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
                        </svg>
                      </button>
                      <transition name="fade">
                        <div
                          v-if="questionMenu[q.id]"
                          class="absolute right-0 top-full z-10 mt-2 min-w-[140px] rounded-xl border border-slate-200 bg-white py-2 shadow-xl"
                          @click.stop
                        >
                          <button v-if="q.is_owner" class="w-full px-4 py-2 text-left text-sm text-slate-700 hover:bg-slate-50" @click="startEditQuestion(q); questionMenu[q.id]=false">✏️ Sửa</button>
                          <button v-if="q.is_owner" class="w-full px-4 py-2 text-left text-sm text-rose-600 hover:bg-rose-50" @click="deleteQuestion(q.id); questionMenu[q.id]=false">🗑️ Xóa</button>
                          <button v-if="!q.is_owner" class="w-full px-4 py-2 text-left text-sm text-amber-600 hover:bg-amber-50" @click="openReport(q.id, null); questionMenu[q.id]=false">🚨 Báo cáo</button>
                        </div>
                      </transition>
                      </div>
                    </div>
                  
                  <!-- Edit Mode -->
                  <div v-if="editingQuestion.id === q.id" class="mt-3 space-y-3">
                    <textarea
                      v-model="editingQuestion.draft"
                      rows="3"
                      class="w-full rounded-xl border-2 border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 transition-all focus:border-orange-400 focus:bg-white focus:outline-none focus:ring-4 focus:ring-orange-100"
                    ></textarea>
                    <div class="flex gap-2">
                      <button
                        class="rounded-xl bg-gradient-to-r from-orange-500 to-orange-600 px-4 py-2 text-sm font-bold text-white shadow-md transition-all hover:from-orange-600 hover:to-orange-700 hover:shadow-lg active:scale-95"
                        @click="saveEditQuestion(q.id)"
                      >
                        Lưu
                      </button>
                      <button
                        class="rounded-xl border-2 border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition-all hover:bg-slate-50 active:scale-95"
                        @click="cancelEditQuestion"
                      >
                        Hủy
                      </button>
                    </div>
                  </div>
                  
                  <!-- Content -->
                  <p v-else class="mt-3 text-sm leading-relaxed text-slate-800 whitespace-pre-line">{{ q.content }}</p>
                  
                  <!-- Actions -->
                    <div class="mt-4 flex flex-wrap items-center gap-3">
                    <button
                      class="inline-flex items-center gap-1 rounded-full px-3 py-1.5 text-xs font-semibold transition-all"
                      :class="q.reacted ? 'bg-rose-100 text-rose-600' : 'bg-slate-100 text-slate-600 hover:bg-rose-100 hover:text-rose-600'"
                      :disabled="reacting[`q-${q.id}`]"
                      @click="toggleReactionOnQuestion(q.id)"
                    >
                      <span class="text-sm">❤️</span>
                      <span>{{ q.reactions_count || 0 }}</span>
                    </button>
                    <button
                      class="inline-flex items-center gap-1.5 rounded-full bg-sky-50 px-3 py-1.5 text-xs font-semibold text-sky-600 transition-all hover:bg-sky-100 hover:scale-105 active:scale-95"
                      @click="toggleReplyBox(q.id)"
                    >
                      <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6" />
                      </svg>
                      Phản hồi
                    </button>
                    <button
                      class="inline-flex items-center gap-1.5 rounded-full bg-gradient-to-r from-purple-500 to-indigo-500 px-3 py-1.5 text-xs font-semibold text-white shadow-sm transition-all hover:from-purple-600 hover:to-indigo-600 hover:shadow-md hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
                      :disabled="askingAI[q.id]"
                      @click="askAI(q.id)"
                    >
                      <span v-if="askingAI[q.id]" class="h-3 w-3 animate-spin rounded-full border-2 border-white/30 border-t-white"></span>
                      <svg v-else class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                      </svg>
                      {{ askingAI[q.id] ? 'Đang hỏi...' : 'Hỏi AI' }}
                    </button>
                  </div>

                  <!-- Replies -->
                  <div v-if="q.replies && q.replies.length > 0" class="mt-4 space-y-3 border-t border-slate-100 pt-4">
                    <div
                      v-for="rep in q.replies"
                      :key="rep.id"
                      class="group/reply rounded-xl border border-slate-100 bg-gradient-to-br from-slate-50 to-white p-4 shadow-sm transition-all hover:border-slate-200 hover:shadow-md"
                    >
                      <div class="flex items-start gap-3">
                        <!-- Reply Avatar -->
                        <div class="relative flex-shrink-0">
                          <div 
                            class="relative flex h-8 w-8 items-center justify-center overflow-hidden rounded-full text-xs font-bold shadow-sm ring-2 ring-white transition-all group-hover/reply:ring-blue-200"
                            :class="rep.is_teacher 
                              ? 'bg-gradient-to-br from-blue-500 to-blue-600 text-white' 
                              : (rep.user === 'AI_Assistant' ? 'bg-gradient-to-br from-purple-500 to-indigo-500 text-white' : 'bg-gradient-to-br from-slate-200 to-slate-300 text-slate-700')"
                          >
                            <!-- AI Avatar -->
                            <span v-if="rep.user === 'AI_Assistant'" class="text-sm">🤖</span>
                            <!-- Avatar Image -->
                            <img
                              v-else-if="!avatarErrors[`r-${rep.id}`]"
                              :src="avatarUrlForReply(rep)"
                              :alt="rep.is_teacher ? 'Giáo viên' : (rep.user || 'Học sinh')"
                              class="absolute inset-0 h-full w-full object-cover"
                              @error="handleAvatarError(`r-${rep.id}`)"
                              @load="handleAvatarLoad(`r-${rep.id}`)"
                            />
                            <!-- Fallback Initials -->
                            <span 
                              v-else-if="avatarErrors[`r-${rep.id}`]"
                              class="text-xs font-bold"
                            >
                              {{ rep.is_teacher ? 'GV' : getInitials(rep.user) || 'HS' }}
                            </span>
                          </div>
                          <div v-if="rep.user === 'AI_Assistant'" class="absolute -bottom-0.5 -right-0.5 flex h-4 w-4 items-center justify-center rounded-full bg-gradient-to-r from-purple-500 to-indigo-500 ring-2 ring-white shadow-sm">
                            <svg class="h-2.5 w-2.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                            </svg>
                          </div>
                          <div v-else-if="rep.is_teacher" class="absolute -bottom-0.5 -right-0.5 flex h-4 w-4 items-center justify-center rounded-full bg-blue-500 ring-2 ring-white shadow-sm">
                            <svg class="h-2.5 w-2.5 text-white" fill="currentColor" viewBox="0 0 20 20">
                              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                            </svg>
                          </div>
                          <div v-else-if="rep.is_owner" class="absolute -bottom-0.5 -right-0.5 flex h-4 w-4 items-center justify-center rounded-full bg-orange-500 ring-2 ring-white shadow-sm">
                            <svg class="h-2.5 w-2.5 text-white" fill="currentColor" viewBox="0 0 20 20">
                              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                            </svg>
                          </div>
                        </div>
                        
                        <!-- Reply Content -->
                        <div class="flex-1 min-w-0">
                          <div class="flex items-center justify-between gap-2">
                            <div class="flex items-center gap-2">
                              <span class="text-xs font-bold" :class="rep.is_teacher ? 'text-blue-700' : (rep.user === 'AI_Assistant' ? 'text-purple-700' : 'text-slate-700')">
                                {{ rep.is_teacher ? '👨‍🏫 Giáo viên' : (rep.user === 'AI_Assistant' ? '🤖 Trợ lý AI' : rep.user || 'Học sinh') }}
                              </span>
                              <span v-if="rep.user === 'AI_Assistant'" class="rounded-full bg-gradient-to-r from-purple-100 to-indigo-100 px-1.5 py-0.5 text-xs font-semibold text-purple-700">AI</span>
                              <span v-else-if="rep.is_owner" class="rounded-full bg-orange-100 px-1.5 py-0.5 text-xs font-semibold text-orange-700">Bạn</span>
                        </div>
                        <div class="flex items-center gap-2">
                          <span class="text-xs text-slate-400">{{ formatDateTimeShort(rep.created_at) }}</span>
                          <div class="relative">
                                <button
                                  class="flex h-6 w-6 items-center justify-center rounded text-slate-400 transition-all hover:bg-slate-100 hover:text-slate-600"
                                  @click="toggleReplyMenu(rep.id)"
                                >
                                  <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                                    <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
                                  </svg>
                                </button>
                                <transition name="fade">
                                  <div
                                    v-if="replyMenu[rep.id]"
                                    class="absolute right-0 top-full z-10 mt-2 min-w-[140px] rounded-xl border border-slate-200 bg-white py-2 shadow-xl"
                                    @click.stop
                                  >
                                    <button v-if="rep.is_owner" class="w-full px-4 py-2 text-left text-sm text-slate-700 hover:bg-slate-50" @click="startEditReply(rep); replyMenu[rep.id]=false">✏️ Sửa</button>
                                    <button v-if="rep.is_owner" class="w-full px-4 py-2 text-left text-sm text-rose-600 hover:bg-rose-50" @click="deleteReply(rep.id, q.id); replyMenu[rep.id]=false">🗑️ Xóa</button>
                                    <button v-if="!rep.is_owner" class="w-full px-4 py-2 text-left text-sm text-amber-600 hover:bg-amber-50" @click="openReport(null, rep.id); replyMenu[rep.id]=false">🚨 Báo cáo</button>
                            </div>
                                </transition>
                          </div>
                        </div>
                      </div>
                          
                          <!-- Edit Reply -->
                          <div v-if="editingReply.id === rep.id" class="mt-3 space-y-2">
                        <textarea
                          v-model="editingReply.draft"
                          rows="2"
                              class="w-full rounded-lg border-2 border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 transition-all focus:border-orange-400 focus:outline-none focus:ring-4 focus:ring-orange-100"
                        ></textarea>
                        <div class="flex gap-2">
                              <button
                                class="rounded-lg bg-gradient-to-r from-orange-500 to-orange-600 px-3 py-1.5 text-xs font-bold text-white shadow-md transition-all hover:from-orange-600 hover:to-orange-700 active:scale-95"
                                @click="saveEditReply(rep.id, q.id)"
                              >
                            Lưu
                          </button>
                              <button
                                class="rounded-lg border-2 border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-700 transition-all hover:bg-slate-50 active:scale-95"
                                @click="cancelEditReply"
                              >
                            Hủy
                          </button>
                        </div>
                      </div>
                          
                          <!-- Reply Text -->
                          <p v-else class="mt-2 text-sm leading-relaxed text-slate-800 whitespace-pre-line">{{ rep.content }}</p>
                          
                          <!-- Reply Actions -->
                          <div class="mt-3 flex items-center gap-3">
                        <button
                              class="inline-flex items-center gap-1 rounded-full px-2.5 py-1 text-xs font-semibold transition-all"
                              :class="rep.reacted ? 'bg-rose-100 text-rose-600' : 'bg-slate-100 text-slate-600 hover:bg-rose-100 hover:text-rose-600'"
                          :disabled="reacting[rep.id]"
                          @click="toggleReaction(rep.id)"
                        >
                              <span class="text-sm">❤️</span>
                              <span>{{ rep.reactions_count || 0 }}</span>
                        </button>
                            <!-- Nút chat tiếp với AI -->
                            <button 
                              v-if="rep.user === 'AI_Assistant'" 
                              class="inline-flex items-center gap-1 rounded-full bg-gradient-to-r from-purple-500 to-indigo-500 px-2.5 py-1 text-xs font-semibold text-white transition-all hover:from-purple-600 hover:to-indigo-600 hover:scale-105 active:scale-95"
                              @click="toggleAIChatBox(q.id, rep.id)"
                            >
                              <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                              </svg>
                              Chat tiếp
                            </button>
                            <button v-if="rep.is_owner" class="text-xs font-semibold text-sky-600 hover:underline" @click="startEditReply(rep)">Sửa</button>
                            <button v-if="rep.is_owner" class="text-xs font-semibold text-rose-600 hover:underline" @click="deleteReply(rep.id, q.id)">Xóa</button>
                            <button class="text-xs font-semibold text-amber-600 hover:underline" @click="openReport(null, rep.id)">Báo cáo</button>
                          </div>
                          
                          <!-- AI Chat Box -->
                          <transition name="slide-down">
                            <div v-if="aiChatBox[`${q.id}-${rep.id}`]" class="mt-3 space-y-2 rounded-xl border-2 border-purple-200 bg-gradient-to-br from-purple-50 to-indigo-50 p-3">
                              <div class="flex items-center gap-2 text-xs font-semibold text-purple-700">
                                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                                </svg>
                                Hỏi thêm AI
                              </div>
                              <textarea
                                v-model="aiChatDrafts[`${q.id}-${rep.id}`]"
                                rows="2"
                                class="w-full rounded-lg border-2 border-purple-200 bg-white px-3 py-2 text-sm text-slate-900 placeholder:text-slate-400 transition-all focus:border-purple-400 focus:outline-none focus:ring-4 focus:ring-purple-100"
                                placeholder="Nhập câu hỏi tiếp theo cho AI..."
                              ></textarea>
                              <div class="flex justify-end gap-2">
                                <button
                                  class="rounded-lg border-2 border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-700 transition-all hover:bg-slate-50 active:scale-95"
                                  @click="toggleAIChatBox(q.id, rep.id)"
                                >
                                  Hủy
                                </button>
                                <button
                                  class="inline-flex items-center gap-1.5 rounded-lg bg-gradient-to-r from-purple-500 to-indigo-500 px-4 py-1.5 text-xs font-bold text-white shadow-md transition-all hover:from-purple-600 hover:to-indigo-600 hover:shadow-lg active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
                                  :disabled="askingAI[q.id] || !(aiChatDrafts[`${q.id}-${rep.id}`]?.trim())"
                                  @click="continueAIChat(q.id, rep.id)"
                                >
                                  <span v-if="askingAI[q.id]" class="h-3 w-3 animate-spin rounded-full border-2 border-white/30 border-t-white"></span>
                                  <svg v-else class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                                  </svg>
                                  {{ askingAI[q.id] ? 'Đang hỏi...' : 'Gửi' }}
                                </button>
                              </div>
                            </div>
                          </transition>
                        </div>
                      </div>
                      </div>
                    </div>

                  <!-- Reply Box -->
                  <transition name="slide-down">
                    <div v-if="replyBox[q.id]" class="mt-4 space-y-3 rounded-xl border-2 border-dashed border-slate-200 bg-slate-50 p-4">
                      <textarea
                        v-model="replyDrafts[q.id]"
                        rows="2"
                        class="w-full rounded-xl border-2 border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 placeholder:text-slate-400 transition-all focus:border-orange-400 focus:outline-none focus:ring-4 focus:ring-orange-100"
                        placeholder="Viết phản hồi của bạn..."
                      ></textarea>
                      <div class="flex justify-end gap-2">
                        <button
                          class="rounded-xl border-2 border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition-all hover:bg-slate-50 active:scale-95"
                          @click="toggleReplyBox(q.id)"
                        >
                          Hủy
                        </button>
                        <button
                          class="rounded-xl bg-gradient-to-r from-orange-500 to-orange-600 px-5 py-2 text-sm font-bold text-white shadow-md transition-all hover:from-orange-600 hover:to-orange-700 hover:shadow-lg active:scale-95 disabled:cursor-not-allowed disabled:from-slate-300 disabled:to-slate-400 disabled:shadow-none"
                          :disabled="replying[q.id] || !(replyDrafts[q.id]?.trim())"
                          @click="submitReply(q.id)"
                        >
                          <span v-if="replying[q.id]" class="inline-flex items-center gap-2">
                            <span class="h-3 w-3 animate-spin rounded-full border-2 border-white/30 border-t-white"></span>
                            Đang gửi...
                          </span>
                          <span v-else>Gửi phản hồi</span>
                        </button>
                      </div>
                    </div>
                  </transition>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Modal báo cáo -->
    <transition name="fade">
      <div
        v-if="reporting.open"
        class="modal-backdrop fixed inset-0 z-50 flex items-center justify-center p-4"
        @click.self="reporting.open = false"
      >
        <div class="w-full max-w-md rounded-2xl bg-white p-5 shadow-2xl">
          <h3 class="mb-3 text-lg font-semibold text-slate-900">Báo cáo vi phạm</h3>
          <div class="space-y-3">
            <input
              v-model="reporting.reason"
              type="text"
              class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm focus:border-amber-400 focus:outline-none focus:ring-2 focus:ring-amber-100"
              placeholder="Lý do (vd: Nội dung không phù hợp)"
            />
            <textarea
              v-model="reporting.detail"
              rows="3"
              class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm focus:border-amber-400 focus:outline-none focus:ring-2 focus:ring-amber-100"
              placeholder="Mô tả chi tiết..."
            ></textarea>
          </div>
          <div class="mt-4 flex justify-end gap-2">
            <button
              class="rounded-lg border px-4 py-2 text-sm font-semibold text-slate-600 hover:bg-slate-50"
              @click="reporting.open = false"
            >
              Hủy
            </button>
            <button
              class="rounded-lg bg-amber-500 px-4 py-2 text-sm font-semibold text-white hover:bg-amber-600"
              @click="submitReport"
            >
              Gửi báo cáo
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Modal làm bài tập -->
    <transition name="fade">
      <div
        v-if="exercisePlayer.open"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 px-4 py-6"
        @click.self="exercisePlayer.open = false"
      >
        <div class="max-h-[90vh] w-full max-w-3xl overflow-y-auto rounded-2xl bg-white p-6 shadow-xl">
          <div class="mb-4 flex items-center justify-between">
            <div>
              <p class="text-xs uppercase tracking-wide text-slate-500">Bài tập</p>
              <h3 class="text-xl font-bold text-gray-900">{{ exercisePlayer.exercise?.title || 'Bài tập' }}</h3>
            </div>
            <button class="text-sm text-slate-500 hover:text-slate-700" @click="exercisePlayer.open = false">Đóng</button>
          </div>

          <div v-if="exercisePlayer.loading" class="py-10 text-center text-slate-500">Đang tải câu hỏi...</div>

          <div v-else>
            <div v-for="(q, idx) in exercisePlayer.questions" :key="q.id" class="mb-4 rounded-xl border border-slate-200 p-4">
              <div class="mb-2 flex items-start justify-between gap-2">
                <span class="rounded bg-cyan-50 px-2 py-1 text-xs font-semibold text-cyan-700">Câu {{ idx + 1 }}</span>
                <div class="flex items-center gap-2">
                  <!-- Nút gợi ý AI -->
                  <AIHintButton
                    v-if="!exercisePlayer.submitted"
                    :question-text="q.prompt"
                    :choices="q.choices?.map((c: any) => c.text)"
                  />
                  <span class="text-xs font-medium text-slate-500">{{ q.type }}</span>
                </div>
              </div>
              <p class="mb-3 text-sm font-semibold text-gray-900">{{ q.prompt }}</p>

              <!-- MCQ -->
              <div v-if="q.type === 'mcq'" class="space-y-2">
                <label
                  v-for="choice in q.choices"
                  :key="choice.id"
                  class="flex items-center gap-2 rounded-lg border border-slate-200 px-3 py-2 text-sm hover:bg-slate-50"
                >
                  <input
                    v-if="q.meta?.multiple"
                    type="checkbox"
                    :value="choice.id"
                    class="h-4 w-4 text-cyan-600"
                    v-model="exercisePlayer.answers[q.id]"
                    :disabled="exercisePlayer.submitted"
                  />
                  <input
                    v-else
                    type="radio"
                    :name="`q-${q.id}`"
                    :value="choice.id"
                    class="h-4 w-4 text-cyan-600"
                    v-model="exercisePlayer.answers[q.id]"
                    :disabled="exercisePlayer.submitted"
                  />
                  <span>{{ choice.text }}</span>
                </label>
              </div>

              <!-- Short answer -->
              <div v-else-if="q.type === 'short_answer'">
                <textarea
                  v-model="exercisePlayer.answers[q.id]"
                  rows="3"
                  class="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
                  placeholder="Nhập câu trả lời..."
                  :disabled="exercisePlayer.submitted"
                ></textarea>
              </div>

              <!-- Matching -->
              <div v-else-if="q.type === 'matching'" class="space-y-2">
                <div
                  v-for="pair in buildMatchingOptions(q)"
                  :key="pair.leftId"
                  class="flex items-center gap-2"
                >
                  <span class="w-1/2 rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm">{{ pair.leftText }}</span>
                  <select
                    class="w-1/2 rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
                    :value="exercisePlayer.answers[q.id]?.[pair.leftId] || ''"
                    :disabled="exercisePlayer.submitted"
                    @change="handleAnswerChange(q, { ...(exercisePlayer.answers[q.id] || {}), [pair.leftId]: ($event.target as HTMLSelectElement).value })"
                  >
                    <option value="">Chọn vế phải</option>
                    <option v-for="opt in pair.rights" :key="opt.rightId" :value="opt.rightId">
                      {{ opt.rightText }}
                    </option>
                  </select>
                </div>
              </div>

              <div v-else class="text-sm text-slate-500">Loại câu hỏi chưa hỗ trợ hiển thị.</div>
            </div>

            <div class="mt-6 flex items-center justify-between">
              <div v-if="exercisePlayer.result" class="text-sm text-green-600">
                Điểm: {{ exercisePlayer.result.score ?? 0 }}
              </div>
              <div class="flex gap-2">
                <button
                  class="rounded-lg border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50"
                  @click="exercisePlayer.open = false"
                  :disabled="exercisePlayer.submitting"
                >
                  Hủy
                </button>
                <button
                  class="rounded-lg bg-cyan-600 px-4 py-2 text-sm font-semibold text-white hover:bg-cyan-700 disabled:opacity-50"
                  @click="submitExercise"
                  :disabled="exercisePlayer.submitting || exercisePlayer.submitted"
                >
                  <span v-if="exercisePlayer.submitted">Đã nộp</span>
                  <span v-else-if="exercisePlayer.submitting">Đang nộp...</span>
                  <span v-else>Nộp bài</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Modal Hỏi AI về Video -->
    <transition name="fade">
      <div
        v-if="aiVideoModalOpen"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm px-4 py-6"
        @click.self="closeAIVideoModal"
      >
        <div class="w-full max-w-2xl rounded-3xl bg-white shadow-2xl overflow-hidden">
          <!-- Header -->
          <div class="bg-gradient-to-r from-purple-500 to-indigo-600 px-6 py-5">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-white/20 backdrop-blur">
                  <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <div>
                  <p class="text-xs font-bold uppercase tracking-wider text-purple-200">HỎI AI VỀ VIDEO</p>
                  <h3 class="text-lg font-bold text-white">Tại {{ formatTimestamp(aiVideoTimestamp) }}</h3>
                </div>
              </div>
              <button
                class="flex h-10 w-10 items-center justify-center rounded-full text-white/70 transition-all hover:bg-white/20 hover:text-white"
                @click="closeAIVideoModal"
              >
                <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Conversation -->
          <div class="max-h-[400px] overflow-y-auto px-6 py-4 space-y-4">
            <!-- Empty state -->
            <div v-if="aiVideoConversation.length === 0" class="text-center py-8">
              <div class="flex h-16 w-16 mx-auto items-center justify-center rounded-full bg-purple-100">
                <svg class="h-8 w-8 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <p class="mt-4 text-sm font-semibold text-slate-600">Hỏi AI về đoạn video này!</p>
              <p class="mt-1 text-xs text-slate-400">Bạn đang xem tại {{ formatTimestamp(aiVideoTimestamp) }}</p>
            </div>

            <!-- Messages -->
            <div v-for="(msg, idx) in aiVideoConversation" :key="idx" class="flex gap-3" :class="msg.role === 'user' ? 'justify-end' : 'justify-start'">
              <!-- AI Avatar - Mặt Trời -->
              <div v-if="msg.role === 'ai'" class="flex-shrink-0">
                <div class="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-yellow-400 to-orange-500 shadow-lg shadow-orange-200">
                  <span class="text-xl">☀️</span>
                </div>
              </div>
              
              <!-- Message bubble -->
              <div 
                class="max-w-[80%] rounded-2xl px-4 py-3"
                :class="msg.role === 'user' 
                  ? 'bg-gradient-to-r from-purple-500 to-indigo-600 text-white' 
                  : 'bg-slate-100 text-slate-800'"
              >
                <p v-if="msg.timestamp && msg.role === 'user'" class="text-xs mb-1" :class="msg.role === 'user' ? 'text-purple-200' : 'text-slate-500'">
                  Tại {{ msg.timestamp }}
                </p>
                <p class="text-sm whitespace-pre-line">{{ msg.content }}</p>
              </div>

              <!-- User Avatar -->
              <div v-if="msg.role === 'user'" class="flex-shrink-0">
                <div class="flex h-10 w-10 items-center justify-center rounded-full bg-slate-200 text-slate-600 text-sm font-bold">
                  {{ auth.user?.name?.charAt(0) || 'HS' }}
                </div>
              </div>
            </div>

            <!-- Loading -->
            <div v-if="aiVideoAsking" class="flex gap-3 justify-start">
              <div class="flex-shrink-0">
                <div class="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-yellow-400 to-orange-500 shadow-lg shadow-orange-200 animate-pulse">
                  <span class="text-xl">☀️</span>
                </div>
              </div>
              <div class="bg-slate-100 rounded-2xl px-4 py-3">
                <div class="flex items-center gap-2">
                  <div class="h-2 w-2 rounded-full bg-purple-500 animate-bounce" style="animation-delay: 0ms"></div>
                  <div class="h-2 w-2 rounded-full bg-purple-500 animate-bounce" style="animation-delay: 150ms"></div>
                  <div class="h-2 w-2 rounded-full bg-purple-500 animate-bounce" style="animation-delay: 300ms"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Input -->
          <div class="border-t border-slate-200 px-6 py-4">
            <div class="flex gap-3">
              <input
                v-model="aiVideoQuestion"
                type="text"
                class="flex-1 rounded-xl border-2 border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 placeholder:text-slate-400 transition-all focus:border-purple-400 focus:bg-white focus:outline-none focus:ring-4 focus:ring-purple-100"
                placeholder="Hỏi về đoạn video này..."
                @keyup.enter="submitAIVideoQuestion"
                :disabled="aiVideoAsking"
              />
              <button
                class="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-purple-500 to-indigo-600 px-5 py-3 text-sm font-bold text-white shadow-lg shadow-purple-200 transition-all hover:from-purple-600 hover:to-indigo-700 hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="!aiVideoQuestion.trim() || aiVideoAsking"
                @click="submitAIVideoQuestion"
              >
                <span v-if="aiVideoAsking" class="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white"></span>
                <svg v-else class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </button>
            </div>
            <div class="mt-3 flex items-center justify-between">
              <p class="text-xs text-slate-400">
                Đang xem: {{ currentLesson?.title || 'Video' }}
              </p>
              <button
                v-if="aiVideoConversation.length > 0"
                class="text-xs text-slate-500 hover:text-slate-700 transition"
                @click="clearAIVideoConversation"
              >
                Xóa hội thoại
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
  <div v-else class="grid min-h-screen place-items-center text-gray-600 dark:text-gray-400">Đang tải…</div>
  
  <!-- 🎉 Celebration khi hoàn thành khóa học -->
  <CourseCompletionCelebration
    :show="showCelebration"
    :course-title="course?.title || 'Khóa học'"
    @close="showCelebration = false"
  />
</template>

<script setup lang="ts">
import { computed, onMounted, onBeforeUnmount, reactive, ref, watchEffect, watch, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { courseService, type CourseDetail } from '@/services/course.service'
import { contentService } from '@/services/content.service'
import AIHintButton from '@/components/ai/AIHintButton.vue'
import CourseCompletionCelebration from '@/components/ui/CourseCompletionCelebration.vue'
import api from '@/config/axios'
import { showToast } from '@/utils/toast'
import { getAvatarSrc } from '@/utils/avatar'
import { useAuthStore } from '@/store/auth.store'

type Lesson = CourseDetail['sections'][0]['lessons'][0];

const router = useRouter()
const route = useRoute()

const course = ref<CourseDetail | null>(null)
const auth = useAuthStore()
const videoRef = ref<HTMLVideoElement|null>(null)
const youtubeIframeRef = ref<HTMLIFrameElement|null>(null)
const youtubePlayer = ref<any>(null)
const doneSet = reactive(new Set<string>())
const openIndex = ref<number>(0)
const cur = ref<{ si: number; li: number }>({ si: 0, li: 0 })

// Lesson detail and progress
const currentLessonDetail = ref<any>(null)
const currentLessonExercises = ref<any[]>([])
const lessonProgress = ref<any>(null)
const lessonLocked = ref(false)
const unlockReason = ref<string>('')
const videoWatchedPercentage = ref<number>(0)
const hasMarkedAsWatched = ref<boolean>(false)
const WATCHED_THRESHOLD = 75 // Phải xem 75% video mới tính là đã xem
const autoCompletedLessons = new Set<string>()

function isTodayLocal(dateInput?: string | Date | null): boolean {
  if (!dateInput) return false
  const date = dateInput instanceof Date ? dateInput : new Date(dateInput)
  if (Number.isNaN(date.getTime())) return false
  const now = new Date()
  return date.getFullYear() === now.getFullYear() &&
    date.getMonth() === now.getMonth() &&
    date.getDate() === now.getDate()
}

function hasProgressToday(progress?: any): boolean {
  if (!progress) return false
  return isTodayLocal(progress.last_accessed_at) || isTodayLocal(progress.completed_at)
}

// Celebration state
const showCelebration = ref(false)
const hasShownCelebration = ref(false)

// Làm bài tập ngay trong trang xem bài học
const exercisePlayer = reactive({
  open: false,
  loading: false,
  submitting: false,
  result: null as any,
  submitted: false,
  exercise: null as any,
  attemptId: '' as string,
  questions: [] as any[],
  answers: {} as Record<string, any>
})

function normalizeRouteParam(param: any): string | number | undefined {
  if (Array.isArray(param)) return param[0]
  return param as string | number | undefined
}

const courseId = computed(() => {
  const raw = normalizeRouteParam(route.params.id)
  return raw != null ? String(raw) : ''
})

async function load() {
  const id = courseId.value
  const lessonParam = normalizeRouteParam(route.params.lessonId) as any
  if (!id) {
    console.warn('Missing course id in route params')
    return
  }
  
  // Sử dụng student API endpoint để lấy isEnrolled
  try {
    const { data } = await api.get(`/student/courses/${id}/`)
    course.value = data
    
    // Cập nhật doneSet từ course data (sync với backend progress)
    if (data && data.sections) {
      doneSet.clear() // Clear trước để tránh duplicate
      doneSetTrigger.value++ // Force reactivity
      data.sections.forEach((section: any) => {
        if (section.lessons && Array.isArray(section.lessons)) {
          section.lessons.forEach((lesson: any) => {
            // Check nhiều cách để đảm bảo nhận được completed status
            const isCompleted = lesson.completed === true || 
                               lesson.completed === 'true' || 
                               lesson.completed === 1 ||
                               lesson.completed === '1' ||
                               lesson.videoWatched === true ||
                               lesson.videoWatched === 'true'
            
            if (isCompleted) {
              doneSet.add(String(lesson.id))
              console.log('Loaded completed lesson:', lesson.id, lesson.title)
            }
          })
        }
      })
      // Force reactivity sau khi load
      doneSetTrigger.value++
      console.log('Loaded progress from backend:', doneSet.size, 'lessons completed, total sections:', data.sections?.length || 0)
      
      // Rebuild UI sau khi load
      await nextTick()
      rebuildAndKeepCursor(lessonParam ?? null)
    } else {
      console.warn('No sections found in course data:', data)
    }
  } catch (e: any) {
    // Fallback to regular endpoint nếu student endpoint không có
    const d = await courseService.detail(id)
    course.value = d
  }
  
  // Kiểm tra enrollment - nếu chưa enroll thì redirect về course detail
  // Chỉ redirect nếu thực sự chưa enroll (không phải do API chưa trả về)
  if (course.value && (course.value as any).isEnrolled === false) {
    console.log('Course not enrolled, redirecting to detail page')
    router.push({ name: 'student-course-detail', params: { id } })
    return
  }
  
  // Nếu isEnrolled không có trong response, giả sử đã enroll (để tránh redirect loop)
  if (course.value && (course.value as any).isEnrolled === undefined) {
    console.log('isEnrolled not in response, assuming enrolled')
  }
  
  rebuildAndKeepCursor(lessonParam ?? null)
  if (lessonParam) openIndex.value = findById(lessonParam)?.si ?? 0
}

type LessonKind = 'video' | 'text' | 'image' | 'pdf' | 'doc' | 'quiz' | 'unknown'
type UiLesson = {
  id: string|number
  title: string
  durationMinutes?: number
  type?: string
  done?: boolean
  kind: LessonKind
}
type UiSection = { id: string|number; title: string; items: UiLesson[] }
const uiSections = ref<UiSection[]>([])
type LessonState = LessonKind | 'done' | 'current' | 'next'
const lessonStateLabels: Record<LessonState, string> = {
  done: 'Đã hoàn thành',
  current: 'Đang học',
  next: 'Bài tiếp theo',
  video: 'Video bài giảng',
  text: 'Nội dung văn bản',
  image: 'Hình ảnh',
  pdf: 'Tài liệu PDF',
  doc: 'Tài liệu',
  quiz: 'Bài luyện tập',
  unknown: 'Tài nguyên khóa học'
}
const lessonStateColors: Record<LessonState, string> = {
  done: 'bg-emerald-100 text-emerald-600',
  current: 'bg-cyan-600 text-white',
  next: 'bg-cyan-100 text-cyan-600',
  video: 'bg-cyan-50 text-cyan-600',
  text: 'bg-slate-100 text-slate-500',
  image: 'bg-indigo-100 text-indigo-600',
  pdf: 'bg-rose-100 text-rose-600',
  doc: 'bg-slate-100 text-slate-500',
  quiz: 'bg-amber-100 text-amber-600',
  unknown: 'bg-slate-100 text-slate-500'
}

const lessonKindLabels: Record<LessonKind, string> = {
  video: 'Video bài giảng',
  text: 'Văn bản',
  image: 'Hình ảnh',
  pdf: 'Tài liệu PDF',
  doc: 'Tài liệu',
  quiz: 'Bài tập',
  unknown: 'Bài học'
}

type LessonIntroMeta = {
  contentType?: string
  payload?: any
} | null

const QUIZ_KEYWORDS = ['quiz', 'exercise', 'question', 'exam', 'test', 'practice']
const VIDEO_KEYWORDS = ['video', 'mp4', 'mov', 'm4v', 'avi', 'mkv', 'youtube', 'youtu', 'vimeo']
const PDF_KEYWORDS = ['pdf']
const DOC_KEYWORDS = ['doc', 'docx', 'word', 'ppt', 'pptx', 'slides', 'presentation', 'xls', 'xlsx', 'sheet', 'document']
const IMAGE_KEYWORDS = ['image', 'img', 'png', 'jpg', 'jpeg', 'gif', 'svg', 'bmp', 'webp', 'photo', 'ảnh']
const TEXT_KEYWORDS = ['text', 'txt', 'markdown', 'note', 'article', 'md', 'văn bản']

function matchKindFromString(value?: string | null): LessonKind | null {
  if (!value) return null
  const lowered = value.toString().toLowerCase()
  if (QUIZ_KEYWORDS.some((key) => lowered.includes(key))) return 'quiz'
  if (VIDEO_KEYWORDS.some((key) => lowered.includes(key))) return 'video'
  if (PDF_KEYWORDS.some((key) => lowered.includes(key))) return 'pdf'
  if (DOC_KEYWORDS.some((key) => lowered.includes(key))) return 'doc'
  if (IMAGE_KEYWORDS.some((key) => lowered.includes(key))) return 'image'
  if (TEXT_KEYWORDS.some((key) => lowered.includes(key))) return 'text'
  return null
}

function kindFromPayload(payload: any): LessonKind | null {
  if (!payload || typeof payload !== 'object') return null
  const candidateKeys = ['contentType', 'type', 'mimeType', 'mime', 'fileType', 'format']
  for (const key of candidateKeys) {
    const match = matchKindFromString(payload[key])
    if (match) return match
  }
  const fileName = payload.fileName || payload.name
  if (typeof fileName === 'string') {
    const ext = fileName.split('.').pop()?.toLowerCase()
    const extMatch = matchKindFromString(ext)
    if (extMatch) return extMatch
  }
  const url = payload.url || payload.fileData || payload.embedUrl
  if (typeof url === 'string') {
    const cleanUrl = url.split('?')[0]
    const urlExt = cleanUrl.includes('.') ? cleanUrl.split('.').pop() : url
    const urlMatch = matchKindFromString(urlExt)
    if (urlMatch) return urlMatch
  }
  if (payload.questions || payload.quiz || payload.items || payload.options || payload.answers) {
    return 'quiz'
  }
  if (payload.text || payload.content || payload.html || payload.markdown) {
    return 'text'
  }
  if (payload.image || payload.imageUrl || payload.image_url || payload.images || payload.picture) {
    return 'image'
  }
  return null
}

function parseJsonLike(value: any): any {
  if (typeof value !== 'string') return value
  const trimmed = value.trim()
  if (!trimmed) return null
  const isJson =
    (trimmed.startsWith('{') && trimmed.endsWith('}')) ||
    (trimmed.startsWith('[') && trimmed.endsWith(']'))
  if (!isJson) return null
  try {
    return JSON.parse(trimmed)
  } catch {
    return null
  }
}

function normalizeIntroduction(intro: any): LessonIntroMeta {
  if (!intro) return null
  let current: any = intro
  
  // Nếu là string rỗng, return null
  if (typeof current === 'string' && !current.trim()) return null
  
  for (let depth = 0; depth < 5; depth++) {
    if (!current) return null
    
    // Parse JSON string
    if (typeof current === 'string') {
      const trimmed = current.trim()
      if (!trimmed) return null
      
      // Thử parse JSON
      const parsed = parseJsonLike(trimmed)
      if (parsed) {
        current = parsed
        continue
      }
      
      // Nếu không phải JSON nhưng có nội dung, coi như text
      if (trimmed.length > 0 && !trimmed.startsWith('{') && !trimmed.startsWith('[')) {
        return {
          contentType: 'text',
          payload: { content: trimmed }
        }
      }
      
      return null
    }
    
    // Xử lý object
    if (typeof current === 'object' && current !== null) {
      const payloadRaw = (current as any).payload
      const payloadParsed = parseJsonLike(payloadRaw)
      const payload =
        payloadParsed && typeof payloadParsed === 'object'
          ? payloadParsed
          : typeof payloadRaw === 'object' && payloadRaw !== null
            ? payloadRaw
            : typeof payloadRaw === 'string' && payloadRaw.trim()
              ? { content: payloadRaw }
              : undefined
      
      const contentType =
        (current as any).contentType ||
        (current as any).type ||
        (payload && (payload.contentType || payload.type))
      
      // Nếu có contentType hoặc payload, return
      if (contentType || payload) {
        return {
          contentType: typeof contentType === 'string' ? contentType : undefined,
          payload: payload || {},
        }
      }
      
      // Nếu có introduction nested, tiếp tục parse
      if ((current as any).introduction) {
        current = (current as any).introduction
        continue
      }
      
      // Nếu có payload nhưng chưa return, tiếp tục với payload
      if (payload) {
        current = payload
        continue
      }
      
      // Nếu object có keys nhưng không match pattern, coi như text
      const keys = Object.keys(current)
      if (keys.length > 0) {
        // Kiểm tra xem có phải là object chứa nội dung text không
        if ('content' in current || 'text' in current || 'html' in current) {
          return {
            contentType: 'text',
            payload: current
          }
        }
      }
      
      return null
    }
    return null
  }
  return null
}

function resolveLessonKind(lesson: any, introOverride?: LessonIntroMeta | null): LessonKind {
  // Ưu tiên kiểm tra content_type từ backend trước
  const contentType = lesson?.content_type?.toLowerCase()
  if (contentType) {
    if (contentType === 'exercise' || contentType === 'quiz') return 'quiz'
    if (contentType === 'pdf') return 'pdf'
    if (contentType === 'text') return 'text'
    if (contentType === 'document') return 'doc'
    if (contentType === 'video') return 'video'
  }
  
  const explicitType = String(lesson?.type || '').toLowerCase()
  if (explicitType && explicitType !== 'lesson') {
    const match = matchKindFromString(explicitType)
    if (match) return match
  }
  
  const introMeta = introOverride ?? normalizeIntroduction(lesson?.introduction)
  const payloadKind = kindFromPayload(introMeta?.payload)
  if (payloadKind) return payloadKind
  const introKind = matchKindFromString(introMeta?.contentType)
  if (introKind) return introKind
  
  if (lesson?.video_url || lesson?.video_file) {
    return 'video'
  }
  if (lesson?.document_file) {
    return 'pdf'
  }
  if (lesson?.text_content) {
    return 'text'
  }
  return 'text'
}

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
      done: doneSet.has(String(l.id)),
      kind: resolveLessonKind(l)
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
// Force reactivity bằng cách tạo computed từ reactive Set
const doneSetTrigger = ref(0) // Trigger để force reactivity
const doneCount = computed(() => {
  // Access trigger để force reactivity
  doneSetTrigger.value // Trigger reactivity
  // Access doneSet để track changes
  const size = doneSet.size
  return size
})
const progressPct = computed(() => {
  const total = totalCount.value
  const done = doneCount.value
  const pct = total > 0 ? Math.round((done / total) * 100) : 0
  console.log('Progress calculation:', done, '/', total, '=', pct + '%')
  return pct
})
const dash = computed(() => progressPct.value)

const currentLesson = computed<UiLesson | null>(() => uiSections.value[cur.value.si]?.items[cur.value.li] || null);
const currentLessonId = computed(() => currentLesson.value?.id || null)
const qaLessonId = computed(() => {
  return (
    currentLessonId.value ||
    currentLessonDetail.value?.id ||
    normalizeRouteParam(route.params.lessonId) ||
    null
  )
})
const currentLessonTitle = computed(() => currentLesson.value?.title || '')

const currentLessonIntro = computed(() => normalizeIntroduction(currentLessonDetail.value?.introduction))

const lessonContentPayload = computed(() => {
  const intro = currentLessonDetail.value?.introduction
  const meta = currentLessonIntro.value
  
  // Nếu có meta từ normalizeIntroduction, dùng nó
  if (meta) {
    const payload = (meta.payload && typeof meta.payload === 'object') ? meta.payload : {}
    
    // Ưu tiên: contentType từ meta, sau đó infer từ payload, cuối cùng dùng currentLessonKind
    let contentType = matchKindFromString(meta.contentType) || kindFromPayload(payload)
    
    // Nếu vẫn không có, dùng currentLessonKind làm fallback (nhưng chỉ nếu không phải video)
    if (!contentType && currentLessonKind.value && currentLessonKind.value !== 'video') {
      contentType = currentLessonKind.value
    }
    
    // Nếu có payload hoặc contentType, trả về
    if (contentType || (payload && Object.keys(payload).length > 0)) {
      return {
        contentType: contentType || 'text', // Default to text nếu không xác định được
        payload,
      }
    }
  }
  
  // Fallback: Nếu có introduction nhưng không parse được, coi như text
  if (intro && typeof intro === 'string' && intro.trim()) {
    const trimmed = intro.trim()
    // Nếu không phải JSON string, coi như text content
    if (!trimmed.startsWith('{') && !trimmed.startsWith('[')) {
      return {
        contentType: 'text',
        payload: { content: trimmed }
      }
    }
    // Nếu là JSON string nhưng không parse được, vẫn coi như text
    try {
      JSON.parse(trimmed)
      // Nếu parse được nhưng normalizeIntroduction trả về null, có thể là JSON không đúng format
      // Vẫn return null để fallback về phần render introduction
    } catch {
      // Không phải JSON hợp lệ, coi như text
      return {
        contentType: 'text',
        payload: { content: trimmed }
      }
    }
  }
  
  return null
})

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

const lessonVideoUrl = computed(() => currentLessonDetail.value?.video_url)
const lessonVideoFile = computed(() => currentLessonDetail.value?.video_file)

const libraryMedia = computed(() => {
  if (!lessonContentPayload.value) return { video: null, type: null, payload: null }
  const { contentType: type, payload } = lessonContentPayload.value
  let video: string | null = null
  let doc: string | null = null
  if (type === 'video' && payload) {
    const source = payload.fileData || payload.url || payload.embedUrl
    if (typeof source === 'string') {
      video = isYouTubeUrl(source) ? getYouTubeEmbedUrl(source) : source
    }
  }
  if (type === 'pdf' || type === 'doc') {
    const source = payload?.fileData || payload?.url
    if (typeof source === 'string') {
      doc = resolveDocumentUrl(source)
    }
  }
  return { video, doc, type, payload }
})

const lessonVideoSrc = computed(() => {
  if (libraryMedia.value.video) return libraryMedia.value.video
  if (lessonVideoUrl.value) {
    if (isYouTubeUrl(lessonVideoUrl.value)) {
      return getYouTubeEmbedUrl(lessonVideoUrl.value)
    }
    return lessonVideoUrl.value
  }
  if (lessonVideoFile.value) {
    return getVideoFileUrl(lessonVideoFile.value)
  }
  return null
})

const currentSrc = computed(() => {
  // Ưu tiên video từ lesson
  if (lessonVideoSrc.value) return lessonVideoSrc.value
  // Nếu có video_url hoặc video_file từ course, dùng nó
  if (course.value?.video_url) {
    if (isYouTubeUrl(course.value.video_url)) {
      return getYouTubeEmbedUrl(course.value.video_url)
    }
    return course.value.video_url
  }
  if (course.value?.video_file) {
    return getVideoFileUrl(course.value.video_file)
  }
  // Fallback: mock video
  return null
})

const docUrlFromPayload = computed(() => {
  if (libraryMedia.value.doc) return libraryMedia.value.doc
  return null
})

const docUrlFromLesson = computed(() => {
  if (currentLessonDetail.value?.document_file) {
    return resolveDocumentUrl(currentLessonDetail.value.document_file)
  }
  return ''
})

const docViewerFromPayload = computed(() => {
  if (!docUrlFromPayload.value) return ''
  return getDocViewerUrl(docUrlFromPayload.value, libraryMedia.value.type === 'doc' ? 'doc' : 'pdf')
})

const docViewerFromLesson = computed(() => {
  if (!docUrlFromLesson.value) return ''
  const type = currentLessonKind.value === 'doc' ? 'doc' : currentLessonKind.value === 'pdf' ? 'pdf' : undefined
  return getDocViewerUrl(docUrlFromLesson.value, type)
})

const currentLessonKind = computed<LessonKind>(() => {
  if (currentLessonDetail.value) {
    return resolveLessonKind(
      { ...(currentLesson.value || {}), ...currentLessonDetail.value },
      currentLessonIntro.value
    )
  }
  if (currentLesson.value) {
    return resolveLessonKind(currentLesson.value)
  }
  return 'text'
})

const currentLessonKindLabel = computed(() => lessonKindLabel(currentLessonKind.value))

const hasVideo = computed(() => {
  if (currentLessonKind.value !== 'video') return false
  return !!lessonVideoSrc.value
})

function isYouTubeUrl(url?: string): boolean {
  if (!url) return false
  return url.includes('youtube.com') || url.includes('youtu.be')
}

function getYouTubeEmbedUrl(url: string): string {
  if (!url) return ''
  let videoId = ''
  if (url.includes('youtube.com/watch?v=')) {
    videoId = url.split('v=')[1]?.split('&')[0] || ''
  } else if (url.includes('youtu.be/')) {
    videoId = url.split('youtu.be/')[1]?.split('?')[0] || ''
  } else if (url.includes('youtube.com/embed/')) {
    videoId = url.split('embed/')[1]?.split('?')[0] || ''
  }
  
  if (!videoId) return url
  
  // Thêm các tham số để cho phép controls và tua video
  const params = new URLSearchParams({
    'enablejsapi': '1',
    'controls': '1', // Cho phép controls
    'rel': '0', // Không hiển thị video liên quan
    'modestbranding': '1', // Giảm branding
    'fs': '1', // Cho phép fullscreen
    'iv_load_policy': '3', // Không hiển thị annotations
  })
  
  return `https://www.youtube.com/embed/${videoId}?${params.toString()}`
}

function getYouTubeVideoId(url: string): string {
  if (!url) return ''
  if (url.includes('youtube.com/watch?v=')) {
    return url.split('v=')[1]?.split('&')[0] || ''
  } else if (url.includes('youtu.be/')) {
    return url.split('youtu.be/')[1]?.split('?')[0] || ''
  } else if (url.includes('youtube.com/embed/')) {
    return url.split('embed/')[1]?.split('?')[0] || ''
  }
  return ''
}

async function onYouTubeIframeLoad() {
  try {
    const videoUrl = lessonVideoUrl.value || course.value?.video_url
    if (!videoUrl || !isYouTubeUrl(videoUrl)) {
      console.log('Not a YouTube URL, skipping YouTube API initialization')
      return
    }
    
    // Load YouTube IFrame API nếu chưa có
    if (!(window as any).YT) {
      // Kiểm tra xem script đã được thêm chưa
      const existingScript = document.querySelector('script[src="https://www.youtube.com/iframe_api"]')
      if (!existingScript) {
        const tag = document.createElement('script')
        tag.src = 'https://www.youtube.com/iframe_api'
        const firstScriptTag = document.getElementsByTagName('script')[0]
        firstScriptTag.parentNode?.insertBefore(tag, firstScriptTag)
      }
      
      // Đợi YouTube API load (với timeout)
      await new Promise((resolve, reject) => {
        const timeout = setTimeout(() => {
          reject(new Error('YouTube API load timeout'))
        }, 10000) // 10 seconds timeout
        
        if ((window as any).YT && (window as any).YT.Player) {
          clearTimeout(timeout)
          resolve(true)
          return
        }
        
        ;(window as any).onYouTubeIframeAPIReady = () => {
          clearTimeout(timeout)
          resolve(true)
        }
      })
    }
    
    // Khởi tạo YouTube player
    const videoId = getYouTubeVideoId(videoUrl)
    if (!videoId || !youtubeIframeRef.value) {
      console.log('Missing videoId or iframe ref')
      return
    }
    
    // Chỉ khởi tạo nếu chưa có player
    if (!youtubePlayer.value) {
      youtubePlayer.value = new (window as any).YT.Player(youtubeIframeRef.value, {
        events: {
          'onStateChange': onYouTubeStateChange,
          'onReady': () => {
            console.log('YouTube player ready')
            // Bắt đầu track progress cho YouTube video
            startYouTubeProgressTracking()
          },
          'onError': (event: any) => {
            console.error('YouTube player error:', event.data)
          }
        }
      })
    }
  } catch (e) {
    console.error('Error initializing YouTube player:', e)
    // Không throw error, chỉ log để video vẫn có thể hiển thị
  }
}

let youtubeProgressInterval: any = null

function startYouTubeProgressTracking() {
  // Clear interval cũ nếu có
  if (youtubeProgressInterval) {
    clearInterval(youtubeProgressInterval)
  }
  
  // Track progress mỗi 2 giây
  youtubeProgressInterval = setInterval(() => {
    if (youtubePlayer.value && youtubePlayer.value.getCurrentTime && youtubePlayer.value.getDuration) {
      try {
        const currentTime = youtubePlayer.value.getCurrentTime()
        const duration = youtubePlayer.value.getDuration()
        if (duration > 0) {
          const percentage = (currentTime / duration) * 100
          videoWatchedPercentage.value = percentage
          checkAndMarkVideoWatched(percentage)
        }
      } catch (e) {
        console.error('Error tracking YouTube progress:', e)
      }
    }
  }, 2000) // Check mỗi 2 giây
}

function onYouTubeStateChange(event: any) {
  // YouTube player states:
  // -1 (unstarted), 0 (ended), 1 (playing), 2 (paused), 3 (buffering), 5 (cued)
  if (event.data === 0) { // Video ended
    // Clear interval khi video kết thúc
    if (youtubeProgressInterval) {
      clearInterval(youtubeProgressInterval)
      youtubeProgressInterval = null
    }
    onVideoEnded()
  } else if (event.data === 1) { // Video playing
    // Bắt đầu track progress khi video bắt đầu phát
    startYouTubeProgressTracking()
  } else if (event.data === 2) { // Video paused
    // Có thể dừng tracking khi pause để tiết kiệm tài nguyên
    // Nhưng giữ lại để tiếp tục track khi resume
  }
}

function getVideoFileUrl(videoFile?: string): string {
  if (!videoFile) return ''
  const apiBase = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/+$/, '')

  // Nếu BE trả về URL tuyệt đối (http/https), map sang endpoint stream để hỗ trợ Range
  if (videoFile.startsWith('http://') || videoFile.startsWith('https://')) {
    try {
      const url = new URL(videoFile)
      const mediaPath = url.pathname.startsWith('/media/') ? url.pathname.replace(/^\/media\//, '') : url.pathname.replace(/^\//, '')
      return `${apiBase}/api/media/stream/${encodeURI(mediaPath)}`
    } catch {
      return videoFile
    }
  }

  // Nếu là path tương đối, cũng đưa qua stream endpoint
  const safePath = videoFile.replace(/^\/+/, '') // bỏ slash đầu để tránh path trống
  return `${apiBase}/api/media/stream/${encodeURI(safePath)}`
}

function getDocumentUrl(documentFile?: string): string {
  if (!documentFile) return ''
  const apiBase = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/+$/, '')

  // Nếu là URL tuyệt đối, trả về luôn
  if (documentFile.startsWith('http://') || documentFile.startsWith('https://')) {
    return documentFile
  }

  // Nếu là path tương đối, thêm media URL
  const safePath = documentFile.replace(/^\/+/, '')
  return `${apiBase}/media/${safePath}`
}

function getDocumentStreamUrl(documentFile?: string): string {
  if (!documentFile) return ''
  const apiBase = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/+$/, '')

  // Data URL hoặc tuyệt đối thì dùng luôn (cùng origin sẽ không bị CORS)
  if (documentFile.startsWith('data:')) return documentFile
  if (documentFile.startsWith('http://') || documentFile.startsWith('https://')) {
    try {
      const url = new URL(documentFile)
      // Nếu cùng host, chuyển qua stream; nếu khác host, giữ nguyên để tải
      const apiHost = new URL(apiBase)
      if (url.host === apiHost.host) {
        const mediaPath = url.pathname.startsWith('/media/') ? url.pathname.replace(/^\/media\//, '') : url.pathname.replace(/^\//, '')
        return `${apiBase}/api/media/stream/${encodeURI(mediaPath)}`
      }
      return documentFile
    } catch {
      return documentFile
    }
  }

  // Relative path -> stream endpoint để browser có content-type đúng
  const safePath = documentFile.replace(/^\/+/, '')
  return `${apiBase}/api/media/stream/${encodeURI(safePath)}`
}

function getDocViewerUrl(url?: string, type?: 'pdf' | 'doc'): string {
  if (!url) return ''
  const lower = url.toLowerCase()
  const isPdf = type === 'pdf' || lower.endsWith('.pdf')
  const isDoc = type === 'doc' || lower.endsWith('.doc') || lower.endsWith('.docx')
  // PDF: trả về URL trực tiếp (object/pdf sẽ render)
  if (isPdf) return url
  // Word: dùng Office viewer nếu có thể
  if (isDoc) {
    const encoded = encodeURIComponent(url)
    return `https://view.officeapps.live.com/op/embed.aspx?src=${encoded}`
  }
  // Fallback: dùng Google viewer
  const encoded = encodeURIComponent(url)
  return `https://docs.google.com/gview?url=${encoded}&embedded=true`
}

function resolveDocumentUrl(raw?: string): string {
  if (!raw) return ''
  // Data URL thì trả thẳng
  if (raw.startsWith('data:')) return raw
  // URL tuyệt đối
  if (raw.startsWith('http://') || raw.startsWith('https://')) {
    // Nếu cùng host, dùng stream để đảm bảo header
    return getDocumentStreamUrl(raw)
  }
  // Relative -> ưu tiên stream để browser nhận đúng content-type, fallback /media
  return getDocumentStreamUrl(raw)
}

function formatDuration(min?: number){
  if (!min || min <= 0) return '—'
  const total = Math.round(min * 60)
  const mm = Math.floor(total / 60).toString().padStart(2,'0')
  const ss = (total % 60).toString().padStart(2,'0')
  return `${mm}:${ss}`
}

function lessonState(lesson: UiLesson): LessonState {
  const idStr = String(lesson.id)
  if (lesson.done) return 'done'
  if (String(currentLesson.value?.id || '') === idStr) return 'current'
  if (nextLesson.value && String(nextLesson.value.id) === idStr) return 'next'
  return lesson.kind || 'unknown'
}

function lessonStateLabel(state: LessonState): string {
  return lessonStateLabels[state] || lessonStateLabels.unknown
}

function lessonStateClass(state: LessonState): string {
  return lessonStateColors[state] || lessonStateColors.unknown
}

function lessonKind(lesson: UiLesson): LessonKind {
  const idStr = String(lesson.id)
  if (String(currentLesson.value?.id || '') === idStr) {
    return currentLessonKind.value || lesson.kind || 'unknown'
  }
  return lesson.kind || 'unknown'
}

function lessonKindLabel(kind: LessonKind): string {
  return lessonKindLabels[kind] || lessonKindLabels.unknown
}

function goBack() {
  const courseId = normalizeRouteParam(route.params.id)
  // Navigate về course detail để trigger reload
  if (courseId) {
    router.push({ name: 'student-course-detail', params: { id: String(courseId) } }).catch(() => {
      window.history.length > 1 ? window.history.back() : router.push('/student/courses')
    })
    return
  }
  router.push('/student/courses').catch(() => {
    // Fallback nếu route không tồn tại
    window.history.length > 1 ? window.history.back() : router.push('/student/courses')
  })
}

async function loadLessonDetail(lessonId: string | number | null) {
  const cid = courseId.value
  if (!cid) return
  
  // Reset video tracking state khi chuyển lesson
  videoWatchedPercentage.value = 0
  hasMarkedAsWatched.value = false
  
  // Clear YouTube progress interval nếu có
  if (youtubeProgressInterval) {
    clearInterval(youtubeProgressInterval)
    youtubeProgressInterval = null
  }
  
  try {
    const endpoint = lessonId
      ? `/student/courses/${cid}/player/${lessonId}/`
      : `/student/courses/${cid}/player/`
    const { data } = await api.get(endpoint)
    currentLessonDetail.value = data
    lessonProgress.value = data.progress || null
    
    // Nếu đã được đánh dấu là watched từ backend và đã ghi nhận hôm nay, giữ nguyên flag.
    // Ngược lại, cho phép cập nhật lại để log hoạt động hôm nay (phục vụ streak/daily goal).
    const progressTouchedToday = hasProgressToday(lessonProgress.value)
    hasMarkedAsWatched.value = !!lessonProgress.value?.video_watched && progressTouchedToday
    
    const activeLessonId = String(data.id || lessonId || '')
    
    // Load exercises (filter đúng bài học hiện tại)
    try {
      const { data: exercisesData } = await api.get('/activities/exercises/', {
        params: { lesson_id: activeLessonId, published: true }
      })
      currentLessonExercises.value = Array.isArray(exercisesData) ? exercisesData : exercisesData.results || []
    } catch (e) {
      currentLessonExercises.value = []
    }
    
    // Check unlock
    try {
      const unlockCheck = await contentService.checkLessonUnlock(activeLessonId)
      lessonLocked.value = !unlockCheck.can_unlock
      unlockReason.value = unlockCheck.reason || ''
    } catch {
      lessonLocked.value = false
    }
  } catch (e) {
    console.error('Error loading lesson detail:', e)
    currentLessonDetail.value = null
    currentLessonExercises.value = []
    lessonProgress.value = null
    lessonLocked.value = false
  }
}

async function autoCompleteNonVideo() {
  const lessonId = currentLesson.value?.id
  const kind = currentLessonKind.value
  if (!lessonId || lessonLocked.value || !kind || kind === 'video') {
    return
  }
  const key = String(lessonId)
  const progressTouchedToday = hasProgressToday(lessonProgress.value)
  if (progressTouchedToday) {
    // Đã ghi nhận hoạt động hôm nay cho bài này, không cần gọi API thêm
    hasMarkedAsWatched.value = !!lessonProgress.value?.video_watched
    autoCompletedLessons.add(key)
    return
  }
  if (autoCompletedLessons.has(key)) {
    return
  }
  autoCompletedLessons.add(key)
  try {
    const completedFlag = currentLessonExercises.value.length === 0
    await contentService.updateLessonProgress(key, { video_watched: true, completed: completedFlag })
    if (lessonProgress.value) {
      lessonProgress.value.video_watched = true
      lessonProgress.value.completed = completedFlag
      lessonProgress.value.last_accessed_at = new Date().toISOString()
    }
    hasMarkedAsWatched.value = true
    if (completedFlag) {
      markDone(key)
    }
  } catch (error) {
    autoCompletedLessons.delete(key)
    console.error('Failed to auto-complete non-video lesson:', error)
  }
}

async function goToLesson(si: number, li: number){
  cur.value = { si, li }
  openIndex.value = si
  const id = uiSections.value[si]?.items[li]?.id
  if (id != null) {
    await loadLessonDetail(id)
    router.replace({ params: { ...route.params, lessonId: String(id) } })
    videoRef.value?.play?.()
  }
}

async function goPrev(){
  if (!prevLesson.value) return
  const found = findById(prevLesson.value.id)
  if (found) await goToLesson(found.si, found.li)
}

async function goNext(){
  if (!nextLesson.value) return
  // Check if current lesson requires exercise completion
  const mustFinishExercise = (currentLessonExercises.value.length > 0) || currentLessonDetail.value?.requires_exercise_completion
  if (mustFinishExercise && !lessonProgress.value?.exercise_completed) {
    alert('Bạn cần hoàn thành bài tập trước khi tiếp tục!')
    return
  }
  // Đảm bảo đánh dấu hoàn thành bài hiện tại trước khi sang bài tiếp theo
  if (
    currentLesson.value?.id &&
    currentLessonKind.value === 'video' &&
    !lessonProgress.value?.completed
  ) {
    try {
      await contentService.updateLessonProgress(currentLesson.value.id, {
        video_watched: true,
        completed: true,
      })
      if (lessonProgress.value) {
        lessonProgress.value.video_watched = true
        lessonProgress.value.completed = true
      }
      markDone(currentLesson.value.id)
    } catch (e) {
      console.error('Không thể đánh dấu hoàn thành trước khi chuyển bài:', e)
    }
  }
  const found = findById(nextLesson.value.id)
  if (found) await goToLesson(found.si, found.li)
}

function onVideoTimeUpdate() {
  if (!videoRef.value || !currentLesson.value?.id) return
  
  const video = videoRef.value
  if (video.duration > 0) {
    const percentage = (video.currentTime / video.duration) * 100
    videoWatchedPercentage.value = percentage
    checkAndMarkVideoWatched(percentage)
  }
}

async function checkAndMarkVideoWatched(percentage: number) {
  // Chỉ đánh dấu một lần khi đạt 75%
  if (hasMarkedAsWatched.value || percentage < WATCHED_THRESHOLD) {
    return
  }
  
  if (!currentLesson.value?.id) return
  
  hasMarkedAsWatched.value = true
  try {
    const completedFlag = currentLessonExercises.value.length === 0 || lessonProgress.value?.exercise_completed
    await contentService.updateLessonProgress(currentLesson.value.id, {
      video_watched: true,
      completed: completedFlag,
    })
    if (lessonProgress.value) {
      lessonProgress.value.video_watched = true
      lessonProgress.value.completed = completedFlag
      lessonProgress.value.last_accessed_at = new Date().toISOString()
    }
    if (completedFlag) {
      markDone(currentLesson.value.id)
    }
    console.log(`Video marked as watched at ${percentage.toFixed(1)}%`)
  } catch (e) {
    console.error('Error updating video watched:', e)
    hasMarkedAsWatched.value = false // Reset để thử lại
  }
}

async function onVideoWatched() {
  // Deprecated: Giữ lại để tương thích nhưng không dùng nữa
  // Logic mới dùng checkAndMarkVideoWatched thay thế
  if (!currentLesson.value?.id) return
  const percentage = videoWatchedPercentage.value
  await checkAndMarkVideoWatched(percentage)
}

async function onVideoEnded() {
  if (!currentLesson.value?.id) return
  
  const lessonId = String(currentLesson.value.id)
  console.log('Video ended for lesson:', lessonId)
  
  // Clear YouTube progress interval
  if (youtubeProgressInterval) {
    clearInterval(youtubeProgressInterval)
    youtubeProgressInterval = null
  }
  
  // Đảm bảo video được đánh dấu là đã xem (nếu chưa đạt 75% thì đánh dấu luôn khi kết thúc)
  if (!hasMarkedAsWatched.value) {
    await checkAndMarkVideoWatched(100) // 100% khi video kết thúc
  }
  
  // Cập nhật progress: video completed
  try {
    const completedFlag = currentLessonExercises.value.length === 0 || lessonProgress.value?.exercise_completed
    const progressResponse = await contentService.updateLessonProgress(lessonId, { 
      video_watched: true,
      completed: completedFlag
    })
    console.log('Progress updated:', progressResponse)
    
    if (lessonProgress.value) {
      lessonProgress.value.video_watched = true
      lessonProgress.value.completed = completedFlag
      lessonProgress.value.last_accessed_at = new Date().toISOString()
    }
    
    // Đánh dấu lesson đã hoàn thành trong local state NGAY LẬP TỨC (nếu đủ điều kiện)
    if (completedFlag) {
      markDone(lessonId)
    }
    console.log('Lesson marked as done in local state. Current progress:', doneCount.value, '/', totalCount.value)
    
    // Reload course data để lấy progress mới từ backend và sync
    const courseId = normalizeRouteParam(route.params.id) as any
    const { data } = await api.get(`/student/courses/${courseId}/`, {
      params: { _t: Date.now() } // Cache busting
    })
    
    if (data && data.sections) {
      course.value = data
      
      // CLEAR doneSet trước khi repopulate để tránh duplicate
      doneSet.clear()
      doneSetTrigger.value++ // Force reactivity
      
      // Repopulate doneSet từ backend data
      let totalLessonsFromBackend = 0
      data.sections.forEach((section: any) => {
        if (section.lessons && Array.isArray(section.lessons)) {
          totalLessonsFromBackend += section.lessons.length
          section.lessons.forEach((lesson: any) => {
            const requiresExercise = lesson.requires_exercise_completion || lesson.content_type === 'exercise' || lesson.exerciseExists
            const hasExerciseCompleted = lesson.exerciseCompleted || lesson.exercise_completed
            // Only count as completed when exercise condition is satisfied
            const isCompleted = lesson.completed === true || 
                               lesson.completed === 'true' || 
                               lesson.completed === 1 ||
                               lesson.completed === '1' ||
                               (lesson.videoWatched === true || lesson.videoWatched === 'true') && (!requiresExercise || hasExerciseCompleted) ||
                               (requiresExercise && hasExerciseCompleted)
            
            if (isCompleted) {
              doneSet.add(String(lesson.id))
              console.log('Added lesson to doneSet:', lesson.id, lesson.title, 'completed:', lesson.completed, 'videoWatched:', lesson.videoWatched)
            }
          })
        }
      })
      
      // Force reactivity sau khi repopulate
      doneSetTrigger.value++
      
      console.log('After reload - doneSet size:', doneSet.size, 'total lessons from backend:', totalLessonsFromBackend, 'UI totalCount:', totalCount.value)
      
      // Force UI update với nextTick
      await nextTick()
      
      // Rebuild UI với progress mới - QUAN TRỌNG: phải rebuild để totalCount được tính lại
      rebuildAndKeepCursor(lessonId)
      
      // Force reactivity update - đợi UI rebuild xong
      await nextTick()
      doneSetTrigger.value++ // Force reactivity one more time
      
      // Log final state
      const finalDone = doneCount.value
      const finalTotal = totalCount.value
      const finalPct = progressPct.value
      console.log('Final progress after rebuild:', finalDone, '/', finalTotal, '=', finalPct + '%')
      
      // Nếu vẫn 0%, log warning
      if (finalTotal > 0 && finalDone === 0) {
        console.warn('⚠️ Progress is 0% but should be updated! doneSet:', Array.from(doneSet), 'sections:', data.sections)
      }
    }
  } catch (e) {
    console.error('Error updating lesson progress:', e)
    // Vẫn mark done trong local state nếu API fail
    markDone(lessonId)
  }
  
  // Final log
  await nextTick()
  console.log('Video ended - Final progress:', doneCount.value, '/', totalCount.value, '=', progressPct.value + '%')
}

// Q&A
const qaOpen = ref(false)
const qaLoading = ref(false)
const qaItems = ref<any[]>([])
const questionText = ref('')
const sendingQuestion = ref(false)
const canSendQuestion = computed(() => !!questionText.value.trim() && !!qaLessonId.value)
const replyDrafts = reactive<Record<string, string>>({})
const replying = reactive<Record<string, boolean>>({})
const reacting = reactive<Record<string, boolean>>({})
const replyBox = reactive<Record<string, boolean>>({})
const editingQuestion = reactive<{ id: string | null; draft: string }>({ id: null, draft: '' })
const editingReply = reactive<{ id: string | null; draft: string }>({ id: null, draft: '' })
const reporting = reactive<{ open: boolean; questionId?: string; replyId?: string; reason: string; detail: string }>({ open: false, reason: '', detail: '' })
const questionMenu = reactive<Record<string, boolean>>({})
const replyMenu = reactive<Record<string, boolean>>({})
const avatarErrors = reactive<Record<string, boolean>>({})
const askingAI = reactive<Record<string, boolean>>({})
const aiChatBox = reactive<Record<string, boolean>>({})
const aiChatDrafts = reactive<Record<string, string>>({})

// AI Video Question - Hỏi AI về đoạn video đang xem
const aiVideoModalOpen = ref(false)
const aiVideoQuestion = ref('')
const aiVideoAsking = ref(false)
const aiVideoResponse = ref('')
const aiVideoTimestamp = ref(0)
const aiVideoConversation = ref<Array<{ role: 'user' | 'ai'; content: string; timestamp?: string }>>([])

function getCurrentVideoTimestamp(): number {
  // Lấy timestamp từ video HTML5
  if (videoRef.value && videoRef.value.currentTime) {
    return Math.floor(videoRef.value.currentTime)
  }
  // Lấy timestamp từ YouTube player
  if (youtubePlayer.value && youtubePlayer.value.getCurrentTime) {
    try {
      return Math.floor(youtubePlayer.value.getCurrentTime())
    } catch {
      return 0
    }
  }
  return 0
}

function formatTimestamp(seconds: number): string {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

function openAIVideoModal() {
  aiVideoTimestamp.value = getCurrentVideoTimestamp()
  aiVideoModalOpen.value = true
  aiVideoQuestion.value = ''
  aiVideoResponse.value = ''
}

function closeAIVideoModal() {
  aiVideoModalOpen.value = false
}

async function submitAIVideoQuestion() {
  if (!aiVideoQuestion.value.trim() || aiVideoAsking.value) return
  
  const question = aiVideoQuestion.value.trim()
  const timestamp = aiVideoTimestamp.value
  const timestampStr = formatTimestamp(timestamp)
  
  // Thêm câu hỏi vào conversation
  aiVideoConversation.value.push({
    role: 'user',
    content: question,
    timestamp: timestampStr
  })
  
  aiVideoAsking.value = true
  aiVideoQuestion.value = ''
  
  try {
    const { data } = await api.post('/student/ai/tutor/video-question/', {
      lesson_id: currentLesson.value?.id,
      question: question,
      timestamp: timestamp,
      video_title: currentLesson.value?.title || course.value?.title || ''
    }, { timeout: 60000 })
    
    if (data.success && data.message) {
      aiVideoResponse.value = data.message
      aiVideoConversation.value.push({
        role: 'ai',
        content: data.message,
        timestamp: timestampStr
      })
    } else {
      aiVideoResponse.value = 'AI không thể trả lời câu hỏi này. Hãy thử lại nhé! 🌟'
      aiVideoConversation.value.push({
        role: 'ai',
        content: aiVideoResponse.value
      })
    }
  } catch (e: any) {
    console.error('AI Video Question error:', e)
    aiVideoResponse.value = 'Có lỗi xảy ra. Hãy thử lại sau nhé! 🌟'
    aiVideoConversation.value.push({
      role: 'ai',
      content: aiVideoResponse.value
    })
  } finally {
    aiVideoAsking.value = false
  }
}

function clearAIVideoConversation() {
  aiVideoConversation.value = []
  aiVideoResponse.value = ''
}

function normalizeAvatar(input: any) {
  if (!input) return ''
  const str = String(input).trim()
  if (!str) return ''
  const lower = str.toLowerCase()
  if (lower === 'avatar' || lower === 'null' || lower === 'undefined' || lower === 'none') return ''
  return str
}
function avatarUrlForQuestion(q: any) {
  const source =
    (q?.is_owner ? auth.user?.avatar : null) ||
    normalizeAvatar(q?.avatar) ||
    normalizeAvatar(q?.avatar_url) ||
    normalizeAvatar(q?.student_avatar)
  return getAvatarSrc(source, (q?.gender as any) || 'male', q?.is_teacher ? 'instructor' : 'student')
}
function avatarUrlForReply(rep: any) {
  const source =
    (rep?.is_owner ? auth.user?.avatar : null) ||
    normalizeAvatar(rep?.avatar) ||
    normalizeAvatar(rep?.avatar_url) ||
    normalizeAvatar(rep?.student_avatar)
  return getAvatarSrc(source, (rep?.gender as any) || 'male', rep?.is_teacher ? 'instructor' : 'student')
}

async function submitQuestion() {
  if (!canSendQuestion.value || sendingQuestion.value) return
  sendingQuestion.value = true
  try {
    const lessonId = qaLessonId.value
    if (!lessonId) {
      showToast('Không xác định được bài học để gửi hỏi đáp', 'error')
      return
    }
    await api.post('/student/lesson-questions/', {
      lesson_id: lessonId,
      content: questionText.value.trim(),
    })
    showToast('Đã gửi câu hỏi tới giáo viên!', 'success')
    questionText.value = ''
    await loadQuestions()
  } catch (e: any) {
    console.error('Send question error:', e)
    const msg = e?.response?.data?.detail || e?.message || 'Gửi câu hỏi thất bại'
    showToast(msg, 'error')
  } finally {
    sendingQuestion.value = false
  }
}

function formatDateTimeShort(iso?: string) {
  if (!iso) return ''
  try {
    const d = new Date(iso)
    return d.toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit' }) + ' ' + d.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
  } catch {
    return iso
  }
}

function getInitials(name?: string | null): string {
  if (!name || !name.trim()) return ''
  // Lấy chữ cái đầu tiên của từ đầu tiên và từ cuối cùng (nếu có)
  const parts = name.trim().split(/\s+/)
  if (parts.length === 1) {
    // Chỉ có một từ, lấy 2 ký tự đầu
    return name.slice(0, 2).toUpperCase()
  }
  // Có nhiều từ, lấy chữ cái đầu của từ đầu và từ cuối
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
}

function handleAvatarError(key: string) {
  // Khi avatar load lỗi, đánh dấu để hiển thị fallback
  avatarErrors[key] = true
  console.log(`Avatar load error for ${key}, showing fallback`)
}

function handleAvatarLoad(key: string) {
  // Khi avatar load thành công, đảm bảo không có error flag
  if (avatarErrors[key]) {
    delete avatarErrors[key]
  }
}

async function loadQuestions() {
  const lessonId = qaLessonId.value
  if (!lessonId) {
    showToast('Không xác định được bài học để tải hỏi đáp', 'error')
    return
  }
  qaLoading.value = true
  try {
    const { data } = await api.get('/student/lesson-questions/', {
      params: { lesson_id: lessonId },
    })
    const userId = auth.user?.id ? String(auth.user.id) : null
    const items = (data?.items || []).map((q: any) => {
      const isOwner = q.is_owner || (userId && String(q.student_id || q.studentId) === userId)
      const avatar = isOwner ? (auth.user?.avatar || q.avatar || q.avatar_url || q.student_avatar) : (q.avatar || q.avatar_url || q.student_avatar)
      const gender = isOwner ? (auth.user?.gender || q.gender) : q.gender
      const replies = (q.replies || []).map((rep: any) => {
        const repOwner = rep.is_owner || (userId && String(rep.student_id || rep.user_id || rep.userId) === userId)
        return {
          ...rep,
          is_owner: repOwner,
          avatar: repOwner ? (auth.user?.avatar || rep.avatar || rep.avatar_url || rep.student_avatar) : (rep.avatar || rep.avatar_url || rep.student_avatar),
          gender: repOwner ? (auth.user?.gender || rep.gender) : rep.gender,
          reactions_count: rep.reactions_count || 0,
          reacted: rep.reacted || false,
        }
      })
      return {
        ...q,
        is_owner: isOwner,
        avatar,
        gender,
        reactions_count: q.reactions_count || 0,
        reacted: q.reacted || false,
        replies,
      }
    })
    qaItems.value = items
  } catch (e) {
    console.error('Load questions error:', e)
    showToast('Không tải được hỏi đáp', 'error')
  } finally {
    qaLoading.value = false
  }
}

function toggleQA(open: boolean) {
  qaOpen.value = open
  if (open) {
    loadQuestions()
  }
}

function startReply(questionId: string) {
  replying[questionId] = true
  if (!replyDrafts[questionId]) replyDrafts[questionId] = ''
}

async function submitReply(questionId: string) {
  const content = (replyDrafts[questionId] || '').trim()
  if (!content) return
  replying[questionId] = true
  try {
    await api.post(`/student/lesson-questions/${questionId}/reply/`, { content })
    replyDrafts[questionId] = ''
    await loadQuestions()
  } catch (e: any) {
    console.error('Send reply error:', e)
    const msg = e?.response?.data?.detail || e?.message || 'Gửi phản hồi thất bại'
    showToast(msg, 'error')
  } finally {
    replying[questionId] = false
  }
}

async function toggleReaction(replyId: string) {
  if (reacting[replyId]) return
  reacting[replyId] = true
  try {
    const { data } = await api.post(`/student/lesson-question-replies/${replyId}/react/`)
    const reacted = data?.reacted ?? false
    const reactionsCount = data?.reactions_count ?? 0
    
    // Update optimistic state
    qaItems.value.forEach((q: any) => {
      (q.replies || []).forEach((rep: any) => {
        if (rep.id === replyId) {
          rep.reacted = reacted
          rep.reactions_count = reactionsCount
        }
      })
    })
  } catch (e) {
    console.error('Reaction error:', e)
    showToast('Không thực hiện được thao tác', 'error')
    // Reload to sync state
    await loadQuestions()
  } finally {
    reacting[replyId] = false
  }
}

function toggleReplyBox(questionId: string) {
  replyBox[questionId] = !replyBox[questionId]
  if (replyBox[questionId] && !replyDrafts[questionId]) {
    replyDrafts[questionId] = ''
  }
}

async function toggleReactionOnQuestion(questionId: string) {
  const key = `q-${questionId}`
  if (reacting[key]) return
  reacting[key] = true
  try {
    const { data } = await api.post(`/student/lesson-questions/${questionId}/react/`)
    const reacted = data?.reacted ?? false
    const reactionsCount = data?.reactions_count ?? 0
    
    // Update optimistic state
    const target = qaItems.value.find((q: any) => q.id === questionId)
    if (target) {
      target.reacted = reacted
      target.reactions_count = reactionsCount
    }
  } catch (e: any) {
    console.error('Question reaction error:', e)
    showToast('Không thực hiện được thao tác', 'error')
    // Reload to sync state
    await loadQuestions()
  } finally {
    reacting[key] = false
  }
}

function startEditQuestion(q: any) {
  editingQuestion.id = q.id
  editingQuestion.draft = q.content
}
function cancelEditQuestion() {
  editingQuestion.id = null
  editingQuestion.draft = ''
}
async function saveEditQuestion(id: string) {
  if (!editingQuestion.draft.trim()) return
  try {
    await api.patch(`/student/lesson-questions/${id}/`, { content: editingQuestion.draft })
    cancelEditQuestion()
    await loadQuestions()
    showToast('Đã cập nhật bình luận', 'success')
  } catch (e: any) {
    showToast(e?.response?.data?.detail || 'Không sửa được', 'error')
  }
}
async function deleteQuestion(id: string) {
  try {
    await api.delete(`/student/lesson-questions/${id}/`)
    await loadQuestions()
    showToast('Đã xóa bình luận', 'success')
  } catch (e: any) {
    showToast(e?.response?.data?.detail || 'Không xóa được', 'error')
  }
}

async function askAI(questionId: string) {
  if (askingAI[questionId]) return
  askingAI[questionId] = true
  try {
    // Tăng timeout vì AI có thể mất thời gian để phản hồi
    const { data } = await api.post(`/student/lesson-questions/${questionId}/ai-answer/`, {}, { timeout: 60000 })
    showToast('AI đã trả lời câu hỏi của bạn!', 'success')
    await loadQuestions()
  } catch (e: any) {
    console.error('AI answer error:', e)
    let msg = 'AI không thể trả lời lúc này'
    if (e?.code === 'ECONNABORTED' || e?.message?.includes('timeout')) {
      msg = 'AI đang xử lý quá lâu, vui lòng thử lại sau'
    } else if (e?.response?.data?.detail) {
      msg = e.response.data.detail
    } else if (e?.message) {
      msg = e.message
    }
    showToast(msg, 'error')
  } finally {
    askingAI[questionId] = false
  }
}

function toggleAIChatBox(questionId: string, replyId: string) {
  const key = `${questionId}-${replyId}`
  aiChatBox[key] = !aiChatBox[key]
  if (aiChatBox[key] && !aiChatDrafts[key]) {
    aiChatDrafts[key] = ''
  }
}

async function continueAIChat(questionId: string, replyId: string) {
  const key = `${questionId}-${replyId}`
  const content = (aiChatDrafts[key] || '').trim()
  if (!content || askingAI[questionId]) return
  
  askingAI[questionId] = true
  try {
    // Gửi câu hỏi mới như một reply, sau đó gọi AI trả lời
    await api.post(`/student/lesson-questions/${questionId}/reply/`, { content })
    
    // Gọi AI trả lời câu hỏi mới
    await api.post(`/student/lesson-questions/${questionId}/ai-answer/`, {}, { timeout: 60000 })
    
    aiChatDrafts[key] = ''
    aiChatBox[key] = false
    showToast('AI đã trả lời!', 'success')
    await loadQuestions()
  } catch (e: any) {
    console.error('Continue AI chat error:', e)
    let msg = 'AI không thể trả lời lúc này'
    if (e?.response?.data?.detail) {
      msg = e.response.data.detail
    } else if (e?.message) {
      msg = e.message
    }
    showToast(msg, 'error')
  } finally {
    askingAI[questionId] = false
  }
}

function startEditReply(rep: any) {
  editingReply.id = rep.id
  editingReply.draft = rep.content
}
function cancelEditReply() {
  editingReply.id = null
  editingReply.draft = ''
}
function toggleQuestionMenu(id: string) {
  questionMenu[id] = !questionMenu[id]
}
function toggleReplyMenu(id: string) {
  replyMenu[id] = !replyMenu[id]
}
async function saveEditReply(id: string, questionId: string) {
  if (!editingReply.draft.trim()) return
  try {
    await api.patch(`/student/lesson-question-replies/${id}/`, { content: editingReply.draft })
    cancelEditReply()
    await loadQuestions()
    showToast('Đã cập nhật phản hồi', 'success')
  } catch (e: any) {
    showToast(e?.response?.data?.detail || 'Không sửa được', 'error')
  }
}
async function deleteReply(id: string, questionId: string) {
  try {
    await api.delete(`/student/lesson-question-replies/${id}/`)
    await loadQuestions()
    showToast('Đã xóa phản hồi', 'success')
  } catch (e: any) {
    showToast(e?.response?.data?.detail || 'Không xóa được', 'error')
  }
}

function openReport(questionId?: string | null, replyId?: string | null) {
  reporting.open = true
  reporting.questionId = questionId || undefined
  reporting.replyId = replyId || undefined
  reporting.reason = ''
  reporting.detail = ''
}

async function submitReport() {
  if (!reporting.questionId && !reporting.replyId) return
  try {
    await api.post('/student/lesson-question-report/', {
      question_id: reporting.questionId,
      reply_id: reporting.replyId,
      reason: reporting.reason || 'Báo cáo vi phạm',
      detail: reporting.detail || '',
    })
    showToast('Đã gửi báo cáo tới admin', 'success')
    reporting.open = false
  } catch (e: any) {
    showToast(e?.response?.data?.detail || 'Không gửi được báo cáo', 'error')
  }
}

async function openExercise(exerciseId: string | number) {
  if (lessonProgress.value?.exercise_completed) {
    showToast('Bạn đã nộp bài tập này', 'info')
    return
  }
  exercisePlayer.loading = true
  exercisePlayer.open = true
  exercisePlayer.exercise = currentLessonExercises.value.find((ex) => String(ex.id) === String(exerciseId)) || null
  exercisePlayer.result = null
  exercisePlayer.submitted = false
  exercisePlayer.answers = {}
  try {
    const { data } = await api.post(`/activities/exercises/${exerciseId}/start/`)
    exercisePlayer.attemptId = data.id || data.attempt_id
    // Questions kèm meta
    const qs = data.questions || []
    exercisePlayer.questions = qs.map((q: any) => ({
      ...q,
      type: q.meta?.type || q.type || 'mcq',
      choices: q.choices || [],
      meta: q.meta || {},
      pairs: q.pairs || []
    }))
    // Prefill answers nếu có
    const existingAnswers = data.answers || {}
    exercisePlayer.answers = { ...existingAnswers }
    if (data.finished_at || data.status === 'finished') {
      exercisePlayer.result = { score: data.score }
      exercisePlayer.submitted = true
    }
  } catch (e: any) {
    showToast(e?.response?.data?.detail || 'Không thể bắt đầu bài tập', 'error')
    exercisePlayer.open = false
  } finally {
    exercisePlayer.loading = false
  }
}

function handleAnswerChange(q: any, payload: any) {
  exercisePlayer.answers = { ...exercisePlayer.answers, [q.id]: payload }
}

function buildMatchingOptions(q: any) {
  const pairs = q.meta?.pairs || q.pairs || []
  const correctPairs = q.meta?.correct_pairs || {}

  // Build left/right ids: prefer existing ids from correct_pairs
  let lefts: string[] = Object.keys(correctPairs)
  if (lefts.length === 0 && pairs.length > 0) {
    lefts = pairs.map((pair: any, idx: number) => `L${idx + 1}`)
  }

  return lefts.map((leftId: string, idx: number) => ({
    leftId,
    leftText: pairs[idx]?.left || leftId,
    rights: pairs.map((p: any, i: number) => ({
      rightId: `R${i + 1}`,
      rightText: p.right || `R${i + 1}`
    }))
  }))
}

async function submitExercise() {
  if (!exercisePlayer.attemptId) return
  exercisePlayer.submitting = true
  try {
    // Gửi từng câu trả lời
    for (const q of exercisePlayer.questions) {
      const ans = exercisePlayer.answers[q.id]
      let payload: any = null
      if (q.type === 'mcq') {
        const multiple = !!q.meta?.multiple
        if (multiple) {
          payload = { selected_choice_ids: Array.isArray(ans) ? ans : ans ? [ans] : [] }
        } else {
          payload = { selected_choice_id: ans }
        }
      } else if (q.type === 'short_answer') {
        payload = { text: ans || '' }
      } else if (q.type === 'matching') {
        // ans dạng { [leftId]: rightId } hoặc array
        let pairs: any[] = []
        if (ans && typeof ans === 'object' && !Array.isArray(ans)) {
          pairs = Object.entries(ans).map(([left_id, right_id]) => ({ left_id, right_id }))
        } else if (Array.isArray(ans)) {
          pairs = ans
        }
        payload = { pairs }
      } else {
        payload = ans
      }
      await api.post(`/activities/attempts/${exercisePlayer.attemptId}/answers/`, {
        question_id: q.id,
        answer: payload
      })
    }
    // Chốt bài
    const { data: summary } = await api.post(`/activities/attempts/${exercisePlayer.attemptId}/finalize/`)
    exercisePlayer.result = summary
    exercisePlayer.submitted = true
    showToast('Đã nộp bài tập', 'success')
    // Cập nhật progress bài học
    if (currentLessonDetail.value?.id) {
      await contentService.updateLessonProgress(currentLessonDetail.value.id, {
        exercise_completed: true,
        exercise_score: summary.score ?? 0,
        completed: true
      })
      if (lessonProgress.value) {
        lessonProgress.value.exercise_completed = true
        lessonProgress.value.exercise_score = summary.score ?? 0
        lessonProgress.value.completed = true
      }
      markDone(currentLessonDetail.value.id)
    }
  } catch (e: any) {
    showToast(e?.response?.data?.detail || 'Không thể nộp bài tập', 'error')
  } finally {
    exercisePlayer.submitting = false
  }
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
  const idStr = String(id)
  if (!doneSet.has(idStr)) {
    doneSet.add(idStr)
    // Force reactivity trigger
    doneSetTrigger.value++
    console.log('markDone: Added lesson', idStr, 'to doneSet. New size:', doneSet.size, 'total:', totalCount.value)
    // Rebuild UI để cập nhật trạng thái 'done' cho các bài học
    nextTick(() => {
      rebuildAndKeepCursor(idStr)
      // Force reactivity update
      doneSetTrigger.value++
      console.log('UI rebuilt after markDone. Progress:', doneCount.value, '/', totalCount.value, '=', progressPct.value + '%')
      
      // 🎉 Kiểm tra hoàn thành 100% và hiển thị celebration
      if (progressPct.value >= 100 && !hasShownCelebration.value) {
        hasShownCelebration.value = true
        setTimeout(() => {
          showCelebration.value = true
        }, 500) // Delay nhẹ để animation mượt hơn
      }
    })
  } else {
    console.log('markDone: Lesson', idStr, 'already in doneSet')
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

watch(
  () => [currentLesson.value?.id, currentLessonKind.value, lessonLocked.value],
  () => {
    autoCompleteNonVideo()
  },
  { immediate: true }
)

// Watch for lesson changes
watch(() => currentLesson.value?.id, async (newId) => {
  if (newId) {
    await loadLessonDetail(newId)
    if (qaOpen.value) {
      await loadQuestions()
    }
  }
}, { immediate: true })

// Watch route params for lessonId changes
watch(() => route.params.lessonId, async (newLessonId) => {
  const normalized = normalizeRouteParam(newLessonId)
  if (normalized) {
    await loadLessonDetail(normalized)
  }
})

onMounted(async () => {
  await load()
  const lessonParam = normalizeRouteParam(route.params.lessonId)
  if (lessonParam) {
    await loadLessonDetail(lessonParam)
  }
})

// Cleanup khi component unmount
onBeforeUnmount(() => {
  // Clear YouTube progress interval
  if (youtubeProgressInterval) {
    clearInterval(youtubeProgressInterval)
    youtubeProgressInterval = null
  }
})
</script>

<style scoped>
/* Fade transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Slide transition for drawer */
.slide-enter-active {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.3s ease;
}
.slide-leave-active {
  transition: transform 0.25s cubic-bezier(0.4, 0, 1, 1), opacity 0.25s ease;
}
.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

/* Slide down transition for reply box */
.slide-down-enter-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.slide-down-leave-active {
  transition: all 0.2s cubic-bezier(0.4, 0, 1, 1);
}
.slide-down-enter-from {
  opacity: 0;
  transform: translateY(-10px);
  max-height: 0;
}
.slide-down-enter-to {
  opacity: 1;
  transform: translateY(0);
  max-height: 500px;
}
.slide-down-leave-from {
  opacity: 1;
  transform: translateY(0);
  max-height: 500px;
}
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-10px);
  max-height: 0;
}

.modal-backdrop {
  background: rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(4px);
}

/* Line clamp utility */
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Smooth scrollbar */
.overflow-y-auto {
  scrollbar-width: thin;
  scrollbar-color: rgb(203 213 225) transparent;
}

.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: rgb(203 213 225);
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background-color: rgb(148 163 184);
}
</style>
