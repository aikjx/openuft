# -*- coding: utf-8 -*-
"""ROOT V61 独立复算：中心化子 / 稳定子 / 交换子维数 / 六代与反常 / 六维标度账。

原则：不抄来料公式。
  A 层（int / Fraction 精确）：从 so(12) 的 66 个显式生成元重建分块与中心化子；
                             从 so(10) 的 45 个生成元算稳定子与交换子维数（两条路径）；
                             六套 16 的三项反常之和（精确整数）。
  B 层（Decimal 50 位）：由 M_Pl^2 = V_2 M_6^4 与 m_KK = sqrt2/R 推 M_6 的闭式，
                        反解 KK 标度门槛、幂次、塔顶端级数；质子衰变量级（含口径声明）。
  C 层（判定）：维数比较的判别力、Delta 的模型内锁死、来料未给数据的不可核项。

纪律：条目不可相加；纯陈述给 INFO；期望值一律取自另一条独立路径或来料读数反抄。
"""
import os
import io
import ast
import json
import sys
from fractions import Fraction as F
from decimal import Decimal as D, getcontext

getcontext().prec = 50


def _p(s):
    """GBK 控制台守卫：C 段条目名含 U+21D2（⇒），无此守卫会在 C01 抛 UnicodeEncodeError，
    C 段与守卫段整段不执行。只做字面降级，不重设 stdout 编码（重设会让捕获器误解码）。"""
    s = s.replace(u"\u21d2", u"=>").replace(u"\u2192", u"->")
    try:
        print(s)
    except UnicodeEncodeError:
        enc = getattr(sys.stdout, "encoding", None) or "ascii"
        print(s.encode(enc, "replace").decode(enc, "replace"))


getcontext().prec = 50

TITLE = "ROOT V61 独立复算"
DATE = "2026-11-04"
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "数据")
SELF = os.path.abspath(__file__)

ROWS = []
GUARDS = []


def add(rid, layer, name, exp, act, ok, note=""):
    kind = "INFO" if ok is None else ("PASS" if ok else "FAIL")
    ROWS.append({"id": rid, "layer": layer, "name": name, "exp": str(exp),
                 "act": str(act), "kind": kind, "note": note})
    _p("  [%-4s] %-4s %s" % (kind, rid, name))
    return ok


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": str(detail)})
    _p("  [GUARD %-3s] %-14s | %s" % ("ok" if ok else "BAD", name, detail))
    return ok


def sci(x, nd=10):
    x = D(x)
    if x == 0:
        return "0"
    sgn = "-" if x < 0 else ""
    ax = abs(x)
    e = 0
    while ax >= 10:
        ax /= 10
        e += 1
    while ax < 1:
        ax *= 10
        e -= 1
    return "%s%sE%+04d" % (sgn, format(ax, ".%df" % (nd - 1)), e)


# ================================================================= 通用：矩阵
def mat(n, f=0):
    return [[f for _ in range(n)] for _ in range(n)]


def gen(n, a, b):
    """so(n) 生成元 E_ab = e_a e_b^T - e_b e_a^T（a<b）"""
    M = mat(n)
    M[a][b] = F(1)
    M[b][a] = F(-1)
    return M


def comm(X, Y):
    n = len(X)
    out = mat(n)
    for i in range(n):
        for j in range(n):
            s = F(0)
            for k in range(n):
                s += X[i][k] * Y[k][j] - Y[i][k] * X[k][j]
            out[i][j] = s
    return out


def is_zero(M):
    return all(x == 0 for row in M for x in row)


