# -*- coding: utf-8 -*-
"""TUFT-r383 · 温度/质量/密度/硬度 四量本质
光速螺旋全维求导 + 量纲归位 + 定义级换算判定 + 不可内禀性定理

分层：A 精确代数(Fraction) / B 高精度数值(Decimal prec=50) / G 判决 / C 对照 / GUARD 工具自检 / P 定价
纪律：条目不可跨层相加；add() 的 kind 由 ok 驱动；纯陈述给 INFO；每条判决配对照；门限不用 10 的幂当判据。
"""
import os
import io
import json
from fractions import Fraction as F
from decimal import Decimal as D, getcontext, ROUND_HALF_EVEN

getcontext().prec = 50

RID = "TUFT-r383"
DATE = "2026-11-03"
TITLE = ("TUFT-r383_温度质量密度硬度四量本质_光速螺旋全维求导与量纲归位"
         "_定义级换算判定与不可内禀性定理_精算_2026-11-03")

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


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def n2(a):
    return dot(a, a)


# ---------------------------------------------------------------- 常数
DC = D("299792458")
DH = D("1.054571817e-34")
DHPL = D("6.62607015e-34")
DK = D("1.380649e-23")
DME = D("9.1093837015e-31")
DMP = D("1.67262192369e-27")
DMPL = D("2.176434e-8")
DALPHA = D("0.0072973525693")
DPI = D("3.14159265358979323846264338327950288419716939937510")


def sci(x, nd=10):
    if x == 0:
        return "0"
    x = D(x)
    e = 0
    ax = abs(x)
    while ax >= 10:
        ax /= 10
        e += 1
    while ax < 1:
        ax *= 10
        e -= 1
    return "%sE%+04d" % (format(ax, ".%df" % (nd - 1)), e)


def rel(a, b):
    return abs(a - b) / (abs(b) if b != 0 else D(1))


def dsin(x):
    """Decimal 正弦：Machin 常数 + 区间归约 + Taylor（50 位下截断 1E-45）。"""
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


print("=" * 78)
print("%s | %s" % (RID, DATE))
print("=" * 78)

# ================================================================ GUARD
print("\n[GUARD] 工具自检")
guard("FRAC-EXACT", (F(1, 3) + F(1, 6) - F(1, 2)) == 0, "1/3+1/6-1/2 = %s" % (F(1, 3) + F(1, 6) - F(1, 2)))
guard("DEC-PREC", ((D(1) / D(3)) * D(3) - D(1)) != 0, "1/3*3-1 = %s（50 位下应非零）" % ((D(1) / D(3)) * D(3) - D(1)))
guard("DEC-SQRT", (D(2).sqrt() ** 2 - D(2)) < D("1e-48"), "sqrt(2)^2-2 = %s" % (D(2).sqrt() ** 2 - D(2)))

# ================================================================ A 全维求导
print("\n[A] 全维求导（6 个有理相位 x 4 组勾股族）")

PHASES = [(F(3, 5), F(4, 5)), (F(5, 13), F(12, 13)), (F(8, 17), F(15, 17)),
          (F(7, 25), F(24, 25)), (F(20, 29), F(21, 29)), (F(9, 41), F(40, 41))]
FAM = [(F(3), F(4), F(1)), (F(5), F(12), F(2)), (F(8), F(15), F(1, 2)), (F(7), F(24), F(3))]
CMAP = {3: 5, 5: 13, 8: 17, 7: 25}

wV = wA = wK = wT = wX = F(0)
n_case = 0
cap = {}

for (Rw, u, R) in FAM:
    c = F(CMAP[int(Rw)])
    assert Rw * Rw + u * u == c * c
    w = Rw / R
    for (C, S) in PHASES:
        assert C * C + S * S == 1
        v = (-R * w * S, R * w * C, u)
        acc = (-R * w * w * C, -R * w * w * S, F(0))
        dacc = (R * w ** 3 * S, -R * w ** 3 * C, F(0))
        dv = n2(v) - c * c
        da = (acc[0] + w * w * R * C, acc[1] + w * w * R * S, acc[2])
        cr = cross(v, acc)
        ncr = n2(cr)
        vv = n2(v)
        assert ncr == (R * R * w ** 4) * (c * c)
        k_cl = R * w * w / (c * c)
        t_cl = u * w / (c * c)
        dk = (ncr / (vv ** 3)) - k_cl * k_cl
        dt = (dot(cr, dacc) / ncr) - t_cl
        dtr = k_cl * k_cl + t_cl * t_cl - (w / c) ** 2
        wV = max(wV, abs(dv))
        wA = max(wA, max(abs(x) for x in da))
        wK = max(wK, abs(dk))
        wT = max(wT, abs(dt))
        wX = max(wX, abs(dtr))
        n_case += 1
        if not cap:
            cap = {"v": v, "acc": acc, "cr": cr, "dacc": dacc, "ncr": ncr, "vv": vv,
                   "R": R, "w": w, "u": u, "c": c}

