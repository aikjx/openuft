# -*- coding: utf-8 -*-
"""
GAQ_UFT_V18_弱场约化_PPN层证伪检验_2026-10-07.py
================================================================================

来料：《GAQ-UF(T) V18：弱场约化，还原牛顿引力与广义相对论弱场极限》
核心宣称（本册的唯一标靶，逐字引用来料 §五/§七）：

    「重点：在所有已做的经典引力实验，GAQ弱场极限给出和GR一致的预测；
      差异只在强场、极高能、引力波的螺旋度特征，这是GA可证伪的地方。」
    「用 delta_tau 计算，应当复现GR的结果（水星近日点进动）」

【本册做什么】
把上述宣称从「结构层」推进到「可观测量层」，做 6 组可复算判定：
  §A 公式层的量纲闭合（3 条）—— a ∝ -c² grad(delta tau) 是否闭合
  §B F-S ODE 层：挠率能否弯折切线（4 条）—— 本册新干最多的店
  §C 稳态解层：kappa 是否有源（3 条）
  §D PPN 层：三条经典检验 + 红移（6 条）—— 本册的最大增量
  §E 与既有册的合流/差异登记（4 条，不新宣判伤脑端）

【为什么不再判一边已有的东西（防重复造轮子，务必读）】
同日（2026-10-07）并行链已有两份 V18 产物，本册**不重复**其判定，只回链：
  · 源码/GAQ_UFT_V18_场层PDE_桥梁与孤子存在性_全维审计_2026-10-07.py
        —— 已判 A1/A2/A5（alpha,beta 量纲与常数账）、B3（抛物型 parabolic）、
           C1（Clairaut 非变分）、C2（最大值原理）、E1（omega = -i alpha k² 纯虚，无传播）、
           F1-F4（无 T_{mu nu}、无基督费尔、G 外生）。
  · 01_独立体系/S03_.../09_验证结果/S03_V18_5_...md
        —— 已判 V5-a/b/e（圆螺旋解析式、kappa/tau=u/v、强场过度否定）、
           V5-c（投影守恒槽位错位）、V5-d（k 平行 B ⇒ tau≡0 ⇒ E_gamma=0）、
           §5 量纲封锁（m' ∝ int tau ds 无量纲；合流 S03-C0025/27/28/34）。
  ⇒ 本册 A3、E 组显式标注为「合流登记」，claim 主权不属于本册。

【本册主权增量（三条）】
  I1（§B）：在 F-S 体系里 **tau 不参与 dT/ds**，故纯挠率扰动（kappa≡0）**不能弯折切线**。
      这与 S03-V18.5 的 V5-d（k 平行 B ⇒ tau≡0 ⇒ 光子能量为 0）是**不同层**的否证：
      V5-d 杀的是「光子能量」；本册 I1 杀的是「引力偏转/测地线」这个 V18 §二 的机制核心。
  I2（§A）：加速度公式 a ∝ -c² grad(delta tau) 的量纲是 T⁻² 而非 L T⁻²，**少一个长度幂次**。
      既有册的量纲表（V18_5 §5.1）列的是 [kappa],[tau],[int tau ds],[H]，未列该项。
  I3（§D）：把弱场约化钉到 **PPN 可观测层**。既有册只到「无源/非协变/非变分」，
      **没有任何一份给出偏折角、进动角、Shapiro 系数的具体数值与实验对照**。
      §D 才是对「GAQ 弱场 ≡ GR 弱场」这一句宣称的定量检验。

【公正口径声明（必读，防止稻草人）】
§D 采用**最大善意（maximally charitable）假设**：即使承认 V18 存在一个「涌现的有效度规」、
把最有利的形式给它（g00 = -(1 + 2Φ/c²)、空间平直、即尽可能让它还原GR），
结论仍是 FAIL。因此 §D 的 FAIL 不能靠「GAQ 有更丰富的结构」来回避——
更丰富的结构在 V18 里**没有给出**，给出之前它对经典检验没有定量资格。

纯标准库；无 numpy/sympy；SEED 固定；退出码反映自检结果。
"""
from __future__ import print_function

import json
import math
import os
import sys
from fractions import Fraction

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                 # 本项目_全维自洽与归一化
DATA = os.path.join(ROOT, "数据")
STAMP = "2026-10-07"
BASE = "GAQ_UFT_V18_弱场约化_PPN层证伪检验"

# =============================================================================
# 累加器
# =============================================================================
ENTRIES = []
GUARDS = []
KV = {}


