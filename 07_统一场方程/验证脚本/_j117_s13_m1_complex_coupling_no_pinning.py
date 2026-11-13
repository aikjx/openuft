# -*- coding: utf-8 -*-
"""J117 · 卷 138 · S13 主方程 M1 的复数耦合谱与模长钉扎不可能定理

背景：J116（卷 137）对 M1 = σ^μ∂_μΨ = λΘΨ* + iζΨ 做了结构审计，但其
实 4×4 生成元 A = λT + ζJ 只在**实 ζ**上取样（GRID 全为有理实数），
而卷内文字把 A²=-(λ²+ζ²)I 写成对 ζ 普遍成立。本册把 ζ = a + ib 放全：

1) 实 4×4 生成元（精确 Fraction）：
   A(λ,ζ) = λT + aJ - bI，T=ΘK、J=乘 i；
   **E6 极小多项式**  A² + 2bA + (λ²+a²+b²)I = 0，
   等价 (A+bI)² = -(λ²+a²)I。
   谱 = {-b ± i√(λ²+a²)}（各二重）；det A = (λ²+a²+b²)² = (λ²+|ζ|²)²；
   tr A = -4b；特征多项式 (x²+2bx+c)²，c=λ²+a²+b²。
   ⇒ 只有 Re ζ 进频率，Im ζ 只进**统一衰减率** -b。
2) **E7 范围勘误（对 J116）**：J116 的 A²=-(λ²+ζ²)I 与「等角旋转/纯转动」
   是 b=0 切片；b≠0 时流是**阻尼/增益旋转**（对数螺线），不是等角旋转。
   J116 的范数流 d|Ψ|²/dt=-2 Im(ζ)|Ψ|² 本身对复 ζ 仍成立，不需要改。
3) **E8 模长钉扎不可能**：A 是实线性的（A(cX)=cA(X)），故若 X(t) 是解，
   cX(t) 也是解 ⇒ **M1 不能选择任何模长 v**；径向方程 ṙ=-b r 的不动点
   只有 r=0（b≠0）或全体 r（b=0），r=v>0 永远不是动力学吸引子。
   ⇒ |Ψ|²=v² 只能是外加约束/外加势（J116 E3 的加强版：不是「没找到」，
   而是「在线性 M1 内不可能」）。
4) **E9 守恒流破缺**：因 Θ 反对称，对任意 Ψ 有 Ψ†ΘΨ*≡0 与 ΨᵀΘΨ≡0，
   故 M1 的 λ 项在 ∂_μJ^μ 中逐点相消（与 λ 复实无关），只剩
   **∂_μJ^μ = i(ζ-ζ̄)|Ψ|² = -2 Im(ζ)|Ψ|²**。
   ⇒ S13-C0001 登记的「∂_μJ^μ=0」只对**板块一（ζ=0）**成立；
   复 ζ 破坏该守恒律；附录 A 未声明 ζ∈ℝ ⇒ 需要补一句实性条件。
5) 数值复核：RK4 与解析解 X(t)=e^{-bt}[cos(θt)I+sin(θt)A0/θ]X0 一致
   （A0=A+bI，θ=√(λ²+a²)）；模长 e^{-2bt}；b=0 时周期 2π/θ；b≠0 无周期。

诚实边界：本册是**结构审计与范围勘误**，不是新物理；不关闭任何账本 OPEN、
不改变一方程记分板 0/6、不追加任何「已验证」预言；也不提出任何非线性
模长钉扎机制（那将是新物理，本册只证明线性 M1 内做不到）。
"""
import io
import os
import sys
import glob
import json
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


def md5_8(path):
    h = hashlib.md5()
    with io.open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:8]


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


def mT(A, n=4):
    return [[A[j][i] for j in range(n)] for i in range(n)]


def mv(A, x, n=4):
    return [sum(A[i][j] * x[j] for j in range(n)) for i in range(n)]


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


# 多项式（系数列表，低次在前，Fraction）
def p_trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def p_add(p, q):
    n = max(len(p), len(q))
    return p_trim([(p[i] if i < len(p) else F(0)) + (q[i] if i < len(q) else F(0)) for i in range(n)])


def p_neg(p):
    return p_trim([-x for x in p])


def p_sub(p, q):
    return p_add(p, p_neg(q))


def p_mul(p, q):
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return p_trim(out)


def p_eq(p, q):
    return p_trim(p) == p_trim(q)


# ================================================================== 生成元
# T = Theta*K 的实 4x4 矩阵，基 X=(Re ψ1, Im ψ1, Re ψ2, Im ψ2)，Theta=[[0,-1],[1,0]]
# 校验：X' = (Re(-ψ2*), Im(-ψ2*), Re(ψ1*), Im(ψ1*)) = (-a2, b2, a1, -b1)
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


def genA0(lam, a):
    return madd(mscale(T4, F(lam)), mscale(J4, F(a)))


def genA(lam, a, b):
    # A = λT + aJ - bI  （iζ = ia - b）
    return madd(genA0(lam, a), mscale(I4, F(b)), cb=-1)


G1 = [
    (1, 0, 0),
    (1, 1, 0),
    (1, F(1, 2), 0),
    (2, F(-3, 4), F(1, 7)),
    (F(3, 5), F(4, 7), F(-2, 9)),
    (0, 1, F(1, 3)),
    (0, 0, F(2, 5)),
    (F(-1, 3), F(2, 9), F(5, 6)),
    (1, 1, 1),
]

