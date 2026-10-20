<template>
  <div>
    <div class="page-head">
      <div class="page-title">术语表 · Glossary</div>
      <div class="page-sub">本系统使用的核心术语与判据口径，便于跨视图引用与长期维护。</div>
    </div>
    <div class="toolbar">
      <input v-model="q" class="gl-search" placeholder="检索术语或释义…" />
      <span class="dim" style="font-size:12px">{{ filtered.length }} / {{ glossary.length }} 条</span>
    </div>
    <div class="grid grid-2col">
      <div v-for="g in filtered" :key="g.term" class="card">
        <div class="card-title">{{ g.term }} <span class="tag">{{ g.tag }}</span></div>
        <p class="dim" style="font-size:12.5px;line-height:1.7;margin:0">{{ g.def }}</p>
      </div>
    </div>
    <div v-if="!filtered.length" class="empty-state">无匹配术语。</div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useOpenuft } from '@/composables/useOpenuft.js'
const { cores, blacklist, correctSystem } = useOpenuft()
const boundaryTotal = computed(() => Object.values(correctSystem.value?.boundaries || {}).reduce((s, g) => s + (g.items ? g.items.length : 0), 0))

const glossary = ref([
  { term: '正确核', tag: '账本', def: `53 卷保留清单共 ${cores.value.length} 条，其中 ${cores.value.filter(c=>c.status==='correct').length} 条保留：教科书物理在另一套记号下的改写、代数恒等或已证几何定理，全部非本库新增；另 ${cores.value.filter(c=>c.status==='downgraded').length} 条因定义欠定或单位约定降级。` },
  { term: '黑名单', tag: '账本', def: `${blacklist.value.length} 条不可引用登记：被 r 系列判否的对象（循环恒等、欠定定义、伪精度、原理性 no-go、低能标 GUT 等），不得作为推导前提。` },
  { term: '攻破轮 (rNNN)', tag: '审计', def: '对某一宣称的可机读判决单元；每轮含靶宣称、审计条目、verdict（PASS/FAIL/BOUNDARY/INFO）与守卫，产物为 json + 判定册 md + 报告三件套。' },
  { term: '主题射程', tag: '聚合', def: '五主题（力的统一 / 引力的本源 / 光子的本质 / 螺旋几何化 / 正确理论体系）把 r 轮按攻击对象归类，便于看「一个宣称被几轮合流攻破」；正确理论体系主题为 PASS（整理核），其余四主题均为 FAIL。' },
  { term: '退守路径', tag: '审计', def: '主宣称被判否后改换的弱化版本（换群族、加阈值凑汇聚、降能标、紫外完备、剔除引力）。攻破链铁律：封死一条路后必须立刻堵退守路径，否则判决只是把问题推后一格（r123 即 r120 的退守封堵增补卷，两册条目不可相加）。' },
  { term: '质子衰变安全线', tag: '判据', def: '由 Super-K 上限 τ_p>2.4e34 yr 与 τ_p∝M_GUT⁴（维度-6）反算的统一能标下限 M_GUT ≥ 6.12e15 GeV；越线方案不是「未检验」而是「已被排除」（r123 R3）。' },
  { term: 'de Broglie 内时钟', tag: '光子', def: 'ω_int=mc²/ħ；光子 m=0 ⇒ 内时钟恒为零，即光子无内部时间演化（r117 锁死）。' },
  { term: 'κ-τ 螺旋', tag: '螺旋', def: '曲率 κ 与挠率 τ 参数化；ROOT 部署用 R=λ/2π、Ω=2πf。版本 A（轴向=c）类空超光速、版本 B（总速=c）类光致 Frenet 无定义，无第三支（66/67 号卷）。' },
  { term: '电弱统一控制组', tag: '判据', def: '用同一套判据判人类唯一已完成的统一（SU(2)×U(1)：预言 m_t 偏差 0.139%）：6/6 通过，证判据有判别力而非一律否定（r119）；r123 控制组 4/4 同款。' },
  { term: '量纲审计', tag: '判据', def: '在自然单位与 (M,L,T) 双基下检查作用量/场方程量纲自洽；有量纲自由参数 = 非定律。' },
  { term: '数值稳定性五戒', tag: '判据', def: '差分步长按 ω·h≈1e-4 自适应；Simpson 复合公式 1/3 因子不漏；量级 sanity 守卫（t<宇宙年龄、长度>ℓ_Pl、v≤c）；枚举门含局域光速门；单调性守卫先固定自变量排序方向。' },
  { term: '可证伪性', tag: '判据', def: '理论须给出至少一个近期可观测预言（如质子衰变寿命）；否则本代不可证伪（r119 U6 最致命缺口）。' },
  { term: '洛伦兹协变', tag: '判据', def: 'κ,τ,ω 必须洛伦兹协变，否则不同观测者给出矛盾判决（r116 分歧闭合条款）。' },
  { term: '抄录检测', tag: '判据', def: '靶模型独有参数对结论的依赖计数须 >0；若依赖 0 即 GR/教科书抄录，无新增内容。' },
  { term: '反解闭环', tag: '判据', def: '常数由自身反解再「验证」自身即循环恒等（如 G=2Z/c、Gε₀）。' },
  { term: '参数计数门', tag: '判据', def: '自由参数当量须 ≤ 观测量−1；凑汇聚型方案（如加阈值）参数当量 41 ≫ 2 ⇒ 不可辨识（r123 R2，同 r112 款）。' },
  { term: '断裂边界', tag: '攻破', def: `同一套判据压测正确理论（SM+GR）自身得到的失效边界，已定价到 dex（r127/r128/r131 共 ${boundaryTotal.value} 条）；不解释其中任意一条就谈不上超越标准模型——这是未来任何新理论的最低任务清单。` },
  { term: '推导链闭合率', tag: '攻破', def: 'r130 口径：推导链前提中 DERIVED 的占比。18 条链 0 闭合（总闭合率 0.327）⇒ SOUND-BUT-PREMISE-OPEN：方程对，但 EH 作用量/规范原理/测量公设等都是公设不是导出。' },
  { term: 'SOUND-BUT-PREMISE-OPEN', tag: '攻破', def: 'r130 总判：理论在其公设内自洽（sound）但无一条推导链从更底层闭合（premise-open）。与「已证伪」不同——它否证的是「第一性导出」宣称，不是方程本身。' },
  { term: '宇宙运行秘密', tag: '本质', def: '任何宣称若提不出可审动力学方程（如 ROOT 站点 §04 自承零方程），即不在证据射程内，登记为「无方程可审」。' },
  { term: '关联图谱节点', tag: '可视化', def: '主题(枢纽) — 攻破轮 — 正确核/黑名单。边：蓝=隶属主题、红虚线=登记黑名单、橙点线=降级正确核；点击出判决详情，可拖拽固定。' },
  { term: '攻破工作台', tag: '系统', def: '复用审计判据库录入新宣称、逐条守卫自检、生成机读 verdict 并持久化到本机 localStorage，立即进入图谱与攻破链；支持导出与 53 引擎同 schema 的 JSON。' }
])

const q = ref('')
const filtered = computed(() => {
  const s = q.value.trim().toLowerCase()
  if (!s) return glossary.value
  return glossary.value.filter(g => (g.term + g.def + g.tag).toLowerCase().includes(s))
})
</script>

<style scoped>
.gl-search { max-width: 340px; }
.grid-2col { grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); }
</style>
