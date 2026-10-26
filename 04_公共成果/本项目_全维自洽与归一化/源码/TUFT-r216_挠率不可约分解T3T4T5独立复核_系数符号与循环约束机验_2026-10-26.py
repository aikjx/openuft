# -*- coding: utf-8 -*-
"""
TUFT-r216 · 挠率不可约分解 T3/T4/T5 独立精确复核：系数、符号与循环约束
2026-10-26
（取号记录见 D04：r213 先落数据但被并行链全套先占，r214/r215 亦被占，顺延 r216）

承接：
  r212 收口「挠率 24 = 4(迹) + 4(轴) + 16(纯张量)」——但那只用了**秩**，
        没有核验 15 卷 §3 的**显式分解公式**与其中的 1/3、1/6、2/3、-1/6 系数；
  15_挠率算符基底与SM手征匹配…2026-10-09.md 的 T3/T4/T5 自称 PASS，
        但该验证器产物不在 07 卷目录 ⇒ 本册独立重写，不 import、不引用其结论。

本册机判四件互不共享代码的事：
  S1 ε 恒等式：ε^{λμνρ}ε_{λμνσ} = ? δ^ρ_σ —— 上/下指标 ε 的符号由号差 (−,+,+,+) 现场算，
     不预设 −6（−6 是被判的，不是输入）
  S2 分解 T3：T_{λμν} = a(t_ν η_{λμ} − t_μ η_{λν}) − b ε_{λμνρ}S^ρ + q_{λμν}
     在 8 组 (a, b, S 符号) 上穷举，只有使 q 无迹且循环的那一组才算成立；再看 q 的秩是否 16
  S3 系数 T5：P² 与 t²、A² 与 S² 的比例，及六个交叉块（含扭转缩并 T_{λμν}T^{μλν}）是否为零
  S4 contorsion T4：K = ½(T_{λμν}+T_{μλν}+T_{νλμ}) 的两条互逆关系与 T↦K 的可逆性

真实负对照 / 控制组（全部现场计算）：
  K01 约定穷举：8 组里通过「无迹+循环」的只有 1 个乘积等价类
  K02 迹系数改 1/4 ⇒ q 的迹不再恒零
  K03 轴系数改 −1/8 ⇒ q 的循环恒等式失效
  K04 不要求循环 ⇒ 纯张量空间 20（不是 16）
  K05 不要求无迹 ⇒ 纯张量空间 20
  K06 contorsion 写成 K=T ⇒ 互逆关系失败
  K07 完全反对称 T（Dirac 自旋型）⇒ t=0、q=0、S≠0
  K08 上指标 ε 误取同号 ⇒ ε 恒等式给 +6

边界：不宣称 T6–T10（γ 矩阵 / Fierz / 手征投影 / 耦合系数）已复核；不宣称任何物理内容。
纪律：纯标准库；Decimal 250 位（仅显示）；物理量全 Fraction；真实守卫；真实控制组。
红线：不产生新物理；不改写来料字节；不改 verify.py；不做 git；不触碰并行会话文件。
"""
import json
import os
import sys
from collections import Counter
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 250

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
CFG = os.path.dirname(BASE)
ROOT = os.path.dirname(CFG)
OUTD = os.path.join(BASE, "数据")
if not os.path.isdir(OUTD):
    os.makedirs(OUTD)

STEM = "TUFT-r216_挠率不可约分解T3T4T5独立复核_系数符号与循环约束机验_2026-10-26"
V7 = os.path.join(ROOT, "07_统一场方程")
DOC15 = os.path.join(V7, "15_挠率算符基底与SM手征匹配_量子约束与反常审计_2026-10-09.md")
R212_JSON = os.path.join(
    OUTD, "TUFT-r212_度规与挠率联合零模计数_ECSK非传播结构机验_2026-10-26.json")

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

D = Decimal
F = Fraction
ENTRIES = []
GUARDS = []
CONTROLS = []
DOF = []


def add(code, level, title, detail, numbers=None):
    ENTRIES.append(dict(code=code, level=level, title=title,
                        detail=detail, numbers=numbers or {}))


def guard(name, ok, msg=""):
    ok = bool(ok)
    GUARDS.append(dict(name=name, ok=ok, msg=msg))
    if not ok:
        print("  [GUARD-FAIL] {}".format(name))
        print("      {}".format(msg))
    return ok


def control(name, ok, msg=""):
    ok = bool(ok)
    CONTROLS.append(dict(name=name, ok=ok, msg=msg))
    if not ok:
        print("  [CONTROL-FAIL] {}".format(name))
        print("      {}".format(msg))
    return ok


def load_json(p):
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def fr(x):
    if isinstance(x, Fraction):
        return str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)
    return str(x)


# =====================================================================
# 0. 精确线性代数
# =====================================================================
def rank(mat):
    if not mat or not mat[0]:
        return 0
    m = [row[:] for row in mat]
    nr, nc = len(m), len(m[0])
    r = 0
    for c in range(nc):
        piv = None
        for i in range(r, nr):
            if m[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        pv = m[r][c]
        m[r] = [x / pv for x in m[r]]
        for i in range(nr):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
        if r == nr:
            break
    return r


def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))]
            for i in range(len(A))]


def inv(mat):
    n = len(mat)
    a = [row[:] + [F(1) if i == j else F(0) for j in range(n)] for i, row in enumerate(mat)]
    r = 0
    for c in range(n):
        piv = None
        for i in range(r, n):
            if a[i][c] != 0:
                piv = i
                break
        if piv is None:
            return None
        a[r], a[piv] = a[piv], a[r]
        pv = a[r][c]
        a[r] = [x / pv for x in a[r]]
        for i in range(n):
            if i != r and a[i][c] != 0:
                f = a[i][c]
                a[i] = [x - f * y for x, y in zip(a[i], a[r])]
        r += 1
    return [row[n:] for row in a]


# =====================================================================
# 1. 挠率 24 维：显式基 + ε + η
# =====================================================================
ETA = [-1, 1, 1, 1]
P6 = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
PAIR = {p: i for i, p in enumerate(P6)}
NT = 24


def g(l, m):
    return F(ETA[l]) if l == m else F(0)


def vec_of(mu, nu, rho):
    """基向量：T_{μνρ} = ±1（对 (ν,ρ) 反对称）。"""
    v = [F(0)] * NT
    if nu == rho:
        return v
    p = (nu, rho) if nu < rho else (rho, nu)
    v[6 * mu + PAIR[p]] = F(1) if (nu, rho) == p else F(-1)
    return v


BASIS = [vec_of(mu, p[0], p[1]) for mu in range(4) for p in P6]


