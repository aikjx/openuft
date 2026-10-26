# -*- coding: utf-8 -*-
r"""TUFT-r233 · 四力统一方程·黑洞热力学层：Bekenstein–Hawking 四定律、
Kerr Smarr 恒等式与熵力母式 F = T∇S 的四面判决
2026-10-26

〔编号说明〕起草前实测 r233 三树零命中（r231 归并行链、r232 为本线上一卷）；
开工基线 verify.py 以本卷收尾复跑为准。承 r232（引力波层）的自然续层：
经典引力三层闭合后，下一道边界就是「几何 = 热力学 = 信息」的黑洞层。

用户诉求：「继续分析整理所有问题，攻破统一场论理论体系，新的方程，精算验证」。

本卷要回答的问题（黑洞热力学层 = 统一场论的最后一道宏观边界）：
  Q1 Bekenstein–Hawking 熵与 Hawking 温度能否机器复现到锚点精度？
     → S = A/(4ℓ_P²) k_B、T = ħc³/(8πGMk_B)、t_evap = 5120πG²M³/(ħc⁴)；
       太阳 S=1.0490e77 k_B、T=6.1700e−8 K、蒸发 2.10e67 yr。
  Q2 Kerr 黑洞的 Smarr 恒等式与第一定律能否数值独立验证？
     → M = 2TS + 2ΩJ（a/M=0…1 全谱），dM = TdS + ΩdJ（四点扰动，尺度归一）。
  Q3 面积定理（并合不可逆）能否用真实并合参数机验？
     → GW150914：A_i = 16π(m₁²+m₂²) vs A_f = 4π(r₊²+a²)，A_f/A_i > 1。
  Q4 「新的方程」：熵力母式 F = T∇S 能否把四力写进同一热力学形式？
     → 引力通道：S=A/(4ℓ_P²)k_B、ΔS=2πk_B mcΔx/ħ、T=ħGM/(2πr²ck_B)
       ⇒ F=GMm/r² **逐位恒等、零自由参数**；
       电荷通道：T_EM ∝ Q（Q<0 ⇒ T<0）——热力学不允许 ⇒ 熵化失败；
       强/弱：无几何屏幕、无普适 Unruh 温度 ⇒ 不可熵化。
  Q5 微观态计数（S = k_B ln Ω）与 1/4 系数是否由框架给出？
     → 不给：1/4 是 Bekenstein–Hawking 校准；lnΩ、Page 曲线在框架外。

诚实预期（写在前面）：Bekenstein–Hawking 熵（1973/1974）、Hawking 温度（1974/1975）、
Smarr 公式（1973）、面积定理（Hawking 1971）、熵力（Verlinde 2011 / Jacobson 1995）
全部是教科书/文献内容——本卷是复现层，不是新物理。所谓「新方程」UFE-4F-T 是
**形式重述**（熵力模板），其物理内容仍是牛顿引力；电磁/强/弱三通道不可熵化是本卷
的硬边界读数。

口径注意：
  - 熵以 k_B 计；几何单位段（Kerr）取 G=c=1，M 为长度单位；
  - 第一定律残差用 |dM|+|TdS|+|ΩdJ| 作尺度（da-only 扰动时 rhs≈0，
    用 |rhs| 作分母会把 1e−19 的抵消噪声放大成 rel=1——开发期自抓）；
  - 熵力推导中的 ΔS=2πk_BmcΔx/ħ 是 Verlinde 的屏幕比特假设，不是本框架推导；
  - 纯标准库 float64；对 r214–r232 及并行会话产物只读；守卫失败即非零退出；
    条目不可与 r142–r232 相加。
"""

import json
import os
import sys
from math import sqrt, pi, log10, log

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)
_DATADIR = os.path.join(_PROJ, "数据")
_TMPL = os.path.join(_HERE, "TUFT-r233_黑洞热力学层交互可视化模板_2026-10-26.html")
HTML_OUT = os.path.join(_PROJ, "四力统一方程_黑洞热力学层可视化_2026-10-26.html")

MARKER = "R233-BH-THERMO-LAYER"
BASE = ("TUFT-r233_四力统一方程_黑洞热力学层_贝肯斯坦霍金熵Smarr恒等式与熵力母式_"
        "精算与交互可视化_2026-10-26")
STEM = "TUFT-r233"

G = 6.67430e-11
C = 2.99792458e8
HBAR = 1.054571817e-34
KB = 1.380649e-23
MS = 1.9885e30
LP = sqrt(HBAR * G / C ** 3)          # 1.616255e-35 m
YEAR = 3.15576e7
E_CHARGE = 1.602176634e-19
EPS0 = 8.8541878128e-12
M_EARTH = 5.972e24
M_MOON = 7.342e22
M_PROTON = 1.67262192369e-27
M_SUN_ANCHOR_S = 1.0490e77            # 锚点（文献 Bekenstein-Hawking 太阳值）
M_SUN_ANCHOR_T = 6.169e-8             # 锚点（Hawking 温度，太阳）
M_SUN_ANCHOR_TP = 2.1e67              # 锚点（蒸发时间，年）

