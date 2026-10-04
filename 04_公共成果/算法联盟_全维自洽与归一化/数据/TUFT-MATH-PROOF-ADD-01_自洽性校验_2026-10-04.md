# TUFT-MATH-PROOF-ADD-01 自洽性校验报告（分支 4）

- 引擎：源码/TUFT-MATH-PROOF-ADD-01_自洽性校验_2026-10-04.py（纯标准库）
- 日期：2026-10-04
- 分区：三正瓣（EM 0° / Strong 120° / Weak 240°，各 60°）+ G 三负瓣之并
- 读数：14 guard —— PASS 14 / FAIL 0（退出码 0）

| PASS | chiral_asymmetry_identically_zero | A_chiral = 0 （恒等于 0）→ 与「不对称来自干涉相位」自相矛盾 |
| PASS | interference_deltaA_nonzero | θ=225°, φ=-0.125, |Ω|=0.7071：奇项 −2|Ω|c_I sinφ = 0.1763 ≠ 0；纯实 c 时该奇项 = 0 ⇒ δA_TUFT 非零要求 c_I≠0 |
| PASS | parity_omega_star_needs_odd_phase | φ(225°)=-0.1250, φ(−225°)=0.0000, −φ(225°)=0.1250 ⇒ φ(−θ)≠−φ(θ) （差 -0.1250，θ_W,c=240°≠0）；仅 θ_W,c=0 时成立 |
| PASS | parity_breaking_holds_POmega_ne_Omega | PΩ(225°)=|Ω|0.7071 e^{i0.0000} vs Ω(225°)=|Ω|0.7071 e^{i-0.1250} ⇒ PΩ≠Ω |
| PASS | sigma_delta_a_mismatch | √(0.0076²+0.02²)=0.0214 ⇒ 相对 2.1%，σ_computed=5.13e-15；引用 σ=6.50e-14，比值 12.7× |
| PASS | alpha_scale_repeat | α(0)=7.297353e-03 vs α(M_Z)=7.815431e-03，相对差 -7.0995%（复现前置 C-01） |
| PASS | gz_interval_arithmetic | ΔE∈[2.60e+18,1.10e+19]；SM 基线反解 3.6400e+19 eV（两路一致 0.0 eV）——标准 GZK 常引 ~5e19，基线来源未交代 |
| PASS | gz_falsify_window_narrow | TUFT 上界 4.74 e19，证伪阈值 5.0e19，余量 0.26 e19（窄窗口） |
| PASS | cos3theta_identity | κ,τ∈{1..4} 最大偏差 1.39e-16 |
| PASS | omega_dimensionless_under_scaling | 缩放 1e6 倍：0.1788854382 vs 0.1788854382 |
| PASS | real_omega_parity_even | Ω_real(−θ)=Ω_real(θ)=0.707107（偶） |
| PASS | parity_theta_flips | atan2(1,2)=0.463648 → atan2(−1,2)=-0.463648（=−θ） |
| PASS | amplitude_continuous_at_weak_boundary | 弱域边界 |Ω| 两侧差最大 2.63e-15（连续） |
| PASS | phase_discontinuous_at_weak_boundary | φ(210°⁺)=-0.2500, φ(210°⁻)=0.0000 ⇒ 相位跳变 0.2500 = φ_0/2 ≠ 0 ⇒ 「相位连续（φ光滑）✔」不成立 |

### 结论映射

- N1（A_chiral≡0）确认；N1 修正给出 δA_TUFT∝−2|Ω|c_I sinφ，非零要求 c_I≠0（SM×TUFT 干涉有虚部）。
- N2（PΩ=Ω* 需 θ_W,c=0）确认：三正瓣 θ_W,c=240°≠0，PΩ=Ω* 不成立；但破缺本身（PΩ≠Ω）成立。
- N3（σ_{Δa_e} 与预算差 ~13 倍）确认：需重算区间或补 27% 级第三误差源。
- N4（C-01 复现，α 标度差 7.10%）确认：Part C 须改 μ=M_Z 或明确 μ→0。
- N5（UHECR 区间算术自洽但 SM 基线 3.64e19 未交代 + 证伪窗口窄）确认。