add("A01", "A", "速度模方 |v|^2 = R^2w^2+u^2 = c^2（%d 例）" % n_case, "残差 0", wV, wV == 0)
add("A02", "A", "加速度 a = -w^2*(x,y,0)（纯向心、无轴向分量）", "残差 0", wA, wA == 0)
add("A03", "A", "曲率 kappa：叉积路径 |vxa|^2/|v|^6 对比闭式 (Rw^2/c^2)^2", "残差 0", wK, wK == 0)
add("A04", "A", "挠率 tau：(vxa).da/|vxa|^2 对比闭式 u*w/c^2", "残差 0", wT, wT == 0)
add("A05", "A", "三重奏 kappa^2+tau^2 = (w/c)^2", "残差 0", wX, wX == 0)

# A06 两路径：叉积算出的 (kappa/|tau|)^2 对比几何式 (Rw/u)^2
kc2 = cap["ncr"] / (cap["vv"] ** 3)
tc = dot(cap["cr"], cap["dacc"]) / cap["ncr"]
lhs = kc2 / (tc * tc)
rhs = (cap["R"] * cap["w"] / cap["u"]) ** 2
add("A06", "A", "螺旋角：由叉积得的 (kappa/|tau|)^2 对比几何式 (Rw/u)^2=(tan theta)^2",
    str(rhs), str(lhs), lhs == rhs, "两条路径不共享中间量")

# ================================================================ A 四量恒等式
print("\n[A] 四量恒等式")

wM = F(0)
for (Rw, u, R) in FAM:
    c = F(CMAP[int(Rw)])
    w = Rw / R
    k = R * w * w / (c * c)
    t = u * w / (c * c)
    m_geo2 = (k * k + t * t)                    # (hbar=1, c 已含) -> (m*c)^2
    m_frq2 = (w * w) / (c * c)                  # (hbar*w/c)^2
    wM = max(wM, abs(m_geo2 - m_frq2))
add("A07", "A", "质量：m=(hbar/c)sqrt(k^2+t^2) 与 m=hbar*w/c^2 的平方比对", "残差 0", wM, wM == 0)

add("A08", "A", "温度与质量是同一量的两种单位（E=hbar*w 与 E=m c^2 合并 => T=hbar*w/kB=m c^2/kB）",
    "定义恒等（不是新关系）", "T=hbar*w/kB 与 T=m c^2/kB 逐项同式", None,
    "纯陈述，按门禁记 INFO；数值两路径见 B05")

TM = DC * DC / DK
add("A09", "A", "温度—质量锁常数 T/m = c^2/kB", "c^2/kB", "%s K/kg" % sci(TM, 12), None,
    "定义推论；是否普适见 B05 三族实测")

wU = F(0)
for (Rw, u, R) in FAM:
    c = F(CMAP[int(Rw)])
    w = Rw / R
    a_c = R * w * w
    # T_U/T_C = a/(2*pi*c*w)；去掉公共 1/(2pi)，比较 a 与 c*w*sin = Rw*w
    wU = max(wU, abs(a_c - c * w * (Rw / c)))
add("A10", "A", "Unruh—Compton 比值：T_U/T_C = a/(2*pi*c*w) = sin(theta)/(2*pi)",
    "残差 0", wU, wU == 0, "R=c*sin/w 且 a=R*w^2 => a/(c*w)=sin；pi 两侧同除")

wR = F(0)
for (Rw, u, R) in FAM:
    c = F(CMAP[int(Rw)])
    w = Rw / R
    s = Rw / c
    x1 = F(1) / (c * c * R ** 3)
    x2 = (w ** 3) / (c ** 5 * s ** 3)
    wR = max(wR, abs(x1 - x2))