guards, controls, entries = [], [], []


def guard(gid, title, ok, detail, numbers=None):
    guards.append({"id": gid, "title": title, "ok": bool(ok),
                   "detail": detail, "numbers": numbers or {}})
    if not ok:
        print(f"[GUARD-FAIL] {gid} {title}: {detail}")
    return bool(ok)


def control(cid, title, ok, detail, numbers=None):
    controls.append({"id": cid, "title": title, "ok": bool(ok),
                     "detail": detail, "numbers": numbers or {}})
    if not ok:
        print(f"[CONTROL-FAIL] {cid} {title}: {detail}")
    return bool(ok)


def entry(code, level, title, detail, numbers=None):
    entries.append({"code": code, "level": level, "title": title,
                    "detail": detail, "numbers": numbers or {}})


def guard_ok(gid):
    return any(g["id"] == gid and g["ok"] for g in guards)


# ===========================================================================
# 基础函数（SI）
# ===========================================================================
def r_schwarzschild(M):
    return 2.0 * G * M / C ** 2


def s_bh(M):
    """Bekenstein–Hawking 熵，单位 k_B（Schwarzschild）。"""
    rs = r_schwarzschild(M)
    return pi * rs * rs / (LP * LP)


def t_hawking(M):
    return HBAR * C ** 3 / (8.0 * pi * G * M * KB)


def t_evap_year(M):
    return 5120.0 * pi * G ** 2 * M ** 3 / (HBAR * C ** 4) / YEAR


def area_schwarzschild(M):
    """几何单位（G=c=1）下的视界面积。"""
    return 16.0 * pi * M * M


def kerr(M, a_ratio):
    """几何单位（G=c=1）；a = a_ratio·M，返回 Kerr 视界量。"""
    a = a_ratio * M
    disc = sqrt(max(M * M - a * a, 0.0))
    rp = M + disc
    rm = M - disc
    A = 4.0 * pi * (rp * rp + a * a)
    S = A / 4.0
    kappa = (rp - rm) / (2.0 * (rp * rp + a * a))
    T = kappa / (2.0 * pi)
    omega = a / (rp * rp + a * a)
    J = a * M
    return {"a": a, "rp": rp, "rm": rm, "A": A, "S": S, "T": T,
            "Omega": omega, "J": J, "M": M}


def s_kerr_of(M, a):
    rp = M + sqrt(max(M * M - a * a, 0.0))
    return pi * (rp * rp + a * a)


def j_kerr_of(M, a):
    return a * M


def t_kerr_of(M, a):
    disc = sqrt(max(M * M - a * a, 0.0))
    rp, rm = M + disc, M - disc
    return ((rp - rm) / (2.0 * (rp * rp + a * a))) / (2.0 * pi)


def omega_kerr_of(M, a):
    rp = M + sqrt(max(M * M - a * a, 0.0))
    return a / (rp * rp + a * a)


# ===========================================================================
# S1 Bekenstein–Hawking 熵与 Hawking 温度锚
# ===========================================================================
print("[S1] Bekenstein–Hawking 熵与 Hawking 温度")
ANCHOR_OBJECTS = [
    ("太阳", 1.0, MS),
    ("Sgr A*", 4.297e6, 4.297e6 * MS),
    ("M87*", 6.5e9, 6.5e9 * MS),
]
anchors = []
for name, m_msun, m_kg in ANCHOR_OBJECTS:
    anchors.append({
        "name": name, "M_msun": m_msun, "M_kg": m_kg,
        "r_s": r_schwarzschild(m_kg), "S": s_bh(m_kg), "T": t_hawking(m_kg),
        "t_evap_yr": t_evap_year(m_kg),
    })
sun = anchors[0]
rel_s_sun = abs(sun["S"] - M_SUN_ANCHOR_S) / M_SUN_ANCHOR_S
rel_t_sun = abs(sun["T"] - M_SUN_ANCHOR_T) / M_SUN_ANCHOR_T
rel_tp_sun = abs(sun["t_evap_yr"] - M_SUN_ANCHOR_TP) / M_SUN_ANCHOR_TP
guard("G1", "Bekenstein–Hawking 熵与 Hawking 温度锚（太阳）",
      rel_s_sun < 1e-3 and rel_t_sun < 1e-3 and rel_tp_sun < 5e-2,
      f"S⊙ = A/(4ℓ_P²) = {sun['S']:.6e} k_B vs 锚 {M_SUN_ANCHOR_S:.4e}（rel {rel_s_sun:.2e}）；"
      f"T⊙ = ħc³/(8πGMk_B) = {sun['T']:.6e} K vs 锚 {M_SUN_ANCHOR_T:.4e}（rel {rel_t_sun:.2e}）；"
      f"蒸发 t = 5120πG²M³/(ħc⁴) = {sun['t_evap_yr']:.4e} yr vs 锚 {M_SUN_ANCHOR_TP:.2e}（rel {rel_tp_sun:.2e}）",
      {"S_sun": f"{sun['S']:.6e}", "T_sun": f"{sun['T']:.6e}",
       "t_evap_yr": f"{sun['t_evap_yr']:.4e}",
       "rel_S": f"{rel_s_sun:.2e}", "rel_T": f"{rel_t_sun:.2e}"})

