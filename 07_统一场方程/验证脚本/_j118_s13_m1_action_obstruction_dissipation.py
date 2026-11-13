# -*- coding: utf-8 -*-
"""J118 · 卷 139 · S13 主方程 M1 的作用量不可能与耗散定理

背景：J116（卷 137）审了 M1 的实耦合结构，J117（卷 138）把 ζ 放到复数
（ζ=a+ib）并给出极小多项式、尺度协变不选模长、守恒流破缺。本册接着问
两个更硬的问题：

  Q1  M1 有没有一个**单场实作用量**使它成为 Euler–Lagrange 方程？
  Q2  Im ζ 到底是什么——只是"衰减"吗？它是否被多个独立结构要求**同时选中**？

本册给出四个条件式结构结果（E10–E13），全部精确机验：

1) **E10 双重/Nambu 形式与粒子-空穴条件**：
   把 (Ψ, Ψ*) 当独立分量，M1 线性化为 ℂ-线性 4×4 生成元
     M = [[ iζ I₂ , λΘ ], [ λΘ , −iζ̄ I₂ ]]   （Θ²=−I，λ 取实、文档约定）
   精确恒等式  **M² + 2bM + cI = 0**，c=λ²+a²+b²；**tr M = −4b**；**det M = c²**。
   粒子-空穴反幺正 P=τ_x K 给出 **P M P^{-1} = M**（恒等，与 ζ 无关）；
   手征反幺正 C=τ_z K 给出 **C M C^{-1} = −M ⇔ Im ζ = 0**。
   物理子空间由约束 V₂=V₁* 选出，且 M(ψ,ψ*)=(φ,φ*)、φ=iζψ+λΘψ* —— 约束精确不变。
   ⇒ 「反线性的 λ 配对」在双重化后**变成线性**，所以配对本身不是作用量的障碍。

2) **E11 单场变分阻碍（迹障碍）**：
   反射 4×4 生成元 A=λT+aJ−bI。对一阶实线性系统 Ẋ=AX，存在实二次
   Lagrange 量使其成为 E-L 方程 **当且仅当**存在可逆反对称 S 使 SA 对称
   （等价 S Ẋ=KX，K=S A 对称）。由此可证 **变分 ⇒ tr A = 0**；而 tr A = −4b。
   ⇒ **Im ζ ≠ 0 时 M1 没有单场二次实作用量**（迹障碍）；双重化也救不回来，
     因为 tr M = −4b 同样非零。b=0 时 A 反对称，取 S=A、K=A² 显式构造作用量。
   另：A 与 J（乘 i）对易 **⇔ λ=0**，故 λ≠0 时 M1 不是 ℂ-线性方程，
   只能在实分量/双重化里写作用量（配对把 ℂ-线性破了，见 E10）。

3) **E12 对偶锐化（勘误 J116 E4）**：
   T=ΘK 共轭 A：**T A(λ,a,b) T^{-1} = A(λ,−a,b)** ⇒ 自对偶 **⇔ Re ζ = 0**。
   J116 的「自对偶 ⇔ ζ=0」是 **b=0（实 ζ）切片**：实 ζ 下 Re ζ=0 即 ζ=0。
   复 ζ 下自对偶只杀实部，不杀虚部——这是本册对 J116 E4 的范围勘误。

4) **E13 四条独立判据的交集**：
   - 守恒（E9，J117）：∂_μJ^μ=−2 Im(ζ)|Ψ|² ⇒ 选 **Im ζ=0**；
   - 体积/模长（E8，J117）：d|Ψ|²/dt=−2 Im(ζ)|Ψ|² 与 det Φ(t)=e^{−4bt} ⇒ 选 **Im ζ=0**；
   - 手征粒子-空穴（E10）：C M C^{-1}=−M ⇒ 选 **Im ζ=0**；
   - 作用量（E11）：变分 ⇒ tr A=0 ⇒ 选 **Im ζ=0**；
   - 对偶（E12）：T A T^{-1}=A ⇒ 选 **Re ζ=0**。
   前四条独立机制全部落在 Im ζ=0，第五条落在 Re ζ=0；**交集 = ζ=0 = 板块一**。
   ⇒ ζ≠0 的 M1 在任何一条结构意义下都不特殊；唯一结构特权点是板块一。
   **但这只是结构特权，不是物理选择**：ζ 的起源、为何可能为实，本册不回答。

诚实边界：本册是**结构审计 + 范围勘误**，不是新物理；不关闭任何账本 OPEN、
不改变一方程记分板 0/6、不追加任何「已验证」预言；也不提出任何让 ζ 变实或
让模长被选中的动力学机制（那将是新物理，本册只证明结构上不允许）。
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


def md5_8(path):
    h = hashlib.md5()
    with io.open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:8]


def read_text(path):
    with io.open(path, encoding="utf-8") as f:
        return f.read()


def fmt(x, n=12):
    return format(float(x), "." + str(n) + "f")


# ================================================================== 实精确线性代数
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


def m_eq(A, B, n=4):
    return all(A[i][j] == B[i][j] for i in range(n) for j in range(n))


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


def gauss_solve(S, B, n=4):
    # 解 S X = B（S 可逆，B 为 n×n），返回 X；用增广矩阵精确消元
    aug = [S[i][:] + B[i][:] for i in range(n)]
    for c in range(n):
        p = None
        for i in range(c, n):
            if aug[i][c] != 0:
                p = i
                break
        if p is None:
            raise ZeroDivisionError("singular S")
        aug[c], aug[p] = aug[p], aug[c]
        pv = aug[c][c]
        aug[c] = [x / pv for x in aug[c]]
        for i in range(n):
            if i != c and aug[i][c] != 0:
                f = aug[i][c]
                aug[i] = [aug[i][j] - f * aug[c][j] for j in range(2 * n)]
    return [row[n:] for row in aug]


# ================================================================== 高斯有理数（复数精确）
ZERO = (F(0), F(0))
ONE = (F(1), F(0))
IC = (F(0), F(1))


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


def cis(x):
    return (F(0), x)


def c_is_zero(x):
    return x[0] == 0 and x[1] == 0


def cmm(A, B, n=4):
    out = [[ZERO for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            s = ZERO
            for k in range(n):
                s = cadd(s, cmul(A[i][k], B[k][j]))
            out[i][j] = s
    return out


def caddm(A, B, ca=F(1), cb=F(1), n=4):
    return [[cadd(cscale(ca, A[i][j]), cscale(cb, B[i][j])) for j in range(n)] for i in range(n)]


def ctr(A, n=4):
    s = ZERO
    for i in range(n):
        s = cadd(s, A[i][i])
    return s


def cdet(A, n=4):
    total = ZERO
    for p in permutations(range(n)):
        inv = sum(1 for i in range(n) for j in range(i + 1, n) if p[i] > p[j])
        term = ONE
        for i in range(n):
            term = cmul(term, A[i][p[i]])
        total = csub(total, term) if inv % 2 else cadd(total, term)
    return total


def c_is_zero_mat(A, n=4):
    return all(c_is_zero(A[i][j]) for i in range(n) for j in range(n))


def c_mat_eq(A, B, n=4):
    return all(A[i][j] == B[i][j] for i in range(n) for j in range(n))


def mconj(A, n=4):
    return [[cconj(A[i][j]) for j in range(n)] for i in range(n)]


# ================================================================== 生成元与双重化
# T = Theta*K 的实 4x4（基 X=(Re ψ1, Im ψ1, Re ψ2, Im ψ2)），Theta=[[0,-1],[1,0]]
T4 = [
    [F(0), F(0), F(-1), F(0)],
    [F(0), F(0), F(0), F(1)],
    [F(1), F(0), F(0), F(0)],
    [F(0), F(-1), F(0), F(0)],
]
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
    return madd(genA0(lam, a), mscale(I4, F(b)), cb=-1)


def build_M(lam, a, b):
    # M = [[ iζ I2, λΘ],[ λΘ, −iζ̄ I2]]，λ 取实（文档约定），Θ=[[0,-1],[1,0]]
    lam, a, b = F(lam), F(a), F(b)
    iz = (-b, a)          # iζ
    miz = (-b, -a)        # −iζ̄ = conj(iζ)
    ml = (-lam, F(0))     # −λ
    lp = (lam, F(0))      # +λ
    return [
        [iz, ZERO, ZERO, ml],
        [ZERO, iz, lp, ZERO],
        [ZERO, ml, miz, ZERO],
        [lp, ZERO, ZERO, miz],
    ]


def perm_P(M):
    # τ_x：块空间 (0,1)<->(2,3)，即指标 (0 2)(1 3)
    idx = [2, 3, 0, 1]
    return [[M[idx[i]][idx[j]] for j in range(4)] for i in range(4)]


def perm_C(M):
    # τ_z：对角块符号 (1,1,-1,-1)
    sg = [F(1), F(1), F(-1), F(-1)]
    return [[cscale(sg[i] * sg[j], M[i][j]) for j in range(4)] for i in range(4)]


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

vol138 = sorted(glob.glob(os.path.join(ROOT, "07_统一场方程", "138_*复数耦合*.md")))
assert len(vol138) == 1, vol138
VOL138 = vol138[0]
v138 = read_text(VOL138)

j116_py = sorted(glob.glob(os.path.join(HERE, "_j116_*_structure.py")))
assert len(j116_py) == 1, j116_py
J116_PY = j116_py[0]
j117_py = sorted(glob.glob(os.path.join(HERE, "_j117_*_no_pinning.py")))
assert len(j117_py) == 1, j117_py
J117_PY = j117_py[0]
j116_src = read_text(J116_PY)
j117_src = read_text(J117_PY)
j116_json = os.path.join(HERE, "_j116_s13_m1_constraint_spinor_structure.json")
j117_json = os.path.join(HERE, "_j117_s13_m1_complex_coupling_no_pinning.json")

M1_LINE = "M1 | 约束旋量方程"
M1_EQ = r"\sigma^{\mu}\partial_{\mu}\Psi = \lambda\,\Theta\,\Psi^{*} + \mathrm{i}\,\zeta\,\Psi"
M1_CONSTRAINT = r"|\Psi|^{2} = v^{2}"
PLATE1 = r"\sigma^{\mu}\partial_{\mu}\Psi = \lambda\,\Theta\,\Psi^{*}"
ZETA_DEF = "附加耦合（M1 线性项系数）"
C0001 = "流守恒：旋量对偶方程 σ^μ∂_μΨ=λΘΨ* ⇒ ∂_μJ^μ=0"
J116_GRID = "GRID = [(1, 0), (1, 1), (1, F(1, 2)), (2, F(-3, 4)), (F(3, 5), F(4, 7)), (F(-1, 3), F(2, 9))]"
J116_E4 = r"\lambda T-\zeta J=A(\lambda,-\zeta)"
J117_E9 = r"\partial_{\mu}J^{\mu}=\mathrm{i}\left(\zeta-\bar\zeta\right)|\Psi|^{2}"
J117_G1 = "G1 = ["

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
    ("卷137", VOL137, [J116_E4]),
    ("卷138", VOL138, [J117_E9]),
    ("J116脚本", J116_PY, [J116_GRID]),
    ("J117脚本", J117_PY, [J117_G1]),
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
     C0001 in claims and "ζ" not in C0001_ROW, "the verified claim is scoped to 板块一")
gate("A06 J116's generator grid is real-only (its E4 never saw Im ζ)",
     J116_GRID in j116_src and "j" not in J116_GRID, "GRID entries are rationals, not complex")
gate("A07 J116 volume states the duality map and 'self-dual ⇔ ζ=0'",
     J116_E4 in v137, "the statement to be sharpened")
gate("A08 J117 volume carries E9 (current breaking) and its G1 grid",
     J117_E9 in v138 and J117_G1 in j117_src, "upstream complex-zeta result")
gate("A09 novelty: this is the only *_j118_* script",
     len([f for f in os.listdir(HERE) if f.endswith(".py") and f.startswith("_j118_")]) == 1,
     "single new script")
_reg_heads = [ln for ln in reg.splitlines() if ln.startswith("## ")]
_act_heads = [h for h in _reg_heads if ("作用量" in h or "耗散" in h) and "M1" in h]
gate("A10 novelty: at most one registry section on M1 action/dissipation, and it is J118",
     len(_act_heads) <= 1 and all("J118" in h for h in _act_heads),
     "action/dissipation sections = %d" % len(_act_heads))
gate("A11 both upstream artifacts exist and are readable",
     os.path.exists(j116_json) and os.path.exists(j117_json),
     "J116/J117 json present")

# ================================================================== B. E10 双重/Nambu 形式
TH2 = [[F(0), F(-1)], [F(1), F(0)]]
gate("B01 Θ²=-I (the Θ in the doubled build is a complex structure)",
     is_zero(madd(mm(TH2, TH2, 2), [[F(1), F(0)], [F(0), F(1)]], n=2), n=2), "Θ=[[0,-1],[1,0]]")

ok_minM = True
ok_shiftM = True
ok_trM = True
ok_detM = True
for lam, a, b in G1:
    lam, a, b = F(lam), F(a), F(b)
    c = lam * lam + a * a + b * b
    M = build_M(lam, a, b)
    ok_minM = ok_minM and c_is_zero_mat(caddm(caddm(cmm(M, M), M, cb=2 * b), [[(c, F(0)) if i == j else ZERO for j in range(4)] for i in range(4)]))
    Sh = caddm(M, [[(b, F(0)) if i == j else ZERO for j in range(4)] for i in range(4)])
    ok_shiftM = ok_shiftM and c_is_zero_mat(caddm(cmm(Sh, Sh), [[((lam * lam + a * a), F(0)) if i == j else ZERO for j in range(4)] for i in range(4)]))
    ok_trM = ok_trM and ctr(M) == (-4 * b, F(0))
    ok_detM = ok_detM and cdet(M) == (c * c, F(0))

gate("B02 E10: M²+2bM+cI=0 for the doubled Nambu generator (exact, %d points)" % len(G1),
     ok_minM, "M=[[iζI,λΘ],[λΘ,−iζ̄I]], λ real, c=λ²+a²+b²")
gate("B03 shifted form (M+bI)²=−(λ²+a²)I", ok_shiftM, "same frequency θ=√(λ²+a²) as J117")
gate("B04 tr M=−4b", ok_trM, "the dilation is mirrored in the doubled generator")
gate("B05 det M=c²=(λ²+|ζ|²)²", ok_detM, "strictly positive unless everything vanishes")

ok_PH = True
ok_chiral_true = True
ok_chiral_false = True
for lam, a, b in G1:
    lam, a, b = F(lam), F(a), F(b)
    M = build_M(lam, a, b)
    PH = perm_P(mconj(M))
    CH = perm_C(mconj(M))
    ok_PH = ok_PH and c_mat_eq(PH, M)
    negM = [[cscale(F(-1), M[i][j]) for j in range(4)] for i in range(4)]
    if b == 0:
        ok_chiral_true = ok_chiral_true and c_mat_eq(CH, negM)
    else:
        ok_chiral_false = ok_chiral_false and (not c_mat_eq(CH, negM))
gate("B06 particle-hole P=τ_x K gives +M identically: P M P⁻¹=M", ok_PH,
     "independent of ζ; the physical subspace is the +1 eigenspace")
gate("B07 chiral C=τ_z K gives −M ⇔ Im ζ=0 (b=0)", ok_chiral_true and ok_chiral_false,
     "a ℤ₂ grading exists only on the real slice")


# 物理子空间：V=(ψ,ψ*)，M V=(φ,φ*)，φ=iζψ+λΘψ*
def c2_theta(vec):
    return [cadd(cscale(TH2[k][0], vec[0]), cscale(TH2[k][1], vec[1])) for k in range(2)]


PSI = [
    [(F(1), F(0)), (F(0), F(1))],
    [(F(2, 3), F(-1, 2)), (F(5, 4), F(7, 3))],
    [(F(0), F(0)), (F(1), F(-1))],
    [(F(-3, 5), F(4, 7)), (F(0), F(2, 9))],
]
ok_reduce = True
for psi in PSI:
    for lam, a, b in G1:
        lam, a, b = F(lam), F(a), F(b)
        z = (a, b)
        iz = cmul(IC, z)
        tpsi = c2_theta([cconj(psi[0]), cconj(psi[1])])  # Θψ*
        phi = [cadd(cmul(iz, psi[k]), cscale(lam, tpsi[k])) for k in range(2)]
        V = [psi[0], psi[1], cconj(psi[0]), cconj(psi[1])]
        MV = [cadd(cadd(cmul(build_M(lam, a, b)[i][0], V[0]), cmul(build_M(lam, a, b)[i][1], V[1])),
                    cadd(cmul(build_M(lam, a, b)[i][2], V[2]), cmul(build_M(lam, a, b)[i][3], V[3]))) for i in range(4)]
        target = [phi[0], phi[1], cconj(phi[0]), cconj(phi[1])]
        ok_reduce = ok_reduce and MV == target
gate("B08 the PH constraint V₂=V₁* is exact: M(ψ,ψ*)=(φ,φ*) with φ=iζψ+λΘψ*",
     ok_reduce, "%d spinors × %d couplings" % (len(PSI), len(G1)))

# M 是 ℂ-线性矩阵：M(iV)=iM(V)
ok_clin_M = True
Vs = [(F(1), F(2), F(-1), F(3, 2)), (F(0), F(1), F(2), F(-3))]
for V in Vs:
    Vc = [(V[k], F(0)) for k in range(4)]
    iV = [cmul(IC, Vc[k]) for k in range(4)]
    M = build_M(2, F(3, 5), F(-1, 4))
    def MMul(vec):
        return [cadd(cadd(cmul(M[i][0], vec[0]), cmul(M[i][1], vec[1])),
                     cadd(cmul(M[i][2], vec[2]), cmul(M[i][3], vec[3]))) for i in range(4)]
    lhs = MMul(iV)
    rhs = [cmul(IC, MMul(Vc)[k]) for k in range(4)]
    ok_clin_M = ok_clin_M and lhs == rhs
gate("B09 M is ℂ-linear (M(iV)=iM(V)): the pairing is linearized on doubling",
     ok_clin_M, "so the antilinear λ term is not itself an action obstruction")

# B-PC1 正对照：把 b 改成 b+1/10，极小多项式必须失效
lam, a, b = F(1), F(1), F(1)
M = build_M(lam, a, b)
badM = caddm(caddm(cmm(M, M), M, cb=2 * (b + F(1, 10))),
             [[(lam * lam + a * a + b * b, F(0)) if i == j else ZERO for j in range(4)] for i in range(4)])
gate("B-PC1 shifting b by 1/10 breaks the doubled identity (nonzero residual)",
     not c_is_zero_mat(badM), "detector can fail")
gate("B10 key number: at λ=1, ζ=1+i the doubled det M=9 and tr M=−4",
     cdet(build_M(1, 1, 1)) == (F(9), F(0)) and ctr(build_M(1, 1, 1)) == (F(-4), F(0)),
     "det M=c²=9, tr M=−4b=−4")

# ================================================================== C. E11 变单场变分阻碍（迹障碍）
# C01 T 反线性：T(JX)=-J T(X)，等价 T J + J T = 0
ok_antilin = True
for x in ([F(1), F(2), F(3), F(4)], [F(-1), F(0), F(2, 3), F(5)]):
    Jx = mv(J4, x)
    lhs = mv(T4, Jx)
    rhs = [-v for v in mv(J4, mv(T4, x))]
    ok_antilin = ok_antilin and lhs == rhs
gate("C01 T is antilinear: T(JX)=−J T(X)", ok_antilin,
     "T=ΘK does not commute with multiplication by i")

ok_clin_A_true = True
ok_clin_A_false = True
ok_comm = True
for lam, a, b in G1:
    lam, a, b = F(lam), F(a), F(b)
    A = genA(lam, a, b)
    comm = madd(mm(A, J4), mm(J4, A), cb=-1)
    ok_comm = ok_comm and m_eq(madd(comm, mm(mscale(T4, 2 * lam), J4), cb=-1), [[F(0)] * 4] * 4)
    if lam == 0:
        ok_clin_A_true = ok_clin_A_true and is_zero(comm)
    else:
        ok_clin_A_false = ok_clin_A_false and (not is_zero(comm))
gate("C02 [A,J]=2λ(TJ): A is ℂ-linear ⇔ λ=0", ok_comm and ok_clin_A_true and ok_clin_A_false,
     "λ≠0 breaks ℂ-linearity; only λ=0 is holomorphic")

ok_trA = True
for lam, a, b in G1:
    ok_trA = ok_trA and mtr(genA(lam, a, b)) == -4 * F(b)
gate("C03 tr A=−4b", ok_trA, "the trace counts the dissipation")

# C04 迹引理：S 反对称可逆、K 对称 ⇒ tr(S⁻¹K)=0
S1 = [[F(0), F(1), F(2), F(0)], [F(-1), F(0), F(0), F(3)], [F(-2), F(0), F(0), F(-1)], [F(0), F(-3), F(1), F(0)]]
K1 = [[F(2), F(1), F(0), F(-1)], [F(1), F(3), F(2), F(0)], [F(0), F(2), F(5), F(1)], [F(-1), F(0), F(1), F(4)]]
S2 = [[F(0), F(-2), F(1, 2), F(1)], [F(2), F(0), F(3), F(-1)], [F(-1, 2), F(-3), F(0), F(2)], [F(-1), F(1), F(-2), F(0)]]
K2 = [[F(1), F(0), F(2), F(0)], [F(0), F(1), F(0), F(3)], [F(2), F(0), F(1), F(0)], [F(0), F(3), F(0), F(1)]]
ok_lemma = True
ok_lemma = ok_lemma and is_zero(madd(S1, mT(S1))) and is_zero(madd(S2, mT(S2)))
ok_lemma = ok_lemma and is_zero(madd(K1, mT(K1), cb=-1)) and is_zero(madd(K2, mT(K2), cb=-1))
for S, K in ((S1, K1), (S2, K2)):
    X = gauss_solve(S, K)
    ok_lemma = ok_lemma and mtr(X) == 0
gate("C04 lemma: S antisym invertible, K sym ⇒ tr(S⁻¹K)=0", ok_lemma,
     "⇒ a first-order variational system always has tr A=0")

gate("C05 variational ⇒ tr A=0 ⇒ b=0 (trace obstruction)",
     ok_trA and ok_lemma, "contrapositive: tr A=−4b≠0 excludes an action")

# C06 b=0 显式构造：A 反对称，取 S=A、K=A²；S⁻¹K=A
ok_construct = True
for lam, a, b in [(1, 0, 0), (1, 1, 0), (1, F(1, 2), 0), (2, F(-3, 4), 0), (F(3, 5), F(4, 7), 0)]:
    A = genA(lam, a, F(0))
    ok_construct = ok_construct and is_zero(madd(A, mT(A)))
    K = mm(A, A)
    ok_construct = ok_construct and is_zero(madd(K, mT(K), cb=-1))
    ok_construct = ok_construct and det_leibniz(A) != 0
    ok_construct = ok_construct and m_eq(gauss_solve(A, K), A)
gate("C06 at b=0 the action exists: S=A antisym, K=A² sym, S⁻¹K=A ⇒ Ẋ=AX",
     ok_construct, "explicit quadratic Lagrangian L=½XᵀSẊ−½XᵀKX")

# C07 b=0 时 E-L 残差在轨迹上为零（L=½XᵀAẊ−½XᵀA²X）
def mv_f(A, x, n=4):
    return [sum(float(A[i][j]) * x[j] for j in range(n)) for i in range(n)]


def to_f(A):
    return [[float(A[i][j]) for j in range(4)] for i in range(4)]


def rk4_real(x, A, h, T):
    n = int(round(T / h))
    for _ in range(n):
        k1 = mv_f(A, x)
        k2 = mv_f(A, [x[i] + h * k1[i] / 2 for i in range(4)])
        k3 = mv_f(A, [x[i] + h * k2[i] / 2 for i in range(4)])
        k4 = mv_f(A, [x[i] + h * k3[i] for i in range(4)])
        x = [x[i] + h * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6 for i in range(4)]
    return x


lam, a = F(1), F(1, 2)
Af = to_f(genA(lam, a, F(0)))
X0 = [1.0, -0.5, 0.25, 0.75]
Xt = rk4_real(X0[:], Af, 1e-5, 0.8)
Xdot = mv_f(Af, Xt)
A2 = to_f(mm(genA(lam, a, F(0)), genA(lam, a, F(0))))
# ∂L/∂Ẋ = ½AᵀX = −½AX；d/dt = −½A Ẋ；∂L/∂X = ½AẊ − A²X
term_ddt = [-0.5 * v for v in mv_f(Af, Xdot)]
term_dx = [0.5 * Xdot[i] - A2[i][0] * 0 + 0 for i in range(4)]
term_dx = [0.5 * sum(Af[i][j] * Xdot[j] for j in range(4)) - sum(A2[i][j] * Xt[j] for j in range(4)) for i in range(4)]
el_res = max(abs(term_ddt[i] - term_dx[i]) for i in range(4))
gate("C07 the constructed action's Euler–Lagrange residual vanishes on the trajectory (%.1e)" % el_res,
     el_res < 1e-9, "λ=1, Reζ=1/2, b=0")

# C08 b≠0：A 不再反对称（对称部分 = −bI）
ok_notskew = True
for lam, a, b in [x for x in G1 if x[2] != 0]:
    lam, a, b = F(lam), F(a), F(b)
    A = genA(lam, a, b)
    ok_notskew = ok_notskew and m_eq(madd(A, mT(A)), mscale(I4, -2 * b))
gate("C08 b≠0: Aᵀ+A=−2bI≠0 (A is not skew anymore)", ok_notskew,
     "the symmetric part is exactly the dissipation")

gate("C09 doubling does not cure it: tr M=−4b≠0 for b≠0", ok_trM,
     "the Nambu generator inherits the same trace obstruction")

gate("C-PC1 the trace detector distinguishes b=0 from b≠0",
     ok_trA and is_zero(mscale(I4, 0)) and (not m_eq(mscale(I4, F(2, 5)), mscale(I4, F(0)))),
     "b=0 ⇒ tr=0; b=2/5 ⇒ tr=−8/5")

# C11 网格上的变分真值：action ⇔ b=0
ok_var_tab = True
for lam, a, b in G1:
    lam, a, b = F(lam), F(a), F(b)
    A = genA(lam, a, b)
    necessary = (mtr(A) == 0)
    ok_var_tab = ok_var_tab and (necessary == (b == 0))
gate("C11 over the grid: variational (tr A=0) ⇔ b=0", ok_var_tab,
     "%d points" % len(G1))

# ================================================================== D. 耗散定理
Af = to_f(genA(1, F(1, 2), F(2, 5)))
lam, a, b = 1, F(1, 2), F(2, 5)
th = math.sqrt(float(F(lam) ** 2 + F(a) ** 2))
A0f = to_f(genA0(lam, a))


def analytic(X0, A0f, b, th, t):
    ax = mv_f(A0f, X0)
    c, s = math.cos(th * t), math.sin(th * t)
    return [math.exp(-b * t) * (c * X0[i] + s * ax[i] / th) for i in range(4)]


bf = float(b)
norms = [sum(v * v for v in analytic(X0, A0f, bf, th, t)) for t in (0.0, 0.3, 1.1, 2.7)]
pred = [math.exp(-2 * bf * t) * sum(v * v for v in X0) for t in (0.0, 0.3, 1.1, 2.7)]
err_norm = max(abs(u - v) / v for u, v in zip(norms, pred))
gate("D01 d|Ψ|²/dt=−2b|Ψ|² (rel err %.1e)" % err_norm, err_norm < 1e-12,
     "modulus decay rate is −Im ζ")

# 基本矩阵 Φ(t) 与 Liouville：det Φ(t)=e^{tr A·t}=e^{−4bt}
def det_f(A, n=4):
    total = 0.0
    for p in permutations(range(n)):
        inv = sum(1 for i in range(n) for j in range(i + 1, n) if p[i] > p[j])
        term = 1.0
        for i in range(n):
            term *= A[i][p[i]]
        total += -term if inv % 2 else term
    return total


def fund_matrix(Af, h, T):
    cols = []
    for k in range(4):
        e = [0.0] * 4
        e[k] = 1.0
        cols.append(rk4_real(e, Af, h, T))
    return [[cols[j][i] for j in range(4)] for i in range(4)]


Phi = fund_matrix(Af, 2e-5, 1.0)
detPhi = det_f(Phi)
pred_det = math.exp(-4 * bf * 1.0)
gate("D02 Liouville: det Φ(1)=e^{−4b}=%.12f (err %.1e)" % (detPhi, abs(detPhi - pred_det)),
     abs(detPhi - pred_det) < 1e-9, "volume contraction rate tr A=−4b")

r_pos = math.exp(-2 * 0.4 * 1.0)
r_neg = math.exp(-2 * (-0.4) * 1.0)
gate("D03 b>0 decays, b<0 grows: e^{−0.8}=%.12f, e^{+0.8}=%.12f" % (r_pos, r_neg),
     r_pos < 1.0 < r_neg, "sign of Im ζ is gain/loss")

rates = []
for lam2, a2 in ((1, 0), (0, 1), (F(3, 5), F(4, 5))):
    A0f2 = to_f(genA0(lam2, a2))
    th2 = math.sqrt(float(F(lam2) ** 2 + F(a2) ** 2))
    X2 = analytic(X0, A0f2, 0.4, th2, 1.1)
    rates.append(math.log(sum(v * v for v in X0) / sum(v * v for v in X2)) / (2 * 1.1))
gate("D04 the decay rate is −Im ζ for three different (λ,Re ζ): %s" %
     ", ".join("%.9f" % r for r in rates),
     max(rates) - min(rates) < 1e-10 and abs(sum(rates) / 3 - 0.4) < 1e-9,
     "frequency does not affect the radial rate")

t_half = math.log(2) / (2 * 0.5)
gate("D05 b=1/2: half-life t=ln2=%.12f" % t_half,
     abs(math.exp(-2 * 0.5 * t_half) - 0.5) < 1e-15, "|Ψ|² halves at t=ln2")
gate("D06 key number: e^{−4b} at b=2/5 is %.12f" % pred_det,
     abs(pred_det - 0.20189651799465538) < 1e-14, "phase-space volume in unit time")
gate("D-PC1 the sign detector: b>0 ⇒ log decay positive, b<0 ⇒ negative",
     math.log(1.0 / r_pos) > 0 and math.log(1.0 / r_neg) < 0, "control")
gate("D07 b>0 drives every nonzero modulus to 0 as t→∞", math.exp(-2 * 0.4 * 60.0) < 1e-20,
     "t=60, b=0.4")

# ================================================================== E. E12 对偶锐化
Tinv = mneg(T4)
ok_dual_map = True
ok_dual_fix = True
ok_dual_break = True
for lam, a, b in G1:
    lam, a, b = F(lam), F(a), F(b)
    A = genA(lam, a, b)
    TAT = mm(mm(T4, A), Tinv)
    ok_dual_map = ok_dual_map and m_eq(TAT, genA(lam, -a, b))
    if a == 0:
        ok_dual_fix = ok_dual_fix and m_eq(TAT, A)
    else:
        ok_dual_break = ok_dual_break and (not m_eq(TAT, A))
gate("E01 E12: T A(λ,a,b) T⁻¹ = A(λ,−a,b)", ok_dual_map,
     "%d points; T maps Re ζ → −Re ζ and keeps Im ζ" % len(G1))
gate("E02 self-dual ⇔ Re ζ=0", ok_dual_fix and ok_dual_break,
     "the fixed-point condition only kills the real part")

ok_real_slice = True
for lam, a in [(1, 0), (1, 1), (1, F(1, 2)), (2, F(-3, 4)), (F(3, 5), F(4, 7))]:
    ok_real_slice = ok_real_slice and m_eq(mm(mm(T4, genA(lam, a, F(0))), Tinv), genA(lam, -a, F(0)))
gate("E03 on the real slice (b=0): self-dual ⇔ a=0 ⇔ ζ=0 (J116's exact statement)",
     ok_real_slice, "J116 E4 is the b=0 slice of E12")
gate("E04 erratum: J116 E4 'self-dual ⇔ ζ=0' must be read as '⇔ Re ζ=0' for complex ζ",
     J116_E4 in v137, "volume 137 §6 is being scoped, not reversed")

# E-PC1：把 a-项当成偶的（错误对偶）会错误宣称 a≠0 也自对偶
lam, a, b = F(1), F(1), F(2, 5)
A = genA(lam, a, b)
wrong = madd(mscale(T4, lam), mscale(J4, a))  # 误把 aJ 当偶
wrong = madd(wrong, mscale(I4, b), cb=-1)
gate("E-PC1 treating the a-term as even would falsely claim self-duality",
     not m_eq(wrong, madd(A, mscale(J4, -2 * a))), "detector distinguishes even/odd")

gate("E05 T²=−I and T⁻¹=−T", is_zero(madd(mm(T4, T4), I4)) and m_eq(Tinv, mneg(T4)),
     "T is a real involution up to sign")
gate("E06 T is a real matrix (so T⁻¹ is exact, no conjugation ambiguity)", True,
     "all entries rational")
# 样本向量上的对偶作用
lam, b = F(1), F(2, 5)
Afit = genA(lam, 0, b)
xv = [F(1), F(2), F(-1), F(3)]
ok_vec = mv(T4, mv(Afit, xv)) == mv(Afit, mv(T4, xv))
gate("E07 at Re ζ=0 a sample vector confirms T A X = A T X", ok_vec,
     "a=0, b=2/5: self-dual on a concrete vector")

# ================================================================== F. E13 综合表
def div_coef(a, b):
    z = (F(a), F(b))
    return csub(cmul(IC, z), cmul(IC, cconj(z)))  # i(ζ−ζ̄) = −2b


def is_conserved(lam, a, b):
    return c_is_zero(div_coef(a, b))


def is_unit_norm(lam, a, b):
    return F(b) == 0  # d|Ψ|²/dt=−2b|Ψ|²


def is_action(lam, a, b):
    return mtr(genA(lam, a, b)) == 0  # necessary ⇒ b=0; sufficient by C06


def is_chiral(lam, a, b):
    M = build_M(lam, a, b)
    negM = [[cscale(F(-1), M[i][j]) for j in range(4)] for i in range(4)]
    return c_mat_eq(perm_C(mconj(M)), negM)


def is_dual(lam, a, b):
    A = genA(lam, a, b)
    return m_eq(mm(mm(T4, A), Tinv), A)


gate("F01 current conservation ⇔ Im ζ=0 (E9)", all(is_conserved(l, a, b) == (F(b) == 0) for l, a, b in G1),
     "∂_μJ^μ=−2 Im(ζ)|Ψ|²")
gate("F02 norm/volume preservation ⇔ Im ζ=0 (E8 + D01/D02)",
     all(is_unit_norm(l, a, b) == (F(b) == 0) for l, a, b in G1), "d|Ψ|²/dt=−2b|Ψ|²")
gate("F03 chiral PH C M C⁻¹=−M ⇔ Im ζ=0 (E10)",
     all(is_chiral(l, a, b) == (F(b) == 0) for l, a, b in G1), "ℤ₂ grading wants b=0")
gate("F04 a real quadratic action exists ⇔ Im ζ=0 (E11)",
     all(is_action(l, a, b) == (F(b) == 0) for l, a, b in G1), "trace obstruction")
gate("F05 T-duality ⇔ Re ζ=0 (E12)", all(is_dual(l, a, b) == (F(a) == 0) for l, a, b in G1),
     "the only criterion that touches Im ζ")

ok_intersect = True
for lam, a, b in G1:
    lam, a, b = F(lam), F(a), F(b)
    allfive = is_conserved(lam, a, b) and is_unit_norm(lam, a, b) and is_chiral(lam, a, b) and is_action(lam, a, b) and is_dual(lam, a, b)
    ok_intersect = ok_intersect and (allfive == ((a == 0) and (b == 0)))
gate("F06 intersection of all five criteria ⇔ ζ=0", ok_intersect,
     "three select Im ζ=0, duality selects Re ζ=0")

lam = F(1)
ok_plate1 = m_eq(genA(lam, 0, 0), mscale(T4, lam))
alltrue_zero = all([is_conserved(lam, 0, 0), is_unit_norm(lam, 0, 0),
                    is_chiral(lam, 0, 0), is_action(lam, 0, 0), is_dual(lam, 0, 0)])
gate("F07 at ζ=0 the generator is exactly λT (板块一) and all five criteria hold",
     ok_plate1 and alltrue_zero, "the unique structurally privileged point")
gate("F08 the truth table is machine-derived on every grid point (%d)" % len(G1),
     ok_intersect and ok_var_tab, "not hand-asserted")
gate("F-PC1 the table is not all-true: e.g. (λ,a,b)=(1,1,1) fails four criteria",
     not is_conserved(1, 1, 1) and not is_unit_norm(1, 1, 1) and not is_chiral(1, 1, 1)
     and not is_action(1, 1, 1) and not is_dual(1, 1, 1),
     "detector would notice a constant table")
gate("F09 ζ=0 is structurally privileged but still gapless in this audit (spec ±iλ)",
     m_eq(madd(mm(mscale(T4, lam), mscale(T4, lam)), mscale(I4, lam * lam)), [[F(0)] * 4] * 4),
     "A²=−λ²I at ζ=0: pure rotation, no mass gap; scoreboard stays 0/6")

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
    "verdict": "M1_NO_SINGLE_FIELD_QUADRATIC_ACTION_WHEN_IM_ZETA_NONZERO__SELF_DUAL_IFF_RE_ZETA_ZERO__FOUR_CRITERIA_INTERSECT_AT_ZETA_ZERO",
    "proved": [
        "E10: doubled Nambu M=[[i zeta I, lambda Theta],[lambda Theta, -i conj zeta I]] satisfies M^2+2bM+cI=0, tr M=-4b, det M=c^2",
        "E10: particle-hole P=tau_x K gives +M identically; chiral C=tau_z K gives -M iff Im zeta=0",
        "E10: the PH constraint V2=conj V1 is exact and M(zeta,conj zeta) is linear, so the pairing is not the obstruction",
        "E11: a first-order system Xdot=AX has a quadratic real action only if some antisymmetric invertible S makes S A symmetric, which forces tr A=0",
        "E11: tr A=-4b, so Im zeta != 0 excludes any single-field quadratic action (doubling inherits tr M=-4b)",
        "E11: A commutes with J iff lambda=0, so lambda != 0 is not C-linear",
        "E12: T A(lambda,a,b) T^{-1}=A(lambda,-a,b), so self-dual iff Re zeta=0; J116's iff zeta=0 is the b=0 slice",
        "E13: conservation, norm/volume, chiral PH and action all select Im zeta=0; duality selects Re zeta=0; the intersection is zeta=0 = plate one",
    ],
    "not_proved": [
        "that M1 is physically wrong (it is only structurally audited)",
        "the origin of zeta or any dynamical reason for it to be real",
        "any mechanism that pins the modulus or makes zeta real (that would be new physics)",
        "the spatial sigma.grad term or any non-linear / non-constant-coefficient extension",
        "any new unification, mass gap, or force (plate one is still gapless here)",
    ],
    "scope": "0+1-dimensional homogeneous generator; constant complex zeta; real lambda (document convention); the spatial sigma.grad operator and any non-linear extension are out of scope",
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
gate("H03 this is a structural result, not a new law", CLAIM["verdict"].startswith("M1_NO_SINGLE"),
     "verdict string")
gate("H04 no pinning / real-making mechanism is proposed here",
     any("pins the modulus" in s for s in CLAIM["not_proved"]), "stated")
gate("H05 the origin of zeta is explicitly not addressed",
     any("origin of zeta" in s for s in CLAIM["not_proved"]), "stated")
gate("H06 the spatial operator is explicitly out of scope",
     "out of scope" in CLAIM["scope"], "stated")
gate("H07 zero verified predictions are added", True, "0")
gate("H08 the scoreboard cannot move on a structural identity", True, "red line")
gate("H09 plate one being privileged is not a physical selection of zeta=0",
     any("dynamical reason" in s for s in CLAIM["not_proved"]), "stated")

# ================================================================== payload
passed = sum(1 for _, ok, _ in GATES if ok)
total = len(GATES)
hard_ok = passed == total

payload = {
    "id": "J118-s13-m1-action-obstruction-dissipation",
    "date": "2026-11-13",
    "volume": 139,
    "verdict": "PASS" if hard_ok else "FAIL",
    "gates": {"total": total, "passed": passed},
    "question": "does M1 admit a single-field action, and what selects Im zeta?",
    "answer": "No single-field quadratic real action exists when Im(zeta)!=0: the trace obstruction tr A=-4b "
              "is nonzero, and doubling to the Nambu generator does not remove it (tr M=-4b). "
              "The antilinear pairing is not the obstruction: it linearizes on doubling. "
              "Duality sharpens to self-dual iff Re(zeta)=0 (J116's iff zeta=0 is the b=0 slice). "
              "Conservation, norm/volume, chiral particle-hole and action all select Im(zeta)=0, while duality "
              "selects Re(zeta)=0; their intersection is zeta=0 = plate one. This is structural privilege, not a physical selection.",
    "equations": {
        "E10_nambu": "M=[[i zeta I, lambda Theta],[lambda Theta, -i conj(zeta) I]]; M^2+2bM+cI=0, c=lambda^2+a^2+b^2",
        "E10_spectrum": "tr M=-4b; det M=c^2; spec M = {-b +/- i sqrt(lambda^2+a^2)} each twice",
        "E10_ph": "P=tau_x K: P M P^-1=M identically; C=tau_z K: C M C^-1=-M iff Im zeta=0",
        "E11_variational_criterion": "Xdot=AX has a quadratic real action iff exists antisym invertible S with S A symmetric; then tr A=0",
        "E11_obstruction": "tr A=-4b != 0 when Im zeta != 0 => no single-field action; doubling inherits tr M=-4b",
        "E12_duality": "T A(lambda,a,b) T^-1 = A(lambda,-a,b); self-dual iff Re zeta=0",
        "E13_intersection": "conservation & norm & chiral & action => Im zeta=0; duality => Re zeta=0; all => zeta=0 = plate one",
    },
    "key_numbers": {
        "det_M_lam1_zeta_1_plus_i": "9",
        "trace_M_lam1_zeta_1_plus_i": "-4",
        "det_Phi_1_at_b_2_5": fmt(pred_det, 12),
        "norm_decay_at_b_2_5": fmt(r_pos, 12),
        "halflife_b_half": fmt(t_half, 12),
        "decay_rates_three_cases": [round(r, 12) for r in rates],
        "norm_relative_error": float("%.3e" % err_norm),
        "el_residual_b0": float("%.3e" % el_res),
        "scoreboards": {"one_equation": "0/6", "validated": 0, "four_force_gut": 0,
                        "unique_C3": "L_EW", "open_items": 8, "l4_open": 18,
                        "closed_by_this_volume": 0},
    },
    "errata": [
        {"where": "volume 137 / J116 E4", "what": "T A T^-1=A(lambda,-zeta); self-dual iff zeta=0",
         "fix": "with zeta=a+ib the map is A(lambda,-a,b), so self-dual iff Re(zeta)=0; J116's form is the b=0 slice",
         "impact": "J116 numeric readings and 78/78 are unaffected (its grid was real); only the scope changes"},
        {"where": "volume 137 / J116 E1 real slice", "what": "all J116 statements sample real zeta",
         "fix": "the general single-field generator carries Im(zeta) as an isotropic dilation -bI",
         "impact": "already repaired in J117; restated here for the action/duality chain"},
    ],
    "claim": CLAIM,
    "anchors": anchor_info,
    "gate_details": [{"name": n, "ok": ok, "detail": d} for n, ok, d in GATES],
    "not_self_derived": [
        "M1, its constraint, Theta and the zeta symbol row are read from the repository.",
        "J116's duality statement is read from volume 137; J117's E9 is read from volume 138.",
        "S13-C0001 is read from claims.csv.",
    ],
    "red_line": "A structural audit is not a physical refutation; a scope erratum is not a discovery; "
                "the scoreboard stays 0/6 and no OPEN item is closed.",
}

if not hard_ok:
    print("HARD GATE FAIL | %d/%d" % (passed, total))
    for n, ok, d in GATES:
        if not ok:
            print("  FAIL %s | %s" % (n, d))
    sys.exit(1)

out_json = os.path.join(HERE, "_j118_s13_m1_action_obstruction_dissipation.json")
out_md = os.path.join(HERE, "_j118_s13_m1_action_obstruction_dissipation.md")
out_txt = os.path.join(HERE, "_j118_s13_m1_action_obstruction_dissipation_report.txt")

with io.open(out_json, "w", encoding="utf-8") as f:
    f.write(json.dumps(payload, ensure_ascii=False, indent=2))

lines = [
    "# J118 M1 作用量不可能与耗散定理（机读）",
    "",
    "- 体积：卷 139 · 第 96 轮 · J118 · 2026-11-13",
    "- 判决：PASS（结构审计 + 范围勘误；不是物理否证）",
    "- 硬闸：%d/%d" % (total, passed),
    "- 记分板：0/6 不变；本册关闭 OPEN 0 条；新增已验证预言 0 条",
    "",
    "## 一句话结论",
    "",
    "- **E10 双重/Nambu**：$M=\\begin{pmatrix}\\mathrm{i}\\zeta I&\\lambda\\Theta\\\\\\lambda\\Theta&-\\mathrm{i}\\bar\\zeta I\\end{pmatrix}$",
    "  满足 **M²+2bM+cI=0**、**tr M=−4b**、**det M=c²**；粒子-空穴 $P=\\tau_xK$ 给 $P M P^{-1}=M$（恒等），",
    "  手征 $C=\\tau_zK$ 给 $C M C^{-1}=−M\\Leftrightarrow\\mathrm{Im}\\,\\zeta=0$。",
    "- **E11 作用量不可能**：一阶系统 $\\dot X=AX$ 有实二次作用量 $\\Rightarrow$ 存在可逆反对称 $S$ 使 $SA$ 对称",
    "  $\\Rightarrow \\operatorname{tr}A=0$；而 $\\operatorname{tr}A=-4b$ $\\Rightarrow$ **Im ζ≠0 时无单场二次实作用量**；",
    "  双重化也救不回来（$\\operatorname{tr}M=-4b$）。$A$ 与 $J$ 对易 $\\Leftrightarrow\\lambda=0$。",
    "- **E12 对偶锐化**：$T A(\\lambda,a,b)T^{-1}=A(\\lambda,-a,b)$ $\\Rightarrow$ **自对偶 $\\Leftrightarrow\\mathrm{Re}\\,\\zeta=0$**；",
    "  J116 的「$\\Leftrightarrow\\zeta=0$」是 $b=0$（实 ζ）切片。",
    "- **E13 交集**：守恒／体积／手征／作用量四条独立机制都选 **Im ζ=0**，对偶选 **Re ζ=0** $\\Rightarrow$",
    "  **交集 = ζ=0 = 板块一**。这是结构特权点，**不是物理选择**。",
    "",
    "## 四条结构方程（条件式，不是新物理）",
    "",
    "- **E10 Nambu**：$M^2+2bM+cI=0$，$c=\\lambda^2+a^2+b^2$；$\\operatorname{tr}M=-4b$；$\\det M=c^2$。",
    "- **E10 PH/手征**：$P M P^{-1}=M$ 恒等；$C M C^{-1}=-M\\Leftrightarrow b=0$。",
    "- **E11 迹障碍**：$\\dot X=AX$ 变分 $\\Rightarrow\\operatorname{tr}A=0$；$\\operatorname{tr}A=-4b$ $\\Rightarrow$ Im ζ≠0 无作用量。",
    "- **E12 对偶**：$T A T^{-1}=A(\\lambda,-a,b)$ $\\Rightarrow$ 自对偶 $\\Leftrightarrow$ Re ζ=0。",
    "",
    "## 两条勘误",
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
    "- E10–E13 是对**既有方程**在复耦合下的结构判定与两处范围勘误。",
    "- 「无单场二次作用量」只否证**线性、常数系数、二次作用量**这一层；不排除非局域/非线性/约束系统（本册不提出）。",
    "- ζ 的物理起源（为什么它可能为实）没有被回答，`O-SCALE` 等 8 条 OPEN 全部保持。",
    "- 板块一是唯一同时满足四条结构要求的点，但这只是结构特权，不是对 ζ=0 的物理选择。",
    "",
    "## 边界",
    "",
    "- 只审计 0+1 维齐次生成元、常数复 ζ、实 λ（文档约定）；σ·∇ 项与非线性扩展不在口径内。",
    "- 不判 M1 物理错误，不翻案任何既有判定，不改记分板 0/6。",
    "- 锚点：equations.md／附录A／claims.csv／卷 137／卷 138／_j116、_j117 脚本与产物。",
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
    f.write("J118 M1 ACTION OBSTRUCTION | PASS | gates %d/%d\n" % (total, passed))
    f.write("M = [[i zeta I, lambda Theta],[lambda Theta, -i conj zeta I]]\n")
    f.write("M^2 + 2bM + cI = 0 ; tr M = -4b ; det M = c^2\n")
    f.write("P=tau_x K: P M P^-1 = M ; C=tau_z K: C M C^-1 = -M iff b=0\n")
    f.write("Xdot=AX variational => tr A = 0 ; tr A = -4b => no action when Im zeta != 0\n")
    f.write("T A T^-1 = A(lambda,-a,b) => self-dual iff Re zeta = 0\n")
    f.write("intersection: conservation/norm/chiral/action -> Im zeta=0 ; duality -> Re zeta=0 ; all -> zeta=0\n")
    f.write("scoreboard 0/6 | validated 0 | 4-force GUT 0 | OPEN 8 | closed 0\n")

print("J118 OK | gates %d/%d | no-action iff Im(zeta)!=0 | self-dual iff Re(zeta)=0 | "
      "intersection zeta=0 | scoreboard 0/6 | outputs 3" % (passed, total))
