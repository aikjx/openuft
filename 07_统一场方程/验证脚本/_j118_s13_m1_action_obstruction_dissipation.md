# J118 M1 作用量不可能与耗散定理（机读）

- 体积：卷 139 · 第 96 轮 · J118 · 2026-11-13
- 判决：PASS（结构审计 + 范围勘误；不是物理否证）
- 硬闸：77/77
- 记分板：0/6 不变；本册关闭 OPEN 0 条；新增已验证预言 0 条

## 一句话结论

- **E10 双重/Nambu**：$M=\begin{pmatrix}\mathrm{i}\zeta I&\lambda\Theta\\\lambda\Theta&-\mathrm{i}\bar\zeta I\end{pmatrix}$
  满足 **M²+2bM+cI=0**、**tr M=−4b**、**det M=c²**；粒子-空穴 $P=\tau_xK$ 给 $P M P^{-1}=M$（恒等），
  手征 $C=\tau_zK$ 给 $C M C^{-1}=−M\Leftrightarrow\mathrm{Im}\,\zeta=0$。
- **E11 作用量不可能**：一阶系统 $\dot X=AX$ 有实二次作用量 $\Rightarrow$ 存在可逆反对称 $S$ 使 $SA$ 对称
  $\Rightarrow \operatorname{tr}A=0$；而 $\operatorname{tr}A=-4b$ $\Rightarrow$ **Im ζ≠0 时无单场二次实作用量**；
  双重化也救不回来（$\operatorname{tr}M=-4b$）。$A$ 与 $J$ 对易 $\Leftrightarrow\lambda=0$。
- **E12 对偶锐化**：$T A(\lambda,a,b)T^{-1}=A(\lambda,-a,b)$ $\Rightarrow$ **自对偶 $\Leftrightarrow\mathrm{Re}\,\zeta=0$**；
  J116 的「$\Leftrightarrow\zeta=0$」是 $b=0$（实 ζ）切片。
- **E13 交集**：守恒／体积／手征／作用量四条独立机制都选 **Im ζ=0**，对偶选 **Re ζ=0** $\Rightarrow$
  **交集 = ζ=0 = 板块一**。这是结构特权点，**不是物理选择**。

## 四条结构方程（条件式，不是新物理）

- **E10 Nambu**：$M^2+2bM+cI=0$，$c=\lambda^2+a^2+b^2$；$\operatorname{tr}M=-4b$；$\det M=c^2$。
- **E10 PH/手征**：$P M P^{-1}=M$ 恒等；$C M C^{-1}=-M\Leftrightarrow b=0$。
- **E11 迹障碍**：$\dot X=AX$ 变分 $\Rightarrow\operatorname{tr}A=0$；$\operatorname{tr}A=-4b$ $\Rightarrow$ Im ζ≠0 无作用量。
- **E12 对偶**：$T A T^{-1}=A(\lambda,-a,b)$ $\Rightarrow$ 自对偶 $\Leftrightarrow$ Re ζ=0。

## 两条勘误

- **volume 137 / J116 E4**：T A T^-1=A(lambda,-zeta); self-dual iff zeta=0 → with zeta=a+ib the map is A(lambda,-a,b), so self-dual iff Re(zeta)=0; J116's form is the b=0 slice。影响：J116 numeric readings and 78/78 are unaffected (its grid was real); only the scope changes
- **volume 137 / J116 E1 real slice**：all J116 statements sample real zeta → the general single-field generator carries Im(zeta) as an isotropic dilation -bI。影响：already repaired in J117; restated here for the action/duality chain

## 关键读数

- det_M_lam1_zeta_1_plus_i: 9
- trace_M_lam1_zeta_1_plus_i: -4
- det_Phi_1_at_b_2_5: 0.201896517995
- norm_decay_at_b_2_5: 0.449328964117
- halflife_b_half: 0.693147180560
- decay_rates_three_cases: [0.4, 0.4, 0.4]
- norm_relative_error: 1.428e-16
- el_residual_b0: 1.11e-16
- scoreboards:
  - one_equation: 0/6
  - validated: 0
  - four_force_gut: 0
  - unique_C3: L_EW
  - open_items: 8
  - l4_open: 18
  - closed_by_this_volume: 0

## 为什么这不是「新统一」

- E10–E13 是对**既有方程**在复耦合下的结构判定与两处范围勘误。
- 「无单场二次作用量」只否证**线性、常数系数、二次作用量**这一层；不排除非局域/非线性/约束系统（本册不提出）。
- ζ 的物理起源（为什么它可能为实）没有被回答，`O-SCALE` 等 8 条 OPEN 全部保持。
- 板块一是唯一同时满足四条结构要求的点，但这只是结构特权，不是对 ζ=0 的物理选择。

## 边界

