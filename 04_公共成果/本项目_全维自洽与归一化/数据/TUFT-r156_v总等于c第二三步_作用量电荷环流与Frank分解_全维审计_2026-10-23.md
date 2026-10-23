# TUFT-r156 判定数据（机器产物）

- verdict：`V2V3-PARAMETERIZED-NOT-DERIVED`
- 条目 25：BOUNDARY 4 / CORRECTION 1 / FAIL 8 / INFO 1 / PASS 11
- 控制组 11（ok 11）｜守卫 8（ok 8）

| 条目 | 状态 | 标题 |
| --- | --- | --- |
| A1 | PASS | 光速约束使动能项 0.5*rho_s*v^2 = 0.5*rho_s*c^2 为常数（对变分无贡献） |
| A2 | BOUNDARY | 恒等式 kappa^2=[(n.grad)n]^2：场路线只覆盖切向部分，法向部分缺场外延 |
| A3 | PASS | EL 公式 deltaS/deltan_j = K[B_i d_j n_i - d_i(n_i B_j)] 的扰动法验证 |
| A4 | CORRECTION | EL 在轴对称 swirl 外推下对任意 n 可解，该扇区不过定 |
| A5 | BOUNDARY | 靶从未指定圆锥螺线解的 3D 场外推，EL 从未在真实解上被求值 |
| A6 | PASS | 作用量与 EL 的量纲齐次性 |
| B1 | PASS | v2 球对称可积扇区精确解：渐近式与数值表逐项复算 |
| B2 | PASS | 闭合式的非循环验证：几何角速度 Omega=v_phi/(r s0) vs c*sqrt(kappa^2+tau^2) |
| B3 | FAIL | v2 的「电磁势正比于 omega」是空指派：源强度 A 放大 10 倍 omega 只变 1e-4~1e-2 |
| B4 | PASS | 标度拟合：kappa 正比于 r^-1、tau 正比于 r^-3、omega 正比于 r^-1 |
| C1 | PASS | C1+C2+C3 闭式解复算：v_phi=Gamma_Q/(2 pi r s0)、v_r=sqrt(c^2-v_phi^2) |
| C2 | FAIL | 定义域空洞与密度奇点：解只存在于 r>=r_min，rho_s 在 r_min 平方根发散 |
| C3 | PASS | 源依赖线性：复算第三步 A.4 的四条比值（EM 正比于源、引力正比于 M、两路不串扰） |
| C4 | FAIL | 远场退化：Gamma_Q=0 严格给出 kappa=tau=omega=0；几何只活在电荷近邻 |
| D1 | FAIL | 引力源被指派为介质外流：Mdot/M = 4 pi G/beta_g 是普适常数 |
| D2 | FAIL | 参数计数门 n_free <= n_obs-1：8 <= 1 不通过（SU(5) 控制组通过） |
| D3 | FAIL | 两个自由耦合恰好吸收两个观测量 ⇒ 「双导出」净预言为零 |
| D4 | FAIL | alpha_em 仍含 4 个自由参数（zeta、gamma_Q、Gamma_0、theta_0） |
| E1 | PASS | 恒等式 (n.grad)n = -n x (curl n)（|n|=1 时成立） |
| E2 | FAIL | Frank 角色指派是字典：互换 splay/twist 立即破坏库仑定律 |
| E3 | PASS | bend-only 算子非椭圆：横向扰动零代价（主象征 -(K)(n0·k)^2 对 k⟂n0 恒零） |
| E4 | PASS | 完整 Frank 三项只有**两支**角度依赖横模（bend 不是第三支） |
| F1 | BOUNDARY | BOUNDARY：beta_g 的取值未定，D1 的绝对读数不可证伪 |
| F2 | BOUNDARY | BOUNDARY：未处理量子辐射反作用、引力自能与介质物态 |
| F3 | INFO | INFO：v4/v5 已由靶自己完成下游审计（光速判据二分/螺旋度/Derrick/K 定标 ×4） |

## 关键读数
- `r_min_closed` = Gamma_Q/(2 pi c sin theta0)
- `r_min_electron_natural_quantum` = lambda_bar_C / sin theta0
- `r_model_electron` = hbar/(2 m c) = lambda_bar_C/2
- `ratio_rmin_over_rmodel` = 2.3094010767585034
- `vphi_over_c_at_model_radius` = 2.3094010767585034
- `Mdot_over_M` = 4 pi G / beta_g（普适）
- `tau_loss_beta1_s` = 1192296893.246448
- `P_sun_over_L_sun_beta1` = 391653831323.3061
- `n_free` = 8
- `n_obs` = 2
- `lambda_bar_C` = 3.8615926772428334e-13
