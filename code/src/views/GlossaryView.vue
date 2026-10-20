<template>
  <div>
    <div class="page-head">
      <div class="page-title">术语表 · Glossary</div>
      <div class="page-sub">本系统使用的核心术语与判据口径，便于跨视图引用与长期维护。</div>
    </div>
    <div class="grid" style="grid-template-columns: 1fr 1fr">
      <div v-for="g in glossary" :key="g.term" class="card">
        <div class="card-title">{{ g.term }} <span class="tag">{{ g.tag }}</span></div>
        <p class="dim" style="font-size:12.5px;line-height:1.7;margin:0">{{ g.def }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
const glossary = [
  { term: '正确核', tag: '账本', def: '53 卷保留的 16 条物理内容：教科书物理在另一套记号下的改写、代数恒等或已证几何定理，全部非本库新增。' },
  { term: '黑名单', tag: '账本', def: '13 条不可引用登记：被 r 系列判否的对象（循环恒等、欠定定义、伪精度、原理性 no-go 等），不得作为推导前提。' },
  { term: '攻破轮 (rNNN)', tag: '审计', def: '对某一宣称的可机读判决单元；每轮含靶宣称、审计条目、verdict（PASS/FAIL/BOUNDARY）与守卫。' },
  { term: '主题射程', tag: '聚合', def: '四主题（力的统一 / 引力的本源 / 光子的本质 / 螺旋几何化）把 r 轮按攻击对象归类，便于看「一个宣称被几轮合流攻破」。' },
  { term: 'de Broglie 内时钟', tag: '光子', def: 'ω_int=mc²/ħ；光子 m=0 ⇒ 内时钟恒为零，即光子无内部时间演化（r117 锁死）。' },
  { term: 'κ-τ 螺旋', tag: '螺旋', def: '曲率 κ 与挠率 τ 参数化；ROOT 部署用 R=λ/2π、Ω=2πf。版本 A（轴向=c）类空超光速、版本 B（总速=c）类光致 Frenet 无定义，无第三支（66/67 号卷）。' },
  { term: '电弱统一控制组', tag: '判据', def: '用同一套判据判人类唯一已完成的统一（SU(2)×U(1)）：6/6 通过，证判据有判别力而非一律否定（r119）。' },
  { term: '量纲审计', tag: '判据', def: '在自然单位与 (M,L,T) 双基下检查作用量/场方程量纲自洽；有量纲自由参数 = 非定律。' },
  { term: '可证伪性', tag: '判据', def: '理论须给出至少一个近期可观测预言（如质子衰变寿命）；否则本代不可证伪（r119 U6 最致命缺口）。' },
  { term: '洛伦兹协变', tag: '判据', def: 'κ,τ,ω 必须洛伦兹协变，否则不同观测者给出矛盾判决（r116 分歧闭合条款）。' },
  { term: '抄录检测', tag: '判据', def: '靶模型独有参数对结论的依赖计数须 >0；若依赖 0 即 GR/教科书抄录，无新增内容。' },
  { term: '反解闭环', tag: '判据', def: '常数由自身反解再「验证」自身即循环恒等（如 G=2Z/c、Gε₀）。' },
  { term: '宇宙运行秘密', tag: '本质', def: '任何宣称若提不出可审动力学方程（如 ROOT 站点 §04 自承零方程），即不在证据射程内，登记为「无方程可审」。' },
  { term: '关联图谱节点', tag: '可视化', def: '主题(蓝枢纽) — 攻破轮(红) — 正确核(绿)/黑名单(红点)。边：蓝=隶属主题、红虚线=登记黑名单、橙点线=降级正确核。' },
  { term: '攻破工作台', tag: '系统', def: '复用审计判据库录入新宣称、逐条守卫自检、生成机读 verdict 并持久化到本机，立即进入图谱与攻破链。' }
]
</script>

<style scoped>
</style>
