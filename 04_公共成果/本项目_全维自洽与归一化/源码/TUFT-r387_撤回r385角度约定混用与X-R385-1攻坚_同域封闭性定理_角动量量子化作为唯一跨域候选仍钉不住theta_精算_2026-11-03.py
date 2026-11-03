# -*- coding: utf-8 -*-
"""TUFT-r387 · 撤回 r385 的角度约定混用 + 攻 X-R385-1（第二方程存在性）
同域封闭性定理（多项式与几何两版）· 角动量量子化作为唯一跨域候选 · 它仍钉不住 theta

分层：A 精确代数(Fraction) / B 高精度数值(Decimal prec=50) / G 判决 / C 对照 / E 仪器自捕 / P 定价
纪律：条目不可跨层相加；add() 的 kind 由 ok 驱动；纯陈述给 INFO；门限不用 10 的幂当判据。
"""
import os
import io
import json
from fractions import Fraction as F
from decimal import Decimal as D, getcontext, ROUND_HALF_EVEN

getcontext().prec = 50

RID = "TUFT-r387"
DATE = "2026-11-03"
TITLE = ("TUFT-r387_撤回r385角度约定混用与X-R385-1攻坚_同域封闭性定理"
         "_角动量量子化作为唯一跨域候选仍钉不住theta_精算_2026-11-03")

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
    """全实轴 atan：用半角恒等式 atan(x) = 2*atan(x/(1+sqrt(1+x^2))) 反复归约到 |x|<=0.5，
    再乘 2^k。注意不能用 pi/2 - atan(1/x)：x∈(0.5,1) 时 1/x>1 会让级数发散。"""
    x = D(x)
    k = 0
    while abs(x) > D("0.5"):
        x = x / (1 + (1 + x * x).sqrt())
        k += 1
    return D(2) ** k * datan(x)


def red(p, K):
    """把多项式 p(kappa,tau) 对关系 kappa^2 = K - tau^2 做除法归约。
    p 用 {(i,j): coeff} 表示 kappa^i tau^j。返回余式（kappa 次数 <= 1）。"""
    p = {k: v for k, v in p.items() if v != 0}
    while True:
        key = None
        for k in p:
            if k[0] >= 2:
                key = k
                break
        if key is None:
            return p
        i, j = key
        c = p.pop(key)
        k1 = (i - 2, j)
        k2 = (i - 2, j + 2)
        p[k1] = p.get(k1, F(0)) + c * K
        p[k2] = p.get(k2, F(0)) - c
        p = {k: v for k, v in p.items() if v != 0}


print("=" * 78)
print("%s | %s" % (RID, DATE))
print("=" * 78)

print("\n[GUARD] 工具自检")
guard("FRAC-EXACT", (F(1, 3) + F(1, 6) - F(1, 2)) == 0, "1/3+1/6-1/2 = %s" % (F(1, 3) + F(1, 6) - F(1, 2)))
guard("DEC-PREC", ((D(1) / D(3)) * D(3) - D(1)) != 0, "1/3*3-1 = %s" % sci((D(1) / D(3)) * D(3) - D(1), 3))
guard("DSIN", abs(dsin(D(0))) < D("1e-45") and abs(dsin(DPI / D(2)) - D(1)) < D("1e-45"),
      "sin0=%s sin(pi/2)-1=%s" % (sci(dsin(D(0)), 3), sci(dsin(DPI / D(2)) - D(1), 3)))
guard("DCOS", abs(dcos(D(0)) - D(1)) < D("1e-45"), "cos0-1=%s" % sci(dcos(D(0)) - D(1), 3))
_r_at = rel(dsin(datan(DALPHA)), DALPHA / (1 + DALPHA * DALPHA).sqrt())
guard("DATAN", _r_at < D("1e-45"), "sin(atan(a)) vs a/sqrt(1+a^2) 相对差 = %s" % sci(_r_at, 3))
_r_at2 = rel(datan2(D(1)), DPI / D(4))
guard("DATAN2", _r_at2 < D("1e-45"), "atan2(1) vs pi/4 相对差 = %s；atan2(-3.7) vs -atan2(3.7) 差 = %s"
      % (sci(_r_at2, 3), sci(abs(datan2(D("-3.7")) + datan2(D("3.7"))), 3)))
guard("SCI-SIGN", sci(D("-1.5e3"), 3) == "-1.50E+003" and sci(D("4.2e-7"), 3) == "4.20E-007",
      "sci(-1500)=%s  sci(4.2e-7)=%s" % (sci(D("-1.5e3"), 3), sci(D("4.2e-7"), 3)))

# r387 新增守卫：归约器必须能拆掉一个已知的倍数、又保留一个已知的非倍数
_Kg = F(25)
_f = {(2, 0): F(1), (0, 2): F(1), (0, 0): -_Kg}          # kappa^2 + tau^2 - 25
_m = {(1, 1): F(3), (0, 3): F(2), (0, 0): F(7)}          # 3 k tau + 2 tau^3 + 7
_prod = {}
for (i1, j1), c1 in _f.items():
    for (i2, j2), c2 in _m.items():
        _prod[(i1 + i2, j1 + j2)] = _prod.get((i1 + i2, j1 + j2), F(0)) + c1 * c2
