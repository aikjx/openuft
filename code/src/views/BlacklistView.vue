<template>
  <div>
    <div class="page-head">
      <div class="page-title">不可引用黑名单 · {{ blacklist.length }} 条</div>
      <div class="page-sub">黑名单对象不得作为任何推导的前提；若需讨论，只能以「已被 X 号卷判否」的形式出现。</div>
    </div>
    <div class="grid" style="grid-template-columns: repeat(auto-fill, minmax(380px,1fr))">
      <div v-for="b in blacklist" :key="b.id" class="bl-card">
        <div class="bl-head"><span class="mono bl-id">{{ b.id }}</span><span class="tag tag-fail">BAN</span></div>
        <div class="bl-item">{{ b.item }}</div>
        <div class="bl-reason"><span class="muted">理由 ▸ </span>{{ b.reason }}</div>
        <div class="bl-src"><span class="muted">来源 ▸ </span>{{ b.source }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useOpenuft } from '@/composables/useOpenuft.js'
const { blacklist } = useOpenuft()
</script>

<style scoped>
.bl-card { background: var(--panel); border: 1px solid var(--line-soft); border-left: 3px solid var(--fail); border-radius: 10px; padding: 13px 15px; }
.bl-head { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.bl-id { font-size: 13px; font-weight: 700; }
.bl-item { font-size: 13px; color: var(--text); line-height: 1.5; margin-bottom: 8px; }
.bl-reason { font-size: 12px; color: var(--text-dim); line-height: 1.6; }
.bl-src { font-size: 11px; color: var(--text-mute); margin-top: 6px; }
</style>
