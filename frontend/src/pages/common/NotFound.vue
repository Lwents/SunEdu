<template>
  <div class="min-h-screen flex items-center justify-center bg-white">
    <div class="text-center px-6 py-16 max-w-xl w-full">
      <!-- Số 404 -->
      <h1 class="text-8xl md:text-9xl font-black text-black mb-4">
        404
      </h1>

      <!-- Tiêu đề -->
      <h2 class="text-2xl md:text-3xl font-bold text-gray-900 mb-4">
        Oops! Trang không tồn tại.
      </h2>

      <!-- Mô tả -->
      <p class="text-base md:text-lg text-gray-600 leading-relaxed mb-8">
        Trang bạn tìm kiếm không được tìm thấy hoặc đã bị di chuyển.
      </p>

      <!-- Nút về trang chủ -->
      <router-link
        to="/"
        class="inline-block px-8 py-3 bg-black text-white font-semibold rounded-lg border-2 border-black hover:bg-white hover:text-black transition-colors duration-200"
      >
        Quay về trang chủ
      </router-link>
    </div>
  </div>
</template>

<script setup>
// Không cần script
</script>

<style scoped>
/* Không cần custom CSS */
</style>
