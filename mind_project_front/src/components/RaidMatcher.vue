<template>
  <section id="raid-matcher" class="py-24 px-4 sm:px-6 lg:px-8 bg-apple-gray">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-16">
        <h2 class="text-4xl font-bold tracking-tight text-apple-black mb-4">Raid Matcher</h2>
        <p class="text-lg text-apple-secondary">조용하지만 강력한 팀원들을 만나보세요.</p>
      </div>

      <!-- Bento Grid Layout -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <!-- Feature Card 1 -->
        <div class="group bg-white rounded-[2rem] p-10 shadow-sm hover:shadow-2xl transition-all duration-500 ease-in-out border border-gray-100 flex flex-col h-full transform hover:-translate-y-1">
          <div class="h-12 w-12 bg-purple-50 rounded-2xl flex items-center justify-center mb-6 text-wow-purple group-hover:scale-110 transition-transform duration-500">
            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          </div>
          <h3 class="text-2xl font-semibold text-apple-black mb-3">소음 없는 매칭</h3>
          <p class="text-apple-secondary flex-grow leading-relaxed">디스코드 마이크 필수? 아닙니다. 브리핑은 텍스트로, 실력은 로그로 증명하세요.</p>
        </div>

        <!-- Feature Card 2 -->
        <div class="group bg-white rounded-[2rem] p-10 shadow-sm hover:shadow-2xl transition-all duration-500 ease-in-out border border-gray-100 flex flex-col h-full transform hover:-translate-y-1">
          <div class="h-12 w-12 bg-purple-50 rounded-2xl flex items-center justify-center mb-6 text-wow-purple group-hover:scale-110 transition-transform duration-500">
            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <h3 class="text-2xl font-semibold text-apple-black mb-3">검증된 로그</h3>
          <p class="text-apple-secondary flex-grow leading-relaxed">Warcraft Logs API와 연동하여 정확한 퍼포먼스 데이터를 기반으로 팀을 구성합니다.</p>
        </div>

        <!-- Login Card -->
        <div class="group bg-apple-black rounded-[2rem] p-10 shadow-lg hover:shadow-2xl transition-all duration-500 ease-in-out flex flex-col h-full justify-center items-center text-center transform hover:-translate-y-1 md:col-span-2 lg:col-span-1">
          <h3 class="text-2xl font-semibold text-white mb-3">지금 시작하기</h3>
          <p class="text-gray-400 mb-8 max-w-xs leading-relaxed">배틀넷 계정을 연동하고 당신에게 맞는 공격대를 찾아보세요.</p>
          
          <RouterLink to="/matching" class="w-full flex items-center justify-center space-x-3 bg-white hover:bg-gray-100 text-apple-black font-semibold py-4 px-6 rounded-full transition-colors duration-300">
            <!-- Simplified Battle.net Logo placeholder -->
            <svg class="w-6 h-6 text-blue-500" viewBox="0 0 24 24" fill="currentColor">
              <path d="M11.5 0C5.148 0 0 5.148 0 11.5C0 17.852 5.148 23 11.5 23C17.852 23 23 17.852 23 11.5C23 5.148 17.852 0 11.5 0ZM15.42 16.962C12.983 18.293 10.017 18.293 7.58 16.962L11.5 10.183L15.42 16.962ZM11.5 2.5C13.434 2.5 15.228 3.109 16.711 4.148L11.5 13.166L6.289 4.148C7.772 3.109 9.566 2.5 11.5 2.5ZM3.812 6.845L9.023 15.863L5.053 22.75C3.178 20.25 2.222 17.022 2.527 13.753C2.83 10.468 4.382 7.491 6.845 5.513L3.812 6.845Z" fill-rule="evenodd" clip-rule="evenodd"/>
            </svg>
            <span>매칭 시작하기</span>
          </RouterLink>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
</script>
