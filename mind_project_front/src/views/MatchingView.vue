<script setup>
import { computed, ref } from 'vue'

const raidSize = ref('10')
const role = ref('DPS')
const voice = ref('no')
const region = ref('KR')

const canStart = computed(() => {
  return Boolean(raidSize.value && role.value && voice.value && region.value)
})

function startMatching() {
  if (!canStart.value) return
  alert(`매칭 시작: 레이드 ${raidSize.value} / 역할 ${role.value} / 음성 ${voice.value} / 지역 ${region.value}`)
}
</script>

<template>
  <section class="px-4 sm:px-6 lg:px-8 py-14">
    <div class="max-w-4xl mx-auto">
      <div class="flex items-start justify-between gap-6">
        <div>
          <h1 class="text-4xl md:text-5xl font-bold tracking-tighter text-apple-black">Matching</h1>
          <p class="mt-2 text-apple-secondary text-base md:text-lg">조건을 선택하고 버튼 한 번으로 파티를 찾아요.</p>
        </div>
        <RouterLink
          to="/raid-rankings"
          class="hidden sm:inline-flex items-center justify-center h-11 px-5 rounded-full bg-white/80 backdrop-blur border border-gray-200 text-sm font-semibold text-apple-black shadow-sm hover:bg-white transition-colors"
        >
          순위표 보기
        </RouterLink>
      </div>

      <div class="mt-8 rounded-[2rem] bg-white/70 backdrop-blur border border-gray-200 shadow-sm overflow-hidden">
        <div class="px-8 py-7 border-b border-gray-100/80">
          <div class="text-sm font-semibold text-apple-black">매칭 옵션</div>
          <div class="mt-1 text-sm text-apple-secondary">추후 Battle.net / WCL 연동 시 프로필 자동 세팅 가능</div>
        </div>

        <div class="px-8 py-8 grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <div class="text-xs font-semibold tracking-widest uppercase text-apple-secondary">Raid Size</div>
            <div class="mt-2 grid grid-cols-3 gap-2">
              <button
                type="button"
                class="h-11 rounded-full border text-sm font-semibold transition-colors"
                :class="raidSize === '10' ? 'bg-apple-black text-white border-apple-black' : 'bg-white/70 border-gray-200 text-apple-black hover:bg-white'"
                @click="raidSize = '10'"
              >
                10
              </button>
              <button
                type="button"
                class="h-11 rounded-full border text-sm font-semibold transition-colors"
                :class="raidSize === '20' ? 'bg-apple-black text-white border-apple-black' : 'bg-white/70 border-gray-200 text-apple-black hover:bg-white'"
                @click="raidSize = '20'"
              >
                20
              </button>
              <button
                type="button"
                class="h-11 rounded-full border text-sm font-semibold transition-colors"
                :class="raidSize === '25' ? 'bg-apple-black text-white border-apple-black' : 'bg-white/70 border-gray-200 text-apple-black hover:bg-white'"
                @click="raidSize = '25'"
              >
                25
              </button>
            </div>
          </div>

          <div>
            <div class="text-xs font-semibold tracking-widest uppercase text-apple-secondary">Role</div>
            <div class="mt-2">
              <select
                v-model="role"
                class="h-11 w-full rounded-full bg-white/80 backdrop-blur border border-gray-200 px-4 text-sm text-apple-black shadow-sm focus:outline-none focus:ring-2 focus:ring-wow-purple/40"
              >
                <option value="DPS">DPS</option>
                <option value="HEAL">HEAL</option>
                <option value="TANK">TANK</option>
              </select>
            </div>
          </div>

          <div>
            <div class="text-xs font-semibold tracking-widest uppercase text-apple-secondary">Voice</div>
            <div class="mt-2">
              <select
                v-model="voice"
                class="h-11 w-full rounded-full bg-white/80 backdrop-blur border border-gray-200 px-4 text-sm text-apple-black shadow-sm focus:outline-none focus:ring-2 focus:ring-wow-purple/40"
              >
                <option value="no">필요 없음</option>
                <option value="optional">선택</option>
                <option value="required">필수</option>
              </select>
            </div>
          </div>

          <div>
            <div class="text-xs font-semibold tracking-widest uppercase text-apple-secondary">Region</div>
            <div class="mt-2">
              <select
                v-model="region"
                class="h-11 w-full rounded-full bg-white/80 backdrop-blur border border-gray-200 px-4 text-sm text-apple-black shadow-sm focus:outline-none focus:ring-2 focus:ring-wow-purple/40"
              >
                <option value="KR">KR</option>
                <option value="US">US</option>
                <option value="EU">EU</option>
              </select>
            </div>
          </div>
        </div>

        <div class="px-8 pb-8">
          <button
            type="button"
            class="w-full h-12 rounded-full font-semibold tracking-tight transition-colors"
            :disabled="!canStart"
            :class="canStart ? 'bg-wow-purple text-white hover:bg-fuchsia-600' : 'bg-gray-200 text-gray-500 cursor-not-allowed'"
            @click="startMatching"
          >
            매칭 시작
          </button>
          <div class="mt-3 text-xs text-apple-secondary">
            버튼 클릭 시 현재는 데모 알림만 뜹니다. 다음 단계로 API 붙여서 매칭 생성/조회로 바꾸면 돼요.
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