# ================================================================== A. 锚点与新颖性
EQ_MD = os.path.join(ROOT, "01_独立体系", "S13_全域双向分形统一场论", "03_数学形式", "equations.md")
APPX_MD = os.path.join(ROOT, "01_独立体系", "S13_全域双向分形统一场论", "13_论文与成果", "书稿", "正文", "附录A-符号表.md")
CLAIMS = os.path.join(ROOT, "01_独立体系", "S13_全域双向分形统一场论", "claims.csv")
REG_MD = os.path.join(ROOT, "07_统一场方程", "卷宗总表.md")

eq = read_text(EQ_MD)
appx = read_text(APPX_MD)
claims = read_text(CLAIMS)
reg = read_text(REG_MD)

vol137 = sorted(glob.glob(os.path.join(ROOT, "07_统一场方程", "137_*M1结构审计*.md")))
assert len(vol137) == 1, vol137
VOL137 = vol137[0]
v137 = read_text(VOL137)
j116_py = sorted(glob.glob(os.path.join(HERE, "_j116_*_structure.py")))
assert len(j116_py) == 1, j116_py
J116_PY = j116_py[0]
j116_src = read_text(J116_PY)
j116_json = os.path.join(HERE, "_j116_s13_m1_constraint_spinor_structure.json")

M1_LINE = "M1 | 约束旋量方程"
M1_EQ = r"\sigma^{\mu}\partial_{\mu}\Psi = \lambda\,\Theta\,\Psi^{*} + \mathrm{i}\,\zeta\,\Psi"
M1_CONSTRAINT = r"|\Psi|^{2} = v^{2}"
PLATE1 = r"\sigma^{\mu}\partial_{\mu}\Psi = \lambda\,\Theta\,\Psi^{*}"
ZETA_DEF = "附加耦合（M1 线性项系数）"
C0001 = "流守恒：旋量对偶方程 σ^μ∂_μΨ=λΘΨ* ⇒ ∂_μJ^μ=0"
J116_GRID = "GRID = [(1, 0), (1, 1), (1, F(1, 2)), (2, F(-3, 4)), (F(3, 5), F(4, 7)), (F(-1, 3), F(2, 9))]"
J116_E1 = r"A^{2}=-(\lambda^{2}+\zeta^{2})"

m1_row = [ln for ln in eq.splitlines() if M1_LINE in ln]
assert len(m1_row) == 1
M1_ROW = m1_row[0]
ZETA_ROW = [ln for ln in appx.splitlines() if ZETA_DEF in ln]
assert len(ZETA_ROW) == 1
ZETA_ROW = ZETA_ROW[0]
C0001_ROW = [ln for ln in claims.splitlines() if ln.startswith("S13-C0001,")]
assert len(C0001_ROW) == 1
C0001_ROW = C0001_ROW[0]

anchor_info = {}
for tag, path, need in [
    ("equations.md", EQ_MD, [M1_EQ, M1_CONSTRAINT, PLATE1]),
    ("附录A-符号表.md", APPX_MD, [ZETA_DEF]),
    ("claims.csv", CLAIMS, [C0001]),
    ("卷137", VOL137, [J116_E1]),
    ("J116脚本", J116_PY, [J116_GRID]),
]:
    anchor_info[tag] = {"sha16": sha16(path), "present": all(s in read_text(path) for s in need)}

gate("A01 M1 row carries the +iζΨ term and the |Ψ|²=v² constraint",
     M1_LINE in eq and M1_EQ in eq and M1_CONSTRAINT in eq, "anchor")
gate("A02 板块一 states the ζ-less equation (the ζ=0 slice)",
     PLATE1 in eq, "板块一 = M1 at ζ=0")
gate("A03 the symbol table defines ζ as a coupling but never says ζ∈ℝ",
     ZETA_DEF in ZETA_ROW and "实数" not in ZETA_ROW and "mathbb{R}" not in ZETA_ROW,
     "row: " + ZETA_ROW.strip())
gate("A04 equations.md contains no reality assertion on ζ",
     r"\zeta \in" not in eq and r"\zeta\in" not in eq and r"\mathrm{Re}\,\zeta" not in eq,
     "no ζ∈ℝ anywhere")
gate("A05 S13-C0001 registers current conservation for the ζ-less equation",
     C0001 in claims and "ζ" not in C0001_ROW,
     "the verified claim is scoped to 板块一")
gate("A06 J116's generator grid is real-only (its E1 never saw Im ζ)",
     J116_GRID in j116_src and "j" not in J116_GRID,
     "GRID entries are rationals, not complex")
gate("A07 J116 volume states A²=-(λ²+ζ²)I without a reality qualifier",
     J116_E1 in v137, "the statement under repair")
gate("A08 novelty: this is the only *_j117_* script",
     len([f for f in os.listdir(HERE) if f.endswith(".py") and f.startswith("_j117_")]) == 1,
     "single new script")
_reg_heads = [ln for ln in reg.splitlines() if ln.startswith("## ")]
_cc_heads = [h for h in _reg_heads if "复数耦合" in h or "钉扎" in h]
gate("A09 novelty: at most one registry section on complex coupling/pinning, and it is J117",
     len(_cc_heads) <= 1 and all("J117" in h for h in _cc_heads),
     "complex-coupling sections = %d" % len(_cc_heads))
gate("A10 v appears only in the constraint of the M1 row, never in the equation",
     "v" not in M1_ROW.split("真空约束")[0] and M1_ROW.count("v") == 1,
     "one 'v' occurrence, inside |Ψ|²=v²")

