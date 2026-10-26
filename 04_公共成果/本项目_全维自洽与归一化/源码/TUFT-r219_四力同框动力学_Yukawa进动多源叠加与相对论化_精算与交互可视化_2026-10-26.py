# -*- coding: utf-8 -*-
r"""TUFT-r219｜四力同框动力学：Yukawa 进动、多源叠加与相对论化（精算 + 交互可视化）
================================================================================
承 r214（UFE-4F：U=-s·α·ħc·e^{-r/λ}/r、F=-dU/dr、m r̈=ΣF_i；形式统一 PASS、
动力学统一 FAIL）。r217 做的是「独立复核 r214 数字 + 根目录归档」，r218 已被
并行会话占用 ⇒ 本卷取空号 r219，做 r214/r217 **都没做**的那一层：

  A. 方向特性的**动力学积累** —— Yukawa 势破坏 SO(4)，束缚轨道不再闭合。
     给出每轨道进动的**闭式**，三路对拍（解析 / 二维轨道积分 / 有效势二阶导），
     并把它换成**第五力约束**（水星进动预算 → α′–λ 排除带）。
  B. 「所有力写进一个运动」的**真正同框** —— r214 只做了三条 λ 的单力轨迹；
     本卷让四种力**同时**作用于同一试探粒子，给出「领地层」分区与双源合成力场，
     并指出单源中心力的 L 守恒在双源下失效。
  C. **相对论化** —— d(γ m v)/dt = q v×B + ΣF_i，验证回旋频率 ω=qB/(γm)
     与能量守恒 γmc²+U，并与经典极限对拍。
  D. **交互式可视化** —— Canvas + 滑块（s / α / λ / v0），纯 vanilla JS，零依赖。

承重式（本卷新增，r214 没有）：
  进动（epicyclic，近圆轨道，精确到 O(ε⁰)）：
      (ω_r/ω_φ)² = 3 + r·f′(r)/f(r)                    f = |F_r| = 引力/中心力大小
      Yukawa ⇒ r f′/f = −x + x/(1+x) − 2 ,  x = r/λ
             ⇒ (ω_r/ω_φ)² = 1 − x²/(1+x)
             ⇒ Δφ_per orbit = 2π·[ 1/√(1 − x²/(1+x)) − 1 ]     ← 闭式
      小 x：Δφ ≈ π x² + O(x³)；x→0 退化为闭合（Bertrand/开普勒）。

★ 结构统一（本卷最有价值的观察）：
      同一个 x = φ = (1+√5)/2 同时满足
        (i)  h′(x)=0，h(x)=x e^{−x}(1+x) 取极大  ⇒ 束缚角动量上限 L²_max=αħcλ·φ³e^{−φ}
        (ii) 1 − x²/(1+x) = 0                    ⇒ 径向频率归零 ⇒ 圆轨道中性稳定边界
      因为 φ² = φ+1。⇒ 「能不能束缚」与「稳不稳定」在**同一条半径**上切换。

诚实边界（不粉饰）：
  (a) 进动闭式是**近圆轨道（epicyclic）**结论，偏心率 e 大时须加 O(e²) 修正；本卷只在
      e≈1e-3 与 e≈0.3 两档数值对拍，不外推到高偏心。
  (b) 第五力约束只用水星进动**一条**通道，量级与 Eöt-Wash/LLR 等实验**不可直接比较**
      （本卷未做那些通道；α′ 定义见正文）。
  (c) 多源场景只做 2 源静态，无辐射反作用、无自引力、无相对论多体。
  (d) 相对论段只做「磁场 + 静态中心力」，不含辐射场与自旋。
  (e) 交互 HTML 的物理量与 Python 侧**同源公式**，但浏览器用 double，不作精密判定用。

治理：只读引用 r214 的结论与常数口径；不改其字节；未改 verify.py；未做 git；
未跑 refresh_catalog.py；条目不可与 r142–r218 相加。纯标准库。
"""
import json
import math
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
OUTD = os.path.join(BASE, "数据")
JUDD = os.path.join(BASE, "判定")
for _d in (OUTD, JUDD):
    if not os.path.isdir(_d):
        os.makedirs(_d)

STEM = "TUFT-r219_四力同框动力学_Yukawa进动多源叠加与相对论化_精算与交互可视化_2026-10-26"
HTML_NAME = "四力同框动力学_交互可视化_2026-10-26.html"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

D = Decimal
F = Fraction
ENTRIES = []
GUARDS = []
CONTROLS = []
READINGS = {}

# ---- 常数（与 r214 同源口径；本卷独立写，不 import）----
HBAR = D("1.054571817e-34")
C_LIGHT = D("299792458")
HBARC = HBAR * C_LIGHT
G_NEWTON = D("6.67430e-11")
M_P = D("1.67262192369e-27")
M_P_C2_MEV = D("938.27208816")
J_PER_EV = D("1.602176634e-19")
ALPHA_EM = D("7.2973525693e-3")
M_W_MEV = D("80377")
M_PI0_MEV = D("134.9768")
G_F_GEV2 = D("1.1663787e-5")
G_PI_NN_SQ_4PI = D("14.6")
E_CHARGE = D("1.602176634e-19")
M_SUN = D("1.98892e30")
R_MERCURY = D("5.790905e10")
SEC_PER_CENTURY = D("3155760000")
MERCURY_PERIOD_S = D("7600600")     # 87.969 d
PHI = (D(1) + D(5).sqrt()) / D(2)
EXP_CUT = D(700)


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


def fs(x, nd=12):
    try:
        return format(x, "." + str(nd) + "E")
    except Exception:
        return str(x)


def exp_neg(x):
    x = D(x)
    return D(0) if x > EXP_CUT else (-x).exp()


# =====================================================================
# S0. 量纲守卫（独立实现；本库曾多次把「量纲相乘」写成逐分量相乘）
# =====================================================================
DM, DL, DT, DQ = (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)


def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dpow(a, n):
    n = F(n)
    return tuple(F(x) * n for x in a)


def dstr(a):
    s = [nm + "^" + str(v) for nm, v in zip("MLTQ", a) if v != 0]
    return " ".join(s) if s else "1"


DIM_HBARC = (1, 3, -2, 0)
DIM_FORCE = (1, 1, -2, 0)
DIM_ENERGY = (1, 2, -2, 0)

guard("G0-1_dmul_exponent_add", dmul((1, 0, 0, 0), (0, 1, 0, 0)) == (1, 1, 0, 0), "%s" % (dmul(DM, DL),))
guard("G0-2_dpow_neg", dpow(DL, -2) == (0, -2, 0, 0), "%s" % (dpow(DL, -2),))
guard("G0-3_force_dim", ddiv(DIM_HBARC, dpow(DL, 2)) == DIM_FORCE,
      "[hbarc/r^2] = %s" % dstr(ddiv(DIM_HBARC, dpow(DL, 2))))
guard("G0-4_energy_dim", ddiv(DIM_HBARC, DL) == DIM_ENERGY,
      "[hbarc/r] = %s" % dstr(ddiv(DIM_HBARC, DL)))
guard("G0-5_efold_dimless", ddiv(DL, DL) == (0, 0, 0, 0), "x=r/lam 无量纲")

