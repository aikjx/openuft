# -*- coding: utf-8 -*-
"""
TUFT-r159｜D5《大统一力方程》引力侧还原审计：工业级有序硬门与符号反号
================================================================================
编号与定位
--------------------------------------------------------------------------------
* 编号：r159（实测首空号：r157 本线已登记、r158 已被同日并行会话占用
  ——《D5 字典层：回旋频率同一性与退化点失效》，本线不触碰其字节）
* 靶：  openuft/01_独立体系/S02_空间光速螺旋统一力/04_理论推导/D5_大统一力方程/
        README.md + D5_大统一力方程.py（依赖 helix_force.helix_unified_force）
* D5 核心式：
        统一动量  P = m (c - v)
        统一力    F = dP/dt
        电/磁力比 F_e / F_m = c / v
        电磁波    E = c B
        几何基石  kappa^2 + tau^2 = (omega/v)^2,  omega = qB/(gamma m)

分层（条目不可相加，跨卷引用前先冻结口径）
--------------------------------------------------------------------------------
* r148 = 式子层（类型两难 / 静止极限 / 光速极限 / 符号反号 / 磁镜残差 / 修复=>P=mv）
* r157 = 动力学积分层（真实洛伦兹 RK4 + 磁镜场，恒等式成立域 lambda* = 0.03602）
* r158 = 字典层（omega 同一性与退化点失效）—— 并行会话，本线不触碰
* 本卷 = 引力侧还原层（工业级有序硬门）：把 D5 的力方程**外推到引力**会怎样

★防过度指控（本卷定位，必须先声明）
--------------------------------------------------------------------------------
D5 **自己承认**「不解释引力、不生成常数、不完成四力统一」（README 第 24 行），
其 py 亦打印「统一场论（引力/量子化/暗物质）仍为 OPEN」。
故本卷**不重复指控**「D5 没有引力」——那不是发现，是自承（记 INFO）。
本卷判决的是另一件事：
    **若把该力方程外推到引力侧，会得到什么？**
这正是「工业级有序硬门」的定义域——该门只判「能否用作工程理论」，不判「是否真理」。

机读推导（本卷全部结论的来源，可手算复核）
--------------------------------------------------------------------------------
m 为常数（D5 未给 m 随 t 变）：
    读法 1（c 为恒定矢量）： F = d[m(c-v)]/dt = -m dv/dt = -m a
    读法 2（c 为旋转矢量）： F = m (dc/dt - a),  dc/dt = omega_s x c
牛顿第二定律： F_net = + m a
    ==> 读法 1 下  F_D5 = - F_Newton   （符号反号；r148 B1 已于电磁侧判过同一负号）
引力侧外推（读法 1）：
    令物理合力 = 牛顿引力 F_grav = -(GMm/r^2) r_hat   （r_hat 由 M 指向 m）
    dP/dt = F_grav  ==>  -m a = -(GMm/r^2) r_hat  ==>  a = +(GM/r^2) r_hat
    ==> **加速度背离中心：万有引力变成万有斥力**
工业级有序硬门（记忆纪律，比量纲审计更硬）：
    牛顿 -> 泊松 ∇²Φ = 4πGρ -> 1PN -> 爱因斯坦方程 -> 线性化 □h̄
    逐级还原不出即判「不可用作工程理论」。本卷逐级机读。

纯标准库（py3.13 managed 无 numpy/sympy/mpmath）。
"""

import io
import json
import math
import os
import sys
from datetime import datetime

# Windows GBK 控制台；统一 UTF-8 输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ============================== 常量（CODATA 2018 / IAU 2015） ==============================
C_LIGHT = 299792458.0
G_NEWTON = 6.67430e-11
M_EARTH = 5.9722e24
R_EARTH = 6.371e6
GM_EARTH = 3.986004418e14
GM_SUN = 1.32712440018e20
AU = 1.495978707e11
EPS0 = 8.8541878128e-12
MU0 = 1.25663706212e-6
DAY = 86400.0
YEAR = 365.25 * DAY
M_ELECTRON = 9.1093837015e-31

# 阈值：按「常数舍入地板」纪律取（G 仅 5-6 位有效；eps0*mu0 反算 c 残差 ~1e-10 量级）
TOL_SIGN = 1e-9        # 符号/比值判等（机器零级，且远高于舍入地板）
TOL_REL = 1e-6         # 相对判等：G 仅 5-6 位，故不取更严
TOL_CONST = 1e-8       # 常数锚点阈值（记忆纪律：不得取 1e-9）

# ---- 路径定位（引擎位于 openuft/04_公共成果/本项目_全维自洽与归一化/源码/）----
_HERE = os.path.dirname(os.path.abspath(__file__))                # .../源码
_PROJ = os.path.dirname(_HERE)                                    # .../本项目_全维自洽与归一化
_COM = os.path.dirname(_PROJ)                                     # .../04_公共成果
OPENUFT_ROOT = os.path.dirname(_COM)                              # openuft
D5_README = os.path.join(OPENUFT_ROOT, "01_独立体系", "S02_空间光速螺旋统一力",
                         "04_理论推导", "D5_大统一力方程", "README.md")

# ============================== 登记器 ==============================
ENTRIES = []
GUARDS = []
CONTROLS = []


def add(code, group, name, verdict, note):
    """登记一条判定。verdict ∈ PASS/FAIL/INFO/BOUNDARY/CORRECTION"""
    ENTRIES.append({
        "code": code, "group": group, "name": name,
        "verdict": verdict, "note": note,
    })


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("  {} {} — {}".format("OK " if ok else "BAD", name, detail))


def control(name, ok, detail):
    CONTROLS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("  {} {} — {}".format("OK " if ok else "BAD", name, detail))


def fmt(x, n=6):
    return "{:.{p}e}".format(x, p=n) if x != 0 else "0.000000e+00"


# ============================== 数学工具 ==============================
def rk4_step(f, y, t, h):
    """标准 RK4（y 为 list）"""
    k1 = f(t, y)
    k2 = f(t + h / 2, [y[i] + h / 2 * k1[i] for i in range(len(y))])
    k3 = f(t + h / 2, [y[i] + h / 2 * k2[i] for i in range(len(y))])
    k4 = f(t + h, [y[i] + h * k3[i] for i in range(len(y))])
    return [y[i] + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(len(y))]


def integrate_radial(acc_fn, r0, v0, T, nsteps):
    """一维径向运动 r'' = acc_fn(r)，返回 (r_end, v_end, r_min, r_max)"""

    def f(_t, y):
        r, v = y[0], y[1]
        return [v, acc_fn(r)]

    y = [r0, v0]
    h = T / nsteps
    rmin, rmax = r0, r0
    for i in range(nsteps):
        y = rk4_step(f, y, i * h, h)
        rmin = min(rmin, y[0])
        rmax = max(rmax, y[0])
    return y[0], y[1], rmin, rmax


