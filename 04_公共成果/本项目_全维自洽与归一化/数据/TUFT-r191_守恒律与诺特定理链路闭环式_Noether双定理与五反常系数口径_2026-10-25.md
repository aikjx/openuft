# TUFT-r191_守恒律与诺特定理链路闭环式_Noether双定理与五反常系数口径_2026-10-25

**条目 27（PASS 19 / FAIL 1 / BOUNDARY 1 / INFO 6 / CORRECTED 0）；守卫 35/35；控制组 22/22；退出码 0**

## 一句话

守恒律卷闭环式审计：Noether 第一定理的**在壳性**与第二定理的**离壳性**都被机器分开——双模在壳叠加 ∂·J=0（<1E−200），把第二模偏壳 δ ⇒ ∂·J=2δ·Im(φ*a₂E₂) 逐位吻合；阿贝尔「反对称 F × 对称 ∂∂」与 su(2) Jacobi（243 组）精确 0；线性化收缩比安基 k^μG^(1)_{μν}≡0（有理精确，删迹负对照非零）；实标量 ∂^μT_μν=(□φ−m²φ)∂_νφ 在壳 0。五个反常系数独立重算全零（Fraction），U(1)_em 的 ΣQ³=0、ΣQ=0，超荷被反常条件定到**1 维射线 × Z₂**（u↔d）。**一处 FAIL**：§3.2 自旋流恒等式与同页总角动量式按同一 s 展开相差 **−2**（应为 ∇̃_λs^{λμν}=−2T_{[μν]}，来料写 +T_{[μν]}）。**一处 BOUNDARY**：§3.5「B−L 严格守恒（反常自由）」在最小 SM（无 ν_R）不成立——(B−L)³=−1、[grav]²(B−L)=−1；sphaleron 保 B−L 的那部分成立（SU(2)²B=SU(2)²L=1/2），加一个 ν_R 后两通道归零。§5 总表 10 行机读 10/10。四扇区 C1，TUFT 供给 0/12 不变。

## 条目

| 编号 | 级 | 标题 |
|---|---|---|
| A01 | PASS | 第一定理在壳守恒：双模在壳叠加 ∂·J=0（恒等式路线 <1E−200），差分路线受 h² 截断限 |
| A02 | PASS | 第一定理的在壳性负对照：第二模偏壳 δ=k²+m² ⇒ ∂·J=2δ·Im(φ*a₂E₂)（机器预测逐位吻合） |
| A03 | PASS | 第二定理（阿贝尔）离壳恒等：任意反对称 F ⇒ ∂_ν∂_μF^{μν} ≡ 0（有理精确 0） |
| A04 | PASS | 第二定理（非阿贝尔）代数核：su(2) Jacobi 恒等 243 组指标全零 ⇒ D_νE^ν ≡ 0 离壳 |
| A05 | PASS | 线性化收缩比安基：k^μG^(1)_{μν}(k) ≡ 0（任意有理 h、k 精确 0）；删迹项负对照非零 |
| A06 | INFO | 计数：4 个微分同胚参数 ξ^μ ↔ 4 条收缩比安基恒等式（不是 1 条、也不是 10 条） |
| B01 | PASS | §3.1 在壳能量–动量守恒：∂^μT_μν=(□φ−m²φ)∂_νφ（机器双路线），在壳 0、偏壳 ∝δ |
| B02 | FAIL | §3.2 自旋流恒等式与总角动量式按同一 s 展开相差因子 −2：∇̃_λs^{λμν}=−2T_{[μν]}，来料写 +T_{[μν]}（F-sign/F-factor） |
| B03 | PASS | §3.3 SU(3)_C：A_[SU(3)]³=0（精确），局域 SU(N) 无反常 ⇒ 色荷守恒 |
| B04 | PASS | §3.4「超荷只差一个整体尺度」：线性条件秩 3（零空间 2 维）+ 三次条件 ⇒ 1 维射线 × Z₂（u↔d） |
| B05 | BOUNDARY | §3.5 B−L：sphaleron 保 B−L 成立（SU(2)²B=SU(2)²L=1/2），但「反常自由」在最小 SM 不成立：(B−L)³=−1、[grav]²(B−L)=−1 |
| B06 | PASS | §3.5 sphaleron 系数口径：∂·(j_B+j_L)=3g₂²/16π²·W W̃ ⇔ N_g·g₂²/16π²，N_g=3 |
| B07 | PASS | §3.6 U(1)_em 反常自由：Σ Q³=0、Σ Q=0（分量级精确） |
| B08 | INFO | §3.7 C/P/T 与 CPT：C、P、T 的破缺为结构后果；CPT 定理为不可机算的定理层陈述 |
| B09 | PASS | §3.7 T 破缺定量：CKM 相位 δ=1.196 rad（来料 ≈1.2）、Jarlskog J=3.078E−5 ≠ 0 |
| C01 | PASS | A_[SU(3)]³ = 2(+1)+1(−1)+1(−1) = 0（机器独立重算） |
| C02 | PASS | A_[SU(3)]²U(1) = 1/6−1/3+1/6 = 0（机器独立重算） |
| C03 | PASS | A_[SU(2)]²U(1) = 1/4−1/4 = 0（机器独立重算） |
| C04 | PASS | A_[U(1)]³ = 1/36−8/9+1/9−1/4+1 = 0（机器独立重算） |
| C05 | PASS | A_[grav]²U(1) = 1−2+1−1+1 = 0（机器独立重算） |
| C06 | PASS | 推论 4.1 代数电荷中性：两条路线（物理粒子计数 / 左手分量多重数）都给 0 |
| C07 | PASS | 推论 4.2 第 4 代在反常上同样合法：N_g 整倍 ⇒ 五系数 = N_g×0 = 0 |
| C08 | INFO | 交叉：反常消去与超荷唯一性同源（B04/C02–C05），非两条独立公设 |
| D01 | PASS | §5 守恒律状态总表：10 行机读、10 个守恒量全部在表内、§3 恰 7 个小节 |
| D02 | INFO | 三判定：四扇区全部 C1（守恒层不产生新的独立数值供给） |
| D03 | INFO | 缺陷族登记：本册新增 F-sign/F-factor 1 条（B02 自旋流系数 −2）+ 口径 1 条（B05 B−L 括注） |
| D04 | INFO | 本卷红线与产出定性 |