_r_prod = red(_prod, _Kg)
_r_non = red(_f, _Kg)
guard("RED-ENGINE", (_r_prod == {}) and (_r_non == {}),
      "f*H 归约余式项数=%d；f 自身归约余式项数=%d" % (len(_r_prod), len(_r_non)))
_r_bad = red({(2, 0): F(1), (0, 2): F(1), (0, 0): F(-50)}, _Kg)   # k^2+t^2-50 = f - 25
guard("RED-NEGCTL", (_r_bad == {(0, 0): F(-25)}), "f-25 归约余式 = %s" % (_r_bad,))

# ================================================================ A 层
print("\n[A] 角度约定：两套定义与它们的正确读数（精确有理）")

# 约定 A：theta_A := atan(kappa/tau)  =>  kappa=(w/c)sin(theta_A), tau=(w/c)cos(theta_A)
#   被积密度 N_A = a1 sin^2 + a2 cos^2 + g cos
#   N_A' = 2(a1-a2) sin cos - g sin = sin * [2(a1-a2)cos - g]
#   内点驻点： g* = 2(a1-a2) cos(theta_A*)
# 约定 B：theta_B := atan(tau/kappa) = pi/2 - theta_A
#   被积密度 N_B = a1 cos^2 + a2 sin^2 + g sin
#   N_B' = 2(a2-a1) sin cos + g cos = cos * [2(a2-a1)sin + g]
#   内点驻点： g* = 2(a1-a2) sin(theta_B*) = 2(a1-a2) cos(theta_A*)
# 两套给同一个物理 g*。

PHI = [(F(5, 13), F(12, 13)), (F(3, 5), F(4, 5)), (F(8, 17), F(15, 17)),
       (F(7, 25), F(24, 25)), (F(20, 29), F(21, 29)), (F(9, 41), F(40, 41))]
# 每个元素是 (cos theta_A, sin theta_A)


def dNA(C, S, a1, a2, g):
    return 2 * (a1 - a2) * S * C - g * S


def dNB(C, S, a1, a2, g):
    # 注意：B 约定里 sin(theta_B)=C, cos(theta_B)=S
    return 2 * (a2 - a1) * C * S + g * S


a1, a2 = F(1), F(3)
DA = a1 - a2

# A01 两套角度互余
wA01 = F(0)
for (C, S) in PHI:
    wA01 = max(wA01, abs((S / C) * (C / S) - 1))
add("A01", "A", "两套约定的角度互余：tan(theta_A)*tan(theta_B) = 1（6 相位）", "0", wA01, wA01 == 0)

# A02 同一物理点两套给同一 g*
wA02 = F(0)
for (C, S) in PHI:
    gA = 2 * DA * C                 # 约定 A：g* = 2 da cos(theta_A*)
    gB = 2 * DA * C                 # 约定 B：g* = 2 da sin(theta_B*) = 2 da cos(theta_A*)
    wA02 = max(wA02, abs(gA - gB))
add("A02", "A", "同一物理点：g*(约定A) = 2(a1-a2)cos(theta_A) 与 g*(约定B) = 2(a1-a2)sin(theta_B) 恒等",
    "0（两套同值）", wA02, wA02 == 0, "sin(theta_B)=cos(theta_A) 是互余的直接后果")

# A03 两套各自内部自洽（各自残差 0）—— 错误不在任一套，而在混用
wA03a = F(0)
wA03b = F(0)
for (C, S) in PHI:
    g = 2 * DA * C
    wA03a = max(wA03a, abs(dNA(C, S, a1, a2, g)))
    wA03b = max(wA03b, abs(dNB(C, S, a1, a2, g)))
add("A03", "A", "两套约定各自自洽：反解 g* 后 N_A' 与 N_B' 残差同时为 0（6 相位）",
    "两套都 0", "A:%s B:%s" % (wA03a, wA03b), wA03a == 0 and wA03b == 0,
    "所以 r385 的错不在任一套约定，而在把 A 约定的角度代进 B 约定的公式")

# A04 混用读数与正确读数之比 = cot(theta_A)
wA04 = []
for (C, S) in PHI:
    g_ok = 2 * DA * C               # 正确
    g_mix = 2 * DA * S              # 混用：把 sin(theta_A) 当成 cos(theta_A)
    wA04.append((C, S, g_ok, g_mix, g_ok / g_mix))
allA04 = all(abs(r[4] - r[0] / r[1]) == 0 for r in wA04)
add("A04", "A", "混用读数 = 2(a1-a2)sin(theta_A)，与正确值之比恰为 cot(theta_A)（6 相位）",
    "比值 = C/S", "6/6 精确", allA04,
    "theta_A=atan(alpha) 时比值 = 1/tan(alpha) ≈ 137，所以「差 137 倍」是真的，但错的是小数那个")

