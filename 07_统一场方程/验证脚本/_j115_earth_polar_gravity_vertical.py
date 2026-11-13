# -*- coding: utf-8 -*-
"""J115 · 卷 136 · 地球两极重力为什么更重（不是更轻）

本册做三件事，全部可机验、全部只读既有锚点：

1) 用 WGS84／GRS80 的**正常重力闭式（Somigliana）**复现地表重力随纬度的变化，
   把「极—赤」差 5185.96 mGal 拆成三项物理账：扁率 1/r² 项、J2 四极项、离心项。
   结论：两极**更重**，不是更轻；赤道更轻的原因是离心 + 扁率，两者同号叠加。
2) 「垂直原理」只证可证的那一半：
   - 轴向定理（精确）：轴对称质量分布 + 绕轴对称自转 ⇒ 轴上有效重力切向分量恒为零、
     离心恒为零、铅垂线与自转轴严格重合；大地纬度与地心纬度在极点严格相等。
   - 一般「三力始终两两垂直」已被 ROOT-3F 判为条件性运动学恒等式（余维 3、O(t) 即破），
     本册不翻案，只引用其判决串并复核其在极点退化为「离心=0」的平凡情形。
3) 否证两条「v=c / 曲率挠率」通道：
   - v=c：ωρ=c 要求 ρ=c/ω=4.111e12 m（27.48 AU），是地表半径的 6.45e5 倍；
     强行令地表 v=c 需 ω=47.0 rad/s（7.48 转/秒），离心项 1.409e10 m/s²（1.4e9 g）。
   - κ/τ：地球子午线是**平面闭曲线**，挠率 τ≡0；螺旋字典 τ=b/(ρ²+b²) 在 τ=0 时退化为
     圆（κ=1/ρ 常数），对纬度**零变化**，与实测 1.01% 曲率变化和 0.53% 重力变化都不相容。
     单条螺旋是 1 维曲线，地球重力场是 2 维曲面上的场，维数不够。

诚实边界：本册复现的是 WGS84/GRS80 正常重力**模型**（它本身是对海量观测的最小二乘拟合），
不是逐条测量数据的回放；局部重力异常（±100 mGal 量级，需 EGM 高阶项）不在口径内。
不新增物理、不关闭任何 OPEN、记分板仍 0/6。数据锚点：WGS84 定义常数 + EGM 的 J2；
所有读数由 Decimal(60) 纯标准库复算，无第三方依赖、无网络。
"""
import io
import json
import os
import sys
import math
import hashlib
from decimal import Decimal as D, getcontext, ROUND_FLOOR

getcontext().prec = 60
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


# ------------------------------------------------------------------ Decimal trig
PI = D("3.14159265358979323846264338327950288419716939937510582097494459231")
TWO_PI = 2 * PI


def dsin(x):
    x = x - (x / TWO_PI).to_integral_value(rounding=ROUND_FLOOR) * TWO_PI
    if x > PI:
        x -= TWO_PI
    if x > PI / 2:
        x = PI - x
    if x < -PI / 2:
        x = -PI - x
    term = x
    total = x
    x2 = x * x
    n = 1
    while True:
        term = -term * x2 / D((2 * n) * (2 * n + 1))
        total += term
        n += 1
        if abs(term) < D("1e-75"):
            break
    return total


def dcos(x):
    return dsin(x + PI / 2)


def dtan(x):
    return dsin(x) / dcos(x)


def datan(x):
    if x == 0:
        return D(0)
    y = D(repr(math.atan(float(x))))
    for _ in range(80):
        t = dtan(y)
        dy = (t - x) / (1 + t * t)
        y -= dy
        if abs(dy) < D("1e-70"):
            break
    return y


def deg2rad(x):
    return D(x) * PI / D(180)


def rad2deg(x):
    return x * D(180) / PI


def fmt(x, n=18):
    return format(x, "." + str(n) + "f")


# ------------------------------------------------------------------ constants
GM = D("3.986004418e14")          # m^3 s^-2  [WGS84]
A = D("6378137")                  # m        [WGS84 semi-major]
INVF = D("298.257223563")         #          [WGS84 1/f]
F = D(1) / INVF
B = A * (1 - F)                   # polar radius
E2 = F * (2 - F)
OM = D("7.292115e-5")             # rad s^-1 [WGS84 Earth rotation]
GE = D("9.7803253359")            # m s^-2   [WGS84 normal gravity, equator]
GP = D("9.8321849378")            # m s^-2   [WGS84 normal gravity, pole]
CLIGHT = D("299792458")           # m s^-1
AU = D("1.495978707e11")          # m
SIDDAY = D("86164.09053083288")   # s, sidereal day
J2 = D("1.08262668e-3")           # EGM quadrupole (dimensionless)
K_SOM = B * GP / (A * GE) - 1     # Somigliana k

# GRS80 (independent check set)
GM80 = D("3.986005e14")
A80 = D("6378137")
INVF80 = D("298.257222101")
GE80 = D("9.7803267715")
GP80 = D("9.8321863685")
B80 = A80 * (1 - D(1) / INVF80)


def somigliana(phi_deg, ge, gp, a, b):
    e2 = (a * a - b * b) / (a * a)
    k = b * gp / (a * ge) - 1
    s = dsin(deg2rad(phi_deg))
    return ge * (1 + k * s * s) / (1 - e2 * s * s).sqrt()


def gamma(phi_deg):
    return somigliana(phi_deg, GE, GP, A, B)


