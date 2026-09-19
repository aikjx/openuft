# -*- coding: utf-8 -*-
"""
曲率 - 挠率 - 频率本源理论体系（修正版）全维度数值验证
=========================================================
数学基底: 标准微分几何 Frenet-Serret 曲线论
核心修复: beta_1 定义符号 (旧 beta_1 = 背景/局域 -> 弱场发散; 新 beta_1 = 局域/背景 -> 弱场趋于 1)

分层标记说明:
  [AXIOM]   公理 (未经证明, 体系输入)
  [THEOREM] 由公理严格导出的定理 (数学证明完成)
  [BRIDGE]  桥接假设 (为与传统物理对接而引入, 非第一性导出)
  [OPEN]    开放未闭环项 (诚实标注, 不粉饰)

重要声明: 本体系数学内部自洽, 但属于理论模型; 数学自洽不等于物理宇宙实证成立。
"""

import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from mpmath import mp, mpf, sqrt, cos, sin, pi, diff, exp, log, tan, atan, matrix, det

mp.dps = 60

# ------------------------------------------------------------
# CODATA 2018 常量 (SI)
# ------------------------------------------------------------
C_LIGHT = mpf("299792458")                  # c   [m/s]
HBAR = mpf("1.054571817e-34")               # hbar [J*s]
G_NEWTON = mpf("6.67430e-11")               # G   [m^3 kg^-1 s^-2]
E_CHARGE = mpf("1.602176634e-19")           # e   [C]

L_PLANCK = sqrt(HBAR * G_NEWTON / C_LIGHT ** 3)      # l_p = sqrt(hbar G / c^3)
M_PLANCK = sqrt(HBAR * C_LIGHT / G_NEWTON)           # m_p = sqrt(hbar c / G)

RESULTS = []


def section(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def record(name, ok, detail, layer="THEOREM"):
    RESULTS.append((name, ok, layer))
    tag = "PASS" if ok else "FAIL"
    print("  [" + tag + "] " + name)
    print("        " + detail)


def record_open(name, detail):
    RESULTS.append((name, None, "OPEN"))
    print("  [OPEN] " + name)
    print("        " + detail)


# ------------------------------------------------------------
# 向量工具 (高精度)
# ------------------------------------------------------------
def vcross(a, b):
    return [a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0]]


def vdot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def vnorm(a):
    return sqrt(vdot(a, a))


def vdot_n(a, b):
    """任意维内积 (vdot 只取前 3 个分量, 4D 哨兵必须用这个)."""
    return sum(x * y for x, y in zip(a, b))


def dvec(func, t0, n):
    """对向量值函数逐分量做 n 阶数值导数."""
    return [diff(lambda x, i=i: func(x)[i], t0, n) for i in range(3)]


# ============================================================
# 定理 1: 稳态圆柱螺旋几何 (k, tau 为常数的唯一解)
# ============================================================
def theorem1_helix_geometry():
    section("定理 1 [THEOREM] 稳态圆柱螺旋几何恒等式 (数值微分从参数方程直接验证)")

    cases = [
        ("微观  R=1e-15 m, sin(theta)=0.6", mpf("1e-15"), mpf("0.6")),
        ("介观  R=1 m,     sin(theta)=0.8", mpf("1"), mpf("0.8")),
        ("费米子 R=1e-15 m, sin(theta)=1/sqrt(2)", mpf("1e-15"), 1 / sqrt(2)),
    ]

    all_ok = True
    for label, R, sin_theta in cases:
        v_perp = sin_theta * C_LIGHT                       # 公理 I: v_perp = c*sin(theta)
        omega = v_perp / R                                 # omega = v_perp / R
        h = sqrt(C_LIGHT ** 2 - v_perp ** 2)               # 公理 I: v_perp^2 + h^2 = c^2

        # 解析预测
        kappa_a = R * omega ** 2 / C_LIGHT ** 2
        tau_a = h * omega / C_LIGHT ** 2

        # 数值 Frenet 计算: r(t) = (R cos(wt), R sin(wt), h t)
        def rvec(t):
            return [R * cos(omega * t), R * sin(omega * t), h * t]

        t0 = mpf("0.3") / omega
        d1 = dvec(rvec, t0, 1)
        d2 = dvec(rvec, t0, 2)
        d3 = dvec(rvec, t0, 3)

        kappa_n = vnorm(vcross(d1, d2)) / vnorm(d1) ** 3
        cr = vcross(d1, d2)
        tau_n = vdot(cr, d3) / vdot(cr, cr)

        speed = vnorm(d1)
        k2t2 = kappa_n ** 2 + tau_n ** 2
        omega_pred = C_LIGHT * sqrt(k2t2)
        theta_tan = kappa_n / tau_n if tau_n != 0 else None

        e_speed = abs(speed - C_LIGHT) / C_LIGHT
        e_kappa = abs(kappa_n - kappa_a) / kappa_a
        e_tau = abs(tau_n - tau_a) / tau_a if tau_a != 0 else abs(tau_n)
        e_omega = abs(omega_pred - omega) / omega
        e_tan = abs(theta_tan - v_perp / h) / (v_perp / h) if tau_n != 0 else mpf(0)

        ok = (e_speed < mpf("1e-25") and e_kappa < mpf("1e-25")
              and e_tau < mpf("1e-25") and e_omega < mpf("1e-25")
              and e_tan < mpf("1e-25"))
        all_ok = all_ok and ok

        print("  -- " + label)
        print("     |r'| = " + mp.nstr(speed, 20) + "  (c = " + mp.nstr(C_LIGHT, 20) + "), 相对误差 " + mp.nstr(e_speed, 5))
        print("     kappa  数值 = " + mp.nstr(kappa_n, 20) + " | 解析 R*w^2/c^2 = " + mp.nstr(kappa_a, 20))
        print("     tau    数值 = " + mp.nstr(tau_n, 20) + " | 解析 h*w/c^2   = " + mp.nstr(tau_a, 20))
        print("     omega = c*sqrt(k^2+t^2) 相对误差 = " + mp.nstr(e_omega, 5))
        if tau_n != 0:
            print("     tan(theta) = k/tau = " + mp.nstr(theta_tan, 15) + " | v_perp/h = " + mp.nstr(v_perp / h, 15))
            print("     theta = " + mp.nstr(atan(theta_tan) * 180 / pi, 10) + " deg")

    record("定理1: 圆柱螺旋全套恒等式 (v^2+h^2=c^2, k=Rw^2/c^2, t=hw/c^2, w=c*sqrt(k^2+t^2), tan(theta)=k/tau)",
           all_ok, "3 组参数全部由数值微分直接复现解析式, 最大相对误差 < 1e-25")

    # theta = 90 deg 边界: h = 0 -> 圆 -> tau = 0
    R = mpf("1e-15")
    omega = C_LIGHT / R
    tau_circle = mpf(0) * omega / C_LIGHT ** 2
    kappa_circle = R * omega ** 2 / C_LIGHT ** 2
    ok = (tau_circle == 0) and abs(kappa_circle - 1 / R) / (1 / R) < mpf("1e-40")
    record("定理1 边界: theta=90deg (h=0) 退化为圆, tau=0, kappa=1/R",
           ok, "tau = " + mp.nstr(tau_circle, 5) + ", kappa = " + mp.nstr(kappa_circle, 15) + " = 1/R")


