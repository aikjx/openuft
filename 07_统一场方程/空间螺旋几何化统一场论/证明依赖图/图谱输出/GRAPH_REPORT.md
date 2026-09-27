# TUFT 正文证明依赖图：阅读地图，不是证明认证

范围：顶层29份tuft_*.md。原始目录33项检测后，排除README与原稿子目录3份。仅聚焦论证接口和正文显式引文，未穷举全部公式，也未执行原有物理脚本。

边方向：论点 → 所采用的输入/前提；文档 → 所引用的文档。EXTRACTED=正文确实这么说，绝不表示其数学或物理内容已成立。AMBIGUOUS表示桥梁或适用性未证。节点epistemic_status与rationale保留来源断言的地位。

成本：本机内联语义提取，无独立API调用；实际宿主token不可读取，图工具计数0不是零工作量。缓存、manifest、脚本和全部产物均写入本输出目录，未改源正文。

工具限制：graphify benchmark已运行，但其内置示例问题未匹配中文图节点，返回No matching nodes found；因此不报告token压缩成绩。有向图无边折叠；健康检查中的7条“无向折叠”只是反向引文对在假设改成无向图时的结果，本产物保持方向。

## 必须重审的来源断言

- **轴挠率单模传播：需完整拉氏量**：正文只列L_T^axial名字与谱表，未给完整系数和约束；4维轴向分量不能自动当1个传播自由度。（tuft_统一场论_完成版_终版陈述.md，83行）
- **b+4c=0：适用几何必须限定**：无挠Levi-Civita曲率二次型可如此换基；独立Cartan联络含挠时不能直接推广无鬼充分性。（tuft_统一场论_完成版_终版陈述.md，66行）
- **曲率平方前因子存在量纲风险**：自然单位[κ]=-2，[R²]=4，1/κ²使密度为8；若α无量纲，则与正文7/7配平声明冲突。（tuft_统一场论_完成版_终版陈述.md，41行）
- **直积是唯一选择：只记来源断言**：非紧群不能嵌入紧致群不推出所有统一方案不可达；只否定此种嵌入，应限定no-go范围。（tuft_统一场论_完成版_终版陈述.md，21行）
- **Nieh–Yan恰当形式与整数化条件**：恒等式NY=d(e∧T)与整数化不同：一般积分依赖边界、归一化和几何尺度；正文没有一般整值性证明。（tuft_公理化_文稿_修订版.md，117行）
- **半整数Gauss链接：端点需复查**：奇半扭转单侧法向偏移q(2π)≠q(0)，不能直接当两条不交闭曲线的Gauss链接数；数值半整数不是通常链接整值定理。（tuft_相位pi_文稿_修订版.md，127行）
- **s=|Lk|：几何到自旋对应输入**：计算Tw或标架周期不自行给出SO3/SU2量子表示、算符代数或旋转生成元；保留来源声称。（tuft_r2_全维求导证明验证精算报告.md，11行）
- **跑动公式K→0与文稿文字冲突**：正b0公式α0/[1+b0α0 ln(Ksat/K)]在K→0为0，不增强或趋1/b0；只记录待修正断言。（tuft_色挠率_SU3_文稿_修订版.md，167行）
- **自屏蔽数值解及波形代理**：静态质量比不能自动给完整双星波形；来源LIGO排除结论需真实动力学映射与数据似然复核。（tuft_B_自屏蔽_数值求解报告.md，17行）
- **δu径向应变映射需场方程**：标量波方程不能直接认证GR张量偏振或所有度规响应；需场方程、规范和探测器响应。（tuft_续篇B_挠率引力波.md，13行）

## 图完整性