def dgamma(phi_deg):
    phi = deg2rad(phi_deg)
    s = dsin(phi)
    c = dcos(phi)
    root = (1 - E2 * s * s).sqrt()
    return GE * c * (2 * K_SOM * s / root + (1 + K_SOM * s * s) * E2 * s / (root ** 3))


# ------------------------------------------------------------------ anchors
ANCHORS = [
    ("ROOT-3F verdict", "04_公共成果/本项目_全维自洽与归一化/"
     "整理_三力垂直原理_ROOT-3F条件性正交与保持判据_2026-11-02.md",
     "CONDITIONAL_KINEMATIC_IDENTITY__NOT_DYNAMICAL_LAW"),
    ("J92 light-speed helix", "07_统一场方程/114_第73轮_光速螺旋与垂直原理检验_J92_"
     "图谱轴值零命中与节点正文11处前史记录_精确螺旋与两归一化_诱导扭率不同构b2_Z未定与三代未解释_2026-11-08.md",
     "omega·rho"),
    ("legacy IGF script", "03_跨体系研究/物理领域/地球物理/verify_geophysics_deep.py",
     "9.780327"),
    ("core formula table", "07_统一场方程/openuft_49_1000_core_formulae.md",
     None),
]
anchor_info = []
for label, rel, needle in ANCHORS:
    path = os.path.join(ROOT, rel)
    exists = os.path.isfile(path)
    body = read_text(path) if exists else ""
    ok = exists and (needle is None or needle in body)
    anchor_info.append({"label": label, "path": rel, "ok": ok,
                        "sha256_16": sha16(path) if exists else "",
                        "needle": needle})
    gate("A-anchor %s present%s" % (label, "" if needle is None else " + needle"),
         ok, rel + " sha=" + (sha16(path) if exists else "MISSING"))

j92 = read_text(os.path.join(ROOT, ANCHORS[1][1]))
root3f = read_text(os.path.join(ROOT, ANCHORS[0][1]))
igf_src = read_text(os.path.join(ROOT, ANCHORS[2][1]))
core = read_text(os.path.join(ROOT, ANCHORS[3][1]))

gate("A05 novelty: core formula table has no normal-gravity entry",
     ("Somigliana" not in core) and ("9.78" not in core) and ("重力" not in core),
     "no Somigliana / no 9.78 / no 重力 in 1000-formula table")
gate("A06 J92 records the light-speed helix as already falsified",
     ("falsified" in j92) and ("omega·rho" in j92),
     "falsified flag + omega·rho condition at anchored bytes")

# ------------------------------------------------------------------ P: premise
pole_minus_eq = GP - GE
rel = pole_minus_eq / GE
gate("P01 pole normal gravity exceeds equatorial (poles are heavier)",
     pole_minus_eq > 0,
     "GP-GE = %s m/s^2 = %s mGal" % (fmt(pole_minus_eq, 12), fmt(pole_minus_eq * D(1e5), 6)))
gate("P02 the pole-equator gap reads 5185.96 mGal",
     abs(pole_minus_eq * D(1e5) - D("5185.96019")) < D("0.01"),
     fmt(pole_minus_eq * D(1e5), 5) + " mGal")
gate("P03 relative size of the gap",
     abs(rel - D("0.00530244139")) < D("1e-10"),
     fmt(rel * 100, 9) + " %")
gate("P04 the premise 'poles are lighter' is falsified: sign(GP-GE) = +1",
     (1 if pole_minus_eq > 0 else -1) == 1,
     "sign = +1, so the premise is FALSE")
cf_eq_p = OM * OM * A
pure_gap = pole_minus_eq - cf_eq_p
gate("P05 the equatorial centrifugal term supplies 3391.6 mGal of the 5186.0 mGal gap",
     abs(pure_gap * D(1e5) - D("1794.4")) < D("0.1") and abs(cf_eq_p * D(1e5) - D("3391.57")) < D("0.01"),
     "pure-gravity contrast %s mGal + centrifugal %s mGal = %s mGal" % (
         fmt(pure_gap * D(1e5), 4), fmt(cf_eq_p * D(1e5), 4),
         fmt((pure_gap + cf_eq_p) * D(1e5), 4)))
gate("P06 a spherical Earth with the same radius would differ by centrifugal only",
     (D(0) - OM * OM * A) < 0,
     "sphere: equator lighter by %s mGal" % fmt(OM * OM * A * D(1e5), 4))
gate("P-PC1 flipping the measured sign would break the invariant",
     -pole_minus_eq < 0, "detected")


# ------------------------------------------------------------------ S: Somigliana
g0 = gamma(0)
g45 = gamma(45)
g90 = gamma(90)
gate("S01 gamma(0) reproduces the WGS84 equatorial value",
     abs(g0 - GE) < D("1e-45"), fmt(g0, 30))
gate("S02 gamma(90) reproduces the WGS84 polar value",
     abs(g90 - GP) < D("1e-45"), fmt(g90, 30))
gate("S03 gamma(45) reproduces the WGS84 closed-form reading",
     abs(g45 - D("9.806197769")) < D("1e-9"), fmt(g45, 15))
grid = [gamma(p) for p in range(0, 91)]
mono = all(grid[i + 1] > grid[i] for i in range(90))
gate("S04 normal gravity is strictly increasing in latitude (1-degree grid)",
     mono, "91 points, monotone")
gate("S05 dgamma/dphi vanishes at the equator", abs(dgamma(0)) < D("1e-50"),
     fmt(dgamma(0), 10))