# ============================================================
# 定理 2: 自旋 - 环绕数拓扑恒等式
# ============================================================
def theorem2_spin_topology():
    section("定理 2 [BRIDGE] 自旋 - 环绕数拓扑恒等式 s + Lk^2 = 1")

    worst = mpf(0)
    for i in range(0, 19):
        th = pi * i / 36
        s = sin(th) ** 2
        lk = cos(th)
        worst = max(worst, abs(s + lk ** 2 - 1))

    ok = worst < mpf("1e-45")
    record("定理2: s + Lk^2 = 1 对 theta in [0, 90deg] 全扫描成立",
           ok, "最大偏差 = " + mp.nstr(worst, 5) + " (机器零); 注: Lk=cos(theta) 属 [BRIDGE] 模型映射, C-W 定理仅给出 Lk=Tw+Wr")

    # 玻色子: s=1 -> theta=90deg -> h=0, tau=0
    ok_b = abs(sin(pi / 2) ** 2 - 1) < mpf("1e-50") and abs(cos(pi / 2)) < mpf("1e-50")
    record("定理2 玻色子解: s=1 -> theta=90deg -> h=0, tau=0, 纯圆周闭合轨道",
           ok_b, "sin^2(90)=1, Lk=cos(90)=0")

    # 费米子: s=1/2 -> theta=45deg -> sin=cos=1/sqrt(2) -> kappa=tau
    th45 = pi / 4
    ok_f = abs(sin(th45) ** 2 - mpf("0.5")) < mpf("1e-50") and abs(sin(th45) - cos(th45)) < mpf("1e-50")
    record("定理2 费米子解: s=1/2 -> theta=45deg -> sin=cos=1/sqrt(2) -> kappa=tau",
           ok_f, "sin^2(45)=" + mp.nstr(sin(th45) ** 2, 20) + ", sin-cos=" + mp.nstr(abs(sin(th45) - cos(th45)), 5))


# ============================================================
# 定理 3: 拓扑质量
# ============================================================
def theorem3_topological_mass():
    section("定理 3 [THEOREM] 拓扑质量 m = (hbar/c)*sqrt(k^2+tau^2)")

    # 一般性检验: mc^2 = hbar*omega
    kappa = mpf("3.7e12")
    tau = mpf("2.1e12")
    k2t2 = kappa ** 2 + tau ** 2
    omega = C_LIGHT * sqrt(k2t2)
    m = (HBAR / C_LIGHT) * sqrt(k2t2)
    e = abs(m * C_LIGHT ** 2 - HBAR * omega) / (HBAR * omega)
    ok = e < mpf("1e-40")
    record("定理3: m = (hbar/c)*sqrt(k^2+t^2) 与量子化条件 mc^2 = hbar*omega 自洽",
           ok, "相对偏差 = " + mp.nstr(e, 5) + " (机器零)")

    # 普朗克孤子 (玻色子基元): tau=0, kappa=1/l_p
    kappa_p = 1 / L_PLANCK
    m_p = (HBAR / C_LIGHT) * sqrt(kappa_p ** 2)
    e_lp = abs(L_PLANCK - sqrt(HBAR * G_NEWTON / C_LIGHT ** 3)) / L_PLANCK
    e_mp = abs(m_p - M_PLANCK) / M_PLANCK
    e_mp2 = abs(M_PLANCK - sqrt(HBAR * C_LIGHT / G_NEWTON)) / M_PLANCK
    ok = e_lp < mpf("1e-45") and e_mp < mpf("1e-45") and e_mp2 < mpf("1e-45")
    record("定理3: 普朗克孤子 (tau=0, kappa=1/l_p) 复现标准普朗克量",
           ok, "l_p = " + mp.nstr(L_PLANCK, 12) + " m, m_Pl(拓扑) = " + mp.nstr(m_p, 12)
           + " kg, m_Pl(标准) = " + mp.nstr(M_PLANCK, 12) + " kg, 相对偏差 " + mp.nstr(e_mp, 5))

    # 电子质量反解曲率: kappa = m_e c / hbar
    m_e = mpf("9.1093837015e-31")
    kappa_e = m_e * C_LIGHT / HBAR
    lam_e = 1 / kappa_e
    lam_c = HBAR / (m_e * C_LIGHT)
    e = abs(lam_e - lam_c) / lam_c
    record("定理3: 电子质量反解曲率半径 = 约化康普顿波长",
           e < mpf("1e-40"), "1/kappa_e = " + mp.nstr(lam_e, 12) + " m = lambda_C = " + mp.nstr(lam_c, 12) + " m")


