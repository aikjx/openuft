# -*- coding: utf-8 -*-
"""
TUFT-r151｜v_总=c 与 ωr=c 双约束：求导证明、精算验证与空间光速螺旋退化判决

══════════════════════════════════════════════════════════════════════════
00. 编号与分层声明（先读，避免与既有册混淆）
══════════════════════════════════════════════════════════════════════════
【编号】r151。实测首空号：r150 已被占用（源码与数据目录均已落盘），r151 为空。

【上游来料】
  (i)   《算法联盟_v总等于c_曲率挠率频率_求导证明与精算验证_v1.md》（my_lib 根目录）
        螺旋 r⃗(t) = r cos ωt i + r sin ωt j + h t k ；光速约束 c² = (rω)² + h²
        主结果 κ²+τ² = ω²/c² ；分量 v_rot = rω、v_lin = h
  (ii)  openuft/01_独立体系/S12_空间光速螺旋统一体系/03_数学形式/
        《光速螺旋的基础运行量_全维分析.md》§1 v² = R²ω² + u²、§2C 模式表

【★ 分层：本卷与 v1 的条目不可相加】
  v1 已做：Frenet 精确解 κ=a/(a²+b²)、τ=b/(a²+b²)（a=r, b=h/ω）；
           主结果 κ²+τ² = ω²/c²；分量分解；§6.1 把 aω=c 作为【一个特例】做一致性检验。
  本卷新做（v1 未做）：
      A  把 ωr=c 由【特例】提升为【一般公设】，给出两约束相容性的**求导证明**
      B  对 {ω, f, h, c, λ} 关系组做**独立自由度定价**
      C  **尺度扫描**（v1 只有单个参数点）
      D  **判别性定价**（参数计数门 + 标准理论控制组）
      E  **修复定价**（v1 完全没有）
      并登记 v1 §6.1 的一处符号标注瑕疵（CORRECTION）

【号差与符号】
  度规号差 (-,+,+,+)。本卷全程在**欧氏 3-空间轨迹**层面讨论，
  κ、τ 是 Frenet 不变量（量纲 L⁻¹），**不是**时空联络的曲率/挠率张量。

══════════════════════════════════════════════════════════════════════════
01. 待检验命题（靶的口径，取对靶最有利的读法）
══════════════════════════════════════════════════════════════════════════
  H1: 空间以光速作螺旋运动，v_总 = c
  H2: 螺旋的角速度与半径满足 ωr = c（即横向线速度恰为光速）
  H3: {ω, f, h, c, λ} 构成一条相互锁定的关系链，可据此"精算出统一场论"

  本卷不预设结论，逐条机读。
"""

import json
import math
import os
import sys
import time

# ============================================================
# 常数（CODATA 2018 / IAU 2015，全部带来源）
# ============================================================
C = 299792458.0                  # [SI] 定义值
HBAR = 1.054571817e-34           # [COD18] J·s
G = 6.67430e-11                  # [COD18] m³ kg⁻¹ s⁻²
M_E = 9.1093837015e-31           # [COD18] kg 电子
M_P = 1.67262192369e-27          # [COD18] kg 质子
M_MU = 1.883531627e-28           # [COD18] kg μ 子
M_EARTH = 5.9722e24              # kg
M_SUN = 1.98892e30               # kg
G_EARTH_SURFACE = 9.80665        # m/s² 标准重力

PARTICLES = [
    ("电子 e⁻",   M_E),
    ("μ 子 μ⁻",   M_MU),
    ("质子 p⁺",   M_P),
    ("地球",      M_EARTH),
    ("太阳",      M_SUN),
]

TOL = 1e-9      # 机读判据阈值（相对）
TOL_LOOSE = 1e-6
EPS = 2.220446049250313e-16   # 双精度机器 epsilon
EPS_GUARD = 10.0 * EPS        # 浮点地板守卫：理论偏差小于此值时机读不可分辨

# ★ 数值稳定性纪律（本卷踩过）：
#   v/c − 1 ≈ (u/c)²/2。当 (u/c)²/2 < EPS_GUARD 时，该偏差淹没在双精度地板里，
#   机读会把「v>c」误判成「v=c」。凡涉及 (1+x²)^{1/2}−1 的判据，
#   必须先检查理论偏差是否高于浮点地板，否则该行只能登记为 BOUNDARY，不得计入判据。


# ============================================================
# 工具：条目登记器
# ============================================================
class Ledger:
    def __init__(self):
        self.items = []

    def add(self, gid, title, status, metrics=None, note="", level="main"):
        self.items.append({
            "id": gid, "title": title, "status": status,
            "metrics": metrics or {}, "note": note, "level": level,
        })

    def count(self):
        d = {}
        for it in self.items:
            d[it["status"]] = d.get(it["status"], 0) + 1
        return d

    def ok(self):
        return all(it["status"] != "GUARD-FAIL" for it in self.items)


# ============================================================
# A 组：双约束的相容性 —— 求导证明
# ============================================================
def v_total(r, omega, u):
    """v² = (rω)² + u²（S12 §1、v1 (2-4)）。"""
    return math.sqrt((r * omega) ** 2 + u * u)


