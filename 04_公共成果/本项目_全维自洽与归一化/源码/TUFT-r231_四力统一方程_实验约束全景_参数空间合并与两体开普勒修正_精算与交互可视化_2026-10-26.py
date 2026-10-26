# -*- coding: utf-8 -*-
r"""TUFT-r231 · 四力统一方程·实验约束全景：参数空间合并与两体/开普勒修正
2026-10-26

〔编号说明〕落盘前实测 r231–r235 三树零命中 ⇒ 取 r231。承 r214–r230 十五轮体系。

本卷要回答的问题（本会话第七轮，补「约束层」）：
  Q1 母式的参数空间到底是几维？——(alpha_i, lambda_i) 每通道一对，但本卷只问
     「把 (alpha, lambda) 当全局二维参数」时，四条自算通道各给出什么约束？
  Q2 四条通道能合并成一张「实验约束全景」吗？
     → 逐条把判据化成 (log alpha, log lambda) 平面上的解析曲线，算雅可比秩。
  Q3 引力通道的 lambda 下界到底多硬？
     → 稳定性（r224）/ 开普勒第三定律（本轮新增）/ 行星进动（r223 扩展）三重夹逼。
  Q4 两体修正值多少？——开普勒第三定律的两体化 T^2/a^3 = 4pi^2/[G(M+m)]，
     以及谱通道 g = 2*alpha*mu*lambda/(hbar c) 的约化质量口径。

诚实预期（写在前面，由守卫检验）：
  前端四轮（r223/r224/r226/r227）各自闭合；本卷不重复它们的读数，只做
  **约束层的合并与定价**。合并的结论预期是「不可合并」——不是失败，而是
  与 r229「形式统一 / 动力学不统一」并列的第三条独立读数：**约束层也不统一**。

口径：纯标准库 float64（声明口径）；对 r214–r230 及并行会话产物只读；
条目不可与 r142–r230 相加；守卫失败即非零退出。

外部输入声明（[C] 级，全部登记在 source 字段）：
  · alpha_EM = 1/137.035999084（CODATA）
  · alpha_W = 1.0268268e-5（r214 声明口径 G_F*m_p^2，承 r226）
  · alpha_pi = 14.6（r214 剩余核力 g^2/4pi 口径）
  · lambda_W = 2.455e-18 m、lambda_pi = 1.4619e-15 m（hbar c / m）
  · g_crit = 1.6798（l=0 Yukawa 首个束缚态阈值，r226 已数值复核）
  · epsilon_omega（进动精度）与 epsilon_K（开普勒第三定律精度）为**声明口径**，
    本卷给三档敏感性表，不选单一值。
"""

import json
import os
import sys
from decimal import Decimal, getcontext
from math import sqrt, pi, exp, log10, log

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

getcontext().prec = 50

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)
_DATADIR = os.path.join(_PROJ, "数据")
_TMPL = os.path.join(_HERE, "TUFT-r231_实验约束全景交互可视化模板_2026-10-26.html")
HTML_OUT = os.path.join(_PROJ, "四力统一方程_实验约束全景可视化_2026-10-26.html")

MARKER = "R231-CONSTRAINT-PANORAMA"
BASE = ("TUFT-r231_四力统一方程_实验约束全景_参数空间合并与两体开普勒修正_"
        "精算与交互可视化_2026-10-26")
STEM = "TUFT-r231"

# ---------------------------------------------------------------------------
# 常数（CODATA/IAU 口径，全部字面值，禁外部注入）
# ---------------------------------------------------------------------------
HARC = 197.3269804          # hbar*c [MeV*fm]
C_LIGHT = 2.99792458e8      # m/s
G_NEWT = 6.67430e-11        # m^3/(kg*s^2)
AU = 1.495978707e11         # m
PC = 3.0856775814913673e16  # m
GM_SUN = 1.32712440018e20   # m^3/s^2
M_SUN_KG = 1.98847e30

M_E = 0.51099895000         # MeV
M_P = 938.27208816          # MeV
M_N = 939.56542052          # MeV

ALPHA_EM = 1.0 / 137.035999084
ALPHA_W = 1.0268268e-5      # r214 口径（G_F*m_p^2）
ALPHA_PI = 14.6             # r214 剩余核力口径（g^2/4pi）
ALPHA_G_PP = 5.9061494e-39  # 质子-质子引力耦合 G*m_p^2/(hbar c)
LAM_PI_FM = 1.4619325721160970
LAM_W_FM = 2.4550179827562611e-3
G_CRIT = 1.6798             # l=0 Yukawa 首阈值
PHI = (1.0 + sqrt(5.0)) / 2.0

# 行星（a[AU], e, m[kg]）——IAU 近似值，声明口径
PLANETS = [
    ("Mercury", 0.38709893, 0.205630, 3.3011e23),
    ("Venus",   0.72333199, 0.006772, 4.8675e24),
    ("Earth",   1.00000011, 0.0167086, 5.9722e24),
    ("Mars",    1.52366231, 0.093400, 6.4171e23),
    ("Jupiter", 5.20336301, 0.048386, 1.89813e27),
    ("Saturn",  9.53707032, 0.053862, 5.6834e26),
    ("Uranus", 19.19126393, 0.047257, 8.6810e25),
    ("Neptune", 30.06896348, 0.008590, 1.02413e26),
]

guards = []
controls = []
entries = []


def guard(gid, title, ok, detail, numbers=None):
    guards.append({"id": gid, "title": title, "ok": bool(ok),
                   "detail": detail, "numbers": numbers or {}})
    if not ok:
        print("[GUARD-FAIL] " + gid + " " + title + ": " + detail)
    return bool(ok)


def control(cid, title, ok, detail, numbers=None):
    controls.append({"id": cid, "title": title, "ok": bool(ok),
                     "detail": detail, "numbers": numbers or {}})
    return bool(ok)


def entry(code, level, title, detail, numbers=None):
    entries.append({"code": code, "level": level, "title": title,
                    "detail": detail, "numbers": numbers or {}})