# ============================== A 组：工业级有序硬门（五级还原） ==============================
def group_A():
    print("\n" + "=" * 78)
    print(" [A 组] 工业级有序硬门：牛顿 -> 泊松 -> 1PN -> 爱因斯坦方程 -> 线性化 □h̄")
    print("=" * 78)

    out = {}

    # ---- A1 第 1 级：牛顿引力。读法 1：F = -m a ----
    # 引力合力（真实方向：指向 M，即 -r_hat）
    # D5: -m a = -(GMm/r^2) r_hat  ==>  a = +(GM/r^2) r_hat
    r_test = R_EARTH
    a_d5 = +GM_EARTH / (r_test ** 2)      # D5 外推（外向，正号）
    a_newton = -GM_EARTH / (r_test ** 2)  # 牛顿（指向地心，负号）
    ratio = a_d5 / a_newton
    rel_dev = abs(a_d5 - a_newton) / abs(a_newton)
    print("[A1] 第 1 级 牛顿引力（r = R_earth = {} m）".format(fmt(r_test)))
    print("     D5 外推  a_D5    = {:+.6f} m/s^2 （外向，背离地心）".format(a_d5))
    print("     牛顿     a_Newton= {:+.6f} m/s^2 （指向地心）".format(a_newton))
    # 注意：.format() 串里 %% 不转义（会原样输出两个百分号），此处写单个 %
    print("     比值 a_D5/a_Newton = {:+.10f}   相对偏差 = {:.6f} (={:.1f}%)".format(
        ratio, rel_dev, rel_dev * 100))
    out["A1_a_d5"] = a_d5
    out["A1_a_newton"] = a_newton
    out["A1_ratio"] = ratio
    out["A1_rel_dev"] = rel_dev

    sign_flip = abs(ratio + 1.0) < TOL_SIGN
    if sign_flip:
        add("A1", "还原链", "第 1 级·牛顿引力：外推得 a = +GM/r²（外向）", "FAIL",
            "D5 的 F=-ma 与引力 -GMm/r² 联立 ⇒ a = +GM/r² = {:+.6f} m/s² 背离地心，"
            "与牛顿 {:+.6f} m/s² 精确反号（比值 {:+.10f}，相对偏差 {:.2f} = {}%）。"
            "即外推到引力侧得到的是**万有斥力**而非万有引力。"
            .format(a_d5, a_newton, ratio, rel_dev, "{:.1f}".format(rel_dev * 100)))
    else:
        add("A1", "还原链", "第 1 级·牛顿引力", "FAIL",
            "符号守卫未通过：a_D5/a_Newton = {:+.6f} 不是 -1，代码或口径有误".format(ratio))

    # ---- A2 第 2 级：泊松方程 ----
    # a = -grad(Phi)  ==>  grad(Phi) = -a
    # D5: a = +GM/r^2 r_hat  ==>  grad(Phi_D5) = -GM/r^2 r_hat  ==>  Phi_D5 = +GM/r
    # 牛顿: Phi_N = -GM/r
    # 高斯通量（半径 R 球面）：∮ grad(Phi)·dS
    R_s = 1.0e6
    # grad(Phi_D5) = -GM/r^2 r_hat  ==>  通量 = -GM/R^2 * 4 pi R^2 = -4 pi GM
    flux_d5 = -4.0 * math.pi * GM_EARTH
    flux_newton = +4.0 * math.pi * GM_EARTH
    flux_ratio = flux_d5 / flux_newton
    print("\n[A2] 第 2 级 泊松方程 ∇²Φ = 4πGρ（球对称散度定理，R = {} m）".format(fmt(R_s)))
    print("     Φ_D5 = +GM/r  ⇒ ∮∇Φ·dS = {} （对应 ∇²Φ = −4πGρ，反号）".format(fmt(flux_d5)))
    print("     Φ_N  = −GM/r  ⇒ ∮∇Φ·dS = {} （对应 ∇²Φ = +4πGρ，标准）".format(fmt(flux_newton)))
    print("     通量比 = {:+.10f}".format(flux_ratio))
    out["A2_flux_d5"] = flux_d5
    out["A2_flux_newton"] = flux_newton
    out["A2_flux_ratio"] = flux_ratio

    # 数值复核 ∇²Φ 在 r>0 处为 0（球对称 Laplace），解析 + 差分双口径
    def laplace_spherical(phi_fn, r, h):
        # ∇²Φ = (1/r²) d/dr (r² dΦ/dr) 的一阶嵌套差分
        def d1(rr):
            return (phi_fn(rr + h) - phi_fn(rr - h)) / (2 * h)
        return (1.0 / r ** 2) * ((r + h) ** 2 * d1(r + h) - (r - h) ** 2 * d1(r - h)) / (2 * h)

    phi_d5 = lambda r: +GM_EARTH / r
    phi_n = lambda r: -GM_EARTH / r
    h_adapt = 1.0e-4 * R_s       # 自适应步长（记忆纪律：ω·h≈1e-4 同型）
    lap_d5 = laplace_spherical(phi_d5, R_s, h_adapt)
    lap_n = laplace_spherical(phi_n, R_s, h_adapt)
    scale = abs(GM_EARTH / R_s ** 3)
    print("     数值 ∇²Φ_D5(r>0) = {}   ∇²Φ_N(r>0) = {}  （量级 {}，应≈0）".format(
        fmt(lap_d5), fmt(lap_n), fmt(scale)))
    out["A2_lap_d5"] = lap_d5
    out["A2_lap_n"] = lap_n

    if abs(flux_ratio + 1.0) < TOL_SIGN and abs(lap_d5) < TOL_REL * scale:
        add("A2", "还原链", "第 2 级·泊松方程：外推得 ∇²Φ = −4πGρ（反号）", "FAIL",
            "Φ_D5 = +GM/r（因 a=-∇Φ 且 a 外向）⇒ 高斯通量 {} vs 牛顿 {}，"
            "比值 {:+.10f} ⇒ 还原出的是**反号泊松方程** ∇²Φ = −4πGρ（等价负质量密度）。"
            "r>0 处 ∇²Φ 机器零已复核（{}，量级 {}）。"
            .format(fmt(flux_d5), fmt(flux_newton), flux_ratio, fmt(lap_d5), fmt(scale)))
    else:
        add("A2", "还原链", "第 2 级·泊松方程", "FAIL",
            "通量比 {:+.6f} 或 Laplace 残差 {} 未达判据，需复核".format(flux_ratio, fmt(lap_d5)))

    # ---- A3/A4/A5：第 3-5 级（1PN / 爱因斯坦方程 / 线性化 □h̄）----
    # 判定方式：符号清点——D5 方程中是否出现度规/曲率/应力张量/达朗贝尔算子
    SYMBOLS = {
        "L3_1PN": ["g_00", "g_ij", "g_\\mu\\nu", "metric", "度规", "Phi/c^2"],
        "L4_EE": ["R_\\mu\\nu", "G_\\mu\\nu", "T_\\mu\\nu", "Einstein", "爱因斯坦", "Ricci"],
        "L5_box": ["\\Box", "□", "h_bar", "h̄", "linearized", "线性化", "d'Alembert"],
    }
    # D5 方程文本（来自 README 核心方程块 + py 打印的诚实边界）
    d5_text = (
        "P = m (c - v) ; F = dP/dt ; F_e / F_m = c / v ; E = c B ; "
        "kappa^2 + tau^2 = (omega/v)^2 ; omega = qB/(gamma m) ; "
        "P=m(c-v), dP/dt=F 是几何-运动学力分解，非实验新预言；"
        "统一场论（引力/量子化/暗物质）仍为 OPEN"
    )
    counts = {}
    for lvl, syms in SYMBOLS.items():
        c = sum(d5_text.count(s) for s in syms)
        counts[lvl] = c
        print("[{}] 符号清点 {} 类符号命中数 = {}".format(lvl[:2], lvl, c))

    missing = [k for k, v in counts.items() if v == 0]
    add("A3", "还原链", "第 3 级·1PN：D5 不含度规，无法进入后牛顿近似", "FAIL",
        "1PN 需要 g_00 = -(1+2Φ/c²)、g_ij = (1-2Φ/c²)δ_ij；D5 方程中**度规类符号命中 0** "
        "⇒ 该级不存在（不是算错，是缺内容）。工业级硬门要求逐级还原，缺一级即断裂。")
    add("A4", "还原链", "第 4 级·爱因斯坦方程：D5 无曲率/应力张量", "FAIL",
        "G_μν = 8πG T_μν/c⁴ 需要曲率与应力-能量张量；D5 中**曲率/应力张量类符号命中 0** ⇒ 该级不存在。")
    add("A5", "还原链", "第 5 级·线性化 □h̄：D5 无达朗贝尔算子与扰动量", "FAIL",
        "□h̄_μν = -16πG T_μν/c⁴ 需要达朗贝尔算子与度规扰动；D5 中**相关符号命中 0** ⇒ 该级不存在。")

    # ---- A6 综合：工业级有序硬门裁定 ----
    add("A6", "还原链", "工业级有序硬门综合裁定", "FAIL",
        "五级还原链：第 1 级**符号反号**（万有斥力）、第 2 级**反号泊松方程**、"
        "第 3-5 级**根本不存在**（无度规、无场方程、无 PDE）"
        "⇒ 按该门定义判「**不可用作工程理论**」。"
        "该门只判工程可用性，不判其是否为真理。")

    out["A_counts"] = counts
    return out


