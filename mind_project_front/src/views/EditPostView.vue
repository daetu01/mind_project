<script setup>
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route  = useRoute()
const router = useRouter()

const DUNGEONS = [
  '아라카라', '스레드의 도시', '그림 배톨', '스톤볼트',
  '던브레이커', '티르나 시의 안개', '보랄루스 공성전', '부식 괴멸',
]

/* ── Load post from router state ───────────────────────── */
const original = history.state?.post ?? null
const postType = computed(() => original?.dungeon ? 'key' : 'raid')

/* ── Raid form ─────────────────────────────────────────── */
const raidForm = ref({
  guild:      original?.guild      ?? '',
  realm:      original?.realm      ?? '',
  raid:       original?.raid       ?? '네루바르 궁전',
  difficulty: original?.difficulty ?? 'Heroic',
  progress:   original?.progress   ?? '',
  tankSlots:  original?.slots?.tank ?? 0,
  healSlots:  original?.slots?.heal ?? 1,
  dpsSlots:   original?.slots?.dps  ?? 2,
  ilvlReq:    original?.ilvlReq    ?? '',
  wclReq:     original?.wclReq     ?? '',
  voice:      original?.voice      ?? false,
  schedule:   original?.schedule   ?? '',
  region:     original?.region     ?? 'KR',
  note:       original?.note       ?? '',
})

/* ── Keystone form ─────────────────────────────────────── */
const keyForm = ref({
  player:    original?.player    ?? '',
  realm:     original?.realm     ?? '',
  dungeon:   original?.dungeon   ?? '아라카라',
  keyLevel:  original?.keyLevel  ?? 10,
  tankSlots: original?.slots?.tank ?? 0,
  healSlots: original?.slots?.heal ?? 1,
  dpsSlots:  original?.slots?.dps  ?? 2,
  rioReq:    original?.rioReq    ?? '',
  ilvlReq:   original?.ilvlReq   ?? '',
  voice:     original?.voice     ?? false,
  goal:      original?.goal      ?? 'any',
  region:    original?.region    ?? 'KR',
  note:      original?.note      ?? '',
})

function keyColor(lv) {
  if (lv >= 20) return '#ff8000'
  if (lv >= 15) return '#a335ee'
  if (lv >= 10) return '#0070dd'
  return '#6b6b8a'
}

const keyPct = computed(() => ((+keyForm.value.keyLevel - 2) / 23 * 100).toFixed(1))

/* ── Save ──────────────────────────────────────────────── */
const saved = ref(false)

function save() {
  saved.value = true
  setTimeout(() => router.push({ name: 'lfg' }), 1200)
}

function cancel() {
  router.push({ name: 'lfg' })
}
</script>

