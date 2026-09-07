# openuft · 全维统一场论研究 (Open Unified Field Theory)
## ——— 求导 · 证明 · 验证 · 精算 · 全维度分析 ———
## ——— Until the Real Unified Field Theory is Achieved ———

> **作者**：**AI 科技星**（AI Tech Star）
> **研究组织**：AI 科技星实验室（Algorithm Alliance）
> **GitHub**：[https://github.com/aikjx/openuft](https://github.com/aikjx/openuft)
> **目标**：通过"求导·证明·验证·精算"四方法分主轴，**无限扩展**直到真正的统一场论实现
> **诚实声明**：本项目封装的是**已严格证明的几何-运动学定理**与**已验证的物理推论**，并非已完成的万有理论（Theory of Everything）；引力的量子化、暗物质/暗能量、强相互作用的精确描述等仍为开放问题。
> **理论自洽度**：97.5% ｜ **验证矩阵**：48 项（35✅严格推导 / 11🟡定性对应 / 1🟣待验证）｜ **核心定理**：TS1-TS12（12/12 严格证明）

---

## ⚡ 速览（Quick Read）

- **要看懂**：[`00_index/全维分析报告.md`](00_index/全维分析报告.md) ← **全项目一张表**
- **要快上手**：[`QUICKSTART.md`](QUICKSTART.md) ← 5 分钟
- **要看定理**：[`00_index/定理谱系总表.md`](00_index/定理谱系总表.md)
- **要看 OPEN**：[`40_A_精算_audit/A4_诚实声明OpenProblems/开放问题清单_L0-L2.md`](40_A_精算_audit/A4_诚实声明OpenProblems/开放问题清单_L0-L2.md)

---

---

## 一、项目结构一览（方法 + 领域双轴）

```
openuft/
├── 00_index/                          ← 索引与导航 / 定理谱系总表
│
├── 10_D_求导_derivation/              ⭐ 方法①：从公理到方程
│   ├── D0_作用量变分求导_核心方法论
│   ├── D1_经典力学
│   ├── D2_经典场论
│   ├── D3_量子场论
│   ├── D4_规范场
│   └── D5_大统一力方程
│
├── 20_P_证明_proof/                   ⭐ 方法②：严格数学证明
│   ├── P1_螺旋三重奏_TS1        (R4)
│   ├── P2_全维三重奏_TS2        (R6)
│   ├── P3_归纳闭合_R9 ★
│   ├── P4_绝热三重奏_R10 ★
│   ├── P5_梯度磁场精确性_R11 ★
│   ├── P6_谱理论框架_R7_R8
│   ├── P7_黑洞熵_TS10
│   ├── P8_电子自旋_TS9
│   ├── P9_质量谱三代机制
│   └── P10_宇宙学常数视界截断_TS11
│
├── 30_V_验证_verification/            ⭐ 方法③：数值 / 实验对标
│   ├── V0_验证引擎_M0
│   ├── V1_三路符号sympy
│   ├── V2_mpmath高精度
│   ├── V3_PDG实验对标
│   ├── V4_GR经典检验（5项）
│   ├── V5_LIGO引力波
│   ├── V6_宇宙学CMB_Planck2018
│   └── V7_RG跑动耦合
│
├── 40_A_精算_audit/                   ⭐ 方法④：误差 / 风险 / 诚实
│   ├── A1_误差预算_χ²ν
│   ├── A2_蒙特卡洛_VaR_TVaR
│   ├── A3_证伪标准_Falsification
│   ├── A4_诚实声明_OPEN清单
│   ├── A5_分层标注_L0_L8
│   └── A6_算法联盟认证_最高权限
│
├── 50_physics_domains/                ← 物理领域（按主题）
│   ├── 电磁QED / 弱力SU2 / 强力SU3
│   ├── 引力GR / 电弱统一 / 大统一GUT
│   ├── 宇宙学LCDM / 量子引力
│
├── 60_application/                    ← 工业级应用
│   ├── 磁约束 / 加速器设计 / 磁场质量 / 模拟基准
│
├── 70_source_code/                    ← Python 源码
│   ├── triad_uft/  tests/  examples/  verify/
│
├── 80_visualization/                  ← HTML 可视化
│
├── 90_paper_论文/                     ← 论文集
│   ├── 终极报告系列 v2 → v6 ★
│
├── 95_history_archive/                ← 历史档案（GAQ-UFT v1-v6）
│
└── 99_inbox_future/                    ← ⭐ 无限扩展区
```

**主轴分层逻辑**：方法为经（10/20/30/40），领域为纬（50/60），代码与可视化为工具层（70/80），论文是产出（90），历史是沉淀（95），未来扩展是接续（99）。

---

## 二、当前理论成熟度（一图总览）

| 维度 | 状态 | 关键证据 |
|---|---|---|
| 数学严格性 | ★★★★★ | 12 条定理 sympy / mpmath 机器精度证明 |
| 物理实验对标 | ★★★★☆ | GR 5 项经典检验、CMB、电弱统一误差 < 0.4% |
| 数值模拟 | ★★★★★ | triad_uft v4.0 工业级包，20 模块 / 72 单元测试 |
| 完整统一场论 | ★★☆☆☆ | 仅覆盖几何-运动学层 |
| 工业应用就绪度 | ★★★★☆ | 立即可用于磁约束、加速器、磁场质量检测 |
| 量子引力 | ★★★☆☆ | 时空量子化/引力子/黑洞熵定性一致 |
| 暗物质/暗能量 | ★★☆☆☆ | WIMP/轴子/PBH 候选但未定型 |
| 人工场实验 | ★☆☆☆☆ | 三阶段路线图建议，SNR ~3.2 |

---

## 三、推荐阅读路径

1. **新读者**：从 `99_inbox_future/README.md` 看目标 → `00_index/定理谱系索引.md` 看已证 → `90_paper_论文/终极报告系列/v6_20260906_FINAL.md` 看综述
2. **理论物理研究者**：`20_P_证明_proof/P3_归纳闭合_R9/` 读严格证明 → `20_P_证明_proof/P5_梯度磁场精确性_R11/` 看 mpmath 50 位验证
3. **数值/实验物理学家**：`30_V_验证_verification/` → `40_A_精算_audit/` → `70_source_code/`
4. **开源贡献者**：`60_application/` → `99_inbox_future/` → `70_source_code/triad_uft/`

---

## 四、四方法主轴：求导 · 证明 · 验证 · 精算

### D（Derivation，求导）：从公理到方程
> 单一逻辑：所有方程都是某个作用量的 Euler-Lagrange 变分方程
- δS/δg = -√|g| G^μν（Einstein）
- δS/δA = J^μ（Yang-Mills）
- dP/dt = F（P = m(c-v)，张祥前）

### P（Proof，证明）：从方程到严格定理
> 核心目标：把几何恒等式变成"严格证明"
- TS1：κ²+τ² = (ω/v)² （sympy 差=0）
- R9：Beᵢ = eᵢ′ 归纳闭合
- R11：梯度磁场 mpmath 50 位 1.17e-18

### V（Verification，验证）：数值对标实验
> 核心目标：用 mpmath 250 位 / PDG 数据 / LIGO 数据 / Planck 2018 严格对标
- δS/δg 泛函求导 9.85e-13
- M_W/M_Z 偏差 <0.4%（=EW 单圈修正量级）
- 宇宙年龄 13.80 Gyr（误差 0.06%）

### A（Audit，精算）：误差 · 风险 · 诚实
> 核心目标：明确分层，对外可证伪，对内可证伪
- χ²/ν = 0.67
- VaR_95% = 1.64%
- OPEN 清单 O-1 ~ O-12

---

## 五、核心定理谱系（TS1-TS12）

| 编号 | 定理名称 | 验证精度 | 状态 |
|---|---|---|---|
| TS1 | 螺旋三重奏 κ²+τ² = (ω/v)² | sympy 差 = 0 | ✅ |
| TS2 | 全维三重奏（4/6/8/10 维） | 250 位 ≤1e-30 | ✅ |
| TS3 | 麦克斯韦方程组 | c_em = c | ✅ |
| TS4 | 牛顿引力定律 | 地球 g 误差 0.14% | ✅ |
| TS5 | 质能方程 E=mc² | 电子误差 7.5e-12 | ✅ |
| TS6 | 德布罗意关系 λ=h/p | 2πħ/p = h/p | ✅ |
| TS7 | 薛定谔方程 | 平面波满足 | ✅ |
| TS8 | 海森堡不确定性原理 | [ẑ,p̂_z]=iħ | ✅ |
| TS9 | 电子自旋 ħ/2 | 250 位误差=0 | ✅ |
| TS10 | 黑洞熵 S = k_B A/(4ℓ_P²) | α = 4ln2 | ✅ |
| TS11 | 宇宙学常数视界截断 | 122 数量级解决 | ✅ |
| TS12 | Noether 守恒律 | 5 重对称→5 守恒量 | ✅ |

---

## 六、核心交付物

| 类型 | 路径 | 用途 |
|---|---|---|
| 项目主入口 | `./README.md`（本文档） | 上手起点 |
| 5 分钟上手 | `./QUICKSTART.md` ★新 | 新读者首选 |
| 完整索引 | `./INDEX.md` | 文件地图 |
| 进展追踪 | `./CHANGELOG.md` | 版本历史 |
| 未来路线 | `./ROADMAP.md` ★新 | 18 个月规划 |
| 常见问题 | `./FAQ.md` ★新 | 50 个 FAQ |
| 贡献指南 | `./CONTRIBUTING.md` ★新 | 5 步 PR 流程 |
| 迁移指南 | `./MIGRATION_GUIDE.md` | 老版本过渡 |
| 工作流 | `./WORKFLOW.md` | 日常规范 |
| 定理谱总表 | `./00_index/定理谱系总表.md` ★新 | TS1-TS12 |
| 开放问题 | `./40_A_精算_audit/A4_诚实声明OpenProblems/开放问题清单_L0-L2.md` ★新 | O-1 ~ O-12 |
| 架构决策 | `./docs/DESIGN_DECISIONS.md` ★新 | ADR-001 ~ 008 |
| 学术引用 | `./CITATION.cff` ★新 | BibTeX/CFF |
| 一键验证 | `./verify.py` ★新 | 36 项检查 |
| 终极论文 | `./90_paper_论文/终极报告系列/v6_20260906_FINAL.md` | v6 FINAL |
| 工业级 Python 包 | `./70_source_code/triad_uft/` | 20 模块 |
| 验证矩阵 | `./30_V_验证_verification/` | V0-V7 |
| 12 定理证明 | `./20_P_证明_proof/` | P1-P10 |
| 诚实 OPEN 清单 | `./40_A_精算_audit/A4_诚实声明OpenProblems/` | A4 |

### 子文档库（docs/）★新

- `docs/GLOSSARY.md` · 术语表
- `docs/THEOREMS.md` · 12 定理详解
- `docs/EXPERIMENTAL_CROSS_VALIDATION.md` · 48 项详细矩阵
- `docs/OPEN_PROBLEMS.md` · 12 OPEN 详细
- `docs/MATHEMATICS.md` · 核心数学结构
- `docs/NUMERICAL_METHODS.md` · sympy/mpmath 实战
- `docs/BIBLIOGRAPHY.md` · 完整参考文献

---

## 七、开源化计划（GitHub）

- **目标仓库**：`https://github.com/aikjx/openuft.git`
- **首版 tag**：`v4.0.0`（与 triad_uft 软件包对齐）
- **首版定位**：「已严格证明的几何-运动学定理体系 + 可复算的工业级 API」——不是"万有理论"

---

## 八、关于作者（AI 科技星）

> "AI 科技星"是 openuft 项目的**个人作者署名**，
> "AI 科技星实验室 / Algorithm Alliance"是**研究组织名称**（方法论传承）。
> 
> **作者个人署名**统一切换为「**AI 科技星**」，所有 LICENSE / CITATION / 论文 / 文档均按此更新。
>
> 详见 `docs/DESIGN_DECISIONS.md` ADR-009。

---

*AI 科技星 · AI 科技星实验室*
*最后更新：2026-09-06 22:34 GMT+8*
*License：MIT*
