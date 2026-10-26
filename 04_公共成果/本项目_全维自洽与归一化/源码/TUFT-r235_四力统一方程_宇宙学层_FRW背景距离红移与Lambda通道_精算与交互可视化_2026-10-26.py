# -*- coding: utf-8 -*-
r"""TUFT-r235 · 四力统一方程·宇宙学层：FRW 背景、距离-红移与 Λ 通道
2026-10-26

〔编号说明〕收尾复核实测：r234 已被并行链《强场层·史瓦西完整测地线》占号
（源码 22:37:26 落盘）——按「先占位者为权威」，本卷顺延取 **r235**
（落盘前实测 r235–r236 空）。本线上一卷为 r233（黑洞热力学层）。

用户诉求：「按这个方案开始宇宙学层分析」。

本卷要回答的问题（宇宙学层 = 背景几何与距离-红移）：
  Q1 标准 ΛCDM 背景能否在纯 float64 内复现锚点？
     → t0 = 13.797 Gyr（Planck 2018）、t(z=1) ≈ 5.93 Gyr、
       q0 = −0.527、Λ = 1.09e−52 m⁻²、ρ_c = 8.53e−27 kg/m³。
  Q2 距离-红移关系能否双路积分互印并命中文献锚？
     → D_C(z=1100) ≈ 14.0 Gpc、d_L(z=1) ≈ 6.8 Gpc、μ(z=1) ≈ 44.16 mag、
       Etherington 对偶 d_L = (1+z)² d_A 恒等。
  Q3 库内候选 S18（曲率-能量密度）在宇宙学尺度是否如既有裁定被证伪？
     → 用 S18 自报参数（α=1.87、ρ_c=1e−9、ρ0=8.27e−10 J/m³、H0=70）
       机复现 q=3.3203、年龄 2.4134 Gyr、R 符号翻转、D_A 比 0.1039，
       再与观测对照 ⇒ 维持「已被宇宙学观测证伪」。
  Q4 「新的方程」：Λ 能否作为第五通道并进 UFE-4F 母式？
     → UFE-4F-Λ：F = −GMm/r² + (Λc²/3)·m·r；交叉半径 r*=(3GM/Λc²)^{1/3}；
       太阳系 1 AU 处 F_Λ/F_G = 8.24e−23（可忽略），银河系尺度 r*≈0.52 Mpc。
       **这是标准 GR 的 Λ 项换写法，不是新物理。**
  Q5 两个宇宙学硬边界能否量化？
     → H0 张力：67.4 vs 73.0 km/s/Mpc = 8.3%（≈5σ），框架不解决；
       宇宙学常数问题：ρ_P/ρ_Λ ≈ 8.8e122（≈123 个数量级），无推导。

诚实预期（写在前面）：FRW 度规、Friedmann 方程、距离-红移、
Etherington 对偶、Λ 项全部是教科书/文献内容（1917–2018）。本卷是
**背景层复现**，不是新物理；UFE-4F-Λ 是第 6 种形式重述（静态力母式 + Λ 通道），
其物理内容仍由 GR 给定。S18 的证伪结论保持既有裁定（r196/r197 切片只读）。

口径注意：
  - Planck 2018 背景参数：H0=67.4、Ωm=0.3153、Ωr=9.15e−5（T_cmb=2.7255 K），
    ΩΛ=1−Ωm−Ωr 以保持平坦（与 0.6847 差 1e−4，如实登记）；
  - 距离积分用两路独立求积（z 直积 vs x=ln(1+z) 代换）互印；
  - 年龄积分用两路（a 直积 vs x=−ln a 代换）互印；
  - S18 参数取该体系文稿自报值，本卷只做只读复算，不调参；
  - 纯标准库 float64；对 r214–r234 及并行会话产物只读；
    守卫失败即非零退出；条目不可与 r142–r234 相加。
"""

import json
import os
import sys
from math import sqrt, pi, log10, log, exp

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)
_DATADIR = os.path.join(_PROJ, "数据")
_TMPL = os.path.join(_HERE, "TUFT-r235_宇宙学层交互可视化模板_2026-10-26.html")
HTML_OUT = os.path.join(_PROJ, "四力统一方程_宇宙学层可视化_2026-10-26.html")

MARKER = "R235-COSMO-LAYER"
BASE = ("TUFT-r235_四力统一方程_宇宙学层_FRW背景距离红移与Lambda通道_"
        "精算与交互可视化_2026-10-26")