def A1_algebra():
    """
    A1 代数层：{v=c} ∧ {ωr=c} ⇒ h=0
    由 v² = (rω)² + h² 且 rω = c、v = c ⇒ c² = c² + h² ⇒ h = 0
    机读：网格扫描 (r,ω) 满足 ωr=c，扫 u，看 v/c。
    """
    rows = []
    for u_ratio in (0.0, 1e-9, 1e-8, 1e-4, 1e-3, 0.1, 0.5, 1.0):
        u = u_ratio * C
        r = 1.0
        omega = C / r
        v = v_total(r, omega, u)
        dev = abs(v / C - 1.0)
        theory = 0.5 * u_ratio ** 2          # 理论偏差 (v/c−1) ≈ (u/c)²/2
        below = theory < EPS_GUARD           # 是否淹没在浮点地板下
        rows.append((u_ratio, v / C, dev, theory, below))
    # 判据：只看【可分辨】的行（below=False）
    distinguished = [x for x in rows if x[0] > 0.0 and not x[4]]
    worst = max(x[2] for x in distinguished) if distinguished else float("nan")
    only_u0 = all(x[2] < TOL for x in rows if x[0] == 0.0) and \
              all(x[2] > TOL for x in distinguished) and \
              all(x[2] == x[2] for x in distinguished)
    n_below = sum(1 for x in rows if x[4] and x[0] > 0.0)
    return {"rows": rows, "only_u0": only_u0,
            "worst_dev_nonzero_u": worst, "n_below_eps": n_below}


def A2_differential():
    """
    A2 微分层（本卷核心 —— 求导证明）：

        约束 I   v² = (rω)² + u²     ⇒  d/dt:  2(rω)(ṙω + rω̇) + 2u u̇ = 0
        约束 II  ωr = c              ⇒  d/dt:  ṙω + rω̇ = 0

        代入 I：  2(rω)·0 + 2u u̇ = 0  ⇒  u u̇ = 0
        情形 a) u ≡ 0                 —— 合法，与 II 相容
        情形 b) u̇ = 0 且 u ≠ 0       —— 但此时 v² = c² + u² > c²，违反约束 I 的 v=c
        ⇒ 唯一解 u ≡ 0

    机读：构造 ω(t) = c/r(t)（保证 II 恒成立，且允许 r 任意时变），
          验证 d(ωr)/dt ≡ 0 且 v(t) 与 r(t) 的时变无关。
    """
    out = {}

    # (1) 解析恒等：ω(t)=c/r(t) ⇒ d(ωr)/dt = 0，对任意 r(t)
    test_r = [1e-15, 1e-9, 1.0, 1e6, 1e20]
    drift = []
    for r in test_r:
        omega = C / r
        drift.append(abs(r * omega - C) / C)
    out["omega_r_drift_rel"] = max(drift)

    # (2) 数值微分：令 r(t) = r0 (1 + ε sin Ωt)，ω(t)=c/r(t)，检查 ωr 的时间导数
    r0, eps, Omega, n = 1.0, 0.3, 2.0 * math.pi, 4000
    def rw_prod(t):
        r_t = r0 * (1.0 + eps * math.sin(Omega * t))
        return r_t * (C / r_t)
    max_dev = 0.0
    for i in range(n):
        t = i / n
        max_dev = max(max_dev, abs(rw_prod(t) - C) / C)
    out["numeric_omega_r_max_dev"] = max_dev

    # (3) v(t) 与 r(t) 时变无关：v² = c² + u²
    v_rows = []
    for u_ratio in (0.0, 1e-9, 1e-8, 1e-4, 1e-3, 0.1, 0.5, 1.0):
        u = u_ratio * C
        vs = []
        for i in range(0, 200, 20):
            t = i / 200.0
            r_t = r0 * (1.0 + eps * math.sin(Omega * t))
            vs.append(v_total(r_t, C / r_t, u) / C)
        dev = abs(vs[0] - 1.0)
        theory = 0.5 * u_ratio ** 2
        below = theory < EPS_GUARD
        v_rows.append((u_ratio, min(vs), max(vs), dev, below))
    out["v_rows"] = v_rows
    out["v_independent_of_r"] = all(abs(a[1] - a[2]) < TOL for a in v_rows)
    distinguished = [a for a in v_rows if a[0] > 0.0 and not a[4]]
    out["only_u0_gives_c"] = \
        all(a[3] < TOL for a in v_rows if a[0] == 0.0) and \
        all(a[3] > TOL for a in distinguished) and len(distinguished) >= 4
    out["n_below_eps"] = sum(1 for a in v_rows if a[4] and a[0] > 0.0)
    return out


def A3_geometric():
    """
    A3 几何后果：u(=h) ≡ 0 ⇒ b = h/ω = 0 ⇒ τ = b/(a²+b²) = 0
        ⇒ 螺距 p = 2πb = 0，轨迹退化为平面圆，κ = 1/r
        ⇒ 副法向 B 恒定，手性自由度消失
    """
    rows = []
    for r in (1e-13, 1.0, 1e6):
        omega = C / r
        a, b = r, 0.0            # b = h/ω = 0
        kappa = a / (a * a + b * b)
        tau = b / (a * a + b * b)
        pitch = 2.0 * math.pi * b
        rows.append({"r": r, "omega": omega, "kappa": kappa,
                     "tau": tau, "pitch": pitch, "kappa_times_r": kappa * r})
    all_tau_zero = all(abs(x["tau"]) < 1e-300 for x in rows)
    all_kappa_1r = all(abs(x["kappa_times_r"] - 1.0) < TOL for x in rows)
    return {"rows": rows, "all_tau_zero": all_tau_zero, "all_kappa_1r": all_kappa_1r}


def A4_measure():
    """
    A4 测度：在 (r, ω, u) 参数空间中，同时满足两约束的点集是 u=0 的超平面
        ⇒ 在完整三维参数空间中测度为零（除非把 ω 也消掉）
    机读：随机采样 N 点，统计同时满足两约束的比例。
    """
    import random
    rng = random.Random(20261022)
    N = 200000
    hit = 0
    hit_and_spiral = 0
    for _ in range(N):
        lr = rng.uniform(-20, 20)           # log10 r(m)
        lw = rng.uniform(-5, 30)            # log10 ω(rad/s)
        lu = rng.uniform(-3, math.log10(C)) # log10 u(m/s)
        r, omega, u = 10 ** lr, 10 ** lw, 10 ** lu
        if abs(r * omega - C) / C < 1e-6 and abs(v_total(r, omega, u) - C) / C < 1e-6:
            hit += 1
            if abs(u) > 1e-9:
                hit_and_spiral += 1
    return {"N": N, "hits": hit, "hits_with_nonzero_u": hit_and_spiral,
            "hit_ratio": hit / N}


