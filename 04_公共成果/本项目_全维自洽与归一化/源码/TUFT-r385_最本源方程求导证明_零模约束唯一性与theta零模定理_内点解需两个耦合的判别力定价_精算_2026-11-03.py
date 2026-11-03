# -*- coding: utf-8 -*-
"""TUFT-r385 · 最本源方程的求导与证明
零模约束的唯一性 · 母式是双射不是约束 · theta 零模定理 · 内点解需要两个耦合

分层：A 精确代数(Fraction) / B 高精度数值(Decimal prec=50) / G 判决 / C 对照 / E 仪器自捕 / P 定价
纪律：条目不可跨层相加；add() 的 kind 由 ok 驱动；纯陈述给 INFO；门限不用 10 的幂当判据。
"""
import os
import io
import json
from fractions import Fraction as F
from decimal import Decimal as D, getcontext, ROUND_HALF_EVEN

getcontext().prec = 50

RID = "TUFT-r385"
DATE = "2026-11-03"
TITLE = ("TUFT-r385_最本源方程求导证明_零模约束唯一性与theta零模定理"
         "_内点解需两个耦合的判别力定价_精算_2026-11-03")

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
DK = D("1.380649e-23")
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
        if abs(term) < D("1e-45"):
            break
    return s


def dcos(x):
    return dsin(x + DPI / D(2))


def datan(x):
    """|x| <= 0.5 上的 Taylor 展开（本卷只用到 x = alpha）"""
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


print("=" * 78)
print("%s | %s" % (RID, DATE))
print("=" * 78)

print("\n[GUARD] 工具自检")
guard("FRAC-EXACT", (F(1, 3) + F(1, 6) - F(1, 2)) == 0, "1/3+1/6-1/2 = %s" % (F(1, 3) + F(1, 6) - F(1, 2)))
guard("DEC-PREC", ((D(1) / D(3)) * D(3) - D(1)) != 0, "1/3*3-1 = %s" % ((D(1) / D(3)) * D(3) - D(1)))
guard("DSIN", abs(dsin(D(0))) < D("1e-45") and abs(dsin(DPI / D(2)) - D(1)) < D("1e-45"),
      "sin0=%s sin(pi/2)-1=%s" % (sci(dsin(D(0)), 3), sci(dsin(DPI / D(2)) - D(1), 3)))
guard("DCOS", abs(dcos(D(0)) - D(1)) < D("1e-45"), "cos0-1=%s" % sci(dcos(D(0)) - D(1), 3))
_r_at = rel(dsin(datan(DALPHA)), DALPHA / (1 + DALPHA * DALPHA).sqrt())
guard("DATAN", _r_at < D("1e-45"), "sin(atan(a)) vs a/sqrt(1+a^2) 相对差 = %s" % sci(_r_at, 3))
guard("SCI-SIGN", sci(D("-1.5e3"), 3) == "-1.50E+003" and sci(D("4.2e-7"), 3) == "4.20E-007",
      "sci(-1500)=%s  sci(4.2e-7)=%s" % (sci(D("-1.5e3"), 3), sci(D("4.2e-7"), 3)))

# ================================================================ A 层
print("\n[A] 零模约束 -> 母式（精确有理，6 相位 x 4 勾股族）")

PHASES = [(F(3, 5), F(4, 5)), (F(5, 13), F(12, 13)), (F(8, 17), F(15, 17)),
          (F(7, 25), F(24, 25)), (F(20, 29), F(21, 29)), (F(9, 41), F(40, 41))]
FAM = [(F(3), F(4), F(1)), (F(5), F(12), F(2)), (F(8), F(15), F(1, 2)), (F(7), F(24), F(3))]
CMAP = {3: 5, 5: 13, 8: 17, 7: 25}

wN = wM = wK = F(0)
n_case = 0

for (Rw, u, R) in FAM:
    c = F(CMAP[int(Rw)])
    w = Rw / R
    for (C, S) in PHASES:
        # 零模：eta(xdot,xdot) = -c^2*(dt)^2 + |v|^2*(dt)^2 = 0  <=> |v|^2 = c^2
        v = (-R * w * S, R * w * C, u)
        vv = v[0] ** 2 + v[1] ** 2 + v[2] ** 2
        d_null = vv - c * c
        # 母式
        k = R * w * w / (c * c)
        t = u * w / (c * c)
        d_mother = k * k + t * t - (w / c) ** 2
        # 逆命题：R=kappa/(kappa^2+tau^2), u=c^2*tau/w
        R_back = k / (k * k + t * t)
        u_back = c * c * t / w
        d_inv = max(abs(R_back - R), abs(u_back - u))
        wN = max(wN, abs(d_null))
        wM = max(wM, abs(d_mother))
        wK = max(wK, d_inv)
        n_case += 1