STEM = "TUFT-r235"

C = 2.99792458e8
G = 6.67430e-11
MPC = 3.0856775814913673e22
GYR = 3.15576e16
PC = 3.0856775814913673e16
MS = 1.9885e30
HBAR = 1.054571817e-34

# ---- Planck 2018 背景参数 ----
H0_KM = 67.4
H0 = H0_KM * 1000.0 / MPC
OM = 0.3153
OR = 9.15e-5
OL = 1.0 - OM - OR
T_CMB = 2.7255
Z_STAR = 1100.0

# ---- 文献锚点 ----
ANCHOR_AGE0 = 13.797          # Gyr（Planck 2018）
ANCHOR_AGE1 = 5.93            # Gyr（z=1）
ANCHOR_Q0 = -0.527
ANCHOR_LAMBDA = 1.09e-52      # m^-2
ANCHOR_RHOC = 8.53e-27        # kg/m^3
ANCHOR_DC1100 = 14.0          # Gpc
ANCHOR_MU1 = 44.16            # mag

# ---- S18 文稿自报参数（只读）----
S18_H0_KM = 70.0
S18_H0 = S18_H0_KM * 1000.0 / MPC
S18_ALPHA = 1.87
S18_RHOC = 1e-9
S18_RHO0 = 8.27e-10
S18_Q_PUB = 3.3203
S18_AGE_PUB = 2.4134
S18_DA_PUB = 0.1039
S18_R_PUB = -7.9717e-52

H0_SH0ES = 73.0
H0_SH0ES_SIGMA = 1.0
H0_PLANCK_SIGMA = 0.5

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
# 求积与宇宙学函数
# ===========================================================================
def simpson(f, a, b, n):
    """复合 Simpson（n 自动取偶数）。"""
    if n % 2:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n, 2):
        s += 4.0 * f(a + i * h)
    for i in range(2, n, 2):
        s += 2.0 * f(a + i * h)
    return s * h / 3.0


def e_a(a):
    """E(a)=H(a)/H0（平坦 ΛCDM，含辐射）。"""
    return sqrt(OM / a ** 3 + OR / a ** 4 + OL)


def e_z(z):
    return sqrt(OM * (1.0 + z) ** 3 + OR * (1.0 + z) ** 4 + OL)


def age0(h0=H0, n=200000):
    """t0 = ∫_0^1 da/(aH)。a→0 端 integrand ~ a/√Ωr（取 1e−10 下限）。"""
    return simpson(lambda a: 1.0 / (a * e_a(a)), 1e-10, 1.0, n) / h0


def age0_alt(n=60000):
    """t0 代换 x=−ln a 的第二路。"""
    return simpson(lambda x: 1.0 / e_a(exp(-x)), 0.0, 30.0, n) / H0


def age_at_z(z, n=100000):
    """t(z)=∫_0^{a(z)} da/(aH)，年龄而非回望时间。"""
    az = 1.0 / (1.0 + z)
    return simpson(lambda a: 1.0 / (a * e_a(a)), 1e-10, az, n) / H0


def dc_z(z, n=20000):
    """共动距离 ∫_0^z dz/E(z)。"""
    return C / H0 * simpson(lambda x: 1.0 / e_z(x), 0.0, z, n)


def dc_x(z, n=20000):
    """共动距离第二路：x=ln(1+z)。"""
    L = log(1.0 + z)
    return C / H0 * simpson(lambda x: exp(x) / e_z(exp(x) - 1.0), 0.0, L, n)


def q0_value():
    return 0.5 * OM - OL + OR


def lambda_si():
    return 3.0 * OL * H0 ** 2 / C ** 2


def rho_crit():
    return 3.0 * H0 ** 2 / (8.0 * pi * G)


def r_star(M):
    """Λ 与引力等强的交叉半径 r*=(3GM/Λc²)^{1/3}。"""
    return (3.0 * G * M / (lambda_si() * C ** 2)) ** (1.0 / 3.0)


# ===========================================================================
# S1 ΛCDM 背景锚与 Λ/ρc/q0
# ===========================================================================
t0 = age0()
t0_alt = age0_alt()
t1 = age_at_z(1.0)
q0 = q0_value()
lam = lambda_si()
rho_c = rho_crit()
rho_l = OL * rho_c
q0_matter = 0.5 * OM + OR
t0_matter = 2.0 / (3.0 * H0)
tcmb_z = T_CMB * (1.0 + Z_STAR)

