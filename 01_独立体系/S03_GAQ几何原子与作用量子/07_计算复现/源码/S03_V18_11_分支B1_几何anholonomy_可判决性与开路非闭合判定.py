# -*- coding: utf-8 -*-
"""
S03-V18_11 · 分支 B-1 执行判定
==============================================================
主题：Frenet / 加框（ribbon）holonomy 作为「味变换」几何描述的可判决性
体系：s03_gaq_geometric_atom（GAQ 几何原子与作用量子）
承接：S03-V9 = S03_V18_9（中微子振荡拓扑重联来稿审计）§9 建议路线 B-1 + 六条门禁 G1–G6
红线：本册不提供任何 GAQ 正面证据。两个 PASS 分别是
      ① 标准事实（PMNS 幺正性 / Jarlskog）的独立复算；
      ② 对既有产物读数的交叉复核。
运行：python -B 源码/S03_V18_11_分支B1_几何anholonomy_可判决性与开路非闭合判定.py
      （纯标准库，Python 3.8，约 3 s）
==============================================================
"""

import sys
import os
import io
import math

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

RPT = []


def say(line=""):
    print(line)
    RPT.append(line)


ITEMS = []
SCS = []


def item(vid, verdict, title, lines):
    ITEMS.append((vid, verdict, title))
    say("[%s] %s %s" % (verdict, vid, title))
    for ln in lines:
        say("      " + ln)
    say("")


def sc(tag, ok, detail):
    SCS.append((tag, bool(ok), detail))
    say("[SC-%s] %s  %s" % (tag, "OK" if ok else "NG", detail))


say("=" * 78)
say("S03-V18_11  分支 B-1：几何 anholonomy 作为味变换描述的可判决性判定")
say("体系 s03_gaq_geometric_atom ｜ 承接 S03-V9 §9（建议路线 B-1）+ 门禁 G1–G6")
say("红线：不提供 GAQ 正面证据；PASS 仅限标准事实复算与对既有读数的交叉复核")
say("=" * 78)
say("")

# ------------------------------------------------------------------
# 0. 常量与几何工具
# ------------------------------------------------------------------
HBARC_EVM = 1.973269804e-7            # ħc = 197.3269804 MeV·fm，换算为 [eV·m]
GEV_EV = 1.0e9
K_CONV = 1.0 / (4.0 * HBARC_EVM * GEV_EV)   # 相位换算：Δm²[eV²]·L[m]/E[GeV] → rad
M_NU_EV = 0.05                        # 质量口径示例（S03-V18_9 §3 同值）


def hv0(t, R, c):
    return (R * math.cos(t), R * math.sin(t), c * t)


def hv1(t, R, c):
    return (-R * math.sin(t), R * math.cos(t), c)


def hv2(t, R, c):
    return (-R * math.cos(t), -R * math.sin(t), 0.0)