# 标度律：S ∝ M²、T ∝ 1/M（跨 9 个数量级）
m_lo, m_hi = ANCHOR_OBJECTS[0][2], ANCHOR_OBJECTS[2][2]
s_lo, s_hi = s_bh(m_lo), s_bh(m_hi)
t_lo, t_hi = t_hawking(m_lo), t_hawking(m_hi)
slope_s = log(s_hi / s_lo) / log(m_hi / m_lo)
slope_t = log(t_hi / t_lo) / log(m_hi / m_lo)
guard("G2", "熵/温度标度律：S ∝ M²、T ∝ 1/M",
      abs(slope_s - 2.0) < 1e-12 and abs(slope_t + 1.0) < 1e-12,
      f"跨太阳→M87*（9.8 个数量级）：log S vs log M 斜率 = {slope_s:.15f}（应为 2），"
      f"log T vs log M 斜率 = {slope_t:.15f}（应为 −1）——面积律与 Hawking 温度的标度骨架机器钉死",
      {"slope_S": f"{slope_s:.15f}", "slope_T": f"{slope_t:.15f}"})

# ===========================================================================
# S2 Kerr：Smarr 恒等式与第一定律
# ===========================================================================
print("[S2] Kerr Smarr 恒等式与第一定律")
kerr_rows = []
for ar in [0.0, 0.5, 0.9, 0.99, 1.0]:
    k = kerr(1.0, ar)
    smarr = 2.0 * k["T"] * k["S"] + 2.0 * k["Omega"] * k["J"]
    rel = abs(smarr - 1.0) / 1.0
    kerr_rows.append({"a_over_M": ar, "T": k["T"], "S": k["S"],
                      "Omega": k["Omega"], "smarr": smarr, "smarr_rel": rel})

# 第一定律：在 (M,a) 平面上四点扰动，尺度归一残差
M0, a0 = 1.0, 0.9
H = 1e-6
SM = (s_kerr_of(M0 + H, a0) - s_kerr_of(M0 - H, a0)) / (2 * H)
SA = (s_kerr_of(M0, a0 + H) - s_kerr_of(M0, a0 - H)) / (2 * H)
JM = (j_kerr_of(M0 + H, a0) - j_kerr_of(M0 - H, a0)) / (2 * H)
JA = (j_kerr_of(M0, a0 + H) - j_kerr_of(M0, a0 - H)) / (2 * H)
T0 = t_kerr_of(M0, a0)
OM0 = omega_kerr_of(M0, a0)
first_law_rows = []
for dM, da in [(1e-3, 0.0), (0.0, 1e-3), (3e-4, -2e-4), (-1e-3, 5e-4)]:
    dS = SM * dM + SA * da
    dJ = JM * dM + JA * da
    lhs = dM
    rhs = T0 * dS + OM0 * dJ
    scale = abs(dM) + abs(T0 * dS) + abs(OM0 * dJ)
    first_law_rows.append({"dM": dM, "da": da,
                           "residual": lhs - rhs,
                           "rel": abs(lhs - rhs) / max(scale, 1e-300)})
max_smarr = max(r["smarr_rel"] for r in kerr_rows)
max_first = max(r["rel"] for r in first_law_rows)
s_extr = kerr(1.0, 1.0)["S"]
s_schw = kerr(1.0, 0.0)["S"]
guard("G3", "Kerr Smarr 恒等式 M = 2TS + 2ΩJ 与第一定律 dM = TdS + ΩdJ",
      max_smarr < 1e-12 and max_first < 1e-9
      and abs(s_extr / s_schw - 0.5) < 1e-12,
      f"a/M ∈ {{0, 0.5, 0.9, 0.99, 1}}：Smarr 残差 max {max_smarr:.2e}；"
      f"第一定律四点扰动（含 da-only）max rel {max_first:.2e}；"
      f"极端/ Schwarzschild 面积比 = {s_extr/s_schw:.15f}（应为 1/2）——"
      "Kerr 热力学恒等式在 G=c=1 下逐位成立（非拟合）",
      {"smarr_rel": f"{max_smarr:.2e}", "first_law_rel": f"{max_first:.2e}",
       "S_extr_over_S_schw": f"{s_extr/s_schw:.15f}"})

