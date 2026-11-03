# -*- coding: utf-8 -*-
"""TUFT-r389 · 攻 X-R387-2：手性耦合量子化能否定出 theta
「整数比搬家」定理 · 稠密集判负 · N >= 1/alpha^2 阈值 · 精确匹配不可能

分层：A 精确代数(Fraction) / B 高精度数值(Decimal prec=50) / G 判决 / C 对照 / E 仪器自捕 / P 定价
纪律：条目不可跨层相加；add() 的 kind 由 ok 驱动；纯陈述给 INFO；门限禁用 10 的幂当判据。
"""
import os
import io
import json
from math import gcd
from fractions import Fraction as F
from decimal import Decimal as D, getcontext, ROUND_HALF_EVEN

getcontext().prec = 50

RID = "TUFT-r389"
DATE = "2026-11-03"
TITLE = ("TUFT-r389_攻XR387-2_手性耦合量子化不能定出theta_整数比搬家定理"
         "_稠密集与万级整数阈值与精确匹配不可能_精算_2026-11-03")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "数据")

ROWS = []
GUARDS = []


def add(rid, layer, name, exp, act, ok, note=""):
    if ok is None:
        kind = "INFO"
    elif ok:
        kind = "PASS"
    else:
        kind = "FAIL"
    ROWS.append({"id": rid, "layer": layer, "name": name, "exp": str(exp),
                 "act": str(act), "kind": kind, "note": note})
    print("  [%-4s] %-5s %s" % (kind, rid, name))
    return ok


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": str(detail)})
    print("  [GUARD %-4s] %-10s | %s" % ("ok" if ok else "BAD", name, detail))
    return ok


DC = D("299792458")
DH = D("1.054571817e-34")
DME = D("9.1093837015e-31")
DALPHA = D("0.0072973525693")
DPI = D("3.14159265358979323846264338327950288419716939937510")


def sci(x, nd=10):
    if x == 0:
        return "0"
    x = D(x)
    sgn = "-" if x < 0 else ""
    e = 0
    ax = abs(x)
    while ax >= 10:
        ax /= 10
        e += 1
    while ax < 1:
        ax *= 10
        e -= 1
    return "%s%sE%+04d" % (sgn, format(ax, ".%df" % (nd - 1)), e)


def rel(a, b):
    return abs(a - b) / (abs(b) if b != 0 else D(1))


def dsin(x):
    tp = D(2) * DPI
    k = (x / tp).to_integral_value(rounding=ROUND_HALF_EVEN)
    x = x - k * tp
    if x > DPI:
        x -= tp
    if x < -DPI:
        x += tp
    term = x
    s = x
    n = 1
    while True:
        term = -term * x * x / (D(2 * n) * D(2 * n + 1))
        s += term
        n += 1
        if abs(term) < D("1e-48"):
            break
    return s


def dcos(x):
    return dsin(x + DPI / D(2))


def datan(x):
    x = D(x)
    s = D(0)
    p = x
    k = 0
    while True:
        t = p / D(2 * k + 1)
        s = s + t if k % 2 == 0 else s - t
        p = p * x * x
        k += 1
        if abs(t) < D("1e-48"):
            break
    return s


def datan2(x):
    """全实轴 atan：半角恒等式归约到 |x|<=0.5（不能用 pi/2-atan(1/x)，x∈(0.5,1) 时发散）"""
    x = D(x)
    k = 0
    while abs(x) > D("0.5"):
        x = x / (1 + (1 + x * x).sqrt())
        k += 1
    return D(2) ** k * datan(x)


def darcsin(x):
    """asin，含 |x|=1 端点（1-x^2 = 0 会让除零）"""
    x = D(x)
    if x * x == 1:
        return DPI / D(2) if x > 0 else -DPI / D(2)
    return datan2(x / (1 - x * x).sqrt())


def dacos1m(u):
    """arccos(1-u) 的稳定算法：2*asin(sqrt(u/2))，避免 x->1 处相消（u 必须是精确量）"""
    return D(2) * darcsin((D(u) / D(2)).sqrt())


def darccos(x):
    return DPI / D(2) - darcsin(x)


print("=" * 78)
print("%s | %s" % (RID, DATE))
print("=" * 78)

print("\n[GUARD] 工具自检")
guard("FRAC-EXACT", (F(1, 3) + F(1, 6) - F(1, 2)) == 0, "1/3+1/6-1/2 = %s" % (F(1, 3) + F(1, 6) - F(1, 2)))
guard("DEC-PREC", ((D(1) / D(3)) * D(3) - D(1)) != 0, "1/3*3-1 = %s" % sci((D(1) / D(3)) * D(3) - D(1), 3))
guard("DSIN", abs(dsin(D(0))) < D("1e-45") and abs(dsin(DPI / D(2)) - D(1)) < D("1e-45"),
      "sin0=%s sin(pi/2)-1=%s" % (sci(dsin(D(0)), 3), sci(dsin(DPI / D(2)) - D(1), 3)))
_r_at = rel(dsin(datan(DALPHA)), DALPHA / (1 + DALPHA * DALPHA).sqrt())
guard("DATAN", _r_at < D("1e-45"), "sin(atan(a)) vs a/sqrt(1+a^2) 相对差 = %s" % sci(_r_at, 3))
leg = D("0.6")
guard("DATAN2", rel(datan2(leg), DPI / D(2) - datan2(D(1) / leg)) < D("1e-45") and
      rel(datan2(D(1)), DPI / D(4)) < D("1e-45"),
      "atan2(0.6)+atan2(1/0.6)-pi/2 = %s ; atan2(1)-pi/4 = %s"
      % (sci(datan2(leg) + datan2(D(1) / leg) - DPI / D(2), 3), sci(datan2(D(1)) - DPI / D(4), 3)))