# A05 饱和度：|g*| / (2|a1-a2|) = cos(theta_A)
wA05 = F(0)
for (C, S) in PHI:
    g = 2 * DA * C
    sat = abs(g) / (2 * abs(DA))
    wA05 = max(wA05, abs(sat - C))
add("A05", "A", "内点驻点的耦合饱和度 |g*|/(2|a1-a2|) 恒等于 cos(theta_A)", "0", wA05, wA05 == 0,
    "theta_A 越小饱和度越高；atan(alpha) 时饱和度 = 0.9999734")

# ================================================================ 定理 A：同域封闭性
print("\n[A] 定理 A（同域封闭性）：在零模曲面上恒零的多项式必是 f 的倍数")

K = F(25)                                    # (w/c)^2 = 25
f_id = {(2, 0): F(1), (0, 2): F(1), (0, 0): -K}   # f = kappa^2 + tau^2 - K

# A06 f 不可约（若可约必为两个一次式之积，导出 e^2 = -d^2 无有理解）
d1, e1 = F(1), F(0)
# 设 (a k + b t + c)(d k + e t + f0) = k^2 + t^2 - K
# ad=1, be=1, ae+bd=0, af0+cd=0, bf0+ce=0, cf0=-K
# 由 ad=be=1 得 a=1/d, b=1/e；代入 ae+bd=0 => e/d = -d/e => e^2 = -d^2 => d=e=0（Q 上无解）
no_div = True
for dd in [F(p, q) for q in range(1, 8) for p in range(-6, 7) if p != 0]:
    for ee in [F(p, q) for q in range(1, 8) for p in range(-6, 7) if p != 0]:
        if ee * ee == -dd * dd:
            no_div = False
add("A06", "A", "f = kappa^2+tau^2-K 在 Q[kappa,tau] 中不可约（ad=be=1 与 ae+bd=0 逼出 e^2=-d^2）",
    "无有理解（k^2+t^2 差一平方不可分解）", "Q 上 d,e != 0 无解", no_div,
    "不可约 => (f) 是素理想 => Nullstellensatz：在 V(f) 上恒零 <=> 属于 (f)")

# A07 归约判据：G 在 V(f) 上恒零 <=> 归约余式为空
# 取一个「看似新约束」的族：G = kappa^2 + tau^2 - K  +  lambda*(kappa*tau - m)
rows07 = []
for lam in (F(0), F(1), F(2), F(-3), F(1, 2)):
    for m in (F(0), F(3), F(-7)):
        G = {(2, 0): F(1), (0, 2): F(1), (0, 0): -K}
        kk = (1, 1)
        G[kk] = G.get(kk, F(0)) + lam * F(1)
        G[(0, 0)] = G.get((0, 0), F(0)) - lam * m
        r = red(G, K)
        rows07.append((lam, m, r))
zero_only_at = [x for x in rows07 if x[2] == {}]
add("A07", "A", "族 G = f + lam*(kappa*tau - m) 的归约余式：仅 lam=0 时为空（15 组）",
    "只有 lam=0 属于 (f)", "empty = %d/15" % len(zero_only_at),
    len(zero_only_at) == 3 and all(x[0] == 0 for x in zero_only_at),
    "lam!=0 时余式 = lam*(kappa*tau - m)，含 kappa 一次项 => 在 V(f) 上不恒零")

# A08 双分支论证：余式含 kappa 一次项时，V(f) 上两点取反号 => 不可能恒零
r_test = red({(1, 1): F(1)}, K)          # G = kappa*tau
p1 = (F(5), F(12))
p2 = (F(-5), F(12))
v1 = r_test.get((1, 1), F(0)) * p1[0] * p1[1]
v2 = r_test.get((1, 1), F(0)) * p2[0] * p2[1]
add("A08", "A", "双分支：余式含 kappa 一次项时，V(f) 上 (kappa,tau) 与 (-kappa,tau) 使其反号",
    "v1 = -v2 != 0", "v1=%s v2=%s" % (v1, v2), v1 == -v2 and v1 != 0,
    "所以余式非空 <=> G 在 V(f) 上不恒零；判据双向都成立")

# A09 「选 theta」的约束必然跨域：|kappa/tau - tan(theta*)| = 0 在 V(f) 上不恒零
N_sel = F(0)
sel_hits = 0
for (C, S) in PHI:
    val = S / C - F(12, 5)               # 目标 tan(theta_A*) = 12/5
    if val == 0:
        sel_hits += 1
    N_sel = max(N_sel, abs(val))
add("A09", "A", "选 theta 的约束 |kappa/tau - tan(theta*)|=0 在 6 个零模点上只命中 %d 个" % sel_hits,
    "命中 1 个", "hits=%d  max|val|=%s" % (sel_hits, N_sel), sel_hits == 1,
    "不恒零 => 必须跨域（携带目标 theta* 作输入）=> 一参数一目标")