[graphify] MultiDiGraph edge-collapse diagnostic
input: <in-memory>
input_stage: provided JSON (normal graph.json is post-build)
effective_directed: <direct-call>
nodes: 68
unverified_code_nodes: 0
raw_edges: 110
valid_candidate_edges: 110
missing_endpoint_edges: 0
dangling_endpoint_edges: 0
self_loop_edges: 0
exact_duplicate_edges: 0
directed_unique_endpoint_pairs: 110
directed_same_endpoint_collapsed_edges: 0
undirected_unique_endpoint_pairs: 103
undirected_same_endpoint_collapsed_edges: 7
same_endpoint_group_count: 0
relation_variant_groups: 0
source_file_variant_groups: 0
source_location_variant_groups: 0
context_variant_groups: 0
post_build_graph_type: DiGraph
post_build_edges: 110
producer_suppression_sites: 12
producer_suppression_examples:
  - L1336 seen_ids arity=unknown
  - L1869 seen_ids arity=unknown
  - L1871 seen_doc_refs arity=unknown
  - L2241 seen_ids arity=unknown
  - L2388 seen_ids arity=unknown
  - L3026 seen_keys arity=unknown
  - L3195 seen_keys arity=unknown
  - L4887 seen_ids arity=unknown
note: normal graph.json is post-build; raw producer loss must be measured earlier.

# Graph Report - 论文正文  (2026-09-27)

## Corpus Check
- Corpus is ~22,021 words - fits in a single context window. You may not need a graph.

## Summary
- 68 nodes · 110 edges · 12 communities (11 shown, 1 thin omitted)
- Extraction: 87% EXTRACTED · 9% INFERRED · 4% AMBIGUOUS · INFERRED: 10 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- 自旋统计接口与引力波续篇
- 自屏蔽源项与UV选型
- 终版作用量与传播谱边界
- Cartan公理与规范外部输入
- 莫比乌斯标架与旋转桥梁
- 跨册判据与审查引文
- 宇宙学慢滚与全书总账
- SU3接入与色挠率映射
- 四力直积与参数继承
- 黑洞热力学与奇点边界
- 公理化修复与ξ尺度限制
- R1到R4验证标签边界

## God Nodes (most connected - your core abstractions)
1. `TUFT 全景索引` - 27 edges
2. `TUFT 全景总报告（最终交付版）` - 12 edges
3. `TUFT《数学公理化：微分几何 + 主丛公理体系》· 诚实修订版 v2.1` - 11 edges
4. `TUFT v3《自洽的引力–挠率–标量体系》· 终版陈述与收口报告` - 10 edges
5. `TUFT 全维统一场论 — 续篇：费米子自旋统计、泡利原理、拓扑螺旋本征态` - 8 edges
6. `TUFT 全维统一场论 · 全书交付版（生成件）` - 6 edges
7. `TUFT 全维统一场论：色挠率 SU(3) 多分量挠率张量、渐近自由与色禁闭 —— **诚实修订版**` - 6 edges
8. `TUFT 公理化 · 修复后「全维修复优化」报告` - 5 edges
9. `TUFT 全维统一场论：四大相互作用完整规范群统一结构 —— **诚实修订版**` - 5 edges
10. `TUFT 全维统一场论：费米子闭环一圈相位翻转 π —— **诚实修订版**` - 5 edges

## Surprising Connections (you probably didn't know these)
- `完成仅限写形：非四力统一` --depends_on--> `ξ三视界约束：具体耦合边界`  [INFERRED]
  tuft_统一场论_完成版_终版陈述.md → tuft_公理化_修复优化报告.md
- `TUFT 全景索引` --cites--> `TUFT-B 修复检验报告：UV 完成能否抑制强场自屏蔽？`  [EXTRACTED]
  tuft_总索引.md → tuft_B_UV完成报告.md
- `TUFT 全景索引` --cites--> `TUFT-B 根因溯源报告：自屏蔽因子 exp(−u) 从哪来？`  [EXTRACTED]
  tuft_总索引.md → tuft_B_根因溯源报告.md
- `TUFT 全景索引` --cites--> `TUFT-B 科学处理流程报告：R1 自屏蔽场方程的数值求解与观测对标`  [EXTRACTED]
  tuft_总索引.md → tuft_B_自屏蔽_数值求解报告.md
- `TUFT 全景索引` --cites--> `TUFT-R2 全维求导证明 · 验证 · 分析 · 精算`  [EXTRACTED]
  tuft_总索引.md → tuft_r2_全维求导证明验证精算报告.md

## Communities (12 total, 1 thin omitted)