_s = D("0.3")
guard("DASIN", rel(dcos(darcsin(_s)), (1 - _s * _s).sqrt()) < D("1e-45"),
      "cos(asin 0.3) vs sqrt(1-0.09) 相对差 = %s" % sci(rel(dcos(darcsin(_s)), (1 - _s * _s).sqrt()), 3))
guard("SCI-SIGN", sci(D("-1.5e3"), 3) == "-1.50E+003" and sci(D("4.2e-7"), 3) == "4.20E-007",
      "sci(-1500)=%s  sci(4.2e-7)=%s" % (sci(D("-1.5e3"), 3), sci(D("4.2e-7"), 3)))

# ================================================================ A 层
print("\n[A] 角度约定沿用 r387 的约定 A：theta_A = atan(kappa/tau)，tan(theta_A) = kappa/tau")
print("    内点驻点（r387 A02）：g* = N cos(theta_A)，其中 N := 2(a1-a2)")
print("    r387 已撤回混用版；本卷一切公式按约定 A 写。")

N_SYM = F(5)          # 先取一个有理的 N = 2(a1-a2)，a1=4, a2=3/2 -> N=5
thA_loc = datan(DALPHA)          # 物理点 theta_A = atan(alpha)，A/B 层共用
a2d = DALPHA * DALPHA

# ---- 量纲代数：(M, L, T, Q, Theta) 五元组，只用原语做加法 ----
D_HBAR = (1, 2, -1, 0, 0)
D_OMEGA = (0, 0, -1, 0, 0)
D_C = (0, 1, -1, 0, 0)
D_R = (0, 1, 0, 0, 0)
D_ENERGY = (1, 2, -2, 0, 0)


def dadd(*ds):
    return tuple(sum(d[i] for d in ds) for i in range(5))


def dsub(a, b):
    return tuple(a[i] - b[i] for i in range(5))


# A01 g 的量纲必须与候选 E0 相同（否则 g=n*E0 非法）
d_g = D_ENERGY                                   # g = N cos(theta)，N = 2(a1-a2)，a1/a2 是能量系数
d_E1 = dadd(D_HBAR, D_OMEGA)                     # hbar*w
d_E2 = dadd(dadd(D_HBAR, D_C), tuple(-x for x in D_R))   # hbar*c/R
add("A01", "A", "g 的量纲 = 能量；两种候选 E0 = hbar*w 与 hbar*c/R 也都是能量 ⇒ g=n*E0 合法",
    "E0 两者都 = %s" % (D_ENERGY,), "hbar*w = %s ; hbar*c/R = %s ; g = %s" % (d_E1, d_E2, d_g),
    d_E1 == d_g and d_E2 == d_g, "量纲只筛掉非法组合，不区分两种选法（见 C03 负对照）")


# A02 两种自然 E0 给出的 g 互不相同（比值恰好 1/cos(theta_A)）
ratioA02 = D(1) / dcos(thA_loc)
add("A02", "A", "两种自然能量单位：(i) E0=hbar*w ⇒ g=n；(ii) E0=hbar*c/R（唯一内禀长度）⇒ g=n*c/(R*w)=n/cos(theta_A)",
    "g_ii/g_i = 1", "1/cos(theta_A) = %s ⇒ 偏离 1 达%s" % (sci(ratioA02, 12), sci(abs(ratioA02 - D(1)), 3)),
    abs(ratioA02 - D(1)) > 0,
    "(ii) 用到 R*w = c*cos(theta_A)（零模 + 约定 A）；两选法只在 theta→0 时合并")


# A03 两种情形各自的方程（Fraction 精确回代：n1/N 与 C 相等、n2/N 与 C^2 相等）
w1A03 = F(0)
w2A03 = F(0)
rows03 = []
for (C, S) in ((F(5, 13), F(12, 13)), (F(3, 5), F(4, 5)), (F(12, 37), F(35, 37))):
    n1 = N_SYM * C               # (i)  n = N*C   =>  C = n/N
    n2 = N_SYM * C * C           # (ii) n = N*C^2 =>  C^2 = n/N
    rows03.append((C, S, n1, n2))
    w1A03 = max(w1A03, abs(n1 / N_SYM - C))
    w2A03 = max(w2A03, abs(n2 / N_SYM - C * C))
add("A03", "A", "情形(i)：n = N cos(theta_A) ⇒ cos(theta_A)=n/N；情形(ii)：n/cos = N cos ⇒ cos^2(theta_A)=n/N",
    "(i) 残差 0 ; (ii) 残差 0", "(i) %s ; (ii) %s" % (w1A03, w2A03), w1A03 == 0 and w2A03 == 0,
    "两式的解都是 cos 的有理（或有理平方根）表达，3 组相位精确回代")


# A04 两种情形归一到同一集合：tan^2(theta_A) ∈ Q
wA04 = F(0)
cnt04 = 0
for (C, S) in ((F(5, 13), F(12, 13)), (F(3, 5), F(4, 5)), (F(12, 37), F(35, 37)), (F(20, 29), F(21, 29))):
    # 情形(i): C = n/N  => tan^2 = (S/C)^2 = (N/n)^2 - 1  ∈ Q
    t2_i = (N_SYM / (N_SYM * C)) ** 2 - 1
    # 情形(ii): C^2 = n/N => tan^2 = N/n - 1 ∈ Q
    t2_ii = N_SYM / (N_SYM * C * C) - 1
    if t2_i.denominator == 1 or t2_i.denominator != 1:
        cnt04 += 1
    wA04 = max(wA04, abs(t2_i - (S / C) ** 2))
    wA04 = max(wA04, abs(t2_ii - (S / C) ** 2))