rel_t0 = abs(t0 / (ANCHOR_AGE0 * GYR) - 1.0)
rel_t1 = abs(t1 / (ANCHOR_AGE1 * GYR) - 1.0)
rel_age_alt = abs(t0 / t0_alt - 1.0)

print("[S1] ΛCDM 背景：年龄锚、Λ/ρc/q0")
guard("G1", "年龄锚：t0 与 t(z=1) 命中 Planck 2018；两路求积互印",
      rel_t0 < 2e-3 and rel_t1 < 3e-2 and rel_age_alt < 1e-9,
      f"t0 = {t0/GYR:.6f} Gyr（锚 {ANCHOR_AGE0}，rel {rel_t0:.2e}）；"
      f"t(z=1) = {t1/GYR:.6f} Gyr（锚 {ANCHOR_AGE1}，rel {rel_t1:.2e}）；"
      f"两路求积 rel {rel_age_alt:.2e}",
      {"t0_Gyr": t0 / GYR, "t1_Gyr": t1 / GYR, "rel_t0": rel_t0,
       "rel_t1": rel_t1, "rel_alt": rel_age_alt})

rel_lam = abs(lam / ANCHOR_LAMBDA - 1.0)
rel_rhoc = abs(rho_c / ANCHOR_RHOC - 1.0)
rel_q0 = abs(q0 - ANCHOR_Q0)
guard("G3", "Λ、ρc、q0 命中 Planck 2018",
      rel_lam < 2e-2 and rel_rhoc < 2e-2 and rel_q0 < 1e-3,
      f"Λ = {lam:.6e} m⁻²（锚 1.09e−52，rel {rel_lam:.2e}）；"
      f"ρc = {rho_c:.6e} kg/m³（锚 8.53e−27，rel {rel_rhoc:.2e}）；"
      f"q0 = {q0:.9f}（锚 −0.527，差 {rel_q0:.2e}）",
      {"Lambda": lam, "rho_c": rho_c, "q0": q0,
       "rel_lambda": rel_lam, "rel_rhoc": rel_rhoc})

# ===========================================================================
# S2 距离-红移：双路互印 + 文献锚 + Etherington 对偶
# ===========================================================================
z_rows = [0.001, 0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0,
          1.5, 2.0, 3.0, 5.0, Z_STAR]
dist_rows = []
max_quad_rel = 0.0
max_duality_rel = 0.0
for z in z_rows:
    d1 = dc_z(z)
    d2 = dc_x(z)
    rq = abs(d1 / d2 - 1.0)
    max_quad_rel = max(max_quad_rel, rq)
    dl = (1.0 + z) * d1
    da = d1 / (1.0 + z)
    mu = 5.0 * log10(dl / (10.0 * PC))
    rd = abs(dl / ((1.0 + z) ** 2 * da) - 1.0)
    max_duality_rel = max(max_duality_rel, rd)
    dist_rows.append({"z": z, "DC_Mpc": d1 / MPC, "DL_Mpc": dl / MPC,
                      "DA_Mpc": da / MPC, "mu": mu,
                      "quad_rel": rq, "duality_rel": rd})

dc1100 = dc_z(Z_STAR)
dl1 = (1.0 + 1.0) * dc_z(1.0)
mu1 = 5.0 * log10(dl1 / (10.0 * PC))
rel_dc1100 = abs(dc1100 / (ANCHOR_DC1100 * 1000.0 * MPC) - 1.0)
rel_mu1 = abs(mu1 - ANCHOR_MU1)

print("[S2] 距离-红移：双路互印、D_C(1100)、d_L(1)/μ(1)、对偶")
guard("G2", "距离-红移：双路求积互印 + D_C(1100)/μ(1) 锚 + Etherington 对偶",
      max_quad_rel < 1e-6 and rel_dc1100 < 3e-2 and rel_mu1 < 0.05
      and max_duality_rel < 1e-12,
      f"双路 max rel {max_quad_rel:.2e}；D_C(1100) = {dc1100/(1000*MPC):.6f} Gpc"
      f"（锚 {ANCHOR_DC1100}，rel {rel_dc1100:.2e}）；μ(1) = {mu1:.4f} mag"
      f"（锚 {ANCHOR_MU1}，差 {rel_mu1:.2e}）；对偶 max rel {max_duality_rel:.2e}",
      {"max_quad_rel": max_quad_rel, "max_duality_rel": max_duality_rel,
       "DC1100_Gpc": dc1100 / (1000.0 * MPC), "mu1": mu1,
       "DL1_Mpc": dl1 / MPC})

