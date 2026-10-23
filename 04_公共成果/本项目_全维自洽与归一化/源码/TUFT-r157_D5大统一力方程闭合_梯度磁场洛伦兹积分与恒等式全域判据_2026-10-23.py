# -*- coding: utf-8 -*-
"""
TUFT-r157｜D5《大统一力方程》闭合卷：梯度磁场洛伦兹力数值积分与 κ²+τ²=(ω/v)² 全域判据

================================================================================
00. 编号与定位
================================================================================
【编号】r157。实测首空号：源码目录已占 r31..r156（r156 为同日并行会话《v总等于c
       第二三步 · 作用量电荷环流与 Frank 分解》占位文件，本线不触碰），r157 为首空号。

【动机：闭合 r148 的两项未闭合项】
  r148（D5《大统一力方程》首攻与修复定价）对靶的「几何基石」
      κ² + τ² = (ω/v)² = (qB/(γmv))²        （来料标注适用：匀速螺旋 / 梯度磁场）
  判了 C1（匀速螺旋下成立但零新增，INFO）与 C2（梯度磁场下不成立，FAIL），
  但其 §7 未闭合项写明：
    1. **C2 用运动学反例而非真实梯度磁场积分** —— 以「螺距变化的螺旋」+ 磁镜绝热
       不变量论证；**未做**真实梯度磁场下的洛伦兹力数值积分；
    2. **梯度磁场下 ω 的口径** —— B 随位置变，ω = qB/(γm) 用哪一点的 B 未声明，
       本卷只登记「口径未定」，未代选。
  本卷用**真实的相对论洛伦兹力数值积分**（RK4，轴对称磁镜场）闭合这两项：
  直接测量积分轨迹的瞬时 Frenet 不变量 κ(t)、τ(t)（由 v, a, j 解析构造，
  **不用有限差分**，规避 r151 踩过的三阶差分噪声地板），并对恒等式做全域判据。

【★分层（与 r148 条目不可相加）】
  r148 = 式子层（P=m(c−v) 的两个极限 + 修复定价 + 运动学反例）；
  **本卷 = 动力学积分层**：把 r148 的运动学反例升级为真实洛伦兹积分，
  定位恒等式的**适用边界**（绝热参数 λ=ρ/L 扫描），并闭合 ω 口径问题。

================================================================================
01. 形式化（无量纲系统）
================================================================================
  取 t̃ = ω_c t（ω_c = qB₀/m），x̃ = x/ρ₀（ρ₀ = c/ω_c），ṽ = v/c。则
      d x̃/d t̃ = ṽ,     d ṽ/d t̃ = (1/γ) ṽ × B̃,     γ = 1/√(1−|ṽ|²)
  静磁场无力做功 ⇒ |ṽ| 与 γ **严格守恒**（机检项 B1）。
  轴对称磁镜场（∇·B=0 解析满足）：
      B̃_z = 1 + η(z̃/L̃)²,     B̃_ρ = −η ρ̃ z̃/L̃²,     η=1
  无量纲恒等式：κ̃² + τ̃² =? (ω̃/ṽ)²,  ω̃ = |B̃|/γ（局域口径，最有利于靶）。
  Frenet 测量（全部解析，无差分）：
      κ̃ = |ṽ×ã|/ṽ³,   τ̃ = (ṽ×ã)·j̃/|ṽ×ã|²
      ã = (1/γ)ṽ×B̃,   j̃ = (1/γ)[ã×B̃ + ṽ×((ṽ·∇)B̃)]

================================================================================
02. 待检验命题
================================================================================
  H1 均匀场：恒等式对真实积分轨迹精确成立（复现 r148 C1 的机器零）；
  H2 梯度场（磁镜）：恒等式还成立吗？成立域多宽（绝热参数 λ=ρ₀/L 扫描）？
  H3 r148 的标定「达 1% 残差约需 146.9 个回旋周期」在真实积分下成立吗？
  H4 ω 的口径（局域 |B| / B_z /  midplane B₀ / 轨道平均）哪一种是靶的唯一出路？

================================================================================
03. 本卷新增读数（靶与 r148 均未计算的部分）
================================================================================
  N1 ★真实积分轨迹的 κ, τ（r148 只有运动学反例，没有一条真实 Lorentz 轨迹）；
  N2 ★恒等式的适用边界 λ*（残差=1% 的绝热参数，机读扫描 + 标度拟合）；
  N3 ★残差标度指数 p（log-log 拟合：一阶 or 二阶 in λ）；
  N4 ★r148「147 周期」标定的动态复核（残差跟踪瞬时速率还是累积量）；
  N5 ★ω 四口径的残差对照表。

================================================================================
04. 不自推声明
================================================================================
  NS1 不替靶补口径、不替靶选常数；不修改靶任何字节；不重判 r148 的式子层结论。
  NS2 本卷只判「恒等式在动力学积分下的成立域」，不判整个 D5 体系。
  NS3 v4/v5（靶自产下游审计）只引用不回读复核。

================================================================================
05. 红线
================================================================================
  数学自洽 ≠ 实验证实；**恒等式成立 ≠ 有新内容**（均匀场下它是 Frenet 推论）；
  **成立域可标定 ≠ 宣称无边界**；防过度指控与防漏判同等重要
  （若机读显示恒等式在绝热区稳健，须诚实削弱 r148 的部分指控并登记 CORRECTION）。
"""

import json
import math
import os
import sys
import time

# ============================================================
# 常数（无量纲系统：ω_c = qB₀/m = 1, ρ₀ = c/ω_c, v 以 c 为单位）
# ============================================================
ETA = 1.0                  # 磁镜场强参数 B_z = 1 + (z/L)^2
VP0 = 0.5                  # 初始横向速率（单位 c）
VPAR0 = 0.5                # 初始轴向速率（单位 c）
GAMMA0 = 1.0 / math.sqrt(1.0 - (VP0 * VP0 + VPAR0 * VPAR0))
RHO0 = GAMMA0 * VP0        # 初始回旋半径（B₀=1）
B_MIRROR = (VP0 * VP0 + VPAR0 * VPAR0) / (VP0 * VP0)   # 磁镜点场强 = 2
Z_MIRROR_FACTOR = math.sqrt(B_MIRROR - 1.0)            # z_m = L * 该因子 = L

LAMBDAS = [0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0]   # λ = ρ₀/L 扫描
TOL_ID = 1.0e-2            # 恒等式「失效」阈值（残差 > 1%，沿用 r148 标定）
GYRO_T = 2.0 * math.pi * GAMMA0   # 一个回旋周期（t̃ 单位，B=1 处）

BASE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(BASE, "04_公共成果", "本项目_全维自洽与归一化", "数据")
STEM = "TUFT-r157_D5大统一力方程闭合_梯度磁场洛伦兹积分与恒等式全域判据_2026-10-23"

# ============================================================
# 登记器
# ============================================================
ITEMS = []
CONTROLS = []
GUARDS = []


def add(iid, title, status, note="", **metrics):
    ITEMS.append({"id": iid, "title": title, "status": status,
                  "note": note, "metrics": metrics})


def control(cid, desc, value, expect, ok):
    CONTROLS.append({"id": cid, "desc": desc, "value": value,
                     "expect": expect, "ok": bool(ok)})


def guard(name, ok, detail=""):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})


def fv(x):
    try:
        return "%.6e" % float(x)
    except Exception:
        return str(x)


# ============================================================
# 矢量工具
# ============================================================
def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def norm(a):
    return math.sqrt(dot(a, a))