add("A04", "A", "两种量子化都归一到同一集合：tan^2(theta_A) ∈ Q（4 组相位，两式各自回代）",
    "tan^2 精确等于 (S/C)^2", "max|res| = %s" % wA04, wA04 == 0,
    "所以 S = {arctan(sqrt(q)) : q ∈ Q, q>=0} 就是量子化允许的全部 theta")

# A05 N 固定时谱有限：n = 0..N
Nsmall = 10
spec = [F(k, Nsmall) for k in range(0, Nsmall + 1)]
add("A05", "A", "N 固定为整数时 cos(theta_A)=n/N 只给 N+1 个值（N=%d 枚举）" % Nsmall,
    "%d 个值" % (Nsmall + 1), "%d 个值" % len(spec), len(spec) == Nsmall + 1,
    "有限谱 = 真钉住；但前提是 N 被独立固定")

# A06 空隙恒等式 k = 2N sin^2(theta/2) 本身是**半角恒等式**（定义级、零信息）；
#     有内容的是「k 必须取整数」⇒ 最小非零谱角由 k=1 反解：theta_min(N) = 2*asin(1/sqrt(2N))
wA06 = D(0)
for Nb in (3, 7, 100, 18780):
    th_min = D(2) * darcsin(D(1) / (D(2) * D(Nb)).sqrt())
    back = D(2) * D(Nb) * dsin(th_min / D(2)) ** 2       # 回代应恰为 k=1
    wA06 = max(wA06, abs(back - D(1)))
add("A06", "A", "空隙反解：k = 2N sin^2(theta/2) 反解出最小非零谱角 theta_min(N)=2*asin(1/sqrt(2N))，回代 k=1",
    "回代 k = 1", "max|2N sin^2(theta_min/2) - 1| = %s（N=3/7/100/18780）" % sci(wA06, 4),
    wA06 < D("1e-42"),
    "注意：恒等式本身是半角恒等式（定义级、零信息）；有内容的是 k 只能取整数 ⇒ theta 谱离散")



# A07 谱空隙：N < 1/alpha^2 <=> theta_min(N) > theta_A <=> 谱在 (0, theta_A) 内为空
cnt07 = 0
det07 = []
for Nb in (1, 10, 100, 1000, 18778):
    th_min = D(2) * darcsin(D(1) / (D(2) * D(Nb)).sqrt())
    if D(Nb) * a2d < 1 and th_min > thA_loc:
        cnt07 += 1
    det07.append("N=%d:%.2f" % (Nb, float(th_min / thA_loc)))
add("A07", "A", "空隙判据：N*alpha^2 < 1 ⇔ theta_min(N) > theta_A ⇔ 谱在 (0,theta_A) 内无点（N=1/10/100/1000/18778）",
    "5/5 谱在 (0,theta_A) 内为空", "%d/5 ; theta_min/theta_A = %s" % (cnt07, " ".join(det07)), cnt07 == 5,
    "alpha 落在第一个空隙里 —— 这就是「小 theta 需要万级 N」的几何含义")


# A08 精确匹配不可能：N = n(1+alpha^2) 是整数 ⇔ (q/gcd(p,q)) | n
#     口径自守：alpha 用 CODATA 定点值 72973525693/10^13（这是实测值，不是精确常数）
numA, denA = 72973525693, 10 ** 13
a2q = F(numA, denA) ** 2
pA, qA = a2q.numerator, a2q.denominator
gA = gcd(pA, qA)
need = qA // gA
notint = sum(1 for n in range(1, 11) if (n * (1 + a2q)).denominator != 1)
needS = "10^26" if need == 10 ** 26 else str(need)
add("A08", "A", "精确匹配 cos^2(theta_A)=1/(1+alpha^2) 需 N=n(1+alpha^2) 为整数 ⇔ (q/gcd) | n",
    "n 必须是 %s 的倍数" % needS, "alpha 定点值的平方：分母 = %s、gcd = %d ⇒ 需 n 是 %s 的倍数 ; n=1..10 全非整数 (%d/10)"
    % ("10^26", gA, needS, notint), need == 10 ** 26 and notint == 10,
    "口径自守：alpha 是实测定点值（十进制表示是约定）⇒ 本条的「不可能」只在用给定有效位数的 alpha 时成立")


# A09 手性：sign(g) = sign(N)，逐组核算（4 组）
cntA09 = 0
totA09 = 0
for (C, S) in ((F(5, 13), F(12, 13)), (F(3, 5), F(4, 5)), (F(12, 37), F(35, 37)), (F(20, 29), F(21, 29))):
    for Ns in (F(5), F(-5)):
        totA09 += 1
        gs = Ns * C
        if (gs > 0) == (Ns > 0):
            cntA09 += 1
add("A09", "A", "手性由 sign(N) 决定：g* = N cos(theta_A) 与 N 同号 ⇒ 拓扑荷不提供手性信息",
    "%d/%d 同号" % (totA09, totA09), "%d/%d 同号" % (cntA09, totA09), cntA09 == totA09,
    "量子化只给「荷有多大」，不给「往哪边」—— 手性仍是 sign(N) 的输入")


add("A10", "A", "推论：量子化把「连续自由参数 theta」换成「整数比 n/N」，判别力取决于 N 是否被独立钉住",
    "条件性", "见 A05 与 B 层", None, "纯陈述：这是本卷全部结论的骨架")

