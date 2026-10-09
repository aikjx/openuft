# TUFT-MATH-PROOF-ADD-01 自洽性校验报告（分支 4）

- 引擎：源码/TUFT-MATH-PROOF-ADD-01_自洽性校验_2026-10-04.py（纯标准库）
- 日期：2026-10-04
- 分区：三正瓣（EM 0° / Strong 120° / Weak 240°，各 60°）+ G 三负瓣之并
- 读数：18 guard —— PASS 18 / FAIL 0（退出码 0）

| PASS | chiral_asymmetry_identically_zero | A_chiral = 0 （恒等于 0）→ 与「不对称来自干涉相位」自相矛盾 |
| PASS | interference_deltaA_nonzero | θ=225°, φ=-0.125, |Ω|=0.7071：奇项 −2|Ω|c_I sinφ = 0.1763 ≠ 0；纯实 c 时该奇项 = 0 ⇒ δA_TUFT 非零要求 c_I≠0 |
| PASS | parity_omega_star_needs_odd_phase | φ(225°)=-0.1250, φ(−225°)=0.0000, −φ(225°)=0.1250 ⇒ φ(−θ)≠−φ(θ) （差 -0.1250，θ_W,c=240°≠0）；仅 θ_W,c=0 时成立 |
| PASS | parity_breaking_holds_POmega_ne_Omega | [历史基线] PΩ(225°)=|Ω|0.7071 e^{i0.0000} vs Ω(225°)=|Ω|0.7071 e^{i-0.1250} ⇒ PΩ≠Ω 成立；**但该式不构成破缺判据**（复场自动满足）⇒ 结论以作用量判据 guard 为准 |
| PASS | parity_criterion_lagrangian_three_lobe | φ(225°)=-0.1250（域内）、φ(−225°)=φ(135°)=0.0000（出弱域）⇒ 守恒残差 |C_L(θ)−C_R(−θ)|=0.0883（归一化 0.1249）≠0 ⇒ 按作用量判据 P 破缺；破缺来源 = 分段定义下 φ(−θ)≠−φ(θ)，**与「复相位」无关** |
| PASS | parity_criterion_bump_centered_conserves | bump 居中窗 5 点守恒残差最大 0.00e+00（机器零）⇒ P 守恒；与历史基线（同窗内 PΩ≠Ω 成立）并存 ⇒ 该基线判据**零信息量** |
| PASS | parity_residual_nonzero_in_weak_domain | 弱域内 5 点守恒残差 min=0.0402 max=0.0883（spread=4.81e-02 ⇒ 随 θ 变化，**恒 ≠0**）；Δ_P=0.0e+00 ≡ 0 ⇒ 破缺为纯相位型，不给出 |g_L|≠|g_R| 的手征强度不对称 |
| PASS | sigma_delta_a_mismatch | √(0.0076²+0.02²)=0.0214 ⇒ 相对 2.1%，σ_computed=5.13e-15；引用 σ=6.50e-14，比值 12.7×。**继承声明：g-2 窗口已关（链 A-④ D-02），故正确做法不是重算区间，而是先证伪关窗前提** |
| PASS | alpha_scale_repeat | α(0)=7.297353e-03 vs α(M_Z)=7.815431e-03，相对差 -7.0995%（复现前置 C-01） |
| PASS | gz_interval_arithmetic | ΔE∈[2.60e+18,1.10e+19]；SM 基线反解 3.6400e+19 eV（两路一致 0.0 eV）——标准 GZK 常引 ~5e19，基线来源未交代。**继承声明：窗口已关（链 A-④ D-02），此区间不可用** |
| PASS | window_closed_inherited_from_chainA4 | 自证：窗口已关声明=True（10 处）、β 通道单列声明=True ⇒ 继承声明已落盘，勿删 |
| PASS | gz_falsify_window_narrow | TUFT 上界 4.74 e19，证伪阈值 5.0e19，余量 0.26 e19（窄窗口） |
| PASS | cos3theta_identity | κ,τ∈{1..4} 最大偏差 1.39e-16 |
| PASS | omega_dimensionless_under_scaling | 缩放 1e6 倍：0.1788854382 vs 0.1788854382 |
| PASS | real_omega_parity_even | Ω_real(−θ)=Ω_real(θ)=0.707107（偶） |
| PASS | parity_theta_flips | atan2(1,2)=0.463648 → atan2(−1,2)=-0.463648（=−θ） |
| PASS | amplitude_continuous_at_weak_boundary | 弱域边界 |Ω| 两侧差最大 2.63e-15（连续） |
| PASS | phase_discontinuous_at_weak_boundary | φ(210°⁺)=-0.2500, φ(210°⁻)=0.0000 ⇒ 相位跳变 0.2500 = φ_0/2 ≠ 0 ⇒ 「相位连续（φ光滑）✔」不成立 |

### 结论映射

- N1（A_chiral≡0）确认；N1 修正给出 δA_TUFT∝−2|Ω|c_I sinφ，非零要求 c_I≠0（SM×TUFT 干涉有虚部）。
- **N2 已用作用量判据重写（步0）**：`PΩ=Ω*` 需 θ_W,c=0 仍成立；但**「破缺本身（PΩ≠Ω）成立」是错误论断，已删除**。
  正确判据 C_L(θ)=C_R(−θ)：三正瓣 θ_W,c=240° 下残差 ≠0 ⇒ P 破缺，归因为「相位非奇 + 弱域非 P-自反」；
  bump 居中窗（θ_W,c=0）下残差机器零 ⇒ **P 守恒** ⇒ 复相位本身既不破坏宇称也不产生手征强度不对称（Δ_P≡0）。
  原 guard 已降级为**历史基线**保留（不可回退），不再作为破缺结论。
- N3（σ_{Δa_e} 与预算差 ~13 倍）确认；**继承声明：g-2 窗口已关（链 A-④ D-02 物理层 FAIL）**
  ⇒ 正确处置不是重算区间，而是先证伪关窗前提。
- N4（C-01 复现，α 标度差 7.10%）确认：Part C 须改 μ=M_Z 或明确 μ→0。
- N5（UHECR 区间算术自洽但 SM 基线 3.64e19 未交代 + 证伪窗口窄）确认；
  **继承声明：UHECR 窗口已关（链 A-④ D-02）**，该区间不可用作预言。
- **通道范围分离（步1）**：关窗范围 = {g-2, EDM, UHECR}；**β 衰变不在关窗范围**，
  其阻塞是 δA_TUFT 未定义（五项前置）+ 参数账 6→7、c_I 无源（见 ADD-01R F04）。
