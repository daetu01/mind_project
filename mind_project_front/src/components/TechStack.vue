<template>
  <section id="console" class="py-24 px-4 sm:px-6 lg:px-8 bg-white border-t border-gray-100">
    <div class="max-w-4xl mx-auto text-center">
      <h2 class="text-xs font-semibold tracking-widest text-apple-secondary uppercase mb-12">Powered by Modern Infrastructure</h2>
      
      <!-- Tech Logos (Monotone style) -->
      <div class="flex flex-wrap justify-center items-center gap-10 md:gap-16 opacity-60 grayscale hover:grayscale-0 transition-all duration-700">
        <!-- WSL2 Text Logo -->
        <div class="text-2xl font-bold tracking-tighter text-apple-black">WSL2</div>
        <!-- Docker Logo Placeholder -->
        <svg class="h-10 text-apple-black" viewBox="0 0 24 24" fill="currentColor">
          <path d="M13.983 11.078h2.119a.186.186 0 00.186-.185V9.006a.186.186 0 00-.186-.186h-2.119a.185.185 0 00-.185.185v1.888c0 .102.083.185.185.185m-2.95 0h2.118a.186.186 0 00.185-.185V9.006a.185.185 0 00-.185-.186h-2.118a.185.185 0 00-.185.185v1.888c0 .102.082.185.185.185m0-2.816h2.118a.186.186 0 00.185-.186V6.188a.185.185 0 00-.185-.185h-2.118a.185.185 0 00-.185.185v1.888c0 .102.082.186.185.186m-2.95 2.816h2.119a.186.186 0 00.185-.185V9.006a.185.185 0 00-.185-.186h-2.119a.186.186 0 00-.186.185v1.888c0 .102.084.185.186.185m-.001-2.816h2.119a.186.186 0 00.186-.186V6.188a.185.185 0 00-.186-.185h-2.119a.186.186 0 00-.186.185v1.888c0 .102.084.186.186.186m-2.95 2.816h2.119a.186.186 0 00.185-.185V9.006a.185.185 0 00-.185-.186h-2.119a.186.186 0 00-.186.185v1.888c0 .102.084.185.186.185"/>
        </svg>
        <!-- Nginx Text Logo -->
        <div class="text-2xl font-bold tracking-tight text-apple-black">NGINX</div>
        <!-- Spring Text Logo -->
        <div class="text-2xl font-bold tracking-tighter text-apple-black">Spring Boot</div>
      </div>

      <!-- Server Status Dot -->
      <div class="mt-16 flex items-center justify-center space-x-3 bg-apple-gray inline-flex px-6 py-3 rounded-full border border-gray-200">
        <span class="relative flex h-3 w-3">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
          <span class="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
        </span>
        <span class="text-sm font-medium text-apple-black">Live on WSL2 (Personal PC)</span>
      </div>
    </div>
  </section>
</template>

<script setup>
</script>