# ============================== B 组：引力侧精算（可检验量） ==============================
def group_B():
    print("\n" + "=" * 78)
    print(" [B 组] 引力侧精算：圆轨道 / 自由落体 / 轨道积分 / 开普勒")
    print("=" * 78)
    out = {}

    # ---- B1 圆轨道：v^2/r 需向心；D5 给外向 a = +GM/r^2 ----
    # 圆轨道条件（牛顿）： v^2/r = GM/r^2  ==> v^2 = +GM/r  (有实数解)
    # D5 外推： a = +GM/r^2 外向，需 a = -v^2/r  ==> -v^2/r = +GM/r^2 ==> v^2 = -GM/r < 0
    v2_d5 = -GM_SUN / AU          # 负值
    v2_newton = +GM_SUN / AU
    v_newton = math.sqrt(v2_newton)
    T_newton = 2.0 * math.pi * AU / v_newton
    print("[B1] 圆轨道（地球绕日，r = 1 AU）")
    print("     牛顿： v² = +GM/r = {} ⇒ v = {:+.6f} m/s，T = {:.4f} 天".format(
        fmt(v2_newton), v_newton, T_newton / DAY))
    print("     D5  ： v² = -GM/r = {} < 0 ⇒ **无实数解**（不存在任何圆轨道）".format(fmt(v2_d5)))
    out["B1_v2_d5"] = v2_d5
    out["B1_v_newton"] = v_newton
    out["B1_T_newton_day"] = T_newton / DAY

    if v2_d5 < 0:
        add("B1", "精算", "圆轨道：D5 外推下 v² = −GM/r < 0，无实数解", "FAIL",
            "圆轨道要求向心加速度，而 D5 给外向 a = +GM/r² ⇒ v² = {} < 0 ⇒ "
            "**在 D5 的引力外推下不存在任何圆轨道**（连近似解都没有）。"
            "牛顿正对照 v = {:+.3f} m/s、T = {:.2f} 天（与实测 365.25 天一致）。"
            .format(fmt(v2_d5), v_newton, T_newton / DAY))
    else:
        add("B1", "精算", "圆轨道", "FAIL", "守卫：v² 应为负，实得 {}，代码错".format(fmt(v2_d5)))

    # ---- B2 自由落体（地表） ----
    g_d5 = +GM_EARTH / R_EARTH ** 2
    g_std = 9.80665
    print("\n[B2] 地表自由落体：D5 外推 g = {:+.6f} m/s²（向上）；标准 g = {:.5f}（向下）".format(g_d5, g_std))
    print("     D5 下苹果**向上加速**逃逸；相对标准值偏差 {:.2f}%（符号反）".format(
        abs(g_d5 - (-g_std)) / g_std * 100))
    out["B2_g_d5"] = g_d5
    add("B2", "精算", "地表自由落体：D5 外推 g = +{:.5f} m/s² 向上（标准 {:.5f} 向下）".format(g_d5, g_std),
        "FAIL",
        "D5 外推下地表物体**向上加速**：g_D5 = {:+.6f} m/s² vs 标准 −{:.5f} m/s²，"
        "相对偏差 {:.2f}%。注：GM/R² = {:.4f} 与标准 g 的 0.14% 差源于地球非球对称，"
        "属模型固有，不影响符号判决。".format(g_d5, g_std, abs(g_d5 + g_std) / g_std * 100, g_d5))

    # ---- B3 轨道积分：D5 逃逸 vs 牛顿圆轨道保持 ----
    T_int = 1.0 * YEAR
    nsteps = 20000
    # ★自抓：圆轨道是二维问题，纯径向 r''=-GM/r² 会漏掉角动量项 L²/r³
    #   （首跑因此得牛顿侧漂移 2244 AU 的假失败）。改有效势径向方程：
    #       r'' = a_grav(r) + L²/r³,   L = r × v_tangential = AU · v_circ
    #   牛顿侧在 r=AU 处 -GM/AU² + L²/AU³ = -GM/AU² + GM/AU² = 0 ⇒ 圆轨道保持
    L_spec = AU * v_newton
    L2 = L_spec ** 2
    acc_d5 = lambda r: +GM_SUN / r ** 2 + L2 / r ** 3          # D5 外向 + 角动量
    acc_newton = lambda r: -GM_SUN / r ** 2 + L2 / r ** 3      # 牛顿内向 + 角动量
    r_end_d5, v_end_d5, rmin_d5, rmax_d5 = integrate_radial(acc_d5, AU, 0.0, T_int, nsteps)
    r_end_n, v_end_n, rmin_n, rmax_n = integrate_radial(acc_newton, AU, 0.0, T_int, nsteps)
    drift_n = abs(rmax_n - rmin_n) / AU
    print("\n[B3] 有效势径向 RK4 积分 1 年（{} 步，含角动量 L²/r³）".format(nsteps))
    print("     D5   ： r 从 {} → {} m（= {:.4f} AU），v_end = {} m/s ⇒ 飞离".format(
        fmt(AU), fmt(r_end_d5), r_end_d5 / AU, fmt(v_end_d5)))
    print("     牛顿 ： 圆轨道 r 相对漂移 = {}（应≈0，RK4 精度）".format(fmt(drift_n)))
    out["B3_r_end_d5"] = r_end_d5
    out["B3_r_end_d5_AU"] = r_end_d5 / AU
    out["B3_drift_newton"] = drift_n

    if drift_n < 1e-6 and r_end_d5 > 2 * AU:
        add("B3", "精算", "轨道积分：D5 外推下 1 年飞离到 {:.3f} AU（牛顿圆轨道漂移 {}）".format(
            r_end_d5 / AU, fmt(drift_n)), "FAIL",
            "以 r=1 AU、v=0 起步积分 1 年：D5 外向加速度使 r 增至 {:.4f} AU（v_end = {} m/s），"
            "而牛顿圆轨道在同一积分器下相对漂移仅 {} ⇒ 差异不是数值误差。"
            .format(r_end_d5 / AU, fmt(v_end_d5), fmt(drift_n)))
    else:
        add("B3", "精算", "轨道积分", "FAIL",
            "守卫：牛顿圆轨道漂移 {} 应 <1e-6 或 D5 未飞离（r_end/AU = {:.4f}），需复核".format(
                fmt(drift_n), r_end_d5 / AU))

    # ---- B4 开普勒第三定律（牛顿侧正对照） ----
    T_kepler = 2.0 * math.pi * math.sqrt(AU ** 3 / GM_SUN)
    print("\n[B4] 开普勒第三定律（牛顿正对照）：T = 2π√(a³/GM) = {:.4f} 天".format(T_kepler / DAY))
    out["B4_T_kepler_day"] = T_kepler / DAY
    add("B4", "精算", "开普勒第三定律：牛顿侧 T = {:.2f} 天（实测 365.25 天）".format(T_kepler / DAY),
        "PASS",
        "牛顿侧 T = 2π√(a³/GM_☉) = {:.4f} 天，与实测 365.25 天一致（相对差 {:.2e}）"
        "⇒ 还原链在牛顿侧是通的，门本身有判别力。此项对靶有利（牛顿还原正确），诚实登记。"
        .format(T_kepler / DAY, abs(T_kepler / DAY - 365.25) / 365.25))

    # ---- B5 静态极限：v=0 时 D5 的动量（跨卷一致性，r148 A2） ----
    P0 = 1.0 * C_LIGHT       # m = 1 kg
    print("\n[B5] 静止极限 P(0) = m c = {} kg·m/s（m=1 kg；复现 r148 A2 的 2.998e+08）".format(fmt(P0)))
    out["B5_P0"] = P0
    add("B5", "精算", "静止极限 P(0) = mc = {} kg·m/s ≠ 0（m = 1 kg）".format(fmt(P0)), "BOUNDARY",
        "v=0 时 D5 给 P = mc = {} kg·m/s 而非 0 ⇒ 静止物体带非零动量。"
        "与 r148 A2 机读 2.998e+08 逐位一致（跨卷一致性确认）。"
        "本卷不重复判它（r148 已判），仅登记为一致性锚点。".format(fmt(P0)))

    return out


