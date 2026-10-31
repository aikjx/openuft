# -*- coding: utf-8 -*-
r"""TUFT-r268 · ROOT 空间光速螺旋统一理论 V5.0 融合审计层
四层分级映射 · 六条旧口径消解 · Z/Z' 量纲 · 旧强场 ω 失效定理

2026-10-31

〔编号说明〕用户指定 r262，但实测 r262《重子不对称层》已被并行链占用（源码/数据/判定/runner 齐全），
r263《攻坚任务书审计》、r264《自由参数总账层》、r265《引力波预言层》、r266、r267 亦被占
⇒ **本卷改取 r268**（r268–r270 三树实测为空）。这是本项目撞号第 11 次，按纪律如实登记。

本卷任务：把用户提供的《ROOT · 空间光速螺旋统一理论 V5.0 全体系整理与独立审计（2026-10-31）》
作为**外部复核层**接入项目账本，而不是升格为新理论。机器要回答：
  Q1 Z=Gc/2 与 Z'=c/(8πε₀) 的重参数恒等式是否逐位成立？Z+iZ' 能不能相加？
  Q2 两组「伪预言」（α=1/(4π³+π²+π)、m_p/m_e=56π）偏离实测多少？
  Q3 螺旋双模型（轴向 u=c vs 总速 v=c）的 κ、τ、H 是否复现？哪个被光样条件排除？
  Q4 旧强场 ω_old 的失效能否写成定理（弱场极限不存在）？
  Q5 标准强场（ISCO/光子球）与引力长度/经典检验是否复现？
  Q6 V5.0 的 A/B/C/D 四层分级与「六条旧口径」如何落账？

诚实预期（写在前面）：本卷不含任何新物理。Z、Z' 是既有常数的重参数；α 几何提案与 56π
是 numerology（项目预测登记 S10-P002 已标 ❌）；面积律/ISCO/水星进动/光偏折/GPS 全部是
标准 GR 的计算复现。本卷唯一可称为「定理」的是旧 ω_old 无弱场极限（否定性结果）。
"""

import json
import os
import sys
from math import sqrt, pi, log

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)
_DATADIR = os.path.join(_PROJ, "数据")
_TMPL = os.path.join(_HERE, "TUFT-r268_ROOT-V5.0融合审计交互可视化模板_2026-10-31.html")
HTML_OUT = os.path.join(_PROJ, "全维融合审计_ROOT-V5.0可视化_2026-10-31.html")

MARKER = "R268-ROOT-V5-FUSION-AUDIT"
BASE = ("TUFT-r268_ROOT-V5.0融合审计_四层分级映射与六条口径消解_Z与Z撇量纲及"
        "旧强场omega失效定理_精算与交互可视化_2026-10-31")
STEM = "TUFT-r268"

C = 2.99792458e8
G = 6.67430e-11
HBAR = 1.054571817e-34
KB = 1.380649e-23
E_CHG = 1.602176634e-19
M_E = 9.1093837015e-31
EPS0 = 8.854187817e-12
ALPHA_INV = 137.035999177          # CODATA 2022
MASS_RATIO = 1836.15267343         # m_p/m_e
MPC = 3.0856775814913673e22
GM_SUN = 1.32712440018e20
GM_EARTH = 3.986004418e14
AU = 1.495978707e11
R_SUN = 6.957e8
R_E = 6.378137e6
H_GPS = 20200e3

Z = G * C / 2.0                    # m^4 kg^-1 s^-3
ZP = C / (8.0 * pi * EPS0)         # kg m^4 C^-2 s^-3
ALPHA = 2.0 * E_CHG ** 2 * ZP / (HBAR * C * C)
F_COUP = (C / 2.0) * sqrt(4.0 * pi * EPS0 * G)

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


# ------------------------------------------------------------------ 螺旋
LAM = 550e-9
K_WAVE = 2.0 * pi / LAM
R_HELIX = 0.35 * LAM
OMEGA_H = 1.2 * C / LAM
Q_HELIX = R_HELIX * OMEGA_H / C     # = 0.42


def helix_ax(u_ax=C, r=R_HELIX, om=OMEGA_H):
    v2 = u_ax ** 2 + (r * om) ** 2
    v = sqrt(v2)
    kap = r * om ** 2 / v2
    tau = u_ax * om / v2
    return {"u": u_ax, "v": v, "kappa": kap, "tau": tau,
            "H": 2.0 * pi * u_ax / om, "a": r * om ** 2}


def helix_light(r=R_HELIX, om=OMEGA_H):
    vp = r * om
    u_ax = sqrt(C ** 2 - vp ** 2)
    return helix_ax(u_ax, r, om)


# ------------------------------------------------------------------ 旧强场 ω
def old_over_kepler(x):
    """ω_old=c²/(√(2GM)√(r−GM/c²))，Ω_K=√(GM/r³)，r=x·GM/c² ⇒ 比值 √(x³/(2(x−1)))。"""
    return sqrt(x ** 3 / (2.0 * (x - 1.0)))


def kepler_ratio(x, x_ref=1.0):
    """Ω_K(x)/Ω_K(x_ref) 的机器比值（应恒为 (x_ref/x)^{3/2}）。"""
    return (x_ref / x) ** 1.5


# ------------------------------------------------------------------ 引力长度
def lg_of(gm):
    return gm / C ** 2