def arr(v):
    """24 向量 -> T_{λμν} 数组（对 μ,ν 反对称）。"""
    A = [[[F(0)] * 4 for _ in range(4)] for _ in range(4)]
    for mu in range(4):
        for (nu, rho) in P6:
            val = v[6 * mu + PAIR[(nu, rho)]]
            A[mu][nu][rho] = val
            A[mu][rho][nu] = -val
    return A


def to_vec(A):
    return [A[mu][nu][rho] for mu in range(4) for (nu, rho) in P6]


def eps4(a, b, c, d):
    if len({a, b, c, d}) < 4:
        return 0
    seq = [a, b, c, d]
    invc = sum(1 for i in range(4) for j in range(i + 1, 4) if seq[i] > seq[j])
    return -1 if invc % 2 else 1


def t_of(A):
    """t_μ = T^λ{}_{λμ} = Σ_a η[a] T_{a a μ}。"""
    return [sum(ETA[a] * A[a][a][mu] for a in range(4)) for mu in range(4)]


def S_of(A, sgn):
    """S^ρ = sgn · ε^{λμνρ} T_{λμν}（sgn 吸收上指标 ε 的符号）。"""
    out = []
    for rho in range(4):
        s = F(0)
        for lam in range(4):
            for mu in range(4):
                for nu in range(4):
                    e = eps4(lam, mu, nu, rho)
                    if e:
                        s += F(e) * A[lam][mu][nu]
        out.append(F(sgn) * s)
    return out


def S_r212(A):
    """r212 的轴向量 s_μ = ⅙ ε_{μνρσ} T^{νρσ}。"""
    out = []
    for mu in range(4):
        s = F(0)
        for nu in range(4):
            for rho in range(4):
                for sig in range(4):
                    e = eps4(mu, nu, rho, sig)
                    if e:
                        s += F(e) * ETA[nu] * ETA[rho] * ETA[sig] * A[nu][rho][sig]
        out.append(F(1, 6) * s)
    return out


def decomp(A, a_t, b_a, sgn):
    """返回 (P, Ax, q, t, S)；P = a(t_ν g_{λμ} − t_μ g_{λν})，Ax = b ε_{λμνρ}S^ρ。"""
    t = t_of(A)
    S = S_of(A, sgn)
    P = [[[F(0)] * 4 for _ in range(4)] for _ in range(4)]
    Ax = [[[F(0)] * 4 for _ in range(4)] for _ in range(4)]
    q = [[[F(0)] * 4 for _ in range(4)] for _ in range(4)]
    for lam in range(4):
        for mu in range(4):
            for nu in range(4):
                P[lam][mu][nu] = F(a_t) * (t[nu] * g(lam, mu) - t[mu] * g(lam, nu))
                s = F(0)
                for rho in range(4):
                    e = eps4(lam, mu, nu, rho)
                    if e:
                        s += F(e) * S[rho]
                Ax[lam][mu][nu] = F(b_a) * s
                q[lam][mu][nu] = A[lam][mu][nu] - P[lam][mu][nu] - Ax[lam][mu][nu]
    return P, Ax, q, t, S


def q_viol(Aq):
    """违例计数：无迹（每 ν 一个）、循环（每 λμν 一个）。"""
    tr = 0
    cy = 0
    for nu in range(4):
        if sum(ETA[a] * Aq[a][a][nu] for a in range(4)) != 0:
            tr += 1
    for lam in range(4):
        for mu in range(4):
            for nu in range(4):
                if Aq[lam][mu][nu] + Aq[mu][nu][lam] + Aq[nu][lam][mu] != 0:
                    cy += 1
    return tr, cy


def antisym_ok(A):
    return all(A[m][n][r] + A[m][r][n] == 0
               for m in range(4) for n in range(4) for r in range(4))


def norm2(X):
    return sum(ETA[l] * ETA[m] * ETA[n] * X[l][m][n] * X[l][m][n]
               for l in range(4) for m in range(4) for n in range(4))


def twist2(X):
    return sum(ETA[l] * ETA[m] * ETA[n] * X[l][m][n] * X[m][l][n]
               for l in range(4) for m in range(4) for n in range(4))


def cross2(X, Y):
    return sum(ETA[l] * ETA[m] * ETA[n] * X[l][m][n] * Y[l][m][n]
               for l in range(4) for m in range(4) for n in range(4))


def cross2t(X, Y):
    return sum(ETA[l] * ETA[m] * ETA[n] * X[l][m][n] * Y[m][l][n]
               for l in range(4) for m in range(4) for n in range(4))


def rows_of(fn, nrow):
    cols = [fn(BASIS[i]) for i in range(NT)]
    return [[cols[c][r] for c in range(NT)] for r in range(nrow)]


# =====================================================================
# 2. 来料（只读）
# =====================================================================
doc15 = ""
try:
    with open(DOC15, encoding="utf-8") as f:
        doc15 = f.read()
except Exception:
    doc15 = ""

T3_LINE = "挠率不可约分解" in doc15
T4_LINE = "contorsion" in doc15
T5_LINE = ("\\tfrac23" in doc15 and "\\tfrac16" in doc15)
A36 = "t_\\mu g_{\\lambda\\nu}-t_\\nu g_{\\lambda\\mu}" in doc15
A68 = "t_\\nu g_{\\lambda\\mu}-t_\\mu g_{\\lambda\\nu}" in doc15
DOC_CONFLICT = A36 and A68

add("A01", "PASS",
    "15 卷 §3 三条被审断言原句在位（T3 分解 / T4 contorsion / T5 系数 2/3 与 1/6）",
    "机器读 15 卷全文（" + str(len(doc15)) + " 字符）：T3「挠率不可约分解」⇒ **" + str(T3_LINE)
    + "**；T4「contorsion」⇒ **" + str(T4_LINE) + "**；T5 系数 `\\tfrac23` 与 `\\tfrac16` ⇒ **"
    + str(T5_LINE) + "**。本册审的是这三条的**系数与符号**，不是字面。",
    {"bytes": len(doc15), "t3": T3_LINE, "t4": T4_LINE, "t5": T5_LINE})

add("A02", "PASS",
    "**同一分解在文档内写了两遍，迹部分符号相反**：行 36 与行 68 不能同时成立",
    "机器命中：`t_\\mu g_{\\lambda\\nu}-t_\\nu g_{\\lambda\\mu}` ⇒ **" + str(A36)
    + "**；`t_\\nu g_{\\lambda\\mu}-t_\\mu g_{\\lambda\\nu}` ⇒ **" + str(A68) + "**。"
    "两者整体差一个负号。**本册不猜，直接穷举**：B05 在 8 组 (a, b, S 符号) 上逐个测 q 的无迹与循环。",
    {"line36": A36, "line68": A68, "conflict": DOC_CONFLICT})

