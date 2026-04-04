<script setup>
import { computed, nextTick, ref, watch } from 'vue'

const API_BASE_URL = (import.meta.env.VITE_FASTAPI_BASE_URL || '').replace(/\/$/, '')

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

const realm = ref('')
const name = ref('')

const isLoading = ref(false)
const errorMessage = ref('')
const character = ref(null)

const rio = ref(null)
const rioErrorMessage = ref('')

const rawCharacter = ref(null)
const rawCharacterErrorMessage = ref('')

const bundle = ref(null)
const bundleErrorMessage = ref('')

const activeTab = ref('summary')

const tabs = [
  { key: 'summary', label: '요약' },
  { key: 'stats', label: '전투능력치' },
  { key: 'talents', label: '특성정보' },
  { key: 'gear', label: '장비' },
  { key: 'rio', label: 'RIO' },
  { key: 'raw', label: '원본' },
]

const showRioTab = computed(() => {
  return Boolean(rio.value) || Boolean(rioErrorMessage.value)
})

const showRawTab = computed(() => {
  return Boolean(rawCharacter.value) || Boolean(rawCharacterErrorMessage.value)
})

const visibleTabs = computed(() => {
  return tabs.filter((t) => {
    if (t.key === 'rio') return showRioTab.value
    if (t.key === 'raw') return showRawTab.value
    return true
  })
})

const rioScore = computed(() => {
  const v = rio.value
  if (!v || typeof v !== 'object') return null
  const n = Number(v.score)
  return Number.isFinite(n) ? n : null
})

function normalizeMaybeArray (value) {
  if (!value) return []
  if (Array.isArray(value)) return value
  return [value]
}

const equipmentRows = computed(() => {
  const c = character.value
  if (!c || typeof c !== 'object') return []
  return Array.isArray(c['장비']) ? c['장비'] : []
})

const talentRows = computed(() => {
  const c = character.value
  if (!c || typeof c !== 'object') return []
  return Array.isArray(c['특성정보']) ? c['특성정보'] : []
})

const combatStats = computed(() => {
  const c = character.value
  if (!c || typeof c !== 'object') return null
  return c['전투능력치'] && typeof c['전투능력치'] === 'object' ? c['전투능력치'] : null
})

const displayName = computed(() => {
  const c = character.value
  if (!c || typeof c !== 'object') return name.value
  return c.name || c['이름'] || rawCharacter.value?.name || name.value
})

const displayRace = computed(() => {
  const r = rawCharacter.value
  if (r && typeof r === 'object' && r.race && typeof r.race === 'object' && typeof r.race.name === 'string') {
    return r.race.name
  }
  const c = character.value
  if (c && typeof c === 'object' && typeof c['종족'] === 'string') return c['종족']
  return ''
})

const displayFaction = computed(() => {
  const r = rawCharacter.value
  if (r && typeof r === 'object' && r.faction && typeof r.faction === 'object' && typeof r.faction.name === 'string') {
    return r.faction.name
  }
  return ''
})

const displayRealm = computed(() => {
  const c = character.value
  if (c && typeof c === 'object') {
    if (typeof c.realm === 'string' && c.realm.trim()) return c.realm
    if (c.realm && typeof c.realm === 'object') {
      if (typeof c.realm.name === 'string' && c.realm.name.trim()) return c.realm.name
      if (typeof c.realm.slug === 'string' && c.realm.slug.trim()) return c.realm.slug
    }
    if (typeof c['서버'] === 'string' && c['서버'].trim()) return c['서버']
  }

  const r = rawCharacter.value
  if (r && typeof r === 'object' && r.realm && typeof r.realm === 'object') {
    if (typeof r.realm.name === 'string' && r.realm.name.trim()) return r.realm.name
    if (typeof r.realm.slug === 'string' && r.realm.slug.trim()) return r.realm.slug
  }

  return realm.value
})

const displayClass = computed(() => {
  const c = character.value
  if (c && typeof c === 'object') {
    if (typeof c.class === 'string') return c.class
    if (typeof c['직업'] === 'string') return c['직업']
    if (c.character_class && typeof c.character_class === 'object' && typeof c.character_class.name === 'string') return c.character_class.name
  }

  const r = rawCharacter.value
  if (r && typeof r === 'object' && r.character_class && typeof r.character_class === 'object' && typeof r.character_class.name === 'string') {
    return r.character_class.name
  }

  return ''
})

const displaySpec = computed(() => {
  const c = character.value
  if (c && typeof c === 'object') {
    if (typeof c.spec === 'string') return c.spec
    if (typeof c['전문화'] === 'string') return c['전문화']
    if (c.active_spec && typeof c.active_spec === 'object' && typeof c.active_spec.name === 'string') return c.active_spec.name
  }

  const r = rawCharacter.value
  if (r && typeof r === 'object' && r.active_spec && typeof r.active_spec === 'object' && typeof r.active_spec.name === 'string') {
    return r.active_spec.name
  }

  return ''
})

const displayLevel = computed(() => {
  const c = character.value
  if (!c || typeof c !== 'object') return null
  return c.level ?? c['레벨'] ?? rawCharacter.value?.level ?? null
})

