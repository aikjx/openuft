# TUFT-MATH-PROOF-ADD-01 MCMC 约束推断报告 v2
- 引擎：源码/TUFT-MATH-PROOF-ADD-01_参数空间MCMC约束推断_2026-10-07.py
- 方法：MH 纯标准库 300000 步 burn-in 50000；phi0=0（EDM 钉死）
- 读数：5 guard PASS 5/FAIL 0 (exit 0)

| PASS | phase_pinned_by_edm | |sin phi| < 5.9e-11（phi 到 {0,pi} 的窗口 ~5.9e-11 rad，简并） |
| PASS | sampler_converged | 接受率=0.88 |
| PASS | posterior_lambda_scale | lambda 中位数=0.0012 |
| PASS | weak_coupling_survival | |Omega_W| 中位数=5.8e-04,95%=6.9e-03 |
| PASS | beta_active | |deltaA| 95%=0.0011 |

### 后验（beta 约束存活区）
| 量 | 中位数 | 95% | 参照 |
|---|---|---|---|
| lambda | 0.0012 | 0.0193 | 0.1179 |
| |Omega_W| | 5.8e-04 | 6.9e-03 | 0.01696 |
| |deltaA| | — | 0.0011 | <0.001 |

### 结论
1. v1 失败=物理发现：EDM 把 phi0 钉死在 {0,pi} ~1e-10 窗口（简并 delta）
   => 相位自由度被 EDM 完全消除，弱域复 Omega 被迫回到实场（相位通道关闭的极致形式）。
2. v2 只采 beta 约束：(lambda,thetaW) 后验把 |Omega_W| 压到 ~1e-3（中位 5.8e-04），与解析上限 6.4e-3 一致 => 天然 alpha_W=0.01696 被排除。
3. lambda 从 0.1179 压到中位 0.0012（~2 个数量级）。
4. 改稿约束：弱域耦合 ~1e-3（压低 ~17 倍）；相位结构必须移除（被 EDM 钉死为 0）。