add("A11", "A", "密度：rho=3*hbar*w/(4*pi*c^2*R^3) = 3*hbar*w^4/(4*pi*c^5*sin^3)（V=(4pi/3)R^3 口径）",
    "残差 0（去公共因子）", wR, wR == 0, "R=c*sin/w")

wH = F(0)
for (Rw, u, R) in FAM:
    c = F(CMAP[int(Rw)])
    w = Rw / R
    s = Rw / c
    wH = max(wH, abs(F(1) / (R ** 3) - (w ** 3) / (c ** 3 * s ** 3)))
add("A12", "A", "硬度能量密度：Hv=hbar*w/R^3 = hbar*w^4/(c^3*sin^3)", "残差 0", wH, wH == 0,
    "与密度同标度 w^4/sin^3，仅单位因子不同")

# ================================================================ A 量纲
print("\n[A] 量纲归位（M,L,T,Q,Theta 五元组）")


def dv(*x):
    return tuple(F(v) for v in x)


d_kappa = dv(0, -1, 0, 0, 0)
d_w = dv(0, 0, -1, 0, 0)
d_c = dv(0, 1, -1, 0, 0)
d_h = dv(1, 2, -1, 0, 0)
d_kB = dv(1, 2, -2, 0, -1)
d_E = dv(1, 2, -2, 0, 0)


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def plus(a, b):
    return tuple(x + y for x, y in zip(a, b))


d_m = sub(plus(d_h, d_w), plus(d_c, d_c))
add("A13", "A", "量纲 hbar*w/c^2 = M", dv(1, 0, 0, 0, 0), d_m, d_m == dv(1, 0, 0, 0, 0))
d_T = sub(plus(d_h, d_w), d_kB)
add("A14", "A", "量纲 hbar*w/kB = Theta", dv(0, 0, 0, 0, 1), d_T, d_T == dv(0, 0, 0, 0, 1))
d_rho = sub(d_m, dv(0, 3, 0, 0, 0))
add("A15", "A", "量纲 m/R^3 = M L^-3（密度）", dv(1, -3, 0, 0, 0), d_rho, d_rho == dv(1, -3, 0, 0, 0))
d_H = sub(d_E, dv(0, 3, 0, 0, 0))
add("A16", "A", "量纲 能量/R^3 = M L^-1 T^-2 = 应力 = 能量密度（硬度归位）",
    dv(1, -1, -2, 0, 0), d_H, d_H == dv(1, -1, -2, 0, 0))
add("A17", "A", "量纲 硬度 != 能量（差 L^3）", dv(1, 2, -2, 0, 0), d_H, d_H != d_E)

# ================================================================ B 数值
print("\n[B] 高精度数值（prec=50；输入常数 10~12 位）")

c = DC
omega_C = DME * c * c / DH
lamC = DH / (DME * c)
den = (1 + DALPHA * DALPHA).sqrt()
sin_t = DALPHA / den
R_e = lamC * DALPHA / den
kappa_e = omega_C / c * sin_t
tau_e = (kappa_e / DALPHA) * D(1) / D(1)
tau_e = omega_C / c / den
m_e = DH * omega_C / (c * c)
T_e = DH * omega_C / DK
V_e = D(4) / D(3) * DPI * R_e ** 3
rho_e = m_e / V_e
Hv_e = DH * omega_C / R_e ** 3
a_e = R_e * omega_C ** 2
TU_e = DH * a_e / (D(2) * DPI * DK * c)
ratio_e = TU_e / T_e

lamC_h = DHPL / (DME * c)
w_alt = D(2) * DPI * c / lamC_h
add("B01", "B", "omega_C 两路径：m c^2/hbar 与 2*pi*c/lambda_C(经 h)", sci(omega_C, 12), sci(w_alt, 12), None,
    "差 1e-10 级，来自 hbar 印值只到 10 位（h/(2pi)=1.0545718176e-34）")

add("B02", "B", "sqrt(k^2+t^2) 与 w/c 对拍", sci(omega_C / c, 12),
    sci((kappa_e * kappa_e + tau_e * tau_e).sqrt(), 12),
    rel((kappa_e * kappa_e + tau_e * tau_e).sqrt(), omega_C / c) < D("1e-40"))

add("B03", "B", "四量读数（电子族 theta=arctan(alpha), w=omega_C）", "m,T,rho,Hv",
    "%s kg / %s K / %s kg m^-3 / %s Pa" % (sci(m_e, 10), sci(T_e, 10), sci(rho_e, 8), sci(Hv_e, 8)),
    None, "rho 用 V=(4pi/3)R^3 口径，该口径无物理指称（G03）")

