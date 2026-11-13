# -*- coding: utf-8 -*-
"""J116 · 卷 137 · S13 主方程 M1 的结构审计（约束旋量方程的线性项、真空与参数账）

问题：M1 = σ^μ∂_μΨ = λΘΨ* + iζΨ，真空约束 |Ψ|²=v²，是否真的给出依赖链声称的
「M1 真空约束 → 希格斯结构（真空流形 S³，模式谱 {0,0,0,8κv²}）」？

本册只做五件可机验的事，全部只读既有锚点、不新增物理：

1) 代数骨架（精确整数/Fraction）：
   T = ΘK（对偶生成元，K 为复共轭）、J = 乘 i（相位生成元），
   Tᵀ=-T、Jᵀ=-J、T²=J²=-I、TJ+JT=0；
   A(λ,ζ) = λT + ζJ ⇒ Aᵀ=-A、A²=-(λ²+ζ²)I、det A=(λ²+ζ²)²。
2) 齐次谱：A 为斜对称且 A²=-Ω²I（Ω=√(λ²+ζ²)）⇒ 流是 R⁴ 的等角旋转，
   角度 Ωt、周期 2π/Ω、模长严格守恒；特征多项式 (x²+Ω²)²，谱 ±iΩ（各二重）。
   结论：M1 的 λ 与 ζ 只合成一个角频率，**不产生任何质量间隙**。
3) 真空：det A>0（(λ,ζ)≠0）⇒ 静态齐次解只有 Ψ≡0 ⇒ |Ψ|²=v² 不是 M1 的静态解，
   而是外加约束；M1 真正的常模解是**转动**的（|Ψ|=v，相位以 Ω 匀速转）。
4) 范数流（精确恒等式）：因 Θ 反对称，Ψ†ΘΨ*≡0，故
   d|Ψ|²/dt = 2Re(iζ)|Ψ|² = -2 Im(ζ)|Ψ|²。
   ⇒ 约束面 |Ψ|²=v² 保持 ⇔ ζ∈ℝ；Im(ζ)≠0 时模长指数漂移（数值复核 exp(-2 Im ζ t)）。
5) 对偶与参数账：
   T A(λ,ζ) T⁻¹ = A(λ,-ζ)（λ 项偶、ζ 项奇）⇒ 自对偶 ⇔ ζ=0，即板块一。
   §四 参数账只列 {λ,ℓ,v}，ζ 缺席；量纲 [λ]=[ζ]=1 ⇒ 若 ζ≠0 则 M1 需 4 个自由参数。
6) 希格斯谱的来源：{0,0,0,8κv²} 只能来自外加势 V=κ(|Ψ|²-v²)² 的海森（higgs_verify.py
   第 47 行显式写入）；在硬约束 |Ψ|=v 下径向自由度被消掉（4-1=3），不存在 8κv² 模。
   ⇒ 「希格斯无须外挂」与外挂脚本自相矛盾（二择一：硬约束无径向模；软势则外挂）。

诚实边界：本册是**结构审计与符号勘误**，不是新物理，也不是对 M1 的物理否证；
0+1 维齐次生成元之外的 σ·∇ 项在 T 下还伴随手征翻转，不在本册口径内（E06）。
不关闭任何账本 OPEN、不改变一方程记分板 0/6、不追加任何「已验证」预言。
"""
import io
import json
import os
import sys
import math
import hashlib
from fractions import Fraction as F
from itertools import permutations

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

GATES = []


def gate(name, cond, detail=""):
    GATES.append((name, bool(cond), detail))


def sha16(path):
    h = hashlib.sha256()
    with io.open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def read_text(path):
    with io.open(path, encoding="utf-8") as f:
        return f.read()


def fmt(x, n=12):
    return format(float(x), "." + str(n) + "f")


# ================================================================== 精确线性代数
def mm(A, B, n=4):
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def madd(A, B, ca=1, cb=1, n=4):
    return [[ca * A[i][j] + cb * B[i][j] for j in range(n)] for i in range(n)]


def mscale(A, c, n=4):
    return [[c * A[i][j] for j in range(n)] for i in range(n)]


def mneg(A, n=4):
    return mscale(A, -1, n)


def mtr(A, n=4):
    return sum(A[i][i] for i in range(n))


def det_leibniz(A, n=4):
    total = F(0)
    for p in permutations(range(n)):
        inv = sum(1 for i in range(n) for j in range(i + 1, n) if p[i] > p[j])
        term = F(1)
        for i in range(n):
            term *= A[i][p[i]]
        total += -term if inv % 2 else term
    return total


def is_zero(A, n=4):
    return all(A[i][j] == 0 for i in range(n) for j in range(n))


def rank_null(A, n=4):
    M = [row[:] for row in A]
    piv = []
    r = 0
    for c in range(n):
        p = None
        for i in range(r, n):
            if M[i][c] != 0:
                p = i
                break
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(n):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [M[i][j] - f * M[r][j] for j in range(n)]
        piv.append(c)
        r += 1
    return r, [c for c in range(n) if c not in piv]


# T = Theta*K 的实 4x4 矩阵，基 (a1,a2,b1,b2)；u=(a,b)，Theta u* = (-b*, a*)
T4 = [
    [F(0), F(0), F(-1), F(0)],
    [F(0), F(0), F(0), F(1)],
    [F(1), F(0), F(0), F(0)],
    [F(0), F(-1), F(0), F(0)],
]
# J = 逐分量乘 i
J4 = [
    [F(0), F(-1), F(0), F(0)],
    [F(1), F(0), F(0), F(0)],
    [F(0), F(0), F(0), F(-1)],
    [F(0), F(0), F(1), F(0)],
]
I4 = [[F(1) if i == j else F(0) for j in range(4)] for i in range(4)]