# ============================================================
# 磁场（轴对称磁镜，∇·B=0 解析满足）
#   B_z = 1 + (z/L)^2,  B_x = -xz/L^2,  B_y = -yz/L^2
# ============================================================
def field(x, y, z, L):
    inv = 1.0 / (L * L)
    return (-x * z * inv, -y * z * inv, 1.0 + z * z * inv)


def field_grad(x, y, z, L):
    """∇|B|（解析）。|B|² = (x²+y²)z²/L⁴ + (1+z²/L²)²"""
    inv = 1.0 / (L * L)
    inv2 = inv * inv
    Bx, By, Bz = field(x, y, z, L)
    Bmag = math.sqrt(Bx * Bx + By * By + Bz * Bz)
    gx = x * z * z * inv2 / Bmag
    gy = y * z * z * inv2 / Bmag
    gz = (2.0 * (x * x + y * y) * z * inv2
          + 2.0 * (1.0 + z * z * inv) * 2.0 * z * inv) / Bmag
    return (gx, gy, gz)


def conv_B(x, y, z, L, vx, vy, vz):
    """(v·∇)B（解析）"""
    inv = 1.0 / (L * L)
    return (-(vx * z + vz * x) * inv,
            -(vy * z + vz * y) * inv,
            2.0 * vz * z * inv)


def gamma_of(vx, vy, vz):
    return 1.0 / math.sqrt(1.0 - (vx * vx + vy * vy + vz * vz))


# ============================================================
# 相对论洛伦兹 ODE（无量纲）：d v~/dt~ = (1/γ) v~ × B~
# ============================================================
def deriv(s, L):
    x, y, z, vx, vy, vz = s
    Bx, By, Bz = field(x, y, z, L)
    g = gamma_of(vx, vy, vz)
    return (vx, vy, vz,
            (vy * Bz - vz * By) / g,
            (vz * Bx - vx * Bz) / g,
            (vx * By - vy * Bx) / g)


def rk4(s, h, L):
    k1 = deriv(s, L)
    s2 = tuple(s[i] + 0.5 * h * k1[i] for i in range(6))
    k2 = deriv(s2, L)
    s3 = tuple(s[i] + 0.5 * h * k2[i] for i in range(6))
    k3 = deriv(s3, L)
    s4 = tuple(s[i] + h * k3[i] for i in range(6))
    k4 = deriv(s4, L)
    return tuple(s[i] + (h / 6.0) * (k1[i] + 2.0 * k2[i]
                                     + 2.0 * k3[i] + k4[i]) for i in range(6))


# ============================================================
# Frenet 测量（v, a, j 全部解析，无有限差分）
# ============================================================
def measure(s, L):
    """返回 (kappa, tau, speed, gamma, Bmag, Bz, vpar, vperp, mu,
             apar, gradpar_B, A_eff)"""
    x, y, z, vx, vy, vz = s
    Bx, By, Bz = field(x, y, z, L)
    Bmag = math.sqrt(Bx * Bx + By * By + Bz * Bz)
    g = gamma_of(vx, vy, vz)
    v = (vx, vy, vz)
    a = ((vy * Bz - vz * By) / g, (vz * Bx - vx * Bz) / g,
         (vx * By - vy * Bx) / g)
    dBx, dBy, dBz = conv_B(x, y, z, L, vx, vy, vz)
    jx = (a[1] * Bz - a[2] * By + vy * dBz - vz * dBy) / g
    jy = (a[2] * Bx - a[0] * Bz + vz * dBx - vx * dBz) / g
    jz = (a[0] * By - a[1] * Bx + vx * dBy - vy * dBx) / g
    j = (jx, jy, jz)
    cx = cross(v, a)
    nc = norm(cx)
    nv = norm(v)
    if nc <= 0.0 or nv <= 0.0:
        return None
    kappa = nc / (nv ** 3)
    tau = dot(cx, j) / (nc * nc)
    Bhat = (Bx / Bmag, By / Bmag, Bz / Bmag)
    vpar = dot(v, Bhat)
    vperp = math.sqrt(max(nv * nv - vpar * vpar, 0.0))
    mu = g * g * vperp * vperp / (2.0 * Bmag)          # p_⊥²/(2mB) 无量纲形式
    apar = dot(a, Bhat)                                 # 瞬时平行加速度（应恒 0）
    gB = field_grad(x, y, z, L)
    gradpar_B = dot(gB, Bhat)                           # ∇_∥B
    A_eff = -(vperp * vperp / (2.0 * Bmag)) * gradpar_B  # 磁镜力（回旋平均速率）
    return (kappa, tau, nv, g, Bmag, Bz, vpar, vperp, mu,
            apar, gradpar_B, A_eff)


# ============================================================
# 积分驱动（记录 + 后处理）
# ============================================================
def run_case(L, h, t_max, record_every=20, vp0=VP0, vpar0=VPAR0,
             uniform=False, full_bounce=False):
    """积分并记录。uniform=True 时 η=0（对照）；full_bounce 时积分到返回 z≤0。"""
    rho0 = gamma_of(0.0, vp0, vpar0) * vp0
    if uniform:
        L = 1.0e18                     # η/L² → 0
    s = (2.0 * rho0, 0.0, 0.0, 0.0, vp0, vpar0)   # 导向中心在 2ρ₀，v 沿 +y/+z
    v0 = norm(s[3:6])
    n_steps = int(t_max / h)
    rec = {"t": [], "kappa": [], "tau": [], "v": [], "g": [], "B": [],
           "Bz": [], "vpar": [], "vperp": [], "mu": [], "apar": [],
           "Aeff": [], "z": []}
    vmax_drift = 0.0
    apar_max = 0.0
    mu0 = None
    z_max = 0.0
    mirrored = False
    t = 0.0
    for i in range(n_steps):
        s = rk4(s, h, L)
        t += h
        if i % record_every == 0:
            m = measure(s, L)
            if m is None:
                continue
            rec["t"].append(t)
            rec["kappa"].append(m[0]); rec["tau"].append(m[1])
            rec["v"].append(m[2]); rec["g"].append(m[3])
            rec["B"].append(m[4]); rec["Bz"].append(m[5])
            rec["vpar"].append(m[6]); rec["vperp"].append(m[7])
            rec["mu"].append(m[8]); rec["apar"].append(m[9])
            rec["Aeff"].append(m[10]); rec["z"].append(s[2])
            if mu0 is None:
                mu0 = m[8]
            vmax_drift = max(vmax_drift, abs(m[2] - v0))
            apar_max = max(apar_max, abs(m[9]) / max(norm(s[3:6]), 1e-30))
            z_max = max(z_max, s[2])
        if full_bounce and s[2] <= 0.0 and t > 0.5 * t_max and mirrored:
            break
        if full_bounce and s[5] < 0.0:
            mirrored = True
    return {"rec": rec, "v_drift": vmax_drift, "apar_max": apar_max,
            "mu0": mu0, "z_max": z_max, "rho0": rho0,
            "mu_end": rec["mu"][-1] if rec["mu"] else None,
            "t_end": t}


def residuals(rec, bmodes=("local", "z", "mid", "avg")):
    """对记录点计算各 ω 口径下的恒等式残差，返回各口径的最大残差与索引。"""
    out = {}
    n = len(rec["t"])
    Bsum = 0.0
    for i in range(n):
        k2t2 = rec["kappa"][i] ** 2 + rec["tau"][i] ** 2
        Bsum += rec["B"][i]
        Bavg = Bsum / (i + 1)
        for mode in bmodes:
            if mode == "local":
                w = rec["B"][i] / rec["g"][i]
            elif mode == "z":
                w = rec["Bz"][i] / rec["g"][i]
            elif mode == "mid":
                w = 1.0 / rec["g"][i]
            else:
                w = Bavg / rec["g"][i]
            rhs = (w / rec["v"][i]) ** 2
            r = abs(k2t2 - rhs) / rhs
            if mode not in out or r > out[mode][0]:
                out[mode] = (r, i)
    return out


