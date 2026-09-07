# 按模块类型浏览

本文件由各体系 system.json 生成；主文件始终保留在独立体系目录。类型改变无需移动路径，ID 前缀不决定类型。

[扩展与最优性分析](../00_governance/SCALABILITY_REVIEW.md) · [独立体系总入口](README.md)。

| 类型 | 数量 | 职责 |
|---|---:|---|
| 数学框架 | 1 | 研究条件性数学结构、恒等式和证明，不自动提出新的物理本体。 |
| 物理理论候选 | 7 | 有原始本体或动力学主张的独立研究对象，成立性待检验。 |
| 待完备理论框架 | 1 | 已有结构性对应或机制纲领，但动力学或边界尚未完整建立。 |
| 组合候选 | 1 | 显式组合多个上游体系假设，并独立研究其兼容性。 |
| 扩展分支 | 2 | 从已有体系出发，改变基础输入或引入独立机制的研究分支。 |
| 待建模方向 | 4 | 有研究问题但尚未形成明确、冻结的具体公设与动力学。 |

## 数学框架

可供理论借用，但数学结果不能直接认证物理公设。

- [螺旋三重奏与谱几何](s01_triad_kinematics/README.md) · `unreviewed` · 曲线曲率、挠率及运动生成元；不自动引入统一场论本体

## 物理理论候选

需要公设版本和可检验预测；候选身份不是已验证状态。

- [张祥前空间运动与统一力](s02_zhang_space_motion/README.md) · `unreviewed` · 空间运动与 P=m(c-v)、F=dP/dt 的统一力假设
- [GAQ 几何原子与作用量子](s03_gaq_geometric_atom/README.md) · `unreviewed` · 离散几何元胞、作用量子化、曲率—能量对应及信息—质量对应
- [IEG 信息熵引力](s04_ieg_information_gravity/README.md) · `unreviewed` · 几何信息场、信息熵与引力动力学的联系
- [HDU 高维紧致化统一](s05_hdu_higher_dimensions/README.md) · `unreviewed` · 高维几何、紧致化及低维常数的投影关系
- [TCL 拓扑手征锁定](s06_tcl_topological_chirality/README.md) · `unreviewed` · 边界态、手征与费米子代结构的对应
- [频率本源与复螺旋宇宙](s10_frequency_helix_ontology/README.md) · `unreviewed` · 振动本体、作用量子及复曲率轨迹三项原理
- [空间光速螺旋统一体系](s12_light_speed_helix/README.md) · `unreviewed` · v≡c 空间光速螺旋本源公设（垂直原理、光速约束、螺旋参数化）及统一力方程 F=dP/dt, P=m(c−v)

## 待完备理论框架

不与拥有明确场方程的候选自动等同。

- [GMUFT 几何自由度与耦合](s11_gmuft_geometric_coupling/README.md) · `unreviewed` · 曲率、挠率、拖拽与引力—电磁对应；完整场方程待建立

## 组合候选

必须说明组合前提；上游各自结论不能自动转移。

- [GAQ 复曲率融合体系](s07_gaq_complex_curvature/README.md) · `unreviewed` · v4 复曲率 κ+iτ 及 IEG/HDU/TCL 组合假设

## 扩展分支

与不改变前提的普通文件版本区分，独立管理证据。

- [GAQ 常数几何化体系](s08_gaq_geometrized_constants/README.md) · `unreviewed` · v5 将 c、hbar 的独立地位改写为几何关系；与 v4 分开审查
- [GAQ 粒子质量谱体系](s09_gaq_mass_spectrum/README.md) · `unreviewed` · v6 代结构、质量比与 Yukawa/QCD 几何化探索

## 待建模方向

不能计为已建立理论；成熟后可改类型而保留原 ID。

- [空间压缩与密度本体](p01_space_compression/README.md) · `unformulated` · 保留原 H02 独立方向；具体公设尚未建立
- [物体驱动与源场本体](p02_matter_source/README.md) · `unformulated` · 保留原 H03 独立方向；不与张祥前统一力自动等同
- [规范对称统一候选](p03_gauge_unification/README.md) · `unformulated` · 保留原 H05 独立方向；需要具体群、表示和作用量
- [量子结构与时空涌现候选](p04_quantum_emergence/README.md) · `unformulated` · 保留原 H06 独立方向；需要微观自由度和动力学

类型描述研究对象，status 描述工作状态，证据类型记录在 claims.csv；三者不能相互替代。