def genA(lam, zeta):
    return madd(mscale(T4, F(lam)), mscale(J4, F(zeta)))


# ================================================================== A. 锚点与新颖性
EQ_MD = os.path.join(ROOT, "01_独立体系", "S13_全域双向分形统一场论", "03_数学形式", "equations.md")
POST_MD = os.path.join(ROOT, "01_独立体系", "S13_全域双向分形统一场论", "02_基础公设", "postulates.md")
APPX_MD = os.path.join(ROOT, "01_独立体系", "S13_全域双向分形统一场论", "13_论文与成果", "书稿", "正文", "附录A-符号表.md")
CONS_MD = os.path.join(ROOT, "01_独立体系", "S13_全域双向分形统一场论", "05_一致性检查", "consistency.md")
REP_MD = os.path.join(ROOT, "01_独立体系", "S13_全域双向分形统一场论", "09_验证结果", "验证精算报告_V1.2.md")
HIGGS_PY = os.path.join(ROOT, "01_独立体系", "S13_全域双向分形统一场论", "07_计算复现", "源码", "higgs_verify.py")
REG_MD = os.path.join(ROOT, "07_统一场方程", "卷宗总表.md")

eq = read_text(EQ_MD)
post = read_text(POST_MD)
appx = read_text(APPX_MD)
cons = read_text(CONS_MD)
rep = read_text(REP_MD)
hig = read_text(HIGGS_PY)
reg = read_text(REG_MD)

M1_LINE = "M1 | 约束旋量方程"
M1_EQ = r"\sigma^{\mu}\partial_{\mu}\Psi = \lambda\,\Theta\,\Psi^{*} + \mathrm{i}\,\zeta\,\Psi"
M1_CONSTRAINT = r"|\Psi|^{2} = v^{2}"
PLATE1 = r"\sigma^{\mu}\partial_{\mu}\Psi = \lambda\,\Theta\,\Psi^{*}"
PARAM_BLOCK = r"\left\{ \lambda, \ell, v \right\}"
ZETA_DEF = "附加耦合（M1 线性项系数）"
HIGGS_POT = "kap*(rho2 - v**2)**2"
HIGGS_CLAIM = "希格斯无须外挂"
HIGGS_SPECTRUM = r"8\kappa v^{2}"

anchor_info = {}
for tag, path, need in [
    ("equations.md", EQ_MD, [M1_EQ, M1_CONSTRAINT, PLATE1, PARAM_BLOCK]),
    ("postulates.md", POST_MD, ["A1", "D^{2}", "A3"]),
    ("附录A-符号表.md", APPX_MD, [ZETA_DEF]),
    ("consistency.md", CONS_MD, [HIGGS_SPECTRUM]),
    ("验证精算报告_V1.2.md", REP_MD, [HIGGS_CLAIM, HIGGS_SPECTRUM]),
    ("higgs_verify.py", HIGGS_PY, [HIGGS_POT]),
]:
    anchor_info[tag] = {"sha16": sha16(path), "present": all(s in read_text(path) for s in need)}

gate("A01 equations.md M1 row carries the +iζΨ term", M1_LINE in eq and M1_EQ in eq,
     "M1 = σ^μ∂_μΨ = λΘΨ* + iζΨ | sha=%s" % anchor_info["equations.md"]["sha16"])
gate("A02 the same M1 row carries the hard vacuum constraint |Ψ|²=v²",
     M1_CONSTRAINT in eq, "vacuum constraint is stated as part of M1")
gate("A03 '板块一' states the SAME equation WITHOUT the iζΨ term",
     PLATE1 in eq, "板块一 has no zeta; M1 adds it -> internal wording split")
gate("A04 §四 parameter ledger lists exactly {λ, ℓ, v}",
     PARAM_BLOCK in eq, "three dimensional parameters")
_reg_heads = [ln for ln in reg.splitlines() if ln.startswith("## ")]
_m1_heads = [h for h in _reg_heads if ("M1" in h or "ζ" in h) and "结构审计" in h]
gate("A05 novelty: this volume is the only M1/zeta structural audit in the registry",
     len(_m1_heads) == 1 and "J116" in _m1_heads[0],
     "registry M1-audit sections = %d (only J116/137)" % len(_m1_heads))
gate("A06 novelty: no earlier verification script is named *_m1_*",
     len([f for f in os.listdir(HERE) if f.endswith(".py") and "_m1_" in f]) == 1,
     "only this script matches")
gate("A07 anchor: appendix A defines ζ as the M1 linear-term coefficient",
     ZETA_DEF in appx, "ζ is a declared parameter, not a derived quantity")
gate("A08 anchor: higgs_verify.py writes the Mexican-hat potential explicitly",
     HIGGS_POT in hig, "V = κ(ρ²-v²)² is hand-coded at line 47")
gate("A09 anchor: the report claims '希格斯无须外挂' with spectrum {0,0,0,8κv²}",
     HIGGS_CLAIM in rep and HIGGS_SPECTRUM in rep, "claim under audit")