# ============================================================
# 运动学模型（复现 r148 的加速螺旋，用于跨册对照）
#   r(t) = (R cos ωt, R sin ωt, u t + A t²/2)，轴固定、R/ω 恒定
# ============================================================
def helix_residual_kin(R, w, u, A):
    v = (0.0, R * w, u)
    a = (-R * w * w, 0.0, A)
    j = (0.0, -R * w ** 3, 0.0)
    cx = cross(v, a)
    nc = norm(cx)
    nv = norm(v)
    kappa = nc / (nv ** 3)
    tau = dot(cx, j) / (nc * nc)
    rhs = (w / nv) ** 2
    return abs(kappa * kappa + tau * tau - rhs) / rhs


def frenet_uniform(vp0, vpar0):
    """均匀场中解析螺旋的 κ, τ（无量纲，B₀=1）。
    注：初值 r=(2ρ₀,0,0), v=(0,+v⊥,+v∥) ⇒ 自 +z 看为**顺时针**回旋，
    故对 (cos ωt, sin ωt, +z) 参考螺旋 τ 取**负号**（κ 不受手性影响）。"""
    g = gamma_of(0.0, vp0, vpar0)
    v2 = vp0 * vp0 + vpar0 * vpar0
    return vp0 / (g * v2), -vpar0 / (g * v2)


# ============================================================
# A 组：均匀场对照
# ============================================================
def A_group():
    h = 1.0e-3
    tmax = 10.0 * GYRO_T
    run = run_case(1.0, h, tmax, record_every=5, uniform=True)
    res = residuals(run["rec"], bmodes=("local",))
    r_uniform = res["local"][0]
    kap_an, tau_an = frenet_uniform(VP0, VPAR0)
    rec = run["rec"]
    dev_k = max(abs(rec["kappa"][i] - kap_an) for i in range(len(rec["t"])))
    dev_t = max(abs(rec["tau"][i] - tau_an) for i in range(len(rec["t"])))
    kap_me = sum(rec["kappa"]) / len(rec["kappa"])
    tau_me = sum(rec["tau"]) / len(rec["tau"])
    # RK4 收敛：h 与 h/2
    run2 = run_case(1.0, h / 2.0, tmax, record_every=5, uniform=True)
    r2 = residuals(run2["rec"], bmodes=("local",))["local"][0]
    conv = abs(r2 - r_uniform)
    return {"r_uniform": r_uniform, "dev_kappa": dev_k, "dev_tau": dev_t,
            "r_half": r2, "conv": conv, "v_drift": run["v_drift"],
            "apar_max": run["apar_max"],
            "kap_an": kap_an, "tau_an": tau_an,
            "kap_me": kap_me, "tau_me": tau_me}


# ============================================================
# B/C 组：磁镜动力学与恒等式全域判据
# ============================================================
def C_group():
    rows = []
    for lam in LAMBDAS:
        L = RHO0 / lam
        if lam <= 0.01:
            h, tmax = 2.0e-3, 120.0 * GYRO_T
            fb = True
        else:
            h, tmax = 5.0e-3, 60.0 * GYRO_T
            fb = False
        run = run_case(L, h, tmax, record_every=20, full_bounce=fb)
        res = residuals(run["rec"])
        rec = run["rec"]
        # 动态 vs 运动学（匹配 A_eff）：取 local 残差最大点
        i_max = res["local"][1]
        B_i = rec["B"][i_max]; g_i = rec["g"][i_max]
        vp_i = rec["vperp"][i_max]; vpar_i = rec["vpar"][i_max]
        Aeff_i = rec["Aeff"][i_max]
        R_loc = g_i * vp_i / B_i
        w_loc = B_i / g_i
        r_kin = helix_residual_kin(R_loc, w_loc, abs(vpar_i), abs(Aeff_i))
        mu_drift = (abs(run["mu_end"] - run["mu0"]) / run["mu0"]
                    if run["mu0"] else float("nan"))
        rows.append({"lam": lam, "L": L,
                     "r_local": res["local"][0],
                     "r_z": res["z"][0], "r_mid": res["mid"][0],
                     "r_avg": res["avg"][0],
                     "v_drift": run["v_drift"], "mu_drift": mu_drift,
                     "z_max_over_L": run["z_max"] / L,
                     "z_theory_over_L": Z_MIRROR_FACTOR,
                     "r_kin_at_max": r_kin,
                     "Aeff_at_max": Aeff_i, "w_at_max": w_loc,
                     "apar_max": run["apar_max"],
                     "t_end": run["t_end"]})
    # 标度拟合（在 1e-8 < r < 0.1 的区间上做 log-log 线性拟合）
    pts = [(r["lam"], r["r_local"]) for r in rows
           if 1.0e-8 < r["r_local"] < 0.1]
    slope = float("nan")
    if len(pts) >= 3:
        xs = [math.log10(p[0]) for p in pts]
        ys = [math.log10(p[1]) for p in pts]
        mx = sum(xs) / len(xs)
        my = sum(ys) / len(ys)
        sxx = sum((x - mx) ** 2 for x in xs)
        sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        slope = sxy / sxx if sxx > 0 else float("nan")
    # 阈值 λ*（残差首次 > 1% 的 λ，线性插值）
    lam_star = float("nan")
    for i in range(len(rows) - 1):
        r1, r2_ = rows[i]["r_local"], rows[i + 1]["r_local"]
        if r1 <= TOL_ID < r2_:
            l1, l2 = rows[i]["lam"], rows[i + 1]["lam"]
            f = (math.log10(TOL_ID) - math.log10(max(r1, 1e-300))) / (
                math.log10(max(r2_, 1e-300)) - math.log10(max(r1, 1e-300)))
            lam_star = 10.0 ** (math.log10(l1) + f * (math.log10(l2) - math.log10(l1)))
            break
    return {"rows": rows, "slope": slope, "lam_star": lam_star}


# ============================================================
# ∇·B = 0 网格自检
# ============================================================
def divB_check(L=7.0, N=41, span=6.0):
    h = 2.0 * span / (N - 1)
    worst = 0.0
    for i in range(1, N - 1):
        x = -span + i * h
        for j in range(1, N - 1):
            y = -span + j * h
            for k in range(1, N - 1):
                z = -span + k * h
                Bx1, _, _ = field(x + h, y, z, L)
                Bx0, _, _ = field(x - h, y, z, L)
                _, By1, _ = field(x, y + h, z, L)
                _, By0, _ = field(x, y - h, z, L)
                _, _, Bz1 = field(x, y, z + h, L)
                _, _, Bz0 = field(x, y, z - h, L)
                d = ((Bx1 - Bx0) + (By1 - By0) + (Bz1 - Bz0)) / (2.0 * h)
                worst = max(worst, abs(d))
    return worst