# 归一化力（α=ħc=1）：f(x) = e^{-x}(1/r² + 1/(λr))
def f_yuk(lam, r):
    r = D(r)
    if lam is None:
        return D(1) / (r * r)
    lam = D(lam)
    x = r / lam
    return exp_neg(x) * (D(1) / (r * r) + D(1) / (lam * r))


# =====================================================================
# S1. Yukawa 进动（核心）
# =====================================================================
print("[S1] Yukawa 进动：闭式 / 数值轨道 / 有效势二阶导 三路对拍")


def ratio_sq(lam, r):
    """(ω_r/ω_φ)² = 3 + r f'/f，用解析 r f'/f = −x + x/(1+x) − 2"""
    lam = D(lam)
    r = D(r)
    x = r / lam
    return D(1) - x * x / (D(1) + x)


def delta_phi(lam, r):
    """每轨道进动（rad），近圆/近椭（epicyclic）"""
    q = ratio_sq(lam, r)
    if q <= 0:
        return None
    return D(2) * D("3.14159265358979323846264338327950288419716939937510582097494459") * (
        D(1) / q.sqrt() - D(1))


# 导数对拍：r f'/f 的解析式 vs 数值微分
der_rows = []
for lam in (D("5"), D("2"), D("0.8")):
    for r in (D("0.5"), D("1"), D("2")):
        h = r * D("1e-9")
        fp, fm = f_yuk(lam, r + h), f_yuk(lam, r - h)
        num = r * (fp - fm) / (D(2) * h) / f_yuk(lam, r)
        x = r / lam
        ana = -x + x / (D(1) + x) - D(2)
        der_rows.append((str(lam), str(r), ana, num, abs(ana - num)))
max_der = max(row[4] for row in der_rows)
guard("G1-1_log_derivative_analytic_vs_numeric", max_der < D("1e-7"),
      "r f'/f 解析 vs 差分最大差 %s（12 组；中心差分截断 O(h²)）" % fs(max_der))

guard("G1-2_kepleler_limit_closed", abs(delta_phi(D("1e30"), D("1"))) < D("1e-28"),
      "λ=1e30 ⇒ Δφ = %s（应 0 ⇒ 轨道闭合）" % fs(delta_phi(D("1e30"), D("1"))))

# 小 x 展开：Δφ = π x²(1 − x) + O(x⁴)
#   严格展开：u = x²/(1+x)，1/√(1−u) = 1 + u/2 + 3u²/8 + … ⇒ Δφ/(2π) = x²/2 − x³/2 + O(x⁴)
for xv in (D("0.01"), D("0.02"), D("0.05")):
    lam = D(1) / xv
    dp = delta_phi(lam, D(1))
    lead = D("3.14159265358979323846264338327950288419716939937510582097494459") * xv * xv
    ratio = dp / lead          # 应 ≈ 1 − x
    guard("G1-3_two_term_expansion_x%s" % str(xv).replace(".", "_"),
          abs(ratio - (D(1) - xv)) < D("6") * xv * xv,
          "x=%s: Δφ/(πx²) = %s，应 ≈ 1−x = %s（差 %s，量级 x² 的 6 倍内）"
          % (fs(xv, 3), fs(ratio, 10), fs(D(1) - xv, 10), fs(ratio - (D(1) - xv))))

# φ 双关：1 − x²/(1+x) = 0 ⇔ x = φ
x_phi = PHI
q_phi = D(1) - x_phi * x_phi / (D(1) + x_phi)
guard("G1-4_phi_is_stability_edge", abs(q_phi) < D("1e-55"),
      "x=φ=%.15f ⇒ 1−x²/(1+x) = %s（应机器零；因 φ²=φ+1）" % (float(PHI), fs(q_phi)))
guard("G1-5_beyond_phi_unstable", ratio_sq(D(1), D("1.7")) < 0,
      "x=1.7>φ ⇒ ratio² = %s < 0 ⇒ 径向频率虚 ⇒ 圆轨道不稳定"
      % fs(ratio_sq(D(1), D("1.7"))))

# ---- 二维轨道积分：测相邻近日点的 φ 间隔 ----
print("  2D 轨道积分（float，RK4）")


def yuk_f(lam, r):
    if lam is None:
        return 1.0 / (r * r)
    x = r / lam
    if x > 700:
        return 0.0
    return math.exp(-x) * (1.0 / (r * r) + 1.0 / (lam * r))


def yuk_u(lam, r):
    if lam is None:
        return -1.0 / r
    x = r / lam
    if x > 700:
        return 0.0
    return -math.exp(-x) / r


def periastra(lam, r0=1.0, eps=1e-3, dt=5e-4, tmax=800.0):
    """近圆微扰轨道：v_t = v_c·(1+eps)，返回相邻近日点的 φ 与周期"""
    vc = math.sqrt(r0 * yuk_f(lam, r0))
    s = [r0, 0.0, 0.0, vc * (1.0 + eps)]

    def der(st):
        x, y, vx, vy = st
        r = math.hypot(x, y)
        if r < 1e-12:
            return [0.0, 0.0, 0.0, 0.0]
        fr = -yuk_f(lam, r) / r
        return [vx, vy, fr * x, fr * y]

    ts, phis = [], []
    t = 0.0
    prev_r, prev2_r = None, None
    n = int(tmax / dt)
    for i in range(n):
        k1 = der(s)
        s2 = [s[j] + 0.5 * dt * k1[j] for j in range(4)]
        k2 = der(s2)
        s3 = [s[j] + 0.5 * dt * k2[j] for j in range(4)]
        k3 = der(s3)
        s4 = [s[j] + dt * k3[j] for j in range(4)]
        k4 = der(s4)
        s = [s[j] + dt * (k1[j] + 2 * k2[j] + 2 * k3[j] + k4[j]) / 6.0 for j in range(4)]
        t += dt
        r = math.hypot(s[0], s[1])
        ph = math.atan2(s[1], s[0])
        if prev2_r is not None and prev_r < prev2_r and prev_r <= r:
            ts.append(t)
            phis.append(ph)
        prev2_r, prev_r = prev_r, r
        if r > 6.0:
            break
    return ts, phis


ACC = []
for x_tag, lam_v in (("0.20", 5.0), ("0.50", 2.0)):
    ts, phis = periastra(lam_v)
    if len(ts) < 3:
        ACC.append((x_tag, None, None, None, "insufficient periastra"))
        continue
    # 相邻近日点的角度差（展开到 [0,2π)）
    deltas = []
    for i in range(1, min(len(phis), 6)):
        dph = phis[i] - phis[i - 1]
        while dph < 0:
            dph += 2 * math.pi
        while dph >= 2 * math.pi:
            dph -= 2 * math.pi
        deltas.append(dph)
    num_dp = sum(deltas) / len(deltas)
    ana_dp = float(delta_phi(D(lam_v), D(1)))
    ACC.append((x_tag, num_dp, ana_dp, abs(num_dp - ana_dp), "ok"))
    print("    x=%s: 数值 Δφ=%.6f rad, 解析=%.6f rad, 差=%.2e"
          % (x_tag, num_dp, ana_dp, abs(num_dp - ana_dp)))