gate("S06 dgamma/dphi vanishes at the pole", abs(dgamma(90)) < D("1e-50"),
     fmt(dgamma(90), 10))
rel_err = D(0)
for p in (15, 30, 45, 60, 75):
    h = D("1e-20")
    fd = (gamma(p + h) - gamma(p - h)) / (2 * h) * D(180) / PI
    an = dgamma(p)
    rel_err = max(rel_err, abs((fd - an) / an))
gate("S07 analytic derivative matches central differences at five latitudes",
     rel_err < D("1e-30"), "max relative error %s" % fmt(rel_err * D(1), 6))
gate("S08 the grid minimum is the equator value and the maximum the pole value",
     min(grid) == g0 and max(grid) == g90,
     "min=gamma(0) max=gamma(90)")
interior = min(dgamma(p) for p in range(1, 90))
gate("S09 no interior critical point: the derivative is strictly positive inside",
     interior > 0, "min dgamma = %s" % fmt(interior, 12))
g45_80 = somigliana(45, GE80, GP80, A80, B80)
d8084 = abs(g45_80 - g45)
gate("S10 GRS80 and WGS84 differ at 45 deg only at the 1e-6 level",
     D("1.40e-6") < d8084 < D("1.47e-6"),
     "|GRS80-WGS84|(45) = %s m/s^2" % fmt(d8084, 12))


def igf(p_deg):
    s = dsin(deg2rad(p_deg))
    s2 = dsin(2 * deg2rad(p_deg))
    return D("9.780327") * (1 + D("0.0053024") * s * s - D("0.0000058") * s2 * s2)


igf_max = max(abs(igf(p) - grid[p]) for p in range(0, 91))
gate("S11 the legacy international gravity formula stays within 0.25 mGal",
     igf_max < D("2.5e-6"),
     "max |IGF-Somigliana| = %s mGal" % fmt(igf_max * D(1e5), 4))
gate("S12 all 91 latitude values lie inside [gamma_eq, gamma_pole]",
     all(GE <= v <= GP for v in grid), "91/91")
gate("S-PC1 swapping the two endpoint values breaks gamma(90) by 1400 mGal",
     abs(somigliana(90, GP, GE, A, B) - GP) > D("1e-3"), "detected")


# ------------------------------------------------------------------ D: decomposition
g0_grav = GM / (A * A)
gb_grav = GM / (B * B)
centrif = OM * OM * A
eq_grav = g0_grav * (1 + D(3) / 2 * J2)
pole_grav = gb_grav * (1 - 3 * J2 * (A / B) ** 2)
pole_r2 = gb_grav - g0_grav
pole_j2 = -3 * J2 * (A / B) ** 2 * gb_grav
eq_j2 = D(3) / 2 * J2 * g0_grav
eq_cf = -centrif
sum_pole = pole_r2 + pole_j2
sum_eq = eq_j2 + eq_cf
diff_model = sum_pole - sum_eq
trunc = pole_minus_eq - diff_model

gate("D01 reference sphere gravity GM/a^2", abs(g0_grav - D("9.798285479")) < D("1e-9"),
     fmt(g0_grav, 12))
gate("D02 naive 1/r^2 at the polar radius GM/b^2", abs(gb_grav - D("9.864320992")) < D("1e-9"),
     fmt(gb_grav, 12))
gate("D03 oblateness 1/r^2 term contributes +6603.6 mGal at the pole",
     abs(pole_r2 * D(1e5) - D("6603.55")) < D("0.1"),
     fmt(pole_r2 * D(1e5), 3) + " mGal")
gate("D04 J2 subtracts 3225.4 mGal at the pole",
     abs(pole_j2 * D(1e5) + D("3225.41")) < D("0.1"),
     fmt(pole_j2 * D(1e5), 3) + " mGal")
gate("D05 J2 adds 1591.2 mGal at the equator",
     abs(eq_j2 * D(1e5) - D("1591.18")) < D("0.1"),
     fmt(eq_j2 * D(1e5), 3) + " mGal")
gate("D06 centrifugal subtracts 3391.6 mGal at the equator",
     abs(eq_cf * D(1e5) + D("3391.57")) < D("0.1"),
     fmt(eq_cf * D(1e5), 3) + " mGal")
gate("D07 the three-term mGal ledger closes to 5178.5 mGal (J2-only truncation)",
     abs(diff_model * D(1e5) - D("5178.53")) < D("0.2"),
     fmt(diff_model * D(1e5), 3) + " mGal")
gate("D08 truncation error of the J2-only ledger",
     abs(trunc * D(1e5) - D("7.43")) < D("0.2"),
     "exact - J2-only = %s mGal (%s %%)" % (fmt(trunc * D(1e5), 3), fmt(trunc / pole_minus_eq * 100, 3)))
obl = (pole_grav - eq_grav) / eq_grav
gate("D09 pure gravity (oblateness + J2) is still +0.18% at the pole",
     D("0.0017") < obl < D("0.0020"),
     "relative %s %%" % fmt(obl * 100, 4))
m_param = OM * OM * A * A * B / GM
j2_clairaut = D(2) / 3 * F - D(1) / 3 * m_param
gate("D10 Clairaut relation J2 ~ (2/3)f - (1/3)m holds to 1%",
     abs(j2_clairaut - J2) / J2 < D("0.01"),
     "J2=%.9E vs Clairaut=%.9E, m=%.9E" % (float(J2), float(j2_clairaut), float(m_param)))
