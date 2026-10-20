<template>
  <div class="graph-wrap">
    <div class="graph-toolbar">
      <div class="seg">
        <button v-for="t in typeFilters" :key="t.key" :class="{ active: activeTypes.includes(t.key) }" @click="toggleType(t.key)">
          <span class="dot" :style="{ background: t.color }"></span>{{ t.label }}
        </button>
      </div>
      <div class="legend">
        <span class="lg"><span class="dot" style="background:var(--theme-force)"></span>主题</span>
        <span class="lg"><span class="dot" style="background:var(--fail)"></span>攻破轮(FAIL)</span>
        <span class="lg"><span class="dot" style="background:var(--ok)"></span>正确核</span>
        <span class="lg"><span class="dot" style="background:var(--boundary)"></span>降级/边界</span>
        <span class="lg"><span class="dot" style="background:var(--fail)"></span>黑名单</span>
      </div>
      <button class="btn" @click="restart">重排</button>
    </div>
    <div class="graph-stage" ref="stage" @pointermove="onMove" @pointerup="onUp" @pointerleave="onUp">
      <svg :width="W" :height="H" @pointerdown="onStageDown">
        <defs>
          <marker id="arr" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto">
            <path d="M0,0 L6,3 L0,6 Z" fill="#3a4a6a" />
          </marker>
        </defs>
        <g v-for="(e, i) in visibleEdges" :key="'e' + i">
          <line :x1="pos[e.source].x" :y1="pos[e.source].y" :x2="pos[e.target].x" :y2="pos[e.target].y"
                :stroke="edgeColor(e.kind)" :stroke-width="e.kind === 'member' ? 1.4 : 1"
                :stroke-dasharray="e.kind === 'registers' ? '4 3' : (e.kind === 'downgrades' ? '2 3' : 'none')"
                :opacity="0.55" />
        </g>
        <g v-for="n in visibleNodes" :key="n.id">
          <circle :cx="pos[n.id].x" :cy="pos[n.id].y" :r="nodeR(n)" :fill="n.color"
                  :stroke="selected === n.id ? '#fff' : 'rgba(255,255,255,.18)'" :stroke-width="selected === n.id ? 2.5 : 1"
                  @pointerdown.stop="onNodeDown(n, $event)" style="cursor:pointer" />
          <text v-if="nodeR(n) >= 9 || selected === n.id" :x="pos[n.id].x" :y="pos[n.id].y + nodeR(n) + 11"
                text-anchor="middle" fill="#cdd7ec" font-size="10">{{ shortLabel(n) }}</text>
        </g>
      </svg>
      <transition name="fade">
        <div class="node-detail" v-if="detail" @pointerdown.stop>
          <div class="nd-head">
            <span class="dot" :style="{ background: detail.color }"></span>
            <b>{{ detail.id }}</b>
            <span class="nd-tag">{{ typeName(detail.type) }}</span>
            <button class="nd-close" @click="selected = null">×</button>
          </div>
          <div class="nd-body" v-if="detail.type === 'theme'">
            <div class="nd-line"><span class="muted">判决</span><span :class="verdictClass(detail.verdict)">{{ detail.verdict }}</span></div>
            <p class="nd-desc">{{ themeSummary(detail.id) }}</p>
          </div>
          <div class="nd-body" v-else-if="detail.type === 'round'">
            <div class="nd-line"><span class="muted">判决</span><span :class="verdictClass(detail.verdict)">{{ detail.verdict }}</span></div>
            <div class="nd-line"><span class="muted">标题</span>{{ roundTitle(detail.id) }}</div>
            <div class="nd-line"><span class="muted">靶宣称</span>{{ roundTarget(detail.id) }}</div>
            <p class="nd-desc">{{ roundConclusion(detail.id) }}</p>
            <div class="nd-links" v-if="roundExtras(detail.id)">
              <span class="chip" v-for="x in roundExtras(detail.id)" :key="x">{{ x }}</span>
            </div>
          </div>
          <div class="nd-body" v-else-if="detail.type === 'blacklist'">
            <p class="nd-desc"><b>对象：</b>{{ blItem(detail.id) }}</p>
            <p class="nd-desc"><b>理由：</b>{{ blReason(detail.id) }}</p>
            <div class="nd-line"><span class="muted">来源</span>{{ blSource(detail.id) }}</div>
          </div>
          <div class="nd-body" v-else-if="detail.type === 'core'">
            <div class="nd-line"><span class="muted">状态</span><span :class="detail.verdict === 'OK' ? 'tag-ok' : 'tag-boundary'">{{ detail.verdict === 'OK' ? '保留(正确核)' : '降级' }}</span></div>
            <p class="nd-desc">{{ coreDesc(detail.id) }}</p>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { useOpenuft } from '@/composables/useOpenuft.js'