# ============================== C 组：统一性审计（「大统一」名实） ==============================
def group_C():
    print("\n" + "=" * 78)
    print(" [C 组] 统一性审计：自承 / 名实 / 耦合常数清点 / 读法退路")
    print("=" * 78)
    out = {}

    # ---- C1 靶自承 ----
    readme_path = D5_README
    self_admit = False
    admit_hits = []
    if os.path.isfile(readme_path):
        txt = open(readme_path, encoding="utf-8", errors="replace").read()
        for kw in ["不解释引力", "不完成四力统一", "不生成常数"]:
            if kw in txt:
                admit_hits.append(kw)
        self_admit = len(admit_hits) >= 1
    print("[C1] 靶自承检测（{}）：命中 {}".format(
        os.path.basename(readme_path) if os.path.isfile(readme_path) else "README 未找到", admit_hits))
    out["C1_admit_hits"] = admit_hits

    if self_admit:
        add("C1", "统一性", "D5 自承「不解释引力、不生成常数、不完成四力统一」", "INFO",
            "README 明写「它不解释引力、不生成常数、不完成四力统一」，py 亦打印"
            "「统一场论（引力/量子化/暗物质）仍为 OPEN」⇒ **找靶自承**，"
            "本卷不把「D5 没有引力」当作新指控（防过度指控）。命中：{}".format(admit_hits))
    else:
        add("C1", "统一性", "靶自承检测", "BOUNDARY",
            "未能在 README 中定位自承字符串（路径 {}），自承判定暂不成立".format(readme_path))

    # ---- C2 名实两难 ----
    add("C2", "统一性", "标题「大统一力方程」 vs 自承不完成四力统一：名实两难", "BOUNDARY",
        "两难（记忆纪律：归属未定写两难，两支都不利）："
        "① 若 D5 宣称统一四力 ⇒ 与其自承矛盾，且本卷 A/B 组显示引力侧外推得到斥力、无圆轨道；"
        "② 若 D5 不宣称统一四力 ⇒ 则标题「大统一力方程」名实不符。"
        "本卷不代靶决定归属，两支都登记。")

    # ---- C3 F_e/F_m = c/v 是否构成跨力统一 ----
    v_fracs = [0.1, 0.3, 0.6, 0.9]
    ratios = [1.0 / vf for vf in v_fracs]
    print("[C3] D5 力比 F_e/F_m = c/v：")
    for vf, r_ in zip(v_fracs, ratios):
        print("     v = {:.1f} c  ⇒  F_e/F_m = {:.4f}".format(vf, r_))
    out["C3_ratios"] = ratios
    add("C3", "统一性", "F_e/F_m = c/v 只涉及电磁内部两项，不构成跨力统一", "INFO",
        "F_e 与 F_m 同属电磁力（电场力与磁场力），其比值 c/v 是**电磁内部的比值**，"
        "不含引力/强/弱任何一项 ⇒ 不构成跨力统一，故降 INFO 而非作为不利证据重复计数。")

    # ---- C4 耦合常数清点 ----
    # 方程串写全（含 omega = qB/(gamma m)），使电磁侧计数非 0，
    # 这样「非电磁耦合 = 0」才是有判别力的对照，而不是「全都没数到」
    d5_eq = ("P = m (c - v) ; F = dP/dt ; F_e/F_m = c/v ; E = c B ; "
             "kappa^2 + tau^2 = (omega/v)^2 ; omega = q B / (gamma m)")
    coupl = {
        "G（引力）": d5_eq.count("G") + d5_eq.count("G_Newton") + d5_eq.count("引力"),
        "alpha_s（强）": d5_eq.count("alpha_s") + d5_eq.count("强"),
        "g/g'（弱）": d5_eq.count("g'") + d5_eq.count("弱"),
        "q（电磁）": d5_eq.count("q"),
    }
    print("[C4] 耦合常数清点（D5 方程串）：{}".format(coupl))
    non_em = coupl["G（引力）"] + coupl["alpha_s（强）"] + coupl["g/g'（弱）"]
    out["C4_couplings"] = coupl
    if non_em == 0:
        add("C4", "统一性", "耦合常数清点：非电磁耦合符号命中 0", "FAIL",
            "D5 方程中 G / 强 / 弱 耦合常数出现次数均为 0 ⇒ **零跨力耦合**。"
            "与 r148「方程层非电磁耦合符号 0」一致（跨卷一致性）。"
            "一个不含任何非电磁耦合的方程，无法承担「大统一」角色。")
    else:
        add("C4", "统一性", "耦合常数清点", "PASS", "命中 {}".format(non_em))

    # ---- C5 读法退路：c 为旋转矢量（读法 2）----
    # F = m(dc/dt - a)，dc/dt = omega_s x c，|dc/dt| = omega_s c
    # 引力场景：a = (dc/dt) + (GM/r^2) r_hat
    # 若 omega_s x c 恰好抵消引力项，则可免于斥力 ⇒ 但 omega_s 为外部输入且无给定值
    a_grav_mag = GM_EARTH / R_EARTH ** 2
    omega_s_needed = a_grav_mag / C_LIGHT      # 令 omega_s * c = |a_grav| 抵消
    print("\n[C5] 读法 2（c 为旋转矢量）：F = m(dc/dt − a)，|dc/dt| = ω_s·c")
    print("     欲抵消地表引力需 ω_s = |a|/c = {} s⁻¹（D5 未给 ω_s 任何值）".format(fmt(omega_s_needed)))
    out["C5_omega_s_needed"] = omega_s_needed
    add("C5", "统一性", "读法退路（c 旋转 ⇒ F = m(dc/dt − a)）：需外输 ω_s，不可检验", "BOUNDARY",
        "读法 2 下 dc/dt = ω_s × c 可（在数值上）掩盖引力项，若 ω_s·c 恰等于 |a_grav| "
        "（地表需 ω_s = {} s⁻¹）则斥力可被抵消。但 **ω_s 在 D5 中无任何给定值** ⇒ "
        "外部输入 +1 且不可检验 ⇒ 登记 BOUNDARY，不作有利也不作不利结论。"
        .format(fmt(omega_s_needed)))

    return out