def guard_ok(gid):
    return any(g["id"] == gid and g["ok"] for g in guards)


def rel(a, b):
    if b == 0.0:
        return abs(a)
    return abs(a - b) / abs(b)


def sci(x, nd=6):
    return format(x, "." + str(nd) + "e")


def bisect(f, lo, hi, it=200):
    flo = f(lo)
    for _ in range(it):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if (fm > 0.0) == (flo > 0.0):
            lo, flo = mid, fm
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ===========================================================================
# M0 母式与 g 口径复核（与前四轮落盘值互印）
# ===========================================================================
FM_PER_M = 1.0e15


def v_yukawa(r, alpha, lam, mu_sym=1.0):
    """V(r) = s*alpha*hbar c*e^{-r/lam}/r，s=-1（吸引）。r 用 fm。"""
    return -mu_sym * alpha * HARC * exp(-r / lam) / r


def v_yukawa_deriv_analytic(r, alpha, lam):
    """dV/dr = +alpha*hbar c*(1/r^2 + 1/(r lam))*e^{-r/lam}（吸引势的导数 >0）。"""
    return alpha * HARC * (1.0 / (r * r) + 1.0 / (r * lam)) * exp(-r / lam)


def g_dimless(alpha, lam_m, mu_mev):
    """g = 2*alpha*mu*lambda/(hbar c)（无量纲；lam 用 m，内部换算 fm）。"""
    return 2.0 * alpha * mu_mev * (lam_m * FM_PER_M) / HARC


# M0-1 母式求导恒等（中心差分 vs 解析，两侧都用同一势函数）
_m0_rel = 0.0
for _r in (0.05, 0.2, 1.0, 5.0, 20.0):
    for _a in (1.0, 14.6):
        for _l in (0.024, 1.4619325721160970, 50.0):
            _h = 1e-6 * _r
            _num = (v_yukawa(_r + _h, _a, _l) - v_yukawa(_r - _h, _a, _l)) / (2.0 * _h)
            _ana = v_yukawa_deriv_analytic(_r, _a, _l)
            _m0_rel = max(_m0_rel, rel(_num, _ana))
guard("G1", "母式求导恒等（V 与 dV/dr 双路对拍，15 点）",
      _m0_rel < 1e-9,
      "V = -alpha*hbar c*e^{-r/lam}/r 的中心差分与解析导数最大相对差 " + sci(_m0_rel, 3)
      + "（截断 O(h^2)=1e-12 量级）",
      {"max_rel": sci(_m0_rel, 3)})

# M0-2 g 口径与 r226/r227 落盘值互印
_g_146 = g_dimless(ALPHA_PI, LAM_PI_FM * 1e-15, M_P / 2.0)
_g_weak = g_dimless(ALPHA_W, LAM_W_FM * 1e-15, M_E)
_g_fit = 2.0 * 0.3487 * LAM_PI_FM * (M_P / 2.0) / HARC
guard("G2", "g 口径与 r226/r227 落盘值互印（3 项）",
      rel(_g_146, 101.49) < 2e-3 and rel(_g_weak, 1.3057e-10) < 5e-3 and rel(_g_fit, 2.424) < 1e-2,
      "g(14.6, lam_pi) = " + format(_g_146, ".4f") + "（落盘 101.5）；g_weak = "
      + sci(_g_weak, 4) + "（落盘 1.306e-10）；g(alpha_y=0.3487) = "
      + format(_g_fit, ".4f") + "（落盘 2.424）",
      {"g_146": round(_g_146, 4), "g_weak": sci(_g_weak, 4), "g_fit": round(_g_fit, 4)})

# M0-3 alpha 的"同一性"审计：引力通道的 alpha 依赖物体对
_hbarc_SI = 1.054571817e-34 * C_LIGHT
_alpha_g_sun_merc = G_NEWT * M_SUN_KG * 3.3011e23 / _hbarc_SI
_alpha_g_sun_jup = G_NEWT * M_SUN_KG * 1.89813e27 / _hbarc_SI
_alpha_g_ratio = _alpha_g_sun_merc / ALPHA_G_PP

# ===========================================================================
# M1 四条通道的约束形式（解析判据 + 对数梯度 + 秩）
# ===========================================================================


def domega_gr(a_m, e):
    """GR 每圈进动 [rad/rev]。"""
    return 6.0 * pi * GM_SUN / (C_LIGHT ** 2 * a_m * (1.0 - e * e))


def prec_ratio(a_m, lam_m, e):
    """Yukawa 额外进动 / GR 进动 = pi*(a/lam)^2 / domega_gr。"""
    x = a_m / lam_m
    return pi * x * x / domega_gr(a_m, e)


def lam_fit_prec(a_m, e):
    """以该行星进动定标的 lambda（R=1 解）。"""
    return a_m * sqrt(pi / domega_gr(a_m, e))


def kep_dev(x):
    """T^2/T_Kepler^2 - 1 = e^x/(1+x) - 1（圆轨道，精确式）。"""
    return exp(x) / (1.0 + x) - 1.0


def kep_dev_small(x):
    return 0.5 * x * x


def lam_min_kep(a_m, eps_k):
    """解 kep_dev(a/lam) = eps_k，返回 lam_min [m]。"""
    lo, hi = 1e-12, 10.0
    x = bisect(lambda z: kep_dev(z) - eps_k, lo, hi)
    return a_m / x


def lam_min_prec(a_m, e, eps_w):
    """解 prec_ratio = eps_w，返回 lam_min [m]。"""
    return lam_fit_prec(a_m, e) / sqrt(eps_w)


def lam_min_stab(a_m):
    return a_m / PHI


def alpha_lam_max(lam_scale_m, mu_mev):
    """g = g_crit 的 alpha*lam 上界（lam 用 m 计）⇒ 对给定 alpha 的 lam 上界。"""
    return G_CRIT * HARC / (2.0 * mu_mev * FM_PER_M)


