<template>
  <div class="app-shell">
    <aside class="sidebar">
      <div class="brand">
        <div class="brand-mark">⊕</div>
        <div class="brand-text">
          <div class="brand-title">openuft</div>
          <div class="brand-sub">全域物理审计图谱</div>
        </div>
      </div>
      <nav class="nav">
        <RouterLink v-for="item in navItems" :key="item.to" :to="item.to" class="nav-item">
          <span class="nav-icon">{{ item.icon }}</span>
          <span class="nav-label">{{ item.label }}</span>
        </RouterLink>
      </nav>
      <div class="sidebar-foot">
        <div class="foot-line">机读合账 · 53 卷</div>
        <div class="foot-line dim">守卫 21/21 · 退出码 0</div>
      </div>
    </aside>
    <main class="main">
      <header class="topbar">
        <div class="crumbs">
          <span class="crumb-root">openuft / 07_统一场方程</span>
          <span class="crumb-sep">·</span>
          <span class="crumb-cur">{{ currentTitle }}</span>
        </div>
        <div class="topbar-right">
          <span class="pill pill-fail">攻破链 FAIL 主导</span>
          <span class="pill pill-ok">正确核 16 保留</span>
        </div>
      </header>
      <section class="content">
        <RouterView />
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const navItems = [
  { to: '/', icon: '▤', label: '总览' },
  { to: '/graph', icon: '◉', label: '关联图谱' },
  { to: '/timeline', icon: '⏣', label: '攻破链时间线' },
  { to: '/ledger', icon: '▦', label: '正确核与账本' },
  { to: '/blacklist', icon: '⊘', label: '黑名单' },
  { to: '/essence', icon: '✦', label: '宇宙运动的本质' },
  { to: '/workbench', icon: '⚒', label: '攻破工作台' },
  { to: '/glossary', icon: 'ⓘ', label: '术语表' }
]

const route = useRoute()
const currentTitle = computed(() => route.meta.title || '总览')
</script>