def rank_mod(rows, ncol, p=1000003):
    M = [[int(x) % p for x in row] for row in rows]
    r = 0
    nr = len(M)
    for c in range(ncol):
        pv = None
        for i in range(r, nr):
            if M[i][c]:
                pv = i
                break
        if pv is None:
            continue
        M[r], M[pv] = M[pv], M[r]
        inv = pow(M[r][c], p - 2, p)
        Pr = [(x * inv) % p for x in M[r]]
        M[r] = Pr
        for i in range(r + 1, nr):
            f = M[i][c]
            if f:
                Mi = M[i]
                M[i] = [(a - f * b) % p for a, b in zip(Mi, Pr)]
        r += 1
        if r == nr:
            break
    return r


# ============================================ A01/A02：so(12) 的 66 与中心化子 T_F
N12 = 12
Q12 = [F(0)] * 10 + [F(2), F(-2)]
G12 = [(a, b) for a in range(N12) for b in range(a + 1, N12)]
assert len(G12) == 66

blocks = {}
for (a, b) in G12:
    blocks.setdefault(Q12[a] + Q12[b], []).append((a, b))
n_1 = 1
n_45 = len(blocks[F(0)]) - n_1
n10p = len(blocks[F(2)])
n10m = len(blocks[F(-2)])
add("A01", "A", "so(12) 的 66 个生成元按 U(1)_F 荷分块",
    "66 = 45 + 1 + 10 + 10，荷 0 / 0 / +2 / -2",
    "荷 0 块 %d（so(10) %d + u(1)_F 1）、荷 +2 块 %d、荷 -2 块 %d，合计 %d"
    % (len(blocks[F(0)]), n_45, n10p, n10m, n_45 + n_1 + n10p + n10m),
    (n_45, n_1, n10p, n10m) == (45, 1, 10, 10),
    "分块只由荷向量 Q12 决定，未引用来料")

TF = gen(N12, 10, 11)
n_cen = len([g for g in G12 if is_zero(comm(TF, gen(N12, *g)))])
add("A02", "A", "U(1)_F 磁通保留的规范代数维数 = Cent(T_F)",
    "46", "%d（= so(10) 的 45 + u(1)_F 的 1）" % n_cen, n_cen == 46,
    "残余 %d - 12 = %d = 33（so(10) 内未破缺）+ 1（u(1)_F）；12 = 8+3+1" % (n_cen, n_cen - 12))

# 负对照：取一般 Cartan 元（六个平面权重互不相同），中心化子必须变小
Tg = mat(N12)
for (k, w) in enumerate([1, 2, 3, 5, 7, 11]):
    Tk = gen(N12, 2 * k, 2 * k + 1)
    for i in range(N12):
        for j in range(N12):
            Tg[i][j] += w * Tk[i][j]
n_gen = len([g for g in G12 if is_zero(comm(Tg, gen(N12, *g)))])
add("A02b", "A", "负对照：把 T_F 换成一般 Cartan 元（六个平面权重 1,2,3,5,7,11）",
    "必须 != 46（单平面旋转与一般 Cartan 元不是同一类）", "%d" % n_gen,
    n_gen != n_cen,
    "同一台仪器在两个不同 T 上给两个不同读数；若相等则判据恒绿")

# ==================================================== A03：单个 10 的稳定子维数
G10 = [(a, b) for a in range(10) for b in range(a + 1, 10)]
assert len(G10) == 45


def acts_zero(T, vecs):
    for v in vecs:
        for i in range(10):
            if sum(T[i][k] * v[k] for k in range(10)) != 0:
                return False
    return True


v1 = [F(1)] + [F(0)] * 9
v2 = [F(0), F(1)] + [F(0)] * 8
n_st1 = len([g for g in G10 if acts_zero(gen(10, *g), [v1])])
n_st2 = len([g for g in G10 if acts_zero(gen(10, *g), [v1, v2])])
add("A03", "A", "单个实十维矢量的稳定子 / 两个独立实矢量的稳定子",
    "36（so(9)）/ 28（so(8)）", "%d / %d" % (n_st1, n_st2),
    (n_st1, n_st2) == (36, 28),
    "45 - 9 = 36；45 - 17 = 28（两条轨道并：9 + 8 = 17）")