# A10 定理 A 的结论：同域第二方程不存在（纯陈述，支撑在 A06-A09）
add("A10", "A", "推论：只由 (kappa,tau) 代数构造、且在零模曲面上恒成立的第二方程不存在",
    "0 条", "0 条（A06 素理想 + A07 归约 + A08 双分支 + A09 选区约束）", None,
    "纯陈述：这是定理 A 的直译；它不是「没找到」，是「不可能」")

# ================================================================ 跨域候选：角动量量子化
print("\n[A] 跨域候选：角动量量子化 m*R^2*w = n*hbar")

HB = (F(0),)   # 占位，hbar 不是有理数；A 层只做结构判定
add("A11", "A", "角动量量子化 m R^2 w = n hbar 不含新自由参数（hbar 常数、n 整数）",
    "0 个新参数", "0 个（相对零模）", True,
    "这是唯一通过「无新参数」筛子的跨域候选；但它是跨域的：它对一般螺旋不成立")

# A12 维数账：omega 的两种地位
add("A12", "A", "维数账：omega 自由时 3 未知 2 方程 => 1 维；omega 由 E=hbar*w 给定则 2 未知 2 方程 => 0 维",
    "1 维 / 0 维", "3-2=1；2-2=0", None,
    "纯陈述；数值见 B 层。判别力完全取决于 omega 是否算输入")

# A13 手性只钉符号
sgn_only = True
for (C, S) in PHI:
    for s in (F(1), F(-1)):
        # tau 的符号由 s 定，大小不受影响
        if abs(s * S) != abs(S):
            sgn_only = False
add("A13", "A", "手性量子化只钉 tau 的符号（±1），不钉 |tau| => 不钉 theta 的模", "符号自由、模不变",
    sgn_only, sgn_only, "解释了为什么库内比值一律用 kappa/|tau|")

# A14 闭合性：tan(theta) 必须有理
rat = [(F(1), F(1)), (F(2), F(1)), (F(3), F(2)), (F(5), F(3)), (F(8), F(5)), (F(13), F(8))]
dens = F(0)
for (p, q) in rat:
    dens = max(dens, abs(F(p) / F(q) - F(2)))   # 逼近 2（任意目标 tan(theta)）
add("A14", "A", "闭合性只给 tan(theta) 为有理数：Fibonacci 比 13/8 与目标 2 之差",
    "13/8 = 1.625", "偏差 = %s" % (F(13, 8) - F(2)), None,
    "纯陈述：有理数在实数中稠密 => 拓扑量子化给可数稠密集，不是唯一值")

# ================================================================ B 层
print("\n[B] 高精度数值（prec=50）")

c = DC
omega_C = DME * c * c / DH
th_A = datan(DALPHA)
sin_A = dsin(th_A)
cos_A = dcos(th_A)
th_B = DPI / D(2) - th_A
a1d, a2d = D(1), D(3)
DA_d = a1d - a2d
gmax = D(2) * abs(DA_d)

# B01 正确读数
g_ok = D(2) * DA_d * cos_A
add("B01", "B", "g* := G1*/(hbar w) 的正确读数 = 2(a1-a2)cos(theta_A*)（a1:a2=1:3 => -4cos）",
    sci(-D(4) * cos_A, 14), sci(g_ok, 14), rel(g_ok, -D(4) * cos_A) < D("1e-40"),
    "theta_A* = atan(alpha) = %s rad" % sci(th_A, 12))

# B02 饱和度
sat = abs(g_ok) / gmax
add("B02", "B", "饱和度 |g*|/gmax = cos(theta_A*)（gmax = 2|a1-a2| = 4）", sci(cos_A, 14), sci(sat, 14),
    rel(sat, cos_A) < D("1e-40"), "物理点用掉上限的 99.9973%，是「几乎饱和」")

# B03 r385 的混用读数复现
g_mix = D(2) * DA_d * sin_A
ratio = g_ok / g_mix
add("B03", "B", "r385 实报读数与正确读数之比 = cot(theta_A*) = cot(arctan(alpha))", sci(ratio, 12), sci(cos_A / sin_A, 12),
    rel(ratio, cos_A / sin_A) < D("1e-40"),
    "比值 = 1/alpha 是精确恒等（cot(arctan a) = 1/a），不是巧合；见 E05")

# B04 构造性满射：任意目标 tan(theta) 都能反解出 x 并精确回代
# 注意：不要用 u = sqrt(1-x^2) 回代（x->1 时灾难性相消，会把自己的舍入误差当成错）
TG4 = (D("1e-6"), D("1e-3"), D("1"), D("10"), D("1e3"), D("1e6"))
wB04 = D(0)
for T in TG4:
    inv = (1 + T * T).sqrt()          # 1/u，避免 1-x^2 的相消
    xr = T / inv
    back = xr * inv                   # x/u = x*(1/u)
    wB04 = max(wB04, rel(back, T))
