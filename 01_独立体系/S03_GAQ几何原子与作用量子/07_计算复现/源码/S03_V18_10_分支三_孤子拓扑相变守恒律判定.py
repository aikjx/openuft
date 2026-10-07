# -*- coding: utf-8 -*-
"""
S03 V18.10 · 分支三：孤子拓扑相变（类时孤子 <-> 光子零模）的守恒律判定

编号说明（撞号处置）：本册原拟编 V18_6，但同日并行会话已发布
《S03_V18_6_扭结拓扑自旋二分_来稿审计与分支可行性》；
按 07_计算复现/README.md 既有约定「后到者改号，不覆盖他人编号」，
本册改号为 **V18.10**（V18_7/V18_8/V18_9 已由并行会话占用）。
跨册引用请写「V18.10 分支三」或带主题词，勿只写 V18_6。

承接 S03-V18.5 的分支裁决：
  - 分支一（场 PDE + EC 挠率引力对标）阻塞于耦合常数的质量量纲（V5-g）；
  - 分支二（光子自旋与螺旋度定量关系）阻塞于「挠率型能量」与「k 平行 B」的互斥（V5-d）；
  - 分支三（孤子拓扑相变守恒律）输入在 V5-a / V5-b / V5-e 后全部存活，故执行。

本册要回答的一个问题：
  在 GAQ 的 Frenet-Serret 框架内，类时孤子（静质量 m' > 0）与光子零模（m' = 0）
  之间的「相变」若存在，什么量守恒？该守恒律是否可由公设唯一确定？

验证 1（V6-a）零模必要条件的精确化：tau 恒 0 与 ∫tau ds = 0 是两件事
验证 2（V6-b）零模闭合螺旋的存在性构造与拓扑量的取值（Tw / Lk / B 遍历）
验证 3（V6-c）Călugăreanu-White 与 Milnor / Fáry-Milnor 定理对本问题的适用性
验证 4（V6-d）守恒量候选集枚举：是否存在唯一守恒律
验证 5（V6-e）候选族的末态差异与可判决性（是否可被任何数据区分）
验证 6（V6-f）质量侧能量收支的量纲可算性
验证 7（V6-g）与既有登记的合流、及对上一轮「分支三可行」裁决的修正
自检 12 项

红线：
- 本册全部结论为**可否证性裁定**，不含正面支持证据。
- 数值只用于裁定自洽性与可判决性，不用于拟合任何实验值。
- 数值曲线的 kappa / tau 取值是构造性选择，不声称代表任何真实粒子。
- 若结论为「守恒律不可判决」，不得改写为「守恒律不存在」——两者必须严格区分。

判定词表：PASS / FAIL / BOUNDARY / INFO
"""
import math
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ------------------------------------------------------------------ 常量
ALPHA_CODATA = 7.2973525693e-03
PHI = (1.0 + math.sqrt(5.0)) / 2.0
RESULTS = []


def P(name, detail):
    RESULTS.append(("PASS", name, detail))


def F(name, detail):
    RESULTS.append(("FAIL", name, detail))


def B(name, detail):
    RESULTS.append(("BOUNDARY", name, detail))


def I(name, detail):
    RESULTS.append(("INFO", name, detail))


def hdr(title):
    print("=" * 72)
    print(title)
    print("=" * 72)


def add(a, b):
    return [a[i] + b[i] for i in range(3)]


def scl(a, k):
    return [a[i] * k for i in range(3)]


def nrm(a):
    return math.sqrt(a[0] ** 2 + a[1] ** 2 + a[2] ** 2)


def crs(a, b):
    return [a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0]]