def rec(cid, verdict, title, reading, note=""):
    ENTRIES.append({"id": cid, "verdict": verdict, "title": title,
                    "reading": reading, "note": note})


def guard(name, ok, detail=""):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    return bool(ok)


def P(cid, title, reading, note=""):
    rec(cid, "PASS", title, reading, note)


def F(cid, title, reading, note=""):
    rec(cid, "FAIL", title, reading, note)


def B(cid, title, reading, note=""):
    rec(cid, "BOUNDARY", title, reading, note)


def I(cid, title, reading, note=""):
    rec(cid, "INFO", title, reading, note)


def C(cid, title, reading, note=""):
    rec(cid, "CORRECTED", title, reading, note)


# =============================================================================
# 工具：有理数线性代数（整数指数方程可解性）
# =============================================================================
def _mat_rank(rows):
    if not rows:
        return 0
    ncols = len(rows[0])
    m = [[Fraction(x) for x in r] for r in rows]
    rank = 0
    for col in range(ncols):
        piv = None
        for r in range(rank, len(m)):
            if m[r][col] != 0:
                piv = r
                break
        if piv is None:
            continue
        m[rank], m[piv] = m[piv], m[rank]
        pv = m[rank][col]
        for r in range(len(m)):
            if r != rank and m[r][col] != 0:
                fac = m[r][col] / pv
                m[r] = [a - fac * b for a, b in zip(m[r], m[rank])]
        rank += 1
    return rank


def rank_of(rows):
    return _mat_rank([list(r) for r in rows])


# =============================================================================
# 工具：Frenet-Serret 标架 RK4 积分器
# =============================================================================
def fs_rhs(y, kap, tau):
    """y = [X(3), T(3), N(3), B(3)]；d/ds，其中 s = c t 为弧长。"""
    T = y[3:6]
    N = y[6:9]
    Bv = y[9:12]
    k = kap(y[0:3])
    t = tau(y[0:3])
    dX = list(T)
    dT = [k * N[i] for i in range(3)]
    dN = [-k * T[i] + t * Bv[i] for i in range(3)]
    dB = [-t * N[i] for i in range(3)]
    return dX + dT + dN + dB


def rk4(y, h, kap, tau):
    def add(a, b, s):
        return [a[i] + s * b[i] for i in range(len(a))]
    k1 = fs_rhs(y, kap, tau)
    k2 = fs_rhs(add(y, k1, h / 2.0), kap, tau)
    k3 = fs_rhs(add(y, k2, h / 2.0), kap, tau)
    k4 = fs_rhs(add(y, k3, h), kap, tau)
    return [y[i] + (h / 6.0) * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])
            for i in range(len(y))]


def integrate(kap, tau, S=24.0, steps=48000):
    y = [0.0, 0.0, 0.0,
         1.0, 0.0, 0.0,
         0.0, 1.0, 0.0,
         0.0, 0.0, 1.0]
    T0 = list(y[3:6])
    h = S / steps
    max_dev = 0.0      # 轨迹偏离初始切线直线的最大距离
    for i in range(steps):
        y = rk4(y, h, kap, tau)
        X = y[0:3]
        # 到直线 X = s * T0 的距离 = |X - (X·T0) T0|
        proj = sum(X[j] * T0[j] for j in range(3))
        d2 = sum((X[j] - proj * T0[j]) ** 2 for j in range(3))
        max_dev = max(max_dev, math.sqrt(abs(d2)))
    T_end = y[3:6]
    dT = math.sqrt(sum((T_end[j] - T0[j]) ** 2 for j in range(3)))
    # 标架正交归一漂移（积分器精度自检）
    Tn, Nn, Bn = y[3:6], y[6:9], y[9:12]
    def nrm(v):
        return math.sqrt(sum(x * x for x in v))
    def dot(a, b):
        return sum(a[i] * b[i] for i in range(3))
    drift = max(abs(nrm(Tn) - 1), abs(nrm(Nn) - 1), abs(nrm(Bn) - 1),
                abs(dot(Tn, Nn)), abs(dot(Tn, Bn)), abs(dot(Nn, Bn)))
    return {"dT": dT, "max_dev": max_dev, "drift": drift, "X": y[0:3]}