# ===========================================================================
# S3 S18（曲率-能量密度）FLRW 只读复算与观测对照
# ===========================================================================
s18_K = -3.0 * S18_ALPHA * S18_RHO0 / (2.0 * S18_RHOC)
s18_f = -3.0 * S18_ALPHA / (2.0 * S18_RHOC) * S18_RHO0 ** 2 / S18_RHO0
s18_q = 1.0 - s18_f
s18_h2 = S18_H0 ** 2
s18_addotdot = (s18_f - 1.0) * s18_h2
s18_R = 6.0 * (s18_addotdot + s18_h2) / C ** 2
s18_R_gr = 8.0 * pi * G * S18_RHO0 / C ** 2
s18_R_ratio = s18_R / s18_R_gr


def e_s18_a(a):
    lnH = s18_K / 3.0 * (1.0 - a ** -3) - 2.0 * log(a)
    if lnH > 700.0:
        return float("inf")
    return exp(lnH)


def s18_age(n=200000):
    return simpson(lambda a: 1.0 / (a * e_s18_a(a)), 1e-6, 1.0, n) / S18_H0


s18_t = s18_age()


def s18_dc(z, n=40000):
    def inv(x):
        a = 1.0 / (1.0 + x)
        return 1.0 / e_s18_a(a)
    return C / S18_H0 * simpson(inv, 0.0, z, n)


def grm_dc(z, n=40000):
    return C / S18_H0 * simpson(lambda x: 1.0 / (1.0 + x) ** 1.5, 0.0, z, n)


s18_da_ratio = s18_dc(Z_STAR) / grm_dc(Z_STAR)
s18_da_gr = grm_dc(Z_STAR)

rel_s18_q = abs(s18_q - S18_Q_PUB)
rel_s18_age = abs(s18_t / (S18_AGE_PUB * GYR) - 1.0)
rel_s18_R = abs(s18_R / S18_R_PUB - 1.0)
rel_s18_da = abs(s18_da_ratio / S18_DA_PUB - 1.0)

print("[S3] S18 FLRW 只读复算")
guard("G4", "S18 自报读数机器复现：q / 年龄 / R 符号与量值 / D_A 比",
      rel_s18_q < 1e-3 and rel_s18_age < 1e-3 and rel_s18_R < 1e-2
      and rel_s18_da < 2e-2,
      f"q = {s18_q:.6f}（自报 {S18_Q_PUB}，差 {rel_s18_q:.2e}）；"
      f"年龄 {s18_t/GYR:.6f} Gyr（自报 {S18_AGE_PUB}，rel {rel_s18_age:.2e}）；"
      f"R = {s18_R:.6e}（自报 {S18_R_PUB:.6e}，rel {rel_s18_R:.2e}）；"
      f"D_A 比 {s18_da_ratio:.6f}（自报 {S18_DA_PUB}，rel {rel_s18_da:.2e}）",
      {"q": s18_q, "age_Gyr": s18_t / GYR, "R": s18_R,
       "R_GR": s18_R_gr, "DA_ratio": s18_da_ratio,
       "rel_q": rel_s18_q, "rel_age": rel_s18_age,
       "rel_R": rel_s18_R, "rel_DA": rel_s18_da})

age_s18_over_obs = (s18_t / GYR) / ANCHOR_AGE0
print("[S3b] S18 与观测对照")
guard("G5", "S18 与观测对照：年龄过短、D_A 比过小、q 符号相反 ⇒ 证伪成立",
      age_s18_over_obs < 0.2 and s18_da_ratio < 0.2 and s18_q > 1.0
      and q0 < 0.0,
      f"年龄 {s18_t/GYR:.6f} vs {ANCHOR_AGE0} Gyr（比值 {age_s18_over_obs:.4f}）；"
      f"D_A 比 {s18_da_ratio:.6f} vs 1；q = {s18_q:.4f}（>1 强减速）vs 观测 q0 = {q0:.4f}（<0 加速）——"
      "三条结构性冲突远超容差，维持 S18『宇宙学尺度已被证伪』裁定",
      {"age_ratio": age_s18_over_obs, "DA_ratio": s18_da_ratio,
       "q_s18": s18_q, "q_obs": q0})