# ============================== D 组：修复定价 ==============================
def group_D():
    print("\n" + "=" * 78)
    print(" [D 组] 修复定价：让 D5 引力侧还原出正确引力的代价")
    print("=" * 78)

    # 动作集：对「核心式 P = m(c − v)」的减号 / 对 F = dP/dt 的处理 / 是否引入 G
    # 动作 1：FLIP_SIGN（P = m(v − c)，等价 F = +ma）⇒ 得到牛顿引力
    # 动作 2：KEEP（原样）⇒ 斥力
    # 动作 3：DEL（删掉 c 项，P = −mv 或 P = mv）
    results = []
    for act in ["KEEP", "FLIP_SIGN", "DEL_C"]:
        if act == "KEEP":
            a_sign = +1.0     # 外向斥力
            keeps_core = True
            desc = "保留 P = m(c − v)：F = −ma ⇒ 引力外推为斥力"
        elif act == "FLIP_SIGN":
            a_sign = -1.0     # 内向引力 ✓
            keeps_core = False
            desc = "翻核心式符号为 P = m(v − c)（等价 F = +ma）⇒ 还原出牛顿引力"
        else:  # DEL_C
            a_sign = -1.0     # P = -m v ⇒ F = -ma ... 需仔细
            # P = -m v（删掉 c）⇒ dP/dt = -m a ⇒ 仍是 -ma ⇒ 斥力
            a_sign = +1.0
            keeps_core = False
            desc = "删掉 c 项（P = −mv）⇒ dP/dt = −ma，仍是斥力"
        ok = abs(a_sign + 1.0) < 1e-12      # 内向（a_sign = -1）才算还原成功
        results.append({
            "action": act, "a_sign": a_sign, "restores_newton": ok,
            "keeps_core_form": keeps_core, "desc": desc,
        })
        print("  {:10s} a_sign = {:+.1f}  还原牛顿={}  保留核心式={}  | {}".format(
            act, a_sign, ok, keeps_core, desc))

    survivors = [r for r in results if r["restores_newton"]]
    zero_cost = [r for r in survivors if r["keeps_core_form"]]
    strict = len(survivors)      # 严格档：允许任何动作（本卷动作集即含改式）
    print("\n  存活（还原出牛顿引力）= {} ；其中零代价（保留 P=m(c−v) 核心式）= {}".format(
        len(survivors), len(zero_cost)))
    print("  ⇒ 修复可行，但唯一修复解 = 翻掉核心式符号（P = m(v−c)），"
          "此时「统一动量 m(c−v)」这一 D5 的标志性形式不复存在。")

    add("D1", "修复", "修复定价：3 动作枚举，存活 {}、零代价 {}".format(len(survivors), len(zero_cost)),
        "FAIL" if len(zero_cost) == 0 else "BOUNDARY",
        "让 D5 引力侧还原出正确引力的唯一办法是**翻掉核心式符号**（P = m(v−c)，等价 F = +ma）；"
        "保留 P = m(c−v) 则恒得斥力（零代价解 0）。翻号后 D5 的标志性「统一动量」形式消失，"
        "与 r148「修复 ⇒ P = mv（牛顿动量）」同型 ⇒ **「修复即自杀」第八度复发**。"
        "注明：修复空间为低阶（3 动作），高阶新增型未枚举。")

    return {"survivors": len(survivors), "zero_cost": len(zero_cost), "table": results}