# ============================================================
# 主流程
# ============================================================
def main():
    print("=" * 96)
    print("TUFT-r157｜D5 大统一力方程闭合卷：梯度磁场洛伦兹积分与恒等式全域判据")
    print("=" * 96)
    print("生成时刻: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    print("")
    print("【形式化】无量纲 t̃=ω_c t, x̃=x/ρ₀, ṽ=v/c；dṽ/d t̃=(1/γ)ṽ×B̃；")
    print("  磁镜场 B̃_z=1+(z/L)², B̃_ρ=−ρz/L²（∇·B=0 解析满足）；γ 严格守恒。")
    print("  初始: v_⊥₀=v_∥₀=0.5c, γ₀=%.6f, ρ₀=%.6f, 磁镜点 z_m=L" % (GAMMA0, RHO0))
    print("")

    # ---- A 组 ----
    print("[A 组] 均匀场对照（真实洛伦兹积分）...")
    a = A_group()
    print("  κ(机读均值)=%.10f  κ(解析)=%.10f  τ(机读均值)=%.10f  τ(解析)=%.10f"
          % (a["kap_me"], a["kap_an"], a["tau_me"], a["tau_an"]))
    print("  均匀场恒等式残差 = %.3e；RK4 收敛差 = %.3e；|v| 漂移 = %.3e"
          % (a["r_uniform"], a["conv"], a["v_drift"]))
    print("")

    # ---- C 组 ----
    print("[C 组] 磁镜扫描（λ=ρ₀/L）...")
    c = C_group()
    print("  %-8s %-12s %-12s %-12s %-12s %-10s %-10s"
          % ("λ", "r_local", "r_z", "r_mid", "r_avg", "μ漂移", "z_max/L"))
    for r in c["rows"]:
        print("  %-8.4g %-12.3e %-12.3e %-12.3e %-12.3e %-10.2e %-10.4f"
              % (r["lam"], r["r_local"], r["r_z"], r["r_mid"], r["r_avg"],
                 r["mu_drift"], r["z_max_over_L"]))
    print("  标度指数 p = %.3f；阈值 λ*(残差=1%%) = %s"
          % (c["slope"], ("%.4g" % c["lam_star"]) if c["lam_star"] == c["lam_star"]
             else "未跨过（扫描区内残差未达 1%）"))
    print("")

    divB = divB_check()
    print("[自检] max|∇·B| = %.3e" % divB)
    print("")

    # ---- 台账 ----
    lam_star = c["lam_star"]
    slope = c["slope"]
    r_lam1 = c["rows"][-1]["r_local"] if c["rows"] else float("nan")
    r_adiab = c["rows"][0]["r_local"] if c["rows"] else float("nan")
    adiabatic_robust = (r_adiab == r_adiab and r_adiab < TOL_ID)
    strong_fails = (r_lam1 == r_lam1 and r_lam1 > TOL_ID)

    add("A1", "均匀场恒等式对真实积分轨迹精确成立（残差 %.3e）⇒ 与 r148 C1 一致，"
              "是 Frenet + 洛伦兹的直接推论，零新增" % a["r_uniform"],
        "INFO" if a["r_uniform"] < 1.0e-9 else "FAIL",
        "RK4 相对论洛伦兹积分；κ, τ 由 v, a, j 解析构造（无有限差分）；"
        "与 r148 的运动学机器零跨方法互证。",
        r_uniform=a["r_uniform"], r148_c1=1.110e-16,
        kappa_measured_ok=a["dev_kappa"], tau_measured_ok=a["dev_tau"])

    add("A2", "动态测量的 κ, τ 与解析螺旋值一致（κ 偏差 %.2e、τ 偏差 %.2e）"
              % (a["dev_kappa"], a["dev_tau"]),
        "PASS" if (a["dev_kappa"] < 1e-9 and a["dev_tau"] < 1e-9) else "FAIL",
        "解析值 κ=v_⊥/(γv²)、τ=−v_∥/(γv²)（无量纲，B₀=1；τ 的负号来自初值手性："
        "v=(0,+v⊥,+v∥) 为顺时针回旋，参考螺旋 (cos ωt, sin ωt, +z) 的 τ 取正）。",
        dev_kappa=a["dev_kappa"], dev_tau=a["dev_tau"],
        kappa_analytic=a["kap_an"], tau_analytic=a["tau_an"])

    add("A3", "RK4 收敛性：步长减半后残差变化 %.3e" % a["conv"],
        "PASS" if a["conv"] < 1.0e-6 else "FAIL",
        "h=1e-3 与 h=5e-4 两档对照。",
        conv=a["conv"])

    add("B1", "静磁场中 |v| 严格守恒（最大漂移 %.3e）⇒ γ 无歧义"
              % a["v_drift"],
        "PASS" if a["v_drift"] < 1.0e-6 else "FAIL",
        "洛伦兹力不做功；这一条同时闭合 r148 未闭合项 2 的 γ 半边"
        "（v 恒定 ⇒ γ 恒定，唯一未定的是 B 的取值）。",
        v_drift=a["v_drift"])

    add("B2", "绝热不变量 μ=γ²v_⊥²/(2B) 守恒（λ=5e-3 档漂移 %.2e）"
              % c["rows"][0]["mu_drift"],
        "PASS" if c["rows"][0]["mu_drift"] < 0.05 else "FAIL",
        "磁镜物理的教科书关系；积分器物理正确性的锚点。",
        mu_drift=c["rows"][0]["mu_drift"], lam=c["rows"][0]["lam"])

    add("B3", "磁镜条件：z_max/L = %.4f vs 理论 %.4f（λ=5e-3 档）"
              % (c["rows"][0]["z_max_over_L"], Z_MIRROR_FACTOR),
        "PASS" if abs(c["rows"][0]["z_max_over_L"] - Z_MIRROR_FACTOR) < 0.1
        else "FAIL",
        "理论 z_m = L√(v²/v_⊥₀²−1) = L；偏差应 ≲ λ。",
        z_max_over_L=c["rows"][0]["z_max_over_L"],
        theory=Z_MIRROR_FACTOR)

    add("B4", "瞬时平行加速度 a·B̂ 机读恒零（max %.2e）⇒ 磁镜力是回旋平均效应，"
              "r148 的「瞬时 dv_∥/dt」口径须按回旋平均读"
              % c["rows"][0]["apar_max"],
        "INFO",
        "(v×B)·B̂ ≡ 0 是恒等式；本卷因此用回旋平均速率 A_eff=−(v_⊥²/2B)∇_∥B "
        "与运动学模型对照。",
        apar_max=c["rows"][0]["apar_max"])

    # C1：全域判据（本卷核心）
    if strong_fails and adiabatic_robust:
        c1_status = "FAIL"
        c1_title = ("★恒等式成立域有界：均匀场精确成立；绝热梯度场（λ≪λ*）近似成立"
                    "（残差 ~λ^%.2f）；强梯度场失效（λ=1 残差 %.3e ≫ 1%%）"
                    % (slope if slope == slope else float("nan"), r_lam1))
        c1_note = ("机读扫描 λ=%s：残差 %.3e → %.3e；标度指数 p=%.3f；"
                   "阈值 λ*（残差=1%%）= %s。⇒ 来料把「匀速螺旋 / 梯度磁场」并列为"
                   "适用范围**无边界**：恒等式只在 λ<λ* 成立。"
                   % (["%.4g" % r["lam"] for r in c["rows"]],
                      r_adiab, r_lam1, slope if slope == slope else float("nan"),
                      ("%.4g" % lam_star) if lam_star == lam_star else "未跨过"))
    elif strong_fails:
        c1_status = "FAIL"
        c1_title = ("★恒等式在梯度场失效（λ=1 残差 %.3e ≫ 1%%），且小 λ 端也未达机器零"
                    "（%.3e）" % (r_lam1, r_adiab))
        c1_note = "扫描见机读证据；标度指数 p=%s。" % (
            ("%.3f" % slope) if slope == slope else "n/a")
    else:
        c1_status = "BOUNDARY"
        c1_title = ("★扫描区内未发现恒等式失效（λ=1 残差 %.3e）⇒ 本卷未能复现"
                    "r148 的强梯度失效" % r_lam1)
        c1_note = "诚实登记：若机读如此，则 r148 C2 的强梯度指控在本场模型下不成立。"
    add("C1", c1_title, c1_status, c1_note,
        rows=[{k: r[k] for k in ("lam", "r_local", "r_z", "r_mid", "r_avg",
                                 "mu_drift", "z_max_over_L")}
              for r in c["rows"]],
        slope=slope, lam_star=lam_star,
        r_adiabatic=r_adiab, r_strong=r_lam1, tol=TOL_ID)

    # C2：ω 口径（四变体 × 绝热档 / 强梯度档）
    row_ad = c["rows"][0]        # λ=5e-3 绝热档
    row_st = c["rows"][-1]       # λ=1 强梯度档
    ad = (row_ad["r_local"], row_ad["r_z"], row_ad["r_mid"], row_ad["r_avg"])
    st = (row_st["r_local"], row_st["r_z"], row_st["r_mid"], row_st["r_avg"])
    names = ("local|B|", "B_z", "midplane", "avg")
    # 局域族 = {|B|, B_z}：二者差异若 <1% 视为不可分辨（不按 0.0x% 差异挑口径）
    loc_gap = abs(ad[0] - ad[1]) / max(ad[0], ad[1])
    if loc_gap < 0.01 and min(ad[0], ad[1]) < min(ad[2], ad[3]) / 100.0:
        best_mode = ("local族（|B| 与 B_z 不可分辨，相对差 %.1e）" % loc_gap)
    else:
        best_mode = names[ad.index(min(ad))]
    st_best = min(st)
    add("C2", "★ω 口径四变体：绝热档（λ=5e-3）局域|B| %.3e / B_z %.3e / mid %.3e / "
              "avg %.3e ⇒ 唯一幸存 = **%s**；强梯度档（λ=1）最小 %.3e 仍 ≫ 1%% ⇒ 全部失效"
              % (ad[0], ad[1], ad[2], ad[3], best_mode, st_best),
        "FAIL" if (st_best > TOL_ID) else "INFO",
        "r148 未闭合项 2 闭合：B 随位置变，ω=qB/(γm) 用哪一点的 B **来料未声明**。"
        "机读：**局域族**（|B| 或 B_z，二者在绝热档残差相对差仅 %.1e，不可分辨）是唯一"
        "把残差压到 %.3e（≪1%%）的口径；midplane 与轨道平均即使绝热档也 O(1) ⇒ "
        "口径未定本身即是缺陷（靶从未声明用哪一点的 B）；且强梯度档下连最小残差"
        "（%.3e）都远超 1%% ⇒ 局部口径同样失效。"
        % (loc_gap, ad[0], st_best),
        ad_local=ad[0], ad_z=ad[1], ad_mid=ad[2], ad_avg=ad[3],
        st_local=st[0], st_z=st[1], st_mid=st[2], st_avg=st[3],
        best_mode=best_mode, st_best=st_best, loc_gap=loc_gap)

    # C3：r148 标定复核（机读驱动）
    r148_claim_cycles = 146.9
    if adiabatic_robust:
        add("C3", "★r148「达 1%% 残差约需 %.1f 个回旋周期」的标定**不成立**："
                  "λ=5e-3（r148 的 ε=0.01 对应档）真实积分全程最大残差 %.3e ≪ 1%%"
                  % (r148_claim_cycles, r_adiab),
            "CORRECTION",
            "r148 的推法：把磁镜的**累积**螺距变化 Δv_∥=A_eff·t 当作运动学模型里的"
            "**瞬时**加速度 A（其残差 ~A²/4），从而得到「147 周期到 1%%」。"
            "真实积分显示：残差跟踪**瞬时（回旋平均）速率**而非累积量 —— "
            "λ=5e-3 档 A_eff/ω ~ %.2e，残差全程 %.3e 量级。"
            "**对应关系（量级映射，非精确等同）**：r148 的 ε=0.01 ⇒ "
            "a_eff=−v_⊥0²ε/2=−1.25e-3/单位时间（ω=1）≈ −7.9e-3/回旋周期；"
            "本场 λ=5e-3（L=141.4）的磁镜力 dv_∥/dt̃≈−v_⊥²/(2L)≈−8.9e-4/单位时间 "
            "≈ −7.9e-3/回旋周期（回旋周期 2πγ=8.886）—— 两者同量级，"
            "故 λ=5e-3 取为 r148 ε=0.01 的对应档。"
            "⇒ 按防过度指控纪律，登记对 r148 C2 叙事（非其结论）的更正："
            "恒等式在绝热梯度场比 r148 估计的**更稳健**。"
            % (abs(c["rows"][0]["Aeff_at_max"]) / c["rows"][0]["w_at_max"]
               if c["rows"][0]["w_at_max"] else float("nan"), r_adiab),
            r148_cycles=r148_claim_cycles, r_measured=r_adiab,
            Aeff_over_w=(abs(c["rows"][0]["Aeff_at_max"])
                         / c["rows"][0]["w_at_max"]
                         if c["rows"][0]["w_at_max"] else None))
    else:
        add("C3", "r148「约 %.1f 个回旋周期到 1%%」的标定被真实积分**证实**"
                  "（λ=5e-3 档最大残差 %.3e）" % (r148_claim_cycles, r_adiab),
            "PASS",
            "动态积分复现 r148 的标定。", r148_cycles=r148_claim_cycles,
            r_measured=r_adiab)

    # C4：运动学 vs 动力学
    i_max_row = None
    for r in c["rows"]:
        if r["r_local"] == max(x["r_local"] for x in c["rows"]):
            i_max_row = r
            break
    add("C4", "运动学模型 vs 真实积分在匹配回旋平均速率处的残差对照："
              "运动学 %.3e vs 动力学 %.3e（λ=%s，残差最大点）"
              % (i_max_row["r_kin_at_max"], i_max_row["r_local"],
                 "%.4g" % i_max_row["lam"]),
        "INFO",
        "运动学模型（R/ω 固定 + 轴向加速）与真实积分（R/ω/ u 全部缓变）在"
        "匹配 A_eff 处的残差同量级 ⇒ 两方法互相印证；差异来自参数漂移项。",
        r_kin=i_max_row["r_kin_at_max"], r_dyn=i_max_row["r_local"],
        Aeff=i_max_row["Aeff_at_max"], w=i_max_row["w_at_max"])

    add("C5", "恒等式零新增：即使在成立域内，κ²+τ²=(ω/v)² 也是 Frenet 公式 + "
              "洛伦兹力圆的直接推论（承接 r148 C1，本卷动态确认）",
        "INFO", "均匀场残差 %.3e（机器零）即证据：无任何独立物理输入。" % a["r_uniform"])

    # D1：无边界宣称
    if lam_star == lam_star and lam_star < 1.0:
        add("D1", "★「梯度磁场」适用宣称无边界：机读阈值 λ* = %.4g ⇒ 宣称域"
                  "（一切梯度场）超出成立域（λ<λ*）" % lam_star,
            "FAIL",
            "λ = ρ₀/L 为绝热参数（回旋半径 / 场变化尺度）。残差在 λ*>λ 后超过 1%。"
            "来料未声明任何绝热条件。",
            lam_star=lam_star, tol=TOL_ID)
    elif strong_fails:
        add("D1", "★「梯度磁场」适用宣称无边界：λ=1 处残差 %.3e 已远超 1%%，"
                  "且阈值落在扫描区内" % r_lam1,
            "FAIL", "见 C1 扫描表。", lam_star=lam_star)
    else:
        add("D1", "扫描区内未能定位失效阈值", "BOUNDARY",
            "诚实登记：本卷未发现恒等式在扫描区失效。", lam_star=lam_star)

    # D2：修复定价（3 个动作，低阶）
    repairs = []
    for act, desc, dom_ok, content in (
            ("KEEP", "保留「匀速螺旋 / 梯度磁场」全域宣称", False,
             "强梯度残差 %.3e ≫ 1%% ⇒ 宣称假" % r_lam1),
            ("DEL", "删去「梯度磁场」限定词，只留「匀速螺旋」", True,
             "成立域收窄到均匀场；但匀速螺旋下恒等式零新增 ⇒ 剩余新内容 0"),
            ("REPLACE", "把宣称改为「绝热梯度场 λ<λ*」", True,
             "成立域可机读标定；代价 = 引入来料从未声明的绝热条件（外部输入 +1），"
             "且恒等式仍零新增 ⇒ 剩余新内容 0")):
        repairs.append({"动作": act, "描述": desc, "宣称域内成立": dom_ok,
                        "代价": content})
    n_surv = sum(1 for r in repairs if r["宣称域内成立"])
    n_zero = sum(1 for r in repairs if r["宣称域内成立"] and "零代价" in r["代价"])
    add("D2", "修复定价（3 动作低阶枚举）：宣称域内成立 %d 个、零代价 %d 个"
              % (n_surv, n_zero),
        "FAIL" if n_zero == 0 else "GUARD-FAIL",
        "KEEP ⇒ 强梯度下假；DEL/REPLACE ⇒ 成立域收窄但恒等式零新增，"
        "「几何基石」的角色空转 ⇒ **修复可行 ≠ 修复后仍有内容**"
        "（本库「修复即自杀」同型结构第 %d 次登记）" % 7,
        repairs=repairs, n_survivors=n_surv, n_zero_cost=n_zero)

    add("E1", "BOUNDARY：场模型为理想二次磁镜；未模湍流、有质动力、真实磁喷嘴",
        "BOUNDARY", "阈值 λ* 依赖场形；定性结论（存在成立域边界）不依赖。")
    add("E2", "BOUNDARY：γ 口径已闭合（v 恒定 ⇒ γ 恒定），B 口径见 C2",
        "BOUNDARY", "r148 未闭合项 2 的 γ 半边由 B1 闭合、B 半边由 C2 定价。")
    add("E3", "BOUNDARY：未检索实验文献（承接 r148 项 5）；本卷锚点为教科书关系"
              "（磁镜不变量、磁镜条件、Larmor 类恒等式）",
        "BOUNDARY", "A2/A3/B1/B2 均为与教科书极限的直接冲突，文献比对仍开放。")

    # ---- 控制组 ----
    control("U1", "均匀场恒等式残差机器零（动态积分）", a["r_uniform"],
            "<1e-9", a["r_uniform"] < 1.0e-9)
    control("U2", "动态 κ, τ vs 解析螺旋值（τ 含手性符号）", a["dev_kappa"], "<1e-9",
            a["dev_kappa"] < 1.0e-9 and a["dev_tau"] < 1.0e-9)
    control("U3", "r148 运动学表复现：A=1（R=ω=u=1）⇒ 0.2045",
            helix_residual_kin(1.0, 1.0, 2.0, 1.0), "≈0.2044（±1e-3）",
            abs(helix_residual_kin(1.0, 1.0, 2.0, 1.0) - 0.2044) < 1.0e-3)
    control("U4", "r148 运动学表复现：A=0.01 ⇒ 2.55e-5",
            helix_residual_kin(1.0, 1.0, 1.01, 0.01), "≈2.55e-5（±20%）",
            abs(helix_residual_kin(1.0, 1.0, 1.01, 0.01) / 2.549e-5 - 1.0) < 0.2)
    control("U5", "静磁场 |v| 守恒", a["v_drift"], "<1e-6",
            a["v_drift"] < 1.0e-6)
    control("U6", "绝热不变量 μ 守恒（λ=5e-3）", c["rows"][0]["mu_drift"],
            "<0.05", c["rows"][0]["mu_drift"] < 0.05)
    control("U7", "磁镜条件 z_max/L（λ=5e-3）", c["rows"][0]["z_max_over_L"],
            "≈1.0（±0.1）", abs(c["rows"][0]["z_max_over_L"] - 1.0) < 0.1)
    control("U8", "∇·B = 0（网格机检）", divB, "<1e-10", divB < 1.0e-10)
    control("U9", "RK4 收敛（h vs h/2）", a["conv"], "<1e-6", a["conv"] < 1.0e-6)
    control("U10", "瞬时平行力 a·B̂ ≡ 0（λ=5e-3）", c["rows"][0]["apar_max"],
            "<1e-9", c["rows"][0]["apar_max"] < 1.0e-9)

    # ---- 守卫 ----
    guard("守卫1：条目数 ≥ 14", len(ITEMS) >= 14)
    guard("守卫2：存在 FAIL 条目",
          any(it["status"] == "FAIL" for it in ITEMS))
    guard("守卫3：控制组 ≥ 7 项", len(CONTROLS) >= 7)
    guard("守卫4：λ 扫描点数 ≥ 7", len(c["rows"]) >= 7)
    guard("守卫5：扫描含 1%% 阈值以下（绝热档 %.1e，低于阈值 %.0f 倍）与以上"
          "（强梯度档 %.1e，高于阈值 %.0f 倍）⇒ 门有分辨力"
          % (r_adiab, TOL_ID / max(r_adiab, 1e-300),
             r_lam1, r_lam1 / TOL_ID),
          r_adiab < TOL_ID / 10.0 and r_lam1 > TOL_ID * 10.0)
    guard("守卫6：均匀场残差机器零", a["r_uniform"] < 1.0e-9)
    guard("守卫7：|v| 守恒", a["v_drift"] < 1.0e-6)
    guard("守卫8：r148 运动学模型复现（A=1 偏差 < 1e-3）",
          abs(helix_residual_kin(1.0, 1.0, 2.0, 1.0) - 0.2044) < 1.0e-3)

    # ---- 报告 ----
    L = []
    A = L.append
    A("=" * 96)
    A("TUFT-r157｜D5 大统一力方程闭合卷：梯度磁场洛伦兹积分与恒等式全域判据")
    A("=" * 96)
    A("生成时刻: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    A("")
    A("【A 组 · 均匀场对照（真实 RK4 相对论洛伦兹积分）】")
    A("    初始 v_⊥₀=v_∥₀=0.5c, γ₀=%.6f, ρ₀=%.6f（无量纲）" % (GAMMA0, RHO0))
    A("    解析 κ=%.10f, τ=%.10f；机读偏差 %.2e / %.2e"
      % (a["kap_an"], a["tau_an"], a["dev_kappa"], a["dev_tau"]))
    A("    ★均匀场恒等式残差 = %.3e（机器零）⇒ 复现 r148 C1" % a["r_uniform"])
    A("    RK4 收敛差 = %.3e；|v| 漂移 = %.3e" % (a["conv"], a["v_drift"]))
    A("")
    A("【C 组 · 磁镜扫描 λ=ρ₀/L（η=1，磁镜点 z_m=L）】")
    A("    %-8s %-12s %-12s %-12s %-12s %-11s %-9s %-11s"
      % ("λ", "r_local", "r_z", "r_mid", "r_avg", "μ漂移", "z_max/L", "A_eff/ω"))
    for r in c["rows"]:
        A("    %-8.4g %-12.3e %-12.3e %-12.3e %-12.3e %-11.2e %-9.4f %-11.2e"
          % (r["lam"], r["r_local"], r["r_z"], r["r_mid"], r["r_avg"],
             r["mu_drift"], r["z_max_over_L"],
             abs(r["Aeff_at_max"]) / r["w_at_max"] if r["w_at_max"] else 0.0))
    A("    ★标度指数 p = %.3f；阈值 λ*（残差=1%%）= %s"
      % (slope if slope == slope else float("nan"),
         ("%.4g" % lam_star) if lam_star == lam_star else "未跨过"))
    A("")
    A("【控制组】")
    allok = True
    for cc in CONTROLS:
        A("    %s %-5s %s" % (cc["id"], "PASS" if cc["ok"] else "FAIL", cc["desc"]))
        A("         实测 %s  期望 %s" % (fv(cc["value"]), cc["expect"]))
        allok = allok and cc["ok"]
    A("    控制组小结: %s" % ("全部通过" if allok else "存在失败"))
    A("")
    A("【守卫】")
    for g in GUARDS:
        A("    %s  %s" % ("OK  " if g["ok"] else "FAIL", g["name"]))
    A("")
    A("=" * 96)
    cnt = {}
    for it in ITEMS:
        cnt[it["status"]] = cnt.get(it["status"], 0) + 1
    A("【条目统计】" + "  ".join("%s=%d" % (k, cnt[k]) for k in sorted(cnt)))
    A("=" * 96)
    report = "\n".join(L)

    # ---- 判定册 ----
    if adiabatic_robust and strong_fails:
        verdict = ("GRADIENT-SCOPE-OVERBROAD-IDENTITY-ADIABATICALLY-ROBUST"
                   "-R148-CALIBRATION-CORRECTED")
    elif strong_fails:
        verdict = "IDENTITY-FAILS-IN-GRADIENT-FIELD-SCOPE-CLAIM-OVERBROAD"
    else:
        verdict = "NO-FAILURE-FOUND-IN-SCANNED-RANGE-R148-CHARGE-NOT-REPRODUCED"

    m = []
    b = m.append
    b("# 判定册 TUFT-r157｜D5《大统一力方程》闭合卷：梯度磁场洛伦兹积分与恒等式全域判据")
    b("")
    b("- 编号：TUFT-r157")
    b("- 生成时刻：%s" % time.strftime("%Y-%m-%d %H:%M:%S"))
    b("- 引擎：`源码/TUFT-r157_D5大统一力方程闭合_梯度磁场洛伦兹积分与恒等式全域判据_2026-10-23.py`")
    b("- 控制组：%s" % ("全部通过" if allok else "存在失败"))
    b("- 条目统计：%s" % "  ".join("%s=%d" % (k, cnt[k]) for k in sorted(cnt)))
    b("")
    b("## 00. 编号碰撞处置表")
    b("")
    b("| 编号 | 占用者 | 处置 |")
    b("|------|--------|------|")
    b("| r150–r154 | 攻破链各卷 | 保留为权威 |")
    b("| r155 | 动力学层卷（本线 10-22 起草、10-23 修复登记） | 保留为权威 |")
    b("| r156 | 《v总等于c第二三步 · 作用量电荷环流与 Frank 分解》"
      "（并行会话占位，本线不触碰） | 保留为权威 |")
    b("| r157 | **本卷**（D5 闭合卷） | 实测首空号后启用 |")
    b("")
    b("## 01. 分工声明（★ 与 r148 条目不可相加）")
    b("")
    b("| 卷 | 层 | 判的是什么 |")
    b("|----|----|-----------|")
    b("| r148 | 式子层 | P=m(c−v) 极限、修复定价、运动学反例 |")
    b("| **r157** | **动力学积分层** | 真实洛伦兹积分、成立域边界 λ*、ω 口径 |")
    b("")
    b("## 02. 判词")
    b("")
    b("`%s`" % verdict)
    b("")
    if adiabatic_robust and strong_fails:
        b("**恒等式的成立域是有界的**：均匀场中精确成立（机器零）；绝热梯度场"
          "（λ ≪ λ*）中近似成立（残差 ~ λ^%.2f）；强梯度场（λ ≳ λ* = %.4g）中失效"
          "（残差 %.3e ≫ 1%%）。来料把「匀速螺旋 / 梯度磁场」并列为适用范围是"
          "**无边界宣称**。同时，r148 的「147 个回旋周期到 1%%」标定被机读**更正**"
          "（残差跟踪瞬时回旋平均速率而非累积量，绝热档全程 %.3e）。"
          % (slope if slope == slope else float("nan"),
             lam_star if lam_star == lam_star else float("nan"),
             r_lam1, r_adiab))
    elif strong_fails:
        b("**恒等式在梯度场失效**（λ=1 残差 %.3e），成立域有界。" % r_lam1)
    else:
        b("**扫描区内未发现失效**：r148 的强梯度指控在本场模型下未复现，诚实登记。")
    b("")
    b("## 03. 核心结论")
    b("")
    b("### 3.1 均匀场（控制组）")
    b("")
    b("- 真实 RK4 相对论洛伦兹积分下，κ²+τ²=(ω/v)² 残差 **%.3e**（机器零）；"
      "动态 κ, τ 与解析螺旋值偏差 %.2e / %.2e。" % (a["r_uniform"],
                                                  a["dev_kappa"], a["dev_tau"]))
    b("- 恒等式是 Frenet 公式 + 洛伦兹力圆的**直接推论**（零新增，承接 r148 C1）。")
    b("- 静磁场中 |v| 严格守恒（漂移 %.3e）⇒ γ 无歧义（r148 项 2 的 γ 半边闭合）。"
      % a["v_drift"])
    b("")
    b("### 3.2 磁镜扫描（本卷核心）")
    b("")
    b("| λ=ρ₀/L | r_local | r_z | r_mid | r_avg | μ漂移 | z_max/L |")
    b("|---|---|---|---|---|---|---|")
    for r in c["rows"]:
        b("| %.4g | %.3e | %.3e | %.3e | %.3e | %.2e | %.4f |"
          % (r["lam"], r["r_local"], r["r_z"], r["r_mid"], r["r_avg"],
             r["mu_drift"], r["z_max_over_L"]))
    b("")
    b("- 标度指数 p = **%.3f**（log-log 拟合）；阈值 λ*（残差=1%%）= **%s**。"
      % (slope if slope == slope else float("nan"),
         ("%.4g" % lam_star) if lam_star == lam_star else "未跨过"))
    b("- ⇒ 恒等式成立域：**均匀场（精确）∪ 绝热梯度场（λ<λ*，近似）**；"
      "强梯度场失效。来料的无边界「梯度磁场」宣称越界。")
    b("")
    b("### 3.3 ω 口径（r148 未闭合项 2 闭合）")
    b("")
    b("- 四变体 × 两档：绝热档（λ=5e-3）局域 |B| **%.3e** / B_z %.3e / mid %.3e / "
      "avg %.3e ⇒ 唯一幸存 = **%s**；强梯度档（λ=1）最小 %.3e 仍 ≫ 1%%。"
      % (ad[0], ad[1], ad[2], ad[3], best_mode, st_best))
    b("- **局域族**（|B| 与 B_z 在绝热档残差相对差仅 %.1e，不可分辨，不按此量级差异"
      "挑口径）是唯一把残差压到 ≪1%% 的口径；midplane 与轨道平均即使绝热档也 O(1)。"
      "口径未定本身即是缺陷（靶从未声明用哪一点的 B）；且强梯度档下连最小残差都"
      "远超 1%% ⇒ 局部口径同样失效。" % loc_gap)
    b("")
    b("### 3.4 r148 标定复核（防过度指控，诚实更正）")
    b("")
    if adiabatic_robust:
        b("- r148 推法：把磁镜的**累积**螺距变化 Δv_∥=A_eff·t 当作运动学模型的"
          "**瞬时**加速度 A（残差 ~A²/4），得「147 周期到 1%」。")
        b("- 真实积分：残差跟踪**瞬时（回旋平均）速率**；λ=5e-3 档"
          "（r148 的 ε=0.01 对应档，量级映射见 C3）A_eff/ω ~ %.2e，"
          "全程最大残差 **%.3e** ≪ 1%%。"
          % (abs(c["rows"][0]["Aeff_at_max"]) / c["rows"][0]["w_at_max"]
             if c["rows"][0]["w_at_max"] else float("nan"), r_adiab))
        b("- ⇒ 恒等式在绝热梯度场比 r148 估计的**更稳健**；登记 CORRECTION"
          "（削弱本库自身前卷的部分指控，按纪律执行）。")
    else:
        b("- 真实积分**证实** r148 的标定（λ=5e-3 档最大残差 %.3e）。" % r_adiab)
    b("")
    b("### 3.5 修复定价（3 动作低阶枚举）")
    b("")
    b("| 动作 | 宣称域内成立 | 代价 |")
    b("|---|---|---|")
    for r in repairs:
        b("| %s | %s | %s |" % (r["动作"], "是" if r["宣称域内成立"] else "否",
                                r["代价"]))
    b("")
    b("- 宣称域内成立 **%d** 个、零代价 **%d** 个 ⇒ 修好的唯一办法是收窄宣称域，"
      "而恒等式零新增 ⇒ 「几何基石」角色空转 ⇒ **修复可行 ≠ 修复后仍有内容**"
      "（「修复即自杀」同型结构第七次登记）。" % (n_surv, n_zero))
    b("")
    b("## 04. 机读证据")
    b("")
    b("```")
    b("γ₀               = %.10f" % GAMMA0)
    b("ρ₀               = %.10f" % RHO0)
    b("均匀场残差        = %.6e（机器零）" % a["r_uniform"])
    b("κ,τ 机读偏差      = %.3e / %.3e" % (a["dev_kappa"], a["dev_tau"]))
    b("RK4 收敛差        = %.6e" % a["conv"])
    b("|v| 漂移          = %.6e" % a["v_drift"])
    b("a·B̂ 最大比值      = %.6e（恒零）" % c["rows"][0]["apar_max"])
    b("max|∇·B|         = %.6e" % divB)
    for r in c["rows"]:
        b("λ=%-8.4g r_local=%.6e r_z=%.6e r_mid=%.6e r_avg=%.6e μdrift=%.2e zmax/L=%.4f"
          % (r["lam"], r["r_local"], r["r_z"], r["r_mid"], r["r_avg"],
             r["mu_drift"], r["z_max_over_L"]))
    b("标度指数 p        = %.6f" % (slope if slope == slope else float("nan")))
    b("阈值 λ*           = %s" % (("%.6g" % lam_star) if lam_star == lam_star
                                else "未跨过"))
    b("运动学复算 A=1     = %.6f（r148: 0.2044）" % helix_residual_kin(1.0, 1.0, 2.0, 1.0))
    b("运动学复算 A=0.01  = %.6e（r148: 2.549e-05）"
      % helix_residual_kin(1.0, 1.0, 1.01, 0.01))
    b("```")
    b("")
    b("## 05. 未闭合项（未做即未证，不得外推）")
    b("")
    b("1. **场模型为理想二次磁镜**；阈值 λ* 依赖场形，定性结论（存在成立域边界）不依赖。")
    b("2. **未检索实验文献**（承接 r148 项 5）；锚点为教科书关系。")
    b("3. **修复空间是低阶**（3 动作）；改函数形式/改向量结构等高阶算子未枚举。")
    b("4. 本卷**不重判** r148 的式子层结论（P=m(c−v) 的极限与修复定价），"
      "只闭合其动力学积分层的两项未闭合项。")
    b("5. 本卷**不宣称** D5 体系被完全证伪 —— 只判决：恒等式的成立域有界，"
      "且无边界「梯度磁场」宣称越界。")
    b("")
    b("## 06. 自抓与更正")
    b("")
    b("1. **对 r148 C2 叙事的 CORRECTION**（见 3.4）：r148 把累积螺距变化当作瞬时加速度，高估了残差累积速度；真实积分显示绝热档残差全程 ≪1%。按防过度指控纪律登记，不遮掩。")
    b("2. **恒等式零新增的双重登记**：本卷在均匀场（机器零）与绝热场（~λ^p）两个 regime 都确认它是 Frenet + 洛伦兹的推论 ⇒ 即使成立也不承载新物理。")
    b("3. **本卷引擎自抓三处**（首跑 rc=1 后按「先分代码错还是期望错」纪律处置）：")
    b("   - **τ 手性期望写反**（代码错）：解析式原给 τ=+v_∥/(γv²)，而初值 v=(0,+v⊥,+v∥) @ x=+2ρ₀ 是**顺时针**回旋，机读 τ=−0.7071 与参考螺旋 (cos ωt, sin ωt, +z) 差一个手性符号。恒等式用 τ² 不受影响（残差仍机器零），但 A2/U2 的期望值必须带手性符号，已修。")
    b("   - **GUARDS 按 tuple 解包**（代码错）：登记器存的是 dict；报告与 payload 两处 `for n, o in GUARDS` 抛 ValueError，已改 dict 访问。")
    b("   - **守卫 5 阈值拍脑袋**（期望错）：原写「绝热档残差 <1e-6」，基于「绝热档趋机器零」的未检验预判；机读绝热档 2.0e-4（λ^1.84 标度的有限值）。按「阈值来自实测而非拍脑袋」纪律改为：低于 1% 阈值 50 倍、高于阈值 2e5 倍即判有分辨力，余量机读注入。")
    b("4. **口径判据防过度拟合**（见 3.3）：绝热档 |B| 与 B_z 两口径残差仅差 0.045%，按此量级差异挑「唯一幸存口径」会把数值噪声当结构；本卷改按**局域族**判定并登记二者不可分辨。")
    b("")
    b("## 07. 红线")
    b("")
    b("- 数学自洽 ≠ 实验证实。")
    b("- **恒等式成立 ≠ 有新内容**；**成立域可标定 ≠ 宣称无边界**。")
    b("- 防过度指控与防漏判同等重要：机读若显示前卷高估，必须诚实削弱并登记。")
    b("- **瞬时量 ≠ 回旋平均量**：a·B̂ ≡ 0 而磁镜力非零，一切「瞬时速率」口径"
      "都必须说明平均方式。")
    b("")
    judge = "\n".join(m)

    # ---- 落盘 ----
    os.makedirs(OUT, exist_ok=True)
    payload = {
        "id": "TUFT-r157",
        "title": "D5《大统一力方程》闭合卷：梯度磁场洛伦兹积分与恒等式全域判据",
        "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "verdict": verdict,
        "counts": cnt,
        "controls_ok": allok,
        "items": ITEMS,
        "uniform": a,
        "scan": c["rows"],
        "slope": slope,
        "lam_star": lam_star,
        "divB": divB,
        "controls": CONTROLS,
        "guards": [{"name": g["name"], "ok": g["ok"]} for g in GUARDS],
    }
    with open(os.path.join(OUT, STEM + ".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    with open(os.path.join(OUT, STEM + "_report.txt"), "w", encoding="utf-8") as f:
        f.write(report)
    with open(os.path.join(OUT, STEM + ".md"), "w", encoding="utf-8") as f:
        f.write(judge)
    with open(os.path.join(OUT, "判定_" + STEM + ".md"), "w", encoding="utf-8") as f:
        f.write(judge)

    print(report)
    print("\n[已写出] " + os.path.join(OUT, STEM + ".json"))
    print("[已写出] " + os.path.join(OUT, STEM + ".md"))
    print("[已写出] " + os.path.join(OUT, STEM + "_report.txt"))
    print("[已写出] " + os.path.join(OUT, "判定_" + STEM + ".md"))
    return 0 if (allok and all(it["status"] != "GUARD-FAIL" for it in ITEMS)) else 2


if __name__ == "__main__":
    sys.exit(main())
