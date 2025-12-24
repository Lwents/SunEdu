<template>
  <div v-if="show" class="nav">
    <img 
      :src="logo" 
      alt="SunnyEdu Logo" 
      class="logo-sunnyedu"
      :style="{ 
        height: computedHeight,
        transform: `scale(${scale})`
      }"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import logo from '@/assets/images/logo3.png'

const props = defineProps({
  size: { type: Number, default: 24 },
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
.logo-sunnyedu {
  width: auto;
  transform-origin: left center;
  transition: transform 0.2s ease;
}
</style>