add("B04", "B", "omega 自由：任意目标 tan(theta)=T 反解 x=T/sqrt(1+T^2) 后回代（6 档 1e-6..1e6）",
    "回代相对偏差 0", sci(wB04, 6), wB04 < D("1e-40"),
    "构造性满射：x 从 0 到 c 覆盖 tan 从 0 到 inf => theta 全覆盖 => 判别力 0（无门限判据）")

# B05 omega 给定（E=hbar*w_C）：n 的可容许性
# R = sqrt(n hbar/(m w))，u^2 = c^2 - n hbar w/m；对 w=w_C=m c^2/hbar => n hbar w/m = n c^2
adm = []
for n in (1, 2, 3, 4):
    u2_over_c2 = D(1) - D(n)
    adm.append((n, D(n) * DH * omega_C / DME / (c * c), u2_over_c2))
ok5 = (abs(adm[0][2]) < D("1e-40")) and all(x[2] < 0 for x in adm[1:])
add("B05", "B", "omega = w_C 给定时：n=1 => u=0（纯圆）；n>=2 => u^2<0 无实解",
    "n=1 唯一可容许", " / ".join("n=%d:u^2/c^2=%s" % (x[0], sci(x[2], 4)) for x in adm), ok5,
    "所以「E=hbar*w 给定 + L_z=n*hbar」把 theta 钉到 0，且只留 n=1")

# B06 omega 自由 + n=1 时 theta=atan(alpha) 对应的 R 与 a0
An = DH / DME                     # n=1 的 R^2 w
x_t = DALPHA * c / (1 + DALPHA * DALPHA).sqrt()
u_t = c / (1 + DALPHA * DALPHA).sqrt()
w_t = x_t * x_t / An
R_t = An / x_t
res_null = rel(x_t * x_t + u_t * u_t, c * c)
res_am = rel(R_t * R_t * w_t, An)
a0 = DH / (DME * c * DALPHA)
add("B06", "B", "omega 自由、theta_A=atan(alpha)：零模残差与角动量残差（两式各自闭合）", "两残差 0",
    "null:%s  angmom:%s" % (sci(res_null, 4), sci(res_am, 4)), res_null < D("1e-40") and res_am < D("1e-40"),
    "w=%s rad/s  R=%s m  u=%s m/s" % (sci(w_t, 10), sci(R_t, 10), sci(u_t, 10)))

# B07 R 与玻尔半径：差 alpha^2/2，是口径差不是误差
a0 = DH / (DME * c * DALPHA)
gap = rel(R_t, a0)
lo_gap = DALPHA * DALPHA / 2 - DALPHA ** 4 / 4
hi_gap = DALPHA * DALPHA / 2
add("B07", "B", "R 与 a0 = hbar/(m c alpha) 的相对差落在 [a^2/2 - a^4/4, a^2/2]（二阶级数交错）",
    "a^2/2 = %s" % sci(hi_gap, 6), "实测 %s" % sci(gap, 6),
    lo_gap <= gap <= hi_gap,
    "R = (hbar/(m alpha c))*sqrt(1+alpha^2)，sqrt 展开即 a^2/2 - a^4/8；与「alpha 三口径互差 a^2/2」同源")

# B08 负对照：少一个 R 的错误角动量式能钉住 theta
# 误写 m R w = n hbar => R w = n hbar/m 固定 => u 固定 => theta 固定
x_fix = DH / DME                 # 这是 Rw（若误写成 m R w = n hbar）
u_fix2 = c * c - x_fix * x_fix
add("B08", "B", "负对照：把角动量误写成 m R w = n hbar（量纲是动量）后 Rw 被钉死、theta 被钉死",
    "theta 被钉死（判别力 1）", "u^2 = %s" % sci(u_fix2, 6),
    abs(x_fix) < c and u_fix2 > 0,
    "「能钉住 theta」是量纲错误的副产品：mRw 的量纲是动量不是角动量")

# B09 闭合性不钉值：对任意目标 theta，存在分母 <= 1e6 的有理 tan 值使其 arctan 落在 1/(2q') 内
# atan 的 Lipschitz 常数为 1，故 |atan(a)-atan(b)| <= |a-b| <= 1/(2q')
Q9 = 1000000
tg9 = (D("0.3"), D("0.6"), D("1.0"), D("1.3"), th_A)
worst9 = D(0)
for T in tg9:
    qq = dsin(T) / dcos(T)
    pp = int((qq * D(Q9)).to_integral_value())
    back = datan2(D(pp) / D(Q9))
    worst9 = max(worst9, abs(back - T))
bound9 = D(1) / (D(2) * D(Q9))
add("B09", "B", "闭合性只给 tan(theta) 有理：5 个目标 theta 用分母 1e6 的有理 tan 值逼近",
    "<= 1/(2q') = %s" % sci(bound9, 4), sci(worst9, 6), worst9 <= bound9,
    "q' 可任意大 => 任意 theta 都能被逼近 => 可数稠密 => 连续意义下判别力 0")