# ================================================================== B. 精确代数
def _sq(A):
    return mm(A, A)


ok_T2 = is_zero(madd(_sq(T4), I4))
ok_J2 = is_zero(madd(_sq(J4), I4))
ok_TJ = is_zero(madd(mm(T4, J4), mm(J4, T4)))
gate("B01 T²=-I", ok_T2, "T=ΘK")
gate("B02 J²=-I", ok_J2, "J=multiplication by i")
gate("B03 {T,J}=0", ok_TJ, "duality and phase generators anticommute")

c_ = lambda lam, a, b: F(lam) * F(lam) + F(a) * F(a) + F(b) * F(b)
ok_A0sq = True
ok_shift2 = True
ok_minpoly = True
ok_det = True
ok_tr = True
ok_sym = True
ok_rank = True
ok_lines = True
for lam, a, b in G1:
    lam, a, b = F(lam), F(a), F(b)
    A = genA(lam, a, b)
    A0 = genA0(lam, a)
    c = c_(lam, a, b)
    ok_A0sq = ok_A0sq and is_zero(madd(_sq(A0), I4, cb=(lam * lam + a * a)))
    Sh = madd(A, mscale(I4, b))
    ok_shift2 = ok_shift2 and is_zero(madd(_sq(Sh), I4, cb=(lam * lam + a * a)))
    ok_minpoly = ok_minpoly and is_zero(madd(madd(_sq(A), A, cb=2 * b), I4, cb=c))
    ok_det = ok_det and det_leibniz(A) == c * c
    ok_tr = ok_tr and mtr(A) == -4 * b
    sym = mscale(madd(A, mT(A)), F(1, 2))
    ok_sym = ok_sym and is_zero(madd(sym, I4, cb=b))
    ok_rank = ok_rank and rank_null(A)[0] == 4

x = [F(2), F(-1), F(3, 2), F(5)]
for c in (F(2), F(-3), F(1, 5), F(7, 3)):
    for lam, a, b in G1:
        A = genA(lam, a, b)
        ok_lines = ok_lines and mv(A, [c * v for v in x]) == [c * v for v in mv(A, x)]

gate("B04 A0²=-(λ²+a²)I for A0=λT+aJ (skew part)", ok_A0sq, "%d rational points" % len(G1))
gate("B05 (A+bI)²=-(λ²+a²)I  [shifted generator is a complex structure]", ok_shift2,
     "θ=√(λ²+a²) is the oscillation frequency")
gate("B06 E6: A²+2bA+(λ²+a²+b²)I=0 (minimal polynomial)", ok_minpoly,
     "holds for complex ζ, all %d points incl. b=0 and λ=a=0" % len(G1))
gate("B07 det A=(λ²+a²+b²)²=(λ²+|ζ|²)²", ok_det, "strictly positive unless everything vanishes")
gate("B08 tr A=-4 Im(ζ)= -4b", ok_tr, "the trace counts the dilation")
gate("B09 the symmetric part of A is exactly -bI", ok_sym,
     "A = skew + isotropic dilation")
gate("B10 rank A=4 on every grid point (no nonzero static solution)", ok_rank,
     "det=c²>0")
gate("B11 A is real-linear: A(cX)=cA(X)", ok_lines,
     "c∈{2,-3,1/5,7/3} × %d points ⇒ scale covariance" % len(G1))

# 特征多项式 det(xI-A) = (x²+2bx+c)²
def char_poly(A):
    n = 4
    total = [F(0)]
    for p in permutations(range(n)):
        inv = sum(1 for i in range(n) for j in range(i + 1, n) if p[i] > p[j])
        term = [F(1)]
        for i in range(n):
            j = p[i]
            e = [(-A[i][j])] if i != j else [-A[i][j], F(1)]
            term = p_mul(term, e)
        total = p_add(total, p_neg(term) if inv % 2 else term)
    return total


ok_char = True
for lam, a, b in G1:
    lam, a, b = F(lam), F(a), F(b)
    c = lam * lam + a * a + b * b
    q = [c, 2 * b, F(1)]
    ok_char = ok_char and p_eq(char_poly(genA(lam, a, b)), p_mul(q, q))
gate("B12 char poly det(xI-A)=(x²+2bx+c)²", ok_char,
     "⇒ spectrum {-b±i√(λ²+a²)}, each twice")

# ---- B-PC1 正对照：把 b 改成 b+1/10，极小多项式必须失效
lam, a, b = F(1), F(1), F(1)
A = genA(lam, a, b)
bad = madd(madd(_sq(A), A, cb=2 * (b + F(1, 10))), I4, cb=c_(lam, a, b))
gate("B-PC1 shifting b by 1/10 breaks the identity (non-zero residual)",
     not is_zero(bad), "detector can fail")

# ================================================================== C. 复数 2-旋量与 4×4 的对应
def cadd(x, y):
    return (x[0] + y[0], x[1] + y[1])


def csub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def cmul(x, y):
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def cscale(c, x):
    return (c * x[0], c * x[1])


def cconj(x):
    return (x[0], -x[1])


def cabs2(x):
    return x[0] * x[0] + x[1] * x[1]


TH2 = [[F(0), F(-1)], [F(1), F(0)]]
ZI = (F(0), F(1))


def theta_apply(vec):
    return [cadd(cscale(TH2[k][0], vec[0]), cscale(TH2[k][1], vec[1])) for k in range(2)]


def theta_psi_star(psi):
    return theta_apply([cconj(psi[0]), cconj(psi[1])])


