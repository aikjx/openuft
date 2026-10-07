# TUFT 统一场论攻破：UHECR GZK 判别力诊断报告
- 引擎：源码/突破_TUFT统一场论_UHECR_GZK判别力_2026-10-07.py
- 对象：TUFT 宣称的 GZK 截断 95%CI 是否真与 SM 区分
- 读数：6 guard PASS 6/FAIL 0 (exit 0)

| PASS | tuft_ci | E_GZK^TUFT ∈ [3.90e+19, 4.74e+19] eV |
| PASS | sm_canonical | SM 截断 ~5e+19 eV |
| PASS | naive_separation | SM 值=5.0e+19 > TUFT 上限 4.74e+19（分离 2.60e+18 eV，0.02 dex） |
| PASS | obs_systematic | 观测系统跨度 2.3e+19 eV（±0.10 dex） |
| PASS | sm_inside_obs | SM 5.0e+19 ∈ [4.0e+19, 6.3e+19] → 观测上不判别 |
| PASS | inflation_via_exclusion | TUFT-SM 分离 0.02 dex < 观测系统 0.1 dex → 吸收进系统误差，不判别 |

### 关键数值
| 量 | 值 | 含义 |
|---|---|---|
| TUFT E_GZK 95%CI | [3.90e+19, 4.74e+19] eV | 理论固有（ADD-01） |
| SM 阈值 | 5.0e+19 eV | log10≈19.7 |
| TUFT−SM 分离 | 2.60e+18 eV（0.02 dex） | 微小 |
| 观测系统误差 | ±0.1 dex → [4.0e+19, 6.3e+19] | ADD-01 刻意剥离 |

### 结论（GZK 判别力诊断）
1. **TUFT 宣称 E_GZK^TUFT=[3.90e+19, 4.74e+19] eV**，SM 阈值 5.0e19 恰在其上限之外（~2.60e+18 eV 分离）。
2. **但分离仅 ~0.02 dex**，而观测截断系统误差 ±0.1 dex（E∈[4.0e+19,6.3e+19]）——SM 值落入观测范围。
3. **ADD-01 刻意剥离宇宙线传播/观测系统误差**，宣称 CI 才显得排除 SM——这是 g-2 同款的精度通胀。
4. **攻破裁定**：GZK 维度与 g-2、弱域**同构**——TUFT 的「下移」在观测系统误差内无法分辨，安全但不可证伪。
5. **三观测量全部同构**（弱域宇称、g-2、GZK）：统一场论的可证伪性在结构上**系统性破产**——每个预言都落在「含 SM 的宽区间」。
6. **可证伪路径**：需观测截断能量系统误差收紧一个量级（±0.1 dex→±0.01 dex）且 TUFT 下移显著（>0.3 dex）方可判别。