### Community 0 - "自旋统计接口与引力波续篇"
Cohesion: 0.31
Nodes (9): TUFT 全维统一场论 — 续篇：费米子自旋统计、泡利原理、拓扑螺旋本征态, 合法质量式仍缺尺度生成, 反对称波函数⇒同态Slater为零, SU2自旋表示：赋以而非导出, 弱手性映射仍为定性假设, TUFT 续篇 · 全维求导证明与精算报告, 交换相位含循环输入, TUFT 续篇·选项 B：挠率诱导引力波（定量 + 诚实边界） (+1 more)

### Community 1 - "自屏蔽源项与UV选型"
Cohesion: 0.25
Nodes (8): TUFT-B 修复检验报告：UV 完成能否抑制强场自屏蔽？, UV填回为唯象选型, β∇²lnβ恒等式与条件源项, TUFT-B 根因溯源报告：自屏蔽因子 exp(−u) 从哪来？, TUFT-B 科学处理流程报告：R1 自屏蔽场方程的数值求解与观测对标, 自屏蔽数值解及波形代理, β层场方程是修复选择, TUFT 收口报告：分析 + 修复 + 优化方案

### Community 2 - "终版作用量与传播谱边界"
Cohesion: 0.39
Nodes (8): 轴挠率单模传播：需完整拉氏量, 直积是唯一选择：只记来源断言, 完成仅限写形：非四力统一, TUFT v3《自洽的引力–挠率–标量体系》· 终版陈述与收口报告, 曲率平方前因子存在量纲风险, 挠率代数分解 24=4+4+16, 群选择、耦合映射、量子化未完成, b+4c=0：适用几何必须限定

### Community 3 - "Cartan公理与规范外部输入"
Cohesion: 0.38
Nodes (7): Cartan几何与内部规范丛并列, TUFT《数学公理化：微分几何 + 主丛公理体系》· 诚实修订版 v2.1, Nieh–Yan恰当形式与整数化条件, θ0、V0、Λeff为外锚, 标量Euler-Lagrange条件式, SU3×SU2×U1：外部规范输入, T²代数项与挠率传播项区分

### Community 4 - "莫比乌斯标架与旋转桥梁"
Cohesion: 0.40
Nodes (6): TUFT-R2 全维求导证明 · 验证 · 分析 · 精算, s=|Lk|：几何到自旋对应输入, TUFT 全维统一场论：费米子闭环一圈相位翻转 π —— **诚实修订版**, Möbius标架翻转与4π复原, 半整数Gauss链接：端点需复查, 标架绕行与空间旋转桥梁未证

### Community 5 - "跨册判据与审查引文"
Cohesion: 0.33
Nodes (6): TUFT 三路线 A/B/C · 全维分析 + 处理 + 修复 + 优化报告, 量纲门禁不认证物理正确, TUFT 判据门禁（自动生成）, TUFT 全景索引, TUFT 文稿 · 全维求导证明与精算报告（费米子闭环一圈相位 = π）, TUFT 色挠率 SU(3) · 全维求导证明与精算报告

### Community 6 - "宇宙学慢滚与全书总账"
Cohesion: 0.53
Nodes (6): TUFT 全维统一场论 · 全书交付版（生成件）, TUFT 全景总报告（最终交付版）, 原势慢滚预言未闭合, TUFT 全维统一场论：宇宙暴胀、原初扰动与 CMB 可观测预言 —— **诚实修订版**, TUFT 宇宙暴胀 / 原初扰动 / CMB 可观测预言 · 全维求导证明与精算报告, TUFT 跨册缺陷族与汇编一致性（自动生成）

### Community 7 - "SU3接入与色挠率映射"
Cohesion: 0.50
Nodes (5): TUFT 全维统一场论：色挠率 SU(3) 多分量挠率张量、渐近自由与色禁闭 —— **诚实修订版**, K∝r积分给r²：非线性弦势, 标准QCD拉氏量被采用, 跑动公式K→0与文稿文字冲突, T^a→A^a及K→Q²映射开放

### Community 8 - "四力直积与参数继承"
Cohesion: 0.67
Nodes (4): TUFT 全维统一场论：四大相互作用完整规范群统一结构 —— **诚实修订版**, 直积规范群不自动约束耦合, 继承SM自由参数, TUFT 四大相互作用完整规范群统一结构 · 全维求导证明与精算报告

