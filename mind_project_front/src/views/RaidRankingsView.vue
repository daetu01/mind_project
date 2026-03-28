<script setup>
import { computed, ref } from 'vue'

const raids = [
  {
    id: 1,
    rank: 1,
    guild: 'Midnight Protocol',
    realm: '아즈샤라',
    boss: '최종 보스',
    progress: '9/9',
    bestTime: '03:41',
    updatedAt: '2026-03-28',
  },
  {
    id: 2,
    rank: 2,
    guild: 'Silent Raiders',
    realm: '듀로탄',
    boss: '최종 보스',
    progress: '9/9',
    bestTime: '03:58',
    updatedAt: '2026-03-27',
  },
  {
    id: 3,
    rank: 3,
    guild: 'Less Talk More DPS',
    realm: '하이잘',
    boss: '최종 보스',
    progress: '8/9',
    bestTime: '—',
    updatedAt: '2026-03-26',
  },
  {
    id: 4,
    rank: 4,
    guild: 'Glass Cannon Club',
    realm: '세나리우스',
    boss: '8번째 보스',
    progress: '8/9',
    bestTime: '05:12',
    updatedAt: '2026-03-25',
  },
]

const query = ref('')
const progressOnly = ref(false)

const filtered = computed(() => {
  const q = query.value.trim().toLowerCase()
  return raids
    .filter((r) => {
      if (!q) return true
      return (
        r.guild.toLowerCase().includes(q) ||
        r.realm.toLowerCase().includes(q) ||
        r.boss.toLowerCase().includes(q)
      )
    })
    .filter((r) => {
      if (!progressOnly.value) return true
      return r.progress === '9/9'
    })
})
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
          <label class="relative">
            <span class="sr-only">Search</span>
            <input
              v-model="query"
              type="text"
              placeholder="길드/서버/보스 검색"
              class="h-11 w-full sm:w-72 rounded-full bg-white/80 backdrop-blur border border-gray-200 px-4 text-sm text-apple-black shadow-sm focus:outline-none focus:ring-2 focus:ring-wow-purple/40"
            />
          </label>

          <button
            type="button"
            class="h-11 rounded-full bg-white/80 backdrop-blur border border-gray-200 px-4 text-sm font-medium text-apple-black shadow-sm hover:bg-white transition-colors"
            :class="progressOnly ? 'ring-2 ring-wow-purple/40' : ''"
            @click="progressOnly = !progressOnly"
          >
            9/9만
          </button>
        </div>
      </div>

      <div class="mt-8 rounded-[1.5rem] bg-white/70 backdrop-blur border border-gray-200 shadow-sm overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-100/80 flex items-center justify-between">
          <div class="text-sm text-apple-secondary">총 {{ filtered.length }}개</div>
          <RouterLink
            to="/matching"
            class="inline-flex items-center justify-center h-10 px-4 rounded-full bg-apple-black text-white text-sm font-semibold tracking-tight hover:bg-black/90 transition-colors"
          >
            매칭하러 가기
          </RouterLink>
        </div>

        <div class="overflow-x-auto">
          <table class="min-w-full text-left">
            <thead class="bg-apple-gray/60">
              <tr class="text-xs uppercase tracking-widest text-apple-secondary">
                <th class="px-6 py-3 font-semibold">순위</th>
                <th class="px-6 py-3 font-semibold">길드</th>
                <th class="px-6 py-3 font-semibold">서버</th>
                <th class="px-6 py-3 font-semibold">진행도</th>
                <th class="px-6 py-3 font-semibold">최고 기록</th>
                <th class="px-6 py-3 font-semibold">갱신</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100/80">
              <tr
                v-for="row in filtered"
                :key="row.id"
                class="hover:bg-white transition-colors"
              >
                <td class="px-6 py-4 text-sm font-semibold text-apple-black">{{ row.rank }}</td>
                <td class="px-6 py-4">
                  <div class="text-sm font-semibold text-apple-black">{{ row.guild }}</div>
                  <div class="text-xs text-apple-secondary">{{ row.boss }}</div>
                </td>
                <td class="px-6 py-4 text-sm text-apple-black">{{ row.realm }}</td>
                <td class="px-6 py-4">
                  <span
                    class="inline-flex items-center justify-center px-2.5 py-1 rounded-full text-xs font-semibold"
                    :class="row.progress === '9/9' ? 'bg-green-50 text-green-700' : 'bg-purple-50 text-wow-purple'"
                  >
                    {{ row.progress }}
                  </span>
                </td>
                <td class="px-6 py-4 text-sm text-apple-black tabular-nums">{{ row.bestTime }}</td>
                <td class="px-6 py-4 text-sm text-apple-secondary tabular-nums">{{ row.updatedAt }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="mt-6 text-xs text-apple-secondary">
        실제 연동 시: 서버에서 순위/로그 데이터를 내려주고, 여기서는 검색/필터/정렬만 담당하게 만들면 됩니다.
      </div>
    </div>
  </section>
</template>