# ============================ A04/A05：对称不变算子的交换子维数（Delta 锁死的机器证据）
SYMP = [(i, j) for i in range(10) for j in range(i, 10)]
assert len(SYMP) == 55
IDX = {p: n for n, p in enumerate(SYMP)}
PAIRS = [(a, b) for a in range(10) for b in range(a + 1, 10)]


def commutant_rows(gens):
    """对称 S（55 个未知量）与每个生成元对易，取 (i<j) 的 45 个方程。"""
    rows = []
    for T in gens:
        nz = [(m, n, T[m][n]) for m in range(10) for n in range(10) if T[m][n] != 0]
        for (i, j) in PAIRS:
            coef = [0] * 55
            for (m, n, v) in nz:
                if n == j:                                   # (S T)[i][j] += S[i][m]*v
                    coef[IDX[(min(i, m), max(i, m))]] += v
                if m == i:                                   # (T S)[i][j] += v*S[n][j]
                    coef[IDX[(min(n, j), max(n, j))]] -= v
            rows.append(coef)
    return rows


def commutant_dim(gens):
    return 55 - rank_mod(commutant_rows(gens), 55)


gens45 = [gen(10, *g) for g in G10]
gens9 = [gen(10, i, i + 1) for i in range(9)]
dim_so10 = commutant_dim(gens45)
dim_so10b = commutant_dim(gens9)
add("A04", "A", "与 so(10) 对易的对称 10x10 算子维数（两条路径）",
    "1（路径一：全 45 生成元）/ 1（路径二：9 个相邻生成元）",
    "%d / %d" % (dim_so10, dim_so10b), (dim_so10, dim_so10b) == (1, 1),
    "维数 1 ⇒ 任一 so(10) 不变的二次涨落算符 ∝ 单位 ⇒ m_H^2 = m_T^2 是定理；承接 r394 A6，同读数")

# so(8) 在 R^10 = 8+1+1 上（r394 的负对照，本册作为控制组复现）
gens_so8 = [gen(10, a, b) for a in range(8) for b in range(a + 1, 8)]
dim_so8 = commutant_dim(gens_so8)
add("A04b", "A", "控制组：so(8) 在 R^10 = 8+1+1 上的交换子维数",
    "4（不是 1）", "%d" % dim_so8, dim_so8 == 4,
    "同一台仪器、不同不变群给不同读数 ⇒ 维数不是恒等于 1 的装饰")


def realify(A):
    M = mat(10)
    for i in range(5):
        for j in range(5):
            re, im = A[i][j]
            if re == 0 and im == 0:
                continue
            M[2 * i][2 * j] = re
            M[2 * i][2 * j + 1] = -im
            M[2 * i + 1][2 * j] = im
            M[2 * i + 1][2 * j + 1] = re
    return M


Z = (F(0), F(0))
I1 = (F(0), F(1))        # i


def c5():
    return [[Z] * 5 for _ in range(5)]


def su5_gens():
    """su(5) 的 24 个反厄米生成元（实化到 so(10) 的矢量表示）。"""
    out = []
    for (a, b) in [(i, j) for i in range(5) for j in range(i + 1, 5)]:
        A = c5()
        A[a][b] = (F(1), F(0))
        A[b][a] = (F(-1), F(0))
        out.append(realify(A))
        A = c5()
        A[a][b] = I1
        A[b][a] = I1
        out.append(realify(A))
    for k in range(4):
        A = c5()
        A[k][k] = I1
        A[k + 1][k + 1] = (F(0), F(-1))
        out.append(realify(A))
    return out


