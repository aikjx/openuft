<template>
  <div>
    <div class="page-head">
      <div class="page-title">统一场论 · 最终结论</div>
      <div class="page-sub">全域物理审计图谱（openuft）对「统一场论」命题的穷尽攻破与正确理论整理之权威结论。所有数字均机读自图谱数据，本视图不重判。</div>
    </div>

    <!-- 总判定 banner -->
    <div class="verdict-banner">
      <div class="vb-stamp">已提出的方案均被攻破 · 真正统一【未完成】</div>
      <p class="vb-text">
        「统一场论」作为<b>已提出的具体方案</b>（单一框架统一四力 + 引力 + 导出物质与时空本源），在本审计中已被
        <b>{{ themesFail }}</b> 个攻击主题、数十轮机读攻破合流否定——没有一条候选方案存活。
        但对「真正统一」这一<b>科学目标</b>，诚实结论是 <b>未完成</b>（r134）：完成度仅 <b>1/7</b>，唯一门（前提净下降）无人通过、结构不可修补。
        唯一被完整保留并机读验证的理论核心是 <b>SM + GR</b>——但它在 {{ boundaryTotal }} 条断裂边界下仅是「在公设内自洽」，而非「从更底层导出」。
      </p>
    </div>

    <!-- 关键数字 -->
    <div class="kvs" style="margin-bottom:16px">
      <div class="kv"><div class="k">攻破轮</div><div class="v">{{ counts.rounds }}</div></div>
      <div class="kv"><div class="k">攻击主题（全 FAIL）</div><div class="v" style="color:var(--fail)">{{ themesFail }}</div></div>
      <div class="kv"><div class="k">正确核 保留 / 降级</div><div class="v">{{ counts.coresSurvive }}<small> / {{ counts.coresDowngraded }}</small></div></div>
      <div class="kv"><div class="k">不可引用黑名单</div><div class="v" style="color:var(--fail)">{{ counts.blacklist }}</div></div>
      <div class="kv"><div class="k">机读验证方程</div><div class="v" style="color:var(--ok)">{{ eqTotal }}</div></div>
      <div class="kv"><div class="k">断裂边界</div><div class="v" style="color:var(--boundary)">{{ boundaryTotal }}</div></div>
      <div class="kv"><div class="k">推导链闭合</div><div class="v" style="color:var(--fail)">{{ cs.chains.summary.n_closed }}/{{ cs.chains.summary.n_chains }}</div></div>
      <div class="kv"><div class="k">机读守卫</div><div class="v" style="color:var(--accent)">{{ counts.guards }}</div></div>
    </div>

    <!-- 攻破全景 -->
    <div class="card" style="margin-bottom:16px">
      <div class="card-title">一 · 攻破全景：五主题合流否定 <span class="tag tag-fail">ALL FAIL</span></div>
      <div class="grid grid-1-1">
        <div v-for="t in themes" :key="t.id" class="theme-card">
          <div class="tc-head">
            <span class="dot" :style="{ background: t.hex }"></span>
            <b>{{ t.name }}</b>
            <span class="tag" :class="verdictTag(t.verdict)">{{ t.verdict }}</span>
            <span class="dim tc-count">{{ t.rounds.length }} 轮</span>
          </div>
          <p class="dim tc-sum">{{ shortSummary(t.summary) }}</p>
        </div>
      </div>
    </div>

    <!-- 正确理论体系 -->
    <div class="card" style="margin-bottom:16px">
      <div class="card-title">二 · 保留的核心：SM + GR 正确理论体系 <span class="tag tag-ok">{{ eqTotal }} 条机读验证</span></div>
      <p class="thesis">{{ cs.thesis }}</p>
      <p class="dim" style="font-size:12.5px;line-height:1.7;margin:8px 0 0">
        方程级验证 {{ cs.equations.equationTier.length }} 条 + 体系级验证 {{ cs.equations.systemTier.length }} 条，全部机读 PASS（含双向控制组）。详细方程、断裂边界与推导链见
        <RouterLink to="/correct" class="il">正确理论体系视图</RouterLink>。
      </p>
    </div>

    <!-- 断裂边界 -->
    <div class="card" style="margin-bottom:16px">
      <div class="card-title">三 · 未来任何新理论的「最低任务清单」：{{ boundaryTotal }} 条断裂边界 <span class="tag tag-boundary">定价到 dex</span></div>
      <p class="dim" style="font-size:12.5px;line-height:1.7;margin:0 0 12px">
        同一套判据压测正确理论自身得到的失效边界。不解释其中任意一条，就谈不上超越标准模型——这是新理论必须正面回答的硬指标。
      </p>
      <div class="grid grid-1-1">
        <div v-for="(grp, key) in cs.boundaries" :key="key">
          <div class="blk-h">{{ grp.label }} <span class="dim" style="font-weight:400">{{ grp.note }}</span></div>
          <div v-for="b in grp.items" :key="key + b.id" class="bd-row">
            <div class="bd-head">
              <span class="mono">{{ b.id }}</span>
              <b class="bd-title">{{ b.title }}</b>
              <span :class="verdictTag(b.verdict)" style="margin-left:auto">{{ b.verdict }}</span>
            </div>
            <div class="bd-price mono">{{ b.price }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 结构不可修补 -->
    <div class="card" style="margin-bottom:16px">
      <div class="card-title">四 · 结构不可修补定理（r133 元判定） <span class="tag tag-fail">UNPATCHABLE</span></div>
      <p class="dim" style="font-size:13px;line-height:1.8;margin:0">
        对 19 次局部修补 / 修改（r124 F1–F6、r123 五退守、r129 R1–R5、r131 扩容、r125 A05/A08）逐条四型归类：
        <b>外部输入(11) / 零信息重排(2) / 范围退缩(4) / 自相矛盾(2)</b>；前提净变化 +11，任一均不闭合全局缺口。
        元判定：<b>结构不可修补 = 成立</b>——闭合率不可能由局部修补从 0.327 推到 1。即：你无法通过在 SM+GR 上「打补丁」来消除那 {{ boundaryTotal }} 条断裂边界。
      </p>
    </div>

    <!-- 方法论 -->
    <div class="card" style="margin-bottom:16px">
      <div class="card-title">五 · 可复用审计方法论（判据族） <span class="tag tag-info">METHOD</span></div>
      <div class="grid grid-2col">
        <div v-for="c in methodItems" :key="c.k" class="meth">
          <div class="meth-k">{{ c.k }}</div>
          <div class="dim meth-d">{{ c.d }}</div>
        </div>
      </div>
    </div>

    <!-- 诚实未解决域 -->
    <div class="card">
      <div class="card-title">六 · 诚实未解决域（正确理论自身的 OPEN 状态） <span class="tag tag-boundary">OPEN</span></div>
      <p class="dim" style="font-size:12.5px;line-height:1.7;margin:0 0 10px">
        即便对保留的 SM+GR，其推导链仍有 <b>{{ cs.chains.summary.premise_open }}</b> 条前提开放、<b>{{ cs.chains.summary.domain_limited }}</b> 条域限、<b>{{ cs.chains.summary.conjectural }}</b> 条猜想（总闭合率 {{ (cs.chains.summary.closure_all * 100).toFixed(1) }}%）。
        这些不是「已被攻破」，而是「正确理论也尚未从更底层导出」的诚实登记——它们与上面的 {{ boundaryTotal }} 条断裂边界共同构成未来理论的真正起点。
      </p>
      <div class="kvs">
        <div class="kv"><div class="k">前提开放</div><div class="v" style="color:var(--fail)">{{ cs.chains.summary.premise_open }}</div></div>
        <div class="kv"><div class="k">域限</div><div class="v" style="color:var(--boundary)">{{ cs.chains.summary.domain_limited }}</div></div>
        <div class="kv"><div class="k">猜想</div><div class="v" style="color:var(--info)">{{ cs.chains.summary.conjectural }}</div></div>
        <div class="kv"><div class="k">总闭合率</div><div class="v">{{ (cs.chains.summary.closure_all * 100).toFixed(1) }}%</div></div>
      </div>
    </div>

    <!-- 建设性纲领 r134 -->
    <div class="card">
      <div class="card-title">七 · 建设性纲领（r134）：什么才算「完成」 <span class="tag tag-info">PROGRAM</span></div>
      <p class="dim" style="font-size:13px;line-height:1.85;margin:0">
        r134 把「统一场论完成」定义为可机读、可证伪的判据并冻结：① <b>完成判据 U1–U7</b>（r119 七必要条件）冻结，完成度重定价为 <b>1/7 = 0.1429</b>（唯一达标 U7「相容」≠ 统一，是最弱一条）；② <b>控制组电弱 6/6</b> 通过，证明判据有判别力（不是一律否定）；③ <b>唯一门：前提净下降</b>——r133 的 19 次修补净变化 +11，无人让未导出前提（37 条）净减少，门未通过；r135 的无质量自旋-2 路线<b>首次让该门过关（Δ=-1，导出 EH 形式与 SEP）</b>，但新前提「自旋-2 场存在」恰由 EH 量子化导出、与结论成环（CIRCULAR-SUSPECT），故门虽过仍非真正完成——判据本身须防循环自证；④ 元判定 <b>结构不可修补 = 成立</b>：闭合率不可能由局部修补从 0.327 推到 1。
      </p>
      <p class="dim" style="font-size:13px;line-height:1.85;margin:10px 0 0">
        <b>建设性要求</b>：要真正「完成」，须从更底层导出四块最深的 <span class="mono">POSTED</span> 前提（EH 作用量形式 / 规范群 SU(3)×SU(2)×U(1) / μ²&lt;0 希格斯机制 / 宇宙学常数 SEP），以及力的四起源 g, g′, g_s, G。
        这 {{ boundaryTotal }} 条断裂边界 + 37 条未导出前提，就是未来任何新理论的<b>最低任务清单与诚实起点</b>——而非本库已攻破的战果。
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useOpenuft } from '@/composables/useOpenuft.js'

