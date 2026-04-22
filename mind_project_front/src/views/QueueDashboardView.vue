<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'

/* ── Queue state ──────────────────────────────────────── */
const q = ref({ tank: 8, heal: 12, dps: 27, kr: 31, us: 10, eu: 6 })
const matchesToday = ref(183)
const flash = ref(null)   // key of element flashing

const avgWait = { tank: '1분 12초', heal: '2분 45초', dps: '4분 38초' }

const total = computed(() => q.value.tank + q.value.heal + q.value.dps)
const pct   = (v) => total.value ? Math.round(v / total.value * 100) : 0

/* ── Event feed ───────────────────────────────────────── */
const ROLES    = ['DPS', 'DPS', 'DPS', 'HEAL', 'TANK']
const REGIONS  = ['KR', 'KR', 'KR', 'US', 'EU']
const SIZES    = [10, 20, 25]
const WAITS    = ['0분 32초', '1분 07초', '2분 15초', '3분 44초', '0분 58초', '4분 03초']

let eid = 100
const events = ref([
  { id: eid++, role: 'DPS',  region: 'KR', size: 20, wait: '2분 34초', age: 0 },
  { id: eid++, role: 'HEAL', region: 'KR', size: 10, wait: '1분 52초', age: 1 },
  { id: eid++, role: 'TANK', region: 'US', size: 25, wait: '0분 47초', age: 2 },
  { id: eid++, role: 'DPS',  region: 'EU', size: 20, wait: '3분 15초', age: 4 },
  { id: eid++, role: 'DPS',  region: 'KR', size: 10, wait: '4분 02초', age: 6 },
])

function rand(arr) { return arr[Math.floor(Math.random() * arr.length)] }
function nudge(v, d = 2) { return Math.max(0, v + Math.floor((Math.random() - 0.4) * d)) }
function flashKey(key) {
  flash.value = key
  setTimeout(() => { flash.value = null }, 500)
}

let simTimer = null
let matchTimer = null

function simulate() {
  const before = total.value
  q.value.tank = nudge(q.value.tank, 2)
  q.value.heal = nudge(q.value.heal, 2)
  q.value.dps  = nudge(q.value.dps, 3)
  q.value.kr   = nudge(q.value.kr, 2)
  q.value.us   = nudge(q.value.us, 1)
  q.value.eu   = nudge(q.value.eu, 1)
  if (total.value !== before) flashKey('total')
}

function addMatch() {
  events.value.forEach(e => { e.age++ })
  events.value.unshift({ id: eid++, role: rand(ROLES), region: rand(REGIONS), size: rand(SIZES), wait: rand(WAITS), age: 0 })
  if (events.value.length > 7) events.value.pop()
  matchesToday.value++
  flashKey('today')
}

onMounted(() => {
  simTimer   = setInterval(simulate, 2000)
  matchTimer = setInterval(addMatch, 4500)
})
onUnmounted(() => { clearInterval(simTimer); clearInterval(matchTimer) })

/* ── Helpers ──────────────────────────────────────────── */
const ROLE_COLOR = { DPS: '#ff4646', HEAL: '#1eff00', TANK: '#0070dd' }
const ROLE_BG    = { DPS: 'rgba(255,70,70,0.12)', HEAL: 'rgba(30,255,0,0.1)', TANK: 'rgba(0,112,221,0.1)' }
const ROLE_KR    = { DPS: '딜러', HEAL: '힐러', TANK: '탱커' }

function ageLabel(age) {
  if (age === 0) return '방금 전'
  return `${age * Math.ceil(4.5 / 60)}분 전`  // rough
}
</script>

