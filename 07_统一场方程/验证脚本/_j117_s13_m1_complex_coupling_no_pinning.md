# J117 M1 复数耦合谱与模长钉扎不可能（机读）

- 体积：卷 138 · 第 95 轮 · J117 · 2026-11-13
- 判决：PASS（结构审计 + 范围勘误；不是物理否证）
- 硬闸：75/75
- 记分板：0/6 不变；本册关闭 OPEN 0 条；新增已验证预言 0 条

## 一句话结论

- ζ=a+ib 时实生成元 A=λT+aJ−bI 满足 **A²+2bA+(λ²+a²+b²)I=0**；
  等价 **(A+bI)²=−(λ²+a²)I**。谱 = **{−b ± i√(λ²+a²)}**（各二重）。
- 也就是说：**只有 Re ζ 进频率，Im ζ 只给一个统一衰减率 −b**；
  b≠0 时流是对数螺线（阻尼/增益旋转），不是 J116 说的等角旋转。
- **det A=(λ²+a²+b²)²>0**、rank A=4 ⇒ 复 ζ 下仍只有静止解 Ψ≡0。
- M1 实线性 ⇒ **A(cX)=cA(X)** ⇒ 任何模长都是等价的；径向方程 ṙ=−br 的
  不动点只有 r=0（b≠0）或全体 r（b=0）⇒ **r=v 永远不是吸引子**。
- **∂_μJ^μ=−2 Im(ζ)|Ψ|²**（λ 项逐点相消，与 λ 复实无关）⇒ S13-C0001 的
  「∂_μJ^μ=0」只在**板块一（ζ=0）**成立；附录未声明 ζ∈ℝ。

## 四条结构方程（条件式，不是新物理）

- **E6 极小多项式**：A²+2bA+(λ²+a²+b²)I=0；(A+bI)²=−(λ²+a²)I。
- **E6′ 谱**：{−b±i√(λ²+a²)}（二重）；det=(λ²+|ζ|²)²；tr=−4b。
- **E7 J116 范围**：A²=−(λ²+ζ²)I 与纯转动是 b=0 切片。
- **E8 钉扎不可能**：A 实线性 ⇒ 不选模长；|Ψ|²=v² 只能外加。
- **E9 守恒破缺**：∂_μJ^μ=−2 Im(ζ)|Ψ|²。

## 三条勘误

- **volume 137 / J116 E1**：A^2=-(lambda^2+zeta^2)I stated without a reality qualifier → general identity is A^2+2bA+(lambda^2+a^2+b^2)I=0; the old form is b=0。影响：J116 numeric readings and its 78/78 gates are unaffected (its grid was real)
- **volume 137 / J116 rotation language**：'isoclinic rotation' with frequency sqrt(lambda^2+zeta^2) → with Im(zeta)!=0 the flow is a damped/growing rotation with frequency sqrt(lambda^2+Re(zeta)^2)。影响：presentation only; norm identity already allowed complex zeta
- **S13-C0001 / 附录A**：current conservation registered as verified; zeta has no reality condition → conservation holds iff Im(zeta)=0, i.e. for 板块一。影响：the verified claim is not false, but its scope must be stated

## 关键读数

- theta_lam1_re1: 1.414213562373
- period_at_b0: 4.442882938158
- det_lam1_zeta_1_plus_i: 9
- trace_lam1_zeta_1_plus_i: -4
- eigen_real_part: -1
- halflife_b1: 0.346573590280
- decay_rates_three_cases: [0.4, 0.4, 0.4]
- rk4_vs_analytic_error: 1.11e-15
- norm_relative_error: 1.428e-16
- scoreboards:
  - one_equation: 0/6
  - validated: 0
  - four_force_gut: 0
  - unique_C3: L_EW
  - open_items: 8
  - l4_open: 18
  - closed_by_this_volume: 0

## 为什么这不是「新统一」

- E6–E9 是对**既有方程**在复耦合下的结构判定与三处范围勘误。
- 「不能钉扎模长」是线性 M1 的性质，不排除未来某个非线性扩展；本册不提出该扩展。
- ζ 的物理起源（为什么它可能为实）没有被回答，`O-SCALE` 等 8 条 OPEN 全部保持。