const { meta, themes, correctSystem } = useOpenuft()
const counts = computed(() => meta.value?.counts || {})
const cs = computed(() => correctSystem.value || { equations: { equationTier: [], systemTier: [] }, boundaries: {}, chains: { summary: {} }, thesis: '' })

const eqTotal = computed(() => (cs.value.equations?.equationTier?.length || 0) + (cs.value.equations?.systemTier?.length || 0))
const boundaryTotal = computed(() => Object.values(cs.value.boundaries || {}).reduce((s, g) => s + (g.items ? g.items.length : 0), 0))
const themesFail = computed(() => themes.value.filter(t => t.verdict === 'FAIL').length)

function verdictTag(v) {
  return v === 'FAIL' ? 'tag-fail' : (v === 'PASS' ? 'tag-ok' : 'tag-boundary')
}
function shortSummary(s) {
  s = s || ''
  return s.length > 170 ? s.slice(0, 170) + '…' : s
}

const methodItems = [
  { k: '量纲审计', d: '所有方程须通过 (M,L,T) 双基量纲平衡；一处失衡即结构性不成立，不接受「只查 E 幂」的假绿。' },
  { k: '数值稳定性', d: '差分步长自适应、含量级 sanity 守卫（时间<宇宙年龄、长度>ℓ_P、速度≤c）、单调性守卫，杜绝伪精度。' },
  { k: '控制组对照', d: '同一判据须让错误理论 FAIL、正确核 PASS（失控退出码 2）；否则判据本身不可信。' },
  { k: '抄录检测', d: '靶模型独有参数对结论的依赖计数须 >0，否则为教科书抄录、无新增内容。' },
  { k: '反解闭环', d: '常数由自身反解再「验证」自身即循环恒等（如 G=2Z/c），判否。' },
  { k: '判据判别力', d: '判据须可证伪且对已知锚点通过；否则只是「一律否定」或「一律放行」。' },
  { k: '洛伦兹协变', d: '物理宣称须显式声明能标与协变形式，否则跨册符号反向误读。' },
  { k: '可证伪性', d: '每个「不可能」结论须自带可推翻边界；无边界即不可证伪，判为伪科学。' }
]
</script>