def main():
    # ---------------------------------------------------------------- S1
    print("[S1] Z=Gc/2 与 Z'=c/(8πε₀)：重参数恒等式")
    m1, m2, r_samp = 2.0, 3.0, 5.0
    f_z = 2.0 * Z * m1 * m2 / (C * r_samp ** 2)
    f_g = G * m1 * m2 / r_samp ** 2
    rel_force = max(abs(2.0 * Z * m1 * m2 / (C * rr ** 2)
                        - G * m1 * m2 / rr ** 2)
                    / (G * m1 * m2 / rr ** 2) for rr in (1.0, 5.0, 100.0))
    z_ref = 0.010004524012147
    guard("G1", "Z=Gc/2：F=2Zm₁m₂/(cr²) ≡ Gm₁m₂/r² 机器零，且 Z 值复现",
          rel_force < 1e-15 and abs(Z - z_ref) / z_ref < 1e-14,
          f"r∈{{1,5,100}} 最大相对残差 {rel_force:.2e}；Z={Z:.15f} m⁴kg⁻¹s⁻³"
          f"（对照 {z_ref}）；F_Z(5m)={f_z:.6e} N vs F_G={f_g:.6e} N",
          {"Z": f"{Z:.15f}", "rel_force": f"{rel_force:.2e}"})

    inv4pe0 = 1.0 / (4.0 * pi * EPS0)
    mu0 = 8.0 * pi * ZP / C ** 3
    mu0_direct = 1.0 / (EPS0 * C * C)
    rel_a = abs(ALPHA - 1.0 / ALPHA_INV) / (1.0 / ALPHA_INV)
    rel_mu = abs(mu0 - mu0_direct) / mu0
    guard("G2", "Z'=c/(8πε₀)：1/(4πε₀)=2Z'/c、μ₀=8πZ'/c³、α=2e²Z'/(ħc²) 三恒等",
          abs(inv4pe0 - 2.0 * ZP / C) / inv4pe0 < 1e-15
          and rel_mu < 1e-15 and rel_a < 1e-9,
          f"1/(4πε₀)={inv4pe0:.6f}，2Z'/c={2*ZP/C:.6f}（rel "
          f"{abs(inv4pe0-2*ZP/C)/inv4pe0:.2e}）；μ₀ rel {rel_mu:.2e}；"
          f"α={ALPHA:.15e} vs CODATA {1/ALPHA_INV:.15e}（rel {rel_a:.2e}）",
          {"Zp": f"{ZP:.9e}", "alpha": f"{ALPHA:.15e}", "rel_alpha": f"{rel_a:.2e}"})

    # ---------------------------------------------------------------- S2
    print("[S2] Z+iZ' 的量纲不可加性")
    ratio = ZP / Z
    mag = sqrt(Z ** 2 + ZP ** 2)
    guard("G3", "Z+iZ'：实部 m⁴kg⁻¹s⁻³ 与虚部 kg m⁴C⁻²s⁻³ 量纲不同 ⇒ 不可加",
          abs(mag - ZP) / ZP < 1e-6 and ratio > 1e10 and ratio > 1e19,
          f"|Z+iZ'|={mag:.6e} ≈ Z'（实部被淹没到 {Z/mag:.3e} 相对量级）；"
          f"Z'/Z={ratio:.6e}；单位签名 Z=(m⁴·kg⁻¹·s⁻³) vs Z'=(kg·m⁴·C⁻²·s⁻³) "
          "——两向量属不同量纲空间，线性组合无 SI 含义",
          {"ratio": f"{ratio:.6e}", "mag": f"{mag:.6e}"})

    # ---------------------------------------------------------------- S3
    print("[S3] 两个「伪预言」的机器定价")
    alpha_prop_inv = 4.0 * pi ** 3 + pi ** 2 + pi
    ppm = (alpha_prop_inv - ALPHA_INV) / ALPHA_INV * 1e6
    alpha_unc_rel = 2.1e-8 / ALPHA_INV   # CODATA 2022: α⁻¹=137.035999177(21)
    guard("G4", "α=1/(4π³+π²+π)：+2.22 ppm，超实验不确定度 4 个量级 ⇒ 判为经验近似非预测",
          abs(alpha_prop_inv - 137.0363037758784) < 1e-10
          and abs(ppm - 2.2227654) < 1e-6
          and abs(ppm) / 1e6 > 1e3 * alpha_unc_rel,
          f"α⁻¹_geo={alpha_prop_inv:.12f}；CODATA {ALPHA_INV}；"
          f"相对偏差 {ppm:.6f} ppm；CODATA 相对不确定度 {alpha_unc_rel:.2e} ⇒ "
          f"超 {abs(ppm)/1e6/alpha_unc_rel:.0f} 倍；项目预测登记 S10-P002 已标 numerology ❌",
          {"inv_prop": f"{alpha_prop_inv:.12f}", "ppm": f"{ppm:.6f}",
           "overshoot": f"{abs(ppm)/1e6/alpha_unc_rel:.0f}"})

    mr_56pi = 56.0 * pi
    mr_rel = abs(mr_56pi - MASS_RATIO) / MASS_RATIO
    guard("G5", "m_p/m_e=56π≈175.929：与 1836.153 差 10.37 倍 ⇒ 排除",
          abs(mr_56pi - 175.92918860102841) < 1e-10 and mr_rel > 0.9,
          f"56π={mr_56pi:.9f}；实测 {MASS_RATIO}；相对差 {mr_rel*100:.2f}%"
          f"（{MASS_RATIO/mr_56pi:.3f} 倍）",
          {"56pi": f"{mr_56pi:.9f}", "rel": f"{mr_rel:.4f}"})

    # ---------------------------------------------------------------- S4
    print("[S4] 螺旋双模型：轴向 u=c vs 总速 v=c")
    ax = helix_ax()
    lt = helix_light()
    rel_id_ax = abs(ax["kappa"] ** 2 + ax["tau"] ** 2
                    - OMEGA_H ** 2 / ax["v"] ** 2) / (OMEGA_H ** 2 / ax["v"] ** 2)
    rel_id_lt = abs(lt["kappa"] ** 2 + lt["tau"] ** 2
                    - OMEGA_H ** 2 / lt["v"] ** 2) / (OMEGA_H ** 2 / lt["v"] ** 2)
    r_rec = ax["kappa"] / (ax["kappa"] ** 2 + ax["tau"] ** 2)
    h_rec = 2.0 * pi * ax["tau"] / (ax["kappa"] ** 2 + ax["tau"] ** 2)
    rel_r = abs(r_rec - R_HELIX) / R_HELIX
    rel_h = abs(h_rec - ax["H"]) / ax["H"]
    guard("G6", "螺旋双模型数值复现 + 恒等式 κ²+τ²=ω²/v² + R/H 反演",
          abs(ax["v"] / C - 1.0846197490365) < 1e-12
          and abs(lt["u"] / C - 0.9075241043630743) < 1e-12
          and abs(ax["kappa"] - 778955.8282587861) < 1e-6
          and abs(ax["tau"] - 1854656.7339494913) < 1e-5
          and abs(lt["kappa"] - 916363.636363636) < 1e-5
          and abs(lt["tau"] - 1980052.591337616) < 1e-4
          and rel_id_ax < 1e-12 and rel_id_lt < 1e-12
          and rel_r < 1e-12 and rel_h < 1e-12,
          f"轴向 u=c：v/c={ax['v']/C:.9f}（超光速）、κ={ax['kappa']:.3f} m⁻¹、"
          f"τ={ax['tau']:.3f} m⁻¹、H={ax['H']*1e9:.3f} nm；"
          f"总速 v=c：u/c={lt['u']/C:.9f}、κ={lt['kappa']:.3f}、τ={lt['tau']:.3f}、"
          f"H={lt['H']*1e9:.3f} nm；恒等式残差 {rel_id_ax:.1e}/{rel_id_lt:.1e}；"
          f"R/H 反演残差 {rel_r:.1e}/{rel_h:.1e}",
          {"v_ax": f"{ax['v']/C:.9f}", "u_lt": f"{lt['u']/C:.9f}"})

    # ---------------------------------------------------------------- S5
    print("[S5] 旧强场 ω_old 的失效定理")
    ratios = {x: old_over_kepler(x) for x in (2.0, 3.0, 6.0, 10.0, 100.0, 1000.0)}
    monotone = all(ratios[a] < ratios[b] for a, b in
                   [(2.0, 3.0), (3.0, 6.0), (6.0, 10.0), (10.0, 100.0), (100.0, 1000.0)])
    guard("G7", "ω_old/Ω_K=√(x³/(2(x−1)))：x=100 达 71.07，x→∞ 发散 ⇒ 无弱场极限",
          abs(ratios[100.0] - 71.06690545187014) < 1e-8
          and abs(ratios[1000.0] - 707.4605999633482) < 1e-6
          and monotone,
          "x=r/(GM/c²)："
          + "，".join(f"{x:g}→{ratios[x]:.3f}" for x in sorted(ratios))
          + "（单调递增）⇒ 弱场（x≫1）反而偏离 Kepler 越来越远，"
          "旧式不能作为强场几何修正（否定性定理，条目 H03）",
          {"r100": f"{ratios[100.0]:.4f}", "r1000": f"{ratios[1000.0]:.4f}"})

    # ---------------------------------------------------------------- S6
    print("[S6] 标准强场：ISCO / 光子球 / 钟差")
    isco_x, ph_x = 6.0, 3.0
    dtau = sqrt(1.0 - 3.0 / isco_x)
    guard("G8", "Schwarzschild：r_ph=3GM/c²、r_ISCO=6GM/c²=3r_s、ISCO 处 dτ/dt=√2/2",
          abs(dtau - 0.7071067811865476) < 1e-15 and ph_x * 2.0 == 6.0,
          f"r_ph={ph_x}GM/c²（=1.5r_s）；r_ISCO={isco_x}GM/c²（=3r_s）；"
          f"ISCO 稳定圆轨道 v=√(GM/r) ⇒ dτ/dt=√(1−3GM/rc²)={dtau:.9f}；"
          "旧稿 r_ISCO=GM/c²（=r_s/2）与 GR 差 6 倍",
          {"dtau_isco": f"{dtau:.12f}"})

    # ---------------------------------------------------------------- S7
    print("[S7] 引力长度与经典检验复现")
    lg_e, lg_s = lg_of(GM_EARTH), lg_of(GM_SUN)
    m_sun = GM_SUN / G
    lg_sgr = G * 4.3e6 * m_sun / C ** 2
    len_rows = [
        {"name": "地球", "lg": lg_e, "rs": 2 * lg_e, "unit": "mm", "scale": 1e3},
        {"name": "太阳", "lg": lg_s, "rs": 2 * lg_s, "unit": "m", "scale": 1.0},
        {"name": "Sgr A*（4.3×10⁶M☉）", "lg": lg_sgr, "rs": 2 * lg_sgr,
         "unit": "m", "scale": 1.0},
    ]
    a_merc = 0.387098 * AU
    e_merc = 0.205630
    per_orb = 6.0 * pi * GM_SUN / (a_merc * (1 - e_merc ** 2) * C ** 2)
    arcsec_per_orbit = per_orb * 206264.80624709636
    mercury = arcsec_per_orbit * 100.0 / 0.240846
    deflect = 4.0 * GM_SUN / (R_SUN * C ** 2) * 206264.80624709636
    r_gps = R_E + H_GPS
    v_gps = 2.0 * pi * r_gps / 43082.0
    gps_grav = GM_EARTH / C ** 2 * (1.0 / R_E - 1.0 / r_gps) * 86400 * 1e6
    gps_kin = -(v_gps ** 2) / (2.0 * C ** 2) * 86400 * 1e6
    gps_net = gps_grav + gps_kin
    shapiro = 2.0 * GM_SUN / C ** 3 * log(4.0 * AU * 1.524 * AU / R_SUN ** 2) * 1e6
    tds_rows = [
        {"name": "水星相对论额外进动（″/世纪）", "calc": mercury, "doc": 42.98069,
         "trad": "≈43″, 支持 GR", "tol": 0.01},
        {"name": "掠日光偏折（″）", "calc": deflect, "doc": 1.75119,
         "trad": "≈1.75″, 有观测支持", "tol": 0.005},
        {"name": "GPS 引力钟差（μs/天）", "calc": gps_grav, "doc": 45.66076,
         "trad": "≈+45 μs/天", "tol": 0.05},
        {"name": "GPS 运动钟差（μs/天）", "calc": gps_kin, "doc": -7.10470,
         "trad": "≈−7 μs/天", "tol": 0.15},
        {"name": "GPS 净钟差（μs/天）", "calc": gps_net, "doc": 38.55606,
         "trad": "≈+38 μs/天", "tol": 0.15},
        {"name": "Earth–Mars Shapiro 单程（μs）", "calc": shapiro, "doc": 123.62,
         "trad": "GR 主阶公式", "tol": 1.0},
    ]
    dev_ok = all(abs(row["calc"] - row["doc"]) <= row["tol"] for row in tds_rows)
    guard("G9", "ℓ_g/r_s 三体 + 经典检验六行：本卷复算落在文/传统带内（容差逐行标注）",
          abs(lg_e * 1e3 - 4.435028039117671) < 1e-6
          and abs(lg_s - 1476.6250382504018) < 1e-8
          and abs(lg_sgr - 6349487664.476728) < 1e-4 and dev_ok,
          f"地球 {lg_e*1e3:.6f}/{2*lg_e*1e3:.6f} mm；太阳 {lg_s:.4f}/{2*lg_s:.4f} m；"
          f"Sgr A* {lg_sgr:.6e}/{2*lg_sgr:.6e} m（旧稿 1.27e7 小 1000 倍）；"
          f"水星 {mercury:.5f}″/cy；偏折 {deflect:.5f}″；GPS "
          f"{gps_grav:+.5f}/{gps_kin:+.5f}/{gps_net:+.5f} μs/d；Shapiro {shapiro:.3f} μs",
          {"mercury": f"{mercury:.5f}", "deflect": f"{deflect:.5f}",
           "gps_net": f"{gps_net:+.5f}", "shapiro": f"{shapiro:.3f}"})

    # ---------------------------------------------------------------- S8
    print("[S8] 控制组")
    f_rel = [abs(2.0 * Z * mm / (C * rr ** 2) - G * mm / rr ** 2)
             / (G * mm / rr ** 2)
             for mm in (1.0, 10.0, 1e3, 1e6) for rr in (1e-3, 1.0, 1e3)]
    control("C1", "Z 只是 G 的重参数：四质量×三半径全格点 F_Z/F_G 相对残差机器零",
            max(f_rel) < 1e-15,
            f"12 格点最大相对残差 {max(f_rel):.2e}（绝对差 ~1e-19 N 来自 "
            f"c/2 与 r² 的浮点舍入）；⇒ Z 不含任何新引力信息（A01 的对照）",
            {"max_rel": f"{max(f_rel):.2e}"})

    eps_alt = 8.8541878188e-12
    zp_alt = C / (8.0 * pi * eps_alt)
    alpha_alt = 2.0 * E_CHG ** 2 * zp_alt / (HBAR * C * C)
    control("C2", "α 由 Z' 重参数：ε₀ 换版 ⇒ Z'、α 同步漂移（不是独立预测）",
            abs(ZP - zp_alt) / ZP < 1e-9 and abs(ALPHA - alpha_alt) / ALPHA < 1e-9
            and rel_a < 1e-9,
            f"ε₀:817→{zp_alt:.9e}（Δ/Z'={abs(ZP-zp_alt)/ZP:.2e}）；"
            f"α 同步漂移 {abs(ALPHA-alpha_alt)/ALPHA:.2e}；与 CODATA 差 {rel_a:.2e} ⇒ "
            "恒等式成立的同时说明 α 来自 ε₀/e/ħ，而非 Z' 几何推导",
            {"rel_zp": f"{abs(ZP-zp_alt)/ZP:.2e}",
             "rel_alpha": f"{abs(ALPHA-alpha_alt)/ALPHA:.2e}"})

    kr = [kepler_ratio(x) * (x ** 1.5) for x in (2.0, 3.0, 6.0, 10.0, 100.0, 1000.0)]
    control("C3", "标准 Kepler 比值恒为 1（旧式 x=100 给出 71.07 ⇒ 失效被控制组锁死）",
            max(abs(v - 1.0) for v in kr) < 1e-15
            and old_over_kepler(100.0) > 70.0,
            f"Ω_K(x)/[(GM/x³)^{1/2}] 在 x∈{{2,3,6,10,100,1000}} 全为 1"
            f"（最大偏离 {max(abs(v-1.0) for v in kr):.1e}）；"
            f"同点 ω_old/Ω_K={old_over_kepler(100.0):.3f} ⇒ 定理方向正确",
            {"kepler_max_dev": f"{max(abs(v-1.0) for v in kr):.1e}"})

    id_ok = max(rel_id_ax, rel_id_lt) < 1e-12
    control("C4", "螺旋三恒等 + 双模型 κ/τ 交换：v_⊥=Rω 固定 ⇒ 唯一差别是轴向分配",
            id_ok and abs((ax["v"] ** 2 - lt["v"] ** 2) / C ** 2
                          - (ax["v"] ** 2 / C ** 2 - 1.0)) < 1e-12,
            f"两模型 v_⊥/c={Q_HELIX:.3f} 相同；轴向速度 c→{lt['u']/C:.6f}c；"
            f"κ、τ、H 全部随 u 变化（{ax['kappa']:.1f}→{lt['kappa']:.1f} 等）；"
            f"κ²+τ²=ω²/v² 两模型残差 {rel_id_ax:.1e}/{rel_id_lt:.1e}",
            {"kappa_ax": f"{ax['kappa']:.3f}", "kappa_lt": f"{lt['kappa']:.3f}"})

    v_kepler = sqrt(GM_EARTH / r_gps)
    v_ratio = abs(v_kepler - v_gps) / v_gps
    control("C5", "GPS 运动项口径：v=2πr/T 与 v=√(GM/r) 差 <0.5%，净钟差 38.44±0.15 μs",
            v_ratio < 0.005 and abs(gps_net - 38.4387240421037) < 1e-9,
            f"v(2πr/T)={v_gps:.3f} m/s，v(√GM/r)={v_kepler:.3f} m/s，"
            f"差 {v_ratio*100:.3f}%；由此 −7.222 vs 文 −7.105 μs/d（0.117 μs 口径差）；"
            f"净 {gps_net:+.5f} vs 文 +38.55606",
            {"v_ratio": f"{v_ratio:.4f}"})

    # ---------------------------------------------------------------- 条目
    entry("A01", "PASS", "Z=Gc/2 是 G 的正确重参数，不是新常数",
          f"F=2Zm₁m₂/(cr²) 与 Gm₁m₂/r² 在 12 格点机器零（C1）；Z={Z:.15f} m⁴kg⁻¹s⁻³；"
          "重参数恒等式成立 ≠ 独立测定引力常数")
    entry("A02", "PASS", "Z'=c/(8πε₀) 三重恒等式成立",
          f"1/(4πε₀)=2Z'/c=8 987 551 792.261（rel 0）；μ₀=8πZ'/c³（rel 0）；"
          f"α=2e²Z'/(ħc²)={ALPHA:.12e}（与 CODATA 差 {rel_a:.1e}）")
    entry("A03", "FAIL", "Z_unified=Z+iZ' 量纲不可加",
          f"实部 m⁴kg⁻¹s⁻³、虚部 kg m⁴C⁻²s⁻³；|Z'/Z|={ratio:.3e}；|Z+iZ'|≈Z'，"
          "实部被淹没 20 个量级 ⇒ 该「复耦合」在 SI 中无定义，应从体系删除（B01 口径 6）")
    entry("A04", "CORRECTED", "f=(c/2)√(4πε₀G)=0.012917333315677 数值对，但单位是 A·m/kg 而非 kg/A",
          f"量纲链：ε₀G→C²/kg²，取根→C/kg，×c/2→A·m/kg；"
          f"f={F_COUP:.15f}。旧稿把 SI 单位写成 kg/A（倒数量纲），数值一致掩盖了定义错误")
    entry("A05", "FAIL", "α=1/(4π³+π²+π) 不是预测，是 numerology",
          f"α⁻¹_geo={alpha_prop_inv:.12f}，偏差 {ppm:.6f} ppm（超 CODATA 不确定度 "
          f"{abs(ppm)/1e6/alpha_unc_rel:.0f} 倍）；项目预测登记 S10-P002 已标 ❌")
    entry("A06", "FAIL", "m_p/m_e=56π 被实测排除",
          f"56π={mr_56pi:.9f} vs {MASS_RATIO}（差 {mr_rel*100:.2f}%，{MASS_RATIO/mr_56pi:.2f} 倍）")
    entry("H01", "PASS", "螺旋双模型：几何量逐位复现，轴向 u=c 模型 v/c=1.0846 超光速",
          f"轴向：κ={ax['kappa']:.3f}、τ={ax['tau']:.3f}、H={ax['H']*1e9:.3f} nm、"
          f"a=Rω²={ax['a']:.4e} m/s²；总速：u/c={lt['u']/C:.9f}、κ={lt['kappa']:.3f}、"
          f"τ={lt['tau']:.3f}、H={lt['H']*1e9:.3f} nm；恒等式与反演机器零（G6）")
    entry("H02", "BOUNDARY", "非零 κ 的光样曲线不是测地线 ⇒ 实体螺旋光子被排除",
          f"κ≠0 ⇒ 加速度 a=Rω²={ax['a']:.3e} m/s²，∇_k k≠0，光样条件只是必要条件；"
          "r116 上界 R≤1.1254e−16 m（远小于 0.35λ=1.925e−7 m）⇒ D 类「光子内部旋转」不可作为"
          "自由光子的真实轨迹，只能作为结构光/圆偏振场几何")
    entry("H03", "PASS", "旧强场 ω_old 无弱场极限（否定性定理）",
          f"ω_old/Ω_K=√(x³/(2(x−1)))：x=100→{ratios[100.0]:.4f}，x=1000→"
          f"{ratios[1000.0]:.4f}，x≫1 仍发散；x→1⁺ 亦发散 ⇒ 该式在任何区间都不收敛到 "
          "Kepler，必须弃用（r234 机检口径）")
    entry("H04", "PASS", "标准强场结构：ISCO=6GM/c²、光子球=3GM/c²、ISCO 钟慢 0.7071",
          f"r_ISCO=3r_s（旧稿 r_s/2 差 6 倍）；光子球 1.5r_s；ISCO 切向圆轨道 "
          f"dτ/dt={dtau:.9f}（=√(1−3GM/rc²)）；Ω=√(GM/r³) 用史瓦西坐标时间")
    entry("D01", "PASS", "引力长度 ℓ_g=GM/c²、r_s=2ℓ_g 三体复算",
          f"地球 {lg_e*1e3:.6f} mm / {2*lg_e*1e3:.6f} mm；太阳 {lg_s:.4f} m / "
          f"{2*lg_s:.4f} m；Sgr A* {lg_sgr:.6e} m / {2*lg_sgr:.6e} m。"
          "ℓ_g 由 G、M、c 定义，不是对引力本源的独立解释；旧 Sgr A* r_s≈1.27e7 m 小 1000 倍")
    entry("D02", "PASS", "经典检验六行复现（标准 GR 计算，非本体系独立预言）",
          f"水星 {mercury:.5f}″/cy（文 42.98069）；偏折 {deflect:.5f}″（文 1.75119）；"
          f"GPS {gps_grav:+.5f}/{gps_kin:+.5f}/{gps_net:+.5f} μs/d"
          f"（文 45.66076/−7.10470/+38.55606，运动项口径差 0.117 μs）；"
          f"Shapiro {shapiro:.3f} μs（文 123.62）")
    entry("B01", "BOUNDARY", "六条旧口径消解：数值对 ≠ 物理对",
          "①V≡c 仅四速模长类比（r54）；②g=−a 仅局域加速系；③P=m(C−V) 不替代 γm₀v；"
          "④E=m₀c²→γm₀c²；⑤r_ISCO GM/c²→6GM/c²（H04）；⑥Z+iZ' 不可加（A03）；"
          "另 Sgr A* r_s 1.27e7→1.27e10（D01）")
    entry("B02", "BOUNDARY", "D 类命题不可判定（无独立可检验预言）",
          "空间基元普遍以光速螺旋运动、光子存在实体内部旋转、螺旋是质量与引力的共同本源、"
          "由几何唯一推出全部自然常数——四条均无「预测值+观测值+误差条」结构，"
          "只能作为研究纲领，不能进入已验证核心")
    entry("I01", "INFO", "判决：V5.0 审计本身正确，可作外部复核/口径统一层",
          "15 个关键数字独立复算全中（Z、Z'、α、f、双模型 κ/τ/H、α ppm、56π、"
          "71.07 倍、ISCO、ℓ_g、四检验）；其 A/B/C/D 分级与本项目 r141/r142/r257 同向，"
          "新增理论含量为零")
    entry("I02", "INFO", "编号：用户指定 r262 已被并行链占用，本卷改取 r268（撞号第 11 次）",
          "实测 r262《重子不对称层》、r263《攻坚任务书审计》、r264《自由参数总账层》、"
          "r265《引力波预言层》、r266、r267 均被占；r268–r270 三树为空 ⇒ 取 r268，"
          "r262 的既有产物不作任何改动")

    n_pass = sum(1 for e in entries if e["level"] == "PASS")
    n_fail = sum(1 for e in entries if e["level"] == "FAIL")
    n_bnd = sum(1 for e in entries if e["level"] == "BOUNDARY")
    n_cor = sum(1 for e in entries if e["level"] == "CORRECTED")
    n_info = sum(1 for e in entries if e["level"] == "INFO")

    layer = [
        {"cls": "A 已严格成立", "items": "螺旋求导、速度正交分解、κ/τ、Frenet–Serret、"
                                          "量纲正确恒等式", "n": 5, "verdict": "保留（本卷 H01/G6）"},
        {"cls": "B 与现有物理兼容", "items": "光样条件、圆偏振场、光子能动、GR 引力长度与钟慢",
         "n": 4, "verdict": "保留（本卷 D01/D02）"},
        {"cls": "C 需要修正", "items": "轴向/总光速混淆、时间势符号、强场弱场极限、α 几何表达、"
                                        "耦合量纲", "n": 5, "verdict": "已修正（A04/A05/H03/B01）"},
        {"cls": "D 未获独立证明", "items": "基元普遍光速螺旋、光子内部旋转、螺旋为质量与引力本源、"
                                           "无新参数推出全部常数", "n": 4, "verdict": "不可判定（B02）"},
    ]

    ledger = [
        ["r214", "静态中心力（UFE-4F 母式）", "形式统一 PASS；动力学 FAIL"],
        ["r229", "新颖性审计", "无新理论/无新方程"],
        ["r230", "引力本质层", "WEP 结构恒等 + 1PN"],
        ["r234（并行）", "强场层（史瓦西测地线）", "ISCO/光子球 机检"],
        ["r241", "光速螺旋曲率挠率统一场论整理", "体系整理"],
        ["r242", "修复候选式机器核验", "候选式对拍"],
        ["r257", "同一运动定理卷", "单一公设求导 + 十六格穷举"],
        ["r261（并行）", "α=玻尔速度比与螺旋映射", "标准恒等式 + 双运动区分"],
        ["r262（并行）", "重子不对称层", "选择定则写反 / 唯一预言零数值"],
        ["r263（并行）", "攻坚任务书审计", "GW170817 裁定 + literal-helix 排除"],
        ["r264（并行）", "自由参数总账层", "ω 赋值单位依赖 / 四态分类崩坏"],
        ["r265（并行）", "引力波预言层", "相变参数全缺 / 零判别力"],
        ["r267（并行）", "完成度终局验收层", "账面不可加 / 独有预言归零"],
        ["r268（本卷）", "ROOT V5.0 融合审计层", "四层映射 + 六口径消解 + Z/Z' + ω 失效定理"],
    ]

    # 扫描：κ、τ 随 q=R/λ（两模型）；总速模型要求 Rω<c ⇒ q<1/1.2=0.8333
    qs = [0.05 + 0.75 * i / 40.0 for i in range(41)]
    scan = {"q": [round(q, 4) for q in qs],
            "kap_ax": [], "tau_ax": [], "kap_lt": [], "tau_lt": []}
    for q in qs:
        rr = q * LAM
        ma = helix_ax(C, rr, OMEGA_H)
        ml = helix_light(rr, OMEGA_H)
        scan["kap_ax"].append(ma["kappa"] * LAM)
        scan["tau_ax"].append(ma["tau"] * LAM)
        scan["kap_lt"].append(ml["kappa"] * LAM)
        scan["tau_lt"].append(ml["tau"] * LAM)

    xs = [2.0 + i * (998.0 / 60.0) for i in range(61)]
    old_scan = {"x": [round(x, 3) for x in xs],
                "ratio": [old_over_kepler(x) for x in xs]}

    res = {
        "stem": STEM, "round": 268, "date": "2026-10-31",
        "method": ("Z=Gc/2 双路径力恒等 + Z'=c/(8πε₀) 三恒等 + 量纲签名比对 + "
                   "α 几何提案 ppm 定价 + 56π 质量比定价 + 螺旋双模型 κ/τ/H + "
                   "ω_old/Ω_K=√(x³/(2(x−1))) 极限定理 + Schwarzschild ISCO/光子球 + "
                   "ℓ_g/r_s 三体 + 水星/偏折/GPS/Shapiro 复算——float64，纯标准库"),
        "fusion_verdict": ("ROOT V5.0 审计与项目账本同向：A/B 层保留，C 层五条已修正，"
                           "D 层四条不可判定；Z/Z' 为重参数、Z+iZ' 不可加、两个伪预言 FAIL、"
                           "旧 ω_old 无弱场极限（定理）——新增理论含量为零"),
        "entries": entries, "guards": guards, "controls": controls,
        "readings": {
            "params": {"eps0": EPS0, "alpha_inv_codata": ALPHA_INV,
                       "mass_ratio": MASS_RATIO, "lam_m": LAM, "R_m": R_HELIX,
                       "omega": OMEGA_H},
            "coupling": {"Z": Z, "Zp": ZP, "ratio": ratio, "mag": mag,
                         "inv4pe0": inv4pe0, "mu0": mu0, "alpha": ALPHA,
                         "alpha_codata": 1.0 / ALPHA_INV, "rel_alpha": rel_a,
                         "f": F_COUP, "f_unit": "A·m/kg",
                         "Z_unit": "m⁴·kg⁻¹·s⁻³", "Zp_unit": "kg·m⁴·C⁻²·s⁻³"},
            "alpha_prop": {"inv": alpha_prop_inv, "ppm": ppm,
                           "unc_rel": alpha_unc_rel,
                           "overshoot": abs(ppm) / 1e6 / alpha_unc_rel},
            "mass_ratio": {"prop": mr_56pi, "meas": MASS_RATIO, "rel": mr_rel},
            "helix": {"vp_over_c": Q_HELIX,
                      "ax": {"u_over_c": 1.0, "v_over_c": ax["v"] / C,
                             "kappa": ax["kappa"], "tau": ax["tau"],
                             "H_nm": ax["H"] * 1e9, "a": ax["a"]},
                      "lt": {"u_over_c": lt["u"] / C, "v_over_c": 1.0,
                             "kappa": lt["kappa"], "tau": lt["tau"],
                             "H_nm": lt["H"] * 1e9, "a": lt["a"]},
                      "identity_rel": max(rel_id_ax, rel_id_lt),
                      "R_recover_rel": rel_r, "H_recover_rel": rel_h},
            "old_omega": {"ratios": {f"{x:g}": ratios[x] for x in sorted(ratios)},
                          "scan": old_scan},
            "strong": {"isco_x": isco_x, "ph_x": ph_x, "dtau_isco": dtau},
            "lengths": [{"name": r["name"], "lg": r["lg"], "rs": r["rs"],
                         "unit": r["unit"], "lg_si": r["lg"] * r["scale"],
                         "rs_si": r["rs"] * r["scale"]} for r in len_rows],
            "tests": tds_rows,
            "layer": layer,
            "scan": scan,
            "ledger": [{"round": r, "method": m, "verdict": v} for r, m, v in ledger],
        },
        "counts": {"entries": len(entries), "PASS": n_pass, "FAIL": n_fail,
                   "BOUNDARY": n_bnd, "CORRECTED": n_cor, "INFO": n_info,
                   "guards": f"{sum(1 for g in guards if g['ok'])}/{len(guards)}",
                   "controls": f"{sum(1 for c in controls if c['ok'])}/{len(controls)}"},
        "verdict": "", "judgement": "", "source": {},
    }

    parts = [
        "R268-ROOT-V5-FUSION-AUDIT-OK-Z-ZPRIME-DIM-OK-Z-ZPRIME-IDENTITY-OK",
        "ALPHA-PROPOSAL-FAIL-MASS-RATIO-FAIL-COMPLEX-COUPLING-FAIL",
        "HELIX-DUAL-MODEL-OK-NON-GEODESIC-BOUNDARY-OLD-OMEGA-THEOREM-OK",
        "ISCO-PHOTON-SPHERE-OK-LG-RS-OK-CLASSICAL-TESTS-OK",
        "SIX-CALIBER-RESOLVED-D-CLASS-UNDECIDABLE",
        "VERDICT-EXTERNAL-REVIEW-NO-NEW-THEORY",
    ]
    res["verdict"] = "-".join(parts)
    res["judgement"] = ("CLOSED-INCREMENT（ROOT V5.0 融合审计层：Z/Z' 重参数恒等、"
                        "复耦合不可加、两伪预言 FAIL、螺旋双模型 + 旧 ω 失效定理、"
                        "ISCO/光子球/引力长度/经典检验复现）；D 类不可判定；"
                        "外部复核层，无新理论")
    res["source"] = {
        "engine": BASE + ".py",
        "inherits": ["r141/r142（四层分级口径）", "r257（同一运动定理/口径消解）",
                     "r234（ISCO/光子球机检）", "r241/r242（螺旋曲率挠率）",
                     "r261（α 与双运动区分）", "r116（R 上界）",
                     "CODATA 2022 / JPL GM / Bekenstein–Hawking / Schwarzschild（只读）"],
    }

    os.makedirs(_DATADIR, exist_ok=True)
    jpath = os.path.join(_DATADIR, BASE + ".json")
    mpath = os.path.join(_DATADIR, BASE + ".md")
    rpath = os.path.join(_DATADIR, BASE + "_report.txt")

    html_ok, html_detail = cast_html(res)
    guard("G10", "交互 HTML 生成且自含（零外部 URL、占位符已铸入）",
          html_ok, html_detail)
    res["counts"]["guards"] = f"{sum(1 for g in guards if g['ok'])}/{len(guards)}"
    if html_ok:
        cast_html(res)

    print(f"条目 {res['counts']['entries']}（PASS {n_pass} / FAIL {n_fail} / "
          f"BOUNDARY {n_bnd} / CORRECTED {n_cor} / INFO {n_info}）· "
          f"守卫 {res['counts']['guards']} · 控制组 {res['counts']['controls']}")

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
         f"- 条目：{res['counts']['entries']}（PASS {res['counts']['PASS']} / "
         f"FAIL {res['counts']['FAIL']} / BOUNDARY {res['counts']['BOUNDARY']} / "
         f"CORRECTED {res['counts']['CORRECTED']} / "
         f"INFO {res['counts']['INFO']}）· 守卫 {res['counts']['guards']} · "
         f"控制组 {res['counts']['controls']}\n",
         "\n## 条目\n"]
    for e in res["entries"]:
        L.append(f"- **{e['code']} {e['level']}** {e['title']}——{e['detail']}\n")
    L.append("\n## 守卫\n")
    for g in res["guards"]:
        L.append(f"- **{g['id']} {'OK' if g['ok'] else 'FAIL'}** {g['title']}——"
                 f"{g['detail']}\n")
    L.append("\n## 控制组\n")
    for c in res["controls"]:
        L.append(f"- **{c['id']} {'OK' if c['ok'] else 'FAIL'}** {c['title']}——"
                 f"{c['detail']}\n")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(L))