# ================================================================ B 层
print("\n[B] 高精度数值（prec=50）")

c = DC
alpha = DALPHA
a2 = alpha * alpha
inv_a2 = D(1) / a2
th_A = datan(alpha)
cosA = dcos(th_A)
sinA = dsin(th_A)

# B01 物理点
add("B01", "B", "物理点（theta_A = atan(alpha)）：cos^2 与 sin^2 的读数", "cos^2 = 1/(1+a^2)",
    "cos^2=%s  sin^2=%s" % (sci(cosA * cosA, 10), sci(sinA * sinA, 10)),
    rel(cosA * cosA, 1 / (1 + a2)) < D("1e-40"), "sin^2 与 a^2 的相对差 = %s" % sci(rel(sinA * sinA, a2), 4))

# B02 精确匹配所需的连续 N
add("B02", "B", "精确匹配所需的连续 N（情形 ii：cos^2=n/N，取 n=1）", "1/(1+a^2)", sci(1 / (1 + a2), 12),
    None, "这个数略小于 1，离整数 1 差 a^2 = %s；所以 n=1 时 N 必须略大于 1（非整数）" % sci(a2, 6))

# B03 靶心：由 cos^2 = 1-1/N 解出 N* = 1/alpha^2 + 1，再扫描三个相邻整数取最优
Nstar = inv_a2 + D(1)
n0 = int(Nstar.to_integral_value(rounding=ROUND_HALF_EVEN))
best = None
for Nn in (n0 - 1, n0, n0 + 1):
    th = darcsin(D(1) / D(Nn).sqrt())      # 解 sin^2 = 1/N（即空隙 k=N-n=1）
    e = abs(th - th_A)
    if best is None or e < best[2]:
        best = (Nn, th, e)
add("B03", "B", "空隙 k=N-n=1 的靶心：N* = 1/alpha^2+1（由 1-1/N = 1/(1+alpha^2) 反解），扫描 N*-1,N*,N*+1",
    "解析靶心最近整数 = %d" % n0,
    "N* = %s ⇒ 最近整数 %d ; 扫描最优 N=%d  |dtheta|=%s"
    % (sci(Nstar, 12), n0, best[0], sci(best[2], 6)), best[0] == n0,
    "N* 是 alpha 的函数、不是理论产出 —— 「整数比搬家」的直接证据")

# B04 偏差与解析界：dtheta/dN = -1/(2N^{3/2})，|dN|<=1/2 ⇒ |dtheta| <= 1/(4*N^{3/2})
bound04 = D(1) / (D(4) * (D(n0) ** 3).sqrt())
add("B04", "B", "靶心整数点的偏差与解析界：dtheta/dN = -1/(2N^{3/2}) 且 |dN|<=1/2 ⇒ |dtheta| <= 1/(4N^{3/2})",
    sci(bound04, 6),
    sci(best[2], 6), best[2] < bound04,
    "相对偏差 |dtheta|/theta_A = %s ⇒ 单靠「取最近整数」只到 1e-6 相对精度"
    % sci(best[2] / th_A, 4))

# B05 偏差对 N 的依赖是 V 形（唯一极小在靶心），不是单调下降
gridB05 = (1000, 10000, 18779, 18780, 100000, 1000000, 10000000)
rowsB05 = []
for Nn in gridB05:
    th = darcsin(D(1) / D(Nn).sqrt())
    rowsB05.append((Nn, abs(th - th_A)))
Lft = rowsB05[:3]        # 1000 / 10000 / 18779 均 < N*
Rgt = rowsB05[3:]        # 18780 / 1e5 / 1e6 / 1e7 均 > N*
monoL = all(Lft[i + 1][1] < Lft[i][1] for i in range(len(Lft) - 1))
monoR = all(Rgt[i + 1][1] > Rgt[i][1] for i in range(len(Rgt) - 1))
minat = Rgt[0][1] < Lft[-1][1]
add("B05", "B", "|dtheta| 对 N 是 V 形（唯一极小在靶心 N*）：左侧严格递减、右侧严格递增、极小在 %d" % n0,
    "V 形（左 3/3 递减、右 4/4 递增、极小在 %d）" % n0,
    " ".join("N=%d:%s" % (x[0], sci(x[1], 3)) for x in rowsB05), monoL and monoR and minat,
    "首版断言「N 越大越准」是错的：N 超过靶心后偏差回升 ⇒ 不是「随便放大 N」")

# B06 小整数 N 的谱完全够不着
rowsB06 = []
for Nb in (1, 2, 3, 5, 10):
    th = darcsin(D(1) / D(Nb).sqrt())
    rowsB06.append((Nb, th, th / th_A))
allbig = all(x[2] > D(10) for x in rowsB06)
add("B06", "B", "小整数 N=1,2,3,5,10 时最小非零 theta = asin(1/sqrt(N))，与 theta_A 的倍数", "全部 >> 1",
    " ; ".join("N=%d:%.3f倍" % (x[0], float(x[2])) for x in rowsB06), allbig,
    "小 N 的谱点比 alpha 大一到两个量级，根本不在同一区域")

# B07 阈值：asin(1/sqrt(N)) <= theta_A 当且仅当 N >= 1/alpha^2
thrD = inv_a2
add("B07", "B", "阈值：asin(1/sqrt(N)) <= theta_A 当且仅当 N >= 1/alpha^2", "N >= 1/alpha^2",
    "1/alpha^2 = %s" % sci(thrD, 12), thrD > D(18778) and thrD < D(18780),
    "所以「量子化能给出物理量级的小 theta」本身要求 N 是万级整数")

