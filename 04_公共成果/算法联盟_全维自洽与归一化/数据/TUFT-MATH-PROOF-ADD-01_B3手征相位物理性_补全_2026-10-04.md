# TUFT-MATH-PROOF-ADD-01 B.3 手征相位物理性补全报告（分支 3b）

- 引擎：源码/TUFT-MATH-PROOF-ADD-01_B3手征相位物理性补全_2026-10-04.py
- 日期：2026-10-04
- 读数：8 guard —— PASS 8 / FAIL 0（退出码 0）

| PASS | sm_beta_asymmetry_reference | A(lambda_SM)=-0.1195（实验 -0.1184；差 0.0011，O(高阶修正)） |
| PASS | phase_only_lambda_pure_imaginary | lambda(phi)=-i*tan(phi)：实部=0（纯虚）-> T 破坏耦合，非实宇称不对称 |
| PASS | phase_only_std_A_not_produced | Re A(-ix)=0.0206（小正数 O(x^2)），与 SM A=-0.118（大负值）不同构；相位不产生标准实宇称不对称 |
| PASS | phase_only_replaces_VA | |g_R|=|g_L| => 右旋弱流占比 100%，与『弱作用纯左手』(M_WR>>M_W) 冲突 |
| PASS | correction_reading_imaginary_axial | Im lambda(g_2)=0.0522，Im lambda(sqrt_alphaW)=0.2605 —— O(0.05-0.26) 的 T 破坏污染 |
| PASS | timereversal_excluded_by_EDM | 粗估 d_n~theta_bar*1e-13 e*cm，theta_bar~0.05 => 5.0e-15 e*cm，超上限 1.8e-26 约 3e+11 倍（粗估，标假设） |
| PASS | real_magnitude_axis_physical | g_SM in {0.65,0.130} 下 eps=0->1 的 deltaA>DeltaA（需 eps 调谐或 rho 压低），与分支 3 结论一致 |
| PASS | phase_assigned_to_CPT_odd_channel | D-03 的『相位 vs 手征性』区分：相位->CP/T-odd（受 d_n<1.8e-26 强约束）；实幅值差->标准宇称不对称 A。B.3 的『相位产生手征不对称』应改写为『幅值差产生宇称；相位产生 T-odd』 |

### 结论

1. **B.3 等幅反相相位机制（|g_L|=|g_R|=|Omega|，反相）产出纯虚 lambda=-i*tan(phi)** ——
   这是 CP/T-odd（T 破坏）耦合，**不是标准 beta 衰变的实宇称不对称 A**。
   A 依赖 Re lambda；纯虚 lambda 下标准 A 的前导实宇称不对称不产生。
2. **全耦合读取**：右旋弱流占比 ~100%，与『弱作用纯左手』（M_WR>>M_W）直接冲突。
3. **修正读取**：Im lambda ~ 2|Omega|sin(phi)/g_SM ~ O(0.05-0.26)；O(0.05) 的 T 破坏轴矢
   耦合被中子 EDM（d_n<1.8e-26 e*cm）按数量级排除（粗估超 ~1e11 倍，标注假设）。
4. **补全（使预言唯一且物理）**：宇称不对称须来自**实幅值差** |g_L|!=|g_R|（eps 参数）；
   此时 deltaA(eps) 可算、可证伪（g_SM in {0.65,0.130} 下 eps=0->1 的 deltaA>DeltaA，
   需 eps 调谐或 rho 压低）。相位则归入 CP/T-odd 通道（受 EDM 强约束）。
5. **D-03 深度闭合**：审计所指『相位 vs 手征性』的区分在此显影——**相位->CP/T-odd；
   幅值差->宇称**。B.3 的『相位产生手征不对称』须改写为『幅值差产生宇称；
   相位产生 T-odd』，否则 deltaA_TUFT 无法成为唯一、可证伪、物理的数值预言。