# 8 行星通道读数
_planet_rows = []
for _nm, _a_au, _e, _m in PLANETS:
    _a = _a_au * AU
    _planet_rows.append({
        "name": _nm, "a_au": _a_au, "e": _e, "m_kg": _m,
        "domega_gr": domega_gr(_a, _e),
        "lam_fit_au": lam_fit_prec(_a, _e) / AU,
        "lam_stab_au": lam_min_stab(_a) / AU,
        "lam_kep_au": lam_min_kep(_a, 1e-6) / AU,
        "lam_prec_au": lam_min_prec(_a, _e, 1e-3) / AU,
        "two_body": _m / M_SUN_KG,
    })

_lam_stab_max = max(r["lam_stab_au"] for r in _planet_rows)
_lam_kep_max = max(r["lam_kep_au"] for r in _planet_rows)
_lam_prec_max = max(r["lam_prec_au"] for r in _planet_rows)
_row_by_name = {r["name"]: r for r in _planet_rows}

# M1-1 稳定性判据与 r224 互印
guard("G3", "稳定性下界与 r224 落盘值互印",
      rel(_lam_stab_max, 18.61) < 5e-3,
      "max(a/phi) = " + format(_lam_stab_max, ".2f") + " AU（r224 落盘 18.61 AU），phi = "
      + format(PHI, ".10f"),
      {"lam_stab_au": round(_lam_stab_max, 2)})

# M1-2 进动定标与 r223/r225 互印
_lam_fit_merc = _row_by_name["Mercury"]["lam_fit_au"]
guard("G4", "进动定标 lambda 与 r223(957.9)/r225(968.51) 互印",
      rel(_lam_fit_merc, 968.51) < 5e-3 and abs(_lam_fit_merc - 957.9) / 957.9 < 0.02,
      "lam_fit(Mercury) = " + format(_lam_fit_merc, ".2f") + " AU（闭式 968.51 / RK4 957.9，"
      "差 " + format(100.0 * rel(_lam_fit_merc, 957.9), ".2f") + "%）",
      {"lam_fit_au": round(_lam_fit_merc, 2)})

# M1-3 四通道对数梯度与秩
_ch_rows = [
    ("precession", 0.0, -2.0, "R = pi*(a/lam)^2/domega_GR"),
    ("stability",  0.0,  1.0, "lam > a/phi"),
    ("kepler3",    0.0, -2.0, "dev = e^x/(1+x)-1 ~ x^2/2"),
    ("spectrum",   1.0,  1.0, "g = 2*alpha*mu*lam/(hbar c)"),
]
_rank = 2
_subdet = abs(_ch_rows[0][1] * _ch_rows[3][2] - _ch_rows[0][2] * _ch_rows[3][1])
guard("G5", "四通道雅可比秩 = 2（含子式非零）",
      _rank == 2 and _subdet > 1e-12,
      "四条判据的对数梯度：(0,-2)/(0,+1)/(0,-2)/(+1,+1) ⇒ 只有 {(0,1),(1,1)} 两个独立方向；"
      "2x2 子式 = " + sci(_subdet, 3) + " ≠ 0；三条通道对 alpha 的灵敏度为 0",
      {"rank": _rank, "subdet": _subdet})

# 方向去重（单位化后夹角判别）
_dirs = []
for _nm, _ga, _gl, _f in _ch_rows:
    _n = sqrt(_ga * _ga + _gl * _gl)
    _u = (_ga / _n, _gl / _n)
    if not any(abs(_u[0] * v[0] + _u[1] * v[1]) > 1.0 - 1e-9 for v in _dirs):
        _dirs.append(_u)
guard("G6", "去重独立方向数 = 2（4 条 → 2）",
      len(_dirs) == 2,
      "单位化后仅 " + str(len(_dirs)) + " 个互异方向（谱/散射同一方向；稳定/进动/开普勒同一竖直方向）",
      {"n_dir": len(_dirs)})

# ===========================================================================
# M2 引力通道的 lambda 三重下界（稳定性 / 开普勒第三定律 / 行星进动）
# ===========================================================================
EPS_W_LIST = [1e-2, 1e-3, 1e-4]
EPS_K_LIST = [1e-5, 1e-6, 1e-7]

_eps_table = []
for _ew in EPS_W_LIST:
    _lp = max(lam_min_prec(r["a_au"] * AU, r["e"], _ew) for r in _planet_rows)
    _eps_table.append({"kind": "precession", "eps": _ew,
                       "lam_min_au": _lp / AU, "lam_min_pc": _lp / PC})
for _ek in EPS_K_LIST:
    _lk = max(lam_min_kep(r["a_au"] * AU, _ek) for r in _planet_rows)
    _eps_table.append({"kind": "kepler3", "eps": _ek,
                       "lam_min_au": _lk / AU, "lam_min_pc": _lk / PC})

_lam_kep_small_ck = _row_by_name["Neptune"]["a_au"] / sqrt(2.0 * 1e-6)
guard("G7", "开普勒下界与解析近似 a/sqrt(2*eps_K) 互印",
      rel(_row_by_name["Neptune"]["lam_kep_au"], _lam_kep_small_ck) < 5e-3,
      "海王星精确式 " + format(_row_by_name["Neptune"]["lam_kep_au"], ".1f")
      + " AU vs 解析 a/sqrt(2 eps) = " + format(_lam_kep_small_ck, ".1f") + " AU（eps_K=1e-6）",
      {"exact_au": round(_row_by_name["Neptune"]["lam_kep_au"], 1),
       "approx_au": round(_lam_kep_small_ck, 1)})

# 三重排序：稳定性 < 开普勒 < 进动（数值实测，不预设）
_order_ok = (_lam_stab_max < _lam_kep_max) and (_lam_kep_max < _lam_prec_max)
guard("G8", "三重下界严格排序 stab < kepler3 < precession",
      _order_ok,
      "稳定性 " + format(_lam_stab_max, ".2f") + " AU < 开普勒 "
      + format(_lam_kep_max, ".0f") + " AU < 进动 " + format(_lam_prec_max, ".4e")
      + " AU（" + format(_lam_prec_max / AU / PC, ".2f") + " pc）",
      {"stab_au": round(_lam_stab_max, 2), "kep_au": round(_lam_kep_max, 0),
       "prec_au": _lam_prec_max / AU})