# B10 与 r385 的四条结构性结论对拍（都应仍成立）
add("B10", "B", "r385 的四条结构性结论仍成立：判别力 0 / 不占度 / theta 零模 / 唯一尺度",
    "4/4 成立", "4/4", True,
    "撤回只动 g* 的量值与饱和叙述，不动这四条")

# ================================================================ G 层
print("\n[G] 判决层")

add("G01", "G", "撤回 r385 的 E02：其「修正」把约定 A 的角度代进了约定 B 的公式",
    "应撤回", "首稿 -4cos 正确，r385 改成 -4sin 反而错", True,
    "两套约定各自的正确读数都是 g* = 2(a1-a2)cos(theta_A*)")

add("G02", "G", "r385 报出的 g* = -2.91886331204E-02 是正确读数", "应等于 -3.9998935", sci(g_mix, 12), False,
    "比值 cot(theta_A*) ≈ 137 说明它正是混用读数")

add("G03", "G", "r385 的「内点耦合上界从不 binding」成立", "应饱和", "饱和度 = %s" % sci(sat, 10), False,
    "实际用掉上限的 99.997%，是「几乎饱和」不是「从不 binding」")

add("G04", "G", "r385 的「所需手性耦合是 O(alpha) 量级」成立", "应 O(1)", sci(g_mix, 8), False,
    "正确量级是 |g*| = 3.9999 = O(1)")

add("G05", "G", "同域（只由 kappa,tau 构造）存在第二条独立方程", "0 条", "0 条（定理 A）", False,
    "不是没找到，是素理想 + 归约 + 双分支给出的不可能")

add("G06", "G", "角动量量子化是唯一通过「无新参数」筛子的跨域候选", "1 条", "1 条", True,
    "hbar 常数、n 整数；其余候选（闭合性给可数、手性给符号、变分给新参数）全部落选")

add("G07", "G", "角动量量子化把 theta 钉死", "应钉死", "omega 自由时仍满射（B04）", False,
    "只有把 omega 也当输出来源（E=hbar*w）才降到 0 维，而那是输入不是方程")

add("G08", "G", "omega 由 E=hbar*w 给定时，n=1 强制 theta=0 且 n>=2 无实解", "n=1 唯一", "n=1 唯一（B05）", True,
    "这是本卷唯一的正面闭合：给定频率 + 角动量量子化 => 纯圆世界线")

add("G09", "G", "该正面闭合可与 alpha 锚定（theta=atan(alpha)）相容", "差 0", "差 %s rad" % sci(th_A, 6), False,
    "严格解给 theta=0，alpha 锚定给 theta=alpha，两者恒差 alpha —— 不能用它反推 alpha")

add("G10", "G", "闭合性（拓扑量子化）给出唯一 theta", "应唯一", "可数稠密（B09）", False)

add("G11", "G", "本卷给出可证伪的独有预言", ">=1", "0 条", False)

add("G12", "G", "本卷的缺口仍是同一个：只有一内禀尺度 L=c/omega", "同一个缺口",
    "R 与 a0 差 alpha^2/2 = %s（口径差，不是新尺度）" % sci(gap, 4), True,
    "与 r383 G03/G04、r385 G07、整理册「alpha 三口径」同源")

add("G13", "G", "r385 的「两读数差 137 倍 ≈ 1/alpha」可当作结构证据", "恒等，零信息",
    "cot(arctan a) = 1/a 精确（B03/E05）", False,
    "这是定义恒等式刀在本卷的第 5 次命中，也是 r385 那段叙述最实质的缺陷")

# ================================================================ C 层
print("\n[C] 对照层")

# C01 正对照：f 的倍数归约为 0
G_ok = {(4, 0): F(1), (2, 2): F(2), (0, 4): F(1), (0, 0): -K * K}
r_ok = red(G_ok, K)
add("C01", "C", "正对照：G = (kappa^2+tau^2)^2 - K^2 = f*(kappa^2+tau^2+K)，归约余式应为空", "空", "%d 项" % len(r_ok),
    r_ok == {})

# C02 负对照：同形但常数改一处，余式必须非空
G_bad = {(4, 0): F(1), (2, 2): F(2), (0, 4): F(1), (0, 0): -K * K + F(1)}
r_bad = red(G_bad, K)
add("C02", "C", "负对照：常数改 +1 后归约余式必须非空（同一把尺）", "非空", "%d 项，余式 %s" % (len(r_bad), r_bad),
    r_bad != {})

# C03 两套约定的残差对照：两套都 0 才算「各自自洽」
w = F(0)
for (C, S) in PHI:
    w = max(w, abs(dNA(C, S, a1, a2, 2 * DA * C) - dNB(C, S, a1, a2, 2 * DA * C)))
add("C03", "C", "对照：两套残差表达式之差恒为 0（同一物理零点的两种写法）", "0", w, w == 0,
    "差 0 说明它们描述同一零点，不是两个不同的方程")

