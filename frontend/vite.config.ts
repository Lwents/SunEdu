// vite.config.ts
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import vueJsx from '@vitejs/plugin-vue-jsx'
import sitemap from 'vite-plugin-sitemap'

export default defineConfig(({ mode }) => ({
  plugins: [
    vue(), 
    vueDevTools(), 
    vueJsx(), 
    sitemap({ 
      hostname: 'https://smartedu.click',
      readable: true,
    })
  ],
  resolve: {
    alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) },
  },
  // chỉ bật proxy khi dev (vite serve)
  server:
    mode === 'development'
      ? {
          proxy: {
            '/api': {
              target: 'https://api.smartedu.click',
              changeOrigin: true,
              secure: true,
              rewrite: (p) => p.replace(/^\/api/, '/api'),
            },
          },
        }
      : undefined,
  // Build optimization
  build: {
    rollupOptions: {
      output: {
        manualChunks: (id) => {
          // Vue core & router (small, frequently used)
          if (id.includes('node_modules/vue/') || id.includes('node_modules/@vue/')) {
            return 'vue-vendor'
          }
          if (id.includes('node_modules/vue-router')) {
            return 'vue-vendor'
          }
          if (id.includes('node_modules/pinia')) {
            return 'vue-vendor'
          }

          // Element Plus UI (large library)
          if (id.includes('node_modules/element-plus')) {
            return 'element-plus'
          }

          // ECharts (large visualization library)
          if (id.includes('node_modules/echarts') || id.includes('node_modules/vue-echarts')) {
            return 'echarts'
          }
          if (id.includes('node_modules/zrender')) {
            return 'echarts'
          }

          // Icons & UI utilities (small but many)
          if (
            id.includes('node_modules/@heroicons') ||
            id.includes('node_modules/lucide') ||
            id.includes('node_modules/feather-icons')
          ) {
            return 'icons'
          }

          // VueUse utilities
          if (id.includes('node_modules/@vueuse')) {
            return 'vueuse'
          }

          // Axios & HTTP
          if (id.includes('node_modules/axios')) {
            return 'http'
          }

          // AOS animation
          if (id.includes('node_modules/aos')) {
            return 'animations'
          }

          // Other node_modules -> generic vendor
          if (id.includes('node_modules')) {
            return 'vendor'
          }
        },
        // Naming pattern cho chunks
        chunkFileNames: 'assets/js/[name]-[hash].js',
        entryFileNames: 'assets/js/[name]-[hash].js',
        assetFileNames: 'assets/[ext]/[name]-[hash].[ext]',
      },
    },
    // Tăng warning limit
    chunkSizeWarningLimit: 800,
    // CSS code splitting
    cssCodeSplit: true,
    // Minification
    minify: 'esbuild',
    target: 'es2015',
    // Source map cho production debugging (optional)
    sourcemap: false,
  },
}))