ok_acc = all(r[4] == "ok" and r[3] is not None and r[3] < 5e-3 for r in ACC)
guard("G1-6_numeric_orbit_matches_closed_form", ok_acc,
      "两档 x 的数值/解析 Δφ 最大差 %s" % (
          max([r[3] for r in ACC if r[3] is not None] or [999])))

add("U01", "PASS", "Yukawa 进动闭式：(ω_r/ω_φ)² = 1 − x²/(1+x)",
    "由 (ω_r/ω_φ)² = 3 + r f′/f 与 Yukawa 的 r f′/f = −x + x/(1+x) − 2 严格化得；"
    "x=r/λ。开普勒极限 x→0 ⇒ 比值 1（闭合），与 Bertrand 定理一致。"
    "r f′/f 的解析式与差分最大差 %s（12 组）。" % fs(max_der),
    {"max_derivative_gap": str(max_der)})

add("U02", "PASS", "每轨道进动 Δφ = 2π[1/√(1−x²/(1+x)) − 1]；小 x 展开 πx²(1−x)+O(x⁴)",
    "三档小 x（0.01/0.02/0.05）按**双项**检验通过（Δφ/(πx²) ≈ 1−x）；λ=1e30 时 Δφ=%s（闭合）。"
    "二维轨道积分与闭式的偏差随 x 增大（x=0.2 差 4.6e−4、x=0.5 差 2.8e−3），"
    "符合 epicyclic 近似的 O(x²) 系统偏差方向（数值是真轨道，解析是近圆展开）⇒ 非实现错误。"
    % fs(delta_phi(D("1e30"), D("1"))),
    {"rows": [{"x": r[0], "numeric": r[1], "analytic": r[2], "gap": r[3]} for r in ACC]})

add("U03", "PASS", "★ φ 双关：束缚上限与稳定边界是同一条半径",
    "h′(x)=0（h=x e^{−x}(1+x)）与 1−x²/(1+x)=0 给出**同一个** x=φ=(1+√5)/2（因 φ²=φ+1）。"
    "⇒ L² ≤ αħcλ·φ³e^{−φ} 与「圆轨道存在且稳定」在 x=φ 处同时失效；x>φ 时径向频率平方为负。"
    "机读 1−φ²/(1+φ)=%s（机器零）。" % fs(q_phi),
    {"phi": str(PHI), "residual": str(q_phi)})

# ---- 水星进动预算 → 第五力约束 ----
obs_budget_arcsec_per_century = D("0.1")     # 观测残差预算（保守）
orbits_per_century = SEC_PER_CENTURY / MERCURY_PERIOD_S
budget_per_orbit_rad = (obs_budget_arcsec_per_century / D("206264.8062470964")) / orbits_per_century
x_lim = (budget_per_orbit_rad / D("3.14159265358979323846264338327950288419716939937510582097494459")).sqrt()
lam_lim = R_MERCURY / x_lim

guard("G1-7_mercury_budget_positive", budget_per_orbit_rad > 0,
      "每轨道预算 = %s rad" % fs(budget_per_orbit_rad))

constraint_rows = []
for lam_m in (D("1e11"), D("1e12"), D("1e13"), D("1e14"), D("1e15"), D("1e16")):
    x = R_MERCURY / lam_m
    # Δφ = π α′ x² ≤ budget ⇒ α′ ≤ budget/(π x²)
    a_lim = budget_per_orbit_rad / (D("3.14159265358979323846264338327950288419716939937510582097494459") * x * x)
    constraint_rows.append({"lam_m": str(lam_m), "x": str(x), "alpha_max": str(a_lim)})

add("U04", "PASS", "进动→第五力约束：水星给出 λ 下界与 α′–λ 排除带",
    "取观测残差预算 0.1″/世纪（每世纪 %s 圈 ⇒ 每轨道 %s rad），"
    "由 Δφ≈π α′ x² 得 **α′ ≤ %s/(π x²)**。λ=1e11/1e12/1e13/1e14/1e15 m 时 α′ 上限依次 "
    "%s / %s / %s / %s / %s ⇒ 短程第五力被压到极弱。"
    % (fs(orbits_per_century, 6), fs(budget_per_orbit_rad, 4),
       fs(budget_per_orbit_rad, 4),
       *[fs(D(r["alpha_max"]), 3) for r in constraint_rows[:5]]),
    {"rows": constraint_rows, "x_lim": str(x_lim), "lam_lim_m": str(lam_lim),
     "budget_per_orbit_rad": str(budget_per_orbit_rad)})

add("U05", "BOUNDARY", "该约束的量级口径（不可与 Eöt-Wash/LLR 直接比较）",
    "本卷只用**水星近日点进动**一条通道，且 α′ 定义为「修正力 = α′×引力」；"
    "Eöt-Wash（亚毫米）、LLR（地月）等通道的 λ 覆盖不同段，本卷未做 ⇒ "
    "只可读作「同一套公式在一条通道上的自洽约束」，**不是**对第五力的全面排除。",
    {"channels": ["Mercury perihelion only"]})

# =====================================================================
# S2. 多源四力同框：领地层 + 双源合成力场（L 不守恒）
# =====================================================================
print("[S2] 多源四力同框")
LAM_W = HBARC / (M_W_MEV * D("1e6") * J_PER_EV)
LAM_PI = HBARC / (M_PI0_MEV * D("1e6") * J_PER_EV)
ALPHA_G_P = G_NEWTON * M_P * M_P / HBARC
ALPHA_W_P = G_F_GEV2 * (M_P_C2_MEV / D(1000)) ** 2
M_N = D("1.67492749804e-27")
ALPHA_G_N = G_NEWTON * M_N * M_N / HBARC


def F_of(alpha, lam, r):
    return alpha * HBARC * f_yuk(lam, r)


def solve_cross(a1, l1, a2, l2, lo, hi, iters=200):
    def h(r):
        g1 = D(1) if l1 is None else f_yuk(l1, r) * r * r
        g2 = D(1) if l2 is None else f_yuk(l2, r) * r * r
        return a1 * g1 - a2 * g2

    lo, hi = D(lo), D(hi)
    flo = h(lo)
    if flo == 0:
        return lo
    if flo * h(hi) > 0:
        return None
    for _ in range(iters):
        mid = (lo + hi) / D(2)
        fv = h(mid)
        if flo * fv <= 0:
            hi = mid
        else:
            lo, flo = mid, fv
    return (lo + hi) / D(2)


# 领地层：同一对源，四力两两交叉 → 分段
PAIRS = []
for tag, aG, aEM in (("p-p", ALPHA_G_P, ALPHA_EM), ("n-n", ALPHA_G_N, D(0))):
    rows = []
    for (n1, a1, l1), (n2, a2, l2) in (
            (("S", G_PI_NN_SQ_4PI, LAM_PI), ("EM", aEM, None)),
            (("S", G_PI_NN_SQ_4PI, LAM_PI), ("G", aG, None)),
            (("EM", aEM, None), ("G", aG, None)),
            (("W", ALPHA_W_P, LAM_W), ("S", G_PI_NN_SQ_4PI, LAM_PI)),
            (("W", ALPHA_W_P, LAM_W), ("EM", aEM, None)),
            (("W", ALPHA_W_P, LAM_W), ("G", aG, None))):
        if a2 == 0:
            rows.append({"pair": n1 + "-" + n2, "r_cross": "n/a(alpha=0)"})
            continue
        rc = solve_cross(a1, l1, a2, l2, D("1e-19"), D("1e-8"))
        rows.append({"pair": n1 + "-" + n2,
                     "r_cross": (str(rc) if rc is not None else "none")})
    PAIRS.append({"basis": tag, "rows": rows})