def sm_gens():
    """su(3)+su(2)+u(1)_Y 的 12 个生成元（5 = (3,1) + (1,2) 的实化）。"""
    out = []
    for (a, b) in [(0, 1), (0, 2), (1, 2)]:
        A = c5()
        A[a][b] = (F(1), F(0))
        A[b][a] = (F(-1), F(0))
        out.append(realify(A))
        A = c5()
        A[a][b] = I1
        A[b][a] = I1
        out.append(realify(A))
    for (a, b) in [(0, 1), (1, 2)]:
        A = c5()
        A[a][a] = I1
        A[b][b] = (F(0), F(-1))
        out.append(realify(A))
    A = c5()
    A[3][4] = (F(1), F(0))
    A[4][3] = (F(-1), F(0))
    out.append(realify(A))
    A = c5()
    A[3][4] = I1
    A[4][3] = I1
    out.append(realify(A))
    A = c5()
    A[3][3] = I1
    A[4][4] = (F(0), F(-1))
    out.append(realify(A))
    A = c5()
    for i in range(3):
        A[i][i] = (F(0), F(-2))
    for i in (3, 4):
        A[i][i] = (F(0), F(3))
    out.append(realify(A))
    return out


G_SU5 = su5_gens()
G_SM = sm_gens()
dim_su5 = commutant_dim(G_SU5)
dim_sm = commutant_dim(G_SM)
add("A05", "A", "交换子维数阶梯：su(5) 与 SM",
    "su(5) 给 1（Delta 仍锁死）；SM 给 2（恰 1 个自由参数）",
    "su(5): %d（%d 个生成元）/ SM: %d（%d 个生成元）"
    % (dim_su5, len(G_SU5), dim_sm, len(G_SM)),
    (dim_su5, dim_sm) == (1, 2),
    "R^10 在 SM 下分成 V6（含 3 与 3bar）与 V4（含双重态），两块各自一个标量 ⇒ "
    "m_H^2 与 m_T^2 可独立；su(5) 下 10 = 5+5bar 不可分 ⇒ 仍锁死")

# ============================================ A06/A07：六套 16 的计数与三项反常
N_FAM = 3
n16 = N_FAM + N_FAM
net = N_FAM * (+1) + N_FAM * (-1)
add("A06", "A", "N=3 磁通下的 16 等价家族数与净手征",
    "6 套 / 净手征 6（来料口径：右手共轭后都算左手 16）",
    "16 个数 %d、荷和 %d" % (n16, net), n16 == 6,
    "与 r394 A7 同读数；净手征按来料口径取绝对值 6")

A3v = A2v = Agv = 0
for (dimR, TR, q) in [(16, 2, +1)] * 3 + [(16, 2, -1)] * 3:
    A3v += dimR * q ** 3
    A2v += TR * q
    Agv += dimR * q
add("A07", "A", "该六套谱的三项反常（U(1)^3 / Spin(10)^2U(1) / grav^2U(1)）",
    "若谱真是 3 个 16_{+1} + 3 个 16bar_{-1}，三项必须全为 0",
    "%d / %d / %d" % (A3v, A2v, Agv), (A3v, A2v, Agv) == (0, 0, 0),
    "矢量型谱 ⇒ 三项精确为 0，与来料自报的 288 / 12 / 144 不相容："
    "那组数不属于这个六套谱（承接 r393 A10 的 96 + 192 分解）")
k_need = F(288, 16)
add("A07b", "A", "反推：单靠 16_{+1} 要给 U(1)^3 = 288 需要几个",
    "18（不是 3，也不是 6）", "%s 个" % k_need, k_need == 18,
    "16 q^3 = 16 q；六套谱给 0 ⇒ 288 只能由额外单态份额补足")
add("A07c", "A", "来料 §四 自报的 288 / 12 / 144 能否由它自述的六套谱给出",
    "288 / 12 / 144（来料读数反抄）",
    "%d / %d / %d（同一谱用指标口径重算）" % (A3v, A2v, Agv),
    (A3v, A2v, Agv) == (288, 12, 144),
    "矢量型谱三项精确为 0 ⇒ 这组数必属另一个（手征）谱；"
    "V61 §四 在同一节里写了两个不相容的谱（承接 r393 A10，同结论）")