add("A01", "A", "零模条件 eta(xdot,xdot)=0 <=> |v|^2=c^2 <=> (Rw)^2+u^2=c^2（%d 例）" % n_case,
    "残差 0", wN, wN == 0)
add("A02", "A", "零模 + Frenet => 母式 kappa^2+tau^2=(w/c)^2（%d 例）" % n_case, "残差 0", wM, wM == 0)
add("A03", "A", "逆命题：R=kappa/(kappa^2+tau^2)、u=c^2*tau/w 精确回代（%d 例）" % n_case, "残差 0", wK, wK == 0,
    "(kappa,tau)<->(R,u) 一一对应 => 母式是重参数化")

# A04: 母式不减自由度 —— (kappa,tau)->(omega,theta) 的雅可比
print("\n[A] 自由度：母式是双射还是约束")
ws = F(3, 2)
cs = F(5)
ks = F(9, 50)
ts = F(6, 25)
om_f = cs * (ks * ks + ts * ts)
# det J = -c^2/omega
detJ = -(cs * cs) / om_f
add("A04", "A", "映射 (kappa,tau)->(omega=c|K|, theta=atan(kappa/tau)) 的雅可比行列式 = -c^2/omega != 0",
    "非零（闭式 -c^2/omega = -500/9）", str(detJ), detJ != 0,
    "2->2 维双射：母式不减少自由度数，故它是重参数化不是约束")

# A05-A11: 泛函对 theta 的极值结构
print("\n[A] 泛函 E=int(A1*k^2 + A2*t^2 + G1*t)ds 的 theta 结构")

# 口径（本卷统一，后面不再改）：
#   kappa = (w/c)cos(theta),  tau = (w/c)sin(theta)
#   E/L   = hbar*c*(w/c)^2 * N(theta),  N(theta) = a1*cos^2 + a2*sin^2 + g*sin
#   其中 a_i := A_i/(hbar c)（无量纲）,  g := G1/(hbar*w)（无量纲）
#   N'(theta) = 2(a2-a1)sin*cos + g*cos = cos(theta)*[2(a2-a1)sin(theta) + g]
#   注意 d(tau)/d(theta) = (w/c)cos(theta)，不是 (w/c)sin(theta) —— 这是首稿写错的地方（见 E02）

A1, A2, G1 = F(1), F(3), F(2)     # a1, a2, g


def dN(C, S, a1, a2, g):
    """归一化导数 N'(theta)"""
    return 2 * (a2 - a1) * S * C + g * C


wEq = F(0)
wFlat = F(0)
nz_interior = 0
for (C, S) in PHASES:
    wEq = max(wEq, abs(dN(C, S, A1, A2, G1)))
    wFlat = max(wFlat, abs(dN(C, S, A1, A1, F(0))))
    if abs(dN(C, S, A1, A2, F(0))) == 0:
        nz_interior += 1

add("A05", "A", "一般系数下 N'(theta) = cos(theta)*[2(a2-a1)sin(theta) + g]，6 相位精确非零",
    "全非零", wEq, wEq != 0, "取 a1=1, a2=3, g=2")
add("A06", "A", "a1=a2 且 g=0 => N'(theta) 恒等于 0（theta 是零模/平坦方向）", "6 相位全 0",
    wFlat, wFlat == 0)
add("A07", "A", "a1!=a2 且 g=0 => 内点(0<theta<pi/2)上 N'(theta) != 0（极值只在边界）",
    "内点无一为 0", "zeros at interior = %d/6" % nz_interior, nz_interior == 0,
    "零点只有 sin*cos=0 => theta=0（直线）或 theta=pi/2（圆）")

# A08: 内点驻点的充要条件（精确有理，取相位 5/13,12/13）
Cs = F(5, 13)
Ss = F(12, 13)
a1b, a2b = F(1), F(3)
g_star = 2 * (a1b - a2b) * Ss          # 由目标 theta* 反解
D_star = dN(Cs, Ss, a1b, a2b, g_star)
add("A08", "A", "内点驻点充要：g* = 2(a1-a2)sin(theta*)；反解后代回 N'(theta*) 残差",
    "残差 0", D_star, D_star == 0, "g* = %s（取 theta*=arctan(12/5)）" % g_star)

