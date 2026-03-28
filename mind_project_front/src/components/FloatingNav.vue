<template>
  <nav class="fixed top-0 w-full z-50 backdrop-blur-md bg-white/70 border-b border-gray-100/50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-14">
        <!-- Logo / Brand -->
        <div class="flex-shrink-0 flex items-center">
          <RouterLink to="/" class="text-apple-black font-semibold text-lg tracking-tight">daiswhat</RouterLink>
        </div>
        <!-- Navigation Links -->
        <div class="hidden md:flex space-x-8">
          <RouterLink :to="{ path: '/', hash: '#raid-matcher' }" class="text-apple-black hover:text-wow-purple text-xs font-medium tracking-wide transition-colors duration-300">Raid Matcher</RouterLink>
          <RouterLink to="/raid-rankings" class="text-apple-black hover:text-wow-purple text-xs font-medium tracking-wide transition-colors duration-300">Raid Rankings</RouterLink>
          <RouterLink to="/matching" class="text-apple-black hover:text-wow-purple text-xs font-medium tracking-wide transition-colors duration-300">Matching</RouterLink>
          <RouterLink :to="{ path: '/', hash: '#console' }" class="text-apple-black hover:text-wow-purple text-xs font-medium tracking-wide transition-colors duration-300">Console(Server Status)</RouterLink>
        </div>
        <!-- Mobile menu button placeholders (optional) -->
        <div class="md:hidden flex items-center">
          <button class="text-apple-black">
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
// Component logic if required
</script>