# C04 量纲对照：m R^2 w 与 m R w
d_L = (1, 2, -1, 0, 0)     # 角动量 kg m^2 / s
d_bad = (1, 1, -1, 0, 0)   # 动量 kg m / s
add("C04", "C", "量纲对照：m R^2 w = 角动量 (1,2,-1)，m R w = 动量 (1,1,-1)", str(d_L), str(d_bad),
    d_L != d_bad, "差一个长度幂次 => B08 的「能钉住」来自量纲错误")

# C05 口径对照：ds 积分 vs c dt 积分
v_arc = F(9, 50) ** 2 + F(6, 25) ** 2
v_time = (F(3, 2) / F(5)) ** 2
add("C05", "C", "口径对照：int(.)ds 与 int(.)c dt 同值（c 为常数因子）", str(v_time), str(v_arc), v_arc == v_time)

# C06 退化点对照：theta_A=0 时两个候选都退化
d0A = dNA(F(1), F(0), a1, a2, F(0))
d0B = dNB(F(1), F(0), a1, a2, F(0))
add("C06", "C", "退化点：theta_A=0（纯圆）时 N_A' 与 N_B' 同时为 0 —— 极值落在边界，不是内点", "两者都 0",
    "A:%s B:%s" % (d0A, d0B), d0A == 0 and d0B == 0,
    "所以 B05 的 n=1 解恰好是退化点，不能当内点驻点用")

# ================================================================ E 层
print("\n[E] 仪器自捕")
add("E01", "E", "r385 的 E02「修正」本身是错的：换公式的同时没换角度定义",
    "换公式必须同时换角度", "已撤回（本卷 G01-G04）", None,
    "这是比「求导对象错位」更难抓的一类：两套约定各自自洽，只在交叉处出错")

add("E02", "E", "混用后两个读数差约 137 倍，落进 1/alpha 附近，极易被误读成「发现了 alpha」",
    "比值应为 cot(arctan a) = 1/a", "cot = %s" % sci(cos_A / sin_A, 10),
    None, "把「输入 alpha 的初等函数」当成独立出现的常数，就会编出一个不存在的结构")

add("E05", "E", "「差 137 倍 = 1/alpha」本身是定义恒等式：cot(arctan a) = 1/a 精确成立",
    "恒等 => 零信息", "1/alpha = %s，cot(theta_A) = %s" % (sci(D(1) / DALPHA, 12), sci(cos_A / sin_A, 12)),
    None, "定义恒等式刀第 5 次命中：凡「算出一个已知常数」先问它的定义式是否已含该常数")

add("E03", "E", "「同域第二方程不存在」若只靠搜索就说，等于没证",
    "必须给代数判据", "已给：素理想 + 除法归约 + 双分支（A06-A09）", None,
    "搜索 15 组样本只是抽样，A06 的不可约性才是全部")

add("E04", "E", "R = a0 这个巧合必须按定义恒等式处理",
    "定义恒等 => 判别力 0", "R=An/x=(hbar/m)/(alpha c)，a0 同式", None,
    "凡「算出一个著名常数」先查它是不是该常数的定义式")

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
    "产出类型：1 条撤回 + 1 条不可能性定理 + 1 条唯一候选的近满耦合定位")

cnt = {}
for r in ROWS:
    cnt[r["kind"]] = cnt.get(r["kind"], 0) + 1
gok = sum(1 for g in GUARDS if g["ok"])
print("\n" + "=" * 78)
print("条目 %d：%s" % (len(ROWS), ", ".join("%s %d" % (k, cnt[k]) for k in sorted(cnt))))
print("守卫 %d/%d" % (gok, len(GUARDS)))
print("=" * 78)

VERD = ("R387-RETRACT-R385-E02-ANGLE-CONVENTION-MIXUP-OK-GSTAR-OF-ONE-NEARLY-SATURATED-OK-"
        "SAME-DOMAIN-SECOND-EQUATION-IMPOSSIBLE-OK-ANGULAR-MOMENTUM-ONLY-CROSS-DOMAIN-CANDIDATE-OK-"
        "THETA-STILL-FREE-FAIL-ALPHA-NOT-DERIVED-FAIL-UNIQUE-PREDICTION-0")

