<template>
  <div>
    <div class="page-head">
      <div class="page-title">攻破链时间线 · {{ chainRange }}</div>
      <div class="page-sub">从边界裁定到命题穷举到退守封口到语料审计的完整攻击序列；每一环都是对「统一场论/光子内部运行」宣称的可机读判决。</div>
    </div>
    <div class="toolbar">
      <div class="seg">
        <button :class="{active: filter==='all'}" @click="filter='all'">全部 {{ roundsAll.length }}</button>
        <button :class="{active: filter==='T-photon'}" @click="filter='T-photon'">光子 {{ byTheme('T-photon').length }}</button>
        <button :class="{active: filter==='T-force'}" @click="filter='T-force'">力的统一 {{ byTheme('T-force').length }}</button>
        <button :class="{active: filter==='T-gravity'}" @click="filter='T-gravity'">引力 {{ byTheme('T-gravity').length }}</button>
        <button :class="{active: filter==='T-spiral'}" @click="filter='T-spiral'">螺旋 {{ byTheme('T-spiral').length }}</button>
      </div>
    </div>
    <div class="timeline">
      <div v-for="r in shown" :key="r.id" class="tl-item">
        <div class="tl-dot" :style="{ background: themeColor(r.theme) }"></div>
        <div class="tl-card">
          <div class="tl-head">
            <span class="mono tl-id">{{ r.id }}</span>
            <span class="chip" :style="{ background: themeColor(r.theme)+'22', color: themeColor(r.theme) }">{{ themeName(r.theme) }}</span>
            <span :class="verdictClass(r.verdict)" style="margin-left:auto">{{ r.verdict }}</span>
            <span class="dim mono" style="font-size:11px">{{ r.date }}</span>
          </div>
          <div class="tl-title">{{ r.title }}</div>
          <div class="tl-target"><span class="muted">靶宣称 ▸ </span>{{ r.target }}</div>
          <p class="tl-concl">{{ r.conclusion }}</p>
          <div class="tl-links" v-if="extras(r).length">
            <span class="chip" v-for="x in extras(r)" :key="x">{{ x }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useOpenuft } from '@/composables/useOpenuft.js'
const { roundsAll, themes } = useOpenuft()
const filter = ref('all')
const shown = computed(() => filter.value === 'all' ? roundsAll.value : roundsAll.value.filter(r => r.theme === filter.value))
function byTheme(t) { return roundsAll.value.filter(r => r.theme === t) }
function themeName(id) { const t = themes.value.find(x => x.id === id); return t ? t.name : id }
function themeColor(id) { const t = themes.value.find(x => x.id === id); return t ? t.hex : '#f5b13d' }
function verdictClass(v) { return (v === 'FAIL') ? 'tag-fail' : (v === 'PASS' ? 'tag-ok' : 'tag-boundary') }
function extras(r) { const o = []; (r.blacklists||[]).forEach(b=>o.push('→ B '+b)); (r.downgrades||[]).forEach(k=>o.push('→ ↓'+k)); if (r.user) o.push('★ 本地攻破轮'); return o }
// 链射程由数据驱动（底座首轮 → 末轮；本地轮单列不计入区间）
const chainRange = computed(() => {
  const base = roundsAll.value.filter(r => !r.user)
  return base.length ? `${base[0].id} → ${base[base.length - 1].id}` : '—'
})
</script>

<style scoped>
.timeline { position: relative; padding-left: 26px; }
.timeline::before { content: ''; position: absolute; left: 9px; top: 4px; bottom: 4px; width: 2px; background: var(--line); }
.tl-item { position: relative; margin-bottom: 16px; }
.tl-dot { position: absolute; left: -22px; top: 16px; width: 13px; height: 13px; border-radius: 50%; box-shadow: 0 0 0 3px var(--bg); }
.tl-card { background: var(--panel); border: 1px solid var(--line-soft); border-radius: 10px; padding: 12px 15px; }
.tl-head { display: flex; align-items: center; gap: 9px; }
.tl-id { font-size: 13px; font-weight: 700; }
.tl-title { font-size: 13.5px; margin: 8px 0 4px; color: var(--text); }
.tl-target { font-size: 12px; color: var(--text-dim); }
.tl-concl { font-size: 12px; color: var(--text-dim); line-height: 1.65; margin: 8px 0 0; }
.tl-links { margin-top: 8px; }
</style>