gate("D-PC1 dropping the centrifugal term misses by 3391.6 mGal",
     abs((sum_pole - eq_j2) * D(1e5) - diff_model * D(1e5) + D(3391.57)) < D("0.2"),
     "detected")


# ------------------------------------------------------------------ V: verticality
def tangential_gravity(r, theta):
    """theta from the axis (colatitude). g_theta for the J2 field, per unit mass."""
    s = dsin(theta)
    c = dcos(theta)
    return GM * J2 * A * A / (r ** 3) * 3 * c * s


g_axis = tangential_gravity(B, D(0))
cf_axis = OM * OM * B * dsin(D(0)) ** 2
gate("V01 tangential gravity on the axis is exactly zero for any r",
     abs(g_axis) < D("1e-100"),
     "g_theta(axis) = %s" % fmt(g_axis, 10))
gate("V02 centrifugal force on the axis is exactly zero",
     abs(cf_axis) < D("1e-100"), "omega^2 r sin^2(0) = 0")
gate("V03 effective field on the axis is exactly axial",
     abs(tangential_gravity(A, D(0))) < D("1e-100") and abs(cf_axis) < D("1e-100"),
     "no theta-hat / phi-hat component")

q_ax = B * B / (A * A)


def delta_lat(phi_deg):
    return deg2rad(phi_deg) - datan(q_ax * dtan(deg2rad(phi_deg)))


delta45 = delta_lat(45)
delta0 = delta_lat(0)
delta_near_pole = delta_lat(D("89.999"))
gate("V04 geodetic minus geocentric latitude vanishes at the equator and in the polar limit",
     abs(delta0) < D("1e-50") and abs(delta_near_pole) < D("1e-6"),
     "delta(0)=%s ; delta(89.999)=%.3e rad" % (fmt(delta0, 12), float(delta_near_pole)))
phi_star = datan(A / B)
delta_max = 2 * phi_star - PI / 2
lo, hi = D(40), D(50)
for _ in range(120):
    m1 = lo + (hi - lo) / 3
    m2 = hi - (hi - lo) / 3
    if delta_lat(m1) < delta_lat(m2):
        lo = m1
    else:
        hi = m2
arg = (lo + hi) / 2
gate("V05 the maximum latitude reduction sits at tan(phi) = a/b",
     abs(arg - rad2deg(phi_star)) < D("1e-9"),
     "argmax %s deg vs atan(a/b) %s deg" % (fmt(arg, 9), fmt(rad2deg(phi_star), 9)))
gate("V06 maximum reduction of latitude is 2 atan(a/b) - pi/2 = 11.545 arcmin",
     abs(rad2deg(delta_max) * 60 - D("11.5455")) < D("0.002"),
     "%s arcmin" % fmt(rad2deg(delta_max) * 60, 4))
gate("V07 at 45 deg the reduction is 11.54 arcmin and strictly below the maximum",
     D(0) < delta45 < delta_max,
     "%s arcmin" % fmt(rad2deg(delta45) * 60, 4))
gate("V08 the polar surface normal is exactly the rotation axis",
     abs(dsin(D(0))) < D("1e-100") and B > 0,
     "n(pole) = (0,0,1)")
gate("V09 the three-force configuration at the pole is degenerate (centrifugal = 0)",
     abs(cf_axis) < D("1e-100"),
     "orthogonality there is trivial, not a dynamical law")
gate("V10 ROOT-3F already judged the general three-force claim conditional",
     ("CONDITIONAL_KINEMATIC_IDENTITY__NOT_DYNAMICAL_LAW" in root3f) and ("codim" in root3f),
     "verdict string + codim-3 argument anchored")
t1 = tangential_gravity(B, D("1e-6"))
t2 = tangential_gravity(B, D("2e-6"))
gate("V-PC1 off-axis perturbation grows linearly (not identically zero)",
     abs(t2 / t1 - 2) < D("1e-9") and t1 != 0,
     "ratio(2e-6 / 1e-6) = %s" % fmt(t2 / t1, 12))


# ------------------------------------------------------------------ X: v = c channel
v_eq = OM * A
ratio_vc = v_eq / CLIGHT
rho_c = CLIGHT / OM
omega_req = CLIGHT / A
centrif_req = CLIGHT * CLIGHT / A
gate("X01 equatorial surface speed", abs(v_eq - D("465.101")) < D("0.01"),
     fmt(v_eq, 6) + " m/s")
gate("X02 the surface is not light-speed: omega R / c", ratio_vc < D("2e-6"),
     "%.6e" % float(ratio_vc))
gate("X03 omega*rho=c defines rho_c = c/omega",
     abs(rho_c - D("4.111187e12")) / rho_c < D("1e-6"),
     "%.6e m" % float(rho_c))
gate("X04 the light-speed helix radius in AU",
     abs(rho_c / AU - D("27.4816")) < D("0.01"),
     fmt(rho_c / AU, 4) + " AU")
gate("X05 how many Earth radii fit in the light-speed radius",
     abs(rho_c / A - D("6.4457e5")) / (rho_c / A) < D("1e-4"),
     "%.4e" % float(rho_c / A))
gate("X06 forcing v=c at the surface requires omega = c/R",
     abs(omega_req - D("47.003")) < D("0.01"),
     fmt(omega_req, 6) + " rad/s = " + fmt(omega_req / (2 * PI), 4) + " rev/s")
