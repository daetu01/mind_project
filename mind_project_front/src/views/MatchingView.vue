<script setup>
import { computed, onUnmounted, ref } from 'vue'

/* ── Mode ─────────────────────────────────────────────── */
const mode = ref('raid')   // 'raid' | 'key'

const DUNGEONS = [
  '아라카라', '스레드의 도시', '그림 배톨', '스톤볼트',
  '던브레이커', '티르나 시의 안개', '보랄루스 공성전', '부식 괴멸',
]

/* ── Raid fields ──────────────────────────────────────── */
const raidSize = ref('10')
const role     = ref('DPS')
const voice    = ref('no')
const region   = ref('KR')

/* ── Keystone fields ──────────────────────────────────── */
const dungeon  = ref('아라카라')
const keyLevel = ref(10)
const keyGoal  = ref('any')   // 'timer' | 'clear' | 'any'
const keyRole  = ref('DPS')
const keyRegion = ref('KR')

/* ── Shared ───────────────────────────────────────────── */
const isMatching  = ref(false)
const matchFound  = ref(false)
const matchedData = ref(null)
let matchTimer = null

const CLASS_COLORS = {
  '죽음의 기사': '#C41E3A', '악마사냥꾼': '#A330C9', '드루이드': '#FF7C0A',
  '기원사': '#33937F', '사냥꾼': '#AAD372', '마법사': '#3FC7EB',
  '수도사': '#00FF98', '성기사': '#F48CBA', '사제': '#FFFFFF',
  '도적': '#FFF468', '주술사': '#0070DD', '흑마법사': '#8788EE', '전사': '#C69B3A',
}

const MOCK_RAID_PARTY = [
  { name: '어둠의검사', cls: '죽음의 기사', role: '탱커', ilvl: 642, rio: 2810 },
  { name: '빛의심판자', cls: '성기사', role: '힐러', ilvl: 639, rio: 2340 },
  { name: '폭풍의눈', cls: '마법사', role: 'DPS', ilvl: 645, rio: 3120 },
  { name: '달빛방랑자', cls: '드루이드', role: 'DPS', ilvl: 638, rio: 2650 },
]

const MOCK_KEY_PARTY = [
  { name: '철갑수호자', cls: '전사', role: '탱커', ilvl: 641, rio: 2980 },
  { name: '신성한빛', cls: '성기사', role: '힐러', ilvl: 637, rio: 2540 },
  { name: '번개주술사', cls: '주술사', role: 'DPS', ilvl: 643, rio: 3240 },
  { name: '허공의화살', cls: '사냥꾼', role: 'DPS', ilvl: 640, rio: 3080 },
]

const canStart = computed(() => mode.value === 'raid'
  ? Boolean(raidSize.value && role.value && voice.value && region.value)
  : Boolean(dungeon.value && keyLevel.value && keyRole.value)
)

const roleLabel = computed(() => {
  const r = mode.value === 'raid' ? role.value : keyRole.value
  return { DPS: 'DPS', HEAL: '힐러', TANK: '탱커' }[r] ?? r
})

function rioColor(score) {
  if (score >= 3000) return '#ff8000'
  if (score >= 2500) return '#a335ee'
  if (score >= 2000) return '#0070dd'
  if (score >= 1000) return '#1eff00'
  return '#9d9d9d'
}

function startMatching() {
  if (!canStart.value || isMatching.value) return
  isMatching.value = true
  matchFound.value = false
  matchedData.value = null
  window.addEventListener('keydown', onEsc)
  matchTimer = setTimeout(onMatchFound, 5000)
}

function onMatchFound() {
  matchedData.value = {
    party: mode.value === 'raid' ? MOCK_RAID_PARTY : MOCK_KEY_PARTY,
    dungeon: dungeon.value,
    keyLevel: keyLevel.value,
    raidSize: raidSize.value,
    mode: mode.value,
  }
  matchFound.value = true
}

