<template>
  <div>
    <div class="page-head">
      <div class="page-title">关联图谱 · 主题 — 攻破轮 — 正确核/黑名单</div>
      <div class="page-sub">点击节点查看判决详情，拖拽可固定位置；边色：蓝=隶属主题，红=登记黑名单，橙=降级正确核。</div>
    </div>
    <div class="grid" style="grid-template-columns: 1fr 280px;">
      <AssocGraph />
      <div class="card">
        <div class="card-title">节点清单 <span class="tag">{{ graph.nodes.length }}</span></div>
        <div class="node-list">
          <div v-for="t in themes" :key="t.id" class="nl-group">
            <div class="nl-h"><span class="dot" :style="{background:t.color}"></span>主题</div>
            <div v-for="r in roundsByTheme(t.id)" :key="r.id" class="nl-item" @click="focus(r.id)">
              <span class="dot dot-fail"></span>{{ r.id }} · {{ t.name }}
            </div>
          </div>
        </div>
        <div class="nl-h" style="margin-top:10px"><span class="dot" style="background:var(--ok)"></span>正确核（{{ cores.filter(c=>c.status==='correct').length }} 保留）</div>
        <div class="nl-item" v-for="c in cores.filter(c=>c.status==='correct')" :key="c.id" @click="focus(c.id)"><span class="dot dot-ok"></span>{{ c.id }} · {{ c.kind }}</div>
        <div class="nl-h" style="margin-top:10px"><span class="dot" style="background:var(--fail)"></span>黑名单（{{ blacklist.length }}）</div>
        <div class="nl-item" v-for="b in blacklist" :key="b.id" @click="focus(b.id)"><span class="dot dot-fail"></span>{{ b.id }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import AssocGraph from '@/components/AssocGraph.vue'
import { useOpenuft } from '@/composables/useOpenuft.js'
const { graph, themes, cores, blacklist, roundsAll } = useOpenuft()
function roundsByTheme(tid) { return roundsAll.value.filter(r => r.theme === tid) }
function focus(id) { window.dispatchEvent(new CustomEvent('focus-node', { detail: id })) }
</script>

<style scoped>
.node-list { max-height: 520px; overflow-y: auto; font-size: 12px; }
.nl-group { margin-bottom: 8px; }
.nl-h { font-size: 11px; color: var(--text-mute); margin: 6px 0 3px; display: flex; align-items: center; gap: 6px; }
.nl-item { padding: 4px 6px; border-radius: 6px; cursor: pointer; color: var(--text-dim); display: flex; align-items: center; gap: 6px; }
.nl-item:hover { background: var(--panel-2); color: #fff; }
</style>