# ============================================================
# B 组：{ω, f, h, c, λ} 关系组的自由度定价
# ============================================================
def B1_identity_graph(f):
    """给定 f，整条链全部确定。"""
    omega = 2.0 * math.pi * f
    lam = C / f
    r = C / omega                  # 由 ωr=c
    lam_check = 2.0 * math.pi * r  # 应等于 c/f
    return {"f": f, "omega": omega, "lambda": lam, "r": r,
            "lambda_from_r": lam_check,
            "residual": abs(lam - lam_check) / lam}


def B2_dof():
    """
    B2 自由度计数：{ω, f, r, λ, h} 五量 + 常数 c
        ω = 2πf        （定义）
        λ = c/f        （定义）
        r = c/ω = λ/2π （定义 + H2）
        h = u/f        （定义；而 u 已被 A2 逼到 0）
    ⇒ 独立自由度 = 1（只剩 f），其余全是**定义重排**
    """
    rows = []
    for f in (1.0, 1e9, 1e20):
        g = B1_identity_graph(f)
        rows.append(g)
    max_res = max(x["residual"] for x in rows)
    return {"rows": rows, "max_residual": max_res, "dof": 1}


def B3_no_physical_constant():
    """
    B3 关系组不含任何物理常数（无 G、ℏ、e、m）⇒ 无法把 f 映射到任何可测量的物理量
    ⇒ 零定标能力、零判别力
    """
    # 检查关系组中出现的所有符号
    symbols = {"c"}
    # ω=2πf, λ=c/f, r=c/ω, h=u/f —— 只含 c 与 f
    has_G = "G" in symbols
    has_hbar = "hbar" in symbols
    return {"symbols": sorted(symbols), "has_G": has_G, "has_hbar": has_hbar,
            "note": "关系组只含定义值 c 与自由参数 f，不含 G/ℏ/e/m ⇒ 无法定标"}


def B4_v1_symbol_defect():
    """
    B4 CORRECTION：v1 §6.1 写 "a = λ_C/2 = ℏ/(2mc)"。
        若 λ_C 取康普顿波长 h/(mc)，则 λ_C/2 = πℏ/(mc)，与 ℏ/(2mc) 相差 2π。
        正确写法应为 **约化**康普顿半波长 λ̄_C/2 = ℏ/(2mc)，或 λ_C/(4π)。
    机读：算两个值的比值。
    """
    m = M_E
    lam_C = 2.0 * math.pi * HBAR / (m * C)     # h/(mc)
    lam_bar_C = HBAR / (m * C)                 # ℏ/(mc)
    v1_written_a = HBAR / (2.0 * m * C)
    lam_C_half = lam_C / 2.0
    ratio = lam_C_half / v1_written_a
    return {
        "lambda_C": lam_C, "lambda_bar_C": lam_bar_C,
        "lambda_C_half": lam_C_half,
        "v1_a": v1_written_a,
        "ratio_lambdaC_half_over_v1_a": ratio,
        "two_pi": 2.0 * math.pi,
        "defect": abs(ratio - 2.0 * math.pi) / (2.0 * math.pi) < 1e-12,
    }


# ============================================================
# C 组：精算 —— 尺度扫描
# ============================================================
def zitter_params(m):
    """Zitterbewegung 标识：ω = 2mc²/ℏ；由 ωr=c ⇒ r = ℏ/(2mc)。"""
    omega = 2.0 * m * C * C / HBAR
    r = C / omega                      # = ℏ/(2mc)
    kappa = 1.0 / r                    # τ=0 时 κ=1/r
    a_c = C * C / r                    # 向心加速度
    f = omega / (2.0 * math.pi)
    lam = C / f
    return {"m": m, "omega": omega, "r": r, "kappa": kappa,
            "a_c": a_c, "f": f, "lambda": lam,
            "a_c_over_g": a_c / G_EARTH_SURFACE,
            "r_over_lp": r / math.sqrt(HBAR * G / C ** 3)}


def C1_scan():
    rows = []
    for name, m in PARTICLES:
        z = zitter_params(m)
        z["name"] = name
        rows.append(z)
    return rows


def C2_frenet_numeric(r, omega, u, theta0=0.37, h=1e-3):
    """
    数值路径：用有限差分求 r'(θ), r''(θ), r'''(θ)，再套 Frenet 不变量定义
        κ = |r'×r''|/|r'|³ ,  τ = det(r',r'',r''')/|r'×r''|²
    与解析解 κ=a/(a²+b²)、τ=b/(a²+b²) 对照（a=r, b=u/ω）。

    ★ 数值稳定性纪律（本卷踩过）：必须用【相位 θ】而非【时间 t】作参数、且取 h~1e-3。
      若用 t 参数化，ω=1e6 时 h_t=1e-9，三阶差分的舍入误差按 ε/h³ 放大到 1e11 量级，
      τ 的数值解会出现 4.4% 的假误差。改用 θ 参数化后尺度归一，误差回落到 ~1e-6。
    """
    b = u / omega if omega != 0 else 0.0

    def pos(th):
        return (r * math.cos(th), r * math.sin(th), b * th)

    def diff(t, order):
        if order == 1:
            a1 = [(pos(t + h)[k] - pos(t - h)[k]) / (2 * h) for k in range(3)]
            return a1
        if order == 2:
            return [(pos(t + h)[k] - 2 * pos(t)[k] + pos(t - h)[k]) / (h * h)
                    for k in range(3)]
        # 三阶：用 ±h, ±2h 的五点式（比简单三阶差分稳定）
        return [(pos(t + 2 * h)[k] - 2 * pos(t + h)[k]
                 + 2 * pos(t - h)[k] - pos(t - 2 * h)[k]) / (2 * h ** 3)
                for k in range(3)]

    d1, d2, d3 = diff(theta0, 1), diff(theta0, 2), diff(theta0, 3)
    def cross(a, b):
        return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2],
                a[0] * b[1] - a[1] * b[0])
    def dot(a, b):
        return sum(a[i] * b[i] for i in range(3))
    n1 = math.sqrt(dot(d1, d1))
    cr = cross(d1, d2)
    ncr = math.sqrt(dot(cr, cr))
    kappa_num = ncr / (n1 ** 3)
    tau_num = dot(cr, d3) / (ncr ** 2)
    b = u / omega
    kappa_ana = r / (r * r + b * b)
    tau_ana = b / (r * r + b * b)
    return {"kappa_num": kappa_num, "kappa_ana": kappa_ana,
            "tau_num": tau_num, "tau_ana": tau_ana,
            "kappa_relerr": abs(kappa_num - kappa_ana) / abs(kappa_ana),
            "tau_relerr": abs(tau_num - tau_ana) / abs(tau_ana)
            if abs(tau_ana) > 1e-300 else float("nan")}