const displayItemLevel = computed(() => {
  const c = character.value
  if (c && typeof c === 'object') {
    return c.item_level ?? c.equipped_item_level ?? c.average_item_level ?? c['착용아이템레벨'] ?? c['평균아이템레벨'] ?? null
  }

  const r = rawCharacter.value
  if (r && typeof r === 'object') {
    return r.equipped_item_level ?? r.average_item_level ?? null
  }

  return null
})

const achievementPoints = computed(() => {
  const c = character.value
  if (c && typeof c === 'object') {
    return c['업적점수'] ?? c.achievement_points ?? null
  }
  const r = rawCharacter.value
  if (r && typeof r === 'object') return r.achievement_points ?? null
  return null
})

function formatLastLogin (ms) {
  const n = Number(ms)
  if (!Number.isFinite(n) || n <= 0) return null
  const d = new Date(n)
  if (Number.isNaN(d.getTime())) return null
  return d.toLocaleString()
}

const lastLogin = computed(() => {
  const c = character.value
  if (c && typeof c === 'object' && c['마지막접속']) return c['마지막접속']
  const r = rawCharacter.value
  if (r && typeof r === 'object') return formatLastLogin(r.last_login_timestamp)
  return null
})

const bundleEquipment = computed(() => {
  const b = bundle.value
  if (!b || typeof b !== 'object') return null
  return b.equipment ?? null
})

const bundleStatistics = computed(() => {
  const b = bundle.value
  if (!b || typeof b !== 'object') return null
  return b.statistics ?? null
})

const bundleSpecializations = computed(() => {
  const b = bundle.value
  if (!b || typeof b !== 'object') return null
  return b.specializations ?? null
})

const blizzSpecs = computed(() => {
  const s = bundleSpecializations.value
  if (!s || typeof s !== 'object') return null
  return s
})

const activeSpecializationId = computed(() => {
  const s = blizzSpecs.value
  if (!s || typeof s !== 'object') return null
  const id = s.active_specialization?.id
  return Number.isFinite(Number(id)) ? Number(id) : null
})

const activeHeroTalentTreeName = computed(() => {
  const s = blizzSpecs.value
  if (!s || typeof s !== 'object') return ''
  return s.active_hero_talent_tree?.name || ''
})

const activeSpecEntry = computed(() => {
  const s = blizzSpecs.value
  if (!s || typeof s !== 'object') return null
  const list = Array.isArray(s.specializations) ? s.specializations : []
  const activeId = activeSpecializationId.value
  if (activeId) {
    const found = list.find((x) => x?.specialization?.id === activeId)
    if (found) return found
  }
  const activeName = s.active_specialization?.name
  if (activeName) {
    const found = list.find((x) => x?.specialization?.name === activeName)
    if (found) return found
  }
  return list[0] || null
})

const activeLoadout = computed(() => {
  const entry = activeSpecEntry.value
  if (!entry || typeof entry !== 'object') return null
  const loadouts = Array.isArray(entry.loadouts) ? entry.loadouts : []
  return loadouts.find((l) => l && typeof l === 'object' && l.is_active) || null
})

function talentTitle (node) {
  if (!node || typeof node !== 'object') return ''
  const tooltip = node.tooltip && typeof node.tooltip === 'object' ? node.tooltip : null
  const talentName = tooltip?.talent?.name
  const spellName = tooltip?.spell_tooltip?.spell?.name
  return talentName || spellName || ''
}

function talentSpellId (node) {
  if (!node || typeof node !== 'object') return null
  const tooltip = node.tooltip && typeof node.tooltip === 'object' ? node.tooltip : null
  const id = tooltip?.spell_tooltip?.spell?.id
  const n = Number(id)
  return Number.isFinite(n) ? n : null
}

function talentDescription (node) {
  if (!node || typeof node !== 'object') return ''
  const tooltip = node.tooltip && typeof node.tooltip === 'object' ? node.tooltip : null
  const desc = tooltip?.spell_tooltip?.description
  return typeof desc === 'string' ? desc : ''
}

const activeClassTalents = computed(() => {
  const l = activeLoadout.value
  if (!l || typeof l !== 'object') return []
  return Array.isArray(l.selected_class_talents) ? l.selected_class_talents : []
})

const activeSpecTalents = computed(() => {
  const l = activeLoadout.value
  if (!l || typeof l !== 'object') return []
  return Array.isArray(l.selected_spec_talents) ? l.selected_spec_talents : []
})

const activeHeroTalents = computed(() => {
  const l = activeLoadout.value
  if (!l || typeof l !== 'object') return []
  return Array.isArray(l.selected_hero_talents) ? l.selected_hero_talents : []
})

const activePvpTalents = computed(() => {
  const entry = activeSpecEntry.value
  if (!entry || typeof entry !== 'object') return []
  const slots = Array.isArray(entry.pvp_talent_slots) ? entry.pvp_talent_slots : []
  return slots
    .map((s) => {
      const selected = s?.selected
      const name = selected?.talent?.name || selected?.spell_tooltip?.spell?.name || ''
      const description = selected?.spell_tooltip?.description || ''
      const id = selected?.spell_tooltip?.spell?.id
      const n = Number(id)
      return {
        slot: s?.slot_number ?? null,
        name,
        description,
        spellId: Number.isFinite(n) ? n : null,
      }
    })
    .filter((x) => x && x.name)
})

async function refreshWowheadTooltips () {
  await nextTick()
  const w = window
  const wh = w?.$WowheadPower
  if (wh && typeof wh.refreshLinks === 'function') {
    try {
      wh.refreshLinks()
    } catch (e) {
      // ignore
    }
  }
}