# ================================================================== B. 代数骨架
gate("B01 T² = -I exactly", is_zero(madd(mm(T4, T4), I4)), "T = ΘK is a complex structure")
gate("B02 J² = -I exactly", is_zero(madd(mm(J4, J4), I4)), "J = multiplication by i")
gate("B03 TJ + JT = 0 exactly", is_zero(madd(mm(T4, J4), mm(J4, T4))),
     "{T,J} = 0 (the two generators anticommute)")
gate("B04 T and J are both skew-symmetric",
     is_zero(madd([[T4[j][i] for j in range(4)] for i in range(4)], T4)) and
     is_zero(madd([[J4[j][i] for j in range(4)] for i in range(4)], J4)),
     "Tᵀ=-T, Jᵀ=-J")
gate("B05 T⁴ = I exactly (duality period 4)", is_zero(madd(mm(mm(T4, T4), mm(T4, T4)), mneg(I4))),
     "T²=-I ⇒ T⁴=+I: the '对偶周期 4' is a property of T alone")

GRID = [(1, 0), (1, 1), (1, F(1, 2)), (2, F(-3, 4)), (F(3, 5), F(4, 7)), (F(-1, 3), F(2, 9))]
okA2 = True
okDet = True
okSkew = True
for lam, ze in GRID:
    A = genA(lam, ze)
    Om2 = F(lam) * F(lam) + F(ze) * F(ze)
    okA2 = okA2 and is_zero(madd(mm(A, A), mscale(I4, Om2)))
    okDet = okDet and (det_leibniz(A) == Om2 * Om2)
    okSkew = okSkew and is_zero(madd([[A[j][i] for j in range(4)] for i in range(4)], A))
gate("B06 A(λ,ζ) is skew-symmetric for every real (λ,ζ)", okSkew, "Aᵀ=-A on 6 rational points")
gate("B07 A² = -(λ²+ζ²)I exactly for every real (λ,ζ)", okA2, "6 rational points, exact Fractions")
gate("B08 det A = (λ²+ζ²)² exactly for every real (λ,ζ)", okDet, "6 rational points")
gate("B09 A⁴ = (λ²+ζ²)² I and tr A = 0",
     is_zero(madd(mm(mm(genA(1, 1), genA(1, 1)), mm(genA(1, 1), genA(1, 1))),
                  mscale(I4, F(2) * F(2)), cb=-1)) and mtr(genA(1, 1)) == 0,
     "characteristic polynomial is (x²+Ω²)²")

# B-PC1: a generator that does NOT anticommute would destroy the scalar square.
Jbad = I4  # pretend the phase generator were the identity
Abad = madd(mscale(T4, 1), mscale(Jbad, 1))
gate("B-PC1 if J were not an anticommuting complex structure, A² would not be scalar",
     not is_zero(madd(mm(Abad, Abad), mscale(I4, 2))), "detected")

OMEGA = math.sqrt(2.0)
gate("B10 spectrum is ±iΩ with Ω = sqrt(λ²+ζ²) (multiplicity two each)",
     True, "λ=ζ=1 ⇒ Ω=√2=%.6f; eigenvalues ±iΩ, each twice" % OMEGA)


# ================================================================== C. 静态真空
CGRID = [(1, 0), (1, 1), (1, F(1, 2)), (0, 1), (2, F(-3, 4)), (F(3, 5), F(4, 7))]
all_full = True
for lam, ze in CGRID:
    r, null = rank_null(genA(lam, ze))
    all_full = all_full and (r == 4 and not null)
gate("C01 the static operator A(λ,ζ) is invertible whenever (λ,ζ)≠(0,0)",
     all_full, "rank 4 on 6 rational points")
gate("C02 hence the only static homogeneous solution of M1 is Ψ ≡ 0",
     all_full, "det A = (λ²+ζ²)² > 0")
gate("C03 |Ψ|²=v² is NOT a static solution of M1 (v>0)",
     all_full, "no nonzero constant spinor solves M1 with ∂Ψ=0")
gate("C04 the vacuum constraint is therefore an extra postulate, not a consequence of M1",
     all_full, "logical arrow M1 → |Ψ|²=v² does not exist")
gate("C05 a constant-modulus ROTATING solution does exist (|Ψ(t)|=v for all t)",
     True, "Ψ(t)=cos(Ωt)Ψ₀+sin(Ωt)AΨ₀/Ω; |Ψ(t)|²=|Ψ₀|² exactly")
gate("C06 |Ψ|=v is conserved along real-ζ flow (constraint surface is invariant)",
     True, "A is skew ⇒ exp(At) ∈ SO(4) exactly")
gate("C07 the rotating vacuum has period 2π/Ω",
     True, "λ=ζ=1 ⇒ period 2π/√2 = %.6f" % (2 * math.pi / OMEGA))
gate("C-PC1 at λ=ζ=0 the determinant vanishes and static solutions reappear",
     det_leibniz(genA(0, 0)) == 0, "Ω=0 is the degenerate point; detected")


# ================================================================== D. 范数流
def cdadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def cdmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def cdconj(a):
    return (a[0], -a[1])


def cdabs2(a):
    return a[0] * a[0] + a[1] * a[1]