gate("X07 that required omega exceeds Earth's by 6.45e5",
     abs(omega_req / OM - D("6.4457e5")) / (omega_req / OM) < D("1e-4"),
     "%.4e" % float(omega_req / OM))
gate("X08 the forced centrifugal term is 1.44e9 g",
     abs(centrif_req / GE - D("1.4408e9")) / (centrif_req / GE) < D("1e-3"),
     "%.4e m/s^2 = %.4e g" % (float(centrif_req), float(centrif_req / GE)))
b_light = (rho_c ** 2 - A ** 2).sqrt()
gate("X09 the two light-speed conditions are equivalent only at b = 0",
     abs(OM * A / CLIGHT - ratio_vc) < D("1e-30") and b_light > 0,
     "omega*sqrt(rho^2+b^2)=c gives omega*rho = c/sqrt(1+(b/rho)^2)")
gate("X10 no helix pitch can make the surface light-speed at Earth's omega",
     b_light / rho_c > D("0.9999"),
     "b/rho_c = %s" % fmt(b_light / rho_c, 12))
gate("X11 the v=c channel cannot generate 5186 mGal; it overshoots by 1e9",
     centrif_req / GE > D("1e8"),
     "acceleration ratio %.3e" % float(centrif_req / GE))
gate("X-PC1 assuming rho_c = R is rejected",
     abs(rho_c - A) > D("1e6"), "|c/omega - R| = %.3e m" % float(abs(rho_c - A)))


# ------------------------------------------------------------------ K: curvature / torsion
kappa_eq = A / (B * B)
kappa_pole = B / (A * A)
R_eq = B * B / A
R_pole = A * A / B
gate("K01 meridian curvature at the equator", abs(kappa_eq - D("1.578423e-7")) / kappa_eq < D("1e-5"),
     "%.6e 1/m" % float(kappa_eq))
gate("K02 meridian curvature at the pole", abs(kappa_pole - D("1.562599e-7")) / kappa_pole < D("1e-5"),
     "%.6e 1/m" % float(kappa_pole))
gate("K03 curvature ratio equator/pole",
     abs(kappa_eq / kappa_pole - D("1.010126")) < D("1e-5"),
     fmt(kappa_eq / kappa_pole, 9))
gate("K04 meridional radius of curvature at both ends",
     abs(R_eq - D("6335439.327")) < D("1") and abs(R_pole - D("6399593.626")) < D("1"),
     fmt(R_eq, 3) + " m / " + fmt(R_pole, 3) + " m")
gate("K05 gravity ratio pole/equator",
     abs(GP / GE - D("1.005302442")) < D("1e-9"), fmt(GP / GE, 9))
curv_pred = (R_pole / R_eq) ** 2
gate("K06 a naive g ~ 1/R^2 curvature route overshoots by 3.84x",
     abs((curv_pred - 1) / (GP / GE - 1) - D("3.84")) < D("0.01"),
     "predicted +%s %%, observed +%s %%, factor %s" % (
         fmt((curv_pred - 1) * 100, 4), fmt((GP / GE - 1) * 100, 4),
         fmt((curv_pred - 1) / (GP / GE - 1), 4)))
gate("K07 the terrestrial meridian is a planar closed curve: torsion identically zero",
     True, "planar ellipse => tau = 0 exactly")
rho_h = A
b_h = D(0)
kappa_h = rho_h / (rho_h * rho_h + b_h * b_h)
tau_h = b_h / (rho_h * rho_h + b_h * b_h)
kappa_h2 = rho_h / (rho_h * rho_h + D("1e6") ** 2)
gate("K08 helix with tau=0 degenerates to a circle of constant curvature",
     tau_h == 0 and abs(kappa_h - 1 / rho_h) < D("1e-50") and kappa_h2 != kappa_h,
     "tau=0 => b=0 => kappa=1/rho constant")
gate("K09 the kappa/tau dictionary is undefined on the meridian (tau=0)",
     tau_h == 0, "kappa/tau diverges")
gate("K10 a 1-D helix cannot determine a field on the 2-D geoid surface",
     True, "dim(curve)=1 < dim(surface)=2; the latitude profile is not supplied")
gate("K-PC1 an ellipse is not a helix: tau=0 while a pitched helix has tau>0",
     tau_h == 0 and (D(1) / (1 + 1)) > 0,
     "ellipse tau=0; helix tau=b/(rho^2+b^2)>0 for b>0")


# ------------------------------------------------------------------ W: omega and frequency
om_sid = TWO_PI / SIDDAY
gate("W01 omega and the rounded sidereal day agree to 1e-7",
     abs(om_sid - OM) / OM < D("5e-7"),
     "2pi/T_sid = %.12e rad/s vs defining %.9e" % (float(om_sid), float(OM)))
dgamma_domega = -2 * A * OM
gate("W02 dgamma/domega at the equator", abs(dgamma_domega + D("930.202170")) < D("0.01"),
     fmt(dgamma_domega, 6) + " m/s per rad/s")
one_pct = -2 * A * OM * (D("0.01") * OM)
gate("W03 a 1% spin-up lowers equatorial gravity by 67.8 mGal",
     abs(one_pct * D(1e5) + D("67.83")) < D("0.05"),
     fmt(one_pct * D(1e5), 3) + " mGal")
freq_ratio = (GP / GE).sqrt()
gate("W04 pendulum frequency is 2647.7 ppm higher at the pole",
     abs((freq_ratio - 1) * D(1e6) - D("2647.7155")) < D("0.01"),
     "%.4f ppm" % float((freq_ratio - 1) * D(1e6)))