watch([bundleSpecializations, activeTab], () => {
  if (activeTab.value !== 'talents') return
  if (!bundleSpecializations.value) return
  refreshWowheadTooltips()
})

const blizzStats = computed(() => {
  const s = bundleStatistics.value
  if (!s || typeof s !== 'object') return null
  return s
})

function numberOrNull (value) {
  const n = Number(value)
  return Number.isFinite(n) ? n : null
}

function statEffective (obj) {
  if (!obj || typeof obj !== 'object') return null
  if ('effective' in obj) return numberOrNull(obj.effective)
  if ('value' in obj) return numberOrNull(obj.value)
  return null
}

const blizzPrimaryStats = computed(() => {
  const s = blizzStats.value
  if (!s) return null
  return {
    strength: statEffective(s.strength),
    agility: statEffective(s.agility),
    intellect: statEffective(s.intellect),
    stamina: statEffective(s.stamina),
  }
})

const blizzSecondaryStats = computed(() => {
  const s = blizzStats.value
  if (!s) return null
  return {
    crit: numberOrNull(s.spell_crit?.value ?? s.melee_crit?.value ?? s.ranged_crit?.value),
    haste: numberOrNull(s.spell_haste?.value ?? s.melee_haste?.value ?? s.ranged_haste?.value),
    mastery: numberOrNull(s.mastery?.value),
    versatilityDone: numberOrNull(s.versatility_damage_done_bonus),
    versatilityTaken: numberOrNull(s.versatility_damage_taken_bonus),
    speed: numberOrNull(s.speed?.rating_bonus),
  }
})

const blizzResource = computed(() => {
  const s = blizzStats.value
  if (!s) return null
  return {
    health: numberOrNull(s.health),
    power: numberOrNull(s.power),
    powerType: typeof s.power_type?.name === 'string' ? s.power_type.name : null,
  }
})

const avatarUrl = computed(() => {
  const c = character.value
  if (!c || typeof c !== 'object') return ''

  if (c.images && typeof c.images === 'object') {
    const url = c.images.avatar || c.images.inset || c.images['main-raw']
    if (typeof url === 'string' && url.trim().length > 0) return url.trim()
  }

  const candidates = [
    c.avatarUrl,
    c.avatar_url,
    c.thumbnail,
    c.thumbnail_url,
    c.portrait,
    c.portrait_url,
    c.imageUrl,
    c.image_url,
    c['이미지'],
  ]

  const first = candidates.find((v) => typeof v === 'string' && v.trim().length > 0)
  return first ? first.trim() : ''
})

async function fetchCharacterViaApi (realmValue, nameValue) {
  const response = await fetch(apiUrl(`/wow/character-card/${encodeURIComponent(realmValue)}/${encodeURIComponent(nameValue)}`))
  if (!response.ok) {
    throw new Error(`Failed to fetch character: ${response.status}`)
  }
  return response.json()
}

async function fetchCharacterViaPipeline (realmValue, nameValue) {
  const response = await fetch(apiUrl(`/character/${encodeURIComponent(realmValue)}/${encodeURIComponent(nameValue)}`))
  if (!response.ok) {
    throw new Error(`Failed to fetch character: ${response.status}`)
  }
  return response.json()
}

async function fetchRio (realmValue, nameValue) {
  const response = await fetch(apiUrl(`/wow/rio/${encodeURIComponent(realmValue)}/${encodeURIComponent(nameValue)}`))
  if (!response.ok) {
    throw new Error(`Failed to fetch rio: ${response.status}`)
  }
  return response.json()
}

async function fetchRawCharacter (realmValue, nameValue) {
  const response = await fetch(apiUrl(`/wow/character/${encodeURIComponent(realmValue)}/${encodeURIComponent(nameValue)}`))
  if (!response.ok) {
    throw new Error(`Failed to fetch character raw: ${response.status}`)
  }
  return response.json()
}

async function fetchCharacterBundle (realmValue, nameValue) {
  const response = await fetch(apiUrl(`/wow/character-bundle/${encodeURIComponent(realmValue)}/${encodeURIComponent(nameValue)}`))
  if (!response.ok) {
    throw new Error(`Failed to fetch character bundle: ${response.status}`)
  }
  return response.json()
}