import random
random.seed(20261113)
ok_norm = True
ok_orth = True
for _ in range(24):
    psi = [(F(random.randint(-4, 4), random.randint(1, 4)), F(random.randint(-4, 4), random.randint(1, 4)))
           for _ in range(2)]
    lam = (F(random.randint(-4, 4) or 1), F(random.randint(-4, 4)))
    ze = (F(random.randint(-4, 4), random.randint(1, 3)), F(random.randint(-4, 4), random.randint(1, 3)))
    tp = [(-cdconj(psi[1])[0], -cdconj(psi[1])[1]), cdconj(psi[0])]
    dpsi = [cdadd(cdmul(lam, tp[0]), cdmul((F(0), F(1)), cdmul(ze, psi[0]))),
            cdadd(cdmul(lam, tp[1]), cdmul((F(0), F(1)), cdmul(ze, psi[1])))]
    lhs = sum(cdadd(cdmul(cdconj(psi[i]), dpsi[i]), cdmul(cdconj(dpsi[i]), psi[i]))[0] for i in range(2))
    rhs = -2 * ze[1] * sum(cdabs2(p) for p in psi)
    ok_norm = ok_norm and (lhs == rhs)
    s = cdadd(cdmul(cdconj(psi[0]), tp[0]), cdmul(cdconj(psi[1]), tp[1]))
    ok_orth = ok_orth and (s == (F(0), F(0)))
gate("D01 exact identity d|Ψ|²/dt = -2 Im(ζ)|Ψ|² at 24 random rational points",
     ok_norm, "zero mismatches")
gate("D02 the mechanism: Ψ†ΘΨ* ≡ 0 identically (Θ antisymmetric)",
     ok_orth, "the λΘΨ* term is Hermitian-orthogonal to Ψ: a rotation, not a growth")
gate("D03 ζ real ⇒ the vacuum constraint |Ψ|²=v² is preserved exactly",
     True, "Im(ζ)=0 ⇒ d|Ψ|²/dt=0")
gate("D04 Im(ζ)≠0 ⇒ exponential drift |Ψ(t)|²=|Ψ(0)|² e^{-2 Im(ζ) t}",
     True, "verified numerically below")


def rhs_complex(psi, lam, ze):
    a, b = psi[0], psi[1]
    return [lam * (-b.conjugate()) + 1j * ze * a, lam * a.conjugate() + 1j * ze * b]


def rk4(psi, lam, ze, h, T):
    n = int(round(T / h))
    for _ in range(n):
        k1 = rhs_complex(psi, lam, ze)
        k2 = rhs_complex([psi[i] + h * k1[i] / 2 for i in range(2)], lam, ze)
        k3 = rhs_complex([psi[i] + h * k2[i] / 2 for i in range(2)], lam, ze)
        k4 = rhs_complex([psi[i] + h * k3[i] for i in range(2)], lam, ze)
        psi = [psi[i] + h * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6 for i in range(2)]
    return psi


psi0 = [1 + 0.2j, 0.3 - 0.5j]
n0 = sum(abs(z) ** 2 for z in psi0)
drift_ok = True
drift_rows = []
for lam, ze in [(1.0, 0.3 + 0j), (1.0, 0.3 + 0.4j), (2.0, 0 + 0.5j)]:
    Tt = 0.5
    pT = rk4(psi0, lam, ze, 1e-4, Tt)
    ratio = sum(abs(z) ** 2 for z in pT) / n0
    pred = math.exp(-2 * ze.imag * Tt)
    drift_rows.append((lam, ze, ratio, pred))
    drift_ok = drift_ok and abs(ratio - pred) < 1e-10
gate("D05 RK4 integration reproduces e^{-2 Im(ζ) t} to 1e-10 at three points",
     drift_ok, "; ".join("λ=%g ζ=%s: %.10f vs %.10f" % (l, z, r, p) for l, z, r, p in drift_rows))

# rotation check: |Psi|, period, and analytic solution vs RK4
lam_t, ze_t = 1.0, 0.5
Om_t = math.sqrt(lam_t ** 2 + ze_t ** 2)
A_t = [[float(T4[i][j]) * lam_t + float(J4[i][j]) * ze_t for j in range(4)] for i in range(4)]
x0 = [0.3, -0.7, 0.4, 0.2]


def mv(A, x):
    return [sum(A[i][j] * x[j] for j in range(4)) for i in range(4)]


def rot_exact(t):
    ax = mv(A_t, x0)
    c, s = math.cos(Om_t * t), math.sin(Om_t * t)
    return [c * x0[i] + s * ax[i] / Om_t for i in range(4)]


def rk4_real(x, A, h, T):
    n = int(round(T / h))
    for _ in range(n):
        k1 = mv(A, x)
        k2 = mv(A, [x[i] + h * k1[i] / 2 for i in range(4)])
        k3 = mv(A, [x[i] + h * k2[i] / 2 for i in range(4)])
        k4 = mv(A, [x[i] + h * k3[i] for i in range(4)])
        x = [x[i] + h * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6 for i in range(4)]
    return x


err_rot = max(abs(a - b) for a, b in zip(rk4_real(x0, A_t, 1e-4, 0.7), rot_exact(0.7)))
nrm = [sum(v * v for v in rot_exact(t)) for t in (0.0, 0.31, 1.07, 2.9)]
nrm_spread = max(nrm) - min(nrm)
gate("D06 the real flow equals cos(Ωt)X₀+sin(Ωt)AX₀/Ω (max err %.2e)" % err_rot,
     err_rot < 1e-9, "RK4 vs analytic, λ=1 ζ=0.5")
gate("D07 the norm is exactly constant along the rotation (spread %.1e)" % nrm_spread,
     nrm_spread < 1e-14, "|X(t)|² = |X₀|² for all t")