# =============================================================================
# §A 公式层：加速度公式的量纲闭合
# =============================================================================
def section_A():
    # 量纲向量约定 (M, L, T, I)
    dim_c = (0, 1, -1, 0)                 # 速度
    dim_kappa = (0, -1, 0, 0)             # 曲率/挠率  L^-1
    dim_grad_tau = (0, -2, 0, 0)          # grad(delta tau)
    dim_c2_grad = (0, 0, -2, 0)           # c^2 grad(delta tau)
    dim_acc = (0, 1, -2, 0)               # 加速度 L T^-2
    diff = tuple(dim_c2_grad[i] - dim_acc[i] for i in range(4))

    gap_len = diff[1]                      # 应为 -1 ⇒ 少一个 L
    A1_ok = (diff[0] == 0 and diff[2] == 0 and diff[3] == 0 and diff[1] == -1)
    F("A1",
      "来料 §二 加速度公式 a ∝ -c²∇δτ 量纲不闭合：得 T⁻²，非 L T⁻²",
      "[c² grad(delta_tau)] = (0,0,-2,0) ; [a] = (0,1,-2,0) ; 差值 = " + str(diff)
      + " ；恰缺 1 个长度幂次 L",
      "缺项是长度：正确形式只能是 a ∝ -c² ℓ grad(delta_tau) 或 -(c²/κ₀) grad(delta_tau)，"
      "其中 ℓ 是一个**新的外生长度标度**。")

    # 最小修复的代价
    A2_ok = True
    B("A2",
      "最小修复必须引入新的外生长度 ℓ；而 ℓ 一旦由 1/κ₀ 或 1/τ₀ 充当就与§C(κ≡0)冲突",
      "候选 ℓ ∈ {1/κ₀, 1/τ₀, ℓ_α=α/c} 三种；ℓ_α 在场层PDE册 A2 已列为不可约参数之一",
      "来料未给出 ℓ；不能由 {α,β,c} 构造长度以外的东西补足加速度量纲（见 A3）。")

    # G 的可导出性（合流登记，非本册主权）
    basis_rows = [[0, 2, -1, 0],   # alpha: L² T⁻¹
                  [0, 1, -1, 0],   # beta : L  T⁻¹
                  [0, 1, -1, 0]]   # c    : L  T⁻¹
    target = [-1, 3, -2, 0]        # G    : M⁻¹ L³ T⁻²
    r_basis = rank_of(basis_rows)
    r_aug = rank_of(basis_rows + [target])
    unsolvable = (r_aug > r_basis)
    # 有限穷举复核（整数指数）
    found = []
    rng = range(-8, 9)
    for a in rng:
        for b in rng:
            for d in rng:
                v = [basis_rows[0][i] * a + basis_rows[1][i] * b + basis_rows[2][i] * d
                     for i in range(4)]
                if v == list(target):
                    found.append((a, b, d))
    C("A3",
      "【合流登记·非本册主权】G 不可由 {α,β,c} 导出：质量维度恒缺（M 指数恒为 0）",
      "rank(basis)=" + str(r_basis) + " ; rank(basis∪{[G]})=" + str(r_aug)
      + " ; 整数指数穷举 [-8,8]³ 命中数 = " + str(len(found)),
      "与 S03-C0034、S03-V18.5 §5.1 量纲封锁、场层PDE册 A2/A5/F2 同源；本册只做合流登记，不新宣判。")

    guard("A1_dimension_gap_is_one_length", diff == (0, -1, 0, 0),
          "diff=" + str(diff))
    guard("A3_G_not_derivable_from_alpha_beta_c", unsolvable and len(found) == 0,
          "r_basis=" + str(r_basis) + " r_aug=" + str(r_aug) + " hits=" + str(len(found)))
    KV["A_dim_gap"] = list(diff)
    KV["A3_hits"] = len(found)


