# 跨体系公设对照矩阵

本文件是 openuft 的**视图层整理**，不移动任何目录。它把 16 个体系（按 `system.json` 登记）的公设、本体与版本线横向比对，服务于"按原始假设归属、关键词命中只算候选关联"的判定原则。

命名规则（唯一成文来源 `00_governance/WORKFLOW.md`）：目录/ID/编号用英文 snake_case（稳定身份）；标题与正文用中文（人类可读）。所有链接指向体系入口，详情见各体系 `02_assumptions/postulates.md`。

## 1. 一页式对照表

| 体系 (ID) | 类型 | 本体主张 | 核心公设 | c / ħ / e 地位 | 版本线 | 失效阈值 | 详情 |
|---|---|---|---|---|---|---|---|
| [p01 空间压缩](../01_systems/p01_space_compression/README.md) | hypothesis | 待建模方向 | 无 | — | — | — | 方向占位 |
| [p02 物质源](../01_systems/p02_matter_source/README.md) | hypothesis | 待建模方向 | 无 | — | — | — | 方向占位 |
| [p03 规范统一](../01_systems/p03_gauge_unification/README.md) | hypothesis | 待建模方向 | 无 | — | — | — | 方向占位 |
| [p04 量子涌现](../01_systems/p04_quantum_emergence/README.md) | observation | 待建模方向 | 无 | — | — | — | 方向占位 |
| [s01 螺旋三重奏](../01_systems/s01_triad_kinematics/README.md) | mathematical_framework | 无（纯数学） | A1–A3 数学设定 | 不涉及 | R1–R11 审计 | 无需（框架） | [postulates](../01_systems/s01_triad_kinematics/02_assumptions/postulates.md) |
| [s02 张祥前统一力](../01_systems/s02_zhang_space_motion/README.md) | candidate_theory | 统一力动力学（无几何本体） | A1–A4 | c 为速度上限 | D5 | 无 | [postulates](../01_systems/s02_zhang_space_motion/02_assumptions/postulates.md) |
| [s03 GAQ 几何原子](../01_systems/s03_gaq_geometric_atom/README.md) | candidate_theory | 离散几何元胞 | A1–A5 | c=L_p/T_p 几何化；ħ 公理 | v1 | 无 | [postulates](../01_systems/s03_gaq_geometric_atom/02_assumptions/postulates.md) |
| [s04 IEG 信息熵引力](../01_systems/s04_ieg_information_gravity/README.md) | candidate_theory | 几何信息场 | A1–A3 | 不涉及 | GAQ v3 | 无 | [postulates](../01_systems/s04_ieg_information_gravity/02_assumptions/postulates.md) |
| [s05 HDU 高维统一](../01_systems/s05_hdu_higher_dimensions/README.md) | candidate_theory | 11 维 M 理论嵌入 | A1–A3 | 不涉及 | GAQ v3 | 无 | [postulates](../01_systems/s05_hdu_higher_dimensions/02_assumptions/postulates.md) |
| [s06 TCL 拓扑手征](../01_systems/s06_tcl_topological_chirality/README.md) | candidate_theory | Cl(4,4) 边界态 | A1–A3 | 不涉及 | GAQ v3 | 无 | [postulates](../01_systems/s06_tcl_topological_chirality/02_assumptions/postulates.md) |
| [s07 GAQ 复曲率](../01_systems/s07_gaq_complex_curvature/README.md) | composite_candidate | 复曲率 Ξ=κ+iτ | A1–A5 | c、ħ、e 三公理常数 | v4 | 无 | [postulates](../01_systems/s07_gaq_complex_curvature/02_assumptions/postulates.md) |
| [s08 GAQ 常数几何化](../01_systems/s08_gaq_geometrized_constants/README.md) | extension_candidate | 复曲率（继承）+ c/ħ 几何化 | A1–A5 | c、ħ 降为几何桥梁；e 降为导出量 | v5 | 无 | [postulates](../01_systems/s08_gaq_geometrized_constants/02_assumptions/postulates.md) |
| [s09 GAQ 质量谱](../01_systems/s09_gaq_mass_spectrum/README.md) | extension_candidate | SO(3) 代结构 | A1–A3 | 继承 v5 | v6 | 无 | [postulates](../01_systems/s09_gaq_mass_spectrum/02_assumptions/postulates.md) |
| [s10 频率本源](../01_systems/s10_frequency_helix_ontology/README.md) | candidate_theory | 振动/频率（螺旋是轨迹） | A1–A3 | c 为**上限** v≤c | 原著 2026 | 无 | [postulates](../01_systems/s10_frequency_helix_ontology/02_assumptions/postulates.md) |
| [s11 GMUFT 几何耦合](../01_systems/s11_gmuft_geometric_coupling/README.md) | candidate_framework | 四几何自由度 | A1–A4 | 不涉及 | 全维分析 | 无（场方程 OPEN） | [postulates](../01_systems/s11_gmuft_geometric_coupling/02_assumptions/postulates.md) |
| [s12 空间光速螺旋](../01_systems/s12_light_speed_helix/README.md) | candidate_theory | 空间以光速螺旋运动 | A1–A4（含借用 S02） | v≡c 恒等约束 | v6.0-20260906 | 仅人工场设计级 | [postulates](../01_systems/s12_light_speed_helix/02_assumptions/postulates.md) |

## 2. 最易混淆的五组

1. **s10 vs s12（都叫"螺旋"）**：s10 本体是振动/频率，螺旋是振动轨迹，c 是上限 `v ≤ c`；s12 本体是空间以光速运动，c 是恒等约束 `v ≡ c`。共用 `√(κ²+τ²)=ω/c` 骨架，但互不认证。
2. **s07 vs s08（GAQ v4 vs v5）**：同一复曲率本体，关键差异是 c、ħ、e 的地位——v4 为三条公理常数，v5 把 c、ħ 降为几何桥梁、e 降为导出量。这是版本演进而非独立体系。
3. **s06 vs s09（代结构两版）**：都用 `π₃(SU(3))×ℤ₂^chiral=6`；s06 用 Cl(4,4) 边界态，s09 用 SO(3) 本征方向。同谱系不同阐述。
4. **s01 vs s12/s10（数学 vs 本体）**：s01 是纯数学框架，三重奏 `κ²+τ²=(ω/v)²` 是导出定理而非公设；s12/s10 借用数学语言但各自主张本体，数学成立不转移证据。
5. **s02 vs s12（统一力方程）**：s12 借用 s02 的 `P=m(c−v)`、`F=dP/dt`（登记为 S12-A4 借用项），但 s02 不主张几何本体。

## 3. 诚实结论（跨体系）

- **失效阈值几乎全缺**：16 个体系中，仅 s12 的人工场条目有原文阈值（5 预言 / 4 证伪）；其余公设均无独立可证伪条件，当前只能作 conjecture 登记。
- **GAQ 谱系是重灾区**：s03→s07→s08→s09 是同一研究的 v1→v4→v5→v6 演进，公设地位（尤其 c/ħ/e）逐版变化。按原始假设各自归属，不得假设版本间公设"完全相同"。
- **p01–p04 是方向占位**：无公设、无证据，不构成体系，仅供后续建模立项。
- **均未经独立复现**：各体系数值精算多属代数恒等与 CODATA 回算，仓库内 `07_computation/runs` 普遍空缺，证据等级不应高于 conjecture / numerical_check（未复现）。