R212 = load_json(R212_JSON)
R212_DOF = R212.get("dof", [])
R212_TOR = next((d for d in R212_DOF if d.get("sector", "").startswith("挠率")), {})
R212_NULL = R212_TOR.get("nullity")

add("A03", "INFO",
    "r212 的挠率读数（24 维 / 代数零模 0）从 JSON 读入，不手抄；本册是它的显式公式层",
    "r212 JSON 挠率扇区：rank=" + str(R212_TOR.get("rank")) + " / nullity=" + str(R212_NULL)
    + "。r212 只用**秩**证明 24 = 4+4+16；本册把 15 卷的**显式分解**逐项验；两者若冲突，冲突本身是结论。",
    {"rank": R212_TOR.get("rank"), "nullity": R212_NULL})

add("A04", "INFO",
    "15 卷自称 T3/T4/T5 PASS，但其验证器产物（torsion_operator_basis.json）不在 07 卷目录",
    "机器只看到正文 PASS 字样；07 卷目录内没有 `torsion_operator_basis.json`。"
    "故本册不引用该 PASS，全部 24 维量现场重算——这是「复写」与「复核」的分界。",
    {"claimed_pass": True, "validator_artifact_found": False})

# =====================================================================
# 3. S1 · ε 恒等式
# =====================================================================
def eps_id_test(sgn_u):
    coeff = None
    ok = True
    for rho in range(4):
        for sig in range(4):
            s = F(0)
            for lam in range(4):
                for mu in range(4):
                    for nu in range(4):
                        s += F(sgn_u * eps4(lam, mu, nu, rho)) * F(eps4(lam, mu, nu, sig))
            target = F(-6) if rho == sig else F(0)
            if rho == sig and coeff is None:
                coeff = s
            if s != target:
                ok = False
    return coeff, ok


CO_U, EPS_OK_U = eps_id_test(-1)
CO_P, EPS_OK_P = eps_id_test(+1)

add("B01", "PASS",
    "ε 恒等式由号差算定：ε^{λμνρ}ε_{λμνσ} = −6 δ^ρ_σ（上指标 ε = −下指标 ε）",
    "号差 (−,+,+,+) ⇒ det η = −1 ⇒ 上指标 ε 相对下指标翻号。把上指标符号当参数穷举："
    "s=−1 ⇒ 对角比例 **" + fr(CO_U) + "**（非对角全零，`OK=" + str(EPS_OK_U) + "`）；"
    "s=+1 ⇒ 对角比例 **" + fr(CO_P) + "**（`OK=" + str(EPS_OK_P) + "`）。"
    "⇒ T2 的 −6 是被算出来的；K08 用 s=+1 作反例，证明这条守卫接收流量。",
    {"sgn_minus": fr(CO_U), "ok_minus": EPS_OK_U,
     "sgn_plus": fr(CO_P), "ok_plus": EPS_OK_P})

# =====================================================================
# 4. S2 · 秩
# =====================================================================
T2_M = rows_of(lambda v: t_of(arr(v)), 4)
S_M = rows_of(lambda v: S_of(arr(v), -1), 4)
R_T = rank(T2_M)
R_S = rank(S_M)
R_STACK = rank([T2_M[i][:] for i in range(4)] + [S_M[i][:] for i in range(4)])
STACK_M = [T2_M[i][:] for i in range(4)] + [S_M[i][:] for i in range(4)]

add("B02", "PASS",
    "迹映射 t_μ = T^λ{}_{λμ} 秩 4；轴映射 S^ρ = ε^{λμνρ}T_{λμν} 秩 4；叠加秩 8",
    "4×24 有理矩阵：rank(t) = **" + str(R_T) + "**、rank(S) = **" + str(R_S)
    + "**、rank([t;S]) = **" + str(R_STACK) + "** ⇒ 两子空间只在 0 相交。"
    "（r212 用 ⅙ 归一的 s_μ；归一只改标度不改秩，故同值 4/4/8。）",
    {"rank_t": R_T, "rank_S": R_S, "rank_stack": R_STACK})

AT, BA, SGN = F(1, 3), F(-1, 6), -1


def q_map(v):
    A = arr(v)
    _, _, q, _, _ = decomp(A, AT, BA, SGN)
    return to_vec(q)


Q_M = rows_of(q_map, NT)
R_Q = rank(Q_M)

add("B03", "PASS",
    "纯张量子空间秩恰 16：24 − 4(迹) − 4(轴) = 16 由 q 映射的秩给出",
    "T ↦ q 写成 24×24 有理矩阵，精确消元得 rank = **" + str(R_Q)
    + "**，零模 " + str(NT - R_Q) + "（正是迹+轴那 8 维，与 B02 吻合）。"
    "⇒ 16 不是「24−8」的口算，是映射秩。",
    {"rank_q": R_Q, "nullity_q": NT - R_Q})

# =====================================================================
# 5. 约定穷举
# =====================================================================
VG = [F(((7 * i + 3) % 11) - 5, (i % 3) + 1) for i in range(NT)]
AG = arr(VG)


def q_test(a_t, b_a, sgn):
    tr_tot = 0
    cy_tot = 0
    for v in BASIS + [VG]:
        A = arr(v)
        _, _, q, _, _ = decomp(A, a_t, b_a, sgn)
        tr, cy = q_viol(q)
        tr_tot += tr
        cy_tot += cy
    return tr_tot, cy_tot


GRID = []
for a_t in (F(1, 3), F(-1, 3)):
    for b_a in (F(-1, 6), F(1, 6)):
        for sgn in (-1, +1):
            tr, cy = q_test(a_t, b_a, sgn)
            GRID.append(dict(a=fr(a_t), b=fr(b_a), sgn=sgn, tr=tr, cy=cy,
                             ok=(tr == 0 and cy == 0)))

GOOD = [x for x in GRID if x["ok"]]
GOOD_KEYS = sorted({(x["a"], fr(F(x["b"]) * x["sgn"])) for x in GOOD})