# B08 N 自由时稠密：取 sin^2(theta_A)（不是 alpha^2！）的最佳有理逼近，偏差远小于 1/(4*alpha*N)
sin2A = sinA * sinA
offset_naive = darcsin(alpha) - th_A      # 误用 alpha^2 当靶会引入的假偏差
rowsB08 = []
for mden in (10 ** 5, 10 ** 7, 10 ** 9):
    fr = F(sin2A).limit_denominator(mden)       # k/N 是 sin^2(theta_A) 的最佳有理逼近
    kk, Nn = fr.numerator, fr.denominator
    th = darcsin((D(kk) / D(Nn)).sqrt())
    rowsB08.append((Nn, kk, abs(th - th_A)))
downB08 = all(rowsB08[i + 1][2] < rowsB08[i][2] for i in range(2))
boundB08 = all(x[2] < D(1) / (D(4) * alpha * D(x[0])) for x in rowsB08)
add("B08", "B", "N 自由时取 sin^2(theta_A) 的最佳有理逼近 k/N（连分数）：偏差远小于四舍五入界 1/(4*alpha*N) ⇒ 稠密、判别力 0",
    "3/3 远低于解析界且严格下降",
    " ".join("k=%d/N=%d:d=%s (界 %s)" % (x[1], x[0], sci(x[2], 3), sci(D(1) / (D(4) * alpha * D(x[0])), 3))
             for x in rowsB08),
    downB08 and boundB08,
    "任一精度都可达、N 只要百万级 ⇒ 同 r387「构造性满射」。靶必须是 sin^2(theta_A)：误用 alpha^2 会引入 arcsin(alpha)-arctan(alpha)=%s 的假偏差（α 三口径刀第 4 次命中）"
    % sci(offset_naive, 4))

# B09 与 r387 对拍（第三条独立路径：r387 用 A/B 两套约定各算一次）
gg = -D(4) * dcos(thA_loc)          # a1:a2 = 1:3 ⇒ N = 2(1-3) = -4 ⇒ g* = N cos
add("B09", "B", "与 r387 对拍：N=-4（a1:a2=1:3）时 g* = N cos(theta_A*)", "-3.9998935015443（r387 读数）",
    sci(gg, 12), rel(gg, D("-3.9998935015443")) < D("1e-12"),
    "跨卷独立性：本卷用约定 A 直接算，与 r387 两套约定的结果三者一致")

# B10 有限谱的分辨率标度 gap(N) ∝ N^{-1/2}（用稳定算法，且用比值判幂次而非等差）
rowsB10 = []
for Nn in (10 ** 4, 10 ** 6, 10 ** 8):
    gap = D(2) * darcsin(D(1) / D(Nn).sqrt()) - D(2) * darcsin(D(1) / (D(2) * D(Nn)).sqrt())
    rowsB10.append((Nn, gap))
ratiosB10 = [(rowsB10[i + 1][1] / rowsB10[i][1]) for i in range(2)]
add("B10", "B", "有限谱分辨率：零点附近最小谱间距 gap(N)=2[asin(1/sqrt N)-asin(1/sqrt 2N)] ∝ N^{-1/2}",
    "N 涨 100 倍 ⇒ 比值 = 0.1（两档）",
    " ".join("N=%s:gap=%s ratio=%s" % (sci(D(x[0]), 1), sci(x[1], 6),
                                       ("—" if i == 0 else sci(ratiosB10[i - 1], 6)))
             for i, x in enumerate(rowsB10)),
    all(abs(r - D("0.1")) < D("1e-3") for r in ratiosB10),
    "定到 1e-9 需 N ~ 3e17 ⇒ 有限谱虽「真钉住」，代价天文数字（用比值判幂次，不用等差）")


# ================================================================ G 层
print("\n[G] 判决层")

add("G01", "G", "手性耦合量子化能定出唯一 theta", "1 个点",
    "只给 tan^2(theta) ∈ Q（A04）；N 自由时偏差随 N 十年一档降一个量级（B08）", False,
    "可数稠密集，不是单点：离散 ≠ 有限")

add("G02", "G", "判别力取决于 N = 2(a1-a2) 是否被独立钉住", "是",
    "N 固定 ⇒ %d 个分立值（A05，N=10）; N 自由 ⇒ 稠密（B08）" % (Nsmall + 1), True,
    "同一条量子化，两种命运 —— 分岔点不在物理，在「分母有没有被钉住」")

add("G03", "G", "N 能被框架内生", "应内生", "r385/r387 已证 a1,a2 无内生来源 ⇒ N 无来源", False,
    "本卷只是把缺口从 theta 挪到 N，没有补上")

minratio = min(x[2] for x in rowsB06)
add("G04", "G", "小整数 N 能给出 theta ~ alpha", "应能给",
    "最小非零 theta 仍比 theta_A 大 %.1f 倍（B06，N=10）" % float(minratio), False,
    "小 N 谱完全不在物理量级上")

add("G05", "G", "量子化谱中存在精确等于 arctan(alpha) 的点", "应存在",
    "需 n 是 10^26 的倍数（A08，CODATA 定点口径）", False,
    "用给定有效位数的 alpha 时精确解不存在；但 alpha 是实测量 ⇒ 本条只在定点口径下成立")

add("G06", "G", "量子化把 alpha 搬到 N 上（整数比搬家）", "是",
    "靶心 N* = 1/alpha^2+1 = %s ⇒ 最近整数 %d（B03）" % (sci(Nstar, 10), best[0]), True,
    "输入总数不减少：theta 的自由度换成了 N 的自由度，而 N 由 alpha 反解")