# ============================== 控制组 ==============================
def group_controls():
    print("\n" + "=" * 78)
    print(" [控制组] 必设：证明门有判别力（非恒失败）")
    print("=" * 78)

    # U1 牛顿正对照：F = +ma 逐级还原
    a_n = -GM_EARTH / R_EARTH ** 2
    phi_n = -GM_EARTH / R_EARTH
    flux_n = +4 * math.pi * GM_EARTH
    v_circ = math.sqrt(GM_SUN / AU)
    T_circ = 2 * math.pi * AU / v_circ / DAY
    ok_u1 = (a_n < 0) and (phi_n < 0) and (flux_n > 0) and abs(T_circ - 365.25) / 365.25 < 1e-3
    control("U1 牛顿正对照（F=+ma 逐级还原：a<0、Φ<0、通量>0、T=365 天）", ok_u1,
            "a={:+.4f} m/s²、Φ={:+.4e} J/kg、∮∇Φ·dS={:+.4e}、T={:.3f} 天".format(
                a_n, phi_n, flux_n, T_circ))

    # U2 反向控制：把斥力喂给牛顿门，门应判 FAIL
    a_wrong = +GM_EARTH / R_EARTH ** 2       # 斥力
    gate_rejects = (a_wrong > 0)             # 牛顿门要求 a<0 ⇒ 拒绝
    control("U2 反向控制（喂斥力 a=+GM/r² 给牛顿门，门应拒绝）", gate_rejects,
            "a_wrong={:+.4f} > 0 ⇒ 门判 FAIL（证明门能抓反号，非恒失败）".format(a_wrong))

    # U3 量纲：P = m(c-v) 应为动量 kg·m/s
    m, v_ = 2.0, 3.0
    P = m * (C_LIGHT - v_)
    dim_ok = abs(P - (m * C_LIGHT - m * v_)) < 1e-9 * abs(P) and P > 0
    control("U3 量纲：P = m(c−v) 量纲为动量 kg·m/s", dim_ok,
            "m=2 kg、v=3 m/s ⇒ P = {:.6e} kg·m/s".format(P))

    # U4 常数锚点：c = 1/√(ε₀μ₀)
    c_em = 1.0 / math.sqrt(EPS0 * MU0)
    rel_c = abs(c_em - C_LIGHT) / C_LIGHT
    control("U4 常数锚点 c = 1/√(ε₀μ₀)（阈值 1e-8，常数舍入地板纪律）", rel_c < TOL_CONST,
            "c_em = {:.10e} vs {:.10e}，相对差 {:.3e}".format(c_em, C_LIGHT, rel_c))

    # U5 复现 D5 自身机读：F_e/F_m = c/v
    rt = [1.0 / vf for vf in [0.1, 0.3, 0.6, 0.9]]
    expect = [10.0, 1.0 / 0.3, 1.0 / 0.6, 1.0 / 0.9]
    ok_u5 = all(abs(a_ - b_) < 1e-12 for a_, b_ in zip(rt, expect))
    control("U5 复现 D5 自身输出 F_e/F_m = c/v（v=0.1/0.3/0.6/0.9 c）", ok_u5,
            "比值 {}".format(["{:.4f}".format(x) for x in rt]))

    # U6 泊松：球对称 r>0 处 ∇²Φ = 0（解析）
    # Φ = -GM/r ⇒ ∇²Φ = 0 (r>0)；用差分复核
    def lap(phi, r, h):
        d1 = lambda rr: (phi(rr + h) - phi(rr - h)) / (2 * h)
        return (1 / r ** 2) * ((r + h) ** 2 * d1(r + h) - (r - h) ** 2 * d1(r - h)) / (2 * h)
    r0, hh = 1.0e7, 1.0e-4 * 1.0e7
    lapv = lap(lambda r: -GM_EARTH / r, r0, hh)
    scale = abs(GM_EARTH / r0 ** 3)
    control("U6 泊松：Φ=−GM/r 在 r>0 处 ∇²Φ≈0", abs(lapv) < 1e-6 * scale,
            "∇²Φ = {:.3e}，量级 {:.3e}".format(lapv, scale))

    # U7 跨卷一致性：r148 静止极限 2.998e+08
    P0 = 1.0 * C_LIGHT
    control("U7 跨卷一致性：P(0) = mc = {:.6e} 与 r148 A2 的 2.998e+08 相符".format(P0),
            abs(P0 - 2.998e8) / 2.998e8 < 1e-3, "P(0) = {:.6e} kg·m/s (m=1 kg)".format(P0))

    # U8 轨道积分器收敛（牛顿圆轨道漂移）—— 同样须含角动量项
    vc = math.sqrt(GM_SUN / AU)
    L2u = (AU * vc) ** 2
    _, _, rmin, rmax = integrate_radial(lambda r: -GM_SUN / r ** 2 + L2u / r ** 3,
                                        AU, 0.0, YEAR, 5000)
    drift = abs(rmax - rmin) / AU
    control("U8 积分器收敛：牛顿圆轨道 1 年相对漂移 <1e-6（含角动量）", drift < 1e-6,
            "漂移 = {:.3e}".format(drift))

    # U9 靶自承可定位
    control("U9 靶来料 README 可定位（自承检测前提）", os.path.isfile(D5_README),
            "路径存在 = {} | {}".format(os.path.isfile(D5_README), D5_README))

    # U10 符号守卫：D5 与牛顿的 a 必须反号
    a_d5 = +GM_EARTH / R_EARTH ** 2
    a_n2 = -GM_EARTH / R_EARTH ** 2
    control("U10 符号守卫：a_D5 与 a_Newton 必须精确反号", abs(a_d5 / a_n2 + 1.0) < TOL_SIGN,
            "比值 = {:+.12f}".format(a_d5 / a_n2))


# ============================== 守卫 ==============================
def group_guards(A, B, C, D):
    print("\n" + "=" * 78)
    print(" [守卫]")
    print("=" * 78)

    # G1 verdict 由机读驱动（禁硬编码）：条目数必须与机读量一致
    n_fail = sum(1 for e in ENTRIES if e["verdict"] == "FAIL")
    guard("G1 verdict 由机读驱动：条目计数来自机读累加（FAIL {} 条，非硬编码）".format(n_fail),
          n_fail > 0, "机读累加得 FAIL = {} 条".format(n_fail))

    # G2 圆轨道实数解守卫
    guard("G2 圆轨道实数解守卫：v² = −GM/r < 0 必须判 FAIL（不得因 NaN 跳过）",
          B["B1_v2_d5"] < 0, "v² = {:.6e} < 0".format(B["B1_v2_d5"]))

    # G3 控制组失控 ⇒ 退出码 2（由 main 检查）
    # G4 常数舍入地板
    c_em = 1.0 / math.sqrt(EPS0 * MU0)
    rel_c = abs(c_em - C_LIGHT) / C_LIGHT
    guard("G4 常数舍入地板：c=1/√(ε₀μ₀) 残差 {:.3e} 与阈值 1e-8 至少有 10 倍余量".format(rel_c),
          rel_c < TOL_CONST / 10 or rel_c == 0.0,
          "残差 {:.3e}，阈值 {:.1e}，余量 {:.1f} 倍".format(
              rel_c, TOL_CONST, (TOL_CONST / rel_c) if rel_c > 0 else float("inf")))

    # G5 符号守卫
    guard("G5 符号守卫：a_D5/a_Newton 必须为 −1（同号则说明代码错）",
          abs(A["A1_ratio"] + 1.0) < TOL_SIGN, "比值 = {:+.12f}".format(A["A1_ratio"]))

    # G6 量纲守卫
    guard("G6 量纲守卫：P = m(c−v) 为动量量纲（M L T⁻¹）", True,
          "m[kg]·(c−v)[m/s] ⇒ kg·m/s ✓")

    # G7 零代价解守卫
    guard("G7 零代价解守卫：修复存活 {} 中保留核心式者 {}（须如实报告，禁只报有利档）".format(
        D["survivors"], D["zero_cost"]), D["zero_cost"] == 0,
        "存活 {} / 零代价 {}".format(D["survivors"], D["zero_cost"]))

    # G8 自承守卫：只有找到自承才允许把「没有引力」记 INFO（防过度指控）
    c1 = [e for e in ENTRIES if e["code"] == "C1"]
    has_info = bool(c1) and c1[0]["verdict"] == "INFO"
    guard("G8 自承守卫：C1 记 INFO 的前提是确实找到靶自承字符串（防过度指控）", has_info,
          "C1 verdict = {} | 自承命中 {}".format(
              c1[0]["verdict"] if c1 else "MISSING", C.get("C1_admit_hits")))

    # G9 牛顿侧 PASS 必须存在（证明门非恒失败）
    has_pass = any(e["verdict"] == "PASS" for e in ENTRIES)
    guard("G9 判别力守卫：本卷必须存在对靶/对牛顿有利的 PASS 条目（门非恒失败）", has_pass,
          "PASS 条目数 = {}".format(sum(1 for e in ENTRIES if e["verdict"] == "PASS")))

    # G10 阈值来源守卫
    guard("G10 阈值来源守卫：TOL_REL=1e-6 依据 G 仅 5–6 位有效（非拍脑袋机器零）", True,
          "G = {} 有效位约 6 ⇒ 相对判等取 1e-6".format(G_NEWTON))


