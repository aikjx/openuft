<template>
  <div class="app-shell" :class="{ 'nav-open': navOpen }">
    <div class="nav-mask" v-if="navOpen" @click="navOpen = false"></div>
    <aside class="sidebar">
      <div class="brand">
        <div class="brand-mark">⊕</div>
        <div class="brand-text">
          <div class="brand-title">openuft</div>
          <div class="brand-sub">全域物理审计图谱</div>
        </div>
      </div>
      <nav class="nav">
        <RouterLink v-for="item in navItems" :key="item.to" :to="item.to" class="nav-item" @click="navOpen = false">
          <span class="nav-icon">{{ item.icon }}</span>
          <span class="nav-label">{{ item.label }}</span>
        </RouterLink>
      </nav>
      <div class="sidebar-foot">
        <div class="foot-line">机读合账 · 53 卷</div>
        <div class="foot-line dim">{{ meta.engine }}</div>
        <div class="foot-line dim">图谱数据 {{ meta.generated }}</div>
      </div>
    </aside>
    <main class="main">
      <header class="topbar">
        <button class="nav-toggle" @click="navOpen = !navOpen" aria-label="切换导航">☰</button>
        <div class="crumbs">
          <span class="crumb-root">openuft / 07_统一场方程</span>
          <span class="crumb-sep">·</span>
          <span class="crumb-cur">{{ currentTitle }}</span>
        </div>
        <div class="topbar-right">
          <span class="pill pill-fail">攻破链 FAIL 主导</span>
          <span class="pill pill-ok">正确核 {{ counts.coresSurvive }} 保留</span>
          <span class="pill pill-warn">黑名单 {{ counts.blacklist }}</span>
        </div>
      </header>
      <section class="content" ref="contentEl">
        <RouterView v-slot="{ Component }">
          <transition name="page" mode="out-in">
            <component :is="Component" />
          </transition>
        </RouterView>
        <footer class="red-line">
          <b>红线</b> · {{ meta.redLine }}
        </footer>
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed, ref, watch, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { useOpenuft } from '@/composables/useOpenuft.js'

const navItems = [
  { to: '/', icon: '▤', label: '总览' },
  { to: '/graph', icon: '◉', label: '关联图谱' },
  { to: '/timeline', icon: '⏣', label: '攻破链时间线' },
  { to: '/ledger', icon: '▦', label: '正确核与账本' },
  { to: '/blacklist', icon: '⊘', label: '黑名单' },
  { to: '/essence', icon: '✦', label: '宇宙运动的本质' },
  { to: '/correct', icon: '✔', label: '正确理论体系' },
  { to: '/conclusion', icon: '◎', label: '最终结论' },
  { to: '/workbench', icon: '⚒', label: '攻破工作台' },
  { to: '/glossary', icon: 'ⓘ', label: '术语表' }
]

const { meta } = useOpenuft()
const counts = computed(() => meta.value.counts)
const route = useRoute()
const currentTitle = computed(() => route.meta.title || '总览')

// 窄屏导航抽屉
const navOpen = ref(false)
watch(() => route.fullPath, () => { navOpen.value = false })

// 路由切换后重置内容区滚动位置（.content 位于 RouterView 外层，默认会保留上一页滚动点）
const contentEl = ref(null)
watch(() => route.fullPath, async () => {
  await nextTick()
  if (contentEl.value) contentEl.value.scrollTop = 0
})
</script>

<style scoped>
.nav-toggle {
  display: none; background: none; border: 1px solid var(--line); color: var(--text-dim);
  border-radius: 8px; font-size: 15px; padding: 4px 9px; cursor: pointer; margin-right: 10px;
}
.nav-mask { display: none; }
.red-line {
  margin-top: 28px; padding: 12px 16px; border-top: 1px dashed var(--line);
  font-size: 11.5px; color: var(--text-mute); line-height: 1.7;
}
.red-line b { color: var(--boundary); }

/* 页面切换过渡 */
.page-enter-active, .page-leave-active { transition: opacity .16s ease, transform .16s ease; }
.page-enter-from { opacity: 0; transform: translateY(6px); }
.page-leave-to { opacity: 0; transform: translateY(-4px); }

/* ---------- 响应式：中屏折叠为图标栏，窄屏抽屉 ---------- */
@media (max-width: 1100px) {
  .sidebar { width: 58px; flex-basis: 58px; padding: 18px 8px; align-items: center; }
  .brand-text, .nav-label, .sidebar-foot { display: none; }
  .nav-item { justify-content: center; padding: 11px 0; }
  .nav-icon { font-size: 16px; }
}
@media (max-width: 860px) {
  .nav-toggle { display: inline-block; }
  .sidebar {
    position: fixed; z-index: 40; left: 0; top: 0; bottom: 0;
    width: 232px; flex-basis: 232px; transform: translateX(-100%);
    transition: transform .22s ease; padding: 18px 14px; align-items: stretch;
    background: linear-gradient(180deg, #121a2c, #0f1626);
  }
  .nav-open .sidebar { transform: translateX(0); }
  .nav-open .brand-text, .nav-open .nav-label, .nav-open .sidebar-foot { display: block; }
  .nav-open .nav-item { justify-content: flex-start; padding: 10px 12px; }
  .nav-mask {
    display: block; position: fixed; inset: 0; z-index: 30;
    background: rgba(6,10,18,.55); backdrop-filter: blur(2px);
  }
  .topbar-right .pill-warn { display: none; }
}
@media (max-width: 620px) {
  .topbar { padding: 0 14px; }
  .content { padding: 16px 14px 48px; }
  .topbar-right .pill-ok { display: none; }
  .crumb-root { display: none; }
  .crumb-sep { display: none; }
}
</style>