async function onSearch () {
  const realmValue = realm.value.trim()
  const nameValue = name.value.trim()

  if (!realmValue || !nameValue) {
    errorMessage.value = '서버(realm)와 캐릭터 이름을 입력해 주세요.'
    character.value = null
    return
  }

  isLoading.value = true
  errorMessage.value = ''
  character.value = null
  rio.value = null
  rioErrorMessage.value = ''
  rawCharacter.value = null
  rawCharacterErrorMessage.value = ''
  bundle.value = null
  bundleErrorMessage.value = ''
  activeTab.value = 'summary'

  try {
    try {
      character.value = await fetchCharacterViaApi(realmValue, nameValue)
    } catch (e) {
      character.value = await fetchCharacterViaPipeline(realmValue, nameValue)
    }

    try {
      rio.value = await fetchRio(realmValue, nameValue)
      if (rio.value && typeof rio.value === 'object' && 'error' in rio.value) {
        const msg = typeof rio.value.error === 'string' ? rio.value.error : 'RIO 정보를 불러오지 못했습니다.'
        throw new Error(msg)
      }
    } catch (e) {
      rio.value = null
      rioErrorMessage.value = e instanceof Error ? e.message : 'RIO 정보를 불러오지 못했습니다.'
    }

    try {
      rawCharacter.value = await fetchRawCharacter(realmValue, nameValue)
      if (rawCharacter.value && typeof rawCharacter.value === 'object' && 'error' in rawCharacter.value) {
        const msg = typeof rawCharacter.value.error === 'string' ? rawCharacter.value.error : '원본 캐릭터 정보를 불러오지 못했습니다.'
        throw new Error(msg)
      }
    } catch (e) {
      rawCharacter.value = null
      rawCharacterErrorMessage.value = e instanceof Error ? e.message : '원본 캐릭터 정보를 불러오지 못했습니다.'
    }

    try {
      bundle.value = await fetchCharacterBundle(realmValue, nameValue)
      if (bundle.value && typeof bundle.value === 'object' && 'error' in bundle.value) {
        const msg = typeof bundle.value.error === 'string' ? bundle.value.error : '번들 정보를 불러오지 못했습니다.'
        throw new Error(msg)
      }
      if (bundle.value && typeof bundle.value === 'object' && bundle.value.summary && typeof bundle.value.summary === 'object') {
        rawCharacter.value = bundle.value.summary
      }
    } catch (e) {
      bundle.value = null
      bundleErrorMessage.value = e instanceof Error ? e.message : '번들 정보를 불러오지 못했습니다.'
    }

    if (character.value && typeof character.value === 'object' && 'error' in character.value) {
      const msg = typeof character.value.error === 'string' ? character.value.error : '캐릭터 정보를 불러오지 못했습니다.'
      throw new Error(msg)
    }
  } catch (err) {
    errorMessage.value = err instanceof Error ? err.message : '캐릭터 정보를 불러오지 못했습니다.'
    character.value = null
    rio.value = null
    rioErrorMessage.value = ''
    rawCharacter.value = null
    rawCharacterErrorMessage.value = ''
    bundle.value = null
    bundleErrorMessage.value = ''
  } finally {
    isLoading.value = false
  }
}

function displayValue (value) {
  if (value === null || value === undefined) return '—'
  if (typeof value === 'string' && value.trim() === '') return '—'
  if (typeof value === 'object') return JSON.stringify(value)
  return String(value)
}
</script>