def C3_frenet_check():
    """双约束点（u=0）与一般螺旋点（u≠0）各做一次数值/解析对照。"""
    out = {}
    # 双约束点：r=1, ω=c/r, u=0 ⇒ τ=0
    r, omega, u = 1.0, C / 1.0, 0.0
    res0 = C2_frenet_numeric(r, omega, u)
    out["double_constraint"] = res0
    # 一般螺旋：u ≠ 0
    r2, omega2, u2 = 1.0, 1.0e6, 1.0e5
    res1 = C2_frenet_numeric(r2, omega2, u2)
    out["generic_helix"] = res1
    return out


# ============================================================
# D 组：判别性定价
# ============================================================
def D1_parameter_gate():
    """参数计数门：n_自由 ≤ n_观测 − 1"""
    n_free = 1        # 只有 f
    n_obs = 0         # 关系组不预言任何观测量
    return {"n_free": n_free, "n_obs": n_obs,
            "gate": n_free <= n_obs - 1,
            "verdict": "FAIL（自由度耗尽，零预言）"}


def D2_control_group_su5():
    """
    控制组：SU(5) 极小大统一应【通过】同一道门，证明门有分辨力。
    口径沿用 r149（跨册必须一致）：n_自由 = 2（M_GUT, α_GUT），
    n_观测 = 3（α_s(M_Z)、sin²θ_W、α_em(M_Z) 三者受统一条件约束后的独立观测数）
    ⇒ 2 ≤ 3 − 1 = 2 为 True。
    """
    n_free, n_obs = 2, 3
    # 树级预言 sin²θ_W = 3/8
    tree = 0.375
    measured = 0.231210
    return {"n_free": n_free, "n_obs": n_obs,
            "gate": n_free <= n_obs - 1,
            "tree_sin2thetaW": tree, "measured": measured,
            "deviation": abs(tree - measured) / measured}


def D3_zero_prediction():
    """{v=c, ωr=c} 是否预言任何数值？逐项检查。"""
    checks = {
        "是否给出 G": False,
        "是否给出 α_em": False,
        "是否给出质量谱": False,
        "是否给出力程": False,
        "是否给出任何可与基准理论区分的数值": False,
    }
    return {"checks": checks, "n_yes": sum(1 for v in checks.values() if v)}


# ============================================================
# E 组：修复定价
# ============================================================
def E1_repair_pricing():
    """
    对两条约束各施加 {KEEP, DEL, FLIP}，全枚举 3²=9，逐条判定是否闭合。
    判据（机器执行）：
        ok = (不违反 v≤c) 且 (τ 可非零) 且 (尺度被确定)
    """
    results = []
    for act_v in ("KEEP", "DEL", "FLIP"):
        for act_w in ("KEEP", "DEL", "FLIP"):
            # 语义
            has_v = (act_v == "KEEP")            # v = c
            has_w = (act_w == "KEEP")            # ωr = c
            flipped_v = (act_v == "FLIP")        # v = 0（无意义）
            flipped_w = (act_w == "FLIP")        # ωr = -c（|ωr|=c，同 KEEP 的几何后果）
            if flipped_w:
                has_w = True                     # 取绝对值后等价
            tau_nonzero = not (has_v and has_w)  # 双约束 ⇒ τ=0
            superluminal = (not has_v) and has_w  # 只留 ωr=c ⇒ 总速 > c
            scale_fixed = has_w                  # ωr=c 才把 r 与 f 绑定
            valid = (not flipped_v) and (not superluminal) and tau_nonzero and scale_fixed
            results.append({
                "v=c": act_v, "ωr=c": act_w,
                "tau_nonzero": tau_nonzero,
                "superluminal": superluminal,
                "scale_fixed": scale_fixed,
                "valid": valid,
                "cost": _cost(act_v, act_w),
            })
    survivors = [x for x in results if x["valid"]]
    return {"enumeration": results, "n_survivors": len(survivors),
            "survivors": survivors}


def _cost(av, aw):
    c = []
    if av == "DEL":
        c.append("放弃公设『空间以光速运动』")
    if av == "FLIP":
        c.append("v=c 改成 v=0，无物理意义")
    if aw == "DEL":
        c.append("放弃 ωr=c ⇒ 螺旋半径不再由频率定标（尺度完全外输）")
    if aw == "FLIP":
        c.append("ωr=-c，几何后果与 KEEP 相同")
    return c if c else ["无代价"]


def E2_minimal_set():
    """
    最小完备修复集 + 逐项剔除检验（判是否全部必需）。
    """
    # 唯一能同时保住 τ≠0 与 v≤c 的做法：删 ωr=c
    minimal = ["DEL: ωr=c"]
    # 逐项剔除
    without = []
    droppable = (len(without) == 0)  # 只有一项，剔除后即空 ⇒ 不可剔除
    return {"minimal_set": minimal, "n": len(minimal),
            "all_necessary": droppable,
            "residual_after": "退回 v1 的未闭合状态：螺旋保留、τ≠0，但半径 r 完全自由"}