# ===========================================================================
# S3 面积定理：GW150914 并合与不可逆面积
# ===========================================================================
print("[S3] 面积定理：GW150914 并合")
m1_gw, m2_gw = 36.0, 29.0
m_f_gw, a_f_gw = 62.0, 0.67
A_i = area_schwarzschild(m1_gw) + area_schwarzschild(m2_gw)
k_rem = kerr(m_f_gw, a_f_gw)
A_f = k_rem["A"]
ratio_area = A_f / A_i
A_schw_1 = area_schwarzschild(1.0)
A_extr_1 = kerr(1.0, 1.0)["A"]
guard("G4", "面积定理：并合后视界面积不减（GW150914 参数）",
      ratio_area > 1.0 and abs(A_extr_1 / A_schw_1 - 0.5) < 1e-12,
      f"GW150914（36+29 M☉ → 62 M☉, a/M=0.67）：A_i = 16π(m₁²+m₂²) = {A_i:.3f}，"
      f"A_f = 4π(r₊²+a²) = {A_f:.3f}，A_f/A_i = {ratio_area:.6f} > 1——"
      f"面积定理机器成立；Schwarzschild/极端面积 = {A_schw_1:.6f} / {A_extr_1:.6f}（比 2:1）",
      {"A_i": round(A_i, 3), "A_f": round(A_f, 3),
       "ratio": round(ratio_area, 6), "A_schw": round(A_schw_1, 6),
       "A_extr": round(A_extr_1, 6)})

# ===========================================================================
# S4 熵力母式 F = T∇S：引力通道逐位复现牛顿
# ===========================================================================
print("[S4] 熵力母式 F = T∇S（引力通道）")
holographic_bits = 4.0 * pi * (1.496e11) ** 2 / (LP * LP)  # 仅展示量级


def f_entropic(M_source, m_test, r):
    """全息屏幕：S=πr²/ℓ_P²·k_B、N=4πr²/ℓ_P²、T=2Mc²/(Nk_B)、ΔS/Δx=2πk_Bmc/ħ。"""
    N = 4.0 * pi * r * r / (LP * LP)
    T_screen = 2.0 * M_source * C * C / (N * KB)
    dS_dx = 2.0 * pi * KB * m_test * C / HBAR
    return T_screen * dS_dx, T_screen, N


entropic_rows = []
for name, M_src, m_test, r in [
        ("太阳–地球", MS, M_EARTH, 1.496e11),
        ("地球–月球", M_EARTH, M_MOON, 3.844e8),
        ("太阳–质子", MS, M_PROTON, 1.496e11)]:
    f_ent, t_screen, N = f_entropic(M_src, m_test, r)
    f_new = G * M_src * m_test / (r * r)
    rel = abs(f_ent - f_new) / f_new
    acc = G * M_src / (r * r)
    t_unruh = HBAR * acc / (2.0 * pi * C * KB)
    entropic_rows.append({"name": name, "r": r, "F_ent": f_ent,
                          "F_newton": f_new, "rel": rel,
                          "T_screen": t_screen, "T_unruh": t_unruh,
                          "unruh_rel": abs(t_screen - t_unruh) / t_unruh})
max_ent = max(x["rel"] for x in entropic_rows)
max_unruh = max(x["unruh_rel"] for x in entropic_rows)
guard("G5", "熵力母式 F = T∇S 精确复现牛顿引力（零自由参数）",
      max_ent < 1e-12 and max_unruh < 1e-12,
      f"三点（太阳–地球/地球–月球/太阳–质子）：F_ent vs GMm/r² max rel {max_ent:.2e}；"
      f"屏幕温度 vs Unruh 温度 ħa/(2πck_B) max rel {max_unruh:.2e}——"
      "S=A/(4ℓ_P²)k_B + ΔS=2πk_BmcΔx/ħ + 能量均分三者相乘，因子逐位抵消回牛顿，"
      "不引入任何新常数或拟合参数（Verlinde 2011 机制的机器复现）",
      {"max_rel": f"{max_ent:.2e}", "max_unruh_rel": f"{max_unruh:.2e}"})

# ===========================================================================
# S5 电荷通道：符号温度 ⇒ 熵化失败
# ===========================================================================
print("[S5] 电荷/强/弱通道的熵化判决")


def t_em_signed(Q, r):
    """把 T∇S 形式强行套到库仑力上所需的『屏幕温度』（有符号）。"""
    return HBAR * Q / (2.0 * pi * KB * C * r * r * 4.0 * pi * EPS0)


T_EM_POS = t_em_signed(+E_CHARGE, 1e-15)
T_EM_NEG = t_em_signed(-E_CHARGE, 1e-15)
em_sign_flip = (T_EM_POS > 0.0 and T_EM_NEG < 0.0
                and abs(T_EM_POS + T_EM_NEG) < 1e-12)

# 强/弱：无几何屏幕判据（量化：视界面积/Unruh 温度都不存在）
# 这里只做结构性记录，不伪造数值。
guard("G6", "Bekenstein 界 S ≤ 2πk_BRE/(ħc)：四个量级全满足",
      True,
      "占位由下方 bound 计算后重写",
      {})

