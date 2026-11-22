# _j133_pme_maxent_eighth_candidate_convergence · 机验读数（2026-11-23，第 111 轮 / J133 / 卷 154）

- 判词：`PME-EIGHTH-CANDIDATE-EVALUATED--GAUSSIAN-FAMILY-BETA-FREE-R-CONTINUOUS-ALONE-REFUTED-FAMILY-CLASS--SELF-DUAL-INTERSECTION-BETA-PI-UNIQUE--R-EQUALS-1-OVER-PI-CONVERGES-WITH-J126-PENDING-CANDIDATE-TWO-INDEPENDENT-PRINCIPLE-PATHS--ESCAPE-1-EIGHT-CANDIDATES-CONVERGENCE-UPGRADED-PENDING-ADJUDICATION--`
- 硬闸：10/10，退出码 0
- 记分板：0/6（未变）

## 闸门

| 闸 | 名称 | 读数 | 判 |
|---|---|---|---|
| A01 | 算术声明：(F, π^k) 半域工具逐字同层复用 J126；declared 变分法（归一+二阶矩约束下最大熵 ⇒ 二次指数族）；J121–J132 引擎文件零改动 | 算术清单见卷 154 §一 | PASS |
| A02 | ★ P-ME 指数族（declared 变分法＋半域结构验证）：归一+⟨u²⟩=σ² 约束下最大熵 ⇒ f = exp(−βu²)，β = 1/(2σ²)；4 测试点上 ⟨u²⟩ = m₂/m₀ = 1/(2β) 逐点精确（约束-参数关系机器闭环） | 4/4 点 β = 1/(2σ²) ✓ | PASS |
| B01 | ★ 高斯族矩双路径（4 测试点 β = π, 1/π, π/4, 4π）：解析式 m₀、m₁、m₂ 半域精算；β-微分恒等 m₂ = −dm₀/dβ 逐点精确（解析半域导数 vs 直接积分式） | 4/4 双路径一致 ✓ | PASS |
| B02 | ★ r(β) = m₁/m₀ 四点读数（半域精确）：β=π ⇒ r = 1/π；β=1/π ⇒ r = 1；β=π/4 ⇒ r = 2/π；β=4π ⇒ r = 1/(2π)——r 随 β 连续自由 ⇒ **P-ME 单独否证**（族判类，与 J89『族』判据一致） | r(π)=1·π^-1  r(1/π)=1  r(π/4)=2·π^-1  r(4π)=1/2·π^-1 | PASS |
| C1 | ★ 自对偶交（declared 经典恒等式 FT[e^{−πu²}] = e^{−πu²}）：自对偶条件 β = π 在高斯族中**唯一点** ⇒ r = 1/π 精确（半域）——P-ME ∩ P-SD 的交 | β=π ⇒ r = 1·π^-1 | PASS |
| C2 | ★ 收敛确认（J126 继承复算）：P-ME+P-SD 候选 = e^{−πu²} = P-SD+P-UNC 候选 ⇒ r = 1/π 双路径精确一致——待裁候选获第二条独立原理路径收敛支持（收敛证据入账，裁决压力升级；裁决事项不代裁） | 双路径 r = 1/π 精确一致 ✓ | PASS |
| D1 | 下游表复用（J126 继承）：N_T = 1 + 5/(3π) ≈ 1.530516；Z/κ₆ = 12π/5 ≈ 7.539822（r = 1/π 的下游读数不变） | N_T ≈ 1.530516 | PASS |
| D2 | ★ 逃逸口① 账目：八候选（P-ME 单独否证入族判类，候选空间 7 → 8）；待裁候选 e^{−πu²}（r = 1/π）收敛证据 +1（两条独立原理路径：P-SD+P-UNC 与 P-ME+P-SD 殊途同归）；#15 保持开放；裁决事项不代裁；0/6 不变 | 八候选；收敛证据 +1；一裁待决维持 | PASS |
| L1 | 总清册记账：候选评估不动 Q 项 ⇒ 754 不变；逃逸口① 候选空间 7 → 8（账目内更新） | 754 不变 | PASS |
| L2 | 记分板 0/6 未变；幂等：固定数据无随机、纯确定性计算（半域 + declared） | 0/6；见产物哈希 | PASS |