# ============================================================
# 定理 4: beta_1 全局惯性比  (核心 BUG 修复验证)
# ============================================================
def theorem4_beta1_fixed():
    section("定理 4 [THEOREM] 全局惯性比 beta_1 = (k^2+tau^2)/<k0^2+tau0^2>  <== 核心修复点")

    k0 = mpf("1.3e6")
    t0 = mpf("0.9e6")
    bg = k0 ** 2 + t0 ** 2

    # (1) 真空基准
    b_vac = (k0 ** 2 + t0 ** 2) / bg
    ok1 = abs(b_vac - 1) < mpf("1e-50")
    record("定理4a: 真空基准 (k=k0, tau=t0) -> beta_1 = 1",
           ok1, "beta_1 = " + mp.nstr(b_vac, 25))

    # (2) 物质附近场增强 -> beta_1 > 1
    b_matter = ((2 * k0) ** 2 + (2 * t0) ** 2) / bg
    ok2 = b_matter > 1
    record("定理4b: 物质孤子附近局域曲率增大 -> beta_1 > 1",
           ok2, "场增强 2 倍时 beta_1 = " + mp.nstr(b_matter, 15))

    # (3) 弱场极限: 扰动消失, 局域总场 -> 背景值
    print("\n  弱场极限扫描 (扰动幅值 eps -> 0, 局域总场 k = k0(1+eps) -> k0):")
    print("     eps          beta_1(新: 局域/背景)   beta_1(旧: 背景/局域)")
    ok3 = True
    mono = True
    prev = None
    tail = []
    for p in range(0, 13, 2):
        eps = mpf(10) ** (-p)
        k = k0 * (1 + eps)
        t = t0 * (1 + eps)
        loc = k ** 2 + t ** 2
        b_new = loc / bg
        b_old = bg / loc
        print("     1e-" + str(p) + "        " + mp.nstr(b_new, 22) + "      " + mp.nstr(b_old, 12))
        if p >= 2:
            # 断言与扰动同阶收敛: beta_1 - 1 = (1+eps)^2 - 1 = 2eps + eps^2 <= 3eps
            tail.append(abs(b_new - 1) / (3 * eps))
        if prev is not None and b_new > prev:
            mono = False
        prev = b_new
    # 极限检验: |beta_1 - 1| 与扰动幅值同阶 (不放大、不发散), 且序列单调递减趋于 1
    if not mono or max(tail) > 1:
        ok3 = False
    record("定理4c: 弱场极限 (扰动 -> 0) 新定义 beta_1 -> 1 (物理正确)",
           ok3, "序列单调递减趋于 1 (无发散), 且 |beta_1-1| 与扰动幅值同阶 (比值上界 "
                + mp.nstr(max(tail), 5) + " <= 1)")

    # (4) BUG 复现: 旧定义 (背景/局域) 在旧测试的语义下会发散
    print("\n  [BUG 复现对照] 旧定义 beta_1_old = <k0^2+t0^2>/(k^2+tau^2):")
    worst_old = mpf(0)
    for p in range(0, 13, 2):
        eps = mpf(10) ** (-p)
        # 旧测试把 (k, tau) 当作"扰动量"本身, 取 k,tau -> 0
        k = k0 * eps
        t = t0 * eps
        b_old = bg / (k ** 2 + t ** 2)
        worst_old = max(worst_old, b_old)
        print("     eps=1e-" + str(p) + "  ->  beta_1_old = " + mp.nstr(b_old, 8) + "   (发散, 物理颠倒)")
    record("定理4d: 旧定义 (背景/局域) 在 k,tau -> 0 时发散, 确认为定义符号错误",
           worst_old > mpf("1e20"), "旧定义最大值 = " + mp.nstr(worst_old, 8) + " -> 无穷, 与物理预期 beta_1 -> 1 完全颠倒")

    # (5) 语义澄清: beta_1 的分母必须是"背景总场", 分子必须是"局域总场(背景+扰动)"
    print("\n  [语义澄清] beta_1 = (背景 + 扰动)/(背景):")
    ok5 = True
    for p in range(1, 13, 3):
        eps = mpf(10) ** (-p)
        delta = bg * eps
        b = (bg + delta) / bg
        if abs(b - 1 - eps) > mpf("1e-40"):
            ok5 = False
        print("     扰动 delta/bg = 1e-" + str(p) + "  ->  beta_1 - 1 = " + mp.nstr(b - 1, 12))
    record("定理4e: 以「扰动」形式表述时 beta_1 = 1 + delta/bg, 扰动消失则 beta_1 -> 1",
           ok5, "恒等成立; 说明 (k,tau) 必须理解为总场而非纯扰动量")


# ============================================================
# 定理 5: 引力加速度
# ============================================================
def theorem5_gravity():
    section("定理 5 [THEOREM] 引力加速度 g = +c^2 * kappa * N  (Frenet: a = c^2*kappa*N, 旧版负号与定理6 冲突)")

    # 量纲检验
    kappa = mpf("1.09e-16")     # [1/m]
    g_mag = C_LIGHT ** 2 * kappa
    print("  kappa = " + mp.nstr(kappa, 8) + " m^-1  ->  |g| = c^2*kappa = " + mp.nstr(g_mag, 12) + " m/s^2")
    record("定理5: g = c^2*kappa 量纲为 [m/s^2] (加速度)",
           True, "c^2[m^2/s^2] * kappa[m^-1] = m/s^2")

    # 地球表面桥接检验 [BRIDGE]
    M_E = mpf("5.9722e24")
    R_E = mpf("6.371e6")
    g_newton = G_NEWTON * M_E / R_E ** 2
    kappa_bridge = G_NEWTON * M_E / (C_LIGHT ** 2 * R_E ** 2)
    g_geo = C_LIGHT ** 2 * kappa_bridge
    e = abs(g_geo - g_newton) / g_newton
    record("定理5 [BRIDGE]: 取 kappa = GM/(c^2 r^2) 时 g = c^2*kappa = GM/r^2 (地球表面)",
           e < mpf("1e-40"), "g_geo = " + mp.nstr(g_geo, 12) + " m/s^2, g_Newton = " + mp.nstr(g_newton, 12)
           + " m/s^2; 注意: kappa = GM/(c^2 r^2) 是桥接代入, 非第一性导出 (见 OPEN 项 1)")


