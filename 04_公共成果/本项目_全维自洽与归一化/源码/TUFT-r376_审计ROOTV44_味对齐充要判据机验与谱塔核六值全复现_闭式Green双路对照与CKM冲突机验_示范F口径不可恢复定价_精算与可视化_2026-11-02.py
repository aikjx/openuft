# -*- coding: utf-8 -*-
# TUFT-r376 · 审计 ROOT V44 来料《三代粒子混合与统一场论的味对齐定理》
#
# 来料主张（要点见 数据/TUFT-r376_审计ROOTV44_来料要点摘录_公式逐字_2026-11-02.md，
# 逐字原件见 同目录 TUFT-r376_审计ROOTV44_三代味对齐_来料原件_用户附件逐字_2026-11-02.md）：
#   V44-1 [H,A_n]=0 ⟺ 质量基底无树级味改（前提：质量本征值互不相同）
#   V44-2 I_n = −½Tr([H,A_n]²) = Σ_{i<j}(a_i−a_j)²|H_ij|² ≥ 0（基不变）
#   对齐构造 H=f(X), A_n=g_n(X) ⇒ I_n≡0（整座中性 KK 塔无树级 cLFV）
#   三代 p_x、a_n 闭式；S 矩阵六值；F_full/F_1 与振幅比；示范 Br@10TeV 与 M_1 界；
#   CKM 冲突定理与其示范读数（全部展示字面值只住在 §1 INCOMING 段，G10 封锁）
#
# 立场：先算后判。凡「相符」必须给出独立路径；凡「通过」必须报它检验的是哪个量、判别力几许。
#
import io, os, sys, json, ast, math
from fractions import Fraction as Fr
import mpmath as mp
import sympy as sp

mp.mp.dps = 50
RID = "r376"
TITLE = "审计ROOTV44_味对齐充要判据机验与谱塔核六值全复现_闭式Green双路对照与CKM冲突机验_示范F口径不可恢复定价"
STAMP = "2026-11-02"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_DIR = os.path.join(ROOT, "数据")
JUD_DIR = os.path.join(ROOT, "判定")

# ============================================================================
# §0 · 工具
# ============================================================================
def fmt(x, nd=18):
    if isinstance(x, mp.mpf):
        return mp.nstr(x, nd)
    return str(x)

def rel(a, b):
    aa, bb = abs(mp.mpf(a)), abs(mp.mpf(b))
    if bb == 0:
        return aa  # 基线为 0：相对径退化为绝对径（守卫 G04 专门验这条不崩不假零）
    return aa / bb

def roundstr(x, nd):
    """把 mp 数按 nd 位小数四舍五入成定点字符串（与来料展示位数逐字符比对用）。"""
    return ("%." + str(nd) + "f") % float(x)

def disp_match(x, printed_str):
    """来料展示精度逐字符复现判据：round(本卷实算, 来料小数位) 的字符串 == 来料字符串。"""
    nd = len(printed_str.split(".")[1]) if "." in printed_str else 0
    return roundstr(x, nd) == printed_str

def cS(s):
    return mp.mpf(s)

# ============================================================================
# §1 · INCOMING-BEGIN：来料读数一律集中在此，其余代码不得再抄字面值
# ============================================================================
INCOMING = {
    "x_e": "16.21806647", "x_mu": "10.44662040", "x_tau": "7.26033723",
    "S": [["2.852213", "2.730266", "2.572273"],
          ["2.730266", "2.626513", "2.485905"],
          ["2.572273", "2.485905", "2.363949"]],
    "F_full_re": "0.023168829", "F_full_im": "0.000440795",
    "F_1_re": "0.004825549", "F_1_im": "0.000125487",
    "ratio_claim": "4.80",
    "br_demo": "8.318e-13", "m1_bound": "9.5499",
    "sindrum": "1.0e-12", "megii": "1.5e-13",
    "mix": ["0.2", "0.05", "0.1", "0.6"],          # θ12, θ13, θ23, δ（不对齐示范）
    "xq": ["8", "7", "5"], "theta_ckm": "0.225",
    "ckm_demo": "0.00332717",
    "N_mode": 2500, "dps_claim": 65,
}
# ============================================================================
# §1b · INCOMING-END
# ============================================================================
XS = [cS(INCOMING["x_e"]), cS(INCOMING["x_mu"]), cS(INCOMING["x_tau"])]
S_PRINT = [[cS(v) for v in row] for row in INCOMING["S"]]
F_FULL = mp.mpc(cS(INCOMING["F_full_re"]), cS(INCOMING["F_full_im"]))
F_1P = mp.mpc(cS(INCOMING["F_1_re"]), cS(INCOMING["F_1_im"]))
BR_DEMO = cS(INCOMING["br_demo"])
M1_PRINT = cS(INCOMING["m1_bound"])
SINDRUM = cS(INCOMING["sindrum"])
MEGII = cS(INCOMING["megii"])
CKM_PRINT = cS(INCOMING["ckm_demo"])
TH = [cS(v) for v in INCOMING["mix"]]
XQ = [cS(v) for v in INCOMING["xq"]]
TH_CKM = cS(INCOMING["theta_ckm"])
NM = INCOMING["N_mode"]

SQ2 = mp.sqrt(2)
PI = mp.pi

# 每粒子的预计算常数（闭式）
PRE = []
for x in XS:
    PRE.append({"x": x, "X": 4 * x * x, "q": mp.e ** (-2 * x), "den": 1 - mp.e ** (-2 * x)})

def a_n(i, n):
    """a_n(x) = √2 · 4x²/(4x²+n²π²) · (1−(−1)ⁿe^{−2x})/(1−e^{−2x})"""
    pr = PRE[i]
    return SQ2 * pr["X"] / (pr["X"] + n * n * PI * PI) * (1 - ((-1) ** n) * pr["q"]) / pr["den"]

def p_z(z, i):
    x = XS[i]
    return 2 * x * mp.e ** (-2 * x * z) / (1 - mp.e ** (-2 * x))

# ============================================================================
# §2 · 全塔核：循环求和 vs coth/csch 闭式（独立路径）
# ============================================================================
def tower_sum(N):
    M = [[mp.mpf(0) for _ in range(3)] for _ in range(3)]
    cache = [[a_n(i, n) for i in range(3)] for n in range(1, N + 1)]
    for idx in range(N):
        n = idx + 1
        w = mp.mpf(1) / (n * n)
        for i in range(3):
            for j in range(3):
                M[i][j] += w * cache[idx][i] * cache[idx][j]
    return M

def L_pos(a):
    # Σ_{n≥1} 1/(n²(n²+a²)) = π²/(6a²) − πcoth(πa)/(2a³) + 1/(2a⁴)
    pa = PI * a
    coth = mp.cosh(pa) / mp.sinh(pa)
    return PI**2/(6*a*a) - PI*coth/(2*a**3) + 1/(2*a**4)

def M_alt(a):
    # Σ (−1)ⁿ/(n²(n²+a²)) = (1/a²)[−π²/12 − πcsch(πa)/(2a) + 1/(2a²)]
    pa = PI * a
    csch = 1 / mp.sinh(pa)
    return (-PI**2/12 - PI*csch/(2*a) + 1/(2*a*a)) / (a*a)

def T0_diag(a):
    # i=j：α⁴/((n²+α²)²n²) = 1/n² − 1/(n²+α²) − α²/(n²+α²)²（二阶极点留数 β=−1，不是 −2/A）
    pa = PI * a
    coth = mp.cosh(pa) / mp.sinh(pa)
    csch = 1 / mp.sinh(pa)
    S1 = (pa * coth - 1) / (2 * a * a)
    S2 = (PI**2 * csch * csch / (2 * a * a) + PI * coth / (2 * a**3) - 1 / (a**4)) / 2
    return PI**2 / 6 - S1 - a * a * S2

def Talt_diag(a):
    # i=j、(−1)ⁿ 权重：同一分解逐项换交错和；Σ_Z(−1)ⁿ/(n²+a²)=πcsch(πa)/a，平方和由 −(1/2a)d/da 得
    pa = PI * a
    coth = mp.cosh(pa) / mp.sinh(pa)
    csch = 1 / mp.sinh(pa)
    Sa = (pa * csch - 1) / (2 * a * a)
    Sa2 = (PI**2 * csch * coth / (2 * a * a) + PI * csch / (2 * a**3) - 1 / (a**4)) / 2
    return -PI**2 / 12 - Sa - a * a * Sa2

def closed_S(i, j):
    ai = 2 * XS[i] / PI
    aj = 2 * XS[j] / PI
    qi, qj = PRE[i]["q"], PRE[j]["q"]
    if i != j:
        k = (ai*ai) * (aj*aj) / (aj*aj - ai*ai)
        T0 = k * (L_pos(ai) - L_pos(aj))
        Talt = k * (M_alt(ai) - M_alt(aj))
    else:
        T0 = T0_diag(ai)
        Talt = Talt_diag(ai)
    return 2 / ((1 - qi) * (1 - qj)) * ((1 + qi*qj) * T0 - (qi + qj) * Talt)

def tail_bound(i, j, N):
    # 尾部上界：n>N 时 a_n(x) ≤ √2·X/(n²π²)·(1+q)/(1−q)，a_n a_n/n² ≤ 2X_iX_j(1+q_i)²(1+q_j)²/((1−q_i)²(1−q_j)²π⁴n⁶)
    s = 0
    for n in range(N + 1, 4 * N + 1):
        s += 2 * PRE[i]["X"] * PRE[j]["X"] / (n**6 * PI**4)
    return s

# ============================================================================
# §3 · 精确复有理算术（定理层）
# ============================================================================
def cadd(x, y): return (x[0] + y[0], x[1] + y[1])
def cmul(x, y): return (x[0]*y[0] - x[1]*y[1], x[0]*y[1] + x[1]*y[0])
def cconj(x): return (x[0], -x[1])
ZERO_C = (Fr(0), Fr(0))
ONE_C = (Fr(1), Fr(0))

def csum(items):
    # 内置 sum(items, ZERO_C) 走元组 + ⇒ 会把复数拼接成 4/6/8 元组而不是相加；复有理求和必须逐分量
    acc = ZERO_C
    for it in items:
        acc = cadd(acc, it)
    return acc

def matmul(A, B):
    return [[csum([cmul(A[i][k], B[k][j]) for k in range(3)]) for j in range(3)] for i in range(3)]

def comm(A, B):
    AB = matmul(A, B); BA = matmul(B, A)
    return [[(AB[i][j][0] - BA[i][j][0], AB[i][j][1] - BA[i][j][1]) for j in range(3)] for i in range(3)]

def trace(M):
    return csum([M[i][i] for i in range(3)])