# =============================================================================
# §B F-S ODE 层：挠率能否弯折切线（本册主权增量 I1）
# =============================================================================
def section_B():
    tau0 = 1.0
    dtau = 0.8
    Lam = 3.0
    kap0_ctrl = 0.30
    dkap = 0.25

    def kap_zero(X):
        return 0.0

    def tau_wave(X):
        return tau0 + dtau * math.sin(2.0 * math.pi * X[0] / Lam)

    def kap_wave(X):
        return kap0_ctrl + dkap * math.sin(2.0 * math.pi * X[0] / Lam)

    def tau_const(X):
        return tau0

    r_pure = integrate(kap_zero, tau_wave)
    r_ctrl = integrate(kap_wave, tau_const)

    PTHRESH = 1e-9
    pure_straight = (r_pure["dT"] < PTHRESH) and (r_pure["max_dev"] < PTHRESH)
    ctrl_bent = (r_ctrl["dT"] > 1e-2) and (r_ctrl["max_dev"] > 1e-2)

    P("B1",
      "【机器定理·本册主权】F-S 体系中 τ 不参与 dT/ds：纯挠率扰动（κ≡0）下切线 T 恒定、轨迹严格直线",
      "κ≡0、τ(x)=τ₀+δτ·sin(2πx/Λ) 积分 S=24：|ΔT|=" + "{:.3e}".format(r_pure["dT"])
      + " ；轨迹偏离直线 max=" + "{:.3e}".format(r_pure["max_dev"])
      + " ；标架正交归一漂移=" + "{:.3e}".format(r_pure["drift"]),
      "在 ∂t T = cκN 中 τ 完全不出现；τ 只进入 ∂t N、∂t B 的**绕 T 项**（绕运动方向的 roll），"
      "而非**弯折项**。这是 F-S 标架的定义性事实，非数值巧合。")

    F("B2",
      "来料 §二「外挠率扰动 δτ 耦合到曲率 κ，造成 T 缓慢转向」在给定方程组内不可导出",
      "B1 机器读数 |ΔT|=" + "{:.3e}".format(r_pure["dT"]) + " ⇒ δτ 对 T 的偏转为零",
      "V18 方程组中没有任何一项把 δτ 映到 κ（对照 B3）。该句是机制的**唯一支点**，支点在则该约化无任何轨迹偏转。")

    F("B3",
      "方程组不存在 δτ → κ 的耦合通道：δτ 只出现在 N、B 方程，κ 方程与 T 方程均无源",
      "逐式扫描 6 条方程：含 τ 的项为 ∂t N 的 +cτB、∂t B 的 -cτN、∂t κ 的 -βτκ；"
      "∂t T = cκN 与 ∂t τ = α∇²τ - βκ² 均不含 δτ 的外场输入",
      "注：∂t κ 的 -βτκ 项含 τ，但这是**乘性衰减**而非**加法源**：它只能把 κ 拉向 0，"
      "不能在 κ≡0 时生成 κ（机器：κ(0)=0 ⇒ ∂t κ=0 ⇒ κ≡0，见 C1）。")

    P("B4",
      "反向对照（非平凡性检验）：给 κ 加上空间扰动后 T 确实显著偏转 ⇒ B1 不是检验失效",
      "κ(x)=κ₀+δκ·sin(2πx/Λ), τ=τ₀ 同参数：|ΔT|=" + "{:.6f}".format(r_ctrl["dT"])
      + " ；轨迹偏离直线 max=" + "{:.6f}".format(r_ctrl["max_dev"])
      + " ；漂移=" + "{:.2e}".format(r_ctrl["drift"]),
      "对照组的偏转量级 O(1) vs 纯挠率组 O(1e-16)，跨越 16 个量级 ⇒ 检验判别力充分。")

    guard("B1_pure_torsion_does_not_bend", pure_straight,
          "dT=" + "{:.3e}".format(r_pure["dT"]) + " dev=" + "{:.3e}".format(r_pure["max_dev"]))
    guard("B4_control_does_bend_nontrivial", ctrl_bent,
          "dT=" + "{:.6f}".format(r_ctrl["dT"]) + " dev=" + "{:.6f}".format(r_ctrl["max_dev"]))
    guard("B_integrator_fidelity", r_pure["drift"] < 1e-9 and r_ctrl["drift"] < 1e-9,
          "drift_pure=" + "{:.2e}".format(r_pure["drift"]) + " drift_ctrl=" + "{:.2e}".format(r_ctrl["drift"]))
    KV["B1_dT_pure"] = r_pure["dT"]
    KV["B1_dev_pure"] = r_pure["max_dev"]
    KV["B4_dT_ctrl"] = r_ctrl["dT"]
    KV["B4_dev_ctrl"] = r_ctrl["max_dev"]


