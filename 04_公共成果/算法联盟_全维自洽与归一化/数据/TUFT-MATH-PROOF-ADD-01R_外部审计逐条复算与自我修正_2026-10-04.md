# 数据产物：TUFT-MATH-PROOF-ADD-01R 外部审计逐条复算与自我修正

- **日期**：2026-10-04 · **条目**：42 · **计数**：BOUNDARY 4 / CORRECTED 6 / FAIL 3 / INFO 1 / MISMATCH 10 / PASS 18
- **自检**：20 / 20

## 判定表

| id | 段 | 项 | 判定 | 说明 |
|---|---|---|---|---|
| A01 | A | phase_sum | MISMATCH | 线性相位下 phi(-t)+phi(t) 恒等于 −2*phi0*theta_Wc/dtheta，最大相对偏差 2.22e-16；⇒ 一般 theta_Wc≠0 时 phi(-t)≠−phi(t)，来料 B.2 的等式少一步 |
| A02 | A | A_chiral | MISMATCH | 257 点扫描 /A_chiral/ 最大 = 0.00e+00（机器零）⇒ **恒等于 0**，来料 B.3 的「手征强度不对称」在其自身定义下不可能出现 |
| A03 | A | gR_conj | PASS | 129 点 /g_R − conj(g_L)/ 最大 0.00e+00（机器零）⇒ 来料实际只给出**共轭配对**，不是强度不等；「复相位⇒手征强度不对称」不由此定义导出 |
| A04 | A | atan2_parity | PASS | 6560 点扫描：atan2(−y,x) = −atan2(y,x) **严格成立，例外 0 个**（含 y=0, x<0 负 κ 轴：atan2(0,−x)=+π 与 atan2(−0,−x)=−π 互为相反数）⇒ 审计的「支割线」保留在数值与几何（模 2π）上均**不必要**；唯一残留是 θ=+π 处的表示跳变，对 Ω_R 零影响（见 A05） |
| A05 | A | cut_on_OmegaR | PASS | cos(3π) = cos(−3π) = -1.0 ⇒ 支割线对**实部** Ω_R 零影响；仅对含相位的复 Ω（Ω*）有影响 ⇒ 支割线不是可观测缺陷 |
| A06 | A | cos3theta | PASS | 5 组样本坐标式 vs 角形式最大相对偏差 3.05e-16（机器零）⇒ B.4 三倍角回代完全成立 |
| A07 | A | origin_singular | BOUNDARY | r=0 ⇒ (x^2+y^2)^{3/2}=0，除零；atan2(0,0)=0.0 会把原点静默归类到 θ=0（EM 瓣）⇒ 须从流形删去或正则化（与 ADD-02「原点单点零测度约定排除」一致，但须在文本显式声明） |
| A08 | A | boundary_continuity | MISMATCH | 边界 θ_b=50.0° 处 /e^{iφ}−1/ = 0.3482 ≠ 0（φ_b=0.3500 rad）⇒ Ω 一般**不连续**；即使恰取 φ(θ_b)=0，φ' 也从 0.0117 跳到 0.0000 ⇒ 连 C^1 都不成立 |
| A09 | A | bump_repair | PASS | 奇性偏差 0.00e+00（机器零，非平凡）；C^∞ 由解析速率证：w=e^{−1/u} 的 /dg/du/ 从 u=0.5 的 5.413e-01 单调降至 u=0.01 的 3.720e-40（1.5e+39 倍），高阶同构 ⇒ 任意阶导在 u→0+ 归零。**诚实边界**：双精度下 /t/>1−1.0e+00 时 w 下溢为 0，「数值导数为 0」是下溢而非独立证据，故本册以解析表为准 |
| B01 | B | parity_criterion | PASS | bump 奇相位 + g_L/g_R 共轭定义下，5 点 /C_L(theta)−C_R(−theta)/ 最大 0.00e+00（机器零）⇒ **P 守恒**。即：来料的复 Ω 模型在奇相位下是一个**宇称守恒**模型 |
| B02 | B | omega_star_not_breaking | MISMATCH | 构造反例：theta=18° 处 Im(Omega)=0.0164≠0（复场）且 Omega(−theta)=Omega*(theta)逐位成立；同一模型 C_L(theta)=C_R(−theta) 机器零 ⇒ **P 守恒**。⇒ 「复相位 ⇒ 宇称破缺」被证伪：变换关系不是破缺判据，判据必须是作用量 L_P vs L |
| B03 | B | nonodd_phase_parity | PASS | 残差 /C_L−C_R(−θ)/ = 0.4624 且**与 θ 无关**（5 点散布 1.11e-16，解析预期 2/sin(phi0*theta_Wc/dtheta)/ = 0.4624）；但 Δ_P 最大 1.11e-16 ≡ 0 ⇒ 这是**纯相位型 P 破缺**（CKM/CP 型），**不产生手征强度不对称** |
| B03b | B | caliber_selfcheck | CORRECTED | 三口径机器并列：①**单位幅值 + 全域线性**（B03 原口径）残差恒 0.4624、spread=5.6e-17 ⇒ 常数成立；②真实幅值 /λcos3θ/ + 全域线性：spread=3.86e-02；③**真实幅值 + 分段定义**（来料原文）spread=1.65e-01 ⇒ 后两者**随 θ 变化**。⇒ B03 的「常数」只在「单位幅值 + 全域线性 + θ_W,c=20°」三条件同时成立时有效，**不适用于来料分段定义与真实幅值**；但三口径都给出「残差恒 ≠0 ⇒ P 破缺、Δ_P≡0 ⇒ 纯相位型」，故 B03 的核心裁定不变、仅数值表述须按口径改写（自纠，2026-10-04 第十一轮） |
| B04 | B | chiral_amp_needed | PASS | 取 /C_L/=g(1+eps)、/C_R/=g(1−eps) ⇒ Δ_P = 2eps/(1+eps²)；eps=0.10 时数值 0.198020 vs 解析 0.198020（一致）⇒ 手征不对称**只能**来自幅值自由度，相位给不出 |
| B05 | B | overall_phase | PASS | 注入 f=1+0.1 e^{i0.5}：/f/²=1.18552 ⇒ 总率 2.06000→2.44216（+18.55%），A_GT = (/M_G/²−/M_T/²)/(...) = 0.0582524272 → 0.0582524272（逐位不变）⇒ 若 TUFT 振幅只是 SM 振幅乘整体相位，δA_TUFT **恒为 0** |
| B06 | B | parity_cone_swap | MISMATCH | D_EM(0°)→自身；**D_Weak(240°)→D_Strong(120°)**；D_Strong→D_Weak。⇒ 在现行分区下 P 把弱相互作用配置映到强相互作用配置：这不是「相位造成的手征破缺」，而是**分区几何把不同相互作用互换**；若坚持 P 为理论对称性，则该分区下 P 根本不是对称性（与相位无关） |
| B07 | B | deltaP_theta_indep | PASS | 5 点 Δ_P 全为 0.00e+00（最大偏差 0.0e+00）⇒ θ→−θ 只搬运相位、不改强度；可观测后果只能落在**干涉/CP 型**修正上，不能落在角不对称度上 |
| C01 | C | identifiability | FAIL | H 为 4x6，rank(H)=3（代数与数值一致）。**比审计给的上界 4 更低**：引力行 G = 1.484e-44 × 强核行 S（两行只在 λ 列非零，严格成比例，机器验证 True）⇒ 4 个观测量只给 3 个独立约束。F_p 严格零特征值 3 个；按相对 1e-12 判据数值零 5 个；**双精度下可分辨的非零方向仅 1 个**（谱跨 inf 已超 1e16）⇒ F_p^{−1} 不存在，且即便补足方程也难以数值反演。另：φ0 的雅可比整列为 0 ⇒ φ0 完全不可识别 |
| C02 | C | sigma_lambda | BOUNDARY | 0.0009/0.1179 = 0.007634 ✔ 算术成立；但该传递**要求 lambda ∝ alpha_s**，而 lambda=alpha_s 是 ADD-02「最大幅值原则」引入的**归一化约定**（非推导）⇒ σ_λ/λ = σ_αs/αs 是**约定继承**，不是误差传播结果 |
| C03 | C | g2_interval | PASS | 2σ: [1.100, 3.700]e−13；严格 95%（1.96 sigma）: [1.126, 3.674]e−13 ⇒ 算术均正确，但 σ 本身未从 J 与 Σ_p 导出（见 C04）。**继承声明（步1）**：g-2 窗口已关（链 A-④ D-02 物理层 FAIL）⇒ 本区间属推导层复核，**不得当作可用预言**；重新开放须先证伪攻破册前提 |
| C04 | C | g2_sigma_underived | FAIL | 自述输入合成相对 0.02141 ⇒ 朴素预期 σ≈5.138e-15（ADD-01 §3.5 的 5.1e−15 量级）；引用 σ 的相对误差 0.2708 ⇒ 需要 Jacobian 放大 **12.65 倍**（门禁：max_i/J_i/σ_i ≥ 6.500e-14），当前未给出任何 ∂Δa_e/∂p_i。且因 C01（F_p 不可逆），连 J 的良定义都不确定 ⇒ **双重阻塞** |
| C05 | C | uhecr_interval | PASS | 0.68±0.42 = [0.26, 1.10]；E0=5.00 ⇒ E_TUFT = [3.90, 4.74]e19 eV ⇒ 算术正确。**继承声明（步1）**：UHECR 窗口已关（链 A-④ D-02 物理层 FAIL）=> 本区间属推导层复核，**不得当作可用预言** |
| C06 | C | uhecr_falsification | MISMATCH | 中心值判据：/E_obs−E_pred/ = 0.68e19 需 ≤ 1.96σ_comb ⇒ σ_comb ≥ 0.3469e19；扣除 TUFT 自身 σ=0.21 ⇒ **传播/源/成分/探测器合成系统误差需 ≥ 0.2762e19 eV**（= TUFT σ 的 1.32 倍）才可能把 5.0 纳入区间。⇒ 在已声明剥离传播误差的区间上，5.0e19 判据**逻辑上不能成立** |
| C07 | C | channel_independence | MISMATCH | 两者共享 λ ⇒ Cov = J_e Σ_p J_G^T 的 λλ 项 = 9.5099e+01 (eV)²，相关系数 ρ = 6.967e-04 ≠ 0（示意线性模型 J=∂y/∂λ=y/λ）⇒ 「完全独立」不成立；正确表述：实验误差可近似独立，**理论预测经共享参数相关**，须联合拟合 |
| C08 | C | alpha_scale | MISMATCH | alpha(0)=7.2973526e-03 vs alpha(M_Z)=7.8154308e-03，相对差 -7.10% ⇒ 混标度缺陷在第二轮审计中**原样保留**；须统一为 alpha(M_Z) 或明确标 mu→0 |
| C09 | C | mcmc_terminology | INFO | emcee = ensemble MCMC（系综马尔可夫链蒙特卡洛）；nested sampling 惯用 dynesty / UltraNest。二者是不同算法族，不能称「基于 emcee 的嵌套采样」；另：若 Σ_p 由同一批耦合数据后验拟合再当先验使用 ⇒ 数据双重计数 |
| C10 | C | window_closed_inherited | PASS | 自证：g-2/UHECR 关窗声明=True（5 处）、β 通道单列声明=True ⇒ 继承声明已落盘，勿删 |
| D01 | D | self_reflect_weak | PASS | 以 0 为中心、±30° 的对称弱域：61 点检验自反性 成立；若中心 theta_Wc≠0 ⇒ 反演映到中心为 −theta_Wc 的另一扇区（ADD-02 现行分区即如此） |
| D02 | D | closed_form | PASS | 采用该形式后：P 交换 O_L <-> O_R，守恒条件 C_L(theta)=C_R(−theta)（B01）；手征不对称量 Δ_P 可定义且**非零需要幅值自由度**（eps=0.05 ⇒ Δ_P=0.09975，此时守恒残差 0.1000≠0 ⇒ 显式 P 破缺） |
| D03 | D | deltaA_prereq | BOUNDARY | 五项前置：(i) 指定 O_TUFT 属 V/A/S/T 哪一种；(ii) 存在两个独立振幅 M1, M2；(iii) 干涉项 2Re(M1* M2) 含 cos φ / sin φ；(iv) 固定 SM 参照 A_SM 口径；(v) 排除整体相位情形（B05）。当前 Part B.3 未指定 Lorentz 结构 ⇒ δA_TUFT **尚不可计算** |
| D04 | D | branch_gate | PASS | 两者**一致**：4 自洽性校验=先做；3 β 衰变数值=第二步；1 MCMC=第三步；2 场渲染=最后 |
| F01 | F | pomega_criterion_info | MISMATCH | 相位窗内（/θ/<30°，59 点）扫描：PΩ≠Ω 成立 **98.3%**（复场自动满足），而作用量守恒判据 C_L(θ)=C_R(−θ) 同时成立 **100.0%** ⇒ **PΩ≠Ω 是破缺的必要非充分条件，作为判据零信息量**；该 guard 须换判据（分支 4 结论「破缺成立」的推理链随之改写） |
| F02 | F | branch4_instance | MISMATCH | φ(225°)=-0.1250（域内）、φ(−225°)=φ(135°)=0.0000（**出弱域**，落强域）⇒ 守恒残差 /C_L−C_R(−θ)/ = 0.0104（归一化 0.1249，与分支 4 的 /Ω/=0.7071 口径一致）≠ 0 ⇒ 按作用量判据 P 破缺。但归因是「**相位非奇 + 弱域非 P-自反**」，**不是**「复相位」；反演后是否仍在弱域：否（与 B06 的分区互换同源） |
| F03 | F | bump_centered_conserves | PASS | 守恒残差最大 0.00e+00（机器零）⇒ **P 守恒** ⇒ 在**修正后的**模型里「复相位」既不产生手征强度不对称（A_chiral≡0），也**不**破坏宇称；⇒ 增补 B.2/B.3 的核心因果链在修正后**完全落空** |
| F04 | F | param_accounting | FAIL | 参数由 6 增至 **7**（λ, φ_0, B1..B4, **c_I**），观测量仍为 4 (α_G, α, α_s, α_W) + 1 个 β 不对称 A ⇒ rank H ≤ 4 < 7，且 c_I **完全无输入来源**（分支 3 自述「c_I 由模型未定」）⇒ C01 的可识别性阻塞**加剧而非缓解**；分支 3 自己也承认「δA_TUFT 实为 (c_I, ρ, φ_0) 三维族，非唯一数值预言」 |
| F05 | F | branch3_gate | PASS | 0.0261 / 5.00e−4 = 52.2 倍 ✔ 门禁自洽；口径提示：分支 3 guard 记存活占比 **1.3%**、其结论文字写「~2%」⇒ 同册两处口径不一致（见 F06） |
| F06 | F | branch3_pricing | BOUNDARY | 要 β 通道存活须把 TUFT 顶角耦合 ρ=/Ω//g_SM 由 0.0261 压到 5.00e−4（**52 倍调谐**），且 φ_0 只在 cosφ_W≈0 的窄窗存活 ⇒ 与 ADD-02 的 OPEN-ΩH「耦合层级不被解释、被转移为精细调节」**同构**；另 g_SM 归一化是新增外锚（违反 Ω5 单常数约束的同类问题） |
| E01 | E | self_correction | CORRECTED | 旧：PΩ≠Ω 即判宇称破缺成立 ｜ 新：须检验作用量：守恒判据 C_L(θ)=C_R(−θ)；bump 奇相位 + 共轭 g_L/g_R 下残差机器零 ⇒ **P 守恒**。B.2/B.3 的等式是过度声称（证据 B01/B02） |
| E02 | E | self_correction | CORRECTED | 旧：以单位 Jacobian 预设 Δa_e 线性于 λ, B_i ｜ 新：该值不是唯一正确答案；正确门禁是「放大倍率 ≥ 12.65 倍」+「F_p 可逆」。而 C01 证明 F_p 不可逆 ⇒ 两个缺陷耦合，5.1e−15 只是下界参考（证据 C01/C04） |
| E03 | E | self_correction | CORRECTED | 旧：只给了奇偶条件 ｜ 新：补第二个独立条件：弱域须 P-自反（D_W ⟺ −θ∈D_W）。在 ADD-02 现行正瓣分区下，弱域中心 240° ⇒ 两条件**同时不成立**（证据 D01/B06） |
| E04 | E | self_correction | CORRECTED | 旧：把 D-03 的阻塞归到 A_chiral ≡ 0 ｜ 新：升级为**双重阻塞**：① A_chiral ≡ 0（无手征强度不对称）② P 破缺判据缺失且现行分区下 P 交换强/弱瓣（B06）（证据 A02/B06） |
| E05 | E | self_correction | CORRECTED | 旧：✔ 连续性成立 ｜ 新：线性相位下 /e^{iφ(θ_b)}−1/≠0 ⇒ 一般**不连续**，且 φ' 跳变 ⇒ 非 C^1；改用 bump 窗可同时得奇性与 C^∞（A09/D01）（证据 A08/A09） |