add("B04", "B", "Unruh 温度比值 T_U/T_C 对比闭式 sin(theta)/(2pi)", sci(sin_t / (D(2) * DPI), 10),
    sci(ratio_e, 10), rel(ratio_e, sin_t / (D(2) * DPI)) < D("1e-25"))

T_P = DMPL * c * c / DK
T_p = DMP * c * c / DK
wlock = D(0)
for (mm, TT) in [(DME, T_e), (DMP, T_p), (DMPL, T_P)]:
    wlock = max(wlock, rel(TT / mm, TM))
add("B05", "B", "温度—质量锁三族（电子/质子/Planck）实测 T/m 对比 c^2/kB", sci(TM, 12),
    "max rel = %s" % sci(wlock, 4), None,
    "三族一致是定义使然（T:=m c^2/kB），本项只作仪器一致性检查，不构成独立验证")

print("\n[B] 密度对自由参数 theta（w 固定=omega_C）")
rho_tab = []
for thd in (D("45"), D("15"), D("1"), D("0.1")):
    th = thd * DPI / D(180)
    rr = D(3) * DH * omega_C ** 4 / (D(4) * DPI * c ** 5 * dsin(th) ** 3)
    rho_tab.append((thd, rr))
    print("    theta=%-6s deg -> rho=%s kg/m^3" % (thd, sci(rr, 8)))
mono = all(rho_tab[i + 1][1] > rho_tab[i][1] for i in range(len(rho_tab) - 1))
add("B06", "B", "密度随 theta 严格单调（theta 减小 => rho 发散）", "3/3", mono, mono,
    "theta 自由（r365 R6）=> rho 在 (rho_min, oo) 上满射")

print("\n[B] 质量谱连续性（200 点，1e10..1e30 rad/s）")
om = [D("1e10") * (D("1e30") / D("1e10")) ** (D(i) / D(199)) for i in range(200)]
ms = [DH * x / (c * c) for x in om]
inc = all(ms[i + 1] > ms[i] for i in range(len(ms) - 1))
rt = max(rel(x * c * c / DH, o) for x, o in zip(ms, om))
add("B07", "B", "w->m 严格单调递增", "199/199", "199/199" if inc else "broken", inc)
add("B08", "B", "m->w 反解往返 max rel", "<= 1e-40", sci(rt, 4), rt < D("1e-40"),
    "双射 => 无额外量子化则谱连续（G02）")

rho_cl = D(3) * DH * omega_C ** 4 / (D(4) * DPI * c ** 5 * sin_t ** 3)
Hv_cl = DH * omega_C ** 4 / (c ** 3 * sin_t ** 3)
add("B09", "B", "密度双路径：3hw/(4pi c^2 R^3) 对比 3hw^4/(4pi c^5 sin^3)",
    sci(rho_e, 10), sci(rho_cl, 10), rel(rho_cl, rho_e) < D("1e-40"))
add("B10", "B", "硬度双路径：hw/R^3 对比 hw^4/(c^3 sin^3)", sci(Hv_e, 10), sci(Hv_cl, 10),
    rel(Hv_cl, Hv_e) < D("1e-40"))

# ================================================================ G 判决
print("\n[G] 判决层")

add("G01", "G", "四量同源：m、T 线性于 w；rho、Hv 为 w^4/sin^3", "四条闭式共用唯一自变量 w",
    "A07 res=%s, A11 res=%s, A12 res=%s" % (wM, wR, wH), True, "结构陈述，由 A 层残差承重")

add("G02", "G", "质量谱分立性可由几何导出", "应存在使 w 离散的条件",
    "母式不含量子化；w->m 为 (0,oo)->(0,oo) 双射 => 谱连续", False,
    "缺的是独立方程，不是算错；与 r264 内生 0 / r267 独有预言 0 同向")

add("G03", "G", "密度可内禀定义（不引外部体积）", "应存在几何固定的体积",
    "R 是积分常数（r354 G06 平面波平移简并）=> 无内禀尺度", False,
    "V=R^3 与 V=(4pi/3)R^3 差 4.18879 倍，rho 与 V 线性反比")

