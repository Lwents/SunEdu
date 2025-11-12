# 🎨 SunEdu Purple Gradient Theme - Tailwind Configuration

## Overview
Theme mới với màu gradient tím đẹp mắt, hiện đại và hỗ trợ đầy đủ Dark Mode.

---

## 🎯 Màu Sắc Chính

### Light Mode
- **Primary**: Purple gradient (#667eea → #764ba2)
- **Secondary**: Indigo (#6366f1)
- **Accent**: Pink/Purple (#d946ef)
- **Background**: Gradient từ purple-50 qua white đến indigo-50

### Dark Mode
- **Primary**: Dark purple gradient (#434343 → #000000 with purple accent)
- **Background**: Gradient từ gray-900 qua gray-800 đến slate-900
- **Text**: Gray-100
- **Glow Effects**: Purple glow shadows

---

## 🚀 Cách Sử dụng

### 1. Colors

#### Primary Colors (Purple)
```vue
<div class="bg-primary-500 text-white">Purple background</div>
<div class="text-primary-600">Purple text</div>
<div class="border-primary-400">Purple border</div>
```

#### Secondary Colors (Indigo)
```vue
<div class="bg-secondary-500 text-white">Indigo background</div>
```

#### Accent Colors (Pink)
```vue
<div class="bg-accent-500 text-white">Pink accent</div>
```

---

### 2. Gradient Backgrounds

#### Purple Gradient (Chính - như Login page)
```vue
<button class="bg-gradient-primary hover:bg-gradient-primary-hover">
  Button với gradient tím
</button>
```

#### Mesh Gradients (Background toàn trang)
```vue
<!-- Light mode -->
<div class="bg-mesh-light">
  Mesh gradient background
</div>

<!-- Dark mode -->
<div class="dark:bg-mesh-dark">
  Mesh gradient dark
</div>
```

---

### 3. Components với Dark Mode

#### Cards
```vue
<div class="student-card">
  <!-- Tự động đổi màu khi dark mode -->
  Card content
</div>
```

#### Buttons
```vue
<button class="btn-gradient">
  <!-- Purple gradient trong light mode -->
  <!-- Purple accent gradient trong dark mode -->
  Gradient Button
</button>
```

#### Input Fields
```vue
<input type="text" class="input-field" placeholder="Email...">
<!-- Tự động dark mode styling -->
```

#### Tabs
```vue
<div class="student-tabs">
  <button class="student-tab student-tab--active">Active Tab</button>
  <button class="student-tab">Inactive Tab</button>
</div>
```

---

### 4. Shadow Effects

#### Purple Glow (Light Mode)
```vue
<div class="shadow-purple-glow">Light purple glow</div>
<div class="shadow-purple-glow-lg">Bigger purple glow</div>
```

#### Dark Mode Glow
```vue
<div class="dark:shadow-dark-glow">Dark mode glow</div>
```

---

### 5. Glass Effect
```vue
<div class="glass-effect">
  <!-- Glassmorphism với purple tint -->
  Glass effect card
</div>
```

---

### 6. Utility Classes

#### Gradient Text
```vue
<h1 class="text-gradient text-4xl font-bold">
  Gradient Text
</h1>
```

#### Hover Lift
```vue
<div class="hover-lift rounded-xl bg-white p-6">
  <!-- Nổi lên khi hover -->
  Hover me
</div>
```

#### Glow on Hover
```vue
<button class="glow-on-hover rounded-xl px-6 py-3">
  Glow when hover
</button>
```

#### Smooth Transitions
```vue
<div class="smooth-transition">
  <!-- Mượt mà khi chuyển đổi -->
  Smooth animations
</div>
```

---

### 7. Animations

```vue
<!-- Fade in -->
<div class="animate-fade-in">Fade in</div>

<!-- Scale in với bounce -->
<div class="animate-scale-in">Scale in</div>

<!-- Shimmer effect -->
<div class="animate-shimmer bg-gradient-primary">Shimmer</div>

<!-- Glow pulse -->
<div class="animate-glow">Glowing</div>

<!-- Float animation -->
<div class="animate-float">Floating</div>
```

---

## 🌓 Dark Mode Toggle

### Sử dụng Component
```vue
<script setup>
import DarkModeToggle from '@/components/DarkModeToggle.vue'
</script>

<template>
  <DarkModeToggle />
</template>
```

### Manual Toggle
```javascript
// Toggle dark mode manually
function toggleDarkMode() {
  if (document.documentElement.classList.contains('dark')) {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  } else {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  }
}
```

---

## 📱 Responsive Dark Mode Classes

```vue
<!-- Tự động dark mode -->
<div class="bg-white dark:bg-gray-800">
  Content
</div>

<p class="text-gray-900 dark:text-gray-100">
  Text tự động đổi màu
</p>

<div class="border-purple-200 dark:border-primary-800">
  Border tự động
</div>
```

---

## 🎨 Color Palette Reference

### Primary Purple Scale
- `primary-50` → `#f5f3ff` (Rất nhạt)
- `primary-100` → `#ede9fe`
- `primary-200` → `#ddd6fe`
- `primary-300` → `#c4b5fd`
- `primary-400` → `#a78bfa`
- `primary-500` → `#8b5cf6` ⭐ Main
- `primary-600` → `#7c3aed`
- `primary-700` → `#6d28d9`
- `primary-800` → `#5b21b6`
- `primary-900` → `#4c1d95` (Rất đậm)

### Secondary Indigo Scale
- `secondary-500` → `#6366f1` ⭐ Main
- Tương tự primary scale

### Accent Pink Scale
- `accent-500` → `#d946ef` ⭐ Main

---

## ✨ Examples

### Login Page Button Style
```vue
<button class="w-full bg-gradient-primary hover:bg-gradient-primary-hover text-white font-semibold py-3 px-6 rounded-xl shadow-purple-glow transition-all duration-300 hover:shadow-purple-glow-lg hover:scale-105 active:scale-95">
  Đăng nhập
</button>
```

### Card with Hover Effect
```vue
<div class="student-card hover-lift glow-on-hover cursor-pointer">
  <h3 class="text-gradient text-xl font-bold">Card Title</h3>
  <p class="text-gray-600 dark:text-gray-400">Card description</p>
</div>
```

### Glass Card
```vue
<div class="glass-effect rounded-2xl p-6">
  <h2 class="text-gradient text-2xl font-bold mb-4">Glass Card</h2>
  <p class="text-gray-700 dark:text-gray-300">
    Beautiful glassmorphism effect
  </p>
</div>
```

---

## 🔥 Best Practices

1. **Luôn thêm dark mode classes** cho components mới
2. **Sử dụng gradient backgrounds** cho CTAs và highlights
3. **Thêm smooth-transition** cho interactive elements
4. **Sử dụng shadow-purple-glow** thay vì shadow thông thường
5. **Test cả light và dark mode** trước khi deploy

---

## 📦 Files Updated

- ✅ `tailwind.config.js` - Main configuration
- ✅ `src/styles/tailwind.css` - Global styles & components
- ✅ `src/components/DarkModeToggle.vue` - Dark mode toggle component

---

## 🎯 Migration Guide

### Từ màu cũ sang màu mới:

```vue
<!-- Cũ -->
<div class="bg-brand-500">Old brand color</div>

<!-- Mới -->
<div class="bg-primary-500">New primary purple</div>
```

```vue
<!-- Cũ -->
<div class="bg-green-500">Old green</div>

<!-- Mới -->
<div class="bg-gradient-primary">New gradient</div>
```

---

**Enjoy your beautiful purple gradient theme! 💜✨**
