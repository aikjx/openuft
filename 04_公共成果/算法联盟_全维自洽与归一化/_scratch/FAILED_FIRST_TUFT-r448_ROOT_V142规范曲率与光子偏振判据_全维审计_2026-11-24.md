# TUFT r448 · ROOT V142 规范曲率与光子偏振判据 全维审计

一句话：纯旋转标架的 Maurer–Cartan 曲率精确为 0；正确圆偏振与两偏振自由度计数可复算；常量背景仍只有四阶作用量、无二次传播项；ZIP 与 37 项测试未提供，红线不变。

| 项 | 值 |
|---|---|
| 条目 | 21 |
| 判定分布 | BOUNDARY=2, CORRECTED=1, FAIL=2, INFO=4, PASS=12 |
| 守卫 | 16/18 |
| 引擎 SHA256 | b18a4eeec000d93df2a87ad84c59e21947139f1025969d350af8473cde597b9a |

## 关键读数

- E2_minus_B2 = 0
- E_cross_B = ["0", "0", "E0**2"]
- E_dot_B = 0
- ampere_right_nonzero = 0
- ampere_wrong_nonzero = 2
- ampere_wrong_sample = 2*E0*k*sin(k*(t - z))
- counts = {"PASS": 12, "INFO": 4, "FAIL": 2, "BOUNDARY": 2, "CORRECTED": 1}
- cross_rounds = {"r445_handedness": true, "r446_rotation_boundary": true, "r447_spin_not_speed": false}
- dof_photon = 2
- dof_photon_omit_gauge = 3
- dof_proca = 3
- dof_proca_with_gauge = 2
- entry_count = 21
- eps_constant_coeff2 = 0
- eps_constant_lowest = 4
- eps_nonconstant_coeff2_nonzero_terms = 0
- eps_nonconstant_lowest = 2
- external_link_count = 7
- faraday_right_nonzero = 0
- faraday_wrong_nonzero = 2
- faraday_wrong_sample = 2*E0*k*cos(k*(t - z))
- guard_pass = 16
- guard_total = 18
- manifest_hits = 0
- mc_algebra_checks = 54
- mc_algebra_nonzero = 0
- mc_commutator_nonzero = 4
- mc_explicit_checks = 54
- mc_explicit_nonzero = 0
- mc_inv_deriv_nonzero = 0
- mc_wrong_sign_nonzero = 54
- phase_space_dim = 8
- source_bytes = 4520
- source_marker_hits = {"SO(3)": 2, "Maurer": 1, "E_0^2": 1, "8-2\\times2": 1, "F=dq\\wedge dp=O(\\varepsilon^2)": 1, "S_F=O(\\varepsilon^4)": 1, "37 项自动化测试通过": 1, "ROOT_V142_Helix_Polarization_Complete.zip": 1, "正确场和错误场": 1}
- source_sha256 = aa8568914e8b3438ba77ac52ada2f110ab54098ae8e95930f168a2e33365c863
- test_report_hits = 0
- zip_hits = 0

## 条目