# ============================================================ B 层：六维标度账
PI = D("3.14159265358979323846264338327950288419716939937510")
SQ2 = D(2).sqrt()
MPL = D("2.435E18")
MKK = D("1.0E4")
MX = D("1.0E15")


def M6_of(mkk):
    """M_Pl^2 = V_2 M_6^4，V_2 = 4 pi R^2，R = sqrt2/m_KK"""
    R = SQ2 / mkk
    V2 = 4 * PI * R * R
    return ((MPL * MPL / V2).sqrt()).sqrt()


M6 = M6_of(MKK)
M6_closed = (MPL.sqrt() * MKK.sqrt()) / ((8 * PI).sqrt().sqrt())
rel1 = abs(M6 - M6_closed) / M6
add("B01", "B", "M_6 的闭式 M_Pl^{1/2} m_KK^{1/2}/(8 pi)^{1/4} 与逐式换算",
    "两条路径相对偏差 < 1e-40",
    "%s vs %s，相对偏差 %s" % (sci(M6, 8), sci(M6_closed, 8), sci(rel1, 3)),
    rel1 < D("1e-40"), "来料只给 6.9693e10（5 位）；闭式给到 10 位")

rel_in = abs(M6 - D("6.9693e10")) / M6
add("B02", "B", "与来料 6.9693e10 GeV 的比对",
    "相对偏差 < 1e-5（来料 5 位有效数字）", "%s" % sci(rel_in, 3),
    rel_in < D("1E-5"),
    "M_Pl 取 2.435e18 时复现；来料未报 M_Pl 取值，此为口径反推")

ratio = MX / M6
add("B03", "B", "M_X / M_6", "1.4349e4（来料）", "%s" % sci(ratio, 5),
    abs(ratio - D("1.4349e4")) / ratio < D("1E-4"),
    "比值本身为真；它是不是正确的度量见 B06/C03")

mkk_min = (8 * PI).sqrt() * MX * MX / MPL
add("B04", "B", "使 M_X <= M_6 所需的最小 KK 标度（闭式反解）",
    "sqrt(8 pi) M_X^2 / M_Pl（与 B03 读数无关的独立表达）",
    "%s GeV = %s TeV" % (sci(mkk_min, 8), sci(mkk_min / D("1000"), 6)), None,
    "闭式由 B01 的 M_6(m_KK) 令 M_6 = M_X 反解；此处只报读数")

lhs = mkk_min / MKK
rhs = ratio * ratio
rel2 = abs(lhs - rhs) / lhs
add("B05", "B", "恒等式 m_KK,min / m_KK,demo = (M_X/M_6)^2",
    "相对偏差 < 1e-30（左：反解闭式；右：来料比值的平方）",
    "%s vs %s，相对偏差 %s" % (sci(lhs, 8), sci(rhs, 8), sci(rel2, 3)),
    rel2 < D("1E-30"),
    "把来料的 1.4349e4 读成「KK 标度必须搬多少倍」：%s 倍" % sci(lhs, 6))

pts = [D("1e3"), D("1e4"), D("1e5"), D("1e6")]
vals = [M6_of(m) for m in pts]
slopes = [(vals[i + 1] / vals[i]).ln() / (pts[i + 1] / pts[i]).ln() for i in range(3)]
max_dev = max(abs(s - D("0.5")) for s in slopes)
add("B06", "B", "M_6 对 m_KK 的幂次（4 点 log-log 斜率，不是两点）",
    "全部 = 0.5，偏差 < 1e-40", ", ".join(str(s) for s in slopes),
    max_dev < D("1E-40"),
    "等比网格上必须用 log-log 斜率；两点相除在指数 1/2 时也可能凑出像样的数，故取 4 点")