add("G07", "G", "本卷给出可证伪的独有预言", ">=1", "0 条", False,
    "唯一的「预言」是 N* 的数值，而 N* 是 alpha 的算式 ⇒ 定义恒等式刀")

add("G08", "G", "X-R387-2 可关闭：量子化路线判负（条件性）", "关闭",
    "关闭，条件 =「N 无内生来源」这一条保持", True,
    "若将来 N 被独立钉住（例如 a1,a2 由拓扑整数给出），本卷结论自动失效并需重开")

# ================================================================ C 层
print("\n[C] 对照层")

# C01 正对照：情形(i) 与情形(ii) 在同一相位上给同一 tan^2
C1, S1 = F(5, 13), F(12, 13)
t2a = (N_SYM / (N_SYM * C1)) ** 2 - 1
t2b = N_SYM / (N_SYM * C1 * C1) - 1
add("C01", "C", "正对照：两种量子化在同一相位给同一 tan^2（不是巧合，都是 (S/C)^2）", str((S1 / C1) ** 2),
    "i:%s  ii:%s" % (t2a, t2b), t2a == t2b and t2a == (S1 / C1) ** 2,
    "两式形式不同、集合相同 ⇒ 归约成立")

# C02 负对照：去掉 n 的整性，有限谱立刻失效
spec10 = set(F(k, Nsmall) for k in range(0, Nsmall + 1))
cnt02 = 0
vals02 = []
for nn in (F(5, 2), F(13, 3), F(37, 10)):
    cval = nn / Nsmall
    if cval not in spec10:
        cnt02 += 1
    vals02.append("n=%s⇒cos=%s" % (nn, cval))
add("C02", "C", "负对照：若 n 允许非整数（去掉量子化），N=10 的有限谱立刻失效 —— 有限性完全来自 n∈Z",
    "3/3 落在谱外", "%d/3 ; %s" % (cnt02, " ".join(vals02)), cnt02 == 3,
    "所以 A05 的「N+1 个值」不是形式的产物，是「n 与 N 都是整数」这条的产物")

# C03 量纲负对照：漏掉 c 的 E0 被量纲直接排除
d_bad = dadd(D_HBAR, tuple(-x for x in D_R))          # hbar/R
add("C03", "C", "量纲负对照：E0 取 hbar/R（漏掉 c）给 %s，不是能量 ⇒ 该选法被量纲排除" % (d_bad,),
    "不是能量 %s" % (D_ENERGY,), "hbar/R = %s" % (d_bad,), d_bad != D_ENERGY,
    "量纲只能筛非法项；hbar*w 与 hbar*c/R 都合法（A01）⇒ 判据在数值后果，不在量纲")

# C04 退化点：theta=0 是所有 N 共享的唯一谱点
cnt04 = 0
tot04 = 0
for Nb in (1, 5, 10, 1000):
    tot04 += 1
    if darcsin(D(0)) == 0:
        cnt04 += 1
add("C04", "C", "退化点：k=N-n=0 给 theta=0，是**所有** N 共享的唯一谱点", "%d/%d 个 N 含 theta=0" % (tot04, tot04),
    "%d/%d 个 N 含 theta=0" % (cnt04, tot04), cnt04 == tot04,
    "量子化能无歧义定出的只有 theta=0（纯圆）；物理点不是它 ⇒ 判别力 0")

# C05 口径对照：约定 B 重算 g*，与约定 A 同值（r387 A02 的复现）
thB = DPI / D(2) - thA_loc                 # 约定 B：theta_B = pi/2 - theta_A
gB = -D(4) * dsin(thB)                     # g* = N sin(theta_B)
add("C05", "C", "口径对照：约定 B（theta_B=pi/2-theta_A, g*=N sin theta_B）重算 g*，与约定 A 同值",
    "-3.9998935015443", sci(gB, 12), rel(gB, gg) < D("1e-40"),
    "r387 A02 的对拍在本卷复现：两套约定内部自洽，交叉处必须给同一读数")

# C06 负对照：错版恒等式 k = N sin^2(theta) 不成立（本卷首版的原话）
wC06 = F(0)
for (Cv, Sv) in ((F(5, 13), F(12, 13)), (F(3, 5), F(4, 5)), (F(12, 37), F(35, 37))):
    kk = N_SYM - N_SYM * Cv
    wC06 = max(wC06, abs(kk - N_SYM * Sv * Sv))
add("C06", "C", "负对照：错版「k = N sin^2(theta)」不成立（本卷首版就是这么写的）", "残差应 > 0",
    "max|k - N sin^2| = %s" % wC06, wC06 > 0,
    "证明 A06 的正版检验有判别力；同时记录本卷第一处自伤")

# ================================================================ E 层
print("\n[E] 仪器自捕")
add("E01", "E", "首版把「量子化 ⇒ 离散 ⇒ 能定值」当作链条，漏了「分母是否固定」这一步",
    "离散 ≠ 有限", "已改：A05（N 固定）与 B08（N 自由）分开判", None,
    "离散但无限 = 可数稠密 = 判别力 0；这是「退化点恒绿」的近亲")

add("E02", "E", "首版断言「N 越大越准」，被 B05 的 V 形否掉：N 超过靶心后偏差回升",
    "单调下降", "已改：B05 拆成左侧递减/右侧递增/极小在靶心三条", None,
    "凡「越大越准」的直觉，先问目标函数在哪个方向取极小")