def cross3(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def dot3(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def norm3(a):
    return math.sqrt(dot3(a, a))


def frenet_analytic(t, R, c):
    """圆螺旋 r(t)=(R cos t, R sin t, c t) 的 F–S 量与标架（解析）。"""
    v2 = R * R + c * c
    v = math.sqrt(v2)
    kap = R / v2
    tau = c / v2
    Tvec = tuple(x / v for x in hv1(t, R, c))
    Nvec = (-math.cos(t), -math.sin(t), 0.0)
    Bvec = tuple(x / v for x in (c * math.sin(t), -c * math.cos(t), R))
    return kap, tau, Tvec, Nvec, Bvec


def fd2(fun, t, h, R, c):
    a = fun(t - h, R, c)
    b = fun(t, R, c)
    d = fun(t + h, R, c)
    return tuple((a[i] - 2.0 * b[i] + d[i]) / (h * h) for i in range(3))


def fd3(fun, t, h, R, c):
    a = fun(t - 2.0 * h, R, c)
    b = fun(t - h, R, c)
    d = fun(t + h, R, c)
    e = fun(t + 2.0 * h, R, c)
    return tuple((-a[i] + 2.0 * b[i] - 2.0 * d[i] + e[i]) / (2.0 * h * h * h)
                 for i in range(3))


def frenet_numeric(t, R, c, h):
    r1 = hv1(t, R, c)
    r2 = fd2(hv0, t, h, R, c)
    r3 = fd3(hv0, t, h, R, c)
    cr = cross3(r1, r2)
    ncr = norm3(cr)
    n1 = norm3(r1)
    kap = ncr / (n1 ** 3)
    tau = dot3(cr, r3) / (ncr * ncr)
    return kap, tau


def bishop_twist(R, c, nturn, M):
    """RK4 积分 Bishop 方程 du/dt = -(dT/dt·u)·T，累计 u 绕 T 的转角。

    Bishop 方程 du/ds = -(dT/ds·u)T 的等价形式；沿弧长积分给出
    dθ/ds = τ，故 θ(L)-θ(0) = ∫τ ds = 2π·n·sinα（圆螺旋解析值）。
    """
    v = math.sqrt(R * R + c * c)
    t = 0.0
    h = (2.0 * math.pi * nturn) / float(M)
    u = frenet_analytic(0.0, R, c)[3]
    total = 0.0

    def rhs(tt, uu):
        Tv = tuple(x / v for x in hv1(tt, R, c))
        dTv = tuple(x / v for x in hv2(tt, R, c))
        k = -dot3(dTv, uu)
        return (k * Tv[0], k * Tv[1], k * Tv[2])

    def theta_of(uu, tt):
        fram = frenet_analytic(tt, R, c)
        return math.atan2(dot3(uu, fram[4]), dot3(uu, fram[3]))

    th_prev = theta_of(u, 0.0)
    for _ in range(M):
        k1 = rhs(t, u)
        k2 = rhs(t + 0.5 * h, tuple(u[i] + 0.5 * h * k1[i] for i in range(3)))
        k3 = rhs(t + 0.5 * h, tuple(u[i] + 0.5 * h * k2[i] for i in range(3)))
        k4 = rhs(t + h, tuple(u[i] + h * k3[i] for i in range(3)))
        un = tuple(u[i] + h * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) / 6.0
                   for i in range(3))
        nn = norm3(un)
        u = (un[0] / nn, un[1] / nn, un[2] / nn)
        t += h
        th_now = theta_of(u, t)
        dth = th_now - th_prev
        while dth > math.pi:
            dth -= 2.0 * math.pi
        while dth < -math.pi:
            dth += 2.0 * math.pi
        total += dth
        th_prev = th_now
    return total


def pmns_matrix(th12, th23, th13, dcp):
    """PDG 三味标准参数化（θ 以度给出，δ 以弧度给出）。"""
    s12 = math.sin(math.radians(th12)); c12 = math.cos(math.radians(th12))
    s23 = math.sin(math.radians(th23)); c23 = math.cos(math.radians(th23))
    s13 = math.sin(math.radians(th13)); c13 = math.cos(math.radians(th13))
    ph = complex(math.cos(dcp), math.sin(dcp))
    return [
        [c12 * c13, s12 * c13, s13 * ph.conjugate()],
        [-s12 * c23 - c12 * s23 * s13 * ph,
         c12 * c23 - s12 * s23 * s13 * ph, s23 * c13],
        [s12 * s23 - c12 * c23 * s13 * ph,
         -c12 * s23 - s12 * c23 * s13 * ph, c23 * c13],
    ]


def jarlskog_from_matrix(u):
    return (u[0][1] * u[1][2] * u[0][2].conjugate() * u[1][1].conjugate()).imag


def jarlskog_closed(th12, th23, th13, dcp):
    s12 = math.sin(math.radians(th12)); c12 = math.cos(math.radians(th12))
    s23 = math.sin(math.radians(th23)); c23 = math.cos(math.radians(th23))
    s13 = math.sin(math.radians(th13)); c13 = math.cos(math.radians(th13))
    return s12 * c12 * s23 * c23 * s13 * c13 * c13 * math.sin(dcp)


# ------------------------------------------------------------------
# 1. 自检：先校准工具，再判来稿路线
# ------------------------------------------------------------------
say("-" * 78)
say("1. 自检（工具校准与既有读数交叉复核）")
say("-" * 78)

R0, C0, NT = 1.0, 0.5, 3.0
KAP0, TAU0, TV0, NV0, BV0 = frenet_analytic(0.0, R0, C0)
VV0 = math.sqrt(R0 * R0 + C0 * C0)
SIN_A0 = C0 / VV0
ALPHA0 = math.asin(SIN_A0)
TW_OPEN = NT * SIN_A0
INTS_TAU = 2.0 * math.pi * TW_OPEN

HS = (1.0e-2, 3.0e-3, 1.0e-3, 3.0e-4, 1.0e-4)
err_kap = []
err_tau = []
for hh in HS:
    kn, tn = frenet_numeric(0.7, R0, C0, hh)
    err_kap.append(abs(kn - KAP0) / KAP0)
    err_tau.append(abs(tn - TAU0) / TAU0)
best_kap = min(err_kap)
best_tau = min(err_tau)
sc("1", (best_kap < 1.0e-6 and best_tau < 1.0e-5),
   "Frenet 解析/数值对拍 (κ=%.6f τ=%.6f)：rel_err(κ) 窗口最小 %.3e@%.0e；rel_err(τ) 窗口最小 %.3e@%.0e；"
   "h=1e-4 处回升至 %.3e/%.3e（三阶差分舍入 ε/h^3 与截断 h^2 的折中窗口）"
   % (KAP0, TAU0, best_kap, HS[err_kap.index(best_kap)],
      best_tau, HS[err_tau.index(best_tau)], err_kap[-1], err_tau[-1]))

th_num = bishop_twist(R0, C0, NT, 8000)
sc("2", abs(abs(th_num) - INTS_TAU) / abs(INTS_TAU) < 1.0e-8,
   "Bishop 平行传输 RK4 复现 ∫τds：数值 %.12f rad（Bishop 标准约定 θ'=−τ，故带负号）；"
   "|数值| vs 解析 2πn·sinα %.12f，rel %.3e（自抓：首版把解析预期写成 +∫τds）"
   % (th_num, INTS_TAU, abs(abs(th_num) - INTS_TAU) / abs(INTS_TAU)))

th_flat = bishop_twist(1.0, 0.0, 2.0, 4000)
sc("3", abs(th_flat) < 1.0e-12,
   "平直圆（c=0 ⇒ τ=0，κ=1/R=%.6f）总扭转 %.3e（机器零）"
   % (frenet_analytic(0.0, 1.0, 0.0)[0], th_flat))

scale_vals = []
for lam in (1.0, 2.0, 5.0, 10.0, 100.0):
    scale_vals.append(bishop_twist(R0 * lam, C0 * lam, NT, 4000))
dev_scale = max(abs(x - scale_vals[0]) / abs(scale_vals[0]) for x in scale_vals)
sc("4", dev_scale < 1.0e-7,
   "∫τds 尺度不变（λ=1,2,5,10,100）：最大相对偏差 %.3e（复现 S03-V18_6 SC6）" % dev_scale)

TH12, TH23, TH13 = 33.44, 49.0, 8.57
DCP = 1.19 * math.pi
SIG_DCP = 0.22 * math.pi
U_PMNS = pmns_matrix(TH12, TH23, TH13, DCP)
dev_unitarity = 0.0
for i in range(3):
    for j in range(3):
        val = sum(U_PMNS[i][k] * U_PMNS[j][k].conjugate() for k in range(3))
        tgt = 1.0 if i == j else 0.0
        dev_unitarity = max(dev_unitarity, abs(val - tgt))
j_mat = jarlskog_from_matrix(U_PMNS)
j_cls = jarlskog_closed(TH12, TH23, TH13, DCP)
sc("5", (dev_unitarity < 1.0e-15 and abs(j_mat - j_cls) < 1.0e-15),
   "PMNS 幺正性 max|UU†−I| = %.3e；Jarlskog 九元式 %.12e vs 闭式 %.12e（偏差 %.3e）"
   % (dev_unitarity, j_mat, j_cls, abs(j_mat - j_cls)))

J_CKM_REF = 3.145434e-05
j_ckm = jarlskog_closed(13.0029, 2.3968, 0.2114, math.radians(68.526))
sc("6", abs(j_ckm - J_CKM_REF) / J_CKM_REF < 1.0e-3,
   "交叉复核 S03-V18_8 的 J_quark：本册复算 %.9e vs 其登记 %.9e，相对差 %.2e"
   % (j_ckm, J_CKM_REF, abs(j_ckm - J_CKM_REF) / J_CKM_REF))

lam_c = HBARC_EVM / M_NU_EV
tau_nu = 1.0 / lam_c
l_first_max = math.pi * 0.001 / (2.0 * K_CONV * 7.42e-05)
sc("7", (abs(K_CONV - 1.266933e-03) / 1.266933e-03 < 1.0e-6
         and abs(tau_nu - 2.5339e05) / 2.5339e05 < 1.0e-4
         and abs(l_first_max - 1.6709e04) / 1.6709e04 < 1.0e-4),
   "交叉复核 S03-V18_9 三读数：K_conv %.9e（其 1.266933e-03）；τ_ν %.6e m^-1（其 2.5339e5）；反应堆第一极大 %.6e m（其 1.6709e4）"
   % (K_CONV, tau_nu, l_first_max))
say("")

# ------------------------------------------------------------------
# 2. 判定项
# ------------------------------------------------------------------
say("-" * 78)
say("2. 判定项（分支 B-1 执行结果）")
say("-" * 78)

_, _, T_end, N_end, B_end = frenet_analytic(2.0 * math.pi * NT, R0, C0)
dT_end = max(abs(T_end[i] - TV0[i]) for i in range(3))
dN_end = max(abs(N_end[i] - NV0[i]) for i in range(3))
dF_end = max(abs(B_end[i] - BV0[i]) for i in range(3))
SEAM_CHORD = (0.5 * math.pi - ALPHA0) / (2.0 * math.pi)

item("V11-a", "FAIL",
     "开路 holonomy 非唯一：同一中微子基线（产生→探测）给出三种互不相等的“几何相位”读数",
     ["读数① 全局标架直接比较（Frenet 标架 t=0 与 t=2πn）：|ΔT|=%.3e |ΔN|=%.3e |ΔB|=%.3e ⇒ 转角 0 (mod 2π)；"
      % (dT_end, dN_end, dF_end),
      "读数② Bishop 平行传输（本册 RK4，M=8000）：θ(L)−θ(0) = %.12f rad（Bishop 约定 θ'=−τ）⇒ |扭转| = %.12f 圈 = Tw_open = n·sinα"
      % (th_num, TW_OPEN),
      "读数③ 闭合缝处扭转 δ_seam 无体系内判据：Tw_closed = Tw_open + δ_seam/(2π)，δ_seam∈[−π,π] ⇒ 取值区间宽度 1.000000 圈",
      "读数① 与 ② 的绝对值之差 = %.12f rad ≠ 0 ⇒ 同一开路没有唯一的 holonomy 读数" % abs(th_num),
      "弦闭合（把端点用直弦接回）的缝修正是 |T 不连续角| = π/2 − α = %.9f rad = %.9f 圈；"
      "换任一其它闭合约定即得另一个值" % (0.5 * math.pi - ALPHA0, SEAM_CHORD),
      "结论：holonomy 是**闭路**的示性量；中微子从产生到探测是开路，闭合约定属外加输入 ⇒ "
      "B-1 所承诺的“可判决量 = holonomy 角”在物理基线上不存在。",
      "射程：否定的是“把 holonomy 角用作味变换的可判决量”；不否定“几何相位作为附加相位存在”"
      "（但那需先给耦合系数，见 V11-k 的 G5）。"])

CAP_BITS = math.log(2.0, 2.0)
NEED_BITS = math.log(3.0, 2.0)
GAP_BITS = NEED_BITS - CAP_BITS
feasible_tbl = []
for kk in (1, 2, 3):
    for mm in (1, 2, 3):
        feasible_tbl.append("%d→%d:%s" % (kk, mm, "可" if kk >= mm else "不可"))

item("V11-b", "FAIL",
     "内生离散标签容量 1 bit < 三味需求 log₂3 ⇒ 缺口 0.5849625007 bit（与 S03-V18_6 V6-g 同数字）",
     ["体系内生离散标签只有手性符号 ±1（S03-V18_8 V8-a/V8-e；本册不重复计否证）⇒ 容量 2 ⇒ %.10f bit"
      % CAP_BITS,
      "三味（ν_e / ν_μ / ν_τ）需求 log₂3 = %.10f bit" % NEED_BITS,
      "缺口 = %.10f bit" % GAP_BITS,
      "该数字与 S03-V18_6 V6-g 的“4π 判据只给 Z₂”缺口**逐位相同** ⇒ 同一算术（3 标签对 2 标签）"
      "在不同判据上重复出现，属体系能力上限，**登记为合流，不重复计否证**。",
      "标签容量/味数可行性：%s（k 为可用标签数、m 为味数）" % "  ".join(feasible_tbl),
      "若强行用全息量（Tw 连续 / Lk 整数）补足第三标签 ⇒ 落入 V11-d 的连续自由度，回到恒可拟合。"])

solve_set = []
for nn in (1, 2, 3):
    for kk in range(1, nn):
        aa = math.degrees(math.asin(float(kk) / float(nn)))
        val = nn * math.sin(math.radians(aa))
        solve_set.append((nn, kk, aa, abs(val - kk)))
counts = dict((nn, sum(1 for s in solve_set if s[0] == nn)) for nn in (1, 2, 3))
solved_txt = "  ".join("n=%d: α=%.6f°" % (s[0], s[2]) for s in solve_set)
max_dev_sol = max(s[3] for s in solve_set) if solve_set else 0.0

item("V11-c", "FAIL",
     "加框（Bishop）闭合条件一般不成立 ⇒ 螺旋孤子无良定义 Lk",
     ["闭合条件：θ(L)−θ(0) ∈ 2πℤ ⇔ n·sinα ∈ ℤ（圈数 × 螺距角正弦为整数）。",
      "固定 n 时 f(α)=n·sinα 在 (0,π/2) 严格单调（f'=n·cosα>0），像集为 (0,n) ⇒ 整数解恰 n−1 个：α_k = arcsin(k/n)。",
      "机器解集：n=1 ⇒ %d 个；n=2 ⇒ %d 个；n=3 ⇒ %d 个（%s）"
      % (counts[1], counts[2], counts[3], solved_txt),
      "解处残差 max|n·sinα − k| = %.3e（机器零）⇒ 解真实但为**孤立点**（(0,90°) 内 Lebesgue 测度 0）"
      % (max_dev_sol,),
      "⇒ 一般螺距角不满足闭合 ⇒ 一般螺旋孤子经 Bishop 加框得不到闭合 ribbon ⇒ 无良定义 Lk"
      "（V18_7 已对 trefoil 得到同款结论，本册把它落到中微子荷构型）。",
      "射程：否定“用闭路 Lk 作味标签”；不否定螺旋构型本身。"])

seed = 20261008
lcg_state = seed


def lcg_unit():
    global lcg_state
    lcg_state = (1103515245 * lcg_state + 12345) % 2147483648
    return lcg_state / 2147483648.0


max_resid = 0.0
ntest = 1000
for _ in range(ntest):
    for _i in range(3):
        target = lcg_unit()
        if target <= 0.0 or target >= 1.0:
            target = 0.5
        al = math.asin(target)
        max_resid = max(max_resid, abs(math.sin(al) - target))

item("V11-d", "FAIL",
     "连续标签 ⇒ 恒可拟合（构造性满射；与 S03-C0023 / S03-C0050 同型）",
     ["构造：给定任意目标标签三元组 ℓ ∈ (0,1)³，取 sinα_i = ℓ_i ⇒ α_i = arcsin(ℓ_i) 精确复现。",
      "机器：%d 组伪随机目标（LCG 种子 %d），最大残差 max|sin(arcsin ℓ) − ℓ| = %.3e（机器零）"
      % (ntest, seed, max_resid),
      "⇒ 每个构型 1 个连续自由参数、映射为**满射且非单射**（同一标签值对应连续多构型）⇒ 零信息。",
      "⇒ 把连续量纳入味标签不新增任何可检验内容；三味所需的是**离散**标签（V11-b 给出容量缺口）。"])

J_LEP = jarlskog_closed(TH12, TH23, TH13, DCP)
J_MAX = jarlskog_closed(TH12, TH23, TH13, 0.5 * math.pi)
SIG_J = J_MAX * abs(math.cos(DCP)) * SIG_DCP
N_SIGMA_ZERO = abs(J_LEP) / SIG_J if SIG_J > 0.0 else float("inf")
SIG_TO_PI = abs(1.19 - 1.00) / 0.22

item("V11-e", "BOUNDARY",
     "主动放弃的判据（防过度否定）：δ_CP 对当前轻子数据无判别力，不得用作 FAIL 依据",
     ["实代数封闭（S03-V18_8 V8-*/F2-3）⇒ 轻子 Jarlskog J ≡ 0 ⇔ δ_CP ∈ {0, π}。",
      "本册独立复算：J_max = %.9e（δ=π/2）；以 δ=(1.19±0.22)π 代入 ⇒ J_lep = %.6e ± %.6e"
      % (J_MAX, J_LEP, SIG_J),
      "⇒ |J_lep|/σ = %.2f（<1）⇒ J=0 在 1σ 内；且 δ=π 距实测 %.2fσ ⇒ δ∈{0,π} **未被排除**。"
      % (N_SIGMA_ZERO, SIG_TO_PI),
      "对比：quark 扇区的 J = %.9e 相对不确定度极小（S03-V18_8 判 FAIL 成立），"
      "**该 FAIL 不得直接移植到轻子扇区**。" % J_CKM_REF,
      "⇒ 本判据主动放弃，登记留痕以防后续被误用为支持证据（与 S03-V18_8 对 δ/π 有理逼近的处置同型）。"])

item("V11-f", "BOUNDARY",
     "非绝热畸变不可定量（合流 S03-V18_9 V7-f，不重复计否证）",
     ["来稿 §4/§5-1 的“强挠率背景 ⇒ 非标准振荡畸变”需要在体系内给出 τ_bg(x) 场方程、"
      "耦合系数 g_τ 与边界条件。",
      "S03-V18_9 §7 已判：三项全缺，且数据反向给出 δτ 上限（太阳基线处 δτ_max/τ_ν ~ 1e-18）。",
      "本册不重复计否证，只登记为 B-1 的输入缺口（对应门禁 G5）。"])

item("V11-g", "PASS",
     "标准事实独立复算（非 GAQ 证据）：PMNS 幺正性 + Jarlskog 两式一致",
     ["max|U U† − I| = %.3e（三味标准参数化，θ12=%.2f° θ23=%.2f° θ13=%.2f° δ=1.19π）"
      % (dev_unitarity, TH12, TH23, TH13),
      "Jarlskog 九元式 %.12e vs 闭式 s12c12s23c23s13c13²sinδ %.12e，偏差 %.3e"
      % (j_mat, j_cls, abs(j_mat - j_cls)),
      "⇒ 属标准事实的机器复现，**不构成对 GAQ 的任何正面证据**。"])

item("V11-h", "PASS",
     "交叉复核既有产物读数（四项全部一致，非新发现）",
     ["S03-V18_8：J_quark 本册复算 %.9e vs 其登记 %.9e（相对差 %.2e）"
      % (j_ckm, J_CKM_REF, abs(j_ckm - J_CKM_REF) / J_CKM_REF),
      "S03-V18_9：K_conv 本册 %.9e vs 其 1.266933e-03；τ_ν 本册 %.6e vs 其 2.5339e5；"
      "反应堆第一极大 本册 %.6e m vs 其 1.6709e4 m" % (K_CONV, tau_nu, l_first_max),
      "⇒ 四读数一致，本册对 S03-V18_9 §2/§3 的数值基础无异议。"])

item("V11-i", "CORRECTED",
     "修正 S03-V18_9 §9“B-1 可立即开工”的读法：开工可行，但执行结论为阻塞",
     ["S03-V18_9 §9 称 B-1“3 项前提在体系内具备、可立即开工”，并给可判决量"
      "“(b) 手性符号与 holonomy 角”。",
      "执行后：① holonomy 角一项**不成立**（V11-a：开路非唯一）；② 剩余可判决量仅手性符号 ⇒ "
      "容量 1 bit（V11-b）；③ 加框闭合一般不成立（V11-c）；④ 连续量纳入标签即恒可拟合（V11-d）。",
      "⇒ 修正为：B-1 的**输入**在体系内具备（可开工），但**结论为阻塞**；"
      "与 S03-V18_10 对 S03-V18_5“分支三可行”的自我推翻同型。",
      "射程：修正的是“可立即开工 ⇒ 可行”的读法，不否定 S03-V18_9 的其余裁定。"])

claim_rows = 0
claim_unique = 0
claim_dups = []
try:
    HERE0 = os.path.dirname(os.path.abspath(__file__))
    CLAIMPATH = os.path.join(os.path.dirname(os.path.dirname(HERE0)), "claims.csv")
    with io.open(CLAIMPATH, "r", encoding="utf-8") as fh:
        body = [ln for ln in fh.read().splitlines() if ln.strip()]
    ids = [ln.split(",")[0] for ln in body[1:]]
    claim_rows = len(ids)
    seen = {}
    for cid in ids:
        seen[cid] = seen.get(cid, 0) + 1
    claim_unique = len(seen)
    claim_dups = sorted([k for k, v in seen.items() if v > 1])
except Exception as exc:
    say("      （claims.csv 审计跳过：%r）" % (exc,))

item("V11-j", "INFO",
     "治理：claims.csv 编号空间冲突（双占）与 S03-V18_9 零登记",
     ["机器审计（本册运行时读取）：claims.csv 数据行 %d，唯一 id %d，"
      "重复 id %d 个：%s" % (claim_rows, claim_unique, len(claim_dups), " ".join(claim_dups)),
      "成因：2026-10-07 批（S03-V18_10 分支三守恒律）与 2026-10-04 批（S03-V18_8 CKM）"
      "各自占用同一号段 C0045–C0053。",
      "另有缺口：S03-V18_9（中微子振荡来稿审计，12 条判定）**在 claims.csv 中无任何登记行**。",
      "处置：不擅自改写他人 claim 行；本册新条目自 S03-C0054 起，"
      "并在判定册中声明“跨册引用裸编号 C0045–C0053 有歧义，须带主题词/卷次”。"])

item("V11-k", "INFO",
     "六条门禁（S03-V18_9 §9 G1–G6）状态表：五条未满足、一条部分满足",
     ["G1 声明 ∫…ds 的积分域与标度读法 —— **未满足**（来稿未声明；V11-c/V11-d 给出的两类读法标度不同）",
      "G2 声明 τ 是否与 E 无关 —— **未满足**（来稿未声明；几何量 ∝L 而观测相位 ∝L/E，S03-V18_9 V7-b）",
      "G3 显式承担质量标度锚为外加公设 —— **未满足**（来稿未声明；S03-V18_3）",
      "G4 独立自由参数 ≤6 且无零信息方向 —— **未满足**（S03-V18_9 V7-d 判 ≥11 与 ≥3 个零信息方向）",
      "G5 给出 τ_bg(x) 动力学 + 耦合系数 + 边界条件 —— **未满足**（V11-f）",
      "G6 若走 B-1：显式加框 ✓ ／声明不还原 SM 相位 ✓ ／可判决量取手性符号与 holonomy 角 ✗"
      "（holonomy 一项见 V11-a）⇒ **部分满足**",
      "⇒ 按 S03-V18_9 §9“不满足不得开工”，B-1 亦不得开工；本册对 B-1 的判定是在"
      "**放松门禁**下“若开工会得到什么”的预演，不得读作对 B-1 的放行。"])

item("V11-l", "INFO",
     "分支裁定（回答来稿 §7 与“是否直接推导三味耦合 PDE”）",
     ["A（三味耦合 PDE + Rust 并行 FDTD）：**阻塞**。S03-V18_9 §9 的四项输入缺口 + "
      "拓扑非局域 vs PDE 局域的结构障碍；本册再加一条：三味区分需 1.585 bit，体系内生离散容量 1 bit。",
      "B（Berry 不变量）：半阻塞 → **执行其降级形式 B-1 后判为阻塞**（V11-a/b/c/d）。",
      "C（三者退耦时间对标 Planck）：**阻塞**（缺 GAQ 自己的 N_eff 与退耦温度，见 S03-V18_9 §9）。",
      "直接推三味耦合 PDE：**不推**。除 S03-V18_9 §9 三条理由（参数账未过约束、相位标度冲突未解、"
      "数值侧无已核验基线）外，本册新增第 4 条：离散标签容量缺口 0.5849625007 bit。",
      "⇒ 四条路全部阻塞，本轮**不产生新的可执行分支**。最小增广方向：需由**新增离散结构**"
      "（非连续几何量）承载该 0.585 bit，且必须显式登记为公设增广而非推导补全。"])

say("-" * 78)
n_pass = sum(1 for it in ITEMS if it[1] == "PASS")
n_fail = sum(1 for it in ITEMS if it[1] == "FAIL")
n_bnd = sum(1 for it in ITEMS if it[1] == "BOUNDARY")
n_cor = sum(1 for it in ITEMS if it[1] == "CORRECTED")
n_inf = sum(1 for it in ITEMS if it[1] == "INFO")
SC_OK = sum(1 for s in SCS if s[1])
say("汇总：条目 %d（PASS=%d FAIL=%d BOUNDARY=%d CORRECTED=%d INFO=%d）；自检 %d/%d"
    % (len(ITEMS), n_pass, n_fail, n_bnd, n_cor, n_inf, SC_OK, len(SCS)))
say("红线：本册未对 GAQ 任何物理预言给出正面支持；两个 PASS 均为标准事实复算与他人读数交叉复核。")
say("-" * 78)

HERE = os.path.dirname(os.path.abspath(__file__))
RUNDIR = os.path.join(os.path.dirname(HERE), "运行记录")
RPTPATH = os.path.join(RUNDIR, "S03_V18_11_分支B1_几何anholonomy_验证报告.txt")
WRITTEN = False
try:
    if not os.path.isdir(RUNDIR):
        os.makedirs(RUNDIR)
    with io.open(RPTPATH, "w", encoding="utf-8") as fh:
        fh.write("\n".join(RPT) + "\n")
    WRITTEN = True
    print("运行记录已写入：%s" % RPTPATH)
except Exception as exc:
    print("运行记录写入失败：%r" % (exc,))

EXIT_OK = (SC_OK == len(SCS)) and (len(ITEMS) > 0) and WRITTEN
sys.exit(0 if EXIT_OK else 1)
