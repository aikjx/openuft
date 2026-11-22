# _j128_nomizu_cohomology_and_index_verdict · 机验读数（2026-11-23，第 106 轮 / J128 / 卷 149）

- 判词：`NOMIZU-EXACT-COHOMOLOGY-BUILT--BETTI-1-3-4-3-1-CHI-0-TAU-0-EULER-0--INDEX-D-0-EXACT--INTEGRAL-NY4-2-NONZERO--INTEGRAL-NY4-EQUALS-INDEX-SHIFT-REFUTED-ON-CLASS--QJ125-1b-CLOSED--QJ128-1-REGISTERED-LOCAL-HEAT-KERNEL-LAYER`
- 硬闸：18/18，退出码 0
- 记分板：0/6（未变）

## 闸门

| 闸 | 名称 | 读数 | 判 |
|---|---|---|---|
| A01 | 引擎同步声明：J127 修复版引擎逐字同层复用（E-J125-1 键长归一化＋E-J125-2 interior v^μ 因子）；新增不变形式复形、精确秩/Betti、交叠矩阵、Pfaffian；J123–J127 引擎文件零改动 | 引擎清单见卷 149 §一 | PASS |
| A02 | 不变形式复形建成：σ-基 16 维（C⁰..C⁴ = 1/4/6/4/1），d 规约 dσ³ = −σ¹∧σ²、d(σ³∧σ⁴) = −σ¹∧σ²∧σ⁴（Heisenberg⊕ℝ 结构常数的复形实现） | dσ³ = −σ¹σ²；d(σ³σ⁴) = −σ¹σ²σ⁴；维数 1/4/6/4/1 ✓ | PASS |
| B01 | d² = 0：全部基形式（1+4+6+4 = 15 个非常元素）二次微分为零（精确） | 15/15 恒零 | PASS |
| C1 | rank d¹ (C¹→C²) = 1（im = span(dσ³) = span(−σ¹σ²)） | rank = 1 | PASS |
| C2 | rank d² (C²→C³) = 1（im = span(−σ¹σ²σ⁴)，仅 d(σ³∧σ⁴) 非零） | rank = 1 | PASS |
| C3 | rank d³ (C³→C⁴) = 0（全部 3-形式闭） | rank = 0 | PASS |
| C4 | ★ Betti 数机器读数：b = (1, 3, 4, 3, 1) 精确（Künneth 交叉验证：H*(𝔥₃)=(1,2,2,1) ⊗ H*(ℝ)=(1,1) ⇒ (1,3,4,3,1) ✓） | b = (1,3,4,3,1) | PASS |
| D1 | Euler 示性数 χ = b⁰−b¹+b²−b³+b⁴ = 0（精确；紧 nilmanifold 纤维化于 S¹ ⇒ χ=0 一致） | χ = 0 | PASS |
| D2 | Euler 形式交叉：Pfaffian Pf = R^{01}∧R^{23} − R^{02}∧R^{13} + R^{03}∧R^{12} ≡ 0（e-基常系数曲率）⇒ ∫e-form = 0 = χ（Hirzebruch/Chern declared 归一化） | Pf 恒零（0 项）⇒ ∫e = 0 = χ ✓ | PASS |
| E1 | H² 确定性代表元：{σ¹σ³, σ²σ³, σ¹σ⁴, σ²σ⁴} 全部闭（ker d²）且不含 im d¹ 方向（σ¹σ² 分量为零）⇒ 4 维商空间代表元 ✓（b² = 4 一致） | 4 代表元全闭 ✓；b² = 4 | PASS |
| E2 | 配对良定性（Stokes）：∫(dσ³ ∧ Y) = 0 对全部 H² 代表元（紧流形上 exact∧closed 积分为零） | 4/4 精确零 | PASS |
| E3 | ★ 交叠矩阵机器读数：H² 交叠形式 = 两个双曲 2×2 块〔(0,∓1),(∓1,0)〕＋〔(0,1),(1,0)〕⇒ 特征值 ±1 对称 ⇒ 签名 τ = 0 精确 | 非零元 {'(0,1)': '-1', '(1,0)': '-1', '(2,3)': '1', '(3,2)': '1'} ⇒ τ = 0 | PASS |
| F1 | p₁-form ≡ 0 复算（Tr(R∧R) = Σ R^{ab}∧R^{ab}，对角机制）——J127 读数再现 | p₁-form 精确零 ⇒ ∫p₁ = 0 | PASS |
| F2 | ★ Hirzebruch 链（declared 公式＋机器读数）：τ = ∫L₁ = ∫p₁/3 = 0；指数链：index(D) = −τ/8 = 0（Â 公式 declared；自旋 declared：紧幂零流形可平行化 ⇒ w₂ = 0） | τ = 0；index(D) = 0（两者均为机器读数＋declared 公式的算术结论） | PASS |
| F3 | ∫NY₄ 复算（J127 路径再现，修复版引擎）：NY₄_full 秩 4 ≠ 0 且 ∫NY₄ = ∫ΣT∧⋆T = 2（Fraction 精确，T*_A 数据） | ∫ΣT∧⋆T = 2；∫NY₄ = 2 | PASS |
| F4 | ★ Q-J125-1b 裁定：∫NY₄ = 2 ≠ 0 = index(D) ⇒ 「∫NY₄ = Dirac index shift」在 H₃×ℝ 幂零类上**驳回**（机器矛盾）——NY₄ 是局域密度泛函，不是全局指标不变量（主符号不变形变下指标稳定：declared 标准定理）；1b CLOSED-AS-REFUTED-ON-CLASS；新登记 Q-J128-1：NY₄ 是否进入局域热核系数/Lichnerowicz 层（需局域热核仪器，缺仪器登记） | ∫NY₄ = 2 ≠ 0 = index(D) ⇒ 驳回成立 | PASS |
| L1 | 总清册记账：Q-J125-1b 关闭（本类驳回）⇒ 开放 752 → 751；新登记 Q-J128-1（局域热核层）⇒ 开放 751 → 752；总数 753 → 754 | 753 → 754（open 752 不变） | PASS |
| L2 | 记分板 0/6 未变；幂等：固定数据无随机、纯确定性计算 | 0/6；见产物哈希 | PASS |
