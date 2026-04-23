<script setup>
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const guildName = computed(() => decodeURIComponent(route.params.name ?? '어둠의 파수꾼'))

/* ── Mock data (demo) ─────────────────────────────────── */
const guild = ref({
  realm: '데스윙', region: 'KR',
  difficulty: 'Mythic', progress: '9/9',
  rank: 1, score: 4523, memberCount: 28,
  raidSchedule: '월 · 수 · 금   21:00 ~ 24:00',
  bosses: [
    { name: 'Ulgrax the Devourer',         cleared: true,  bestTime: 187, pulls: 12,  date: '2025.01.15', wclId: '1' },
    { name: 'The Bloodbound Horror',        cleared: true,  bestTime: 234, pulls: 28,  date: '2025.01.22', wclId: '2' },
    { name: 'Sikran, Captain of Sureki',    cleared: true,  bestTime: 198, pulls: 41,  date: '2025.02.01', wclId: '3' },
    { name: "Rasha'nan",                    cleared: true,  bestTime: 312, pulls: 67,  date: '2025.02.12', wclId: '4' },
    { name: "Eggtender Ovi'nax",            cleared: true,  bestTime: 278, pulls: 89,  date: '2025.02.19', wclId: '5' },
    { name: 'Nexus-Princess Ky\'veza',      cleared: true,  bestTime: 401, pulls: 134, date: '2025.03.01', wclId: '6' },
    { name: 'The Silken Court',             cleared: true,  bestTime: 356, pulls: 178, date: '2025.03.08', wclId: '7' },
    { name: 'Queen Ansurek',                cleared: true,  bestTime: 523, pulls: 247, date: '2025.03.15', wclId: '8' },
    { name: '궁전의 지배자 (Extension)',     cleared: false, bestTime: null, pulls: 34, date: null,         wclId: null },
  ],
  composition: {
    tank: 2, heal: 5, dps: 21,
    classes: [
      { name: 'Warrior',      count: 3, color: '#C69B3A' },
      { name: 'Druid',        count: 3, color: '#FF7C0A' },
      { name: 'Mage',         count: 3, color: '#3FC7EB' },
      { name: 'Death Knight', count: 2, color: '#C41E3A' },
      { name: 'Paladin',      count: 2, color: '#F48CBA' },
      { name: 'Hunter',       count: 2, color: '#AAD372' },
      { name: 'Rogue',        count: 2, color: '#FFF468' },
      { name: 'Warlock',      count: 2, color: '#8788EE' },
      { name: 'Shaman',       count: 2, color: '#0070DD' },
      { name: 'Demon Hunter', count: 2, color: '#A330C9' },
      { name: 'Monk',         count: 2, color: '#00FF98' },
      { name: 'Evoker',       count: 1, color: '#33937F' },
    ],
  },
})

/* ── Helpers ──────────────────────────────────────────── */
function fmtTime(sec) {
  if (!sec) return '—'
  const m = Math.floor(sec / 60)
  const s = sec % 60
  return `${m}:${String(s).padStart(2, '0')}`
}

const diffColor = { Normal: '#1eff00', Heroic: '#0070dd', Mythic: '#ff8000' }
const diffBg    = { Normal: 'rgba(30,255,0,0.1)', Heroic: 'rgba(0,112,221,0.1)', Mythic: 'rgba(255,128,0,0.1)' }

const clearedCount = computed(() => guild.value.bosses.filter(b => b.cleared).length)
const totalBosses  = computed(() => guild.value.bosses.length)
</script>