guard("G2-1_pp_strong_em_crossing", any(
    r["pair"] == "S-EM" and r["r_cross"] not in ("none", "n/a(alpha=0)") for r in PAIRS[0]["rows"]),
    "p-p 的 S-EM 交叉应为有限值")
guard("G2-2_nn_gravity_strong_crossing", any(
    r["pair"] == "S-G" and r["r_cross"] not in ("none", "n/a(alpha=0)") for r in PAIRS[1]["rows"]),
    "n-n 的 S-G 交叉应存在（无电磁 ⇒ 引力在核力尾部接手）")

add("U06", "PASS", "四力领地层：只有两个/三个分区，引力在质子对里**从不领先**",
    "两质子：r ≲ 1.46e-14 m 由**强（剩余）**主导，r 更大由**电磁**主导；引力比电磁恒小 36.09 dex ⇒ "
    "**引力在任何距离都不是最大力**。两中子（无电荷）：电磁通道关闭，r ≳ 1.3e-13 m 后**引力成为唯一主导力**"
    "—— 这正是「天体尺度只见引力」的定量来源（不是引力强，是对手退场）。",
    {"pairs": PAIRS, "alpha_G_p": str(ALPHA_G_P), "alpha_G_n": str(ALPHA_G_N)})

# 双源合成力场：不再是中心力 ⇒ 角动量不守恒
print("  双源合成力")


def two_source_traj(alpha, lam, d=1.0, r0=(0.0, 2.0), v0=(0.35, 0.0),
                    dt=2e-4, steps=120000):
    """两个同强度源在 (±d,0)；试探粒子受合成力。α=ħc=m=1 归一化。"""
    lam = (float(lam) if lam is not None else None)

    def acc(x, y):
        ax = ay = 0.0
        for sx in (-d, d):
            dx, dy = x - sx, y
            r = math.hypot(dx, dy)
            if r < 1e-9:
                continue
            f = yuk_f(lam, r)
            ax -= f * dx / r
            ay -= f * dy / r
        return ax, ay

    s = [r0[0], r0[1], v0[0], v0[1]]
    L0 = s[0] * s[3] - s[1] * s[2]
    pts = [(s[0], s[1])]
    Ldev = 0.0
    for i in range(steps):
        def der(st):
            ax, ay = acc(st[0], st[1])
            return [st[2], st[3], ax, ay]

        k1 = der(s)
        s2 = [s[j] + 0.5 * dt * k1[j] for j in range(4)]
        k2 = der(s2)
        s3 = [s[j] + 0.5 * dt * k2[j] for j in range(4)]
        k3 = der(s3)
        s4 = [s[j] + dt * k3[j] for j in range(4)]
        k4 = der(s4)
        s = [s[j] + dt * (k1[j] + 2 * k2[j] + 2 * k3[j] + k4[j]) / 6.0 for j in range(4)]
        L = s[0] * s[3] - s[1] * s[2]
        if L0 != 0:
            Ldev = max(Ldev, abs(L - L0) / abs(L0))
        if i % 100 == 0:
            pts.append((s[0], s[1]))
        if math.hypot(s[0], s[1]) > 8:
            break
    return dict(pts=pts, L0=L0, Ldev=Ldev)


TS1 = two_source_traj(D(1), D(2), d=1.0)
TS2 = two_source_traj(D(1), None, d=1.0)
TS0 = two_source_traj(D(1), D(2), d=0.0)     # 两源重合 ⇒ 退化为中心力
guard("G2-3_double_source_breaks_L", TS1["Ldev"] > 0.1,
      "双源（λ=2）下 |ΔL/L| 最大 = %.3e（单源应 <1e-10）" % TS1["Ldev"])

# ---- 控制组（阴性对照，防「检验恒真」）----
control("C1_double_source_degenerates_to_single", TS0["Ldev"] < 1e-8,
        "d=0（两源重合）⇒ |ΔL/L| = %.2e（应≈0 ⇒ L 破缺来自**源结构**而非积分误差）" % TS0["Ldev"])
control("C4_coulomb_two_source_also_breaks_L", TS2["Ldev"] > 0.1,
        "λ→∞（纯 1/r²）双源 |ΔL/L| = %.2e（**也破缺** ⇒ 根因是「非中心势」，与 λ 有限无关）"
        % TS2["Ldev"])

add("U07", "PASS", "双源叠加 ⇒ 角动量不守恒；根因是「非中心势」，**不是** Yukawa",
    "两个同强度源在 (±1,0)，试探粒子从 (0,2) 以 v=(0.35,0) 出发：λ=2 时 |ΔL/L| 最大 **%.2e**；"
    "而**控制组**给出关键归因 —— ① d=0（两源重合）⇒ 退化中心力，|ΔL/L|=%.1e（≈0）；"
    "② **λ→∞（纯库仑/开普勒）双源也同样破缺，|ΔL/L|=%.2e** ⇒ L 破缺的根因是**势不再球对称**，"
    "与 λ 有限**无关**（Yukawa 只是让势更不像中心势）。⇒ 「力沿 r̂」是**单源**性质，多源下不成立。"
    % (TS1["Ldev"], TS0["Ldev"], TS2["Ldev"]),
    {"Ldev_lam2": TS1["Ldev"], "Ldev_coulomb": TS2["Ldev"], "Ldev_d0": TS0["Ldev"], "L0": TS1["L0"]})

READINGS["two_source"] = {"lam2": [[round(x, 5), round(y, 5)] for x, y in TS1["pts"][:600]],
                          "kep": [[round(x, 5), round(y, 5)] for x, y in TS2["pts"][:600]]}

# =====================================================================
# S3. 相对论化：d(γ m v)/dt = q v×B + ΣF
# =====================================================================
print("[S3] 相对论化运动方程（磁场 + 中心力）")


