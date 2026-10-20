<template>
  <div class="nf">
    <div class="nf-code">404</div>
    <div class="nf-title">视图不存在</div>
    <p class="dim nf-sub">路径 <span class="mono">{{ route.fullPath }}</span> 未登记。审计图谱的入口在左侧导航。</p>
    <RouterLink class="btn btn-primary" to="/">返回总览</RouterLink>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
const route = useRoute()
</script>

<style scoped>
.nf { text-align: center; padding: 80px 20px; }
.nf-code { font-size: 64px; font-weight: 800; color: var(--line); letter-spacing: 4px; }
.nf-title { font-size: 18px; font-weight: 700; margin-top: 8px; }
.nf-sub { font-size: 13px; margin: 10px 0 22px; }
</style>
