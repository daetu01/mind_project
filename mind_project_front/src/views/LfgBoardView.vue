<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

/* ── Constants ────────────────────────────────────────── */
const DUNGEONS = [
  '아라카라',  '스레드의 도시', '그림 배톨',   '스톤볼트',
  '던브레이커', '티르나 시의 안개', '보랄루스 공성전', '부식 괴멸',
]

/* ── Mode ─────────────────────────────────────────────── */
const mode = ref('raid')   // 'raid' | 'key'

/* ── Raid mock data ───────────────────────────────────── */
const raidPosts = ref([
  { id: 1, guild: '어둠의 파수꾼', realm: '데스윙', raid: '네루바르 궁전', difficulty: 'Mythic', progress: '9/9',
    slots: { tank: 0, heal: 1, dps: 2 }, ilvlReq: 645, wclReq: 75, voice: false,
    schedule: '월수금 21:00~24:00', region: 'KR', note: 'WCL 75+ DPS · 힐러 1명. 장기 고정팟 모집합니다.', createdAt: '10분 전' },
  { id: 2, guild: '실버문의 후예', realm: '아즈샤라', raid: '네루바르 궁전', difficulty: 'Heroic', progress: '9/9',
    slots: { tank: 1, heal: 0, dps: 3 }, ilvlReq: 619, wclReq: null, voice: true,
    schedule: '화목토 20:00~23:00', region: 'KR', note: '자유로운 분위기. 초보 환영. 탱커 급구!', createdAt: '32분 전' },
  { id: 3, guild: 'Frost Vanguard', realm: 'Azralon', raid: '네루바르 궁전', difficulty: 'Mythic', progress: '6/9',
    slots: { tank: 0, heal: 1, dps: 1 }, ilvlReq: 636, wclReq: 60, voice: true,
    schedule: 'Mon/Wed/Fri 20:00~23:00', region: 'US', note: 'Progression team. 6/9M exp required.', createdAt: '1시간 전' },
  { id: 4, guild: '달빛 기사단', realm: '불타는 군단', raid: '네루바르 궁전', difficulty: 'Normal', progress: '9/9',
    slots: { tank: 1, heal: 2, dps: 5 }, ilvlReq: 590, wclReq: null, voice: false,
    schedule: '주말 오후 2시~5시', region: 'KR', note: '입문자 대환영. 편하게 같이 즐겨요 :)', createdAt: '2시간 전' },
  { id: 5, guild: 'Sanctum Elite', realm: 'Kazzak', raid: '아문 타울 니루프', difficulty: 'Mythic', progress: '8/8',
    slots: { tank: 0, heal: 0, dps: 2 }, ilvlReq: 658, wclReq: 85, voice: true,
    schedule: 'Tue/Thu 20:00~23:00 ST', region: 'EU', note: 'CE achieved. DPS 85+ orange logs preferred.', createdAt: '3시간 전' },
  { id: 6, guild: '폭풍의 정점', realm: '줄진', raid: '네루바르 궁전', difficulty: 'Heroic', progress: '7/9',
    slots: { tank: 0, heal: 1, dps: 2 }, ilvlReq: 610, wclReq: null, voice: false,
    schedule: '수금 21:30~23:30', region: 'KR', note: '조용한 분위기 선호. 텍스트 콜 공대입니다.', createdAt: '5시간 전' },
])

/* ── Keystone mock data ───────────────────────────────── */
const keyPosts = ref([
  { id: 201, player: 'Frostmourne', realm: '데스윙', dungeon: '아라카라', keyLevel: 15,
    slots: { tank: 0, heal: 0, dps: 2 }, rioReq: 2800, ilvlReq: 636, voice: false,
    goal: 'timer', region: 'KR', note: '빠른 클리어 원합니다. RIO 2800+ 딜러 2명 구합니다.', createdAt: '5분 전' },
  { id: 202, player: 'Shadowstep', realm: '줄진', dungeon: '그림 배톨', keyLevel: 12,
    slots: { tank: 1, heal: 0, dps: 1 }, rioReq: 2000, ilvlReq: 620, voice: false,
    goal: 'clear', region: 'KR', note: '조용하게 클리어해요. 부담 없이 오세요.', createdAt: '15분 전' },
  { id: 203, player: 'ArcaneBlast', realm: 'Azralon', dungeon: '스톤볼트', keyLevel: 20,
    slots: { tank: 0, heal: 1, dps: 0 }, rioReq: 3200, ilvlReq: 645, voice: true,
    goal: 'timer', region: 'US', note: 'High push. 3200+ RIO healer needed. Quick depletes.', createdAt: '22분 전' },
  { id: 204, player: 'Moonwhisper', realm: '아즈샤라', dungeon: '부식 괴멸', keyLevel: 10,
    slots: { tank: 1, heal: 1, dps: 1 }, rioReq: null, ilvlReq: 608, voice: false,
    goal: 'any', region: 'KR', note: '주간 쐐기 완성 목적. 입문자 환영합니다.', createdAt: '41분 전' },
  { id: 205, player: 'Stormcaller', realm: 'Kazzak', dungeon: '보랄루스 공성전', keyLevel: 17,
    slots: { tank: 0, heal: 0, dps: 3 }, rioReq: 3000, ilvlReq: 639, voice: true,
    goal: 'timer', region: 'EU', note: 'Looking for 3k+ RIO DPS. Timer focus.', createdAt: '1시간 전' },
  { id: 206, player: 'Darkbrew', realm: '불타는 군단', dungeon: '던브레이커', keyLevel: 8,
    slots: { tank: 0, heal: 1, dps: 2 }, rioReq: null, ilvlReq: 590, voice: false,
    goal: 'any', region: 'KR', note: '부담 없이 해요. 힐러·딜러 구합니다.', createdAt: '2시간 전' },
  { id: 207, player: 'IceQueen', realm: '공허의 바람', dungeon: '티르나 시의 안개', keyLevel: 13,
    slots: { tank: 0, heal: 0, dps: 1 }, rioReq: 2300, ilvlReq: 625, voice: false,
    goal: 'timer', region: 'KR', note: 'DPS 1명만 구해요. RIO 2300+ 빠르게 완성해요.', createdAt: '3시간 전' },
])

