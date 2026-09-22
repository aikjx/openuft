# -*- coding: utf-8 -*-
"""生成实现方式档案、关系图谱与交互式关系图。

档案内容来自对仓库内实际代码与报告的逐项勘察；凡结论标记为 disputed / falsified
者，一律保留负面记录，不因进入统一层而改变。
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LAYER = ROOT / '06_统一体系层'
DOSSIER = LAYER / '实现方式总览' / '实现方式档案'

DOSSIERS = {}

DOSSIERS['TUFT主线.md'] = '''# 实现方式档案：TUFT 主线 v2–v18

[实现方式总览](../README.md) · 归属体系：[s14 挠率统一场论 TUFT](../../../01_独立体系/S14_挠率统一场论TUFT/README.md)

- **形态**：M1 符号推导 · M2 数值精算 · M3 谱方法与打靶 · M6 书稿
- **位置**：仓库根 `tuft_v*.py`、`tuft_v*_out.txt`、`TUFT_*.md`、`_ma_v*_*.py`
- **状态**：active，主线在研

## 主线做了什么

以 `v_total=c` 为唯一公设，把曲率 K 与挠率 T 作为几何两分量，主张挠率内禀代数承载 U(1)×SU(2)×SU(3)。版本线 v2（2026-09-16）至 v18（2026-09-18，在研），每期配 `_out.txt` 运行报告与独立审计裁决文档。

工作流编号说明：`line1/line2/line3` 是**每期内部重排**的编号，不是固定的三条推论链。真正连续的主轴是 line1（强场与 QNM）。

## 关键转折

- v6 用 WKB 估谱 → v7 首试 Leaver 连续分数法
- v9–v12 转向"先证明引擎能复现已知答案"：GR Schwarzschild QNM 标量/引力双通道达 13–15 位（`tuft_v12_line1_rw_out.txt`，GATE: PASS）
- v13/v14 双向打靶找 TUFT 壁谱，**两次均被证明在 GR 上就不收敛**
- v15 范式转换：放弃复极点，改走实频散射相位
- v16 发现 |R_TUFT|²≡1，所谓"0.90 反射峰"不存在
- v17 坐标纠错：odd 势必须用面积半径 R=ρ√B，结论翻转为"外垒与 GR 几乎相同，差异只在内边界"

## 诚实评级

**算过且站得住**：GR QNM 双通道 13–15 位复现；`|R_TUFT|²−1 ≤ 4.4e−16` 全频；无高 Q 壁腔窄谱；几何壁垒 r_h=0.6099/0.7071M、ISCO 4.9491M、b_crit 5.1928M。

**已推翻或勘误（23 条）**：C_k 三代、"Leaver PASS"（实为查表冒充）、2L 几何回波、v13 六个壁频、v14 两个外推根、0.90 Lorentzian 反射率峰、E399/E400 隧穿率（坐标错）、Hz 换算漏 2π。

**仍 OPEN**：TUFT 反射壁渐近复谱（连续五期未闭合）、回波模板 SNR、C18 可观测性——v17 后已从"TUFT 独有"降级为 ECO 通用判据。

**常数预言：没有。** α 在 v2 规格中为外部标定输入，主册明写"几何给不了 1/137"。三代质量与 mass hierarchy 双否决。

## 与体系的关系

本档案是 s14 的**主力实现**。s14 的 `claims.csv` 已登记多项 falsified，与本档案一致。两者不可互提证据等级。

## 建议保留的核心文件

`TUFT_企业级归一化主册_v1.0.md`（SSOT）、`TUFT_归一化台账_v1.0.json`、`TUFT_v2.0_企业级规格.md`、`tuft_v2_verify.py`、`tuft_v4_line2_geodesic.py`、`tuft_v7_line2_c_deriv.py`、`tuft_v9_line1_leaver.py`、`tuft_v10_line1_scalar.py`、`tuft_v12_line1_rw.py`、`tuft_v13/v14_tuft_wall.py`（负面结果存档）、`tuft_v16_gr_reflection.py`、`tuft_v17_odd_potential.py`、`_ma_v13/v14/v16/v17_*`（审计代码）。

调试产物（`_diag_*.py`、`_probe_v14*.py`、`_proto_*.py`、`_ricc*.py` 等）建议归档，其数字禁止引用。
'''

DOSSIERS['TUFT原始工作区.md'] = '''# 实现方式档案：TUFT 原始工作区

[实现方式总览](../README.md) · 归属体系：[s14](../../../01_独立体系/S14_挠率统一场论TUFT/README.md)

- **形态**：M2 数值精算 · M6 书稿
- **位置**：`tuft/`（175 文件 / 2.4 MB，扁平无子目录）
- **状态**：archived（内容已迁入 s14 体系目录）

## 内容

`tuft_r1`–`tuft_r25`、`tuft_Q量子A/B`、`tuft_B_*`、`tuft_D2/D3`、`tuft_O_SCALE` 等成对出现的「.py + _report.txt + .md 文稿」。入口为 `tuft_总索引.md` / `tuft_总索引.py`、`tuft_全书_交付版.md`、`tuft_全景总报告.md`、`tuft_第一性归一化总览.{py,md,json}`、`tuft_判据门禁.py`。

依赖 numpy / scipy / mpmath（另见 `emd_out.log` 涉及 sympy）。

关键词：挠率、结与链环、陈–西蒙斯对偶、三叶结 SU(3) 表示、QNM/ringdown/echo、机电对偶压电实验。

## 与主线 v2–v18 的区别

这是**原始工作区**，编号体系（r1–r25）与主线（v2–v18）不同。主线是后来的规范化产物，带独立审计裁决与本仓可校验的台账。两者不可直接对号入座。

## 使用提醒

状态为 archived：保留供溯源，**结论不自动转移**到 s14 或主线。引用本工作区的数值前，需确认主线是否已复算或勘误。
'''

DOSSIERS['全域双向分形S13.md'] = '''# 实现方式档案：全域双向分形统一场论（S13）

[实现方式总览](../README.md) · 归属体系：[s13](../../../01_独立体系/S13_全域双向分形统一场论/README.md)

- **形态**：M1 符号推导 · M2 数值精算 · M6 书稿
- **位置**：`01_独立体系/S13_全域双向分形统一场论/`
- **状态**：active

## 三公理与六方程闭环

| 公设 | 内容 | 数学 |
|---|---|---|
| A1 对偶 | 世界由不可再分基元 0 与 1 张成；物理量以对偶对 (a, ā) 存在 | D² = 1 |
| A2 守恒 | 基本拓扑荷为整数，最小单位 ±1，严格守恒 | Q ∈ ℤ，min\\|Q\\|=1 |
| A3 自相似 | 一切尺度双向分形，无尺度断点，只有重整化不动点 | β(−g)=−β(g)；g\\*=±√(ε/c) |

六方程闭环 M1–M6：

- **M1** 约束旋量方程 `σ^μ∂_μΨ = λΘΨ* + iζΨ`，真空约束 `|Ψ|²=v²`
- **M2** 涌现规范场 `a_μ=(i/2)(Ψ̂†∂_μΨ̂−∂_μΨ̂†Ψ̂)`，`A_μ=E†∂_μE`，`E=(Ψ̂,ΘΨ̂*)∈U(2)`
- **M3** Hopf 拓扑荷 `Q_H=(1/4π²)∫ε^{ijk}a_i∂_ja_k d³x ∈ ℤ`
- **M4** 双向 β 流 `β(−g)=−β(g)`
- **M5** 对偶镜像度规 `g_eff(r)=g_eff(ℓ²/r)`
- **M6** 因果畴通量

真空约束使对偶旋量即希格斯对偶，电弱规范结构从阴阳对偶几何自涌现。

## 诚实边界

- **1D 绕数已证伪**（π₁(S²)=0），已改 3D Hopf（π₃(S²)=ℤ）并如实记录。
- 电弱候选 `sin²θ_W=1/4` 与实验 0.231 差约 5.4%，为负面结果，已记录。
- 代数自洽已精算；**公设无失效阈值**，当前只能作 conjecture 登记。
- 该体系是全部体系中唯一在 `claims.csv` 登记 `verified` 条目的体系，该证据**不得因"都用几何语言"转移给螺旋族**。
'''

DOSSIERS['全域统一场论书稿.md'] = '''# 实现方式档案：全域统一场论书稿

[实现方式总览](../README.md) · 归属体系：[s13](../../../01_独立体系/S13_全域双向分形统一场论/README.md)

- **形态**：M6 书稿
- **位置**：`全域统一场论_书稿/`（`outline.md`、`chapter-ledger.md`、`manuscript/ch01`–`ch25` 与附录）
- **状态**：active

## 内容

s13 的长篇书稿形式。可见章节包括 `ch03-第二三公理.md`、`ch04-河图洛书.md`、`ch05-旋量对偶方程.md`、`ch07-霍普夫拓扑荷.md`。

配套精算与审校材料在仓库根：`全域统一场论_TUFT全维求导验证.py`、`全域统一场论_TUFT全维求导验证与异常修复报告.md`、`全域统一场论_TUFT实验预言白皮书_优化版.md`、`全域统一场论_TUFT拓扑统一场论_汤川势与电磁挠率章_修复版.md`、`全域统一场论_TUFT续篇_全维审校与异常报告.md`、`全域统一场论_理论总纲与体系总结.md`。

## 命名陷阱

这批文件虽带"TUFT"字样，但本体是**阴阳对偶旋量 + Hopf 纤维丛的六方程闭环**，与 s14 挠率统一场论是**两条不同的理论**。文件命名把两者混在了一起。

按 [术语消歧](../../跨体系翻译表/术语翻译表.md)：本档案归属 s13，不归属 s14。引用其中结论前必须先确认该段落讨论的是哪一条 L1 本体。

## 提醒

书稿篇幅不构成证据（八层 T3）。见 [实现方式总览](../README.md) 使用纪律。
'''

DOSSIERS['GAQ谱系.md'] = '''# 实现方式档案：GAQ 谱系 v1→v6

[实现方式总览](../README.md) · 归属体系：[s03](../../../01_独立体系/S03_GAQ几何原子与作用量子/README.md) [s07](../../../01_独立体系/S07_GAQ复曲率融合体系/README.md) [s08](../../../01_独立体系/S08_GAQ常数几何化体系/README.md) [s09](../../../01_独立体系/S09_GAQ粒子质量谱体系/README.md)

- **形态**：M1 符号推导 · M2 数值精算 · M6 论文
- **位置**：`02_共享基础/公共计算/源码/`（`gaq_uft_*.py` 系列）、`90_历史归档/历史资料/几何原子统一场论/`
- **状态**：active

## 版本线

| 版本 | 体系 | 关键变化 |
|---|---|---|
| v1 | s03 几何原子 | 离散几何元胞、作用量子化、曲率—能量对应 |
| v3 | s04/s05/s06 分支 | 拆出 IEG 信息熵引力、HDU 高维紧致化、TCL 拓扑手征锁定 |
| v4 | s07 复曲率 | 复曲率 Ξ=κ+iτ；c、ħ、e 为三条公理常数 |
| v5 | s08 常数几何化 | c、ħ 降为几何桥梁，e 降为导出量 |
| v6 | s09 质量谱 | 代结构、质量比、Yukawa/QCD 几何化 |

## 关键差异（易混淆点）

s07 与 s08 是**同一复曲率本体**，差异在 c/ħ/e 的地位：v4 为公理常数，v5 降为几何桥梁。这是版本演进而非独立体系。

s06 与 s09 都用 `π₃(SU(3))×ℤ₂^chiral=6`，但 s06 用 Cl(4,4) 边界态、s09 用 SO(3) 本征方向——同谱系不同阐述。

## 诚实评级

GAQ 谱系是**版本演进重灾区**：公设地位逐版变化，按原始假设各自归属，不得假设版本间公设"完全相同"（见 [跨体系公设矩阵](../../../03_跨体系研究/postulate_matrix.md)）。

主要脚本：`gaq_uft_verification.py`、`gaq_uft_strict_proof.py`、`gaq_uft_v3_three_systems.py`、`gaq_uft_v4_unified.py`、`gaq_uft_v5_full_geo.py`、`gaq_uft_v6_mass_spectrum.py`、`gaq_uft_precision_compare.py`、`gaq_uft_unsolved_mysteries.py`。
'''

DOSSIERS['GAQ成书.md'] = '''# 实现方式档案：GAQ-UFT 成书

[实现方式总览](../README.md) · 归属体系：[s03](../../../01_独立体系/S03_GAQ几何原子与作用量子/README.md) [s07](../../../01_独立体系/S07_GAQ复曲率融合体系/README.md) [s08](../../../01_独立体系/S08_GAQ常数几何化体系/README.md) [s09](../../../01_独立体系/S09_GAQ粒子质量谱体系/README.md)

- **形态**：M6 书稿
- **位置**：`GAQ-UFT_Complete_Book/`（68 文件 / 0.5 MB）
- **状态**：active

## 内容

书名原文：**GAQ-UFT《万物几何统一场论——全维分析与第一性原理推导》**（Geometric-Axiomatic Quantum Unified-Field Theory），约 102 万字，7 卷：

1. Foundations
2. Geometric_Vacuum
3. Constant_Geometry_Origins
4. Particle_Spectra
5. Lorentz_Spacetime_Extension
6. Prediction_Falsification
7. Open_Problems

入口 `main_book.md`、`preface.md`，编译 `compile_book.bat|sh`（pandoc + XeLaTeX）。数值验证 `frenet_high_prec.py`、`geometry_verify.py`、`koide_simulation.py`（mpmath 200 位）。

## 值得肯定的做法

书中明确声明："书中标注的'猜想''开放问题'章节不代表已证实结论"，并单列 Prediction_Falsification 与 Open_Problems 两卷。这是本仓库中**诚实分级做得较好的一份实现**。

## 与谱系的关系

是 [GAQ 谱系](GAQ谱系.md) 的成书版，对应 s03/s07/s08/s09，**不是新的独立体系**。引用时须注明对应版本。
'''

DOSSIERS['空间光速螺旋族.md'] = '''# 实现方式档案：空间光速螺旋族展示层

[实现方式总览](../README.md) · 归属体系：[s02](../../../01_独立体系/S02_空间光速螺旋统一力/README.md) [s10](../../../01_独立体系/S10_频率本源与复螺旋宇宙/README.md) [s12](../../../01_独立体系/S12_空间光速螺旋统一体系/README.md)

- **形态**：M2 数值 · M7 可视化
- **位置**：`unified-field-theory/`、`unified-field-theory-full/`、`tan_arctan_unified_field/`、`utf_visualization/`、`可视化/`
- **状态**：active

## 内容

| 位置 | 形式 | 核心句 |
|---|---|---|
| `unified-field-theory/` | 单页 HTML（15 文件 / 5.2 MB） | 「空间光速螺旋量子几何统一场论」；α = tan θ = τ/κ = 0.0072973525693 |
| `unified-field-theory-full/` | 单页 HTML 九卷完整版 | 两公理：c 是空间内禀属性；螺旋自相似/尺度不变 |
| `tan_arctan_unified_field/` | 单页 HTML | 正切与反正切在螺旋几何中的地位（α=tanθ 支） |
| `utf_visualization/` | 静态站（19 文件） | 核心方程、四力、垂直原理、UFO 原理等分栏 |
| `可视化/` | 单页 HTML | 螺旋运动引力生成机制静态配图 |

四力来源图：κ 梯度→引力、τ 场→电磁、κ&τ 紧致化→强力、κ&τ 对称破缺→弱力。含 15.092 GHz + 251.6 T 人工引力实验方案。

## 归属判定（重要）

这三个目录是**展示层**，本体分别落在 s02（统一力动力学，无几何本体）、s10（振动/频率本体，c 为上限 v≤c）、s12（空间光速螺旋本体，c 为恒等约束 v≡c）三个**互不认证**的体系上。

展示层共用同一套视觉语言与"α=tanθ"公式，但**不能据此认为三个体系可以合并**。见 [术语消歧](../../跨体系翻译表/术语翻译表.md)「螺旋」条目。

## 提醒

单页 HTML 的完整性不构成证据（八层 T3）。其中 α=τ/κ 的赋值关系需回到对应体系的 `claims.csv` 核对证据等级。
'''

DOSSIERS['全域数学UM.md'] = '''# 实现方式档案：全域数学统一场论（UM）

[实现方式总览](../README.md) · 归属体系：**候登记**（未取得稳定编号）

- **形态**：M1 符号推导 · M6 论文
- **位置**：`uft/06-论文/全域数学统一场论-完整论文.md`（5.9 KB）；同源目录 `uft/01-核心公理/`、`uft/arxiv/`（main.tex + Makefile + build_package.py）
- **状态**：candidate

## 主张

**全域数学（Universal Mathematics, UM）**：自定义完备公理系统，核心思想是"整个物理世界仅由空间自身的几何属性决定"。从 3 个第一性本源参数——光速 c、空间本征曲率 κ、空间本征挠率 τ——出发，声称推导全部基本物理常数、实现四力几何统一，并建立易经符号系统与量子物理的同构、意识科学的高维拓扑理论。

配套：32 维超复数、O9 场方程。已做 arXiv 投稿打包。

## 诚实评级（重要）

论文顶部自印「算法联盟 ROOT 级权限认证 ✅ 通过 / 本源级（最高级别）」，并称"与 CODATA 2022 标准值误差均小于 10⁻⁵%"。

按本仓库纪律：**自印认证横幅不构成审查**（见 [实现方式总览](../README.md) 使用纪律 2）。在无独立复跑脚本、无失败明细、无第三方评审记录的情况下，本实现一律按 `conjecture` 登记。

"误差小于 10⁻⁵%"若来自用 CODATA 值反解本源参数再回算，属**循环拟合**，不构成预测验证。

## 待办

- 裁定是否登记为独立体系（路线图 B5）
- 若登记：迁移原文至体系目录，补齐 17 阶段与 `system.json`（见 [接口约定](../../体系接口约定/统一接口约定.md)）
- 核对 `uft` 与 `utf` 的同源关系（两者含同名 `01-核心公理`、`02-易经科学证明`，uft 是 utf 的较晚精简/审计版）
'''

DOSSIERS['三分量统一场论库.md'] = '''# 实现方式档案：三分量统一场论库（triad_uft）

[实现方式总览](../README.md) · 归属体系：**跨体系代码库**（触及 s01、s02、s12 等）

- **形态**：M5 代码库
- **位置**：`triad_uft/`（25 文件，含 v4.0.0 / v5.0.0 / v5.1.0 发布包）
- **状态**：active

## 内容

本仓库中**唯一形态完整的 Python 包**，21 个模块：

`triad.py`、`geometry.py`、`lorentz.py`、`constants.py`、`particle_masses.py`、`cosmology_deep.py`、`quantization.py`、`grand_unification.py`、`theorem_system.py`、`provenance.py`、`strong_force.py`、`weak_force.py`、`nuclear.py`、`curved_spacetime.py`、`artificial_field.py`、`artificial_field_deep.py`、`deep_directions.py`、`export.py`、`light_speed_helix.py`、`quantum_gravity_deep.py`、`theorem_system.py`

其中 `README.md` 21 KB、`theorem_system.py` 20 KB、`__init__.py` 15 KB 为最大三件。

## 为什么重要

该库把**多个体系的数学内核实现在同一套代码里**：三重奏运动学（s01）、光速螺旋（s02/s12）、人工场、大统一、粒子质量、宇宙学、核物理、弯曲时空。它实际上是"不同体系统一实现"的一个**工程先例**——但请注意，这是**代码层面的统一**，不是物理层面的统一。

## 诚实评级

- 代码层面：接口自洽、可分发的包，形态 M5 成立。
- 物理层面：库内部实现的是多个体系的公式集合，**不代表这些体系已被证明相容**。跨体系调用时仍须遵守 [T1 本体隔离](../../统一架构/统一架构总纲.md)。
- 早期支线 `core_validation_report.txt` 中 α=0.007297352564 源自觉察的 ZZ′=0.25 构造，属早期支线，**不宜进主线**。

## 建议

作为 [体系接口约定](../../体系接口约定/统一接口约定.md) 的参考实现：其 `provenance.py`（溯源字段）与 `export.py`（导出）的设计思路值得抽象为通用接口。见路线图 D4。
'''

DOSSIERS['双向分形bifuf.md'] = '''# 实现方式档案：双向分形统一场论（bifuf）

[实现方式总览](../README.md) · 归属体系：**候裁定**

- **形态**：M2 数值 · M4 格点/离散
- **位置**：`utf/17-空间光速螺旋引力理论/code/`（`bifuf_core_algo_validation.py`、`bifuf_full_rigorous_validation.py`、`bifuf_validation_final.py`）
- **状态**：**disputed** —— 认证存疑，裁定前结论不得引用

## 它是什么

bifuf = Bidirectional Fractal Unified Field（双向分形统一场）。

**不含任何物理**：没有拉格朗日量、没有作用量、没有与实验常数对接。它验证的是作者自己写的一棵分形树数据结构（每层生成 k 个子节点、缩放 s）的自洽性。

## 三份 JSON 互相矛盾

| 文件 | 声称 | 实际 |
|---|---|---|
| `bifuf_core_algo_validation.json` | 脚本只在 6/6 时才打印"OMEGA-PRIME 认证通过"横幅 | **`all_pass: false`，2/6 通过**；可逆性、维数、同构均 fail |
| `bifuf_validation_final.json` | — | **`all_pass: false`，6/8**；自相似性、数值精度稳定性失败 |
| `bifuf_full_validation_report.json` | 顶层 `all_passed: true` + OMEGA-PRIME | **自相矛盾**：`validation_3_convergence` 内 `contraction_ok` 三项全 false（实测 α=0 / 1.1427 / 0.8898，期望 0.5；α>1 意味着**根本不是压缩映射**），该块 `summary.all_passed: false` |

## 硬编码证据

`bifuf_full_rigorous_validation.py`：

- 第 753/755/756 行把验证 3、5、6 直接写成 `True`，注释"数学证明成立"
- 第 558 行 `contraction_mapping: True` 硬编码；第 550 行实测失败时只打印"△ 近似成立"
- 第 722–728 行群公理是**字面量 True 列表**（封闭性/结合律/单位元/逆元/交换性），不是计算
- 第 797 行 `core_conclusions` 六个键全硬编码 True

另有一处方法学缺陷：所谓"盒计数维数验证"是同义反复——节点数恒为 k^level、尺度恒为 s^level，线性回归斜率必然等于 log k/log(1/s)，不可能失败。

## 裁定结论（本层立场）

bifuf 的"认证"是**自我一致性单元测试被包装成物理验证**。在独立复跑并移除硬编码之前：

- 证据等级登记为 `conjecture`
- 状态标记为 `disputed`
- 其"认证通过"结论**不得引用**

## 与 s13 的关系（重要澄清）

bifuf 与 [s13 全域双向分形统一场论](../../../01_独立体系/S13_全域双向分形统一场论/README.md) 名称相近，但 s13 的本体是 0/1 对偶基元与六方程闭环 M1–M6，bifuf 只是分形树数据结构的自我一致性检查。**两者不是同一体系的版本关系**，不得互相转移证据。见 [术语消歧](../../跨体系翻译表/术语翻译表.md)「分形」条目。
'''

DOSSIERS['GMUFT.md'] = '''# 实现方式档案：GMUFT 几何流形统一场论

[实现方式总览](../README.md) · 归属体系：[s11 GMUFT 几何自由度与耦合](../../../01_独立体系/S11_GMUFT几何自由度与耦合/README.md)

- **形态**：M1 符号推导 · M6 论文
- **位置**：`article/zh/2026/9/GMUFT_v2.1_修复版统一场论.md`（13.5 KB）+ `verify_gmuft_v21.py` + `verification_results_v21.json`
- **状态**：active（完整场方程 OPEN）

## 全称与公理

原文第一行：**GMUFT v2.1 — 基于 v=c 公理与垂直原理的几何流形统一场论**（Geometric Manifold Unified Field Theory）。

- A1 `u_r² + u_⊥² = c²`
- A2 垂直原理 `r̂·⊥̂ = 0`
- A3 θ 场参数化 `u_r = c cosθ`，`u_⊥ = c sinθ`
- C3 修复 `Z₀ = β²c⁴/(4πG)`

## 诚实评级

作者自评"强/弱相互作用部分仍为框架性开放问题"，并**主动废弃** `G=α²μ₀`（差 0.26%）。这是值得肯定的诚实做法。

体系类型为 `candidate_framework`（待完备理论框架）：已有结构性对应与机制纲领，但**完整场方程待建立**。按 [模块类型](../../../00_项目治理/module_types.json)，不与拥有明确场方程的候选自动等同。

## 与统一层的关系

在八层坐标下，GMUFT 的 L4 动力学层为 `none`，L6 破缺层未建立。它是本仓库中**最能体现"框架 ≠ 理论"**的例子：几何自由度与耦合关系已给出，但没有场方程，因此目前无法产生可检验预测（C9=0）。
'''

DOSSIERS['V21元一方程.md'] = '''# 实现方式档案：V21 Ω 元一方程

[实现方式总览](../README.md) · 归属体系：**候登记**

- **形态**：M6 宣言/文稿
- **位置**：仓库根 `V21_Ω终极_元一方程_全维封王_全书.txt`（7.5 KB）
- **状态**：candidate

## 主张

元一方程 **Ω = exp(iπN²)**，自称"一条方程包含全部物理"：模为概率幅、相位为动力学、lnΩ 为全息熵。含黑洞信息悖论的全息解决与 Page 曲线论述。

## 诚实评级

**宣言性质，非验证**。无推导链、无数值脚本、无可检验预测、无失效阈值。

按 [禁止夸大表述](../../../00_项目治理/CONTRIBUTING.md) 纪律，标题中"终极""封王""全书"等表述本身即违反本仓库的用词规范；登记时应以内容为准，不得沿用该标题作为证据或宣传语。

在八层坐标下：L1 本体为"元一方程 N"，L4 动力学 `none`，C9 冻结预测 0，C10 证据等级 `conjecture`。

## 待办

- 裁定是否登记为独立体系（路线图 B5）
- 若保留，须改写为中性标题并补齐公设清单
'''

DOSSIERS['算法联盟自洽引擎.md'] = '''# 实现方式档案：算法联盟全维自洽引擎

[实现方式总览](../README.md) · 归属体系：**跨体系**（治理与审计）

- **形态**：M8 治理与审计
- **位置**：`04_公共成果/算法联盟_全维自洽与归一化/`
- **状态**：active，可复跑

## 内容

本仓库中**工程完成度最高的审计实现**：符号求导 + 80 位精算 + 雅可比自由度审计 + 量纲审计 + 归一化，统一由 `算法联盟_全维自洽引擎.py`（74 KB）驱动。

配套 20 余个专项脚本：`O级体系_隔离审查.py`、`体系量纲可行性审计.py`、`无量纲靶场审计.py`、`全维勘误精算修复验证.py`、`普朗克锚定谬误_修正与派生链重算.py`、`量纲零空间与判别式V3.py`、`预测登记与V3判别引擎.py` 等。

## 已检出的冲突（如实标 FAIL / BOUNDARY，未粉饰）

**第一性冲突 3 项**：

1. **普朗克锚定谬误（M02）**
2. **螺旋半径普适性矛盾（M01）**
3. **`P=m(c−v)` 低速极限（M03）**

**约定冲突 1 项**：s13 β 函数符号（F08）。

## 为什么这份档案重要

它是"统一层"能在不合并体系的前提下成立的**工程基础**：统一层要做跨体系对照，依赖的正是这种可复跑、可定位缺陷、且不因结果不利而删除记录的审计能力。

## 提醒

审计引擎能证明的是**内部一致性缺陷的定位于否证**，不能证明任何理论成立（八层 T3，形态 M8）。
'''

DOSSIERS['螺旋时空数据库.md'] = '''# 实现方式档案：螺旋时空数据库（helical_db）

[实现方式总览](../README.md) · 归属体系：**无**（工程原型）

- **形态**：M5 代码库
- **位置**：`helical_db/`（13 文件）
- **状态**：active

## 内容

`core/` 下 7 个模块：`helical_spacetime_database.py`、`helical_quantum.py`、`anti_database.py`、`infinite_associations.py`、`infinite_storage.py`、`instant_query_engine.py`、`infinite_expansion_engine.py`，另有 `config/constants.py` 与 `tests/`。

## 定性

**"螺旋时空数据库"概念原型 / 工程 demo，不是理论分支。**

它借用螺旋时空的术语命名数据库组件，但不提出本体主张、不含作用量、不产生可检验预测。在八层坐标下 C1 本体为"—"，不纳入体系登记。

## 处理建议

保留在 [实现方式总览](../README.md) 中作为工程原型登记，不迁入 `01_独立体系`。若日后被用于承载某体系的计算数据，再按 [接口约定](../../体系接口约定/统一接口约定.md) 登记为 `code_dependencies`。
'''

DOSSIERS['治理宪章移植.md'] = '''# 实现方式档案：治理宪章（openmath，移植来源）

[实现方式总览](../README.md) · 归属体系：**跨体系**（治理层）

- **形态**：M8 治理与审计
- **位置**：`openmath/00-宪章/`（`01-宪章总纲` … `06-治理与决策`）
- **状态**：active

## 为什么登记在这里

openuft 已有自己的 [研究流程](../../../00_项目治理/WORKFLOW.md) 与 [诚实声明](../../../LICENSE)，但**证据等级的机器可读标准**尚不完备。`openmath` 的宪章提供了一套成熟度更高的框架，可直接移植。

## 可移植的三项

### 1. 证据等级 L0–L6

| 级 | 含义 | 可否称"已证明" |
|---|---|---|
| L0 | 结构合规 | 否 |
| L1 | 良构 | 否 |
| L2 | 数值（mpmath 50 位、≥1000 组带种子） | **否——L2 唯一能做的是证伪** |
| L3 | 符号（双引擎交叉） | 否 |
| L4 | 形式化（Lean4/Coq/Isabelle，无 sorry） | **是，唯一** |
| L5 | 对抗性 | — |
| L6 | 长期可复现守护 | — |

强制写法：`status: VERIFIED` 必须写成 `VERIFIED(L2)`，lint 拦截裸 `VERIFIED`。状态机：`任意状态 --发现反例--> FALSIFIED`；`FALSIFIED` 与 `CANONICAL` 同为终态。

### 2. 诚实红线（一票否决）

- **数值验证不是证明**：禁止把"10⁶ 样例无反例 / SymPy 返回 True / LLM 给的证明"说成"已证明"
- **反例优先**：出反例即置 FALSIFIED 并**保留原条目**，不得改定义规避
- **假设必须显式化**：评审者发现隐含假设即退回，不看结论是否正确
- **禁止结论漂移**（改断言数值、放宽容差、删测试样例、try/except 吞异常）
- **AI 内容须标 provenance**；AI 生成证明不得作为 L3+ 证据；AI 不得自批 PR、自改 status
- **禁止夸大表述**：终极/彻底/颠覆/完美/革命性/首次/首创/显然/易见

一句话自检：*"如果我错了，别人能通过本仓库发现吗？"*

### 3. 标识与编号规范

`OM-<类型>-<域代码>-<4位序号>`；**ID 一经分配永不改变、永不回收**；`.yaml` 与 `.md` 必须成对。

## 待办

见 [路线图](../../路线图/统一层路线图.md) D3（行为准则与治理决策机制）。移植时应保留 openmath 的署名与出处，并适配 openuft 已有的 `sNN`/`pNN` 编号体系。

另一相关项：openmath 的 `04-数学统一场论/` 含桥接定理 `OM-BR-0001_三重奏定理_线性动力学谱与Frenet曲率.md`，与 [s01](../../../01_独立体系/S01_螺旋三重奏与谱几何/README.md) 存在实质关联，后续可建立跨库关系边（路线图 C4）。
'''

DOSSIERS['UFE1统一场方程.md'] = '''# 实现方式档案：UFE-1 统一场方程

[实现方式总览](../README.md) · 归属：[候登记_ufe1](../../体系坐标系/体系坐标表.md) · 理论正文：[07_统一场方程](../../../07_统一场方程/README.md)

- **形态**：M1 符号推导 · M2 数值验算 · M6 论文
- **位置**：`openuft/07_统一场方程/`（11 篇正文 + 2 个 CSV + 1 个生成器 + 1 个验证器）
- **状态**：active（自证完备，外部校准未做）

## 主张与本体

主方程取自单一总联络 $\\mathcal A$ 的曲率：

$$\\frac{\\delta S}{\\delta\\Phi}=0,\\quad \\Phi=(e,\\mathcal A,H,\\Psi);\\qquad
\\star D_{\\mathcal A}\\!\\star\\mathcal F=\\mathcal J,\\quad \\mathcal F=d\\mathcal A+\\mathcal A\\wedge\\mathcal A$$

"四种力写在一个方程"的机制是**李代数直和分解**：

$$\\mathfrak g=\\mathfrak{so}(1,3)\\oplus\\mathfrak{su}(3)\\oplus\\mathfrak{su}(2)\\oplus\\mathfrak u(1)$$

四种力是同一曲率沿四个因子的分量，不是四个并列项。麦克斯韦齐次方程来自统一比安基恒等式
$D_{\\mathcal A}\\mathcal F\\equiv0$，不来自变分。

## 诚实评级

| 项 | 结论 |
|---|---|
| 理论实质 | **Einstein–Cartan（含挠率）引力 + 标准模型**，非新提出的替代物理 |
| 已完成 | 五组变分（$\\delta\\omega,\\delta e,\\delta A,\\delta H,\\delta\\Psi$）逐步展开；四力还原；反常消除精确有理计算 |
| 关键推算 | 由 $G_F,\\alpha,m_Z,m_t$ 算出 $m_W=80.409$ GeV，实测 $80.377\\pm0.012$，**偏差 0.04%** |
| 主要缺陷 | **19 个输入参数**（含 $\\alpha$ 的数值、质量谱、代数、$\\Lambda$ 全部为输入）；无右手中微子致 $m_\nu=0$，与振荡实验矛盾 |
| 未解决 | 禁闭无解析证明（Clay 问题）、引力量子化、层级问题、强 CP、暗物质 |

**与既有体系的区别**：S14（TUFT）同样以主丛与联络为骨架，但其多项 claims 已登记为 falsified
（挠率多分量相加为类型错误、$\\sin^2\\theta_W$ 尺度混淆、单圈三耦合不汇聚）。UFE-1 不重复这些错误：
挠率在本体中是**代数**方程（不传播、不产生第五种力），$\\sin^2\\theta_W$ 与耦合统一作为**检验项**而非结论登记。

## 验证方式与结果

`07_统一场方程/验证脚本/verify_core.py` —— **零第三方依赖**（纯 `fractions` + `math`），可复跑：

```bash
cd openuft/07_统一场方程/验证脚本 && python -B verify_core.py
```

**47 项：PASS 38 / FAIL 3 / INFO 6。** 三项 FAIL 是如实登记的否定结果：
SM 单圈三耦合不统一（$\\alpha^{-1}$ 最小散布 3.66，MSSM 对照 0.049）、无右手中微子。

## 待裁定事项

1. **编号归属未定**：本板块现为顶层 section，未进入 `01_独立体系/` 的 `sNN` 注册。
   是否改登记为 `s15`、是否补 `system.json` + 17 阶段 + `claims.csv`，需维护者裁定。
   在此之前，坐标表中以 `候登记_ufe1` 记录。
2. **外部校准未做**：UFT-1…UFT-6 判据未与标准模型之外的其他路线做定量计分（路线图 D3）。
3. **C8=19 未被优化**：参数数目未做任何自然性论证。
'''

# ---------------- 关系图谱 ----------------
RELATIONS = [
    # source, relation, target, evidence, status
    ('s07_gaq_complex_curvature', 'version_of', 's03_gaq_geometric_atom', 'GAQ v1→v4 同一复曲率本体', 'active'),
    ('s08_gaq_geometrized_constants', 'version_of', 's07_gaq_complex_curvature', 'v5 把 c/ħ 降为几何桥梁', 'active'),
    ('s09_gaq_mass_spectrum', 'version_of', 's08_gaq_geometrized_constants', 'v6 加代结构与质量比', 'active'),
    ('s04_ieg_information_gravity', 'version_of', 's03_gaq_geometric_atom', 'GAQ v3 拆出 IEG 分支', 'active'),
    ('s05_hdu_higher_dimensions', 'version_of', 's03_gaq_geometric_atom', 'GAQ v3 拆出 HDU 分支', 'active'),
    ('s06_tcl_topological_chirality', 'version_of', 's03_gaq_geometric_atom', 'GAQ v3 拆出 TCL 分支', 'active'),
    ('s06_tcl_topological_chirality', 'competes', 's09_gaq_mass_spectrum', '同为 π₃(SU(3))×ℤ₂=6，Cl(4,4) vs SO(3) 不同阐述', 'active'),
    ('s12_light_speed_helix', 'borrows_math', 's02_light_speed_helix_force', '借用 P=m(c−v)、F=dP/dt（登记为 S12-A4 借用项）', 'active'),
    ('s12_light_speed_helix', 'competes', 's10_frequency_helix_ontology', 'v≡c 恒等 vs v≤c 上限，本体互斥', 'active'),
    ('s10_frequency_helix_ontology', 'borrows_math', 's01_triad_kinematics', '共用 κ²+τ²=(ω/v)² 骨架', 'active'),
    ('s12_light_speed_helix', 'borrows_math', 's01_triad_kinematics', '共用 κ²+τ²=(ω/v)² 骨架', 'active'),
    ('s13_duality_fractal_uft', 'independent', 's12_light_speed_helix', '0/1 对偶基元 vs 空间光速运动，无公设交集', 'active'),
    ('s13_duality_fractal_uft', 'independent', 's14_torsion_unified_field_tuft', 'L1 本体互斥，不可公度', 'active'),
    ('s14_torsion_unified_field_tuft', 'borrows_math', 's01_triad_kinematics', 'Frenet 曲率/挠率语言', 'active'),
    ('s11_gmuft_geometric_coupling', 'competes', 's14_torsion_unified_field_tuft', '同为几何自由度路线，场方程完备性不同', 'active'),
    ('实现:TUFT主线 v2–v18', 'implements', 's14_torsion_unified_field_tuft', 'tuft_v*.py 系列与独立审计裁决', 'active'),
    ('实现:TUFT原始工作区 tuft/', 'implements', 's14_torsion_unified_field_tuft', 'tuft_r1–r25 成对脚本', 'archived'),
    ('实现:全域统一场论书稿', 'implements', 's13_duality_fractal_uft', '六方程闭环 M1–M6 书稿；命名含 TUFT 但本体属 s13', 'active'),
    ('实现:GAQ-UFT 成书', 'implements', 's03_gaq_geometric_atom', '7 卷成书，覆盖 s03/s07/s08/s09', 'active'),
    ('实现:GAQ 谱系 v1→v6', 'implements', 's03_gaq_geometric_atom', 'gaq_uft_*.py 系列', 'active'),
    ('实现:空间光速螺旋族展示', 'implements', 's12_light_speed_helix', '单页 HTML 展示层', 'active'),
    ('实现:空间光速螺旋族展示', 'implements', 's10_frequency_helix_ontology', '共用 α=tanθ=τ/κ 视觉语言', 'active'),
    ('实现:空间光速螺旋族展示', 'implements', 's02_light_speed_helix_force', '四力来源图', 'active'),
    ('实现:三分量统一场论库 triad_uft/', 'implements', 's01_triad_kinematics', 'triad.py / geometry.py', 'active'),
    ('实现:三分量统一场论库 triad_uft/', 'implements', 's12_light_speed_helix', 'light_speed_helix.py', 'active'),
    ('实现:GMUFT v2.1', 'implements', 's11_gmuft_geometric_coupling', 'verify_gmuft_v21.py', 'active'),
    ('实现:算法联盟自洽引擎', 'implements', '跨体系', '量纲/自由度/量纲零空间审计', 'active'),
    ('s14_torsion_unified_field_tuft', 'falsified_by', 'S14-C0001 挠率多分量相加为类型错误', '维数不可加；实为 SM 表示论重述', 'falsified'),
    ('s14_torsion_unified_field_tuft', 'falsified_by', 'S14-C0002 sin²θ_W 尺度混淆', '1/4 vs 0.23122 差 8.12%', 'falsified'),
    ('s14_torsion_unified_field_tuft', 'falsified_by', 'S14-C0003 1-loop SM 三耦合不汇聚', '10^16 GeV 处 21.0% 分散', 'falsified'),
    ('s13_duality_fractal_uft', 'falsified_by', '1D 绕数（π₁(S²)=0）', '已改 3D Hopf（π₃(S²)=ℤ）', 'falsified'),
    # UFE-1（07_统一场方程）接入
    ('实现:UFE-1 统一场方程', 'implements', '候登记_ufe1', '07_统一场方程/ 主方程 + 五组变分 + 47 项验证', 'active'),
    ('候登记_ufe1', 'competes', 's14_torsion_unified_field_tuft',
     '同为几何联络路线；S14 挠率多分量相加已被证伪，UFE-1 取挠率为代数约束', 'active'),
    ('候登记_ufe1', 'competes', 's11_gmuft_geometric_coupling',
     '同为几何自由度统一路线；S11 完整场方程 OPEN（其 L4=none）', 'active'),
    ('候登记_ufe1', 'independent', 's13_duality_fractal_uft',
     '规范场论本体 vs 0/1 对偶基元，L1 无公设交集', 'active'),
    # 候登记 / 候裁定的具体化（原先指向泛化节点，图上不可见）
    ('实现:全域数学 UM', 'implements', '候登记_um', 'uft/06-论文/', 'candidate'),
    ('实现:V21 Ω 元一方程', 'implements', '候登记_v21omega', 'V21_Ω…txt', 'candidate'),
    ('实现:双向分形 bifuf', 'implements', '候裁定_bifuf', '**disputed**，见档案；裁定前结论不得引用', 'disputed'),
    ('候裁定_bifuf', 'independent', 's13_duality_fractal_uft',
     '仅名称相近：分形树自洽检查 vs 0/1 对偶基元，本体不同', 'active'),
]

RELATION_DOC = '''# 体系关系图谱

[统一体系层](../README.md) · [关系边 CSV](体系关系边.csv) · [交互式图谱](体系关系图.html)

## 关系边是谱系标注，不是已证明的逻辑依赖

一条边只说明两个体系（或实现）之间存在**版本、借用、竞争或实现**关系。它不构成证据转移，也不表示任一体系成立。

## 关系边类型

| 类型 | 含义 | 是否转移证据 |
|---|---|---|
| `version_of` | 版本演进（同一 L1 本体的后续版本） | 否，逐版独立审查 |
| `borrows_math` | 借用另一个体系的数学工具（形式，非结论） | **否**，见八层 T1 |
| `competes` | 本体互斥，不可公度 | 否 |
| `implements` | 代码/书稿实现了某体系 | 否，实现不是证据（T3） |
| `supersedes` | 取代（旧版停更） | 否 |
| `falsified_by` | 该条目已被证伪 | 终态，不得删除 |
| `independent` | 无公设交集 | 否 |

## 边清单

| 起点 | 关系 | 终点 | 依据 | 状态 |
|---|---|---|---|---|
''' + '\n'.join(
    '| `{}` | `{}` | `{}` | {} | {} |'.format(r[0], r[1], r[2], r[3], r[4])
    for r in RELATIONS
) + '''

## 四类高危误解

1. **把 `borrows_math` 当依赖**：s10/s12 借用 s01 的三重奏恒等式，但 s01 的数学结果不能为 s10/s12 的本体主张背书。
2. **把 `implements` 当认证**：TUFT 主线跑了 17 个版本，不等于 s14 成立；s14 的 claims 中多项为 falsified。同理，UFE-1 有 47 项验证通过，不等于它已被证实。
3. **把 `version_of` 当等价**：s03→s07→s08→s09 是同一研究逐版改公设，不是四个互相支持的独立证据。
4. **把 `候登记` 当已登记**：`候登记_ufe1`、`候登记_um`、`候登记_v21omega` 与 `候裁定_bifuf` 尚未取得 `sNN` / `pNN` 编号。它们在图中出现只为标注关系，不表示身份已确立；`候裁定_bifuf` 在裁定前其结论不得引用。

## 待完成

- 每条边补 `locator`（具体文件与章节），见路线图 C3
- 与 [全球 9 条路线](../../05_全球研究/02_全球路线/README.md) 建立外部体系边，见路线图 C4
'''

RELATION_CSV = '起点,关系,终点,依据,状态\n' + '\n'.join(
    ','.join('"{}"'.format(c.replace('"', '""')) for c in row) for row in RELATIONS
)


def build_graph_html():
    """生成交互式体系关系图（纯 SVG + 内联 JS，无外部依赖）。"""
    groups = {
        '螺旋 / 光速族': ['s01_triad_kinematics', 's02_light_speed_helix_force',
                       's10_frequency_helix_ontology', 's12_light_speed_helix'],
        'GAQ 几何族': ['s03_gaq_geometric_atom', 's04_ieg_information_gravity',
                    's05_hdu_higher_dimensions', 's06_tcl_topological_chirality',
                    's07_gaq_complex_curvature', 's08_gaq_geometrized_constants',
                    's09_gaq_mass_spectrum'],
        '对偶 / 挠率族': ['s13_duality_fractal_uft', 's14_torsion_unified_field_tuft'],
        '待完备与方向': ['s11_gmuft_geometric_coupling', 'p01_space_compression',
                    'p02_matter_source', 'p03_gauge_unification', 'p04_quantum_emergence'],
        '形式化核心 / 候登记': ['候登记_ufe1', '候登记_um',
                        '候登记_v21omega', '候裁定_bifuf'],
    }
    labels = {
        's01_triad_kinematics': 'S01 螺旋三重奏\n(数学框架)',
        's02_light_speed_helix_force': 'S02 光速螺旋统一力',
        's10_frequency_helix_ontology': 'S10 频率本源',
        's12_light_speed_helix': 'S12 空间光速螺旋',
        's03_gaq_geometric_atom': 'S03 GAQ 几何原子',
        's04_ieg_information_gravity': 'S04 IEG 信息熵引力',
        's05_hdu_higher_dimensions': 'S05 HDU 高维紧致化',
        's06_tcl_topological_chirality': 'S06 TCL 拓扑手征',
        's07_gaq_complex_curvature': 'S07 GAQ 复曲率',
        's08_gaq_geometrized_constants': 'S08 GAQ 常数几何化',
        's09_gaq_mass_spectrum': 'S09 GAQ 质量谱',
        's13_duality_fractal_uft': 'S13 全域双向分形',
        's14_torsion_unified_field_tuft': 'S14 挠率统一场论 TUFT',
        's11_gmuft_geometric_coupling': 'S11 GMUFT 几何耦合',
        'p01_space_compression': 'P01 空间压缩',
        'p02_matter_source': 'P02 物体驱动',
        'p03_gauge_unification': 'P03 规范统一',
        'p04_quantum_emergence': 'P04 量子涌现',
        '候登记_ufe1': 'UFE-1 统一场方程\n(07 · 候登记)',
        '候登记_um': 'UM 全域数学\n(候登记)',
        '候登记_v21omega': 'V21 Ω 元一方程\n(候登记)',
        '候裁定_bifuf': 'bifuf 双向分形\n(disputed)',
    }
    colors = {
        '螺旋 / 光速族': '#2563eb',
        'GAQ 几何族': '#7c3aed',
        '对偶 / 挠率族': '#c2410c',
        '待完备与方向': '#64748b',
        '形式化核心 / 候登记': '#0f766e',
    }
    # 布局：两列两行分区
    boxes = {
        '螺旋 / 光速族': (60, 120, 430, 300),
        'GAQ 几何族': (530, 120, 430, 420),
        '对偶 / 挠率族': (60, 470, 430, 220),
        '待完备与方向': (530, 590, 430, 330),
        '形式化核心 / 候登记': (60, 710, 430, 210),
    }
    node_pos = {}
    for g, members in groups.items():
        x, y, w, h = boxes[g]
        per_row = 2 if g != '待完备与方向' else 2
        for i, sid in enumerate(members):
            col, row = i % per_row, i // per_row
            nx = x + 20 + col * (w - 40) / per_row + (w - 40) / per_row / 2
            ny = y + 55 + row * 95
            node_pos[sid] = (nx, ny)

    edge_color = {
        'version_of': '#16a34a',
        'borrows_math': '#0891b2',
        'competes': '#dc2626',
        'implements': '#94a3b8',
        'falsified_by': '#b91c1c',
        'independent': '#cbd5e1',
        'supersedes': '#a16207',
    }
    svg_w, svg_h = 1020, 1120
    falsified_count = {'s14_torsion_unified_field_tuft': 3, 's13_duality_fractal_uft': 1}
    parts = []
    parts.append('<svg viewBox="0 0 {} {}" xmlns="http://www.w3.org/2000/svg" '
                 'font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Microsoft YaHei,sans-serif">'
                 .format(svg_w, svg_h))
    parts.append('<rect width="100%" height="100%" fill="#ffffff"/>')
    parts.append('<text x="30" y="40" font-size="22" font-weight="700" fill="#0f172a">'
                 'openuft 统一体系层 · 体系关系图</text>')
    parts.append('<text x="30" y="66" font-size="13" fill="#475569">'
                 '节点按本体族分区；边为谱系与借用标注，不构成证据转移</text>')
    # 分区背景
    for g, (x, y, w, h) in boxes.items():
        parts.append('<rect x="{}" y="{}" width="{}" height="{}" rx="12" fill="#f8fafc" '
                     'stroke="{}" stroke-width="1.5" stroke-dasharray="5 4"/>'.format(x, y, w, h, colors[g]))
        parts.append('<text x="{}" y="{}" font-size="14" font-weight="700" fill="{}">{}</text>'
                     .format(x + 14, y + 26, colors[g], g))
    # 边
    for src, rel, dst, _ev, st in RELATIONS:
        if src in node_pos and dst in node_pos:
            x1, y1 = node_pos[src]
            x2, y2 = node_pos[dst]
            parts.append('<line x1="{:.1f}" y1="{:.1f}" x2="{:.1f}" y2="{:.1f}" stroke="{}" '
                         'stroke-width="1.6" opacity="0.55" data-rel="{}"/>'
                         .format(x1, y1, x2, y2, edge_color.get(rel, '#94a3b8'), rel))
    # 节点
    for sid, (nx, ny) in node_pos.items():
        g = next(k for k, v in groups.items() if sid in v)
        c = colors[g]
        lines = labels[sid].split('\n')
        wnode, hnode = 190, 56 if len(lines) == 1 else 68
        parts.append('<g class="node"><rect x="{:.1f}" y="{:.1f}" width="{}" height="{}" rx="8" '
                     'fill="#ffffff" stroke="{}" stroke-width="2"/>'
                     .format(nx - wnode / 2, ny - hnode / 2, wnode, hnode, c))
        if len(lines) == 1:
            parts.append('<text x="{:.1f}" y="{:.1f}" font-size="13" font-weight="600" '
                         'text-anchor="middle" fill="#0f172a">{}</text>'.format(nx, ny + 4, lines[0]))
        else:
            parts.append('<text x="{:.1f}" y="{:.1f}" font-size="13" font-weight="600" '
                         'text-anchor="middle" fill="#0f172a">{}</text>'.format(nx, ny - 4, lines[0]))
            parts.append('<text x="{:.1f}" y="{:.1f}" font-size="11" text-anchor="middle" '
                         'fill="#64748b">{}</text>'.format(nx, ny + 14, lines[1]))
        if sid in falsified_count:
            n = falsified_count[sid]
            cx, cy = nx + wnode / 2 - 8, ny - hnode / 2 + 8
            parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="9" fill="#b91c1c"/>'.format(cx, cy))
            parts.append('<text x="{:.1f}" y="{:.1f}" font-size="11" font-weight="700" '
                         'text-anchor="middle" fill="#ffffff">{}</text>'.format(cx, cy + 4, n))
        tip = sid + ('（含 {} 条已证伪条目，见 claims.csv）'.format(falsified_count[sid])
                     if sid in falsified_count else '')
        parts.append('<title>{}</title></g>'.format(tip))
    # 图例
    lx, ly = 60, 960
    parts.append('<text x="{}" y="{}" font-size="13" font-weight="700" fill="#0f172a">关系类型</text>'.format(lx, ly))
    legend = [('version_of', '版本演进'), ('borrows_math', '借用数学（不转移证据）'),
              ('competes', '本体互斥'), ('implements', '实现'), ('falsified_by', '已证伪'),
              ('independent', '无公设交集')]
    parts.append('<circle cx="{}" cy="{}" r="8" fill="#b91c1c"/>'.format(lx + 300, ly + 40))
    parts.append('<text x="{}" y="{}" font-size="11" font-weight="700" text-anchor="middle" '
                 'fill="#ffffff">n</text>'.format(lx + 300, ly + 44))
    parts.append('<text x="{}" y="{}" font-size="12" fill="#334155">角标 n = 该体系已登记证伪条目数</text>'
                 .format(lx + 316, ly + 44))
    for i, (k, name) in enumerate(legend):
        yy = ly + 22 + i * 21
        parts.append('<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="{}" stroke-width="2.4"/>'
                     .format(lx, yy - 4, lx + 30, yy - 4, edge_color[k]))
        parts.append('<text x="{}" y="{}" font-size="12" fill="#334155">{}</text>'.format(lx + 38, yy, name))
    parts.append('<text x="640" y="980" font-size="13" font-weight="700" fill="#0f172a">阅读提醒</text>')
    notes = ['本图不表示任何统一场论已经成立。',
             'S14 已登记多项 falsified，见其 claims.csv。',
             '候登记 / 候裁定节点未进入 sNN 注册，编号待裁定。',
             '实现（代码 / 书稿 / 图谱）不提升证据等级。']
    for i, n in enumerate(notes):
        parts.append('<text x="640" y="{}" font-size="12" fill="#475569">· {}</text>'.format(1002 + i * 21, n))
    parts.append('</svg>')

    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>openuft 体系关系图</title>
<style>
  :root {{ --ink:#0f172a; --sub:#475569; --line:#e2e8f0; --bg:#ffffff; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--ink);
         font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Microsoft YaHei",sans-serif; }}
  header {{ padding:22px 32px 14px; border-bottom:1px solid var(--line); }}
  header h1 {{ margin:0 0 6px; font-size:21px; }}
  header p {{ margin:0; font-size:13px; color:var(--sub); }}
  .toolbar {{ padding:12px 32px; display:flex; flex-wrap:wrap; gap:8px; border-bottom:1px solid var(--line); }}
  .chip {{ border:1px solid var(--line); background:#f8fafc; border-radius:999px;
           padding:5px 13px; font-size:12px; cursor:pointer; color:#334155; }}
  .chip.active {{ background:#0f172a; color:#fff; border-color:#0f172a; }}
  main {{ padding:10px 32px 40px; }}
  svg {{ width:100%; height:auto; }}
  .node rect {{ transition:all .15s ease; }}
  .node:hover rect {{ filter:drop-shadow(0 3px 8px rgba(15,23,42,.16)); }}
  .node:hover {{ cursor:default; }}
  line[data-rel] {{ transition:opacity .15s ease; }}
  svg.filtering line[data-rel] {{ opacity:.08; }}
  svg.filtering line[data-rel].on {{ opacity:.85; }}
  footer {{ padding:16px 32px 30px; font-size:12px; color:var(--sub); border-top:1px solid var(--line); }}
  code {{ background:#f1f5f9; padding:1px 5px; border-radius:4px; font-size:12px; }}
</style>
</head>
<body>
<header>
  <h1>openuft 统一体系层 · 体系关系图</h1>
  <p>节点按本体族分区。边表示版本演进、数学借用、本体竞争或实现关系，<strong>不构成证据转移</strong>。</p>
</header>
<div class="toolbar" id="bar">
  <button class="chip active" data-rel="all">全部关系</button>
  <button class="chip" data-rel="version_of">版本演进</button>
  <button class="chip" data-rel="borrows_math">借用数学</button>
  <button class="chip" data-rel="competes">本体互斥</button>
  <button class="chip" data-rel="implements">实现</button>
  <button class="chip" data-rel="falsified_by">已证伪</button>
  <button class="chip" data-rel="independent">无交集</button>
</div>
<main>
{svg}
</main>
<footer>
  生成脚本：<code>06_统一体系层/维护脚本/build_impl_dossiers.py</code> ·
  数据：<a href="体系关系边.csv">体系关系边.csv</a> ·
  说明：<a href="体系关系图谱.md">体系关系图谱.md</a><br>
  本图为视图层整理，不移动任何目录，不改变任何体系的证据等级。
</footer>
<script>
  var svg = document.querySelector('svg');
  document.querySelectorAll('.chip').forEach(function(btn) {{
    btn.addEventListener('click', function() {{
      document.querySelectorAll('.chip').forEach(function(b) {{ b.classList.remove('active'); }});
      btn.classList.add('active');
      var rel = btn.dataset.rel;
      if (rel === 'all') {{ svg.classList.remove('filtering');
        svg.querySelectorAll('line[data-rel]').forEach(function(l) {{ l.classList.remove('on'); }}); return; }}
      svg.classList.add('filtering');
      svg.querySelectorAll('line[data-rel]').forEach(function(l) {{
        l.classList.toggle('on', l.dataset.rel === rel);
      }});
    }});
  }});
</script>
</body>
</html>
'''.format(svg='\n'.join(parts))
    return html


def main():
    DOSSIER.mkdir(parents=True, exist_ok=True)
    for name, body in DOSSIERS.items():
        (DOSSIER / name).write_text(body.rstrip() + '\n', encoding='utf-8')
    (DOSSIER / 'README.md').write_text(
        '# 实现方式档案\n\n[实现方式总览](../README.md) · [统一体系层](../../README.md)\n\n'
        '逐个实现的勘察档案，包含位置、形态、理论归属、诚实评级与待裁定事项。\n\n'
        + '\n'.join('- [{}]({})'.format(n[:-3], n) for n in sorted(DOSSIERS))
        + '\n\n档案中的 disputed / falsified 标记保留原样，不因进入统一层而改变。\n',
        encoding='utf-8')
    (LAYER / '关系体系图' / '体系关系图谱.md').write_text(RELATION_DOC.rstrip() + '\n', encoding='utf-8')
    (LAYER / '关系体系图' / '体系关系边.csv').write_text(RELATION_CSV, encoding='utf-8')
    (LAYER / '关系体系图' / '体系关系图.html').write_text(build_graph_html(), encoding='utf-8')
    print('dossiers: {}; relations: {}'.format(len(DOSSIERS), len(RELATIONS)))


if __name__ == '__main__':
    main()
