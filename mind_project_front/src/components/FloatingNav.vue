<template>
  <nav class="fixed top-0 w-full z-50 backdrop-blur-xl border-b border-rim/40"
       style="background: rgba(8,8,16,0.78)">
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
          <RouterLink to="/" class="text-silver font-semibold text-base tracking-tight">daiswhat</RouterLink>
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
              : 'background: rgba(22,22,42,0.8)'">
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
            </svg>
            프로필
          </RouterLink>
        </div>

        <!-- Mobile menu button -->
        <div class="md:hidden flex items-center">
          <button class="text-steel hover:text-silver transition-colors">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useRoute } from 'vue-router'
const route = useRoute()
</script>
