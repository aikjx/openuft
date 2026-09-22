# 实现方式档案：GAQ 谱系 v1→v6

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