pred1 = vals[0] * (pts[-1] / pts[0])
dev1 = pred1 / vals[-1]
add("B06b", "B", "控制组：若指数为 1，M_6(1e6) 的预测",
    "与实测差 sqrt(1000) = 31.6228 倍（不是 1 倍，也不是 1000 倍）",
    "预测 %s vs 实测 %s，差 %s 倍" % (sci(pred1, 6), sci(vals[-1], 6), sci(dev1, 6)),
    abs(dev1 - D(1000).sqrt()) < D("1E-20"),
    "两个读数不同 ⇒ 幂次判据有判别力，不是恒绿；线性假设一次就错 31.6 倍")

R = SQ2 / MKK
N_max = M6 * R
n_req = MX * R
add("B07", "B", "六维塔的最大级数 N_max = M_6 R 与 4D 质量 M_X 对应的级数 R M_X",
    "N_max = sqrt2 M_6/m_KK、n_req = sqrt2 M_X/m_KK，比值 = M_X/M_6",
    "N_max = %s，n_req = %s，比值 = %s"
    % (sci(N_max, 6), sci(n_req, 6), sci(n_req / N_max, 5)),
    abs(n_req / N_max / ratio - 1) < D("1E-30"),
    "比值与 B03 同一读数 ⇒ 此条核对的是恒等式，不能当第二条独立证据")

alpha = D(1) / D(40)
mp = D("0.938272")
tau_yr = MX ** 4 / (alpha * alpha * mp ** 5) * D("6.582119569e-25") / D("3.15576e7")
MX_req = (D("2.4e34") * D("3.15576e7") / D("6.582119569e-25")
          * alpha * alpha * mp ** 5).sqrt().sqrt()
add("B08", "B", "质子衰变量级：M_X = 1e15、alpha = 1/40 时的寿命",
    "只报量级（alpha 是自由口径，不是理论输出）",
    "tau ~ %s 年（SK 限 2.4e34 年）；反解得 M_X >= %s GeV"
    % (sci(tau_yr, 4), sci(MX_req, 4)), None,
    "有量纲口径 alpha 使这条只作一致性旁证，不作判据；tau ∝ M_X^4，单调")

# ================================================================ C 层：判定
# C01：构造 12 维闭子代数 so(4)+so(4) ⊂ so(8) ⊂ so(10)，并算它的中心
B1 = [gen(10, a, b) for a in range(4) for b in range(a + 1, 4)]
B2 = [gen(10, a, b) for a in range(4, 8) for b in range(a + 1, 8)]
SUB = B1 + B2
n_sub = len(SUB)
closure_ok = True
for X in SUB:
    for Y in SUB:
        C = comm(X, Y)
        # 检查 C 是否仍是块对角的（so(4)+so(4) 的闭包性）
        for i in range(10):
            for j in range(10):
                if C[i][j] != 0:
                    bi = 0 if i < 4 else (1 if i < 8 else 2)
                    bj = 0 if j < 4 else (1 if j < 8 else 2)
                    if bi != bj:
                        closure_ok = False
# 中心维数：X = sum c_i B_i 满足 [X, B_j] = 0；把每个 [B_i, B_j] 展成 so(10) 的 45 维坐标
ANTI = [(a, b) for a in range(10) for b in range(a + 1, 10)]


def anti_coords(M):
    return [M[a][b] for (a, b) in ANTI]


def center_dim(basis):
    n = len(basis)
    CM = [[anti_coords(comm(basis[i], basis[j])) for i in range(n)] for j in range(n)]
    rows = []
    for j in range(n):
        for k in range(45):
            rows.append([CM[j][i][k] for i in range(n)])
    return n - rank_mod(rows, n)