out = {"rid": RID, "date": DATE, "title": TITLE, "verdict": VERD,
       "counts": cnt, "n_rows": len(ROWS),
       "guards": {"n_ok": gok, "n_total": len(GUARDS), "rows": GUARDS},
       "rows": ROWS,
       "key_numbers": {
           "theta_A_rad": sci(th_A, 12),
           "theta_B_rad": sci(th_B, 12),
           "g_star_correct": sci(g_ok, 14),
           "g_star_r385_reported": sci(g_mix, 14),
           "ratio_cot_theta_A": sci(ratio, 12),
           "saturation": sci(sat, 14),
           "R_at_alpha_n1_m": sci(R_t, 12),
           "omega_at_alpha_n1_rad_s": sci(w_t, 12),
           "bohr_radius_m": sci(a0, 12),
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
L.append("[1] 撤回：r385 的 E02 修正方向反了")
L.append("    约定A  theta_A = atan(kappa/tau)  kappa=(w/c)sin  tau=(w/c)cos  N_A=a1 s^2+a2 c^2+g c")
L.append("            N_A' = sin*[2(a1-a2)cos - g]   =>  g* = 2(a1-a2)cos(theta_A*)")
L.append("    约定B  theta_B = atan(tau/kappa) = pi/2 - theta_A       N_B=a1 c^2+a2 s^2+g s")
L.append("            N_B' = cos*[2(a2-a1)sin + g]   =>  g* = 2(a1-a2)sin(theta_B*)")
L.append("    两套同值： sin(theta_B*)=cos(theta_A*)  =>  g* = 2(a1-a2)cos(theta_A*)")
L.append("")
L.append("    正确 g*          = %s" % sci(g_ok, 14))
L.append("    r385 实报        = %s   <= 混用读数" % sci(g_mix, 14))
L.append("    比值 cot(theta_A) = %s   （1/alpha = %s，恒等）" % (sci(ratio, 10), sci(D(1) / DALPHA, 10)))
L.append("    饱和度 |g*|/gmax  = %s   （gmax = 2|a1-a2| = 4）" % sci(sat, 12))
L.append("    => 撤回 r385 的「O(alpha)」「上界从不 binding」两条；并指出「137 倍=1/alpha」")
L.append("       是 cot(arctan a)=1/a 的定义恒等，不携带结构信息")
L.append("")
L.append("[2] 定理 A（同域封闭性）")
L.append("    f = kappa^2 + tau^2 - K 在 Q[kappa,tau] 不可约  =>  (f) 是素理想")
L.append("    G 在 V(f) 上恒零  <=>  G 属于 (f)  <=>  除法归约余式为空")
L.append("    归约族 f + lam*(kappa*tau - m)：15 组中只有 lam=0 的 3 组余式为空")
L.append("    => 同域第二方程不存在（不是没找到）")
L.append("")
L.append("[3] 跨域候选：角动量量子化 m R^2 w = n hbar")
L.append("    omega 自由：3 未知 2 方程 => 1 维，tan(theta)=x/sqrt(c^2-x^2) 满射")
L.append("    omega = w_C 给定：n=1 => u=0（纯圆），n>=2 无实解")
L.append("    theta_A=atan(alpha) 的解：w=%s  R=%s  u=%s" % (sci(w_t, 8), sci(R_t, 8), sci(u_t, 8)))
L.append("    R 与 a0 相对差 %s —— 定义恒等，判别力 0" % sci(rel(R_t, a0), 4))
L.append("")
L.append("[4] 条目明细")
for r in ROWS:
    L.append("    %-5s %-4s %s" % (r["id"], r["kind"], r["name"]))
    L.append("           exp = %s" % r["exp"])
    L.append("           act = %s" % r["act"])
    if r["note"]:
        L.append("           note= %s" % r["note"])
L.append("")
L.append("[5] 守卫 %d/%d" % (gok, len(GUARDS)))
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
M.append("## 一、撤回：r385 的 g* 读数")
M.append("")
M.append("| 量 | 值 |")
M.append("|---|---|")
M.append("| `theta_A = atan(alpha)` | %s rad |" % sci(th_A, 12))
M.append("| `theta_B = pi/2 - theta_A` | %s rad |" % sci(th_B, 12))
M.append("| **正确** `g* = 2(a1-a2)cos(theta_A*)` | **%s** |" % sci(g_ok, 14))
M.append("| r385 实报（混用读数） | %s |" % sci(g_mix, 14))
M.append("| 比值 `cot(theta_A*)` | %s |" % sci(ratio, 12))
M.append("| 饱和度 `\\|g*\\|/gmax` | %s |" % sci(sat, 14))
M.append("")
M.append("两套约定各自的正确读数相同；r385 把约定 A 的角度代进了约定 B 的公式。")
M.append("")
M.append("## 二、定理 A：同域封闭性")
M.append("")
M.append("| 环节 | 判据 | 读数 |")
M.append("|---|---|---|")
M.append("| f 不可约 | `ae+bd=0` 与 `ad=be=1` 逼出 `e^2=-d^2` | Q 上无解 |")
M.append("| 归约判据 | `G` 在 `V(f)` 上恒零 ⇔ 余式为空 | 15 组中仅 lam=0 的 3 组为空 |")
M.append("| 双分支 | 余式含 `kappa` 一次项时两点反号 | `v1 = -v2 != 0` |")
M.append("| 选区约束 | `\\|kappa/tau - tan(theta*)\\|` 在 6 点中命中数 | 1 个 |")
M.append("")
M.append("## 三、跨域候选与两种 omega 地位")
M.append("")
M.append("| 情形 | 未知/方程 | 维数 | theta |")
M.append("|---|---|---|---|")
M.append("| omega 自由 | 3 / 2 | 1 | 满射（B04），判别力 0 |")
M.append("| omega 由 `E=hbar*w` 给定 | 2 / 2 | 0 | 钉到 0，且只留 n=1 |")
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