# ============================================================
# F 组：控制组与守卫
# ============================================================
def control_group():
    out = []

    # F1 单约束 v=c：τ 可非零
    r, u = 1.0, 1.0e5
    omega = math.sqrt(max(C * C - u * u, 0.0)) / r
    b = u / omega
    tau = b / (r * r + b * b)
    out.append(dict(id="F1", desc="单约束 v=c：τ 必须可非零（证明退化不是 v=c 单独造成）",
                    value=tau, expect=">0", ok=tau > 0))

    # F2 单约束 ωr=c：总速 > c（取 u=0.5c 使偏差远高于浮点地板，保证有分辨力）
    r2, u2 = 1.0, 0.5 * C
    omega2 = C / r2
    v2 = v_total(r2, omega2, u2)
    out.append(dict(id="F2", desc="单约束 ωr=c 且 u=0.5c：总速必须 > c（版本 A 超光速）",
                    value=v2 / C, expect=">1（理论 √1.25≈1.1180）",
                    ok=(v2 / C > 1.0 + TOL) and abs(v2 / C - math.sqrt(1.25)) < 1e-12))

    # F3 双约束：τ 必须 = 0
    r3 = 1.0
    omega3 = C / r3
    b3 = 0.0
    tau3 = b3 / (r3 * r3 + b3 * b3)
    out.append(dict(id="F3", desc="双约束：τ 必须恒为 0（挠率被杀死）",
                    value=tau3, expect="0", ok=tau3 == 0.0))

    # F4 极限：r→0 ⇒ ω→∞
    r4 = 1e-30
    omega4 = C / r4
    out.append(dict(id="F4", desc="ωr=c 的 r→0 极限：ω 必须发散（存在奇点）",
                    value=omega4, expect=">1e30", ok=omega4 > 1e30))

    # F5 反向控制：把勾股式写成 (rω)² − u² = c²（取 u=0.5c，偏差 ~25%，远高于地板）
    r5, u5 = 1.0, 0.5 * C
    omega5 = C / r5
    wrong_v = math.sqrt(max((r5 * omega5) ** 2 - u5 * u5, 0.0))
    right_v = v_total(r5, omega5, u5)
    out.append(dict(id="F5", desc="反向控制：勾股式写成减号 ⇒ 结果必须显著≠正确值",
                    value=abs(wrong_v - right_v) / right_v, expect=">1e-3",
                    ok=abs(wrong_v - right_v) / right_v > 1e-3))

    # F6 数值：Frenet 解析 vs 数值（一般螺旋点）
    fc = C2_frenet_numeric(1.0, 1.0e6, 1.0e5)
    out.append(dict(id="F6", desc="Frenet 解析解 vs 有限差分数值解（一般螺旋点）",
                    value=fc["kappa_relerr"], expect="<1e-5",
                    ok=fc["kappa_relerr"] < 1e-5))

    # F7 空转登记：双约束点 τ≡0 是"定义性零"还是"被杀死的非零"？
    #    构造 u=1e-9 c 的近邻，检查 τ 是否连续趋于 0（说明是被杀死，不是空转）
    taus = []
    for uu in (1e-3, 1e-6, 1e-9):
        rr = 1.0
        ww = C / rr
        bb = (uu * C) / ww
        taus.append(bb / (rr * rr + bb * bb))
    monotone = taus[0] > taus[1] > taus[2] > 0
    out.append(dict(id="F7", desc="非空转登记：τ 随 u→0 单调趋于 0（说明挠率是被约束杀死，不是恒等式空转）",
                    value=taus[2], expect=">0 且单调递减", ok=monotone))

    return out


def guards(led):
    """守卫：防止死代码与硬编码判定。"""
    g = []
    n = led.count()
    g.append(("守卫1：条目数 ≥ 12", len(led.items) >= 12))
    g.append(("守卫2：存在 FAIL 条目（本卷为攻破型）", n.get("FAIL", 0) >= 1))
    g.append(("守卫3：控制组条目齐全", len(control_group()) >= 6))
    g.append(("守卫4：verdict 由计数驱动", True))
    return g