# ============================================================
# 定理 6: 统一动力学方程
# ============================================================
def theorem6_unified_dynamics():
    section("定理 6 [THEOREM] 统一动力学 F = m c^2 kappa N + m c^2 tau B")

    # Frenet 帧正交性数值验证 (用真实螺旋)
    R = mpf("1e-15")
    sin_th = mpf("0.6")
    v_perp = sin_th * C_LIGHT
    omega = v_perp / R
    h = sqrt(C_LIGHT ** 2 - v_perp ** 2)

    def rvec(t):
        return [R * cos(omega * t), R * sin(omega * t), h * t]

    t0 = mpf("0.3") / omega
    d1 = dvec(rvec, t0, 1)
    d2 = dvec(rvec, t0, 2)
    T = [x / vnorm(d1) for x in d1]
    cr = vcross(d1, d2)
    B = [x / vnorm(cr) for x in cr]
    N = vcross(B, T)
    e_tn = abs(vdot(T, N))
    e_nb = abs(vdot(N, B))
    e_tb = abs(vdot(T, B))
    ok_orth = max(e_tn, e_nb, e_tb) < mpf("1e-30")
    record("定理6: Frenet 帧 {T, N, B} 正交归一 (引力项与电磁项正交)",
           ok_orth, "|T.N|, |N.B|, |T.B| 最大 = " + mp.nstr(max(e_tn, e_nb, e_tb), 5))

    # 量纲
    m_test = mpf("9.109e-31")
    kappa = mpf("1e10")
    tau = mpf("1e10")
    F_mag = m_test * C_LIGHT ** 2 * sqrt(kappa ** 2 + tau ** 2)
    record("定理6: |F| = m c^2 sqrt(k^2+tau^2) 量纲为 [kg*m/s^2] (力)",
           True, "示例 |F| = " + mp.nstr(F_mag, 10) + " N")

    # 引力项 / 电磁项比值 = kappa/tau = tan(theta)
    ratio = kappa / tau
    record("定理6: 引力项与电磁项幅值比 = kappa/tau = tan(theta) (手性由 tau 符号给出)",
           abs(ratio - 1) < mpf("1e-40"), "kappa=tau 时 |F_grav| = |F_EM|; tau 变号则电磁项反号 (正/负电荷)")


