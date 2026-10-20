<template>
  <div>
    <div class="page-head">
      <div class="page-title">正确理论体系 · SM+GR —— 整理与攻破</div>
      <div class="page-sub">本视图整理「正确的」理论体系与方程（{{ eqTotal }} 条机读验证），并呈现对它的攻破（{{ totalBoundaries }} 条断裂边界定价 + {{ chainTotal }} 条推导链 0 闭合）。条目全部来自 r127 / r128 / r130 / r131 机审产物，本视图不重判。</div>
    </div>

    <!-- 核心命题 + 关键数字 -->
    <div class="card" style="margin-bottom:16px">
      <div class="card-title">核心命题 <span class="tag tag-theme">THESIS</span></div>
      <p class="thesis">{{ cs.thesis }}</p>
      <div class="kvs" style="margin-top:14px">
        <div v-for="kn in cs.keyNumbers" :key="kn.k" class="kv">
          <div class="k">{{ kn.k }}</div>
          <div class="v" :style="{ color: knColor(kn.v) }">{{ kn.v }}<small> {{ kn.note }}</small></div>
        </div>
      </div>
    </div>

    <!-- 第一章：整理 —— 已验证方程体系 -->
    <div class="card" style="margin-bottom:16px">
      <div class="card-title">
        第一章 · 整理：已验证方程体系
        <div class="seg" style="margin-left:auto">
          <button :class="{active: tier==='equation'}" @click="tier='equation'">方程级 {{ cs.equations.equationTier.length }}</button>
          <button :class="{active: tier==='system'}" @click="tier='system'">体系级 {{ cs.equations.systemTier.length }}</button>
        </div>
      </div>
      <div v-if="tier==='equation'">
        <div v-for="dom in domainsOf(cs.equations.equationTier)" :key="dom" class="dom-group">
          <div class="dom-h"><span class="dot" :style="{ background: domColor(dom) }"></span>{{ dom }}<span class="dim" style="font-weight:400;margin-left:6px">{{ countDom(cs.equations.equationTier, dom) }} 条</span></div>
          <div v-for="e in byDom(cs.equations.equationTier, dom)" :key="e.id" class="eq-row">
            <span class="mono eq-id">{{ e.id }}</span>
            <div class="eq-body">
              <div class="eq-formula">{{ e.eq }}</div>
              <div class="eq-value"><span class="muted">机读 ▸ </span>{{ e.value }}</div>
              <div class="dim eq-note">{{ e.note }}</div>
            </div>
            <span class="tag tag-ok">PASS</span>
          </div>
        </div>
      </div>
      <div v-else>
        <div v-for="e in cs.equations.systemTier" :key="e.id" class="eq-row">
          <span class="mono eq-id">{{ e.id }}</span>
          <div class="eq-body">
            <div class="eq-formula">{{ e.eq }}</div>
            <div class="eq-value"><span class="muted">机读 ▸ </span>{{ e.value }}</div>
            <div class="dim eq-note">{{ e.note }}</div>
          </div>
          <span :class="e.id === 'O5' ? 'tag-info' : 'tag-ok'">{{ e.id === 'O5' ? 'INFO' : 'PASS' }}</span>
        </div>
      </div>
    </div>

    <!-- 第二章：攻破一 —— 断裂边界 -->
    <div class="card" style="margin-bottom:16px">
      <div class="card-title">第二章 · 攻破：断裂边界（定价到 dex） <span class="tag tag-fail">{{ totalBoundaries }} 条</span></div>
      <p class="dim" style="font-size:12px;line-height:1.7;margin:0 0 12px">
        同一套判据压测正确理论自身。两册条目<b>不可相加</b>：重叠项（宇宙学常数 / 等级 / 暗物质 / 强 CP / 中微子 / 引力量子化）是不同截断口径或不同射程，分别登记。
      </p>
      <div class="grid grid-1-1">
        <div v-for="(grp, key) in cs.boundaries" :key="key">
          <div class="blk-h">{{ grp.label }} <span class="dim" style="font-weight:400">{{ grp.note }}</span></div>
          <div v-for="b in grp.items" :key="key + b.id" class="bd-row">
            <div class="bd-head">
              <span class="mono">{{ b.id }}</span>
              <b class="bd-title">{{ b.title }}</b>
              <span :class="verdictClass(b.verdict)" style="margin-left:auto">{{ b.verdict }}</span>
            </div>
            <div class="bd-price mono">{{ b.price }}</div>
            <div class="dim bd-detail">{{ b.detail }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 第三章：攻破二 —— 推导链隐藏前提 -->
    <div class="card" style="margin-bottom:16px">
      <div class="card-title">
        第三章 · 攻破：推导链的隐藏前提 <span class="tag tag-boundary">{{ cs.chains.summary.n_closed }}/{{ cs.chains.summary.n_chains }} 闭合</span>
      </div>
      <p class="dim" style="font-size:12px;line-height:1.7;margin:0 0 6px">{{ cs.chains.note }}</p>
      <div class="kvs" style="margin-bottom:14px">
        <div class="kv"><div class="k">推导链总数</div><div class="v">{{ cs.chains.summary.n_chains }}</div></div>
        <div class="kv"><div class="k">闭合</div><div class="v" style="color:var(--fail)">{{ cs.chains.summary.n_closed }}</div></div>
        <div class="kv"><div class="k">总闭合率</div><div class="v" style="color:var(--boundary)">{{ (cs.chains.summary.closure_all * 100).toFixed(1) }}%</div></div>
        <div class="kv"><div class="k">前提开放 / 域限 / 猜想</div><div class="v" style="font-size:18px">{{ cs.chains.summary.premise_open }} / {{ cs.chains.summary.domain_limited }} / {{ cs.chains.summary.conjectural }}</div></div>
      </div>
      <div v-for="fam in cs.chains.families" :key="fam.id" class="dom-group">
        <div class="dom-h"><span class="dot" :style="{ background: famColor(fam.id) }"></span>{{ fam.name }}</div>
        <div v-for="c in fam.items" :key="c.id" class="ch-row">
          <span class="mono ch-id">{{ c.id }}</span>
          <div class="ch-body">
            <div class="ch-claim">{{ c.claim }}</div>
            <div class="dim ch-note">{{ c.note }}</div>
            <div class="ch-bar"><div class="bar" style="margin-top:6px"><span :style="{ width: (c.closure * 100) + '%', background: chainColor(c.verdict) }"></span></div></div>
          </div>
          <div class="ch-meta">
            <span :class="chainTag(c.verdict)">{{ chainLabel(c.verdict) }}</span>
            <span class="mono dim" style="font-size:11px">闭合 {{ (c.closure * 100).toFixed(0) }}%</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 控制组 -->
    <div class="card">
      <div class="card-title">判据判别力凭证 · 双向控制组 <span class="tag tag-info">CONTROLS</span></div>
      <p class="dim" style="font-size:12px;line-height:1.7;margin:0 0 10px">同一套判据：错误理论必须 FAIL、正确核必须 PASS——否则判据本身不可信（失控退出码 2）。r130 另设反向对照：扰动赋值下反常必须非零。</p>
      <div v-for="c in cs.controls" :key="c.id" class="ctl-row">
        <span class="tag tag-ok">{{ c.result }}</span>
        <b>{{ c.name }}</b>
        <span class="dim ctl-detail">{{ c.detail }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useOpenuft } from '@/composables/useOpenuft.js'
const { correctSystem } = useOpenuft()
const cs = computed(() => correctSystem.value || { equations: { equationTier: [], systemTier: [] }, boundaries: {}, chains: { families: [], summary: {} }, controls: [], keyNumbers: [], thesis: '' })
const totalBoundaries = computed(() => Object.values(cs.value.boundaries || {}).reduce((s, g) => s + (g.items ? g.items.length : 0), 0))
const eqTotal = computed(() => (cs.value.equations?.equationTier?.length || 0) + (cs.value.equations?.systemTier?.length || 0))
const chainTotal = computed(() => cs.value.chains?.summary?.n_chains || 0)

const tier = ref('equation')

function verdictClass(v) { return (v === 'FAIL') ? 'tag-fail' : (v === 'PASS' ? 'tag-ok' : (v === 'BOUNDARY' ? 'tag-boundary' : 'tag-info')) }
function knColor(v) { return v.indexOf('/') >= 0 && v.startsWith('0/') ? 'var(--fail)' : (v.indexOf('11/11') === 0 ? 'var(--ok)' : 'var(--boundary)') }
function domainsOf(list) { const s = new Set(list.map(e => e.domain)); return [...s] }
function byDom(list, dom) { return list.filter(e => e.domain === dom) }
function countDom(list, dom) { return list.filter(e => e.domain === dom).length }
function domColor(dom) {
  return { '电弱统一': 'var(--theme-gravity)', '量子色动力学': 'var(--theme-correct)', '量子电动力学': 'var(--theme-photon)', '引力（GR）': 'var(--theme-force)', '体系层': 'var(--accent-2)', '已验证域登记': 'var(--text-mute)' }[dom] || 'var(--text-mute)'
}
function famColor(f) { return { GR: 'var(--theme-force)', SM: 'var(--theme-correct)', X: 'var(--theme-photon)' }[f] || 'var(--text-mute)' }
function chainColor(v) { return v === 'PREMISE-OPEN' ? 'var(--fail)' : (v === 'DOMAIN-LIMITED' ? 'var(--boundary)' : 'var(--accent-2)') }
function chainTag(v) { return v === 'PREMISE-OPEN' ? 'tag-fail' : (v === 'DOMAIN-LIMITED' ? 'tag-boundary' : 'tag-info') }
function chainLabel(v) { return { 'PREMISE-OPEN': '前提开放', 'DOMAIN-LIMITED': '域限', 'CONJECTURAL': '猜想' }[v] || v }
</script>

<style scoped>
.thesis { font-size: 14px; color: var(--text); line-height: 1.8; margin: 0; }
.dom-group { margin-bottom: 14px; }
.dom-h { font-size: 12px; font-weight: 700; color: var(--text-dim); margin: 10px 0 6px; display: flex; align-items: center; gap: 7px; }
.eq-row, .ch-row, .bd-row, .ctl-row { display: flex; gap: 12px; padding: 10px 4px; border-bottom: 1px solid var(--line-soft); align-items: flex-start; }
.eq-row:last-child, .ch-row:last-child, .bd-row:last-child, .ctl-row:last-child { border-bottom: none; }
.eq-id { flex: 0 0 44px; font-weight: 700; color: var(--accent); padding-top: 2px; }
.eq-body, .ch-body { flex: 1; min-width: 0; }
.eq-formula { font-size: 13.5px; color: var(--text); font-weight: 600; }
.eq-value { font-size: 12px; color: var(--text-dim); margin-top: 3px; }
.eq-note { font-size: 11.5px; margin-top: 3px; line-height: 1.55; }
.blk-h { font-size: 13px; font-weight: 700; margin: 4px 0 8px; color: var(--text); }
.bd-head { display: flex; align-items: center; gap: 8px; font-size: 12.5px; }
.bd-title { font-size: 13px; }
.bd-price { font-size: 12px; color: var(--boundary); margin: 4px 0 2px; }
.bd-detail { font-size: 11.5px; line-height: 1.55; }
.ch-id { flex: 0 0 52px; font-weight: 700; color: var(--accent); padding-top: 2px; }
.ch-claim { font-size: 13px; color: var(--text); }
.ch-note { font-size: 11.5px; margin-top: 3px; line-height: 1.55; }
.ch-meta { flex: 0 0 92px; display: flex; flex-direction: column; align-items: flex-end; gap: 5px; }
.ctl-row { align-items: baseline; font-size: 12.5px; }
.ctl-detail { font-size: 12px; line-height: 1.6; }
@media (max-width: 860px) {
  .ch-meta { flex-basis: 72px; }
  .eq-id, .ch-id { flex-basis: 40px; }
}
</style>
