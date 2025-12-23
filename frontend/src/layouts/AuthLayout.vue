<template>
  <div class="auth-layout">
    <!-- Background with 3D Elements -->
    <div class="bg-canvas">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
      <div class="floating-shape shape-1"></div>
      <div class="floating-shape shape-2"></div>
      <div class="floating-shape shape-3"></div>
    </div>

    <!-- Home Button -->
    <router-link to="/" class="home-button">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
      </svg>
      <span class="home-text">Trang chủ</span>
    </router-link>

    <!-- Main Container -->
    <div class="content-wrapper">
      <!-- Sliding Auth Container -->
      <div v-if="isLoginOrRegister" class="auth-container" :class="{ 'register-mode': isRegisterPage }">
        <!-- Left Panel - Login -->
        <div class="form-panel left-panel">
          <div class="form-wrapper">
            <div class="brand-header">
              <h2 class="form-title">Đăng nhập</h2>
              <p class="form-subtitle">Chào mừng trở lại! Tiếp tục hành trình học tập</p>
            </div>
            <Login v-if="route.path === '/auth/login'" />
          </div>
        </div>

        <!-- Right Panel - Register -->
        <div class="form-panel right-panel">
          <div class="form-wrapper">
            <div class="brand-header">
              <h2 class="form-title">Đăng ký</h2>
              <p class="form-subtitle">Tạo tài khoản để bắt đầu học tập</p>
            </div>
            <Register v-if="route.path === '/auth/register'" />
          </div>
        </div>

        <!-- Sliding Overlay -->
        <div class="overlay-container">
          <div class="overlay">
            <div class="overlay-panel overlay-left">
              <div class="overlay-content">
                <div class="overlay-icon">👋</div>
                <h2 class="overlay-title">Chào mừng trở lại!</h2>
                <p class="overlay-text">Đăng nhập để tiếp tục hành trình học tập của bạn</p>
                <button class="overlay-btn" @click="switchToLogin">
                  <span>Đăng nhập</span>
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/>
                  </svg>
                </button>
              </div>
            </div>
            <div class="overlay-panel overlay-right">
              <div class="overlay-content">
                <div class="overlay-icon">🚀</div>
                <h2 class="overlay-title">Chào bạn mới!</h2>
                <p class="overlay-text">Tạo tài khoản để bắt đầu học tập cùng SmartEdu</p>
                <button class="overlay-btn" @click="switchToRegister">
                  <span>Đăng ký ngay</span>
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Simple Card for Other Pages -->
      <div v-else class="simple-auth-card">
        <div class="brand-header">
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
import Login from '@/pages/auth/Login.vue'
import Register from '@/pages/auth/Register.vue'

const route = useRoute()
const router = useRouter()

const isLoginOrRegister = computed(() => 
  route.path === '/auth/login' || route.path === '/auth/register'
)
const isRegisterPage = computed(() => route.path === '/auth/register')

function switchToLogin() { router.push('/auth/login') }
function switchToRegister() { router.push('/auth/register') }
</script>

