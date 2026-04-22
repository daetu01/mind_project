<template>
  <section id="raid-matcher" class="py-24 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto">

      <!-- Section header -->
      <div class="text-center mb-16">
        <div class="inline-block text-xs font-semibold tracking-widest text-steel uppercase mb-4">Features</div>
        <h2 class="text-4xl font-bold tracking-tight text-silver mb-4">Raid Matcher</h2>
        <p class="text-lg text-steel">조용하지만 강력한 팀원들을 만나보세요.</p>
      </div>

      <!-- Bento Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

        <!-- Feature Card 1 — 소음 없는 매칭 -->
        <div class="group rounded-[2rem] p-10 border border-rim/50 flex flex-col h-full
                    transition-all duration-500 ease-out hover:-translate-y-1"
             style="background: rgba(15,15,26,0.7); backdrop-filter: blur(12px);
                    box-shadow: 0 1px 0 rgba(255,255,255,0.04) inset;">
          <div class="h-12 w-12 rounded-2xl flex items-center justify-center mb-6 transition-transform duration-500 group-hover:scale-110"
               style="background: rgba(163,53,238,0.12)">
            <svg class="w-6 h-6 text-wow-epic" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round"
                    d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-silver mb-3">소음 없는 매칭</h3>
          <p class="text-steel flex-grow leading-relaxed text-sm">
            디스코드 마이크 필수? 아닙니다. 브리핑은 텍스트로, 실력은 로그로 증명하세요.
          </p>
          <div class="mt-6 pt-6 border-t border-rim/30">
            <span class="inline-flex items-center gap-1.5 text-xs font-medium text-wow-epic">
              <span class="w-1.5 h-1.5 rounded-full bg-wow-epic"></span>
              Epic Feature
            </span>
          </div>
        </div>

        <!-- Feature Card 2 — 검증된 로그 -->
        <div class="group rounded-[2rem] p-10 border border-rim/50 flex flex-col h-full
                    transition-all duration-500 ease-out hover:-translate-y-1"
             style="background: rgba(15,15,26,0.7); backdrop-filter: blur(12px);
                    box-shadow: 0 1px 0 rgba(255,255,255,0.04) inset;">
          <div class="h-12 w-12 rounded-2xl flex items-center justify-center mb-6 transition-transform duration-500 group-hover:scale-110"
               style="background: rgba(0,112,221,0.12)">
            <svg class="w-6 h-6 text-wow-rare" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round"
                    d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-silver mb-3">검증된 로그</h3>
          <p class="text-steel flex-grow leading-relaxed text-sm">
            Warcraft Logs API와 연동하여 정확한 퍼포먼스 데이터를 기반으로 팀을 구성합니다.
          </p>
          <div class="mt-6 pt-6 border-t border-rim/30">
            <span class="inline-flex items-center gap-1.5 text-xs font-medium text-wow-rare">
              <span class="w-1.5 h-1.5 rounded-full bg-wow-rare"></span>
              Rare Feature
            </span>
          </div>
        </div>

        <!-- CTA Card — 지금 시작하기 (gradient border) -->
        <div class="rounded-[2rem] p-[1px] md:col-span-2 lg:col-span-1"
             style="background: linear-gradient(135deg, rgba(255,128,0,0.4), rgba(163,53,238,0.4), rgba(0,112,221,0.3))">
          <div class="group rounded-[1.9rem] p-10 flex flex-col h-full justify-center items-center text-center
                      transition-all duration-500 ease-out"
               style="background: rgba(15,15,26,0.95); backdrop-filter: blur(12px)">

            <!-- Legendary icon -->
            <div class="h-16 w-16 rounded-2xl flex items-center justify-center mb-6"
                 style="background: linear-gradient(135deg, rgba(255,128,0,0.15), rgba(163,53,238,0.15))">
              <svg class="w-8 h-8" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <defs>
                  <linearGradient id="ctaIconGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#ff8000"/>
                    <stop offset="100%" stop-color="#a335ee"/>
                  </linearGradient>
                </defs>
                <path stroke="url(#ctaIconGrad)" stroke-linecap="round" stroke-linejoin="round"
                      d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>

            <h3 class="text-2xl font-semibold text-silver mb-3">지금 시작하기</h3>
            <p class="text-steel mb-8 max-w-xs leading-relaxed text-sm">
              배틀넷 계정을 연동하고 당신에게 맞는 공격대를 찾아보세요.
            </p>

            <RouterLink to="/matching"
              class="w-full flex items-center justify-center gap-3 py-4 px-6 rounded-full font-semibold text-sm
                     text-white transition-all duration-300 hover:-translate-y-0.5"
              style="background: linear-gradient(90deg, #ff8000, #a335ee); box-shadow: 0 8px 24px rgba(163,53,238,0.25)">
              <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="currentColor">
                <path fill-rule="evenodd" clip-rule="evenodd"
                  d="M11.5 0C5.148 0 0 5.148 0 11.5C0 17.852 5.148 23 11.5 23C17.852 23 23 17.852 23 11.5C23 5.148 17.852 0 11.5 0ZM15.42 16.962C12.983 18.293 10.017 18.293 7.58 16.962L11.5 10.183L15.42 16.962ZM11.5 2.5C13.434 2.5 15.228 3.109 16.711 4.148L11.5 13.166L6.289 4.148C7.772 3.109 9.566 2.5 11.5 2.5ZM3.812 6.845L9.023 15.863L5.053 22.75C3.178 20.25 2.222 17.022 2.527 13.753C2.83 10.468 4.382 7.491 6.845 5.513L3.812 6.845Z"/>
              </svg>
              <span>매칭 시작하기</span>
            </RouterLink>
          </div>
        </div>

      </div>
    </div>
  </section>
</template>

<script setup>
</script>