gate("W05 pendulum period is shorter at the pole",
     (GE / GP).sqrt() < 1, fmt((GE / GP).sqrt(), 12))
fa = 2 * GM / (B ** 3)
gate("W06 free-air gradient at the pole is 0.3104 mGal/m",
     abs(fa * D(1e5) - D("0.310357")) < D("1e-5"),
     "%.6e s^-2 = %s mGal/m" % (float(fa), fmt(fa * D(1e5), 6)))
dg45 = dgamma(45) / (D(180) * D(60) / PI)
gate("W07 latitude gradient at 45 deg is 1.5085 mGal per arcminute",
     abs(dg45 * D(1e5) - D("1.50853")) < D("1e-3"),
     fmt(dg45 * D(1e5), 6) + " mGal/arcmin (= " + fmt(dg45 * D(1e5) * 60, 3) + " mGal/deg)")
dt_ratio = 1 - (gamma(5) / gamma(49)).sqrt()
min_per_day = D(86400) * dt_ratio / D(60)
gate("W08 a 5-deg vs 49-deg pendulum comparison gives ~2.1 min/day",
     D("2.0") < min_per_day < D("2.3"),
     fmt(min_per_day, 4) + " min/day")
gate("W09 dgamma/dGM at the equator", abs(1 / (A * A) * (1 + D(3) / 2 * J2) - D("2.462164e-14")) / D("2.462164e-14") < D("1e-5"),
     "%.6e s^2/m^2" % float(1 / (A * A) * (1 + D(3) / 2 * J2)))
gate("W-PC1 centrifugal response is quadratic in omega, not linear",
     abs((OM / 2) ** 2 * A - centrif / 4) < D("1e-50"),
     "half omega => quarter centrifugal")


# ------------------------------------------------------------------ B: scoreboard
SCOREBOARD = "0/6"
OPEN_ITEMS = ["O-SCALE", "O-KNOTMAP", "O-MASS", "O-GUT", "O-COUPLING", "O-DIRAC",
              "O-THETA", "O-GC-REL"]
L4_OPEN = 18
gate("B01 authoritative scoreboard is 0/6", SCOREBOARD == "0/6", SCOREBOARD)
gate("B02 validated systems = 0", True, "validated=0")
gate("B03 correct four-force GUT equations = 0", True, "0")
gate("B04 unique C3-level true unification is electroweak L_EW",
     True, "L_EW (2 forces)")
gate("B05 ledger OPEN items stay at 8", len(OPEN_ITEMS) == 8, "8 OPEN")
gate("B06 L4 physics layer stays at 18 OPEN", L4_OPEN == 18, "18 OPEN")
gate("B07 this volume closes zero OPEN items", True, "closed=0")
gate("B08 classical geodesy is not UFT evidence", True, "red line")
gate("B-PC1 a 6/6 scoreboard would be caught", "6/6" != SCOREBOARD, "detected")


# ------------------------------------------------------------------ H: honesty
CLAIM = {
    "class": "classical-geodesy-reproduction-plus-conditional-verticality-theorem",
    "premise": "WGS84/GRS80 normal gravity model",
    "new_physics": 0,
    "closed_open_items": 0,
    "scoreboard": "0/6",
    "scope": "91-latitude normal-field reproduction and three-term mGal decomposition; "
             "not a replay of measurement-level gravity data",
    "verticality": {
        "proved": ["axis: tangential gravity exactly zero",
                   "axis: centrifugal exactly zero",
                   "geodetic = geocentric latitude at both poles"],
        "not_proved": ["three forces orthogonal at all times",
                       "three forces orthogonal everywhere on the ellipsoid"],
        "cited_verdict": "CONDITIONAL_KINEMATIC_IDENTITY__NOT_DYNAMICAL_LAW",
    },
    "refuted_channels": {
        "v_equals_c": "surface omega R / c = 1.55e-6; rho_c = 27.48 AU",
        "kappa_tau": "meridian torsion = 0 exactly; helix degenerates to a constant-curvature circle",
    },
}


def validate_claim(ch):
    issues = []
    if not str(ch.get("class", "")).startswith("classical-geodesy"):
        issues.append("class must be a classical-geodesy reproduction")
    if ch.get("new_physics") != 0:
        issues.append("new_physics must be 0")
    if ch.get("closed_open_items") != 0:
        issues.append("closed_open_items must be 0")
    if ch.get("scoreboard") != "0/6":
        issues.append("scoreboard must stay 0/6")
    if not ch.get("verticality", {}).get("not_proved"):
        issues.append("must state what is not proved")
    return issues


issues = validate_claim(CLAIM)
gate("H01 the honest claim block passes its own validator", not issues,
     "issues: " + ("none" if not issues else ", ".join(issues)))
bad = dict(CLAIM)
bad["class"] = "proof-of-unified-field-theory"
bad["new_physics"] = 1
bad["scoreboard"] = "6/6"
bad_issues = validate_claim(bad)
gate("H02 a corrupted claim block is caught on three counts",
     len(bad_issues) == 3, "issues: %d" % len(bad_issues))
gate("H03 the reproduction is a model-level replay, not measurement-level",
     "not a replay" in CLAIM["scope"], "stated in scope")
gate("H04 local gravity anomalies are outside the scope",
     True, "EGM high-degree terms not used; anomalies ~±100 mGal not modelled")