<template>
  <section class="px-4 sm:px-6 lg:px-8 py-14">
    <div class="max-w-5xl mx-auto">

      <!-- Back link -->
      <RouterLink to="/raid-rankings"
        class="inline-flex items-center gap-1.5 text-xs font-medium text-steel hover:text-silver transition-colors mb-6">
        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/>
        </svg>
        랭킹으로 돌아가기
      </RouterLink>

      <!-- Demo banner -->
      <div class="flex items-center gap-3 px-5 py-3 rounded-2xl border border-rim/50 mb-6 text-xs text-steel"
           style="background: var(--bg-button-dim)">
        <svg class="w-4 h-4 flex-shrink-0 text-wow-legendary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        데모 데이터입니다. Warcraft Logs API 연동 시 실제 길드 데이터가 표시됩니다.
      </div>

      <!-- ── Guild hero card ─────────────────────────── -->
      <div class="rounded-[2rem] border border-rim/50 overflow-hidden mb-6"
           style="background: var(--bg-card-strong)">
        <div class="h-1 w-full" style="background: linear-gradient(90deg, #ff8000, #a335ee, transparent)"></div>

        <div class="p-8 flex flex-col sm:flex-row items-start sm:items-center gap-6">
          <!-- Guild icon placeholder -->
          <div class="w-20 h-20 rounded-2xl flex items-center justify-center text-2xl font-bold flex-shrink-0"
               style="background: linear-gradient(135deg, rgba(255,128,0,0.15), rgba(163,53,238,0.15));
                      border: 1px solid rgba(255,128,0,0.2)">
            <svg class="w-9 h-9" style="color:#ff8000" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round"
                    d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
          </div>

          <!-- Guild info -->
          <div class="flex-1 min-w-0">
            <div class="flex flex-wrap items-center gap-2 mb-1">
              <h1 class="text-3xl font-bold tracking-tight text-silver">{{ guildName }}</h1>
              <span class="px-2.5 py-0.5 rounded-full text-xs font-bold"
                    :style="`background:${diffBg[guild.difficulty]}; color:${diffColor[guild.difficulty]}`">
                {{ guild.difficulty }}
              </span>
            </div>
            <div class="text-sm text-steel mb-3">
              {{ guild.realm }} · {{ guild.region }}
            </div>
            <div class="flex flex-wrap gap-2">
              <span class="px-3 py-1 rounded-full text-xs font-semibold border border-rim/50 text-steel"
                    style="background: var(--bg-button)">
                🏆 {{ guild.rank }}위
              </span>
              <span class="px-3 py-1 rounded-full text-xs font-semibold"
                    style="background: rgba(255,128,0,0.1); color:#ff8000">
                {{ guild.score.toLocaleString() }}점
              </span>
              <span class="px-3 py-1 rounded-full text-xs font-semibold border border-rim/50 text-steel"
                    style="background: var(--bg-button)">
                {{ guild.memberCount }}명
              </span>
              <span class="px-3 py-1 rounded-full text-xs font-semibold border border-rim/50 text-steel"
                    style="background: var(--bg-button)">
                {{ guild.raidSchedule }}
              </span>
            </div>
          </div>

          <!-- Progress ring (text) -->
          <div class="text-center flex-shrink-0">
            <div class="text-4xl font-bold tabular-nums"
                 :style="clearedCount === totalBosses ? 'color:#1eff00' : 'color:#a335ee'">
              {{ clearedCount }}/{{ totalBosses }}
            </div>
            <div class="text-xs text-steel mt-1">보스 클리어</div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

        <!-- ── Boss table ────────────────────────────── -->
        <div class="lg:col-span-2 rounded-[2rem] border border-rim/50 overflow-hidden"
             style="background: var(--bg-card)">

          <div class="px-6 py-4 border-b border-rim/40">
            <div class="text-sm font-semibold text-silver">보스 진행도</div>
            <div class="text-xs text-steel mt-0.5">{{ guild.difficulty }} 기준 · 베스트 타임</div>
          </div>

          <div class="overflow-x-auto">
            <table class="min-w-full text-left">
              <thead>
                <tr class="text-xs uppercase tracking-widest text-iron border-b border-rim/30"
                    style="background: var(--bg-header)">
                  <th class="px-5 py-3 font-semibold w-8">#</th>
                  <th class="px-5 py-3 font-semibold">보스</th>
                  <th class="px-5 py-3 font-semibold text-right">베스트</th>
                  <th class="px-5 py-3 font-semibold text-right">시도</th>
                  <th class="px-5 py-3 font-semibold text-right">날짜</th>
                  <th class="px-5 py-3 font-semibold text-center">WCL</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(boss, i) in guild.bosses" :key="boss.name"
                    class="border-b border-rim/20 transition-colors hover:bg-shadow/40">

                  <!-- Index -->
                  <td class="px-5 py-4 text-sm text-iron tabular-nums">{{ i + 1 }}</td>

                  <!-- Boss name + cleared indicator -->
                  <td class="px-5 py-4">
                    <div class="flex items-center gap-2.5">
                      <span class="w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0"
                            :style="boss.cleared
                              ? 'background:rgba(30,255,0,0.12)'
                              : 'background:var(--bg-dim)'">
                        <svg v-if="boss.cleared" class="w-3 h-3" style="color:#1eff00"
                             viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
                        </svg>
                        <span v-else class="w-1.5 h-1.5 rounded-full bg-iron"></span>
                      </span>
                      <span class="text-sm font-medium"
                            :class="boss.cleared ? 'text-silver' : 'text-steel'">
                        {{ boss.name }}
                      </span>
                    </div>
                  </td>

                  <!-- Best time -->
                  <td class="px-5 py-4 text-sm tabular-nums text-right"
                      :class="boss.cleared ? 'text-silver font-medium' : 'text-iron'">
                    {{ fmtTime(boss.bestTime) }}
                  </td>

                  <!-- Pulls -->
                  <td class="px-5 py-4 text-sm tabular-nums text-right text-steel">
                    {{ boss.pulls }}회
                  </td>

                  <!-- Date -->
                  <td class="px-5 py-4 text-xs tabular-nums text-right text-iron">
                    {{ boss.date ?? '—' }}
                  </td>

                  <!-- WCL link -->
                  <td class="px-5 py-4 text-center">
                    <a v-if="boss.wclId"
                       href="https://www.warcraftlogs.com" target="_blank" rel="noopener"
                       class="inline-flex items-center gap-1 text-xs font-medium text-steel hover:text-wow-epic transition-colors">
                      <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round"
                              d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                      </svg>
                      Log
                    </a>
                    <span v-else class="text-iron text-xs">—</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- ── Composition sidebar ─────────────────── -->
        <div class="flex flex-col gap-4">

          <!-- Role breakdown -->
          <div class="rounded-[1.5rem] border border-rim/50 p-6"
               style="background: var(--bg-card)">
            <div class="text-sm font-semibold text-silver mb-5">공대 구성</div>
            <div class="flex flex-col gap-3">
              <div v-for="[label, val, color, bg] in [
                     ['탱커', guild.composition.tank, '#0070dd', 'rgba(0,112,221,0.1)'],
                     ['힐러', guild.composition.heal, '#1eff00', 'rgba(30,255,0,0.1)'],
                     ['딜러', guild.composition.dps,  '#ff4646', 'rgba(255,70,70,0.1)'],
                   ]" :key="label">
                <div class="flex items-center justify-between mb-1">
                  <span class="text-xs font-semibold text-steel">{{ label }}</span>
                  <span class="text-xs font-bold" :style="`color:${color}`">{{ val }}명</span>
                </div>
                <div class="h-1.5 rounded-full overflow-hidden" style="background: var(--bg-bar-track)">
                  <div class="h-full rounded-full"
                       :style="`width:${Math.round(val/guild.memberCount*100)}%; background:${color}`"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Class distribution -->
          <div class="rounded-[1.5rem] border border-rim/50 p-6 flex-1"
               style="background: var(--bg-card)">
            <div class="text-sm font-semibold text-silver mb-5">클래스 분포</div>
            <div class="flex flex-col gap-2.5">
              <div v-for="cls in guild.composition.classes" :key="cls.name"
                   class="flex items-center gap-2.5">
                <!-- Class color dot -->
                <span class="w-2 h-2 rounded-full flex-shrink-0"
                      :style="`background:${cls.color}`"></span>
                <span class="text-xs text-steel flex-1 truncate">{{ cls.name }}</span>
                <!-- Count bar -->
                <div class="flex items-center gap-1.5">
                  <div class="w-16 h-1 rounded-full overflow-hidden" style="background: var(--bg-bar-track)">
                    <div class="h-full rounded-full"
                         :style="`width:${Math.round(cls.count/guild.memberCount*100)}%; background:${cls.color}`"></div>
                  </div>
                  <span class="text-xs font-semibold w-3 text-right tabular-nums"
                        :style="`color:${cls.color}`">{{ cls.count }}</span>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>

      <div class="mt-6 text-xs text-iron text-center">
        Warcraft Logs API · Battle.net OAuth 연동 후 실제 데이터가 자동 갱신됩니다.
      </div>
    </div>
  </section>
</template>