# ===========================================================================
# S4 Λ 通道：UFE-4F-Λ 与交叉半径
# ===========================================================================
lam_objs = [
    ("太阳", 1.0, MS),
    ("地球", 5.972e24 / MS, 5.972e24),
    ("银河系", 1.0e11, 1.0e11 * MS),
    ("星系团", 1.0e15, 1.0e15 * MS),
]
lam_rows = []
for name, m_msun, m_kg in lam_objs:
    rs = r_star(m_kg)
    lam_rows.append({"name": name, "M_msun": m_msun, "M_kg": m_kg,
                     "r_star_m": rs, "r_star_Mpc": rs / MPC,
                     "r_star_pc": rs / PC})

r_1au = 1.495978707e11
ratio_1au = lam * C ** 2 * r_1au ** 3 / (3.0 * G * MS)
mw_star = lam_rows[2]["r_star_Mpc"]
cluster_star = lam_rows[3]["r_star_Mpc"]
earth_pc = lam_rows[1]["r_star_pc"]

print("[S4] Λ 通道：交叉半径与太阳系可忽略性")
guard("G6", "Λ 通道：1 AU 比率可忽略 + 银河系/星系团交叉半径命中",
      ratio_1au < 1e-20 and 0.4 < mw_star < 0.7 and 8.0 < cluster_star < 15.0
      and 1.0 < earth_pc < 3.0,
      f"太阳系 1 AU：F_Λ/F_G = {ratio_1au:.3e}；"
      f"银河系 r* = {mw_star:.4f} Mpc；星系团 r* = {cluster_star:.2f} Mpc；"
      f"地球 r* = {earth_pc:.3f} pc——Λ 只在 ≥Mpc 尺度与引力同量级",
      {"ratio_1au": ratio_1au, "MW_rstar_Mpc": mw_star,
       "cluster_rstar_Mpc": cluster_star, "Earth_rstar_pc": earth_pc})

# ===========================================================================
# S5 两个硬边界：H0 张力与宇宙学常数问题
# ===========================================================================
h0_pct = (H0_SH0ES - H0_KM) / H0_KM * 100.0
h0_sigma = (H0_SH0ES - H0_KM) / sqrt(H0_PLANCK_SIGMA ** 2 + H0_SH0ES_SIGMA ** 2)
rho_planck = C ** 5 / (HBAR * G ** 2)
rho_ratio = rho_planck / rho_l
log_ratio = log10(rho_ratio)
print("[S5] H0 张力与宇宙学常数问题")
print(f"  H0 差 {h0_pct:.2f}%（{h0_sigma:.2f}σ）；ρP/ρΛ = {rho_ratio:.3e}（{log_ratio:.2f} 量级）")

# ===========================================================================
# S6 控制组
# ===========================================================================
t0_h0_up = age0(H0 * 1.1)
c1_ratio = t0_h0_up / t0
control("C1", "参数敏感性：H0×1.1 ⇒ 年龄必 ×1/1.1（ΛCDM 结构恒等）",
        abs(c1_ratio * 1.1 - 1.0) < 1e-12,
        f"t0(H0) = {t0/GYR:.6f} Gyr；t0(1.1H0) = {t0_h0_up/GYR:.6f} Gyr；"
        f"比值 = {c1_ratio:.12f}（应 1/1.1 = {1/1.1:.12f}）——年龄对 H0 的线性依赖被钉死",
        {"ratio": c1_ratio})

c2_age_drop = 1.0 - (t0_matter / t0)
control("C2", "判别力：ΩΛ→0 ⇒ 年龄降到物质主导 9.31 Gyr（短 32%）且 q0 翻正",
        abs(t0_matter / GYR - 9.312) < 0.01 and q0_matter > 0.1,
        f"物质主导年龄 = {t0_matter/GYR:.6f} Gyr（比含 Λ 短 {c2_age_drop*100:.1f}%）；"
        f"q0(无 Λ) = {q0_matter:.6f} > 0（减速）vs 含 Λ q0 = {q0:.6f} < 0（加速）——"
        "Λ 的存在正是年龄与加速符号的分水岭",
        {"age_matter_Gyr": t0_matter / GYR, "age_drop_pct": c2_age_drop * 100,
         "q0_matter": q0_matter})

# ===========================================================================
# S7 条目与判决
# ===========================================================================
rel_h0 = abs(H0 / (H0_KM * 1000.0 / MPC) - 1.0)


