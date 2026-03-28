<script setup>
import { computed, onMounted, ref, watch } from 'vue'

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '')

async function fetchRaids ({ page, size, sort }) {
  const qs = new URLSearchParams({
    page: String(page),
    size: String(size),
  })

  if (sort) {
    qs.set('sort', sort)
  }

  const response = await fetch(`${API_BASE_URL}/api/raids?${qs.toString()}`)
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
  if (scoreSortDir.value === 'none') {
    scoreSortDir.value = 'desc'
    return
  }
  if (scoreSortDir.value === 'desc') {
    scoreSortDir.value = 'asc'
    return
  }
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
        return { ok: true, length: data.length }
      }

      const wrapped = Array.isArray(data?.data) ? data.data : null
      if (wrapped) {
        raids.value = wrapped
        serverTotalPages.value = Number.isFinite(Number(data?.totalPages)) ? Number(data.totalPages) : 1
        serverTotalElements.value = Number.isFinite(Number(data?.totalCount)) ? Number(data.totalCount) : wrapped.length
        return { ok: true, length: wrapped.length }
      }

      const content = Array.isArray(data?.content) ? data.content : []
      raids.value = content
      serverTotalPages.value = Number.isFinite(Number(data?.totalPages)) ? Number(data.totalPages) : 1
      serverTotalElements.value = Number.isFinite(Number(data?.totalElements)) ? Number(data.totalElements) : content.length
      return { ok: true, length: content.length }
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

watch([currentPage, pageSize], () => {
  loadPage()
})

watch(scoreSortDir, () => {
  currentPage.value = 1
  loadPage()
})

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

const totalPages = computed(() => {
  return Math.max(1, Number(serverTotalPages.value) || 1)
})