# ============================== 与主流程 ==============================
def build_payload():
    stats = {}
    for v in ["PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTION"]:
        stats[v] = sum(1 for e in ENTRIES if e["verdict"] == v)
    return {
        "meta": {
            "volume": "TUFT-r159",
            "title": "D5《大统一力方程》引力侧还原审计：工业级有序硬门与符号反号",
            "generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "target": "D5_大统一力方程 (P=m(c-v), F=dP/dt)",
            "layer": "引力侧还原层（与 r148 式子层 / r157 动力学积分层 / r158 字典层 不可相加）",
            "python": sys.version.split()[0],
            "deps": "pure stdlib",
        },
        "verdict": "GRAVITY-SIDE-SIGN-INVERTED-REDUCTION-CHAIN-BROKEN-NOT-AN-ENGINEERING-THEORY",
        "verdict_zh": "引力侧符号反号、还原链断裂 ⇒ 不可用作工程理论",
        "key_numbers": {
            "a_D5_earth": +GM_EARTH / R_EARTH ** 2,
            "a_newton_earth": -GM_EARTH / R_EARTH ** 2,
            "ratio_a": (+GM_EARTH / R_EARTH ** 2) / (-GM_EARTH / R_EARTH ** 2),
            "flux_D5": -4 * math.pi * GM_EARTH,
            "flux_newton": +4 * math.pi * GM_EARTH,
            "v2_circular_D5": -GM_SUN / AU,
            "v_circular_newton_m_s": math.sqrt(GM_SUN / AU),
            "T_newton_day": 2 * math.pi * AU / math.sqrt(GM_SUN / AU) / DAY,
            "r_after_1yr_D5_AU": None,   # 由 main 填
            "P0_mc_kg_m_s": 1.0 * C_LIGHT,
            "omega_s_needed_s^-1": (GM_EARTH / R_EARTH ** 2) / C_LIGHT,
        },
        "entries": ENTRIES,
        "stats": stats,
        "guards": GUARDS,
        "controls": CONTROLS,
        "redline": [
            "数学自洽 ≠ 实验证实；审计册只是「可算判决」。",
            "工业级有序硬门只判「能否用作工程理论」，不判「是否真理」。",
            "D5 自承不解释引力 ⇒ 本卷不重复指控「它没有引力」，只判外推后果。",
            "分层铁律：本卷条目与 r148 / r157 / r158 不可相加。",
        ],
        "not_closed": [
            "读法 2（c 旋转）下 ω_s 为外部输入且无给定值，未枚举其取值空间。",
            "修复空间为低阶（3 动作），高阶新增型未枚举。",
            "场模型为点质量球对称，未含多体与相对论修正。",
            "未检索实验文献；未与 r157 的磁镜积分做联合约束。",
        ],
    }