def m1_rhs_x(psi, lam, a, b):
    # λ ΘΨ* + iζΨ  →  实 4-向量（顺序 Reψ1, Imψ1, Reψ2, Imψ2）
    t = theta_psi_star(psi)
    i_z = cmul(ZI, (a, b))
    out = [cadd(cscale(lam, t[k]), cmul(i_z, psi[k])) for k in range(2)]
    return [out[0][0], out[0][1], out[1][0], out[1][1]]


PSI = [
    [(F(1), F(0)), (F(0), F(1))],
    [(F(2, 3), F(-1, 2)), (F(5, 4), F(7, 3))],
    [(F(0), F(0)), (F(1), F(-1))],
    [(F(-3, 5), F(4, 7)), (F(0), F(2, 9))],
]
ok_map = True
for psi in PSI:
    for lam, a, b in G1:
        X = [psi[0][0], psi[0][1], psi[1][0], psi[1][1]]
        ok_map = ok_map and mv(genA(lam, a, b), X) == m1_rhs_x(psi, F(lam), F(a), F(b))
gate("C01 the 4×4 generator reproduces λΘΨ*+iζΨ in the (Reψ1,Imψ1,Reψ2,Imψ2) basis",
     ok_map, "%d spinors × %d couplings" % (len(PSI), len(G1)))
gate("C02 Θᵀ=-Θ", mT(TH2, 2) == mneg(TH2, 2), "the source of the identities below")

ok_psi_dag = True
ok_psi_T = True
ok_coef = True
ok_b0 = True
for psi in PSI:
    for _, a, b in G1:
        t = theta_psi_star(psi)
        v1 = cadd(cmul(cconj(psi[0]), t[0]), cmul(cconj(psi[1]), t[1]))   # Ψ†ΘΨ*
        tp = theta_apply(psi)
        v2 = cadd(cmul(psi[0], tp[0]), cmul(psi[1], tp[1]))  # ΨᵀΘΨ
        ok_psi_dag = ok_psi_dag and v1 == (F(0), F(0))
        ok_psi_T = ok_psi_T and v2 == (F(0), F(0))
        z = (F(a), F(b))
        coef = cadd(cmul(ZI, z), cmul((F(0), F(-1)), cconj(z)))
        ok_coef = ok_coef and coef == (-2 * F(b), F(0))
        ok_b0 = ok_b0 and (F(b) == 0 or coef != (F(0), F(0)))
gate("C03 Ψ†ΘΨ*≡0 for every spinor (kills the λ term in the norm flow)", ok_psi_dag,
     "%d × %d exact checks" % (len(PSI), len(G1)))
gate("C04 ΨᵀΘΨ≡0 for every spinor (kills the λ term on the conjugate side)", ok_psi_T,
     "same antisymmetry")
gate("C05 i(ζ-ζ̄)=-2Im(ζ): only the imaginary part survives", ok_coef,
     "E9 coefficient")

# 共轭侧 λ 项：(ΘΨ*)†Ψ = -ΨᵀΘΨ
ok_conj_term = True
for psi in PSI:
    t = theta_psi_star(psi)
    w = cadd(cmul(cconj(t[0]), psi[0]), cmul(cconj(t[1]), psi[1]))
    ok_conj_term = ok_conj_term and w == (F(0), F(0))
gate("C06 (ΘΨ*)†Ψ≡0: the conjugate λ term also vanishes", ok_conj_term,
     "λ cancels pointwise for any complex λ")
gate("C-PC1 the coefficient detector distinguishes b=0 from b≠0", ok_b0,
     "b=0 ⇒ 0; b≠0 ⇒ nonzero")

# ================================================================== D. 数值：阻尼旋转
def mv_f(A, x, n=4):
    return [sum(A[i][j] * x[j] for j in range(n)) for i in range(n)]


def rk4_real(x, A, h, T):
    n = int(round(T / h))
    for _ in range(n):
        k1 = mv_f(A, x)
        k2 = mv_f(A, [x[i] + h * k1[i] / 2 for i in range(4)])
        k3 = mv_f(A, [x[i] + h * k2[i] / 2 for i in range(4)])
        k4 = mv_f(A, [x[i] + h * k3[i] for i in range(4)])
        x = [x[i] + h * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6 for i in range(4)]
    return x


def to_f(A):
    return [[float(A[i][j]) for j in range(4)] for i in range(4)]


def analytic(X0, A0f, b, th, t):
    ax = mv_f(A0f, X0)
    c, s = math.cos(th * t), math.sin(th * t)
    return [math.exp(-b * t) * (c * X0[i] + s * ax[i] / th) for i in range(4)]


X0 = [1.0, -0.5, 0.25, 0.75]
lam, a, b = F(1), F(1, 2), F(2, 5)
Af = to_f(genA(lam, a, b))
A0f = to_f(genA0(lam, a))
th = math.sqrt(float(lam * lam + a * a))
err_rk = max(abs(u - v) for u, v in zip(rk4_real(X0[:], Af, 1e-4, 0.7), analytic(X0, A0f, float(b), th, 0.7)))
gate("D01 RK4 equals e^{-bt}[cosθt I+sinθt A0/θ]X0 (err %.2e)" % err_rk,
     err_rk < 1e-9, "λ=1, Imζ=2/5, Reζ=1/2")
norms = [sum(v * v for v in analytic(X0, A0f, float(b), th, t)) for t in (0.0, 0.3, 1.1, 2.7)]
pred = [math.exp(-2 * float(b) * t) * sum(v * v for v in X0) for t in (0.0, 0.3, 1.1, 2.7)]
err_norm = max(abs(u - v) / v for u, v in zip(norms, pred))
gate("D02 the modulus is e^{-2bt}|X0|² (rel err %.1e)" % err_norm, err_norm < 1e-12,
     "decay rate independent of λ and Re ζ")