<template>
  <section class="px-4 sm:px-6 lg:px-8 py-14">
    <div class="max-w-5xl mx-auto">

      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4 mb-8">
        <div>
          <h1 class="text-4xl md:text-5xl font-bold tracking-tighter text-silver">실시간 대기열</h1>
          <p class="mt-2 text-steel text-base">지금 이 순간 대기 중인 플레이어 현황.</p>
        </div>
        <!-- Status badge -->
        <div class="inline-flex items-center gap-2.5 px-4 py-2 rounded-full border border-rim/50 text-xs font-medium text-steel"
             style="background: rgba(15,15,26,0.8)">
          <span class="relative flex h-2 w-2">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-wow-uncommon opacity-60"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-wow-uncommon"></span>
          </span>
          시뮬레이션 모드 · WebSocket 연결 대기
        </div>
      </div>

      <!-- ── Top stats row ────────────────────────────── -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">

        <!-- Total -->
        <div class="md:col-span-1 rounded-2xl border border-rim/50 p-5 text-center relative overflow-hidden"
             style="background: rgba(15,15,26,0.85)">
          <div class="absolute inset-0 pointer-events-none"
               style="background: radial-gradient(ellipse at 50% 0%, rgba(163,53,238,0.06), transparent 70%)"></div>
          <div class="text-xs font-semibold tracking-widest uppercase text-iron mb-2">대기 중</div>
          <div class="text-5xl font-bold text-silver tabular-nums transition-colors duration-300"
               :class="flash === 'total' ? 'text-wow-epic' : ''">
            {{ total }}
          </div>
          <div class="text-xs text-steel mt-1">명</div>
        </div>

        <!-- Today's matches -->
        <div class="rounded-2xl border border-rim/50 p-5 text-center"
             style="background: rgba(15,15,26,0.85)">
          <div class="text-xs font-semibold tracking-widest uppercase text-iron mb-2">오늘 매칭</div>
          <div class="text-5xl font-bold tabular-nums transition-colors duration-300"
               :class="flash === 'today' ? 'text-wow-legendary' : 'text-silver'"
               :style="flash === 'today' ? 'color:#ff8000' : ''">
            {{ matchesToday }}
          </div>
          <div class="text-xs text-steel mt-1">건</div>
        </div>

        <!-- Tank avg wait -->
        <div class="rounded-2xl border border-rim/50 p-5 text-center"
             style="background: rgba(15,15,26,0.85)">
          <div class="text-xs font-semibold tracking-widest uppercase text-iron mb-2">탱커 예상 대기</div>
          <div class="text-2xl font-bold text-wow-rare">{{ avgWait.tank }}</div>
          <div class="text-xs text-steel mt-1">평균</div>
        </div>

        <!-- DPS avg wait -->
        <div class="rounded-2xl border border-rim/50 p-5 text-center"
             style="background: rgba(15,15,26,0.85)">
          <div class="text-xs font-semibold tracking-widest uppercase text-iron mb-2">딜러 예상 대기</div>
          <div class="text-2xl font-bold" style="color:#ff4646">{{ avgWait.dps }}</div>
          <div class="text-xs text-steel mt-1">평균</div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-5 gap-6">

        <!-- ── Role breakdown ──────────────────────── -->
        <div class="lg:col-span-3 rounded-[2rem] border border-rim/50 p-7"
             style="background: rgba(15,15,26,0.8)">
          <div class="text-sm font-semibold text-silver mb-6">역할별 현황</div>

          <div class="flex flex-col gap-5">
            <!-- Tank -->
            <div>
              <div class="flex items-center justify-between mb-2">
                <div class="flex items-center gap-2">
                  <span class="w-7 h-7 rounded-lg flex items-center justify-center"
                        style="background: rgba(0,112,221,0.15)">
                    <svg class="w-4 h-4" style="color:#0070dd" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M12 2L3 7v5c0 5.25 3.75 10.15 9 11.35C17.25 22.15 21 17.25 21 12V7l-9-5z"/>
                    </svg>
                  </span>
                  <span class="text-sm font-semibold text-silver">탱커</span>
                </div>
                <div class="flex items-baseline gap-1.5">
                  <span class="text-2xl font-bold tabular-nums text-silver">{{ q.tank }}</span>
                  <span class="text-xs text-steel">명 · {{ pct(q.tank) }}%</span>
                </div>
              </div>
              <div class="h-2 rounded-full overflow-hidden" style="background: rgba(42,42,74,0.6)">
                <div class="h-full rounded-full transition-all duration-700"
                     :style="`width:${pct(q.tank)}%; background:#0070dd`"></div>
              </div>
              <div class="mt-1 text-xs text-steel">예상 대기 {{ avgWait.tank }}</div>
            </div>

            <!-- Heal -->
            <div>
              <div class="flex items-center justify-between mb-2">
                <div class="flex items-center gap-2">
                  <span class="w-7 h-7 rounded-lg flex items-center justify-center"
                        style="background: rgba(30,255,0,0.1)">
                    <svg class="w-4 h-4" style="color:#1eff00" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/>
                    </svg>
                  </span>
                  <span class="text-sm font-semibold text-silver">힐러</span>
                </div>
                <div class="flex items-baseline gap-1.5">
                  <span class="text-2xl font-bold tabular-nums text-silver">{{ q.heal }}</span>
                  <span class="text-xs text-steel">명 · {{ pct(q.heal) }}%</span>
                </div>
              </div>
              <div class="h-2 rounded-full overflow-hidden" style="background: rgba(42,42,74,0.6)">
                <div class="h-full rounded-full transition-all duration-700"
                     :style="`width:${pct(q.heal)}%; background:#1eff00`"></div>
              </div>
              <div class="mt-1 text-xs text-steel">예상 대기 {{ avgWait.heal }}</div>
            </div>

            <!-- DPS -->
            <div>
              <div class="flex items-center justify-between mb-2">
                <div class="flex items-center gap-2">
                  <span class="w-7 h-7 rounded-lg flex items-center justify-center"
                        style="background: rgba(255,70,70,0.12)">
                    <svg class="w-4 h-4" style="color:#ff4646" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M14.5 10L21 3m0 0h-6m6 0v6M10 14l-7 7m0 0h6m-6 0v-6"/>
                    </svg>
                  </span>
                  <span class="text-sm font-semibold text-silver">딜러</span>
                </div>
                <div class="flex items-baseline gap-1.5">
                  <span class="text-2xl font-bold tabular-nums text-silver">{{ q.dps }}</span>
                  <span class="text-xs text-steel">명 · {{ pct(q.dps) }}%</span>
                </div>
              </div>
              <div class="h-2 rounded-full overflow-hidden" style="background: rgba(42,42,74,0.6)">
                <div class="h-full rounded-full transition-all duration-700"
                     :style="`width:${pct(q.dps)}%; background:#ff4646`"></div>
              </div>
              <div class="mt-1 text-xs text-steel">예상 대기 {{ avgWait.dps }}</div>
            </div>

            <!-- Divider -->
            <div class="border-t border-rim/30 pt-5">
              <div class="text-xs font-semibold text-iron uppercase tracking-widest mb-4">지역별</div>
              <div class="flex flex-col gap-3">
                <div v-for="[key, label, val] in [['kr','KR',q.kr],['us','US',q.us],['eu','EU',q.eu]]" :key="key">
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-xs font-semibold text-steel">{{ label }}</span>
                    <span class="text-xs text-iron tabular-nums">{{ val }}명</span>
                  </div>
                  <div class="h-1.5 rounded-full overflow-hidden" style="background: rgba(42,42,74,0.6)">
                    <div class="h-full rounded-full transition-all duration-700 bg-wow-epic"
                         :style="`width:${pct(val)}%`"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ── Recent match feed ───────────────────── -->
        <div class="lg:col-span-2 rounded-[2rem] border border-rim/50 p-7 flex flex-col"
             style="background: rgba(15,15,26,0.8)">
          <div class="flex items-center justify-between mb-6">
            <div class="text-sm font-semibold text-silver">최근 매칭</div>
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-wow-uncommon opacity-60"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-wow-uncommon"></span>
            </span>
          </div>

          <div class="flex flex-col gap-3 flex-1">
            <TransitionGroup name="feed">
              <div v-for="ev in events" :key="ev.id"
                   class="flex items-center gap-3 p-3 rounded-2xl border border-rim/30 transition-all"
                   style="background: rgba(22,22,42,0.6)">
                <!-- Role badge -->
                <span class="w-8 h-8 flex-shrink-0 rounded-xl flex items-center justify-center text-[10px] font-bold"
                      :style="`background:${ROLE_BG[ev.role]}; color:${ROLE_COLOR[ev.role]}`">
                  {{ ev.role[0] }}
                </span>
                <div class="flex-1 min-w-0">
                  <div class="text-xs font-semibold text-silver">
                    {{ ROLE_KR[ev.role] }} · {{ ev.size }}인 · {{ ev.region }}
                  </div>
                  <div class="text-[11px] text-iron mt-0.5">대기 {{ ev.wait }}</div>
                </div>
                <div class="text-[10px] text-iron flex-shrink-0">
                  {{ ev.age === 0 ? '방금' : ev.age + '분 전' }}
                </div>
              </div>
            </TransitionGroup>
          </div>

          <div class="mt-6 pt-5 border-t border-rim/30">
            <RouterLink to="/matching"
              class="flex items-center justify-center gap-2 w-full h-10 rounded-full text-sm font-semibold text-white transition-all hover:-translate-y-0.5"
              style="background: #a335ee; box-shadow: 0 4px 16px rgba(163,53,238,0.3)">
              큐 참가하기
            </RouterLink>
          </div>
        </div>

      </div>

      <p class="mt-6 text-xs text-iron text-center">
        실제 서비스에서는 WebSocket으로 실시간 업데이트됩니다. 현재는 시뮬레이션 데이터입니다.
      </p>
    </div>
  </section>
</template>

<style scoped>
.feed-enter-active { transition: all 0.35s ease-out; }
.feed-leave-active { transition: all 0.2s ease-in; position: absolute; width: 100%; }
.feed-enter-from  { opacity: 0; transform: translateY(-12px); }
.feed-leave-to    { opacity: 0; transform: translateY(8px); }
</style>