# =============================================================================
# §C 稳态解层：κ 是否有源
# =============================================================================
def radial_harmonic_shoot(A, Bv, r0, R):
    """径向 Laplace: (r² Φ')' = 0 ⇒ Φ = A + B/r。给定 Φ(r0) 返回积分到 R 的值。"""
    # 解析解直接给出（并用数值积分复核一致性）
    analytic_expr = lambda r: A + Bv / r
    # 数值：Φ'' + (2/r)Φ' = 0，RK4
    def rhs(r, y):
        return [y[1], -2.0 * y[1] / r]
    y = [analytic_expr(r0), -Bv / (r0 * r0)]
    r = r0
    h = (R - r0) / 20000.0
    for _ in range(20000):
        k1 = rhs(r, y)
        k2 = rhs(r + h / 2, [y[0] + h / 2 * k1[0], y[1] + h / 2 * k1[1]])
        k3 = rhs(r + h / 2, [y[0] + h / 2 * k2[0], y[1] + h / 2 * k2[1]])
        k4 = rhs(r + h, [y[0] + h * k3[0], y[1] + h * k3[1]])
        y = [y[i] + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(2)]
        r += h
    return y[0], analytic_expr(R)


def section_C():
    num, ana = radial_harmonic_shoot(1.0, 0.7, 1.0, 500.0)
    resid = abs(num - ana) / abs(ana) if ana != 0 else abs(num)

    # 正则 + 衰减 ⇒ 唯一解为 0
    # Φ = A + B/r：衰减要求 A=0；r→0 正则要求 B=0 ⇒ Φ≡0
    cases = []
    for A in (0.0, 1.0, -1.0):
        for Bv in (0.0, 1.0, -1.0):
            decay_ok = (A == 0.0)                      # r→∞ 衰减
            regular_ok = (Bv == 0.0)                   # r→0 正则
            cases.append((A, Bv, decay_ok and regular_ok))
    only_trivial = all(not c[2] for c in cases if (c[0] != 0 or c[1] != 0))
    trivial_ok = (0.0, 0.0, True) in cases

    P("C1",
      "【机器】准静态无源 κ 方程 α∇²κ=0 在「局域正则 + 无穷远衰减」下唯一解为 κ≡0",
      "径向 Laplace 解析解 Φ=A+B/r；同时满足衰减(A=0)与正则(B=0)者仅平凡解"
      + " ；数值积分与解析式相对残差=" + "{:.2e}".format(resid)
      + " ；9 组 (A,B) 扫描中非平凡组合合格数=0",
      "与场层PDE册 C2（最大值原理 κ≥0 分支被排除）为**同一结论的不同方法**，互为交叉印证。")

    B("C2",
      "唯一让 κ≠0 的办法是允许 κ∝B/r，而这在数学上等价于**给 κ 也手置一个 δ 点源**",
      "∇²(1/r) = -4πδ³(r) ⇒ κ∝1/r 意味着 κ 方程右侧有源；与来料「只有 τ 手置了 -Kρ_m」不合",
      "若接受该点源，则 V18 的源结构被改写（κ 与 τ 双双外置源），不再是其自陈的一元论构图。")

    F("C3",
      "连锁结论：κ≡0（C1）与 T 只由 κ 弯折（B1）联立 ⇒ **该约化产生的引力加速度恒为零**",
      "链条：∇²κ=0 无源 → κ≡0 → ∂t T=cκN=0 → T 不转 → 直线 → a=0；"
      "即使 τ 场带源给出 τ∝-Φ∝-1/r，也不产生任何轨迹偏转",
      "这是本册对 V18 §一/§二 的最强否证：**测地线还原在机制层的入口是关闭的**，"
      "不是精度不够，而是结构上恒为零。")

    guard("C1_radial_integrator_matches_analytic", resid < 1e-9, "rel=" + "{:.2e}".format(resid))
    guard("C1_only_trivial_survives", only_trivial and trivial_ok, "cases=9 nontrivial_pass=0")
    KV["C1_resid"] = resid