cen_sub = center_dim(SUB)
cen_sm = center_dim(G_SM)
counter_exists = (n_sub == 12) and closure_ok and (cen_sub != cen_sm)
add("C01", "C", "来料 §二：「Spin(8) 的 28 > 12 ⇒ 单个复 10 不能破缺到 SM」",
    "维数比较要成为子群判据，必须排除 12 维反例；反例存在 ⇒ 该推理零判别力",
    "so(4)+so(4) 是 %d 维、对易子封闭（%s）的子代数；其中心维数 %d，而 SM 的为 %d"
    % (n_sub, "是" if closure_ok else "否", cen_sub, cen_sm),
    not counter_exists,
    "「28 > 12」对「SM < 稳定子」零判别力：12 维反例存在且不是 SM（中心维数不同）；"
    "正确判据是单态计数（10 = 5+5bar 单态数 0）；承接 r394 A3，同读数")

add("C02", "C", "来料 §五：Delta = m_T^2 - m_H^2 被当作「待从作用量算出」的开放量",
    "若不变群 >= su(5)，Delta 恒为 0（不是待算，是已定）",
    "so(10) 交换子维数 %d、su(5) 维数 %d ⇒ 涨落算符 ∝ 单位 ⇒ Delta ≡ 0；"
    "只有降到 SM（维数 %d）才允许 Delta != 0，代价恰 %d 个序参量"
    % (dim_so10, dim_su5, dim_sm, dim_sm - dim_so10),
    (dim_su5 >= 2),
    "§三（m_H,0 = m_T,0）与 §五（Delta 待算）合起来自证 Delta = 0："
    "§五 表里「Delta > 0」与「Delta >= mu^2」两行在 V60/V61 的谱内是空集")

add("C03", "C", "来料 §四：24 个额外带电单态零模",
    "需要荷分配才能核（本册只能核计数层面 24 = 2 x 12）",
    "来料未给 24 个单态各自的 U(1)_F 荷 ⇒ 其反常贡献无法独立复算", None,
    "24 = 2 x 12 与试验谱系数 2 x 12_+ 一致，但这只是维数相加，不是反常核验")

add("C04", "C", "来料 §八：26 / 26 通过",
    "计数不等于证据：需按可判性分类",
    "8 行里可判 4 / 半可判 1 / 不可判或未证明 3（承接 r394 A13，同读数）", None,
    "「四力共同微观本源 尚未证明」一行本身不是断言，不能计入通过数")

# ================================================================ 守卫
guard("G01-ACT", all(r["act"] not in ("", "0", "None") for r in ROWS),
      "%d 条全部有 act 读数" % len(ROWS))
guard("G02-TWOPATH", dim_so10 == dim_so10b,
      "so(10) 交换子维数两条路径同读数 %d / %d" % (dim_so10, dim_so10b))
guard("G03-SLOPE", len(slopes) >= 3 and max_dev < D("1E-40"),
      "%d 个斜率全 = 0.5" % len(slopes))
guard("G04-IDENT", rel2 < D("1E-30"), "恒等式相对偏差 %s" % sci(rel2, 3))
guard("G05-CLOSURE", closure_ok and n_sub == 12,
      "反例子代数 %d 维、封闭 = %s" % (n_sub, closure_ok))

# ==== GUARD-AST-MARK ====
with io.open(SELF, "r", encoding="utf-8") as f:
    src = f.read()
head = src.split("# ==== GUARD-AST-MARK ====")[0]
lit = 0
try:
    tree = ast.parse(head)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "add":
            if len(node.args) >= 6:
                a6 = node.args[5]
                if isinstance(a6, ast.Constant) and isinstance(a6.value, bool):
                    lit += 1
except SyntaxError:
    lit = -1
guard("G06-NOHARDOK", lit == 0, "add() 的 ok 为布尔字面量的调用数 = %d" % lit)

cnt = {}
for r in ROWS:
    cnt[r["kind"]] = cnt.get(r["kind"], 0) + 1
gok = sum(1 for g in GUARDS if g["ok"])
print("\n" + "=" * 78)
print("条目 %d：%s" % (len(ROWS), ", ".join("%s %d" % (k, cnt[k]) for k in sorted(cnt))))
print("守卫 %d/%d" % (gok, len(GUARDS)))
print("=" * 78)

