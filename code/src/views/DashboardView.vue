<template>
  <div>
    <div class="page-head">
      <div class="page-title">总览 · 全域物理审计图谱</div>
      <div class="page-sub">{{ meta.source }} —— 本系统只整理与可视化已机读审计的结论，不重判、不发明新物理。</div>
    </div>

    <div class="kvs">
      <div class="kv"><div class="k">攻破轮次</div><div class="v">{{ roundsAll.length }}<small> 轮（全 FAIL 主导）</small></div></div>
      <div class="kv"><div class="k">主题射程</div><div class="v">{{ themes.length }}<small> 个</small></div></div>
      <div class="kv"><div class="k">正确核保留</div><div class="v" style="color:var(--ok)">{{ cores.filter(c=>c.status==='correct').length }}<small> / {{ cores.length }}</small></div></div>
      <div class="kv"><div class="k">黑名单</div><div class="v" style="color:var(--fail)">{{ blacklist.length }}<small> 条不可引用</small></div></div>
      <div class="kv"><div class="k">全物理域</div><div class="v">{{ domains.length }}<small> 个覆盖槽位</small></div></div>
      <div class="kv"><div class="k">机读守卫</div><div class="v" style="color:var(--accent)">21/21<small> 退出码 0</small></div></div>
    </div>

    <div class="grid" style="grid-template-columns: 1.4fr 1fr; margin-top:18px">
      <div class="card">
        <div class="card-title">四主题攻破射程 <span class="tag tag-theme">核心</span></div>
        <div v-for="t in themes" :key="t.id" class="theme-row">
          <span class="dot" :style="{ background: t.color }"></span>
          <b style="min-width:92px;display:inline-block">{{ t.name }}</b>
          <span :class="verdictClass(t.verdict)">{{ t.verdict }}</span>
          <span class="dim" style="margin-left:auto;font-size:11px">{{ t.rounds.length }} 轮</span>
        </div>
        <p class="dim" style="font-size:12px;line-height:1.7;margin-top:12px">{{ cosmic.thesis }}</p>
      </div>

      <div class="card">
        <div class="card-title">宇宙运动的本质 · 四条承重结论</div>
        <div v-for="p in cosmic.pillars" :key="p.title" class="pillar">
          <div class="pillar-h"><b>{{ p.title }}</b><span :class="verdictClass(p.verdict)">{{ p.verdict }}</span></div>
          <p class="dim" style="font-size:11.5px;line-height:1.6;margin:4px 0 0">{{ p.detail }}</p>
        </div>
      </div>
    </div>

    <div class="card" style="margin-top:16px">
      <div class="card-title">最新攻破轮次 <span class="tag">r116 – r121</span></div>
      <table>
        <thead><tr><th>轮</th><th>标题</th><th>主题</th><th>判决</th><th>靶宣称</th></tr></thead>
        <tbody>
          <tr v-for="r in recentRounds" :key="r.id">
            <td class="mono">{{ r.id }}</td>
            <td>{{ r.title }}</td>
            <td><span class="chip">{{ themeName(r.theme) }}</span></td>
            <td><span :class="verdictClass(r.verdict)">{{ r.verdict }}</span></td>
            <td class="dim" style="font-size:11.5px">{{ r.target }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="card" style="margin-top:16px">
      <div class="card-title">诚实边界 · 本库未解决项 <span class="tag tag-boundary">OPEN</span></div>
      <div>
        <span class="chip" v-for="b in cosmic.honestBoundary" :key="b">{{ b }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useOpenuft } from '@/composables/useOpenuft.js'
const { meta, themes, cores, blacklist, domains, roundsAll, cosmic } = useOpenuft()
const recentRounds = computed(() => roundsAll.value.filter(r => /^r11[6-9]|^r12[01]$/.test(r.id)))
function verdictClass(v) { return (v === 'FAIL' || v === 'BAN' || v === 'DOWN') ? 'tag-fail' : (v === 'PASS' || v === 'OK' ? 'tag-ok' : 'tag-boundary') }
function themeName(id) { const t = themes.value.find(x => x.id === id); return t ? t.name : id }
</script>

<style scoped>
.theme-row { display: flex; align-items: center; gap: 9px; padding: 7px 0; border-bottom: 1px solid var(--line-soft); font-size: 13px; }
.theme-row:last-of-type { border-bottom: none; }
.pillar { padding: 9px 0; border-bottom: 1px solid var(--line-soft); }
.pillar:last-child { border-bottom: none; }
.pillar-h { display: flex; align-items: center; gap: 8px; font-size: 13px; }
.pillar-h span { margin-left: auto; }
</style>