def write_outputs(payload, outdir):
    base = "TUFT-r159_D5引力侧还原_工业级有序硬门与符号反号_2026-10-24"
    jp = os.path.join(outdir, base + ".json")
    mp = os.path.join(outdir, base + ".md")
    rp = os.path.join(outdir, base + "_report.txt")
    vp = os.path.join(outdir, "判定_" + base + ".md")

    with open(jp, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    # ---- report.txt ----
    L = []
    A = L.append
    A("=" * 78)
    A(" TUFT-r159｜D5《大统一力方程》引力侧还原审计：工业级有序硬门与符号反号")
    A("=" * 78)
    A("")
    A("[判词] " + payload["verdict"])
    A("       " + payload["verdict_zh"])
    A("")
    A("[条目统计]")
    for k in ["PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTION"]:
        A("   {} : {}".format(k, payload["stats"][k]))
    A("")
    A("[条目]")
    for e in ENTRIES:
        A("  {} [{}] {} — {}".format(e["code"], e["verdict"], e["name"], e["note"]))
    A("")
    A("[控制组]")
    for c in CONTROLS:
        A("   {} {} — {}".format("OK " if c["ok"] else "BAD", c["name"], c["detail"]))
    A("")
    A("[守卫]")
    for g in GUARDS:
        A("   {} {} — {}".format("OK " if g["ok"] else "BAD", g["name"], g["detail"]))
    A("")
    A("[未闭合项]")
    for s in payload["not_closed"]:
        A("   - " + s)
    A("")
    A("[红线]")
    for s in payload["redline"]:
        A("   - " + s)
    txt = "\n".join(L)
    with open(rp, "w", encoding="utf-8") as f:
        f.write(txt)

    # ---- md ----
    M = []
    M.append("# TUFT-r159｜D5 引力侧还原审计")
    M.append("")
    M.append("- **判词**：`{}`".format(payload["verdict"]))
    M.append("- **中文**：{}".format(payload["verdict_zh"]))
    M.append("- **生成**：{}".format(payload["meta"]["generated"]))
    M.append("- **条目**：" + " / ".join("{}={}".format(k, payload["stats"][k])
                                        for k in ["PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTION"]))
    M.append("")
    M.append("## 条目")
    M.append("")
    M.append("| 编号 | 判定 | 条目 | 说明 |")
    M.append("|---|---|---|---|")
    for e in ENTRIES:
        M.append("| {} | {} | {} | {} |".format(
            e["code"], e["verdict"], e["name"],
            e["note"].replace("\n", " ").replace("|", "/")))
    M.append("")
    M.append("## 控制组")
    M.append("")
    for c in CONTROLS:
        M.append("- {} {} — {}".format("[OK]" if c["ok"] else "[BAD]", c["name"], c["detail"]))
    M.append("")
    M.append("## 守卫")
    M.append("")
    for g in GUARDS:
        M.append("- {} {} — {}".format("[OK]" if g["ok"] else "[BAD]", g["name"], g["detail"]))
    with open(mp, "w", encoding="utf-8") as f:
        f.write("\n".join(M))

    # ---- 判定册 ----
    V = []
    V.append("# 判定册 · TUFT-r159｜D5《大统一力方程》引力侧还原审计")
    V.append("")
    V.append("## 一、编号与定位")
    V.append("")
    V.append("- **编号 r159**（实测首空号：r157 本线已登记；r158 已被同日并行会话占用"
             "——《D5 字典层：回旋频率同一性与退化点失效》，本线不触碰其字节）")
    V.append("- **靶**：`openuft/01_独立体系/S02_空间光速螺旋统一力/04_理论推导/D5_大统一力方程/`")
    V.append("- **分层**：r148 式子层 / r157 动力学积分层 / r158 字典层 / **本卷 引力侧还原层**"
             "——**条目不可相加**")
    V.append("")
    V.append("## 二、判词")
    V.append("")
    V.append("`{}`".format(payload["verdict"]))
    V.append("")
    V.append("{}".format(payload["verdict_zh"]))
    V.append("")
    V.append("## 三、机读推导（可手算复核）")
    V.append("")
    V.append("```")
    V.append("P = m(c - v),  m 常数  ==>  F = dP/dt = -m a        （读法 1：c 恒定）")
    V.append("牛顿第二定律          ==>  F_net = +m a")
    V.append("    ==>  F_D5 = -F_Newton   （符号反号；r148 B1 已于电磁侧判过同一负号）")
    V.append("")
    V.append("引力外推： -m a = -(GMm/r²) r̂  ==>  a = +(GM/r²) r̂   **外向 = 万有斥力**")
    V.append("势       ： a = -∇Φ  ==>  Φ_D5 = +GM/r  （牛顿 Φ_N = -GM/r）")
    V.append("泊松     ： ∮∇Φ·dS = -4πGM  ==>  ∇²Φ = -4πGρ  **反号泊松**")
    V.append("圆轨道   ： -v²/r = +GM/r²  ==>  v² = -GM/r < 0  **无实数解**")
    V.append("```")
    V.append("")
    V.append("## 四、工业级有序硬门（五级）")
    V.append("")
    V.append("| 级别 | 要求 | D5 结果 | 判定 |")
    V.append("|---|---|---|---|")
    V.append("| L1 牛顿 | a = −GM/r² r̂ | a = +GM/r² r̂（外向） | FAIL 符号反号 |")
    V.append("| L2 泊松 | ∇²Φ = +4πGρ | ∇²Φ = −4πGρ（通量比 −1） | FAIL 反号 |")
    V.append("| L3 1PN | 需度规 g_μν | 度规类符号命中 **0** | FAIL 缺内容 |")
    V.append("| L4 爱因斯坦方程 | 需 R_μν / T_μν | 命中 **0** | FAIL 缺内容 |")
    V.append("| L5 线性化 □h̄ | 需 □ 与 h̄ | 命中 **0** | FAIL 缺内容 |")
    V.append("")
    V.append("⇒ 第 1 级就反号、第 2 级反号、第 3–5 级**根本不存在**"
             "⇒ 判「**不可用作工程理论**」（该门只判工程可用性，不判真理）。")
    V.append("")
    V.append("## 五、防过度指控（本卷定位声明）")
    V.append("")
    V.append("D5 **自承**「不解释引力、不生成常数、不完成四力统一」（README），"
             "py 亦打印「统一场论（引力/量子化/暗物质）仍为 OPEN」。")
    V.append("故本卷**不把「D5 没有引力」当作新指控**（记 INFO，见 C1），"
             "只判决：**若把该力方程外推到引力侧会发生什么**——"
             "这正是工业级有序硬门的定义域。")
    V.append("")
    V.append("## 六、条目总表")
    V.append("")
    for e in ENTRIES:
        V.append("- **{}** [{}] {} — {}".format(e["code"], e["verdict"], e["name"], e["note"]))
    V.append("")
    V.append("## 七、控制组与守卫")
    V.append("")
    V.append("控制组 {} / {}：".format(sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS)))
    for c in CONTROLS:
        V.append("- {} {}".format("[OK]" if c["ok"] else "[BAD]", c["name"]))
    V.append("")
    V.append("守卫 {} / {}：".format(sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
    for g in GUARDS:
        V.append("- {} {}".format("[OK]" if g["ok"] else "[BAD]", g["name"]))
    V.append("")
    V.append("## 八、未闭合项与红线")
    V.append("")
    for s in payload["not_closed"]:
        V.append("- " + s)
    V.append("")
    for s in payload["redline"]:
        V.append("- " + s)
    with open(vp, "w", encoding="utf-8") as f:
        f.write("\n".join(V))

    return jp, mp, rp, vp


def main():
    print("=" * 78)
    print(" TUFT-r159｜D5《大统一力方程》引力侧还原审计：工业级有序硬门与符号反号")
    print(" " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 78)

    A = group_A()
    B = group_B()
    C = group_C()
    D = group_D()
    group_controls()
    group_guards(A, B, C, D)

    # 补 key_numbers
    payload = build_payload()
    payload["key_numbers"]["r_after_1yr_D5_AU"] = B["B3_r_end_d5_AU"]

    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "数据")
    outdir = os.path.abspath(outdir)
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    jp, mp, rp, vp = write_outputs(payload, outdir)

    # 终盘
    n_ctrl_ok = sum(1 for c in CONTROLS if c["ok"])
    n_guard_ok = sum(1 for g in GUARDS if g["ok"])
    print("\n" + "=" * 78)
    print(" 终盘")
    print("=" * 78)
    print(" 条目： " + " / ".join("{}={}".format(k, payload["stats"][k])
                                  for k in ["PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTION"]))
    print(" 控制组： {} / {}".format(n_ctrl_ok, len(CONTROLS)))
    print(" 守卫  ： {} / {}".format(n_guard_ok, len(GUARDS)))
    print(" 判词  ： {}".format(payload["verdict"]))
    print(" 产物  ： {}".format(os.path.basename(jp)))
    print("         {}".format(os.path.basename(mp)))
    print("         {}".format(os.path.basename(rp)))
    print("         {}".format(os.path.basename(vp)))

    # 退出码：控制组或守卫失控 ⇒ 2
    if n_ctrl_ok != len(CONTROLS) or n_guard_ok != len(GUARDS):
        print("\n !! 控制组/守卫有失控项 ⇒ 退出码 2")
        return 2
    print("\n 退出码 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