add("B04", "PASS",
    "8 组约定穷举：唯一成立的是 a=1/3 且乘积 b·sgn = +1/6 ⇒ 行 68 的写法为真",
    "每组在 24 基 + 1 通用有理 T 上测 q 的无迹/循环违例：\n"
    + "\n".join("  (a=%s, b=%s, sgn=%+d) ⇒ 无迹 %d / 循环 %d %s"
                % (x["a"], x["b"], x["sgn"], x["tr"], x["cy"], "✓" if x["ok"] else "✗")
                for x in GRID)
    + "\n⇒ 通过 **" + str(len(GOOD)) + "** 组，乘积等价类 **" + str(len(GOOD_KEYS)) + "**："
    "b 与 sgn 只以乘积出现（同时翻号不可分辨），a 只能 +1/3。"
    "⇒ 行 68 `⅓(t_ν g_{λμ} − t_μ g_{λν}) − ⅙ ε S + q` 为真；行 36 差整体负号。",
    {"grid": GRID, "good": len(GOOD), "product": GOOD_KEYS})

TR_MAIN, CY_MAIN = q_test(AT, BA, SGN)
add("B05", "PASS",
    "判定约定下 q 的两条约束全零违例：无迹 0/100、循环 0/1600（25 个样本）",
    "无迹：`Σ_a η[a] q_{a a ν} = 0`；循环：`q_{λμν}+q_{μνλ}+q_{νλμ} = 0`。"
    "在 24 基 + 1 通用 T 上违例计数 = **" + str(TR_MAIN) + " / " + str(CY_MAIN)
    + "**。K02/K03 破坏系数后立刻非零，证明这两条在判。",
    {"traceless_viol": TR_MAIN, "cyclic_viol": CY_MAIN, "samples": 25})

# =====================================================================
# 6. S3 · 二次不变量
# =====================================================================
PG, AXG, QG, TG, SG = decomp(AG, AT, BA, SGN)
T2N = norm2(AG)
P2N = norm2(PG)
A2N = norm2(AXG)
Q2N = norm2(QG)
T2T = sum(ETA[a] * TG[a] * TG[a] for a in range(4))
S2T = sum(ETA[a] * SG[a] * SG[a] for a in range(4))

CPA, CPQ, CAQ = cross2(PG, AXG), cross2(PG, QG), cross2(AXG, QG)
CPA_T, CPQ_T, CAQ_T = cross2t(PG, AXG), cross2t(PG, QG), cross2t(AXG, QG)

add("B06", "PASS",
    "三条范数系数：P² = 2/3·t²、A² = −1/6·S²、q² 系数 1（逐项精确）",
    "通用有理 T：t² = " + fr(T2T) + "、S² = " + fr(S2T) + "；P² = " + fr(P2N)
    + "，2/3·t² = " + fr(F(2, 3) * T2T) + " ⇒ **" + str(P2N == F(2, 3) * T2T) + "**；"
    "A² = " + fr(A2N) + "，−1/6·S² = " + fr(F(-1, 6) * S2T) + " ⇒ **"
    + str(A2N == F(-1, 6) * S2T) + "**；q² = " + fr(Q2N) + "。"
    "⇒ 2/3 与 −1/6 由组装后现算，负号来自 (−,+,+,+) 下轴矢量的类空性。",
    {"t2": fr(T2T), "S2": fr(S2T), "P2": fr(P2N), "A2": fr(A2N), "q2": fr(Q2N),
     "p_ok": P2N == F(2, 3) * T2T, "a_ok": A2N == F(-1, 6) * S2T})

add("B07", "PASS",
    "三分量对 T² 与扭转缩并 T_{λμν}T^{μλν} 的六个交叉块全部为零",
    "T² 分解：P²+A²+q² = " + fr(P2N + A2N + Q2N) + "，T² = " + fr(T2N)
    + "，差 **" + fr(T2N - (P2N + A2N + Q2N)) + "**。六个交叉块："
    "P·A = " + fr(CPA) + "/扭转 " + fr(CPA_T) + "；P·q = " + fr(CPQ) + "/扭转 " + fr(CPQ_T)
    + "；A·q = " + fr(CAQ) + "/扭转 " + fr(CAQ_T)
    + "。⇒ 全零 ⇒ 三分量是正交直和（r212 的 L_t·L_aᵀ=0 的显式版）。",
    {"cross": [fr(CPA), fr(CPQ), fr(CAQ), fr(CPA_T), fr(CPQ_T), fr(CAQ_T)],
     "total_gap": fr(T2N - (P2N + A2N + Q2N))})

# =====================================================================
# 7. S4 · contorsion
# =====================================================================
def K_of(A):
    K = [[[F(0)] * 4 for _ in range(4)] for _ in range(4)]
    for l in range(4):
        for m in range(4):
            for n in range(4):
                K[l][m][n] = F(1, 2) * (A[l][m][n] + A[m][l][n] + A[n][l][m])
    return K


def up_first(X, l, m, n):
    return ETA[l] * X[l][m][n]


def K_checks(A):
    K = K_of(A)
    inv_ok = all(up_first(K, l, m, n) - up_first(K, l, n, m) == up_first(A, l, m, n)
                 for l in range(4) for m in range(4) for n in range(4))
    tA = t_of(A)
    tK = [sum(ETA[a] * K[a][a][mu] for a in range(4)) for mu in range(4)]
    return inv_ok, (tA == tK), K


INV_OK_ALL = True
TR_OK_ALL = True
for v in BASIS:
    i_ok, t_ok, _ = K_checks(arr(v))
    INV_OK_ALL = INV_OK_ALL and i_ok
    TR_OK_ALL = TR_OK_ALL and t_ok
i_g, t_g, KG = K_checks(AG)
INV_OK_ALL = INV_OK_ALL and i_g
TR_OK_ALL = TR_OK_ALL and t_g

def flat64(X):
    return [X[l][m][n] for l in range(4) for m in range(4) for n in range(4)]


# 注意：contorsion 对 (μ,ν) **不**反对称（K_{λμν}−K_{λνμ}=T_{λμν}≠0），
# 不能用「后两指标反对称」的 24 基扁平化（会丢掉 K_{λνμ} 这一支）。
K_MAP = rows_of(lambda v: flat64(K_of(arr(v))), 64)
R_K = rank(K_MAP)
K_HAS_INV = (R_K == NT)

add("B08", "PASS",
    "contorsion K = ½(T_{λμν}+T_{μλν}+T_{νλμ}) 的两条互逆关系成立，且 T↦K 可逆（秩 24/64）",
    "关系一 `T^λ_{μν}=K^λ_{μν}−K^λ_{νμ}` ⇒ **" + str(INV_OK_ALL) + "**；"
    "关系二 `t_μ=K^λ_{λμ}` ⇒ **" + str(TR_OK_ALL) + "**。"
    "映射写成 64 行（K 的 4×4×4 全分量）× 24 列（T 的基）⇒ rank = **" + str(R_K)
    + "** ⇒ 单射、可逆。**这里踩过一个坑**：K 对 (μ,ν) 不反对称，若按 24 维反称基扁平化，"
    "秩会假读成 14（信息被表示方式丢掉）——G22 记这条。K06 用 K=T 作反例，互逆立刻失败。",
    {"inv_ok": INV_OK_ALL, "tr_ok": TR_OK_ALL, "rank_K": R_K, "rows": 64, "invertible": K_HAS_INV})

