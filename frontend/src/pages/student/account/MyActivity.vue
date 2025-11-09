<template>
  <div class="space-y-4">
    <ul class="flex flex-col gap-3">
      <li
        v-for="(it, i) in items"
        :key="i"
        class="flex items-start gap-4 rounded-2xl border border-slate-200 bg-white px-4 py-3 shadow-sm shadow-slate-100"
      >
        <div class="mt-2 h-2.5 w-2.5 rounded-full bg-emerald-500"></div>
        <div class="flex-1">
          <p class="text-sm font-semibold text-slate-900">{{ it.title }}</p>
          <p class="text-xs text-slate-500">{{ it.time }}</p>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
const items = [
  { title: 'Đăng nhập hệ thống', time: 'Hôm nay, 09:25' },
  { title: 'Cập nhật thông tin hồ sơ', time: 'Hôm qua, 19:10' },
  { title: 'Đổi mật khẩu', time: '2 ngày trước, 08:02' },
]
</script>