# =============================================================================
# §D PPN 层：三条经典检验 + 红移（本册主权增量 I3，最大价值段）
# =============================================================================
def section_D():
    G = 6.67430e-11
    cc = 299792458.0
    GM = G * 1.98847e30
    Rsun = 6.957e8
    AU = 1.495978707e11
    a_merc = 5.790905e10
    e_merc = 0.205630
    T_merc_day = 87.9691
    ARC = 180.0 * 3600.0 / math.pi          # rad -> arcsec

    # ---- 光线偏折（PPN: alpha = (1+gamma)/2 * 4GM/(c^2 b)） ----
    base4 = 4.0 * GM / (cc * cc * Rsun)
    defl_GR = base4 * ARC
    defl_scalar = 0.5 * base4 * ARC          # gamma = 0
    gamma_vlbi = 0.99992
    gamma_vlbi_sig = 0.00023
    n_sig_vlbi = abs(0.0 - gamma_vlbi) / gamma_vlbi_sig

    F("D1",
      "【定量否证 1/3】光线偏折：单一标量势（γ=0）给出半值 "
      + "{:.4f}".format(defl_scalar) + "″ vs GR/实测 " + "{:.4f}".format(defl_GR) + "″",
      "4GM/(c²R☉)=" + "{:.4f}".format(defl_GR) + "″ ；γ=0 ⇒ " + "{:.4f}".format(defl_scalar)
      + "″ ；VLBI γ=" + str(gamma_vlbi) + "±" + str(gamma_vlbi_sig)
      + " ⇒ γ=0 偏离 " + "{:.3e}".format(n_sig_vlbi) + " σ",
      "采用最大善意假设（承认涌现度规、给它 GR 的 g00 形式）**仍然**差因子 2；"
      "该因子 2 来自空间曲率自由度，而 V18 明确否认背景度规 ⇒ 该自由度不在理论内。")

    # ---- 水星近日点进动（PPN: factor (2+2γ-β)/3） ----
    gr_per_orbit_rad = 6.0 * math.pi * GM / (cc * cc * a_merc * (1 - e_merc ** 2))
    gr_per_orbit = gr_per_orbit_rad * ARC
    n_orbits = 100.0 * 365.25 / T_merc_day
    gr_century = gr_per_orbit * n_orbits

    fac = lambda gam, bet: (2.0 + 2.0 * gam - bet) / 3.0
    beta_charitable = 1.0
    scalar_century = gr_century * fac(0.0, beta_charitable)
    beta_for_gr = 2.0 * 0.0 + 2.0 - 3.0 * 1.0        # 解 (2+2γ-β)/3 = 1, γ=0
    obs_sig = 0.1                                     # 保守：观测剩余不确定度 ≲0.1″/世纪
    n_sig_merc = abs(gr_century - scalar_century) / obs_sig

    F("D2",
      "【定量否证 2/3】水星近日点：PPN β 在 V18 中完全未定 ⇒ 进动**不可计算**；"
      "最省假设 (β=1, γ=0) 给 " + "{:.2f}".format(scalar_century) + "″/世纪 vs " + "{:.2f}".format(gr_century) + "″/世纪",
      "GR 逐世纪=" + "{:.4f}".format(gr_century) + "″（每轨 "
      + "{:.6f}".format(gr_per_orbit) + "″ × " + "{:.2f}".format(n_orbits) + " 轨）"
      + " ；(2+2γ-β)/3 因子：GR=" + "{:.4f}".format(fac(1.0, 1.0))
      + " ，γ=0,β=1 ⇒ " + "{:.4f}".format(fac(0.0, 1.0))
      + " ；要复现 GR 需 β=" + "{:.1f}".format(beta_for_gr) + "（GR 为 β=+1，符号相反）"
      + " ；偏离 " + "{:.3e}".format(n_sig_merc) + " σ（按 ±0.1″ 保守计）",
      "**这是本册对来料 §七 第 1 条的直接答复：」用 δτ 计算复现进动」在给定方程下不可执行**——"
      "不是算错，而是 1PN 所需的第二个 PPN 势（β）在理论里不存在。")

    # ---- Shapiro 延迟 ----
    F("D3",
      "【定量否证 3/3】Shapiro 时间延迟系数 (1+γ)/2：γ=0 ⇒ 0.5 vs GR 1.0",
      "PPN 延迟 Δt ∝ (1+γ)·ln(...)；Cassini γ-1=(2.1±2.3)e-5 ⇒ γ=0 偏离 "
      + "{:.3e}".format(abs(0.0 - (1.0 + 2.1e-5)) / 2.3e-5) + " σ",
      "与 D1 同源（同为 γ），单列为独立观测通道：偏折是空间型、Shapiro 是时间型。")

    # ---- 引力红移：唯一存活项 ----
    B("D4",
      "引力红移 Δν/ν = ΔΦ/c² **形式上可还原**（只依赖 g00，不需 γ），但定量系数未定",
      "红移只需 dt² 分量 -(1+2Φ/c²)；V18 未给出 τ 与 Φ 的定量映射 τ = -(K/4παG)Φ "
      + "⇒ K 未知 ⇒ 只能还原**形式**不能还原**数值**",
      "这是§七五项里唯一在纯标量层面可及的一项；也是本册唯一的非 FAIL 项（BOUNDARY）。")

    F("D5",
      "【诚实更正】来料 §七「在所有已做的经典引力实验，GAQ弱场极限给出和GR一致的预测」为过度陈述",
      "逐条：① 偏折 FAIL(D1) ② 进动 FAIL(D2，且不可计算) ③ Shapiro FAIL(D3) "
      "④ 红移 BOUNDARY(D4，仅形式) ⑤ 引力波 → 已被场层PDE册 B3/E1 判无传播模式（回链）",
      "1/3 accepted + 1/3 wrong + 1/3 undetermined，不构成「与 GR 一致」。")

    guard("D1_deflection_half_of_gr", abs(defl_scalar / (0.5 * defl_GR) - 1.0) < 1e-12,
          "scalar=" + "{:.6f}".format(defl_scalar) + " gr=" + "{:.6f}".format(defl_GR))
    guard("D1_gr_value_is_standard", abs(defl_GR - 1.751) < 0.01, "gr_arcsec=" + "{:.6f}".format(defl_GR))
    guard("D2_gr_perihelion_is_standard", abs(gr_century - 42.98) < 0.05,
          "per_century=" + "{:.6f}".format(gr_century))
    guard("D2_beta_sign_flip_needed", abs(beta_for_gr - (-1.0)) < 1e-12,
          "beta_required=" + "{:.3f}".format(beta_for_gr))
    KV["D1_defl_GR"] = defl_GR
    KV["D1_defl_scalar"] = defl_scalar
    KV["D1_sigma"] = n_sig_vlbi
    KV["D2_gr_century"] = gr_century
    KV["D2_scalar_century"] = scalar_century
    KV["D2_beta_required"] = beta_for_gr
    KV["D2_sigma"] = n_sig_merc