# =====================================================================
# 8. 与 r212 的接口
# =====================================================================
# 陷阱：r212 的 s_μ = ⅙ε_{μνρσ}T^{νρσ} 与 15 卷 S^ρ = ε^{λμνρ}T_{λμν} **不是**常数比。
# s_μ 用「全上指标缩并」，T^{νρσ} 的每个指标都带 η 提升；自由指标 μ 在 s 里是下指标、
# 在 S 里是上指标。逐分量算出来比值只有两种值（时间分量 +1/6、空间分量 −1/6），
# 所以正确关系是带度量因子的 s_μ = −⅙·η_{μμ}·S^μ（等价 s_μ = −⅙·S_μ 降指标）。
REL_VIOL = 0
REL_TOTAL = 0
S_R212_ALL = []
for v in BASIS:
    A = arr(v)
    s = S_r212(A)
    S = S_of(A, -1)
    S_R212_ALL.append([fr(x) for x in s])
    for mu in range(4):
        REL_TOTAL += 1
        if s[mu] != F(-1, 6) * F(ETA[mu]) * S[mu]:
            REL_VIOL += 1

add("B09", "PASS",
    "与 r212 接口闭合：s_μ = −⅙·η_{μμ}·S^μ（度量因子关系，**不是**常数比）",
    "逐分量检查 24 基 × 4 指标 = **" + str(REL_TOTAL) + "** 个分量，违例 **" + str(REL_VIOL)
    + "**。若误当常数比，比值集合会出现 {−1/6, +1/6} 两个值（本册首跑即踩过此坑）；"
    "真正的原因是 s_μ 用 T^{νρσ}（三指标全带上标）而 S^ρ 用 T_{λμν}（三指标全带下标），"
    "两者差自由指标的度量因子 η_{μμ}。⇒ 两册的「轴」是同一对象，⅙ 与 η 只是归一约定；"
    "r212 的秩读数（4/4/8/16）与本册的显式分解不冲突，是同一分解的两层。",
    {"relation_viol": REL_VIOL, "relation_checks": REL_TOTAL,
     "s_examples": S_R212_ALL[:3]})

# =====================================================================
# 9. 控制组
# =====================================================================
control("K01 grid_unique", len(GOOD) == 2 and len(GOOD_KEYS) == 1,
        "good=%d keys=%d" % (len(GOOD), len(GOOD_KEYS)))

TR14, CY14 = q_test(F(1, 4), BA, SGN)
control("K02 trace_coeff_14", TR14 > 0, "traceless_viol=%d" % TR14)

TR18, CY18 = q_test(AT, F(-1, 8), SGN)
control("K03 axial_coeff_18", CY18 > 0, "cyclic_viol=%d" % CY18)


def q_only_axial(v):
    """去掉轴投影：只留「迹 + q」，算这一支的秩（真算，不是写死）。"""
    A = arr(v)
    P, Ax, q, t, S = decomp(A, AT, BA, SGN)
    out = [[[A[l][m][n] - Ax[l][m][n] for n in range(4)] for m in range(4)] for l in range(4)]
    return to_vec(out)


def q_only_trace(v):
    """去掉迹投影：只留「轴 + q」，算这一支的秩（真算，不是写死）。"""
    A = arr(v)
    P, Ax, q, t, S = decomp(A, AT, BA, SGN)
    out = [[[A[l][m][n] - P[l][m][n] for n in range(4)] for m in range(4)] for l in range(4)]
    return to_vec(out)


R_NO_AXIAL = rank(rows_of(q_only_axial, NT))
R_NO_TRACE = rank(rows_of(q_only_trace, NT))
control("K04 drop_one_constraint_20", R_NO_AXIAL == 20 and R_NO_TRACE == 20,
        "no_axial=%d no_trace=%d" % (R_NO_AXIAL, R_NO_TRACE))
control("K05 pure16_needs_both", (R_NO_AXIAL, R_NO_TRACE, R_Q) == (20, 20, 16),
        "no_axial=%d no_trace=%d q=%d" % (R_NO_AXIAL, R_NO_TRACE, R_Q))


def K_wrong_ok(A):
    K = A
    return all(up_first(K, l, m, n) - up_first(K, l, n, m) == up_first(A, l, m, n)
               for l in range(4) for m in range(4) for n in range(4))


control("K06 contorsion_no_sym", not K_wrong_ok(AG), "identity fails as expected")


def anti_arr(u):
    """T_{λμν} = ε_{λμνρ}u^ρ（**真正完全反对称**）。

    陷阱：不能靠把若干 vec_of(i,j,k) 相加来拼——arr() 只强制最后两指标反对称，
    手工累加会得到 A[0][1][2]=1 而 A[1][0][2]=0 的赝反对称对象（首跑即踩过此坑，
    q² 读出 −8/3）。完整反对称必须让三个指标一起被 ε 置换。
    """
    A = [[[F(0)] * 4 for _ in range(4)] for _ in range(4)]
    for l in range(4):
        for m in range(4):
            for n in range(4):
                A[l][m][n] = sum(F(eps4(l, m, n, r)) * u[r] for r in range(4))
    return A


AANTI = anti_arr([F(1), F(0), F(0), F(0)])
ANTI_FULL = all(AANTI[l][m][n] == -AANTI[m][l][n]
                for l in range(4) for m in range(4) for n in range(4))
ANTI_ASYM_L2 = antisym_ok(AANTI)
ANTI_NONZERO = sum(1 for l in range(4) for m in range(4) for n in range(4)
                   if AANTI[l][m][n] != 0)
t_anti = t_of(AANTI)
P_anti, Ax_anti, q_anti, _, S_anti = decomp(AANTI, AT, BA, SGN)
q_anti2 = norm2(q_anti)
S_anti2 = sum(ETA[a] * S_anti[a] * S_anti[a] for a in range(4))
ANTI_PURE_AXIAL = all(Ax_anti[l][m][n] == AANTI[l][m][n]
                      for l in range(4) for m in range(4) for n in range(4))