add("E03", "E", "首版把靶心整数写成 18779：两处错 ——(a) 漏了 arcsin 的立方项；(b) 把 sin^2(theta_A) 当成 alpha^2",
    "N* = 1/alpha^2（错）", "已改：N* = 1/alpha^2+1 = %s ⇒ 最近整数 %d" % (sci(Nstar, 10), best[0]), None,
    "sin^2(theta_A) = alpha^2/(1+alpha^2)，与 alpha^2 差 alpha^2/2 相对 —— α 三口径刀第三次命中")


# ================================================================ P 层
print("\n[P] 定价")
SLOTS = [("S1", "定出唯一的 theta", False),
         ("S2", "不需要新耦合", False),
         ("S3", "新耦合由框架内生", False),
         ("S4", "给出分立谱", False),
         ("S5", "给出可证伪独有预言", False)]
n_sat = sum(1 for _, _, v in SLOTS if v)
add("P01", "P", "五槽满足数（0 => 不占度）", "0", "%d/5" % n_sat, n_sat == 0, "SURVIVE=%d" % n_sat)
add("P02", "P", "可入池的第一性输出条数", "0", "0", None,
    "产出类型：1 条判负（量子化路线）+ 1 条阈值定量 + 1 条「离散≠有限」方法论")

cnt = {}
for r in ROWS:
    cnt[r["kind"]] = cnt.get(r["kind"], 0) + 1
gok = sum(1 for g in GUARDS if g["ok"])
print("\n" + "=" * 78)
print("条目 %d：%s" % (len(ROWS), ", ".join("%s %d" % (k, cnt[k]) for k in sorted(cnt))))
print("守卫 %d/%d" % (gok, len(GUARDS)))
print("=" * 78)

VERD = ("R389-CHIRAL-QUANTIZATION-CANNOT-FIX-THETA-OK-DENSE-SET-CANNOT-PIN-OK-"
        "LARGE-N-THRESHOLD-OK-INTEGER-RATIO-RELOCATES-ALPHA-OK-"
        "TARGET-CENTER-NOT-MONOTONE-OK-EXACT-MATCH-IMPOSSIBLE-OK-"
        "N-NOT-INTERNAL-FAIL-UNIQUE-PREDICTION-0")

out = {"rid": RID, "date": DATE, "title": TITLE, "verdict": VERD,
       "counts": cnt, "n_rows": len(ROWS),
       "guards": {"n_ok": gok, "n_total": len(GUARDS), "rows": GUARDS},
       "rows": ROWS,
       "key_numbers": {
           "theta_A_rad": sci(th_A, 12),
           "cos2_physical": sci(cosA * cosA, 12),
           "sin2_physical": sci(sinA * sinA, 12),
           "one_over_alpha2": sci(inv_a2, 12),
           "N_star": sci(Nstar, 12),
           "best_N": best[0],
           "best_theta": sci(best[1], 12),
           "best_dtheta": sci(best[2], 6),
           "best_rel": sci(best[2] / th_A, 6),
           "bound_1over4aN": sci(bound04, 6),
           "min_ratio_smallN": "%.4f" % float(minratio),
           "exact_match_needs_n_multiple_of": str(need),
       }}

os.makedirs(DATA, exist_ok=True)
jp = os.path.join(DATA, "%s.json" % TITLE)
with io.open(jp, "w", encoding="utf-8") as f:
    f.write(json.dumps(out, ensure_ascii=False, indent=1))

L = []
L.append("=" * 78)
L.append("%s  精算报告  %s" % (RID, DATE))
L.append("=" * 78)
L.append("判词：%s" % VERD)
L.append("")
L.append("[1] 问题：g := G1/(hbar*w) 若来自挠率拓扑荷，则量子化；它能否定出 theta_A？")
L.append("    约定 A（与 r387 一致）：tan(theta_A)=kappa/tau，内点驻点 g* = N cos(theta_A)，N:=2(a1-a2)")
L.append("")
L.append("[2] 两种自然的量子化")
L.append("    (i)  E0=hbar*w    => g=n      => n = N cos(theta_A)   => cos(theta_A) = n/N")
L.append("    (ii) E0=hbar*c/R  => g=n/cos  => n = N cos^2(theta_A) => cos^2(theta_A) = n/N")
L.append("    两式都归一到 tan^2(theta_A) ∈ Q（A04，4 组相位精确 0）")
L.append("")
L.append("[3] 关键分岔")
L.append("    N 自由 => 谱 = {arctan(sqrt(q)) : q∈Q} 在 [0,pi/2) 稠密 => 判别力 0（B08，偏差 ~ 1/(4*alpha*N)）")
L.append("    N 固定 => 只剩 N+1 个值 => 真钉住（A05），但分辨率 ~ 1/sqrt(N)（B10）")
L.append("    而 N 无内生来源（r385/r387 已证）=> 缺口只是从 theta 挪到 N（整数比搬家）")
L.append("")
L.append("[4] 数值")
L.append("    theta_A             = %s rad" % sci(th_A, 12))
L.append("    cos^2(theta_A)      = %s" % sci(cosA * cosA, 12))
L.append("    sin^2(theta_A)      = %s   (alpha^2 = %s)" % (sci(sinA * sinA, 12), sci(a2, 12)))
L.append("    1/alpha^2           = %s" % sci(inv_a2, 12))
L.append("    靶心 N* = 1/a^2 + 1 = %s  => 最近整数 %d" % (sci(Nstar, 12), n0))
L.append("    对应 theta          = %s rad" % sci(best[1], 12))
L.append("    |dtheta|            = %s   (相对 %s)" % (sci(best[2], 6), sci(best[2] / th_A, 6)))
L.append("    解析界 1/(4*N^{3/2}) = %s  => 实测在界内" % sci(bound04, 6))
L.append("")
L.append("    V 形：|dtheta| 在 N* 取唯一极小，两侧都变大（B05）—— 不是「N 越大越准」")
L.append("    阈值：小 theta（<= theta_A）要求 N >= 1/alpha^2，且谱在 (0,theta_A) 内为空（A07/B07）")
L.append("    小 N（1..10）的最小非零 theta 至少比 theta_A 大 %.1f 倍（B06）" % float(minratio))
L.append("    精确匹配需 n 是 10^26 的倍数（A08，CODATA 定点口径）")
L.append("")
L.append("[5] 条目明细")
for r in ROWS:
    L.append("    %-5s %-4s %s" % (r["id"], r["kind"], r["name"]))
    L.append("           exp = %s" % r["exp"])
    L.append("           act = %s" % r["act"])
    if r["note"]:
        L.append("           note= %s" % r["note"])