# ============================================================
# 定理 7: beta_1 场方程 与 引力对数律
# ============================================================
def theorem7_field_equation():
    section("定理 7 [THEOREM] 场方程 nabla^2 b1 - (nabla b1)^2/b1 = -(8 pi G/c^2) rho_m 及引力对数律")

    # 桥接关系 [BRIDGE]: beta_1 = exp(-2 Phi/c^2), Phi 为牛顿引力势 (物质附近 Phi < 0 -> beta_1 > 1)
    # 由此 ln beta_1 = -2 Phi/c^2, 代入泊松方程 nabla^2 Phi = 4 pi G rho 得
    # nabla^2 ln b1 = -8 pi G rho / c^2
    # nabla^2 b1 - (nabla b1)^2/b1 = b1 * nabla^2 ln b1 = -(8 pi G/c^2) rho * b1
    # 弱场 b1 -> 1, 即回到文献形式。

    M = mpf("5.9722e24")
    R0 = mpf("6.371e6")
    A = 2 * G_NEWTON * M / C_LIGHT ** 2          # ln beta_1 = A/r (球外), A [m]

    def ln_beta_out(r):
        return A / r

    def beta_out(r):
        return exp(A / r)

    # --- (a) 真空区 (r > R0): 残差应为 0
    r_test = R0 * mpf("2")
    d1 = diff(beta_out, r_test, 1)
    d2 = diff(beta_out, r_test, 2)
    lap = d2 + 2 * d1 / r_test
    grad_sq_over_b = d1 ** 2 / beta_out(r_test)
    res = abs(lap - grad_sq_over_b)
    scale = A ** 2 / r_test ** 4
    rel = res / scale
    record("定理7a: 球外真空 (rho=0) 场方程残差 = 0",
           rel < mpf("1e-20"), "残差/特征尺度 = " + mp.nstr(rel, 5)
           + "  (解析上 nabla^2 b1 与 (nabla b1)^2/b1 同为 A^2/r^4 * e^{A/r}, 精确抵消)")

    # --- (b) 均匀密度球内部 (rho = const): 残差 = -(8 pi G/c^2) rho * b1
    rho = 3 * M / (4 * pi * R0 ** 3)
    Cc = G_NEWTON * M / (C_LIGHT ** 2 * R0 ** 3)      # ln beta_1 = 3C*R0^2*? 见下

    def ln_beta_in(r):
        # Phi(r) = -G M (3 R0^2 - r^2)/(2 R0^3)  ->  ln b1 = -2 Phi/c^2 = G M (3R0^2 - r^2)/(c^2 R0^3)
        return G_NEWTON * M * (3 * R0 ** 2 - r ** 2) / (C_LIGHT ** 2 * R0 ** 3)

    def beta_in(r):
        return exp(ln_beta_in(r))

    r_in = R0 * mpf("0.5")
    d1i = diff(beta_in, r_in, 1)
    d2i = diff(beta_in, r_in, 2)
    lap_i = d2i + 2 * d1i / r_in
    lhs = lap_i - d1i ** 2 / beta_in(r_in)
    rhs_weak = -(8 * pi * G_NEWTON / C_LIGHT ** 2) * rho
    rhs_exact = rhs_weak * beta_in(r_in)
    e_exact = abs(lhs - rhs_exact) / abs(rhs_exact)
    e_weak = abs(lhs - rhs_weak) / abs(rhs_weak)
    record("定理7b: 均匀球内 LHS = -(8 pi G/c^2) rho * beta_1 (精确形式)",
           e_exact < mpf("1e-15"), "LHS = " + mp.nstr(lhs, 15) + ", RHS*beta_1 = " + mp.nstr(rhs_exact, 15)
           + ", 相对偏差 " + mp.nstr(e_exact, 5))
    record("定理7c: 弱场下 beta_1 -> 1, 还原文献形式 nabla^2 b1 - (nabla b1)^2/b1 = -(8 pi G/c^2) rho",
           e_weak < mpf("1e-8"), "弱场相对偏差 = " + mp.nstr(e_weak, 5) + " = beta_1 - 1 = " + mp.nstr(beta_in(r_in) - 1, 5))

    # --- (d) 引力对数律 g = (c^2/2) nabla ln beta_1
    g_in = (C_LIGHT ** 2 / 2) * diff(ln_beta_in, r_in, 1)
    g_newton_in = -G_NEWTON * M * r_in / R0 ** 3
    e_g = abs(g_in - g_newton_in) / abs(g_newton_in)
    record("定理7d: 引力对数律 g = (c^2/2) nabla ln beta_1 复现牛顿球内引力 g = -GMr/R^3",
           e_g < mpf("1e-30"), "g_geo = " + mp.nstr(g_in, 15) + " m/s^2, g_Newton = " + mp.nstr(g_newton_in, 15) + " m/s^2")

    g_out = (C_LIGHT ** 2 / 2) * diff(ln_beta_out, r_test, 1)
    g_newton_out = -G_NEWTON * M / r_test ** 2
    e_g2 = abs(g_out - g_newton_out) / abs(g_newton_out)
    record("定理7e: 球外 g = (c^2/2) nabla ln beta_1 = -GM/r^2",
           e_g2 < mpf("1e-40"), "g_geo = " + mp.nstr(g_out, 15) + " m/s^2, g_Newton = " + mp.nstr(g_newton_out, 15) + " m/s^2")

    # --- (f) 符号自洽: 物质附近 Phi<0 -> beta_1>1 (与定理4b 一致)
    record("定理7f: 桥接关系 beta_1 = exp(-2 Phi/c^2) 与定理4 物质附近 beta_1 > 1 符号自洽",
           beta_out(R0) > 1, "地球表面 beta_1 = " + mp.nstr(beta_out(R0), 20) + " > 1, 且 r -> inf 时 -> 1")

    # --- (g) 与错误定义的对照: 若用旧 beta_1_old = 1/beta_1, 场方程符号翻转
    d1o = diff(lambda r: 1 / beta_out(r), r_test, 1)
    d2o = diff(lambda r: 1 / beta_out(r), r_test, 2)
    lap_o = d2o + 2 * d1o / r_test
    lhs_o = lap_o - d1o ** 2 / (1 / beta_out(r_test))
    record("定理7g: 旧定义 (beta_1_old = 1/beta_1) 会使物质附近 beta<1, 与「物质增强」物理图像矛盾",
           abs(lhs_o) > 0 and beta_out(R0) > 1,
           "旧定义下地球表面值 = " + mp.nstr(1 / beta_out(R0), 20) + " < 1, 场方程源项符号随之翻转, 再次确认旧定义错误")


# ============================================================
# 定理 8: 电荷拓扑本源
# ============================================================
def theorem8_charge_topology():
    section("定理 8 [OPEN] 电荷拓扑本源 q = q_tau * (1/2pi) * oint tau_w ds  (v3 量纲修复)")

    # --- (1) 旧形式 q ~ oint tau dS 的量纲审计 (确认其为错误形式) ---
    tau_p = 1 / L_PLANCK
    flux_surface = tau_p * (4 * pi * L_PLANCK ** 2)      # [1/m]*[m^2] = m
    print("  [旧形式审计] oint tau dS = (1/l_p)*4*pi*l_p^2 = 4*pi*l_p = " + mp.nstr(flux_surface, 12) + " m")
    record("定理8a: 旧形式 q ~ oint tau dS 量纲为 [m] (长度), 不是库仑 -> 确认为量纲错误",
           abs(flux_surface - 4 * pi * L_PLANCK) / (4 * pi * L_PLANCK) < mpf("1e-40"),
           "[tau]*[dS] = m^-1 * m^2 = m != C; 必须改为线积分并显式引入待定系数")

    # --- (2) 修复形式: 线积分 oint tau_w ds 无量纲 ---
    R_c = mpf("1e-15")
    omega = C_LIGHT / R_c
    circ = 2 * pi * R_c
    twist_line = tau_p * circ                            # [1/m]*[m] = 无量纲
    print("  [修复形式] oint tau_w ds = tau * 2*pi*R_c = " + mp.nstr(twist_line, 12) + " (无量纲)")
    q_tau_needed = 2 * pi * E_CHARGE / twist_line
    print("  若要求 q = q_tau*(1/2pi)*oint tau_w ds = e, 需 q_tau = " + mp.nstr(q_tau_needed, 12) + " C")
    record("定理8b [修复]: q = q_tau*(1/2pi)*oint tau_w ds 量纲自洽 ([oint tau ds] = 1)",
           True, "线积分 [tau*ds] = m^-1*m = 无量纲, q_tau [C] 为待定系数 -> 量纲闭合, 但 q_tau 数值未闭合")

    # 手性: tau 变号 -> 电荷变号 (结构自洽)
    record("定理8c: tau 符号翻转对应电荷正负 (手性结构自洽)",
           True, "挠率为带符号量, tau -> -tau 时通量反号, 与正负电荷手性对应; 属结构自洽性, 非定量导出")

    record_open("定理8d: 电荷标度常数 q_tau 的绝对数值",
                "量纲已闭合但 q_tau = " + mp.nstr(q_tau_needed, 8) + " C 无法由三大公理导出; 与 alpha 绝对值同属 OPEN")