### Community 9 - "黑洞热力学与奇点边界"
Cohesion: 0.50
Nodes (4): BH温度熵采用标准结果, TUFT 全维统一场论：黑洞热力学、视界曲率-挠率边界条件与黑洞信息悖论 —— **诚实修订版**, 曲率有界≠测地完备, TUFT 黑洞热力学 / 视界曲率-挠率边界 / 信息悖论 · 全维求导证明与精算报告

### Community 10 - "公理化修复与ξ尺度限制"
Cohesion: 0.67
Nodes (3): TUFT 公理化 · 修复后「全维修复优化」报告, ξ三视界约束：具体耦合边界, TUFT《数学公理化：微分几何 + 主丛公理体系》· 全维精算报告

## Ambiguous Edges - Review These
- `完成仅限写形：非四力统一` → `曲率平方前因子存在量纲风险`  [AMBIGUOUS]
  tuft_统一场论_完成版_终版陈述.md · relation: depends_on
- `轴挠率单模传播：需完整拉氏量` → `b+4c=0：适用几何必须限定`  [AMBIGUOUS]
  tuft_统一场论_完成版_终版陈述.md · relation: depends_on
- `s=|Lk|：几何到自旋对应输入` → `标架绕行与空间旋转桥梁未证`  [AMBIGUOUS]
  tuft_相位pi_文稿_修订版.md · relation: depends_on
- `标准QCD拉氏量被采用` → `T^a→A^a及K→Q²映射开放`  [AMBIGUOUS]
  tuft_色挠率_SU3_文稿_修订版.md · relation: depends_on

## Knowledge Gaps
- **3 isolated node(s):** `TUFT 三路线 A/B/C · 全维分析 + 处理 + 修复 + 优化报告`, `TUFT 文稿 · 全维求导证明与精算报告（费米子闭环一圈相位 = π）`, `TUFT 色挠率 SU(3) · 全维求导证明与精算报告`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 17 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `完成仅限写形：非四力统一` and `曲率平方前因子存在量纲风险`?**
  _Edge tagged AMBIGUOUS (relation: depends_on) - confidence is low._
- **What is the exact relationship between `轴挠率单模传播：需完整拉氏量` and `b+4c=0：适用几何必须限定`?**
  _Edge tagged AMBIGUOUS (relation: depends_on) - confidence is low._
- **What is the exact relationship between `s=|Lk|：几何到自旋对应输入` and `标架绕行与空间旋转桥梁未证`?**
  _Edge tagged AMBIGUOUS (relation: depends_on) - confidence is low._
- **What is the exact relationship between `标准QCD拉氏量被采用` and `T^a→A^a及K→Q²映射开放`?**
  _Edge tagged AMBIGUOUS (relation: depends_on) - confidence is low._
- **Why does `TUFT 全景索引` connect `跨册判据与审查引文` to `自旋统计接口与引力波续篇`, `自屏蔽源项与UV选型`, `莫比乌斯标架与旋转桥梁`, `宇宙学慢滚与全书总账`, `SU3接入与色挠率映射`, `四力直积与参数继承`, `黑洞热力学与奇点边界`, `R1到R4验证标签边界`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Why does `TUFT 全景总报告（最终交付版）` connect `宇宙学慢滚与全书总账` to `莫比乌斯标架与旋转桥梁`, `跨册判据与审查引文`, `SU3接入与色挠率映射`, `四力直积与参数继承`, `黑洞热力学与奇点边界`?**
  _High betweenness centrality (0.005) - this node is a cross-community bridge._
- **What connects `TUFT 三路线 A/B/C · 全维分析 + 处理 + 修复 + 优化报告`, `TUFT 文稿 · 全维求导证明与精算报告（费米子闭环一圈相位 = π）`, `TUFT 色挠率 SU(3) · 全维求导证明与精算报告` to the rest of the system?**
  _3 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Möbius标架4π复原与费米交换反对称之间缺哪一步独立证明？**
  _追溯输入、适用条件与尚未闭合的物理桥梁。_
- **终版作用量的R²前因子与无鬼条件依赖哪些几何和量纲约定？**
  _追溯输入、适用条件与尚未闭合的物理桥梁。_
- **SU(3)色挠率主张哪些是标准模型输入，哪些是尚缺的映射？**
  _追溯输入、适用条件与尚未闭合的物理桥梁。_