<template>
  <section class="px-4 sm:px-6 lg:px-8 py-14">
    <div class="max-w-7xl mx-auto">
      <div class="flex flex-col gap-6 md:flex-row md:items-end md:justify-between">
        <div>
          <h1 class="text-4xl md:text-5xl font-bold tracking-tighter text-apple-black">Character Search</h1>
          <p class="mt-2 text-apple-secondary text-base md:text-lg">서버/이름으로 캐릭터를 검색하고 상세 정보를 탭으로 확인합니다.</p>
        </div>

        <div class="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
          <label class="relative w-full sm:w-48">
            <span class="sr-only">Realm</span>
            <input v-model="realm" type="text" placeholder="서버 (예: azshara)"
              class="h-11 w-full rounded-full bg-white/80 backdrop-blur border border-gray-200 px-4 text-sm text-apple-black shadow-sm focus:outline-none focus:ring-2 focus:ring-wow-purple/40" />
          </label>

          <label class="relative w-full sm:w-56">
            <span class="sr-only">Name</span>
            <input v-model="name" type="text" placeholder="캐릭터명"
              class="h-11 w-full rounded-full bg-white/80 backdrop-blur border border-gray-200 px-4 text-sm text-apple-black shadow-sm focus:outline-none focus:ring-2 focus:ring-wow-purple/40" @keyup.enter="onSearch" />
          </label>

          <button type="button" class="h-11 rounded-full bg-apple-black text-white px-5 text-sm font-semibold tracking-tight hover:bg-black/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed" :disabled="isLoading" @click="onSearch">
            검색
          </button>
        </div>
      </div>

      <div class="mt-8 rounded-[1.5rem] bg-white/70 backdrop-blur border border-gray-200 shadow-sm overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-100/80 flex items-center justify-between">
          <div class="text-sm text-apple-secondary">
            <span v-if="character && typeof character === 'object'">{{ displayRealm }} / {{ displayName }}</span>
            <span v-else>검색 결과</span>
          </div>
        </div>

        <div v-if="isLoading" class="px-6 py-6 text-sm text-apple-secondary">불러오는 중...</div>
        <div v-else-if="errorMessage" class="px-6 py-6 text-sm text-red-600">{{ errorMessage }}</div>

        <div v-else-if="!character" class="px-6 py-10 text-sm text-apple-secondary">
          서버와 캐릭터명을 입력하고 검색해 주세요.
        </div>

        <div v-else class="px-6 py-6">
          <div class="flex flex-col lg:flex-row gap-6">
            <div class="flex items-start gap-4">
              <div class="h-16 w-16 rounded-2xl bg-apple-gray flex items-center justify-center overflow-hidden border border-gray-200 shadow-sm">
                <img v-if="avatarUrl" :src="avatarUrl" alt="avatar" class="h-full w-full object-cover" />
                <div v-else class="text-lg font-bold text-apple-black/70">
                  {{ String(displayName || '?').slice(0, 1) }}
                </div>
              </div>

              <div>
                <div class="text-lg font-bold text-apple-black">{{ displayName }}</div>
                <div class="mt-1 text-sm text-apple-secondary">
                  {{ displayRealm }}
                  <template v-if="displayClass || displaySpec">
                    · {{ displayRace || '' }} {{ displayClass }}
                    <template v-if="displaySpec"> · {{ displaySpec }}</template>
                  </template>
                  <template v-if="displayFaction">
                    · {{ displayFaction }}
                  </template>
                </div>
                <div class="mt-2 flex flex-wrap gap-2">
                  <span class="inline-flex items-center justify-center px-2.5 py-1 rounded-full text-xs font-semibold bg-purple-50 text-wow-purple">
                    레벨 {{ displayLevel ?? '—' }}
                  </span>
                  <span class="inline-flex items-center justify-center px-2.5 py-1 rounded-full text-xs font-semibold bg-gray-50 text-apple-black/70">
                    iLv {{ displayItemLevel ?? '—' }}
                  </span>
                </div>
              </div>
            </div>

            <div class="flex-1">
              <div class="h-11 p-1 rounded-full bg-white/70 backdrop-blur border border-gray-200 shadow-sm inline-flex items-center" role="tablist" aria-label="Character details tabs">
                <button v-for="t in visibleTabs" :key="t.key" type="button" class="h-9 px-4 rounded-full text-sm font-semibold tracking-tight transition-all" :class="activeTab === t.key ? 'bg-apple-black text-white shadow-sm' : 'text-apple-black/70 hover:text-apple-black'" :aria-selected="activeTab === t.key" @click="activeTab = t.key">
                  {{ t.label }}
                </button>
              </div>

              <div class="mt-6">
                <div v-if="activeTab === 'summary'" class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div class="rounded-2xl bg-white/80 border border-gray-200 px-4 py-3 shadow-sm">
                    <div class="text-xs text-apple-secondary">업적점수</div>
                    <div class="mt-1 text-sm font-semibold text-apple-black tabular-nums">{{ (achievementPoints ?? 0).toLocaleString?.() ?? displayValue(achievementPoints) }}</div>
                  </div>

                  <div class="rounded-2xl bg-white/80 border border-gray-200 px-4 py-3 shadow-sm">
                    <div class="text-xs text-apple-secondary">마지막 접속</div>
                    <div class="mt-1 text-sm font-semibold text-apple-black">{{ displayValue(lastLogin) }}</div>
                  </div>

                  <div class="rounded-2xl bg-white/80 border border-gray-200 px-4 py-3 shadow-sm">
                    <div class="text-xs text-apple-secondary">성별</div>
                    <div class="mt-1 text-sm font-semibold text-apple-black">{{ displayValue(character['성별']) }}</div>
                  </div>

                  <div class="rounded-2xl bg-white/80 border border-gray-200 px-4 py-3 shadow-sm">
                    <div class="text-xs text-apple-secondary">아이디</div>
                    <div class="mt-1 text-sm font-semibold text-apple-black tabular-nums">{{ displayValue(character['아이디']) }}</div>
                  </div>

                  <div class="rounded-2xl bg-white/80 border border-gray-200 px-4 py-3 shadow-sm">
                    <div class="text-xs text-apple-secondary">클래스</div>
                    <div class="mt-1 text-sm font-semibold text-apple-black">{{ displayValue(displayClass) }}</div>
                  </div>

                  <div class="rounded-2xl bg-white/80 border border-gray-200 px-4 py-3 shadow-sm">
                    <div class="text-xs text-apple-secondary">전문화</div>
                    <div class="mt-1 text-sm font-semibold text-apple-black">{{ displayValue(displaySpec) }}</div>
                  </div>
                </div>

                <div v-else-if="activeTab === 'stats'" class="rounded-2xl bg-white/80 border border-gray-200 shadow-sm overflow-hidden">
                  <div v-if="!combatStats && !bundleStatistics" class="px-4 py-4 text-sm text-apple-secondary">전투능력치 정보가 없습니다.</div>
                  <div v-else-if="!combatStats && bundleStatistics" class="p-4 space-y-6">
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                      <div class="rounded-2xl bg-white/80 border border-gray-200 px-4 py-3 shadow-sm">
                        <div class="text-xs text-apple-secondary">체력</div>
                        <div class="mt-1 text-sm font-semibold text-apple-black tabular-nums">{{ (blizzResource?.health ?? 0).toLocaleString?.() ?? displayValue(blizzResource?.health) }}</div>
                      </div>
                      <div class="rounded-2xl bg-white/80 border border-gray-200 px-4 py-3 shadow-sm">
                        <div class="text-xs text-apple-secondary">자원</div>
                        <div class="mt-1 text-sm font-semibold text-apple-black tabular-nums">{{ (blizzResource?.power ?? 0).toLocaleString?.() ?? displayValue(blizzResource?.power) }}</div>
                        <div class="mt-1 text-xs text-apple-secondary">{{ blizzResource?.powerType || '—' }}</div>
                      </div>
                      <div class="rounded-2xl bg-white/80 border border-gray-200 px-4 py-3 shadow-sm">
                        <div class="text-xs text-apple-secondary">이동 속도</div>
                        <div class="mt-1 text-sm font-semibold text-apple-black tabular-nums">{{ blizzSecondaryStats?.speed !== null && blizzSecondaryStats?.speed !== undefined ? `${blizzSecondaryStats.speed.toFixed(2)}%` : '—' }}</div>
                      </div>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div class="rounded-2xl bg-white/80 border border-gray-200 shadow-sm overflow-hidden">
                        <div class="px-4 py-3 border-b border-gray-100/80 text-xs font-semibold tracking-widest uppercase text-apple-secondary">주능력치</div>
                        <div class="p-4 space-y-2 text-sm">
                          <div class="flex items-center justify-between">
                            <div class="text-apple-secondary">힘</div>
                            <div class="font-semibold text-apple-black tabular-nums">{{ displayValue(blizzPrimaryStats?.strength) }}</div>
                          </div>
                          <div class="flex items-center justify-between">
                            <div class="text-apple-secondary">민첩</div>
                            <div class="font-semibold text-apple-black tabular-nums">{{ displayValue(blizzPrimaryStats?.agility) }}</div>
                          </div>
                          <div class="flex items-center justify-between">
                            <div class="text-apple-secondary">지능</div>
                            <div class="font-semibold text-apple-black tabular-nums">{{ displayValue(blizzPrimaryStats?.intellect) }}</div>
                          </div>
                          <div class="flex items-center justify-between">
                            <div class="text-apple-secondary">체력</div>
                            <div class="font-semibold text-apple-black tabular-nums">{{ displayValue(blizzPrimaryStats?.stamina) }}</div>
                          </div>
                        </div>
                      </div>

                      <div class="rounded-2xl bg-white/80 border border-gray-200 shadow-sm overflow-hidden">
                        <div class="px-4 py-3 border-b border-gray-100/80 text-xs font-semibold tracking-widest uppercase text-apple-secondary">보조능력치</div>
                        <div class="p-4 space-y-2 text-sm">
                          <div class="flex items-center justify-between">
                            <div class="text-apple-secondary">치명타</div>
                            <div class="font-semibold text-apple-black tabular-nums">{{ blizzSecondaryStats?.crit !== null && blizzSecondaryStats?.crit !== undefined ? `${blizzSecondaryStats.crit.toFixed(2)}%` : '—' }}</div>
                          </div>
                          <div class="flex items-center justify-between">
                            <div class="text-apple-secondary">가속</div>
                            <div class="font-semibold text-apple-black tabular-nums">{{ blizzSecondaryStats?.haste !== null && blizzSecondaryStats?.haste !== undefined ? `${blizzSecondaryStats.haste.toFixed(2)}%` : '—' }}</div>
                          </div>
                          <div class="flex items-center justify-between">
                            <div class="text-apple-secondary">특화</div>
                            <div class="font-semibold text-apple-black tabular-nums">{{ blizzSecondaryStats?.mastery !== null && blizzSecondaryStats?.mastery !== undefined ? `${blizzSecondaryStats.mastery.toFixed(2)}%` : '—' }}</div>
                          </div>
                          <div class="flex items-center justify-between">
                            <div class="text-apple-secondary">유연성(가한 피해)</div>
                            <div class="font-semibold text-apple-black tabular-nums">{{ blizzSecondaryStats?.versatilityDone !== null && blizzSecondaryStats?.versatilityDone !== undefined ? `${blizzSecondaryStats.versatilityDone.toFixed(2)}%` : '—' }}</div>
                          </div>
                          <div class="flex items-center justify-between">
                            <div class="text-apple-secondary">유연성(받는 피해)</div>
                            <div class="font-semibold text-apple-black tabular-nums">{{ blizzSecondaryStats?.versatilityTaken !== null && blizzSecondaryStats?.versatilityTaken !== undefined ? `${blizzSecondaryStats.versatilityTaken.toFixed(2)}%` : '—' }}</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div v-else class="p-4 grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <div class="text-xs font-semibold tracking-widest uppercase text-apple-secondary">주능력치</div>
                      <div class="mt-3 space-y-2 text-sm">
                        <div v-for="(v, k) in (combatStats['주능력치'] || {})" :key="k" class="flex items-center justify-between">
                          <div class="text-apple-secondary">{{ k }}</div>
                          <div class="font-semibold text-apple-black tabular-nums">{{ displayValue(v) }}</div>
                        </div>
                      </div>
                    </div>

                    <div>
                      <div class="text-xs font-semibold tracking-widest uppercase text-apple-secondary">보조능력치</div>
                      <div class="mt-3 space-y-2 text-sm">
                        <div v-for="(v, k) in (combatStats['보조능력치'] || {})" :key="k" class="flex items-center justify-between">
                          <div class="text-apple-secondary">{{ k }}</div>
                          <div class="font-semibold text-apple-black tabular-nums">{{ displayValue(v) }}</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div v-else-if="activeTab === 'talents'" class="rounded-2xl bg-white/80 border border-gray-200 shadow-sm overflow-hidden">
                  <div v-if="talentRows.length === 0 && !bundleSpecializations" class="px-4 py-4 text-sm text-apple-secondary">특성 정보가 없습니다.</div>
                  <div v-else-if="talentRows.length === 0 && bundleSpecializations" class="p-4 space-y-6">
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                      <div class="rounded-2xl bg-white/80 border border-gray-200 px-4 py-3 shadow-sm">
                        <div class="text-xs text-apple-secondary">활성 전문화</div>
                        <div class="mt-1 text-sm font-semibold text-apple-black">{{ blizzSpecs?.active_specialization?.name || displaySpec || '—' }}</div>
                      </div>
                      <div class="rounded-2xl bg-white/80 border border-gray-200 px-4 py-3 shadow-sm">
                        <div class="text-xs text-apple-secondary">영웅 특성</div>
                        <div class="mt-1 text-sm font-semibold text-apple-black">{{ activeHeroTalentTreeName || '—' }}</div>
                      </div>
                      <div class="rounded-2xl bg-white/80 border border-gray-200 px-4 py-3 shadow-sm">
                        <div class="text-xs text-apple-secondary">로드아웃</div>
                        <div class="mt-1 text-sm font-semibold text-apple-black">{{ activeLoadout ? '활성' : '—' }}</div>
                      </div>
                    </div>

                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                      <div class="rounded-2xl bg-white/80 border border-gray-200 shadow-sm overflow-hidden">
                        <div class="px-4 py-3 border-b border-gray-100/80 text-xs font-semibold tracking-widest uppercase text-apple-secondary">직업 특성</div>
                        <div v-if="activeClassTalents.length === 0" class="px-4 py-4 text-sm text-apple-secondary">—</div>
                        <div v-else class="divide-y divide-gray-100/80">
                          <div v-for="(t, idx) in activeClassTalents" :key="idx" class="px-4 py-3">
                            <div class="text-sm font-semibold text-apple-black">
                              <a v-if="talentSpellId(t)" :href="`https://www.wowhead.com/spell=${talentSpellId(t)}`" :data-wowhead="`spell=${talentSpellId(t)}`" target="_blank" rel="noreferrer">
                                {{ talentTitle(t) || '—' }}
                              </a>
                              <span v-else>{{ talentTitle(t) || '—' }}</span>
                            </div>
                            <div v-if="t.rank" class="mt-1 text-xs text-apple-secondary">Rank {{ t.rank }}</div>
                            <div v-if="talentDescription(t)" class="mt-2 text-xs text-apple-secondary whitespace-pre-wrap">{{ talentDescription(t) }}</div>
                          </div>
                        </div>
                      </div>

                      <div class="rounded-2xl bg-white/80 border border-gray-200 shadow-sm overflow-hidden">
                        <div class="px-4 py-3 border-b border-gray-100/80 text-xs font-semibold tracking-widest uppercase text-apple-secondary">전문화 특성</div>
                        <div v-if="activeSpecTalents.length === 0" class="px-4 py-4 text-sm text-apple-secondary">—</div>
                        <div v-else class="divide-y divide-gray-100/80">
                          <div v-for="(t, idx) in activeSpecTalents" :key="idx" class="px-4 py-3">
                            <div class="text-sm font-semibold text-apple-black">
                              <a v-if="talentSpellId(t)" :href="`https://www.wowhead.com/spell=${talentSpellId(t)}`" :data-wowhead="`spell=${talentSpellId(t)}`" target="_blank" rel="noreferrer">
                                {{ talentTitle(t) || '—' }}
                              </a>
                              <span v-else>{{ talentTitle(t) || '—' }}</span>
                            </div>
                            <div v-if="t.rank" class="mt-1 text-xs text-apple-secondary">Rank {{ t.rank }}</div>
                            <div v-if="talentDescription(t)" class="mt-2 text-xs text-apple-secondary whitespace-pre-wrap">{{ talentDescription(t) }}</div>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                      <div class="rounded-2xl bg-white/80 border border-gray-200 shadow-sm overflow-hidden">
                        <div class="px-4 py-3 border-b border-gray-100/80 text-xs font-semibold tracking-widest uppercase text-apple-secondary">영웅 특성</div>
                        <div v-if="activeHeroTalents.length === 0" class="px-4 py-4 text-sm text-apple-secondary">—</div>
                        <div v-else class="divide-y divide-gray-100/80">
                          <div v-for="(t, idx) in activeHeroTalents" :key="idx" class="px-4 py-3">
                            <div class="text-sm font-semibold text-apple-black">
                              <a v-if="talentSpellId(t)" :href="`https://www.wowhead.com/spell=${talentSpellId(t)}`" :data-wowhead="`spell=${talentSpellId(t)}`" target="_blank" rel="noreferrer">
                                {{ talentTitle(t) || '—' }}
                              </a>
                              <span v-else>{{ talentTitle(t) || '—' }}</span>
                            </div>
                            <div v-if="t.rank" class="mt-1 text-xs text-apple-secondary">Rank {{ t.rank }}</div>
                            <div v-if="talentDescription(t)" class="mt-2 text-xs text-apple-secondary whitespace-pre-wrap">{{ talentDescription(t) }}</div>
                          </div>
                        </div>
                      </div>

                      <div class="rounded-2xl bg-white/80 border border-gray-200 shadow-sm overflow-hidden">
                        <div class="px-4 py-3 border-b border-gray-100/80 text-xs font-semibold tracking-widest uppercase text-apple-secondary">PvP 특성</div>
                        <div v-if="activePvpTalents.length === 0" class="px-4 py-4 text-sm text-apple-secondary">—</div>
                        <div v-else class="divide-y divide-gray-100/80">
                          <div v-for="(t, idx) in activePvpTalents" :key="idx" class="px-4 py-3">
                            <div class="text-sm font-semibold text-apple-black">
                              <span>{{ t.slot ? `Slot ${t.slot}` : 'Slot' }} · </span>
                              <a v-if="t.spellId" :href="`https://www.wowhead.com/spell=${t.spellId}`" :data-wowhead="`spell=${t.spellId}`" target="_blank" rel="noreferrer">{{ t.name }}</a>
                              <span v-else>{{ t.name }}</span>
                            </div>
                            <div v-if="t.description" class="mt-2 text-xs text-apple-secondary whitespace-pre-wrap">{{ t.description }}</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div v-else class="overflow-x-auto">
                    <table class="min-w-full text-left">
                      <thead class="bg-apple-gray/60">
                        <tr class="text-xs uppercase tracking-widest text-apple-secondary">
                          <th class="px-4 py-3 font-semibold">이름</th>
                          <th class="px-4 py-3 font-semibold">레벨</th>
                          <th class="px-4 py-3 font-semibold">설명</th>
                        </tr>
                      </thead>
                      <tbody class="divide-y divide-gray-100/80">
                        <tr v-for="(t, idx) in talentRows" :key="idx" class="hover:bg-white transition-colors">
                          <td class="px-4 py-3 text-sm font-semibold text-apple-black">{{ t['이름'] }}</td>
                          <td class="px-4 py-3 text-sm text-apple-black tabular-nums">{{ displayValue(t['레벨']) }}</td>
                          <td class="px-4 py-3 text-sm text-apple-secondary">{{ displayValue(t['설명']) }}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>

                <div v-else-if="activeTab === 'gear'" class="rounded-2xl bg-white/80 border border-gray-200 shadow-sm overflow-hidden">
                  <div v-if="equipmentRows.length === 0 && !bundleEquipment" class="px-4 py-4 text-sm text-apple-secondary">장비 정보가 없습니다.</div>
                  <div v-else-if="equipmentRows.length === 0 && bundleEquipment" class="p-4">
                    <pre class="text-xs text-apple-black/80 whitespace-pre-wrap break-words">{{ JSON.stringify(bundleEquipment, null, 2) }}</pre>
                  </div>
                  <div v-else class="overflow-x-auto">
                    <table class="min-w-full text-left">
                      <thead class="bg-apple-gray/60">
                        <tr class="text-xs uppercase tracking-widest text-apple-secondary">
                          <th class="px-4 py-3 font-semibold">부위</th>
                          <th class="px-4 py-3 font-semibold">아이템</th>
                          <th class="px-4 py-3 font-semibold">품질</th>
                          <th class="px-4 py-3 font-semibold">iLv</th>
                        </tr>
                      </thead>
                      <tbody class="divide-y divide-gray-100/80">
                        <tr v-for="(g, idx) in equipmentRows" :key="idx" class="hover:bg-white transition-colors">
                          <td class="px-4 py-3 text-sm font-semibold text-apple-black">{{ displayValue(g['부위']) }}</td>
                          <td class="px-4 py-3">
                            <div class="text-sm font-semibold text-apple-black">{{ displayValue(g['아이템명']) }}</div>
                            <div class="text-xs text-apple-secondary tabular-nums">#{{ displayValue(g['아이템아이디']) }}</div>
                          </td>
                          <td class="px-4 py-3 text-sm text-apple-black">{{ displayValue(g['품질']) }}</td>
                          <td class="px-4 py-3 text-sm text-apple-black tabular-nums">{{ displayValue(g['아이템레벨']) }}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>

                <div v-else-if="activeTab === 'rio'" class="rounded-2xl bg-white/80 border border-gray-200 shadow-sm overflow-hidden">
                  <div v-if="rioErrorMessage" class="px-4 py-4 text-sm text-red-600">{{ rioErrorMessage }}</div>
                  <div v-else-if="!rio" class="px-4 py-4 text-sm text-apple-secondary">RIO 정보가 없습니다.</div>
                  <div v-else class="p-4">
                    <div class="text-xs font-semibold tracking-widest uppercase text-apple-secondary">Mythic Rating</div>
                    <div class="mt-2 text-2xl font-bold text-apple-black tabular-nums">{{ rioScore ?? '—' }}</div>
                    <div class="mt-2 text-xs text-apple-secondary">{{ displayRealm }} / {{ displayName }}</div>
                  </div>
                </div>

                <div v-else-if="activeTab === 'raw'" class="rounded-2xl bg-white/80 border border-gray-200 shadow-sm overflow-hidden">
                  <div v-if="rawCharacterErrorMessage" class="px-4 py-4 text-sm text-red-600">{{ rawCharacterErrorMessage }}</div>
                  <div v-else-if="!rawCharacter" class="px-4 py-4 text-sm text-apple-secondary">원본 캐릭터 정보가 없습니다.</div>
                  <div v-else class="p-4">
                    <pre class="text-xs text-apple-black/80 whitespace-pre-wrap break-words">{{ JSON.stringify(rawCharacter, null, 2) }}</pre>
                  </div>
                </div>

                <div v-else class="text-sm text-apple-secondary">—</div>
              </div>
            </div>
          </div>

          <div class="mt-6 rounded-2xl bg-white/50 border border-gray-200 px-4 py-3 text-xs text-apple-secondary">
            API 우선순위: <span class="font-semibold">/api/character</span> → 실패 시 <span class="font-semibold">/character/{realm}/{name}</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