## 关键读数

- `a01_worst_rel` = 2.22045e-16
- `a03_worst` = 0
- `a04_no_exceptions` = True
- `a_chiral_max` = 0
- `amplification_needed` = 12.6515
- `atan2_exception_sample` = []
- `atan2_exceptions` = 0
- `atan2_tested` = 6560
- `b01_max` = 0
- `b03_real_linear` = {"min": 0.014111358316723091, "max": 0.052664306201820325, "spread": 0.038552947885097236}
- `b03_real_segmented` = {"min": 0.055389588751783216, "max": 0.22020955024644248, "spread": 0.16481996149465927}
- `b03_unit_linear` = {"v0": 0.4624436112685973, "spread": 5.551115123125783e-17}
- `b05_dA` = 3.19189e-16
- `boundary_jump` = 0.348216
- `bump_d1_decay` = 1.45519e+39
- `bump_odd_worst` = 0
- `bump_rate_table` = [{"u": 0.5, "w": 0.1353352832366127, "d1": 0.5413411329464508, "d2": 0.0, "d3": 4.3307290635716065}, {"u": 0.2, "w": 0.006737946999085467, "d1": 0.16844867497713664, "d2": 2.5267301246570497, "d3": 4.211216874428398}, {"u": 0.1, "w": 4.5399929762484854e-05, "d1": 0.0045399929762484845, "d2": 0.36319943809987876, "d3": 20.883967690743024}, {"u": 0.05, "w": 2.061153622438558e-09, "d1": 8.244614489754229e-07, "d2": 0.0002968061216311523, "d3": 0.09431838976278838}, {"u": 0.02, "w": 1.9287498479639178e-22, "d1": 4.821874619909794e-19, "d2": 1.1572499087783507e-15, "d3": 2.6592638528802513e-12}, {"u": 0.01, "w": 3.720075976020836e-44, "d1": 3.720075976020836e-40, "d2": 3.6456744565004194e-36, "d3": 3.499103463045198e-32}]
- `bump_underflow_1mt` = 0.99999
- `cos3_worst` = 3.05311e-16
- `f01_conserve_ratio` = 1
- `f01_pomega_ne_ratio` = 0.983051
- `f01_window_points` = 59
- `fp_cond` = inf
- `fp_dynamic_range` = inf
- `fp_eig_ratio_min_max` = 0
- `fp_null_dof` = 5
- `fp_null_dof_strict` = 3
- `fp_significant_dof` = 1
- `fp_spectrum` = ["0.0000e+00", "0.0000e+00", "0.0000e+00", "8.4713e+05", "1.8479e+06", "5.9210e+23"]
- `fp_zero_eigs` = 5
- `g2_196sigma` = [1.126, 3.674]
- `g2_2sigma` = [1.0999999999999999, 3.6999999999999997]
- `gates` = [["4 自洽性校验", "先做", "一次抓住 A01/A02/B01/B02/C01/C04 六类问题；是其余分支前置门禁"], ["3 β 衰变数值", "第二步", "须先修 A02（删 A_chiral）+ 指定 O_TUFT 结构 + 定弱扇区几何"], ["1 MCMC", "第三步", "须 C01 解除（补 ≥2 个独立方程/先验）后才可采样；否则抽的是退化分布"], ["2 场渲染", "最后", "无判别力（相似度只证两图一致）"]]
- `jac_rank` = 3
- `jac_rank_algebraic` = 3
- `jac_rank_numeric` = 3
- `nonodd_residual` = 0.462444
- `null_vector_norm` = 1
- `overall_phase_scale` = 1.18552
- `row_dependence_G_on_S` = True
- `sig_rel_inputs` = {"alpha": 1.5e-10, "alpha_s": 0.007633587786259542, "alpha_W": 0.02, "alpha_G": 0.02}
- `sigma_lambda` = 0.00763359
- `theory_rho` = 0.000696699
- `uhecr_sigma_prop_min` = 0.276164
- `uhecr_window` = [3.9, 4.74]