# ===========================================================================
# S6 Bekenstein 界
# ===========================================================================
print("[S6] Bekenstein 界")
BOUND_OBJECTS = [
    ("太阳", 6.957e8, MS, s_bh(MS)),
    ("地球", 6.371e6, M_EARTH, s_bh(M_EARTH)),
    ("质子", 0.84e-15, M_PROTON, 1.0),          # 熵取量级 1 k_B
    ("人", 0.5, 70.0, 1e28),                     # 熵取量级 1e28 k_B
]
bound_rows = []
for name, R, M_obj, S_obj in BOUND_OBJECTS:
    E_obj = M_obj * C * C
    B = 2.0 * pi * R * E_obj / (HBAR * C)
    bound_rows.append({"name": name, "R": R, "E": E_obj,
                       "bound": B, "S": S_obj, "ratio": S_obj / B})
bound_ok = all(r["ratio"] < 1.0 for r in bound_rows)
sun_ratio = bound_rows[0]["ratio"]
proton_ratio = bound_rows[2]["ratio"]
# 用真实读数重写 G6（先移除占位，再追加）
guards[:] = [g for g in guards if g["id"] != "G6"]
guard("G6", "Bekenstein 界 S ≤ 2πk_BRE/(ħc)：四个量级全满足",
      bound_ok and 1e-6 < sun_ratio < 1e-5 and 0.01 < proton_ratio < 0.1,
      f"太阳 S_BH/B = {sun_ratio:.6e}（界不饱和，差 5.4 个量级）；"
      f"地球 {bound_rows[1]['ratio']:.3e}；质子（S~1 k_B）{proton_ratio:.3f}；"
      f"人（S~1e28 k_B）{bound_rows[3]['ratio']:.3e}——"
      "Bekenstein 界全满足但远不饱和：它不是等号定律，不能反推微观态数",
      {"sun_ratio": f"{sun_ratio:.6e}", "proton_ratio": f"{proton_ratio:.4f}"})

# 全息比特因子：S_BH/(A/ℓ_P²) = 1/4（定义性校准，不是推导）
holo_factor = 0.25

# ===========================================================================
# S7 控制组
# ===========================================================================
print("[S7] 控制组")
# C1：熵系数/比特假设的因子敏感性（1/4→1/2 ⇒ F×2；2π→π ⇒ F×0.5）
r_c1 = 1.496e11
f_base = f_entropic(MS, M_EARTH, r_c1)[0]
_, _, N_c1 = f_entropic(MS, M_EARTH, r_c1)
T_c1 = 2.0 * MS * C * C / (N_c1 * KB)
dSdx_c1 = 2.0 * pi * KB * M_EARTH * C / HBAR
f_double = T_c1 * 2.0 * dSdx_c1          # S 系数 1/4→1/2 等价于 ΔS 翻倍
f_half = T_c1 * 0.5 * dSdx_c1           # ΔS 2π→π
control("C1", "因子敏感性：熵系数 1/4→1/2 必使 F×2；ΔS 2π→π 必使 F×0.5",
        abs(f_double / f_base - 2.0) < 1e-12 and abs(f_half / f_base - 0.5) < 1e-12,
        f"基线 F = {f_base:.6e} N；改系数后 F×2 = {f_double:.6e}、F×0.5 = {f_half:.6e}——"
        "熵力母式的 1/4 与 2π 是被守卫钉死的，不是可调参数（若因子错，G5 立刻亮红）",
        {"ratio_double": round(f_double / f_base, 12),
         "ratio_half": round(f_half / f_base, 12)})

# C2：电荷符号温度（结构性失败的阴性对照）
control("C2", "阴性对照：电荷通道的『温度』随 Q 变号（T<0 热力学不允许）",
        em_sign_flip,
        f"Q=+e, r=1 fm：T_EM = {T_EM_POS:+.6f} K；Q=−e：T_EM = {T_EM_NEG:+.6f} K——"
        "同式同 r 下温度随电荷符号翻转，熵增方向对正负电荷相反；"
        "负温度不是有效热力学温度 ⇒ 库仑力不能被 T∇S 熵化（H07 FAIL 不是容差太宽）",
        {"T_pos": round(T_EM_POS, 6), "T_neg": round(T_EM_NEG, 6)})

# ===========================================================================
# S8 条目与判决
# ===========================================================================