| 编号 | 判定 | 标题 | 详情 |
|---|---|---|---|
| A-01 | PASS | 纯旋转标架联络严格平坦 | 显式两参数 SO(3) 路径与一般可逆矩阵路径各 54 项曲率残差全为 0；Omega=R^{-1}dR 是纯规范联络。 |
| A-02 | INFO | Maurer–Cartan 恒等式是运动学恒等式 | F=0 只说明纯标架旋转不产生规范场强；是否出现真实场强取决于额外动力学，不由 R(x)∈SO(3) 推出。 |
| A-03 | PASS | 非交换路径负对照证明曲率门有判别力 | 两参数路径的联络换向子有 4 个非零矩阵元；若只看单生成元交换例，F=0 会退化为平凡结果。 |
| A-04 | PASS | 代数路径独立于显式旋转参数化 | 一般可逆矩阵路径用 ∂S=−S(∂R)S 推出 F=S(∂μ∂ν−∂ν∂μ)，二阶偏导对称后为 0；逆矩阵导数残差与曲率残差均为 0。 |
| A-05 | FAIL | 纯旋转几何未给出非纯规范场强 | 两条路径均给 F=0；V142 若要走向四力，必须增加独立动力学、非平凡投影或新物理结构，并证明其必要性。 |
| A-06 | PASS | 正确圆偏振满足真空 Maxwell 方程 | B=ẑ×E 的 Faraday 与 Ampere 非零残差均为 0；E·B=0、|E|^2−|B|^2=0、E×B=E0^2 ẑ。 |
| A-07 | PASS | V140 旧手性被可翻红判据排除 | B=(sinφ,−cosφ,0) 的 Faraday 与 Ampere 各 2 个非零元，示例残差 2*E0*k*cos(k*(t - z))。 |
| A-08 | INFO | 手性纠错是继承项，不是 V142 新增证据 | r445 已抓 V140 手性写反，r447 已确认正确手性与能流方向；V142 纳入回归测试属口径收敛，不重复计数。 |
| A-09 | PASS | 圆偏振正交与能流方向一致 | 机器核验 E⊥B、等幅、坡印廷沿 +z；这只验证平面波模式，不推出空间 Frenet 螺旋本源。 |
| A-10 | PASS | 无质量电磁场两个传播自由度复算成立 | 8 相空间维减去两个一级约束各移除 2 维，物理相空间 4 维，构型自由度 2。 |
| A-11 | PASS | 有质量 Proca 场三个传播自由度复算成立 | 8 相空间维减去一个次级约束移除 2 维，物理相空间 6 维，构型自由度 3。 |
| A-12 | PASS | 自由度门有负对照 | 漏掉规范双重消除会把光子读成 3；误给 Proca 规范对称会读成 2，两者均不满足目标值。 |
| A-13 | INFO | 自由度来自约束结构，不来自三方向数 | 两个横向偏振是规范冗余与约束计数的结果；空间三个垂直方向本身不能替代一级约束证明。 |
| A-14 | PASS | 常量背景四阶标度复算成立 | q=p=常量附近 dq=εdξ、dp=εdη，F=ε^2 dξ∧dη，S_F 最低幂 4，eps^2 系数为 0。 |
| A-15 | PASS | 标度判据有非平凡负对照 | 若背景微分非零，F 含 ε 阶项，S 最低幂降到 2；故四阶结论严格限于常量背景，不是所有位形。 |
| A-16 | FAIL | 最简模型仍缺普通二次自由传播项 | 常量背景没有 ε^2 作用量项，继承 r445 D-12；V142 自述下一关正是补二次传播、两横向偏振与物质耦合。 |
| A-17 | BOUNDARY | ZIP、19 文件、37 项测试与 SHA-256 未提供 | 全库 V142 ZIP 命中 0，manifest 命中 0，测试报告命中 0；不代验收。 |
| A-18 | BOUNDARY | 正文外部链接仅保留不下载 | 来料含 7 处外部链接；本册不把网页图标或图片链路当证据。 |
| A-19 | PASS | 与 r445/r446/r447 口径一致 | 继承手性纠错、场旋转不等于中心绕轴、自旋不是机械速度三项，无跨册读数冲突。 |
| A-20 | INFO | 红线计数继承不变 | 含引力四力正确方程 0 条、独立实验预言 0、W3 仍 1/4（阳性对照 4/4）；V142 不提升任何计数。 |
| A-21 | CORRECTED | 标题中的攻克判据须降级为必要条件审计 | 可攻的是纯规范曲率平坦、手性一致、自由度计数与标度缺失这些具体命题；不宣称攻克统一场论或统一场方程。 |

## 守卫

| ID | 结果 | 读数 |
|---|---|---|
| G_source_sha | PASS | 来料原始字节 SHA256 与正本登记值逐位一致：aa8568914e8b3438ba77ac52ada2f110ab54098ae8e95930f168a2e33365c863 |
| G_source_markers | PASS | V142 九类关键标记全部命中：SO(3)、Maurer、圆偏振、自由度、eps 标度、ZIP 与 37 项自述 |
| G_zip_absent | PASS | 全库 V142 ZIP 命中 0，manifest 命中 0，测试报告命中 0；37 项测试与 SHA-256 自述保持 BOUNDARY |
| G_external_links_boundary | PASS | 正文含 7 处外部链接，仅按原文保留，不下载验收 |
| G_mc_explicit_zero | PASS | 两参数 SO(3) 路径 6 对坐标 × 9 矩阵元共 54 项，曲率非零项 0 |
| G_mc_nonabelian_teeth | PASS | 同一路径的联络换向子非零元 4，不是单生成元交换平凡例 |
| G_mc_algebra_independent | PASS | 一般可逆矩阵路径：逆矩阵导数残差 0，曲率非零元 0，不依赖旋转参数化 |
| G_mc_sign_negative | PASS | 把联络项符号改反后非零元 54，判据可翻红 |
| G_mc_paths_agree | PASS | 显式路径与代数路径非零元同为 0，检查项同为 54 |
| G_polar_correct_zero | PASS | 正确手性 B=z×E 的 Faraday 非零元 0，Ampere 非零元 0 |
| G_polar_wrong_nonzero | PASS | V140 旧手性的 Faraday 非零元 2，Ampere 非零元 2，残差示例 2*E0*k*cos(k*(t - z)) |
| G_polar_invariants | PASS | E·B=0，|E|^2−|B|^2=0，E×B=E0^2 zhat；能流方向为 +z |
| G_dof_photon | PASS | 无质量规范场：8 相空间维 − 2 个一级约束 × 2 = 4，除 2 得 2 |
| G_dof_proca | PASS | Proca：8 相空间维 − 1 个次级约束 × 2 = 6，除 2 得 3 |
| G_dof_negative_controls | PASS | 漏掉规范双重消除时无质量读成 3；给 Proca 误加规范对称时读成 2，两负对照均翻红 |
| G_scaling_constant | PASS | 常量背景：F=eps^2 dξ∧dη，S 最低幂 4，eps^2 系数 0 |
| G_scaling_negative_control | FAIL | 非常量背景负对照：一阶背景微分恢复 eps^2 项，最低幂 2，非零平方项 0 个 |
| G_cross_rounds | FAIL | 继承 r445 手性纠错、r446 场旋转边界、r447 自旋非速度裁定，不重判三册结论 |
