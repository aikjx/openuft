# _j127_lc_solver_and_ny4_decomposition · 机验读数（2026-11-23，第 105 轮 / J127 / 卷 148）

- 判词：`LC-SOLVER-BUILT-RANK24-UNIQUE--H3xR-NILMANIFOLD-LC-EXACT-NONFLAT-DIAGONAL-CURVATURE--NY4-ON-LC-EQUALS-PURE-TORSION-STAR-PAIR--CROSS-EXACT-ZERO-BOTH-DATASETS--INTEGRAL-EXACT--QJ125-1-SPLIT-1a-CLOSED-1b-OPEN-DIRAC-INSTRUMENT-REQUIRED`
- 硬闸：28/28，退出码 0
- 记分板：0/6（未变）

## 闸门

| 闸 | 名称 | 读数 | 判 |
|---|---|---|---|
| A00 | ★ 引擎修复回归锁（E-J125-1/E-J125-2）：p_mul 键长归一化——p·q={(1,1,0,0)}、1·p=p（变量部不丢）、p_add({()},p⁴键) 合并不分裂；interior 补回 v^μ 因子——ι_v〔v=[0,p,1+p²,0]〕作用于 dx₁∧dx₂∧dx₃ 得 p·dx₂∧dx₃ −（1+p²）·dx₁∧dx₃；J123/J124/J125 引擎字节不改动，其口径勘误登记卷 148 | p_mul 三对拍 ✓；interior 已知值 ✓（E-J125-2） | PASS |
| A01 | 引擎同步声明：Poly/Form/⋆/structure/ny4 逐字同层复用 _j125（含 E-J125-1 修复版 p_add/p_mul 与 E-J125-2 修复版 interior）；新增 lc/contortion 求解器、e-基转换、精确积分器；_j123/_j124/_j125 引擎文件零改动 | 引擎清单见卷 148 §一 | PASS |
| A02 | H₃×ℝ 标架：det M = 1 精确（单模剪切 I + p·E_{2,1}；det g = (det M)² = 1） | det M ≡ 1（Fraction 精确） | PASS |
| A03 | 结构常数（Maurer–Cartan）：dσ³ = −σ¹∧σ²（e-基 (0,1) 分量 = −1），dσ¹ = dσ² = dσ⁴ ≡ 0 —— Heisenberg⊕ℝ 闭代数 | dσ³ = −σ¹∧σ² 精确；其余恒零 | PASS |
| A04 | e-基表示常值性：de^a 的全部 e-基系数为常数多项式（左不变类 ⇒ LC 连接常系数的前提，求解器适用性确证） | 常值 ✓（12 分量全次数 0） | PASS |
| A05 | det g = (det M)² = 1 且 g·g⁻¹ = I 逐分量机器零（16/16） | det g ≡ 1 | PASS |
| A06 | 逆度量验证：g·g⁻¹ = I（H₃×ℝ 标架，g^{zz} = 1+p² 多项式精确） | 16/16 通过 | PASS |
| A07 | ⋆ 定义性质 ⟨α,β⟩ = ⟨β,α⟩（H₃×ℝ 标架，固定多项式数据） | 精确相等 | PASS |
| B01 | ★ LC 求解器建成：24×24 系统满秩 24 ⇒（Cartan 唯一性 declared ＋ 秩机器证据）ω_LC 唯一 | rank = 24/24 | PASS |
| B02 | LC 残差 ≡ 0：de^a + Σ_b ω^a_b∧e^b 全部恒零（dx-基 structure() 独立复算，含 p-项多项式恒等） | T_LC ≡ 0（4×恒零） | PASS |
| B03 | 对偶路径（方程/未知量双反序）：同一 ω_LC | 双路径逐位一致 | PASS |
| B04 | ★ 非平背景确证（e-基）：R_LC ≠ 0（3 个非零对）且 e-基分量纯对角、常系数——左不变类曲率常值性成立；dx-基 p-项在 e-基转换下精确抵消（机器证明） | R^{01}_e = {(0, 0, 0, 0): Fraction(-3, 4)}·e^0∧e^1; R^{02}_e = {(0, 0, 0, 0): Fraction(1, 4)}·e^0∧e^2; R^{12}_e = {(0, 0, 0, 0): Fraction(1, 4)}·e^1∧e^2 | PASS |
| B05 | 第一 Bianchi（LC）：Σ_b R^{ab}∧e^b ≡ 0（DT^a = 0 恒等式右端） | 4×恒零 | PASS |
| B06 | 第二 Bianchi：dR^{ab} + Σ_c(ω^{ac}∧R^{cb} − ω^{bc}∧R^{ca}) ≡ 0（矩阵交换子约定，R 入式） | 6×恒零 | PASS |
| C01 | ★ NY₄(ω_LC, T=0) 精确读数：对角曲率机制下 e^a∧e^b∧R^{ab} 全灭（R^{ab} ∝ e^a∧e^b ⇒ 楔积重复指标归零） | 精确零（LC 项贡献 = 0，机器裁定） | PASS |
| D01 | ★ contortion 求解（T*_A）：24×24 满秩 24 ⇒ 给定 T* 的 K 唯一（Σ_b K^a_b∧e^b = T*^a 与 LC 同型算子） | rank = 24/24 | PASS |
| D02 | K 残差与交叉复算（T*_A）：structure(ω_LC + K) 的挠率 ≡ T*_A 逐分量精确（K^a_b∧e^b = T*^a 的 dx-基多项式恒等实现） | T(ω_LC+K) ≡ T*_A（4×精确） | PASS |
| D03 | 对偶路径 K（T*_A）：同一解 | 双路径逐位一致 | PASS |
| D04 | 第二数据集 T*_B：K_B 唯一（rank 24）且 structure(ω_LC+K_B) 挠率 ≡ T*_B | rank = 24/24；T ≡ T*_B ✓ | PASS |
| E01 | ⋆-配对阳性（T*_A）：Σ_a T*^a∧⋆T*^a ≠ 0 且 NY₄_full 秩 4（拓扑密度正确秩） | 配对非零单项 1；NY₄ 秩 4 ✓ | PASS |
| E02 | ★ cross 双路径对拍（T*_A）：NY₄_full − ΣT∧⋆T − NY₄_LC ≡ −½Σ_{a,b} e^a∧e^b∧ΔR^{ab}（装配路径 vs 曲率差路径，逐基分量精确相等） | cross = 精确零；双路径一致 ✓ | PASS |
| E03 | 积分器自检：∫1 = 1；∫p² = 1/3；vol = e⁰∧e¹∧e²∧e³ 系数 ≡ 1 且 ∫vol = 1（基本域 = 紧商 nilmanifold 的 ℤ⁴ 基本域，Malcev 格点 declared） | ∫1=1  ∫p²=1/3  ∫vol=1 | PASS |
| E04 | ★ 紧商精确积分（T*_A）：∫ΣT∧⋆T = 精确有理数（非零）；∫NY₄_full = ∫ΣT∧⋆T + ∫cross 精确恒等式 | ∫ΣT∧⋆T = 2  ∫NY₄ = 2  ∫cross = 0 | PASS |
| E05 | 第二数据集（T*_B）同构检验：cross 双路径一致 + ∫ 恒等式 | cross = 精确零；∫ΣT∧⋆T = 2  ∫NY₄ = 2 | PASS |
| L01 | ★ Q-J125-1 拆分：1a（LC/contortion 分解）关闭——左不变多项式标架类内 LC 连接精确求解（rank 24 唯一）、K 由 T* 唯一确定、NY₄ = ΣT∧⋆T + cross 双路径精确提取；1b（∫NY₄ = Dirac index shift 的最终确认）开放——解锁条件 = Dirac 指标仪器（缺仪器，登记） | 1a CLOSED；1b OPEN（需 Dirac 指标仪器） | PASS |
| L02 | 总清册记账：Q-J125-1 拆分为 1a/1b ⇒ 总数 752 → 753，开放数不变 752 | 752 → 753（open 752） | PASS |
| L03 | 记分板 0/6 未变；幂等：固定数据无随机、纯确定性计算 | 0/6；见产物哈希 | PASS |
| L04 | ★ 勘误登记：E-J125-1（p_mul/p_add 键长截断 ⇒ J123–J125 标架数据退化为常值单模特例，其判定在真实数据上仍成立）与 E-J125-2（interior 丢 v^μ 因子 ⇒ J125 的 ⋆/NY₄ 定量读数失效，定性结论「挠率数据上 NY₄ 可非零」由本卷修复引擎重新确证：E01 pair_A = 2 ≠ 0）；J123/J124 经检索证实不使用 interior/hodge，不受影响 | 两则勘误入账；J127 修复版为现行引擎 | PASS |