<template>
  <section class="px-4 sm:px-6 lg:px-8 py-14">
    <div class="max-w-2xl mx-auto">

      <!-- Header -->
      <div class="flex items-center gap-3 mb-2">
        <button type="button"
          class="flex items-center gap-1.5 text-steel hover:text-silver text-sm font-semibold transition-colors"
          @click="cancel">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/>
          </svg>
          목록으로
        </button>
      </div>

      <h1 class="text-3xl md:text-4xl font-bold tracking-tighter text-silver mb-1">
        모집글 수정
      </h1>
      <p class="text-steel text-sm mb-8">
        <span v-if="postType==='raid'">공격대 모집글 · </span>
        <span v-else>쐐기 파티 모집글 · </span>
        <span class="text-iron">ID {{ route.params.id }}</span>
      </p>

      <!-- No post found -->
      <div v-if="!original"
           class="rounded-[2rem] border border-rim/50 p-12 text-center"
           style="background:var(--bg-card)">
        <div class="text-steel text-sm mb-4">수정할 게시글 데이터를 찾을 수 없습니다.</div>
        <button type="button"
          class="h-10 px-5 rounded-full text-sm font-semibold text-steel border border-rim/60 hover:text-silver transition-all"
          style="background:var(--bg-button)"
          @click="cancel">공대 모집 목록으로</button>
      </div>

      <!-- ── RAID EDIT FORM ────────────────────────────── -->
      <div v-else-if="postType==='raid'"
           class="rounded-[2rem] border border-rim/50 overflow-hidden"
           style="background:var(--bg-card-strong);backdrop-filter:blur(16px)">

        <div class="px-8 py-5 border-b border-rim/40 flex items-center gap-3">
          <div class="w-2 h-2 rounded-full" style="background:#a335ee"></div>
          <span class="text-sm font-semibold text-silver">공격대 모집 정보</span>
        </div>

        <div class="px-8 py-8 flex flex-col gap-5">
          <!-- Guild + Realm -->
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">길드명</label>
              <input v-model="raidForm.guild" type="text" placeholder="어둠의 파수꾼"
                class="w-full h-11 rounded-full border border-rim/60 px-4 text-sm text-silver placeholder:text-iron
                       focus:outline-none focus:ring-2 focus:ring-wow-epic/40 transition-all"
                style="background:var(--bg-input)"/>
            </div>
            <div>
              <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">서버</label>
              <input v-model="raidForm.realm" type="text" placeholder="데스윙"
                class="w-full h-11 rounded-full border border-rim/60 px-4 text-sm text-silver placeholder:text-iron
                       focus:outline-none focus:ring-2 focus:ring-wow-epic/40 transition-all"
                style="background:var(--bg-input)"/>
            </div>
          </div>

          <!-- Raid + Difficulty -->
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">레이드</label>
              <select v-model="raidForm.raid"
                class="w-full h-11 rounded-full border border-rim/60 px-4 text-sm text-silver
                       focus:outline-none focus:ring-2 focus:ring-wow-epic/40 transition-all"
                style="background:var(--bg-input)">
                <option>네루바르 궁전</option>
                <option>아문 타울 니루프</option>
              </select>
            </div>
            <div>
              <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">난이도</label>
              <div class="flex gap-2">
                <button v-for="d in ['Normal','Heroic','Mythic']" :key="d" type="button"
                  class="flex-1 h-11 rounded-full border text-xs font-semibold transition-all"
                  :style="raidForm.difficulty===d
                    ?'background:#a335ee;border-color:#a335ee;color:#fff'
                    :'background:var(--bg-button);border-color:var(--border-subtle);color:#6b6b8a'"
                  @click="raidForm.difficulty=d">{{ d[0] }}</button>
              </div>
            </div>
          </div>

          <!-- Progress + Slots -->
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">진행도</label>
              <input v-model="raidForm.progress" type="text" placeholder="9/9"
                class="w-full h-11 rounded-full border border-rim/60 px-4 text-sm text-silver placeholder:text-iron
                       focus:outline-none focus:ring-2 focus:ring-wow-epic/40 transition-all"
                style="background:var(--bg-input)"/>
            </div>
            <div>
              <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">모집 인원</label>
              <div class="grid grid-cols-3 gap-2">
                <div>
                  <div class="text-[10px] text-steel mb-1 text-center">탱커</div>
                  <input v-model.number="raidForm.tankSlots" type="number" min="0" max="5"
                    class="w-full h-11 rounded-xl border border-rim/60 px-2 text-sm text-silver text-center
                           focus:outline-none transition-all"
                    style="background:var(--bg-input)"/>
                </div>
                <div>
                  <div class="text-[10px] text-steel mb-1 text-center">힐러</div>
                  <input v-model.number="raidForm.healSlots" type="number" min="0" max="10"
                    class="w-full h-11 rounded-xl border border-rim/60 px-2 text-sm text-silver text-center
                           focus:outline-none transition-all"
                    style="background:var(--bg-input)"/>
                </div>
                <div>
                  <div class="text-[10px] text-steel mb-1 text-center">딜러</div>
                  <input v-model.number="raidForm.dpsSlots" type="number" min="0" max="20"
                    class="w-full h-11 rounded-xl border border-rim/60 px-2 text-sm text-silver text-center
                           focus:outline-none transition-all"
                    style="background:var(--bg-input)"/>
                </div>
              </div>
            </div>
          </div>

          <!-- Reqs -->
          <div class="grid grid-cols-3 gap-3">
            <div>
              <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">최소 아이템 레벨</label>
              <input v-model.number="raidForm.ilvlReq" type="number" placeholder="619"
                class="w-full h-11 rounded-full border border-rim/60 px-4 text-sm text-silver placeholder:text-iron
                       focus:outline-none focus:ring-2 focus:ring-wow-epic/40 transition-all"
                style="background:var(--bg-input)"/>
            </div>
            <div>
              <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">WCL 점수</label>
              <input v-model.number="raidForm.wclReq" type="number" placeholder="75"
                class="w-full h-11 rounded-full border border-rim/60 px-4 text-sm text-silver placeholder:text-iron
                       focus:outline-none focus:ring-2 focus:ring-wow-epic/40 transition-all"
                style="background:var(--bg-input)"/>
            </div>
            <div>
              <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">지역</label>
              <select v-model="raidForm.region"
                class="w-full h-11 rounded-full border border-rim/60 px-4 text-sm text-silver
                       focus:outline-none focus:ring-2 focus:ring-wow-epic/40 transition-all"
                style="background:var(--bg-input)">
                <option>KR</option><option>US</option><option>EU</option>
              </select>
            </div>
          </div>

          <!-- Schedule + Voice -->
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">공대 일정</label>
              <input v-model="raidForm.schedule" type="text" placeholder="월수금 21:00~24:00"
                class="w-full h-11 rounded-full border border-rim/60 px-4 text-sm text-silver placeholder:text-iron
                       focus:outline-none focus:ring-2 focus:ring-wow-epic/40 transition-all"
                style="background:var(--bg-input)"/>
            </div>
            <div class="flex items-end pb-0.5">
              <label class="flex items-center gap-3 cursor-pointer">
                <div class="relative">
                  <input v-model="raidForm.voice" type="checkbox" class="sr-only"/>
                  <div class="w-10 h-6 rounded-full transition-all duration-200"
                       :style="raidForm.voice?'background:#a335ee':'background:var(--border-subtle)'"></div>
                  <div class="absolute top-1 w-4 h-4 rounded-full bg-white shadow transition-all duration-200"
                       :style="raidForm.voice?'left:22px':'left:4px'"></div>
                </div>
                <span class="text-sm font-semibold text-silver">음성 채팅 필수</span>
              </label>
            </div>
          </div>

          <!-- Note -->
          <div>
            <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">한 줄 소개</label>
            <textarea v-model="raidForm.note" rows="3" placeholder="공대 설명, 요구 사항, 분위기 등..."
              class="w-full rounded-2xl border border-rim/60 px-4 py-3 text-sm text-silver placeholder:text-iron
                     focus:outline-none focus:ring-2 focus:ring-wow-epic/40 resize-none transition-all"
              style="background:var(--bg-input)"></textarea>
          </div>
        </div>

        <!-- Actions -->
        <div class="px-8 pb-8 flex gap-3">
          <button type="button"
            class="flex-1 h-12 rounded-full font-semibold text-sm text-white transition-all duration-200 hover:-translate-y-0.5"
            style="background:#a335ee;box-shadow:0 8px 24px rgba(163,53,238,0.3)"
            @click="save">
            <span v-if="!saved">변경 사항 저장</span>
            <span v-else class="flex items-center justify-center gap-2">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
              </svg>
              저장됐습니다!
            </span>
          </button>
          <button type="button"
            class="h-12 px-6 rounded-full border border-rim/60 text-sm font-semibold text-steel hover:text-silver hover:border-rim transition-all"
            style="background:var(--bg-button)"
            @click="cancel">
            취소
          </button>
        </div>
      </div>

      <!-- ── KEYSTONE EDIT FORM ──────────────────────────── -->
      <div v-else
           class="rounded-[2rem] border overflow-hidden"
           style="background:var(--bg-card-strong);backdrop-filter:blur(16px);border-color:rgba(255,128,0,0.2)">

        <div class="px-8 py-5 border-b border-rim/40 flex items-center gap-3">
          <div class="w-2 h-2 rounded-full" style="background:#ff8000"></div>
          <span class="text-sm font-semibold text-silver">쐐기 파티 모집 정보</span>
          <span class="ml-auto px-3 py-1 rounded-full text-xs font-bold"
                style="background:rgba(255,128,0,0.12);color:#ff8000">Mythic+</span>
        </div>

        <div class="px-8 py-8 flex flex-col gap-5">
          <!-- Player + Realm -->
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">캐릭터명</label>
              <input v-model="keyForm.player" type="text" placeholder="Frostmourne"
                class="w-full h-11 rounded-full border border-rim/60 px-4 text-sm text-silver placeholder:text-iron
                       focus:outline-none focus:ring-2 focus:ring-wow-legendary/40 transition-all"
                style="background:var(--bg-input)"/>
            </div>
            <div>
              <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">서버</label>
              <input v-model="keyForm.realm" type="text" placeholder="데스윙"
                class="w-full h-11 rounded-full border border-rim/60 px-4 text-sm text-silver placeholder:text-iron
                       focus:outline-none focus:ring-2 focus:ring-wow-legendary/40 transition-all"
                style="background:var(--bg-input)"/>
            </div>
          </div>

          <!-- Dungeon -->
          <div>
            <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">던전</label>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
              <button v-for="d in DUNGEONS" :key="d" type="button"
                class="h-10 rounded-xl border text-xs font-semibold transition-all px-2 text-center"
                :style="keyForm.dungeon===d
                  ?'background:#ff8000;border-color:#ff8000;color:#fff'
                  :'background:var(--bg-button);border-color:var(--border-subtle);color:#6b6b8a'"
                @click="keyForm.dungeon=d">{{ d }}</button>
            </div>
          </div>

          <!-- Key level -->
          <div>
            <div class="flex items-center justify-between mb-3">
              <label class="text-xs font-semibold tracking-widest uppercase text-steel">키 레벨</label>
              <div class="flex items-center gap-1.5 px-3 py-1 rounded-lg text-sm font-bold"
                   :style="`background:${+keyForm.keyLevel>=20?'rgba(255,128,0,0.15)':+keyForm.keyLevel>=15?'rgba(163,53,238,0.15)':+keyForm.keyLevel>=10?'rgba(0,112,221,0.15)':'var(--bg-dim)'};
                            color:${keyColor(+keyForm.keyLevel)}`">
                <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                  <path stroke-linecap="round" stroke-linejoin="round"
                        d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/>
                </svg>
                +{{ keyForm.keyLevel }}
              </div>
            </div>
            <input v-model.number="keyForm.keyLevel" type="range" min="2" max="25" step="1"
              class="key-slider w-full h-2 rounded-full appearance-none cursor-pointer"
              :style="`background:linear-gradient(to right,${keyColor(+keyForm.keyLevel)} 0%,${keyColor(+keyForm.keyLevel)} ${keyPct}%,var(--border-subtle) ${keyPct}%,var(--border-subtle) 100%)`"/>
            <div class="flex justify-between text-[10px] text-iron mt-1.5 px-0.5">
              <span>+2</span>
              <span class="text-steel">+10</span>
              <span class="text-wow-epic">+15</span>
              <span class="text-wow-legendary">+20</span>
              <span>+25</span>
            </div>
          </div>

          <!-- Slots -->
          <div>
            <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">모집 인원</label>
            <div class="grid grid-cols-3 gap-3">
              <div>
                <div class="text-[10px] text-steel mb-1 text-center">탱커</div>
                <input v-model.number="keyForm.tankSlots" type="number" min="0" max="1"
                  class="w-full h-11 rounded-xl border border-rim/60 px-2 text-sm text-silver text-center
                         focus:outline-none transition-all"
                  style="background:var(--bg-input)"/>
              </div>
              <div>
                <div class="text-[10px] text-steel mb-1 text-center">힐러</div>
                <input v-model.number="keyForm.healSlots" type="number" min="0" max="1"
                  class="w-full h-11 rounded-xl border border-rim/60 px-2 text-sm text-silver text-center
                         focus:outline-none transition-all"
                  style="background:var(--bg-input)"/>
              </div>
              <div>
                <div class="text-[10px] text-steel mb-1 text-center">딜러</div>
                <input v-model.number="keyForm.dpsSlots" type="number" min="0" max="3"
                  class="w-full h-11 rounded-xl border border-rim/60 px-2 text-sm text-silver text-center
                         focus:outline-none transition-all"
                  style="background:var(--bg-input)"/>
              </div>
            </div>
          </div>

          <!-- Reqs + Region -->
          <div class="grid grid-cols-3 gap-3">
            <div>
              <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">최소 RIO</label>
              <input v-model.number="keyForm.rioReq" type="number" placeholder="2800"
                class="w-full h-11 rounded-full border border-rim/60 px-4 text-sm text-silver placeholder:text-iron
                       focus:outline-none focus:ring-2 focus:ring-wow-legendary/40 transition-all"
                style="background:var(--bg-input)"/>
            </div>
            <div>
              <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">최소 아이템 레벨</label>
              <input v-model.number="keyForm.ilvlReq" type="number" placeholder="636"
                class="w-full h-11 rounded-full border border-rim/60 px-4 text-sm text-silver placeholder:text-iron
                       focus:outline-none focus:ring-2 focus:ring-wow-legendary/40 transition-all"
                style="background:var(--bg-input)"/>
            </div>
            <div>
              <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">지역</label>
              <select v-model="keyForm.region"
                class="w-full h-11 rounded-full border border-rim/60 px-4 text-sm text-silver
                       focus:outline-none focus:ring-2 focus:ring-wow-legendary/40 transition-all"
                style="background:var(--bg-input)">
                <option>KR</option><option>US</option><option>EU</option>
              </select>
            </div>
          </div>

          <!-- Goal + Voice -->
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">목표</label>
              <div class="grid grid-cols-3 gap-2">
                <button v-for="[v,l,c] in [['timer','타이머','#ff8000'],['clear','클리어','#0070dd'],['any','상관없음','#6b6b8a']]"
                  :key="v" type="button"
                  class="h-11 rounded-full border text-xs font-semibold transition-all"
                  :style="keyForm.goal===v?`background:${c};border-color:${c};color:#fff`
                    :'background:var(--bg-button);border-color:var(--border-subtle);color:#6b6b8a'"
                  @click="keyForm.goal=v">{{ l }}</button>
              </div>
            </div>
            <div class="flex items-end pb-1">
              <label class="flex items-center gap-3 cursor-pointer">
                <div class="relative">
                  <input v-model="keyForm.voice" type="checkbox" class="sr-only"/>
                  <div class="w-10 h-6 rounded-full transition-all duration-200"
                       :style="keyForm.voice?'background:#ff8000':'background:var(--border-subtle)'"></div>
                  <div class="absolute top-1 w-4 h-4 rounded-full bg-white shadow transition-all duration-200"
                       :style="keyForm.voice?'left:22px':'left:4px'"></div>
                </div>
                <span class="text-sm font-semibold text-silver">음성 채팅 필수</span>
              </label>
            </div>
          </div>

          <!-- Note -->
          <div>
            <label class="text-xs font-semibold tracking-widest uppercase text-steel mb-2 block">한 줄 소개</label>
            <textarea v-model="keyForm.note" rows="3" placeholder="던전 설명, 요구 사항..."
              class="w-full rounded-2xl border border-rim/60 px-4 py-3 text-sm text-silver placeholder:text-iron
                     focus:outline-none focus:ring-2 focus:ring-wow-legendary/40 resize-none transition-all"
              style="background:var(--bg-input)"></textarea>
          </div>
        </div>

        <!-- Actions -->
        <div class="px-8 pb-8 flex gap-3">
          <button type="button"
            class="flex-1 h-12 rounded-full font-semibold text-sm text-white transition-all duration-200 hover:-translate-y-0.5"
            style="background:#ff8000;color:#080810;box-shadow:0 8px 24px rgba(255,128,0,0.3)"
            @click="save">
            <span v-if="!saved">변경 사항 저장</span>
            <span v-else class="flex items-center justify-center gap-2">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
              </svg>
              저장됐습니다!
            </span>
          </button>
          <button type="button"
            class="h-12 px-6 rounded-full border border-rim/60 text-sm font-semibold text-steel hover:text-silver hover:border-rim transition-all"
            style="background:var(--bg-button)"
            @click="cancel">
            취소
          </button>
        </div>
      </div>

    </div>
  </section>
</template>