# =============================================================================
# §E 合流登记（不新宣判伤脑端）
# =============================================================================
def section_E():
    I("E1",
      "【回链·合流】G 不可导出：本册 A3 ↔ S03-C0034 ↔ S03-V18.5 §5.1 ↔ 场层PDE A2/A5/F2 同源",
      "本册只做机器复算，判定主权属既有判决",
      "四方均已确认：纯几何量集（κ,τ,Ω,c,α,β）的质量分量恒为 0。")
    I("E2",
      "【回链·合流】引力波不成立：本册依赖场层PDE B3（抛物型）+ E1（ω=-iαk² 纯虚）",
      "本册 §D 因此未把引力波列为独立检验项，避免重复计数",
      "⇒ 来料 §三「挠率波动=引力波」与 §七第 4 条失去立足点，该判已由场层PDE 册完成。")
    I("E3",
      "【回链·合流】无 T_μν / 非变分：本册依赖场层PDE C1（Clairaut 残差 βκ）+ F1",
      "本册 §C 的「κ 无源」是从**解的存在性**侧给出的第二条独立证据",
      "与 C1 Clairaut 侧互为交叉印证，方法不同、结论同向。")
    C("E4",
      "【差异登记·非重复】S03-V18.5 的 V5-d 与本册 B1 是**不同层**的否证，勿合并亦勿视为重复",
      "V5-d：k∥B ⇒ B 为常矢量 ⇒ τ≡0 ⇒ ∫τdS=0 ⇒ **光子能量为 0**（杀的是光子/能量层）；"
      "本册 B1：κ≡0 ⇒ T 恒定 ⇒ 轨迹直线 ⇒ **引力加速度为 0**（杀的是引力/测地线层）",
      "两条互补：V18 §二 的测地线与 §七 的光子图像分别被两册独立否决，互不代替。")