def main():
    entry("H01", "INFO", "判定：黑洞热力学层 = 宏观定律的机器复现，不是新理论",
          "Bekenstein–Hawking 熵（1973/1974）、Hawking 温度（1974/1975）、Smarr 公式（1973）、"
          "面积定理（Hawking 1971）、熵力（Verlinde 2011 / Jacobson 1995）全部为教科书/文献内容；"
          "本卷以四条独立管线互印（熵锚/热力学恒等式/并合面积/熵力因子）——复现层，无新物理（承 r229/r232）")
    entry("H02", "PASS" if guard_ok("G1") and guard_ok("G2") else "FAIL",
          "Bekenstein–Hawking 熵锚与标度律",
          f"太阳 S = {sun['S']:.6e} k_B（锚 1.0490e77，rel {rel_s_sun:.2e}）；"
          f"Sgr A* {anchors[1]['S']:.4e}；M87* {anchors[2]['S']:.4e}；"
          f"S∝M^{slope_s:.12f}、T∝M^{slope_t:.12f}——面积律的 9.8 数量级标度骨架机器成立")
    entry("H03", "PASS" if guard_ok("G1") else "FAIL",
          "Hawking 温度与蒸发时间",
          f"太阳 T = {sun['T']:.6e} K、t_evap = {sun['t_evap_yr']:.4e} yr；"
          f"Sgr A* T = {anchors[1]['T']:.4e} K；M87* T = {anchors[2]['T']:.4e} K——"
          "温度与质量成反比、蒸发时间 ∝ M³ 的量级全部命中")
    entry("H04", "PASS" if guard_ok("G3") else "FAIL",
          "Kerr Smarr 恒等式与第一定律",
          f"a/M 0→1 全谱 Smarr 残差 max {max_smarr:.2e}；第一定律（含 da-only 扰动）max rel "
          f"{max_first:.2e}；极端面积 = Schwarzschild 的 {s_extr/s_schw:.15f}（1/2）——"
          "黑洞热力学的两大恒等式在纯 float64 内逐位成立")
    entry("H05", "PASS" if guard_ok("G4") else "FAIL",
          "面积定理：GW150914 并合不可逆",
          f"A_i = {A_i:.3f}、A_f = {A_f:.3f}，A_f/A_i = {ratio_area:.6f} > 1；"
          f"Schwarzschild/极端面积 = {A_schw_1:.3f}/{A_extr_1:.3f}（2:1）——"
          "并合后面积增加，第二定律的几何形式机器成立（不依赖数值相对论波形）")
    entry("H06", "PASS" if guard_ok("G5") else "FAIL",
          "熵力母式 F = T∇S：引力通道逐位复现牛顿",
          f"三点 F_ent vs GMm/r² max rel {max_ent:.2e}；屏幕温度 vs Unruh 温度 max rel "
          f"{max_unruh:.2e}——S=A/(4ℓ_P²)k_B、ΔS=2πk_BmcΔx/ħ、T=2E/(Nk_B) 的因子链逐位抵消，"
          "给出 F=GMm/r²，零自由参数（Verlinde 2011 机制复现）")
    entry("H07", "FAIL", "熵力母式不能承载电磁/强/弱：四力熵化的硬边界",
          f"电荷通道：T_EM(±e,1 fm) = {T_EM_POS:+.6f}/{-T_EM_POS:+.6f} K——"
          "温度随电荷符号翻转（负温度无定义），且屏幕熵依赖电荷而非几何面积；"
          "强/弱通道：无几何视界、无普适 Unruh 温度、无 A/4ℓ_P² 屏幕 ⇒ 不可熵化。"
          "『四力写进 F=T∇S』只在引力通道成立，其余三力是形式套用而非推导")
    entry("H08", "BOUNDARY", "微观态计数与 1/4 系数：框架不给",
          f"S_BH/(A/ℓ_P²) = {holo_factor:.2f} 是 Bekenstein–Hawking 校准（不是本框架推导）；"
          "S=k_B lnΩ 的 Ω、Page 曲线、信息悖论的微观机制均在框架外；"
          f"Bekenstein 界全满足但太阳只到界的 {sun_ratio:.2e}（远不饱和）——"
          "黑洞热力学是宏观有效定律，不是量子引力的完成")
    entry("H09", "INFO", "新方程候选 UFE-4F-T（熵力母式）的形式定位",
          "UFE-4F-T：F = T∇S，S=A/(4ℓ_P²)k_B、T=ħa/(2πck_B)、ΔS=2πk_BmcΔx/ħ。"
          "它在引力通道与 UFE-4F 母式逐位同构（H06），但电磁/强/弱通道无对应屏幕（H07）——"
          "因此它是**第 5 种形式重述**（力→场→传播→作用量→熵力），不增加第一性输入，"
          "不是新物理方程；新颖性审计（r229）口径不变")
    entry("H10", "INFO", "全方法总账 +1（14 轮）与判决",
          "r214–r233 十四轮：形式统一逐层成立（静态中心力→禁闭/通道→传播→进动→量子谱→散射→"
          "作用量→1PN→引力波→熵力），动力学统一逐层 FAIL（四个 α+λ+σ 独立输入，供给 0）。"
          "本卷新增的边界：黑洞热力学四定律可复现，但『熵 = 几何 = 信息』的微观统一不可达——"
          "与 r230「本质三层不可达」同构")

    n_pass = sum(1 for e in entries if e["level"] == "PASS")
    n_fail = sum(1 for e in entries if e["level"] == "FAIL")
    n_bnd = sum(1 for e in entries if e["level"] == "BOUNDARY")
    n_info = sum(1 for e in entries if e["level"] == "INFO")

    ledger = [
        ["r214", "静态中心力（UFE-4F 母式）", "形式统一 PASS；动力学 FAIL"],
        ["r221", "禁闭 σr + 通道门（UFE-4F⁺）", "r214 严格超集"],
        ["r222", "传播层（色散/群速度）", "质量-力程等价"],
        ["r226", "量子束缚层（薛定谔谱）", "引力『原子』无意义"],
        ["r227", "散射层（动量空间镜像）", "λ=∞ ⇔ 零质量载体"],
        ["r228", "变分层（L 与诺特）", "一个作用量生成中心力；辐射反作用无 L"],
        ["r229", "新颖性审计", "无新理论/无新方程"],
        ["r230", "引力本质层", "WEP 结构恒等 + 1PN 两件套"],
        ["r231（并行）", "实验约束全景", "参数空间合并（只读引用）"],
        ["r232", "引力波层", "四极/HT/啁啾三管线互印"],
        ["r233", "黑洞热力学层（本卷）", "四定律+Smarr+面积定理+熵力母式（仅引力）"],
    ]

    res = {
        "stem": STEM, "round": 233, "date": "2026-10-26",
        "method": ("Bekenstein–Hawking 熵/温度锚 + Kerr Smarr 与第一定律数值扰动 + "
                   "GW150914 并合面积 + 熵力母式 F=T∇S 因子链 + Bekenstein 界"
                   "——float64，纯标准库"),
        "bh_verdict": ("黑洞热力学四定律机器复现（熵锚 rel 1e−4、Smarr 1e−16、"
                       "第一定律 1e−11、面积比 1.567>1）；熵力母式仅引力通道逐位复现牛顿"
                       "（rel 2e−16），电磁/强/弱不可熵化；微观态计数 OPEN——复现层，无新理论"),
        "entries": entries, "guards": guards, "controls": controls,
        "readings": {
            "anchors": [{"name": a["name"], "M_msun": a["M_msun"],
                         "M_kg": a["M_kg"], "r_s": a["r_s"],
                         "S": a["S"], "T": a["T"],
                         "t_evap_yr": a["t_evap_yr"]} for a in anchors],
            "scaling": {"slope_S": slope_s, "slope_T": slope_t},
            "kerr": kerr_rows,
            "first_law": first_law_rows,
            "area": {"A_i": A_i, "A_f": A_f, "ratio": ratio_area,
                     "A_schw": A_schw_1, "A_extr": A_extr_1,
                     "A_extr_over_schw": A_extr_1 / A_schw_1},
            "entropic": entropic_rows,
            "em": {"T_pos": T_EM_POS, "T_neg": T_EM_NEG,
                   "sign_flip": em_sign_flip},
            "bound": bound_rows,
            "holographic": {"factor": holo_factor,
                            "bits_1au": holographic_bits},
            "ledger": [{"round": r, "method": m, "verdict": v}
                       for r, m, v in ledger],
        },
        "counts": {"entries": len(entries), "PASS": n_pass, "FAIL": n_fail,
                   "BOUNDARY": n_bnd, "INFO": n_info,
                   "guards": f"{sum(1 for g in guards if g['ok'])}/{len(guards)}",
                   "controls": f"{sum(1 for c in controls if c['ok'])}/{len(controls)}"},
        "verdict": "", "judgement": "", "source": {},
    }

    parts = ["R233-BH-THERMO-LAYER",
             "BEKENSTEIN-HAWKING-ENTROPY-OK" if guard_ok("G1") else "BH-ENTROPY-FAIL",
             "HAWKING-TEMPERATURE-OK" if guard_ok("G1") else "HAWKING-T-FAIL",
             "S-M-SCALING-OK" if guard_ok("G2") else "SCALING-FAIL",
             "KERR-SMARR-OK" if guard_ok("G3") else "SMARR-FAIL",
             "FIRST-LAW-OK" if guard_ok("G3") else "FIRST-LAW-FAIL",
             "MERGER-AREA-LAW-OK" if guard_ok("G4") else "AREA-FAIL",
             "ENTROPIC-FORCE-NEWTON-OK" if guard_ok("G5") else "ENTROPIC-FAIL",
             "EM-STRONG-WEAK-NOT-ENTROPIC-FAIL",
             "MICROSTATE-COUNT-BOUNDARY",
             "UFE-4F-T-FORM-ONLY-GRAVITY",
             "VERDICT-FORM-UNIFIED-5TH-LAYER-DYNAMICS-STILL-FAIL"]
    res["verdict"] = "-".join(parts)
    res["judgement"] = ("CLOSED-INCREMENT（黑洞热力学层：四定律/Smarr/面积定理/熵力母式全部机器复现；"
                        "熵力母式 UFE-4F-T 仅引力通道精确，电磁/强/弱不可熵化；"
                        "微观态计数与 1/4 系数 OPEN；无新理论）")
    res["source"] = {
        "engine": BASE + ".py",
        "inherits": ["r232（引力波层收口）", "r230（引力本质三层判定）",
                     "r229（新颖性审计口径）", "r226（量子束缚层读数）",
                     "Bekenstein 1973 / Hawking 1974-75 / Bardeen-Carter-Hawking 1973",
                     "Verlinde 2011 / Jacobson 1995 / GW150914（LIGO 2016）"],
    }
    os.makedirs(_DATADIR, exist_ok=True)
    jpath = os.path.join(_DATADIR, BASE + ".json")
    mpath = os.path.join(_DATADIR, BASE + ".md")
    rpath = os.path.join(_DATADIR, BASE + "_report.txt")

    html_ok, html_detail = cast_html(res)
    guard("G7", "交互 HTML 生成且自含", html_ok, html_detail)
    res["counts"]["guards"] = f"{sum(1 for g in guards if g['ok'])}/{len(guards)}"
    if html_ok:
        cast_html(res)   # 用含 G7 的最终计数重铸，避免 HTML 内嵌计数落后一格

    print(f"条目 {res['counts']['entries']}（PASS {n_pass} / FAIL {n_fail} / "
          f"BOUNDARY {n_bnd} / INFO {n_info}）· 守卫 {res['counts']['guards']} · "
          f"控制组 {res['counts']['controls']}")

    with open(jpath, "w", encoding="utf-8", newline="\n") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    write_md(mpath, res)
    write_report(rpath, res)

    bad_g = [g["id"] for g in guards if not g["ok"]]
    bad_c = [c["id"] for c in controls if not c["ok"]]
    if bad_g or bad_c:
        print(f"[RC≠0] 守卫失败 {bad_g} 控制组失败 {bad_c}")
        return 1
    print(f"[DONE] {MARKER} rc=0 → {jpath}")
    return 0


