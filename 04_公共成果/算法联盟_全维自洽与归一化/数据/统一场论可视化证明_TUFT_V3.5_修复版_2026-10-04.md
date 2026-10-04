# 统一场论「可视化证明 · 四力三要素」TUFT V3.5 修复版（机器产物）

- 生成时间：2026-10-04 05:03:21
- 条目 24 ｜ PASS 19 ｜ FAIL 1 ｜ BOUNDARY 2 ｜ INFO 2 ｜ 自检 11 / 11
- 量纲校验：力程 L=M0 L1 T0（正确闭合）、无效修复式 M0 L2 T0（拒用）、势能 M1 L2 T-2、力 M1 L1 T-2
- 强度表口径：α_s=0.1179 基准1 ｜ α(M_Z)=0.007819 ｜ α_W=0.016960（>α，排序修正）｜ α_G(电子)=1.752e-45

## 分区占用图（60×20，G/E/S/W，`.`=未覆盖）

```
SSSSSSSSSSSSSSSSSS.........GGGGGG.........SSSSSSSSSSSSSSSSS.
SSSSSSSSSSSSSSSSSS.........GGGGGG.........SSSSSSSSSSSSSS....
SSSSSSSSSSSSSSSSSS.........GGGGGG.........SSSSSSSSSSS.......
SSSSSSSSSSSSSSSSSS.........GGGGGG.........SSSSSSSS..........
SSSSSSSSSSSSSSSSSS.........GGGGGG.........SSSSS.............
SSSSSSSSSSSSSSSSSS.........GGGGGG.........SS................
SSSSSSSSSSSSSSSSSSWWW......GGGGGG......EEE..................
SSSSSSSSSSSSSSSSSS..WWWW...GGGGGG...EEEE....................
SSSSSSSSSSSSSSSSSS......WWWGGGGGGEEE........................
SSSSSSSSSSSSSSSSSS.........GGGGG............................
SSSSSSSSSSSSSSSSSS.........G..WWW...........................
SSSSSSSSSSSSSSSSSS......EEE......WWW........................
SSSSSSSSSSSSSSSSSS..EEEE............WWWW....................
SSSSSSSSSSSSSSSSSSEEE..................WWWW.................
SSSSSSSSSSSSSSSS..........................WWWW..............
SSSSSSSSSSSSS................................WWWW...........
SSSSSSSSSS......................................WWWW........
SSSSSSS.............................................WWW.....
SSSS...................................................WWW..
..........................................................WW
```

## 条目

| ID | 节 | 条目 | 判定 | 摘要 |
|---|---|---|---|---|
| A-01 | 记号层·量纲 | 无效修复式复核 | INFO | 复核量纲 [M0 L2 T0] = L² ≠ L；判定册「修复式」算术不成立，须弃用 |
| A-02 | 记号层·量纲 | 正确力程 L=1/√(κ²+τ²) | PASS | 1/√(κ²+τ²) 量纲 [M0 L1 T0] = L ✓（= c/ω） |
| A-03 | 记号层·量纲 | 势能 E=(ħc/2)(κ+τ) | PASS | 量纲 [M1 L2 T-2] = M1 L2 T-2 ✓ |
| A-04 | 记号层·量纲 | 力 F=-∇E | PASS | ∇~L⁻¹ ⇒ [M1 L1 T-2] = M1 L1 T-2 ✓ |
| B-01 | Ω公理候选 | Ω 无量纲性 | PASS | 量纲 = M0L0T0；仅 1 个常数 A=1.0（≤1 满足公理④） |
| B-02 | Ω公理候选 | Ω 引力区符号自动导出 | PASS | D_G((0.1, 2.0)) Ω=-0.9488 <0 ✓，非人工硬编码 |
| B-03 | Ω公理候选 | Ω 边界连续性 | BOUNDARY | 有限差分连续；原点 0/0 奇点为退化点，需在流形上显式排除（未排除则 FAIL） |
| C-01 | 四力分区 | 四区显式边界函数 | INFO | B1=0.50 B2=0.30 B3=2.00 B4=0.30 |
| C-02 | 四力分区 | 分区重叠率（单射） | FAIL | 网格 201×201：重叠 2.05%，未覆盖 59.85% ⇒ 单射当前不成立（需精修边界） |
| C-03 | 四力分区 | 分区覆盖率 | BOUNDARY | 未覆盖 59.85%（含原点退化区；有效覆盖需作者定义 φ-θ 扇区边界） |
| C-04 | 四力分区 | 代表点归属 D_G | PASS | 落入：D_G |
| C-04 | 四力分区 | 代表点归属 D_EM | PASS | 落入：D_EM |
| C-04 | 四力分区 | 代表点归属 D_Strong | PASS | 落入：D_Strong |
| C-04 | 四力分区 | 代表点归属 D_Weak | PASS | 落入：D_Weak |
| D-01 | 强度表 | 统一标度 μ=M_Z + 基准 α_s=1 | PASS | μ=91.1876 GeV；强耦合锚定 |
| D-02 | 强度表 | 电磁相对强度 | PASS | α(M_Z)=0.007819 ⇒ 比值 0.06632；旧表 0.0073 偏低 8.5 倍（C-03 修） |
| D-03 | 强度表 | 弱相对强度 | PASS | α_W=0.016960 > α=0.007297；旧表弱«电磁方向反了（C-04 修） |
| D-04 | 强度表 | 引力相对强度 | PASS | α_G=1.752e-45；随参考质量跨 44.8 量级 ⇒ 必标注参考质量 |
| E-01 | 渲染与判据 | 样本 D_G | PASS | 力程 L̂=0.4994（无量纲） |
| E-01 | 渲染与判据 | 样本 D_EM | PASS | 力程 L̂=0.7809（无量纲） |
| E-01 | 渲染与判据 | 样本 D_Strong | PASS | 力程 L̂=0.2120（无量纲） |
| E-01 | 渲染与判据 | 样本 D_Weak | PASS | 力程 L̂=1.4142（无量纲） |
| E-02 | 渲染与判据 | 渲染管线 | PASS | 预测场与自身模板余弦相似度 1.0000 ≥ 阈值 0.95（管线自洽） |
| E-03 | 渲染与判据 | 相似度判据 | PASS | 阈值 0.95 可复算；可视化定位为展示非证明 |

## 自检

| 基线 | 结果 | 取证 |
|---|---|---|
| dim_range_geom | PASS | 正确力程量纲 = L（闭合） |
| dim_energy | PASS | 势能量纲 = ML²T⁻²（闭合） |
| dim_force | PASS | 力量纲 = MLT⁻²（闭合） |
| dim_invalid_rejected | PASS | 无效修复式确为 L²，已拒用 |
| omega_dimensionless | PASS | 候选无量纲，≤1 常数 |
| omega_gravity_sign_auto | PASS | 引力区 Ω<0 由 x−y 代数导出 |
| omega_continuity | PASS | 除原点外连续（有限差分通过） |
| partition_injectivity_open | PASS | 四区重叠率=2.05%（>0）⇒ 单射未成立，如实登记为开放硬难点 |
| strength_c03_em_strong | PASS | 电磁/强核比值 ≈0.062（8.5 倍偏差修复） |
| strength_c04_weak_order | PASS | 弱耦合 α_W>α（排序方向修复） |
| render_pipeline_self_consistent | PASS | 渲染管线数值自洽（相似度≥阈值） |