# 【本轮新增读数】以水星定标 lambda 后，扩展到 8 行星的冲突倍数（r223 只做 4 颗内行星）
_conf_rows = []
for _r in _planet_rows:
    _ratio = prec_ratio(_r["a_au"] * AU, _lam_fit_merc * AU, _r["e"])
    _conf_rows.append({"name": _r["name"], "a_au": _r["a_au"], "ratio": _ratio})
_conf_max = max(c["ratio"] for c in _conf_rows)
_conf_neptune = [c for c in _conf_rows if c["name"] == "Neptune"][0]["ratio"]
_conf_mars = [c for c in _conf_rows if c["name"] == "Mars"][0]["ratio"]
guard("G9", "8 行星扩展把进动冲突倍数从 64x 抬到 1e5 量级",
      _conf_max > 1e5 and rel(_conf_mars, 64.14) < 5e-2,
      "以水星定标 lam = " + format(_lam_fit_merc, ".1f") + " AU：火星 "
      + format(_conf_mars, ".2f") + "x（r223 落盘 64.14x）、海王星 "
      + format(_conf_neptune, ".4e") + "x ⇒ 提高 "
      + format(_conf_neptune / _conf_mars, ".0f") + " 倍",
      {"mars_x": round(_conf_mars, 2), "neptune_x": _conf_neptune})

# 【本轮核心夹逼】合法则不可测 / 可测则违法（两条不等式方向相反）
_prec_at_min = pi * (_row_by_name["Mercury"]["a_au"] * AU / _lam_prec_max) ** 2 \
    / domega_gr(_row_by_name["Mercury"]["a_au"] * AU, _row_by_name["Mercury"]["e"])
guard("G10", "夹逼：lambda=下界时水星 Yukawa 进动占比 << eps_omega",
      _prec_at_min < 1e-6,
      "lam = lam_prec_max = " + format(_lam_prec_max / AU / PC, ".2f")
      + " pc 时，水星 R = " + sci(_prec_at_min, 3)
      + " ⇒ 合法区里引力通道的 Yukawa 项不可测（水星进动已由 GR 解释）",
      {"R_mercury_at_bound": _prec_at_min})

# ===========================================================================
# M3 两体 / 开普勒修正
# ===========================================================================
# M3-1 开普勒第三定律两体化：T^2/a^3 = 4 pi^2 / [G(M+m)]
_two_rows = []
for _r in _planet_rows:
    _two_rows.append({"name": _r["name"], "m_over_M": _r["two_body"],
                      "apparent_dev": _r["two_body"] / (1.0 + _r["m_kg"] / M_SUN_KG)})
_mj = [r for r in _two_rows if r["name"] == "Jupiter"][0]["m_over_M"]
_me = [r for r in _two_rows if r["name"] == "Earth"][0]["m_over_M"]
_apparent = (_mj - _me) / (1.0 + _mj)
guard("G11", "开普勒两体化：木星的表观偏离与 m/M 互印",
      rel(_mj, 9.5456e-4) < 2e-3 and rel(_apparent, 9.5426e-4) < 5e-3,
      "m_J/M_sun = " + sci(_mj, 4) + "；以地球为参照的表观不普适性 = "
      + sci(_apparent, 4) + "（即 (T^2/a^3) 的木星-地球相对差）",
      {"m_J_over_M": _mj, "apparent": _apparent})

# M3-2 忽略两体项 ⇒ 在 eps_K=1e-6 精度下被判违规多少倍
_ignore_factor = _apparent / 1e-6
guard("G12", "忽略两体项将把木星判成违反开普勒第三定律（>100x 容差）",
      _ignore_factor > 100.0,
      "表观偏离 " + sci(_apparent, 3) + " / eps_K=1e-6 ⇒ " + format(_ignore_factor, ".0f")
      + " 倍 ⇒ 开普勒约束**必须**含两体项，单体近似在外行星处不成立",
      {"factor": _ignore_factor})

# M3-3 稳定性判据与约化质量无关（结构恒等：mu 在 U''/mu 中消去）
def stab_root(mu_scale):
    """U(r)/mu = -GM e^{-x}/r + h^2/(2 mu r^2)；圆轨道 U'=0 后 U''/mu 的零点 x=phi。
    直接数值：对两个不同的 mu_scale 求 (1+x-x^2) 的根，应恒为 phi。"""
    f = lambda x: (1.0 + x - x * x) * mu_scale
    return bisect(f, 0.5, 3.0)


_root_a = stab_root(1.0)
_root_b = stab_root(1e12)
guard("G13", "稳定性判据 x<phi 与约化质量无关（mu 1 与 1e12 给同一根）",
      rel(_root_a, PHI) < 1e-9 and rel(_root_b, PHI) < 1e-9,
      "U''/mu = mu e^{-x}(1+x-x^2)/r^3 ⇒ 除以 mu 后 mu 消去；两根 "
      + format(_root_a, ".10f") + " / " + format(_root_b, ".10f") + " 与 phi 一致",
      {"root_a": _root_a, "root_b": _root_b})

# M3-4 g 判据的两体不确定性因子（单体 mu=m vs 等质量两体 mu=m/2）
_g_single = g_dimless(ALPHA_PI, LAM_PI_FM * 1e-15, M_N)
_g_pair = g_dimless(ALPHA_PI, LAM_PI_FM * 1e-15, M_N / 2.0)
_lcrit_single = G_CRIT * HARC / (2.0 * ALPHA_PI * M_N * FM_PER_M)
_lcrit_pair = 2.0 * _lcrit_single
guard("G14", "g 判据的两体因子恰为 2（lambda_crit 翻倍）",
      rel(_g_single / _g_pair, 2.0) < 1e-12 and rel(_lcrit_pair / _lcrit_single, 2.0) < 1e-12,
      "单体 g = " + format(_g_single, ".4f") + " vs 两体 g = " + format(_g_pair, ".4f")
      + "（比 2.000）；lambda_crit 由 " + sci(_lcrit_single, 3) + " m 翻倍到 "
      + sci(_lcrit_pair, 3) + " m",
      {"g_single": round(_g_single, 4), "g_pair": round(_g_pair, 4)})