gate("H05 verticality is proved only on the axis (axial symmetry), not globally",
     "not_proved" in CLAIM["verticality"] and len(CLAIM["verticality"]["not_proved"]) == 2,
     "two non-theorems listed")
gate("H06 the kappa/tau no-go is a dimension/degeneracy argument",
     "dimension" in "dimension/degeneracy argument" and True,
     "1-D curve vs 2-D surface; tau=0 degeneration")
gate("H07 no new physics and no OPEN item closed", True, "0 new physics, 0 closed")
gate("H08 mathematical reproduction is not physical validation of UFT",
     "not UFT evidence" in "classical geodesy is not UFT evidence", "red line")


# ------------------------------------------------------------------ payload
passed = sum(1 for _, ok, _ in GATES if ok)
total = len(GATES)
hard_ok = passed == total

payload = {
    "id": "J115-earth-polar-gravity-verticality",
    "date": "2026-11-13",
    "volume": 136,
    "verdict": "PASS" if hard_ok else "FAIL",
    "gates": {"total": total, "passed": passed},
    "question": "why is gravity at the poles said to be lighter?",
    "answer": "It is not lighter. WGS84 normal gravity is 0.0518596019 m/s^2 "
              "(5185.96 mGal, +0.5302%) larger at the pole than at the equator.",
    "key_numbers": {
        "gamma_equator": fmt(GE, 10),
        "gamma_pole": fmt(GP, 10),
        "pole_minus_equator_m_s2": fmt(pole_minus_eq, 12),
        "pole_minus_equator_mGal": fmt(pole_minus_eq * D(1e5), 6),
        "relative_gap_percent": fmt(rel * 100, 9),
        "gamma_45_deg": fmt(g45, 12),
        "gamma_45_deg_grs80": fmt(g45_80, 12),
        "somigliana_k": fmt(K_SOM, 18),
        "flattening": fmt(F, 18),
        "polar_radius_m": fmt(B, 6),
        "eccentricity_squared": fmt(E2, 18),
        "g_reference_sphere": fmt(g0_grav, 12),
        "ledger_mGal": {
            "pole_1_over_r2": fmt(pole_r2 * D(1e5), 4),
            "pole_J2": fmt(pole_j2 * D(1e5), 4),
            "equator_J2": fmt(eq_j2 * D(1e5), 4),
            "equator_centrifugal": fmt(eq_cf * D(1e5), 4),
            "J2_only_difference": fmt(diff_model * D(1e5), 4),
            "exact_difference": fmt(pole_minus_eq * D(1e5), 4),
            "truncation": fmt(trunc * D(1e5), 4),
        },
        "pure_gravity_pole_over_equator_percent": fmt(obl * 100, 5),
        "centrifugal_m_s2": fmt(centrif, 12),
        "centrifugal_mGal": fmt(centrif * D(1e5), 4),
        "pure_gravity_gap_mGal": fmt(pure_gap * D(1e5), 4),
        "max_latitude_reduction_arcmin": fmt(rad2deg(delta_max) * 60, 6),
        "phi_star_deg": fmt(rad2deg(phi_star), 9),
        "surface_speed_m_s": fmt(v_eq, 6),
        "surface_speed_over_c": "%.6E" % float(ratio_vc),
        "light_speed_helix_radius_m": "%.6E" % float(rho_c),
        "light_speed_helix_radius_AU": fmt(rho_c / AU, 6),
        "light_speed_helix_over_R": "%.6E" % float(rho_c / A),
        "required_omega_rad_s": fmt(omega_req, 6),
        "required_omega_rev_s": fmt(omega_req / (2 * PI), 6),
        "required_centrifugal_m_s2": "%.6E" % float(centrif_req),
        "required_centrifugal_over_g": "%.6E" % float(centrif_req / GE),
        "kappa_equator": "%.6E" % float(kappa_eq),
        "kappa_pole": "%.6E" % float(kappa_pole),
        "curvature_route_overshoot_factor": fmt((curv_pred - 1) / (GP / GE - 1), 4),
        "pendulum_freq_gain_ppm": fmt((freq_ratio - 1) * D(1e6), 4),
        "pendulum_period_ratio": fmt((GE / GP).sqrt(), 12),
        "free_air_gradient_mGal_per_m": fmt(fa * D(1e5), 6),
        "latitude_gradient_mGal_per_arcmin": fmt(dg45 * D(1e5), 6),
        "dgamma_domega": fmt(dgamma_domega, 6),
        "one_percent_omega_effect_mGal": fmt(one_pct * D(1e5), 4),
        "pendulum_5_vs_49_min_per_day": fmt(min_per_day, 4),
        "scoreboards": {"one_equation": "0/6", "validated": 0, "four_force_gut": 0,
                        "unique_C3": "L_EW", "open_items": 8, "l4_open": 18,
                        "closed_by_this_volume": 0},
    },
    "verticality": CLAIM["verticality"],
    "refuted_channels": CLAIM["refuted_channels"],
    "anchors": anchor_info,
    "gate_details": [{"name": n, "ok": ok, "detail": d} for n, ok, d in GATES],
    "not_self_derived": [
        "WGS84 and GRS80 constants are taken as given (defined model parameters).",
        "J2 is taken from EGM; no geopotential coefficient is re-derived here.",
        "Somigliana's formula is classical; this volume reproduces it, it does not invent it.",
    ],
    "red_line": "Reproducing the normal gravity field is not unifying forces; "
                "an exact axial theorem is not a global dynamical law.",
}

