<script setup>
import { computed, ref } from 'vue'

/* ── WoW class accent colors ────────────────────────── */
const CLASS_COLORS = {
  'Death Knight': '#C41E3A', 'Demon Hunter': '#A330C9', 'Druid': '#FF7C0A',
  'Evoker': '#33937F',       'Hunter': '#AAD372',       'Mage': '#3FC7EB',
  'Monk': '#00FF98',         'Paladin': '#F48CBA',      'Priest': '#e8e8f0',
  'Rogue': '#FFF468',        'Shaman': '#0070DD',       'Warlock': '#8788EE',
  'Warrior': '#C69B3A',
}

const SPECS = {
  'Death Knight': ['Blood', 'Frost', 'Unholy'],
  'Demon Hunter': ['Havoc', 'Vengeance'],
  'Druid': ['Balance', 'Feral', 'Guardian', 'Restoration'],
  'Evoker': ['Devastation', 'Preservation', 'Augmentation'],
  'Hunter': ['Beast Mastery', 'Marksmanship', 'Survival'],
  'Mage': ['Arcane', 'Fire', 'Frost'],
  'Monk': ['Brewmaster', 'Mistweaver', 'Windwalker'],
  'Paladin': ['Holy', 'Protection', 'Retribution'],
  'Priest': ['Discipline', 'Holy', 'Shadow'],
  'Rogue': ['Assassination', 'Outlaw', 'Subtlety'],
  'Shaman': ['Elemental', 'Enhancement', 'Restoration'],
  'Warlock': ['Affliction', 'Demonology', 'Destruction'],
  'Warrior': ['Arms', 'Fury', 'Protection'],
}

/* ── Mock character data ────────────────────────────── */
const character = ref({
  name: 'Azerothian',
  realm: '데스윙',
  region: 'KR',
  class: 'Death Knight',
  spec: 'Frost',
  role: 'DPS',
  ilvl: 652,
  wclScore: 92.4,
  rioScore: 2847,
  guild: '어둠의 파수꾼',
  achievementPoints: 18_420,
  raidHistory: [
    { raid: '네루바르 궁전',   difficulty: 'Mythic', progress: '9/9',   score: 92.4, date: '2025.03.15', best: true },
    { raid: '아문 타울 니루프', difficulty: 'Heroic', progress: '8/8',   score: 88.1, date: '2025.01.20', best: false },
    { raid: '나트리아 성',      difficulty: 'Mythic', progress: '10/10', score: 71.3, date: '2024.10.05', best: false },
  ],
  mPlus: [
    { dungeon: '아라카라',        bestKey: 18, bestTime: 1823, inTime: true,  score: 312.4 },
    { dungeon: '스레드의 도시',   bestKey: 16, bestTime: 1654, inTime: true,  score: 287.1 },
    { dungeon: '그림 배톨',       bestKey: 15, bestTime: 2105, inTime: false, score: 241.0 },
    { dungeon: '스톤볼트',        bestKey: 17, bestTime: 1980, inTime: true,  score: 298.7 },
    { dungeon: '던브레이커',      bestKey: 14, bestTime: 1433, inTime: true,  score: 256.2 },
    { dungeon: '티르나 시의 안개', bestKey: 16, bestTime: 1521, inTime: true,  score: 281.9 },
    { dungeon: '보랄루스 공성전', bestKey: 13, bestTime: 2234, inTime: false, score: 208.5 },
    { dungeon: '부식 괴멸',       bestKey: 15, bestTime: 1876, inTime: true,  score: 261.3 },
  ],
})

/* ── Computed helpers ───────────────────────────────── */
const classColor  = computed(() => CLASS_COLORS[character.value.class] ?? '#e8e8f0')

function wclColor(score) {
  if (score >= 95) return '#ff8000'
  if (score >= 75) return '#a335ee'
  if (score >= 50) return '#0070dd'
  if (score >= 25) return '#1eff00'
  return '#9d9d9d'
}
function wclLabel(score) {
  if (score >= 95) return 'Legendary'
  if (score >= 75) return 'Epic'
  if (score >= 50) return 'Rare'
  if (score >= 25) return 'Uncommon'
  return 'Common'
}

