<template>
  <div>
    <div class="page-head">
      <div class="page-title">正确核与账本 · {{ cores.length }} → {{ coresSurvive }}</div>
      <div class="page-sub">保留清单 = 教科书物理在另一套记号下的改写、代数恒等或已证几何定理；降级 {{ coresDown }} 条因定义欠定或单位约定被移出正确核。</div>
    </div>

    <div class="kvs" style="margin-bottom:16px">
      <div class="kv"><div class="k">正确核（保留）</div><div class="v" style="color:var(--ok)">{{ coresSurvive }}</div></div>
      <div class="kv"><div class="k">降级</div><div class="v" style="color:var(--boundary)">{{ coresDown }}</div></div>
      <div class="kv"><div class="k">螺旋几何化卷</div><div class="v">{{ spiral.length }}</div></div>
      <div class="kv"><div class="k">全物理域槽位</div><div class="v">{{ domains.length }}</div></div>
    </div>

    <div class="card" style="margin-bottom:16px">
      <div class="card-title">
        正确核清单（机读分区）
        <div class="seg" style="margin-left:auto">
          <button :class="{active: statusFilter==='all'}" @click="statusFilter='all'">全部 {{ cores.length }}</button>
          <button :class="{active: statusFilter==='correct'}" @click="statusFilter='correct'">保留 {{ coresSurvive }}</button>
          <button :class="{active: statusFilter==='downgraded'}" @click="statusFilter='downgraded'">降级 {{ coresDown }}</button>
        </div>
      </div>
      <div class="table-scroll">
        <table>
          <thead><tr><th>ID</th><th>状态</th><th>性质</th><th>说明</th><th>降级来源</th></tr></thead>
          <tbody>
            <tr v-for="c in shownCores" :key="c.id">
              <td class="mono">{{ c.id }}</td>
              <td><span :class="c.status==='correct'?'tag-ok':'tag-boundary'">{{ c.status==='correct'?'保留':'降级' }}</span></td>
              <td class="dim">{{ c.kind }}</td>
              <td class="dim" style="font-size:11.5px;line-height:1.55">{{ c.desc }}</td>
              <td class="mono">{{ c.downgradedBy || '—' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="!shownCores.length" class="empty-state">该状态下无条目。</div>
    </div>

    <div class="grid grid-1-1">
      <div class="card">
        <div class="card-title">螺旋几何化子卷（62–65） <span class="tag tag-fail">全 FAIL</span></div>
        <div v-for="s in spiral" :key="s.id" class="spiral-row">
          <b>{{ s.id }} 号</b><span :class="verdictClass(s.verdict)" style="margin-left:8px">{{ s.verdict }}</span>
          <p class="dim" style="font-size:11.5px;margin:4px 0 10px">{{ s.note }}</p>
        </div>
      </div>
      <div class="card">
        <div class="card-title">全物理覆盖矩阵 · {{ domains.length }} 域</div>
        <div class="table-scroll">
          <div v-for="d in domains" :key="d.vol" class="domain-row">
            <span class="mono dim">{{ d.vol }}</span>
            <span style="margin-left:8px">{{ d.name }}</span>
            <span class="dim" style="margin-left:auto;font-size:11px">{{ d.status }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useOpenuft } from '@/composables/useOpenuft.js'
const { cores, spiral, domains } = useOpenuft()
const statusFilter = ref('all')
const coresSurvive = computed(() => cores.value.filter(c => c.status === 'correct').length)
const coresDown = computed(() => cores.value.filter(c => c.status === 'downgraded').length)
const shownCores = computed(() => statusFilter.value === 'all' ? cores.value : cores.value.filter(c => c.status === statusFilter.value))
function verdictClass(v) { return v === 'FAIL' ? 'tag-fail' : (v === 'PASS' ? 'tag-ok' : 'tag-boundary') }
</script>

<style scoped>
.spiral-row { padding: 8px 0; border-bottom: 1px solid var(--line-soft); font-size: 13px; }
.spiral-row:last-child { border-bottom: none; }
.domain-row { display: flex; align-items: center; padding: 4px 0; font-size: 12px; border-bottom: 1px solid var(--line-soft); }
.domain-row:last-child { border-bottom: none; }
</style>
