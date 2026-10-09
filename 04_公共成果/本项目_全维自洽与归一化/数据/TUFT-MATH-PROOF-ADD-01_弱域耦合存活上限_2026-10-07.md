# TUFT-MATH-PROOF-ADD-01 弱域耦合存活上限（模型无关约束）报告

- 引擎：源码/TUFT-MATH-PROOF-ADD-01_弱域耦合存活上限_2026-10-07.py
- 日期：2026-10-07
- 读数：4 guard —— PASS 4 / FAIL 0（退出码 0）

| PASS | beta_channel_omega_bound | |Omega_W|<6.3700e-03 (g2=0.65); |Omega_W|<1.2740e-03 (sqrt=0.130)；天然 0.01696 超限（需压低 2.7x/13.3x） |
| PASS | edm_channel_omega_bound | |Omega_W|<5.85e-14 (g2); |Omega_W|<1.17e-14 (sqrt)；天然 0.01696 超限约 3e+11 倍（相位/T-odd 通道实质关闭） |
| PASS | combined_survival_window | beta 存活窗 |Omega_W|<6.4e-03；EDM 存活窗 <5.9e-14（差 1e+11 量级）=> 保留复 Omega 只能走幅值差 eps 通道，且须压低到 ~1e-3 以下 |
| PASS | model_independent_bound | |Omega_W|_max(beta) in [1.3e-3, 6.4e-3]（g_SM 两口径）；|Omega_W|_max(EDM)~1e-13。任何版本须满足 beta 上限，且不能把相位当宇称源。 |

### 结论

1. **beta 通道（实幅值差 eps）**：deltaA=0.10*eps，eps=|Omega_W|/g_SM。
   存活 |deltaA|<0.001 => **|Omega_W| < 0.0098*g_SM** = 6.4e-3（g2）/ 1.27e-3（sqrt）。
   天然 |Omega_W|=alpha_W=0.01696 超限，须压低 **2.6-13.4 倍**。
2. **EDM 通道（相位 T-odd）**：Im lambda~2|Omega|/g_SM，d_n~theta_bar*1e-13<1.8e-26
   => **|Omega_W| < ~1e-13**。天然值超限约 1e11 倍 => **相位/T-odd 通道实质关闭**。
3. **合并存活窗**：beta 允许 ~1e-3 量级，EDM 仅 ~1e-13 => **无论 B.3 如何改稿，复 Omega 只能
   保留幅值差 eps 通道，且相位结构不能作为宇称源；弱域耦合须压低到 ~1e-3 以下**。
4. **模型无关**：此上限不依赖改稿方向，是任何 TUFT 弱域版本的硬约束。