function cancelMatching() {
  isMatching.value = false
  matchFound.value = false
  matchedData.value = null
  window.removeEventListener('keydown', onEsc)
  clearTimeout(matchTimer)
}

function joinParty() {
  cancelMatching()
}

function onEsc(e) {
  if (e.key === 'Escape' && !matchFound.value) cancelMatching()
}

onUnmounted(() => {
  window.removeEventListener('keydown', onEsc)
  clearTimeout(matchTimer)
})
</script>

<template>
  <section class="px-4 sm:px-6 lg:px-8 py-14">
    <div class="max-w-4xl mx-auto">

      <!-- Page header -->
      <div class="flex items-start justify-between gap-6 mb-6">
        <div>
          <h1 class="text-4xl md:text-5xl font-bold tracking-tighter text-silver">Matching</h1>
          <p class="mt-2 text-steel text-base md:text-lg">조건을 선택하고 버튼 한 번으로 파티를 찾아요.</p>
        </div>
        <RouterLink
          to="/raid-rankings"
          class="hidden sm:inline-flex items-center justify-center h-11 px-5 rounded-full border border-rim/60
                 text-sm font-semibold text-steel hover:text-silver hover:border-rim transition-all duration-300"
          style="background: var(--bg-button); backdrop-filter: blur(8px)">
          순위표 보기
        </RouterLink>
      </div>

      <!-- Mode tabs -->
      <div class="flex items-center h-12 p-1 rounded-2xl border border-rim/50 mb-6 w-fit"
           style="background: var(--bg-card)">
        <button type="button"
          class="flex items-center gap-2 h-10 px-5 rounded-xl text-sm font-semibold transition-all duration-200"
          :class="mode === 'raid' ? 'text-white' : 'text-steel hover:text-silver'"
          :style="mode === 'raid' ? 'background: #a335ee' : ''"
          @click="mode = 'raid'">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round"
                  d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
          </svg>
          공격대
        </button>
        <button type="button"
          class="flex items-center gap-2 h-10 px-5 rounded-xl text-sm font-semibold transition-all duration-200"
          :class="mode === 'key' ? 'text-white' : 'text-steel hover:text-silver'"
          :style="mode === 'key' ? 'background: #ff8000' : ''"
          @click="mode = 'key'">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round"
                  d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/>
          </svg>
          쐐기
        </button>
      </div>

      <!-- Matching card -->
      <div class="rounded-[2rem] border overflow-hidden transition-all duration-300"
           :style="mode==='raid'
             ? 'background:var(--bg-card-light);backdrop-filter:blur(16px);border-color:var(--bg-dim)'
             : 'background:var(--bg-card-light);backdrop-filter:blur(16px);border-color:rgba(255,128,0,0.2)'">

        <!-- Card header -->
        <div class="px-8 py-6 border-b border-rim/40 flex items-center justify-between">
          <div>
            <div class="text-sm font-semibold text-silver">
              {{ mode === 'raid' ? '공격대 매칭 옵션' : '쐐기 매칭 옵션' }}
            </div>
            <div class="mt-1 text-xs text-steel">추후 Battle.net / RIO 연동 시 프로필 자동 세팅 가능</div>
          </div>
          <span v-if="mode==='key'"
                class="px-3 py-1 rounded-full text-xs font-bold"
                style="background:rgba(255,128,0,0.12);color:#ff8000">
            Mythic+
          </span>
        </div>

        <!-- ── Raid options ── -->
        <div v-if="mode === 'raid'" class="px-8 py-8 grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <div class="text-xs font-semibold tracking-widest uppercase text-steel mb-2">Raid Size</div>
            <div class="grid grid-cols-3 gap-2">
              <button v-for="size in ['10', '20', '25']" :key="size" type="button"
                class="h-11 rounded-full border text-sm font-semibold transition-all duration-200"
                :class="raidSize===size?'border-wow-epic text-white':'border-rim/60 text-steel hover:border-rim hover:text-silver'"
                :style="raidSize===size?'background:#a335ee':'background:var(--bg-button)'"
                @click="raidSize=size">{{ size }}</button>
            </div>
          </div>
          <div>
            <div class="text-xs font-semibold tracking-widest uppercase text-steel mb-2">Role</div>
            <select v-model="role" class="h-11 w-full rounded-full border border-rim/60 px-4 text-sm text-silver focus:outline-none focus:ring-2 focus:ring-wow-epic/40 transition-all duration-200" style="background:var(--bg-input)">
              <option value="DPS">DPS</option><option value="HEAL">HEAL</option><option value="TANK">TANK</option>
            </select>
          </div>
          <div>
            <div class="text-xs font-semibold tracking-widest uppercase text-steel mb-2">Voice</div>
            <select v-model="voice" class="h-11 w-full rounded-full border border-rim/60 px-4 text-sm text-silver focus:outline-none focus:ring-2 focus:ring-wow-epic/40 transition-all duration-200" style="background:var(--bg-input)">
              <option value="no">필요 없음</option><option value="optional">선택</option><option value="required">필수</option>
            </select>
          </div>
          <div>
            <div class="text-xs font-semibold tracking-widest uppercase text-steel mb-2">Region</div>
            <select v-model="region" class="h-11 w-full rounded-full border border-rim/60 px-4 text-sm text-silver focus:outline-none focus:ring-2 focus:ring-wow-epic/40 transition-all duration-200" style="background:var(--bg-input)">
              <option value="KR">KR</option><option value="US">US</option><option value="EU">EU</option>
            </select>
          </div>
        </div>

        <!-- ── Keystone options ── -->
        <div v-else class="px-8 py-8 grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Dungeon -->
          <div class="md:col-span-2">
            <div class="text-xs font-semibold tracking-widest uppercase text-steel mb-2">던전</div>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
              <button v-for="d in DUNGEONS" :key="d" type="button"
                class="h-11 rounded-2xl border text-xs font-semibold transition-all duration-200 px-2 text-center"
                :class="dungeon===d?'text-white':'text-steel hover:text-silver'"
                :style="dungeon===d
                  ?'background:#ff8000;border-color:#ff8000'
                  :'background:var(--bg-button);border-color:var(--border-subtle)'"
                @click="dungeon=d">{{ d }}</button>
            </div>
          </div>

          <!-- Key level -->
          <div>
            <div class="flex items-center justify-between mb-3">
              <div class="text-xs font-semibold tracking-widest uppercase text-steel">키 레벨</div>
              <div class="flex items-center gap-1.5 px-3 py-1 rounded-lg text-sm font-bold"
                   :style="`background:${+keyLevel>=20?'rgba(255,128,0,0.15)':+keyLevel>=15?'rgba(163,53,238,0.15)':+keyLevel>=10?'rgba(0,112,221,0.15)':'var(--bg-dim)'};
                            color:${+keyLevel>=20?'#ff8000':+keyLevel>=15?'#a335ee':+keyLevel>=10?'#0070dd':'#6b6b8a'}`">
                <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                  <path stroke-linecap="round" stroke-linejoin="round"
                        d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/>
                </svg>
                +{{ keyLevel }}
              </div>
            </div>

            <input
              v-model.number="keyLevel"
              type="range" min="2" max="25" step="1"
              class="key-slider w-full h-2 rounded-full appearance-none cursor-pointer"
              :style="`
                background: linear-gradient(to right,
                  ${+keyLevel>=20?'#ff8000':+keyLevel>=15?'#a335ee':+keyLevel>=10?'#0070dd':'#6b6b8a'} 0%,
                  ${+keyLevel>=20?'#ff8000':+keyLevel>=15?'#a335ee':+keyLevel>=10?'#0070dd':'#6b6b8a'} ${(+keyLevel-2)/23*100}%,
                  var(--border-subtle) ${(+keyLevel-2)/23*100}%,
                  var(--border-subtle) 100%)
              `"
            />

            <div class="flex justify-between text-[10px] text-iron mt-1.5 px-0.5">
              <span>+2</span>
              <span class="text-steel">+10</span>
              <span class="text-wow-epic">+15</span>
              <span class="text-wow-legendary">+20</span>
              <span>+25</span>
            </div>
          </div>

          <!-- Goal -->
          <div>
            <div class="text-xs font-semibold tracking-widest uppercase text-steel mb-2">목표</div>
            <div class="grid grid-cols-3 gap-2">
              <button v-for="[v, l, c] in [['timer','타이머 인','#ff8000'],['clear','클리어','#0070dd'],['any','상관없음','#6b6b8a']]"
                :key="v" type="button"
                class="h-11 rounded-full border text-xs font-semibold transition-all duration-200"
                :class="keyGoal===v?'text-white':'text-steel hover:text-silver'"
                :style="keyGoal===v?`background:${c};border-color:${c}`:'background:var(--bg-button);border-color:var(--border-subtle)'"
                @click="keyGoal=v">{{ l }}</button>
            </div>
          </div>

          <!-- Role -->
          <div>
            <div class="text-xs font-semibold tracking-widest uppercase text-steel mb-2">Role</div>
            <select v-model="keyRole" class="h-11 w-full rounded-full border border-rim/60 px-4 text-sm text-silver focus:outline-none focus:ring-2 focus:ring-wow-legendary/40 transition-all" style="background:var(--bg-input)">
              <option value="DPS">DPS</option><option value="HEAL">HEAL</option><option value="TANK">TANK</option>
            </select>
          </div>

          <!-- Region -->
          <div>
            <div class="text-xs font-semibold tracking-widest uppercase text-steel mb-2">Region</div>
            <select v-model="keyRegion" class="h-11 w-full rounded-full border border-rim/60 px-4 text-sm text-silver focus:outline-none focus:ring-2 focus:ring-wow-legendary/40 transition-all" style="background:var(--bg-input)">
              <option value="KR">KR</option><option value="US">US</option><option value="EU">EU</option>
            </select>
          </div>
        </div>

        <!-- Submit -->
        <div class="px-8 pb-8">
          <button type="button"
            class="w-full h-12 rounded-full font-semibold tracking-tight text-sm transition-all duration-300"
            :disabled="!canStart || isMatching"
            :class="canStart ? 'text-white hover:-translate-y-0.5' : 'text-iron cursor-not-allowed'"
            :style="canStart
              ? mode==='raid'
                ? 'background:#a335ee;box-shadow:0 8px 28px rgba(163,53,238,0.3)'
                : 'background:#ff8000;box-shadow:0 8px 28px rgba(255,128,0,0.3)'
              : 'background:var(--bg-dim)'"
            @click="startMatching">
            {{ mode === 'raid' ? '공격대 매칭 시작' : '쐐기 파티 매칭 시작' }}
          </button>
          <div class="mt-3 text-xs text-iron text-center">
            현재는 데모 알림만 뜹니다. 다음 단계로 API 붙여서 매칭 생성/조회로 바꾸면 돼요.
          </div>
        </div>
      </div>

    </div>
  </section>

  <!-- ── Matching Overlay (searching + match found) ─────── -->
  <Teleport to="body">
    <Transition
      enter-active-class="transition-all duration-300 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-all duration-200 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="isMatching"
        class="fixed inset-0 z-[100] flex items-center justify-center"
        style="background: var(--bg-overlay); backdrop-filter: blur(20px)"
        @click.self="!matchFound && cancelMatching()"
      >
        <!-- Dynamic glow -->
        <div class="absolute w-[600px] h-[600px] rounded-full pointer-events-none transition-all duration-700"
             :style="matchFound
               ? 'background:radial-gradient(ellipse,rgba(30,255,0,0.1) 0%,transparent 70%);filter:blur(70px)'
               : 'background:radial-gradient(ellipse,rgba(163,53,238,0.12) 0%,transparent 70%);filter:blur(60px)'"></div>

        <!-- ── SEARCHING card ── -->
        <Transition
          enter-active-class="transition-all duration-300 ease-out"
          enter-from-class="opacity-0 scale-95 translate-y-4"
          enter-to-class="opacity-100 scale-100 translate-y-0"
          leave-active-class="transition-all duration-200 ease-in"
          leave-from-class="opacity-100 scale-100"
          leave-to-class="opacity-0 scale-95"
        >
          <div v-if="!matchFound"
               class="relative w-full max-w-sm mx-4 rounded-[2rem] border border-rim/50 px-10 py-12 text-center"
               style="background: var(--bg-card-opaque)">

            <div class="relative flex items-center justify-center mb-8 mx-auto w-24 h-24">
              <svg class="absolute inset-0 w-full h-full animate-spin" style="animation-duration:3s" viewBox="0 0 96 96" fill="none">
                <circle cx="48" cy="48" r="44" stroke="rgba(163,53,238,0.15)" stroke-width="2"/>
                <path d="M48 4 A44 44 0 0 1 92 48" stroke="#a335ee" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <svg class="absolute inset-0 w-20 h-20 m-auto animate-spin" style="animation-duration:1.2s" viewBox="0 0 80 80" fill="none">
                <circle cx="40" cy="40" r="36" stroke="rgba(255,128,0,0.12)" stroke-width="2"/>
                <path d="M40 4 A36 36 0 0 1 76 40" stroke="#ff8000" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <span class="relative flex h-4 w-4">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-wow-epic opacity-50"></span>
                <span class="relative inline-flex rounded-full h-4 w-4 bg-wow-epic" style="box-shadow:0 0 12px rgba(163,53,238,0.8)"></span>
              </span>
            </div>

            <div class="text-xs font-semibold tracking-widest uppercase text-steel mb-3">Searching...</div>
            <h2 class="text-2xl font-bold tracking-tight text-silver mb-2">상대를 찾는 중</h2>
            <p class="text-sm text-steel mb-8 leading-relaxed">
              조건에 맞는 {{ mode==='raid' ? '공격대원' : '쐐기 파티원' }}을 탐색하고 있습니다.
            </p>

            <div class="flex flex-wrap justify-center gap-2 mb-8">
              <span v-if="mode==='raid'"
                    class="px-3 py-1 rounded-full text-xs font-semibold text-wow-epic border border-wow-epic/30"
                    style="background:rgba(163,53,238,0.1)">
                {{ raidSize }}인 레이드
              </span>
              <span v-else
                    class="px-3 py-1 rounded-full text-xs font-semibold border"
                    style="background:rgba(255,128,0,0.1);color:#ff8000;border-color:rgba(255,128,0,0.3)">
                +{{ keyLevel }} {{ dungeon }}
              </span>
              <span class="px-3 py-1 rounded-full text-xs font-semibold text-wow-rare border border-wow-rare/30"
                    style="background:rgba(0,112,221,0.1)">{{ roleLabel }}</span>
              <span class="px-3 py-1 rounded-full text-xs font-semibold text-steel border border-rim/40"
                    style="background:var(--bg-button)">
                {{ mode==='raid' ? region : keyRegion }}
              </span>
            </div>

            <button type="button"
              class="w-full h-11 rounded-full border border-rim/50 text-sm font-semibold text-steel
                     hover:text-silver hover:border-rim transition-all duration-200"
              style="background:var(--bg-button)"
              @click="cancelMatching">
              취소 (ESC)
            </button>
          </div>
        </Transition>

        <!-- ── MATCH FOUND card ── -->
        <Transition
          enter-active-class="transition-all duration-500 ease-out"
          enter-from-class="opacity-0 scale-90 translate-y-6"
          enter-to-class="opacity-100 scale-100 translate-y-0"
        >
          <div v-if="matchFound && matchedData"
               class="relative w-full max-w-md mx-4 rounded-[2rem] border overflow-hidden"
               style="background:var(--bg-match-card);border-color:rgba(30,255,0,0.25)">

            <!-- Top green accent bar -->
            <div class="h-1 w-full" style="background:linear-gradient(90deg,#1eff00,#00c8ff,#1eff00)"></div>

            <div class="px-8 py-8">
              <!-- Check + title -->
              <div class="flex flex-col items-center mb-6">
                <div class="relative mb-4">
                  <div class="w-16 h-16 rounded-full flex items-center justify-center"
                       style="background:rgba(30,255,0,0.12);box-shadow:0 0 30px rgba(30,255,0,0.25)">
                    <svg class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="#1eff00" stroke-width="2.5">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
                    </svg>
                  </div>
                  <span class="absolute -top-1 -right-1 flex h-4 w-4">
                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full opacity-60" style="background:#1eff00"></span>
                    <span class="relative inline-flex rounded-full h-4 w-4" style="background:#1eff00"></span>
                  </span>
                </div>
                <div class="text-xs font-semibold tracking-widest uppercase mb-1" style="color:#1eff00">Match Found</div>
                <h2 class="text-2xl font-bold tracking-tight text-silver">매칭 완료!</h2>
                <p class="text-sm text-steel mt-1">
                  <span v-if="matchedData.mode==='key'">+{{ matchedData.keyLevel }} {{ matchedData.dungeon }}</span>
                  <span v-else>{{ matchedData.raidSize }}인 공격대</span>
                  파티가 구성되었습니다.
                </p>
              </div>

              <!-- Party members -->
              <div class="space-y-2 mb-6">
                <div v-for="(member, i) in matchedData.party" :key="i"
                     class="flex items-center gap-3 px-4 py-3 rounded-2xl border border-rim/30"
                     style="background:var(--bg-match-member)">
                  <!-- Role icon -->
                  <div class="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0"
                       :style="`background:${member.role==='탱커'?'rgba(255,128,0,0.15)':member.role==='힐러'?'rgba(30,255,0,0.15)':'rgba(0,112,221,0.15)'}`">
                    <svg v-if="member.role==='탱커'" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="#ff8000" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                    </svg>
                    <svg v-else-if="member.role==='힐러'" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="#1eff00" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M12 21.593c-5.63-5.539-11-10.297-11-14.402 0-3.791 3.068-5.191 5.281-5.191 1.312 0 4.151.501 5.719 4.457 1.59-3.968 4.464-4.447 5.726-4.447 2.54 0 5.274 1.621 5.274 5.181 0 4.069-5.136 8.625-11 14.402z"/>
                    </svg>
                    <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="#0070dd" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                    </svg>
                  </div>
                  <!-- Name + class -->
                  <div class="flex-1 min-w-0">
                    <div class="text-sm font-semibold text-silver truncate">{{ member.name }}</div>
                    <div class="text-xs truncate" :style="`color:${CLASS_COLORS[member.cls]??'#9d9d9d'}`">{{ member.cls }}</div>
                  </div>
                  <!-- Stats -->
                  <div class="text-right flex-shrink-0">
                    <div class="text-xs font-semibold text-steel">{{ member.ilvl }} ilvl</div>
                    <div class="text-xs font-bold" :style="`color:${rioColor(member.rio)}`">{{ member.rio.toLocaleString() }}</div>
                  </div>
                </div>
              </div>

              <!-- Actions -->
              <button type="button"
                class="w-full h-12 rounded-full font-semibold text-sm text-white mb-2 transition-all duration-200 hover:-translate-y-0.5"
                style="background:#1eff00;color:#080810;box-shadow:0 8px 24px rgba(30,255,0,0.25)"
                @click="joinParty">
                파티 참가하기
              </button>
              <button type="button"
                class="w-full h-11 rounded-full border border-rim/50 text-sm font-semibold text-steel
                       hover:text-silver hover:border-rim transition-all duration-200"
                style="background:var(--bg-button)"
                @click="cancelMatching">
                닫기
              </button>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>