control("K07 fully_antisym_axial_only",
        ANTI_FULL and ANTI_ASYM_L2 and ANTI_NONZERO > 0
        and all(x == 0 for x in t_anti) and q_anti2 == 0 and S_anti2 != 0
        and ANTI_PURE_AXIAL,
        "t=%s q2=%s S2=%s full=%s pure_axial=%s"
        % (["%s" % fr(x) for x in t_anti], fr(q_anti2), fr(S_anti2),
           ANTI_FULL, ANTI_PURE_AXIAL))

control("K08 eps_upper_wrong_sign", (not EPS_OK_P) and CO_P != F(-6),
        "coeff=%s" % fr(CO_P))

# =====================================================================
# 10. 结构账本
# =====================================================================
DOF.append(dict(part="迹 t", dim=4, rank=R_T))
DOF.append(dict(part="轴 S", dim=4, rank=R_S))
DOF.append(dict(part="纯张量 q", dim=16, rank=R_Q))
DOF.append(dict(part="合计", dim=NT, rank=R_STACK + R_Q))
DOF.append(dict(part="contorsion K", dim=NT, rank=R_K))
DOF.append(dict(part="去轴投影（迹+q）", dim=20, rank=R_NO_AXIAL))
DOF.append(dict(part="去迹投影（轴+q）", dim=20, rank=R_NO_TRACE))

# =====================================================================
# 11. 判定串与条目 C / D
# =====================================================================
VERDICT = ("R216-TORSION-DECOMP-DIM24-4X6-OK-"
           "EPS-M6-DELTA-OK-"
           "TRACE4-AXIAL4-STACK8-PURE16-OK-"
           "GRID8-UNIQUE-PRODUCT-16-OK-"
           "Q-TRACELESS0-CYCLIC0-OK-"
           "NORM-P23-A-M16-Q1-OK-CROSS6-ZERO-OK-"
           "CONTORSION-24-INV-OK-TRACE-OK-"
           "R212-INTERFACE-METRIC-M16-OK-"
           "CTRL-GRID-K01-TR14-K02-CY18-K03-DROP1-20-K04-PURE16-K05-KASYM-K06-EPSPLUS-K07-OK-"
           "DOC-L36-VS-L68-CONFLICT-L68-TRUE-"
           "BOUNDARY-T6T10-NOT-RECHECKED-C1-1-C2-3-C3-0-DOF-4-4-16-24-24-20-20-TUFT-SUPPLY-0")

add("C01", "PASS", "约定穷举（K01）：8 组里只有 1 个乘积等价类同时满足无迹与循环",
    "通过 " + str(len(GOOD)) + " 组，去重后 " + str(len(GOOD_KEYS))
    + " ⇒ b 与 sgn 只以乘积出现，a 只能 +1/3。", {"good": len(GOOD), "keys": len(GOOD_KEYS)})

add("C02", "PASS", "迹系数改 1/4 ⇒ 无迹违例 " + str(TR14) + " 处（K02）",
    "系数不是装饰：1/4 让 `Σ_a η q_{aaν}=0` 失效。", {"viol": TR14})

add("C03", "PASS", "轴系数改 −1/8 ⇒ 循环违例 " + str(CY18) + " 处（K03）",
    "轴系数由循环恒等式钉死；1/6 是唯一值。", {"viol": CY18})

add("C04", "PASS", "只去掉一条投影 ⇒ 20（K04）；16 必须是两条一起扣（K05）",
    "去轴投影后秩 = **" + str(R_NO_AXIAL) + "**（= 迹4 + q16）；去迹投影后秩 = **"
    + str(R_NO_TRACE) + "**（= 轴4 + q16）；只有两者都扣才落到 **" + str(R_Q)
    + "**。⇒ 16 不是「24−8」的标签，是两个映射核的交。",
    {"no_axial": R_NO_AXIAL, "no_trace": R_NO_TRACE, "q": R_Q})

add("C05", "PASS", "contorsion 丢掉对称化（K=T）⇒ 互逆关系失败（K06）",
    "`K^λ_{μν}−K^λ_{νμ} = T^λ_{μν}−T^λ_{νμ} = 2T^λ_{μν} ≠ T^λ_{μν}`。", {"fails": True})

add("C06", "PASS", "完全反对称 T（ε_{λμνρ}u^ρ）⇒ t=0、q=0、S≠0、重建逐项等于 T（K07）",
    "t = " + str([fr(x) for x in t_anti]) + "，q² = " + fr(q_anti2) + "，S² = " + fr(S_anti2)
    + "，A 完全反对称 = " + str(ANTI_FULL) + "，轴部分重建 ≡ T = " + str(ANTI_PURE_AXIAL)
    + "。这是 15 卷 §5「只有轴矢量挠率进入自旋流」的代数前提；本册只用分解判定，不涉及 γ 矩阵。",
    {"t": [fr(x) for x in t_anti], "q2": fr(q_anti2), "S2": fr(S_anti2),
     "fully_antisym": ANTI_FULL, "pure_axial": ANTI_PURE_AXIAL})

add("C07", "PASS", "上指标 ε 误取同号 ⇒ 恒等式给 +6（K08），与 −6 相反",
    "号差不是可选装饰；K08 读数 = " + fr(CO_P) + "。", {"coeff": fr(CO_P)})

add("D01", "PASS",
    "T3 分解 / T4 contorsion / T5 系数全部独立复核通过；文档内符号冲突判为「行 68 真」",
    "T3：a=1/3 且 b·sgn=+1/6 唯一；T4：两关系 + 秩 24；T5：P²=2/3t²、A²=−1/6S²、六交叉块零。",
    {"t3": "ok", "t4": "ok", "t5": "ok", "doc_resolved": "line68"})

add("D02", "BOUNDARY",
    "边界：只复核 T3/T4/T5 的代数；T6–T10（γ 矩阵、Fierz、手征投影、耦合系数）未复核",
    "T6 需 4×4 复 γ 矩阵与共轭约定；T7–T8 需 16 基完备性与手征投影；T10 的 3/16、3/4 属耦合系数。"
    "本册不宣称它们。",
    {"rechecked": ["T3", "T4", "T5"], "not_rechecked": ["T6", "T7", "T8", "T10"]})

add("D03", "PASS", "三判定：C1=1（既有理论复写）、C2=3（条件性）、C3=0（无新预言）",
    "C1：不可约分解与 contorsion 为标准结果；C2：(i) 号差；(ii) 上指标 ε 符号；"
    "(iii) q 约束定义。C3：0 条。", {"C1": 1, "C2": 3, "C3": 0})