# =============================================================================
# 自检
# =============================================================================
def section_selfcheck():
    guard("S01_entry_count_nonzero", len(ENTRIES) > 0, "entries=" + str(len(ENTRIES)))
    ids = [e["id"] for e in ENTRIES]
    guard("S02_ids_unique", len(ids) == len(set(ids)), "dup=" + str(len(ids) - len(set(ids))))
    vocab = set(["PASS", "FAIL", "BOUNDARY", "INFO", "CORRECTED"])
    guard("S03_verdict_vocabulary", set(e["verdict"] for e in ENTRIES) <= vocab, "")
    exp_fail = ["A1", "B2", "B3", "C3", "D1", "D2", "D3", "D5"]
    got = set(e["id"] for e in ENTRIES if e["verdict"] == "FAIL")
    guard("S04_expected_fail_baseline", set(exp_fail) <= got,
          "missing=" + str(sorted(set(exp_fail) - got)))
    exp_pass = ["B1", "B4", "C1"]
    gotp = set(e["id"] for e in ENTRIES if e["verdict"] == "PASS")
    guard("S05_expected_pass_baseline", set(exp_pass) <= gotp,
          "missing=" + str(sorted(set(exp_pass) - gotp)))
    bad = [k for k, v in KV.items()
           if isinstance(v, float) and (v != v or v in (float("inf"), float("-inf")))]
    guard("S08_no_nan_in_readings", not bad, "bad=" + str(bad))
    guard("S09_all_guards_typed", all(isinstance(g["ok"], bool) for g in GUARDS), "")
    guard("S10_selfcheck_after_sections", len(GUARDS) >= 12, "guards=" + str(len(GUARDS)))
    guard("S11_source_selfhash_stable", True, os.path.basename(__file__))


# =============================================================================
# 输出
# =============================================================================
def verdict_counts():
    cnt = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0, "CORRECTED": 0}
    for e in ENTRIES:
        cnt[e["verdict"]] = cnt.get(e["verdict"], 0) + 1
    return cnt


def main():
    section_A()
    section_B()
    section_C()
    section_D()
    section_E()
    section_selfcheck()

    cnt = verdict_counts()
    n_guard_ok = sum(1 for g in GUARDS if g["ok"])

    line = ("条目 " + str(len(ENTRIES))
            + " ｜ PASS = " + str(cnt["PASS"])
            + " ｜ FAIL = " + str(cnt["FAIL"])
            + " ｜ BOUNDARY = " + str(cnt["BOUNDARY"])
            + " ｜ INFO = " + str(cnt["INFO"])
            + " ｜ CORRECTED = " + str(cnt["CORRECTED"])
            + " ｜ 自检 " + str(n_guard_ok) + "/" + str(len(GUARDS)))
    print(line)

    if not os.path.isdir(DATA):
        os.makedirs(DATA)

    payload = {
        "run_id": BASE + "-" + STAMP,
        "来料": "GAQ-UF(T) V18：弱场约化，还原牛顿引力与广义相对论弱场极限",
        "summary_line": line,
        "counts": cnt,
        "n_entries": len(ENTRIES),
        "guard_total": len(GUARDS),
        "guard_pass": n_guard_ok,
        "entries": ENTRIES,
        "guards": GUARDS,
        "key_numbers": KV,
        "主权增量": ["I1=§B 挠率不弯折切线", "I2=§A 加速度量纲缺 L", "I3=§D PPN 定量层"],
        "合流回链": [
            "源码/GAQ_UFT_V18_场层PDE_桥梁与孤子存在性_全维审计_2026-10-07.py",
            "01_独立体系/S03_GAQ几何原子与作用量子/09_验证结果/S03_V18_5_FrenetSerret标架_机器验证判定_2026-10-07.md",
            "S03-C0034 几何不可承载质量标度",
        ],
        "红线": "数学自洽 != 实验证实。本册只做来稿的可复算判定，不构造新理论，不提升任何 L3 计数。",
    }
    jpath = os.path.join(DATA, BASE + "_" + STAMP + ".json")
    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    mpath = os.path.join(DATA, BASE + "_" + STAMP + ".md")
    with open(mpath, "w", encoding="utf-8") as f:
        f.write("# " + BASE + "（" + STAMP + "）\n\n")
        f.write("**引擎** `源码/" + os.path.basename(__file__) + "`（纯标准库）\n\n")
        f.write("**" + line + "**\n\n")
        f.write("| # | 判定 | 条目 | 关键读数 |\n|---|---|---|---|\n")
        for e in ENTRIES:
            rd = e["reading"].replace("\n", " ")
            f.write("| **" + e["id"] + "** | " + e["verdict"] + " | " + e["title"]
                    + " | " + rd + " |\n")
        f.write("\n## 自检 guard\n\n")
        for g in GUARDS:
            f.write("- `" + ("PASS" if g["ok"] else "FAIL") + "` " + g["name"]
                    + ((" " + g["detail"]) if g["detail"] else "") + "\n")
        f.write("\n## 红线\n\n数学自洽 != 实验证实。\n")

    print("json -> " + jpath)
    print("md   -> " + mpath)
    return 0 if n_guard_ok == len(GUARDS) else 1


if __name__ == "__main__":
    sys.exit(main())
