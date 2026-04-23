<template>
  <section id="console" class="py-24 px-4 sm:px-6 lg:px-8 border-t border-rim/30">
    <div class="max-w-4xl mx-auto text-center">

      <div class="text-xs font-semibold tracking-widest text-iron uppercase mb-12">
        Powered by Modern Infrastructure
      </div>

      <!-- Tech logos -->
      <div class="flex flex-wrap justify-center items-center gap-10 md:gap-16 opacity-40 grayscale hover:opacity-70 hover:grayscale-0 transition-all duration-700">
        <div class="text-2xl font-bold tracking-tighter text-silver">WSL2</div>

        <svg class="h-10 text-silver" viewBox="0 0 24 24" fill="currentColor">
          <path d="M13.983 11.078h2.119a.186.186 0 00.186-.185V9.006a.186.186 0 00-.186-.186h-2.119a.185.185 0 00-.185.185v1.888c0 .102.083.185.185.185m-2.95 0h2.118a.186.186 0 00.185-.185V9.006a.185.185 0 00-.185-.186h-2.118a.185.185 0 00-.185.185v1.888c0 .102.082.185.185.185m0-2.816h2.118a.186.186 0 00.185-.186V6.188a.185.185 0 00-.185-.185h-2.118a.185.185 0 00-.185.185v1.888c0 .102.082.186.185.186m-2.95 2.816h2.119a.186.186 0 00.185-.185V9.006a.185.185 0 00-.185-.186h-2.119a.186.186 0 00-.186.185v1.888c0 .102.084.185.186.185m-.001-2.816h2.119a.186.186 0 00.186-.186V6.188a.185.185 0 00-.186-.185h-2.119a.186.186 0 00-.186.185v1.888c0 .102.084.186.186.186m-2.95 2.816h2.119a.186.186 0 00.185-.185V9.006a.185.185 0 00-.185-.186h-2.119a.186.186 0 00-.186.185v1.888c0 .102.084.185.186.185"/>
        </svg>

        <div class="text-2xl font-bold tracking-tight text-silver">NGINX</div>
        <div class="text-2xl font-bold tracking-tighter text-silver">Spring Boot</div>
      </div>

      <!-- Server status -->
      <div class="mt-16 inline-flex items-center gap-3 px-6 py-3 rounded-full border border-rim/50"
           style="background: var(--bg-card)">
        <span class="relative flex h-2.5 w-2.5">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-wow-uncommon opacity-60"></span>
          <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-wow-uncommon"></span>
        </span>
        <span class="text-sm font-medium text-steel">Live on WSL2 (Personal PC)</span>
      </div>

    </div>
  </section>
</template>

<script setup>
</script>
