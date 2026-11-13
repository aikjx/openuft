# J114 S13 A3 流势 BPS 畴壁扇区（机读）

- 体积：卷 135 · 第 92 轮 · J114 · 2026-11-13
- 判决：PASS（E1 条件下的条件数学定理）
- 硬闸：71/71
- 记分板：0/6 不变；本册关闭 OPEN 0 条

## 新方程（E1 条件下，单尺度 M = 1 无量纲代数）

```
V(g)    = (c/4)(g^2 - g*^2)^2 ,  eps = c g*^2 ,  V'(g) = -beta(g)
m^2     = 2 c g*^2 ,  w^2 = 2/(c g*^2)  =>  m w = 2
g(x)    = g* tanh(x/w)
sigma   = 4 g*^2/(3w) = (2/3) m g*^2
W(g)    = sqrt(c/2)(g*^2 g - g^3/3) ,  W' = sqrt(2V) ,  sigma = |dW|
sigma m = (16/3) dV ,  dV = c g*^4/4 = m^2 g*^2/8
sigma   = m^3/(3c)
L       = -d^2/dx^2 + V''(g(x)) :  0 < omega_1^2 = 3 m^2/4 < m^2
```

## 三条无量纲恒等式（与 c、g* 无关）

| 恒等式 | 精确值 | 读数 |
|---|---|---|
| m w | 2 | 2 |
| sigma m / dV | 16/3 | 5.333... |
| omega_1^2 / m^2 | 3/4 | omega_1/m = sqrt(3)/2 = 0.866025... |

## #725 精确化

原式 `sigma_wall ∝ m_P^3`（仅量纲估计）在 E1 下单尺度扇区成为
**`sigma = m^3/(3c)`**；字面 `m_P^3` 需要额外假设 `c = 1/3` 与 `m = m_P`。

## 量纲闭合（D 系列）

四个公式独立解出的提升指数一致：`dim[g*] = 1`（正则场必须带质量量纲 1）。

## 源锚点（当前字节）

- A3 cubic flow | 01_独立体系/S13_全域双向分形统一场论/02_基础公设/postulates.md:L33 | sha256_16=892e05fb435a370a
- A3 degenerate fixed points | 01_独立体系/S13_全域双向分形统一场论/02_基础公设/postulates.md:L29 | sha256_16=892e05fb435a370a
- M4 oddness | 01_独立体系/S13_全域双向分形统一场论/03_数学形式/equations.md:L14 | sha256_16=c3fc6fc1a23b6d55
- #725 wall density | 07_统一场方程/openuft_49_1000_core_formulae.md:L442 | sha256_16=66d90fee03aced6b

## 硬闸明细