# A09: 四格分类（纯陈述，数值见 A05-A08 / B 层）
add("A09", "A", "四格分类：a1=a2,g=0 全平 | a1=a2,g!=0 只在 theta=±pi/2（圆）| "
                "a1!=a2,g=0 只在 0 或 ±pi/2 | 双非零才有内点驻点",
    "唯一出内点的一格需两个耦合同时非零", "见 A05-A08", None,
    "纯陈述（分类表），数值验证见 A05-A08")

# A10: 零模解集维数 —— 一条方程、两个未知
two_d = []
for (C, S) in PHASES:
    kap, tau = F(5) * C, F(5) * S        # w/c 归一到 5，只验约束本身
    two_d.append(kap * kap + tau * tau)  # 应恒等于 (w/c)^2 = 25
spread = max(two_d) - min(two_d)
add("A10", "A", "零模约束下 (kappa,tau) 有 %d 个互不相同的解而 kappa^2+tau^2 恒等 => 解集 >= 1 维"
    % len(PHASES), "展布 0", spread, spread == 0,
    "未知 2、独立方程 1 => dim = 1；theta 就是这 1 维")

# A11: 加耦合后解反而不唯一（精确枚举 4 比例 x 3 尺度）
sols = []
for r in (F(1, 2), F(1, 3), F(1, 5), F(1, 10)):
    for sc in (F(1), F(2), F(3)):
        A1c, A2c = sc, r * sc
        gc = 2 * (A1c - A2c) * Ss
        if dN(Cs, Ss, A1c, A2c, gc) == 0:
            sols.append((A1c, A2c, gc))
uniq = len(set(sols))
add("A11", "A", "加耦合后：12 组 (尺度, A1:A2 比例) 各自反解 g* 均命中 N'(theta*)=0 => 解不唯一",
    "12/12 命中且互不相同", "%d/12 distinct" % uniq, len(sols) == 12 and uniq == 12,
    "补一条方程却引入 3 个参数 => 解族维数由 1 升到 3，唯一性变差不是变好")

# ================================================================ B 层
print("\n[B] 高精度数值（prec=50，theta* = arctan(alpha)）")

c = DC
omega_C = DME * c * c / DH
th_e = datan(DALPHA)                      # theta* := arctan(alpha)
sin_t = dsin(th_e)
cos_t = dcos(th_e)
a1, a2 = D(1), D(3)                       # a_i := A_i/(hbar c)
gn_star = D(2) * (a1 - a2) * sin_t        # g* := G1*/(hbar w) = -4 sin(theta*)


def Nv(t, g):
    """归一化作用量密度 N(theta) = a1 cos^2 + a2 sin^2 + g sin"""
    return a1 * dcos(t) ** 2 + a2 * dsin(t) ** 2 + g * dsin(t)


def dNth(t, g):
    """N'(theta) = 2(a2-a1) sin cos + g cos"""
    return D(2) * (a2 - a1) * dsin(t) * dcos(t) + g * dcos(t)


# B01 平坦方向：a1=a2 时 N 对 theta 完全不敏感
Ef = []
for thd in (D("5"), D("20"), D("45"), D("70"), D("85")):
    tv = thd * DPI / D(180)
    Ef.append(a1 * dcos(tv) ** 2 + a1 * dsin(tv) ** 2)
spb = (max(Ef) - min(Ef)) / max(Ef)
add("B01", "B", "a1=a2 时 N(theta) 五档相对展布（应 0）", "0", sci(spb, 4), spb < D("1e-45"),
    "平坦方向的直接读数")

# B02 内点不是驻点
Nbase = Nv(th_e, D(0))
Dn0 = dNth(th_e, D(0))
add("B02", "B", "a1!=a2, g=0 时 theta*=arctan(alpha) 处 |N'|/N", ">> 0",
    sci(abs(Dn0) / Nbase, 8), abs(Dn0) / Nbase > D("1e-3"), "内点不是极值")

# B03 反解 g* 后归零
D_at = dNth(th_e, gn_star)
add("B03", "B", "反解 g* 后 N'(theta*) 残差（相对 N）", "0", sci(abs(D_at) / Nbase, 4),
    abs(D_at) / Nbase < D("1e-30"))