/* ── Raid filters ─────────────────────────────────────── */
const raidRoleFilter   = ref('all')
const raidDiffFilter   = ref('all')
const raidRegionFilter = ref('all')

const filteredRaids = computed(() => raidPosts.value.filter(p => {
  if (raidRoleFilter.value === 'tank' && p.slots.tank === 0) return false
  if (raidRoleFilter.value === 'heal' && p.slots.heal === 0) return false
  if (raidRoleFilter.value === 'dps'  && p.slots.dps  === 0) return false
  if (raidDiffFilter.value   !== 'all' && p.difficulty !== raidDiffFilter.value) return false
  if (raidRegionFilter.value !== 'all' && p.region    !== raidRegionFilter.value) return false
  return true
}))

/* ── Keystone filters ─────────────────────────────────── */
const keyDungeonFilter  = ref('all')
const keyLevelFilter    = ref('all')  // all | ~9 | 10~14 | 15~19 | 20+
const keyGoalFilter     = ref('all')
const keyRegionFilter   = ref('all')

const filteredKeys = computed(() => keyPosts.value.filter(p => {
  if (keyDungeonFilter.value  !== 'all' && p.dungeon !== keyDungeonFilter.value) return false
  if (keyRegionFilter.value   !== 'all' && p.region  !== keyRegionFilter.value)  return false
  if (keyGoalFilter.value     !== 'all' && p.goal    !== keyGoalFilter.value)    return false
  if (keyLevelFilter.value === '~9'   && p.keyLevel >= 10) return false
  if (keyLevelFilter.value === '10~14' && (p.keyLevel < 10 || p.keyLevel > 14)) return false
  if (keyLevelFilter.value === '15~19' && (p.keyLevel < 15 || p.keyLevel > 19)) return false
  if (keyLevelFilter.value === '20+'   && p.keyLevel < 20) return false
  return true
}))

/* ── Helpers ──────────────────────────────────────────── */
const diffColor = { Normal: '#1eff00', Heroic: '#0070dd', Mythic: '#ff8000' }
const diffBg    = { Normal: 'rgba(30,255,0,0.1)', Heroic: 'rgba(0,112,221,0.1)', Mythic: 'rgba(255,128,0,0.1)' }
const goalLabel = { timer: '타이머 인', clear: '클리어', any: '상관없음' }
const goalColor = { timer: '#ff8000', clear: '#0070dd', any: '#6b6b8a' }

function keyColor(lv) {
  if (lv >= 20) return '#ff8000'
  if (lv >= 15) return '#a335ee'
  if (lv >= 10) return '#0070dd'
  return '#6b6b8a'
}
function keyBg(lv) {
  if (lv >= 20) return 'rgba(255,128,0,0.14)'
  if (lv >= 15) return 'rgba(163,53,238,0.14)'
  if (lv >= 10) return 'rgba(0,112,221,0.14)'
  return 'var(--bg-dim)'
}
function rioColor(score) {
  if (!score) return '#6b6b8a'
  if (score >= 3000) return '#ff8000'
  if (score >= 2500) return '#a335ee'
  if (score >= 2000) return '#0070dd'
  return '#1eff00'
}

/* ── Toast ────────────────────────────────────────────── */
const toast = ref('')
let toastTimer = null
function showToast(msg) {
  toast.value = msg
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => { toast.value = '' }, 3000)
}
function applyToPost(post) { showToast(`지원 완료! (${post.guild ?? post.player})`) }

/* ── Write modal ──────────────────────────────────────── */
const showModal = ref(false)

// Raid form
const raidForm = ref({
  guild: '', realm: '', raid: '네루바르 궁전', difficulty: 'Heroic', progress: '',
  tankSlots: 0, healSlots: 1, dpsSlots: 2,
  ilvlReq: '', wclReq: '', voice: false, schedule: '', region: 'KR', note: '',
})

// Keystone form
const keyForm = ref({
  player: '', realm: '', dungeon: '아라카라', keyLevel: 10,
  tankSlots: 0, healSlots: 1, dpsSlots: 2,
  rioReq: '', ilvlReq: '', voice: false, goal: 'any', region: 'KR', note: '',
})