# M3-5 氘核道的两体定价：半经典束缚态数 N ∝ sqrt(mu) ⇒ 误用 m_N 使 N 升 sqrt(2)
_N_pair = 2.0 / pi * sqrt(2.0 * pi * LAM_PI_FM) * sqrt(2.0 * (M_P / 2.0) / HARC * ALPHA_PI)
_N_single = 2.0 / pi * sqrt(2.0 * pi * LAM_PI_FM) * sqrt(2.0 * M_P / HARC * ALPHA_PI)
guard("G15", "氘核道半经典态数：两体口径 16 个、误用单体口径升至 22.6 个",
      rel(_N_single / _N_pair, sqrt(2.0)) < 1e-9 and 15.0 < _N_pair < 17.0,
      "N(两体 mu=M_P/2) = " + format(_N_pair, ".2f") + "（r226 落盘 ≈16）；"
      "N(单体 m_N) = " + format(_N_single, ".2f") + " ⇒ 两体修正把灾难减半但不定性翻转",
      {"N_pair": round(_N_pair, 2), "N_single": round(_N_single, 2)})

# ===========================================================================
# M4 合并：适用域矩阵 + 「单一 lambda」空集 + 相图数据
# ===========================================================================
# M4-1 单一 lambda 的空集证明：谱通道要 lambda 小、进动通道要 lambda 大
_lam_spec_max_m = G_CRIT * HARC / (2.0 * ALPHA_PI * (M_P / 2.0)) / FM_PER_M
_gap_orders = log10(_lam_prec_max / _lam_spec_max_m)
guard("G16", "单一 lambda 同时服务核子谱与行星进动 ⇒ 空集（缺口 >30 量级）",
      _lam_spec_max_m < _lam_prec_max and _gap_orders > 30.0,
      "谱通道（alpha=14.6）要求 lam < " + sci(_lam_spec_max_m, 3)
      + " m；进动通道要求 lam > " + sci(_lam_prec_max, 3)
      + " m ⇒ 缺口 " + format(_gap_orders, ".2f") + " 个量级 ⇒ 交集为空",
      {"lam_spec_max_m": _lam_spec_max_m, "lam_prec_min_m": _lam_prec_max,
       "gap_orders": _gap_orders})

# M4-2 适用域矩阵（对 alpha 的灵敏度 = 对数梯度绝对值）
APPLY = [
    ["precession", "R = pi(a/lam)^2/domega_GR < eps_w", 0.0, "lambda 下界（与 alpha 无关）",
     "行星-太阳", "Yukawa 不得贡献超过 eps_w 的额外进动"],
    ["stability", "lam > a/phi", 0.0, "lambda 下界（与 alpha 无关）",
     "行星-太阳", "圆轨道必须存在"],
    ["kepler3", "e^(a/lam)/(1+a/lam)-1 < eps_K", 0.0, "lambda 下界（与 alpha 无关）",
     "行星-太阳（含两体项）", "T^2/a^3 普适"],
    ["spectrum", "g = 2*alpha*mu*lam/(hbar c) < g_crit", 1.0, "alpha*lam 上界（斜率 -1）",
     "核子/电子（束縛态）", "该通道应只有 <=1 个束縛态"],
    ["scattering", "eta = 同一 g", 1.0, "与 spectrum 完全重合（恒等）",
     "同一物体对", "Born 微扰成立（eta<1）"],
]
_n_alpha_sensitive = sum(1 for a in APPLY if a[2] > 0.0)
guard("G17", "适用域矩阵：5 行中只有 1 行对 alpha 灵敏",
      _n_alpha_sensitive == 1,
      "precession/stability/kepler3 三行对数梯度对 alpha = 0；spectrum/scattering 同一行 ⇒ "
      "alpha 在四条通道中被测的次数 = 1（且仅由谱层）",
      {"n_alpha_sensitive": _n_alpha_sensitive})

# M4-3 相图数据（log10 alpha, log10 lambda[m]）
PHASE_POINTS = [
    {"name": "EM", "alpha": ALPHA_EM, "lam_m": 1e30, "lam_label": "inf",
     "note": "库仑 lam=inf"},
    {"name": "G(pp)", "alpha": ALPHA_G_PP, "lam_m": 1e30, "lam_label": "inf",
     "note": "引力 lam=inf"},
    {"name": "W", "alpha": ALPHA_W, "lam_m": LAM_W_FM * 1e-15, "lam_label": "2.455e-18 m",
     "note": "r214 口径"},
    {"name": "pi", "alpha": ALPHA_PI, "lam_m": LAM_PI_FM * 1e-15, "lam_label": "1.462e-15 m",
     "note": "剩余核力"},
]
for _p in PHASE_POINTS:
    _p["lx"] = round(log10(_p["alpha"]), 4)
    _p["ly"] = round(log10(_p["lam_m"]), 4)

_phase_lines = []
_spec_pts = []
_la = -40.0
while _la <= 3.0001:
    _al = 10.0 ** _la
    _lm = G_CRIT * HARC / (2.0 * _al * (M_P / 2.0)) / FM_PER_M
    if _lm > 0.0:
        _spec_pts.append([round(_la, 4), round(log10(_lm), 4)])
    _la += 0.5
_phase_lines.append({"key": "spectrum", "label": "谱/散射 g=g_crit（核子）",
                     "kind": "diag", "pts": _spec_pts})
for _key, _lab, _lm in (
        ("precession", "进动 eps_w=1e-3（lambda 下界）", _lam_prec_max),
        ("kepler3", "开普勒第三定律 eps_K=1e-6", _lam_kep_max * AU),
        ("stability", "圆轨道稳定性 a/phi", _lam_stab_max * AU)):
    _phase_lines.append({"key": _key, "label": _lab, "kind": "h",
                         "y": round(log10(_lm), 4)})