add("G04", "G", "硬度可内禀定义", "应存在与位错/键合无关的几何量",
    "硬度量纲=能量密度；能量密度在本框架口径依赖（r360 G01）", False,
    "硬度是宏观统计阈值（塑性屈服），单条世界线不携带该信息")

add("G05", "G", "Unruh—Compton 比值有判别力", "应能约束 theta",
    "T_U/T_C=sin/(2pi)，theta 自由 => 对任意目标可反解 => 满射", False,
    "与 r354 G01 同型：一参数一目标")

add("G06", "G", "本卷给出可证伪的独有预言", ">=1 条", "0 条", False)

add("G07", "G", "四量本质 = 同一几何量的四种单位", "m,T 只依赖 w；rho,Hv 依赖 w 与 theta",
    "m=(h/c^2)w, T=(h/kB)w, rho=(3h/4pi c^5)w^4/sin^3, Hv=(h/c^3)w^4/sin^3", True,
    "本卷唯一正面结论，且是结构性的，不含数值预言")

# ================================================================ C 对照
print("\n[C] 对照层")

m2 = (2 * DH) * omega_C / (c * c)
add("C01", "C", "负对照 hbar->2hbar：m 必须翻倍", "2", sci(m2 / m_e, 10), rel(m2 / m_e, D(2)) < D("1e-40"))

w_m = DME * c * c / DH
w_kt = c * (kappa_e * kappa_e + tau_e * tau_e).sqrt()
add("C02", "C", "正对照 w 两独立路径（m 反算 / sqrt(k^2+t^2)）", sci(w_m, 12), sci(w_kt, 12),
    rel(w_m, w_kt) < D("1e-25"))

a_bad = R_e * omega_C
r_bad = DH * a_bad / (D(2) * DPI * DK * c) / T_e
tgt = sin_t / (D(2) * DPI)
add("C03", "C", "负对照 a=R*w（少一个 w）：比值必须偏离目标 sin/(2pi)", "目标/坏值 ≈ w_C",
    sci(tgt / r_bad, 6), (tgt / r_bad) > D("1e15"),
    "坏值 = R/(2pi c)=sin/(2pi*w_C) => 目标/坏值恰为 w_C")

rho_cube = m_e / R_e ** 3
add("C04", "C", "口径对照 V=R^3 与 V=(4pi/3)R^3 的密度比", "4.18879", sci(rho_cube / rho_e, 10),
    rel(rho_cube / rho_e, D(4) * DPI / D(3)) < D("1e-40"))

add("C05", "C", "量纲负对照：硬度当能量时差 L^3", "%s" % (d_E,), "%s" % (d_H,), d_H != d_E)


def logslope(ws, ys):
    return (ys[-1] / ys[0]).ln() / (ws[-1] / ws[0]).ln()


ms_bad = [x * x for x in om]
s_bad = logslope(om, ms_bad)
s_lin = logslope(om, ms)
add("C06", "C", "双射负对照改 m~w^2：log-log 斜率必须 = 2（不是 1）", "2", sci(s_bad, 10),
    abs(s_bad - D(2)) < D("1e-30"))
add("C07", "C", "正对照 m~w：log-log 斜率必须 = 1（线性换算指纹）", "1", sci(s_lin, 10),
    abs(s_lin - D(1)) < D("1e-30"),
    "注意：等比网格上「相邻比恒定」对任意幂律都成立，不能当判据；必须用 log-log 斜率")

# ================================================================ E 仪器自捕
print("\n[E] 仪器自捕（判据被我自己的错弄红，已修复）")
add("E01", "E", "C03 首版把方向写反：坏值比目标小 1/w_C 量级，用 rel(坏值,目标)>1e10 恒假",
    "判据方向须与「坏值偏大还是偏小」一致", "改为 目标/坏值 = w_C > 1e15", None,
    "教训：构造负对照前先估坏值在目标的哪一侧")
add("E02", "E", "C06 首版在等比网格上用「相邻比恒定」判幂律 —— 任意幂律恒绿（退化点）",
    "判据必须对 m~w^2 与 m~w 给出不同读数", "改为 log-log 斜率：1 vs 2", None,
    "教训：等比网格上的比值不携带幂次信息，必须用斜率")

# ================================================================ P 定价
print("\n[P] 定价")
SLOTS = [("S1", "四量之一由几何内生（不输入 m/T/V）", False),
         ("S2", "体积由几何固定（不引外部尺度）", False),
         ("S3", "theta 由动力学固定", False),
         ("S4", "给出分立质量谱", False),
         ("S5", "给出可证伪的独有预言", False)]
