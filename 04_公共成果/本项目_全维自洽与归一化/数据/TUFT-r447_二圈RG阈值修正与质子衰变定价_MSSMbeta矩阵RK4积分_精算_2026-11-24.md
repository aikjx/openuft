# TUFT-r447_二圈RG阈值修正与质子衰变定价_MSSMbeta矩阵RK4积分_精算_2026-11-24

- 判词：`TWO-LOOP-RG-THRESHOLD-PROTON-PRICED--BETA-CONVERSION-VERIFIED--RK4-CONVERGED--THRESHOLD-EXTERNAL-INPUT--MIN-SU5-PROTON-DECAY-RECOMPUTED--PASS-NOT-FIRST-PRINCIPLE`
- 条目：14；PASS=6 / FAIL=0 / BOUNDARY=2 / INFO=4 / CORRECTED=2
- 守卫：18/18

## 关键读数

| 项 | 读数 |
|---|---|
| beta_conversion_max_rel_err | 1.9760510338904548220506022E-17 |
| beta_matrix_mutation_rel_delta | 4.9061897007600661121046764E-4 |
| inv_alpha_wrong_div_alpha_rel_delta | 5.8019653001688929832642407E+1 |
| convergence_rel_MG | 4.1442737348433168012641542E-10 |
| convergence_abs_dL | 2.6456554209858292615206852E-8 |
| dL | 4.8190772851939696282114751E-1 |
| M_G_GeV | 1.1247473212632112693207773E+16 |
| alpha_G | 3.9024760063852963912598049E-2 |
| threshold_delta3_if_keep12 | -3.1585472082677926668422832E-1 |
| threshold_splitting_factor_b3_1L | 1.9377443305158831894329870E+0 |
| proton_lifetime_yr | 3.0140968407648176095763535E+35 |

## 条目

- **I01 [INFO]** [C] 输入与超荷归一锁：GUT 归一 alpha1=(5/3)alpha_em/cos^2(theta_W)；beta 系数与 B 矩阵均为外部标准输入
- **I02 [PASS]** beta 形式求导一致性：g 形式转 alpha^-1 形式的最大相对误差 1.9760510338904548220506022E-17
- **I03 [PASS]** MSSM 二圈矩阵锁定与变异灵敏：B 矩阵 3x3 逐项匹配；改 B12 后导数相对变化 4.9061897007600661121046764E-4
- **I04 [PASS]** RK4 步长收敛：h=0.02 与 0.01 的相对 M_G 差 4.1442737348433168012641542E-10，dL 差 2.6456554209858292615206852E-8
- **I05 [PASS]** MSSM 二圈分段积分仍汇聚：dL=4.8190772851939696282114751E-1 e-fold，M_G=1.1247473212632112693207773E+16 GeV
- **I06 [BOUNDARY]** 阈值修正为外部自由输入：固定 M_G 维度 1，M_G 可用时维度 2；最小范数 delta=(Decimal('0.1052851259560670236506119439280580049287338178040278315483'), Decimal('0.1052846879284524874722069352264046885714747497477934777617'), Decimal('-0.2105698138845195111228188791544626935002085675518213093099'))
- **I07 [PASS]** 质子衰变寿命独立复算完成：tau~hbar*M_X^4/(alpha_G^2*m_p^5)，kappa=1 口径 tau=3.0140968407648176095763535E+35 yr；M_X^4 与 alpha^-2 标度守卫 G4-3/G4-4 通过
- **I08 [PASS]** 最小 SU(5) 质子衰变未被 1e34 yr 下限排除：tau/limit=3.0140968407648176095763535E+1
- **I09 [CORRECTED]** 登记 r443 U2b 状态更新：二圈/阈值/质子衰变已定价，但不改 r443/r445 字节
- **I10 [INFO]** 全局记分板不变：0/6 · 0/22 · UFT-3=0 · L3=0 · validated=0 · 含引力四力正确方程 0 条 · L3 不升 L4
- **I11 [BOUNDARY]** 强子矩阵元因子未纳入：tau ~ kappa*M_X^4/(alpha_G^2 m_p^5)，本册取 kappa=1，O(1) 不确定度未消除
- **I12 [INFO]** 阈值质量分裂口径：若用一圈 b3=-3 单参数解释 delta3，需要分裂因子 1.9377443305158831894329870E+0；口径依赖，不迁移为预言
- **I13 [CORRECTED]** 来料模块2倒数耦合公式修正：来料写作 -b_i/(2pi)-sum_j B_ij*alpha_j/(8pi^2*alpha_i)；由 dalpha_i/dt 链式推导应无 /alpha_i，错误口径相对差 5.8019653001688929832642407E+1；源码保持正确式
- **I14 [INFO]** r447b 方向登记：顶夸克 Yukawa 耦合二圈反馈 + 非简并阈值全参数扫描 + 三耦合精确交汇微调程度量化；本册只登记不执行