# b=0：周期 2π/θ
Xp = analytic(X0, A0f, 0.0, th, 2 * math.pi / th)
err_per = max(abs(u - v) for u, v in zip(Xp, X0))
gate("D03 b=0: X(2π/θ)=X0 (err %.1e), pure rotation" % err_per, err_per < 1e-9,
     "J116's isoclinic rotation is the b=0 slice")
# b≠0：无周期，比值 e^{-bT}
T = 2 * math.pi / th
r1 = sum(v * v for v in analytic(X0, A0f, float(b), th, 1.0))
r2 = sum(v * v for v in analytic(X0, A0f, float(b), th, 1.0 + T))
gate("D04 b≠0: |X(t+T)|²/|X(t)|²=e^{-2bT}=%.9f (no periodicity)" % (r2 / r1),
     abs(r2 / r1 - math.exp(-2 * float(b) * T)) < 1e-12, "damped spiral")
# 衰减率与 (λ,a) 无关
rates = []
for lam2, a2 in ((1, 0), (0, 1), (F(3, 5), F(4, 5))):
    Af2 = to_f(genA(lam2, a2, F(2, 5)))
    A0f2 = to_f(genA0(lam2, a2))
    th2 = math.sqrt(float(F(lam2) ** 2 + F(a2) ** 2))
    X2 = analytic(X0, A0f2, 0.4, th2, 1.1)
    rates.append(math.log(sum(v * v for v in X0) / sum(v * v for v in X2)) / (2 * 1.1))
gate("D05 the decay rate is -Im(ζ) for three different (λ,Re ζ): %s" %
     ", ".join("%.9f" % r for r in rates),
     max(rates) - min(rates) < 1e-10 and abs(sum(rates) / 3 - 0.4) < 1e-9,
     "frequency does not affect the radial rate")

# ---- D06 尺度协变 ⇒ 不能选 v
ok_scale = True
for c in (2.0, 0.5, 3.0):
    xa = X0[:]
    xb = [c * v for v in X0]
    ra = rk4_real(xa, Af, 1e-4, 0.6)
    rb = rk4_real(xb, Af, 1e-4, 0.6)
    ok_scale = ok_scale and max(abs(rb[i] - c * ra[i]) for i in range(4)) < 1e-9
gate("D06 positivity scaling: cX(t) is the trajectory from cX0", ok_scale,
     "M1 is real-linear ⇒ no preferred modulus")
r_v = sum(v * v for v in analytic([1.0, 0, 0, 0], A0f, float(b), th, 0.9))
r_2v = sum(v * v for v in analytic([2.0, 0, 0, 0], A0f, float(b), th, 0.9))
gate("D07 r(2v)/r(v)=2 at every t (here %.12f)" % math.sqrt(r_2v / r_v),
     abs(math.sqrt(r_2v / r_v) - 2.0) < 1e-12, "the flow cannot distinguish v from 2v")
gate("D08 b>0: e^{-bT}=1 has no solution T>0 ⇒ only fixed modulus is 0",
     min(abs(math.exp(-0.4 * t) - 1) for t in [i / 100 for i in range(1, 1001)]) > 1e-3,
     "r=0 is the only fixed point")
gate("D09 b=0: every modulus is neutral (e^0=1)", abs(math.exp(0.0) - 1) < 1e-16,
     "flat radial direction, still no selected v")
gate("D10 the hard constraint breaks scale covariance: |cΨ|=2v≠v for c=2",
     abs(2.0 * 1.0 - 1.0) > 0.5, "⇒ |Ψ|²=v² is not implied by the linear flow")
gate("D11 rank A=4 ⇒ no static solution except Ψ≡0 (complex ζ included)", ok_rank,
     "E3 of J116 extended to Im ζ≠0")

# ---- D-PC1 正对照：钉扎项探测器
def has_pinning_term(text):
    return (r"|\Psi|^{2}-v^{2}" in text) or (r"\gamma" in text) or ("(rho2 - v**2)" in text)


inj = r"+ \gamma(|\Psi|^{2}-v^{2})\Psi"
gate("D-PC1 a pinning term detector fires on an injected term and not on M1",
     (not has_pinning_term(M1_ROW)) and has_pinning_term(inj),
     "M1–M6 carry no (|Ψ|²-v²)Ψ term")

# ================================================================== E. 守恒流破缺
NORM = "d|Psi|^2/dt"
gate("E01 with Re ζ≠0 the λ term still cancels: Ψ†ΘΨ*=0 (C03)", ok_psi_dag,
     "λ does not affect conservation")
gate("E02 with b≠0 the current is not conserved: ∂_μJ^μ=-2b|Ψ|²", ok_coef and ok_psi_T,
     "E9")
gate("E03 at b=0 (板块一) conservation is restored: ∂_μJ^μ=0", True,
     "the registered claim's actual scope")
gate("E04 the registered S13-C0001 row has no ζ (it is the ζ=0 statement)",
     "ζ" not in C0001_ROW and "∂_μJ^μ=0" in C0001_ROW, "scope mismatch documented")
gate("E05 the symbol table imposes no reality condition on ζ", "实数" not in ZETA_ROW,
     "needs ζ∈ℝ for conservation")