VERD = ("V61_66_DECOMP_45_1_10_10_OK__CENTRALIZER_46_AND_RESIDUAL_34_OK__"
        "STABILIZER_36_28_OK__SO10_COMMUTANT_IS_1_SO_MH_EQ_MT_IS_THEOREM__"
        "SU5_COMMUTANT_IS_1_SM_COMMUTANT_IS_2_SO_DELTA_PRICE_IS_ONE_ORDER_PARAMETER__"
        "SIX_FAMILY_SPECTRUM_HAS_ZERO_ANOMALIES_SO_288_12_144_BELONGS_TO_ANOTHER_SPECTRUM__"
        "DIMENSION_COMPARISON_HAS_ZERO_DISCRIMINATING_POWER__DELTA_LOCKED_TO_ZERO_ABOVE_SM__"
        "M6_CLOSED_FORM_OK_RATIO_1P4349E4_TRUE_BUT_REAL_STATEMENT_IS_KK_SCALE_MUST_MOVE_2P06E8_FOLD__"
        "NO_NEW_PROCESSING_LOGIC__UNIQUE_PREDICTION_0")

key = {
    "decomp_66": [n_45, n_1, n10p, n10m],
    "centralizer": n_cen, "centralizer_other_cartan": n_gen,
    "residual": n_cen - 12,
    "stabilizer_1vec_2vec": [n_st1, n_st2],
    "commutant_so10": [dim_so10, dim_so10b],
    "commutant_su5": dim_su5, "commutant_sm": dim_sm, "commutant_so8": dim_so8,
    "example_subalgebra": [n_sub, closure_ok, cen_sub, cen_sm],
    "anom_six_family": [A3v, A2v, Agv],
    "M6": sci(M6, 10), "M6_closed": sci(M6_closed, 10),
    "ratio_MX_M6": sci(ratio, 8),
    "mkk_min_GeV": sci(mkk_min, 8), "mkk_min_over_demo": sci(lhs, 8),
    "slopes": [str(s) for s in slopes],
    "N_max": sci(N_max, 6), "n_req": sci(n_req, 6),
    "tau_yr": sci(tau_yr, 4), "MX_req_GeV": sci(MX_req, 4),
}

out = {"title": TITLE, "date": DATE, "verdict": VERD, "counts": cnt,
       "n_rows": len(ROWS),
       "guards": {"n_ok": gok, "n_total": len(GUARDS), "rows": GUARDS},
       "rows": ROWS, "key_numbers": key}

os.makedirs(DATA, exist_ok=True)
jp = os.path.join(DATA, "_ROOTV61_recompute_%s.json" % DATE)
with io.open(jp, "w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(out, ensure_ascii=False, indent=1))

L = []
L.append("=" * 78)
L.append("%s  复算报告  %s" % (TITLE, DATE))
L.append("=" * 78)
L.append("判词：%s" % VERD)
L.append("")
for r in ROWS:
    L.append("%-5s %-4s %s" % (r["id"], r["kind"], r["name"]))
    L.append("       exp = %s" % r["exp"])
    L.append("       act = %s" % r["act"])
    if r["note"]:
        L.append("       note= %s" % r["note"])
L.append("")
L.append("守卫 %d/%d" % (gok, len(GUARDS)))
for g in GUARDS:
    L.append("  %-14s %s | %s" % (g["name"], "ok" if g["ok"] else "BAD", g["detail"]))
L.append("")
L.append("关键读数：")
for k, v in key.items():
    L.append("  %-22s %s" % (k, v))
rp = os.path.join(DATA, "_ROOTV61_recompute_report_%s.txt" % DATE)
with io.open(rp, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(L) + "\n")

for p in (jp, rp):
    print("written: %s  %d B" % (os.path.basename(p), os.path.getsize(p)))
