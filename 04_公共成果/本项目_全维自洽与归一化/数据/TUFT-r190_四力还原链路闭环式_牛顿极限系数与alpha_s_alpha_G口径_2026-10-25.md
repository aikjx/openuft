# TUFT-r190_四力还原链路闭环式_牛顿极限系数与alpha_s_alpha_G口径_2026-10-25

**条目 29（PASS 17 / FAIL 4 / BOUNDARY 2 / INFO 6 / CORRECTED 0）；守卫 35/35；控制组 12/12；退出码 0**

## 一句话

四力还原链路闭环式审计：四条终式全部机读成立——泊松方程 ∇²Φ=4πGρ（两条独立路线都落到 4πG）、水星 42.98″/世纪、光线偏折 1.751″、G_F/√2=g2²/(8m_W²)=1/(2v²)（相对差 <1E−40）、R_weak=2.455E−18 m、R_π=1.414 fm、M_Pl/M_Z=1.34E17。**四处 FAIL**：(A) 牛顿极限中间式混用 G_00 与 R_00 两种形式（两个 2× 互消，终式因此仍对，但标签必须改）；(B) 光子质量 1E−18 eV 被挂到「银河尺度」检验（1E−18 eV 对应 1.3 AU，银河尺度应 ~6E−27 eV）；(D) α_s 单圈公式配两圈 Λ=213 MeV，机器 0.13525≠0.1180（单圈自洽 Λ=87.8 MeV，两圈极点 243 MeV）；(E) α_G 来料 5E−33 与 5.58E−35 差约 90×（10⁻³³ vs 10⁻³⁵，两个指数）。另 2 条 BOUNDARY（α 树级网 132.17 的能标口径、α_s 阶次）。四扇区全部 C1，TUFT 供给 0/12 不变。

## 条目

| 编号 | 级 | 标题 |
|---|---|---|
| A01 | FAIL | 牛顿极限中间式混用 G_00 与 R_00 两种形式：两处标签错、两个 2× 互消（F-label） |
| A02 | PASS | 终式自洽：∇²Φ=8.38717274E-10ρ 与 κ²=8πG/c⁴ 定标同位 |
| A03 | PASS | 水星近日点进动：6πGM/(a(1−e²)c²)=1.03517E-1″/轨 ⇒ 4.29807E+1″/世纪（来料 42.98） |
| A04 | PASS | 太阳光线偏折：4GM/(c²R☉)=1.751190E+0″（来料 1.751） |
| A05 | PASS | 引力红移 Δν/ν=GM/(c²r)：太阳 2.122503E-6、地球表面 6.961311E-10、Pound–Rebka gH/c²=2.455058E-15 |
| A06 | PASS | 引力波：□h̄=−16πG/c⁴·T 与 P=G/5c⁵⟨Q⃛Q⃛⟩ 的量纲逐位闭合 |
| A07 | INFO | §1.3「ECSK 挠率非传播 ⇒ 极化仍两种」不可机算，登记为结构断言 |
| B01 | PASS | 规范对角化与本征结构：det M²=0（m_A=0）、m_Z=9.11876000E+1 GeV、旋转矩阵与来料逐字一致 |
| B02 | PASS | 麦克斯韦还原的结构分解成立：非齐次来自变分、齐次来自 Bianchi（无多余假设） |
| B03 | PASS | 库仑定律与 1/r²：∇²(1/r)=−4πδ³(𝐫) 的球面通量机读精确 −4π ⇒ V=e/(4πr) |
| B04 | BOUNDARY | §2.4 关系 α=g2²sin²θ_W/4π 成立，但用实测输入反解给 α^{-1}=1.321678E+2（两端 α 都不等于） |
| B05 | FAIL | §2.3 把「m_γ<1E−18 eV」与「银河磁场尺度」配对：量级差 9 个数量级（F-label/F-scale） |
| C01 | PASS | G_F/√2 = g2²/(8m_W²) = 1/(2v²) 三重恒等：机器相对差 <1E−40 |
| C02 | PASS | 来料算术复核：0.42603/(8×6460.5)=8.242977E-6，来料写 8.2455E−6（相对 5.5366E-4，舍入级） |
| C03 | PASS | 弱力力程：R_weak=ħ/(m_W c)=2.455018E-18 m（来料 2.454E−18） |
| C04 | PASS | §3.5「Z 对电子的矢量耦合几乎为零」在 PDG 归一化下成立（−0.0376，为 g_A 的 7.5%），在 T₃/2−Qs² 归一下不成立（−0.2688，53.8%） |
| C05 | PASS | Proca 型方程的量纲与项数：∂_μW^{−μν}+m_W²W^{−ν}=g2 j^{−ν} 三项同维 |
| C06 | INFO | §3.4 宇称破缺（V−A）为结构后果，不可机算；本册只登记 |
| D01 | FAIL | §4.2 把单圈公式与两圈口径的 Λ=213 MeV 混配：机器 α_s=1.352524E-1 ≠ 0.1180（F-label/F-scale） |
| D02 | BOUNDARY | 阶次未标注是根因：单圈极点 8.78271E+1 MeV vs 两圈极点 2.43180E+2 MeV，来料 213 MeV 贴近后者（1.14×） |
| D03 | PASS | 渐近自由的符号链：b0=23/3>0 ⇒ β(g)<0 ⇒ α_s 随能标下降 |
| D04 | PASS | 核力力程：ħ/(m_π c)=1.41382E+0 fm（来料 1.4 fm） |
| D05 | INFO | §4.3 禁闭/质量隙的「未解决」声明属实且本册不检验 |
| E01 | PASS | α₂=α_em/sin²θ_W=3.380137E-2（来料 0.0338）；α₁=(5/3)α_Y=1.694363E-2（来料 0.0169，GUT 归一） |
| E02 | FAIL | §5 引力强度 α_G~5E−33 与机器 G M_Z²/(ħc)=5.578512E-35 差 8.963E+1×（F-exp） |
| E03 | PASS | 层级比 M_Pl/M_Z=1.338877E+17（来料 ~1E17，同量级） |
| E04 | INFO | 三判定：四扇区全部 C1（TUFT 侧独立数值供给 = 0） |
| E05 | INFO | 缺陷族登记：本册新增 F-label 3 条（牛顿 G/R 混标、光子质量尺度、α_s 阶次）+ F-exp 1 条（α_G） |
| E06 | INFO | 本卷红线与产出定性 |