const { graph, themes, roundsAll } = useOpenuft()

const W = 920, H = 560
const stage = ref(null)
const pos = reactive({})
const vel = reactive({})
const selected = ref(null)
const detail = computed(() => {
  if (!selected.value) return null
  const n = graph.value.nodes.find(x => x.id === selected.value)
  return n || null
})

const typeFilters = [
  { key: 'theme', label: '主题', color: 'var(--theme-force)' },
  { key: 'round', label: '攻破轮', color: 'var(--fail)' },
  { key: 'core', label: '正确核', color: 'var(--ok)' },
  { key: 'blacklist', label: '黑名单', color: 'var(--fail)' }
]
const activeTypes = reactive(['theme', 'round', 'core', 'blacklist'])
function toggleType(k) {
  const i = activeTypes.indexOf(k)
  if (i >= 0) activeTypes.splice(i, 1)
  else activeTypes.push(k)
}

// 新节点（工作台新增攻破轮）需补位，否则模板访问 pos[newId].x 会抛错
watch(graph, () => initPositions())

const visibleNodes = computed(() => graph.value.nodes.filter(n => activeTypes.includes(n.type) && pos[n.id]))
const visibleEdges = computed(() => {
  const ids = new Set(visibleNodes.value.map(n => n.id))
  return graph.value.edges.filter(e => ids.has(e.source) && ids.has(e.target))
})

function nodeR(n) {
  if (n.type === 'theme') return 15
  if (n.type === 'round') return 7
  if (n.type === 'core') return n.verdict === 'OK' ? 6 : 5
  return 6
}
function shortLabel(n) {
  if (n.type === 'theme') return n.label
  if (n.type === 'core') return n.id + (n.verdict === 'OK' ? '' : '↓')
  return n.id
}

// ---- simulation ----
let raf = null, alpha = 1, dragging = null, dragMoved = false

function initPositions() {
  const ns = graph.value.nodes
  ns.forEach((n, i) => {
    if (pos[n.id]) return
    const ang = (i / ns.length) * Math.PI * 2
    const rad = n.type === 'theme' ? 60 : 220 + (i % 5) * 18
    pos[n.id] = { x: W / 2 + Math.cos(ang) * rad, y: H / 2 + Math.sin(ang) * rad }
    vel[n.id] = { x: 0, y: 0 }
  })
}

function tick() {
  const ns = graph.value.nodes, es = graph.value.edges
  const k = 0.012 // spring
  const rep = 2400 // repulsion
  const center = 0.002
  // reset accel via vel decay
  ns.forEach(n => { vel[n.id].x *= 0.86; vel[n.id].y *= 0.86 })
  // repulsion
  for (let i = 0; i < ns.length; i++) {
    for (let j = i + 1; j < ns.length; j++) {
      const a = pos[ns[i].id], b = pos[ns[j].id]
      let dx = a.x - b.x, dy = a.y - b.y
      let d2 = dx * dx + dy * dy + 0.01
      const f = rep / d2
      const d = Math.sqrt(d2)
      const fx = (dx / d) * f, fy = (dy / d) * f
      vel[ns[i].id].x += fx; vel[ns[i].id].y += fy
      vel[ns[j].id].x -= fx; vel[ns[j].id].y -= fy
    }
  }
  // springs
  es.forEach(e => {
    const a = pos[e.source], b = pos[e.target]
    if (!a || !b) return
    let dx = b.x - a.x, dy = b.y - a.y
    const d = Math.sqrt(dx * dx + dy * dy) + 0.01
    const f = (d - 70) * k
    const fx = (dx / d) * f, fy = (dy / d) * f
    vel[e.source].x += fx; vel[e.source].y += fy
    vel[e.target].x -= fx; vel[e.target].y -= fy
  })
  // centering + integrate
  ns.forEach(n => {
    if (dragging === n.id) return
    vel[n.id].x += (W / 2 - pos[n.id].x) * center
    vel[n.id].y += (H / 2 - pos[n.id].y) * center
    pos[n.id].x += vel[n.id].x * alpha
    pos[n.id].y += vel[n.id].y * alpha
    pos[n.id].x = Math.max(20, Math.min(W - 20, pos[n.id].x))
    pos[n.id].y = Math.max(20, Math.min(H - 20, pos[n.id].y))
  })
  alpha *= 0.992
  if (alpha < 0.02) alpha = 0.02 // keep gently alive for dragging
  raf = requestAnimationFrame(tick)
}

function restart() { alpha = 1; graph.value.nodes.forEach(n => { vel[n.id].x = 0; vel[n.id].y = 0 }) }

