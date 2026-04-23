<script setup>
import FloatingNav from './components/FloatingNav.vue'
import AppFooter from './components/AppFooter.vue'
import { RouterView } from 'vue-router'
import { watch, onMounted, computed } from 'vue'
import { useThemeStore } from './stores/theme'

const themeStore = useThemeStore()

function applyTheme(isDark) {
  if (isDark) {
    document.documentElement.classList.remove('light')
  } else {
    document.documentElement.classList.add('light')
  }
}

watch(() => themeStore.isDark, applyTheme)
onMounted(() => applyTheme(themeStore.isDark))

const glowOpacity = computed(() => themeStore.isDark ? 1 : 0.4)
</script>

<template>
  <div class="min-h-screen bg-night font-sans text-silver selection:bg-wow-epic selection:text-white relative overflow-hidden">
    <!-- Ambient background glows (fixed, purely decorative) -->
    <div class="fixed inset-0 pointer-events-none" aria-hidden="true">
      <div class="absolute top-0 left-1/2 -translate-x-1/2 w-[900px] h-[600px] rounded-full blur-[160px]"
           :style="`background: radial-gradient(ellipse, rgba(163,53,238,${0.06 * glowOpacity}) 0%, transparent 70%)`"></div>
      <div class="absolute bottom-0 right-0 w-[600px] h-[450px] rounded-full blur-[130px]"
           :style="`background: radial-gradient(ellipse, rgba(255,128,0,${0.04 * glowOpacity}) 0%, transparent 70%)`"></div>
      <div class="absolute top-1/2 left-0 w-[400px] h-[300px] rounded-full blur-[100px]"
           :style="`background: radial-gradient(ellipse, rgba(0,112,221,${0.03 * glowOpacity}) 0%, transparent 70%)`"></div>
    </div>

    <FloatingNav />
    <main class="pt-14 relative z-10">
      <RouterView />
    </main>
    <AppFooter />
  </div>
</template>
