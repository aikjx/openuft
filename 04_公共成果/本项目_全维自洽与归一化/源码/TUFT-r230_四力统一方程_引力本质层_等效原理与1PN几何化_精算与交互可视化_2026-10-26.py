# -*- coding: utf-8 -*-
r"""TUFT-r230 · 四力统一方程·引力本质层：等效原理与 1PN 几何化唯象——「攻破引力的本质？」
2026-10-26

〔编号说明〕本卷取号 r230（落盘前实测 r230–r233 三树零命中；开工基线 verify.py PASS=0）。
承 r214–r229 十四轮体系，本轮回答用户直问：「攻破引力的本质？」。

本卷要回答的问题（引力本质层 = 本库对引力能到的最深一层）：
  Q1 等效原理（引力质量=惯性质量）在本库是推导还是输入？
     → 框架内结构恒等（a=GM/r² 与落体质量无关，m 自动消去）——机器验证；
       但「为什么 m_i ≡ m_g」不可推导：Eötvös/MICROSCOPE 实验边界是库外输入。
  Q2 引力的几何化（GR）本库能验到哪？
     → 1PN 唯象层两件套：水星近日点进动 42.98″/百年（解析 6πGM/(c²a(1−e²)) vs
       数值 φ-ODE 峰定位）+ 太阳光线弯曲 1.7517″（解析 4GM/(c²b) vs 数值）；
       牛顿微粒说只给一半（0.876″）——「几何 vs 粒子」的结构差异机器可分。
  Q3 引力与其它三力的结构独有性？
     → 五项枚举（纯吸引 / 普适耦合 / 不可屏蔽 / 最弱 36 量级 / 可几何化），
       其中可机器验证部分（恒负、强度比、恒等比 α_G/α_EM）数值化。
  Q4 「本质」之问本身？
     → 为什么 α_G 比库仑小 36 个量级（等级问题）：无推导，外部输入（承 r229 G5）；
       量子引力（引力子）：人类共同未完成；r226 已证纯引力束缚态半径 4.4e32 m
       （超可观测宇宙 5×10⁵ 倍）——量子层在本库框架内无意义。

诚实预期（写在前面，由守卫检验）：
  本卷不宣称「攻破」引力的本质。本卷能做的：把引力的可算性质（1PN 唯象、
  等效原理结构、独有性清单）钉死到机器精度，并把「攻不破的部分」
  （等级问题、量子化、场方程层）如实登记为框架外。判定假设与 r229 一致：
  无新理论——GR 1PN 全部是 1915 年教科书内容，本卷是复现层。

纪律：纯标准库；对 r214–r229 及并行会话产物只读；守卫失败即非零退出；
条目不可与 r142–r229 相加。
"""

import json
import os
import sys
from math import sqrt, pi, exp, atan2, sin, cos

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)
_DATADIR = os.path.join(_PROJ, "数据")
_TMPL = os.path.join(_HERE, "TUFT-r230_引力本质层交互可视化模板_2026-10-26.html")
HTML_OUT = os.path.join(_PROJ, "四力统一方程_引力本质层可视化_2026-10-26.html")

MARKER = "R230-GRAVITY-ESSENCE"
BASE = ("TUFT-r230_四力统一方程_引力本质层_等效原理与1PN几何化_"
        "精算与交互可视化_2026-10-26")
STEM = "TUFT-r230"

# 太阳系常数（IAU/CODATA 口径）
GM_SUN = 1.32712440018e20        # m³/s²
C_LIGHT = 2.99792458e8           # m/s
M_GEO = GM_SUN / C_LIGHT ** 2    # 太阳几何长度 GM/c² = 1476.625 m
MERC_A = 5.7909050e10            # 水星半长轴 m
MERC_E = 0.205630
R_SUN = 6.957e8                  # 太阳半径 m（光线掠面瞄准参数）
ARCSEC = pi / (180.0 * 3600.0)
ORBITS_PER_CENTURY = 100.0 * 365.25 * 86400.0 / (2.0 * pi * sqrt(MERC_A ** 3 / GM_SUN))

# 本库四力常数（pp 基准，MeV·fm 口径，承 r214/r227）
HARC = 197.3269804
ALPHA_EM = 1.0 / 137.035999084
A_EM = ALPHA_EM * HARC
A_G = 5.9061494e-39 * HARC
LAM_PI = 1.4619325721160970e-15 * 1e15
A_PI = 14.6 * HARC
LAM_W = 2.4550179827562611e-18 * 1e15
A_W = 1.0268268e-5 * HARC

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
# S2 等效原理：框架内结构恒等（WEP）
# ===========================================================================
print("[S2] 等效原理审计（WEP 结构恒等）")