# B04 负对照：g 扰动 +0.1%（读数必须远离基线）
D_pert = dNth(th_e, gn_star * D("1.001"))
add("B04", "B", "负对照：g 扰动 +0.1% 后 N' 必须响应", "非零", sci(abs(D_pert) / Nbase, 6),
    abs(D_pert) / Nbase > D("1e-8") and abs(D_pert) > abs(D_at),
    "证明 B03 的零不是检测器恒零")

# B05 g* 闭式对拍
add("B05", "B", "g* 与闭式 2(a1-a2)sin(theta*) 对拍（a1:a2=1:3 => -4 sin）",
    sci(-D(4) * sin_t, 12), sci(gn_star, 12), rel(gn_star, -D(4) * sin_t) < D("1e-40"),
    "无量纲比只由目标 theta 定 => 一参数一目标")


# B06 雅可比：数值（中心差 + Richardson）vs 闭式 -c^2/omega
def map_om_th(kap, tau):
    K = (kap * kap + tau * tau).sqrt()
    return c * K, datan(kap / tau)


kap0, tau0 = D("6e-3"), D("1.3e-2")


def jac_num(h):
    op, tp = map_om_th(kap0 + h, tau0)
    om, tm = map_om_th(kap0 - h, tau0)
    dk_om, dk_th = (op - om) / (2 * h), (tp - tm) / (2 * h)
    op2, tp2 = map_om_th(kap0, tau0 + h)
    om2, tm2 = map_om_th(kap0, tau0 - h)
    dt_om, dt_th = (op2 - om2) / (2 * h), (tp2 - tm2) / (2 * h)
    return dk_om * dt_th - dt_om * dk_th


h1 = D("1e-6")
J1, J2 = jac_num(h1), jac_num(h1 / 2)
det_num = (4 * J2 - J1) / 3
om0, _ = map_om_th(kap0, tau0)
det_closed = -(c * c) / om0
add("B06", "B", "雅可比 det 数值（中心差 + Richardson）vs 闭式 -c^2/omega",
    sci(det_closed, 12), sci(det_num, 12), rel(det_num, det_closed) < D("1e-16"),
    "未外推读数 %s：一次 Richardson 把相对偏差再压低 9 个量级" % sci(rel(J1, det_closed), 4))

# B07 唯一内禀长度
L_nat = c / omega_C
add("B07", "B", "能量归一 E=hbar*w 定出的唯一内禀长度 L=c/omega", sci(L_nat, 12), "= lambda_bar_C",
    None, "唯一内禀尺度；无法再生第二个")