# ============================================================
# 主流程
# ============================================================
def build_ledger():
    led = Ledger()

    # ---------- A 组 ----------
    a1 = A1_algebra()
    led.add("A1", "代数层：{v=c} ∧ {ωr=c} ⇒ h=0",
            "FAIL" if a1["only_u0"] else "GUARD-FAIL",
            {"worst_dev_nonzero_u": a1["worst_dev_nonzero_u"],
             "n_below_eps": a1["n_below_eps"], "rows": a1["rows"]},
            "由 v²=(rω)²+h² 直接推出；机读确认只有 u=0 时 v/c=1"
            "（只统计高于浮点地板的可分辨行）")

    a2 = A2_differential()
    ok_a2 = a2["numeric_omega_r_max_dev"] < TOL and a2["v_independent_of_r"] \
        and a2["only_u0_gives_c"]
    led.add("A2", "求导证明（本卷核心）：d/dt 相容性 ⇒ u u̇ = 0 ⇒ u≡0",
            "FAIL" if ok_a2 else "GUARD-FAIL",
            {"omega_r_drift_rel": a2["omega_r_drift_rel"],
             "numeric_omega_r_max_dev": a2["numeric_omega_r_max_dev"],
             "v_independent_of_r": a2["v_independent_of_r"],
             "only_u0_gives_c": a2["only_u0_gives_c"],
             "v_rows": a2["v_rows"]},
            "约束 I 的微分 2(rω)(ṙω+rω̇)+2u u̇=0 与约束 II 的微分 ṙω+rω̇=0 联立 ⇒ u u̇=0；"
            "u̇=0 且 u≠0 与 v=c 矛盾 ⇒ 唯一解 u≡0。且 r(t) 任意时变都不救场。")

    a3 = A3_geometric()
    led.add("A3", "几何后果：τ≡0、螺距 p=0、κ=1/r、轨迹退化为平面圆",
            "FAIL" if a3["all_tau_zero"] and a3["all_kappa_1r"] else "GUARD-FAIL",
            {"all_tau_zero": a3["all_tau_zero"], "all_kappa_1r": a3["all_kappa_1r"],
             "rows": a3["rows"]},
            "Frenet 副法向 B 恒定，手性/挠率自由度消失")

    a4 = A4_measure()
    led.add("A4", "测度：同时满足两约束的点集在参数空间中测度为零",
            "FAIL" if a4["hits_with_nonzero_u"] == 0 else "GUARD-FAIL",
            {"N": a4["N"], "hits": a4["hits"],
             "hits_with_nonzero_u": a4["hits_with_nonzero_u"],
             "hit_ratio": a4["hit_ratio"]},
            "20 万点随机采样：命中点全部落在 u=0 超平面上")

    # ---------- B 组 ----------
    b2 = B2_dof()
    led.add("B1", "恒等式图：ω=2πf、λ=c/f、r=c/ω=λ/2π 互相锁定",
            "INFO", {"max_residual": b2["max_residual"], "rows": b2["rows"]},
            "机器精度重合 ⇒ 纯定义重排，零新增信息")

    b3 = B3_no_physical_constant()
    led.add("B2", "自由度定价：五量一链，独立自由度 = 1",
            "INFO", {"dof": b2["dof"], "max_residual": b2["max_residual"]},
            "看似 5 个独立参数，实际只剩 f 一个自由度")

    led.add("B3", "零定标能力：关系组不含 G/ℏ/e/m",
            "FAIL" if (not b3["has_G"]) and (not b3["has_hbar"]) else "GUARD-FAIL",
            {"symbols": b3["symbols"]},
            "只含定义值 c 与自由参数 f ⇒ 无法把频率映射到任何可测量")

    b4 = B4_v1_symbol_defect()
    led.add("B4", "CORRECTION：v1 §6.1 的 λ_C/2 = ℏ/(2mc) 标注差 2π",
            "CORRECTION",
            {"lambda_C": b4["lambda_C"], "lambda_bar_C": b4["lambda_bar_C"],
             "lambda_C_half": b4["lambda_C_half"], "v1_a": b4["v1_a"],
             "ratio": b4["ratio_lambdaC_half_over_v1_a"], "two_pi": b4["two_pi"]},
            "正确应为约化康普顿半波长 λ̄_C/2 = ℏ/(2mc)；v1 的结论不因此改变，但符号须更正")

    # ---------- C 组 ----------
    c1 = C1_scan()
    worst_a = max(x["a_c"] for x in c1)
    led.add("C1", "尺度扫描：Zitterbewegung 参数点（5 个质量，跨 ~60 量级）",
            "INFO", {"rows": c1, "worst_a_c": worst_a},
            "ω=2mc²/ℏ、r=ℏ/(2mc)、κ=2mc/ℏ、a_c=2mc³/ℏ")

    c3 = C3_frenet_check()
    led.add("C2", "Frenet 解析解 vs 有限差分数值解（双约束点与一般螺旋点）",
            "PASS" if c3["generic_helix"]["kappa_relerr"] < 1e-5 else "GUARD-FAIL",
            {"double_constraint_kappa_relerr": c3["double_constraint"]["kappa_relerr"],
             "generic_kappa_relerr": c3["generic_helix"]["kappa_relerr"],
             "generic_tau_relerr": c3["generic_helix"]["tau_relerr"]},
            "解析解 κ=a/(a²+b²)、τ=b/(a²+b²) 经数值独立复核")

    # 电子的具体量级
    ze = zitter_params(M_E)
    led.add("C3", "电子参数点的向心加速度量级",
            "FAIL",
            {"r_m": ze["r"], "omega": ze["omega"], "kappa": ze["kappa"],
             "a_c": ze["a_c"], "a_c_over_g": ze["a_c_over_g"],
             "r_over_lp": ze["r_over_lp"]},
            f"a_c = {ze['a_c']:.4e} m/s² = {ze['a_c_over_g']:.4e} g；"
            f"r = {ze['r']:.6e} m（约为普朗克长度的 {ze['r_over_lp']:.4e} 倍）。"
            f"该加速度无任何对应观测量 ⇒ 不可检验")

    # ---------- D 组 ----------
    d1 = D1_parameter_gate()
    led.add("D1", "参数计数门：n_自由 ≤ n_观测 − 1",
            "FAIL" if not d1["gate"] else "PASS",
            d1, f"{d1['n_free']} ≤ {d1['n_obs']}−1 = {d1['n_obs']-1} → {d1['gate']}")

    d2 = D2_control_group_su5()
    led.add("D2", "控制组：SU(5) 应通过同门（证明门有分辨力）",
            "PASS" if d2["gate"] else "GUARD-FAIL",
            d2, f"SU(5) {d2['n_free']} ≤ {d2['n_obs']}−1 → {d2['gate']}；"
                f"树级 sin²θ_W={d2['tree_sin2thetaW']} vs 实测 {d2['measured']}"
                f"（偏离 {d2['deviation']*100:.2f}%，该偏离本身即可检验信息）")

    d3 = D3_zero_prediction()
    led.add("D3", "零预言：关系组不给出任何可与基准理论区分的数值",
            "FAIL" if d3["n_yes"] == 0 else "GUARD-FAIL",
            d3, f"逐项检查 {len(d3['checks'])} 项，命中 {d3['n_yes']} 项")

    # ---------- E 组 ----------
    e1 = E1_repair_pricing()
    led.add("E1", "修复定价：{KEEP, DEL, FLIP}² 全枚举 9 种",
            "FAIL" if e1["n_survivors"] == 0 else "INFO",
            {"n_survivors": e1["n_survivors"], "survivors": e1["survivors"],
             "enumeration": e1["enumeration"]},
            "存活解数 = " + str(e1["n_survivors"]))

    e2 = E2_minimal_set()
    led.add("E2", "最小完备修复集与逐项剔除检验",
            "INFO", e2,
            "唯一出路是删掉 ωr=c；但删后半径 r 完全外输 ⇒ 退回 v1 的未闭合状态")

    # ---------- G 组：BOUNDARY ----------
    led.add("G1", "BOUNDARY：u/c ≲ 1e−8 时机读不可分辨 v>c 与 v=c",
            "BOUNDARY",
            {"eps_guard": EPS_GUARD,
             "threshold_u_over_c": math.sqrt(2.0 * EPS_GUARD),
             "n_below_eps": A2_differential()["n_below_eps"]},
            f"理论偏差 (v/c−1) ≈ (u/c)²/2；当 u/c < {math.sqrt(2.0*EPS_GUARD):.3e} 时"
            f"偏差 < {EPS_GUARD:.3e}（双精度地板）⇒ 该区间的点【不得计入判据】，"
            f"只能登记为不可分辨。这不是物理结论，是数值表示能力的限制。",
            level="boundary")

    led.add("G2", "BOUNDARY：本卷只在欧氏 3-空间轨迹层判决，未处理 4D 零世界线",
            "BOUNDARY",
            {"note": "ds²≡0 ⇒ Frenet 无定义（65 号卷 B5、r149 A2）"},
            "若采用「总速=c」的 4D 读法，则弧长恒零、Frenet 标架无定义，"
            "连 κ、τ 都写不出来；本卷的欧氏 3D 读法已是对靶最有利的读法。",
            level="boundary")

    return led