- 只审计 0+1 维齐次生成元、常数复 ζ、实 λ（文档约定）；σ·∇ 项与非线性扩展不在口径内。
- 不判 M1 物理错误，不翻案任何既有判定，不改记分板 0/6。
- 锚点：equations.md／附录A／claims.csv／卷 137／卷 138／_j116、_j117 脚本与产物。

## 硬闸明细

- [PASS] A01 M1 row carries the +iζΨ term and the |Ψ|²=v² constraint | anchor
- [PASS] A02 板块一 states the ζ-less equation (the ζ=0 slice) | 板块一 = M1 at ζ=0
- [PASS] A03 the symbol table defines ζ as a coupling but never says ζ∈ℝ | row: | $\zeta$ | 附加耦合（M1 线性项系数） |
- [PASS] A04 equations.md contains no reality assertion on ζ | no ζ∈ℝ anywhere
- [PASS] A05 S13-C0001 registers current conservation for the ζ-less equation | the verified claim is scoped to 板块一
- [PASS] A06 J116's generator grid is real-only (its E4 never saw Im ζ) | GRID entries are rationals, not complex
- [PASS] A07 J116 volume states the duality map and 'self-dual ⇔ ζ=0' | the statement to be sharpened
- [PASS] A08 J117 volume carries E9 (current breaking) and its G1 grid | upstream complex-zeta result
- [PASS] A09 novelty: this is the only *_j118_* script | single new script
- [PASS] A10 novelty: at most one registry section on M1 action/dissipation, and it is J118 | action/dissipation sections = 1
- [PASS] A11 both upstream artifacts exist and are readable | J116/J117 json present
- [PASS] B01 Θ²=-I (the Θ in the doubled build is a complex structure) | Θ=[[0,-1],[1,0]]
- [PASS] B02 E10: M²+2bM+cI=0 for the doubled Nambu generator (exact, 9 points) | M=[[iζI,λΘ],[λΘ,−iζ̄I]], λ real, c=λ²+a²+b²
- [PASS] B03 shifted form (M+bI)²=−(λ²+a²)I | same frequency θ=√(λ²+a²) as J117
- [PASS] B04 tr M=−4b | the dilation is mirrored in the doubled generator
- [PASS] B05 det M=c²=(λ²+|ζ|²)² | strictly positive unless everything vanishes
- [PASS] B06 particle-hole P=τ_x K gives +M identically: P M P⁻¹=M | independent of ζ; the physical subspace is the +1 eigenspace
- [PASS] B07 chiral C=τ_z K gives −M ⇔ Im ζ=0 (b=0) | a ℤ₂ grading exists only on the real slice
- [PASS] B08 the PH constraint V₂=V₁* is exact: M(ψ,ψ*)=(φ,φ*) with φ=iζψ+λΘψ* | 4 spinors × 9 couplings
- [PASS] B09 M is ℂ-linear (M(iV)=iM(V)): the pairing is linearized on doubling | so the antilinear λ term is not itself an action obstruction
- [PASS] B-PC1 shifting b by 1/10 breaks the doubled identity (nonzero residual) | detector can fail
- [PASS] B10 key number: at λ=1, ζ=1+i the doubled det M=9 and tr M=−4 | det M=c²=9, tr M=−4b=−4
- [PASS] C01 T is antilinear: T(JX)=−J T(X) | T=ΘK does not commute with multiplication by i
- [PASS] C02 [A,J]=2λ(TJ): A is ℂ-linear ⇔ λ=0 | λ≠0 breaks ℂ-linearity; only λ=0 is holomorphic
- [PASS] C03 tr A=−4b | the trace counts the dissipation
- [PASS] C04 lemma: S antisym invertible, K sym ⇒ tr(S⁻¹K)=0 | ⇒ a first-order variational system always has tr A=0
- [PASS] C05 variational ⇒ tr A=0 ⇒ b=0 (trace obstruction) | contrapositive: tr A=−4b≠0 excludes an action
- [PASS] C06 at b=0 the action exists: S=A antisym, K=A² sym, S⁻¹K=A ⇒ Ẋ=AX | explicit quadratic Lagrangian L=½XᵀSẊ−½XᵀKX
- [PASS] C07 the constructed action's Euler–Lagrange residual vanishes on the trajectory (1.1e-16) | λ=1, Reζ=1/2, b=0
- [PASS] C08 b≠0: Aᵀ+A=−2bI≠0 (A is not skew anymore) | the symmetric part is exactly the dissipation
- [PASS] C09 doubling does not cure it: tr M=−4b≠0 for b≠0 | the Nambu generator inherits the same trace obstruction
- [PASS] C-PC1 the trace detector distinguishes b=0 from b≠0 | b=0 ⇒ tr=0; b=2/5 ⇒ tr=−8/5
- [PASS] C11 over the grid: variational (tr A=0) ⇔ b=0 | 9 points
- [PASS] D01 d|Ψ|²/dt=−2b|Ψ|² (rel err 1.4e-16) | modulus decay rate is −Im ζ
- [PASS] D02 Liouville: det Φ(1)=e^{−4b}=0.201896517995 (err 3.1e-15) | volume contraction rate tr A=−4b
- [PASS] D03 b>0 decays, b<0 grows: e^{−0.8}=0.449328964117, e^{+0.8}=2.225540928492 | sign of Im ζ is gain/loss
- [PASS] D04 the decay rate is −Im ζ for three different (λ,Re ζ): 0.400000000, 0.400000000, 0.400000000 | frequency does not affect the radial rate
- [PASS] D05 b=1/2: half-life t=ln2=0.693147180560 | |Ψ|² halves at t=ln2
- [PASS] D06 key number: e^{−4b} at b=2/5 is 0.201896517995 | phase-space volume in unit time
- [PASS] D-PC1 the sign detector: b>0 ⇒ log decay positive, b<0 ⇒ negative | control
- [PASS] D07 b>0 drives every nonzero modulus to 0 as t→∞ | t=60, b=0.4
- [PASS] E01 E12: T A(λ,a,b) T⁻¹ = A(λ,−a,b) | 9 points; T maps Re ζ → −Re ζ and keeps Im ζ
- [PASS] E02 self-dual ⇔ Re ζ=0 | the fixed-point condition only kills the real part
- [PASS] E03 on the real slice (b=0): self-dual ⇔ a=0 ⇔ ζ=0 (J116's exact statement) | J116 E4 is the b=0 slice of E12
- [PASS] E04 erratum: J116 E4 'self-dual ⇔ ζ=0' must be read as '⇔ Re ζ=0' for complex ζ | volume 137 §6 is being scoped, not reversed
- [PASS] E-PC1 treating the a-term as even would falsely claim self-duality | detector distinguishes even/odd
- [PASS] E05 T²=−I and T⁻¹=−T | T is a real involution up to sign
- [PASS] E06 T is a real matrix (so T⁻¹ is exact, no conjugation ambiguity) | all entries rational
- [PASS] E07 at Re ζ=0 a sample vector confirms T A X = A T X | a=0, b=2/5: self-dual on a concrete vector
- [PASS] F01 current conservation ⇔ Im ζ=0 (E9) | ∂_μJ^μ=−2 Im(ζ)|Ψ|²
- [PASS] F02 norm/volume preservation ⇔ Im ζ=0 (E8 + D01/D02) | d|Ψ|²/dt=−2b|Ψ|²
- [PASS] F03 chiral PH C M C⁻¹=−M ⇔ Im ζ=0 (E10) | ℤ₂ grading wants b=0
- [PASS] F04 a real quadratic action exists ⇔ Im ζ=0 (E11) | trace obstruction
- [PASS] F05 T-duality ⇔ Re ζ=0 (E12) | the only criterion that touches Im ζ
- [PASS] F06 intersection of all five criteria ⇔ ζ=0 | three select Im ζ=0, duality selects Re ζ=0
- [PASS] F07 at ζ=0 the generator is exactly λT (板块一) and all five criteria hold | the unique structurally privileged point
- [PASS] F08 the truth table is machine-derived on every grid point (9) | not hand-asserted
- [PASS] F-PC1 the table is not all-true: e.g. (λ,a,b)=(1,1,1) fails four criteria | detector would notice a constant table
- [PASS] F09 ζ=0 is structurally privileged but still gapless in this audit (spec ±iλ) | A²=−λ²I at ζ=0: pure rotation, no mass gap; scoreboard stays 0/6
- [PASS] G01 authoritative scoreboard is 0/6 | 0/6
- [PASS] G02 validated systems = 0 | validated=0
- [PASS] G03 correct four-force GUT equations = 0 | 0
- [PASS] G04 unique C3-level true unification is electroweak L_EW | L_EW (2 forces)
- [PASS] G05 ledger OPEN items stay at 8 | 8 OPEN
- [PASS] G06 L4 physics layer stays at 18 OPEN | 18 OPEN
- [PASS] G07 this volume closes zero OPEN items | closed=0
- [PASS] G08 this volume adds zero verified predictions | 0 new verified
- [PASS] G-PC1 a 6/6 scoreboard would be caught | detected
- [PASS] H01 the honest claim block passes its own validator | issues: none
- [PASS] H02 a corrupted claim block is caught on four counts | issues: 4
- [PASS] H03 this is a structural result, not a new law | verdict string
- [PASS] H04 no pinning / real-making mechanism is proposed here | stated
- [PASS] H05 the origin of zeta is explicitly not addressed | stated
- [PASS] H06 the spatial operator is explicitly out of scope | stated
- [PASS] H07 zero verified predictions are added | 0
- [PASS] H08 the scoreboard cannot move on a structural identity | red line
- [PASS] H09 plate one being privileged is not a physical selection of zeta=0 | stated

> A structural audit is not a physical refutation; a scope erratum is not a discovery; the scoreboard stays 0/6 and no OPEN item is closed.