- [PASS] A-anchor A3 cubic flow | 01_独立体系/S13_全域双向分形统一场论/02_基础公设/postulates.md:L33 sha=892e05fb435a370a
- [PASS] A-anchor A3 degenerate fixed points | 01_独立体系/S13_全域双向分形统一场论/02_基础公设/postulates.md:L29 sha=892e05fb435a370a
- [PASS] A-anchor M4 oddness | 01_独立体系/S13_全域双向分形统一场论/03_数学形式/equations.md:L14 sha=c3fc6fc1a23b6d55
- [PASS] A-anchor #725 wall density | 07_统一场方程/openuft_49_1000_core_formulae.md:L442 sha=66d90fee03aced6b
- [PASS] A05 novelty snapshot: postulates.md carries no kink/BPS solution | no 'tanh', no 'BPS' at these bytes
- [PASS] A05 novelty snapshot: equations.md carries no kink/BPS solution | no 'tanh', no 'BPS' at these bytes
- [PASS] E01 V'(g) = -beta(g) exactly (V is the exact antiderivative of the A3 flow) | V' = 1 * [c^1 g*^3 2^0 3^0 * (x^3 - 1*x)] | -beta = 1 * [c^1 g*^3 2^0 3^0 * (x^3 - 1*x)]
- [PASS] E02 V is even (A3 odd flow -> reflection-symmetric potential) | powers [0, 2, 4]
- [PASS] E03 V(+g*) = V(-g*) = 0 (two degenerate minima) | V(1)=0 V(-1)=0
- [PASS] E04 dV = c g*^4/4 (and = eps^2/(4c) with eps = c g*^2) | dV = 1 * [c^1 g*^4 2^-2 3^0 * (1)]
- [PASS] E05 V''(g*) = 2 c g*^2 =: m^2 | V''(g*) = 1 * [c^1 g*^2 2^1 3^0 * (1)] ; m^2 = 1 * [c^1 g*^2 2^1 3^0 * (1)]
- [PASS] E06 V''(0) = -m^2/2 exactly (barrier curvature is half the mass squared) | V''(0)/m^2 = -1/2
- [PASS] E-PC1 a quartic with the wrong normalisation is rejected | V/2 != V
- [PASS] K01 (1/2)(g')^2 = V(g) identically in t = tanh(x/w)  =>  w^2 = 2/(c g*^2) | kinetic = 1 * [c^1 g*^4 2^-2 3^0 * (x^4 - 2*x^2 + 1)]
- [PASS] K02 g'' = V'(g) = -beta(g) identically in t with the same w | g'' = 1 * [c^1 g*^3 2^0 3^0 * (x^3 - 1*x)]
- [PASS] K03 boundary conditions g(-inf) = -g*, g(+inf) = +g* | t -> +-1
- [PASS] K04 m w = 2 exactly (scale- and parameter-free) | m w = 1 * [c^0 g*^0 2^1 3^0 * (1)]
- [PASS] K-PC1 a 1% amplitude error breaks the ODE (residual = c g*^3 (1-a) != 0) | residual prefactor c^1 g*^3 2^-2 3^0 * (x^3 - 1*x)
- [PASS] K-PC2 a sqrt(2) width error breaks the kinetic/potential identity | kinetic != V
- [PASS] T01 int_{-1}^{1}(1-t^2)dt = 4/3 (Simpson, exact for degree <= 3) | I = 4/3
- [PASS] T02 sigma = 4 g*^2/(3w) = (2/3) m g*^2 (parameter-free coefficient) | sigma = 1 * [c^1/2 g*^3 2^3/2 3^-1 * (1)]
- [PASS] T03 sigma = (4/(3 sqrt2)) sqrt(c) g*^3 | sigma = 1 * [c^1/2 g*^3 2^3/2 3^-1 * (1)]
- [PASS] T04 (W')^2 = 2V exactly  =>  W' = sqrt(2V) | (W')^2 = 1 * [c^1 g*^4 2^-1 3^0 * (x^4 - 2*x^2 + 1)]
- [PASS] T05 dW/dg = W' (superpotential integrates the BPS equation) | W = -1 * [c^1/2 g*^3 2^-1/2 3^-1 * (x^3 - 3*x)]
- [PASS] T06 sigma = |W(+g*) - W(-g*)| exactly (BPS bound saturated) | |dW| = sigma
- [PASS] T07 g' = W' exactly for the kink (no leftover square term) | g' = W'
- [PASS] T08 sigma m = (16/3) dV exactly | sigma m = 1 * [c^1 g*^4 2^2 3^-1 * (1)]
- [PASS] T09 sigma = m^3/(3c) exactly (exactified core formula #725) | m^3/(3c) = 1 * [c^1/2 g*^3 2^3/2 3^-1 * (1)]
- [PASS] T10 the exact #725 chain sigma = (2/3) m g*^2 = m^3/(3c) with m^2 = 2 c g*^2 | closed
- [PASS] T-PC1 halving dV breaks sigma m / dV = 16/3 | dV/2 -> 32/3
- [PASS] F01 translational zero mode psi0 = sech^2 z solves L psi0 = 0 | L psi0 = c^0 g*^0 2^0 3^0 * (0)
- [PASS] F02 conjugated shape mode: M[t] = 3t (L(sech z tanh z) = 3 sech z tanh z) | M[t] = t * 3^1
- [PASS] F03 continuum threshold is 4 in z units, i.e. omega^2 = m^2 | w^2 m^2 = 1 * [c^0 g*^0 2^2 3^0 * (1)]
- [PASS] F04 omega_1^2 = 3/w^2 = (3/4) m^2 exactly (shape mode) | omega_1^2 = 1 * [c^1 g*^2 2^-1 3^1 * (1)]
- [PASS] F05 ordering 0 < 3 < 4 in z units: one bound state below the continuum | 0 (translation) < 3 (shape) < 4 (threshold)
- [PASS] F06 omega_1/m = sqrt(3)/2 follows from omega_1^2 = (3/4)m^2, omega_1 > 0 | omega_1/m = 0.866025...
- [PASS] F07 V''(0) < 0 but the spectrum is still bounded below (gradient term carries it) | spinodal at the wall centre, omega_1^2 > 0
- [PASS] F-PC1 a shape-mode eigenvalue of 2 instead of 3 fails the identity | 2t != 3t
- [PASS] D01 every formula forces the same promotion exponent dim[g*] = 1 | {'sigma = g*^2/w': Fraction(1, 1), 'm = c^(1/2) g*': Fraction(1, 1), 'dV = c g*^4': Fraction(1, 1), 'W = c^(1/2) g*^3': Fraction(1, 1)}
- [PASS] D02 [sigma] = [m^3] = [m^3/(3c)] = 3 with dim[g*] = 1 | 3 | 3 | 3
- [PASS] D03 [sigma m] = [dV] = 4 and [m w] = 0 with dim[g*] = 1 | 4 | 4 | 0
- [PASS] D-PC1 writing sigma = g*^3/(3w) would force dim[g*] = 2/3 (inconsistent) | 2/3 != 1
- [PASS] R01 m w = 2 has zero c/g* dependence | 2
- [PASS] R02 sigma m / dV = 16/3 has zero c/g* dependence | 16/3
- [PASS] R03 omega_1^2/m^2 = 3/4 has zero c/g* dependence | 3/4
- [PASS] R04 the three ratios are mutually distinct and all O(1) | 2 | 16/3 | 3/4
- [PASS] L01 #725 is a proportionality (no coefficient) at the anchored bytes | sigma_wall ~ m_P^3
- [PASS] L02 at c = 1/3 and m = m_P the exact formula gives sigma = m_P^3 (coefficient 1) | 1/(3c) at c=1/3 -> 1
- [PASS] L03 at c = 1 the coefficient is 1/3, not 1 (c = 1/3 is a real assumption) | 1/(3*1) = 1/3 != 1
- [PASS] L04 the exact statement is an equality, not a proportionality | sigma = m^3/(3c)
- [PASS] N01 Decimal-60 kink ODE residual |g''-V'| < 1e-45 at five points | max residual = 1.000E-61
- [PASS] N02 Decimal sigma equals the closed form to 1e-45 | 0.05796519532760777996 vs 0.05796519532760777996
- [PASS] N03 Decimal-60 shape-mode residual < 1e-45 (omega^2 = 3) | max residual = 1.000E-59
- [PASS] N04 Decimal-60 zero-mode residual < 1e-45 | max residual = 1.000E-60
- [PASS] N05 the numeric ratio sqrt(3)/2 reads 0.86602540378443864676... | sqrt(3)/2
- [PASS] S01 authoritative scoreboard is 0/6 | 0/6
- [PASS] S02 validated systems = 0 | validated=0
- [PASS] S03 correct four-force GUT equations = 0 | 0
- [PASS] S04 unique C3-level true unification is electroweak L_EW (2 forces) | L_EW
- [PASS] S05 ledger OPEN items stay at 8 | 8 OPEN, closed 0
- [PASS] S06 L4 physics layer OPEN items stay at 18 and S13 L3 predictions at 4 | 18 | 4 unreviewed
- [PASS] S07 this volume closes zero OPEN items | closed=0
- [PASS] S-PC1 a 6/6 scoreboard would be caught by the invariant | corrupted value detected
- [PASS] H01 the honest claim block passes its own validator | issues: none
- [PASS] H02 a corrupted claim block is caught on three counts | issues: ['class must be a conditional mathematical theorem', 'new_physics must be 0', 'scoreboard must stay 0/6']
- [PASS] H03 only A3 enters the algebra; A1 and A2 are declared unused | A1/A2 unused
- [PASS] H04 the kink charge Q_top = 1 is not A2's integer charge | Q_top = 1, field-space Z2, not A2
- [PASS] H05 the phi^4 kink is textbook and is not claimed as a discovery | credited as re-derivation
- [PASS] H06 spectrum completeness is inherited, not re-proved here | only two eigenfunctions are machine-checked
- [PASS] H07 no gravity backreaction, no cosmology, no network dynamics | planar static 1+1 reduction
- [PASS] H08 mathematical self-consistency is not physical confirmation | red line

> A conditional mathematical theorem is not new physics; a textbook kink is not a discovery.
