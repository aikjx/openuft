# CHANGELOG.md · openuft 全维统一场论研究进展追踪

> **跟踪原则**：每次有实质进展（理论突破 / 实验对标 / 代码升级 / 论文版本）必追加一条
> **时间戳**：GMT+8
> **当前版本**：v4.0
> **格式**：遵循 [Keep a Changelog](https://keepachangelog.com/) + [Semantic Versioning](https://semver.org/)

---

## [Unreleased]

### Added（计划中 · v4.x）
- `P11_弯曲时空_R12/`：Schwarzschild 度规下三重奏精确证明（R12 / TS13）
- `P12_FRW_R13/`：宇宙学三重奏（R13 / TS14）
- `docs/OPEN_PROBLEMS.md`：扩展开放问题清单（与 A4 同步）
- `三重奏统一场` 子模块集成至 `70_source_code/`（ADR-008）

### Added
- **`04_公共成果/算法联盟_全维自洽与归一化/`**：全维自洽与归一化引擎（可复跑）+ 主报告 + 机器可读图谱。
  146 条核验记录（PASS 106 / BOUNDARY 33 / FAIL 7），覆盖第一性层级分级 L0–L4、
  sympy 符号求导 + mpmath 80 位精算、14 条公式量纲审计、雅可比自由度审计、
  第一性冲突探测、公设同源融合聚类（17 体系 → 6 族系）、四层归一化（符号/量纲/单位制/靶心）

### Changed
- `03_跨体系研究/comparison_matrix.csv`、`03_跨体系研究/postulate_matrix.md`：补齐遗漏的 `s13_duality_fractal_uft`；
  `p01`–`p04` 类型标注统一为 `system.json` 的 `unformulated_direction`；体系计数 16 → 17；
  增补「s13 与螺旋族」易混淆组与「第一性自洽审计已建立」结论
- `书籍/v1/` → `书籍/v1_正文/`：满足「研究目录名须含中文」的治理契约（正文无链接引用，仅自动索引受影响）

### Fixed
- **S13 溯源阻塞修复**：`system.json` 的 `source_records` 指向已不存在的 `12_研究结论/理论总纲_V1.2.md`
  → 改为现存的 `理论总纲_V1.7.md`（同步 `sources.md`、`12_研究结论/README.md`），
  此前 `verify.py` 在 identity 校验阶段即 FAIL，导致后续结构与链接检查长期未执行
- `00_项目治理/system_registry.json` 及派生视图（`TYPE_INDEX.md`、`01_独立体系/README.md`、`体系编号索引.md`）
  用 `module_catalog.py refresh` 重新生成以保持一致
- `00_项目治理/资料索引/material_catalog.md` 断链 → 用 `refresh_catalog.py` 重建（`structure_manifest.json` 同步）
- S01 8 个三重奏文档的迁移清单登记位置更新为整理后的实际位置（`12_研究结论` 3 个 / `13_论文与成果` 5 个），
  `migration_check` 的 Lost localized file 告警清零
- 结果：`python -B verify.py` 由 FAIL（identity 阻塞 + 9 项）转为 **PASS**（17 体系 / 4685 本地链接 / 快照 193+393）

### Conflict Registration（第一性冲突物理登记 · 2026-09-15）
- **普朗克锚定谬误（M01/M02）**：在 S07/S08/S09/S10 各建 `11_证伪与反例/普朗克锚定谬误冲突记录.md`，
  并在各自 `postulates.md` 加「第一性冲突登记」节；`claims.csv` 追加 S07-C0001 / S08-C0001+C0002 / S09-C0001 / S10-C0001（`falsified` 7 行登记）
- **统一动量低速极限（M03）**：在 S02/S12 各建 `11_证伪与反例/统一动量低速极限冲突记录.md`，
  `postulates.md` 加 §6/§7（S12 本体 `v≡c` 与借用动力学 S12-A4 的接口未定义）；
  `claims.csv` 追加 S02-C0001 / S12-C0006（`falsified`）
- 登记脚本（幂等、`hypothesis_revision` 自动读）：`04_公共成果/算法联盟_全维自洽与归一化/源码/登记冲突到体系.py`
- **派生链修正与重算**：`源码/普朗克锚定谬误_修正与派生链重算.py`（mpmath 80 位）——
  旧链 `G_old(m)=ℏc/m²` 对 9 粒子中 8 个 FAIL、仅 `m=m_P` PASS，偏离闭式 `G_old/G=(m_P/m)²` 机器零（跨度 5.71e+44）；
  修正式 `α_grav=Gm²/(ℏc)=(m/m_P)²` 全粒子机器零；修正后几何链 27 检自洽全 PASS；
  诚实标注修正后仍缺 G 外部输入、α 测量锚、质量层级 3 项残留（自由度仍为 2）
- **S13 β 函数符号约定**：`S13/02_基础公设/postulates.md` 的 S13-A3 补注 ε 符号约定（对应 `d=4+ε`，与 `d=4−ε` 主流仅差符号，物理等价）

### Reorg（研究规范与视图层 · 2026-09-15）
- **`02_共享基础/研究规范/method_F_第一性判据.md`**（新增）：无量化判据、循环检测（雅可比秩 + 恒等变形 + 测量噪声伪装）、
  双锚点检验、自由度审计、L3 门槛，含「普朗克锚定谬误」标志案例与诚实边界；已接入 `研究规范/README.md` 方法库
- **`03_跨体系研究/GAQ谱系版本序列比对.md`**（新增）：S03(v1)→S07(v4)→S08(v5)→S09(v6) 版本差异比对、共同根因、共同盲区、管理建议
- 循环检测门禁已沉淀为 `method_F`，作为 claims 登记 `verified` 前的通用判据

### Next-step Closure（P2/P3 · 2026-09-15）
- **P03 立项评估**：`01_独立体系/P03_规范对称统一候选/00_研究立项/立项评估.md` 新写——
  结论「建议立项（中优先级）」；理由：规范对称统一是四力统一标准路径，且**不受 M02 普朗克锚定根因影响**（走群论+表示论，不依赖 c/ħ 几何化）；
  必答题：选定群 G / 破缺链 / 费米子表示 / 耦合常数跑动复现；不得继承已标 falsified 的 GAQ 派生链
- **电子 EDM L3 跟踪**：主报告第十二节建立唯一 L3 产出跟踪表——
  `d_e = eαR_C/(2√(1+α²)) = 2.257e-34 C·m`（B 级框架映射）低于 ACME 上限 `8.7e-34`（90% CL），仍被允许；
  排除阈值 `d_e < 1e-36` 则 ZUFT 螺旋 EDM 模型被排除；该预言不依赖 M02 谱系，恰印证 `method_F` 的 L3 门槛
- 至此用户任务「全维分析 / 整理 / 第一性原理自洽 / 精算验证 / 融合 / 归一化」及报告所列 P0–P3 后续项全部闭环

### Normalization Closure（融合收口 · 第十三节 · 2026-09-15）
- **全仓库第一性健康度归一化总览**：`源码/体系健康度归一化总览.py`（可复跑，C 级从各体系 `claims.csv` 的 `falsified` 自动提取）
  产出 `数据/体系第一性健康度总览.md` + `.json`。17 体系归一到统一坐标系 H/O/C/U：
  **C=6**（s02/s07/s08/s09/s10/s12，已证伪登记）· **O=5**（s03 母体 + s04/s05/s06 依赖 GAQ_v3 + s11 借用几何）· **H=2**（s01 数学框架 / s13 唯一健康候选）· **U=4**（p01–p04 占位，p03 已立项评估）
- 主报告第十三节「融合收口」：把 H/O/C/U 落到决策含义（重点投入 / 须隔离 / 须修根因 / 立项或归档），并指明 S13+EDM 是仓库当前唯一可信第一性参照系，O 级须先与 M02 谱系隔离才能独立审查
- 本轮主线（全维分析→整理→第一性自洽→精算验证→融合→归一化）最终交付 = 一张可复跑、可追责的第一性地图，杜绝「多项精算通过即成立」虚假确信（H01c 机制）

### O 级体系 M02 谱系隔离审查（第十四节 · 2026-09-15）
- 对 O 级 5 体系（s03/s04/s05/s06/s11）做「剥离 M02 谱系后是否自身自洽」的隔离审查：`源码/O级体系_隔离审查.py`（Fraction 精确量纲 + mpmath 60 位），产出 `数据/O级体系隔离审查.md` + `.json`；11 项检查：FAIL 5 / BOUNDARY 2 / L1 2 / L0 1 / PASS 1
- **新发现 2 处独立于 M02 的真实缺陷**：① **s05** 定理 H2 `R₁₁=(ħ/2π)^(1/3)·G^(1/3)·c^(-2/3)` 量纲为 `L·T^(-1/3)`（非长度），实算 `2.318570e-21 m` 与 `L_p=1.616255e-35 m` 差 `1.4345e14` 倍；定理 H3 数值错（实算 `2.2529e19` vs 原文 `3.18e19 GeV`）。② **s06** `Cl(4,4)⊗ℂ` 代数同构错（应 `≅M₁₆(ℂ)`，维数 256；原文 `M₈⊕M₈`=128），精算表维数 `2⁴·2=32` 与定义 4 的 128 及真实 256 三者自相矛盾
- 已登记 `S05-C0001`/`S05-C0002`、`S06-C0001`/`S06-C0002`（各体系 `claims.csv` falsified）+ 建 `11_证伪与反例/HDU紧致化半径公式缺陷记录.md`、`TCL代数维数错误记录.md` + 两体系 `postulates.md` 加 §5 冲突节 + 精算表状态改「已证伪」
- 另 3 体系：**s03** 为 L0 同义反复 + L1 概念循环（「100% 数值与量纲验证通过」实为 H01c 循环自证）、**s04** I1 为恒等重述、**s11** 非标准式 `Q/M=√(4πε₀G)` **原文 8.1 节已诚实标注**（OPEN-2）→ 属已披露欠定
- 归一化总览重跑更新：**C=8 · O=3 · H=2 · U=4**（s05/s06 由 O 升为 C）；主报告第十四节收口

### 全维完成：17 体系统一第一性审查（第十五节 · 2026-09-15）
- 把统一口径第一性审查覆盖全部 17 体系：新增 `源码/全维体系_第一性审查.py`（claim 统计 + 列数一致性），重写 `体系健康度归一化总览.py`（鲁棒读取 + 审计冲突白名单），产出 `数据/全维第一性审查总表.md` + `.json`
- **全维评级**：C=8 · O=3 · H=2 · U=4；**第一性层级**：L0（s01 三重奏 / s13 流守恒·霍普夫荷）、L1（s03/s04/s11）、L2（s13 曲率闭式/希格斯谱）、**L3 全仓库仅 2 处**（电子 EDM + S13 四预言 conjecture）
- **重要修正（鲁棒读取）**：s13 的 `S13-C0005`(falsified，体系自我记录并已修复) 曾被固定列号读取静默跳过；改用「按行末两列定位 status」+「审计冲突白名单」后正确识别，并按「诚实治理 ≠ 未修复冲突」原则不计入 C（保持 s13 为 H）
- **新发现 2 处 claims.csv 数据质量告警**：s12（rows=[11,12]）、s13（rows=[10,11,17]，`statement` 含未转义逗号 `[0,0,0,8]` 致列错位）；原始文件保留不改（治理原则），仅报告 + 建议修复
- 报告第十五节收口；复跑方式补全 6 个脚本

---

## [4.1.0] - 2026-09-12 — 新增 S13 全域双向分形统一场论体系

### Added
- **`S13_全域双向分形统一场论/`**（`s13_duality_fractal_uft`，candidate_theory）：三公理（对偶 0/1、守恒 Q∈Z、双向分形自相似）撑起六方程闭环 M1–M6；真空约束 |Ψ|²=v² 使对偶旋量即希格斯对偶，电弱规范结构自涌现
- **完整生命周期归档**：00_研究立项 → 15_版本发布（含 90_历史归档）17 阶段齐全；公设（postulates.md）、方程（equations.md）、推导（derivations.md）、一致性（consistency.md）、预言（predictions.md）、诚实边界（诚实边界.md）、证伪记录（绕数证伪记录.md）
- **验证证据链**：6 个可复现脚本（verify_unified_theory / diagnose_winding / hopf_verify / hopf_control / higgs_verify / dimension_unify_verify）入 `07_计算复现/源码`，实跑通过（流守恒 2.1e-13、曲率闭式 2.9142135624、希格斯谱 {0,0,0,8}、未破缺 U(1) 零空间维数 1）
- **书稿**：20 章 + 双附录（约 4.9 万字）入 `13_论文与成果/书稿/`；总纲 V1.2（U=58%）入 `12_研究结论`；验证精算报告 V1.2 入 `09_验证结果`
- **证据登记**：`claims.csv` 6 条（3 数学结果 + 1 数值检查 + 1 已证伪 + 1 推测）；`system.json` 登记三公设

### Fixed
- `S02_空间光速螺旋统一力/04_理论推导/偏振与螺旋辨析总览.md`：断链 `../../system.json` → `../system.json`
### Known（历史遗留，非本次引入）
- ~~`S01_螺旋三重奏与谱几何/` 8 个三重奏文档在 20260909 中文目录迁移后又被移入 `12_研究结论`/13_论文与成果 子目录，未补迁移记录，`migration_check` 报 Lost localized file；文件实际均在，不影响使用~~
  **已于 2026-09-15 修复**：迁移清单登记位置已更新为实际位置，告警清零（见 [Unreleased] → Fixed）

---

## [4.0.3] - 2026-09-07 10:03 — 事故恢复 + 目录大小写 git 化修正

### Fixed（关键恢复）
- **事故**：误删 `openUFT/` 目录（Windows 大小写不敏感导致 `openUFT` 与 `openuft` 实为同一物理目录，`rm -rf openUFT` 误删全部）
- **恢复**：`git restore openUFT/` 从 git HEAD（提交 e8945964）完整恢复 93 文件
- **重建**：`99_inbox_future/` 下 10 个开放问题子目录（空目录不被 git 跟踪，恢复后丢失，已用 README 占位重建）
- **验证**：`python verify.py` 36/36 通过

### Changed（目录大小写正确处理）
- **git mv 两步法**：`openUFT/` → `openuft_tmp/` → `openuft/`（配合 `core.ignorecase=false`）
- git 记录中路径从 `openUFT/` 正确变更为 `openuft/`（rename 记录 R 全部就位）
- 物理目录与 git 索引路径统一为小写 `openuft/`

### 教训（ADR-011 记录）
- **Windows 文件系统大小写不敏感**：`openUFT` ≡ `openuft`（同一物理目录），绝不可当作两个目录处理
- 删除任何目录前必须先 `git status` 确认，且用 `git rm` 而非 `rm -rf`
- 空目录不被 git 跟踪 → 需用 `.gitkeep` 或 README 占位

---

## [4.0.2] - 2026-09-06 23:57 — 目录小写化

### Changed（核心变更）
- **目录名**：`openUFT/` → **`openuft/`**（小写，对齐 GitHub URL `github.com/aikjx/openuft.git`）
- **批量替换**：所有 `.md` / `.py` / `.cff` / `LICENSE` 文件中的 `openUFT` 字面改为 `openuft`（71 处）
- **URL 同步**：`github.com/aikjx/openUFT` → `github.com/aikjx/openuft`（所有文件）
- **Python 缓存清理**：删除全部 `__pycache__/`（防 .pyc 文件残留旧名）

### Constraint Note
- 旧目录 `openUFT/` 因 Windows 进程锁定（`WinError 5` Permission Denied）**无法自动删除**
- **用户需手动删除**（详见 `openuft_小写化报告.md` 操作步骤）
- 旧目录 `openUFT_改名与全维整理优化报告.md` 等历史报告文件保留（工作记录）

### Fixed
- verify.py 重跑保持 36/36 通过
- 0 处 `openUFT` 字面残留
- 0 处旧 URL 残留

### 验收
- ✅ `python verify.py` 36/36 通过
- ✅ Markdown: 79 篇
- ✅ Python: 11 个
- ✅ 总文件: 93 · 1.3 MB

---

## [4.0.1] - 2026-09-06 22:34 — 全维整理优化 v2（求导·证明·验证·精算）

### Changed（核心变更）
- **作者统一切换**：`莫国子 / Guozi Mo / AI科技星` → **AI科技星**
  - 60+ 文件批量替换
  - LICENSE / CITATION.cff / README.md / docs 全部更新
  - 组织名保留「AI科技星」作为方法论传承
- **`00_index/全维分析报告.md`** 新建（10 节 · 整合 D/P/V/A 四主轴一张总表）

### Added
- **`00_index/全维分析报告.md`** ★ 全项目一表总览（10 节）
- **`docs/DESIGN_DECISIONS.md` ADR-009**：作者署名切换决策记录
- **`verify.py`** 白名单扩展（识别「全维分析报告.md」的历史叙述提及）

### Fixed
- README 顶部：`项目代号` → `作者：AI科技星`
- README 末尾：补充「八、关于作者」独立小节

### 验证状态
- ✅ verify.py：36/36 通过
- ✅ Markdown：74 篇
- ✅ AI科技星署名：72 处
- ✅ 历史叙述提及：4 处（合法）

---

## [4.0.0] - 2026-09-06 ★ 当前首发版

### Added（首次完整发布）
- **项目改名**：`alg_uft_unified/` → `openuft/` （ADR-001）
- **顶层入口文档（11 件）**：
  - `README.md` · 项目入口
  - `INDEX.md` · 文件索引
  - `CHANGELOG.md` · 本文件
  - `MIGRATION_GUIDE.md` · 迁移指南
  - `WORKFLOW.md` · 工作流
  - **`ROADMAP.md`** · 18 个月路线图
  - **`FAQ.md`** · 50 个常见问题
  - **`QUICKSTART.md`** · 5 分钟上手
  - **`CONTRIBUTING.md`** · 贡献指南（5 步流程）
  - **`LICENSE`** · MIT
  - **`.gitignore`** · Python / Node / OS / Editor
  - **`CITATION.cff`** · 学术引用规范
- **二级目录索引（17 件）**：
  - `00_index/定理谱系总表.md` · TS1-TS12 总览
  - `02_共享基础/研究规范/审计方法/A4_诚实声明与开放问题/开放问题清单_L0-L2.md` · O-1 ~ O-12 详细描述
  - `P3_归纳闭合_R9/README.md` · R9 ★ 重点
  - `P4_绝热三重奏_R10/README.md` · R10 ★ 重点
  - `P5_梯度磁场精确性_R11/README.md` · R11 ★ 重点
  - `99_inbox_future/README.md` · 无限扩展机制
  - `12 个一级目录 README` · 每个主轴的子说明
- **docs/ 文档库（8 件）**：
  - `docs/README.md` · docs 子目录总览
  - `docs/GLOSSARY.md` · 术语表
  - `docs/THEOREMS.md` · 12 定理详细展开
  - `docs/EXPERIMENTAL_CROSS_VALIDATION.md` · 48 项验证矩阵
  - `docs/OPEN_PROBLEMS.md` · 与 A4 同步
  - `docs/MATHEMATICS.md` · 数学结构
  - `docs/NUMERICAL_METHODS.md` · 数值方法
  - `docs/BIBLIOGRAPHY.md` · 完整参考文献
  - `docs/DESIGN_DECISIONS.md` · 8 项架构决策 (ADR-001 ~ ADR-008)
- **GitHub 模板（4 件）**：
  - `.github/ISSUE_TEMPLATE/bug_report.md`
  - `.github/ISSUE_TEMPLATE/feature_request.md`
  - `.github/ISSUE_TEMPLATE/question.md`
  - `.github/PULL_REQUEST_TEMPLATE.md`
- **验证脚本**：`verify.py`（一键检查 36 项可验证项）
- **55 篇历史文档**完整迁移

### Changed（结构改造）
- **目录架构**：12 一级目录 + 66 二级目录 + 80+ 三级文件
- **4 方法主轴**清晰：求导 D + 证明 P + 验证 V + 精算 A

### Deprecated
- `alg_uft_unified/` 命名（已废弃，全文替换为 openuft）

### Removed
- 无

### Fixed
- 无（首次发布无需 fix 历史）

### Security
- 无已知安全问题

---

## [4.0-pre] - 2026-09-06 21:48 — 方法分层骨架完成

### Added（内部骨架）
- `openuft/` 项目根目录建立（原 `alg_uft_unified/`）
- **12 个一级目录**（按"求导·证明·验证·精算"四方法主轴 + 物理领域 + 应用 + 代码 + 可视化 + 论文 + 历史 + 未来扩展）
- **50+ 个二级目录**（每个一级目录下展开）
- **顶层核心文档（初始）**：README.md / INDEX.md / CHANGELOG.md / MIGRATION_GUIDE.md / WORKFLOW.md

---

## [3.x] - 历史档案（详见 `95_history_archive/`）

### [3.6.0] - 2026-07-31 — 质量谱几何化
- GAQ-UFT v6：三代费米子 Cl(4,4) 分类

### [3.5.0] - 2026-07-31 — cħ 几何化
- GAQ-UFT v5：c 与 ħ 的几何化

### [3.4.0] - 2026-07-30 — 全维统一
- GAQ-UFT v4：全维统一顶尖论文

### [3.3.0] - 2026-07-29 — 三大新体系
- GAQ-UFT v3：三大新体系（连续积分、Clifford 几何、分形-类分形）

### [3.0.0] - 2026-07-29 — 三大新体系完整

### [2.0.0] - 2026-06-15 — 前端 README（已退役）

---

## 版本对照表

| 版本 | 日期 | 代号 | 主要变化 |
|---|---|---|---|
| 4.0.0 | 2026-09-06 | **正式首发版** | 项目改名 + 全维整理优化 |
| 4.0-pre | 2026-09-06 | 方法分层骨架 | 内部骨架阶段 |
| 3.6.0 | 2026-07-31 | 质量谱 | Cl(4,4) 分类 |
| 3.5.0 | 2026-07-31 | cħ 几何化 | c 与 ħ 几何化 |
| 3.4.0 | 2026-07-30 | 全维统一 | 顶尖论文 |
| 3.3.0 | 2026-07-29 | 三大新体系 | 完整版 |
| 3.0.0 | 2026-07-29 | 三大新体系 | 初版 |
| 2.0.0 | 2026-06-15 | 前端 README | 已退役 |
| 1.x | 2026-06 前 | 内部研发 | 个人探索 |

— AI科技星 · 2026-09-06