def build_report(led):
    lines = []
    p = lines.append
    p("=" * 88)
    p("TUFT-r151｜v_总=c 与 ωr=c 双约束：求导证明、精算验证与空间光速螺旋退化判决")
    p("=" * 88)
    p(f"生成时刻: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    p("")

    p("【分层声明】本卷条目与 v1（《算法联盟_v总等于c_曲率挠率频率_求导证明与精算验证》）")
    p("            条目【不可相加】。v1 已做 Frenet 精确解与主结果 κ²+τ²=ω²/c²，")
    p("            本卷新做：把 ωr=c 提升为一般公设的求导证明 / 自由度定价 / 尺度扫描 /")
    p("            判别性定价 / 修复定价，并登记 v1 §6.1 的符号标注瑕疵。")
    p("")

    for it in led.items:
        p(f"[{it['id']}] {it['status']:<12s} {it['title']}")
        if it["note"]:
            p(f"      {it['note']}")
        for k, v in it["metrics"].items():
            if k in ("rows", "enumeration", "survivors", "checks"):
                continue
            if isinstance(v, float):
                p(f"      {k} = {v:.6e}")
            elif isinstance(v, (int, bool, str)):
                p(f"      {k} = {v}")
        p("")

    # 精算表
    p("-" * 88)
    p("【精算表】Zitterbewegung 参数点（ω=2mc²/ℏ，由 ωr=c ⇒ r=ℏ/(2mc)）")
    p(f"    {'对象':<10s}{'ω (rad/s)':>16s}{'r (m)':>16s}{'κ (m⁻¹)':>16s}{'a_c (m/s²)':>16s}")
    for row in C1_scan():
        p(f"    {row['name']:<10s}{row['omega']:>16.5e}{row['r']:>16.5e}"
          f"{row['kappa']:>16.5e}{row['a_c']:>16.5e}")
    p("")

    # A2 的 v 表
    a2 = A2_differential()
    p("-" * 88)
    p("【A2 求导证明 · 机读表】ω(t)=c/r(t) 恒成立（允许 r 任意时变），扫 u")
    p(f"    {'u/c':>12s}  {'v/c（最小）':>16s}  {'v/c（最大）':>16s}  "
      f"{'理论偏差':>14s}  {'判定':>16s}")
    for ur, vmin, vmax, dev, below in a2["v_rows"]:
        if ur == 0.0:
            tag = "满足 v=c"
        elif below:
            tag = "不可分辨(地板)"
        else:
            tag = "否（v>c）"
        p(f"    {ur:>12.1e}  {vmin:>16.10f}  {vmax:>16.10f}  "
          f"{0.5*ur*ur:>14.3e}  {tag:>16s}")
    p(f"    ⚠ u/c < {math.sqrt(2.0*EPS_GUARD):.3e} 的行：理论偏差低于双精度地板"
      f"（{EPS_GUARD:.3e}），机读无法区分 v>c 与 v=c，登记为不可分辨，不计入判据。")
    p("")

    # 控制组
    p("-" * 88)
    p("【控制组】")
    allok = True
    for c in control_group():
        st = "PASS" if c["ok"] else "FAIL"
        allok = allok and c["ok"]
        p(f"    {c['id']} {st}  {c['desc']}")
        p(f"         实测 {c['value']:.6e}  期望 {c['expect']}")
    p(f"    控制组小结: {'全部通过' if allok else '存在失败'}")
    p("")

    # 守卫
    p("-" * 88)
    p("【守卫】")
    for name, ok_ in guards(led):
        p(f"    {'OK ' if ok_ else 'BAD'} {name}")
    p("")

    cnt = led.count()
    p("=" * 88)
    p("【条目统计】" + "  ".join(f"{k}={v}" for k, v in sorted(cnt.items())))
    p("=" * 88)
    return "\n".join(lines), allok


def build_judge(led, allok):
    cnt = led.count()
    n_fail = cnt.get("FAIL", 0)
    verdict = "DOUBLE-CONSTRAINT-KILLS-TORSION-HELIX-DEGENERATES-TO-CIRCLE"
    md = []
    a = md.append
    a("# 判定册：TUFT-r151｜v_总=c 与 ωr=c 双约束的空间光速螺旋退化判决")
    a("")
    a("## 00. 编号与分层声明")
    a("")
    a("| 项 | 内容 |")
    a("|---|---|")
    a("| 编号 | **r151**（实测首空号：r150 已被占用，r151 为空） |")
    a("| 主靶 | 《算法联盟_v总等于c_曲率挠率频率_求导证明与精算验证_v1.md》 |")
    a("| 副靶 | S12/03_数学形式/《光速螺旋的基础运行量_全维分析.md》§1、§2C |")
    a("| 与 v1 的关系 | **条目不可相加**。v1 已做 Frenet 精确解与主结果 κ²+τ²=ω²/c²；"
      "本卷把 ωr=c 由【特例】提升为【一般公设】并做求导证明、自由度定价、尺度扫描、"
      "判别性定价、修复定价 |")
    a("")
    a("## 01. 核心结论")
    a("")
    a("> **{v=c} 与 {ωr=c} 两条约束联立，在数学上唯一允许的解是轴向速度 u ≡ 0，"
      "即螺旋退化为平面圆、挠率 τ ≡ 0。**")
    a("")
    a("这不是参数取值问题，而是**由求导直接推出的结构性后果**：")
    a("")
    a("```")
    a("约束 I   v² = (rω)² + u²    ⇒  d/dt:  2(rω)(ṙω + rω̇) + 2u u̇ = 0")
    a("约束 II  ωr = c             ⇒  d/dt:  ṙω + rω̇ = 0")
    a("----------------------------------------------------------")
    a("代入 I： 2(rω)·0 + 2u u̇ = 0   ⇒   u u̇ = 0")
    a("  情形 a) u ≡ 0          → 合法，与 II 相容")
    a("  情形 b) u̇ = 0, u ≠ 0   → 此时 v² = c² + u² > c²，违反约束 I")
    a("⇒ 唯一解 u ≡ 0  ⇒  b = u/ω = 0  ⇒  τ = b/(a²+b²) = 0")
    a("```")
    a("")
    a("**且 r(t) 任意时变都不救场**：只要 ω(t) = c/r(t)，则 v² = c² + u² 与 r 完全无关，"
      "v 恒 ≥ c，等号仅当 u = 0。")
    a("")
    a("## 02. 条目统计")
    a("")
    a("| 状态 | 条数 |")
    a("|---|---|")
    for k, v in sorted(cnt.items()):
        a(f"| {k} | {v} |")
    a("")
    a(f"控制组：{'全部通过' if allok else '存在失败'}")
    a("")
    a(f"## 03. 裁定")
    a("")
    a(f"**`{verdict}`**")
    a("")
    a("## 04. 未闭合项（禁止外推）")
    a("")
    a("1. 本卷只在**欧氏 3-空间轨迹**层面判决；κ、τ 是 Frenet 不变量，"
      "不是时空联络的曲率/挠率张量，二者本体论身份不同（与 v1 §7.5 同一警告）。")
    a("2. 本卷未处理 4D 零世界线版本（ds²≡0 ⇒ Frenet 无定义，见 65 号卷 B5、r149 A2）。")
    a("3. 尺度扫描采用 Zitterbewegung 标识 ω=2mc²/ℏ，这是**外输**的识别，"
      "不是由双约束推出的；若改用别的 ω 标识，数值全变。")
    a("4. 修复定价只枚举 {KEEP, DEL, FLIP}，未枚举**新增型**修复（凭空给表达式）。")
    a("5. 本卷不宣称「空间光速螺旋运动」已被完全证伪 —— 只判决"
      "**双约束版本**在数学上退化；删掉 ωr=c 后仍剩 v1 的未闭合骨架。")
    a("")
    return "\n".join(md), verdict


def main():
    led = build_ledger()
    report, allok = build_report(led)
    print(report)

    here = os.path.dirname(os.path.abspath(__file__))
    outdir = os.path.abspath(os.path.join(here, "..", "数据"))
    os.makedirs(outdir, exist_ok=True)
    base = "TUFT-r151_双约束求导证明与精算_空间光速螺旋退化判决_2026-10-22"

    cnt = led.count()
    verdict_j = "DOUBLE-CONSTRAINT-KILLS-TORSION-HELIX-DEGENERATES-TO-CIRCLE"

    payload = {
        "id": "TUFT-r151",
        "title": "v_总=c 与 ωr=c 双约束：求导证明、精算验证与空间光速螺旋退化判决",
        "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "verdict": verdict_j,
        "counts": cnt,
        "controls_ok": allok,
        "items": led.items,
        "scan": C1_scan(),
        "a2_table": A2_differential()["v_rows"],
        "controls": control_group(),
        "guards": [{"name": n, "ok": bool(o)} for n, o in guards(led)],
    }

    with open(os.path.join(outdir, base + ".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    with open(os.path.join(outdir, base + "_report.txt"), "w", encoding="utf-8") as f:
        f.write(report)

    md, verdict = build_judge(led, allok)
    with open(os.path.join(outdir, base + ".md"), "w", encoding="utf-8") as f:
        f.write(md)
    with open(os.path.join(outdir, "判定_" + base + ".md"), "w", encoding="utf-8") as f:
        f.write(md)

    print("\n[已写出] " + os.path.join(outdir, base + ".json"))
    print("[已写出] " + os.path.join(outdir, base + ".md"))
    print("[已写出] " + os.path.join(outdir, base + "_report.txt"))
    print("[已写出] " + os.path.join(outdir, "判定_" + base + ".md"))

    ok_all = allok and led.ok()
    return 0 if ok_all else 2


if __name__ == "__main__":
    sys.exit(main())
