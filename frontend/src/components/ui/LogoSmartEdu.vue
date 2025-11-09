<template>
  <div class="nav" :style="{ height: computedHeight }">
    <img
      v-if="show"
      :src="logo"
      alt="SmartEdu Logo"
      class="logo-smartedu"
      :style="{ height: computedHeight }"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import logo from '@/assets/images/demologo.png'

const props = defineProps({
  size: { type: Number, default: 56 },
  scale: { type: Number, default: 1 },
  show: { type: Boolean, default: true },
})

const width = ref(window.innerWidth)
function handleResize() {
  width.value = window.innerWidth
}
onMounted(() => window.addEventListener('resize', handleResize))
onUnmounted(() => window.removeEventListener('resize', handleResize))

const computedHeight = computed(() => {
  if (width.value < 640) return `${Math.round(props.size * 0.7)}px`
  if (width.value < 1024) return `${Math.round(props.size * 0.85)}px`
  return `${props.size}px`
})
</script>

<style scoped>
.nav {
  display: flex;
  align-items: center;
  overflow: visible;
}
.logo-smartedu {
  width: auto;
  transform-origin: left center;
  transition: transform 0.2s ease;
}
</style>
