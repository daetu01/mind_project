<template>
  <nav class="fixed top-0 w-full z-50 backdrop-blur-xl border-b border-rim/40"
       :style="navBg">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-14">

        <!-- Logo -->
        <div class="flex-shrink-0 flex items-center gap-2.5">
          <div class="w-7 h-7 rounded-lg flex items-center justify-center shadow-lg"
               style="background: linear-gradient(135deg, #a335ee, #ff8000aa)">
            <svg class="w-3.5 h-3.5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round"
                    d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
          </div>
          <RouterLink to="/" class="text-silver font-semibold text-base tracking-tight" @click="menuOpen = false">
            daiswhat
          </RouterLink>
        </div>

        <!-- Desktop nav -->
        <div class="hidden md:flex items-center space-x-5">
          <RouterLink to="/raid-rankings"
            :class="['text-xs font-medium tracking-wide transition-colors duration-300',
              route.path === '/raid-rankings'
                ? 'text-wow-epic border-b border-wow-epic/50 pb-px'
                : 'text-steel hover:text-wow-epic']">
            Rankings
          </RouterLink>
          <RouterLink to="/queue"
            :class="['flex items-center gap-1.5 text-xs font-medium tracking-wide transition-colors duration-300',
              route.path === '/queue'
                ? 'text-wow-epic border-b border-wow-epic/50 pb-px'
                : 'text-steel hover:text-wow-epic']">
            <span class="relative flex h-1.5 w-1.5">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-wow-uncommon opacity-60"></span>
              <span class="relative inline-flex rounded-full h-1.5 w-1.5 bg-wow-uncommon"></span>
            </span>
            대기열
          </RouterLink>
          <RouterLink to="/lfg"
            :class="['text-xs font-medium tracking-wide transition-colors duration-300',
              route.path === '/lfg'
                ? 'text-wow-epic border-b border-wow-epic/50 pb-px'
                : 'text-steel hover:text-wow-epic']">
            공대 모집
          </RouterLink>
          <RouterLink to="/matching"
            :class="['text-xs font-medium tracking-wide transition-colors duration-300',
              route.path === '/matching'
                ? 'text-wow-epic border-b border-wow-epic/50 pb-px'
                : 'text-steel hover:text-wow-epic']">
            Matching
          </RouterLink>
          <RouterLink to="/profile"
            :class="['flex items-center gap-1.5 h-8 px-4 rounded-full border text-xs font-semibold transition-all duration-300',
              route.path === '/profile'
                ? 'text-wow-epic border-wow-epic/50'
                : 'text-steel hover:text-silver border-rim/60 hover:border-rim']"
            :style="route.path === '/profile'
              ? 'background: rgba(163,53,238,0.1)'
              : profileBtnBg">
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
            </svg>
            프로필
          </RouterLink>

          <!-- Theme toggle -->
          <button
            @click="themeStore.toggle()"
            class="w-8 h-8 flex items-center justify-center rounded-full border border-rim/60 text-steel hover:text-silver hover:border-rim transition-all duration-300"
            :style="profileBtnBg"
            :aria-label="themeStore.isDark ? '라이트 모드로 전환' : '다크 모드로 전환'">
            <svg v-if="themeStore.isDark" class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="5"/>
              <line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/>
              <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
              <line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/>
              <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
            </svg>
            <svg v-else class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/>
            </svg>
          </button>
        </div>

        <!-- Mobile right buttons -->
        <div class="md:hidden flex items-center gap-1">
          <!-- Mobile theme toggle -->
          <button
            @click="themeStore.toggle()"
            class="w-9 h-9 flex items-center justify-center rounded-full text-steel hover:text-silver transition-colors"
            :aria-label="themeStore.isDark ? '라이트 모드로 전환' : '다크 모드로 전환'">
            <svg v-if="themeStore.isDark" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="5"/>
              <line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/>
              <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
              <line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/>
              <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
            </svg>
            <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/>
            </svg>
          </button>

          <!-- Hamburger / X toggle -->
          <button
            @click="menuOpen = !menuOpen"
            class="w-9 h-9 flex items-center justify-center rounded-full text-steel hover:text-silver transition-colors"
            :aria-label="menuOpen ? '메뉴 닫기' : '메뉴 열기'"
            :aria-expanded="menuOpen">
            <!-- Hamburger -->
            <svg v-if="!menuOpen" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"/>
            </svg>
            <!-- X -->
            <svg v-else class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

      </div>
    </div>
  </nav>

  <!-- Mobile menu panel -->
  <Teleport to="body">
    <Transition
      enter-active-class="transition-all duration-200 ease-out"
      enter-from-class="opacity-0 -translate-y-2"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition-all duration-150 ease-in"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 -translate-y-2">
      <div
        v-if="menuOpen"
        class="fixed top-14 inset-x-0 z-40 md:hidden border-b border-rim/40 backdrop-blur-xl"
        :style="navBg">
        <nav class="max-w-7xl mx-auto px-4 py-3 flex flex-col gap-1">

          <RouterLink to="/raid-rankings" @click="menuOpen = false"
            class="flex items-center gap-3 h-12 px-4 rounded-2xl text-sm font-medium transition-colors duration-200"
            :class="route.path === '/raid-rankings'
              ? 'text-wow-epic bg-wow-epic/10'
              : 'text-steel hover:text-silver hover:bg-white/5'">
            <svg class="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
            </svg>
            Rankings
          </RouterLink>

          <RouterLink to="/queue" @click="menuOpen = false"
            class="flex items-center gap-3 h-12 px-4 rounded-2xl text-sm font-medium transition-colors duration-200"
            :class="route.path === '/queue'
              ? 'text-wow-epic bg-wow-epic/10'
              : 'text-steel hover:text-silver hover:bg-white/5'">
            <span class="relative flex h-4 w-4 flex-shrink-0 items-center justify-center">
              <span class="animate-ping absolute inline-flex h-2 w-2 rounded-full bg-wow-uncommon opacity-60"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-wow-uncommon"></span>
            </span>
            대기열
          </RouterLink>

          <RouterLink to="/lfg" @click="menuOpen = false"
            class="flex items-center gap-3 h-12 px-4 rounded-2xl text-sm font-medium transition-colors duration-200"
            :class="route.path === '/lfg'
              ? 'text-wow-epic bg-wow-epic/10'
              : 'text-steel hover:text-silver hover:bg-white/5'">
            <svg class="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
            공대 모집
          </RouterLink>

          <RouterLink to="/matching" @click="menuOpen = false"
            class="flex items-center gap-3 h-12 px-4 rounded-2xl text-sm font-medium transition-colors duration-200"
            :class="route.path === '/matching'
              ? 'text-wow-epic bg-wow-epic/10'
              : 'text-steel hover:text-silver hover:bg-white/5'">
            <svg class="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z"/>
            </svg>
            Matching
          </RouterLink>

          <div class="h-px bg-rim/30 my-1"></div>

          <RouterLink to="/profile" @click="menuOpen = false"
            class="flex items-center gap-3 h-12 px-4 rounded-2xl text-sm font-semibold transition-colors duration-200"
            :class="route.path === '/profile'
              ? 'text-wow-epic bg-wow-epic/10'
              : 'text-steel hover:text-silver hover:bg-white/5'">
            <svg class="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
            </svg>
            프로필
          </RouterLink>

        </nav>
      </div>
    </Transition>

    <!-- Backdrop -->
    <Transition
      enter-active-class="transition-opacity duration-200"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-150"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0">
      <div
        v-if="menuOpen"
        class="fixed inset-0 top-14 z-30 md:hidden bg-black/20"
        @click="menuOpen = false">
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useThemeStore } from '../stores/theme'

const route = useRoute()
const themeStore = useThemeStore()
const menuOpen = ref(false)

watch(() => route.path, () => { menuOpen.value = false })

const navBg = computed(() =>
  themeStore.isDark
    ? 'background: rgba(8,8,16,0.78)'
    : 'background: rgba(248,248,252,0.85)'
)

const profileBtnBg = computed(() =>
  themeStore.isDark
    ? 'background: rgba(22,22,42,0.8)'
    : 'background: rgba(235,235,242,0.8)'
)
</script>