<style scoped>
.auth-layout {
  min-height: 100vh;
  width: 100%;
  position: relative;
  overflow: hidden;
  background: #0f172a;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

/* Background */
.bg-canvas {
  position: absolute;
  inset: 0;
  z-index: 0;
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.5;
}

.orb-1 {
  top: 10%;
  left: -10%;
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #06b6d4, #3b82f6);
  animation: float-slow 8s ease-in-out infinite;
}

.orb-2 {
  bottom: 10%;
  right: -10%;
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #8b5cf6, #ec4899);
  animation: float-medium 6s ease-in-out infinite;
}

.orb-3 {
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 600px;
  height: 600px;
  background: linear-gradient(135deg, #6366f1, #a855f7);
  opacity: 0.3;
}

.floating-shape {
  position: absolute;
  border-radius: 20px;
  opacity: 0.1;
  background: linear-gradient(135deg, #06b6d4, #8b5cf6);
}

.shape-1 {
  top: 15%;
  right: 15%;
  width: 80px;
  height: 80px;
  transform: rotate(45deg);
  animation: float-slow 10s ease-in-out infinite;
}

.shape-2 {
  bottom: 20%;
  left: 10%;
  width: 60px;
  height: 60px;
  transform: rotate(12deg);
  animation: float-medium 8s ease-in-out infinite;
}

.shape-3 {
  top: 60%;
  right: 25%;
  width: 40px;
  height: 40px;
  transform: rotate(-12deg);
  animation: float-fast 6s ease-in-out infinite;
}

@keyframes float-slow {
  0%, 100% { transform: translateY(0) rotate(45deg); }
  50% { transform: translateY(-30px) rotate(45deg); }
}

@keyframes float-medium {
  0%, 100% { transform: translateY(0) rotate(12deg); }
  50% { transform: translateY(-20px) rotate(12deg); }
}

@keyframes float-fast {
  0%, 100% { transform: translateY(0) rotate(-12deg); }
  50% { transform: translateY(-15px) rotate(-12deg); }
}

/* Home Button */
.home-button {
  position: fixed;
  top: 2rem;
  left: 2rem;
  z-index: 100;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border-radius: 50px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
  font-weight: 600;
  transition: all 0.3s ease;
}

.home-button:hover {
  background: rgba(6, 182, 212, 0.2);
  border-color: rgba(6, 182, 212, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(6, 182, 212, 0.2);
}

/* Content */
.content-wrapper {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 1000px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Auth Container */
.auth-container {
  position: relative;
  width: 100%;
  min-height: 600px;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border-radius: 32px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 
    0 25px 50px rgba(0, 0, 0, 0.5),
    0 0 100px rgba(6, 182, 212, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  overflow: hidden;
  animation: fadeInScale 0.6s ease-out;
}

@keyframes fadeInScale {
  from { opacity: 0; transform: scale(0.95) translateY(20px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

/* Form Panels */
.form-panel {
  position: absolute;
  top: 0;
  height: 100%;
  width: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem 2.5rem;
  transition: transform 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  z-index: 2;
  background: rgba(15, 23, 42, 0.8);
}

.left-panel { left: 0; }
.right-panel { right: 0; transform: translateX(100%); }

.auth-container.register-mode .left-panel { transform: translateX(-100%); }
.auth-container.register-mode .right-panel { transform: translateX(0); }

.form-wrapper {
  width: 100%;
  max-width: 380px;
}

/* Brand Header */
.brand-header {
  text-align: center;
  margin-bottom: 2rem;
}

.form-title {
  font-size: 1.75rem;
  font-weight: 800;
  background: linear-gradient(135deg, #06b6d4, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-top: 1rem;
  margin-bottom: 0.5rem;
}

.form-subtitle {
  font-size: 0.875rem;
  color: #94a3b8;
}

/* Overlay */
.overlay-container {
  position: absolute;
  top: 0;
  left: 50%;
  width: 50%;
  height: 100%;
  overflow: hidden;
  transition: transform 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  z-index: 100;
}

.auth-container.register-mode .overlay-container {
  transform: translateX(-100%);
}

.overlay {
  position: relative;
  width: 200%;
  height: 100%;
  left: -100%;
  background: linear-gradient(135deg, #0e7490 0%, #1e1b4b 50%, #0f172a 100%);
  transform: translateX(0);
  transition: transform 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.auth-container.register-mode .overlay {
  transform: translateX(50%);
}

.overlay-panel {
  position: absolute;
  top: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50%;
  height: 100%;
  transition: all 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
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

.overlay-content {
  text-align: center;
  color: white;
  padding: 2rem;
}

.overlay-icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.overlay-title {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 1rem;
  text-shadow: 0 2px 20px rgba(0, 0, 0, 0.3);
}

.overlay-text {
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.overlay-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #06b6d4 0%, #8b5cf6 100%);
  backdrop-filter: blur(10px);
  color: white;
  border: none;
  border-radius: 50px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 10px 30px -5px rgba(6, 182, 212, 0.4);
}

.overlay-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 40px -5px rgba(6, 182, 212, 0.5);
}

/* Simple Auth Card */
.simple-auth-card {
  width: 100%;
  max-width: 480px;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border-radius: 32px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 3rem 2.5rem;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
  animation: fadeInScale 0.6s ease-out;
}

/* Responsive */
@media (max-width: 768px) {
  .auth-container { min-height: 500px; }
  .form-panel { width: 100%; padding: 2rem 1.5rem; }
  .overlay-container { display: none; }
  .home-button { top: 1rem; left: 1rem; padding: 0.5rem 1rem; }
  .home-text { display: none; }
}

@media (max-width: 640px) {
  .auth-layout { padding: 1rem; }
  .auth-container { border-radius: 24px; }
  .form-panel { padding: 1.5rem 1.25rem; }
}
</style>