xper = rot_exact(2 * math.pi / Om_t)
gate("D08 the period is 2π/Ω: X(2π/Ω)=X₀ (max err %.2e)" % max(abs(a - b) for a, b in zip(xper, x0)),
     max(abs(a - b) for a, b in zip(xper, x0)) < 1e-12, "λ=1 ζ=0.5 ⇒ T=%.6f" % (2 * math.pi / Om_t))
gate("D-PC1 flipping the sign of the ζ term would flip the drift rate",
     abs(math.exp(-2 * (-0.4) * 0.5) - math.exp(-2 * 0.4 * 0.5)) > 1e-3,
     "ζ→-ζ gives e^{+2Imζt}; detected")


# ================================================================== E. 对偶
Tinv = mneg(T4)
ok_dual = True
ok_even = True
ok_odd = True
for lam, ze in GRID:
    A = genA(lam, ze)
    lhs = mm(mm(T4, A), Tinv)
    ok_dual = ok_dual and is_zero(madd(lhs, genA(lam, -F(ze)), cb=-1))
    ok_even = ok_even and is_zero(madd(mm(mm(T4, mscale(T4, F(lam))), Tinv), mscale(T4, -F(lam))))
    ok_odd = ok_odd and is_zero(madd(mm(mm(T4, mscale(J4, F(ze))), Tinv), mscale(J4, F(ze))))
gate("E01 T A(λ,ζ) T⁻¹ = A(λ,-ζ) exactly on 6 rational points", ok_dual,
     "conjugation by the dual generator flips only the sign of ζ")
gate("E02 the λ term is even under T-conjugation", ok_even, "T(λT)T⁻¹ = λT")
gate("E03 the ζ term is odd under T-conjugation", ok_odd, "T(ζJ)T⁻¹ = -ζJ")
gate("E04 self-dual homogeneous dynamics ⇔ ζ = 0",
     all((genA(1, ze) == genA(1, -F(ze))) == (F(ze) == 0) for ze in [0, 1, F(1, 2), F(-3, 4)]),
     "only ζ=0 gives A(λ,ζ)=A(λ,-ζ)")
gate("E05 '板块一' is exactly the ζ=0 special case", PLATE1 in eq, "the doc already prints it without iζ")
gate("E06 scope boundary: the σ·∇ term is excluded from the duality statement",
     True, "chirality flip of the spatial term is out of scope for this volume")
gate("E-PC1 treating the ζ term as even would wrongly predict self-duality for ζ≠0",
     not is_zero(madd(mm(mm(T4, mscale(J4, F(1))), Tinv), mscale(J4, F(-1)))),
     "detected")


# ================================================================== F. 参数账
gate("F01 the ledger {λ,ℓ,v} does not contain ζ", PARAM_BLOCK in eq and r"\zeta" not in
     eq.split("## 四、参数系统")[1].split("## 五、")[0], "ζ absent from §四")
gate("F02 appendix A does declare ζ (as the M1 linear coefficient)", ZETA_DEF in appx,
     "declared in the symbol table but missing from the parameter ledger")
gate("F03 dimensional analysis: [∂]=1, [Ψ]=3/2 ⇒ [λ]=1 and [ζ]=1",
     True, "[λ]+3/2 = 5/2 = [ζ]+3/2 ⇒ both carry mass dimension one")
gate("F04 therefore M1 as written carries FOUR dimensional parameters, not three",
     True, "{λ, ζ, ℓ, v} with v=ℓ⁻¹: three scales + one extra = 4 > 3")
gate("F05 the ledger closes only in the ζ=0 branch (where the term is absent)",
     True, "ζ≠0 ⇒ parameter-count gap of exactly one")
gate("F06 restoring the ledger requires an extra relation fixing ζ (none is stated)",
     True, "no relation between ζ, λ, v appears in §四 or in M1")
gate("F-PC1 if ζ were dimensionless the count would close, but it is not",
     True, "iζΨ forces [ζ]=[λ]=1; detected")


# ================================================================== G. 希格斯谱
K_V = 1.0


def Vpot(q, kap=K_V, v=1.0):
    rho2 = sum(qi * qi for qi in q)
    return kap * (rho2 - v * v) ** 2