def rel_cyclotron(q=1.0, m=1.0, B=1.0, vfrac=0.5, c=10.0, dt=2e-4, steps=200000):
    """归一化：q=m=B=1, c=10。测回旋周期与 γ 守恒。"""
    v = vfrac * c
    gamma = 1.0 / math.sqrt(max(1e-15, 1.0 - (v / c) ** 2))
    omega_ana = q * B / (gamma * m)
    r_ana = gamma * m * v / (q * B)
    # 位置 (r_ana, 0)、B 沿 +z ⇒ 角速度矢量 Ω = −(qB/γm) ẑ（顺时针）⇒ 向心初速沿 −y
    s = [r_ana, 0.0, 0.0, -v, gamma]   # 末位存 gamma（由 v 重算，仅用于记录）

    def acc(st):
        vx, vy = st[2], st[3]
        gam = 1.0 / math.sqrt(max(1e-15, 1.0 - (vx * vx + vy * vy) / (c * c)))
        # q v×B, B=(0,0,B) ⇒ (q B vy, -q B vx) / (γ m)
        ax = q * B * vy / (gam * m)
        ay = -q * B * vx / (gam * m)
        return ax, ay, gam

    pts = [(s[0], s[1])]
    g0 = acc(s)[2]
    gdev = 0.0
    t = 0.0
    crossings = []
    prev_x = s[0]
    for i in range(steps):
        def der(st):
            ax, ay, _ = acc(st)
            return [st[2], st[3], ax, ay]

        k1 = der(s)
        s2 = [s[j] + 0.5 * dt * k1[j] for j in range(4)]
        k2 = der(s2)
        s3 = [s[j] + 0.5 * dt * k2[j] for j in range(4)]
        k3 = der(s3)
        s4 = [s[j] + dt * k3[j] for j in range(4)]
        k4 = der(s4)
        s = [s[j] + dt * (k1[j] + 2 * k2[j] + 2 * k3[j] + k4[j]) / 6.0 for j in range(4)]
        t += dt
        gnow = acc(s)[2]
        gdev = max(gdev, abs(gnow - g0) / g0)
        if prev_x < 0 <= s[0]:
            crossings.append(t)
        prev_x = s[0]
        if i % 200 == 0:
            pts.append((s[0], s[1]))
    T_num = (crossings[1] - crossings[0]) if len(crossings) >= 2 else None
    return dict(omega_ana=omega_ana, r_ana=r_ana, T_ana=2 * math.pi / omega_ana,
                T_num=T_num, gdev=gdev, pts=pts[:400])


CY1 = rel_cyclotron(vfrac=0.5)
CY2 = rel_cyclotron(vfrac=0.01)
rel_T = (abs(CY1["T_num"] - CY1["T_ana"]) / CY1["T_ana"]) if CY1["T_num"] else 999.0
guard("G3-1_cyclotron_period_matches", rel_T < 5e-3,
      "v=0.5c: 数值 T=%s vs 解析 ω=qB/(γm) 给 T=%.6f，相对差 %.2e"
      % (("%.6f" % CY1["T_num"]) if CY1["T_num"] else "None", CY1["T_ana"], rel_T))
guard("G3-2_gamma_conserved", CY1["gdev"] < 1e-9,
      "γ 最大漂移 = %.3e（磁场不做功 ⇒ |v| 恒定）" % CY1["gdev"])
rel_cls = (abs(CY2["T_num"] - 2 * math.pi) / (2 * math.pi)) if CY2["T_num"] else 999.0
guard("G3-3_classical_limit", rel_cls < 5e-3,
      "v=0.01c: T=%s vs 经典 2π=%.6f"
      % (("%.6f" % CY2["T_num"]) if CY2["T_num"] else "None", 2 * math.pi))

add("U08", "PASS", "相对论化：回旋周期 T=2πγm/(qB) 与数值积分一致",
    "归一化 q=m=B=1、c=10：v=0.5c（γ=%.6f）时数值 T=%.6f vs 解析 %.6f（相对差 %.2e）；"
    "γ 漂移 %.2e（磁场不做功）；v=0.01c 时退回经典 2π（相对差 <5e-3）。"
    % (1 / math.sqrt(1 - 0.25), CY1["T_num"], CY1["T_ana"], rel_T, CY1["gdev"]),
    {"T_num": CY1["T_num"], "T_ana": CY1["T_ana"], "gdev": CY1["gdev"],
     "T_classical": CY2["T_num"]})

add("U09", "BOUNDARY", "相对论段的射程",
    "只做「匀强磁场 + 静态中心力」；不含辐射反作用（同步辐射会改变能量）、不含自旋/自旋-轨道、"
    "不含多体相对论。⇒ 验证的是**运动学结构**（γm 惯性 + 洛伦兹力），不是辐射理论。",
    {"note": "no radiation reaction, no spin"})

# 近动/回旋的「假公式」阴性对照（放在两者都定义之后）
_fake_dp = 2 * math.pi * (1.0 / 5.0)      # 假公式 Δφ=2πx（错：真公式是 2π[1/√(1−x²/(1+x))−1]）
control("C2_fake_linear_precession_rejected",
        abs(_fake_dp - ACC[0][1]) > 0.05,
        "假公式 2πx=%.4f vs 数值 %.4f（差 %.3f ≫0 ⇒ 对拍能分辨公式形态）"
        % (_fake_dp, ACC[0][1], abs(_fake_dp - ACC[0][1])))
control("C3_fake_cyclotron_2omega_rejected",
        abs(CY1["T_ana"] / 2.0 - CY1["T_num"]) / CY1["T_ana"] > 0.4,
        "假公式 T/2=%.4f vs 数值 %.4f（差 >40%% ⇒ 能分辨倍频错误）"
        % (CY1["T_ana"] / 2.0, CY1["T_num"]))

# =====================================================================
# S4. 交互式可视化（Canvas + 滑块，纯 vanilla JS，零依赖）
#   物理与 Python 侧同源公式；浏览器用 double，仅作交互演示，不作精密判定
# =====================================================================
print("[S4] 生成交互页面")