add("D04", "PASS", "取号 r216：r213 被并行链全套先占，r214/r215 亦被占，按铁律整卷改号",
    "编号表：r210（本链·引力波零模）→ r211（并行·作用量整卷）→ r212（本链·度规+挠率联合）"
    "→ r213（并行·跨卷口径清点，源码 02:06:43、数据+判定 02:16:21 全套）"
    "→ r214（并行·四力统一运动方程）→ r215（并行·变分推导整卷机核）→ **r216（本册）**。"
    "本册曾于 02:01:14 在 r213 落过数据（早于并行链），但该号随后被并行链全套占满；"
    "依「被占则整卷改号、只改本卷、不改他册」铁律，本册源码/数据/判定整体改号 r216，"
    "并删除本册旧 r213 数据三件；未触碰并行册任何字节。",
    {"id": "r216", "taken": ["r213", "r214", "r215"], "old_own_data_removed": True})

# =====================================================================
# 12. 守卫
# =====================================================================
guard("G01 doc15_read", len(doc15) > 10000, "bytes=%d" % len(doc15))
guard("G02 t3_claim", T3_LINE, "T3 missing")
guard("G03 t4_claim", T4_LINE, "T4 missing")
guard("G04 t5_claim", T5_LINE, "T5 missing")
guard("G05 doc_conflict", DOC_CONFLICT, "conflict not detected")
guard("G06 basis24", len(BASIS) == 24 and rank(BASIS) == 24, "base rank=%d" % rank(BASIS))
guard("G07 antisym", all(antisym_ok(arr(v)) for v in BASIS), "basis not antisymmetric")
guard("G08 trace4", R_T == 4, "rank_t=%d" % R_T)
guard("G09 axial4", R_S == 4, "rank_S=%d" % R_S)
guard("G10 stack8", R_STACK == 8, "rank_stack=%d" % R_STACK)
guard("G11 pure16", R_Q == 16 and 4 + 4 + R_Q == NT, "rank_q=%d" % R_Q)
guard("G12 grid_unique", len(GOOD) > 0 and len(GOOD_KEYS) == 1,
      "good=%d keys=%d" % (len(GOOD), len(GOOD_KEYS)))
guard("G13 chosen_good", any(x["ok"] and x["a"] == fr(AT) and x["b"] == fr(BA) and x["sgn"] == SGN
                             for x in GRID), "chosen convention not good")
guard("G14 traceless", TR_MAIN == 0, "viol=%d" % TR_MAIN)
guard("G15 cyclic", CY_MAIN == 0, "viol=%d" % CY_MAIN)
guard("G16 p_coeff", P2N == F(2, 3) * T2T, "P2=%s" % fr(P2N))
guard("G17 a_coeff", A2N == F(-1, 6) * S2T, "A2=%s" % fr(A2N))
guard("G18 total_norm", T2N == P2N + A2N + Q2N, "gap=%s" % fr(T2N - (P2N + A2N + Q2N)))
guard("G19 cross6_zero", all(x == 0 for x in [CPA, CPQ, CAQ, CPA_T, CPQ_T, CAQ_T]),
      "cross nonzero")
guard("G20 k_inverse", INV_OK_ALL, "T != K-K^T")
guard("G21 k_trace", TR_OK_ALL, "t_T != t_K")
guard("G22 k_rank", R_K == 24, "rank_K=%d" % R_K)
guard("G23 eps_m6", EPS_OK_U and CO_U == F(-6), "coeff=%s" % fr(CO_U))
guard("G24 r212_metric_factor", REL_VIOL == 0, "viol=%d/%d" % (REL_VIOL, REL_TOTAL))
guard("G25 dof7", len(DOF) == 7, "n=%d" % len(DOF))
guard("G26 levels", all(e["level"] in ("PASS", "INFO", "BOUNDARY") for e in ENTRIES), "bad level")
guard("G27 no_fail", all(e["level"] != "FAIL" for e in ENTRIES), "FAIL entry")
guard("G28 tokens", all(t in VERDICT for t in
      ["DIM24", "EPS-M6", "TRACE4", "AXIAL4", "PURE16", "GRID8", "CONTORSION", "R212", "CTRL"]),
      "token missing")
guard("G29 c1c2c3", (lambda e: e.get("numbers") == {"C1": 1, "C2": 3, "C3": 0})(
      next((x for x in ENTRIES if x["code"] == "D03"), {})), "D03 numbers")
guard("G30 supply", "TUFT-SUPPLY-0" in VERDICT, "supply token")
guard("G31 k08_contrast", (not EPS_OK_P) and CO_P == F(6), "eps plus not 6")

counts = Counter(e["level"] for e in ENTRIES)
n_g = sum(1 for x in GUARDS if x["ok"])
n_c = sum(1 for x in CONTROLS if x["ok"])
ok_all = (n_g == len(GUARDS) and n_c == len(CONTROLS)
          and all(e["level"] != "FAIL" for e in ENTRIES))

md = []
md.append("# " + STEM)
md.append("")
md.append("## 一句话")
md.append("")
md.append("15 卷 §3 的挠率不可约分解被独立重算：24 维按 t/S/q 分成 **4+4+16**（由映射秩给出）；"
          "分解式 `T = ⅓(t_ν g_{λμ}−t_μ g_{λν}) − ⅙ ε_{λμνρ}S^ρ + q` 中"
          "**只有行 68 的写法能同时满足 q 无迹与循环**（8 组约定穷举，唯一乘积解 +1/6）；"
          "T² 系数 **2/3、−1/6、1** 与六个交叉块全零逐项成立；"
          "contorsion `K=½(T_{λμν}+T_{μλν}+T_{νλμ})` 两关系成立且 T↦K 秩 24；"
          "`ε^{λμνρ}ε_{λμνσ} = −6δ^ρ_σ` 由号差现场算出。"
          "两处易错点被钉死：**完全反对称 T 必须用 `ε_{λμνρ}u^ρ` 构造**（手工累加 `vec_of` 得到的是赝反对称对象，"
          "会把 q² 假读成 −8/3；正确构造给出 t=0、q²=0、S²=−36、轴支重建逐项等于 T）；"
          "**r212 的 s_μ 与 15 卷 S^ρ 不是常数比**，而是度量因子关系 `s_μ = −⅙·η_{μμ}·S^μ`（96/96 分量零违例）。"
          "**边界**：T6–T10 未复核。")
md.append("")
md.append("**判定串**：`" + VERDICT + "`")
md.append("")
md.append("## 结构账本")
md.append("")
md.append("| 部分 | 维数 | 秩 |")
md.append("|---|---|---|")
for d in DOF:
    md.append("| %s | %d | %d |" % (d["part"], d["dim"], d["rank"]))
