# CLAIMS 列语义对账审计 —— 分析记录（OPEN-B8/B9/B10 证据）

> 生成：自动演化引擎·企业级多域守卫「分析优化」轮次
> 工具：`00_项目治理/维护工具/claims_columns_audit.py`（隔离分析，未篡改任何 CURATED 真源）
> 状态：证据完备，待所属方裁定列语义映射

---

## 一、审计范围与口径

- 扫描全部活跃 `01_独立体系/*/claims.csv`，共 **23 个体系**。
- 对 8 个语义列做形态对账：`prediction / prediction_value / prediction_urel / run_id / data_id / uncertainty / evidence_level / status / reviewer`。
- 形态分类：`short(<16字) / long(>=16字) / num / empty`。
- 串列规则（仅报告证据）：evidence_level 长文本→疑 uncertainty 串列；evidence_level 单字母→疑 reviewer 分级串列；status 出现非合法证据词→疑 evidence_level 串列（`verified` 等合法状态词已排除，不误报）。

## 二、全 23 体系扫描结论

| 现象 | 涉及体系 | 判定 |
|---|---|---|
| **evidence_level 列 = 单字母分级 H/O** | **S15、S17** | 🔴 明确列语义错位（reviewer/分级字母串入 evidence_level） |
| **列数错位（行 15/16 列 ≠ 表头 14 列）** | **S14（15列）、S15（16列）** | 🔴 结构错位，需列重映射 |
| **evidence_level 列长文本污染（疑 uncertainty 串列）** | S02/S05/S06/S07/S08/S09/S10/S12/S13/S14/S18、P03（12 个） | 🟡 需抽样确认是"列串位"还是"描述式写法" |
| 列语义健康（无串列证据） | 其余 10 个体系 | ✅ |

## 三、S15 精确列映射证据（逐列对齐）

表头 14 列；数据行实际 16 列（B8 已证）。以 S15-C0001 行为例：

| 表头列(索引) | 行实际内容 | 判定 |
|---|---|---|
| claim_id(0) | S15-C0001 | ✅ 正确 |
| hypothesis_revision(1) | article-2026-6-9 | ✅ 正确 |
| statement(2) | "圆柱螺旋几何基元…" | ✅ 正确 |
| assumptions(3) | S15-A1 | ✅ 正确 |
| derivation(4) | 13_论文与成果/来源语料索引.md | ✅ 正确 |
| prediction(5)/value(6)/urel(7) | 空 | ✅ 正确（空合法） |
| run_id(8) | 09_验证结果/…/verify_ct_uft_report.txt | ✅ 正确 |
| data_id(9)/uncertainty(10) | 空 | ✅ 正确 |
| **evidence_level(11)** | **"代数恒等式"（长描述文本）** | 🔴 应为标准证据词 |
| **status(12)** | **mathematical_result（证据词）** | 🔴 evidence_level 串入 status |
| **reviewer(13)** | **H（单字母分级）** | 🔴 分级字母串入 reviewer |
| 尾缀(14) | **verified（真实状态词）** | 🔴 真实 status 落位尾缀 |
| 尾缀(15) | 空 | 多余列 |

**错位本质**：evidence_level / status / reviewer 三列内容整体右移一格 + 行尾多 2 列（verified + 空）。
**待裁定映射建议**：`evidence_level ← mathematical_result`（col12）；`status ← verified`（col14）；`reviewer ← H`（col13，需确认 H/O 语义——分级体系或审查者代号）；`代数恒等式`（col11）应归入 derivation 补充或证据说明字段。

## 四、S17 一致证据

S17（统一场论核心公式）40 行同现 `evidence_level 列单字母分级 ['H','O']`，与 S15 同族错位模式；S14 为 15 列 vs 14 表头（C0071 起 10 行）。

## 五、待裁定项（不擅自改真源）

| 项 | 待裁定内容 | 影响 |
|---|---|---|
| OPEN-B8（S15） | 列重映射方案（见上）；H/O 语义确认 | evidence_level/status/reviewer 三列纠正 |
| OPEN-B9（S14） | 15 列 vs 14 表头，尾部 10 行列错位裁断 | 结构修复 |
| OPEN-B10（S17） | 同 S15 列映射 | 结构修复 |
| 12 体系长文本 | 确认是 uncertainty 串列还是描述式写法 | 语义规范化 |

## 六、处置

- 分析证据完整、可核验（可重跑 `claims_columns_audit.py` 复现）。
- **未修改任何 claims.csv / system.json**；裁定由所属方确认后另行执行。
- 审计工具已纳入维护工具，供后续演化引擎持续自检。

## 七、守卫域B增强（后续轮次）

- `guard_all.py` 域B 新增 **status 列串列检测**：status 列值 ∈ evidence 词表 且 ∉ 合法状态词表 → WARN（`evidence_level 串入 status`）。
- 合法状态词表含 `verified/open/partial/falsified/...`，避免 `verified` 误报。
- 自测新增 2 用例：`status串列检出`、`status=verified无误报`，自测 **14/14 PASS**。
- 真实数据复跑：**PASS（4 WARN / 548 INFO），无回归**。
- **S14 新检出**：`status 列 9 处放 evidence 词 mathematical_result/methodological/numerical_result/observational/structural_claim`——S14 列语义错位三重证据坐实：
  1. 行 15 列 ≠ 表头 14 列（10 行）
  2. evidence_level 列 10 个非法词（uncertainty 污染）
  3. status 列 9 处串入 evidence 词
