<!-- src/App.vue -->
<template>
  <!-- Element Plus config (tùy chọn, nhưng hữu ích) -->
  <el-config-provider namespace="el" :z-index="3000">
    <IdleWarning />
    <!-- Route outlet -->
    <RouterView v-slot="{ Component }">
      <Transition name="fade" mode="out-in">
        <component :is="Component" />
      </Transition>
    </RouterView>
  </el-config-provider>
</template>

<script setup lang="ts">
import IdleWarning from '@/components/ui/IdleWarning.vue'
import { RouterView } from 'vue-router'
import { ElConfigProvider } from 'element-plus'
</script>

<style>
/* Transition nhẹ nhàng khi đổi page */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