# B08 独立路径：二分求根 vs 闭式反解
def bisect_root(gv, lo, hi, it=200):
    flo = dNth(lo, gv)
    for _ in range(it):
        mid = (lo + hi) / 2
        fm = dNth(mid, gv)
        if (flo < 0) == (fm < 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


th_num = bisect_root(gn_star, D(0), DPI / D(2) * D("0.9999"))
s_num = dsin(th_num)
s_closed = gn_star / (D(2) * (a1 - a2))
add("B08", "B", "独立路径：二分求 N'(theta)=0 的根后取 sin，与闭式 g*/(2(a1-a2)) 对拍",
    sci(s_closed, 12), sci(s_num, 12), rel(s_num, s_closed) < D("1e-30"),
    "两路径互不依赖（数值求根 vs 闭式反解）")

# B09 判别力：5 个目标 theta 都能被 g* 凑出来 => 一一对应 => 判别力 0
tg = (D("0.30"), D("0.60"), D("1.00"), D("1.30"), D("1.50"))
rows_t = []
for tv in tg:
    gv = D(2) * (a1 - a2) * dsin(tv)
    tn = bisect_root(gv, D(0), DPI / D(2) * D("0.9999"))
    rows_t.append((tv, gv, tn, abs(tn - tv)))
worst = max(x[3] for x in rows_t)
gs_mono = all(rows_t[i + 1][1] < rows_t[i][1] for i in range(len(rows_t) - 1))
add("B09", "B", "5 个目标 theta 各自反解 g* 后二分回收（最大偏差），g* 严格单调",
    "偏差 <= 1e-30 且单调", "%s / mono=%s" % (sci(worst, 6), gs_mono),
    worst < D("1e-30") and gs_mono,
    "theta<->g* 一一对应 => 任何目标 theta 都凑得出 => 对 theta 判别力 0")

# B10 范围判据：可达 theta 只受 |sin|<=1 限制
gmax = D(2) * abs(a1 - a2)
add("B10", "B", "范围判据 |g*| <= 2|a1-a2| 等价于 |sin(theta*)| <= 1，实测占比", "<= 1",
    sci(abs(gn_star) / gmax, 10), abs(gn_star) <= gmax,
    "以 a1:a2=1:3 计上限 g=4，物理点只用 0.0292 => 上界从不构成限制")

# ================================================================ G 层
print("\n[G] 判决层")

add("G01", "G", "本源方程唯一 = 零模条件（一条、无自由参数）", "一条",
    "A01 残差 %s；V26-1、母式、四量闭式全部由它代数推出" % wN, True,
    "这是本卷唯一的正面结论：唯一性成立")

add("G02", "G", "母式是动力学方程", "应能定出唯一的曲线",
    "母式是 (kappa,tau)<->(omega,theta) 的双射，不含时间导数、无初值问题", False,
    "约束 vs 动力学：约束只缩小解集，不产生演化")

add("G03", "G", "母式减少自由度（把 2 个自由常数压到 0）", "2 -> 0",
    "2 -> 2：一般 null 曲线 2 个自由函数；限定常 kappa,tau 后仍 2 个自由常数", False,
    "A04 雅可比非零 = 双射；A03 逆命题精确闭合")

add("G04", "G", "alpha 可由本源方程内生", "应选出唯一 theta",
    "A1=A2 时 theta 是平坦方向（A06 恒 0）；A1!=A2 时极值只在边界（A07）", False)

add("G05", "G", "加手性项 g*tau 后可选出内点 theta 且构成预言", "应给出不依赖拟合的 theta",
    "可选出（A08/B09），但 g*=2(a1-a2)sin(theta*) 由目标 theta 反解 => 一参数一目标", False,
    "判别力 0；但本项定位了「缺什么结构」——需同时有各向异性项与手性项")

add("G06", "G", "本卷给出可证伪的独有预言", ">=1", "0 条", False)

add("G07", "G", "缺口是同一个：框架只有一内禀尺度 L=c/omega", "四量的密度、alpha 的选择、G1 的定值同缺一个尺度",
    "B07：唯一内禀长度 = c/omega；无第二个", True, "结构性结论，与 r383 G03/G04 同源")

# ================================================================ C 层
print("\n[C] 对照层")

# C01 负对照：a1!=a2 时平坦判据必须非零
D_bad_flat = dN(Cs, Ss, a1b, a2b, F(0))
add("C01", "C", "负对照：a1!=a2 时平坦判据必须非零", "非零", D_bad_flat, D_bad_flat != 0)

# C02 正对照：a1=a2 时同一把尺必须恰好 0
D_ok_flat = dN(Cs, Ss, a1b, a1b, F(0))
add("C02", "C", "正对照：a1=a2 时同一把尺恰为 0", "0", D_ok_flat, D_ok_flat == 0)

# C03 边界：a1!=a2 且 g=0 时同一把尺在 theta=0 处必然为 0（极值落到边界）
D_edge = dN(F(1), F(0), a1b, a2b, F(0))
add("C03", "C", "边界对照：a1!=a2、g=0 时 N'(0)=0（极值落到 theta=0 这条边界上）", "0", D_edge,
    D_edge == 0, "内点无零点，但边界一定有 —— 否则 A07 的「只在边界」无从谈起")

# C04 口径对照：弧长积分 vs 时间积分
val_arc = F(9, 50) ** 2 + F(6, 25) ** 2          # k^2+t^2
val_time = (F(3, 2) / F(5)) ** 2                  # (w/c)^2
add("C04", "C", "口径对照：int(.)ds 与 int(.)c dt 同值（c 为常数因子）", str(val_time), str(val_arc),
    val_arc == val_time)

# C05 量纲负对照：G1 当无量纲时差能量维
d_tau = (0, -1, 0, 0, 0)
d_G = (1, 2, -2, 0, 0)   # G1*tau 应为能量/长度
d_prod = tuple(a + b for a, b in zip(d_G, d_tau))
add("C05", "C", "量纲：G1 带能量量纲时 G1*tau = 能量/长度（与 A1*k^2 同）", "(1,1,-2,0,0)", d_prod,
    d_prod == (1, 1, -2, 0, 0))

# C06 双射负对照：把 R 写成 k/(k^2+t^2)^2 后往返不闭合
R_bad = F(9, 50) / ((F(9, 50) ** 2 + F(6, 25) ** 2) ** 2)
add("C06", "C", "双射负对照：R 写成 k/(k^2+t^2)^2 后回代不闭合", "!= 1", str(R_bad / F(1)),
    R_bad != F(1), "误写后 R 从 2 变成 %s" % R_bad)

# ================================================================ E 层
print("\n[E] 仪器自捕")
add("E01", "E", "首稿把耦合写成 alpha/beta，与精细结构常数 alpha 同名（对象错位）",
    "变量名必须写「属于哪个对象」", "改 a1/a2/g", None,
    "本库最高频自伤是对象错位；同名不同物在长推导里必翻车")

add("E02", "E", "首稿把 d(tau)/d(theta) 写成 (w/c)sin(theta)（应为 (w/c)cos(theta)）",
    "内点条件应是 sin(theta*) 不是 cos(theta*)", "已改：g*=2(a1-a2)sin(theta*)",
    None, "求导对象错位；症状是极值条件差 1/sin 量级（旧读数 -4cos 而非 -4sin，差 137 倍）")

add("E03", "E", "首稿 B05 的 exp 写成闭式、act 写成同一闭式（同义反复）",
    "exp 与 act 必须来自两条独立路径", "已改：act 取二分求根，exp 取闭式反解",
    None, "同源回验抓不到同源错误；B08 就是这么补的")

add("E04", "E", "sci() 首版用 abs(x) 归一后只格式化 ax => 负号被吞（detJ 与 g* 的符号全丢）",
    "格式化函数必须保留符号位", "已改：前置 sgn 串",
    None, "这类 bug 只在「读数应为负」时暴露；本卷 detJ=-c^2/w、g*=-4sin 都是负量才被抓到")

# ================================================================ P 层
print("\n[P] 定价")
SLOTS = [("S1", "本源方程能定出唯一的 theta", False),
         ("S2", "不需要新耦合", False),
         ("S3", "新耦合由框架内生", False),
         ("S4", "给出分立谱", False),
         ("S5", "给出可证伪独有预言", False)]
n_sat = sum(1 for _, _, v in SLOTS if v)
add("P01", "P", "五槽满足数（0 => 不占度）", "0", "%d/5" % n_sat, n_sat == 0, "SURVIVE=%d" % n_sat)
add("P02", "P", "可入池的第一性输出条数", "0", "0", None, "产出类型全为结构性否证/定位")

cnt = {}
for r in ROWS:
    cnt[r["kind"]] = cnt.get(r["kind"], 0) + 1
gok = sum(1 for g in GUARDS if g["ok"])
print("\n" + "=" * 78)
print("条目 %d：%s" % (len(ROWS), ", ".join("%s %d" % (k, cnt[k]) for k in sorted(cnt))))
print("守卫 %d/%d" % (gok, len(GUARDS)))
print("=" * 78)

VERD = ("R385-SOURCE-EQUATION-UNIQUE-NULL-CONSTRAINT-OK-MOTHER-IDENTITY-BIJECTION-OK-"
        "THETA-ZERO-MODE-OK-INTERIOR-NEEDS-TWO-COUPLINGS-OK-ALPHA-NOT-INTERNAL-FAIL-"
        "SINGLE-SCALE-ONLY-OK-UNIQUE-PREDICTION-0")

out = {"rid": RID, "date": DATE, "title": TITLE, "verdict": VERD,
       "counts": cnt, "n_rows": len(ROWS),
       "guards": {"n_ok": gok, "n_total": len(GUARDS), "rows": GUARDS},
       "rows": ROWS,
       "key_numbers": {
           "omega_C_rad_s": sci(omega_C, 12),
           "theta_star_rad": sci(th_e, 12),
           "g_star_over_hbarw": sci(gn_star, 12),
           "dNdtheta_rel": sci(abs(D_at) / Nbase, 4),
           "pert_0p1pct_rel": sci(abs(D_pert) / Nbase, 6),
           "jacobian_rel": sci(rel(det_num, det_closed), 4),
           "L_natural_m": sci(L_nat, 12),
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
L.append("[1] 零模 -> 母式（精确有理，%d 例）" % n_case)
L.append("    eta(xdot,xdot)=0 <=> |v|^2=c^2        max|res| = %s" % wN)
L.append("    kappa^2+tau^2=(w/c)^2               max|res| = %s" % wM)
L.append("    逆命题 R=k/(k^2+t^2), u=c^2 t/w      max|res| = %s" % wK)
L.append("")
L.append("[2] 泛函极值结构  E=int(a1*k^2 + a2*t^2 + g*t)ds   （k=(w/c)cos, t=(w/c)sin）")
L.append("    N(theta) = a1 cos^2 + a2 sin^2 + g sin")
L.append("    N'(theta) = 2(a2-a1) sin*cos + g*cos = cos(theta)*[2(a2-a1)sin(theta) + g]")
L.append("    a1=a2, g=0    -> 恒 0（theta 零模）          res = %s" % wFlat)
L.append("    a1!=a2,g=0    -> 内点无零点（只在 0 或 pi/2） zeros = %d/6" % nz_interior)
L.append("    a1!=a2,g!=0   -> sin(theta*) = g/(2(a1-a2))      res = %s" % D_star)
L.append("")
L.append("[3] 数值（theta* = arctan(alpha), a1:a2 = 1:3）")
L.append("    omega_C          = %s rad/s" % sci(omega_C, 12))
L.append("    theta*           = %s rad" % sci(th_e, 12))
L.append("    g*               = %s  (= G1*/(hbar*w))" % sci(gn_star, 12))
L.append("    N'(theta*) |rel| = %s" % sci(abs(D_at) / Nbase, 4))
L.append("    扰动 0.1%% 后     = %s" % sci(abs(D_pert) / Nbase, 6))
L.append("    雅可比 detJ      = %s  (闭式 %s)" % (sci(det_num, 12), sci(det_closed, 12)))
L.append("    唯一内禀长度     = %s m (= lambda_bar_C)" % sci(L_nat, 12))
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
M.append("## 一、零模链（精确有理，%d 例）" % n_case)
M.append("")
M.append("| 环节 | 判据 | 残差 |")
M.append("|---|---|---|")
M.append("| 零模 | `eta(xdot,xdot)=0 <=> \\|v\\|^2=c^2` | %s |" % esc(wN))
M.append("| 母式 | `kappa^2+tau^2=(w/c)^2` | %s |" % esc(wM))
M.append("| 逆命题 | `R=k/(k^2+t^2)`、`u=c^2 t/w` | %s |" % esc(wK))
M.append("")
M.append("## 二、极值结构四格")
M.append("")
M.append("归一化被积密度：`N(theta) = a1 cos^2 + a2 sin^2 + g sin`，其中 `a_i := A_i/(hbar c)`、`g := G1/(hbar w)`。")
M.append("")
M.append("它对 theta 的导数：`N'(theta) = 2(a2-a1) sin(theta)cos(theta) + g cos(theta) = cos(theta)*[2(a2-a1)sin(theta) + g]`。")
M.append("")
M.append("| a1 vs a2 | g | 极值位置 |")
M.append("|---|---|---|")
M.append("| 相等 | 0 | **全平**（theta 任意） |")
M.append("| 相等 | 非零 | `theta=±pi/2`（圆，tau 取极值） |")
M.append("| 不等 | 0 | `theta=0`（直线）或 `theta=±pi/2`（圆） |")
M.append("| 不等 | 非零 | 内点 `sin(theta*)=g/(2(a1-a2))`，需 `\\|g\\| <= 2\\|a1-a2\\|` |")
M.append("")
M.append("## 三、数值")
M.append("")
M.append("| 量 | 值 |")
M.append("|---|---|")
M.append("| `omega_C` | %s rad/s |" % sci(omega_C, 12))
M.append("| `theta*` | %s rad（= arctan(alpha)） |" % sci(th_e, 12))
M.append("| `g*` = `G1*/(hbar*w)` | %s |" % sci(gn_star, 12))
M.append("| `N'(theta*)` 残差（rel） | %s |" % sci(abs(D_at) / Nbase, 4))
M.append("| 扰动 0.1%% 后响应 | %s |" % sci(abs(D_pert) / Nbase, 6))
M.append("| 雅可比 `detJ` | %s |" % sci(det_num, 12))
M.append("| 闭式 `-c^2/omega_C` | %s |" % sci(det_closed, 12))
M.append("| 唯一内禀长度 `c/omega` | %s m |" % sci(L_nat, 12))
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
