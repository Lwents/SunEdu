<template>
  <div class="sliding-auth-layout">
    <!-- Simple Gradient Background -->
    <div class="bg-canvas"></div>

    <!-- Home Button -->
    <router-link to="/" class="home-button">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
        />
      </svg>
      <span class="home-text">Trang chủ</span>
    </router-link>

    <!-- Main Container -->
    <div class="content-wrapper">
      <!-- Sliding Auth Container (Login/Register) -->
      <div
        v-if="isLoginOrRegister"
        class="auth-container"
        :class="{ 'register-mode': isRegisterPage }"
      >
        <!-- Left Panel - Login Form -->
        <div class="form-panel left-panel">
          <div class="form-wrapper">
            <div class="brand-header">
              <LogoSmartEdu :size="50" />
              <h2 class="form-title">Đăng nhập</h2>
            </div>
            <Login v-if="route.path === '/auth/login'" />
          </div>
        </div>

        <!-- Right Panel - Register Form -->
        <div class="form-panel right-panel">
          <div class="form-wrapper">
            <div class="brand-header">
              <LogoSmartEdu :size="50" />
              <h2 class="form-title">Đăng ký</h2>
            </div>
            <Register v-if="route.path === '/auth/register'" />
          </div>
        </div>

        <!-- Sliding Overlay Panel -->
        <div class="overlay-container">
          <div class="overlay">
            <!-- Left Overlay (shown when in Register mode) -->
            <div class="overlay-panel overlay-left">
              <h2 class="overlay-title">Chào mừng trở lại!</h2>
              <p class="overlay-text">Đăng nhập để tiếp tục hành trình học tập của bạn</p>
              <button class="overlay-btn" @click="switchToLogin">Đăng nhập</button>
            </div>

            <!-- Right Overlay (shown when in Login mode) -->
            <div class="overlay-panel overlay-right">
              <h2 class="overlay-title">Chào bạn!</h2>
              <p class="overlay-text">Tạo tài khoản mới để bắt đầu học tập cùng SmartEdu</p>
              <button class="overlay-btn" @click="switchToRegister">Đăng ký</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Simple Card for Other Auth Pages -->
      <div v-else class="simple-auth-card">
        <div class="brand-header">
          <LogoSmartEdu :size="50" />
          <h2 class="form-title">{{ route.meta.title }}</h2>
        </div>
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import LogoSmartEdu from '@/components/ui/LogoSmartEdu.vue'
import Login from '@/pages/auth/Login.vue'
import Register from '@/pages/auth/Register.vue'

const route = useRoute()
const router = useRouter()

const isLoginOrRegister = computed(
  () => route.path === '/auth/login' || route.path === '/auth/register',
)

const isRegisterPage = computed(() => route.path === '/auth/register')

function switchToLogin() {
  router.push('/auth/login')
}

function switchToRegister() {
  router.push('/auth/register')
}
</script>