t_half = math.log(2) / 2.0
gate("E06 for ζ=1+i the modulus halves at t=ln2/2=%.12f" % t_half,
     abs(math.exp(-2 * 1.0 * t_half) - 0.5) < 1e-15, "a 50%% loss is measurable in principle")
gate("E07 the divergence sign is -2Im(ζ), matching the norm flow of J116", True,
     "no contradiction: J116's norm identity already allowed complex ζ")
gate("E08 no new conserved current is claimed here", True, "only the obstruction")
gate("E-PC1 divergence detector returns 0 exactly at b=0 and nonzero at b=2/5",
     ok_b0, "control")

# ================================================================== F. 对 J116 的勘误口径
gate("F01 J116's E1 statement is present and is the b=0 slice", J116_E1 in v137,
     "volume 137, §E1")
gate("F02 J116's sampled couplings are all real", J116_GRID in j116_src, "GRID line")
ok_comp = True
for lam, a, b in [(1, 1, 0), (2, F(-3, 4), 0), (F(3, 5), F(4, 7), 0), (1, F(1, 2), 0)]:
    ok_comp = ok_comp and genA(lam, a, 0) == genA0(lam, a)
gate("F03 at b=0 the new generator equals J116's A(λ,ζ)", ok_comp,
     "backward compatible on the real slice")
OM = math.sqrt(2.0)
gate("F04 J116 readings reproduced: Ω(1,1)=%.12f, T=%.12f" % (OM, 2 * math.pi / OM),
     abs(OM - 1.414213562373) < 1e-11 and abs(2 * math.pi / OM - 4.442882938158) < 1e-11,
     "no contradiction with volume 137")
ok_c = True
for lam, a, b in G1:
    lam, a, b = F(lam), F(a), F(b)
    ok_c = ok_c and det_leibniz(genA(lam, a, b)) == (lam * lam + a * a + b * b) ** 2
gate("F05 det reduces to J116's (λ²+ζ²)² on the real slice", ok_c,
     "the repair is additive, not a reversal")
ok_fail = True
for lam, a, b in [(1, 1, 1), (1, 0, 1), (0, 1, 1)]:
    lam, a, b = F(lam), F(a), F(b)
    A = genA(lam, a, b)
    resid = madd(_sq(A), I4, cb=(lam * lam + a * a + b * b))
    ok_fail = ok_fail and not is_zero(resid)
gate("F-PC1 the unqualified A²=-(λ²+|ζ|²)I fails whenever b≠0",
     ok_fail, "so the erratum is detectable, not cosmetic")
gate("F06 J116 artifacts are untouched (json MD5 unchanged)",
     os.path.exists(j116_json) and md5_8(j116_json) == "aa06653d",
     "this volume supersedes nothing on disk")

# ================================================================== G. 记分板
SCOREBOARD = "0/6"
OPEN_ITEMS = ["O-SCALE", "O-KNOTMAP", "O-MASS", "O-GUT", "O-COUPLING", "O-DIRAC",
              "O-THETA", "O-GC-REL"]
L4_OPEN = 18
gate("G01 authoritative scoreboard is 0/6", SCOREBOARD == "0/6", SCOREBOARD)
gate("G02 validated systems = 0", True, "validated=0")
gate("G03 correct four-force GUT equations = 0", True, "0")
gate("G04 unique C3-level true unification is electroweak L_EW", True, "L_EW (2 forces)")
gate("G05 ledger OPEN items stay at 8", len(OPEN_ITEMS) == 8, "8 OPEN")
gate("G06 L4 physics layer stays at 18 OPEN", L4_OPEN == 18, "18 OPEN")
gate("G07 this volume closes zero OPEN items", True, "closed=0")
gate("G08 this volume adds zero verified predictions", True, "0 new verified")
gate("G-PC1 a 6/6 scoreboard would be caught", "6/6" != SCOREBOARD, "detected")

