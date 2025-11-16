<!-- src/pages/teacher/courses/ContentLibrary.vue -->
<template>
  <div class="min-h-screen w-full overflow-x-hidden bg-slate-50">
    <main class="mx-auto w-full max-w-screen-2xl px-6 py-8 md:px-10">
      <!-- Header -->
      <div class="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div class="flex items-center gap-3">
          <button
            class="rounded-xl border border-slate-300 px-4 py-2 text-sm font-medium text-gray-700 transition hover:bg-slate-50"
            @click="goBack"
          >
            <span class="flex items-center gap-2">
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
              Quay lại
            </span>
          </button>
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Thư viện nội dung</h1>
            <p class="mt-1 text-sm text-gray-600">
              Chọn nội dung từ thư viện để thêm vào <strong>các chương</strong> của khóa học
            </p>
          </div>
        </div>
        <div class="flex items-center gap-3">
          <div v-if="courseId" class="flex items-center gap-3 rounded-xl border border-cyan-200 bg-cyan-50 px-4 py-2">
            <svg class="h-5 w-5 text-cyan-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
            <div>
              <p class="text-xs font-medium text-cyan-700">Đang thêm vào</p>
              <p class="text-sm font-semibold text-cyan-900">{{ courseTitle || `Khóa học #${courseId}` }}</p>
            </div>
          </div>
          <button
            class="inline-flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-cyan-600 to-cyan-700 px-4 py-2 text-sm font-semibold text-white shadow-lg shadow-cyan-500/30 transition hover:from-cyan-700 hover:to-cyan-800 hover:shadow-xl hover:-translate-y-0.5"
            @click="openCreateModal"
          >
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            {{ courseId ? 'Tạo bài học mới' : 'Tạo nội dung mới' }}
          </button>
        </div>
      </div>

      <!-- Tools -->
      <div class="mb-6 grid grid-cols-1 gap-3 md:grid-cols-3">
        <!-- Search -->
        <div class="md:col-span-2">
          <div class="flex items-center gap-2 rounded-2xl border border-slate-200 bg-white px-4 py-3 shadow-sm">
            <svg viewBox="0 0 24 24" class="h-5 w-5 text-slate-400" fill="none" stroke="currentColor">
              <circle cx="11" cy="11" r="8" stroke-width="2" />
              <path d="M21 21l-4.3-4.3" stroke-width="2" />
            </svg>
            <input
              v-model.trim="q"
              type="text"
              placeholder="Tìm theo tiêu đề, môn học..."
              class="w-full bg-transparent outline-none placeholder:text-slate-400"
              @input="debouncedFetch"
            />
          </div>
        </div>

        <!-- Filters -->
        <div class="grid grid-cols-2 gap-2">
          <select
            v-model="gradeBand"
            class="rounded-2xl border border-slate-200 bg-white px-3 py-2 text-sm font-medium shadow-sm transition hover:border-cyan-300"
            @change="fetchList(1)"
          >
            <option value="">Tất cả khối</option>
            <option value="Khối 1–2">Khối 1–2</option>
            <option value="Khối 3–5">Khối 3–5</option>
          </select>
          <select
            v-model="ctype"
            class="rounded-2xl border border-slate-200 bg-white px-3 py-2 text-sm font-medium shadow-sm transition hover:border-cyan-300"
            @change="fetchList(1)"
          >
            <option value="">Tất cả loại</option>
            <option value="video">Video</option>
            <option value="pdf">PDF</option>
            <option value="doc">Tài liệu</option>
            <option value="quiz">Quiz</option>
          </select>
        </div>
      </div>

      <!-- Stats -->
      <div class="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-4">
        <div class="rounded-xl border border-slate-200 bg-white p-3 shadow-sm">
          <p class="text-xs font-medium text-gray-600">Tổng nội dung</p>
          <p class="mt-1 text-xl font-bold text-gray-900">{{ total }}</p>
        </div>
        <div class="rounded-xl border border-slate-200 bg-white p-3 shadow-sm">
          <p class="text-xs font-medium text-gray-600">Video</p>
          <p class="mt-1 text-xl font-bold text-blue-600">{{ typeCounts.video }}</p>
        </div>
        <div class="rounded-xl border border-slate-200 bg-white p-3 shadow-sm">
          <p class="text-xs font-medium text-gray-600">Tài liệu</p>
          <p class="mt-1 text-xl font-bold text-emerald-600">{{ typeCounts.doc + typeCounts.pdf }}</p>
        </div>
        <div class="rounded-xl border border-slate-200 bg-white p-3 shadow-sm">
          <p class="text-xs font-medium text-gray-600">Quiz</p>
          <p class="mt-1 text-xl font-bold text-amber-600">{{ typeCounts.quiz }}</p>
        </div>
      </div>

      <!-- List (loading) -->
      <div v-if="loading" class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="i in pageSize"
          :key="'skel-' + i"
          class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"
        >
          <div class="mb-3 flex items-center gap-3">
            <div class="h-12 w-12 animate-pulse rounded-xl bg-slate-200"></div>
            <div class="flex-1 space-y-2">
              <div class="h-4 w-3/4 animate-pulse rounded bg-slate-200"></div>
              <div class="h-3 w-1/2 animate-pulse rounded bg-slate-100"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- List -->
      <div v-else-if="items.length" class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <article
          v-for="item in items"
          :key="item.id"
          class="group relative flex flex-col rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition-all hover:shadow-lg hover:-translate-y-1"
        >
          <!-- Type Badge -->
          <div class="mb-3 flex items-center justify-between">
            <div
              class="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl text-sm font-bold shadow-sm transition"
              :class="getTypeClass(item.type)"
            >
              {{ getTypeIcon(item.type) }}
            </div>
            <!-- Action buttons -->
            <div class="flex items-center gap-2">
              <button
                v-if="courseId"
                class="rounded-lg border border-cyan-200 bg-cyan-50 px-3 py-1.5 text-xs font-semibold text-cyan-700 transition hover:bg-cyan-100"
                @click="openAddModal(item)"
              >
                <span class="flex items-center gap-1">
                  <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                  Thêm vào khóa học
                </span>
              </button>
              <div v-else class="flex items-center gap-2">
                <button
                  class="rounded-lg border border-gray-200 bg-white px-2 py-1.5 text-xs font-medium text-gray-700 transition hover:bg-gray-50"
                  @click="openEditModal(item)"
                  title="Sửa"
                >
                  <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>
                <button
                  class="rounded-lg border border-rose-200 bg-rose-50 px-2 py-1.5 text-xs font-medium text-rose-700 transition hover:bg-rose-100"
                  @click="openDeleteModal(item)"
                  title="Xóa"
                >
                  <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Content Info -->
          <div class="flex-1">
            <h3 class="mb-2 line-clamp-2 text-base font-bold text-gray-900 group-hover:text-cyan-600 transition">
              {{ item.title }}
            </h3>
            
            <!-- Tags -->
            <div class="mb-3 flex flex-wrap items-center gap-2">
              <span class="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-medium text-gray-700">
                {{ subjectLabel(item.subject) }}
              </span>
              <span class="rounded-full bg-blue-100 px-2.5 py-1 text-xs font-medium text-blue-700">
                {{ item.gradeBand }}
              </span>
            </div>

            <!-- Meta Info -->
            <div class="space-y-1 text-xs text-gray-500">
              <p class="flex items-center gap-1">
                <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                Cập nhật {{ item.updatedAt }}
              </p>
              <p v-if="item.meta?.duration" class="flex items-center gap-1">
                <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                {{ item.meta.duration }}
              </p>
              <p v-if="item.meta?.size" class="flex items-center gap-1">
                <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
                {{ item.meta.size }}
              </p>
              <p v-if="item.meta?.questions" class="flex items-center gap-1">
                <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                {{ item.meta.questions }} câu hỏi
              </p>
            </div>
          </div>

          <!-- Preview Button -->
          <div class="mt-4 flex items-center gap-2 border-t border-slate-100 pt-4">
            <button
              class="flex-1 rounded-lg border border-slate-200 px-3 py-2 text-xs font-medium text-gray-700 transition hover:bg-slate-50"
              @click="previewContent(item)"
            >
              <span class="flex items-center justify-center gap-1">
                <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                Xem trước
              </span>
            </button>
            <button
              v-if="!courseId"
              class="rounded-lg border border-gray-200 px-3 py-2 text-xs font-medium text-gray-700 transition hover:bg-gray-50"
              @click="openEditModal(item)"
            >
              <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </button>
            <button
              v-if="!courseId"
              class="rounded-lg border border-rose-200 px-3 py-2 text-xs font-medium text-rose-700 transition hover:bg-rose-50"
              @click="openDeleteModal(item)"
            >
              <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </article>
      </div>

      <!-- Empty State -->
      <div v-else class="mt-16 flex flex-col items-center justify-center rounded-3xl border-2 border-dashed border-slate-300 bg-white px-6 py-16 text-center">
        <svg class="h-16 w-16 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
        <h3 class="mt-4 text-lg font-semibold text-gray-900">Không tìm thấy nội dung</h3>
        <p class="mt-2 max-w-sm text-sm text-gray-500">
          Thử thay đổi bộ lọc hoặc từ khóa tìm kiếm để tìm nội dung phù hợp.
        </p>
      </div>

      <!-- Pager -->
      <div v-if="totalPages > 1" class="mt-8 flex flex-wrap items-center justify-center gap-2">
        <button
          class="inline-flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 bg-white text-sm font-bold text-slate-700 transition hover:border-cyan-500 hover:bg-cyan-50 disabled:cursor-not-allowed disabled:opacity-40 disabled:hover:bg-white disabled:hover:border-slate-200"
          :disabled="page <= 1"
          @click="fetchList(page - 1)"
        >
          ‹
        </button>
        <button
          v-for="p in pagesToShow"
          :key="p.key"
          class="inline-flex h-10 min-w-[40px] items-center justify-center rounded-xl border text-sm font-semibold transition"
          :class="p.sep
            ? 'border-transparent bg-transparent text-slate-400'
            : p.num === page
              ? 'border-cyan-500 bg-cyan-600 text-white shadow-lg shadow-cyan-500/40'
              : 'border-slate-200 bg-white text-slate-700 hover:border-cyan-300 hover:bg-cyan-50'"
          :disabled="p.sep"
          @click="!p.sep && fetchList(p.num!)"
        >
          {{ p.text }}
        </button>
        <button
          class="inline-flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 bg-white text-sm font-bold text-slate-700 transition hover:border-cyan-500 hover:bg-cyan-50 disabled:cursor-not-allowed disabled:opacity-40 disabled:hover:bg-white disabled:hover:border-slate-200"
          :disabled="page >= totalPages"
          @click="fetchList(page + 1)"
        >
          ›
        </button>
      </div>
    </main>

    <!-- Add to Course Modal -->
    <div
      v-if="showAddModal && selectedContent && courseId"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
      @click.self="closeAddModal"
    >
      <div class="w-full max-w-lg rounded-2xl bg-white p-6 shadow-xl">
        <div class="mb-4 flex items-center gap-3">
          <div
            class="flex h-12 w-12 items-center justify-center rounded-xl text-lg font-bold"
            :class="getTypeClass(selectedContent.type)"
          >
            {{ getTypeIcon(selectedContent.type) }}
          </div>
          <div class="flex-1">
            <h2 class="text-lg font-bold text-gray-900">Thêm vào khóa học</h2>
            <p class="text-sm text-gray-600">{{ selectedContent.title }}</p>
          </div>
        </div>

        <div class="mb-4 space-y-3">
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">
              Chọn chương để thêm nội dung
            </label>
            <select
              v-model="selectedModuleId"
              class="w-full rounded-lg border border-slate-300 px-4 py-2 focus:border-cyan-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/20"
            >
              <option value="">-- Tạo chương mới --</option>
              <option v-for="module in modules" :key="module.id" :value="module.id">
                {{ module.title }}
              </option>
            </select>
            <p class="mt-1 text-xs text-gray-500">
              Nội dung sẽ được thêm dưới dạng <strong>bài học</strong> vào chương đã chọn
            </p>
          </div>
          <div v-if="selectedModuleId">
            <label class="mb-2 block text-sm font-medium text-gray-700">Vị trí trong chương</label>
            <select
              v-model="lessonPosition"
              class="w-full rounded-lg border border-slate-300 px-4 py-2 focus:border-cyan-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/20"
            >
              <option value="0">Đầu chương</option>
              <option value="-1">Cuối chương</option>
            </select>
          </div>
          <div v-if="!selectedModuleId">
            <label class="mb-2 block text-sm font-medium text-gray-700">Tên chương mới</label>
            <input
              v-model="newModuleTitle"
              type="text"
              class="w-full rounded-lg border border-slate-300 px-4 py-2 focus:border-cyan-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/20"
              placeholder="Ví dụ: Chương 1 - Giới thiệu"
            />
            <p class="mt-1 text-xs text-gray-500">
              Chương mới sẽ được tạo và nội dung sẽ được thêm vào đó
            </p>
          </div>
        </div>

        <div class="flex justify-end gap-3">
          <button
            type="button"
            class="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-gray-700 transition hover:bg-slate-50"
            @click="closeAddModal"
          >
            Hủy
          </button>
          <button
            type="button"
            class="rounded-lg bg-cyan-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-cyan-700"
            :disabled="adding"
            @click="addToCourse"
          >
            {{ adding ? 'Đang thêm...' : 'Thêm vào khóa học' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Create/Edit Content Modal -->
    <div
      v-if="showEditModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4 overflow-y-auto"
      @click.self="closeEditModal"
    >
      <div class="w-full max-w-2xl rounded-2xl bg-white p-6 shadow-xl my-8">
        <h3 class="mb-4 text-lg font-bold">{{ editingContent ? 'Sửa nội dung' : 'Tạo nội dung mới' }}</h3>
        
        <div class="space-y-4">
          <!-- Tên nội dung -->
          <div>
            <label class="mb-2 block text-sm font-semibold text-gray-700">
              Tên nội dung <span class="text-rose-600">*</span>
            </label>
            <input
              v-model.trim="editForm.title"
              type="text"
              class="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
              placeholder="Ví dụ: Bài giảng về số tự nhiên"
            />
          </div>

          <!-- Môn học -->
          <div>
            <label class="mb-2 block text-sm font-semibold text-gray-700">Môn học</label>
            <select
              v-model="editForm.subject"
              class="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
            >
              <option value="math">Toán</option>
              <option value="vietnamese">Tiếng Việt</option>
              <option value="english">Tiếng Anh</option>
              <option value="science">Khoa học</option>
              <option value="history">Lịch sử</option>
            </select>
          </div>

          <!-- Loại nội dung -->
          <div>
            <label class="mb-2 block text-sm font-semibold text-gray-700">Loại nội dung</label>
            <select
              v-model="editForm.type"
              class="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
            >
              <option value="video">Video</option>
              <option value="pdf">PDF</option>
              <option value="doc">Tài liệu</option>
              <option value="quiz">Quiz</option>
            </select>
          </div>

          <!-- Khối lớp -->
          <div>
            <label class="mb-2 block text-sm font-semibold text-gray-700">Khối lớp</label>
            <select
              v-model="editForm.gradeBand"
              class="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
            >
              <option value="Khối 1–2">Khối 1–2</option>
              <option value="Khối 3–5">Khối 3–5</option>
            </select>
          </div>
        </div>

        <div class="mt-6 flex justify-end gap-3">
          <button
            type="button"
            class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-50"
            @click="closeEditModal"
          >
            Hủy
          </button>
          <button
            type="button"
            class="rounded-lg bg-cyan-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-cyan-700 disabled:opacity-50"
            :disabled="saving || !editForm.title.trim()"
            @click="saveContent"
          >
            {{ saving ? 'Đang lưu...' : (editingContent ? 'Cập nhật' : 'Tạo mới') }}
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div
      v-if="showDeleteModal && deletingContent"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
      @click.self="closeDeleteModal"
    >
      <div class="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl">
        <h3 class="mb-4 text-lg font-bold text-gray-900">Xác nhận xóa</h3>
        <p class="mb-6 text-sm text-gray-600">
          Bạn có chắc chắn muốn xóa nội dung <strong>"{{ deletingContent.title }}"</strong>?
          <br />
          Hành động này không thể hoàn tác.
        </p>
        <div class="flex justify-end gap-3">
          <button
            type="button"
            class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-50"
            @click="closeDeleteModal"
          >
            Hủy
          </button>
          <button
            type="button"
            class="rounded-lg bg-rose-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-rose-700 disabled:opacity-50"
            :disabled="deleting"
            @click="deleteContent"
          >
            {{ deleting ? 'Đang xóa...' : 'Xóa' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { showToast } from '@/utils/toast'
import { contentService, type Module } from '@/services/content.service'
import { courseService } from '@/services/course.service'

/* ==== TYPES ==== */
type Subject = 'math' | 'vietnamese' | 'english' | 'science' | 'history'
type Ctype = 'video' | 'pdf' | 'doc' | 'quiz'
type GradeBand = 'Khối 1–2' | 'Khối 3–5'
type ContentItem = {
  id: number
  title: string
  subject: Subject
  type: Ctype
  gradeBand: GradeBand
  updatedAt: string
  meta?: { duration?: string; size?: string; questions?: number }
}
type ListParams = {
  q?: string
  gradeBand?: GradeBand | ''
  type?: Ctype | ''
  page?: number
  pageSize?: number
}
type ListResult = { items: ContentItem[]; total: number }
type ListFn = (p: ListParams) => Promise<ListResult>

/* ==== ROUTER ==== */
const router = useRouter()
const route = useRoute()
const courseId = route.query.courseId ? String(route.query.courseId) : ''

/* ==== STATE ==== */
const q = ref('')
const gradeBand = ref<'' | GradeBand>('')
const ctype = ref<'' | Ctype>('')
const loading = ref(true)
const items = ref<ContentItem[]>([])
const courseTitle = ref('')
const modules = ref<Module[]>([])

/* Pagination */
const page = ref(1)
const pageSize = ref(12)
const total = ref(0)
const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize.value)))

/* Add Modal */
const showAddModal = ref(false)
const selectedContent = ref<ContentItem | null>(null)
const selectedModuleId = ref<string>('')
const newModuleTitle = ref('')
const lessonPosition = ref<number>(0)
const adding = ref(false)

/* Edit/Delete Modal */
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const editingContent = ref<ContentItem | null>(null)
const deletingContent = ref<ContentItem | null>(null)
const saving = ref(false)
const deleting = ref(false)

const editForm = ref({
  title: '',
  subject: 'math' as Subject,
  type: 'video' as Ctype,
  gradeBand: 'Khối 1–2' as GradeBand,
  meta: {} as ContentItem['meta']
})

/* Create Content */
function openCreateModal() {
  if (courseId) {
    // Nếu đang ở trong context của một khóa học, đi đến trang quản lý nội dung
    router.push({ name: 'teacher-course-content', params: { id: courseId } })
  } else {
    // Mở modal tạo mới
    editingContent.value = null
    editForm.value = {
      title: '',
      subject: 'math',
      type: 'video',
      gradeBand: 'Khối 1–2',
      meta: {}
    }
    showEditModal.value = true
  }
}

function openEditModal(item: ContentItem) {
  editingContent.value = item
  editForm.value = {
    title: item.title,
    subject: item.subject,
    type: item.type,
    gradeBand: item.gradeBand,
    meta: { ...item.meta }
  }
  showEditModal.value = true
}

function closeEditModal() {
  showEditModal.value = false
  editingContent.value = null
  editForm.value = {
    title: '',
    subject: 'math',
    type: 'video',
    gradeBand: 'Khối 1–2',
    meta: {}
  }
}

function openDeleteModal(item: ContentItem) {
  deletingContent.value = item
  showDeleteModal.value = true
}

function closeDeleteModal() {
  showDeleteModal.value = false
  deletingContent.value = null
}

async function saveContent() {
  if (!editForm.value.title.trim()) {
    showToast('Vui lòng nhập tên nội dung', 'error')
    return
  }
  saving.value = true
  try {
    if (editingContent.value) {
      // Update existing
      await contentService.updateContentLibrary(editingContent.value.id, {
        title: editForm.value.title,
        subject: editForm.value.subject,
        type: editForm.value.type,
        grade_band: editForm.value.gradeBand,
        meta: editForm.value.meta
      })
      showToast('Đã cập nhật nội dung thành công', 'success')
    } else {
      // Create new
      await contentService.createContentLibrary({
        title: editForm.value.title,
        subject: editForm.value.subject,
        type: editForm.value.type,
        grade_band: editForm.value.gradeBand,
        meta: editForm.value.meta
      })
      showToast('Đã tạo nội dung mới thành công', 'success')
    }
    closeEditModal()
    // Reload list để cập nhật
    await fetchList(page.value)
  } catch (e: any) {
    showToast(e?.response?.data?.detail || e?.message || 'Không thể lưu nội dung', 'error')
  } finally {
    saving.value = false
  }
}

async function deleteContent() {
  if (!deletingContent.value) return
  deleting.value = true
  try {
    await contentService.deleteContentLibrary(deletingContent.value.id)
    showToast('Đã xóa nội dung thành công', 'success')
    closeDeleteModal()
    // Reload list
    await fetchList(page.value)
  } catch (e: any) {
    showToast(e?.response?.data?.detail || e?.message || 'Không thể xóa nội dung', 'error')
  } finally {
    deleting.value = false
  }
}

/* ==== COMPUTED ==== */
const typeCounts = computed(() => {
  const counts = { video: 0, pdf: 0, doc: 0, quiz: 0 }
  items.value.forEach(item => {
    if (item.type in counts) {
      counts[item.type as keyof typeof counts]++
    }
  })
  return counts
})

/* ==== HELPERS ==== */
const subjectLabel = (s: Subject) =>
  s === 'math'
    ? 'Toán'
    : s === 'vietnamese'
      ? 'Tiếng Việt'
      : s === 'english'
        ? 'Tiếng Anh'
        : s === 'science'
          ? 'Khoa học'
          : 'Lịch sử'

const getTypeClass = (type: Ctype) => {
  const classes = {
    video: 'bg-blue-100 text-blue-700',
    pdf: 'bg-rose-100 text-rose-700',
    doc: 'bg-emerald-100 text-emerald-700',
    quiz: 'bg-amber-100 text-amber-700'
  }
  return classes[type] || 'bg-slate-100 text-slate-700'
}

const getTypeIcon = (type: Ctype) => {
  const icons = {
    video: '▶',
    pdf: '📄',
    doc: '📝',
    quiz: '❓'
  }
  return icons[type] || '📦'
}

/* Debounce search */
let debounceTimer: number | null = null
function debouncedFetch() {
  if (debounceTimer) clearTimeout(debounceTimer)
  debounceTimer = window.setTimeout(() => fetchList(1), 250) as unknown as number
}

/* ==== FETCH ==== */
async function fetchList(p = page.value) {
  loading.value = true
  page.value = p
  try {
    const params: ListParams = {
      q: q.value || undefined,
      gradeBand: gradeBand.value || undefined,
      type: ctype.value || undefined,
      page: page.value,
      pageSize: pageSize.value,
    }

    const res = await contentService.listContentLibrary(params)
    
    // Map backend response to frontend format
    items.value = res.items.map((item: any) => ({
      id: item.id,
      title: item.title,
      subject: item.subject,
      type: item.type,
      gradeBand: item.grade_band,
      updatedAt: item.updatedAt || item.updated_at,
      meta: item.meta || {}
    }))
    total.value = res.total
  } catch (e) {
    console.error('Error fetching content library:', e)
    items.value = []
    total.value = 0
    showToast('Không thể tải danh sách nội dung', 'error')
  } finally {
    loading.value = false
  }
}

async function loadCourseInfo() {
  if (!courseId) return
  try {
    const course = await courseService.detail(courseId, true)
    courseTitle.value = course.title
  } catch (e) {
    console.error('Error loading course:', e)
  }
}

async function loadModules() {
  if (!courseId) return
  try {
    modules.value = await contentService.listModules(courseId)
  } catch (e) {
    console.error('Error loading modules:', e)
  }
}

/* ==== Pager window ==== */
const pagesToShow = computed(() => {
  const max = totalPages.value
  const cur = page.value
  const windowSize = 7
  const arr: { key: string; num?: number; text: string; sep?: boolean }[] = []
  const push = (n: number) => arr.push({ key: 'p' + n, num: n, text: String(n) })
  const sep = (k: string) => arr.push({ key: k, text: '…', sep: true })

  if (max <= windowSize + 2) {
    for (let i = 1; i <= max; i++) push(i)
  } else {
    push(1)
    const start = Math.max(2, cur - 2)
    const end = Math.min(max - 1, cur + 2)
    if (start > 2) sep('s')
    for (let i = start; i <= end; i++) push(i)
    if (end < max - 1) sep('e')
    push(max)
  }
  return arr
})

/* ==== Actions ==== */
function openAddModal(item: ContentItem) {
  selectedContent.value = item
  selectedModuleId.value = ''
  newModuleTitle.value = ''
  lessonPosition.value = 0
  showAddModal.value = true
  if (courseId && modules.value.length === 0) {
    loadModules()
  }
}

function closeAddModal() {
  showAddModal.value = false
  selectedContent.value = null
  selectedModuleId.value = ''
  newModuleTitle.value = ''
  lessonPosition.value = 0
}

async function addToCourse() {
  if (!selectedContent.value || !courseId) return
  
  adding.value = true
  try {
    let moduleId = selectedModuleId.value
    
    // Tạo module mới nếu cần
    if (!moduleId) {
      if (!newModuleTitle.value.trim()) {
        showToast('Vui lòng nhập tên chương', 'error')
        return
      }
      const newModule = await contentService.createModule(courseId, {
        title: newModuleTitle.value.trim(),
        position: modules.value.length,
        course: courseId
      })
      moduleId = String(newModule.id)
      modules.value.push(newModule)
    }
    
    // Tạo lesson từ content
    const lessonData: any = {
      title: selectedContent.value.title,
      content_type: selectedContent.value.type === 'quiz' ? 'exercise' : 'lesson',
      position: lessonPosition.value === -1 ? -1 : lessonPosition.value
    }
    
    // Map content type to lesson fields
    if (selectedContent.value.type === 'video') {
      lessonData.video_url = `content://${selectedContent.value.id}`
    }
    
    await contentService.createLesson(moduleId, lessonData)
    
    showToast('Đã thêm nội dung vào khóa học thành công', 'success')
    closeAddModal()
    
    // Navigate to course content page
    router.push({ name: 'teacher-course-content', params: { id: courseId } })
  } catch (e: any) {
    showToast(e?.message || 'Không thể thêm nội dung vào khóa học', 'error')
  } finally {
    adding.value = false
  }
}

function previewContent(item: ContentItem) {
  // TODO: Implement preview modal or navigate to preview page
  showToast(`Xem trước: ${item.title}`, 'info')
}

function goBack() {
  if (courseId) {
    router.push({ name: 'teacher-course-content', params: { id: courseId } })
  } else {
    router.push({ path: '/teacher/courses' })
  }
}

onMounted(async () => {
  await Promise.all([
    fetchList(1),
    loadCourseInfo(),
    courseId && loadModules()
  ])
})
</script>

<style scoped>
:host,
.min-h-screen {
  overflow-x: hidden;
}
</style>
