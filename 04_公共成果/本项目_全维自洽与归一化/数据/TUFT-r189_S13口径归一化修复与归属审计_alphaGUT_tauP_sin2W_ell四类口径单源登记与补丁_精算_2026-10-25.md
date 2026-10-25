# TUFT-r189 · S13 口径归一化修复与归属审计

> 判词：`R189-CALIBRE-NORMALIZED-4-DEFECTS-REPAIRED-ALPHA-GUT-TIERS-0.187-5.562-6.778-PCT-CANONICAL-24.27645852-TAU-P-SPREAD-4.693-FACTORIZED-M4-4.978-ALPHA-0.897-ANCHOR-1.051-CANONICAL-3.421E36-SIN2W-IDENTITIES-3-8-IFF-A1EQ-A2-1-4-IFF-A1EQ-9-5A2-SAME-SCALE-13.5PCT-ELL-RENAMED-ELLEW-7.7305E-19-ELLP-RATIO-2.09E-17-PATHS-1TO3-STILL-OPEN-SUPPLY-0`
>
> 红线：数学自洽 ≠ 实验证实；记账修复 ≠ 物理闭合；路径 1–3 维持 OPEN；条目不可与 r142–r188 相加

## 一、口径分层（I1）

| 口径 | 值 | 协议 | 归属 | 状态 |
|---|---|---|---|---|
| A0 | 24 | ch25 手锚 ≈1/24 | 借用 SU(5) | DEPRECATED |
| A1 | 24.2764585242 | s* 三线闭式（精确输入） | 借用 MSSM β | CANONICAL |
| A2 | 24.32194824 | α₁=α₂ 交点（精确输入） | 借用 MSSM β | ALTERNATIVE |
| A3 | 25 | 卷三反推锚（M~2e16） | 借用 SU(5) | DEPRECATED |
| A4 | 25.626831814 | rge_sim 圆整输入 + RK4 | 借用 MSSM β | DEPRECATED |

分层极差：T0 精确 0.1874% / T1 圆整 5.562% / T2 手锚 6.778%

## 二、τ_p 口径（I2）

| 口径 | M (GeV) | α_GUT⁻¹ | τ_p (yr) | 状态 |
|---|---|---|---|---|
| T-anchor25 | 1.42000000e+16 | 25.00000000 | 7.288722e+35 | DEPRECATED |
| T-rgesim | 1.42000000e+16 | 25.62683181 | 7.658809e+35 | DEPRECATED |
| T-cross | 1.99047287e+16 | 24.32194824 | 2.663421e+36 | ALTERNATIVE |
| T-sstar | 2.12100038e+16 | 24.27645852 | 3.420989e+36 | CANONICAL |

展宽 4.6935× = M⁴ 4.977 × α⁻² 0.897 × 手锚 1.051（残差 8.9e-16）

## 三、sin²θ 尺度与内容（I3）

| 量 | 读数 |
|---|---|
| at_MZ | 0.23122000 |
| at_v | 0.23638579 |
| at_Mstar | 0.25 (精确) |
| Mstar_gev | 3675.242923 |
| at_2e16_SM | 0.42541334 |
| at_2e16_MSSM | 0.37504102 |
| same_scale_diff_pct | 13.431150927126238 |
| s38_scale_SM_gev | 1.023741e+13 |
| s38_scale_MSSM_gev | 1.990473e+16 |
| cross_vs_star_pct | 50.0 |

## 四、ℓ 三尺度

- **ell_P_m**：1.616255e-35
- **ell_EW_m**：7.730358e-19
- **ell_P_over_ell_EW**：2.0908e-17
- **ell_EW_over_ell_P**：4.7829e+16
- **ell_sd**：符号（M5 自对偶最短尺度），无框架数值
- **v_fit_gev**：255.262424
- **note**：v=ℓ⁻¹ 的 ℓ 是 ℓ_EW=ħc/v，非 ℓ_P；二者相差 4.78e16 倍

## 五、落地勘误

- 03_数学形式/equations.md：1 条，本次已存在（幂等）
- 13_论文与成果/书稿/正文/ch25-常数统一与电荷量子化.md：1 条，本次已存在（幂等）
- 04_理论推导/推导卷_对话产出/openuft_卷三_攻破收口_统一场论补全与可检验预言.md：2 条，本次已存在（幂等）
- 09_验证结果/候选预言验证_V2.0.md：1 条，本次已存在（幂等）

## 六、判词

`R189-CALIBRE-NORMALIZED-4-DEFECTS-REPAIRED-ALPHA-GUT-TIERS-0.187-5.562-6.778-PCT-CANONICAL-24.27645852-TAU-P-SPREAD-4.693-FACTORIZED-M4-4.978-ALPHA-0.897-ANCHOR-1.051-CANONICAL-3.421E36-SIN2W-IDENTITIES-3-8-IFF-A1EQ-A2-1-4-IFF-A1EQ-9-5A2-SAME-SCALE-13.5PCT-ELL-RENAMED-ELLEW-7.7305E-19-ELLP-RATIO-2.09E-17-PATHS-1TO3-STILL-OPEN-SUPPLY-0`