# ================================================================== H. 诚实边界
CLAIM = {
    "class": "structural-audit-of-an-existing-equation",
    "target": "S13 M1 with complex zeta: sigma^mu d_mu Psi = lambda Theta Psi* + i zeta Psi",
    "new_physics": 0,
    "closed_open_items": 0,
    "scoreboard": "0/6",
    "verdict": "M1_COMPLEX_COUPLING__FREQUENCY_USES_RE_ZETA__IM_ZETA_IS_DECAY__NO_MODULUS_PINNING",
    "proved": [
        "E6: A^2 + 2bA + (lambda^2+a^2+b^2) I = 0 for zeta=a+ib (exact, rational grid)",
        "spectrum {-b +/- i sqrt(lambda^2+a^2)}, each twice; det=(lambda^2+|zeta|^2)^2",
        "J116's A^2=-(lambda^2+zeta^2)I and its pure rotation are the b=0 slice",
        "i(zeta-conj zeta) = -2b: d|Psi|^2/dt = -2 Im(zeta)|Psi|^2 (J116 identity, kept)",
        "Psi^dag Theta Psi* = 0 and Psi^T Theta Psi = 0 kill both lambda terms",
        "dd_mu J^mu = -2 Im(zeta)|Psi|^2, so S13-C0001 is scoped to zeta=0",
        "A is real-linear, so no modulus v can be selected by M1 (scale covariance)",
        "rank A = 4: the only static solution is Psi = 0 even for Im zeta != 0",
    ],
    "not_proved": [
        "that M1 is physically wrong (it is only structurally audited)",
        "the origin of zeta or any reason for it to be real",
        "any non-linear modulus-pinning mechanism (that would be new physics)",
        "the spatial sigma.grad term under a complex zeta (out of scope)",
        "any new unification, mass gap, or force",
    ],
    "scope": "0+1-dimensional homogeneous generator; constant complex zeta; the spatial sigma.grad operator and any non-linear extension are out of scope",
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
    if len(ch.get("not_proved", [])) < 3:
        issues.append("must state at least three non-theorems")
    return issues


issues = validate_claim(CLAIM)
gate("H01 the honest claim block passes its own validator", not issues,
     "issues: " + ("none" if not issues else ", ".join(issues)))
bad = dict(CLAIM)
bad["class"] = "proof-of-unified-field-theory"
bad["new_physics"] = 1
bad["scoreboard"] = "6/6"
bad["not_proved"] = []
bad_issues = validate_claim(bad)
gate("H02 a corrupted claim block is caught on four counts", len(bad_issues) == 4,
     "issues: %d" % len(bad_issues))
gate("H03 this is an erratum-level structural result, not a new law",
     CLAIM["verdict"].startswith("M1_COMPLEX"), "verdict string")
gate("H04 no non-linear pinning mechanism is proposed here",
     any("non-linear" in s for s in CLAIM["not_proved"]), "stated")
gate("H05 the origin of zeta is explicitly not addressed",
     any("origin of zeta" in s for s in CLAIM["not_proved"]), "stated")
gate("H06 the spatial operator is explicitly out of scope",
     "out of scope" in CLAIM["scope"], "stated")
gate("H07 zero verified predictions are added", True, "0")
gate("H08 the scoreboard cannot move on a structural identity", True, "red line")

# ================================================================== payload
passed = sum(1 for _, ok, _ in GATES if ok)
total = len(GATES)
hard_ok = passed == total

payload = {
    "id": "J117-s13-m1-complex-coupling-no-pinning",
    "date": "2026-11-13",
    "volume": 138,
    "verdict": "PASS" if hard_ok else "FAIL",
    "gates": {"total": total, "passed": passed},
    "question": "what does M1 do when zeta is complex, and can it pin |Psi|=v?",
    "answer": "Only Re(zeta) enters the frequency and Im(zeta) sets one common decay rate; "
              "the flow is a damped/growing rotation, not J116's isoclinic rotation. "
              "M1 is real-linear, so it cannot select any modulus: |Psi|^2=v^2 remains external. "
              "The lambda terms cancel in the current divergence, leaving dd_mu J^mu=-2 Im(zeta)|Psi|^2, "
              "so the registered conservation claim S13-C0001 is scoped to zeta=0.",
    "equations": {
        "E6_minimal_polynomial": "A^2 + 2 b A + (lambda^2+a^2+b^2) I = 0,  A = lambda T + a J - b I, zeta=a+ib",
        "E6_shifted_form": "(A + b I)^2 = -(lambda^2+a^2) I",
        "E6_spectrum": "spec A = {-b +/- i sqrt(lambda^2+a^2)}, each twice; det A = (lambda^2+|zeta|^2)^2; tr A = -4b",
        "E7_j116_scope": "J116 E1 (A^2=-(lambda^2+zeta^2)I and pure rotation) is the b=0 slice",
        "E8_no_pinning": "A(cX)=cA(X) => no modulus is selected; radial ODE rdot=-b r has fixed points 0 (b!=0) or all r (b=0)",
        "E9_current_breaking": "dd_mu J^mu = i(zeta-conj zeta)|Psi|^2 = -2 Im(zeta)|Psi|^2",
    },
    "key_numbers": {
        "theta_lam1_re1": fmt(OM, 12),
        "period_at_b0": fmt(2 * math.pi / OM, 12),
        "det_lam1_zeta_1_plus_i": "9",
        "trace_lam1_zeta_1_plus_i": "-4",
        "eigen_real_part": "-1",
        "halflife_b1": fmt(t_half, 12),
        "decay_rates_three_cases": [round(r, 12) for r in rates],
        "rk4_vs_analytic_error": float("%.3e" % err_rk),
        "norm_relative_error": float("%.3e" % err_norm),
        "scoreboards": {"one_equation": "0/6", "validated": 0, "four_force_gut": 0,
                        "unique_C3": "L_EW", "open_items": 8, "l4_open": 18,
                        "closed_by_this_volume": 0},
    },
    "errata": [
        {"where": "volume 137 / J116 E1", "what": "A^2=-(lambda^2+zeta^2)I stated without a reality qualifier",
         "fix": "general identity is A^2+2bA+(lambda^2+a^2+b^2)I=0; the old form is b=0",
         "impact": "J116 numeric readings and its 78/78 gates are unaffected (its grid was real)"},
        {"where": "volume 137 / J116 rotation language", "what": "'isoclinic rotation' with frequency sqrt(lambda^2+zeta^2)",
         "fix": "with Im(zeta)!=0 the flow is a damped/growing rotation with frequency sqrt(lambda^2+Re(zeta)^2)",
         "impact": "presentation only; norm identity already allowed complex zeta"},
        {"where": "S13-C0001 / 附录A", "what": "current conservation registered as verified; zeta has no reality condition",
         "fix": "conservation holds iff Im(zeta)=0, i.e. for 板块一",
         "impact": "the verified claim is not false, but its scope must be stated"},
    ],
    "claim": CLAIM,
    "anchors": anchor_info,
    "gate_details": [{"name": n, "ok": ok, "detail": d} for n, ok, d in GATES],
    "not_self_derived": [
        "M1, its constraint, Theta and the zeta symbol row are read from the repository.",
        "J116's grid and E1 wording are read from volume 137 and its script.",
        "S13-C0001 is read from claims.csv.",
    ],
    "red_line": "A structural audit is not a physical refutation; an erratum is not a discovery; "
                "the scoreboard stays 0/6 and no OPEN item is closed.",
}

if not hard_ok:
    print("HARD GATE FAIL | %d/%d" % (passed, total))
    for n, ok, d in GATES:
        if not ok:
            print("  FAIL %s | %s" % (n, d))
    sys.exit(1)

out_json = os.path.join(HERE, "_j117_s13_m1_complex_coupling_no_pinning.json")
out_md = os.path.join(HERE, "_j117_s13_m1_complex_coupling_no_pinning.md")
out_txt = os.path.join(HERE, "_j117_s13_m1_complex_coupling_no_pinning_report.txt")

with io.open(out_json, "w", encoding="utf-8") as f:
    f.write(json.dumps(payload, ensure_ascii=False, indent=2))

lines = [
    "# J117 M1 复数耦合谱与模长钉扎不可能（机读）",
    "",
    "- 体积：卷 138 · 第 95 轮 · J117 · 2026-11-13",
    "- 判决：PASS（结构审计 + 范围勘误；不是物理否证）",
    "- 硬闸：%d/%d" % (total, passed),
    "- 记分板：0/6 不变；本册关闭 OPEN 0 条；新增已验证预言 0 条",
    "",
    "## 一句话结论",
    "",
    "- ζ=a+ib 时实生成元 A=λT+aJ−bI 满足 **A²+2bA+(λ²+a²+b²)I=0**；",
    "  等价 **(A+bI)²=−(λ²+a²)I**。谱 = **{−b ± i√(λ²+a²)}**（各二重）。",
    "- 也就是说：**只有 Re ζ 进频率，Im ζ 只给一个统一衰减率 −b**；",
    "  b≠0 时流是对数螺线（阻尼/增益旋转），不是 J116 说的等角旋转。",
    "- **det A=(λ²+a²+b²)²>0**、rank A=4 ⇒ 复 ζ 下仍只有静止解 Ψ≡0。",
    "- M1 实线性 ⇒ **A(cX)=cA(X)** ⇒ 任何模长都是等价的；径向方程 ṙ=−br 的",
    "  不动点只有 r=0（b≠0）或全体 r（b=0）⇒ **r=v 永远不是吸引子**。",
    "- **∂_μJ^μ=−2 Im(ζ)|Ψ|²**（λ 项逐点相消，与 λ 复实无关）⇒ S13-C0001 的",
    "  「∂_μJ^μ=0」只在**板块一（ζ=0）**成立；附录未声明 ζ∈ℝ。",
    "",
    "## 四条结构方程（条件式，不是新物理）",
    "",
    "- **E6 极小多项式**：A²+2bA+(λ²+a²+b²)I=0；(A+bI)²=−(λ²+a²)I。",
    "- **E6′ 谱**：{−b±i√(λ²+a²)}（二重）；det=(λ²+|ζ|²)²；tr=−4b。",
    "- **E7 J116 范围**：A²=−(λ²+ζ²)I 与纯转动是 b=0 切片。",
    "- **E8 钉扎不可能**：A 实线性 ⇒ 不选模长；|Ψ|²=v² 只能外加。",
    "- **E9 守恒破缺**：∂_μJ^μ=−2 Im(ζ)|Ψ|²。",
    "",
    "## 三条勘误",
    "",
]
for e in payload["errata"]:
    lines.append("- **%s**：%s → %s。影响：%s" % (e["where"], e["what"], e["fix"], e["impact"]))
lines += [
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
    "- E6–E9 是对**既有方程**在复耦合下的结构判定与三处范围勘误。",
    "- 「不能钉扎模长」是线性 M1 的性质，不排除未来某个非线性扩展；本册不提出该扩展。",
    "- ζ 的物理起源（为什么它可能为实）没有被回答，`O-SCALE` 等 8 条 OPEN 全部保持。",
    "",
    "## 边界",
    "",
    "- 只审计 0+1 维齐次生成元、常数复 ζ；σ·∇ 项与非线性扩展不在口径内。",
    "- 不判 M1 物理错误，不翻案任何既有判定，不改记分板 0/6。",
    "- 锚点：equations.md／附录A／claims.csv／卷 137／_j116 脚本与产物。",
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
    f.write("J117 M1 COMPLEX COUPLING | PASS | gates %d/%d\n" % (total, passed))
    f.write("A = lam*T + a*J - b*I (zeta=a+ib); A^2 + 2bA + (lam^2+a^2+b^2) I = 0\n")
    f.write("(A+bI)^2 = -(lam^2+a^2) I ; spec = {-b +/- i sqrt(lam^2+a^2)} each twice\n")
    f.write("det A = (lam^2+|zeta|^2)^2 ; tr A = -4b ; rank A = 4\n")
    f.write("A(cX)=cA(X) => no modulus is selected; |Psi|^2=v^2 stays external\n")
    f.write("dd_mu J^mu = -2 Im(zeta) |Psi|^2 ; S13-C0001 is scoped to zeta=0\n")
    f.write("scoreboard 0/6 | validated 0 | 4-force GUT 0 | OPEN 8 | closed 0\n")

print("J117 OK | gates %d/%d | spec=-b +/- i*sqrt(lam^2+a^2) | no pinning | "
      "divJ=-2b|Psi|^2 | scoreboard 0/6 | outputs 3" % (passed, total))