<style scoped>
/* 🌈 Sliding Auth Layout - Modern Form with Overlay Animation */
.sliding-auth-layout {
  min-height: 100vh;
  width: 100%;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

/* ✨ Simple Gradient Background */
.bg-canvas {
  position: absolute;
  inset: 0;
  z-index: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* 🏠 Home Button */
.home-button {
  position: fixed;
  top: 2rem;
  left: 2rem;
  z-index: 100;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border-radius: 50px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.home-button:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.home-text {
  font-size: 0.9375rem;
}

/* 📦 Content Wrapper */
.content-wrapper {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 990px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 🎴 Auth Container - Main Box */
.auth-container {
  position: relative;
  width: 100%;
  min-height: 660px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 32px;
  box-shadow:
    0 20px 60px rgba(0, 0, 0, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.3) inset;
  overflow: hidden;
  animation: fadeInScale 0.6s ease-out;
}

@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* 📄 Form Panels */
.form-panel {
  position: absolute;
  top: 0;
  height: 100%;
  width: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3.3rem 2.75rem;
  transition:
    transform 1s cubic-bezier(0.34, 1.56, 0.64, 1),
    opacity 0.6s ease-out;
  z-index: 2;
}

.left-panel {
  left: 0;
}

.right-panel {
  right: 0;
  transform: translateX(100%);
}

/* When in Register Mode */
.auth-container.register-mode .left-panel {
  transform: translateX(-100%);
}

.auth-container.register-mode .right-panel {
  transform: translateX(0);
}

/* Form Wrapper */
.form-wrapper {
  width: 100%;
  max-width: 420px;
  animation: fadeIn 0.8s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* 🏷️ Brand Header */
.brand-header {
  text-align: center;
  margin-bottom: 2rem;
}

.form-title {
  font-size: 1.75rem;
  font-weight: 900;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-top: 1rem;
  letter-spacing: 0.5px;
}

/* 🎴 Simple Auth Card (for other auth pages) */
.simple-auth-card {
  width: 100%;
  max-width: 530px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 32px;
  padding: 3.3rem 2.75rem;
  box-shadow:
    0 20px 60px rgba(0, 0, 0, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.3) inset;
  animation: fadeInScale 0.6s ease-out;
}

/*  Overlay Container */
.overlay-container {
  position: absolute;
  top: 0;
  left: 50%;
  width: 50%;
  height: 100%;
  overflow: hidden;
  transition: transform 1s cubic-bezier(0.34, 1.56, 0.64, 1);
  z-index: 100;
}

.auth-container.register-mode .overlay-container {
  transform: translateX(-100%);
}

/* Overlay Background */
.overlay {
  position: relative;
  width: 200%;
  height: 100%;
  left: -100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  transform: translateX(0);
  transition: transform 1s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.auth-container.register-mode .overlay {
  transform: translateX(50%);
}

/* Overlay Panels */
.overlay-panel {
  position: absolute;
  top: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3.3rem 2.75rem;
  width: 50%;
  height: 100%;
  text-align: center;
  color: white;
  transform: translateX(0);
  transition:
    transform 1s cubic-bezier(0.34, 1.56, 0.64, 1),
    opacity 0.7s cubic-bezier(0.4, 0, 0.2, 1);
}

.overlay-left {
  left: 0;
  transform: translateX(-20%);
  opacity: 0;
}

.overlay-right {
  right: 0;
  transform: translateX(0);
  opacity: 1;
}

.auth-container.register-mode .overlay-left {
  transform: translateX(0);
  opacity: 1;
}

.auth-container.register-mode .overlay-right {
  transform: translateX(20%);
  opacity: 0;
}

/* Overlay Content */
.overlay-title {
  font-size: 2rem;
  font-weight: 900;
  margin-bottom: 1rem;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  animation: fadeInUp 0.6s ease-out;
}

.overlay-text {
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 2rem;
  opacity: 0.95;
  animation: fadeInUp 0.6s ease-out 0.1s both;
}

.overlay-btn {
  padding: 0.875rem 2.5rem;
  background: white;
  color: #667eea;
  border: none;
  border-radius: 50px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  text-transform: uppercase;
  letter-spacing: 1px;
  animation: fadeInUp 0.6s ease-out 0.2s both;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.overlay-btn:hover {
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
  background: rgba(255, 255, 255, 0.95);
}

.overlay-btn:active {
  transform: translateY(-1px) scale(1.02);
}

/* � Left Side - Decorative */
.left-side {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  overflow-y: auto;
}

.decoration-content {
  width: 100%;
  max-width: 500px;
  color: white;
}

.brand-section {
  text-align: center;
  margin-bottom: 3rem;
  animation: fadeInUp 0.8s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.brand-title {
  font-size: 2.5rem;
  font-weight: 900;
  margin: 1rem 0 0.5rem;
  letter-spacing: 2px;
}

.brand-tagline {
  font-size: 1.125rem;
  opacity: 0.9;
  font-weight: 500;
}

.features-showcase {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.feature-item {
  display: flex;
  gap: 1.25rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
  animation: fadeInLeft 0.6s ease-out both;
}

@keyframes fadeInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.feature-item:hover {
  transform: translateX(10px);
  background: rgba(255, 255, 255, 0.15);
}

.feature-icon {
  font-size: 2.5rem;
  flex-shrink: 0;
}

.feature-content {
  flex: 1;
}

.feature-title {
  font-size: 1.125rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.feature-desc {
  font-size: 0.875rem;
  opacity: 0.8;
}

.stats-showcase {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.stat-item {
  text-align: center;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
  animation: fadeInUp 0.6s ease-out both;
}

.stat-item:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.15);
}

.stat-icon {
  font-size: 2rem;
  margin-bottom: 0.75rem;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 900;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.875rem;
  opacity: 0.8;
}

/* 📝 Right Side - Form */
.right-side {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  background: rgba(255, 255, 255, 0.95);
  overflow-y: auto;
}

.form-container {
  width: 100%;
  max-width: 480px;
  animation: fadeInRight 0.8s ease-out;
}

@keyframes fadeInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.form-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.form-title {
  font-size: 2.25rem;
  font-weight: 900;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.75rem;
}

.form-subtitle {
  font-size: 1rem;
  color: #6b7280;
  font-weight: 500;
}

/* 🎬 Transitions */
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.2s ease-in;
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* 📱 Responsive Design */
@media (max-width: 768px) {
  .content-wrapper {
    max-width: 100%;
  }

  .auth-container {
    min-height: 550px;
  }

  .form-panel {
    width: 100%;
    padding: 2.5rem 2rem;
  }

  .left-panel {
    left: 0;
  }

  .right-panel {
    right: 0;
    transform: translateX(100%);
  }

  .overlay-container {
    display: none;
  }

  .auth-container.register-mode .left-panel {
    transform: translateX(-100%);
  }

  .auth-container.register-mode .right-panel {
    transform: translateX(0);
  }

  .form-title {
    font-size: 1.5rem;
  }

  .home-button {
    top: 1rem;
    left: 1rem;
    padding: 0.625rem 1.25rem;
  }

  .home-text {
    font-size: 0.875rem;
  }
}

@media (max-width: 640px) {
  .sliding-auth-layout {
    padding: 1.5rem 1rem;
  }

  .auth-container {
    min-height: 500px;
    border-radius: 24px;
  }

  .form-panel {
    padding: 2rem 1.5rem;
  }

  .brand-header {
    margin-bottom: 1.5rem;
  }

  .form-title {
    font-size: 1.375rem;
  }

  .home-button {
    top: 0.75rem;
    left: 0.75rem;
    padding: 0.5rem 1rem;
  }

  .home-text {
    display: none;
  }
}

@media (max-width: 480px) {
  .sliding-auth-layout {
    padding: 1rem 0.75rem;
  }

  .auth-container {
    min-height: 450px;
    border-radius: 20px;
  }

  .form-panel {
    padding: 1.75rem 1.25rem;
  }

  .form-title {
    font-size: 1.25rem;
  }
}

/* Landscape mobile */
@media (max-height: 600px) and (orientation: landscape) {
  .sliding-auth-layout {
    padding: 1rem;
    align-items: flex-start;
    overflow-y: auto;
  }

  .auth-container {
    margin: 1rem 0;
    min-height: auto;
  }

  .form-panel {
    padding: 2rem 1.5rem;
  }
}
</style>