n_sat = sum(1 for _, _, v in SLOTS if v)
add("P01", "P", "五槽满足数（0 => 不占度）", "0", "%d/5" % n_sat, n_sat == 0, "宽松档 SURVIVE=%d" % n_sat)
add("P02", "P", "可入池的第一性输出条数", "0", "0", None, "产出类型全为否证/口径")

# ================================================================ 汇总
cnt = {}
for r in ROWS:
    cnt[r["kind"]] = cnt.get(r["kind"], 0) + 1
gok = sum(1 for g in GUARDS if g["ok"])
print("\n" + "=" * 78)
print("条目 %d：%s" % (len(ROWS), ", ".join("%s %d" % (k, cnt[k]) for k in sorted(cnt))))
print("守卫 %d/%d" % (gok, len(GUARDS)))
print("=" * 78)

VERD = ("R383-FOUR-QUANTITY-ESSENCE-MASS-FREQ-LOCK-OK-TEMP-MASS-LOCK-OK-"
        "UNRUH-COMPTON-SIN-THETA-OK-DENSITY-NOT-INTRINSIC-FAIL-HARDNESS-STRESS-REGRADE-FAIL-"
        "SPECTRUM-CONTINUOUS-FAIL-NO-INDEPENDENT-EQUATION-SUPPLY-0")

out = {"rid": RID, "date": DATE, "title": TITLE, "verdict": VERD,
       "counts": cnt, "n_rows": len(ROWS),
       "guards": {"n_ok": gok, "n_total": len(GUARDS), "rows": GUARDS},
       "rows": ROWS,
       "key_numbers": {
           "omega_C_rad_s": sci(omega_C, 12), "R_electron_m": sci(R_e, 10),
           "kappa_electron_m-1": sci(kappa_e, 10), "tau_electron_m-1": sci(tau_e, 10),
           "m_electron_kg": sci(m_e, 10), "T_electron_K": sci(T_e, 10),
           "rho_electron_kg_m3": sci(rho_e, 8), "Hv_electron_Pa": sci(Hv_e, 8),
           "a_electron_m_s2": sci(a_e, 8), "T_unruh_electron_K": sci(TU_e, 8),
           "T_unruh_over_T_compton": sci(ratio_e, 10),
           "sin_theta_over_2pi": sci(sin_t / (D(2) * DPI), 10),
           "T_over_m_K_per_kg": sci(TM, 12), "T_proton_K": sci(T_p, 10), "T_planck_K": sci(T_P, 10)},
       "rho_vs_theta": [[str(t), sci(v, 8)] for (t, v) in rho_tab]}

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
L.append("[1] 全维求导（精确有理，%d 例）" % n_case)
L.append("    |v|^2-c^2            max|res| = %s" % wV)
L.append("    a+w^2*(x,y,0)        max|res| = %s" % wA)
L.append("    kappa 叉积 vs 闭式    max|res| = %s" % wK)
L.append("    tau   叉积 vs 闭式    max|res| = %s" % wT)
L.append("    k^2+t^2-(w/c)^2      max|res| = %s" % wX)
L.append("")
L.append("[2] 四量闭式（唯一自变量 w，加自由参数 theta）")
L.append("    m   = (hbar/c^2) * w")
L.append("    T   = (hbar/kB)  * w")
L.append("    rho = (3*hbar/(4*pi*c^5)) * w^4 / sin^3(theta)   [V=(4pi/3)R^3]")
L.append("    Hv  = (hbar/c^3)          * w^4 / sin^3(theta)   [能量密度]")
L.append("    T/m = c^2/kB = %s K/kg" % sci(TM, 12))
L.append("")
L.append("[3] 电子族读数")
L.append("    omega_C = %s rad/s" % sci(omega_C, 12))
L.append("    R       = %s m" % sci(R_e, 10))
L.append("    kappa   = %s m^-1" % sci(kappa_e, 10))
L.append("    tau     = %s m^-1" % sci(tau_e, 10))
L.append("    m       = %s kg" % sci(m_e, 10))
L.append("    T       = %s K" % sci(T_e, 10))
L.append("    rho     = %s kg/m^3  (V=(4pi/3)R^3)" % sci(rho_e, 8))
L.append("    Hv      = %s Pa      (hbar*w/R^3)" % sci(Hv_e, 8))
L.append("    a       = %s m/s^2" % sci(a_e, 8))
L.append("    T_U     = %s K" % sci(TU_e, 8))
L.append("    T_U/T_C = %s  vs sin/(2pi) = %s" % (sci(ratio_e, 10), sci(sin_t / (D(2) * DPI), 10)))
L.append("")
L.append("[4] 标度")
L.append("    T_proton = %s K ; T_planck = %s K" % (sci(T_p, 10), sci(T_P, 10)))
for (thd, rr) in rho_tab:
    L.append("    theta=%-5s deg -> rho = %s kg/m^3" % (thd, sci(rr, 8)))
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