- OPEN-B9（S14）证据升级为「三重错位，裁定就绪」。

## 八、错位画像精确化（行级 vs 值语义）【本轮修正】

精确提取 S14/S15/S17 各行列数（区分空行与真错位行）后，修正此前笼统「列错位」归类：

| 体系 | 空行 | 真错位行（非空且列数≠表头14） | 值语义污染 | 归类 |
|---|---|---|---|---|
| **S14** | 85 | **10 行**（列15，行152-158 等：整体右移 1 列，尾缀多余列「本项目审计」） | evidence_level 长文本（uncertainty 串列）+ status 串列（methodology/observational/structural_claim 等） | **行级右移 + 值污染 混合**（OPEN-B9） |
| **S15** | 31 | **0**（非空行全 14 列） | evidence_level 列被单字母分级值污染（H） | **值语义污染，非行错位**（OPEN-B8 归类修正） |
| **S17** | 41 | **0**（非空行全 14 列） | evidence_level 列单字母分级（40 行） | **值语义污染，非行错位**（OPEN-B10 归类修正） |

- **修正要点**：
  1. S15/S17 并**无行级列数错位**——此前「列错位」归类不精确，实际是 **evidence_level 列被单字母分级值（H/O）污染**（值语义问题，非行列错位）。
  2. S14 的 10 行是**真行级右移**（从 data_id 起整体右移 1 列，尾缀多余列还原后即恢复）；其余为 evidence_level/status 值语义污染。
  3. **空行**（S14 85 / S15 31 / S17 41）为 CSV 空行格式问题，非列错位；域A 检测 `if r and len(r)!=ncols` 已排除空行，仅报真错位行。
- **修复方向（待批准后执行）**：
  - S14：10 行去掉尾缀多余列 + 从 data_id 起整体左移 1 列还原；空行清理（保留与否待所属方定）。
  - S15/S17：evidence_level 列单字母分级值 → 核对是否为 reviewer 分级右移进入，按裁决重映射。

## 九、域B status 非法词增强 + 单字母来源核验（后续轮次）

**1. 域B 新增 status 非法词检测**：status 值 ∉ STATUS_WORDS 且 ∉ evidence 词表 → WARN（`不在 STATUS_WORDS/evidence 词表，疑自定义词需规范化`）。
- 自测新增 2 用例（status非法词检出 / status合法词无误报），**自测 16/16 PASS**。
- 真实数据检出 **7 处**：
  - `unreproduced`：P03×2、S12×3（S15×6 被 KNOWN_OPEN 豁免）
  - `repaired`：S05×2、S06×3
  - `structural_failure`：S09×1
  - S14 `methodology`×1（evidence 词串列，非 status 自定义词，实为列串）

**2. 单字母来源核验（S15/S17）**：
- 两体系**所有行 reviewer 列全空** → **排除「reviewer 分级右移」假设**。
- evidence_level 单字母 O/C/H/U 为**体系自定义分级**，与 status 语义对应：`H↔verified / O↔unreviewed / C↔unreproduced-falsified / U(1 处)`。
- 分布：S15 30 行（O14/C11/H4/U1）、S17 40 行（O17/C17/H6）。

**3. 沉淀**：
- 列重映射方案书 §三 已按核验结论更新（选项 A 映射标准词 / 选项 B 纳入词表）。
- status 自定义词（unreproduced/repaired/structural_failure）待裁定：纳入 STATUS_WORDS（合理语义） or 数据规范化。

## 十、域B 长文本检测误报修正 + 12 体系长文本判断修正（后续轮次）

**实证发现**：用域B 实际阈值（>25）重查「12 体系 evidence_level 长文本污染」，发现**基本是误判**：
- evidence_level 合法词 `mathematical_result`（21 字符）及合法组合词 `mathematical_result+numerical_check`（30+ 字符）**超过长文本阈值但实为合法词**。
- 真正 >25 且非法的长文本：仅 **S14 3 行**（右移污染，uncertainty 值进入 evidence_level，真问题）。
- S02 的 3 行"长文本"实为合法组合词，uncertainty 列空为正常。

**域B 修正**：长文本检测加 `and not ok`（`len(v) > 25 and not ok`）——只报「非法 + 超长」真污染，合法词/组合词不再误报。

**验证**：
- 自测 16/16 全过（合法组合词无误报用例覆盖超长组合词）。
- 真实数据：S02 长文本误报消除；S14 3 行真污染保留（右移体系，供裁定）。

**认知修正**：此前「12 体系 evidence_level 长文本（疑 uncertainty 串列）」归类需修正——多数为合法词长度超阈值的**误报**，非真串列；仅 S14 右移污染为真长文本。