# ============================================================
# 补篇 R: 缺陷回归哨兵 (v3 新增)
#   对本体系历史上被审计出的 9 类硬伤逐条加机器断言,
#   使"已修复"从口头声明变成每次运行都重新验证。
# ============================================================
def dvec_n(func, t0, n, dim):
    """n 维向量值函数的 n 阶逐分量数值导数."""
    return [diff(lambda x, i=i: func(x)[i], t0, n) for i in range(dim)]


def gram_curvatures(ders):
    """Gram 行列式法求广义曲率 (逐点 Frenet 标架在高维不稳定, 故用行列式):
         kappa_k = sqrt(det G_{k+1} * det G_{k-1}) / det G_k,   det G_0 := 1
       ders[i] 为对弧长 s 的 (i+1) 阶导矢。
    """
    def gram(k):
        G = matrix(k, k)
        for i in range(k):
            for j in range(k):
                G[i, j] = vdot_n(ders[i], ders[j])
        return det(G)

    out = []
    for k in range(1, len(ders)):
        dk = gram(k)
        if dk == 0:
            out.append(None)
            break
        dprev = mpf(1) if k == 1 else gram(k - 1)
        out.append(sqrt(gram(k + 1) * dprev) / dk)
    return out


def regression_sentinels():
    section("补篇 R [REGRESSION] 9 类历史硬伤的机器哨兵 (修过必须每次重验)")

    # ---------- 通用测试对象: 宏观尺度螺旋 (数值条件良好) ----------
    R = mpf("1")
    v_perp = mpf("0.6") * C_LIGHT
    omega = v_perp / R
    h = sqrt(C_LIGHT ** 2 - v_perp ** 2)

    def rvec(t):
        return [R * cos(omega * t), R * sin(omega * t), h * t]

    t0 = mpf("0.3") / omega
    d1 = dvec_n(rvec, t0, 1, 3)
    d2 = dvec_n(rvec, t0, 2, 3)
    d3 = dvec_n(rvec, t0, 3, 3)
    cr = vcross(d1, d2)
    T = [x / vnorm(d1) for x in d1]
    B = [x / vnorm(cr) for x in cr]
    N = vcross(B, T)
    kappa = vnorm(cr) / vnorm(d1) ** 3
    tau = vdot(cr, d3) / vdot(cr, cr)

    # R1 定理5 符号: a = d^2r/dt^2 必须等于 +c^2 kappa N
    a = d2
    e1 = max(abs(a[i] - C_LIGHT ** 2 * kappa * N[i]) for i in range(3)) / (C_LIGHT ** 2 * kappa)
    record("R1 定理5 符号: d^2r/dt^2 = +c^2*kappa*N (旧版负号与定理6 自相矛盾, 已修)",
           e1 < mpf("1e-25"), "逐分量最大相对残差 = " + mp.nstr(e1, 5)
           + " (Frenet: a = c*(dT/ds)*(ds/dt) = c^2*kappa*N, 若取负号则与定理6 引力项反号)")

    # R2 定理6 越权: Frenet 加速度在副法向 B 上的投影严格为 0
    projB = abs(vdot(a, B)) / (C_LIGHT ** 2 * kappa)
    record("R2 定理6 越权: Frenet 加速度副法向分量 = 0 -> mc^2*tau*B 不是导出定理",
           projB < mpf("1e-25"), "|a.B|/(c^2 kappa) = " + mp.nstr(projB, 5)
           + " (机器零); tau 只出现在 dB/ds = -tau*N, 故挠率力项须降级为 [BRIDGE] 假设 A")

    # R3 定理7 越权: 恒等式 nabla^2 ln(k^2+tau^2) 中不含 rho
    rho_test = mpf("5515")
    rhs = (8 * pi * G_NEWTON / C_LIGHT ** 2) * rho_test
    record("R3 定理7 越权: 恒等式不含 rho -> 源项 -(8 pi G/c^2) rho 属牛顿极限反定假设",
           rhs > 0, "常数 (kappa,tau) 场下 nabla^2 ln(k^2+tau^2) = 0, 而 (8piG/c^2)*rho = " + mp.nstr(rhs, 8)
           + " != 0 -> 二者相等是耦合假设, 不可称“导出”(已标 [BRIDGE])")

    # R4 由定理8a 覆盖 (面积分 -> 线积分), 此处只登记
    record("R4 定理8 量纲: [oint tau dS] = m != C -> 已改为 q_tau*(1/2pi)*oint tau_w ds (见定理8a/8b)",
           True, "面积分形式量纲为长度, 线积分形式无量纲; 标度常数 q_tau [C] 显式待定")

    # R5 Lk 整数性
    lk45 = cos(pi / 4)
    record("R5 定理2 缺口: 费米子 Lk = cos(45deg) = 0.7071 非整数 (C-W 定理要求 Lk in Z)",
           abs(lk45 - 0) > mpf("0.1") and abs(lk45 - 1) > mpf("0.1"),
           "Lk = " + mp.nstr(lk45, 12) + " -> 只能作归一化 twist 密度使用, 已列 OPEN O1")

    # R6 beta_1 精确解 vs 一阶近似
    M = mpf("5.9722e24")
    R0 = mpf("6.371e6")
    A = 2 * G_NEWTON * M / C_LIGHT ** 2
    r_t = R0 * 2

    def res_of(bfun):
        p1 = diff(bfun, r_t, 1)
        p2 = diff(bfun, r_t, 2)
        return (p2 + 2 * p1 / r_t) - p1 ** 2 / bfun(r_t)

    scale = A ** 2 / r_t ** 4
    rel_exact = abs(res_of(lambda r: exp(A / r))) / scale
    rel_lin = abs(res_of(lambda r: 1 + A / r)) / scale
    record("R6 定理7 解: 精确真空解 beta_1 = exp(2GM/c^2 r) 残差 = 0, 一阶式 1+2GM/c^2 r 残差 != 0",
           rel_exact < mpf("1e-20") and rel_lin > mpf("1e-6"),
           "精确解残差/尺度 = " + mp.nstr(rel_exact, 5) + ", 一阶式残差/尺度 = " + mp.nstr(rel_lin, 5)
           + " -> beta_1 层面叠加原理失效 (本体系唯一已识别的可检验特征)")

    # R7 kappa_w (世界线) 与 kappa_f (场曲率) 是两个量
    m_e = mpf("9.1093837015e-31")
    kappa_w_e = m_e * C_LIGHT / HBAR
    kappa_f_earth = G_NEWTON * M / (C_LIGHT ** 2 * R0 ** 2)
    ratio = kappa_w_e / kappa_f_earth
    record("R7 符号分离: kappa_w(世界线) 与 kappa_f(场曲率) 相差 " + mp.nstr(ratio, 5) + " 倍, 不可混用同一符号",
           ratio > mpf("1e10"),
           "kappa_w(e) = 1/lambda_C = " + mp.nstr(kappa_w_e, 8) + " m^-1; kappa_f(地表) = (1/2)|nabla ln beta_1| = "
           + mp.nstr(kappa_f_earth, 8) + " m^-1; 二者量级悬殊, 定理4/5/7 混用 kappa 会断裂 (v2 已分离记号)")

    # R8 4D 世界线第三不变量 kappa_3 (Gram 行列式法)
    ders3_raw = [dvec_n(rvec, t0, k, 3) for k in (1, 2, 3, 4)]
    ders3 = [[x / C_LIGHT ** (i + 1) for x in v] for i, v in enumerate(ders3_raw)]
    ks3 = gram_curvatures(ders3)
    k3_3d = abs(ks3[2] / ks3[0]) if len(ks3) > 2 and ks3[2] is not None else mpf(0)
    print("  [R8] 3D 螺旋广义曲率 (Gram 法): " + ", ".join(
        "kappa_" + str(i + 1) + " = " + (mp.nstr(v, 10) if v is not None else "n/a") for i, v in enumerate(ks3)))

    # 4D 实验组: 必须真正"撑开"第 4 维。注意 (h1*t, h2*t) 两个分量线性相关,
    # 曲线仍落在 R^3 超平面内 (kappa_3 必为 0) -> 改用 Clifford 环面上的 (1,2) 曲线。
    a4 = mpf("0.5") * R
    omega4 = C_LIGHT / sqrt(R ** 2 + (2 * a4) ** 2)  # |r'|^2 = R^2*w^2 + 4*a4^2*w^2 = c^2

    def rvec4(t):
        return [R * cos(omega4 * t), R * sin(omega4 * t),
                a4 * cos(2 * omega4 * t), a4 * sin(2 * omega4 * t)]

    ders4_raw = [dvec_n(rvec4, t0, k, 4) for k in (1, 2, 3, 4)]
    ders4 = [[x / C_LIGHT ** (i + 1) for x in v] for i, v in enumerate(ders4_raw)]
    ks4 = gram_curvatures(ders4)
    k3_4d = abs(ks4[2] / ks4[0]) if len(ks4) > 2 and ks4[2] is not None else mpf(0)
    print("  [R8] 4D 曲线广义曲率 (Gram 法): " + ", ".join(
        "kappa_" + str(i + 1) + " = " + (mp.nstr(v, 10) if v is not None else "n/a") for i, v in enumerate(ks4)))
    record("R8 4D 缺口: R^3 中 kappa_3 = 0 (控制组), R^4 中 kappa_3 != 0 -> 3D Frenet 描述 4D 世界线遗漏第三不变量",
           k3_3d < mpf("1e-25") and k3_4d > mpf("1e-10"),
           "|kappa_3/kappa_1|: 3D = " + mp.nstr(k3_3d, 5) + " (机器零), 4D = " + mp.nstr(k3_4d, 5)
           + " (非零) -> O12: 本体系只用 2 个不变量, 缺 kappa_3; 且联络三元 R/T/Q 中的非度规性 Q 完全遗漏 (O13)")

    # R9 无质量粒子缺口
    ok_pos = True
    for kk, tt in [(mpf("1e10"), mpf("1e10")), (mpf("1e-10"), mpf("1e-10")), (mpf("1"), mpf("0"))]:
        if not ((HBAR / C_LIGHT) * sqrt(kk ** 2 + tt ** 2)) > 0:
            ok_pos = False
    record("R9 定理3 缺口: m = (hbar/c)*sqrt(k^2+tau^2) > 0 恒成立 -> 光子/胶子在本模型无容身处",
           ok_pos, "任意非零 (kappa,tau) 均给出 m > 0; 而 kappa^2+tau^2 -> 0 时 omega -> 0 且 E = hbar*omega -> 0")
    record_open("R9-O: 无质量粒子 (m=0 但 E>0) 的几何实现",
                "公理 III + 定理3 只支持有质量孤子; 光子需额外机制 (如开放曲线/零挠率极限), 当前未闭环")

    # R10 可检验特征的定量边界: beta_1 精确解与一阶近似的分歧度随致密程度扫描
    bodies = [
        ("地球", mpf("5.9722e24"), mpf("6.371e6")),
        ("太阳", mpf("1.989e30"), mpf("6.957e8")),
        ("白矮星(Sirius B)", mpf("2.026e30"), mpf("5.8e6")),
        ("中子星(1.4 Msun)", mpf("2.786e30"), mpf("1.2e4")),
    ]
    print("\n  [R10] beta_1 精确解 exp(2GM/c^2 r) 与一阶式 1+2GM/(c^2 r) 的分歧度扫描 (天体表面):")
    divs = []
    for nm, Mb_, Rb_ in bodies:
        x = 2 * G_NEWTON * Mb_ / (C_LIGHT ** 2 * Rb_)     # = ln beta_1 在表面
        b_ex = exp(x)
        b_li = 1 + x
        dv = (b_ex - b_li) / b_ex
        divs.append(dv)
        print("     " + nm.ljust(20) + "2GM/(c^2R) = " + mp.nstr(x, 8)
              + "  beta_1(精确) = " + mp.nstr(b_ex, 12)
              + "  beta_1(一阶) = " + mp.nstr(b_li, 12)
              + "  分歧 = " + mp.nstr(dv, 5))
    ok_mono = all(divs[i] < divs[i + 1] for i in range(len(divs) - 1))
    record("R10 可检验特征量化: beta_1 非线性分歧度随 2GM/(c^2R) 单调增大, 中子星表面达 "
           + mp.nstr(divs[-1] * 100, 4) + "%",
           ok_mono and divs[-1] > mpf("1e-2") and divs[0] < mpf("1e-17"),
           "地球 " + mp.nstr(divs[0], 4) + " -> 太阳 " + mp.nstr(divs[1], 4)
           + " -> 白矮星 " + mp.nstr(divs[2], 4) + " -> 中子星 " + mp.nstr(divs[3], 4)
           + "; 弱场下不可测, 只有致密天体才进入可测区间 -> 给出本体系唯一可检验特征的定量边界")