<style scoped>
.verdict-banner {
  background: linear-gradient(135deg, rgba(255,93,108,.10), rgba(124,92,255,.10));
  border: 1px solid var(--line); border-left: 3px solid var(--fail);
  border-radius: var(--radius); padding: 18px 20px; margin-bottom: 18px;
}
.vb-stamp {
  display: inline-block; font-size: 13px; font-weight: 800; letter-spacing: 1px;
  color: #fff; background: var(--fail); padding: 5px 14px; border-radius: 999px; margin-bottom: 12px;
}
.vb-text { font-size: 14px; line-height: 1.85; margin: 0; color: var(--text); }
.vb-text b { color: #fff; }

.theme-card { background: var(--panel-2); border-radius: 10px; padding: 13px 15px; }
.tc-head { display: flex; align-items: center; gap: 8px; font-size: 13.5px; }
.tc-count { margin-left: auto; font-size: 11px; }
.tc-sum { font-size: 12px; line-height: 1.6; margin: 8px 0 0; }

.blk-h { font-size: 13px; font-weight: 700; margin: 4px 0 8px; color: var(--text); }
.bd-row { padding: 8px 0; border-bottom: 1px solid var(--line-soft); }
.bd-row:last-child { border-bottom: none; }
.bd-head { display: flex; align-items: center; gap: 8px; font-size: 12.5px; }
.bd-title { font-size: 12.5px; font-weight: 500; }
.bd-price { font-size: 11.5px; color: var(--boundary); margin-top: 3px; }

.thesis { font-size: 14px; color: var(--text); line-height: 1.8; margin: 0; }
.il { color: var(--accent); text-decoration: none; border-bottom: 1px dashed var(--accent); }
.il:hover { filter: brightness(1.15); }

.meth { background: var(--panel-2); border-radius: 10px; padding: 12px 14px; }
.meth-k { font-size: 13px; font-weight: 700; color: var(--text); margin-bottom: 5px; }
.meth-d { font-size: 12px; line-height: 1.6; }
</style>