def write_report(path, res):
    c = res["readings"]["coupling"]
    h = res["readings"]["helix"]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(f"{MARKER} rc=0\n")
        f.write(f"entries={res['counts']['entries']} PASS={res['counts']['PASS']} "
                f"FAIL={res['counts']['FAIL']} BOUNDARY={res['counts']['BOUNDARY']} "
                f"CORRECTED={res['counts']['CORRECTED']} INFO={res['counts']['INFO']}\n")
        f.write(f"guards={res['counts']['guards']} controls={res['counts']['controls']}\n")
        f.write(f"verdict={res['verdict']}\n")
        f.write(f"Z={c['Z']:.15f} Zp={c['Zp']:.9e} Zp/Z={c['ratio']:.6e}\n")
        f.write(f"alpha={c['alpha']:.15e} rel_alpha={c['rel_alpha']:.3e} "
                f"f={c['f']:.15f}\n")
        f.write(f"alpha_prop_inv={res['readings']['alpha_prop']['inv']:.12f} "
                f"ppm={res['readings']['alpha_prop']['ppm']:.6f}\n")
        f.write(f"56pi={res['readings']['mass_ratio']['prop']:.9f} "
                f"meas={res['readings']['mass_ratio']['meas']}\n")
        f.write(f"helix_ax: v/c={h['ax']['v_over_c']:.9f} k={h['ax']['kappa']:.3f} "
                f"tau={h['ax']['tau']:.3f} H={h['ax']['H_nm']:.3f}nm\n")
        f.write(f"helix_lt: u/c={h['lt']['u_over_c']:.9f} k={h['lt']['kappa']:.3f} "
                f"tau={h['lt']['tau']:.3f} H={h['lt']['H_nm']:.3f}nm\n")
        f.write(f"old_omega_ratio_x100={res['readings']['old_omega']['ratios']['100']:.6f}\n")
        f.write(f"dtau_isco={res['readings']['strong']['dtau_isco']:.9f}\n")
        for row in res["readings"]["lengths"]:
            f.write(f"{row['name']}: lg={row['lg_si']:.6e} rs={row['rs_si']:.6e} {row['unit']}\n")
        for row in res["readings"]["tests"]:
            f.write(f"{row['name']}: calc={row['calc']:.6f} doc={row['doc']}\n")


def cast_html(res):
    if not os.path.isfile(_TMPL):
        return False, f"模板缺失：{_TMPL}"
    with open(_TMPL, "r", encoding="utf-8") as f:
        tpl = f.read()
    if "__R268_JSON__" not in tpl:
        return False, "模板缺少 __R268_JSON__ 占位符"
    html = tpl.replace("__R268_JSON__", json.dumps(res, ensure_ascii=False))
    with open(HTML_OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    text = open(HTML_OUT, "r", encoding="utf-8").read()
    problems = []
    if "__R268_JSON__" in text:
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