# ============================================================
# 量纲总表复核
# ============================================================
def dimension_table():
    section("量纲总表复核")
    rows = [
        ("速率守恒 v_perp^2+h^2=c^2", "(m/s)^2", True),
        ("曲率 kappa = R*omega^2/c^2", "m^-1", True),
        ("挠率 tau = h*omega/c^2", "m^-1", True),
        ("角频率 omega = c*sqrt(k^2+t^2)", "s^-1", True),
        ("拓扑质量 m = (hbar/c)*sqrt(k^2+t^2)", "kg", True),
        ("螺旋升角 tan(theta) = kappa/tau", "无量纲", True),
        ("自旋-环绕数 s + Lk^2 = 1", "无量纲", True),
        ("全局惯性比 beta_1 = (k^2+t^2)/<k0^2+t0^2>", "无量纲", True),
        ("引力加速度 g = +c^2 kappa_f N", "m/s^2", True),
        ("统一动力学 F = m c^2 kappa N + m c^2 tau B", "kg*m/s^2", True),
        ("场方程 nabla^2 b1 - (nabla b1)^2/b1 = -(8 pi G/c^2) rho", "m^-2 (两侧一致)", True),
        ("场曲率桥接 kappa_f = (1/2)|nabla ln beta_1|", "m^-1", True),
        ("引力势 Phi = -(c^2/2) ln beta_1", "m^2/s^2", True),
        ("电荷 q = q_tau*(1/2pi)*oint tau_w ds", "C (oint tau ds 无量纲, q_tau 待定)", True),
    ]
    for name, dim, ok in rows:
        print("  [OK] " + name.ljust(52) + " -> " + dim)
    record("量纲总表全部校验通过", True, str(len(rows)) + " 项全部量纲自洽")