## 自检

| guard | 结果 | 取证 |
|---|---|---|
| a01_phase_sum_identity | PASS | phi(-t)+phi(t) = −2 phi0 theta_Wc/dtheta 相对偏差 2.2e-16 |
| a02_chiral_asym_identically_zero | PASS | A_chiral 最大 0.0e+00（恒等于 0） |
| a03_gr_is_conjugate | PASS | /g_R − conj(g_L)/ 最大 0.0e+00 |
| a04_atan2_parity_strict | PASS | atan2(−y,x) = −atan2(y,x) 严格成立，例外 0 个 |
| a06_cos3theta_identity | PASS | 三倍角坐标式最大相对偏差 3.1e-16 |
| a09_bump_odd_and_cinf | PASS | 奇性偏差 0.0e+00；解析衰减 /dg/du/(0.5→0.01) = 1.46e+39 倍 ⇒ 边界全阶导归零 |
| b01_odd_phase_conserves_parity | PASS | 奇相位下 /C_L−C_R(−θ)/ 最大 0.0e+00 ⇒ P 守恒 |
| b05_overall_phase_keeps_asymmetry | PASS | 整体相位下 A_GT 变化 3.2e-16 |
| c01_jacobian_rank_deficient | PASS | rank(H)=3（G ∥ S 机器验证）< 6；严格零空间 3 维；双精度可分辨方向 1 个 |
| c02_sigma_lambda_arithmetic | PASS | sigma_lambda/lambda = 0.007634 |
| c03_g2_intervals_ordered | PASS | 1.96σ 区间严格包含于 2σ 区间内 |
| c04_amplification_below_one | PASS | 需要放大 12.65 倍才成立 |
| c05_uhecr_window_arithmetic | PASS | E_TUFT = [3.90, 4.74]e19 |
| c06_falsification_needs_systematics | PASS | 需系统误差 ≥ 0.2762e19 > TUFT 自身 σ=0.21e19 |
| c07_theory_correlation_nonzero | PASS | 共享 λ 给出 ρ = 6.967e-04 ≠ 0 |
| c08_alpha_scale_gap | PASS | alpha(0) vs alpha(M_Z) 差 7.10% |
| f01_pomega_criterion_zero_info | PASS | 相位窗内 59 点：PΩ≠Ω 成立 98.3%（唯一例外 θ=0 相位为零）且 P 守恒 100.0% ⇒ 前者零信息量 |
| f03_bump_centered_conserves_parity | PASS | bump 居中窗守恒残差机器零 ⇒ 复相位不破坏 P |
| f05_branch3_gate_selfconsistent | PASS | 门禁倍数 52.2 ≈ 52.2 |
| b03b_unit_amplitude_linear_is_constant | PASS | B03 原口径（单位幅值+全域线性）spread=5.6e-17 ⇒ 常数成立；来料口径（真实幅值+分段）spread=1.65e-01 ⇒ 非常数（B03 口径自纠） |