function submitRaid() {
  if (!raidForm.value.guild || !raidForm.value.realm) return
  raidPosts.value.unshift({
    id: Date.now(), guild: raidForm.value.guild, realm: raidForm.value.realm,
    raid: raidForm.value.raid, difficulty: raidForm.value.difficulty,
    progress: raidForm.value.progress || '?/9',
    slots: { tank: +raidForm.value.tankSlots, heal: +raidForm.value.healSlots, dps: +raidForm.value.dpsSlots },
    ilvlReq: +raidForm.value.ilvlReq || null, wclReq: +raidForm.value.wclReq || null,
    voice: raidForm.value.voice, schedule: raidForm.value.schedule,
    region: raidForm.value.region, note: raidForm.value.note, createdAt: '방금 전',
  })
  showModal.value = false
  showToast('모집글이 등록됐습니다!')
}

function editPost(post) {
  router.push({ name: 'edit-post', params: { id: post.id }, state: { post: JSON.parse(JSON.stringify(post)) } })
}

function submitKey() {
  if (!keyForm.value.player || !keyForm.value.realm) return
  keyPosts.value.unshift({
    id: Date.now(), player: keyForm.value.player, realm: keyForm.value.realm,
    dungeon: keyForm.value.dungeon, keyLevel: +keyForm.value.keyLevel,
    slots: { tank: +keyForm.value.tankSlots, heal: +keyForm.value.healSlots, dps: +keyForm.value.dpsSlots },
    rioReq: +keyForm.value.rioReq || null, ilvlReq: +keyForm.value.ilvlReq || null,
    voice: keyForm.value.voice, goal: keyForm.value.goal,
    region: keyForm.value.region, note: keyForm.value.note, createdAt: '방금 전',
  })
  showModal.value = false
  showToast('쐐기 파티 모집글이 등록됐습니다!')
}
</script>

