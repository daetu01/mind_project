<template>
  <section class="pt-32 pb-24 px-4 sm:px-6 lg:px-8 text-center min-h-[78vh] flex flex-col justify-center items-center relative">

    <!-- Local ambient glow -->
    <div class="absolute inset-0 pointer-events-none overflow-hidden" aria-hidden="true">
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[500px] rounded-full blur-[140px]"
           style="background: radial-gradient(ellipse, rgba(163,53,238,0.09) 0%, transparent 70%)"></div>
    </div>

    <div class="max-w-4xl mx-auto relative z-10">

      <!-- Epic status badge -->
      <div class="inline-flex items-center gap-2.5 px-4 py-2 rounded-full border border-rim/60 mb-10 text-xs font-medium text-steel tracking-wider uppercase"
           style="background: var(--bg-card)">
        <span class="relative flex h-2 w-2">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-wow-epic opacity-60"></span>
          <span class="relative inline-flex rounded-full h-2 w-2 bg-wow-epic"></span>
        </span>
        World of Warcraft · Raid Matching
      </div>

      <!-- Main heading -->
      <h1 class="text-5xl md:text-7xl lg:text-8xl font-bold tracking-tighter text-silver mb-6 leading-none">
        Less Talking,<br />
        <span class="text-transparent bg-clip-text"
              style="background-image: linear-gradient(90deg, #ff8000, #a335ee, #0070dd)">
          More Raiding.
        </span>
      </h1>

      <!-- Sub text -->
      <p class="text-xl md:text-2xl text-steel font-medium tracking-tight mb-12 max-w-2xl mx-auto leading-relaxed">
        소극적인 당신을 위한<br class="md:hidden" /> 가장 조용한 공격대 매칭 서비스.
      </p>

      <!-- CTAs -->
      <div class="flex flex-col sm:flex-row justify-center items-center gap-4">
        <RouterLink to="/matching"
          class="group flex items-center gap-2.5 px-7 py-3.5 rounded-full text-white font-semibold text-base transition-all duration-300 hover:-translate-y-0.5"
          style="background: #a335ee; box-shadow: 0 8px 32px rgba(163,53,238,0.3)">
          매칭 시작하기
          <svg class="w-4 h-4 transform group-hover:translate-x-1 transition-transform duration-300"
               fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
          </svg>
        </RouterLink>

        <a href="#raid-matcher"
           class="group flex items-center gap-2 px-7 py-3.5 rounded-full border border-rim/60 text-steel hover:text-silver hover:border-rim transition-all duration-300 text-base font-medium">
          더 알아보기
          <svg class="w-4 h-4 transform group-hover:translate-y-1 transition-transform duration-300"
               fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
          </svg>
        </a>
      </div>
    </div>
  </section>
</template>

<script setup>
</script>