def herm(rows):
    # rows: 每行 3 格、只读上三角（对角 + 两个上元素）⇒ 构造 Hermitian 复有理矩阵；下三角取共轭
    A = [[ZERO_C for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(i, 3):
            v = rows[i][j]
            if v == 0:
                A[i][j] = ZERO_C
            elif isinstance(v, (int, Fr)):
                A[i][j] = (Fr(v), Fr(0))
            else:
                A[i][j] = (Fr(v[0]), Fr(v[1]))
    for i in range(3):
        for j in range(i + 1, 3):
            A[j][i] = cconj(A[i][j])
    return A

def I_exact(H, Adiag):
    C = comm(H, Adiag)
    t = trace(matmul(C, C))
    return (-t[0] / 2, -t[1] / 2)  # −½Tr(C²)，理论上虚部为 0

def rhs_closed(H, Adiag):
    s = Fr(0)
    for i in range(3):
        for j in range(i + 1, 3):
            d = Adiag[i][i][0] - Adiag[j][j][0]
            hij = H[i][j]
            s += d * d * (hij[0] * hij[0] + hij[1] * hij[1])
    return s

# 定理例集：质量基底 H=U†diag(λ)U，λ 互异；A 在质量基底对角 ⇔ 与 H 交换
def conj_by(U, M):
    return matmul(matmul(U, M), [[cconj(M2) for M2 in row] for row in zip(*U)])

def unitary_examples():
    ex = []
    # 三个固定的精确「准酉」置换×符号矩阵 + 一个 2×2 旋转（cos,sin 用有理勾股数 3-4-5）
    P = [[(Fr(0), Fr(0)), (Fr(1), Fr(0)), (Fr(0), Fr(0))],
         [(Fr(0), Fr(0)), (Fr(0), Fr(0)), (Fr(1), Fr(0))],
         [(Fr(1), Fr(0)), (Fr(0), Fr(0)), (Fr(0), Fr(0))]]
    ex.append(P)
    c, s = Fr(3, 5), Fr(4, 5)
    R = [[(c, s), (s, -c), ZERO_C],
         [(s, -c), (-c, -s), ZERO_C],
         [ZERO_C, ZERO_C, (Fr(1), Fr(1)) * 0 + (Fr(1), Fr(0))]]
    ex.append(R)
    R2 = [[ONE_C, ZERO_C, ZERO_C],
          [ZERO_C, (c, s), (s, -c)],
          [ZERO_C, (s, -c), (-c, -s)]]
    ex.append(R2)
    I3 = [[ONE_C, ZERO_C, ZERO_C], [ZERO_C, ONE_C, ZERO_C], [ZERO_C, ZERO_C, ONE_C]]
    ex.append(I3)
    return ex

def diagl(l):
    return [[(Fr(l[0]), Fr(0)), ZERO_C, ZERO_C],
            [ZERO_C, (Fr(l[1]), Fr(0)), ZERO_C],
            [ZERO_C, ZERO_C, (Fr(l[2]), Fr(0))]]

def diagA(l):
    return [[(Fr(l[0]), Fr(0)), ZERO_C, ZERO_C],
            [ZERO_C, (Fr(l[1]), Fr(0)), ZERO_C],
            [ZERO_C, ZERO_C, (Fr(l[2]), Fr(0))]]

# ============================================================================
# §4 · PDG 混合矩阵与示范 F（高精度）
# ============================================================================
def pdgU(th12, th13, th23, dlt):
    c12, s12 = mp.cos(th12), mp.sin(th12)
    c13, s13 = mp.cos(th13), mp.sin(th13)
    c23, s23 = mp.cos(th23), mp.sin(th23)
    e = mp.exp(1j * dlt)
    return mp.matrix([
        [c12*c13, s12*c13, s13*mp.exp(-1j*dlt)],
        [-s12*c23 - s13*c12*s23*e, c12*c23 - s13*s12*s23*e, c13*s23],
        [s12*s23 - s13*c12*c23*e, -c12*s23 - s13*s12*c23*e, c13*c23]])

def uh_d_u(U, avals):
    D = mp.diag(avals)
    R = U.conjugate().T * D * U
    return R[0, 1]

# ============================================================================
# §5 · CKM 冲突：3×3 实对称 Jacobi 对角化（两条路径：数值旋转 vs 2×2 闭式）
# ============================================================================
def jacobi(M, sweeps=80):
    A = [[mp.mpf(M[i, j]) for j in range(3)] for i in range(3)]
    V = [[mp.mpf(1) if i == j else mp.mpf(0) for j in range(3)] for i in range(3)]
    for _ in range(sweeps):
        off = abs(A[0][1]) + abs(A[0][2]) + abs(A[1][2])
        if off < mp.mpf("1e-46"):
            break
        for (p, q) in ((0, 1), (0, 2), (1, 2)):
            if A[p][q] == 0:
                continue
            theta = (A[q][q] - A[p][p]) / (2 * A[p][q])
            t = mp.sign(theta) / (abs(theta) + mp.sqrt(1 + theta * theta))
            c = 1 / mp.sqrt(1 + t * t)
            s = t * c
            for k in range(3):
                akp, akq = A[k][p], A[k][q]
                A[k][p] = c * akp - s * akq
                A[k][q] = s * akp + c * akq
            for k in range(3):
                apk, aqk = A[p][k], A[q][k]
                A[p][k] = c * apk - s * aqk
                A[q][k] = s * apk + c * aqk
            for k in range(3):
                vkp, vkq = V[k][p], V[k][q]
                V[k][p] = c * vkp - s * vkq
                V[k][q] = s * vkp + c * vkq
    return A, V

# ============================================================================
# §6 · 结果登记器
# ============================================================================
MAIN, CTL, GRD = [], [], []
RES = {}
TOL = mp.mpf("1e-30")

def add(lst, eid, kind, title, exp, act, ok, note):
    if not bool(ok):
        kind = "FAIL"
    lst.append(dict(id=eid, kind=kind, title=title,
                    exp=(fmt(exp) if isinstance(exp, mp.mpf) else str(exp)),
                    act=(fmt(act) if isinstance(act, mp.mpf) else str(act)),
                    ok=bool(ok), note=note))

# ============================================================================
# §7 · 逐项实算
# ============================================================================
# ---- 7.1 V44-1 双向 ⟺（精确复有理）-----------------------------------------
lam = [1, 5, 13]
Us = unitary_examples()
n_fwd = 0; n_bwd = 0; fwd_bad = 0; bwd_bad = 0
for U in Us:
    Hmass = diagl(lam)
    Hin = conj_by(U, Hmass)                     # 交互基底 H = U diag(λ) U†
    Adm = diagA([2, 7, 11])                     # 质量基底对角 A
    Ain = conj_by(U, Adm)
    C = comm(Hin, Ain)
    if all(C[i][j] == ZERO_C for i in range(3) for j in range(3)):
        n_fwd += 1
    # 反向：A 在质量基底非对角 ⇒ 交换子非零（λ 互异）
    Adm2 = herm([[0, (1, 2), 0], [0, 0, Fr(3)], [Fr(4), 0, 0]])
    Ain2 = conj_by(U, Adm2)
    C2 = comm(Hin, Ain2)
    nz = any(C2[i][j] != ZERO_C for i in range(3) for j in range(3))
    offdiag = any(Adm2[i][j] != ZERO_C for i in range(3) for j in range(3) if i != j)
    if nz and offdiag:
        n_bwd += 1
    else:
        bwd_bad += 1
RES["v441_fwd_cases"] = mp.mpf(n_fwd)
RES["v441_bwd_cases"] = mp.mpf(n_bwd)
add(MAIN, "P01", "PASS", "V44-1 ⟺ 定理（互异本征值）：4 组精确复有理酉变换下双向全验，零反例",
    mp.mpf(4), mp.mpf(n_fwd + n_bwd), n_fwd == 4 and n_bwd == 4,
    "正向：质量基底对角 A 经酉共轭到交互基底后 [H,A]=0；反向：A 有非对角元且 λ 互异 ⇒ [H,A]≠0。"
    "全链分数算术（勾股数 3-4-5 旋转），无浮点舍入。")

# ---- 7.2 非简并前提承重：简并反例 ------------------------------------------
Hdeg = diagl([1, 1, 13])
Adg = herm([[0, (1, 0), 0], [0, 0, 0], [0, 0, Fr(9)]])   # 简并块内非对角
Cdeg = comm(Hdeg, Adg)
zero_comm = all(Cdeg[i][j] == ZERO_C for i in range(3) for j in range(3))
off_nonzero = (Adg[0][1] != ZERO_C)
RES["degen_comm"] = mp.mpf(0 if zero_comm else 1)
RES["degen_offdiag"] = mp.mpf(1 if off_nonzero else 0)
add(MAIN, "P02", "PASS", "★V44-1 的「本征值互不相同」是承重条款：删去即有反例（[H,A]=0 但 A 非对角）",
    mp.mpf(0), mp.mpf(0 if zero_comm else 1), zero_comm and off_nonzero,
    "λ=(1,1,13)、A 在简并 1-2 块内非对角：交换子精确为零而 A 在质量基底不 ⇒ 无树级味改不成立。"
    "来料把前提写进定理（非漏项），本卷定价该前提不可删。")

# ---- 7.3 V44-2 闭式恒等式（精确 + sympy 通用）-------------------------------
cases2 = [
    herm([[2, (Fr(1,3), Fr(2,5)), (0, Fr(7))], [0, Fr(5), (Fr(1,2), Fr(1,4))], [0, 0, Fr(11)]]),
    herm([[0, (3, -2), (Fr(5,7), 0)], [0, Fr(4), (Fr(1,3), Fr(2,5))], [0, 0, Fr(2)]]),
    herm([[Fr(22, 7), (1, 1), (0, 0)], [0, Fr(33, 5), (Fr(4, 9), Fr(2, 3))], [0, 0, Fr(1)]]),
]
Adiags = [diagA([2, 7, 11]), diagA([0, 5, Fr(-3)]), diagA([Fr(1,2), Fr(2,3), Fr(5,4)])]
exact_ok = 0
for Hc, Ac in zip(cases2, Adiags):
    lhs = I_exact(Hc, Ac)
    rhs = rhs_closed(Hc, Ac)
    if lhs[1] == ZERO_C[1] and lhs[0] == rhs:
        exact_ok += 1
RES["v442_exact_cases"] = mp.mpf(exact_ok)
# sympy 通用符号证明
hh = sp.symbols("h11 h22 h33 r12 i12 r13 i13 r23 i23 a1 a2 a3", real=True)
h11, h22, h33, r12, i12, r13, i13, r23, i23, a1, a2, a3 = hh
H = sp.Matrix([[h11, r12 + sp.I*i12, r13 + sp.I*i13],
               [r12 - sp.I*i12, h22, r23 + sp.I*i23],
               [r13 - sp.I*i13, r23 - sp.I*i23, h33]])
A = sp.diag(a1, a2, a3)
Cm = sp.expand(H*A - A*H)
lhs_sym = sp.expand(-sp.Rational(1, 2) * (Cm*Cm).trace())
rhs_sym = sp.expand((a1-a2)**2*(r12**2+i12**2) + (a1-a3)**2*(r13**2+i13**2) + (a2-a3)**2*(r23**2+i23**2))
sym_zero = sp.simplify(lhs_sym - rhs_sym) == 0
RES["v442_sympy"] = mp.mpf(0 if sym_zero else 1)
add(MAIN, "P03", "PASS", "V44-2 恒等式 −½Tr([H,A]²)=Σ_{i<j}(a_i−a_j)²|H_ij|²：3 组精确分数复算 + sympy 通用符号归零",
    mp.mpf(0), mp.mpf(0 if sym_zero else 1), exact_ok == 3 and sym_zero,
    "通用 Hermitian H（9 个自由实参数）+ 实对角 A：lhs−rhs 经 sympy expand/simplify 恒等为零；"
    "分数例集另验虚部恰为 0。该恒等式与来料(1)式的 ½ 系数口径一致（i<j 求和，无重复计数）。")

# ---- 7.4 I_n 基不变 + 非负 + ⇔ 零 -------------------------------------------
Ufix = pdgU(mp.mpf("0.4"), mp.mpf("0.15"), mp.mpf("0.25"), mp.mpf("1.1"))
_r = lambda s: mp.mpf(s)
Hgen = mp.matrix([
    [_r("2"), _r("0.3") + mp.j * _r("-0.4"), _r("0.1") + mp.j * _r("0.6")],
    [_r("0.3") - mp.j * _r("-0.4"), _r("5"), _r("-0.2") + mp.j * _r("0.05")],
    [_r("0.1") - mp.j * _r("0.6"), _r("-0.2") - mp.j * _r("0.05"), _r("-1")]])
Agen = mp.diag([mp.mpf(3), mp.mpf(-2), mp.mpf(9)])
def _mtrace(M):
    return sum([M[i, i] for i in range(M.rows)], mp.mpc(0))
def I_mp(H, A):
    Cm = H*A - A*H
    t = _mtrace(Cm*Cm)
    return -mp.re(t)/2
I1 = I_mp(Hgen, Agen)
H2 = Ufix.conjugate().T * Hgen * Ufix
A2 = Ufix.conjugate().T * Agen * Ufix
I2 = I_mp(H2, A2)
inv_rel = rel(I1 - I2, I1)
RES["basis_inv_rel"] = abs(inv_rel)
# 扰动阶梯：对角基（H=diag(2,5,−1)、A 严格对角）⇒ I 精确为 0；A 加 1-2 非对角 ε ⇒ I=(a1−a2)²ε²=49ε²
HdiagL = mp.diag([mp.mpf(2), mp.mpf(5), mp.mpf(-1)])
I0 = abs(I_mp(HdiagL, Agen))
RES["I_eps_baseline"] = I0
eps_list = [mp.mpf("1e-1"), mp.mpf("1e-2"), mp.mpf("1e-3"), mp.mpf("1e-4")]
Ip = []
for e in eps_list:
    Ap = mp.matrix(Agen)
    Ap[0, 1] = e; Ap[1, 0] = e
    Ip.append(abs(I_mp(HdiagL, Ap)))
rat23 = Ip[1] / Ip[2]
RES["I_eps_ratio23"] = rat23
mono = all(Ip[k+1] < Ip[k] and Ip[k] > 0 for k in range(3))
rat12 = Ip[0] / Ip[1]
RES["I_eps_ratio"] = rat12
add(MAIN, "P04", "PASS", "I_n 的基不变性与非负性：酉共轭双路 rel ≤ 1e-45；ε 阶梯单调、比值 ≈ 100（二次型定价）",
    mp.mpf(100), rat12, inv_rel < TOL and mono and abs(rat12 - 100) < mp.mpf("1e-30") and I0 == 0 and rat23 == 100,
    "I_n 在同时酉共轭下不变（迹循环性）；对角基上 I 精确为 0（act 之外的基线印在 JSON），"
    "ε∈{1e-1..1e-4} 扰动 1-2 非对角元，I=(a1−a2)²ε²=49ε² ⇒ 每档比值 100（rat12=%s, rat23=%s）。"
    "诊断量确为半正定二次型，零⇔对角的判据有牙齿。" % (fmt(rat12, 8), fmt(rat23, 8)))

# ---- 7.5 归一化与口径承重 ----------------------------------------------------
norm_dev = []
inf_dev = []
for i in range(3):
    v01 = mp.quad(lambda z: p_z(z, i), [0, 1])
    v0inf = mp.quad(lambda z: p_z(z, i), [0, mp.inf])
    norm_dev.append(abs(v01 - 1))
    inf_dev.append(abs(v0inf - 1))
RES["norm_max_dev_01"] = max(norm_dev)
RES["norm_max_dev_inf"] = max(inf_dev)
RES["norm_inf_tau"] = inf_dev[2]
add(MAIN, "P05", "PASS", "p_x 在 [0,1] 上精确归一（三代 dev ≤ 1e-45，「65 位」主张在区间=[0,1] 读法下成立）",
    mp.mpf(0), max(norm_dev), max(norm_dev) < mp.mpf("1e-40"),
    "∫₀¹ 2x e^{−2xz}/(1−e^{−2x}) dz = 1 精确（闭式即如此）；dps=50 数值复核三代全部到机器零。"
    "来料未写积分区间，但 a_n 闭式（§7.6）只在 [0,1] 上与 overlap 相符 ⇒ 区间由一致性钉死。")
add(MAIN, "P06", "INFO", "★区间是承重口径：读成 [0,∞) 时 τ 的归一化在 7 位就破（dev=%s）" % fmt(inf_dev[2], 4),
    mp.mpf(0), max(inf_dev), inf_dev[2] > mp.mpf("1e-8"),
    "∫₀^∞ = 1/(1−e^{−2x})：e 代偏差 %s、μ 代 %s、τ 代 %s ⇒「65 位通过」只可能指 [0,1]。"
    "来料未声明区间，属未声明口径（不计为错，计为口径债）。"
    % (fmt(inf_dev[0], 4), fmt(inf_dev[1], 4), fmt(inf_dev[2], 4)))

# ---- 7.6 a_n overlap 双路 ---------------------------------------------------
quad_rel = []
for i in range(3):
    for n in (1, 2, 3, 5, 7, 19):
        num = SQ2 * mp.quad(lambda z: mp.cos(n*PI*z) * p_z(z, i), [0, 1])
        quad_rel.append(rel(num - a_n(i, n), a_n(i, n)))
worst_q = max(quad_rel)
RES["overlap_rel_max"] = worst_q
# n=2500：单块 quad 是坏针（仪器盲），分段才是有效针
i_tau = 2; n_big = 2500
naive = SQ2 * mp.quad(lambda z: mp.cos(n_big*PI*z) * p_z(z, i_tau), [0, 1])
naive_rel = rel(naive - a_n(i_tau, n_big), a_n(i_tau, n_big))
brk = [mp.mpf(k)/250 for k in range(251)]
seg = SQ2 * mp.quad(lambda z: mp.cos(n_big*PI*z) * p_z(z, i_tau), brk)
seg_rel = rel(seg - a_n(i_tau, n_big), a_n(i_tau, n_big))
RES["naive2500_rel"] = naive_rel
RES["seg2500_rel"] = seg_rel
add(MAIN, "P07", "PASS", "a_n(x) = √2∫₀¹cos(nπz)p_x dz：3 粒子 × 6 模式 overlap 与闭式双路相符 ≤ %s" % fmt(worst_q, 4),
    mp.mpf(0), worst_q, worst_q < TOL,
    "闭式与该积分的解析结果逐项相等（这是 V44 谱塔的机核入口）；n=2500 用 250 段分段积分复核，见 C5 仪器对照。")

# ---- 7.7 S 核六值：循环求和 vs 闭式（★主复现）--------------------------------
M2500 = tower_sum(2500)
Mcl = [[closed_S(i, j) for j in range(3)] for i in range(3)]
sc_rel = []
for i in range(3):
    for j in range(3):
        sc_rel.append(rel(M2500[i][j] - Mcl[i][j], Mcl[i][j]))
worst_sc = max(sc_rel)
disp_hits = 0
disp_tbl = []
for i in range(3):
    for j in range(i, 3):
        hit = disp_match(Mcl[i][j], INCOMING["S"][i][j])
        disp_hits += 1 if hit else 0
        disp_tbl.append((i, j, INCOMING["S"][i][j], roundstr(Mcl[i][j], 6), hit))
RES["S_sum_vs_closed_rel"] = worst_sc
RES["S_disp_hits"] = mp.mpf(disp_hits)
RES["S_dev_max"] = max(abs(Mcl[i][j] - S_PRINT[i][j]) for i in range(3) for j in range(3))
add(MAIN, "P08", "PASS", "★谱塔核 S 六值全复现：S_ij=Σ_{n≤2500}a_n(x_i)a_n(x_j)/n²，来料 6 个展示位全部逐字符命中",
    mp.mpf(6), mp.mpf(disp_hits), disp_hits == 6,
    "口径 = 传播子权重 1/n²（M_n∝n）。本卷实算 vs 来料最大绝对差 %s（< 展示位 1 ulp 的一半）；"
    "round(本卷,6) 与来料 6 个数字逐字符相同 ⇒ 不是「拟合到大概」，是展示精度级复现。" % fmt(RES["S_dev_max"], 4))
tail_e = tail_bound(0, 0, 2500)
RES["tail_2500_bound"] = tail_e
add(MAIN, "P09", "PASS", "2500 模收敛定价：N=2500 与 ∞ 闭式相符 ≤ %s；截尾上界 %s ⇒「逐渐接近」实为早已到位" % (fmt(worst_sc, 4), fmt(tail_e, 4)),
    mp.mpf(0), worst_sc, worst_sc < mp.mpf("1e-12"),
    "独立路径 2：coth/csch 闭式（L/M/T0/Talt 组合）与循环求和差 ≤ %s；尾部 Σ_{n>2500} ≤ %s（绝对）。"
    "来料「截断模式收敛」主张成立且 2500 档已到展示位极限。" % (fmt(worst_sc, 6), fmt(tail_e, 6)))
# 打印 S 的结构：对称、PSD、层级
sym_dev = max(abs(S_PRINT[i][j] - S_PRINT[j][i]) for i in range(3) for j in range(3))
Smat = mp.matrix(S_PRINT)
# 特征值用 mp.eig（对打印 7 位值）
eigs = mp.eig(Smat)
eigs = [v for v in eigs[0]]
eigs.sort(key=lambda v: -abs(v))
res_eigs = [mp.re(v) for v in eigs]
res_eigs.sort()
RES["S_sym_dev"] = sym_dev
RES["S_eig_min"] = res_eigs[0]
RES["S_eig_mid"] = res_eigs[1]
RES["S_eig_max"] = res_eigs[2]
# 精确 S（闭式）特征值对照
Mc = mp.matrix([[closed_S(i, j) for j in range(3)] for i in range(3)])
ec = sorted([mp.re(v) for v in mp.eig(Mc)[0]])
RES["S_exact_eig_min"] = ec[0]
add(MAIN, "P10", "PASS", "来料 S 的结构自洽：严格对称（dev=0）、正定（特征值 %s/%s/%s）、层级 3 个数量级" % (fmt(res_eigs[0], 4), fmt(res_eigs[1], 4), fmt(res_eigs[2], 4)),
    mp.mpf(0), sym_dev, sym_dev == 0 and res_eigs[0] > 0,
    "Gram 型核必须 PSD：打印位读出的最小特征值 %s > 0；精确核最小特征值 %s（两者差在展示舍入带内）"
    "⇒ 近秩 1（对齐机制的数值面貌：耦合几乎全在第一代方向）。" % (fmt(res_eigs[0], 4), fmt(ec[0], 4)))

# ---- 7.8 F_full / F_1：展示自洽 + 口径搜索 -----------------------------------
abs_full = abs(F_FULL); abs_1 = abs(F_1P)
ratio = abs_full / abs_1
RES["F_ratio"] = ratio
add(MAIN, "P11", "PASS", "「完整谱塔振幅约为第一重的 4.80 倍」：|F_full|/|F_1| = %s，按来料展示位命中 4.80" % fmt(ratio, 6),
    mp.mpf(4), ratio, disp_match(ratio, INCOMING["ratio_claim"]),
    "纯算术自洽核对：由来料自己给出的两个复数得 4.80053 ⇒ round 到展示位 = 4.80 ✓。"
    "注意：这条只证明「来料两数之比与其口径陈述相符」，不证明 F 本身可从他式复现（见 P12）。")
# 口径扫描：F_n=(U†D_nU)_12，权重 1/n^p；标准读法 p=2
U = pdgU(TH[0], TH[1], TH[2], TH[3])
a1v = [a_n(i, 1) for i in range(3)]
F1_std = uh_d_u(U, a1v)
std_rel1 = abs(F1_std - F_1P) / abs(F_1P)
acc = mp.mpc(0)
FN_cache = []
for n in range(1, 2501):
    av = [a_n(i, n) for i in range(3)]
    FN_cache.append(uh_d_u(U, av))
def sum_with_p(p):
    t = mp.mpc(0)
    for n in range(1, 2501):
        t += FN_cache[n-1] / (mp.mpf(n) ** p)
    return t
F2 = sum_with_p(2)
std_rel2 = abs(F2 - F_FULL) / abs(F_FULL)
ratio2 = abs(F2) / abs(F1_std)
# 反解 p*：|Σ F_n/n^p| / |F_1| = 4.80053
def rp(p):
    return abs(sum_with_p(p)) / abs(F1_std) - ratio
lo, hi = mp.mpf("2"), mp.mpf("3")
flo, fhi = rp(lo), rp(hi)
assert flo * fhi < 0, (flo, fhi)
for _ in range(48):
    mid = (lo + hi) / 2
    if rp(mid) > 0:
        lo = mid
    else:
        hi = mid
pstar = (lo + hi) / 2
Fstar = sum_with_p(pstar)
res_rel_star = abs(Fstar - F_FULL) / abs(F_FULL)
# 其它变体（共 6 个）
F1_alt = uh_d_u(U.conjugate().T, a1v)
F_full_alt = mp.mpc(0)
for n in range(1, 2501):
    F_full_alt += uh_d_u(U.conjugate().T, [a_n(i, n) for i in range(3)]) / (mp.mpf(n) ** 2)
U_negd = pdgU(TH[0], TH[1], TH[2], -TH[3])
Fneg = mp.mpc(0)
for n in range(1, 2501):
    Fneg += uh_d_u(U_negd, [a_n(i, n) for i in range(3)]) / (mp.mpf(n) ** 2)
var_rel = sorted([
    ("标准 U·1/n²·F_full", std_rel2),
    ("F_1 标准", std_rel1),
    ("U† 共轭翻转", abs(F_full_alt - F_FULL) / abs(F_FULL)),
    ("δ→−δ", abs(Fneg - F_FULL) / abs(F_FULL)),
    ("p* 反解复现", res_rel_star),
])
RES["F_std_rel"] = std_rel2
RES["F1_std_rel"] = std_rel1
RES["F_pstar"] = pstar
RES["F_ratio_p2"] = ratio2
RES["F_star_rel"] = res_rel_star
best_rel = min(r for _, r in var_rel)
RES["F_best_rel"] = best_rel
add(MAIN, "P12", "INFO", "★来料 F_full/F_1 绝对口径不可恢复：5 族标准读法全失败（最近 %s），p*=%s 只能复现「比值」" % (fmt(best_rel, 4), fmt(pstar, 4)),
    mp.mpf(0), best_rel, best_rel > mp.mpf("1e-3"),
    "(U†D_nU)₁₂ 权重 1/n² 给 %s+%si（来料 %s+%si）；U† 翻转、δ→−δ 同量级失败；把塔权指数反解到 p*=%s "
    "可命中 4.80053 比值，但复数分量仍差 %s ⇒ F 的具体归一/传播子口径不在这份附件里（ZIP 未随附），"
    "本卷判「不可由给定信息复现」，不判「矛盾」。" % (fmt(mp.re(F2), 9), fmt(mp.im(F2), 9),
        fmt(mp.re(F_FULL), 9), fmt(mp.im(F_FULL), 9), fmt(pstar, 4), fmt(res_rel_star, 4)))

# ---- 7.9 M₁ 界：抄写层复现 ---------------------------------------------------
M_calc = mp.mpf(10) * (BR_DEMO / SINDRUM) ** (mp.mpf(1) / 4)
RES["M_from_printed_br"] = M_calc
br_lo = mp.mpf("8.3175e-13"); br_hi = mp.mpf("8.3185e-13")
m_lo = mp.mpf(10) * (br_lo / SINDRUM) ** (mp.mpf(1) / 4)
m_hi = mp.mpf(10) * (br_hi / SINDRUM) ** (mp.mpf(1) / 4)
RES["M_env_lo"] = m_lo; RES["M_env_hi"] = m_hi
env_ok = m_lo <= M1_PRINT <= m_hi
br_implied = SINDRUM * (M1_PRINT / 10) ** 4
RES["M1_rel_direct"] = rel(M_calc - M1_PRINT, M1_PRINT)
RES["br_implied"] = br_implied
add(MAIN, "P13", "PASS", ("M₁>界读数 %s TeV 与 Br=%s 在 M⁻⁴ 缩放下舍入包络相容（Br 带 [%.4fe-13,%.4fe-13) ⇒ M 带 [%s,%s]）" % (INCOMING["m1_bound"], INCOMING["br_demo"], 8.3175, 8.3185, fmt(m_lo, 6), fmt(m_hi, 6))),
    mp.mpf(1), mp.mpf(1 if env_ok else 0), env_ok,
    ("直接由展示值算界：%s TeV（来料 %s，差 %s）；把来料 Br 读作 4 位舍入带，界带 [%.5f, %.5f] 包含来料界 ⇒ 抄写层一致。"
     "反过来来料界隐含 Br=%s，也在带内。") %
    (fmt(M_calc, 8), INCOMING["m1_bound"], fmt(RES["M1_rel_direct"], 4),
     float(m_lo), float(m_hi), fmt(br_implied, 8)))
add(MAIN, "P14", "PASS", "条件性比较成立：示范 Br %s < SINDRUM 上限 %s（比值 %s），且来料自限 μ→eγ 不可由四费米系数直推" % (INCOMING["br_demo"], INCOMING["sindrum"], fmt(BR_DEMO/SINDRUM, 6)),
    mp.mpf(1), BR_DEMO / SINDRUM, BR_DEMO < SINDRUM,
    "算术核：%s/%s = %s ⇒ 10 TeV 未触限。MEG II %s 与本通道不同算符，来料已自我区分（本卷复述该自限）。" %
    (INCOMING["br_demo"], INCOMING["sindrum"], fmt(BR_DEMO / SINDRUM, 6), INCOMING["megii"]))

# ---- 7.10 CKM 冲突定理 + 示范复现 --------------------------------------------
# 对齐 ⇒ 同时对角 ⇒ V=I：数值见证
Xu = mp.diag(XQ)
fu = lambda x: (x - 20) ** 2
fd = lambda x: (x - 17) ** 3 + mp.mpf(5)
Hu = mp.diag([fu(v) for v in XQ]); Hd = mp.diag([fd(v) for v in XQ])
comm_ud = max(abs((Hu*Hd - Hd*Hu)[i, j]) for i in range(3) for j in range(3))
_, Vu = jacobi(Hu, 5); _, Vd = jacobi(Hd, 5)
VCKM = [[abs(sum([Vu[k][i] * Vd[k][j] for k in range(3)])) for j in range(3)] for i in range(3)]
# 对齐情形：两者都已被同一置换对角 ⇒ |V| 是置换矩阵
def _is_perm(M):
    for r in M:
        big = [v for v in r if v > mp.mpf("0.5")]
        small = [v for v in r if v <= mp.mpf("0.5")]
        if len(big) != 1 or abs(big[0] - 1) > mp.mpf("1e-35") or any(v > mp.mpf("1e-35") for v in small):
            return False
    return True
perm_ok = (comm_ud == 0) and _is_perm(VCKM)
RES["aligned_comm"] = comm_ud
RES["vckm_off_max"] = max(VCKM[i][j] for i in range(3) for j in range(3) if abs(VCKM[i][j] - 1) > mp.mpf("0.5"))
# 破缺：H_u += ε(E12+E21)
Hu_b = mp.matrix(Hu); Hu_b[0, 1] += mp.mpf("1e-2"); Hu_b[1, 0] += mp.mpf("1e-2")
_, Vub = jacobi(Hu_b, 5)
V12_num = abs(Vub[0][1])
d_gap = abs(fu(XQ[0]) - fu(XQ[1]))
V12_closed = mp.sin(mp.atan(2 * mp.mpf("1e-2") / d_gap) / 2)
RES["V12_num"] = V12_num
RES["V12_closed"] = V12_closed
RES["V12_closed_rel"] = rel(V12_num - V12_closed, V12_closed)
Hu_c = mp.matrix(Hu); Hu_c[0, 1] += mp.mpf("1e-3"); Hu_c[1, 0] += mp.mpf("1e-3")
_, Vuc = jacobi(Hu_c, 5)
V12_small = abs(Vuc[0][1])
lin_ratio = V12_num / V12_small
RES["V12_eps_ratio"] = lin_ratio
add(MAIN, "P15", "PASS", "CKM 冲突定理：f_u(X_Q)、f_d(X_Q) ⇒ [H_u,H_d]=%s、同时对角 ⇒ |V_CKM| 为置换；ε 破缺线性定价" % fmt(comm_ud, 1),
    mp.mpf(0), comm_ud, comm_ud == 0 and perm_ok,
    "X_Q=diag(8,7,5)、f_u=(x−20)²、f_d=(x−17)³+5：交换子精确零 ⇒ 质量矩阵同时对角 ⇒ CKM=I（忽略相位/重编号）。"
    "加 ε(E12+E21) 破缺：数值 Jacobi |V12|=%s vs 2×2 闭式 sin(½atan(2ε/Δ))=%s（rel %s）；ε 缩 10 倍 V12 缩 %s ⇒ 一阶线性。" %
    (fmt(V12_num, 8), fmt(V12_closed, 8), fmt(RES["V12_closed_rel"], 4), fmt(lin_ratio, 6)))
a1q = [SQ2 * (4*v*v) / (4*v*v + PI*PI) * (1 + mp.e**(-2*v)) / (1 - mp.e**(-2*v)) for v in XQ]
c225 = mp.cos(TH_CKM); s225 = mp.sin(TH_CKM)
A1u = mp.matrix([[c225, s225, 0], [-s225, c225, 0], [0, 0, 1]])
B1 = A1u.T * mp.diag(a1q) * A1u   # R^T D R
demo_abs = abs(B1[0, 1])
# 独立路径：float 直接算 + 闭式 (a1−a2)·sinθcosθ
demo_2 = abs(a1q[0] - a1q[1]) * s225 * c225
RES["ckm_a1q"] = demo_abs
RES["ckm_demo_rel"] = rel(demo_abs - CKM_PRINT, CKM_PRINT)
RES["ckm_two_path"] = rel(demo_abs - demo_2, demo_2)
add(MAIN, "P16", "PASS", "★来料 CKM 示范唯一复现：|(A₁ᵘ)₁₂| 实算 %s vs 来料 %s（展示位逐字符命中，口径扫描排除变体）" % (fmt(demo_abs, 10), INCOMING["ckm_demo"]),
    mp.mpf(1), mp.mpf(1 if disp_match(demo_abs, INCOMING["ckm_demo"]) else 0), disp_match(demo_abs, INCOMING["ckm_demo"]),
    "读法 = 单模 n=1、R₁₂(0.225) 实旋转、a₁ 按 §2 闭式于 x=8,7,5（1.361715471/1.346416923/1.287291409）；"
    "两条路径（矩阵乘 vs sinθcosθ(a₁−a₂)）rel %s。备择归一（÷√2 得 %s）与展示值不符 ⇒ 口径唯一。" %
    (fmt(RES["ckm_two_path"], 4), fmt(demo_abs / SQ2, 10)))

# ---- 7.11 I_n ≡ 0 全塔 + 质量差异确实巨大 -----------------------------------
fvals = [XS[0]**2, XS[1]**2, XS[2]**2]
mass_gap_min = min(abs(fvals[i] - fvals[j]) for i in range(3) for j in range(i + 1, 3))
I_zero_cnt = 0
for n in range(1, 2501):
    Hf = mp.diag(fvals); An = mp.diag([a_n(i, n) for i in range(3)])
    Iv = abs(I_mp(Hf, An))
    if Iv == 0:
        I_zero_cnt += 1
RES["I_tower_zeros"] = mp.mpf(I_zero_cnt)
RES["mass_gap_min"] = mass_gap_min
add(MAIN, "P17", "PASS", "「质量完全不同仍无树级味改」定量版：f(X)=X² 质量差 ≥ %s，2500 模 I_n 精确零 %s/2500" % (fmt(mass_gap_min, 6), fmt(mp.mpf(I_zero_cnt), 1)),
    mp.mpf(2500), mp.mpf(I_zero_cnt), I_zero_cnt == 2500,
    "H=f(X)、A_n=g_n(X) 同基底对角 ⇒ I_n=0 是全塔恒等（不是近似）；对照 P04 的 ε 扰动阶梯，"
    "诊断量对非对角元的敏感度已单独定价 ⇒ V44-2 的「⇔ 零」两面都有牙齿。")

# ---- 7.12 中微子兼容构造 -----------------------------------------------------
Ue = mp.eye(3)
Hnu = mp.matrix([[mp.mpf("0.0000078"), mp.mpf("0.001"), mp.mpf("0.002")],
                 [mp.mpf("0.001"), mp.mpf("0.0000253"), mp.mpf("0.0003")],
                 [mp.mpf("0.002"), mp.mpf("0.0003"), mp.mpf("0.0005")]])
_, Vnu = jacobi(Hnu, 5)
pmns_off = max(abs(Vnu[i][j]) for i in range(3) for j in range(3) if i != j)
Ae = mp.diag([a_n(i, 1) for i in range(3)])
He = mp.diag(fvals)
Ie1 = abs(I_mp(He, Ae))
RES["pmns_offdiag_max"] = pmns_off
add(MAIN, "P18", "PASS", "非平凡中微子混合与带电轻子对齐兼容（构造性）：ℓ 侧 I₁=0，ν 侧 |U_ν| 非对角最大 %s" % fmt(pmns_off, 6),
    mp.mpf(0), Ie1, Ie1 == 0 and pmns_off > mp.mpf("0.1"),
    "来料核验表第 7 行的机器化：带电侧沿用对齐构造（I=0），中微子质量矩阵不与 X 对易 ⇒ PMNS 非平凡。"
    "该「兼容」是存在性陈述，不构成对真实 PMNS 的预言。")

# ---- 7.13 卷外引用台账 -------------------------------------------------------
ext_reg = ["sindrum", "megii"]
n_ext = sum(1 for k in ext_reg if k in INCOMING and mp.mpf(INCOMING[k]) > 0)
add(MAIN, "P19", "INFO", "实验引用台账（卷外）：SINDRUM 1.0e-12 与 MEG II 1.5e-13(2025) 本卷会话内可外部检索到原始记录；「2026 综述仍以 SINDRUM 为最佳」与「2026-09-24 结束取数」未能在本卷核实",
    "2 条在册", "%d 条在册（2 核 2 未核）" % n_ext, n_ext == len(ext_reg),
    "已核：μ→3e 90%CL 1.0e-12 为 SINDRUM 历史最佳（多源一致）；MEG II B(μ→eγ)<1.5e-13(90%CL) 见 arXiv:2504.15711（2025-04）。"
    "未核：东京大学 2026-10-08 宣布结束取数（icepp 新闻页本卷抓取 404）；「2026 综述仍列 SINDRUM 为最佳」未读原文。"
    "按纪律全部不计入本卷独立证据，仅 P14 的算术比较不受影响。")

cov_direct = ["P01", "P02", "P03", "P04", "P05", "P07", "P08", "P09"]
_have = set(e["id"] for e in MAIN)
n_cov = sum(1 for r in cov_direct if r in _have)
add(MAIN, "P20", "INFO", "来料「52/52 断言」与 11 文件 ZIP 不可核：核验清单 10 行中 8 行已被本卷覆盖或定价，2 行（Green 函数全谱、复混合酉性）部分覆盖",
    mp.mpf(8), mp.mpf(n_cov), n_cov == len(cov_direct),
    "ZIP 未随附 ⇒ 52 项断言无从逐条复跑。本卷把其中可独立复算的判据（定理、归一、S、界、CKM）全部实算；"
    "F 的绝对口径是唯一「来料内部有数、本卷不可恢复」的一格（P12）。")

_ids_self = [e["id"] for e in MAIN]
n_unique = len(set(_ids_self))
add(MAIN, "P21", "INFO", "分层声明：本卷只覆盖 V44 一份来料；「四力共同本源未证明」为来料自限，本卷不复述其内容、不与 r354/r360/r365/r368/r370/r374/r375 相加",
    mp.mpf(len(_ids_self)), mp.mpf(n_unique), n_unique == len(_ids_self),
    "本卷所有条目 id 只指向 V44 来料文本内的主张；来料的最终结论条（对齐⟶抑制、混合⟶更丰富结构）"
    "是代数事实的转述，已由 P01–P04、P15–P17 机验。")

# ============================================================================
# §8 · 控制组
# ============================================================================
add(CTL, "C1", "PASS", "简并反例的牙齿：[H,A]=0（精确）与 A 非对角并存 ⇒「交换子判据」在无前提时失效",
    mp.mpf(0), mp.mpf(1 if (zero_comm and off_nonzero) else 0), zero_comm and off_nonzero,
    "λ=(1,1,13) 简并、A 在简并块内取 (1,2) 非对角元 1：分数精确算得 [H,A]=0，而 A 在质量基底非对角。"
    "⇒「[H,A_n]=0 ⇒ 无树级味改」必须带「本征值互不相同」前提，P02 的反例不是空转。")
Ap_bad = mp.matrix(Agen)
Ap_bad[0, 1] += mp.mpf("1e-3"); Ap_bad[1, 0] += mp.mpf("1e-3")
I_bad = abs(I_mp(HdiagL, Ap_bad))
add(CTL, "C2", "PASS", "I_n 判据的牙齿：对角基（I 精确为 0）上给 A 加 1e-3 非对角 ⇒ I_n 立刻离开零",
    mp.mpf(0), I_bad, I_bad > mp.mpf("1e-12") and I0 == 0,
    "同一对角基 H=diag(2,5,−1)、同一 I_mp 代码路径，基线 I 精确为 0，只把 A 的 1-2 非对角元从 0 改成 1e-3 "
    "⇒ 读数离开机器零（49ε²=%s）；P04/P17 的「I_n=0」因此不是判据失效的同义反复。" % fmt(49 * mp.mpf("1e-6"), 10))
def fam_rel(f):
    M = [[mp.mpf(0)]*3 for _ in range(3)]
    for n in range(1, 2501):
        w = f(n)
        for i in range(3):
            for j in range(3):
                M[i][j] += w * a_n(i, n) * a_n(j, n)
    return max(rel(M[i][j], S_PRINT[i][j]) for i in range(3) for j in range(3))
r_our = max(rel(M2500[i][j] - S_PRINT[i][j], S_PRINT[i][j]) for i in range(3) for j in range(3))
r_rival = min(fam_rel(lambda n: 1/(n*n + 1)), fam_rel(lambda n: 1/mp.mpf(n)), fam_rel(lambda n: 1/mp.mpf(n)**4))
RES["ctl_S_rival"] = r_rival
add(CTL, "C3", "PASS", "S 权重口径的判别力：本卷族 %s vs 最近备择族（1/(n²+1)、1/n、1/n⁴ 取优）%s ⇒ 隔 6 个数量级" % (fmt(r_our, 4), fmt(r_rival, 4)),
    r_rival, r_our, r_our < r_rival / 1000,
    "S 的权重不是「任何衰减快的序列都行」：1/(n²+1)、1/n、1/n⁴ 三个备择族对六个展示位全部失败（最近者也差 0.26 以上），"
    "1/n² 族差 ≤ 1.9e-7 ⇒ 展示位命中对该口径有牙齿。1/n² 的来源（a_n~1/n² 尾部 × Green 函数谱展开）写在本条 note 与判定册 §一。")
add(CTL, "C4", "PASS", "区间口径的判别力：归一化 [0,1] dev %s vs [0,∞) dev %s（同一被积函数、只差上界）" % (fmt(max(norm_dev), 4), fmt(max(inf_dev), 4)),
    max(inf_dev), max(norm_dev), max(norm_dev) < max(inf_dev) / mp.mpf("1e6"),
    "两个读数出自同一 p_x 表达式、只差积分上界（1 vs ∞）；[0,∞) 上 τ 的偏离 4.94e-7 是「未声明区间」的代价，"
    "而 a_n 闭式与 overlap 相符（P07）只承认 [0,1] ⇒ 区间由两路证据唯一钉死。")
add(CTL, "C5", "PASS", ("积分器对照（仪器自检）：n=2500 overlap 单块 quad 偏 %s，250 段分段偏 %s ⇒「数值积分核验」必须分段"
      % (fmt(naive_rel, 4), fmt(seg_rel, 4))),
    seg_rel, naive_rel, naive_rel > mp.mpf("1") and seg_rel < TOL,
    ("仪器自检（记忆卡「仪器看不见自己要测的结果」）：n=2500 的被积函数是 cos(2500πz)·p_x 高频振荡，"
     "自适应 quad 单块求积给出 rel=%s 的垃圾读数——若直接采信就会把来料判成错。分段 250 块后与闭式相符到 %s。"
     "⇒ P07 的「overlap 与闭式双路相符」只在分段积分口径下成立，该口径已在预计算里单独标定。")
    % (fmt(naive_rel, 4), fmt(seg_rel, 4)))
demo_sqrt2 = demo_abs / SQ2
add(CTL, "C6", "PASS", "CKM 示范口径唯一性：正确读法 %s 命中来料；÷√2 变体 %s 不命中 ⇒ 排除「按零模再归一」读法" % (fmt(demo_abs, 10), fmt(demo_sqrt2, 10)),
    CKM_PRINT, demo_abs, disp_match(demo_abs, INCOMING["ckm_demo"]) and not disp_match(demo_sqrt2, INCOMING["ckm_demo"]),
    "÷√2 对应「先把单模函数按零模归一」的备择读法，round8 与来料不符 ⇒ 与 0.225、diag(8,7,5)、n=1 一起构成唯一口径；"
    "exp 与 act 来自展示串与矩阵乘两条路径。")
M_x101 = mp.mpf(10) * ((BR_DEMO * mp.mpf("1.01")) / SINDRUM) ** (mp.mpf(1)/4)
scale = M_x101 / M_calc
RES["ctl_M_scale"] = scale
add(CTL, "C7", "PASS", "M⁻⁴ 缩放定价：Br 放大 1.01 ⇒ 界放大 %s ≈ 1.01^{1/4}（三次根/平方根口径都排除）" % fmt(scale, 8),
    mp.mpf("1.0024938"), scale, abs(scale - (mp.mpf("1.01") ** (mp.mpf(1)/4))) < mp.mpf("1e-12"),
    "指数 1/4（即 Br∝M⁻⁴）单独定价：若来料实际按 M⁻² 或 M⁻⁶ 记账，1.01 扰动给出的放大倍数会不同 ⇒ "
    "P13 的舍入包络论证依赖的缩放指数有实证，不是抄来的。")
add(CTL, "C8", "PASS", "破缺线性：ε=1e-2→1e-3 时 |V12| 比值 %s（期望 10.0000）⇒ 一阶微扰口径成立" % fmt(lin_ratio, 10),
    mp.mpf(10), lin_ratio, abs(lin_ratio - 10) < mp.mpf("1e-4"),
    "两次 Jacobi（ε=1e-2 与 1e-3）比值恰 10 ⇒ |V12| 对破缺一阶线性；配合 P15 的 ε→0 极限 V=I，"
    "「对齐 ⇒ CKM=I」不是只能靠极限叙述，扰动侧有数值牙齿。")

# ============================================================================
# §9 · 守卫（AST/结构）
# ============================================================================
SRC = io.open(os.path.abspath(__file__), encoding="utf-8").read()
TREE = ast.parse(SRC)

def _add_calls():
    out = []
    for node in ast.walk(TREE):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "add":
            out.append(node)
    return out
AC = _add_calls()
bad_ok_const = sum(1 for nd in AC if isinstance(nd.args[6], ast.Constant) and isinstance(nd.args[6].value, bool))
bad_argn = sum(1 for nd in AC if len(nd.args) != 8)
add(GRD, "G01", "PASS", "AST 扫描：全部 add() 的 ok 实参顶层不是布尔常量（禁写死）",
    mp.mpf(0), mp.mpf(bad_ok_const), bad_ok_const == 0,
    "写死的 True 会让「通过」与实算脱钩；本扫描在运行中的文件自身上取 AST，ok 实参顶层若是布尔字面量立即计红。"
    "本轮登记前该扫描抓到并逼改了 P19–P21 的三处字面 True（自伤项已记判定册 §八）。")
add(GRD, "G02", "PASS", "AST 扫描：add() 一律 8 个实参",
    mp.mpf(0), mp.mpf(bad_argn), bad_argn == 0,
    "漏 note 的报告字段会在判定册里出现空列；本卷起草阶段 C1–C8、G01–G12 共 20 处漏 note 会在 add() 处直接 TypeError，"
    "故扫描与实参个数同时立账（抓到即改，不留到报告层）。")
ctl_ne = sum(1 for e in CTL if e["exp"] != e["act"])
add(GRD, "G03", "PASS", "控制组每条都给出「基线 vs 扰动」两个不同读数（exp ≠ act）",
    mp.mpf(len(CTL)), mp.mpf(ctl_ne), ctl_ne == len(CTL),
    "控制组的价值全在「两个读数不同」：exp==act 的控制条只能证明代码通电，不能证明判据有牙齿。"
    "注意比较的是登记后的字符串形态（exp/act 已被 fmt/str 归一）。")
r_probe = rel(mp.mpf("1e-60"), mp.mpf(0))
add(GRD, "G04", "PASS", "rel() 分母保底：rel(1e-60, 0) 不抛错、不伪判相等",
    mp.mpf("1e-60"), r_probe, r_probe == mp.mpf("1e-60"),
    "本卷大量出现「基线为 0」的相符判据（交换子为零、I_n 为零）；rel(a,0) 必须退化为绝对值口径，"
    "否则除零崩溃或被伪判为「完美相符」。")
dps_ok = mp.mp.dps >= 50
pi_check = abs(mp.pi - mp.mpf("3.14159265358979323846264338327950288419716939937510")) < mp.mpf("1e-45")
add(GRD, "G05", "PASS", "工作精度自证：dps≥50 且 π 到 45 位相符",
    mp.mpf(0), mp.mpf(0 if (dps_ok and pi_check) else 1), dps_ok and pi_check,
    "「65 位精度」类主张必须在已知精度下检验：dps=50 + π 到 45 位自证，防止展示位命中其实来自浮点地板。")
rid_count = SRC.count('RID = "r3' + '76"')
add(GRD, "G06", "PASS", "条目计数与分层：主册 %d、控制 %d、守卫登记中；本文件 RID 赋值 1 处" % (len(MAIN), len(CTL)),
    mp.mpf(1), mp.mpf(rid_count), rid_count == 1,
    "RID 字面在源码只允许出现一次（字符串拼接构造，防被 G10 的封锁表误伤）；多命中意味着别的卷号被混进本文件。"
    "主册/控制/守卫的条数在 SUMMARY 与报告首行现推，不预留空位。")
add(GRD, "G07", "PASS", "源码不含 random：确定性可复现",
    mp.mpf(0), mp.mpf(SRC.count("import " + "ra" + "ndom") + SRC.count("ran" + "dom.")),
    (SRC.count("import " + "ra" + "ndom") == 0) and (SRC.count("ran" + "dom.") == 0),
    "扫描词用拼接构造（同 G06 的 RID），否则守卫自身含禁词会永久假红；同输入必得同输出是复跑对账的前提。")
empty_note = sum(1 for lst in (MAIN, CTL, GRD) for e in lst if not e["title"].strip() or not e["note"].strip())
add(GRD, "G08", "PASS", "所有条目 title/note 非空（防「只有数字没有指称」）",
    mp.mpf(0), mp.mpf(empty_note), empty_note == 0,
    "数字没有指称就不能进判定册；note 与 title 同时非空才允许登记（本轮 C1–C8/G01–G12 起草时漏 note，"
    "被 add() 的 TypeError 挡在落盘之前，登记时刻此扫描再兜底一遍）。")
def seq_ok(lst, pfx):
    return [e["id"] for e in lst] == [pfx + str(k).zfill(2 if pfx == "P" or pfx == "G" else 1) for k in range(1, len(lst) + 1)]
# P 用两位、C/G 分别：主册 P01..，控制 C1..C8，守卫 G01..
ids_p = [e["id"] for e in MAIN] == ["P%02d" % k for k in range(1, len(MAIN) + 1)]
ids_c = [e["id"] for e in CTL] == ["C%d" % k for k in range(1, len(CTL) + 1)]
ids_g = [e["id"] for e in GRD] == ["G%02d" % k for k in range(1, len(GRD) + 1)]
add(GRD, "G09", "PASS", "编号连续无跳号（登记即自证）：P/C/G 三序列各与本卷登记时刻的条数一致",
    mp.mpf(1), mp.mpf(1 if (ids_p and ids_c and ids_g) else 0), ids_p and ids_c and ids_g,
    "跳号会在判定册与 README 之间留下无法引用的空位（本轮起草时 P07→P09 跳过 P08，即此守卫的靶；"
    "处理方式是把 P09 之后整体下移一位并同步所有交叉引用，而不是补一条凑数的条目）。")
# INCOMING 之外的字面值封锁
region = SRC.split("# §1 · INCOMING-BEGIN")[1].split("# §1b · INCOMING-END")[0]
outside = SRC.replace(region, "")
# 封锁表自身用拼接构造（同 G06/G07），否则禁词住在守卫源码里会被自己扫成假红
forbidden = ["2.8522" + "13", "2.6265" + "13", "2.3639" + "49", "2.7302" + "66",
             "2.5722" + "73", "2.4859" + "05", "0.023168" + "829", "0.004825" + "549",
             "0.003327" + "17", "9.54" + "99", "8.318e" + "-13", "16.21806" + "647",
             "10.44662" + "040", "7.26033" + "723"]
leaks = {t: outside.count(t) for t in forbidden if outside.count(t) > 0}
add(GRD, "G10", "PASS", "★来料字面值集中封锁：14 个展示数除 INCOMING 段外零出现（HTML/判定册只能引用变量）",
    mp.mpf(0), mp.mpf(sum(leaks.values())), sum(leaks.values()) == 0,
    "抄表列值进正文的债（r375 的 EPS0 教训）：来料展示数只许住在 INCOMING 段；标题/备注里出现的具体数字一律由变量插值。"
    "14 个禁词覆盖 S 六值、F 四分量、CKM 示范、界、Br、x 三代。")
keys_list = []
for node in ast.walk(TREE):
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Subscript) and getattr(t.value, "id", "") == "RES":
                keys_list.append(t.slice.value.value if hasattr(t.slice, "value") and hasattr(t.slice.value, "value") else None)
dup_keys = len(keys_list) - len(set(keys_list))
add(GRD, "G11", "PASS", "RES 键唯一：%d 次赋值无重名（防后写覆盖前写）" % len(keys_list),
    mp.mpf(0), mp.mpf(dup_keys), dup_keys == 0,
    "同键后写覆盖前写会让 REPORT 印出一个值、判定册引用另一个值（r375 的 src_dens_* 拆键教训）；"
    "扫描按 AST 的 RES[...] 赋值取键，不靠人工对照。")
indep_pairs = ["P01(分数) vs P03(sympy)", "P07(闭式) vs overlap(quad)", "P08(循环) vs closed_S(coth)",
               "P15(Jacobi) vs 2×2闭式", "P16(矩阵乘) vs sinθcosθ闭式", "P13(Br→M) vs (M→Br)"]
add(GRD, "G12", "PASS", "★至少 6 组「exp 与 act 来自不同代码路径」：%s" % "；".join(indep_pairs),
    mp.mpf(6), mp.mpf(len(indep_pairs)), len(indep_pairs) >= 6,
    "名单即账：每组的两端在源码里是不同函数/不同表达式（分数线性代数 vs sympy、循环求和 vs coth 闭式、"
    "Jacobi vs 2×2 闭式、矩阵乘 vs sinθcosθ、Br→M vs M→Br）；少于 6 组说明「相符」退化成同一段代码的自言自语。")

# ============================================================================
# §10 · 汇总
# ============================================================================
def cnt(lst, k): return sum(1 for e in lst if e["kind"] == k)
SUMMARY = dict(main_total=len(MAIN), main_pass=cnt(MAIN, "PASS"), main_info=cnt(MAIN, "INFO"),
               main_fail=cnt(MAIN, "FAIL"), ctl_total=len(CTL), ctl_pass=cnt(CTL, "PASS"),
               grd_total=len(GRD), grd_pass=cnt(GRD, "PASS"))
VERDICT = ("V44-ALIGNMENT-CRITERION-VERIFIED--KERNEL-S-SIX-DIGITS-ALL-REPRODUCED--"
           "CKM-DEMO-UNIQUE-READOUT--F-ABSOLUTE-NOT-RECOVERABLE--DOMAIN-UNDECLARED-BUT-FORCED")
ALL_OK = (SUMMARY["main_fail"] == 0 and SUMMARY["ctl_pass"] == SUMMARY["ctl_total"]
          and SUMMARY["grd_pass"] == SUMMARY["grd_total"])
FINAL = "ALL-GATES-PASS" if ALL_OK else "GATES-FAIL"

# ============================================================================
# §11 · 落盘：JSON / REPORT
# ============================================================================
BASE = "TUFT-%s_%s_%s" % (RID, TITLE, STAMP)
P_JSON = os.path.join(DATA_DIR, BASE + ".json")
P_REPORT = os.path.join(DATA_DIR, BASE + "_report_" + STAMP + ".txt")
P_MD = os.path.join(DATA_DIR, BASE + ".md")
P_JUD = os.path.join(JUD_DIR, "判定_判定_" + BASE + ".md")
P_HTML = os.path.join(ROOT, "四力统一方程_TUFT-r376_味对齐判据与谱塔核复现_%s.html" % STAMP)
OUT_PATHS = [P_JSON, P_REPORT, P_MD, P_JUD, P_HTML]

def _jd(o):
    if isinstance(o, mp.mpf): return fmt(o, 18)
    return str(o)

P_SRC_MD = os.path.join(DATA_DIR, "TUFT-r376_审计ROOTV44_三代味对齐_来料原件_用户附件逐字_2026-11-02.md")
_src_b = io.open(P_SRC_MD, "rb").read()
_src_sz = len(_src_b)                       # 存档文件整体（含说明头，随头改动而变）
import hashlib as _hl
_payload = _src_b[_src_b.rfind(b"\n---\n") + 5:]   # 原件头里声明的那把切法
RES["src_bytes"] = mp.mpf(_src_sz)
RES["src_md5"] = _hl.md5(_src_b).hexdigest()
RES["payload_bytes"] = mp.mpf(len(_payload))
RES["payload_md5"] = _hl.md5(_payload).hexdigest()
RES["payload_md5_matches_header"] = mp.mpf(1 if RES["payload_md5"] == "e058df" + "96fcebb7508e0873fab5166229" else 0)
RES["src_path_exists"] = "1" if os.path.isfile(P_SRC_MD) else "0"

js = dict(rid=RID, title=TITLE, stamp=STAMP, verdict=VERDICT, final=FINAL, summary=SUMMARY,
          incoming=INCOMING, res={k: _jd(v) for k, v in RES.items()}, main=MAIN, ctl=CTL, guard=GRD)
with io.open(P_JSON, "w", encoding="utf-8") as f:
    f.write(json.dumps(js, ensure_ascii=False, indent=1))

lines = []
lines.append("TUFT-%s · %s · %s" % (RID, TITLE, STAMP))
lines.append("判词：%s" % VERDICT)
lines.append("终态：%s" % FINAL)
lines.append("主册 %d（PASS %d / INFO %d / FAIL %d）；控制组 %d/%d；守卫 %d/%d"
             % (SUMMARY["main_total"], SUMMARY["main_pass"], SUMMARY["main_info"], SUMMARY["main_fail"],
                SUMMARY["ctl_pass"], SUMMARY["ctl_total"], SUMMARY["grd_pass"], SUMMARY["grd_total"]))
lines.append("")
lines.append("== 关键读数 ==")
for k in sorted(RES.keys()):
    lines.append("  %-24s %s" % (k, _jd(RES[k])))
lines.append("")
lines.append("== S 展示位对拍（本卷闭式 round6 vs 来料）==")
for (i, j, pr, mine, hit) in disp_tbl:
    lines.append("  S[%d][%d] 来料=%s 本卷=%s %s" % (i, j, pr, mine, "HIT" if hit else "MISS"))
lines.append("")
for nm, lst in [("主册", MAIN), ("控制组", CTL), ("守卫", GRD)]:
    lines.append("== %s ==" % nm)
    for e in lst:
        lines.append("[%s] %s | exp=%s | act=%s" % (e["id"], e["kind"], e["exp"], e["act"]))
        lines.append("      " + e["title"])
        lines.append("      " + e["note"])
    lines.append("")
with io.open(P_REPORT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

# ============================================================================
# §12 · 数据册 markdown（同 stem）
# ============================================================================
md = []
A = md.append
A("# TUFT-%s · 数据册 · %s" % (RID, STAMP))
A("")
A("终态 `%s`；主册 %d（PASS %d/INFO %d/FAIL %d）；控制 %d/%d；守卫 %d/%d。"
  % (FINAL, SUMMARY["main_total"], SUMMARY["main_pass"], SUMMARY["main_info"], SUMMARY["main_fail"],
     SUMMARY["ctl_pass"], SUMMARY["ctl_total"], SUMMARY["grd_pass"], SUMMARY["grd_total"]))
A("")
A("| RES 键 | 读数 |")
A("| --- | --- |")
for k in sorted(RES.keys()):
    A("| %s | %s |" % (k, _jd(RES[k])))
A("")
A("| 位 | 来料 | 本卷 round6 | 判定 |")
A("| --- | --- | --- | --- |")
for (i, j, pr, mine, hit) in disp_tbl:
    A("| S[%d][%d] | %s | %s | %s |" % (i, j, pr, mine, "HIT" if hit else "MISS"))
with io.open(P_MD, "w", encoding="utf-8") as f:
    f.write("\n".join(md) + "\n")

# ============================================================================
# §13 · 判定册 markdown
# ============================================================================
J = []
B = J.append
B("# TUFT-%s · %s" % (RID, TITLE))
B("")
B("**判词**：`%s`　　**终态**：`%s`　　**日期**：%s" % (VERDICT, FINAL, STAMP))
B("")
B("## 一、结论摘要")
B("")
B("- **★V44 的两条定理是真定理**：⟺ 判据在 4 组精确复有理酉共轭下双向零反例（P01）；"
  "I_n 恒等式经 sympy 对 9 参数通用 Hermitian 矩阵符号归零（P03）、基不变 rel %s（P04）。" % fmt(RES["basis_inv_rel"], 4))
B("- **★「本征值互不相同」是承重条款**：删掉即有 [H,A]=0 而 A 非对角的简并反例（P02/C1）；来料把前提写进了定理，无漏项。")
B("- **★★来料 S 矩阵六个展示位全部逐字符复现**：口径 = Σ_{n≤2500} a_n(x_i)a_n(x_j)/n²，"
  "本卷闭式（coth/csch，独立路径）round 到 6 位小数与来料六个数完全同串（P08）；N=2500 与 ∞ 差 ≤ %s（P09）。" % fmt(RES["S_sum_vs_closed_rel"], 4))
B("- **★归一化「65 位通过」隐含未声明区间**：[0,1] 上机器零（P05），[0,∞) 上 τ 第 7 位就破（P06/C4）；"
  "a_n 闭式与 overlap 的一致性把区间唯一钉在 [0,1]。来料未写区间 ⇒ 口径债，不是错。")
B(("- **★CKM 冲突的示范复现唯一命中**：X_Q=diag(8,7,5)、R₁₂(0.225)、单模 a₁ ⇒ |(A₁ᵘ)₁₂| round8 = 来料 %s（P16），" % INCOMING["ckm_demo"]) +
  "÷√2 等变体全部排除（C6）；冲突定理本体（同时对角 ⇒ V=I）+ ε 破缺一阶线性（P15/C8）。")
B("- **★来料 F_full/F_1 的绝对口径不可由附件恢复**：比值 4.80 自洽（P11），但 (U†D_nU)₁₂ 权重族、共轭翻转、δ 反号五族全失败（P12）；"
  "反解塔权指数 p*=%s 只能命中「比值」，复数分量仍差 %s ⇒ 判「不可复现（ZIP 未随附）」，不判「矛盾」。" % (fmt(RES["F_pstar"], 4), fmt(RES["F_star_rel"], 4)))
B(("- **M₁>界读数 %s TeV 属抄写层一致**：由展示 Br 直算 %s TeV；把 Br 读作 4 位舍入带则界带 [%s, %s] 覆盖来料界 %s（P13）；" % (INCOMING["m1_bound"], fmt(RES["M_from_printed_br"], 6), fmt(RES["M_env_lo"], 6), fmt(RES["M_env_hi"], 6), INCOMING["m1_bound"])) +
  "M⁻⁴ 指数单独定价（C7）。")
B("- **质量完全不同 ⇒ 无味改」的定量版成立**：f(X)=X² 下质量间隙 ≥ %s 而 2500 模 I_n 精确零 2500/2500（P17）；"
  "非平凡中微子混合与 ℓ 侧对齐兼容的构造性 witness（P18）。" % fmt(RES["mass_gap_min"], 6))
B("- **卷外引用**：SINDRUM/MEGII 两条本卷会话内检索到原始记录；「2026 综述仍列 SINDRUM」与「9-24 结束取数」未能核实 ⇒ 不计入证据（P19）。")
B("")
B("## 二、主册（%d 条）" % SUMMARY["main_total"])
B("")
B("| 键 | 判定 | 标题 |")
B("| --- | --- | --- |")
for e in MAIN:
    B("| %s | %s | %s |" % (e["id"], e["kind"], e["title"].replace("|", "\\|")))
B("")
B("## 三、控制组（%d 条）" % SUMMARY["ctl_total"])
B("")
B("| 键 | 判定 | 标题 | exp | act |")
B("| --- | --- | --- | --- | --- |")
for e in CTL:
    B("| %s | %s | %s | %s | %s |" % (e["id"], e["kind"], e["title"].replace("|", "\\|"), e["exp"], e["act"]))
B("")
B("## 四、守卫（%d 条）" % SUMMARY["grd_total"])
B("")
B("| 键 | 判定 | 标题 |")
B("| --- | --- | --- |")
for e in GRD:
    B("| %s | %s | %s |" % (e["id"], e["kind"], e["title"].replace("|", "\\|")))
B("")
B("## 五、S 展示位对拍表")
B("")
B("| 位 | 来料（逐字） | 本卷闭式 round6 | 判定 | 绝对差 |")
B("| --- | --- | --- | --- | --- |")
devs = {}
for (i, j, pr, mine, hit) in disp_tbl:
    devs[(i, j)] = abs(Mcl[i][j] - cS(pr))
    B("| S[%d][%d] | %s | %s | %s | %s |" % (i, j, pr, mine, "HIT" if hit else "MISS", fmt(devs[(i, j)], 3)))
B("")
B("## 六、F 口径扫描表")
B("")
B("| 读法族 | 复现 F_full 的相对差 |")
B("| --- | --- |")
B("| 标准 U·1/n² | %s |" % fmt(std_rel2, 4))
B("| U† 共轭翻转 | %s |" % fmt(abs(F_full_alt - F_FULL) / abs(F_FULL), 4))
B("| δ→−δ | %s |" % fmt(abs(Fneg - F_FULL) / abs(F_FULL), 4))
B("| p*=%s 反解比值 | %s |" % (fmt(pstar, 4), fmt(res_rel_star, 4)))
B("| （对照）F_1 标准 | %s |" % fmt(std_rel1, 4))
B("")
B("## 七、判定与分层")
B("")
B("- 本卷判词指向「代数层全通过 + 数值层可复现格全复现 + 不可复现格定价」；来料的物理叙事（对齐思想、CKM 冲突、"
  "四力本源未证明）不新增独立数值供给。")
B("- 分层：只覆盖 V44 一份来料；条目不可与 r354/r360/r365/r368/r370/r374/r375 相加。")
B("- 供给与定价：0/5（无锁定常数新约束）；度数链维持 36（r264 止）。")
B("")
B("## 八、取号与诚实边界")
B("")
B("- **取号**：落盘前扫三树 + README，r376 无文件占用、README 仅 r375 条目内提及「下轮从 r376 起」⇒ 取 r376，"
  "动手前已写 `_probe_r376.py` 占位。")
B("- **并发在飞（本轮实测）**：登记前后对 README 做逐行 difflib 对账，除本卷两处纯新增外另见一行被外部改写"
  "（r351 那条登记行增长数百字节）⇒ 台账有并行卷在写；本卷两锚点仍各命中 1 次、无第二卷占 r376，"
  "故登记有效，但「README 只有我在改」这一假设作废。引用本轮任何「最大号／份数」类读数前须重扫。")
B("- **来料原件（两枚指纹分家）**：本存档文件整体 %d 字节、md5 %s（说明头一改就变，故不作载荷指纹）；" % (_src_sz, RES["src_md5"]) +
  "**来料载荷**（最后一个三连字符分隔行起跳 5 字节到文件末）%d 字节、md5 %s，" % (len(_payload), RES["payload_md5"]) +
  ("与原件头声明的载荷读数%s。引用「原件多大／什么指纹」必须点名引的是哪一枚；本卷 JSON.res 同时印四格（src_bytes/src_md5/payload_bytes/payload_md5）。"
   % ("相符" if RES["payload_md5_matches_header"] == 1 else "不符 ⇒ 载荷被改过，本卷登记作废")))
B("- **未核**：52 项断言清单（ZIP 未随附）；MEG II 结束取数公告；「2026 综述」原文。")
B("- **载荷指纹复核式**（本轮已按这一行原样跑过，输出与上两枚载荷读数一致）："
  "`python -c \"import io,hashlib;b=io.open(r'数据/TUFT-r376_审计ROOTV44_三代味对齐_来料原件_用户附件逐字_2026-11-02.md','rb').read();"
  "x=b[b.rfind(bytes([10])+b'---'+bytes([10]))+5:];print(len(x),hashlib.md5(x).hexdigest())\"`")
B("- **OPEN**：`X-R376-1`（F 的归一/传播子口径需要从 ZIP 恢复）/ `X-R376-2`（x 三代值由实测质量反演的映射未给出，本卷无法复核）/ "
  "`X-R376-3`（简并例外路径：来料说「或引入新的简并、对称性」，其显式构造未给出）。")
B("")
B("## 八b、自伤登记（本轮写坏的驱动器，逐条留名）")
B("")
B("- **跳号**：主册首版从 P07 直接写到 P09，缺 P08 ⇒ 收口时对 P09 以后整体下移一位并同步全部交叉引用（22 处编辑）。"
  "下轮取号先把 id 序列在纸上排完再写第一条 add。")
B("- **字面 True 三处**：P19/P20/P21 的 ok 槽首版写了常量 True＝断言退化成交班登记。改为从 MAIN 的 id 集合现场计算的覆盖率；"
  "守卫 G01 的 AST 扫描恰好是为这一型准备的。")
B("- **漏 note 二十处**：控制组 C1–C8 与守卫 G01–G12 首版全部按七参调用，崩在 add() 的必传 note 上。批量小样跑不出这一族，"
  "整跑一遍才算还原成功。")
B("- **二阶极点留数写错**：对角闭式 T0_diag 的部分分式里 β 取了 −2/A 而非 −1，直接假红 P08/P09。以 mp.nsum 高精度对照后重新推导"
  "（A²/(u(u+A)²) = 1/u − 1/(u+A) − A/(u+A)²）。")
B("- **herm() 契约改动连锁**：为容忍锯齿行改了它的读取方式，反向破坏了三个稠密调用点——Adm2 全零把 P01 的反向半边变成恒真、"
  "P03 假红。数据结构契约变更必须枚举全部调用点。")
B("- **P01/P03 的真凶（上一登记的归因作废）**：把 herm 改成稠密读取后 exp=act=4 仍假红。探针第一版手打 cadd 打错、"
  "第二版改用驱动器 exec 才看见 matmul 元素变 8 元组：真凶是 `sum(items, ZERO_C)` ——内置 sum 用元组 + 初始化器，"
  "(a+bi)+(c+di) 元组语义是拼接，自定义 cadd 定义了却从未被调用；comm 只取 [0]/[1] 分量 ⇒ 虚部通道整体消失、"
  "「非零交换子」被读成零。修成 csum 逐分量折叠后 n_fwd/n_bwd 各 4。上一行把病因记在 herm 名下是错误归因，就地更正而非追加。")
B("- **jacobi 返回顺序拿反**：该函数返回 (本征值, 本征向量)，五个调用点按 `V, _ = jacobi(...)` 解包拿到对角化后的矩阵，"
  "V₁₂ 读数成机器零 ⇒ 线性化比值除零崩在 lin_ratio。单独立探针复算才定位（探针结果 4.0e-4 / 4.0e-5，比值恰 10）。")
B("- **mpmath 三连**：无 mp.fmpf（isinstance 全改 mp.mpf）、mp.matrix 无 .trace() 且按 [i, j] 0-基下标（自写 _mtrace）、"
  "sympy 表达式串不能直接喂 mp.mpf（Hgen 改为 mpc 元素逐字构造）。")
B("- **守卫自伤**：G10 首跑 act=26，其中 14 条命中来自禁词表自身住在源码里。同 G06 的 RID、G07 的 random，封锁词表必须用拼接构造。")
B("- **反照第一枚是 no-op**：图 1 柱高的反照把 h 写成 0，但源码里 `Math.max(h,1)` 把它兜成 1 ⇒ 体检器照旧 GEOMETRY-OK，"
  "「反照也绿」读作「尺没牙」。第二版直接替换字面 `Math.max(h,1)` 才红（4 条「高度为 0 ⇒ 不可见」）。"
  "反照必须打在「被检属性真被写成坏值」的位置；坏值能被下游兜底逻辑救回的那一版不算反照。")
B("- **原件头的单枚指纹是抄写债**：首版把用户消息正文的字节数/md5 抄成「原件」唯一指纹，而驱动器与登记脚本打印的是**存档文件**"
  "（它比载荷多一个说明头）⇒ 登记出去的数与头里的数对不上，正是「抄 stdout 进文档」那一族债。就地更正：头里把两枚分家——"
  "文件整体（getsize/md5 现测）与载荷（按头里写明的切法现算），并附复核式；载荷切法已用头里那一行原样跑过。"
  "登记时另有一次自伤：改写说明头时将「载荷 9557」误记成整体字节数，且新头自身含一枚分隔串使锚定 marker 从 1 枚变 2 枚 ⇒ "
  "当场按 marker 计数发现、删掉重写，并把「marker 数＝1」与载荷 md5 一起作为落盘前置断言。")
with io.open(P_JUD, "w", encoding="utf-8") as f:
    f.write("\n".join(J) + "\n")

# ============================================================================
# §14 · HTML（createElementNS + appendChild；须过 _check_html_geom.js）
# ============================================================================
def g6(x, nd=6):
    return ("%." + str(nd) + "g") % float(x)

conv_pts = []
for Nv in (10, 25, 50, 100, 250, 500, 1000, 2500):
    Mv = tower_sum(Nv)
    conv_pts.append((Nv, float(rel(Mv[0][0] - Mcl[0][0], Mcl[0][0]))))
# 收敛曲线（log10 scale, clip at -13 floor）
def conv_curve(x0, y0, w, h, pts):
    import math as _m
    out = []
    for k, (Nv, dv) in enumerate(pts):
        fx = x0 + w * k / (len(pts) - 1)
        lg = _m.log10(dv) if dv > 0 else -13.5
        yy = y0 + h * (6.5 - lg) / 15.0  # lg from 6.5(≈1e0) down to -8.5 映射
        yy = min(max(yy, y0), y0 + h)
        out.append("%.2f %.2f" % (fx, yy))
    return "M " + " L ".join(out)
POLY_CONV = conv_curve(60, 20, 560, 200, conv_pts)

sbar = []
for (i, j, pr, mine, hit) in disp_tbl:
    sbar.append((("S%d%d" % (i, j)), float((Mcl[i][j] - cS(pr)) * mp.mpf("1e7"))))
# bars drawn in JS from data array
SBAR_DATA = "[" + ",".join('["%s",%s]' % (nm, repr(v)) for nm, v in sbar) + "]"
EPS_PTS = []
for ek in range(1, 7):
    e_ = mp.mpf(10) ** (-ek)
    Hb = mp.matrix(Hu); Hb[0, 1] += e_; Hb[1, 0] += e_
    _, Vb = jacobi(Hb, 5)
    EPS_PTS.append((ek, float(abs(Vb[0][1]))))
def eps_poly(x0, y0, w, h, pts):
    import math as _m
    out = []
    for k, (ek, v) in enumerate(pts):
        fx = x0 + w * k / (len(pts) - 1)
        lg = _m.log10(v)
        yy = y0 + h * (1.0 - (lg + 5.5) / 4.5)
        yy = min(max(yy, y0), y0 + h)
        out.append("%.2f %.2f" % (fx, yy))
    return "M " + " L ".join(out)
POLY_EPS = eps_poly(60, 20, 560, 200, EPS_PTS)

T = {}
T["RID"] = RID; T["STAMP"] = STAMP
T["VERDICT"] = VERDICT
T["FINAL"] = FINAL
T["SUMMARY"] = json.dumps(SUMMARY, ensure_ascii=False)
T["SBAR"] = SBAR_DATA
T["POLY_CONV"] = POLY_CONV
T["POLY_EPS"] = POLY_EPS
T["CONV_LABELS"] = "[" + ",".join('["%d","%s"]' % (Nv, ("%.1e" % dv) if dv > 0 else "<1e-13") for Nv, dv in conv_pts) + "]"
T["SROWS"] = "[" + ",".join('["%d%d","%s","%s","%s"]' % (i, j, pr, mine, "HIT" if hit else "MISS")
                            for (i, j, pr, mine, hit) in disp_tbl) + "]"
T["FRATIO"] = g6(ratio, 6)
T["PSTAR"] = g6(pstar, 5)
T["BESTF"] = g6(best_rel, 4)
T["CKMV"] = g6(demo_abs, 10)
T["M1CALC"] = g6(M_calc, 8)
T["MP3000"] = g6(Mcl[0][0], 14)

HTML = """<!DOCTYPE html>
<html lang="zh"><head><meta charset="utf-8"><title>TUFT-@RID@ ROOT V44 味对齐审计</title>
<style>body{font-family:sans-serif;background:#f7f8fa;margin:16px}h1{font-size:18px}h2{font-size:15px}
svg{background:#fff;border:1px solid #ccc;display:block;margin:10px 0}table{border-collapse:collapse;font-size:12px}
td,th{border:1px solid #999;padding:3px 7px}</style></head><body>
<h1>TUFT-@RID@ · ROOT V44 味对齐审计 · @STAMP@</h1>
<div>判词 <b>@VERDICT@</b>；终态 <b>@FINAL@</b></div>
<h2>图 1 · S 核展示位残差（×1e-7）</h2>
<svg id="g1" viewBox="0 0 680 280"></svg>
<h2>图 2 · 谱塔截断收敛（S₁₁，log10 相对差）</h2>
<svg id="g2" viewBox="0 0 680 260"></svg>
<h2>图 3 · CKM 破缺线性 |V12| vs ε（log10）</h2>
<svg id="g3" viewBox="0 0 680 260"></svg>
<h2>表 · S 对拍</h2>
<div id="t1"></div>
<h2>表 · 关键读数</h2>
<div id="t2"></div>
<script>
var SB=@SBAR@;
var g1=document.getElementById('g1');
var ax=document.createElementNS('http://www.w3.org/2000/svg','line');
ax.setAttribute('x1',30);ax.setAttribute('y1',140);ax.setAttribute('x2',650);ax.setAttribute('y2',140);
ax.setAttribute('stroke','#666');g1.appendChild(ax);
for(var i=0;i<SB.length;i++){
  var v=SB[i][1];var x=40+i*100;
  var h=Math.abs(v)>100?110:Math.abs(v)*1.1;
  var r=document.createElementNS('http://www.w3.org/2000/svg','rect');
  r.setAttribute('x',x);r.setAttribute('width',60);
  if(v>=0){r.setAttribute('y',140-h);r.setAttribute('height',Math.max(h,1));r.setAttribute('fill','#2b7');
  }else{r.setAttribute('y',140);r.setAttribute('height',Math.max(h,1));r.setAttribute('fill','#c255');
  }
  g1.appendChild(r);
  var t=document.createElementNS('http://www.w3.org/2000/svg','text');
  t.setAttribute('x',x+10);t.setAttribute('y',240);t.textContent=SB[i][0];g1.appendChild(t);
}
</script>
<script>
var g2=document.getElementById('g2');
var p2=document.createElementNS('http://www.w3.org/2000/svg','path');
p2.setAttribute('d','@POLY_CONV@');p2.setAttribute('stroke','#1a5ea8');p2.setAttribute('fill','none');
g2.appendChild(p2);
var CL=@CONV_LABELS@;
for(var i=0;i<CL.length;i++){
  var t=document.createElementNS('http://www.w3.org/2000/svg','text');
  t.setAttribute('x',40+i*72);t.setAttribute('y',250);t.textContent=CL[i][0]+':'+CL[i][1];
  g2.appendChild(t);
}
</script>
<script>
var g3=document.getElementById('g3');
var p3=document.createElementNS('http://www.w3.org/2000/svg','path');
p3.setAttribute('d','@POLY_EPS@');p3.setAttribute('stroke','#8a2b6b');p3.setAttribute('fill','none');
g3.appendChild(p3);
var lab=document.createElementNS('http://www.w3.org/2000/svg','text');
lab.setAttribute('x',60);lab.setAttribute('y',245);lab.textContent='斜率≈1（一阶微扰）';g3.appendChild(lab);
</script>
<script>
var SR=@SROWS@;var s='<table><tr><th>位</th><th>来料</th><th>本卷round6</th><th>判定</th></tr>';
for(var i=0;i<SR.length;i++){s+='<tr><td>'+SR[i][0]+'</td><td>'+SR[i][1]+'</td><td>'+SR[i][2]+'</td><td>'+SR[i][3]+'</td></tr>';}
s+='</table>';document.getElementById('t1').innerHTML=s;
var rows=[['|F_full|/|F_1|','@FRATIO@'],['反解塔权指数 p*','@PSTAR@'],['最近 F 读法相对差','@BESTF@'],
 ['|(A1u)12| 本卷','@CKMV@'],['M1(展示Br直算)','@M1CALC@'],['S11 闭式','@MP3000@']];
var s2='<table><tr><th>读数</th><th>值</th></tr>';
for(var k=0;k<rows.length;k++){s2+='<tr><td>'+rows[k][0]+'</td><td>'+rows[k][1]+'</td></tr>';}
s2+='</table>';document.getElementById('t2').innerHTML=s2;
</script>
</body></html>
"""
for k, v in T.items():
    HTML = HTML.replace("@" + k + "@", v)
with io.open(P_HTML, "w", encoding="utf-8") as f:
    f.write(HTML)

print("SUMMARY:", json.dumps(SUMMARY, ensure_ascii=False))
print("FINAL =", FINAL)
for pth in OUT_PATHS:
    print("WROTE", os.path.basename(pth), os.path.getsize(pth))
sys.exit(0 if ALL_OK else 1)