function rioColor(score) {
  if (score >= 3000) return '#ff8000'
  if (score >= 2500) return '#a335ee'
  if (score >= 2000) return '#0070dd'
  if (score >= 1000) return '#1eff00'
  return '#9d9d9d'
}
function rioLabel(score) {
  if (score >= 3000) return 'Legendary'
  if (score >= 2500) return 'Epic'
  if (score >= 2000) return 'Rare'
  if (score >= 1000) return 'Uncommon'
  return 'Common'
}
function keyColor(lv) {
  if (lv >= 20) return '#ff8000'
  if (lv >= 15) return '#a335ee'
  if (lv >= 10) return '#0070dd'
  return '#6b6b8a'
}
function fmtTime(sec) {
  const m = Math.floor(sec / 60)
  const s = sec % 60
  return `${m}:${String(s).padStart(2, '0')}`
}

const diffColor = { Normal: '#1eff00', Heroic: '#0070dd', Mythic: '#ff8000' }
const diffBg    = { Normal: 'rgba(30,255,0,0.1)', Heroic: 'rgba(0,112,221,0.1)', Mythic: 'rgba(255,128,0,0.1)' }
</script>

<template>
  <section class="px-4 sm:px-6 lg:px-8 py-14">
    <div class="max-w-4xl mx-auto">

      <!-- Demo banner -->
      <div class="flex items-center gap-3 px-5 py-3 rounded-2xl border border-rim/50 mb-8 text-xs text-steel"
           style="background: rgba(22,22,42,0.6)">
        <svg class="w-4 h-4 flex-shrink-0 text-wow-legendary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        데모 프로필입니다. Battle.net OAuth 연동 시 실제 캐릭터 데이터가 표시됩니다.
        <button class="ml-auto flex items-center gap-1.5 text-xs font-semibold text-wow-epic hover:text-wow-epic/80 transition-colors">
          연동하기 →
        </button>
      </div>

      <!-- ── Profile hero card ──────────────────────── -->
      <div class="rounded-[2rem] border border-rim/50 overflow-hidden mb-6"
           style="background: rgba(15,15,26,0.85)">

        <!-- Class color accent bar -->
        <div class="h-1 w-full" :style="`background: linear-gradient(90deg, ${classColor}, transparent)`"></div>

        <div class="p-8 flex flex-col sm:flex-row items-start sm:items-center gap-6">

          <!-- Avatar placeholder -->
          <div class="relative flex-shrink-0">
            <div class="w-24 h-24 rounded-2xl flex items-center justify-center text-3xl font-bold"
                 :style="`background: linear-gradient(135deg, ${classColor}22, ${classColor}11); border: 1px solid ${classColor}33`">
              <span :style="`color: ${classColor}`">{{ character.name[0] }}</span>
            </div>
            <!-- Online dot -->
            <span class="absolute -bottom-1 -right-1 flex h-4 w-4">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-wow-uncommon opacity-50"></span>
              <span class="relative inline-flex rounded-full h-4 w-4 bg-wow-uncommon border-2 border-obsidian"></span>
            </span>
          </div>

          <!-- Name / class / guild -->
          <div class="flex-1 min-w-0">
            <div class="flex flex-wrap items-center gap-2 mb-1">
              <h1 class="text-3xl font-bold tracking-tight" :style="`color: ${classColor}`">
                {{ character.name }}
              </h1>
              <span class="text-steel text-lg font-light">-</span>
              <span class="text-steel text-base">{{ character.realm }}</span>
            </div>
            <div class="flex flex-wrap items-center gap-2 mb-3 text-sm text-steel">
              <span :style="`color: ${classColor}`">{{ character.spec }} {{ character.class }}</span>
              <span class="text-iron">·</span>
              <span>{{ character.guild }}</span>
              <span class="text-iron">·</span>
              <span>{{ character.region }}</span>
            </div>
            <div class="flex flex-wrap gap-2">
              <span class="px-2.5 py-1 rounded-full text-xs font-semibold border"
                    :style="`color: ${classColor}; border-color: ${classColor}33; background: ${classColor}11`">
                {{ character.role }}
              </span>
              <span class="px-2.5 py-1 rounded-full text-xs font-semibold border border-rim/50 text-steel"
                    style="background: rgba(22,22,42,0.8)">
                ilvl {{ character.ilvl }}
              </span>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex flex-col gap-2">
            <RouterLink to="/matching"
              class="flex items-center justify-center gap-2 h-10 px-5 rounded-full text-sm font-semibold text-white transition-all hover:-translate-y-0.5"
              style="background: #a335ee; box-shadow: 0 4px 16px rgba(163,53,238,0.3)">
              매칭 시작
            </RouterLink>
            <RouterLink to="/lfg"
              class="flex items-center justify-center h-10 px-5 rounded-full text-sm font-semibold text-steel border border-rim/60
                     hover:text-silver hover:border-rim transition-all"
              style="background: rgba(22,22,42,0.8)">
              공대 찾기
            </RouterLink>
          </div>
        </div>
      </div>

      <!-- ── Stat cards ─────────────────────────────── -->
      <div class="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">

        <!-- ilvl -->
        <div class="rounded-2xl border border-rim/50 p-5 text-center"
             style="background: rgba(15,15,26,0.8)">
          <div class="text-xs font-semibold tracking-widest uppercase text-iron mb-2">아이템 레벨</div>
          <div class="text-3xl font-bold text-silver">{{ character.ilvl }}</div>
          <div class="text-xs text-steel mt-1">Season Average</div>
        </div>

        <!-- WCL Score -->
        <div class="rounded-2xl border p-5 text-center"
             :style="`background: rgba(15,15,26,0.8); border-color: ${wclColor(character.wclScore)}22`">
          <div class="text-xs font-semibold tracking-widest uppercase text-iron mb-2">WCL 점수</div>
          <div class="text-3xl font-bold" :style="`color: ${wclColor(character.wclScore)}`">
            {{ character.wclScore.toFixed(1) }}
          </div>
          <div class="text-xs mt-1 font-semibold" :style="`color: ${wclColor(character.wclScore)}`">
            {{ wclLabel(character.wclScore) }}
          </div>
        </div>

        <!-- RIO Score -->
        <div class="rounded-2xl border p-5 text-center"
             :style="`background: rgba(15,15,26,0.8); border-color: ${rioColor(character.rioScore)}22`">
          <div class="text-xs font-semibold tracking-widest uppercase text-iron mb-2">RIO 점수</div>
          <div class="text-3xl font-bold" :style="`color: ${rioColor(character.rioScore)}`">
            {{ character.rioScore.toLocaleString() }}
          </div>
          <div class="text-xs mt-1 font-semibold" :style="`color: ${rioColor(character.rioScore)}`">
            {{ rioLabel(character.rioScore) }}
          </div>
        </div>

        <!-- Role -->
        <div class="rounded-2xl border border-rim/50 p-5 text-center"
             style="background: rgba(15,15,26,0.8)">
          <div class="text-xs font-semibold tracking-widest uppercase text-iron mb-2">역할</div>
          <div class="text-3xl font-bold" :style="`color: ${classColor}`">
            {{ character.role }}
          </div>
          <div class="text-xs text-steel mt-1">{{ character.spec }}</div>
        </div>

        <!-- Achievements -->
        <div class="rounded-2xl border border-rim/50 p-5 text-center"
             style="background: rgba(15,15,26,0.8)">
          <div class="text-xs font-semibold tracking-widest uppercase text-iron mb-2">업적 점수</div>
          <div class="text-3xl font-bold text-silver">
            {{ character.achievementPoints.toLocaleString() }}
          </div>
          <div class="text-xs text-steel mt-1">Points</div>
        </div>

      </div>

      <!-- ── Raid history ────────────────────────────── -->
      <div class="rounded-[2rem] border border-rim/50 overflow-hidden"
           style="background: rgba(15,15,26,0.8)">

        <div class="px-6 py-4 border-b border-rim/40">
          <div class="text-sm font-semibold text-silver">레이드 기록</div>
          <div class="text-xs text-steel mt-0.5">최근 클리어 기준</div>
        </div>

        <div class="overflow-x-auto">
          <table class="min-w-full text-left">
            <thead>
              <tr class="text-xs uppercase tracking-widest text-iron border-b border-rim/30"
                  style="background: rgba(8,8,16,0.5)">
                <th class="px-6 py-3 font-semibold">레이드</th>
                <th class="px-6 py-3 font-semibold">난이도</th>
                <th class="px-6 py-3 font-semibold">진행도</th>
                <th class="px-6 py-3 font-semibold">최고 점수</th>
                <th class="px-6 py-3 font-semibold">날짜</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in character.raidHistory" :key="row.raid + row.difficulty"
                  class="border-b border-rim/20 transition-colors hover:bg-shadow/40">
                <td class="px-6 py-4">
                  <div class="text-sm font-semibold text-silver flex items-center gap-2">
                    {{ row.raid }}
                    <span v-if="row.best"
                          class="text-[10px] font-semibold px-1.5 py-0.5 rounded-full"
                          style="background:rgba(255,128,0,0.12); color:#ff8000">
                      Best
                    </span>
                  </div>
                </td>
                <td class="px-6 py-4">
                  <span class="text-xs font-semibold px-2.5 py-1 rounded-full"
                        :style="`background:${diffBg[row.difficulty]}; color:${diffColor[row.difficulty]}`">
                    {{ row.difficulty }}
                  </span>
                </td>
                <td class="px-6 py-4">
                  <span class="text-sm font-semibold"
                        :style="row.progress.split('/')[0] === row.progress.split('/')[1] ? 'color:#1eff00' : 'color:#a335ee'">
                    {{ row.progress }}
                  </span>
                </td>
                <td class="px-6 py-4">
                  <span class="text-sm font-bold tabular-nums" :style="`color:${wclColor(row.score)}`">
                    {{ row.score.toFixed(1) }}
                  </span>
                  <span class="ml-1.5 text-xs" :style="`color:${wclColor(row.score)}`">
                    {{ wclLabel(row.score) }}
                  </span>
                </td>
                <td class="px-6 py-4 text-sm text-iron tabular-nums">{{ row.date }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- WCL link placeholder -->
        <div class="px-6 py-4 border-t border-rim/30 flex items-center justify-between">
          <div class="text-xs text-iron">Battle.net 연동 후 실제 데이터가 자동으로 갱신됩니다.</div>
          <a href="https://www.warcraftlogs.com" target="_blank" rel="noopener"
             class="flex items-center gap-1.5 text-xs font-semibold text-steel hover:text-wow-epic transition-colors">
            Warcraft Logs 보기
            <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
            </svg>
          </a>
        </div>
      </div>

      <!-- ── M+ 기록 ────────────────────────────────── -->
      <div class="rounded-[2rem] border border-rim/50 overflow-hidden mt-6"
           style="background: rgba(15,15,26,0.8)">
        <div class="px-6 py-4 border-b border-rim/40 flex items-center justify-between">
          <div>
            <div class="flex items-center gap-2">
              <svg class="w-4 h-4" style="color:#ff8000" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round"
                      d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/>
              </svg>
              <div class="text-sm font-semibold text-silver">Mythic+ 기록</div>
            </div>
            <div class="text-xs text-steel mt-0.5">시즌 최고 기록 · RIO 점수 기준</div>
          </div>
          <div class="text-right">
            <div class="text-xl font-bold" :style="`color:${rioColor(character.rioScore)}`">
              {{ character.rioScore.toLocaleString() }}
            </div>
            <div class="text-xs font-semibold" :style="`color:${rioColor(character.rioScore)}`">
              {{ rioLabel(character.rioScore) }} RIO
            </div>
          </div>
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full text-left">
            <thead>
              <tr class="text-xs uppercase tracking-widest text-iron border-b border-rim/30"
                  style="background: rgba(8,8,16,0.5)">
                <th class="px-6 py-3 font-semibold">던전</th>
                <th class="px-6 py-3 font-semibold text-center">최고 키</th>
                <th class="px-6 py-3 font-semibold text-center">타이머</th>
                <th class="px-6 py-3 font-semibold text-right">최고 시간</th>
                <th class="px-6 py-3 font-semibold text-right">점수</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in character.mPlus" :key="row.dungeon"
                  class="border-b border-rim/20 transition-colors hover:bg-shadow/40">
                <td class="px-6 py-3 text-sm font-medium text-silver">{{ row.dungeon }}</td>
                <td class="px-6 py-3 text-center">
                  <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-bold"
                        :style="`background:${keyColor(row.bestKey)}18;color:${keyColor(row.bestKey)}`">
                    +{{ row.bestKey }}
                  </span>
                </td>
                <td class="px-6 py-3 text-center">
                  <span class="text-xs font-semibold" :style="row.inTime?'color:#1eff00':'color:#ff4646'">
                    {{ row.inTime ? '인타임' : '시간초과' }}
                  </span>
                </td>
                <td class="px-6 py-3 text-sm text-steel tabular-nums text-right">{{ fmtTime(row.bestTime) }}</td>
                <td class="px-6 py-3 text-right">
                  <span class="text-sm font-bold tabular-nums"
                        :style="`color:${rioColor(row.score * 10)}`">
                    {{ row.score.toFixed(1) }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="px-6 py-4 border-t border-rim/30">
          <div class="text-xs text-iron">Raider.IO API · Battle.net OAuth 연동 후 실제 데이터가 자동 갱신됩니다.</div>
        </div>
      </div>

    </div>
  </section>
</template>