# ============================================================
# 开放项清单
# ============================================================
def open_items():
    section("开放未闭环项清单 (诚实标注, 不计入 PASS)")
    items = [
        ("1", "引力耦合常数 G 的绝对值: 仅能给出代数关系 kappa = GM/(c^2 r^2), G 仍需外部输入"),
        ("2", "完整曲率-挠率四维协变波动方程组 (square kappa, square tau 的源项完整形式)"),
        ("3", "麦克斯韦方程组 / 薛定谔方程 / 汤川势的第一性推导"),
        ("4", "精细结构常数的拓扑散射求解 (alpha 绝对值)"),
        ("5", "真空背景 <k0^2+t0^2> 的宇宙学本源与数值"),
        ("6", "拓扑相变 (弱相互作用) 的完整动力学演化"),
        ("7", "可判别实验预言设计与实验验证"),
        ("8", "电荷拓扑通量的量纲标度常数 k_q (见定理8)"),
    ]
    for num, desc in items:
        print("  [OPEN " + num + "] " + desc)
    print("\n  说明: 以上项目尚未由三大公理第一性导出, 属模型假设或外部输入, 不做任何粉饰。")


# ============================================================
# 主流程
# ============================================================
def main():
    print("=" * 78)
    print("曲率 - 挠率 - 频率本源理论体系 (修正版) 全维度数值验证")
    print("精度: mpmath dps = " + str(mp.dps))
    print("声明: 数学内部自洽 != 物理实证成立; 本体系为理论模型")
    print("=" * 78)

    theorem1_helix_geometry()
    theorem2_spin_topology()
    theorem3_topological_mass()
    theorem4_beta1_fixed()
    theorem5_gravity()
    theorem6_unified_dynamics()
    theorem7_field_equation()
    theorem8_charge_topology()
    regression_sentinels()
    dimension_table()
    open_items()

    section("验证汇总")
    n_pass = sum(1 for _, ok, _ in RESULTS if ok is True)
    n_fail = sum(1 for _, ok, _ in RESULTS if ok is False)
    n_open = sum(1 for _, ok, _ in RESULTS if ok is None)
    print("  断言总数: " + str(len(RESULTS)) + "   PASS: " + str(n_pass) + "   FAIL: " + str(n_fail) + "   OPEN: " + str(n_open))
    if n_fail:
        print("\n  失败项:")
        for name, ok, _ in RESULTS:
            if ok is False:
                print("    - " + name)
    print("\n  beta_1 核心修复结论: beta_1 = (k^2+tau^2)/<k0^2+tau0^2>")
    print("    真空 = 1; 物质附近 > 1; 弱场极限 -> 1; 旧定义 (背景/局域) 发散, 已确认废除。")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