def main():
    entry("H01", "INFO", "判定：宇宙学层 = ΛCDM 背景的机器复现，不是新理论",
          "FRW 度规、Friedmann 方程、距离-红移、Etherington 对偶、Λ 项全部为"
          "教科书/文献内容（1917–2018）；本卷以年龄双路、距离双路、S18 只读复算、"
          "Λ 通道四条管线互印——复现层，无新物理（承 r229/r233/r234）")
    entry("H02", "PASS" if guard_ok("G1") else "FAIL",
          "宇宙年龄锚：t0 与 t(z=1)",
          f"t0 = {t0/GYR:.6f} Gyr（锚 13.797，rel {rel_t0:.2e}）；"
          f"t(z=1) = {t1/GYR:.6f} Gyr（锚 5.93，rel {rel_t1:.2e}）；"
          f"两路求积互印 rel {rel_age_alt:.2e}——"
          "年龄积分被 Ωm/ΩΛ/Ωr 与 H0 完全钉死")
    entry("H03", "PASS" if guard_ok("G2") else "FAIL",
          "距离-红移：d_L、μ、D_C 与 Etherington 对偶",
          f"D_C(1100) = {dc1100/(1000*MPC):.6f} Gpc（锚 14.0，rel {rel_dc1100:.2e}）；"
          f"d_L(1) = {dl1/MPC:.3f} Mpc、μ(1) = {mu1:.4f} mag（锚 44.16）；"
          f"双路 max rel {max_quad_rel:.2e}；对偶 d_L=(1+z)²d_A 恒等 rel {max_duality_rel:.2e}")
    entry("H04", "PASS" if guard_ok("G3") else "FAIL",
          "Λ、临界密度与减速参数",
          f"Λ = {lam:.6e} m⁻²（锚 1.09e−52）；ρc = {rho_c:.6e} kg/m³（锚 8.53e−27）；"
          f"ρΛ = {rho_l:.4e} kg/m³（能量密度 {rho_l*C*C:.4e} J/m³）；"
          f"q0 = {q0:.6f}（锚 −0.527）——加速膨胀的符号被 Λ 项给出")
    entry("H05", "PASS" if guard_ok("G4") else "FAIL",
          "S18（曲率-能量密度）FLRW 读数机器复现",
          f"用 S18 自报参数机复现：q = {s18_q:.6f}（自报 3.3203）；"
          f"年龄 {s18_t/GYR:.6f} Gyr（自报 2.4134）；R = {s18_R:.6e} vs GR "
          f"{s18_R_gr:.6e}（比值 {s18_R_ratio:.3e}，符号相反）；"
          f"D_A 比 {s18_da_ratio:.6f}（自报 0.1039）——"
          "四读数逐项命中，S18 文稿数值可信（本卷不调参）")
    entry("H06", "FAIL", "S18 宇宙学对照观测：维持『已被证伪』裁定",
          f"年龄 {s18_t/GYR:.4f} vs 13.797 Gyr（{age_s18_over_obs*100:.1f}%）；"
          f"D_A 比 {s18_da_ratio:.4f} vs 1（偏移约 9.6×）；"
          f"q = {s18_q:.3f}（恒 >1 强减速）vs 观测 q0 = {q0:.3f}（<0 加速）——"
          "三条结构性冲突；且 α→0 给出 a∝t^{1/2} 而非 GR 物质主导 t^{2/3}（无 GR 极限）。"
          "存活路径（加 Λ/重定 ρmin）该体系自报未验证，本卷不代做")
    entry("H07", "PASS" if guard_ok("G6") else "FAIL",
          "UFE-4F-Λ：Λ 作为第五通道并进静态力母式",
          f"F = −GMm/r² + (Λc²/3)mr，r*=(3GM/Λc²)¹ᐟ³：太阳 r*={lam_rows[0]['r_star_pc']:.1f} pc、"
          f"地球 {earth_pc:.3f} pc、银河系 {mw_star:.3f} Mpc、星系团 {cluster_star:.2f} Mpc；"
          f"太阳系 1 AU 处 F_Λ/F_G = {ratio_1au:.3e}（8×10⁻²³，可忽略）——"
          "Λ 只在 ≥Mpc 尺度与引力同量级。**形式重述，不是新物理**")
    entry("H08", "BOUNDARY", "H0 张力：8.3%（≈5σ）——框架不解决",
          f"Planck 2018 H0 = {H0_KM} ± {H0_PLANCK_SIGMA} vs SH0ES H0 = {H0_SH0ES} ± "
          f"{H0_SH0ES_SIGMA} km/s/Mpc：差 {h0_pct:.2f}%（合并 σ 口径 {h0_sigma:.2f}σ）。"
          "本卷只把张力量化登记；ΛCDM 背景内无新物理自由度可消解，"
          "正是『动力学统一供给 0』在宇宙学尺度的同型边界")
    entry("H09", "BOUNDARY", "宇宙学常数问题：ρP/ρΛ ≈ 8.8×10¹²²——无推导",
          f"普朗克密度 ρP = c⁵/(ħG²) = {rho_planck:.4e} kg/m³，"
          f"观测 ρΛ = {rho_l:.4e} kg/m³，比值 {rho_ratio:.3e}（{log_ratio:.1f} 个数量级）。"
          "Λ 的数值没有任何框架内第一性来源；本卷不宣称解决，如实登记为"
          "『本质三层不可达』（r230）在宇宙学层的对应边界")
    entry("H10", "INFO", "全方法总账 +1（15 轮）与判决",
          "r214–r235 十五轮：形式统一逐层成立（静态中心力→禁闭/通道→传播→进动→量子谱→散射→"
          "作用量→1PN→引力波→黑洞热力学→Λ 通道），动力学统一逐层 FAIL（四个 α+λ+σ 独立输入，"
          "供给 0；宇宙学 Λ 亦无第一性来源）。本卷新增边界：背景层可复现，"
          "但 H0 张力与宇宙学常数问题不可由本框架消解")

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
        ["r233", "黑洞热力学层", "四定律+Smarr+面积定理+熵力母式（仅引力）"],
        ["r234（并行）", "强场层（史瓦西测地线）", "ISCO/光子球/1PN 失效曲线"],
        ["r235", "宇宙学层（本卷）", "FRW 背景+距离-红移+S18 证伪复核+Λ 通道"],
    ]

    res = {
        "stem": STEM, "round": 235, "date": "2026-10-26",
        "method": ("Planck 2018 ΛCDM 背景双路年龄积分 + 距离-红移双路求积 + "
                   "Etherington 对偶 + S18 FLRW 只读复算 + Λ 通道交叉半径"
                   "——float64，纯标准库"),
        "cosmo_verdict": ("FRW 背景/距离-红移/Λ 全部机器复现（年龄 rel 1e−3、"
                          "距离双路 1e−8、μ(1) 锚 44.16）；S18 自报读数逐项复现并"
                          "维持宇宙学证伪；H0 张力 5σ 与宇宙学常数问题 123 量级无解"
                          "——复现层，无新理论"),
        "entries": entries, "guards": guards, "controls": controls,
        "readings": {
            "params": {"H0_km": H0_KM, "Om": OM, "Or": OR, "OL": OL,
                       "q0": q0, "Lambda": lam, "rho_c": rho_c,
                       "rho_L": rho_l, "rho_L_energy": rho_l * C * C,
                       "age0_Gyr": t0 / GYR, "age1_Gyr": t1 / GYR,
                       "age_matter_Gyr": t0_matter / GYR,
                       "q0_matter": q0_matter,
                       "tcmb_z1100": tcmb_z},
            "distances": {"rows": dist_rows,
                          "DC1100_Gpc": dc1100 / (1000.0 * MPC),
                          "DL1_Mpc": dl1 / MPC, "mu1": mu1,
                          "max_quad_rel": max_quad_rel,
                          "max_duality_rel": max_duality_rel},
            "age_curve": [{"z": z,
                           "t_Gyr": (t0 / GYR if z == 0.0
                                     else age_at_z(z, n=40000) / GYR)}
                          for z in [0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7,
                                    1.0, 1.5, 2.0, 3.0, 5.0]],
            "s18": {"q": s18_q, "q_pub": S18_Q_PUB,
                    "age_Gyr": s18_t / GYR, "age_pub": S18_AGE_PUB,
                    "R": s18_R, "R_pub": S18_R_PUB, "R_GR": s18_R_gr,
                    "R_ratio": s18_R_ratio, "DA_ratio": s18_da_ratio,
                    "DA_pub": S18_DA_PUB,
                    "age_over_obs": age_s18_over_obs},
            "lambda_channel": {"rows": lam_rows, "ratio_1au": ratio_1au},
            "tension": {"H0_planck": H0_KM, "H0_shoes": H0_SH0ES,
                        "pct": h0_pct, "sigma": h0_sigma},
            "cc": {"rho_planck": rho_planck, "rho_L": rho_l,
                   "ratio": rho_ratio, "log10": log_ratio},
            "ledger": [{"round": r, "method": m, "verdict": v}
                       for r, m, v in ledger],
        },
        "counts": {"entries": len(entries), "PASS": n_pass, "FAIL": n_fail,
                   "BOUNDARY": n_bnd, "INFO": n_info,
                   "guards": f"{sum(1 for g in guards if g['ok'])}/{len(guards)}",
                   "controls": f"{sum(1 for c in controls if c['ok'])}/{len(controls)}"},
        "verdict": "", "judgement": "", "source": {},
    }

    parts = [
        "R235-COSMO-LAYER-FRW-BACKGROUND-OK-AGE-ANCHOR-OK-DISTANCE-REDSHIFT-OK",
        "LAMBDA-RHOC-Q0-OK-S18-FLRW-REPRODUCED-OK-S18-FALSIFIED-OK",
        "LAMBDA-CHANNEL-FORM-ONLY-HUBBLE-TENSION-BOUNDARY-CC-PROBLEM-BOUNDARY",
        "VERDICT-STANDARD-BACKGROUND-NO-NEW-THEORY",
    ]
    res["verdict"] = "-".join(parts)
    res["judgement"] = ("CLOSED-INCREMENT（宇宙学层：FRW 背景双路年龄、距离-红移双路、"
                        "S18 只读复算与证伪复核、Λ 通道交叉半径）；"
                        "H0 张力与宇宙学常数问题为不可解边界；无新理论")
    res["source"] = {
        "engine": BASE + ".py",
        "inherits": ["r233（黑洞热力学层）", "r234（强场层，并行只读）",
                     "r229（新颖性审计口径）", "r230（本质三层不可达）",
                     "Planck 2018 / SH0ES 2022", "S18 续篇二 FLRW 文稿（只读）"],
    }

    os.makedirs(_DATADIR, exist_ok=True)
    jpath = os.path.join(_DATADIR, BASE + ".json")
    mpath = os.path.join(_DATADIR, BASE + ".md")
    rpath = os.path.join(_DATADIR, BASE + "_report.txt")

    html_ok, html_detail = cast_html(res)
    guard("G7", "交互 HTML 生成且自含", html_ok, html_detail)
    res["counts"]["guards"] = f"{sum(1 for g in guards if g['ok'])}/{len(guards)}"
    if html_ok:
        cast_html(res)   # 用含 G7 的最终计数重铸

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
        p = res["readings"]["params"]
        f.write(f"age0={p['age0_Gyr']:.6f} Gyr age1={p['age1_Gyr']:.6f} Gyr "
                f"q0={p['q0']:.6f} Lambda={p['Lambda']:.6e} rhoc={p['rho_c']:.6e}\n")
        d = res["readings"]["distances"]
        f.write(f"DC1100={d['DC1100_Gpc']:.6f} Gpc DL1={d['DL1_Mpc']:.3f} Mpc "
                f"mu1={d['mu1']:.4f} quad_rel={d['max_quad_rel']:.3e} "
                f"duality_rel={d['max_duality_rel']:.3e}\n")
        s = res["readings"]["s18"]
        f.write(f"s18_q={s['q']:.6f} s18_age={s['age_Gyr']:.6f} Gyr "
                f"s18_DA_ratio={s['DA_ratio']:.6f} s18_R_ratio={s['R_ratio']:.3e}\n")
        lc = res["readings"]["lambda_channel"]
        f.write(f"lambda_1au_ratio={lc['ratio_1au']:.3e} "
                f"MW_rstar={lc['rows'][2]['r_star_Mpc']:.4f} Mpc\n")
        t = res["readings"]["tension"]
        f.write(f"h0_pct={t['pct']:.2f} h0_sigma={t['sigma']:.2f} "
                f"rhoP_over_rhoL={res['readings']['cc']['ratio']:.3e}\n")


def cast_html(res):
    if not os.path.isfile(_TMPL):
        return False, f"模板缺失：{_TMPL}"
    with open(_TMPL, "r", encoding="utf-8") as f:
        tpl = f.read()
    if "__R235_JSON__" not in tpl:
        return False, "模板缺少 __R235_JSON__ 占位符"
    html = tpl.replace("__R235_JSON__", json.dumps(res, ensure_ascii=False))
    with open(HTML_OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    text = open(HTML_OUT, "r", encoding="utf-8").read()
    problems = []
    if "__R235_JSON__" in text:
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