function onNodeDown(n, ev) {
  dragging = n.id; dragMoved = false
  selected.value = n.id
  ev.target.setPointerCapture && ev.target.setPointerCapture(ev.pointerId)
}
function onMove(ev) {
  if (!dragging) return
  const rect = stage.value.getBoundingClientRect()
  const x = (ev.clientX - rect.left) * (W / rect.width)
  const y = (ev.clientY - rect.top) * (H / rect.height)
  pos[dragging].x = x; pos[dragging].y = y; vel[dragging].x = 0; vel[dragging].y = 0
  dragMoved = true
}
function onUp() { dragging = null }
function onStageDown() { if (!dragMoved) selected.value = null }

// ---- detail helpers ----
function typeName(t) { return { theme: '主题', round: '攻破轮', core: '正确核', blacklist: '黑名单' }[t] || t }
function verdictClass(v) { return v === 'FAIL' || v === 'BAN' || v === 'DOWN' ? 'tag-fail' : (v === 'PASS' || v === 'OK' ? 'tag-ok' : 'tag-boundary') }
function themeSummary(id) { const t = themes.value.find(x => x.id === id); return t ? t.summary : '' }
function roundTitle(id) { const r = roundsAll.value.find(x => x.id === id); return r ? r.title : '' }
function roundTarget(id) { const r = roundsAll.value.find(x => x.id === id); return r ? r.target : '' }
function roundConclusion(id) { const r = roundsAll.value.find(x => x.id === id); return r ? r.conclusion : '' }
function roundExtras(id) {
  const r = roundsAll.value.find(x => x.id === id)
  if (!r) return []
  const out = []
  ;(r.blacklists || []).forEach(b => out.push('→ 黑名单 ' + b))
  ;(r.downgrades || []).forEach(k => out.push('→ 降级 ' + k))
  return out
}
function blItem(id) { const x = useOpenuft().blacklist.value.find(z => z.id === id); return x ? x.item : '' }
function blReason(id) { const x = useOpenuft().blacklist.value.find(z => z.id === id); return x ? x.reason : '' }
function blSource(id) { const x = useOpenuft().blacklist.value.find(z => z.id === id); return x ? x.source : '' }
function coreDesc(id) { const c = useOpenuft().cores.value.find(z => z.id === id); return c ? c.desc : '' }

function edgeColor(kind) {
  if (kind === 'member') return '#4c8dff'
  if (kind === 'registers') return '#ff5d6c'
  if (kind === 'downgrades') return '#f5b13d'
  return '#3a4a6a'
}

// 必须在 setup 同步初始化：Vue 首次渲染先于 onMounted，
// 若留到 mounted 再建 pos，首帧模板 pos[node].x 会访问 undefined 而抛出。
initPositions()

function onFocusNode(e) { if (e.detail) selected.value = e.detail }
onMounted(() => {
  initPositions()
  raf = requestAnimationFrame(tick)
  window.addEventListener('focus-node', onFocusNode)
})
onBeforeUnmount(() => { if (raf) cancelAnimationFrame(raf); window.removeEventListener('focus-node', onFocusNode) })
</script>

<style scoped>
.graph-wrap { display: flex; flex-direction: column; gap: 12px; }
.graph-toolbar { display: flex; align-items: center; gap: 16px; flex-wrap: wrap; }
.legend { display: flex; gap: 14px; font-size: 11.5px; color: var(--text-dim); }
.lg { display: inline-flex; align-items: center; gap: 5px; }
.graph-stage { position: relative; background: radial-gradient(circle at 50% 40%, #16203a, #0e1320); border: 1px solid var(--line-soft); border-radius: var(--radius); overflow: hidden; }
svg { display: block; width: 100%; height: auto; touch-action: none; }
.node-detail {
  position: absolute; top: 14px; right: 14px; width: 320px; max-height: 90%;
  background: rgba(20,28,46,.96); border: 1px solid var(--line); border-radius: 10px;
  padding: 13px 15px; box-shadow: var(--shadow); backdrop-filter: blur(4px); overflow-y: auto;
}
.nd-head { display: flex; align-items: center; gap: 8px; font-size: 14px; }
.nd-tag { font-size: 10px; padding: 2px 7px; border-radius: 6px; background: var(--panel-2); color: var(--text-dim); }
.nd-close { margin-left: auto; background: none; border: none; color: var(--text-mute); font-size: 18px; cursor: pointer; line-height: 1; }
.nd-body { margin-top: 10px; }
.nd-line { display: flex; gap: 8px; font-size: 12px; margin: 5px 0; align-items: baseline; }
.nd-desc { font-size: 12px; color: var(--text-dim); line-height: 1.6; margin: 8px 0; }
.nd-links { margin-top: 8px; }
.fade-enter-active, .fade-leave-active { transition: opacity .18s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
