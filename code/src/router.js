import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'dashboard', component: () => import('./views/DashboardView.vue'), meta: { title: '总览' } },
  { path: '/graph', name: 'graph', component: () => import('./views/GraphView.vue'), meta: { title: '关联图谱' } },
  { path: '/timeline', name: 'timeline', component: () => import('./views/TimelineView.vue'), meta: { title: '攻破链时间线' } },
  { path: '/ledger', name: 'ledger', component: () => import('./views/LedgerView.vue'), meta: { title: '正确核与账本' } },
  { path: '/blacklist', name: 'blacklist', component: () => import('./views/BlacklistView.vue'), meta: { title: '不可引用黑名单' } },
  { path: '/essence', name: 'essence', component: () => import('./views/EssenceView.vue'), meta: { title: '宇宙运动的本质' } },
  { path: '/workbench', name: 'workbench', component: () => import('./views/WorkbenchView.vue'), meta: { title: '攻破工作台' } },
  { path: '/glossary', name: 'glossary', component: () => import('./views/GlossaryView.vue'), meta: { title: '术语表' } }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
