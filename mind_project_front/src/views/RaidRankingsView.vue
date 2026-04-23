<script setup>
import { computed, onMounted, ref, watch } from 'vue'

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '')

function apiUrl (path) {
  const normalizedPath = path.startsWith('/') ? path : `/${path}`
  if (!API_BASE_URL) return normalizedPath

  const baseHasApiSuffix = API_BASE_URL.endsWith('/api')
  const pathHasApiPrefix = normalizedPath.startsWith('/api/') || normalizedPath === '/api'

  if (baseHasApiSuffix && pathHasApiPrefix) {
    return `${API_BASE_URL}${normalizedPath.replace(/^\/api/, '')}`
  }

  return `${API_BASE_URL}${normalizedPath}`
}

async function fetchRaids ({ page, size, sort }) {
  const qs = new URLSearchParams({
    page: String(page),
    size: String(size),
  })

  if (sort) {
    qs.set('sort', sort)
  }

  const response = await fetch(`${apiUrl('/api/raids')}?${qs.toString()}`)
  if (!response.ok) {
    throw new Error(`Failed to fetch raids: ${response.status}`)
  }
  const data = await response.json()
  return data
}

const raids = ref([])
const isLoading = ref(true)
const errorMessage = ref('')

const serverTotalPages = ref(1)
const serverTotalElements = ref(0)

const pageSize = ref(10)
const currentPage = ref(1)

const scoreSortDir = ref('none')

const scoreSortParam = computed(() => {
  if (scoreSortDir.value === 'asc') return 'score,ASC'
  if (scoreSortDir.value === 'desc') return 'score,DESC'
  return ''
})

function toggleScoreSort () {
  if (scoreSortDir.value === 'none') { scoreSortDir.value = 'desc'; return }
  if (scoreSortDir.value === 'desc') { scoreSortDir.value = 'asc'; return }
  scoreSortDir.value = 'none'
}

async function loadPage () {
  try {
    isLoading.value = true
    errorMessage.value = ''

    const requestAndApply = async (uiPage) => {
      const safePage = Math.max(1, Number(uiPage) || 1)
      const data = await fetchRaids({
        page: safePage,
        size: pageSize.value,
        sort: scoreSortParam.value || undefined,
      })

      if (Array.isArray(data)) {
        raids.value = data
        serverTotalPages.value = 1
        serverTotalElements.value = data.length
        return
      }

      const wrapped = Array.isArray(data?.data) ? data.data : null
      if (wrapped) {
        raids.value = wrapped
        serverTotalPages.value = Number.isFinite(Number(data?.totalPages)) ? Number(data.totalPages) : 1
        serverTotalElements.value = Number.isFinite(Number(data?.totalCount)) ? Number(data.totalCount) : wrapped.length
        return
      }

      const content = Array.isArray(data?.content) ? data.content : []
      raids.value = content
      serverTotalPages.value = Number.isFinite(Number(data?.totalPages)) ? Number(data.totalPages) : 1
      serverTotalElements.value = Number.isFinite(Number(data?.totalElements)) ? Number(data.totalElements) : content.length
    }

    await requestAndApply(currentPage.value)
  } catch (err) {
    errorMessage.value = err instanceof Error ? err.message : 'Failed to fetch raids'
    raids.value = []
    serverTotalPages.value = 1
    serverTotalElements.value = 0
  } finally {
    isLoading.value = false
  }
}

onMounted(loadPage)

watch([currentPage, pageSize], () => { loadPage() })
watch(scoreSortDir, () => { currentPage.value = 1; loadPage() })

/* ── Ranking tab ──────────────────────────────────────── */
const rankTab = ref('raid')   // 'raid' | 'key'

