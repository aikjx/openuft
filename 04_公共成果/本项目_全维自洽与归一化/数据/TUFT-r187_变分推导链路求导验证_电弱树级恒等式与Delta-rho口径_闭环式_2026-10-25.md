# TUFT-r187_变分推导链路求导验证_电弱树级恒等式与Delta-rho口径_闭环式_2026-10-25

**条目 21（PASS 15 / FAIL 1 / BOUNDARY 2 / INFO 3 / CORRECTED 0）；守卫 21/21；控制组 12/12；退出码 0**

## 一句话

变分推导链路（求导证明）闭环式审计：量纲与自然单位账全过；Higgs 势一阶导在真空处机器零、二阶导 = 2λv² = m_h²（解析+差分互证）；质量矩阵本征分解给 m_γ=0 精确、m_Z=91.19；电弱树级五恒等式（v=246.2196、λ=0.12938、sin²θ_W=0.2232、ρ_tree=1）逐项闭合，但树级网反解的 α^{-1}=132.1 落在 137.036 与 127.95 之间（口径边界）。**FAIL**：推论 4.3 把 Δρ_t=0.00935 挂到 PDG ρ_0−1=0.00038 上（24.6× 不符）——改用 MS-bar sin²θ_W 后 ρ=1.010625 ≈ 1+Δρ_t（1.27E−3），证明 Δρ_t 属 MS-bar 口径、不解释 Z-pole 的 1.00038。四费米子 3/8 vs 3/16 差因子 2，登记约定边界。TUFT 供给 0/12 不变。

## 条目

| 编号 | 级 | 标题 |
|---|---|---|
| A01 | PASS | 量纲门禁：κ²=8πG/c⁴ 与 κ²T_μν 回到曲率 L^-2 |
| A02 | PASS | 自然单位（ħ=c=1）能量幂账：G_F/v/κ²/G/T/λ/ρ 全部对齐 |
| B01 | PASS | v=(√2G_F)^{-1/2}=2.462196508E+2 GeV（推论 4.1 的数值位） |
| B02 | PASS | 真空条件：dV/dh\|₀ = 0（机器零），对应 \|H\|²=μ²/(2λ) |
| B03 | PASS | 二阶导：d²V/dh²\|₀ = 2λv² = m_h²（解析与差分互证） |
| B04 | PASS | λ=m_h²/(2v²)=1.29383844E-1（来料写 0.129，四位内一致） |
| B05 | PASS | 自洽闭环：m_h = √2 μ（μ=√λ v=8.85651243E+1 GeV） |
| C01 | PASS | 质量矩阵本征分解：m_γ=0（机器零）、m_Z=9.11876000E+1 GeV |
| C02 | PASS | m_W=g2v/2 ⇒ 由实测 m_W 反解 g2=6.52888587E-1 |
| C03 | PASS | sin²θ_W 两路口径精确同值：2.23051891E-1 = 1−m_W²/m_Z² |
| C04 | PASS | ρ_tree = 1 精确（机器零）——但这是代数恒等，不是 custodial 的证据 |
| C05 | BOUNDARY | 树级网反解的 α^{-1}=1.321678E+2 既不等于 α^{-1}(0)=137.036，也不等于 α^{-1}(m_Z)=127.95 |
| C06 | FAIL | Δρ_t=0.00935 与 PDG ρ_0−1=0.00038 相差 24.6 倍 ⇒ 两者不是同一口径（F-label） |
| C07 | PASS | 口径归一：改用 MS-bar sin²θ_W 后 ρ=1.010625E+0 ≈ 1+Δρ_t（相对差 1.2677E-3）⇒ Δρ_t 的归属被定位 |
| D01 | PASS | (C) 的系数链自洽：1/(4κ²)×2 → 1/(2κ²)，再取变分任意 ⇒ (1/2)εTe=κ²s |
| D02 | BOUNDARY | 四费米子接触项系数 3/8 vs 3/16：差恰好因子 2，属约定未定 |
| D03 | PASS | (YM) 的符号链与电流协变守恒：D_ν j^{aν}=0 是方程推论 |
| D04 | INFO | 三判定：本卷三扇区全部 C1（TUFT 侧独立数值供给 = 0） |
| D05 | INFO | 缺陷族补充：F-label 新增成员（Δρ_t 挂错对照量）；F-scale 同案 |
| E01 | PASS | a_e=α/2π=1.1614097E-3，与实测 1.1596522E-3 差 1.5156E-1%（来料写 0.15%，一致） |
| E02 | INFO | 本卷红线与产出定性 |

## 三判定

| 探针 | 判定 | 理由 |
|---|---|---|
| UFE-1/(C) Cartan torsion | **C1** | 标准 ECSK 代数方程；TUFT 侧无新增数值预言 |
| UFE-1/(E) Einstein-Cartan | **C1** | GR 的含挠改写；s=0 时与 GR 逐字同构，无独立读数 |
| UFE-1/(YM)(H)(D) | **C1** | SM 三式重写；所有数值（v,λ,m_W,m_Z,α）皆为标准常数反演 |

## 守护（21/21）

- [OK] G01 kappa2_dim
- [OK] G02 kappa2_T_is_curvature
- [OK] G03 kappa2_value
- [OK] G04 natural_power_ledger
- [OK] G05 v_from_GF
- [OK] G06 lambda_value
- [OK] G07 vacuum_condition_zero
- [OK] G08 second_deriv_matches
- [OK] G09 mh_squared
- [OK] G10 mu_relation
- [OK] G11 mass_matrix_mZ
- [OK] G12 mass_matrix_mgamma0
- [OK] G13 sin2_identity
- [OK] G14 rho_tree_one
- [OK] G15 alpha_tree_value
- [OK] G16 drho_value
- [OK] G17 drho_vs_pdg_dev
- [OK] G18 rho_msbar_vs_drho
- [OK] G19 cartan_coeff_chain
- [OK] G20 fourfermion_ratio
- [OK] G21 ae_value

## 控制组（12/12）

- [OK] K01 v_246 v=2.46219651E+2
- [OK] K02 lambda_0p129 λ=1.29383844E-1
- [OK] K03 mh2_15688 m_h²=1.56875625E+4
- [OK] K04 yukawa_ok dV0=-1.000E-243
- [OK] K05 fd_close rel=4.1238E-86
- [OK] K06 g2_0p65 g2=6.52888587E-1
- [OK] K07 mZ_91p19 mZ=9.11876000E+1
- [OK] K08 sin2_0p223 sin2=2.23051891E-1
- [OK] K09 alpha_inv_band α^-1=1.321678E+2
- [OK] K10 drho_0p0094 Δρ=9.34524053E-3
- [OK] K11 rho_ms_1p01 ρ_MS=1.01062477E+0
- [OK] K12 ae_1p161e-3 a_e=1.16140973E-3

## 红线

本册只做闭环式复算与结构性判定，不产生新物理，不宣称观测证实/否证；未改写任何来料字节；未改 verify.py；未做 git 操作。TUFT 供给 0/12 维持。