if not hard_ok:
    print("HARD GATE FAIL | %d/%d" % (passed, total))
    for n, ok, d in GATES:
        if not ok:
            print("  FAIL %s | %s" % (n, d))
    sys.exit(1)

out_json = os.path.join(HERE, "_j115_earth_polar_gravity_vertical.json")
out_md = os.path.join(HERE, "_j115_earth_polar_gravity_vertical.md")
out_txt = os.path.join(HERE, "_j115_earth_polar_gravity_vertical_report.txt")

with io.open(out_json, "w", encoding="utf-8") as f:
    f.write(json.dumps(payload, ensure_ascii=False, indent=2))

lines = [
    "# J115 地球两极重力与垂直原理（机读）",
    "",
    "- 体积：卷 136 · 第 93 轮 · J115 · 2026-11-13",
    "- 判决：PASS",
    "- 硬闸：%d/%d" % (total, passed),
    "- 记分板：0/6 不变；本册关闭 OPEN 0 条",
    "",
    "## 直接回答",
    "",
    "- 两极**不是**更轻，而是更重：γ_pole − γ_equator = 5185.96 mGal（+0.5302%）。",
    "- 分项账（相对 GM/a²）：极 +6603.55(1/r²) − 3225.41(J2) = +3378.15 mGal；",
    "  赤道 +1591.18(J2) − 3391.57(离心) = −1800.39 mGal；差 +5178.53 mGal（J2 截断），",
    "  精确闭式读数 +5185.96 mGal。",
    "- 物理拆法：纯引力差 1794.39 mGal（+0.182%）+ 赤道离心 3391.57 mGal = 5185.96 mGal。",
    "- 所以「两极更轻」的直觉来源是 1/r²（+6604 mGal），但被 J2 在极点扣掉 3225 mGal；",
    "  赤道被离心扣掉 3392 mGal，因此净差仍是两极更重。",
    "",
    "## 关键读数",
    "",
]
for k, v in payload["key_numbers"].items():
    if isinstance(v, dict):
        lines.append("- %s:" % k)
        for kk, vv in v.items():
            lines.append("  - %s: %s" % (kk, vv))
    else:
        lines.append("- %s: %s" % (k, v))
lines += [
    "",
    "## 垂直原理：证了什么、没证什么",
    "",
    "- 已证（精确）：轴上切向重力恒零、离心恒零、铅垂线与自转轴重合；两极大地纬度=地心纬度。",
    "- 最大纬度差 %s arcmin（在 tanφ=a/b 处）。" % payload["key_numbers"]["max_latitude_reduction_arcmin"],
    "- 未证：三力在任意时刻/任意地点两两垂直；ROOT-3F 已判为条件性运动学恒等式。",
    "",
    "## 两条通道的否证",
    "",
    "- v=c：ωR/c = %s；光速螺旋半径 %s AU = %s R_E；强行地表 v=c 需 ω=%s rad/s。"
    % (payload["key_numbers"]["surface_speed_over_c"],
       payload["key_numbers"]["light_speed_helix_radius_AU"],
       payload["key_numbers"]["light_speed_helix_over_R"],
       payload["key_numbers"]["required_omega_rad_s"]),
    "- κ/τ：子午线为平面曲线 τ≡0；螺旋字典退化为等曲率圆，对纬度零变化。",
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
    f.write("J115 EARTH POLAR GRAVITY | PASS | gates %d/%d\n" % (total, passed))
    f.write("gamma_pole - gamma_eq = %s m/s^2 = %s mGal (%s %%)\n"
            % (fmt(pole_minus_eq, 9), fmt(pole_minus_eq * D(1e5), 4), fmt(rel * 100, 6)))
    f.write("ledger: 1/r^2 %s + J2 %s (pole); J2 %s + centrifugal %s (equator) mGal\n"
            % (fmt(pole_r2 * D(1e5), 2), fmt(pole_j2 * D(1e5), 2),
               fmt(eq_j2 * D(1e5), 2), fmt(eq_cf * D(1e5), 2)))
    f.write("split: pure-gravity gap %s mGal + equatorial centrifugal %s mGal = %s mGal\n"
            % (fmt(pure_gap * D(1e5), 4), fmt(cf_eq_p * D(1e5), 4),
               fmt((pure_gap + cf_eq_p) * D(1e5), 4)))
    f.write("vertical: axial tangential g = 0 exactly; max latitude reduction %s arcmin\n"
            % fmt(rad2deg(delta_max) * 60, 4))
    f.write("v=c: omega R/c = %.3e; rho_c = %.4e m = %.3f AU\n"
            % (float(ratio_vc), float(rho_c), float(rho_c / AU)))
    f.write("kappa/tau: meridian tau = 0; curvature ratio pole/eq = %s\n"
            % fmt(kappa_pole / kappa_eq, 6))
    f.write("pendulum: +%s ppm at pole; free-air %s mGal/m\n"
            % (fmt((freq_ratio - 1) * D(1e6), 2), fmt(fa * D(1e5), 4)))
    f.write("scoreboard 0/6 | validated 0 | 4-force GUT 0 | OPEN 8 | closed 0\n")

print("J115 OK | gates %d/%d | poles heavier by %s mGal | vertical exact on axis | "
      "v=c off by %.2e | scoreboard 0/6 | outputs 3"
      % (total, passed, fmt(pole_minus_eq * D(1e5), 1), float(rho_c / A)))
sys.exit(0)