const keystoneRows = ref([
  { id:1,  rank:1,  player:'Mythicpusher',  class:'Mage',         realm:'데스윙',        region:'KR', rioScore:3847, bestKey:25, bestDungeon:'스톤볼트',        updatedAt:'2025.03.20' },
  { id:2,  rank:2,  player:'Frostbane',     class:'Death Knight', realm:'Azralon',      region:'US', rioScore:3712, bestKey:24, bestDungeon:'아라카라',          updatedAt:'2025.03.19' },
  { id:3,  rank:3,  player:'ArcaneBlast',   class:'Warlock',      realm:'Kazzak',       region:'EU', rioScore:3654, bestKey:23, bestDungeon:'그림 배톨',         updatedAt:'2025.03.18' },
  { id:4,  rank:4,  player:'Shadowstep',    class:'Rogue',        realm:'줄진',          region:'KR', rioScore:3501, bestKey:22, bestDungeon:'스레드의 도시',     updatedAt:'2025.03.17' },
  { id:5,  rank:5,  player:'Stormcaller',   class:'Shaman',       realm:'아즈샤라',      region:'KR', rioScore:3488, bestKey:22, bestDungeon:'던브레이커',        updatedAt:'2025.03.16' },
  { id:6,  rank:6,  player:'HolyLight',     class:'Paladin',      realm:'불타는 군단',   region:'KR', rioScore:3320, bestKey:21, bestDungeon:'보랄루스 공성전',   updatedAt:'2025.03.15' },
  { id:7,  rank:7,  player:'WildGrowth',    class:'Druid',        realm:'공허의 바람',   region:'KR', rioScore:3210, bestKey:21, bestDungeon:'티르나 시의 안개', updatedAt:'2025.03.14' },
  { id:8,  rank:8,  player:'ShadowVeil',    class:'Priest',       realm:'Firetree',     region:'US', rioScore:3098, bestKey:20, bestDungeon:'부식 괴멸',         updatedAt:'2025.03.13' },
  { id:9,  rank:9,  player:'Moonwhisper',   class:'Evoker',       realm:'데스윙',        region:'KR', rioScore:2954, bestKey:19, bestDungeon:'아라카라',          updatedAt:'2025.03.12' },
  { id:10, rank:10, player:'Darkbrew',      class:'Demon Hunter', realm:'아즈샤라',      region:'KR', rioScore:2847, bestKey:18, bestDungeon:'스톤볼트',          updatedAt:'2025.03.11' },
])

const CLASS_COLORS = {
  'Mage':'#3FC7EB','Death Knight':'#C41E3A','Warlock':'#8788EE','Rogue':'#FFF468',
  'Shaman':'#0070DD','Paladin':'#F48CBA','Druid':'#FF7C0A','Priest':'#e8e8f0',
  'Evoker':'#33937F','Demon Hunter':'#A330C9','Hunter':'#AAD372','Monk':'#00FF98','Warrior':'#C69B3A',
}
function rioColor(score) {
  if (score >= 3000) return '#ff8000'
  if (score >= 2500) return '#a335ee'
  if (score >= 2000) return '#0070dd'
  if (score >= 1000) return '#1eff00'
  return '#9d9d9d'
}
function keyColor(lv) {
  if (lv >= 20) return '#ff8000'
  if (lv >= 15) return '#a335ee'
  if (lv >= 10) return '#0070dd'
  return '#6b6b8a'
}

const searchField = ref('guild')
const searchQuery = ref('')
const progressOnly = ref(false)

const filtered = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  return raids.value
    .filter((r) => r && typeof r === 'object')
    .filter((r) => {
      const guild = String(r.guild ?? '').toLowerCase()
      const realm = String(r.realm ?? '').toLowerCase()
      if (!q) return true
      if (searchField.value === 'guild') return guild.includes(q)
      if (searchField.value === 'realm') return realm.includes(q)
      return true
    })
    .filter((r) => {
      if (!progressOnly.value) return true
      return r.progress === '9/9'
    })
})

const totalPages = computed(() => Math.max(1, Number(serverTotalPages.value) || 1))
const paginatedRows = computed(() => filtered.value)

const visiblePages = computed(() => {
  const total = totalPages.value
  const current = currentPage.value
  const windowSize = 5
  const half = Math.floor(windowSize / 2)
  let start = Math.max(1, current - half)
  let end = Math.min(total, start + windowSize - 1)
  start = Math.max(1, end - windowSize + 1)
  const pages = []
  for (let i = start; i <= end; i += 1) pages.push(i)
  return pages
})

function goToPage (page) {
  currentPage.value = Math.min(totalPages.value, Math.max(1, page))
}

watch([searchQuery, searchField, progressOnly, pageSize, filtered], () => {
  if (currentPage.value > totalPages.value) currentPage.value = totalPages.value
  if (currentPage.value < 1) currentPage.value = 1
})

function formatBestTimeMinutes (seconds) {
  const n = Number(seconds)
  if (!Number.isFinite(n) || n <= 0) return '—'
  return `${(n / 60).toFixed(2)}분`
}
</script>