## 三判定

| 探针 | 判定 | 理由 |
|---|---|---|
| UFE-1/(E) 引力 | **C1** | 守恒层是 ∇̃_μT^μν=0 与比安基恒等，皆为 GR/ECSK 既有结构；无 TUFT 独立数值 |
| UFE-1/(YM)U(1) 电磁 | **C1** | U(1)_em 反常自由是 SM 既有结果；本册只复算 ΣQ³=0 |
| UFE-1/(YM)SU(2)+(H) 弱 | **C1** | sphaleron 系数与 B−L 存活为 SM 既有结论；无反常数新预言 |
| UFE-1/(YM)SU(3) 强 | **C1** | SU(3)³ 为零是群论定理，非 TUFT 供给 |

## 守护（35/35）

- [OK] G01 onshell_divergence_machine_zero
- [OK] G02 offshell_prediction_exact
- [OK] G03 fd_matches_identity
- [OK] G04 abelian_identity_exact
- [OK] G05 abelian_negative_control
- [OK] G06 su2_jacobi_all_zero
- [OK] G07 linearized_bianchi_zero
- [OK] G08 linearized_bianchi_negative
- [OK] G09 Tdiv_onshell_zero
- [OK] G10 Tdiv_prediction_agree
- [OK] G11 Tdiv_offshell_nonzero
- [OK] G12 spin_current_ratio_minus2
- [OK] G13 anomaly_su3_cube
- [OK] G14 anomaly_su3_sqY
- [OK] G15 anomaly_su2_sqY
- [OK] G16 anomaly_Y_cube
- [OK] G17 anomaly_grav_Y
- [OK] G18 Q_cube_zero
- [OK] G19 Q_sum_zero
- [OK] G20 BL_grav_minus_one
- [OK] G21 BL_cubic_minus_one
- [OK] G22 nuR_cancels_BL
- [OK] G23 sphaleron_coefficient
- [OK] G24 hypercharge_rank
- [OK] G25 hypercharge_branches
- [OK] G26 charge_neutrality_two_routes
- [OK] G27 generation_scaling
- [OK] G28 conservation_table_rows
- [OK] G29 sec3_subsections_seven
- [OK] G30 doc_readable_and_claims
- [OK] G31 fail_entries_have_numbers
- [OK] G32 verdict_driven_by_counts
- [OK] G33 no_decimal_in_exact_algebra
- [OK] G34 jarlskog_nonzero
- [OK] G35 delta_close_to_doc

## 控制组（22/22）

- [OK] K01 onshell_divJ_zero |∂·J|=1.200000E-249
- [OK] K02 offshell_divJ_1e-3 |∂·J|=1.781884E-3
- [OK] K03 divJ_linear_in_delta |∂·J(δ)|/|∂·J(2δ)| = 5.000000000000E-1（期望 0.5）
- [OK] K04 divJ_pred_resid 残差=1.452000E-249
- [OK] K05 divJ_fd_agrees 差=1.174677E-41
- [OK] K06 abelian_zero S=0
- [OK] K07 abelian_bad_nonzero S_bad=15/14
- [OK] K08 jacobi_nonzero_zero nz=0
- [OK] K09 bianchi_zero divG=0, 0, 0, 0
- [OK] K10 bianchi_notrace_nonzero divGnt=-9413/14700, -9413/36750, 9413/34300, -9413/29400
- [OK] K11 Tdiv_onshell_zero max=3.366241E-250
- [OK] K12 Tdiv_pred_agree 残差=3.379954E-41
- [OK] K13 anomaly_all_zero 五系数=0, 0, 0, 0, 0
- [OK] K14 Q3_zero ΣQ³=0
- [OK] K15 Qsum_zero ΣQ=0
- [OK] K16 BL_grav_minus1 gravBL=-1
- [OK] K17 BL_cubic_minus1 cubicBL=-1
- [OK] K18 nuR_fixes grav=0 cubic=0
- [OK] K19 rank3_nullity2 rank=3 nullity=2
- [OK] K20 jarlskog_3e-5 J=3.081415E-5
- [OK] K21 delta_1p196 δ=1.196000E+0
- [OK] K22 table_rows_10 rows=10

## 红线

本册只做闭环式复算与结构性判定，不产生新物理，不宣称观测证实/否证；未改写任何来料字节；未改 verify.py；未做 git 操作。TUFT 供给 0/12 维持。