<template>
  <section class="px-4 sm:px-6 lg:px-8 py-14">
    <div class="max-w-5xl mx-auto">

      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4 mb-6">
        <div>
          <h1 class="text-4xl md:text-5xl font-bold tracking-tighter text-silver">파티 모집</h1>
          <p class="mt-2 text-steel text-base">공격대 · 쐐기 파티를 찾거나 직접 모집하세요.</p>
        </div>
        <button type="button"
          class="self-start sm:self-auto flex items-center gap-2 h-11 px-5 rounded-full text-sm font-semibold text-white transition-all duration-300 hover:-translate-y-0.5"
          style="background: #a335ee; box-shadow: 0 6px 20px rgba(163,53,238,0.3)"
          @click="showModal = true">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/>
          </svg>
          모집글 작성
        </button>
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
          공격대 모집
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
          쐐기 모집
        </button>
      </div>

      <!-- ═══ RAID MODE ═══════════════════════════════════ -->
      <template v-if="mode === 'raid'">
        <!-- Raid filters -->
        <div class="flex flex-wrap gap-3 mb-6">
          <div class="flex items-center h-10 p-1 rounded-full border border-rim/50 gap-0.5"
               style="background: var(--bg-card)">
            <button v-for="[v, l] in [['all','전체'],['tank','탱커'],['heal','힐러'],['dps','딜러']]" :key="v"
              type="button"
              class="h-8 px-3.5 rounded-full text-xs font-semibold transition-all duration-200"
              :class="raidRoleFilter === v ? 'text-white' : 'text-steel hover:text-silver'"
              :style="raidRoleFilter === v ? 'background: #a335ee' : ''"
              @click="raidRoleFilter = v">{{ l }}</button>
          </div>
          <div class="flex items-center h-10 p-1 rounded-full border border-rim/50 gap-0.5"
               style="background: var(--bg-card)">
            <button v-for="[v, l] in [['all','난이도'],['Normal','N'],['Heroic','H'],['Mythic','M']]" :key="v"
              type="button"
              class="h-8 px-3.5 rounded-full text-xs font-semibold transition-all duration-200"
              :class="raidDiffFilter === v ? 'text-white' : 'text-steel hover:text-silver'"
              :style="raidDiffFilter === v ? `background:${v==='all'?'#a335ee':diffColor[v]}` : ''"
              @click="raidDiffFilter = v">{{ l }}</button>
          </div>
          <div class="flex items-center h-10 p-1 rounded-full border border-rim/50 gap-0.5"
               style="background: var(--bg-card)">
            <button v-for="[v] in [['all'],['KR'],['US'],['EU']]" :key="v"
              type="button"
              class="h-8 px-3.5 rounded-full text-xs font-semibold transition-all duration-200"
              :class="raidRegionFilter === v ? 'text-white' : 'text-steel hover:text-silver'"
              :style="raidRegionFilter === v ? 'background:#a335ee' : ''"
              @click="raidRegionFilter = v">{{ v }}</button>
          </div>
          <div class="ml-auto flex items-center text-xs text-steel self-center">{{ filteredRaids.length }}개</div>
        </div>

        <!-- Raid posts -->
        <div class="flex flex-col gap-4">
          <TransitionGroup name="post">
            <div v-for="post in filteredRaids" :key="post.id"
                 class="group rounded-[1.5rem] border border-rim/50 p-6 transition-all duration-300 hover:border-rim"
                 style="background: var(--bg-card-light); backdrop-filter: blur(12px)">
              <div class="flex flex-wrap items-center gap-2 mb-3">
                <span class="text-sm font-semibold text-silver">{{ post.guild }}</span>
                <span class="text-iron text-xs">·</span>
                <span class="text-xs text-steel">{{ post.realm }}</span>
                <div class="ml-auto flex items-center gap-2">
                  <span class="px-2.5 py-0.5 rounded-full text-xs font-semibold"
                        :style="post.progress.split('/')[0]===post.progress.split('/')[1]
                          ?'background:rgba(30,255,0,0.1);color:#1eff00'
                          :'background:rgba(163,53,238,0.1);color:#a335ee'">
                    {{ post.progress }}</span>
                  <span class="px-2.5 py-0.5 rounded-full text-xs font-semibold"
                        :style="`background:${diffBg[post.difficulty]};color:${diffColor[post.difficulty]}`">
                    {{ post.difficulty }}</span>
                </div>
              </div>
              <div class="text-base font-semibold text-silver mb-4">{{ post.raid }}</div>
              <div class="flex flex-wrap items-center gap-3 mb-4">
                <div class="flex items-center gap-1.5 text-xs font-semibold" :class="post.slots.tank>0?'':'opacity-25'">
                  <span class="w-6 h-6 rounded-lg flex items-center justify-center"
                        :style="post.slots.tank>0?'background:rgba(0,112,221,0.15)':'background:var(--bg-dim)'">
                    <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                         :style="post.slots.tank>0?'color:#0070dd':'color:var(--color-iron)'">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M12 2L3 7v5c0 5.25 3.75 10.15 9 11.35C17.25 22.15 21 17.25 21 12V7l-9-5z"/>
                    </svg>
                  </span>
                  <span :style="post.slots.tank>0?'color:#0070dd':'color:var(--color-iron)'">탱커 {{ post.slots.tank }}</span>
                </div>
                <div class="flex items-center gap-1.5 text-xs font-semibold" :class="post.slots.heal>0?'':'opacity-25'">
                  <span class="w-6 h-6 rounded-lg flex items-center justify-center"
                        :style="post.slots.heal>0?'background:rgba(30,255,0,0.1)':'background:var(--bg-dim)'">
                    <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                         :style="post.slots.heal>0?'color:#1eff00':'color:var(--color-iron)'">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/>
                    </svg>
                  </span>
                  <span :style="post.slots.heal>0?'color:#1eff00':'color:var(--color-iron)'">힐러 {{ post.slots.heal }}</span>
                </div>
                <div class="flex items-center gap-1.5 text-xs font-semibold" :class="post.slots.dps>0?'':'opacity-25'">
                  <span class="w-6 h-6 rounded-lg flex items-center justify-center"
                        :style="post.slots.dps>0?'background:rgba(255,70,70,0.12)':'background:var(--bg-dim)'">
                    <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                         :style="post.slots.dps>0?'color:#ff4646':'color:var(--color-iron)'">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M14.5 10L21 3m0 0h-6m6 0v6M10 14l-7 7m0 0h6m-6 0v-6"/>
                    </svg>
                  </span>
                  <span :style="post.slots.dps>0?'color:#ff4646':'color:var(--color-iron)'">딜러 {{ post.slots.dps }}</span>
                </div>
                <div class="flex items-center gap-3 ml-auto text-xs text-iron">
                  <span v-if="post.ilvlReq">ilv {{ post.ilvlReq }}+</span>
                  <span v-if="post.wclReq" :style="`color:${post.wclReq>=75?'#a335ee':post.wclReq>=50?'#0070dd':'#1eff00'}`">WCL {{ post.wclReq }}+</span>
                </div>
              </div>
              <p class="text-sm text-steel leading-relaxed mb-4 line-clamp-2">{{ post.note }}</p>
              <div class="flex flex-wrap items-center gap-3 pt-4 border-t border-rim/30">
                <span class="text-xs text-iron">{{ post.region }}</span>
                <span v-if="post.schedule" class="text-xs text-iron">· {{ post.schedule }}</span>
                <span class="text-xs text-iron ml-auto">{{ post.createdAt }}</span>
                <button type="button"
                  class="flex items-center gap-1.5 h-9 px-4 rounded-full border border-rim/60 text-xs font-semibold text-steel hover:text-silver hover:border-rim transition-all"
                  style="background:var(--bg-button)"
                  @click="editPost(post)">
                  <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                  </svg>
                  수정
                </button>
                <button type="button"
                  class="flex items-center gap-1.5 h-9 px-4 rounded-full border border-rim/60 text-xs font-semibold text-steel hover:text-silver hover:border-wow-epic/50 transition-all"
                  style="background:var(--bg-button)"
                  @click="applyToPost(post)">
                  지원하기
                  <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/>
                  </svg>
                </button>
              </div>
            </div>
          </TransitionGroup>
          <div v-if="filteredRaids.length===0" class="text-center py-20 text-steel text-sm">조건에 맞는 모집글이 없습니다.</div>
        </div>
      </template>

      <!-- ═══ KEYSTONE MODE ════════════════════════════════ -->
      <template v-else>
        <!-- Keystone filters -->
        <div class="flex flex-wrap gap-3 mb-6">
          <!-- Dungeon filter -->
          <select v-model="keyDungeonFilter"
            class="h-10 rounded-full border border-rim/50 px-4 text-xs font-semibold text-steel
                   focus:outline-none focus:ring-2 focus:ring-wow-legendary/40 transition-all"
            style="background: var(--bg-card)">
            <option value="all">모든 던전</option>
            <option v-for="d in DUNGEONS" :key="d" :value="d">{{ d }}</option>
          </select>

          <!-- Key level filter -->
          <div class="flex items-center h-10 p-1 rounded-full border border-rim/50 gap-0.5"
               style="background: var(--bg-card)">
            <button v-for="[v, l] in [['all','전체'],['~9','~+9'],['10~14','+10~14'],['15~19','+15~19'],['20+','+20↑']]" :key="v"
              type="button"
              class="h-8 px-3 rounded-full text-xs font-semibold transition-all duration-200"
              :class="keyLevelFilter === v ? 'text-white' : 'text-steel hover:text-silver'"
              :style="keyLevelFilter === v ? 'background: #ff8000' : ''"
              @click="keyLevelFilter = v">{{ l }}</button>
          </div>

          <!-- Goal filter -->
          <div class="flex items-center h-10 p-1 rounded-full border border-rim/50 gap-0.5"
               style="background: var(--bg-card)">
            <button v-for="[v, l] in [['all','목표'],['timer','타이머'],['clear','클리어']]" :key="v"
              type="button"
              class="h-8 px-3.5 rounded-full text-xs font-semibold transition-all duration-200"
              :class="keyGoalFilter === v ? 'text-white' : 'text-steel hover:text-silver'"
              :style="keyGoalFilter === v ? `background:${v==='all'?'#ff8000':goalColor[v]}` : ''"
              @click="keyGoalFilter = v">{{ l }}</button>
          </div>

          <div class="ml-auto flex items-center text-xs text-steel self-center">{{ filteredKeys.length }}개</div>
        </div>

        <!-- Keystone posts -->
        <div class="flex flex-col gap-4">
          <TransitionGroup name="post">
            <div v-for="post in filteredKeys" :key="post.id"
                 class="group rounded-[1.5rem] border p-6 transition-all duration-300"
                 :style="`background:var(--bg-card-light);backdrop-filter:blur(12px);border-color:${keyColor(post.keyLevel)}22`"
                 :class="'hover:border-rim'">

              <!-- Top row: player + key badge -->
              <div class="flex flex-wrap items-center gap-2 mb-4">
                <div>
                  <span class="text-sm font-semibold text-silver">{{ post.player }}</span>
                  <span class="text-iron text-xs mx-1.5">·</span>
                  <span class="text-xs text-steel">{{ post.realm }}</span>
                </div>
                <div class="ml-auto flex items-center gap-2">
                  <!-- Key level badge - the centerpiece -->
                  <div class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl font-bold text-sm"
                       :style="`background:${keyBg(post.keyLevel)};color:${keyColor(post.keyLevel)}`">
                    <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                      <path stroke-linecap="round" stroke-linejoin="round"
                            d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/>
                    </svg>
                    +{{ post.keyLevel }}
                  </div>
                  <!-- Goal badge -->
                  <span class="px-2.5 py-0.5 rounded-full text-xs font-semibold"
                        :style="`background:${goalColor[post.goal]}18;color:${goalColor[post.goal]}`">
                    {{ goalLabel[post.goal] }}
                  </span>
                </div>
              </div>

              <!-- Dungeon name -->
              <div class="text-lg font-semibold mb-4" :style="`color:${keyColor(post.keyLevel)}`">
                {{ post.dungeon }}
              </div>

              <!-- Slots -->
              <div class="flex flex-wrap items-center gap-3 mb-4">
                <div class="flex items-center gap-1.5 text-xs font-semibold" :class="post.slots.tank>0?'':'opacity-25'">
                  <span class="w-6 h-6 rounded-lg flex items-center justify-center"
                        :style="post.slots.tank>0?'background:rgba(0,112,221,0.15)':'background:var(--bg-dim)'">
                    <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                         :style="post.slots.tank>0?'color:#0070dd':'color:var(--color-iron)'">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M12 2L3 7v5c0 5.25 3.75 10.15 9 11.35C17.25 22.15 21 17.25 21 12V7l-9-5z"/>
                    </svg>
                  </span>
                  <span :style="post.slots.tank>0?'color:#0070dd':'color:var(--color-iron)'">탱커 {{ post.slots.tank }}</span>
                </div>
                <div class="flex items-center gap-1.5 text-xs font-semibold" :class="post.slots.heal>0?'':'opacity-25'">
                  <span class="w-6 h-6 rounded-lg flex items-center justify-center"
                        :style="post.slots.heal>0?'background:rgba(30,255,0,0.1)':'background:var(--bg-dim)'">
                    <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                         :style="post.slots.heal>0?'color:#1eff00':'color:var(--color-iron)'">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/>
                    </svg>
                  </span>
                  <span :style="post.slots.heal>0?'color:#1eff00':'color:var(--color-iron)'">힐러 {{ post.slots.heal }}</span>
                </div>
                <div class="flex items-center gap-1.5 text-xs font-semibold" :class="post.slots.dps>0?'':'opacity-25'">
                  <span class="w-6 h-6 rounded-lg flex items-center justify-center"
                        :style="post.slots.dps>0?'background:rgba(255,70,70,0.12)':'background:var(--bg-dim)'">
                    <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                         :style="post.slots.dps>0?'color:#ff4646':'color:var(--color-iron)'">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M14.5 10L21 3m0 0h-6m6 0v6M10 14l-7 7m0 0h6m-6 0v-6"/>
                    </svg>
                  </span>
                  <span :style="post.slots.dps>0?'color:#ff4646':'color:var(--color-iron)'">딜러 {{ post.slots.dps }}</span>
                </div>
                <div class="flex items-center gap-2 ml-auto text-xs">
                  <span v-if="post.ilvlReq" class="text-iron">ilv {{ post.ilvlReq }}+</span>
                  <span v-if="post.rioReq" class="font-semibold" :style="`color:${rioColor(post.rioReq)}`">
                    RIO {{ post.rioReq.toLocaleString() }}+
                  </span>
                </div>
              </div>

              <p class="text-sm text-steel leading-relaxed mb-4 line-clamp-2">{{ post.note }}</p>
              <div class="flex flex-wrap items-center gap-3 pt-4 border-t border-rim/30">
                <span class="text-xs text-iron">{{ post.region }}</span>
                <span class="text-xs text-iron ml-auto">{{ post.createdAt }}</span>
                <button type="button"
                  class="flex items-center gap-1.5 h-9 px-4 rounded-full border border-rim/60 text-xs font-semibold text-steel hover:text-silver hover:border-rim transition-all"
                  style="background:var(--bg-button)"
                  @click="editPost(post)">
                  <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                  </svg>
                  수정
                </button>
                <button type="button"
                  class="flex items-center gap-1.5 h-9 px-4 rounded-full text-xs font-semibold text-white transition-all hover:-translate-y-0.5"
                  :style="`background:${keyColor(post.keyLevel)};box-shadow:0 4px 12px ${keyColor(post.keyLevel)}33`"
                  @click="applyToPost(post)">
                  참가하기
                  <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/>
                  </svg>
                </button>
              </div>
            </div>
          </TransitionGroup>
          <div v-if="filteredKeys.length===0" class="text-center py-20 text-steel text-sm">조건에 맞는 쐐기 파티가 없습니다.</div>
        </div>
      </template>

    </div>
  </section>

  <!-- ═══ Write Modal ══════════════════════════════════════ -->
  <Teleport to="body">
    <Transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0" enter-to-class="opacity-100"
                leave-active-class="transition-all duration-200 ease-in"  leave-from-class="opacity-100" leave-to-class="opacity-0">
      <div v-if="showModal"
           class="fixed inset-0 z-[100] flex items-center justify-center px-4 py-8 overflow-y-auto"
           style="background:var(--bg-overlay);backdrop-filter:blur(16px)"
           @click.self="showModal=false">
        <Transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 scale-95 translate-y-4" enter-to-class="opacity-100 scale-100 translate-y-0">
          <div v-if="showModal" class="relative w-full max-w-lg rounded-[2rem] border border-rim/50 overflow-hidden"
               style="background:var(--bg-card-opaque)">

            <!-- Modal header with mode indicator -->
            <div class="px-8 py-5 border-b border-rim/40 flex items-center justify-between">
              <div>
                <div class="text-sm font-semibold text-silver">
                  {{ mode === 'raid' ? '공격대 모집글 작성' : '쐐기 파티 모집글 작성' }}
                </div>
                <div class="flex items-center gap-1.5 mt-1">
                  <span class="w-2 h-2 rounded-full" :style="mode==='raid'?'background:#a335ee':'background:#ff8000'"></span>
                  <span class="text-xs text-steel">{{ mode==='raid'?'공격대 모드':'쐐기 모드' }}</span>
                </div>
              </div>
              <button type="button" class="text-steel hover:text-silver transition-colors" @click="showModal=false">
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>

            <!-- ── Raid form ── -->
            <div v-if="mode==='raid'" class="px-8 py-6 flex flex-col gap-4">
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">길드명</label>
                  <input v-model="raidForm.guild" type="text" placeholder="어둠의 파수꾼"
                    class="w-full h-10 rounded-full border border-rim/60 px-4 text-sm text-silver placeholder:text-iron focus:outline-none focus:ring-2 focus:ring-wow-epic/40 transition-all"
                    style="background:var(--bg-input)"/>
                </div>
                <div>
                  <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">서버</label>
                  <input v-model="raidForm.realm" type="text" placeholder="데스윙"
                    class="w-full h-10 rounded-full border border-rim/60 px-4 text-sm text-silver placeholder:text-iron focus:outline-none focus:ring-2 focus:ring-wow-epic/40 transition-all"
                    style="background:var(--bg-input)"/>
                </div>
              </div>
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">레이드</label>
                  <select v-model="raidForm.raid" class="w-full h-10 rounded-full border border-rim/60 px-4 text-sm text-silver focus:outline-none focus:ring-2 focus:ring-wow-epic/40 transition-all" style="background:var(--bg-input)">
                    <option>네루바르 궁전</option><option>아문 타울 니루프</option>
                  </select>
                </div>
                <div>
                  <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">난이도</label>
                  <select v-model="raidForm.difficulty" class="w-full h-10 rounded-full border border-rim/60 px-4 text-sm text-silver focus:outline-none focus:ring-2 focus:ring-wow-epic/40 transition-all" style="background:var(--bg-input)">
                    <option>Normal</option><option>Heroic</option><option>Mythic</option>
                  </select>
                </div>
              </div>
              <div>
                <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">모집 인원</label>
                <div class="grid grid-cols-3 gap-3">
                  <div class="text-center">
                    <div class="text-xs text-wow-rare mb-1">탱커</div>
                    <input v-model.number="raidForm.tankSlots" type="number" min="0" max="3" class="w-full h-10 rounded-full border border-rim/60 px-4 text-sm text-silver text-center focus:outline-none focus:ring-2 focus:ring-wow-epic/40 transition-all" style="background:var(--bg-input)"/>
                  </div>
                  <div class="text-center">
                    <div class="text-xs text-wow-uncommon mb-1">힐러</div>
                    <input v-model.number="raidForm.healSlots" type="number" min="0" max="5" class="w-full h-10 rounded-full border border-rim/60 px-4 text-sm text-silver text-center focus:outline-none focus:ring-2 focus:ring-wow-epic/40 transition-all" style="background:var(--bg-input)"/>
                  </div>
                  <div class="text-center">
                    <div class="text-xs mb-1" style="color:#ff4646">딜러</div>
                    <input v-model.number="raidForm.dpsSlots" type="number" min="0" max="20" class="w-full h-10 rounded-full border border-rim/60 px-4 text-sm text-silver text-center focus:outline-none focus:ring-2 focus:ring-wow-epic/40 transition-all" style="background:var(--bg-input)"/>
                  </div>
                </div>
              </div>
              <div class="grid grid-cols-3 gap-3">
                <div>
                  <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">최소 ilvl</label>
                  <input v-model="raidForm.ilvlReq" type="number" placeholder="600" class="w-full h-10 rounded-full border border-rim/60 px-4 text-sm text-silver placeholder:text-iron focus:outline-none focus:ring-2 focus:ring-wow-epic/40 transition-all" style="background:var(--bg-input)"/>
                </div>
                <div>
                  <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">최소 WCL</label>
                  <input v-model="raidForm.wclReq" type="number" placeholder="선택" class="w-full h-10 rounded-full border border-rim/60 px-4 text-sm text-silver placeholder:text-iron focus:outline-none focus:ring-2 focus:ring-wow-epic/40 transition-all" style="background:var(--bg-input)"/>
                </div>
                <div>
                  <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">지역</label>
                  <select v-model="raidForm.region" class="w-full h-10 rounded-full border border-rim/60 px-4 text-sm text-silver focus:outline-none focus:ring-2 focus:ring-wow-epic/40 transition-all" style="background:var(--bg-input)">
                    <option>KR</option><option>US</option><option>EU</option>
                  </select>
                </div>
              </div>
              <div>
                <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">일정</label>
                <input v-model="raidForm.schedule" type="text" placeholder="월수금 21:00~24:00" class="w-full h-10 rounded-full border border-rim/60 px-4 text-sm text-silver placeholder:text-iron focus:outline-none focus:ring-2 focus:ring-wow-epic/40 transition-all" style="background:var(--bg-input)"/>
              </div>
              <div>
                <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">한마디</label>
                <textarea v-model="raidForm.note" rows="2" placeholder="공대 소개..." class="w-full rounded-2xl border border-rim/60 px-4 py-3 text-sm text-silver placeholder:text-iron resize-none focus:outline-none focus:ring-2 focus:ring-wow-epic/40 transition-all" style="background:var(--bg-input)"></textarea>
              </div>
              <div class="flex gap-3 pt-2">
                <button type="button" class="flex-1 h-11 rounded-full border border-rim/50 text-sm font-semibold text-steel hover:text-silver transition-all" style="background:var(--bg-button)" @click="showModal=false">취소</button>
                <button type="button" class="flex-1 h-11 rounded-full text-sm font-semibold text-white transition-all hover:-translate-y-0.5" style="background:#a335ee;box-shadow:0 6px 20px rgba(163,53,238,0.3)" @click="submitRaid">등록하기</button>
              </div>
            </div>

            <!-- ── Keystone form ── -->
            <div v-else class="px-8 py-6 flex flex-col gap-4">
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">닉네임</label>
                  <input v-model="keyForm.player" type="text" placeholder="Playernam"
                    class="w-full h-10 rounded-full border border-rim/60 px-4 text-sm text-silver placeholder:text-iron focus:outline-none focus:ring-2 focus:ring-wow-legendary/40 transition-all"
                    style="background:var(--bg-input)"/>
                </div>
                <div>
                  <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">서버</label>
                  <input v-model="keyForm.realm" type="text" placeholder="데스윙"
                    class="w-full h-10 rounded-full border border-rim/60 px-4 text-sm text-silver placeholder:text-iron focus:outline-none focus:ring-2 focus:ring-wow-legendary/40 transition-all"
                    style="background:var(--bg-input)"/>
                </div>
              </div>
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">던전</label>
                  <select v-model="keyForm.dungeon" class="w-full h-10 rounded-full border border-rim/60 px-4 text-sm text-silver focus:outline-none focus:ring-2 focus:ring-wow-legendary/40 transition-all" style="background:var(--bg-input)">
                    <option v-for="d in DUNGEONS" :key="d">{{ d }}</option>
                  </select>
                </div>
                <div>
                  <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">키 레벨</label>
                  <input v-model.number="keyForm.keyLevel" type="number" min="2" max="30" placeholder="10"
                    class="w-full h-10 rounded-full border border-rim/60 px-4 text-sm text-silver placeholder:text-iron focus:outline-none focus:ring-2 focus:ring-wow-legendary/40 transition-all"
                    style="background:var(--bg-input)"/>
                </div>
              </div>
              <div>
                <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">목표</label>
                <div class="grid grid-cols-3 gap-2">
                  <button v-for="[v, l] in [['timer','타이머 인'],['clear','클리어'],['any','상관없음']]" :key="v"
                    type="button"
                    class="h-10 rounded-full border text-xs font-semibold transition-all"
                    :class="keyForm.goal===v?'text-white':'text-steel'"
                    :style="keyForm.goal===v?`background:${goalColor[v]};border-color:${goalColor[v]}`:'background:var(--bg-button);border-color:var(--color-rim)'"
                    @click="keyForm.goal=v">{{ l }}</button>
                </div>
              </div>
              <div>
                <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">모집 인원</label>
                <div class="grid grid-cols-3 gap-3">
                  <div class="text-center">
                    <div class="text-xs text-wow-rare mb-1">탱커</div>
                    <input v-model.number="keyForm.tankSlots" type="number" min="0" max="1" class="w-full h-10 rounded-full border border-rim/60 px-4 text-sm text-silver text-center focus:outline-none focus:ring-2 focus:ring-wow-legendary/40 transition-all" style="background:var(--bg-input)"/>
                  </div>
                  <div class="text-center">
                    <div class="text-xs text-wow-uncommon mb-1">힐러</div>
                    <input v-model.number="keyForm.healSlots" type="number" min="0" max="1" class="w-full h-10 rounded-full border border-rim/60 px-4 text-sm text-silver text-center focus:outline-none focus:ring-2 focus:ring-wow-legendary/40 transition-all" style="background:var(--bg-input)"/>
                  </div>
                  <div class="text-center">
                    <div class="text-xs mb-1" style="color:#ff4646">딜러</div>
                    <input v-model.number="keyForm.dpsSlots" type="number" min="0" max="3" class="w-full h-10 rounded-full border border-rim/60 px-4 text-sm text-silver text-center focus:outline-none focus:ring-2 focus:ring-wow-legendary/40 transition-all" style="background:var(--bg-input)"/>
                  </div>
                </div>
              </div>
              <div class="grid grid-cols-3 gap-3">
                <div>
                  <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">최소 ilvl</label>
                  <input v-model="keyForm.ilvlReq" type="number" placeholder="600" class="w-full h-10 rounded-full border border-rim/60 px-4 text-sm text-silver placeholder:text-iron focus:outline-none focus:ring-2 focus:ring-wow-legendary/40 transition-all" style="background:var(--bg-input)"/>
                </div>
                <div>
                  <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">최소 RIO</label>
                  <input v-model="keyForm.rioReq" type="number" placeholder="선택" class="w-full h-10 rounded-full border border-rim/60 px-4 text-sm text-silver placeholder:text-iron focus:outline-none focus:ring-2 focus:ring-wow-legendary/40 transition-all" style="background:var(--bg-input)"/>
                </div>
                <div>
                  <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">지역</label>
                  <select v-model="keyForm.region" class="w-full h-10 rounded-full border border-rim/60 px-4 text-sm text-silver focus:outline-none focus:ring-2 focus:ring-wow-legendary/40 transition-all" style="background:var(--bg-input)">
                    <option>KR</option><option>US</option><option>EU</option>
                  </select>
                </div>
              </div>
              <div>
                <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">한마디</label>
                <textarea v-model="keyForm.note" rows="2" placeholder="파티 소개, 요구 조건..." class="w-full rounded-2xl border border-rim/60 px-4 py-3 text-sm text-silver placeholder:text-iron resize-none focus:outline-none focus:ring-2 focus:ring-wow-legendary/40 transition-all" style="background:var(--bg-input)"></textarea>
              </div>
              <div class="flex gap-3 pt-2">
                <button type="button" class="flex-1 h-11 rounded-full border border-rim/50 text-sm font-semibold text-steel hover:text-silver transition-all" style="background:var(--bg-button)" @click="showModal=false">취소</button>
                <button type="button" class="flex-1 h-11 rounded-full text-sm font-semibold text-white transition-all hover:-translate-y-0.5" style="background:#ff8000;box-shadow:0 6px 20px rgba(255,128,0,0.3)" @click="submitKey">등록하기</button>
              </div>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>

  <!-- Toast -->
  <Teleport to="body">
    <Transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-2" enter-to-class="opacity-100 translate-y-0"
                leave-active-class="transition-all duration-200 ease-in"  leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-2">
      <div v-if="toast"
           class="fixed bottom-6 left-1/2 -translate-x-1/2 z-[200] px-6 py-3 rounded-full border border-rim/60 text-sm font-semibold text-silver shadow-xl pointer-events-none"
           style="background:var(--bg-button-strong);backdrop-filter:blur(16px)">
        {{ toast }}
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.post-enter-active { transition: all 0.3s ease-out; }
.post-leave-active { transition: all 0.2s ease-in; position: absolute; width: 100%; }
.post-enter-from  { opacity: 0; transform: translateY(-8px); }
.post-leave-to    { opacity: 0; transform: translateY(8px); }
</style>