## 边界

- 只审计 0+1 维齐次生成元、常数复 ζ；σ·∇ 项与非线性扩展不在口径内。
- 不判 M1 物理错误，不翻案任何既有判定，不改记分板 0/6。
- 锚点：equations.md／附录A／claims.csv／卷 137／_j116 脚本与产物。

## 硬闸明细

- [PASS] A01 M1 row carries the +iζΨ term and the |Ψ|²=v² constraint | anchor
- [PASS] A02 板块一 states the ζ-less equation (the ζ=0 slice) | 板块一 = M1 at ζ=0
- [PASS] A03 the symbol table defines ζ as a coupling but never says ζ∈ℝ | row: | $\zeta$ | 附加耦合（M1 线性项系数） |
- [PASS] A04 equations.md contains no reality assertion on ζ | no ζ∈ℝ anywhere
- [PASS] A05 S13-C0001 registers current conservation for the ζ-less equation | the verified claim is scoped to 板块一
- [PASS] A06 J116's generator grid is real-only (its E1 never saw Im ζ) | GRID entries are rationals, not complex
- [PASS] A07 J116 volume states A²=-(λ²+ζ²)I without a reality qualifier | the statement under repair
- [PASS] A08 novelty: this is the only *_j117_* script | single new script
- [PASS] A09 novelty: at most one registry section on complex coupling/pinning, and it is J117 | complex-coupling sections = 1
- [PASS] A10 v appears only in the constraint of the M1 row, never in the equation | one 'v' occurrence, inside |Ψ|²=v²
- [PASS] B01 T²=-I | T=ΘK
- [PASS] B02 J²=-I | J=multiplication by i
- [PASS] B03 {T,J}=0 | duality and phase generators anticommute
- [PASS] B04 A0²=-(λ²+a²)I for A0=λT+aJ (skew part) | 9 rational points
- [PASS] B05 (A+bI)²=-(λ²+a²)I  [shifted generator is a complex structure] | θ=√(λ²+a²) is the oscillation frequency
- [PASS] B06 E6: A²+2bA+(λ²+a²+b²)I=0 (minimal polynomial) | holds for complex ζ, all 9 points incl. b=0 and λ=a=0
- [PASS] B07 det A=(λ²+a²+b²)²=(λ²+|ζ|²)² | strictly positive unless everything vanishes
- [PASS] B08 tr A=-4 Im(ζ)= -4b | the trace counts the dilation
- [PASS] B09 the symmetric part of A is exactly -bI | A = skew + isotropic dilation
- [PASS] B10 rank A=4 on every grid point (no nonzero static solution) | det=c²>0
- [PASS] B11 A is real-linear: A(cX)=cA(X) | c∈{2,-3,1/5,7/3} × 9 points ⇒ scale covariance
- [PASS] B12 char poly det(xI-A)=(x²+2bx+c)² | ⇒ spectrum {-b±i√(λ²+a²)}, each twice
- [PASS] B-PC1 shifting b by 1/10 breaks the identity (non-zero residual) | detector can fail
- [PASS] C01 the 4×4 generator reproduces λΘΨ*+iζΨ in the (Reψ1,Imψ1,Reψ2,Imψ2) basis | 4 spinors × 9 couplings
- [PASS] C02 Θᵀ=-Θ | the source of the identities below
- [PASS] C03 Ψ†ΘΨ*≡0 for every spinor (kills the λ term in the norm flow) | 4 × 9 exact checks
- [PASS] C04 ΨᵀΘΨ≡0 for every spinor (kills the λ term on the conjugate side) | same antisymmetry
- [PASS] C05 i(ζ-ζ̄)=-2Im(ζ): only the imaginary part survives | E9 coefficient
- [PASS] C06 (ΘΨ*)†Ψ≡0: the conjugate λ term also vanishes | λ cancels pointwise for any complex λ
- [PASS] C-PC1 the coefficient detector distinguishes b=0 from b≠0 | b=0 ⇒ 0; b≠0 ⇒ nonzero
- [PASS] D01 RK4 equals e^{-bt}[cosθt I+sinθt A0/θ]X0 (err 1.11e-15) | λ=1, Imζ=2/5, Reζ=1/2
- [PASS] D02 the modulus is e^{-2bt}|X0|² (rel err 1.4e-16) | decay rate independent of λ and Re ζ
- [PASS] D03 b=0: X(2π/θ)=X0 (err 2.2e-16), pure rotation | J116's isoclinic rotation is the b=0 slice
- [PASS] D04 b≠0: |X(t+T)|²/|X(t)|²=e^{-2bT}=0.011154844 (no periodicity) | damped spiral
- [PASS] D05 the decay rate is -Im(ζ) for three different (λ,Re ζ): 0.400000000, 0.400000000, 0.400000000 | frequency does not affect the radial rate
- [PASS] D06 positivity scaling: cX(t) is the trajectory from cX0 | M1 is real-linear ⇒ no preferred modulus
- [PASS] D07 r(2v)/r(v)=2 at every t (here 2.000000000000) | the flow cannot distinguish v from 2v
- [PASS] D08 b>0: e^{-bT}=1 has no solution T>0 ⇒ only fixed modulus is 0 | r=0 is the only fixed point
- [PASS] D09 b=0: every modulus is neutral (e^0=1) | flat radial direction, still no selected v
- [PASS] D10 the hard constraint breaks scale covariance: |cΨ|=2v≠v for c=2 | ⇒ |Ψ|²=v² is not implied by the linear flow
- [PASS] D11 rank A=4 ⇒ no static solution except Ψ≡0 (complex ζ included) | E3 of J116 extended to Im ζ≠0
- [PASS] D-PC1 a pinning term detector fires on an injected term and not on M1 | M1–M6 carry no (|Ψ|²-v²)Ψ term
- [PASS] E01 with Re ζ≠0 the λ term still cancels: Ψ†ΘΨ*=0 (C03) | λ does not affect conservation
- [PASS] E02 with b≠0 the current is not conserved: ∂_μJ^μ=-2b|Ψ|² | E9
- [PASS] E03 at b=0 (板块一) conservation is restored: ∂_μJ^μ=0 | the registered claim's actual scope
- [PASS] E04 the registered S13-C0001 row has no ζ (it is the ζ=0 statement) | scope mismatch documented
- [PASS] E05 the symbol table imposes no reality condition on ζ | needs ζ∈ℝ for conservation
- [PASS] E06 for ζ=1+i the modulus halves at t=ln2/2=0.346573590280 | a 50%% loss is measurable in principle
- [PASS] E07 the divergence sign is -2Im(ζ), matching the norm flow of J116 | no contradiction: J116's norm identity already allowed complex ζ
- [PASS] E08 no new conserved current is claimed here | only the obstruction
- [PASS] E-PC1 divergence detector returns 0 exactly at b=0 and nonzero at b=2/5 | control
- [PASS] F01 J116's E1 statement is present and is the b=0 slice | volume 137, §E1
- [PASS] F02 J116's sampled couplings are all real | GRID line
- [PASS] F03 at b=0 the new generator equals J116's A(λ,ζ) | backward compatible on the real slice
- [PASS] F04 J116 readings reproduced: Ω(1,1)=1.414213562373, T=4.442882938158 | no contradiction with volume 137
- [PASS] F05 det reduces to J116's (λ²+ζ²)² on the real slice | the repair is additive, not a reversal
- [PASS] F-PC1 the unqualified A²=-(λ²+|ζ|²)I fails whenever b≠0 | so the erratum is detectable, not cosmetic
- [PASS] F06 J116 artifacts are untouched (json MD5 unchanged) | this volume supersedes nothing on disk
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
- [PASS] H03 this is an erratum-level structural result, not a new law | verdict string
- [PASS] H04 no non-linear pinning mechanism is proposed here | stated
- [PASS] H05 the origin of zeta is explicitly not addressed | stated
- [PASS] H06 the spatial operator is explicitly out of scope | stated
- [PASS] H07 zero verified predictions are added | 0
- [PASS] H08 the scoreboard cannot move on a structural identity | red line

> A structural audit is not a physical refutation; an erratum is not a discovery; the scoreboard stays 0/6 and no OPEN item is closed.