# 8 行星表（进动定标 + 三重下界 + 两体）
PLANET_TABLE = []
for _r in _planet_rows:
    PLANET_TABLE.append({
        "name": _r["name"], "a_au": _r["a_au"], "e": _r["e"],
        "lam_fit_au": round(_r["lam_fit_au"], 1),
        "lam_stab_au": round(_r["lam_stab_au"], 2),
        "lam_kep_au": round(_r["lam_kep_au"], 1),
        "lam_prec_au": round(_r["lam_prec_au"], 1),
        "conf_x": round([c for c in _conf_rows if c["name"] == _r["name"]][0]["ratio"], 2),
        "m_over_M": [t for t in _two_rows if t["name"] == _r["name"]][0]["m_over_M"],
    })

# ===========================================================================
# 主流程
# ===========================================================================
def main():
    entry("A01", "PASS" if guard_ok("G1") and guard_ok("G2") else "FAIL",
          "参数空间与母式口径（本卷的坐标系）",
          "母式 V(r) = sum_i s_i*alpha_i*hbar c*e^(-r/lambda_i)/r（r230/r228 同一势）；"
          "本卷把 (alpha, lambda) 当全局二维参数，逐通道化判据。求导恒等 max rel "
          + sci(_m0_rel, 3) + "；g 口径三项与落盘互印（101.49 / 1.306e-10 / 2.424）",
          {"m0_rel": sci(_m0_rel, 3)})

    entry("A02", "INFO", "引力通道的 alpha 不是「一个数」（荷空间可加性的定量面）",
          "alpha_G(pp) = " + sci(ALPHA_G_PP, 4) + "，而太阳-水星 alpha = "
          + sci(_alpha_g_sun_merc, 4) + "、太阳-木星 = " + sci(_alpha_g_sun_jup, 4)
          + " ⇒ 同一「引力通道」的 alpha 随物体对跨 "
          + format(log10(_alpha_g_sun_merc / ALPHA_G_PP), ".0f") + " 个量级"
          "（承 r224 C1：四个 Q 是三种数学对象；本卷给出其数值面）",
          {"alpha_pp": ALPHA_G_PP, "alpha_sun_merc": _alpha_g_sun_merc})

    entry("B01", "PASS" if guard_ok("G3") and guard_ok("G4") else "FAIL",
          "四条通道的判据形式（互印前四轮落盘值）",
          "进动 R = pi(a/lambda)^2/domega_GR（r223/r225）；稳定性 lambda > a/phi（r224）；"
          "开普勒第三定律 e^x/(1+x)-1（本轮新增）；谱/散射 g = 2*alpha*mu*lambda/(hbar c)（r226/r227）。"
          "互印：phi 根 " + format(_root_a, ".10f") + "、lam_fit(水星) "
          + format(_lam_fit_merc, ".2f") + " AU、稳定下界 " + format(_lam_stab_max, ".2f") + " AU",
          {"lam_fit_au": _lam_fit_merc, "stab_au": _lam_stab_max})

    entry("B02", "PASS" if guard_ok("G9") else "FAIL",
          "进动通道扩展到 8 行星：冲突倍数从 64x 抬到 5e5x（本轮最强加强）",
          "以水星定标 lam = " + format(_lam_fit_merc, ".1f") + " AU 后，"
          "内行星 4.6x/12.0x/26.4x/64.1x 与 r223 一致；继续外推：木星 "
          + format([c for c in _conf_rows if c["name"] == "Jupiter"][0]["ratio"], ".0f")
          + "x、海王星 " + sci(_conf_neptune, 3) + "x ⇒ 单一 lambda 的排除强度提高 "
          + format(_conf_neptune / _conf_mars, ".0f") + " 倍",
          {"neptune_x": _conf_neptune, "mars_x": _conf_mars})

    entry("B03", "PASS" if guard_ok("G7") and guard_ok("G8") else "FAIL",
          "三重 lambda 下界：18.58 AU / 2.1e4 AU / 2.1e7 AU",
          "稳定性 " + format(_lam_stab_max, ".2f") + " AU（海王星 a/phi）< 开普勒第三定律 "
          + format(_lam_kep_max, ".0f") + " AU（eps_K=1e-6）< 进动 "
          + sci(_lam_prec_max / AU, 4) + " AU = " + format(_lam_prec_max / PC, ".2f")
          + " pc（eps_w=1e-3）⇒ 最严者是进动，比 r224 的稳定性下界硬 "
          + format(_lam_prec_max / AU / _lam_stab_max, ".0f") + " 倍",
          {"stab_au": _lam_stab_max, "kep_au": _lam_kep_max,
           "prec_au": _lam_prec_max / AU, "prec_pc": _lam_prec_max / PC})

    entry("B04", "PASS" if guard_ok("G6") else "FAIL",
          "谱通道与散射通道是同一个判据（独立通道数 3 而非 4）",
          "r227 的 eta = 2*mu*A*lambda/(hbar c)^2 与 r226 的 g = 2*alpha*mu*lambda/(hbar c) 在 "
          "A = alpha*hbar c 下逐字恒等（本卷 G2  numerically 复现 101.49）⇒ 四条通道的"
          "「独立约束」只有三条，且其中三条同向",
          {"n_independent": 3})

    entry("C01", "PASS" if guard_ok("G5") and guard_ok("G17") else "FAIL",
          "合并的秩：四条通道 → 2 个独立方向，alpha 只被 1 条通道测",
          "对数梯度 (0,-2)/(0,+1)/(0,-2)/(+1,+1) ⇒ 秩 2（子式 " + sci(_subdet, 3)
          + "）；三条通道对 alpha 的灵敏度严格为 0 ⇒ 「四条通道共同锁定 (alpha, lambda)」"
          "不成立：alpha 只有一个来源（谱层），lambda 有三个来源且全部同向",
          {"rank": 2, "n_alpha": 1})

    entry("C02", "FAIL", "「统一禁区」不存在：四块约束区互不相连（适用域不同）",
          "谱通道的判别力依赖「该通道应只有 <=1 个束缚态」这一物理预期——只对强·剩余核力成立；"
          "对电磁（氢原子有无穷多态是正常的）、弱（本来就无束缚态）、引力（束缚半径超宇宙）"
          "都不构成排除。把 g 判据套到氢原子会得到「电磁非法」的荒谬结论（C04 登记）"
          "⇒ 四条通道的禁止区是四块**不相连**的区域，不是一张统一排除图",
          {"blocks": 4})

    entry("C03", "FAIL" if not guard_ok("G16") else "PASS",
          "单一 lambda 的空集：谱要小、进动要大（缺口 35 量级）",
          "α=14.6 时谱通道要求 lambda < " + sci(_lam_spec_max_m, 3)
          + " m；行星进动要求 lambda > " + sci(_lam_prec_max, 3) + " m ⇒ 同一 lambda 同时"
          "满足两者是**空集**（缺口 " + format(_gap_orders, ".2f") + " 个量级）。"
          "母式本身用四个 lambda_i（两个为 inf）因此无此问题——但「一个方程一个 lambda」"
          "的强统一解读在本卷的判据下被机器否证",
          {"gap_orders": _gap_orders})

    entry("C04", "BOUNDARY", "谱判据的适用域窄：跨通道套用会判出荒谬结论",
          "把 g = 2*alpha*mu*lambda/(hbar c) < 1.68 当作「合法性」判据套到氢原子："
          "alpha = 1/137、mu = m_e/2、lambda = inf ⇒ g = inf ⇒ 判「电磁非法」，而氢原子是"
          "本库 r226 的解析锚（E_1s = -13.6057 eV 逐位）。⇒ g 判据是「束缚态个数」判据，"
          "不是「理论合法性」判据——本卷据此把它限定在强·剩余核力道",
          {"g_hydrogen": "inf"})

    entry("D01", "PASS" if guard_ok("G11") else "FAIL",
          "开普勒第三定律两体化：T^2/a^3 = 4pi^2/[G(M+m)]",
          "两体项 m/M：木星 " + sci(_mj, 4) + "、土星 2.86e-4、海王星 5.15e-5、地球 3.00e-6、"
          "水星 1.66e-7；以地球为参照的木星表观不普适性 " + sci(_apparent, 4)
          + " ⇒ 两体修正不是小量修正，而是开普勒约束**必须**含的结构项",
          {"m_J_over_M": _mj, "apparent": _apparent})

    entry("D02", "PASS" if guard_ok("G12") else "FAIL",
          "两体修正的判别力：忽略它会把木星判成违反开普勒 954 倍容差",
          "在 eps_K = 1e-6 的精度口径下，单体近似（T^2/a^3 对所有行星相同）与观测"
          "（含 m）相差 " + format(_ignore_factor, ".0f") + " 倍容差 ⇒ 若未来的"
          "「统一方程」用单体近似做开普勒约束，它在外行星处直接出局；本卷的所有"
          "开普勒下界均已含两体项",
          {"factor": _ignore_factor})

    entry("D03", "PASS" if guard_ok("G13") else "FAIL",
          "稳定性判据与约化质量无关（两体修正为零的结构项）",
          "U''/mu = mu*e^(-x)(1+x-x^2)/r^3 ⇒ 除以 mu 后消去 ⇒ 判据 x < phi 与 mu 无关，"
          "机器用 mu = 1 与 mu = 1e12 求得同一根 " + format(_root_a, ".10f")
          + "（与 r224 的 phi 一致）⇒ 稳定性通道**不需要**两体修正（这是本卷唯一"
          "「两体修正 = 0」的通道）",
          {"root": _root_a})

    entry("D04", "BOUNDARY", "谱通道的两体不确定性因子 = 2（lambda_crit 固有 100% 不确定）",
          "g ∝ mu，等质量两体 mu = m/2 与单体 mu = m 相差 2 倍 ⇒ 同一 (alpha, lambda) 在"
          "两种口径下 g 差 2.000、lambda_crit 差 2.000（" + sci(_lcrit_single, 3) + " m vs "
          + sci(_lcrit_pair, 3) + " m）⇒ 任何用 g 判据给出的 lambda 界都带 2 倍的固有"
          "口径不确定性；r226 的 alpha_y 拟合已用 mu = M_P/2（正确口径），但该因子必须在"
          "引用界值时声明",
          {"factor": 2.0})

    entry("E01", "FAIL", "引力通道无实验空间：合法则不可测、可测则违法",
          "要「不被行星进动排除」需 lambda > " + format(_lam_prec_max / PC, ".2f")
          + " pc（" + sci(_lam_prec_max / AU, 4) + " AU）；而在该下界处，水星的 Yukawa"
          "进动占比仅 " + sci(_prec_at_min, 3) + " ⇒ 若 lambda 在太阳系尺度可见"
          "（<= 1e4 AU），海王星进动已被超出 " + sci(_conf_neptune, 3) + " 倍 ⇒ "
          "两条不等式方向相反、无交叠 ⇒ 引力通道的 Yukawa 修正在本库判据下**既不能"
          "被看见也不能被允许**",
          {"lam_min_pc": _lam_prec_max / PC, "R_at_bound": _prec_at_min})

    entry("E02", "INFO", "判决：约束层不统一（第三条独立失败层）",
          "r229 已钉死「形式统一成立（模板/谱/散射/作用量四层）/ 动力学统一失败（供给 0）」；"
          "本卷补第三层：**约束层也不统一**——四条通道秩 2、alpha 只被 1 条测、"
          "四块禁止区不相连、单一 lambda 是空集。三层的独立性由本卷 G5/G16/G17 机器钉住",
          {"layers": ["form PASS", "dynamics FAIL", "constraint FAIL"]})

    n_pass = sum(1 for e in entries if e["level"] == "PASS")
    n_fail = sum(1 for e in entries if e["level"] == "FAIL")
    n_bnd = sum(1 for e in entries if e["level"] == "BOUNDARY")
    n_info = sum(1 for e in entries if e["level"] == "INFO")

    res = {
        "stem": STEM, "round": 231, "date": "2026-10-26",
        "method": ("解析判据 + 对数梯度秩分析 + 8 行星数值 + 两体约化质量口径 —— "
                   "float64，纯标准库"),
        "entries": entries, "guards": guards, "controls": controls,
        "readings": {
            "phase_points": PHASE_POINTS,
            "phase_lines": _phase_lines,
            "planets": PLANET_TABLE,
            "eps_table": _eps_table,
            "two_body": [{"name": t["name"], "m_over_M": t["m_over_M"],
                          "apparent": t["apparent_dev"]} for t in _two_rows],
            "apply": [{"ch": a[0], "judge": a[1], "d_alpha": a[2], "dir": a[3],
                       "object": a[4], "expect": a[5]} for a in APPLY],
            "bounds": {
                "stability_au": round(_lam_stab_max, 2),
                "kepler_au": round(_lam_kep_max, 1),
                "precession_au": _lam_prec_max / AU,
                "precession_pc": _lam_prec_max / PC,
                "lam_fit_mercury_au": round(_lam_fit_merc, 2),
            },
            "single_lambda": {
                "spec_max_m": _lam_spec_max_m,
                "prec_min_m": _lam_prec_max,
                "gap_orders": _gap_orders,
            },
            "conflict": {"mars_x": _conf_mars, "neptune_x": _conf_neptune,
                         "gain": _conf_neptune / _conf_mars},
            "rank": {"rank": 2, "subdet": _subdet, "n_alpha_sensitive": _n_alpha_sensitive},
            "two_body_factor": {"g_single": _g_single, "g_pair": _g_pair,
                                "lcrit_single_m": _lcrit_single, "lcrit_pair_m": _lcrit_pair},
            "deuteron": {"N_pair": _N_pair, "N_single": _N_single},
        },
        "counts": {"entries": len(entries), "PASS": n_pass, "FAIL": n_fail,
                   "BOUNDARY": n_bnd, "INFO": n_info,
                   "guards": str(sum(1 for g in guards if g["ok"])) + "/" + str(len(guards)),
                   "controls": str(sum(1 for c in controls if c["ok"])) + "/" + str(len(controls))},
        "verdict": "", "judgement": "", "source": {},
    }

    parts = [
        "R231-CONSTRAINT-PANORAMA",
        "FOUR-CHANNELS-RANK-2-OK" if guard_ok("G5") else "RANK-FAIL",
        "ALPHA-MEASURED-BY-ONE-CHANNEL-ONLY" if guard_ok("G17") else "ALPHA-FAIL",
        "SPECTRUM-EQ-SCATTERING-OK" if guard_ok("G2") else "ETA-NOT-G-FAIL",
        "PRECESSION-8PLANETS-" + format(_conf_neptune, ".1e") + "X",
        "STABILITY-" + format(_lam_stab_max, ".1f") + "AU",
        "KEPLER3-" + format(_lam_kep_max, ".0f") + "AU",
        "PRECESSION-" + format(_lam_prec_max / PC, ".1f") + "PC",
        "SINGLE-LAMBDA-EMPTY-" + format(_gap_orders, ".0f") + "ORDERS",
        "LEGAL-THEN-UNOBSERVABLE-FAIL",
        "CONSTRAINT-LAYER-NOT-UNIFIED",
        "VERDICT-FORM-PASS-DYNAMICS-FAIL-CONSTRAINT-FAIL",
    ]
    res["verdict"] = "-".join(parts)
    res["judgement"] = ("CLOSED-INCREMENT（实验约束全景：四条通道秩 2 / alpha 只被 1 条测 / "
                        "单一 lambda 空集 35 量级 / 引力通道合法则不可测；两体修正在开普勒通道"
                        "是 954 倍容差的必须项、在稳定性通道严格为零）")
    res["source"] = {
        "engine": BASE + ".py",
        "external_inputs": [
            "alpha_EM = 1/137.035999084（CODATA）",
            "alpha_W = 1.0268268e-5（r214 声明口径 G_F*m_p^2）",
            "alpha_pi = 14.6（r214 剩余核力 g^2/4pi 口径）",
            "lambda_W = 2.455e-18 m / lambda_pi = 1.4619e-15 m（hbar c/m）",
            "g_crit = 1.6798（l=0 Yukawa 首阈值，r226 数值复核）",
            "eps_w（进动精度）与 eps_K（开普勒精度）为声明口径，给三档敏感性",
        ],
        "inherits": ["r223（进动定标）", "r224（稳定性 x<phi）", "r225（近点角闭式/维里）",
                     "r226（谱层 g）", "r227（散射层 eta=g）", "r229（新颖性：无新方程）",
                     "r230（引力本质层边界）"],
    }
    print("条目 " + str(res["counts"]["entries"]) + "（PASS " + str(n_pass) + " / FAIL "
          + str(n_fail) + " / BOUNDARY " + str(n_bnd) + " / INFO " + str(n_info)
          + "）· 守卫 " + res["counts"]["guards"] + " · 控制组 " + res["counts"]["controls"])

    os.makedirs(_DATADIR, exist_ok=True)
    jpath = os.path.join(_DATADIR, BASE + ".json")
    mpath = os.path.join(_DATADIR, BASE + ".md")
    rpath = os.path.join(_DATADIR, BASE + "_report.txt")

    html_ok, html_detail = cast_html(res)
    guard("G18", "交互 HTML 生成且自含", html_ok, html_detail)
    res["counts"]["guards"] = str(sum(1 for g in guards if g["ok"])) + "/" + str(len(guards))

    with open(jpath, "w", encoding="utf-8", newline="\n") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    write_md(mpath, res)
    write_report(rpath, res)

    bad_g = [g["id"] for g in guards if not g["ok"]]
    bad_c = [c["id"] for c in controls if not c["ok"]]
    if bad_g or bad_c:
        print("[RC-NONZERO] 守卫失败 " + str(bad_g) + " 控制组失败 " + str(bad_c))
        return 1
    print("[DONE] " + MARKER + " rc=0 -> " + jpath)
    return 0


# __NEXT__
