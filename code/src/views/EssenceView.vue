<template>
  <div>
    <div class="page-head">
      <div class="page-title">宇宙运动的本质 · 审计给出的结论</div>
      <div class="page-sub">本视图不分析理论的本质本源，而是把已有审计结论综合成关于「宇宙如何运动」的可视化判读。</div>
    </div>

    <div class="card" style="margin-bottom:16px">
      <div class="card-title">核心命题 <span class="tag tag-theme">THESIS</span></div>
      <p class="thesis">{{ cosmic.thesis }}</p>
    </div>

    <div class="grid" style="grid-template-columns: 1fr 1fr; margin-bottom:16px">
      <div v-for="p in cosmic.pillars" :key="p.title" class="card pillar-card">
        <div class="pillar-h"><b>{{ p.title }}</b><span :class="verdictClass(p.verdict)" style="margin-left:auto">{{ p.verdict }}</span></div>
        <p class="dim" style="font-size:12.5px;line-height:1.7;margin:8px 0 0">{{ p.detail }}</p>
        <div class="chip" :style="{ background: themeColor(p.theme)+'22', color: themeColor(p.theme) }">{{ themeName(p.theme) }}</div>
      </div>
    </div>

    <div class="grid" style="grid-template-columns: 1fr 1fr">
      <div class="card">
        <div class="card-title">诚实边界 · 未解决项 <span class="tag tag-boundary">OPEN</span></div>
        <div v-for="b in cosmic.honestBoundary" :key="b" class="bound-row"><span class="dot dot-boundary"></span>{{ b }}</div>
      </div>
      <div class="card">
        <div class="card-title">对「宇宙运行秘密」的判读 <span class="tag tag-info">VERDICT</span></div>
        <p class="dim" style="font-size:12.5px;line-height:1.75">{{ cosmic.verdictOnCosmicSecret }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useOpenuft } from '@/composables/useOpenuft.js'
const { cosmic, themes } = useOpenuft()
function verdictClass(v) { return (v==='FAIL'||v==='BAN'||v==='DOWN') ? 'tag-fail' : (v==='PASS'||v==='OK' ? 'tag-ok' : 'tag-boundary') }
function themeName(id) { const t = themes.value.find(x => x.id === id); return t ? t.name : id }
function themeColor(id) { const t = themes.value.find(x => x.id === id); return t ? t.color : 'var(--boundary)' }
</script>

<style scoped>
.thesis { font-size: 14px; color: var(--text); line-height: 1.8; margin: 0; }
.pillar-card { border-top: 3px solid var(--accent-2); }
.pillar-h { display: flex; align-items: center; gap: 8px; font-size: 14px; }
.bound-row { display: flex; align-items: center; gap: 8px; padding: 6px 0; font-size: 12.5px; color: var(--text-dim); border-bottom: 1px solid var(--line-soft); }
.bound-row:last-child { border-bottom: none; }
</style>