L.append("")
L.append("[6] 守卫 %d/%d" % (gok, len(GUARDS)))
for g in GUARDS:
    L.append("    %-12s %s | %s" % (g["name"], "ok" if g["ok"] else "BAD", g["detail"]))
L.append("")
L.append("条目 %d：%s" % (len(ROWS), cnt))

rp = os.path.join(DATA, "%s_report_%s.txt" % (TITLE, DATE))
with io.open(rp, "w", encoding="utf-8", newline="\r\n") as f:
    f.write("\n".join(L) + "\n")


def esc(s):
    return str(s).replace("|", "\\|")


M = []
M.append("# %s · 数据侧裁定表（%s）" % (RID, DATE))
M.append("")
M.append("> 判词：`%s`" % VERD)
M.append("")
M.append("> 条目 **%d**（%s）；守卫 **%d/%d**。分层 A 精确代数 / B 高精度数值 / G 判决 / C 对照 / E 仪器自捕 / P 定价。**条目不可跨层相加。**"
         % (len(ROWS), " / ".join("%s %d" % (k, cnt[k]) for k in sorted(cnt)), gok, len(GUARDS)))
M.append("")
M.append("## 一、两种量子化与它们的归约")
M.append("")
M.append("| 能量单位 | `g` 的取值 | 方程 | 后果 |")
M.append("|---|---|---|---|")
M.append("| `E0 = hbar*w` | `g = n` | `cos(theta_A) = n/N` | `tan^2(theta_A) in Q` |")
M.append("| `E0 = hbar*c/R` | `g = n/cos(theta_A)` | `cos^2(theta_A) = n/N` | `tan^2(theta_A) in Q` |")
M.append("")
M.append("两式归一到同一个集合 `S = {arctan(sqrt(q)) : q in Q}`。")
M.append("")
M.append("## 二、数值锚点")
M.append("")
M.append("| 量 | 值 |")
M.append("|---|---|")
M.append("| `theta_A` | %s rad |" % sci(th_A, 12))
M.append("| `cos^2(theta_A)` | %s |" % sci(cosA * cosA, 12))
M.append("| `sin^2(theta_A)` | %s |" % sci(sinA * sinA, 12))
M.append("| `alpha^2` | %s |" % sci(a2, 12))
M.append("| `1/alpha^2` | %s |" % sci(inv_a2, 12))
M.append("| 靶心 `N* = 1/alpha^2+1` | %s |" % sci(Nstar, 12))
M.append("| 最近整数 `N`（`k=1`） | %d |" % best[0])
M.append("| 对应 `theta` | %s rad |" % sci(best[1], 12))
M.append("| `\\|dtheta\\|` | %s |" % sci(best[2], 6))
M.append("| 相对偏差 | %s |" % sci(best[2] / th_A, 6))
M.append("| 解析界 `1/(4*N^{3/2})` | %s |" % sci(bound04, 6))
M.append("")
M.append("## 三、靶心是 V 形，不是单调（`B05`）")
M.append("")
M.append("| `N` | `\\|dtheta\\|` | 侧 |")
M.append("|---|---|---|")
for x in rowsB05:
    M.append("| %d | %s | %s |" % (x[0], sci(x[1], 3), "左（`N<N*`）" if x[0] < 18780 else "右（`N>N*`）"))
M.append("")
M.append("`N` 超过靶心后偏差回升 ⇒ 「N 越大越准」是错的；靶心 `N*` 由 `alpha` 反解，不是理论产出。")
M.append("")
M.append("## 四、条目明细")
M.append("")
M.append("| ID | 层 | 裁定 | 条目 | exp | act |")
M.append("|---|---|---|---|---|---|")
for r in ROWS:
    M.append("| %s | %s | **%s** | %s | %s | %s |"
             % (r["id"], r["layer"], r["kind"], esc(r["name"]), esc(r["exp"]), esc(r["act"])))
M.append("")
M.append("## 五、守卫")
M.append("")
M.append("| 守卫 | 结果 | 读数 |")
M.append("|---|---|---|")
for g in GUARDS:
    M.append("| %s | %s | %s |" % (g["name"], "ok" if g["ok"] else "BAD", esc(g["detail"])))
M.append("")
M.append("[返回目录 README](../README.md) · [判定册](../判定/%s.md)" % TITLE)

mp = os.path.join(DATA, "%s_%s.md" % (TITLE, DATE))
with io.open(mp, "w", encoding="utf-8", newline="\r\n") as f:
    f.write("\n".join(M) + "\n")

print("\nwritten:\n  %s\n  %s\n  %s" % (os.path.basename(jp), os.path.basename(rp), os.path.basename(mp)))