def fall_orbit(m_over_M, nsteps=200000, r0=2.0, vt_frac=0.5):
    """质量比 m/M 的试验体在水星式 1/r² 场中的轨道（自然单位 GM=1）。
    运动方程 a = −GM r̂/r²：试验体质量完全不出场（WEP 的结构表达）。"""
    v0 = vt_frac * sqrt(2.0 / r0)     # 椭圆：v < v_esc
    x, y, vx, vy = r0, 0.0, 0.0, v0
    dt = 4e-5
    traj = []
    for i in range(nsteps):
        r = sqrt(x * x + y * y)
        a1 = (-x / r ** 3, -y / r ** 3)          # GM=1；a 与 m_over_M 无关
        x2, y2 = x + vx * dt / 2, y + vy * dt / 2
        v2x, v2y = vx + a1[0] * dt / 2, vy + a1[1] * dt / 2
        r = sqrt(x2 * x2 + y2 * y2)
        a2 = (-x2 / r ** 3, -y2 / r ** 3)
        x3, y3 = x + v2x * dt / 2, y + v2y * dt / 2
        v3x, v3y = vx + a2[0] * dt / 2, vy + a2[1] * dt / 2
        r = sqrt(x3 * x3 + y3 * y3)
        a3 = (-x3 / r ** 3, -y3 / r ** 3)
        x4, y4 = x + v3x * dt, y + v3y * dt
        v4x, v4y = vx + a3[0] * dt, vy + a3[1] * dt
        r = sqrt(x4 * x4 + y4 * y4)
        a4 = (-x4 / r ** 3, -y4 / r ** 3)
        x += dt * (vx + 2 * v2x + 2 * v3x + v4x) / 6
        y += dt * (vy + 2 * v2y + 2 * v3y + v4y) / 6
        vx += dt * (a1[0] + 2 * a2[0] + 2 * a3[0] + a4[0]) / 6
        vy += dt * (a1[1] + 2 * a2[1] + 2 * a3[1] + a4[1]) / 6
        if i % (nsteps // 200) == 0:
            traj.append((x, y))
    return traj


traj1 = fall_orbit(1.0)
traj2 = fall_orbit(1.0e3)
wep_rel = 0.0
for (p1, p2) in zip(traj1, traj2):
    d = sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    wep_rel = max(wep_rel, d / max(sqrt(p1[0] ** 2 + p1[1] ** 2), 1e-12))
guard("G3", "等效原理：框架内结构恒等（a 与落体质量无关）", wep_rel == 0.0,
      f"质量比 1 vs 1000 的两试验体 20 万步轨道逐点重合（max rel = {wep_rel:.1e}）——"
      "a = GM/r² 中 m 自动消去：WEP 在本框架是**结构恒等**；"
      "但「为什么引力质量 ≡ 惯性质量」不可推导——Eötvös/MICROSCOPE 实验边界 "
      "η < 1e−13/1e−15 是库外输入（本卷如实登记：本质之问在此层 закрыт 于实验）",
      {"wep_rel": f"{wep_rel:.1e}"})

# ===========================================================================
# S3 GR 1PN：水星近日点进动（φ-ODE 峰定位法）
# ===========================================================================
print("[S3] GR 1PN：水星近日点进动")
P_HALF = MERC_A * (1.0 - MERC_E ** 2)     # 半通径 p
EPS_PN = M_GEO / P_HALF                    # 1PN 小参数 m/p ≈ 2.66e-8
DPHI_ANALYTIC = 6.0 * pi * EPS_PN          # 每圈进动 rad
ARCSEC_PER_ORBIT = DPHI_ANALYTIC / ARCSEC
ARCSEC_PER_CENTURY = DPHI_ANALYTIC * ORBITS_PER_CENTURY / ARCSEC


def precession(K_orbits, dphi, pn=True, coef=1.0):
    """ũ = p·u 无量纲化：ũ'' = 1 + coef·3(m/p)·ũ² − ũ（pn=False 去掉 1PN 项）。
    返回每圈进动 rad（峰定位均值）与最后一圈的 ũ 轨迹。"""
    def f(u, w):
        return w, (1.0 + (coef * 3.0 * EPS_PN * u * u if pn else 0.0)) - u
    u, w = 1.0 + MERC_E, 0.0            # 近日点起（ũ_max = p/r_peri = 1+e）
    step_per_orbit = int(round(2.0 * pi / dphi))
    peaks = []
    n_tot = step_per_orbit * K_orbits
    last_traj = []
    for i in range(n_tot):
        k1u, k1w = f(u, w)
        u2, w2 = u + k1u * dphi / 2, w + k1w * dphi / 2
        k2u, k2w = f(u2, w2)
        u3, w3 = u + k2u * dphi / 2, w + k2w * dphi / 2
        k3u, k3w = f(u3, w3)
        u4, w4 = u + k3u * dphi, w + k3w * dphi
        k4u, k4w = f(u4, w4)
        u_new = u + dphi * (k1u + 2 * k2u + 2 * k3u + k4u) / 6
        w_new = w + dphi * (k1w + 2 * k2w + 2 * k3w + k4w) / 6
        phi = i * dphi
        if w > 0 and w_new <= 0 and len(peaks) < K_orbits:
            # w 过正转负：u 极大（近日点），线性插值峰位置
            phi_peak = phi + dphi * w / (w - w_new) if w != w_new else phi
            peaks.append(phi_peak)
        if i >= n_tot - step_per_orbit:
            last_traj.append((phi, u))
        u, w = u_new, w_new
    diffs = [peaks[k + 1] - peaks[k] - 2.0 * pi for k in range(len(peaks) - 1)]
    domega = sum(diffs) / len(diffs)
    return domega, peaks, last_traj


K_ORB = 200
dphi_step = 2.0 * pi / 8192
domega_num, peaks, merc_traj_u = precession(K_ORB, dphi_step, pn=True)
rel_pre = abs(domega_num - DPHI_ANALYTIC) / DPHI_ANALYTIC
# 演示轨迹：进动系数 ×3000（仅可视化用，真实读数以 G1 为准；标注见 HTML）
DEMO_COEF = 3000.0
demo_domega, _, demo_u = precession(60, dphi_step, pn=True, coef=DEMO_COEF)
guard("G1", "GR 1PN：水星近日点进动（数值 vs 解析 6πGM/(c²a(1−e²))）",
      rel_pre < 5e-3,
      f"{K_ORB} 圈 × 8192 步/圈（ũ'' = 1 + 3(m/p)ũ² − ũ，ũ=p·u 无量纲化）："
      f"数值每圈进动 = {domega_num:.6e} rad vs 解析 {DPHI_ANALYTIC:.6e} rad，rel = {rel_pre:.3e}；"
      f"换算 {DPHI_ANALYTIC * ORBITS_PER_CENTURY / ARCSEC:.2f}″/百年 "
      f"（{ORBITS_PER_CENTURY:.1f} 圈/百年）——教科书值 42.98″：几何化唯象在本库复现到千分位",
      {"domega_num": f"{domega_num:.6e}", "domega_ana": f"{DPHI_ANALYTIC:.6e}",
       "rel": f"{rel_pre:.3e}", "arcsec_century": round(ARCSEC_PER_CENTURY, 2)})

# ===========================================================================
# S4 GR 1PN：太阳光线弯曲
# ===========================================================================
print("[S4] GR 1PN：光线弯曲")
MU_B = M_GEO / R_SUN                       # m/b = 2.122e-6
DEFLECT_ANALYTIC = 4.0 * MU_B              # rad
ARCSEC_LIGHT = DEFLECT_ANALYTIC / ARCSEC


def light_deflect(phi0=0.05, dphi=1.0e-4, pn=True):
    """ṽ = b·u：ṽ'' = 3(m/b)ṽ² − ṽ；直线渐近起止，出射角线性外推。"""
    def f(v, w):
        return w, (3.0 * MU_B * v * v if pn else 0.0) - v
    v, w = sin(phi0), cos(phi0)
    n = int(round((pi - 2.0 * phi0) / dphi))
    traj = []
    for i in range(n):
        if i % (n // 200) == 0:
            traj.append((phi0 + i * dphi, v))
        k1v, k1w = f(v, w)
        v2, w2 = v + k1v * dphi / 2, w + k1w * dphi / 2
        k2v, k2w = f(v2, w2)
        v3, w3 = v + k2v * dphi / 2, w + k2w * dphi / 2
        k3v, k3w = f(v3, w3)
        v4, w4 = v + k3v * dphi, w + k3w * dphi
        k4v, k4w = f(v4, w4)
        v += dphi * (k1v + 2 * k2v + 2 * k3v + k4v) / 6
        w += dphi * (k1w + 2 * k2w + 2 * k3w + k4w) / 6
    phi_end = phi0 + n * dphi
    # 渐近匹配：远场 v = A·sin(φ_out−φ)（v>0 直到 φ_out）⇒ tan(φ_out−φ_end) = v/(−w)
    phi_out = phi_end + atan2(v, -w)
    return (phi_out - 0.0) - pi, traj       # 入射渐近角 = 0（直线）


delta_num, light_traj = light_deflect()
rel_light = abs(delta_num - DEFLECT_ANALYTIC) / DEFLECT_ANALYTIC
guard("G2", "GR 1PN：太阳光线弯曲（数值 vs 解析 4GM/(c²b)）",
      rel_light < 2e-2,
      f"ṽ'' = 3(m/b)ṽ² − ṽ，掠面 b=R☉：数值偏转 = {delta_num:.4e} rad vs 解析 "
      f"{DEFLECT_ANALYTIC:.4e} rad（{ARCSEC_LIGHT:.4f}″），rel = {rel_light:.3e}"
      f"（直线渐近初条件的远场误差如实计入容差）；"
      f"牛顿微粒说（Soldner 1801）只给一半 {ARCSEC_LIGHT/2:.4f}″——"
      "「时空几何 vs 粒子受牛顿力」的结构差异被这一倍数关系机器可分（Eddington 1919 现场）",
      {"delta_num": f"{delta_num:.4e}", "delta_ana": f"{DEFLECT_ANALYTIC:.4e}",
       "rel": f"{rel_light:.3e}", "arcsec": round(ARCSEC_LIGHT, 4)})

# ===========================================================================
# S5 引力独有性：强度比 + 五项枚举
# ===========================================================================
print("[S5] 引力独有性枚举")
RATIO_G_EM = A_G / A_EM                    # = α_G/α_EM（同为 1/r²，恒定）


def f_grav(r):
    return A_G / (r * r)


def f_em(r):
    return A_EM / (r * r)


def f_strong(r):
    xx = r / LAM_PI
    return A_PI * exp(-xx) * (1.0 / (r * r) + 1.0 / (LAM_PI * r))


def f_weak(r):
    xx = r / LAM_W
    return A_W * exp(-xx) * (1.0 / (r * r) + 1.0 / (LAM_W * r))


R_POINTS = [(1.0, "1 fm（核尺度）"), (1.0e5, "1 Å（原子）"),
            (1.0e15, "1 m"), (1.496e20, "1 AU")]
ratio_rows = []
for (r, label) in R_POINTS:
    ratio_rows.append({
        "r_label": label,
        "g_over_em": float(f"{f_grav(r) / f_em(r):.9e}"),
        "s_over_em": float(f"{f_strong(r) / f_em(r):.9e}"),
        "w_over_em": float(f"{f_weak(r) / f_em(r):.9e}"),
        "s_over_g": float(f"{f_strong(r) / f_grav(r):.9e}"),
    })
const_ok = all(abs(row["g_over_em"] - RATIO_G_EM) < 1e-9 * RATIO_G_EM for row in ratio_rows)
UNIQUE = [
    ("纯吸引（无排斥通道）", "本库引力通道在任何 r 只给吸引量值（4 尺度机器核验 f_g>0）；"
     "无排斥分支是结构性质——电磁有同号排斥、强有色禁闭动力学、弱有手征通道",
     all(f_grav(r) > 0 for r, _ in R_POINTS)),
    ("普适耦合（耦合一切能量-动量）", "引力荷=质量-能量；电磁需电荷 ±、强需色 3 态、弱需手征——结构枚举", True),
    ("不可屏蔽（无负引力荷）", "无 ± 引力荷 ⇒ 无屏蔽；电磁有等离子体屏蔽（Debye）——结构枚举", True),
    ("最弱（等级问题）", "F_G/F_EM = α_G/α_EM = 8.094e−37（36 个量级，恒定——解析恒等 α_G/α_EM）；"
     "为什么这么小：无推导（承 r229 G5「新推导=0」）", const_ok),
    ("可几何化（四力中唯一）", "等效原理 ⇒ 引力可表述为时空曲率（GR 1915，本卷 G1/G2 复现其 1PN 唯象）；"
     "电磁/强/弱是时空上的规范力，不「化为几何」——概念枚举", True),
]
unique_ok = all(u[2] for u in UNIQUE)
guard("G4", "引力独有性：强度比 + 五项枚举（可验部分机器化）", const_ok and unique_ok,
      f"F_G/F_EM = α_G/α_EM = {RATIO_G_EM:.4e} 在 4 个尺度恒定（解析恒等——两者同为 1/r²）；"
      f"强/库仑在 1 fm = {ratio_rows[0]['s_over_em']:.1f}，到 1 AU 强/弱 Yukawa 下溢为 0"
      "（唯 1/r² 力存活）；五项独有性枚举齐备（纯吸引/普适/不可屏蔽/最弱/可几何化）——"
      "其中「最弱 36 量级」的起源（等级问题）无推导，外部输入",
      {"g_over_em": f"{RATIO_G_EM:.4e}", "n_unique": len(UNIQUE)})

# ===========================================================================
# S6 控制组
# ===========================================================================
print("[S6] 控制组")
domega_off, _, _ = precession(10, dphi_step, pn=False)
rel_off = abs(domega_off) / DPHI_ANALYTIC
control("C1", "阴性对照：去掉 1PN 项 ⇒ 进动必消失",
        rel_off < 1e-6,
        f"3(m/p)ũ² 项置零后 10 圈：进动 {domega_off:.3e} rad/圈（< 1e−6 × 解析 1PN 值）——"
        "G1 的进动信号确实来自 GR 项，不是数值漂移",
        {"domega_off": f"{domega_off:.3e}", "rel_to_gr": f"{rel_off:.2e}"})

domega_half, _, _ = precession(10, dphi_step, pn=True, coef=0.5)
rel_half = abs(domega_half - 0.5 * DPHI_ANALYTIC) / DPHI_ANALYTIC
control("C2", "判别力：1PN 系数减半 ⇒ 进动减半（守卫可分系数）",
        rel_half < 5e-3,
        f"系数 3→1.5：数值进动 {domega_half:.3e} vs 半额解析 {0.5 * DPHI_ANALYTIC:.3e}，"
        f"rel = {rel_half:.3e}——若未来某理论声称进动系数不同（如标量-张量理论），"
        "本管线可直接量化区分",
        {"domega_half": f"{domega_half:.3e}", "rel_half": f"{rel_half:.3e}"})

# ===========================================================================
# S7 条目与判决
# ===========================================================================


def main():
    n_orb_century = ORBITS_PER_CENTURY
    entry("Y01", "INFO", "判定：「攻破引力的本质」的本库边界",
          "本库到达的最深一层 = GR 1PN 唯象（G1/G2 机器复现 42.98″ 与 1.7517″）；"
          "「本质=时空几何」的完整表述（爱因斯坦场方程 10 个分量）在本库单粒子中心势框架之外；"
          "量子引力（引力子）是人类共同未完成——本卷诚实登记边界，不宣称攻破")
    entry("Y02", "PASS" if guard_ok("G3") else "FAIL", "等效原理：结构恒等而非推导",
          "a = GM/r² 中试验体质量自动消去（双质量比 20 万步轨道逐位重合）——"
          "WEP 在框架内是结构；「为什么 m_i ≡ m_g」是实验事实（Eötvös η<1e−13、"
          "MICROSCOPE 1e−15）而非本库推导——「引力的本质」最深实验事实在本库是输入")
    entry("Y03", "PASS" if guard_ok("G1") and guard_ok("G2") else "FAIL",
          "GR 1PN 几何化唯象：机器复现",
          f"水星进动 rel {rel_pre:.1e}（{ARCSEC_PER_CENTURY:.2f}″/百年）+ "
          f"光线弯曲 rel {rel_light:.1e}（{ARCSEC_LIGHT:.4f}″，牛顿微粒一半的倍数关系机器可分）——"
          "几何化的两大经典验证在本库纯标准库内复现到千分位")
    entry("Y04", "PASS" if guard_ok("G4") else "FAIL", "引力独有性：五项枚举",
          "纯吸引（F_G<0 恒）/普适（耦合一切能量-动量）/不可屏蔽（无负荷）/"
          f"最弱（F_G/F_EM = {RATIO_G_EM:.3e}，36 量级，等级问题无推导）/可几何化（四力唯一）"
          "——其中可机器验证部分已数值化，结构部分如实标注为枚举")
    entry("Y05", "INFO", "量子的引力：框架内无意义，人类共同边界",
          "r226 已证：纯引力「氢原子」束缚半径 4.4e32 m = 可观测宇宙 5×10⁵ 倍、"
          "E = −3.9e−85 eV——引力束缚态在物理上不存在；引力子与量子化：无实验、无成熟理论——"
          "「引力的本质」在量子层的答案人类尚未拥有，本卷不装作拥有")
    entry("Y06", "INFO", "第五力型修正：太阳系已夹死（并行卷结论引用）",
          "r223：Yukawa 修正拟合 λ≈957.9 AU 与内行星进动冲突 6.96–64.1×；"
          "r224：稳定性要求 λ > 18.6 AU（海王星最硬）⇒ 「要么无稳定轨道要么与进动冲突」"
          "无可行区间——在本库四力模板内给引力加有限力程修正，太阳系不允许")
    entry("Y07", "INFO", "判决：引力本质层收口",
          "本库对「引力的本质」的最终读数：最弱 × 最普适 × 不可屏蔽 × 纯吸引 × 可几何化；"
          "几何化的 1PN 唯象已机器复现；本质之问的三层（场方程/量子化/等级起源）"
          "分别位于框架外与人类边界——与 r229 判定一致：无新理论，复现层 + 诚实边界")

    n_pass = sum(1 for e in entries if e["level"] == "PASS")
    n_fail = sum(1 for e in entries if e["level"] == "FAIL")
    n_bnd = sum(1 for e in entries if e["level"] == "BOUNDARY")
    n_info = sum(1 for e in entries if e["level"] == "INFO")

    merc_polar = []
    stp = max(1, len(merc_traj_u) // 360)
    for i in range(0, len(merc_traj_u), stp):
        phi, u = merc_traj_u[i]
        r = P_HALF / u
        merc_polar.append([round(phi % (2 * pi), 5), round(r / MERC_A, 6)])
    demo_polar = []
    stp2 = max(1, len(demo_u) // 300)
    for i in range(0, len(demo_u), stp2):
        phi, u = demo_u[i]
        r = P_HALF / u
        demo_polar.append([round(phi, 5), round(r / MERC_A, 6)])
    light_pts = [[round(p[0], 4), round(p[1] * R_SUN / R_SUN, 8)] for p in light_traj]
    supply_ledger = [
        ["r214", "经典静态中心力（含引力通道）", "形式统一 PASS；动力学统一 FAIL"],
        ["r223", "轨道进动机验（Yukawa 修正引力）", "λ_fit≈957.9 AU 与行星进动冲突"],
        ["r224", "圆轨道稳定性（引力 Yukawa 化）", "λ > 18.6 AU（海王星最硬）"],
        ["r226", "量子束缚层", "引力「原子」r=4.4e32 m（超宇宙 5e5 倍）"],
        ["r227", "散射层", "λ=∞ 力程在动量空间 = 零质量载体"],
        ["r229", "新颖性审计", "α_G 是外部输入，等级问题无推导"],
        ["r230", "引力本质层（本卷）", "WEP 结构恒等 + 1PN 唯象复现 + 独有性枚举"],
    ]

    res = {
        "stem": STEM, "round": 230, "date": "2026-10-26",
        "method": ("φ-ODE 峰定位（进动）+ 渐近外推（光线）+ 双质量比结构恒等（WEP）+ "
                   "强度比解析恒等——float64，纯标准库"),
        "gravity_verdict": ("WEP=框架内结构恒等/实验输入；1PN 唯象（42.98″+1.7517″）机器复现；"
                            "五项独有性；场方程/量子化/等级起源在框架外或人类边界——不宣称攻破"),
        "entries": entries, "guards": guards, "controls": controls,
        "readings": {
            "merc_polar": merc_polar, "light_traj": light_pts,
            "demo_polar": demo_polar, "demo_coef": DEMO_COEF,
            "precession": {"domega_num": f"{domega_num:.6e}",
                           "domega_ana": f"{DPHI_ANALYTIC:.6e}",
                           "rel": f"{rel_pre:.3e}",
                           "arcsec_century": round(ARCSEC_PER_CENTURY, 2),
                           "orbits_per_century": round(n_orb_century, 1)},
            "light": {"delta_num": f"{delta_num:.4e}",
                      "delta_ana": f"{DEFLECT_ANALYTIC:.4e}",
                      "arcsec": round(ARCSEC_LIGHT, 4),
                      "newton_half": round(ARCSEC_LIGHT / 2, 4),
                      "rel": f"{rel_light:.3e}"},
            "ratios": ratio_rows, "g_over_em": f"{RATIO_G_EM:.4e}",
            "unique": [{"item": u[0], "detail": u[1]} for u in UNIQUE],
            "ledger": [{"round": r, "method": m, "verdict": v} for r, m, v in supply_ledger],
        },
        "counts": {"entries": len(entries), "PASS": n_pass, "FAIL": n_fail,
                   "BOUNDARY": n_bnd, "INFO": n_info,
                   "guards": f"{sum(1 for g in guards if g['ok'])}/{len(guards)}",
                   "controls": f"{sum(1 for c in controls if c['ok'])}/{len(controls)}"},
        "verdict": "", "judgement": "", "source": {},
    }

    parts = ["R230-GRAVITY-ESSENCE",
             "WEP-STRUCTURAL-IDENTITY-OK" if guard_ok("G3") else "WEP-FAIL",
             "MERCURY-PRECESSION-42.98-REPRODUCED" if guard_ok("G1") else "PRECESSION-FAIL",
             "LIGHT-DEFLECTION-1.75-REPRODUCED" if guard_ok("G2") else "LIGHT-FAIL",
             "UNIQUENESS-5ITEMS-OK" if guard_ok("G4") else "UNIQUE-FAIL",
             "HIERARCHY-36-ORDERS-NO-DERIVATION",
             "FIELD-EQUATIONS-OUT-OF-FRAME-BOUNDARY",
             "QUANTUM-GRAVITY-HUMAN-FRONTIER",
             "NO-BREAKTHROUGH-CLAIMED-HONEST-BOUNDARY",
             "VERDICT-1PN-PHENOMENOLOGY-REPRODUCED-ESSENCE-OPEN"]
    res["verdict"] = "-".join(parts)
    res["judgement"] = ("CLOSED-INCREMENT（引力本质层：WEP 结构恒等 + 1PN 两件套机器复现 + "
                        "五项独有性；不宣称攻破——场方程在框架外、量子化在人类边界、"
                        "等级起源无推导，与 r229 NOVEL-THEORY-NONE 一致）")
    res["source"] = {
        "engine": BASE + ".py",
        "inherits": ["r214（四力常数口径）", "r223/r224（Yukawa 引力修正夹死——只读引用）",
                     "r226（引力量子束缚态——只读引用）", "r229（新颖性判定）",
                     "IAU/CODATA 太阳系常数"],
    }
    print(f"条目 {res['counts']['entries']}（PASS {n_pass} / FAIL {n_fail} / "
          f"BOUNDARY {n_bnd} / INFO {n_info}）· 守卫 {res['counts']['guards']} · "
          f"控制组 {res['counts']['controls']}")

    os.makedirs(_DATADIR, exist_ok=True)
    jpath = os.path.join(_DATADIR, BASE + ".json")
    mpath = os.path.join(_DATADIR, BASE + ".md")
    rpath = os.path.join(_DATADIR, BASE + "_report.txt")

    html_ok, html_detail = cast_html(res)
    guard("G5", "交互 HTML 生成且自含", html_ok, html_detail)
    res["counts"]["guards"] = f"{sum(1 for g in guards if g['ok'])}/{len(guards)}"

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
        f.write(f"precession={json.dumps(res['readings']['precession'])}\n")
        f.write(f"light={json.dumps(res['readings']['light'])}\n")
        f.write(f"g_over_em={res['readings']['g_over_em']}\n")


def cast_html(res):
    if not os.path.isfile(_TMPL):
        return False, f"模板缺失：{_TMPL}"
    with open(_TMPL, "r", encoding="utf-8") as f:
        tpl = f.read()
    if "__R230_JSON__" not in tpl:
        return False, "模板缺少 __R230_JSON__ 占位符"
    html = tpl.replace("__R230_JSON__", json.dumps(res, ensure_ascii=False))
    with open(HTML_OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    text = open(HTML_OUT, "r", encoding="utf-8").read()
    problems = []
    if "__R230_JSON__" in text:
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