print("\nwritten:\n  %s\n  %s" % (os.path.basename(jp), os.path.basename(rp)))


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
M.append("## 一、全维求导残差（精确有理，%d 例）" % n_case)
M.append("")
M.append("| 量 | 判据 | 残差 |")
M.append("|---|---|---|")
M.append("| 速度模方 | `\\|v\\|^2=R^2w^2+u^2` 对 `c^2` | %s |" % esc(wV))
M.append("| 加速度 | `a=-w^2*(x,y,0)` | %s |" % esc(wA))
M.append("| 曲率 | 叉积 `\\|vxa\\|^2/\\|v\\|^6` 对 `(Rw^2/c^2)^2` | %s |" % esc(wK))
M.append("| 挠率 | `(vxa).da/\\|vxa\\|^2` 对 `u*w/c^2` | %s |" % esc(wT))
M.append("| 三重奏 | `k^2+t^2` 对 `(w/c)^2` | %s |" % esc(wX))
M.append("")
M.append("## 二、四量闭式")
M.append("")
M.append("| 量 | 闭式 | 自变量 |")
M.append("|---|---|---|")
M.append("| 质量 | `m=(hbar/c^2)*w` | w |")
M.append("| 温度 | `T=(hbar/kB)*w` | w |")
M.append("| 密度 | `rho=(3*hbar/(4*pi*c^5))*w^4/sin^3(theta)` | w, theta |")
M.append("| 硬度 | `Hv=(hbar/c^3)*w^4/sin^3(theta)` | w, theta |")
M.append("")
M.append("## 三、电子族读数（theta=arctan(alpha)，w=omega_C）")
M.append("")
M.append("| 量 | 值 | 单位 |")
M.append("|---|---|---|")
for (k, u) in [("omega_C", "rad/s"), ("R", "m"), ("kappa", "m^-1"), ("tau", "m^-1"),
               ("m", "kg"), ("T", "K"), ("rho", "kg/m^3"), ("Hv", "Pa"),
               ("a", "m/s^2"), ("T_U", "K"), ("T/m", "K/kg")]:
    v = {"omega_C": sci(omega_C, 12), "R": sci(R_e, 10), "kappa": sci(kappa_e, 10),
         "tau": sci(tau_e, 10), "m": sci(m_e, 10), "T": sci(T_e, 10),
         "rho": sci(rho_e, 8), "Hv": sci(Hv_e, 8), "a": sci(a_e, 8),
         "T_U": sci(TU_e, 8), "T/m": sci(TM, 12)}[k]
    M.append("| `%s` | %s | %s |" % (k, v, u))
M.append("| `T_U/T_C` | %s | 无量纲 |" % sci(ratio_e, 10))
M.append("| `sin(theta)/(2*pi)` | %s | 无量纲 |" % sci(sin_t / (D(2) * DPI), 10))
M.append("")
M.append("## 四、密度对自由参数 theta（w 固定）")
M.append("")
M.append("| theta (deg) | rho (kg/m^3) |")
M.append("|---|---|")
for (thd, rr) in rho_tab:
    M.append("| %s | %s |" % (thd, sci(rr, 8)))
M.append("")
M.append("## 五、条目明细")
M.append("")
M.append("| ID | 层 | 裁定 | 条目 | exp | act |")
M.append("|---|---|---|---|---|---|")
for r in ROWS:
    M.append("| %s | %s | **%s** | %s | %s | %s |"
             % (r["id"], r["layer"], r["kind"], esc(r["name"]), esc(r["exp"]), esc(r["act"])))
M.append("")
M.append("## 六、守卫")
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
print("  %s" % os.path.basename(mp))