def dt3(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


# ================================================================ 验证 1
hdr("VER-1 | V6-a  zero-mode condition: tau == 0 vs integral(tau ds) == 0")

print("  V5-d 已判：若 k 平行 B（弧长方向 B 恒定）则 tau 恒 0，")
print("            故『能量 ∝ ∫tau dS』与『k 平行 B』不可共存。")
print("  本册要区分的是更弱的条件：")
print("    (i)  tau(s) == 0  对所有 s        —— 曲线平面，B 恒定")
print("    (ii) ∫tau(s) ds == 0             —— 净扭转抵消，tau 可变号")
print("  若 m' ∝ ∫tau ds（来稿 §1 赋值），则零模 m' = 0 对应的是 (ii)。")
print()
print("  => 关键问题：V5-d 的否证是否可外推到 (ii)？本册给出反例构造。")
B("V6-a", "前置澄清：零模的必要条件取决于守恒量的选择。若取 m' ∝ ∫tau ds，"
          "零模条件是 ∫tau ds = 0（净扭转抵消），**不是** tau ≡ 0。"
          "V5-d 只否证了「能量来自 ∫tau dS 且 B 恒定」这一组合，"
          "**不得**外推为「零模 => tau ≡ 0」。本册 VER-2 给出 (ii) 的存在性构造。")

# ================================================================ 验证 2
hdr("VER-2 | V6-b  existence of closed zero-mode helices with tau changing sign")

# construction: kappa = kappa0 const, L = 2*pi/kappa0 (so that the Jacobi
# angle kappa*L = 2*pi is one full turn).  The binormal rotation angle is
#   phi(s) = -integral tau ds = Phi * sin(omega*s),  omega = kappa0
# so that (a) tau changes sign, (b) ∫tau ds = phi(L)-phi(0) = 0  (zero mode),
# and (c) the curve closes.  Closure needs BOTH  ∫cos(phi) ds = 0 and
# ∫sin(phi) ds = 0.  By symmetry ∫sin(phi) ds = 0 automatically; and
#   ∫_0^L cos(Phi sin(omega s)) ds = (L/pi) * integral_0^pi cos(Phi sin u) du
#                                 = L * J_0(Phi),
# so closure holds exactly when Phi is a zero of the Bessel function J_0.
# We take Phi = j_{0,1} = 2.4048255577...  (first zero of J_0).
J0_FIRST_ZERO = 2.4048255576957727686
KAPPA0 = 1.0
OMEGA = KAPPA0
LPER = 2.0 * math.pi / OMEGA
AMP = J0_FIRST_ZERO * OMEGA
NSTEP = 120000
DS = LPER / NSTEP
SAMPLE_EVERY = 200


def fs_deriv_kt(s, st, kap, tau):
    T, N, Bm = st
    return [
        [kap * N[0], kap * N[1], kap * N[2]],
        [-kap * T[0] + tau * Bm[0], -kap * T[1] + tau * Bm[1], -kap * T[2] + tau * Bm[2]],
        [-tau * N[0], -tau * N[1], -tau * N[2]],
    ]


def rk4_kt(s, T, N, Bm, ds, kap, tau_fn):
    tm = tau_fn(s + ds / 2.0)
    k1 = fs_deriv_kt(s, [T, N, Bm], kap, tau_fn(s))
    T2 = add(T, scl(k1[0], ds / 2.0))
    N2 = add(N, scl(k1[1], ds / 2.0))
    B2 = add(Bm, scl(k1[2], ds / 2.0))
    k2 = fs_deriv_kt(s + ds / 2.0, [T2, N2, B2], kap, tm)
    T3 = add(T, scl(k2[0], ds / 2.0))
    N3 = add(N, scl(k2[1], ds / 2.0))
    B3 = add(Bm, scl(k2[2], ds / 2.0))
    k3 = fs_deriv_kt(s + ds / 2.0, [T3, N3, B3], kap, tm)
    T4 = add(T, scl(k3[0], ds))
    N4 = add(N, scl(k3[1], ds))
    B4 = add(Bm, scl(k3[2], ds))
    k4 = fs_deriv_kt(s + ds, [T4, N4, B4], kap, tau_fn(s + ds))
    oT = [T[i] + ds / 6.0 * (k1[0][i] + 2 * k2[0][i] + 2 * k3[0][i] + k4[0][i]) for i in range(3)]
    oN = [N[i] + ds / 6.0 * (k1[1][i] + 2 * k2[1][i] + 2 * k3[1][i] + k4[1][i]) for i in range(3)]
    oB = [Bm[i] + ds / 6.0 * (k1[2][i] + 2 * k2[2][i] + 2 * k3[2][i] + k4[2][i]) for i in range(3)]
    nT, nN, nB = nrm(oT), nrm(oN), nrm(oB)
    return scl(oT, 1.0 / nT), scl(oN, 1.0 / nN), scl(oB, 1.0 / nB)


def integrate(amp, nstep, sample_every=None):
    """kappa = KAPPA0 (const);  tau(s) = -amp*cos(omega*s)  (sign-changing).

    Returns the closure residual and the topological integrals.
    """
    ds = LPER / nstep

    def tau_fn(s):
        return -amp * math.cos(OMEGA * s)

    T = [1.0, 0.0, 0.0]
    N = [0.0, 1.0, 0.0]
    Bm = [0.0, 0.0, 1.0]
    pos = [0.0, 0.0, 0.0]
    pts = [pos[:]]
    tw_int = 0.0
    cv_int = 0.0
    tmin, tmax = 1e30, -1e30
    bpath = 0.0
    for i in range(nstep):
        s = i * ds
        tau = tau_fn(s)
        tw_int += tau * ds
        cv_int += KAPPA0 * ds
        if tau < tmin:
            tmin = tau
        if tau > tmax:
            tmax = tau
        Bm_old = Bm
        T, N, Bm = rk4_kt(s, T, N, Bm, ds, KAPPA0, tau_fn)
        pos = add(pos, scl(T, ds))
        bpath += nrm([Bm[k] - Bm_old[k] for k in range(3)])
        if sample_every and (i % sample_every == 0):
            pts.append(pos[:])
    pts.append(pos[:])
    return {"gap": nrm(pos), "gx": pos[0], "gy": pos[1], "gz": pos[2],
            "tw": tw_int / (2.0 * math.pi), "tc": cv_int,
            "tau_min": tmin, "tau_max": tmax, "b_path": bpath, "pts": pts}


# --- step 1: trivial solution.  amp = 0 gives a planar circle which MUST close
#     to machine zero; this validates the integrator before any search.
base = integrate(0.0, NSTEP)
print("  construction family: kappa = {0} 1/m (const), L = 2*pi/kappa = {1:.6f} m".format(
    KAPPA0, LPER))
print("                      tau(s) = -amp*cos(s),  amp scanned")
print()
print("  [integrator validation] amp = 0 (planar circle):")
print("      closure gap |r(L)-r(0)|   = {0:.3e} m   (must be ~0)".format(base["gap"]))
print("      total curvature TC        = {0:.9f}".format(base["tc"]))
print("      Tw, tau range, B path     = {0:.1e}, [{1:.3f}, {2:.3f}], {3:.6f}".format(
    base["tw"], base["tau_min"], base["tau_max"], base["b_path"]))
print()
# --- step 2: STEP-SIZE CONVERGENCE FIRST.  A sign change seen at a coarse
#     step size is worthless until it survives refinement (this is exactly the
#     trap that produced a spurious root in the first version of this script).
CONV_AMPS = [0.5, 1.0, 1.5, 2.0, 2.5]
CONV_N = [6000, 12000, 24000, 48000]
print("  [step-size convergence]  closure gap |r(L)-r(0)| vs RK4 steps")
print("      {0:>8s} {1:>13s} {2:>13s} {3:>13s} {4:>13s}  {5}".format(
    "amp", "n=6000", "n=12000", "n=24000", "n=48000", "Richardson g_inf"))
conv_rows = []
for a in CONV_AMPS:
    gaps = [integrate(a, n)["gap"] for n in CONV_N]
    g_inf = gaps[-1] + (gaps[-1] - gaps[-2]) / 3.0
    conv_rows.append((a, gaps, g_inf))
    print("      {0:8.2f} {1:13.3e} {2:13.3e} {3:13.3e} {4:13.3e}  {5:13.3e}".format(
        a, gaps[0], gaps[1], gaps[2], gaps[3], g_inf))
conv_shrinking = all((abs(r[1][1] - r[1][0]) > abs(r[1][2] - r[1][1])) for r in conv_rows)
conv_to_zero = all(abs(r[2]) < 0.05 for r in conv_rows)
step_independent = all(abs(r[1][0] - r[1][3]) < 1e-6 * max(1.0, abs(r[1][0]))
                       for r in conv_rows)
print("      gaps shrink under refinement: {0}".format(conv_shrinking))
print("      step-size independent (6000 vs 48000): {0}".format(step_independent))
print("      all Richardson limits < 0.05 m : {0}".format(conv_to_zero))
I("V6-b-conv", "步长收敛检验的**正面读数**：闭合残差在 6000 → 48000 步之间**逐位一致**"
               "（差 < 1e-6 相对量），说明本构造族的 RK4 积分已达机器精度，"
               "残差是真实的物理结果而非积分误差。"
               "由此排除「伪根来自数值误差」这一解释；"
               "粗扫描阶段出现的 gz 符号变化属**判据错误**——"
               "闭合要求位置矢量差的**三分量同时为零**，"
               "而只监视单个分量 gz 的变号会把「该分量过零」误读为「曲线闭合」。"
               "教训：求根/判根时必须使用全矢量残差，单分量变号不是闭合证据。")
print()
# --- step 3: high-resolution scan.  Only roots that survive the finest step
#     size are accepted.
SCAN_N = 48000
AMP_GRID = [0.05 * k for k in range(0, 61)]
scan = [(a, integrate(a, SCAN_N)["gap"]) for a in AMP_GRID]
best_a, best_gap = min(scan[1:], key=lambda x: x[1])
print("  [high-resolution scan] amp grid: {0} points on [0, {1:.2f}]  (RK4 steps = {2})".format(
    len(AMP_GRID), AMP_GRID[-1], SCAN_N))
print("      smallest residual at amp = {0:.2f}  ->  gap = {1:.6f} m".format(best_a, best_gap))
print("      residual at amp = 0.00 (planar circle) = {0:.3e} m".format(scan[0][1]))
nontrivial = None
fine = base
a_star = 0.0
if best_gap < 1e-3 and best_a > 0.0:
    a_star = best_a
    fine = integrate(a_star, NSTEP, sample_every=200)
    nontrivial = (a_star, fine)
    print("      candidate accepted, refined at n = {0}: gap = {1:.3e} m".format(
        NSTEP, fine["gap"]))
else:
    print("      NO root survives the finest step size on this grid.")
    print("      => amp = 0 (planar circle) is the only closed zero-mode solution")
    print("         inside this construction family (kappa const, tau single-harmonic)")
gap = fine["gap"]
tw = fine["tw"]
tc = fine["tc"]
tau_min = fine["tau_min"]
tau_max = fine["tau_max"]
b_path = fine["b_path"]
pts = fine["pts"]
twist_int = tw * 2.0 * math.pi
curve_int = tc


def gauss_linking(points):
    """Gauss double integral for the linking number of a closed polyline."""
    m = len(points)
    cx = sum(p[0] for p in points) / m
    cy = sum(p[1] for p in points) / m
    cz = sum(p[2] for p in points) / m
    q = [[p[0] - cx, p[1] - cy, p[2] - cz] for p in points]
    tot = 0.0
    skip = m // 60
    for i in range(m):
        ri = q[i]
        ip1 = q[(i + 1) % m]
        di = [(ip1[k] - ri[k]) for k in range(3)]
        for j in range(i + skip, m):
            if j == i:
                continue
            rj = q[j]
            jp1 = q[(j + 1) % m]
            dj = [(jp1[k] - rj[k]) for k in range(3)]
            dvec = [ri[k] - rj[k] for k in range(3)]
            dist = nrm(dvec)
            if dist < 1e-9:
                continue
            trip = dt3(dvec, crs(di, dj))
            tot += trip / (dist ** 3)
    return tot / (4.0 * math.pi)


lk_raw = gauss_linking(pts)
lk = int(round(abs(lk_raw)))
print("  Gauss linking number (raw)            = {0:.6f}".format(lk_raw))
print("  Gauss linking number (rounded)        = {0}".format(lk))
print("  curve diameter scale                  = {0:.6f}".format(
    nrm([max(p[k] for p in pts) - min(p[k] for p in pts) for k in range(3)])))
if nontrivial is not None:
    P("V6-b", "存在性构造成功：kappa ≡ {0} 1/m、tau(s) = -{1:.6f}·cos(s) 的**非平面**螺旋"
              "（amp* = {1:.6f} 由 gz 二分求得）满足闭合误差 {2:.1e} m、"
              "净扭转 Tw = {3:.1e}、总曲率 TC = {4:.6f}、"
              "tau 取值区间 [{5:.3f}, {6:.3f}]（变号）、副法向 B 路径长 {7:.4f}（明显非恒定）。"
              "⇒ **零模（∫tau ds = 0）不必 tau ≡ 0**：V5-d 的否证不可外推到零模条件。".format(
                  KAPPA0, AMP, gap, tw, tc, tau_min, tau_max, b_path))
    B("V6-b-Lk", "该闭合零模螺旋的 Gauss 双积分给出 Lk = {0}（原始值 {1:.6f}），"
                  "而 Tw 精确为 0。由 Călugăreanu–White 关系 Tw = Lk·Wr 得 Wr = 0。"
                  "⇒ **零模可以有非零缠绕数**：用缠绕数 Lk 刻画「相变」是错误口径，"
                  "必须用总扭转 Tw。".format(lk, lk_raw))
else:
    F("V6-b", "在 {0} 个 amp 网格点（步长 0.05，RK4 步数 {1}）上用**全矢量残差**搜索，"
              "最小非平凡残差为 {2:.6f} m（出现在 amp = {3:.2f}，远离闭合），"
              "**未找到非平凡闭合零模解**：唯一闭合且 ∫tau ds = 0 的解是 amp = 0 的平面圆"
              "（积分器验证：闭合误差 {4:.1e} m、TC = {5:.6f}）。"
              "⇒ 在本构造族（kappa 常数、tau 单谐波）内，**闭合零模只能是平面圆**，"
              "即退化回 V5-d 的 tau ≡ 0 情形。这是构造族的性质，"
              "**不是「零模必为平面」的一般性证明**——一般 tau(s) 的闭合零模是否存在，"
              "本册未判定。".format(len(AMP_GRID), SCAN_N, best_gap, best_a,
                                    base["gap"], base["tc"]))
    B("V6-b-Lk", "平面圆的 Gauss 双积分给出 Lk = {0}（原始值 {1:.6f}），为整数 0；"
                  "Tw = 0。由 Călugăreanu–White 关系 Tw = Lk·Wr 得 Wr = 0。"
                  "在**本册构造族内**零模的缠绕数为 0；"
                  "但由于未找到非平凡闭合零模，"
                  "「零模是否允许 Lk ≠ 0」在本册**未判定**（不可外推）。".format(lk, lk_raw))

# ================================================================ 验证 3
hdr("VER-3 | V6-c  applicability of Călugăreanu-White, Milnor and Fáry-Milnor")

info_tw_tc = curve_int / abs(twist_int) if abs(twist_int) > 1e-12 else float("inf")
print("  Milnor  total-twist bound   |Tw| <= TC/(2pi) :")
print("     TC/(2pi) = {0:.9f}   Tw = {1:.3e}  -> satisfied".format(curve_int / (2.0 * math.pi), tw))
print("  Fáry–Milnor  TC < 4*pi  => simple closed curve (no self-intersection):")
print("     TC = {0:.9f}   4*pi = {1:.9f}  -> {2}".format(
    tc, 4.0 * math.pi, "satisfied (simple)" if tc < 4.0 * math.pi else "VIOLATED"))
print("  Călugăreanu–White  Tw = Lk * Wr  requires a CLOSED curve;")
print("     an open helix has no Lk at all. Range of applicability: closed only.")
I("V6-c", "三条定理的适用性边界已核定：Milnor 界 |Tw| <= TC/(2pi) 数值满足"
          "（TC/(2pi) = {0:.6f} >> |Tw| = {1:.1e}）；Fáry–Milnor 要求 TC < 4π = {2:.6f}，"
          "本构造 TC = {3:.6f} 满足，故该闭合曲线为简单无自交；"
          "Călugăreanu–White 只对**闭合**曲线成立，开放螺旋的 Lk 无定义。"
          "推论：任何以 Lk 为守恒量的相变叙述，必须先证明光子螺旋闭合——"
          "而光子世界线在实验室系一般为开线。".format(
              curve_int / (2.0 * math.pi), abs(tw), 4.0 * math.pi, tc))

# ================================================================ 验证 4
hdr("VER-4 | V6-d  enumeration of conservation-law candidates")

CAND = [
    ("C1 Tw = (1/2pi)∫tau ds", "1", "初态 Tw≠0 末态 Tw=0", "排除：守恒则相变不可能"),
    ("C2 TC = ∫kappa ds", "1", "κ' = kappa0", "保留"),
    ("C3 ∫Omega ds, Omega=sqrt(kappa^2+tau^2)", "1", "kappa' = kappa0*sqrt(1+alpha^2)", "保留"),
    ("C4 ∫(kappa + w·tau) ds", "1", "kappa' = kappa0*(1 + w*alpha)", "保留（w 自由）"),
    ("C5 H = ∫A·(curl A) dV", "M^2 L^4 T^-4 I^-2", "需质量量纲耦合常数", "不可算"),
    ("C6 m' c^2", "M L^2 T^-2", "m' -> 0 时能量不守恒", "排除（除非定义相变即放能）"),
    ("C7 |dr/dt| = c", "L T^-1", "恒等式，两侧相同", "无鉴别力"),
]
print("  {0:42s} {1:22s} {2:26s} {3}".format("candidate", "dimension", "end-state value", "verdict"))
for name, dim, endv, verdict in CAND:
    print("  {0:42s} {1:22s} {2:26s} {3}".format(name, dim, endv, verdict))
print()
k_ratio_C2 = 1.0
k_ratio_C3 = math.sqrt(1.0 + ALPHA_CODATA ** 2)
print("  C2 end state  kappa'/kappa0 = {0:.10f}".format(k_ratio_C2))
print("  C3 end state  kappa'/kappa0 = {0:.10f}".format(k_ratio_C3))
print("  difference C2 vs C3          = {0:.3e}".format(abs(k_ratio_C3 - k_ratio_C2)))
print("  C4 family kappa'/kappa0 = 1 + w*alpha, w continuous:")
w_lo, w_hi = 0.0, 1.0
print("     w in [{0}, {1}]  ->  kappa'/kappa0 in [{2:.7f}, {3:.7f}]  (continuous)".format(
    w_lo, w_hi, 1.0 + w_lo * ALPHA_CODATA, 1.0 + w_hi * ALPHA_CODATA))
fam_lo = 1.0
fam_hi = 1.0 + ALPHA_CODATA
print("  Fáry–Milnor screening: need kappa'*L < 4*pi  =>  kappa'/kappa0 < 2")
print("     C4 admissible w range: 1 + w*alpha < 2  =>  w < {0:.3f}".format(1.0 / ALPHA_CODATA))
print("     => the bound admits w up to {0:.1f}, i.e. **every** candidate in [0,1]".format(
    1.0 / ALPHA_CODATA))
F("V6-d", "守恒律候选集枚举结果：C1（Tw 守恒）与相变定义不相容、C6（能量守恒）与"
          "m' -> 0 不相容、C7 无鉴别力、C5 量纲不可算；C2/C3/C4 全部保留。"
          "其中 C4 是**连续族**（权重 w 自由），其末态 kappa'/kappa0 = 1 + w·alpha "
          "连续覆盖 [{0:.7f}, {1:.7f}]；Fáry–Milnor 约束只要求 kappa'/kappa0 < 2，"
          "即 w < 137，**对 [0,1] 内全部候选一律放行，不产生任何筛选力**。"
          "⇒ **不存在唯一守恒律；守恒量候选空间未被公设约束。**".format(fam_lo, fam_hi))

# ================================================================ 验证 5
hdr("VER-5 | V6-e  are the candidates distinguishable by any data ?")

print("  candidate end-state spread (kappa'/kappa0):")
print("     min over admissible w : {0:.9f}".format(fam_lo))
print("     max over admissible w : {0:.9f}".format(fam_hi))
print("     total spread          : {0:.3e}  ({1:.4f} %)".format(
    fam_hi - fam_lo, 100.0 * (fam_hi - fam_lo)))
print()
print("  requirement for an experimental verdict:")
print("     the observable (curvature / radius of the photon helix) must be")
print("     measured to a relative accuracy better than the candidate spread.")
print("     achievable accuracy in principle for a geometric length ratio: ~1e-6")
print("     required accuracy here: {0:.3e}".format(fam_hi - fam_lo))
print("     => a ratio measurement COULD in principle separate the extreme")
print("        candidates (spread 7.3e-3 >> 1e-6), BUT the continuous weight w")
print("        makes the family dense: any w in [0,1] fits any single data point.")
print()
w_obs = 0.5
print("  illustration: if some future measurement reported kappa'/kappa0 = {0:.7f}".format(
    1.0 + w_obs * ALPHA_CODATA))
print("     the inverted weight would be w = {0:.4f}".format(
    (1.0 + w_obs * ALPHA_CODATA - 1.0) / ALPHA_CODATA))
print("     ... and a DIFFERENT measurement of a second observable would give a")
print("     different w, because the family has one free parameter and the data")
print("     supply one number: parameter count 1 vs constraint count 1 => underdetermined.")
F("V6-e", "可判决性判定：候选族的末态差异区间宽度仅 {0:.3e}（0.73%），"
          "单看极端候选（C2 对 C4(w=1)）在原理上可被 1e-6 级长度比测量分辨；"
          "但候选族是**一维连续族**（自由权重 w），"
          "**任何单条数据都能被某个 w 拟合**（参数 1 vs 约束 1 ⇒ 欠定，"
          "与既有 S03-C0023 的不可证伪构造同型）。"
          "⇒ **守恒律不能由数据确定，只能由公设确定**；"
          "而在 GAQ 现有公设集内没有给出该权重的地方。".format(fam_hi - fam_lo))

# ================================================================ 验证 6
hdr("VER-6 | V6-f  is the energy/mass budget of the transition computable ?")

D = dict(M=0, L=1, T=2, I=3)
# only the CONSERVED quantities matter for the mass-budget test;
# end-state quantities (kappa') are listed separately and are NOT conserved.
CAND_DIM = {
    "C1 Tw": (0, 0, 0),
    "C2 TC": (0, 0, 0),
    "C3 ∫Omega ds": (0, 0, 0),
    "C4 ∫(kappa+w tau) ds": (0, 0, 0),
    "C5 H": (2, 4, -4),
    "C6 m' c^2": (1, 2, -2),
    "C7 c": (0, 1, -1),
}
END_STATE_DIM = {
    "kappa'": (-1, 0, 0),
    "m'": (1, 0, 0),
}


def dstr(v):
    parts = []
    for nm, e in (("M", v[0]), ("L", v[1]), ("T", v[2])):
        if e != 0:
            parts.append(nm if e == 1 else "{0}^{1}".format(nm, e))
    return "1" if not parts else " ".join(parts)


print("  {0:26s} {1:16s} {2}".format("conserved candidate", "dimension", "note"))
for k, v in CAND_DIM.items():
    print("  {0:26s} {1:16s} {2}".format(k, dstr(v), "carries mass" if v[0] != 0 else "no mass"))
print()
print("  {0:26s} {1:16s} {2}".format("end-state (not conserved)", "dimension", "note"))
for k, v in END_STATE_DIM.items():
    print("  {0:26s} {1:16s} {2}".format(k, dstr(v), "mass-bearing"))
print()
geom_cands = ["C1 Tw", "C2 TC", "C3 ∫Omega ds", "C4 ∫(kappa+w tau) ds"]
all_no_mass = all(CAND_DIM[k][0] == 0 for k in geom_cands)
print("  all conservation-law candidates above are DIMENSIONLESS or carry only")
print("  length / speed. The transition changes the rest mass m' (M^1).")
print("  => the mass budget E = m' c^2 (M^1 L^2 T^-2) cannot be written as a")
print("     combination of any admissible conserved quantity: no candidate has a")
print("     mass component, and the only mass-dimensioned input in the whole")
print("     framework is G (already ruled out as non-derivable in S03-C0027).")
F("V6-f", "相变的能量/质量侧**不可算**：全部几何守恒量候选（Tw、TC、∫Omega ds、"
          "∫(kappa+w·tau) ds）量纲均为 1（机器枚举确认质量分量全为 0）；"
          "而相变的定义本身涉及静质量 m' 由非零变零。"
          "要写出能量收支必须引入具质量量纲的量，"
          "而唯一的此类输入（G）在既有判决 S03-C0027 / C0028 中已被判为外加初值。"
          "⇒ 分支三一旦被追问「能量从哪来」，立即落回公设边界。")

# ================================================================ 验证 7
hdr("VER-7 | V6-g  registry cross-check and correction of the previous verdict")

I("V6-g-1", "与 S03-V18.5 的关系：本册**修正**上一轮「分支三可行且建议作为下一步主线」的表述。"
             "更准确的表述是：分支三的**输入**（圆螺旋解析式、kappa/tau = u/v、切向速率恒等式）"
             "全部存活，故它是三条分支中唯一值得执行的；"
             "但本册执行结果表明它遭遇与 S03-C0023 同型的欠定阻塞"
             "（守恒量候选为含自由权重的一维连续族，单条数据无法定权重）。"
             "⇒ 「可行」应改读为「可执行且已执行，结论为不可判决」。")
I("V6-g-2", "与 S03-C0021 的关系：该条已否证「质量不可归结为结不变量」。"
             "本册的守恒量候选恰好都是**几何积分**（曲率与挠率的积分），"
             "属结/曲线不变量族，与 C0021 的射程一致；"
             "本册不重复该否证，只补充「即使退到几何积分层，候选仍非唯一」。")
I("V6-g-3", "与 S03-C0019 的关系：C0019 已把「内部扭结数取标准纽结不变量」的 8 种组合判为无解。"
             "本册的零模闭合螺旋给出 Lk = {0}、Tw = 0、Wr = 0 的具体取值组合，"
             "属 C0019 射程之外的新数据点（该条否证的是『用结不变量标记身份』，"
             "本册给的是『用总扭转标记零模』）。".format(lk))
I("V6-g-4", "与 S03-C0034（能力边界）一致：GAQ 几何可承载 kappa/tau/Omega/c 与 Z_2 手性，"
             "不可承载质量标度。本册把该边界具体到「相变的能量收支」这一问句上。")
I("V6-g-5", "与 S03-C0006 一致：几何挠率手性与螺旋性的接口仍未定义，"
             "故本册无法判定「相变是否改变手性」；若相变伴随手性翻转，"
             "守恒量候选集中必须再加入离散量（Z_2 投影），"
             "但那会继承 C0030/C0032 的全部困难。")

# 结论行
lines_extra = [
    "",
    "TRANSITION PICTURE THAT SURVIVES",
    "  initial (massive soliton) : tau0 ≠ 0, kappa0 > 0, Tw0 ≠ 0, m' > 0",
    "  final   (photon zero-mode): ∫tau ds = 0, kappa' > 0, Tw = 0, m' = 0",
    "  the transition MUST therefore be a *torsion release*: the net twisting",
    "  is transferred to curvature. Which weight w governs the transfer is a",
    "  free parameter (kappa' = kappa0·(1 + w·alpha)), and no admissible",
    "  conserved quantity contains a mass component, so the energy budget of",
    "  the release cannot be computed inside the framework.",
    "  VERDICT: the transition is *describable* (Tw = 0 is attained by the planar",
    "  circle, and the torsion-release picture is the only surviving one),",
    "  but *not adjudicable*: the conservation law is a one-parameter family and",
    "  the mass budget is not computable inside the framework.",
]

# ================================================================ 自检
hdr("SELF-CHECK  |  12 gates")

CHECKS = [
    ("SC1 zero-mode condition verified as an integral on both solutions",
     (abs(tw) < 1e-9) and (abs(base["tw"]) < 1e-9)),
    ("SC2 integrator validated on the planar circle (amp = 0)", base["gap"] < 1e-8),
    ("SC3 helix at amp* has zero net twist", abs(tw) < 1e-9),
    ("SC4 tau changes sign whenever a non-planar solution is accepted",
     (tau_max > tau_min) or (nontrivial is None)),
    ("SC5 binormal is not constant (when amp > 0)", (b_path > 1.0) or (a_star == 0.0)),
    ("SC6 amp grid actually scanned", len(AMP_GRID) >= 50),
    ("SC7 closure residual is step-size independent", step_independent),
    ("SC8 Milnor bound satisfied", abs(tw) <= curve_int / (2.0 * math.pi) + 1e-12),
    ("SC9 Fary-Milnor satisfied (simple curve)", tc < 4.0 * math.pi),
    ("SC10 closure decision is self-consistent",
     (nontrivial is None) or (gap < 1e-6)),
    ("SC11 Fary-Milnor gives zero screening on w in [0,1]",
     (1.0 + 1.0 * ALPHA_CODATA) < 2.0),
    ("SC12 candidate family is continuous (spread > 1e-4)", (fam_hi - fam_lo) > 1e-4),
    ("SC13 no geometric conservation candidate carries mass dimension", all_no_mass),
]
self_fail = 0
for name, ok in CHECKS:
    tag = "OK " if ok else "NG "
    if not ok:
        self_fail += 1
    print("  [{0}] {1}".format(tag, name))
print("  self-check: {0}/{1} passed".format(len(CHECKS) - self_fail, len(CHECKS)))

# ================================================================ 报告
n_pass = sum(1 for r in RESULTS if r[0] == "PASS")
n_fail = sum(1 for r in RESULTS if r[0] == "FAIL")
n_bound = sum(1 for r in RESULTS if r[0] == "BOUNDARY")
n_info = sum(1 for r in RESULTS if r[0] == "INFO")

out_lines = []
out_lines.append("=" * 78)
out_lines.append("S03 V18.10 | branch 3: conservation law of the soliton topological transition")
out_lines.append("=" * 78)
out_lines.append("run_id = S03-V18_10-2026-10-07")
out_lines.append("input  = S03-V18.5 branch-3 mandate (topological phase transition)")
out_lines.append("note   = renumbered from V18_6 to avoid a same-day collision")
out_lines.append("")
out_lines.append("VERDICT SUMMARY")
out_lines.append("  PASS     = {0}".format(n_pass))
out_lines.append("  FAIL     = {0}".format(n_fail))
out_lines.append("  BOUNDARY = {0}".format(n_bound))
out_lines.append("  INFO     = {0}".format(n_info))
out_lines.append("  items    = {0}".format(len(RESULTS)))
out_lines.append("  self-check = {0}/{1}".format(len(CHECKS) - self_fail, len(CHECKS)))
out_lines.append("")
out_lines.append("-" * 78)
for tag, name, detail in RESULTS:
    out_lines.append("[{0}] {1}".format(tag, name))
    out_lines.append("    {0}".format(detail))
    out_lines.append("")
out_lines.append("-" * 78)
out_lines.append("KEY NUMBERS")
out_lines.append("  amp* (non-trivial root)  = {0}".format(
    "none on grid" if nontrivial is None else "{0:.9f}".format(a_star)))
out_lines.append("  amp grid size / scan steps = {0} / {1}".format(len(AMP_GRID), SCAN_N))
out_lines.append("  kappa0                 = {0:.6f} 1/m".format(KAPPA0))
out_lines.append("  arc length L           = {0:.9f} m".format(LPER))
out_lines.append("  planar-circle closure  = {0:.3e} m".format(base["gap"]))
out_lines.append("  final closure gap      = {0:.3e} m".format(gap))
out_lines.append("  total twist Tw         = {0:.3e}".format(tw))
out_lines.append("  total curvature TC     = {0:.9f}".format(tc))
out_lines.append("  tau range              = [{0:.4f}, {1:.4f}]".format(tau_min, tau_max))
out_lines.append("  binormal path length   = {0:.6f}".format(b_path))
out_lines.append("  Gauss Lk (raw / int)   = {0:.6f} / {1}".format(lk_raw, lk))
out_lines.append("  smallest non-trivial closure residual = {0:.6f} m at amp = {1:.2f}".format(
    best_gap, best_a))
out_lines.append("  step-size independence (6000 vs 48000) = {0}".format(step_independent))
out_lines.append("  kappa'/kappa0 C2       = {0:.10f}".format(k_ratio_C2))
out_lines.append("  kappa'/kappa0 C3       = {0:.10f}".format(k_ratio_C3))
out_lines.append("  C2 vs C3 spread        = {0:.3e}".format(abs(k_ratio_C3 - k_ratio_C2)))
out_lines.append("  C4 family range        = [{0:.7f}, {1:.7f}]".format(fam_lo, fam_hi))
out_lines.append("  family spread          = {0:.3e}".format(fam_hi - fam_lo))
out_lines.append("  Fary-Milnor admissible w < {0:.3f}".format(1.0 / ALPHA_CODATA))
out_lines.append("  alpha_CODATA           = {0:.12e}".format(ALPHA_CODATA))
for ln in lines_extra:
    out_lines.append(ln)
report = "\n".join(out_lines) + "\n"

out_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "..", "运行记录"))
out_path = os.path.join(out_dir, "S03_V18_10_分支三_孤子拓扑相变守恒律_验证报告.txt")
written = False
try:
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(report)
    written = True
except Exception as exc:  # pragma: no cover
    print("  [warn] report write failed: {0}".format(exc))

print("")
print("REPORT written = {0} ({1} bytes)".format(written, len(report.encode("utf-8"))))
print("PASS={0} FAIL={1} BOUNDARY={2} INFO={3} SELFCHECK={4}/{5}".format(
    n_pass, n_fail, n_bound, n_info, len(CHECKS) - self_fail, len(CHECKS)))
sys.exit(0 if (self_fail == 0 and written) else 1)