<template>
  <footer class="border-t border-rim/30 py-14 px-4 sm:px-6 lg:px-8 relative z-10">
    <div class="max-w-7xl mx-auto">

      <div class="grid grid-cols-1 md:grid-cols-3 gap-10 mb-12">

        <!-- Brand -->
        <div>
          <div class="flex items-center gap-2.5 mb-4">
            <div class="w-7 h-7 rounded-lg flex items-center justify-center shadow-lg"
                 style="background: linear-gradient(135deg, #a335ee, #ff8000aa)">
              <svg class="w-3.5 h-3.5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round"
                      d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
              </svg>
            </div>
            <span class="text-silver font-semibold text-base tracking-tight">daiswhat</span>
          </div>
          <p class="text-steel text-sm leading-relaxed max-w-xs">
            소극적인 당신을 위한<br/>가장 조용한 공격대 매칭 서비스.
          </p>
        </div>

        <!-- Navigation -->
        <div>
          <h4 class="text-xs font-semibold tracking-widest text-iron uppercase mb-5">Navigation</h4>
          <ul class="space-y-3">
            <li>
              <RouterLink to="/raid-rankings"
                class="text-steel hover:text-silver text-sm transition-colors duration-200">
                Rankings
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/queue"
                class="text-steel hover:text-silver text-sm transition-colors duration-200">
                대기열
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/lfg"
                class="text-steel hover:text-silver text-sm transition-colors duration-200">
                공대 모집
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/matching"
                class="text-steel hover:text-silver text-sm transition-colors duration-200">
                Matching
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/profile"
                class="text-steel hover:text-silver text-sm transition-colors duration-200">
                프로필
              </RouterLink>
            </li>
          </ul>
        </div>

        <!-- External -->
        <div>
          <h4 class="text-xs font-semibold tracking-widest text-iron uppercase mb-5">Links</h4>
          <ul class="space-y-3">
            <li>
              <a href="https://develop.battle.net" target="_blank" rel="noopener"
                 class="text-steel hover:text-silver text-sm transition-colors duration-200 flex items-center gap-1.5 group">
                Battle.net API
                <svg class="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                </svg>
              </a>
            </li>
            <li>
              <a href="https://www.warcraftlogs.com" target="_blank" rel="noopener"
                 class="text-steel hover:text-silver text-sm transition-colors duration-200 flex items-center gap-1.5 group">
                Warcraft Logs
                <svg class="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                </svg>
              </a>
            </li>
            <li>
              <a href="https://raider.io" target="_blank" rel="noopener"
                 class="text-steel hover:text-silver text-sm transition-colors duration-200 flex items-center gap-1.5 group">
                Raider.IO
                <svg class="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                </svg>
              </a>
            </li>
          </ul>
        </div>

      </div>

      <!-- Bottom bar -->
      <div class="pt-8 border-t border-rim/30 flex flex-col sm:flex-row justify-between items-center gap-4">
        <p class="text-iron text-xs tracking-wide">
          © 2026 daiswhat · Not affiliated with Blizzard Entertainment.
        </p>
        <div class="flex items-center gap-2">
          <span class="relative flex h-1.5 w-1.5">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-wow-uncommon opacity-60"></span>
            <span class="relative inline-flex rounded-full h-1.5 w-1.5 bg-wow-uncommon"></span>
          </span>
          <span class="text-iron text-xs">Servers online · WSL2</span>
        </div>
      </div>

    </div>
  </footer>
</template>

<script setup>
</script>
