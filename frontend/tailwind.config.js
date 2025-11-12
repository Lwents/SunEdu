import defaultTheme from 'tailwindcss/defaultTheme'

// Ocean Blue theme with gradient effects
const oceanBluePalette = {
  50: '#f0f9ff',
  100: '#e0f2fe',
  200: '#bae6fd',
  300: '#7dd3fc',
  400: '#38bdf8',
  500: '#0ea5e9',
  600: '#0284c7',
  700: '#0369a1',
  800: '#075985',
  900: '#0c4a6e',
}

const tealPalette = {
  50: '#f0fdfa',
  100: '#ccfbf1',
  200: '#99f6e4',
  300: '#5eead4',
  400: '#2dd4bf',
  500: '#14b8a6',
  600: '#0d9488',
  700: '#0f766e',
  800: '#115e59',
  900: '#134e4a',
}

/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class', // Enable dark mode with class strategy
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        // Primary brand colors - Ocean Blue gradient theme
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9', // Main ocean blue
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
        secondary: {
          50: '#f0fdfa',
          100: '#ccfbf1',
          200: '#99f6e4',
          300: '#5eead4',
          400: '#2dd4bf',
          500: '#14b8a6', // Main teal
          600: '#0d9488',
          700: '#0f766e',
          800: '#115e59',
          900: '#134e4a',
        },
        // Ocean gradient colors
        ocean: {
          light: '#06b6d4',  // Cyan
          main: '#0891b2',   // Ocean blue
          deep: '#0e7490',   // Deep ocean
          dark: '#155e75',   // Dark ocean
        },
        // Gradient colors for backgrounds
        gradient: {
          from: '#06b6d4', // Cyan
          via: '#0891b2',  // Ocean blue
          to: '#14b8a6',   // Teal
        },
        // Accent color - Coral/Orange for contrast
        accent: {
          50: '#fff7ed',
          100: '#ffedd5',
          200: '#fed7aa',
          300: '#fdba74',
          400: '#fb923c',
          500: '#f97316',
          600: '#ea580c',
          700: '#c2410c',
          800: '#9a3412',
          900: '#7c2d12',
        },
        // Keep brand for backward compatibility
        brand: oceanBluePalette,
        'brand-deep': '#0c4a6e',
        'brand-muted': '#64748b',
        'brand-surface': '#f0f9ff',
      },
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', ...defaultTheme.fontFamily.sans],
        display: ['"Space Grotesk"', ...defaultTheme.fontFamily.sans],
      },
      borderRadius: {
        '3xl': '1.75rem',
        '4xl': '2.5rem',
      },
      boxShadow: {
        'student-card': '0 30px 60px rgba(6, 182, 212, 0.12)',
        'ocean-glow': '0 10px 40px rgba(6, 182, 212, 0.3)',
        'ocean-glow-lg': '0 20px 60px rgba(6, 182, 212, 0.4)',
        'teal-glow': '0 10px 40px rgba(20, 184, 166, 0.3)',
        'inner-glow': 'inset 0 2px 8px rgba(6, 182, 212, 0.15)',
        // Dark mode shadows
        'dark-card': '0 10px 40px rgba(0, 0, 0, 0.5)',
        'dark-ocean': '0 0 30px rgba(12, 74, 110, 0.4)',
        'dark-glow': '0 0 20px rgba(6, 182, 212, 0.3)',
      },
      backgroundImage: {
        'student-grid':
          'radial-gradient(circle at 1px 1px, rgba(6,182,212,0.08) 1px, transparent 0)',
        // Ocean Blue gradient themes
        'gradient-primary': 'linear-gradient(135deg, #06b6d4 0%, #0891b2 50%, #14b8a6 100%)',
        'gradient-primary-hover': 'linear-gradient(135deg, #0891b2 0%, #0e7490 50%, #0d9488 100%)',
        'gradient-secondary': 'linear-gradient(135deg, #14b8a6 0%, #0d9488 100%)',
        'gradient-accent': 'linear-gradient(135deg, #06b6d4 0%, #22d3ee 100%)',
        // Ocean wave gradient
        'gradient-ocean': 'linear-gradient(120deg, #06b6d4 0%, #0891b2 25%, #0e7490 50%, #14b8a6 75%, #0d9488 100%)',
        'gradient-ocean-hover': 'linear-gradient(120deg, #0891b2 0%, #0e7490 25%, #155e75 50%, #0d9488 75%, #0f766e 100%)',
        // Dark mode gradients
        'gradient-dark': 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)',
        'gradient-dark-ocean': 'linear-gradient(135deg, #0c4a6e 0%, #075985 50%, #134e4a 100%)',
        // Animated ocean waves
        'ocean-waves': 'linear-gradient(90deg, #06b6d4 0%, #0891b2 25%, #14b8a6 50%, #0891b2 75%, #06b6d4 100%)',
        // Mesh gradients for backgrounds
        'mesh-light': 'radial-gradient(at 0% 0%, rgba(6,182,212,0.3) 0px, transparent 50%), radial-gradient(at 100% 0%, rgba(8,145,178,0.25) 0px, transparent 50%), radial-gradient(at 100% 100%, rgba(20,184,166,0.2) 0px, transparent 50%), radial-gradient(at 0% 100%, rgba(6,182,212,0.15) 0px, transparent 50%)',
        'mesh-dark': 'radial-gradient(at 0% 0%, rgba(12,74,110,0.4) 0px, transparent 50%), radial-gradient(at 100% 0%, rgba(7,89,133,0.35) 0px, transparent 50%), radial-gradient(at 100% 100%, rgba(19,78,74,0.3) 0px, transparent 50%), radial-gradient(at 0% 100%, rgba(12,74,110,0.25) 0px, transparent 50%)',
      },
      container: {
        center: true,
        padding: {
          DEFAULT: '1.25rem',
          sm: '1.5rem',
          lg: '2rem',
        },
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0) scale(1)' },
          '50%': { transform: 'translateY(-5px) scale(1.05)' },
        },
        'gradient-x': {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
        'ripple-out': {
          '0%': { transform: 'scale(0)', opacity: '1' },
          '100%': { transform: 'scale(2.5)', opacity: '0' },
        },
        'ping-animation': {
          '75%, 100%': { transform: 'scale(2.5)', opacity: '0' },
        },
        'gradient-rotate': {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
        'pulse-animation': {
          '0%, 100%': { transform: 'scale(1)', opacity: '0.8' },
          '50%': { transform: 'scale(2)', opacity: '0' },
        },
        'slide-down': {
          from: { opacity: '0', transform: 'translateY(-20px)' },
          to: { opacity: '1', transform: 'translateY(0)' },
        },
        'fade-in': {
          from: { opacity: '0' },
          to: { opacity: '1' },
        },
        'scale-in': {
          from: { opacity: '0', transform: 'scale(0.95)' },
          to: { opacity: '1', transform: 'scale(1)' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        glow: {
          '0%, 100%': { opacity: '1', filter: 'brightness(1)' },
          '50%': { opacity: '0.8', filter: 'brightness(1.2)' },
        },
        wave: {
          '0%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
          '100%': { backgroundPosition: '0% 50%' },
        },
        'wave-slow': {
          '0%, 100%': { transform: 'translateX(0) translateY(0)' },
          '25%': { transform: 'translateX(5px) translateY(-5px)' },
          '50%': { transform: 'translateX(0) translateY(-10px)' },
          '75%': { transform: 'translateX(-5px) translateY(-5px)' },
        },
        'ocean-flow': {
          '0%': { backgroundPosition: '0% 0%' },
          '50%': { backgroundPosition: '100% 100%' },
          '100%': { backgroundPosition: '0% 0%' },
        },
      },
      animation: {
        float: 'float 3s ease-in-out infinite',
        'gradient-x': 'gradient-x 3s ease infinite',
        'ripple-out': 'ripple-out 0.8s cubic-bezier(0.34, 1.56, 0.64, 1)',
        'ping-custom': 'ping-animation 1.5s cubic-bezier(0, 0, 0.2, 1) infinite',
        'gradient-rotate': 'gradient-rotate 3s ease infinite',
        'pulse-custom': 'pulse-animation 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'slide-down': 'slide-down 0.3s ease-out',
        'fade-in': 'fade-in 0.4s ease-out',
        'scale-in': 'scale-in 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)',
        shimmer: 'shimmer 2s linear infinite',
        glow: 'glow 2s ease-in-out infinite',
        wave: 'wave 8s ease-in-out infinite',
        'wave-slow': 'wave-slow 6s ease-in-out infinite',
        'ocean-flow': 'ocean-flow 15s ease-in-out infinite',
      },
      // Transition utilities
      transitionDuration: {
        400: '400ms',
      },
      transitionTimingFunction: {
        'bounce-in': 'cubic-bezier(0.34, 1.56, 0.64, 1)',
      },
    },
  },
  plugins: [],
}