## 三判定

| 探针 | 判定 | 理由 |
|---|---|---|
| UFE-1/(E) 引力 | **C1** | GR 含挠改写；弱场/Schwarzschild 三检验皆为 GR 复算，无 TUFT 独立读数 |
| UFE-1/(YM)U(1) 电磁 | **C1** | 麦克斯韦四式为 (YM) 重写；α 明确声明「不能推导」 |
| UFE-1/(YM)SU(2)+(H) 弱 | **C1** | G_F 与 v 互为改写；m_W/m_Z 为输入；无新增预言 |
| UFE-1/(YM)SU(3) 强 | **C1** | 渐近自由为 QCD 既有结果；Λ 为输入；禁闭自认未解决 |

## 守护（35/35）

- [OK] G01 weak_field_trace
- [OK] G02 lhs_is_G00_not_R00
- [OK] G03 source_trace_factor
- [OK] G04 poisson_4piG
- [OK] G05 kappa2_si
- [OK] G06 mercury_per_orbit
- [OK] G07 mercury_per_century
- [OK] G08 light_deflection
- [OK] G09 redshift_sun
- [OK] G35 pound_rebka
- [OK] G10 gw_equation_dim
- [OK] G11 quadrupole_power_dim
- [OK] G12 mixing_orthogonal
- [OK] G13 mass_eigen_zero
- [OK] G14 mZ_from_eigen
- [OK] G15 coulomb_green
- [OK] G16 alpha_scheme
- [OK] G17 photon_range_1e18
- [OK] G18 galactic_limit
- [OK] G19 gf_identity
- [OK] G20 doc_arithmetic_gf
- [OK] G21 r_weak
- [OK] G22 gV_electron_pdg
- [OK] G23 proca_dim
- [OK] G24 beta_coeffs
- [OK] G25 alpha_s_lo_213
- [OK] G26 lo_lambda_required
- [OK] G27 two_loop_pole
- [OK] G28 pole_separation
- [OK] G29 asympt_free
- [OK] G30 r_pi
- [OK] G31 alpha2
- [OK] G32 alpha1
- [OK] G33 alpha_G
- [OK] G34 planck_ratio

## 控制组（12/12）

- [OK] K01 mercury_42p98 =4.298071E+1″/世纪
- [OK] K02 deflect_1p751 =1.751190E+0″
- [OK] K03 kappa2_2p0766e-43 =2.07664744E-43
- [OK] K04 alpha_tree_132p17 α^-1=1.321678E+2
- [OK] K05 gf_8p2476e-6 G_F/√2=8.24754288E-6
- [OK] K06 rweak_2p455e-18 R=2.455018E-18
- [OK] K07 alpha_s_lo_0p1353 α_s=1.352524E-1
- [OK] K08 lambda_lo_88p1 Λ_LO=8.78271E+1 MeV
- [OK] K09 alpha_g_5p58e-35 α_G=5.578512E-35
- [OK] K10 planck_1p34e17 比=1.338877E+17
- [OK] K11 alpha2_0p0338 α₂=3.380137E-2
- [OK] K12 gV_e_m0p0376 g_V^e=-3.75600E-2

## 红线

本册只做闭环式复算与结构性判定，不产生新物理，不宣称观测证实/否证；未改写任何来料字节；未改 verify.py；未做 git 操作。TUFT 供给 0/12 维持。