<template>
  <section class="px-4 sm:px-6 lg:px-8 py-14">
    <div class="max-w-7xl mx-auto">

      <!-- Ranking mode tabs -->
      <div class="flex items-center h-12 p-1 rounded-2xl border border-rim/50 mb-6 w-fit"
           style="background: var(--bg-card)">
        <button type="button"
          class="flex items-center gap-2 h-10 px-5 rounded-xl text-sm font-semibold transition-all duration-200"
          :class="rankTab==='raid'?'text-white':'text-steel hover:text-silver'"
          :style="rankTab==='raid'?'background:#a335ee':''"
          @click="rankTab='raid'">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round"
                  d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
          </svg>
          공격대 랭킹
        </button>
        <button type="button"
          class="flex items-center gap-2 h-10 px-5 rounded-xl text-sm font-semibold transition-all duration-200"
          :class="rankTab==='key'?'text-white':'text-steel hover:text-silver'"
          :style="rankTab==='key'?'background:#ff8000':''"
          @click="rankTab='key'">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round"
                  d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/>
          </svg>
          쐐기 랭킹
        </button>
      </div>

      <!-- ═══ KEYSTONE RANKINGS ════════════════════════ -->
      <div v-if="rankTab==='key'" class="rounded-[1.5rem] border border-rim/50 overflow-hidden"
           style="background:var(--bg-card-light);backdrop-filter:blur(16px)">
        <div class="px-6 py-4 border-b border-rim/40 flex items-center justify-between">
          <div class="text-sm text-steel">
            Mythic+ 시즌 랭킹 · <span class="text-silver font-semibold">{{ keystoneRows.length }}</span>명
          </div>
          <RouterLink to="/matching?mode=key"
            class="inline-flex items-center justify-center h-9 px-4 rounded-full text-white text-sm font-semibold tracking-tight transition-all hover:-translate-y-0.5"
            style="background:#ff8000;box-shadow:0 4px 16px rgba(255,128,0,0.25)">
            쐐기 매칭하기
          </RouterLink>
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full text-left">
            <thead>
              <tr class="text-xs uppercase tracking-widest text-iron border-b border-rim/30"
                  style="background:var(--bg-header)">
                <th class="px-6 py-3 font-semibold">순위</th>
                <th class="px-6 py-3 font-semibold">플레이어</th>
                <th class="px-6 py-3 font-semibold">서버</th>
                <th class="px-6 py-3 font-semibold text-right">RIO 점수</th>
                <th class="px-6 py-3 font-semibold text-center">최고 키</th>
                <th class="px-6 py-3 font-semibold">최근 던전</th>
                <th class="px-6 py-3 font-semibold">갱신</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in keystoneRows" :key="row.id"
                  class="border-b border-rim/20 transition-colors hover:bg-shadow/40">
                <td class="px-6 py-4 text-sm font-semibold text-steel tabular-nums">{{ row.rank }}</td>
                <td class="px-6 py-4">
                  <div class="text-sm font-semibold" :style="`color:${CLASS_COLORS[row.class]??'#e8e8f0'}`">
                    {{ row.player }}
                  </div>
                  <div class="text-xs text-iron">{{ row.class }}</div>
                </td>
                <td class="px-6 py-4 text-sm text-steel">{{ row.realm }}
                  <span class="ml-1 text-xs text-iron">{{ row.region }}</span>
                </td>
                <td class="px-6 py-4 text-right">
                  <span class="text-sm font-bold tabular-nums" :style="`color:${rioColor(row.rioScore)}`">
                    {{ row.rioScore.toLocaleString() }}
                  </span>
                </td>
                <td class="px-6 py-4 text-center">
                  <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-bold"
                        :style="`background:${keyColor(row.bestKey)}15;color:${keyColor(row.bestKey)}`">
                    +{{ row.bestKey }}
                  </span>
                </td>
                <td class="px-6 py-4 text-sm text-steel">{{ row.bestDungeon }}</td>
                <td class="px-6 py-4 text-xs text-iron tabular-nums">{{ row.updatedAt }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- ═══ RAID RANKINGS (original) ════════════════ -->
      <div v-else>

      <!-- Page header + controls -->
      <div class="flex flex-col gap-6 md:flex-row md:items-end md:justify-between mb-8">
        <div>
          <h1 class="text-4xl md:text-5xl font-bold tracking-tighter text-silver">Raid Rankings</h1>
          <p class="mt-2 text-steel text-base md:text-lg">공격대 진행도와 기록을 한눈에. (현재는 더미 데이터)</p>
        </div>

        <div class="flex flex-col sm:flex-row gap-3">
          <!-- Search field toggle -->
          <div class="flex items-center gap-2">
            <div class="h-11 p-1 rounded-full border border-rim/50 flex items-center"
                 style="background: var(--bg-card); backdrop-filter: blur(8px)"
                 role="group" aria-label="Search field">
              <button type="button"
                class="h-9 px-4 rounded-full text-sm font-semibold tracking-tight transition-all"
                :class="searchField === 'guild' ? 'text-white' : 'text-steel hover:text-silver'"
                :style="searchField === 'guild' ? 'background: #a335ee' : ''"
                :aria-pressed="searchField === 'guild'"
                @click="searchField = 'guild'">
                길드
              </button>
              <button type="button"
                class="h-9 px-4 rounded-full text-sm font-semibold tracking-tight transition-all"
                :class="searchField === 'realm' ? 'text-white' : 'text-steel hover:text-silver'"
                :style="searchField === 'realm' ? 'background: #a335ee' : ''"
                :aria-pressed="searchField === 'realm'"
                @click="searchField = 'realm'">
                서버
              </button>
            </div>

            <!-- Search input -->
            <label class="relative">
              <span class="sr-only">Search</span>
              <input v-model="searchQuery" type="text" placeholder="검색"
                class="h-11 w-full sm:w-64 rounded-full border border-rim/50 px-4 text-sm text-silver
                       placeholder:text-iron focus:outline-none focus:ring-2 focus:ring-wow-epic/40
                       focus:border-wow-epic/50 transition-all duration-200"
                style="background: var(--bg-button); backdrop-filter: blur(8px)" />
            </label>
          </div>

          <!-- Progress filter -->
          <button type="button"
            class="h-11 rounded-full border px-4 text-sm font-medium transition-all duration-200"
            :class="progressOnly ? 'text-white border-wow-uncommon/60' : 'text-steel border-rim/50 hover:text-silver hover:border-rim'"
            :style="progressOnly ? 'background: rgba(30,255,0,0.1)' : 'background: var(--bg-button)'"
            @click="progressOnly = !progressOnly">
            9/9만
          </button>
        </div>
      </div>

      <!-- Table card -->
      <div class="rounded-[1.5rem] border border-rim/50 overflow-hidden"
           style="background: var(--bg-card-light); backdrop-filter: blur(16px)">

        <!-- Card header -->
        <div class="px-6 py-4 border-b border-rim/40 flex items-center justify-between">
          <div class="text-sm text-steel">총 <span class="text-silver font-semibold">{{ filtered.length }}</span>개</div>
          <RouterLink to="/matching"
            class="inline-flex items-center justify-center h-9 px-4 rounded-full text-white text-sm font-semibold
                   tracking-tight transition-all duration-300 hover:-translate-y-0.5"
            style="background: #a335ee; box-shadow: 0 4px 16px rgba(163,53,238,0.25)">
            매칭하러 가기
          </RouterLink>
        </div>

        <!-- Loading -->
        <div v-if="isLoading" class="px-6 py-8 text-sm text-steel text-center">
          <div class="inline-flex items-center gap-2">
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-wow-epic opacity-60"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-wow-epic"></span>
            </span>
            불러오는 중...
          </div>
        </div>

        <!-- Error -->
        <div v-else-if="errorMessage" class="px-6 py-6 text-sm text-red-400">
          {{ errorMessage }}
        </div>

        <!-- Table -->
        <div v-else class="overflow-x-auto">
          <table class="min-w-full text-left">
            <thead>
              <tr class="text-xs uppercase tracking-widest text-iron border-b border-rim/30"
                  style="background: var(--bg-header)">
                <th class="px-6 py-3 font-semibold">순위</th>
                <th class="px-6 py-3 font-semibold">길드</th>
                <th class="px-6 py-3 font-semibold">서버</th>
                <th class="px-6 py-3 font-semibold">진행도</th>
                <th class="px-6 py-3 font-semibold">인원</th>
                <th class="px-6 py-3 font-semibold">
                  <button type="button"
                    class="inline-flex items-center gap-2 hover:text-silver transition-colors"
                    @click="toggleScoreSort">
                    점수
                    <span class="text-[10px] font-semibold text-wow-epic/70">
                      {{ scoreSortDir === 'none' ? '—' : (scoreSortDir === 'desc' ? '↓' : '↑') }}
                    </span>
                  </button>
                </th>
                <th class="px-6 py-3 font-semibold">최고 기록</th>
                <th class="px-6 py-3 font-semibold">갱신</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in paginatedRows" :key="row.id"
                  class="border-b border-rim/20 transition-colors duration-150 hover:bg-shadow/40">
                <td class="px-6 py-4 text-sm font-semibold text-steel">{{ row.rank }}</td>
                <td class="px-6 py-4">
                  <RouterLink
                    :to="`/guild/${encodeURIComponent(row.guild)}`"
                    class="text-sm font-semibold text-silver hover:text-wow-epic transition-colors duration-200 underline-offset-2 hover:underline"
                  >{{ row.guild }}</RouterLink>
                  <div class="text-xs text-iron">{{ row.boss }}</div>
                </td>
                <td class="px-6 py-4 text-sm text-steel">{{ row.realm }}</td>
                <td class="px-6 py-4">
                  <span class="inline-flex items-center justify-center px-2.5 py-1 rounded-full text-xs font-semibold"
                    :class="row.progress === '9/9'
                      ? 'text-wow-uncommon'
                      : 'text-wow-epic'"
                    :style="row.progress === '9/9'
                      ? 'background: rgba(30,255,0,0.1)'
                      : 'background: rgba(163,53,238,0.12)'">
                    {{ row.progress }}
                  </span>
                </td>
                <td class="px-6 py-4 text-sm text-steel tabular-nums">{{ Number(row.memberCount ?? 0).toLocaleString() }}</td>
                <td class="px-6 py-4 text-sm text-silver tabular-nums font-medium">{{ Number(row.score ?? 0).toLocaleString() }}</td>
                <td class="px-6 py-4 text-sm text-steel tabular-nums">{{ formatBestTimeMinutes(row.bestTime) }}</td>
                <td class="px-6 py-4 text-sm text-iron tabular-nums">{{ row.updatedAt }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div v-if="!isLoading && !errorMessage"
          class="px-6 py-4 border-t border-rim/30 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">

          <!-- Page size -->
          <div class="flex items-center gap-2">
            <span class="text-xs text-iron">페이지 크기</span>
            <select v-model.number="pageSize"
              class="h-9 rounded-full border border-rim/50 px-3 text-sm text-silver
                     focus:outline-none focus:ring-2 focus:ring-wow-epic/40 transition-all"
              style="background: var(--bg-button)">
              <option :value="10">10</option>
              <option :value="20">20</option>
              <option :value="50">50</option>
            </select>
          </div>

          <!-- Page nav -->
          <div class="flex items-center justify-between sm:justify-end gap-2">
            <button type="button"
              class="h-9 px-3 rounded-full border border-rim/50 text-sm font-medium text-steel
                     hover:text-silver hover:border-rim transition-all disabled:opacity-30 disabled:cursor-not-allowed"
              style="background: var(--bg-button)"
              :disabled="currentPage === 1" @click="goToPage(currentPage - 1)">
              이전
            </button>

            <button v-for="p in visiblePages" :key="p" type="button"
              class="h-9 w-9 rounded-full border text-sm font-semibold transition-all"
              :class="p === currentPage ? 'text-white border-wow-epic' : 'border-rim/50 text-steel hover:text-silver hover:border-rim'"
              :style="p === currentPage ? 'background: #a335ee' : 'background: var(--bg-button)'"
              @click="goToPage(p)">
              {{ p }}
            </button>

            <button type="button"
              class="h-9 px-3 rounded-full border border-rim/50 text-sm font-medium text-steel
                     hover:text-silver hover:border-rim transition-all disabled:opacity-30 disabled:cursor-not-allowed"
              style="background: var(--bg-button)"
              :disabled="currentPage === totalPages" @click="goToPage(currentPage + 1)">
              다음
            </button>

            <div class="ml-2 text-xs text-iron tabular-nums">
              {{ currentPage }} / {{ totalPages }}
            </div>
          </div>
        </div>
      </div>

      <div class="mt-6 text-xs text-iron">
        실제 연동 시: 서버에서 순위/로그 데이터를 내려주고, 여기서는 검색/필터/정렬만 담당하게 만들면 됩니다.
      </div>

      </div> <!-- end v-else raid rankings -->
    </div>
  </section>
</template>