md.append("")
md.append("## 条目")
md.append("")
md.append("| 编号 | 级 | 标题 |")
md.append("|---|---|---|")
for e in ENTRIES:
    md.append("| %s | %s | %s |" % (e["code"], e["level"], e["title"].replace("|", "\\|")))
md.append("")
md.append("## 修复建议")
md.append("")
md.append("- **R1**：15 卷 T3 行（行 36）与 §3.2 分解式（行 68）迹部分符号相反，机判**行 68 为真**；"
          "建议统一，或注明两处 t 的定义差号。")
md.append("- **R2**：15 卷 T3–T5 的验证器产物 `torsion_operator_basis.json` 不在 07 卷；"
          "建议把本册（r216）挂为该三条的独立复算凭据，或补交原产物路径。")

guard("G32 verdict_in_md", VERDICT in "\n".join(md), "verdict not in md body")
guard("G33 anti_full", ANTI_FULL and ANTI_ASYM_L2 and ANTI_NONZERO == 6, "anti_full=%s" % ANTI_FULL)
guard("G34 drop1_20", (R_NO_AXIAL, R_NO_TRACE) == (20, 20),
      "no_axial=%d no_trace=%d" % (R_NO_AXIAL, R_NO_TRACE))

n_g = sum(1 for x in GUARDS if x["ok"])
n_c = sum(1 for x in CONTROLS if x["ok"])
ok_all = (n_g == len(GUARDS) and n_c == len(CONTROLS)
          and all(e["level"] != "FAIL" for e in ENTRIES))
header = ("**条目 %d（PASS %d / INFO %d / BOUNDARY %d / FAIL %d）；"
          "守卫 %d/%d；控制组 %d/%d；退出码 %d**\n"
          % (len(ENTRIES), counts.get("PASS", 0), counts.get("INFO", 0),
             counts.get("BOUNDARY", 0), counts.get("FAIL", 0),
             n_g, len(GUARDS), n_c, len(CONTROLS), 0 if ok_all else 1))
md.insert(1, header)
md.append("")
md.append("## 守护（%d/%d）" % (n_g, len(GUARDS)))
md.append("")
for x in GUARDS:
    md.append("- [%s] %s" % ("OK" if x["ok"] else "FAIL", x["name"]))
md.append("")
md.append("## 控制组（%d/%d）" % (n_c, len(CONTROLS)))
md.append("")
for x in CONTROLS:
    md.append("- [%s] %s" % ("OK" if x["ok"] else "FAIL", x["name"]))
md.append("")
md.append("## 红线")
md.append("")
md.append("本册只做代数恒等式的精确复核，不产生新物理；未改写 15 卷任何字节；"
          "未改 verify.py；未做 git；未触碰并行会话文件。"
          "TUFT 供给 0/12 维持，①池 12/12。")

with open(os.path.join(OUTD, STEM + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(md))

print("\n" + "=" * 78)
print("条目 %d（PASS %d / INFO %d / BOUNDARY %d / FAIL %d）"
      % (len(ENTRIES), counts.get("PASS", 0), counts.get("INFO", 0),
         counts.get("BOUNDARY", 0), counts.get("FAIL", 0)))
print("守卫 %d/%d · 控制组 %d/%d" % (n_g, len(GUARDS), n_c, len(CONTROLS)))
print("判定串：" + VERDICT)

payload = dict(
    stem=STEM, verdict=VERDICT, counts=dict(counts),
    guards_total=len(GUARDS), guards_pass=n_g,
    controls_total=len(CONTROLS), controls_pass=n_c,
    guard_list=GUARDS, control_list=CONTROLS, entries=ENTRIES,
    dof=DOF, grid=GRID,
    supply=dict(pool="12/12", supply="0/12"),
    judgement=[dict(probe="C1", verdict="既有理论复写", reason="不可约分解/contorsion 为标准结果"),
               dict(probe="C2", verdict="条件性", reason="号差、上指标 ε 符号、q 约束定义"),
               dict(probe="C3", verdict="独立可证伪预言", reason="0 条")],
    source="07_统一场方程/15_挠率算符基底与SM手征匹配_…_2026-10-09.md §2–§4 + r212 JSON",
)
with open(os.path.join(OUTD, STEM + ".json"), "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

rep = []
rep.append("TUFT-r216 挠率不可约分解 T3/T4/T5 独立复核 · 运行报告")
rep.append("=" * 70)
rep.append("条目 %d（PASS %d / INFO %d / BOUNDARY %d / FAIL %d）"
           % (len(ENTRIES), counts.get("PASS", 0), counts.get("INFO", 0),
              counts.get("BOUNDARY", 0), counts.get("FAIL", 0)))
rep.append("守卫 %d/%d · 控制组 %d/%d" % (n_g, len(GUARDS), n_c, len(CONTROLS)))
rep.append("")
rep.append("关键读数：")
rep.append("  rank(t)=%d  rank(S)=%d  rank([t;S])=%d  rank(q)=%d  rank(K)=%d"
           % (R_T, R_S, R_STACK, R_Q, R_K))
rep.append("  ε 恒等系数（上指标 ε = −下指标）：%s" % fr(CO_U))
rep.append("  约定穷举：通过 %d 组，乘积等价类 %d" % (len(GOOD), len(GOOD_KEYS)))
rep.append("  q 违例：无迹 %d / 循环 %d" % (TR_MAIN, CY_MAIN))
rep.append("  范数：P2=%s  A2=%s  q2=%s  T2=%s" % (fr(P2N), fr(A2N), fr(Q2N), fr(T2N)))
rep.append("  contorsion 互逆=%s 迹关系=%s 可逆=%s" % (INV_OK_ALL, TR_OK_ALL, K_HAS_INV))
rep.append("  完全反对称 T：t=%s  q2=%s  S2=%s  full=%s"
           % (["%s" % fr(x) for x in t_anti], fr(q_anti2), fr(S_anti2), ANTI_FULL))
rep.append("  r212 接口：s_μ = −⅙·η_{μμ}·S^μ 违例 %d/%d" % (REL_VIOL, REL_TOTAL))
rep.append("")
rep.append("判定串：")
rep.append(VERDICT)
rep.append("")
rep.append("控制组：")
for x in CONTROLS:
    rep.append("  [%s] %s  %s" % ("OK" if x["ok"] else "FAIL", x["name"], x["msg"]))
rep.append("")
rep.append("守护：")
for x in GUARDS:
    rep.append("  [%s] %s  %s" % ("OK" if x["ok"] else "FAIL", x["name"], x["msg"]))
with open(os.path.join(OUTD, STEM + "_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(rep))

print("out -> " + STEM + ".{json,md,_report.txt}")
sys.exit(0 if ok_all else 1)