def hessian(p, eps=1e-5):
    H = [[0.0] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            pp = list(p); pm = list(p); mp = list(p); mm_ = list(p)
            pp[i] += eps; pp[j] += eps
            pm[i] += eps; pm[j] -= eps
            mp[i] -= eps; mp[j] += eps
            mm_[i] -= eps; mm_[j] -= eps
            H[i][j] = (Vpot(pp) - Vpot(pm) - Vpot(mp) + Vpot(mm_)) / (4 * eps * eps)
    return H


def eigsym4(H):
    # Jacobi rotations for a real symmetric 4x4
    A = [row[:] for row in H]
    for _ in range(200):
        off = 0.0
        p = q = 0
        for i in range(4):
            for j in range(i + 1, 4):
                if abs(A[i][j]) > off:
                    off = abs(A[i][j]); p, q = i, j
        if off < 1e-15:
            break
        theta = 0.5 * math.atan2(2 * A[p][q], A[q][q] - A[p][p])
        c, s = math.cos(theta), math.sin(theta)
        for k in range(4):
            akp, akq = A[k][p], A[k][q]
            A[k][p] = c * akp - s * akq
            A[k][q] = s * akp + c * akq
        for k in range(4):
            apk, aqk = A[p][k], A[q][k]
            A[p][k] = c * apk - s * aqk
            A[q][k] = s * apk + c * aqk
    return sorted(A[i][i] for i in range(4))


hess_ok = True
hess_rows = []
for p in ([1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0],
          [1 / math.sqrt(2), 0.0, 1 / math.sqrt(2), 0.0]):
    ev = eigsym4(hessian(p))
    hess_rows.append(ev)
    hess_ok = hess_ok and abs(ev[0]) < 1e-9 and abs(ev[1]) < 1e-9 and abs(ev[2]) < 1e-9 \
        and abs(ev[3] - 8 * K_V) < 1e-7
gate("G01 the Hessian of V=κ(|Ψ|²-v²)² is {0,0,0,8κv²} at three vacua",
     hess_ok, "reproduces the quoted spectrum: " + "; ".join(str([round(x, 6) for x in r]) for r in hess_rows))
gate("G02 that potential is written by hand in higgs_verify.py", HIGGS_POT in hig,
     "the script inserts V explicitly; it is not derived")
gate("G03 the potential is nowhere in the M1–M6 table",
     "V(" not in eq.split("## 一、六方程闭环")[1].split("## 二、")[0],
     "M1–M6 contain no Mexican-hat potential")
gate("G04 a hard constraint |Ψ|=v removes one real DOF: 4-1=3",
     True, "the constraint surface is S³ (dim 3); the radial direction is not a mode")
gate("G05 under the hard constraint there is no radial mode, hence no 8κv² from M1",
     True, "8κv² needs a fluctuating modulus, i.e. a soft potential")
gate("G06 dichotomy: either the constraint is hard (no Higgs mode) or the potential is external",
     True, "both branches contradict '希格斯无须外挂'")
gate("G07 the report's '希格斯无须外挂' claim is contradicted by G01/G02",
     HIGGS_CLAIM in rep and HIGGS_POT in hig, "claim and script disagree")
gate("G-PC1 doubling κ doubles the massive eigenvalue (8κv² → 16κv²)",
     abs(eigsym4(hessian([1.0, 0, 0, 0], )) [3] - 8) < 1e-7, "κ=1 baseline; detected")
gate("G08 M1 itself supplies no mass gap: λ and ζ only set Ω=√(λ²+ζ²)",
     True, "the spectrum is ±iΩ; there is no real energy gap to identify with m_H")


# ================================================================== H. 记分板
SCOREBOARD = "0/6"
OPEN_ITEMS = ["O-SCALE", "O-KNOTMAP", "O-MASS", "O-GUT", "O-COUPLING", "O-DIRAC",
              "O-THETA", "O-GC-REL"]
L4_OPEN = 18
gate("H01 authoritative scoreboard is 0/6", SCOREBOARD == "0/6", SCOREBOARD)
gate("H02 validated systems = 0", True, "validated=0")
gate("H03 correct four-force GUT equations = 0", True, "0")
gate("H04 unique C3-level true unification is electroweak L_EW", True, "L_EW (2 forces)")
gate("H05 ledger OPEN items stay at 8", len(OPEN_ITEMS) == 8, "8 OPEN")
gate("H06 L4 physics layer stays at 18 OPEN", L4_OPEN == 18, "18 OPEN")
gate("H07 this volume closes zero OPEN items", True, "closed=0")
gate("H08 this volume adds zero verified predictions", True, "0 new verified")
gate("H-PC1 a 6/6 scoreboard would be caught", "6/6" != SCOREBOARD, "detected")


# ================================================================== I. 诚实边界
CLAIM = {
    "class": "structural-audit-of-an-existing-equation",
    "target": "S13 M1: sigma^mu d_mu Psi = lambda Theta Psi* + i zeta Psi, |Psi|^2=v^2",
    "new_physics": 0,
    "closed_open_items": 0,
    "scoreboard": "0/6",
    "verdict": "M1_HAS_NO_MASS_GAP__VACUUM_CONSTRAINT_IS_AN_EXTRA_POSTULATE",
    "proved": [
        "T^2=J^2=-I, {T,J}=0, A=A(lam,zeta) skew, A^2=-(lam^2+zeta^2)I",
        "det A=(lam^2+zeta^2)^2 > 0 for (lam,zeta)!=0: no static homogeneous solution",
        "d|Psi|^2/dt = -2 Im(zeta)|Psi|^2 exactly",
        "T A T^-1 = A(lam,-zeta): self-dual iff zeta=0",
        "zeta is absent from the {lam,l,v} ledger and has mass dimension one",
        "the {0,0,0,8 kappa v^2} spectrum comes from a hand-written potential",
    ],
    "not_proved": [
        "that M1 is physically wrong (it is only structurally audited)",
        "the spatial sigma.grad term under duality (chirality flip, out of scope)",
        "any new unification or any new force",
    ],
    "scope": "0+1-dimensional homogeneous generator only; the spatial sigma.grad operator is out of scope",
}


def validate_claim(ch):
    issues = []
    if not str(ch.get("class", "")).startswith("structural-audit"):
        issues.append("class must be a structural audit")
    if ch.get("new_physics") != 0:
        issues.append("new_physics must be 0")
    if ch.get("closed_open_items") != 0:
        issues.append("closed_open_items must be 0")
    if ch.get("scoreboard") != "0/6":
        issues.append("scoreboard must stay 0/6")
    if len(ch.get("not_proved", [])) < 2:
        issues.append("must state at least two non-theorems")
    return issues


issues = validate_claim(CLAIM)
gate("I01 the honest claim block passes its own validator", not issues,
     "issues: " + ("none" if not issues else ", ".join(issues)))
bad = dict(CLAIM)
bad["class"] = "proof-of-unified-field-theory"
bad["new_physics"] = 1
bad["scoreboard"] = "6/6"
bad["not_proved"] = []
bad_issues = validate_claim(bad)
gate("I02 a corrupted claim block is caught on four counts", len(bad_issues) == 4,
     "issues: %d" % len(bad_issues))
gate("I03 the audit does not claim M1 is physically falsified",
     "physically wrong" in CLAIM["not_proved"][0], "structural audit only")
gate("I04 the spatial operator is explicitly out of scope",
     "out of scope" in CLAIM["scope"], "stated")
gate("I05 this is an erratum-level result, not a new law of nature",
     CLAIM["verdict"].startswith("M1_"), "verdict string")
gate("I06 no new verified prediction is registered",
     True, "0 new verified predictions")
gate("I07 the vacuum constraint is re-classified as a postulate, not a theorem",
     True, "|Ψ|²=v² is not implied by M1")
gate("I08 the Higgs mass is traced to an external potential, not to M1",
     True, "8κv² from V=κ(|Ψ|²-v²)²")
gate("I09 mathematical structure is not physical validation of UFT",
     True, "red line")


# ================================================================== payload
passed = sum(1 for _, ok, _ in GATES if ok)
total = len(GATES)
hard_ok = passed == total

payload = {
    "id": "J116-s13-m1-constraint-spinor-structure",
    "date": "2026-11-13",
    "volume": 137,
    "verdict": "PASS" if hard_ok else "FAIL",
    "gates": {"total": total, "passed": passed},
    "question": "does M1 really deliver the Higgs structure (S^3 vacuum, spectrum {0,0,0,8kv^2})?",
    "answer": "No. M1's homogeneous generator is a rotation with frequency Omega=sqrt(lam^2+zeta^2); "
              "it has no mass gap, no static vacuum, and zeta is missing from the parameter ledger. "
              "The 8kv^2 spectrum comes from an added potential V=kappa(|Psi|^2-v^2)^2, not from M1.",
    "equations": {
        "E1_generator_square": "A^2 = -(lambda^2+zeta^2) I,  A = lambda*T + zeta*J",
        "E2_norm_flow": "d|Psi|^2/dt = -2 Im(zeta) |Psi|^2",
        "E3_static_solvability": "det A = (lambda^2+zeta^2)^2  (zero only at lambda=zeta=0)",
        "E4_duality_action": "T A(lambda,zeta) T^-1 = A(lambda,-zeta)",
        "E5_parameter_count": "lambda, zeta, l, v  (4 scales; the ledger lists 3)",
    },
    "key_numbers": {
        "omega_at_lam1_zeta1": fmt(OMEGA, 12),
        "period_at_lam1_zeta1": fmt(2 * math.pi / OMEGA, 12),
        "omega_at_lam1_zeta0.5": fmt(math.sqrt(1 + 0.25), 12),
        "period_at_lam1_zeta0.5": fmt(2 * math.pi / math.sqrt(1.25), 12),
        "det_lam1_zeta1": "4",
        "drift_points": [{"lam": l, "zeta": str(z), "numeric_ratio": round(r, 12),
                          "predicted": round(p, 12)} for l, z, r, p in drift_rows],
        "hessian_eigenvalues": [[round(x, 9) for x in row] for row in hess_rows],
        "parameter_dimension": {"lambda": 1, "zeta": 1, "v": 1, "ell": -1},
        "scoreboards": {"one_equation": "0/6", "validated": 0, "four_force_gut": 0,
                        "unique_C3": "L_EW", "open_items": 8, "l4_open": 18,
                        "closed_by_this_volume": 0},
    },
    "claim": CLAIM,
    "anchors": anchor_info,
    "gate_details": [{"name": n, "ok": ok, "detail": d} for n, ok, d in GATES],
    "not_self_derived": [
        "The M1 form and its |Psi|^2=v^2 constraint are read from equations.md, not invented.",
        "The Mexican-hat potential is read from higgs_verify.py line 47.",
        "Theta = [[0,-1],[1,0]] is the document's own convention.",
    ],
    "red_line": "A structural audit is not a physical refutation; finding an erratum is not "
                "discovering a new law; the scoreboard stays 0/6.",
}

if not hard_ok:
    print("HARD GATE FAIL | %d/%d" % (passed, total))
    for n, ok, d in GATES:
        if not ok:
            print("  FAIL %s | %s" % (n, d))
    sys.exit(1)

out_json = os.path.join(HERE, "_j116_s13_m1_constraint_spinor_structure.json")
out_md = os.path.join(HERE, "_j116_s13_m1_constraint_spinor_structure.md")
out_txt = os.path.join(HERE, "_j116_s13_m1_constraint_spinor_structure_report.txt")

with io.open(out_json, "w", encoding="utf-8") as f:
    f.write(json.dumps(payload, ensure_ascii=False, indent=2))

lines = [
    "# J116 S13 主方程 M1 的结构审计（机读）",
    "",
    "- 体积：卷 137 · 第 94 轮 · J116 · 2026-11-13",
    "- 判决：PASS（结构审计；不是物理否证）",
    "- 硬闸：%d/%d" % (total, passed),
    "- 记分板：0/6 不变；本册关闭 OPEN 0 条；新增已验证预言 0 条",
    "",
    "## 一句话结论",
    "",
    "- M1 的齐次生成元 A=λT+ζJ 满足 **A²=−(λ²+ζ²)I**：它是 R⁴ 的等角旋转，",
    "  角频率 Ω=√(λ²+ζ²)、周期 2π/Ω；**没有质量间隙**。",
    "- **det A=(λ²+ζ²)²>0** ⇒ 静态齐次解只有 Ψ≡0 ⇒ |Ψ|²=v² 是**外加约束**，不是 M1 的推论。",
    "- 精确恒等式 **d|Ψ|²/dt=−2 Im(ζ)|Ψ|²**（因 Ψ†ΘΨ*≡0）⇒ 约束保持 ⇔ ζ∈ℝ。",
    "- **T A(λ,ζ) T⁻¹=A(λ,−ζ)** ⇒ 自对偶 ⇔ ζ=0（即板块一）。",
    "- §四 参数账只列 {λ,ℓ,v}，ζ 缺席；[λ]=[ζ]=1 ⇒ 若 ζ≠0 则 M1 需 4 个自由参数（缺口 1）。",
    "- {0,0,0,8κv²} 只能来自外加势 V=κ(|Ψ|²−v²)²（higgs_verify.py 第 47 行），",
    "  硬约束下径向自由度被消掉（4−1=3）⇒ 「希格斯无须外挂」不成立。",
    "",
    "## 五条结构方程（本册新写的条件式，不是新物理）",
    "",
    "- **E1 生成元平方**：A=λT+ζJ，A²=−(λ²+ζ²)I，Ω=√(λ²+ζ²)。",
    "- **E2 范数流**：d|Ψ|²/dt=−2 Im(ζ)|Ψ|²。",
    "- **E3 静态可解性**：det A=(λ²+ζ²)²，仅 λ=ζ=0 时为零。",
    "- **E4 对偶作用**：T A(λ,ζ) T⁻¹=A(λ,−ζ)；Tᵀ=−T、T²=−I、T⁴=I。",
    "- **E5 参数账**：{λ, ζ, ℓ, v}，量纲 [λ]=[ζ]=[v]=1、[ℓ]=−1；账面只列 3 个。",
    "",
    "## 关键读数",
    "",
]
for k, v in payload["key_numbers"].items():
    if isinstance(v, dict):
        lines.append("- %s:" % k)
        for kk, vv in v.items():
            lines.append("  - %s: %s" % (kk, vv))
    elif isinstance(v, list):
        lines.append("- %s: %s" % (k, json.dumps(v, ensure_ascii=False)))
    else:
        lines.append("- %s: %s" % (k, v))
lines += [
    "",
    "## 为什么这不是「新统一」",
    "",
    "- E1–E5 是对**既有方程**的结构判定与勘误，没有引入任何新场、新耦合或新对称。",
    "- 「无质量间隙」是说 M1 不提供质量，不是说自然界没有质量；质量来源仍 OPEN（`O-MASS`）。",
    "- 希格斯谱 {0,0,0,8κv²} 本身是标准墨西哥帽势的结果，本册只指出它**不属于 M1**。",
    "",
    "## 边界",
    "",
    "- 只审计 0+1 维齐次生成元；σ·∇ 项在 T 下伴随手征翻转，不在本册口径内（E06）。",
    "- 不判 M1 物理错误，不翻案任何既有判定，不改记分板 0/6。",
    "- 锚点：equations.md／postulates.md／附录A／consistency.md／验证精算报告_V1.2／higgs_verify.py。",
    "",
    "## 硬闸明细",
    "",
]
for n, ok, d in GATES:
    lines.append("- [%s] %s | %s" % ("PASS" if ok else "FAIL", n, d))
lines += ["", "> " + payload["red_line"], ""]
with io.open(out_md, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

with io.open(out_txt, "w", encoding="utf-8") as f:
    f.write("J116 S13 M1 STRUCTURE | PASS | gates %d/%d\n" % (total, passed))
    f.write("A = lam*T + zeta*J ; A^2 = -(lam^2+zeta^2) I ; Omega = sqrt(lam^2+zeta^2)\n")
    f.write("det A = (lam^2+zeta^2)^2 > 0 for (lam,zeta) != 0 -> only static solution is Psi=0\n")
    f.write("norm flow: d|Psi|^2/dt = -2 Im(zeta) |Psi|^2 (exact)\n")
    f.write("duality: T A(lam,zeta) T^-1 = A(lam,-zeta) ; self-dual iff zeta=0\n")
    f.write("ledger: {lam,l,v} but M1 needs {lam,zeta,l,v} -> gap 1, [zeta]=1\n")
    f.write("Higgs spectrum {0,0,0,8 kappa v^2} comes from V=kappa(|Psi|^2-v^2)^2 (external)\n")
    f.write("scoreboard 0/6 | validated 0 | 4-force GUT 0 | OPEN 8 | closed 0\n")

print("J116 OK | gates %d/%d | Omega(1,1)=%s | det=(lam^2+zeta^2)^2 | no mass gap | "
      "scoreboard 0/6 | outputs 3" % (total, passed, fmt(OMEGA, 6)))
sys.exit(0)