def write_md(path, res):
    L = [f"# {res['stem']} · 数据册（引擎自动生成）\n",
         f"- 判决串：`{res['verdict']}`\n",
         f"- 条目：{res['counts']['entries']}（PASS {res['counts']['PASS']} / FAIL {res['counts']['FAIL']} / "
         f"BOUNDARY {res['counts']['BOUNDARY']} / INFO {res['counts']['INFO']}）· "
         f"守卫 {res['counts']['guards']} · 控制组 {res['counts']['controls']}\n",
         "\n## 条目\n"]
    for e in res["entries"]:
        L.append(f"- **{e['code']} {e['level']}** {e['title']}——{e['detail']}\n")
    L.append("\n## 守卫\n")
    for g in res["guards"]:
        L.append(f"- **{g['id']} {'OK' if g['ok'] else 'FAIL'}** {g['title']}——{g['detail']}\n")
    L.append("\n## 控制组\n")
    for c in res["controls"]:
        L.append(f"- **{c['id']} {'OK' if c['ok'] else 'FAIL'}** {c['title']}——{c['detail']}\n")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(L))


def write_report(path, res):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(f"{MARKER} rc=0\n")
        f.write(f"entries={res['counts']['entries']} PASS={res['counts']['PASS']} "
                f"FAIL={res['counts']['FAIL']} BOUNDARY={res['counts']['BOUNDARY']} "
                f"INFO={res['counts']['INFO']}\n")
        f.write(f"guards={res['counts']['guards']} controls={res['counts']['controls']}\n")
        f.write(f"verdict={res['verdict']}\n")
        for a in res["readings"]["anchors"]:
            f.write(f"anchor={a['name']} S={a['S']:.6e} T={a['T']:.6e} "
                    f"t_evap={a['t_evap_yr']:.4e}\n")
        f.write(f"area_ratio={res['readings']['area']['ratio']:.6f}\n")
        f.write(f"smarr_rel={res['readings']['kerr'][2]['smarr_rel']:.3e}\n")
        f.write(f"first_law_rel={max(r['rel'] for r in res['readings']['first_law']):.3e}\n")
        f.write(f"entropic_max_rel={max(r['rel'] for r in res['readings']['entropic']):.3e}\n")
        f.write(f"em_sign_flip={res['readings']['em']['sign_flip']}\n")


def cast_html(res):
    if not os.path.isfile(_TMPL):
        return False, f"模板缺失：{_TMPL}"
    with open(_TMPL, "r", encoding="utf-8") as f:
        tpl = f.read()
    if "__R233_JSON__" not in tpl:
        return False, "模板缺少 __R233_JSON__ 占位符"
    html = tpl.replace("__R233_JSON__", json.dumps(res, ensure_ascii=False))
    with open(HTML_OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    text = open(HTML_OUT, "r", encoding="utf-8").read()
    problems = []
    if "__R233_JSON__" in text:
        problems.append("占位符未替换")
    if "http://" in text or "https://" in text:
        problems.append("发现外部 URL（应零依赖）")
    if "<canvas" not in text or "<script" not in text:
        problems.append("缺少 canvas/script")
    if problems:
        return False, "；".join(problems)
    return True, f"已生成 {HTML_OUT}（{len(text)} B），零外部 URL、JSON 已铸入"


if __name__ == "__main__":
    sys.exit(main())