const paginatedRows = computed(() => {
  return filtered.value
})

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
  const p = Math.min(totalPages.value, Math.max(1, page))
  currentPage.value = p
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
      <div class="flex flex-col gap-6 md:flex-row md:items-end md:justify-between">
        <div>
          <h1 class="text-4xl md:text-5xl font-bold tracking-tighter text-apple-black">Raid Rankings</h1>
          <p class="mt-2 text-apple-secondary text-base md:text-lg">공격대 진행도와 기록을 한눈에. (현재는 더미 데이터)</p>
        </div>

        <div class="flex flex-col sm:flex-row gap-3">
          <div class="flex items-center gap-2">
            <div
              class="h-11 p-1 rounded-full bg-white/70 backdrop-blur border border-gray-200 shadow-sm flex items-center"
              role="group" aria-label="Search field">
              <button type="button" class="h-9 px-4 rounded-full text-sm font-semibold tracking-tight transition-all"
                :class="searchField === 'guild' ? 'bg-apple-black text-white shadow-sm' : 'text-apple-black/70 hover:text-apple-black'"
                :aria-pressed="searchField === 'guild'" @click="searchField = 'guild'">
                길드
              </button>
              <button type="button" class="h-9 px-4 rounded-full text-sm font-semibold tracking-tight transition-all"
                :class="searchField === 'realm' ? 'bg-apple-black text-white shadow-sm' : 'text-apple-black/70 hover:text-apple-black'"
                :aria-pressed="searchField === 'realm'" @click="searchField = 'realm'">
                서버
              </button>
            </div>

            <label class="relative">
              <span class="sr-only">Search</span>
              <input v-model="searchQuery" type="text" placeholder="검색"
                class="h-11 w-full sm:w-72 rounded-full bg-white/80 backdrop-blur border border-gray-200 px-4 text-sm text-apple-black shadow-sm focus:outline-none focus:ring-2 focus:ring-wow-purple/40" />
            </label>
          </div>

          <button type="button"
            class="h-11 rounded-full bg-white/80 backdrop-blur border border-gray-200 px-4 text-sm font-medium text-apple-black shadow-sm hover:bg-white transition-colors"
            :class="progressOnly ? 'ring-2 ring-wow-purple/40' : ''" @click="progressOnly = !progressOnly">
            9/9만
          </button>
        </div>
      </div>

      <div class="mt-8 rounded-[1.5rem] bg-white/70 backdrop-blur border border-gray-200 shadow-sm overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-100/80 flex items-center justify-between">
          <div class="text-sm text-apple-secondary">총 {{ filtered.length }}개</div>
          <RouterLink to="/matching"
            class="inline-flex items-center justify-center h-10 px-4 rounded-full bg-apple-black text-white text-sm font-semibold tracking-tight hover:bg-black/90 transition-colors">
            매칭하러 가기
          </RouterLink>
        </div>

        <div v-if="isLoading" class="px-6 py-6 text-sm text-apple-secondary">
          불러오는 중...
        </div>

        <div v-else-if="errorMessage" class="px-6 py-6 text-sm text-red-600">
          {{ errorMessage }}
        </div>

        <div v-else class="overflow-x-auto">
          <table class="min-w-full text-left">
            <thead class="bg-apple-gray/60">
              <tr class="text-xs uppercase tracking-widest text-apple-secondary">
                <th class="px-6 py-3 font-semibold">순위</th>
                <th class="px-6 py-3 font-semibold">길드</th>
                <th class="px-6 py-3 font-semibold">서버</th>
                <th class="px-6 py-3 font-semibold">진행도</th>
                <th class="px-6 py-3 font-semibold">인원</th>
                <th class="px-6 py-3 font-semibold">
                  <button type="button" class="inline-flex items-center gap-2 hover:text-apple-black transition-colors"
                    @click="toggleScoreSort">
                    점수
                    <span class="text-[10px] font-semibold text-apple-secondary">
                      {{ scoreSortDir === 'none' ? '—' : (scoreSortDir === 'desc' ? 'DESC' : 'ASC') }}
                    </span>
                  </button>
                </th>
                <th class="px-6 py-3 font-semibold">최고 기록</th>
                <th class="px-6 py-3 font-semibold">갱신</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100/80">
              <tr v-for="row in paginatedRows" :key="row.id" class="hover:bg-white transition-colors">
                <td class="px-6 py-4 text-sm font-semibold text-apple-black">{{ row.rank }}</td>
                <td class="px-6 py-4">
                  <div class="text-sm font-semibold text-apple-black">{{ row.guild }}</div>
                  <div class="text-xs text-apple-secondary">{{ row.boss }}</div>
                </td>
                <td class="px-6 py-4 text-sm text-apple-black">{{ row.realm }}</td>
                <td class="px-6 py-4">
                  <span class="inline-flex items-center justify-center px-2.5 py-1 rounded-full text-xs font-semibold"
                    :class="row.progress === '9/9' ? 'bg-green-50 text-green-700' : 'bg-purple-50 text-wow-purple'">
                    {{ row.progress }}
                  </span>
                </td>
                <td class="px-6 py-4 text-sm text-apple-black tabular-nums">{{ Number(row.memberCount ??
                  0).toLocaleString() }}</td>
                <td class="px-6 py-4 text-sm text-apple-black tabular-nums">{{ Number(row.score ?? 0).toLocaleString()
                }}</td>
                <td class="px-6 py-4 text-sm text-apple-black tabular-nums">{{ formatBestTimeMinutes(row.bestTime) }}
                </td>
                <td class="px-6 py-4 text-sm text-apple-secondary tabular-nums">{{ row.updatedAt }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="!isLoading && !errorMessage"
          class="px-6 py-4 border-t border-gray-100/80 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div class="flex items-center gap-2">
            <span class="text-xs text-apple-secondary">페이지 크기</span>
            <select v-model.number="pageSize"
              class="h-9 rounded-full bg-white/80 backdrop-blur border border-gray-200 px-3 text-sm text-apple-black shadow-sm focus:outline-none focus:ring-2 focus:ring-wow-purple/40">
              <option :value="10">10</option>
              <option :value="20">20</option>
              <option :value="50">50</option>
            </select>
          </div>

          <div class="flex items-center justify-between sm:justify-end gap-2">
            <button type="button"
              class="h-9 px-3 rounded-full bg-white/80 backdrop-blur border border-gray-200 text-sm font-medium text-apple-black shadow-sm hover:bg-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="currentPage === 1" @click="goToPage(currentPage - 1)">
              이전
            </button>

            <button v-for="p in visiblePages" :key="p" type="button"
              class="h-9 w-9 rounded-full border text-sm font-semibold transition-colors"
              :class="p === currentPage ? 'bg-apple-black text-white border-apple-black' : 'bg-white/80 backdrop-blur border-gray-200 text-apple-black hover:bg-white'"
              @click="goToPage(p)">
              {{ p }}
            </button>

            <button type="button"
              class="h-9 px-3 rounded-full bg-white/80 backdrop-blur border border-gray-200 text-sm font-medium text-apple-black shadow-sm hover:bg-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="currentPage === totalPages" @click="goToPage(currentPage + 1)">
              다음
            </button>

            <div class="ml-2 text-xs text-apple-secondary tabular-nums">
              {{ currentPage }} / {{ totalPages }}
            </div>
          </div>
        </div>
      </div>

      <div class="mt-6 text-xs text-apple-secondary">
        실제 연동 시: 서버에서 순위/로그 데이터를 내려주고, 여기서는 검색/필터/정렬만 담당하게 만들면 됩니다.
      </div>
    </div>
  </section>
</template>