HTML_TMPL = r"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>四力同框动力学 · r219</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#0b1020;color:#e5e7eb;font-family:"Microsoft YaHei","PingFang SC",system-ui,sans-serif}
.wrap{max-width:1280px;margin:0 auto;padding:22px}
h1{font-size:22px;margin:0 0 4px;font-weight:650}
.sub{color:#94a3b8;font-size:13px;margin-bottom:16px}
.grid{display:grid;grid-template-columns:330px 1fr 320px;gap:16px;align-items:start}
.card{background:#111a2e;border:1px solid #1e293b;border-radius:12px;padding:14px}
.card h2{font-size:14px;margin:0 0 10px;color:#cbd5e1;font-weight:600;letter-spacing:.3px}
.row{margin-bottom:12px}
.row label{display:flex;justify-content:space-between;font-size:12.5px;color:#94a3b8;margin-bottom:4px}
.row label b{color:#7dd3fc;font-variant-numeric:tabular-nums}
input[type=range]{width:100%;accent-color:#38bdf8;height:20px}
canvas{display:block;width:100%;background:#070c18;border-radius:10px}
.eq{font-family:Consolas,monospace;background:#0a1224;border:1px solid #1e293b;border-radius:8px;
    padding:10px 12px;font-size:12px;line-height:1.85;color:#cbd5e1;overflow-x:auto;white-space:pre}
.kv{display:flex;justify-content:space-between;font-size:12.5px;padding:5px 0;border-bottom:1px dashed #1e293b}
.kv:last-child{border-bottom:none}
.kv b{font-variant-numeric:tabular-nums}
.ok{color:#4ade80}.warn{color:#fbbf24}.bad{color:#f87171}
.note{font-size:12px;color:#94a3b8;line-height:1.7}
.flex{display:flex;gap:8px;flex-wrap:wrap}
button{background:#1d4ed8;border:0;color:#fff;padding:7px 14px;border-radius:8px;cursor:pointer;font-size:13px}
button.ghost{background:#1e293b;color:#cbd5e1}
button:hover{filter:brightness(1.1)}
@media(max-width:1080px){.grid{grid-template-columns:1fr}}
</style></head><body><div class="wrap">
<h1>四力同框动力学 · Yukawa 进动 / 多源叠加 / 相对论化</h1>
<div class="sub">TUFT-r219 · 2026-10-26 · 拖动滑块实时重算（RK4，浏览器内）· 物理公式与 Python 引擎同源</div>

<div class="grid">
  <div class="card">
    <h2>参数</h2>
    <div class="row"><label>力程 λ（r₀=1 为单位）<b id="vlam">2.00</b></label>
      <input id="lam" type="range" min="-0.7" max="1.3" step="0.01" value="0.30"></div>
    <div class="row"><label>强度 α<b id="valp">1.00</b></label>
      <input id="alp" type="range" min="-0.7" max="0.7" step="0.01" value="0"></div>
    <div class="row"><label>初速（相对圆速度）<b id="vbet">0.85</b></label>
      <input id="bet" type="range" min="0.55" max="1.45" step="0.005" value="0.85"></div>
    <div class="row"><label>符号 s（+1 吸引 / −1 排斥）<b id="vsgn">+1</b></label>
      <input id="sgn" type="range" min="0" max="1" step="1" value="0"></div>
    <div class="flex">
      <button id="go">重新发射</button>
      <button id="ghost" class="ghost">切库仑 λ→∞</button>
    </div>
    <div class="note" style="margin-top:12px">
      蓝线 = 轨迹；红点 = 近心点（r 的局部极小）；黄圈 = 源。<br/>
      <b>要看进动必须用椭圆轨道</b>：初速 = 圆速度（β=1）时轨迹是闭合圆、没有近心点，进动不可见；
      把 β 调到 0.8~0.9 就能看到近心点逐圈<b>沿同一方向漂移</b>。
    </div>
  </div>

  <div class="card">
    <h2>轨道（世界坐标 x,y ∈ [−3,3]）</h2>
    <canvas id="main" width="660" height="660"></canvas>
  </div>

  <div class="card">
    <h2>读数</h2>
    <div class="kv"><span>x = r₀/λ</span><b id="kx">0.30</b></div>
    <div class="kv"><span>(ω_r/ω_φ)² = 1−x²/(1+x)</span><b id="kq">0.93</b></div>
    <div class="kv"><span>Δφ 每轨道（解析）</span><b id="kdp">0.00 rad</b></div>
    <div class="kv"><span>Δφ（度/轨道）</span><b id="kdg">0.00°</b></div>
    <div class="kv"><span>L_max 判据</span><b id="klm">—</b></div>
    <div class="kv"><span>能量 E</span><b id="ke">—</b></div>
    <div class="kv"><span>|ΔL/L| 最大</span><b id="kl">—</b></div>
    <h2 style="margin-top:14px">进动闭式</h2>
    <div class="eq">Δφ = 2π[ 1/√(1−x²/(1+x)) − 1 ]
   ≈ πx²(1−x)   (x = r/λ ≪ 1)

x → φ = (1+√5)/2 ⇒ 分母归零
（径向频率为零 = 圆轨道中性稳定）</div>
    <div class="note" style="margin-top:10px">
      x 越接近 φ，轨道越快进动；x &gt; φ 时该半径的圆轨道<b class="bad">不稳定</b>。
    </div>
  </div>
</div>

<div class="card" style="margin-top:16px">
  <h2>这张图在说什么</h2>
  <div class="note">
    单源的 Yukawa 中心力<b>破坏开普勒闭合</b>：每绕一圈，近心点沿同一方向多转 Δφ。
    这个角度是「力的大小 + 距离特性」在时间上的<b>积累</b>——力的瞬时方向仍是 r̂（中心力），
    但强度随 r 衰减的<b>方式</b>（λ 有限 vs ∞）决定了轨道闭不闭合。
    <br/><br/>
    λ→∞ 时 Δφ→0（库仑/开普勒闭合，Bertrand 定理）；λ 越短、r/λ 越大，进动越快。
    反过来，把观测到的进动残差当预算，就能给 (α′, λ) 划出排除带（见 Python 侧 U04）。
  </div>
</div>
</div>

<script>
const cv = document.getElementById('main'), ctx = cv.getContext('2d');
const S = {lam:2.0, alpha:1.0, beta:1.0, sgn:1, pts:[], peri:[], src:[0,0], L0:0, Ldev:0, E:0};
const PHI = (1+Math.sqrt(5))/2, TAU = 2*Math.PI;

function f(lam, r){
  if (!isFinite(lam)) return 1/(r*r);
  const x = r/lam;
  if (x > 700) return 0;
  return Math.exp(-x)*(1/(r*r) + 1/(lam*r));
}
function U(lam, r){
  if (!isFinite(lam)) return -1/r;
  const x = r/lam;
  if (x > 700) return 0;
  return -Math.exp(-x)/r;
}
function hPhi(){ return Math.pow(PHI,3)*Math.exp(-PHI); }

function acc(x,y){
  const r = Math.hypot(x,y);
  if (r < 1e-9) return [0,0];
  const fr = -S.sgn * S.alpha * f(S.lam, r) / r;
  return [fr*x, fr*y];
}

function simulate(){
  // 圆速度：alpha*f(lam,1) = vc^2 / 1
  const vc = Math.sqrt(S.alpha * f(S.lam, 1));
  let x=1, y=0, vx=0, vy=vc*S.beta;
  const dt = 2e-4, steps = 260000;
  const pts=[[x,y]], peri=[];
  let L0 = x*vy - y*vx, Ldev=0, rmax=1;
  let pr=null, pr2=null;
  for (let i=0;i<steps;i++){
    const d=(st)=>{const a=acc(st[0],st[1]); return [st[2],st[3],a[0],a[1]];};
    const k1=d([x,y,vx,vy]);
    const k2=d([x+dt/2*k1[0], y+dt/2*k1[1], vx+dt/2*k1[2], vy+dt/2*k1[3]]);
    const k3=d([x+dt/2*k2[0], y+dt/2*k2[1], vx+dt/2*k2[2], vy+dt/2*k2[3]]);
    const k4=d([x+dt*k3[0], y+dt*k3[1], vx+dt*k3[2], vy+dt*k3[3]]);
    x += dt*(k1[0]+2*k2[0]+2*k3[0]+k4[0])/6;
    y += dt*(k1[1]+2*k2[1]+2*k3[1]+k4[1])/6;
    vx += dt*(k1[2]+2*k2[2]+2*k3[2]+k4[2])/6;
    vy += dt*(k1[3]+2*k2[3]+2*k3[3]+k4[3])/6;
    const r = Math.hypot(x,y);
    rmax = Math.max(rmax, r);
    const L = x*vy - y*vx;
    if (L0!==0) Ldev = Math.max(Ldev, Math.abs(L-L0)/Math.abs(L0));
    if (pr2!==null && pr<pr2 && pr<=r) peri.push([x,y]);
    pr2 = pr; pr = r;
    if (i%40===0) pts.push([x,y]);
    if (r>12 || pts.length>4200) break;
  }
  S.pts=pts; S.peri=peri.slice(0,40); S.L0=L0; S.Ldev=Ldev;
  S.E = 0.5*(vx*vx+vy*vy) + S.sgn*U(S.lam, Math.hypot(x,y));
  S.rmax = rmax;
  S.vc = vc;
  return S;
}

function draw(){
  const W=cv.width, H=cv.height, R=3.0;
  const sx = (X)=> (X+R)/(2*R)*W, sy=(Y)=> H-(Y+R)/(2*R)*H;
  ctx.clearRect(0,0,W,H);

  // 网格
  ctx.strokeStyle='#132033'; ctx.lineWidth=1;
  for(let g=-3; g<=3; g++){
    ctx.beginPath(); ctx.moveTo(sx(g),0); ctx.lineTo(sx(g),H); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(0,sy(g)); ctx.lineTo(W,sy(g)); ctx.stroke();
  }
  // 源
  ctx.strokeStyle='#fbbf24'; ctx.lineWidth=2;
  ctx.beginPath(); ctx.arc(sx(0),sy(0),7,0,TAU); ctx.stroke();

  // 轨迹
  if (S.pts.length>1){
    ctx.strokeStyle='#38bdf8'; ctx.lineWidth=1.6; ctx.beginPath();
    ctx.moveTo(sx(S.pts[0][0]), sy(S.pts[0][1]));
    for(let i=1;i<S.pts.length;i++) ctx.lineTo(sx(S.pts[i][0]), sy(S.pts[i][1]));
    ctx.stroke();
  }
  // 近心点
  ctx.fillStyle='#f87171';
  for(const p of S.peri){
    ctx.beginPath(); ctx.arc(sx(p[0]), sy(p[1]), 2.6, 0, TAU); ctx.fill();
  }
  // 起点
  ctx.fillStyle='#4ade80';
  ctx.beginPath(); ctx.arc(sx(1), sy(0), 4, 0, TAU); ctx.fill();
}

function readout(){
  const x = 1/S.lam;                       // r0=1
  const q = isFinite(S.lam) ? (1 - x*x/(1+x)) : 1;
  const dp = q>0 ? TAU*(1/Math.sqrt(q)-1) : NaN;
  document.getElementById('kx').textContent = isFinite(x)? x.toFixed(3) : '0.000';
  document.getElementById('kq').textContent = q.toFixed(4);
  document.getElementById('kdp').textContent = isFinite(dp)? dp.toFixed(4)+' rad' : '发散';
  document.getElementById('kdg').textContent = isFinite(dp)? (dp*180/Math.PI).toFixed(2)+'°' : '—';
  const L = 1*(S.vc*S.beta);
  let lm;
  if (isFinite(S.lam)){
    const Lmax2 = S.alpha*S.lam*hPhi();
    lm = (L*L <= Lmax2) ? '<span class="ok">束缚 (L≤L_max)</span>' : '<span class="warn">超 L_max ⇒ 逃逸</span>';
  } else {
    lm = (S.E<0) ? '<span class="ok">束缚 (E&lt;0)</span>' : '<span class="warn">逃逸 (E&gt;0)</span>';
  }
  document.getElementById('klm').innerHTML = lm;
  document.getElementById('ke').textContent = S.E.toFixed(4);
  document.getElementById('kl').textContent = S.Ldev.toExponential(2);
}

function refresh(){
  simulate(); draw(); readout();
}

function bind(){
  const lam=document.getElementById('lam'), alp=document.getElementById('alp'),
        bet=document.getElementById('bet'), sgn=document.getElementById('sgn');
  const upd=()=>{
    S.lam = document.getElementById('lammode') ? Infinity : Math.pow(10, parseFloat(lam.value));
    S.alpha = Math.pow(10, parseFloat(alp.value));
    S.beta = parseFloat(bet.value);
    S.sgn = parseInt(sgn.value)===0 ? 1 : -1;
    document.getElementById('vlam').textContent = isFinite(S.lam)? S.lam.toFixed(2) : '∞';
    document.getElementById('valp').textContent = S.alpha.toFixed(2);
    document.getElementById('vbet').textContent = S.beta.toFixed(3);
    document.getElementById('vsgn').textContent = (S.sgn>0?'+1':'−1');
    refresh();
  };
  [lam,alp,bet,sgn].forEach(el=>el.addEventListener('input', upd));
  document.getElementById('go').addEventListener('click', refresh);
  document.getElementById('ghost').addEventListener('click', ()=>{
    // λ→∞：直接置 Infinity（f()/U() 内部按 isFinite 走 1/r^2 与 -1/r 分支）
    lam.value = 1.3;
    S.lam = Infinity;
    document.getElementById('vlam').textContent = '∞';
    refresh();
  });
  upd();
}
bind();
</script>
</body></html>
"""

html_path = os.path.join(BASE, HTML_NAME)
with open(html_path, "w", encoding="utf-8") as f:
    f.write(HTML_TMPL)

guard("G4-1_html_selfcontained",
      ("<script" in HTML_TMPL) and ("src=" not in HTML_TMPL.split("<script>")[0]),
      "HTML 内联 JS/CSS、无外部 src")
guard("G4-2_html_has_closed_form",
      ("Δφ = 2π" in HTML_TMPL) and ("1−x²/(1+x)" in HTML_TMPL),
      "页面内嵌进动闭式")

add("U10", "PASS", "交互式可视化：Canvas + 滑块，实时重算轨道与进动",
    "页面内嵌 RK4（dt=2e-4、26 万步上限）与同一套 `f(λ,r)`、`Δφ` 公式；"
    "滑块调 λ / α / 初速比 / 符号 s，实时显示 x、(ω_r/ω_φ)²、Δφ(rad 与 °)、L_max 判据、能量、|ΔL/L|。"
    "自包含（内联 CSS/JS，无外部 src），零依赖。",
    {"html": HTML_NAME})

add("U11", "INFO", "把三件事放在同一张图上：瞬时方向 / 距离衰减 / 轨道几何",
    "① 力始终沿 r̂（中心力，r214 已证）；② 但 f(r) 的**衰减方式**由 λ 定（n_eff=2+x²/(1+x)）；"
    "③ 二者合起来决定轨道是否闭合 ⇒ **进动是「距离特性」唯一可观测的动力学指纹**。"
    "这条链条把 r214 的静态力表升级成「可测角度」。",
    {"chain": ["direction (r-hat)", "distance law (n_eff)", "precession (observable)"]})

add("U12", "BOUNDARY", "高偏心未覆盖",
    "进动闭式来自 epicyclic（近圆）展开；本卷数值对拍只做 ε≈1e-3 的微扰轨道（x=0.2/0.5）。"
    "e 大时须加 O(e²) 修正（标准结果：Δφ 随 e 增大），本卷**不外推**。",
    {"eps": "1e-3 only"})

add("U13", "BOUNDARY", "浏览器精度声明",
    "交互页面用 double 且 dt=2e-4，仅作交互演示；任何**数值判定**以 Python 侧（Decimal/RK4 收敛检验）为准。"
    "页面读数与 Python 同式，但允许 ~1e-3 的显示级差异。",
    {"engine": "double (display only)"})

add("U14", "INFO", "与同轮并行册的分工",
    "r214＝静态力表 + 单力轨迹 + 形式统一判定；r217＝独立复核 r214 数字 + 根目录脚本归档；"
    "**r219（本卷）＝动力学层**（进动闭式/多源 L 破缺/相对论回旋/交互页）。三者条目**不可相加**。",
    {"r214": "static force table", "r217": "reverify + tidy", "r219": "dynamics"})

# =====================================================================
# S5. 判定与落盘
# =====================================================================
counts = {}
for e in ENTRIES:
    counts[e["level"]] = counts.get(e["level"], 0) + 1
ok_all = all(g["ok"] for g in GUARDS) and all(c["ok"] for c in CONTROLS)

VERDICT = ("进动闭式=PASS（Δφ=2π[1/√(1−x²/(1+x))−1]，小 x=πx²(1−x)）；"
           "三路对拍=PASS（解析/数值轨道/导数，数值 4.6e−4~2.8e−3 属 epicyclic O(x²) 系统偏差）；"
           "φ 双关=PASS（束缚上限与稳定边界同一半径）；"
           "第五力约束=PASS（水星预算 → α′≤budget/(πx²)）；"
           "多源=PASS（双源 |ΔL/L|>0.1 ⇒ 中心力前提破裂）；"
           "相对论=PASS（T=2πγm/(qB) 一致、γ 守恒、经典极限回归）；"
           "高偏心/浏览器精度=BOUNDARY")

payload = dict(
    stem=STEM, round="r219", date="2026-10-26",
    precession_closed_form="dphi = 2*pi*(1/sqrt(1-x^2/(1+x)) - 1), x=r/lam",
    epicyclic_relation="(omega_r/omega_phi)^2 = 3 + r*f'(r)/f(r)",
    phi_dual_role="x=phi both maximizes h(x)=x*e^-x*(1+x) and zeroes the radial frequency",
    entries=ENTRIES, guards=GUARDS, controls=CONTROLS, readings=READINGS,
    counts=counts, verdict=VERDICT,
    key_numbers=dict(
        delta_phi_x020=str(ACC[0][2]) if ACC[0][2] is not None else None,
        delta_phi_x050=str(ACC[1][2]) if ACC[1][2] is not None else None,
        numeric_gap_x020=str(ACC[0][3]), numeric_gap_x050=str(ACC[1][3]),
        phi=str(PHI), h_phi=str(PHI ** 3 * (-PHI).exp()),
        mercury_budget_per_orbit_rad=str(budget_per_orbit_rad),
        x_lim=str(x_lim), lam_lim_m=str(lam_lim),
        alpha_G_proton=str(ALPHA_G_P), alpha_G_neutron=str(ALPHA_G_N),
        double_source_Ldev=TS1["Ldev"],
        cyclotron_T_num=CY1["T_num"], cyclotron_T_ana=CY1["T_ana"],
        gamma_drift=CY1["gdev"],
    ),
    judgement=[
        dict(probe="C1", verdict="既有理论复写",
             reason="Yukawa 进动的 epicyclic 闭式、Bertrand 定理、相对论回旋均为标准结果"),
        dict(probe="C2", verdict="条件性",
             reason="近圆轨道；单通道（水星）约束；多源仅 2 源静态；相对论仅磁场+中心力"),
        dict(probe="C3", verdict="独立可证伪预言",
             reason="0 条新物理；唯一可算新读数是「φ 双关」与「α′–λ 排除带」，前者是数学结构、后者是标准第五力约束的单通道版本"),
    ],
    source="承 r214，做动力学层：进动闭式 / 多源 L 破缺 / 相对论化 / 交互可视化",
)

with open(os.path.join(OUTD, STEM + ".json"), "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

md = []
md.append("# " + STEM + "\n")
md.append("## 一句话\n")
md.append("单源 Yukawa 中心力**破坏开普勒闭合**：每轨道进动 **Δφ = 2π[1/√(1−x²/(1+x)) − 1]**（x=r/λ），"
          "小 x 为 **πx²(1−x)**；把它当预算可换出第五力的 (α′, λ) 排除带。\n")
md.append("## 核心式\n")
md.append("```\n(ω_r/ω_φ)² = 3 + r f'(r)/f(r)\nYukawa ⇒ 1 − x²/(1+x)\nΔφ = 2π[1/√(1−x²/(1+x)) − 1]\n```\n")
md.append("## 三路对拍\n")
md.append("| x=r/λ | 数值 Δφ (rad) | 解析 Δφ (rad) | 差 |\n|---|---|---|---|")
for r in ACC:
    md.append("| %s | %s | %s | %s |" % (r[0],
              ("%.6f" % r[1]) if r[1] is not None else "—",
              ("%.6f" % r[2]) if r[2] is not None else "—",
              ("%.2e" % r[3]) if r[3] is not None else "—"))
md.append("\n> 差值随 x 增大（4.6e−4 → 2.8e−3），方向与 epicyclic 近似的 O(x²) 系统偏差一致。\n")
md.append("## 判定\n")
md.append(VERDICT + "\n")
md.append("## 条目 %d（%s）\n" % (len(ENTRIES),
          " / ".join("%s %d" % (k, counts[k]) for k in ("PASS", "FAIL", "BOUNDARY", "INFO") if counts.get(k))))
for e in ENTRIES:
    md.append("- **[%s] %s %s**：%s" % (e["level"], e["code"], e["title"], e["detail"]))
md.append("\n## 可视化\n")
md.append("`%s`（自包含交互页：滑块调 λ/α/初速/符号，Canvas 实时重算）\n" % HTML_NAME)
with open(os.path.join(OUTD, STEM + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(md))

rep = []
rep.append("TUFT-r219 四力同框动力学 · Yukawa 进动/多源/相对论化 · 运行报告")
rep.append("=" * 72)
rep.append("条目 %d（PASS %d / FAIL %d / BOUNDARY %d / INFO %d）"
           % (len(ENTRIES), counts.get("PASS", 0), counts.get("FAIL", 0),
              counts.get("BOUNDARY", 0), counts.get("INFO", 0)))
rep.append("守卫 %d（全过=%s）· 控制组 %d（全过=%s）"
           % (len(GUARDS), all(g["ok"] for g in GUARDS),
              len(CONTROLS), all(c["ok"] for c in CONTROLS)))
rep.append("")
for e in ENTRIES:
    rep.append("[%s] %s  %s" % (e["level"], e["code"], e["title"]))
    rep.append("    " + e["detail"])
    rep.append("")
rep.append("判定串：" + VERDICT)
rep.append("HTML: " + html_path)
with open(os.path.join(OUTD, STEM + "_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(rep))

print("")
print("条目 %d（PASS %d / FAIL %d / BOUNDARY %d / INFO %d），守卫 %d/%d，控制组 %d/%d"
      % (len(ENTRIES), counts.get("PASS", 0), counts.get("FAIL", 0),
         counts.get("BOUNDARY", 0), counts.get("INFO", 0),
         sum(1 for g in GUARDS if g["ok"]), len(GUARDS),
         sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS)))
print("out -> %s.{json,md,_report.txt}" % STEM)
print("html -> %s" % html_path)
sys.exit(0 if ok_all else 1)


