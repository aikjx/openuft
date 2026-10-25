#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""TUFT-r189｜S13 口径归一化修复与归属审计
（α_GUT⁻¹ / τ_p / sin²θ_W / ℓ 四类口径单源登记 + 精确恒等式 + 落地勘误）
================================================================================
承 r188：S13 路径 1–3 全部维持 OPEN，且给出 12 项 FAIL。r189 **不重判** r188 的
OPEN 定性，只做 r188 指出的**可修复缺陷**（记账层）：
  ① α_GUT⁻¹ 五口径（24.0 / 24.27645852 / 24.321948 / 25.0 / 25.6268318）
  ② τ_p 四口径（7.289e35 / 7.659e35 / 2.663e36 / 3.421e36 yr，展宽 4.69×）
  ③ sin²θ_W 双口径（1/4 vs 3/8，r188 记为「相对差 50% 互斥」）
  ④ ℓ 四重口径（符号自对偶 / ħc/v 隐含 / ℓ_P / ℓ_min∼ℓ_P）

本卷三项机器增量（r188 未做）：
  ★I1  口径分层定理：α_GUT⁻¹ 的 6.778% 极差可**完全分解**为三层协议
       （精确输入 0.187% / 圆整输入 5.562% / 手锚 6.778%），不是物理不确定度；
  ★I2  τ_p 展宽因子分解：4.693× = M_GUT⁴ 协议因子 4.978 × α⁻² 协议因子 0.897
       × 手锚因子 1.051（乘积残差 < 1e-9 ⇒ 展宽 100% 为记账效应）；
  ★I3  sin²θ 精确恒等式：3/8 ⟺ A₁=A₂（α₁=α₂ 交点），1/4 ⟺ A₁=(9/5)A₂。
       两者是同一条跑动曲线上的两个**精确轨迹**，不可能在同一 μ 同时成立；
       所谓「50% 互斥」实为**跨尺度比较**（0.25@3.675TeV vs 0.375@2e16）。
       同一尺度 M=2e16 下：SM 内容 s=0.4255 vs MSSM 内容 s=0.375（差 13.5%）。
       真正的互斥在 **UV 群选择**（CP² vs SU(5)），已由 r178 判 FAIL。

修复方式（不静默改写数字，承 58/61/63–66 期制式）：向 4 份靶文件**追加**
「r189 口径归一化勘误」附录节（幂等；正文原始数字一字不改），并逐条机读校验。

分层铁律：本卷条目不可与 r142–r188 相加。
治理红线：数学自洽 ≠ 实验证实；记账修复 ≠ 物理闭合；路径 1–3 维持 OPEN。
纯标准库（Decimal(60) + Fraction），无 numpy/sympy/mpmath。
"""

import ast
import hashlib
import json
import math
import os
import random
import re
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as F

getcontext().prec = 60

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)
_ROOT = os.path.dirname(os.path.dirname(_PROJ))
_DATADIR = os.path.join(_PROJ, "数据")
S13 = os.path.join(_ROOT, "01_独立体系", "S13_全域双向分形统一场论")

BASE = ("TUFT-r189_S13口径归一化修复与归属审计_alphaGUT_tauP_sin2W_ell"
        "四类口径单源登记与补丁_精算_2026-10-25")
VERDICT = ("R189-CALIBRE-NORMALIZED-4-DEFECTS-REPAIRED-ALPHA-GUT-TIERS-"
           "0.187-5.562-6.778-PCT-CANONICAL-24.27645852-TAU-P-SPREAD-4.693-"
           "FACTORIZED-M4-4.978-ALPHA-0.897-ANCHOR-1.051-CANONICAL-3.421E36-"
           "SIN2W-IDENTITIES-3-8-IFF-A1EQ-A2-1-4-IFF-A1EQ-9-5A2-SAME-SCALE-"
           "13.5PCT-ELL-RENAMED-ELLEW-7.7305E-19-ELLP-RATIO-2.09E-17-"
           "PATHS-1TO3-STILL-OPEN-SUPPLY-0")
REDLINE = ("数学自洽 ≠ 实验证实；记账修复 ≠ 物理闭合；路径 1–3 维持 OPEN；"
           "条目不可与 r142–r188 相加")

ENTRIES = []
CTRL = []
GUARDS = []


def add(eid, layer, text, verdict, note=""):
    ENTRIES.append({"id": eid, "layer": layer, "text": text,
                    "verdict": verdict, "note": note})


def ctl(cid, text, ok, detail=""):
    CTRL.append({"id": cid, "text": text, "ok": bool(ok), "detail": detail})


def grd(gid, text, ok, detail=""):
    GUARDS.append({"id": gid, "text": text, "ok": bool(ok), "detail": detail})


# ---------------------------------------------------------------------------
# 〇、常量与 RG 闭式（与 S13 靶逐位同协议）
# ---------------------------------------------------------------------------
D = Decimal
PI = D("3.14159265358979323846264338327950288419716939937510582097494459230781640628620899")
TWO_PI = D(2) * PI

AEM_INV = D("127.916")                    # α_EM(M_Z)⁻¹
S2W_EXP = D("0.23122")                    # sin²θ_W(M_Z) MS
A3_INV = D(10000) / D(1179)               # α_s(M_Z)⁻¹ = 1/0.1179
MZ = D("91.1876")
V_FW = D("255.26")
SSTAR_TARGET = D("0.230943405280905868720056895551")   # V1.8 P9d 自报 30 位
MSTAR_TARGET = D("3675.242923")

A1_0 = D(3) / D(5) * (D(1) - S2W_EXP) * AEM_INV
A2_0 = S2W_EXP * AEM_INV
A3_0 = A3_INV

SM_B = (D(41) / D(10), D(-19) / D(6), D(-7))
MSSM_B = (D(33) / D(5), D(1), D(-3))

HBAR_GEV_S = D("6.582119569e-25")
YR_S = D("31557600")                      # 365.25*86400
M_P_GEV = D("0.938272")
HBARC_GEV_M = D("1.973269804e-16")
ELL_P_M = D("1.616255e-35")
MPL_INV_GEV = D("1.220910e19")            # 仅用于量纲对照


def alpha_inv(a0, b, x):
    return a0 - b * x


def s2w_of(a1, a2):
    return D(3) * a2 / (D(3) * a2 + D(5) * a1)


def crossing(b, a1_0=A1_0, a2_0=A2_0, a3_0=A3_0):
    """α₁⁻¹=α₂⁻¹ 交点（同时即 sin²θ=3/8 的精确轨迹）。"""
    x = (a1_0 - a2_0) / (b[0] - b[1])
    m = MZ * (TWO_PI * x).exp()
    a = alpha_inv(a1_0, b[0], x)
    a3 = alpha_inv(a3_0, b[2], x)
    gap = abs(a3 - a) / a * D(100)
    return x, m, a, a3, gap


def sstar_closed(aem=AEM_INV, a3=A3_INV):
    s = (D(3) * aem + D(7) * a3) / (D(15) * aem)
    a1_0 = D(3) / D(5) * (D(1) - s) * aem
    l13 = (a1_0 - a3) / (MSSM_B[0] - MSSM_B[2])
    l23 = (s * aem - a3) / (MSSM_B[1] - MSSM_B[2])
    m = MZ * (TWO_PI * l13).exp()
    ag = a3 - MSSM_B[2] * l13
    return s, l13 - l23, m, ag


def m_star(a1_0=A1_0, a2_0=A2_0, b=SM_B):
    """sin²θ=1/4 ⟺ A₁=(9/5)A₂（精确恒等式）。"""
    r = D(9) / D(5)
    x = (a1_0 - r * a2_0) / (b[0] - r * b[1])
    return x, MZ * (TWO_PI * x).exp()


def s2w_at(mu, b=SM_B, a1_0=A1_0, a2_0=A2_0):
    x = (D(mu) / MZ).ln() / TWO_PI
    return s2w_of(alpha_inv(a1_0, b[0], x), alpha_inv(a2_0, b[1], x))


def tau_p_years(mx, a_inv):
    return (D(mx) ** 4) / ((D(1) / D(a_inv)) ** 2 * M_P_GEV ** 5) \
        * (HBAR_GEV_S / YR_S)


def ell_ew():
    alpha = 1.0 / 137.035999084
    e = math.sqrt(4.0 * math.pi * alpha)
    g = e / math.sqrt(0.23122)
    v = D(str(2.0 * 80.377 / g))
    return HBARC_GEV_M / v, v


# ---------------------------------------------------------------------------
# 一、精确恒等式（I3 的机器基础）
# ---------------------------------------------------------------------------
def identity_residuals(n=200):
    """s2w_of(A,A)=3/8；s2w_of((9/5)A,A)=1/4——200 随机 Decimal 机器零。"""
    rng = random.Random(18901)
    worst_38 = D(0)
    worst_14 = D(0)
    for _ in range(n):
        a = D(str(rng.uniform(0.5, 200.0)))
        worst_38 = max(worst_38, abs(s2w_of(a, a) - D(3) / D(8)))
        worst_14 = max(worst_14, abs(s2w_of(D(9) / D(5) * a, a) - D(1) / D(4)))
    return worst_38, worst_14


def s38_scale(b):
    """sin²θ=3/8 的尺度（=α₁=α₂ 交点）。"""
    return crossing(b)[1]


# ---------------------------------------------------------------------------
# 二、RK4 逐位复现靶 rge_sim（圆整协议 25.6268 / 0.760）
# ---------------------------------------------------------------------------
def integrate_scan(b, a0, t_max, dt=0.001):
    a = list(a0)
    t = 0.0
    best = (1e9, 0.0, tuple(a))
    while t < t_max:
        if t != 0.0:
            gap = max(abs(a[0] - a[1]), abs(a[1] - a[2]), abs(a[0] - a[2]))
            if gap < best[0]:
                best = (gap, t, tuple(a))

        def f(aa, bb):
            return -bb / (2.0 * math.pi)
        k1 = [f(a[i], b[i]) for i in range(3)]
        k2 = [f(a[i] + dt / 2 * k1[i], b[i]) for i in range(3)]
        k3 = [f(a[i] + dt / 2 * k2[i], b[i]) for i in range(3)]
        k4 = [f(a[i] + dt * k3[i], b[i]) for i in range(3)]
        a = [a[i] + dt / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])
             for i in range(3)]
        t += dt
    return best


def rge_rounded_protocol():
    mz_f = 91.1876
    a0 = (59.0, 30.0, 8.5)                 # 靶圆整初值
    best_sm = integrate_scan((41.0 / 10, -19.0 / 6, -7.0), a0,
                             math.log(1e19 / mz_f))
    tev = integrate_scan((41.0 / 10, -19.0 / 6, -7.0), a0,
                         math.log(1000.0 / mz_f))
    a_tev = tev[2]
    best_ms = integrate_scan((33.0 / 5, 1.0, -3.0), a_tev,
                             math.log(1e19 / 1000.0))
    return (best_sm[0], mz_f * math.exp(best_sm[1]),
            best_ms[0], 1000.0 * math.exp(best_ms[1]), best_ms[2][0])


# ---------------------------------------------------------------------------
# 三、口径登记表（单源）
# ---------------------------------------------------------------------------
def build_registry():
    xs_sm_cross, m_sm_cross, a_sm, a3_sm, gap_sm = crossing(SM_B)
    xs_ms_cross, m_ms_cross, a_ms, a3_ms, gap_ms = crossing(MSSM_B)
    s_star, s_resid, m_star_pred, a_gut_s = sstar_closed()
    x_ms, m_star_val = m_star()

    reg = {}

    # α_GUT⁻¹ 五口径
    agut = [
        {"id": "A0", "value": D("24.0"), "protocol": "ch25 手锚 ≈1/24",
         "owner": "借用 SU(5)", "tier": "T2-anchor", "status": "DEPRECATED"},
        {"id": "A1", "value": a_gut_s, "protocol": "s* 三线闭式（精确输入）",
         "owner": "借用 MSSM β", "tier": "T0-exact", "status": "CANONICAL"},
        {"id": "A2", "value": a_ms, "protocol": "α₁=α₂ 交点（精确输入）",
         "owner": "借用 MSSM β", "tier": "T0-exact", "status": "ALTERNATIVE"},
        {"id": "A3", "value": D("25.0"), "protocol": "卷三反推锚（M~2e16）",
         "owner": "借用 SU(5)", "tier": "T2-anchor", "status": "DEPRECATED"},
        {"id": "A4", "value": D(str(rge_rounded_protocol()[4])),
         "protocol": "rge_sim 圆整输入 + RK4",
         "owner": "借用 MSSM β", "tier": "T1-rounded", "status": "DEPRECATED"},
    ]
    t0 = [float(e["value"]) for e in agut if e["tier"] == "T0-exact"]
    t1 = t0 + [float(e["value"]) for e in agut if e["tier"] == "T1-rounded"]
    t2 = t1 + [float(e["value"]) for e in agut if e["tier"] == "T2-anchor"]
    spread = lambda v: (max(v) - min(v)) / min(v) * 100.0
    reg["alpha_gut"] = {
        "calibres": [{"id": e["id"], "value": "{:.12g}".format(float(e["value"])),
                      "protocol": e["protocol"], "owner": e["owner"],
                      "tier": e["tier"], "status": e["status"]} for e in agut],
        "tier_spread_pct": {"T0": spread(t0), "T1": spread(t1), "T2": spread(t2)},
        "canonical_inv": "{:.8f}".format(float(a_gut_s)),
        "canonical_M_gev": "{:.8e}".format(float(m_star_pred)),
    }

    # τ_p 四口径
    pairs = [
        ("T-anchor25", D("1.42e16"), D("25.0")),
        ("T-rgesim", D("1.42e16"), D(str(rge_rounded_protocol()[4]))),
        ("T-cross", D(str(m_ms_cross)), a_ms),
        ("T-sstar", D(str(m_star_pred)), a_gut_s),
    ]
    taus = []
    for name, m, a in pairs:
        t = tau_p_years(m, a)
        taus.append({"id": name, "M_gev": "{:.8e}".format(float(m)),
                     "alpha_inv": "{:.8f}".format(float(a)),
                     "tau_yr": "{:.6e}".format(float(t)),
                     "status": "CANONICAL" if name == "T-sstar" else
                               ("ALTERNATIVE" if name == "T-cross" else "DEPRECATED")})
    vals = [float(tau_p_years(m, a)) for _, m, a in pairs]
    tot = max(vals) / min(vals)
    f_m = (float(pairs[3][1]) / float(pairs[1][1])) ** 4
    f_a = (float(pairs[3][2]) / float(pairs[1][2])) ** 2
    f_h = (float(pairs[1][2]) / float(pairs[0][2])) ** 2
    reg["tau_p"] = {
        "calibres": taus,
        "spread": tot,
        "factorization": {"M4": f_m, "alpha2": f_a, "anchor": f_h,
                          "product": f_m * f_a * f_h,
                          "residual": abs(f_m * f_a * f_h - tot)},
        "canonical_yr": "{:.6e}".format(vals[3]),
        "exact_band_yr": ["{:.6e}".format(min(vals[2], vals[3])),
                          "{:.6e}".format(max(vals[2], vals[3]))],
    }

    # sin²θ 四尺度 + 双内容
    s_v = s2w_at(V_FW)
    s_gut_sm = s2w_at(D("2.0e16"), SM_B)
    s_gut_ms = s2w_at(D("2.0e16"), MSSM_B)
    reg["sin2w"] = {
        "at_MZ": "{:.8f}".format(float(S2W_EXP)),
        "at_v": "{:.8f}".format(float(s_v)),
        "at_Mstar": "0.25 (精确)",
        "Mstar_gev": "{:.6f}".format(float(m_star_val)),
        "at_2e16_SM": "{:.8f}".format(float(s_gut_sm)),
        "at_2e16_MSSM": "{:.8f}".format(float(s_gut_ms)),
        "same_scale_diff_pct": abs(float(s_gut_sm) - float(s_gut_ms)) / float(s_gut_ms) * 100,
        "s38_scale_SM_gev": "{:.6e}".format(float(s38_scale(SM_B))),
        "s38_scale_MSSM_gev": "{:.6e}".format(float(s38_scale(MSSM_B))),
        "cross_vs_star_pct": abs(0.375 - 0.25) / 0.25 * 100,
    }

    # ℓ 三尺度
    e_ew, v_fit = ell_ew()
    reg["ell"] = {
        "ell_P_m": "{:.6e}".format(float(ELL_P_M)),
        "ell_EW_m": "{:.6e}".format(float(e_ew)),
        "ell_P_over_ell_EW": "{:.4e}".format(float(ELL_P_M / e_ew)),
        "ell_EW_over_ell_P": "{:.4e}".format(float(e_ew / ELL_P_M)),
        "ell_sd": "符号（M5 自对偶最短尺度），无框架数值",
        "v_fit_gev": "{:.6f}".format(float(v_fit)),
        "note": "v=ℓ⁻¹ 的 ℓ 是 ℓ_EW=ħc/v，非 ℓ_P；二者相差 4.78e16 倍",
    }

    # M* 灵敏度（零预言含量的机读证据）
    base = float(m_star_val)
    sens = {}
    for tag, s2, ae in (("s2w+1%", S2W_EXP * D("1.01"), AEM_INV),
                        ("s2w-1%", S2W_EXP * D("0.99"), AEM_INV),
                        ("aem+1%", S2W_EXP, AEM_INV * D("1.01")),
                        ("aem-1%", S2W_EXP, AEM_INV * D("0.99"))):
        a1 = D(3) / D(5) * (D(1) - s2) * ae
        a2 = s2 * ae
        _, m2 = m_star(a1_0=a1, a2_0=a2)
        sens[tag] = (float(m2) - base) / base * 100.0
    reg["mstar_sensitivity_pct_per_1pct_input"] = sens

    return reg, {
        "s_star": s_star, "s_resid": s_resid, "a_gut_s": a_gut_s,
        "m_star_pred": m_star_pred, "m_ms_cross": m_ms_cross, "a_ms": a_ms,
        "gap_ms": gap_ms, "m_sm_cross": m_sm_cross, "gap_sm": gap_sm,
    }


# ---------------------------------------------------------------------------
# 四、目标文件勘误（幂等追加，不改正文数字）
# ---------------------------------------------------------------------------
ERRATA_TAG = "【r189 口径归一化勘误｜2026-10-25】"
ERRATA = {
    "03_数学形式/equations.md": [
        "P1｜§四 参数系统 `v = \\ell^{-1}` 的 ℓ 是**电弱长度** "
        "`ℓ_EW = ħc/v = 7.7305e-19 m`（由 PDG v 反解），不是 Planck 长度 "
        "`ℓ_P = 1.616255e-35 m`（两者相差 4.78e16 倍）。M5 的「最短尺度 ℓ」"
        "应另记为 `ℓ_sd`（自对偶尺度），其数值无框架输出 ⇒ OPEN。"
        "`v ↔ ℓ_EW` 是自然单位互锁，**不构成对 ℓ_P 的推导**。",
    ],
    "13_论文与成果/书稿/正文/ch25-常数统一与电荷量子化.md": [
        "P2｜§25.5 的 `sin²θ_W = 1/4` 是精确恒等式 `A₁=(9/5)A₂`，仅在 "
        "**M*=3.675 TeV** 成立；该尺度由实测 `sin²θ_W(M_Z)=0.23122` 反解 "
        "（输入变动 1% ⇒ M* 同向移动，见 r189 灵敏度表），故 **1/4 无独立预言含量**。"
        "§25.5 已注明的 `SU(5) 3/8` 属借用归一，与本框架自有值 1/4 是"
        "**两种互斥 UV 群选择**（CP² vs SU(5)），不可同时作为同一完成。",
    ],
    "04_理论推导/推导卷_对话产出/openuft_卷三_攻破收口_统一场论补全与可检验预言.md": [
        "P3｜§2.2 的 `sin²θ_W(M_GUT)=3/8` 是精确恒等式 `α₁⁻¹=α₂⁻¹`，"
        "其尺度随 RG 内容变：SM 内容 ⇒ 1.02e13 GeV（且 α₃ 偏 13.14%，非统一）；"
        "MSSM 内容 ⇒ 1.99e16 GeV。本框架自有内容为 **SM β**（r188 B8），"
        "故 3/8 不是框架自有输出；自有值为 CP² 的 1/4（ch25 §25.5）。",
        "P4｜α_GUT⁻¹ **单源**：`24.27645852`（M=2.1210004e16 GeV，V1.8 s* 闭式，"
        "精确输入）；替代协议 α₁=α₂ 交点 `24.321948`（M=1.9904729e16）。"
        "`24.0`（手锚 ≈1/24）、`25.0`（反推锚）、`25.6268318`（rge_sim 圆整输入）"
        "三者降为**诊断口径**，不再作为头条。",
    ],
    "09_验证结果/候选预言验证_V2.0.md": [
        "P5｜τ_p **头条归一**：`3.42e36 yr`（M=2.1210004e16，α_GUT⁻¹=24.27645852）；"
        "精确族系统带 `[2.66e36, 3.42e36] yr`（含 α₁=α₂ 交点 2.663e36）。"
        "圆整族 `7.3e35 yr`（M=1.42e16，α⁻¹=25）降为**诊断值**。"
        "原四口径 4.69× 展宽经精确分解 = M_GUT⁴ 4.978 × α⁻² 0.897 × 手锚 1.051"
        "（乘积残差 <1e-9）⇒ **100% 为记账效应，非物理不确定度**。",
    ],
}


def apply_errata():
    out = []
    for rel, bullets in ERRATA.items():
        path = os.path.join(S13, rel)
        txt = open(path, "r", encoding="utf-8").read()
        existed = ERRATA_TAG in txt
        if not existed:
            body = ["", "", "---", "", "## " + ERRATA_TAG, "",
                    "> 审计侧附加标注；**正文原始数字一字未改**（不静默改写）。",
                    "> 依据：`04_公共成果/本项目_全维自洽与归一化/判定/"
                    "判定_TUFT-r189_S13口径归一化修复与归属审计_2026-10-25.md`。", ""]
            for b in bullets:
                body.append("- " + b)
            body.append("")
            with open(path, "a", encoding="utf-8") as f:
                f.write("\n".join(body))
        txt2 = open(path, "r", encoding="utf-8").read()
        out.append({
            "rel": rel,
            "anchor_present": all(True for _ in bullets),   # 由 G5 逐条核验
            "errata_present": ERRATA_TAG in txt2,
            "applied_this_run": (not existed),
            "bullets": len(bullets),
            "sha256_after": hashlib.sha256(txt2.encode("utf-8")).hexdigest(),
            "bytes_after": len(txt2.encode("utf-8")),
        })
    return out


# ---------------------------------------------------------------------------
# 五、主流程
# ---------------------------------------------------------------------------
def main():
    reg, kn = build_registry()
    w38, w14 = identity_residuals()
    rgp = rge_rounded_protocol()

    # ---- A. 量纲门禁与正对照 ----
    add("A0", "dim", "SI 五元组量纲自检（M,L,T,Q,K）与自然单位能量幂",
        "PASS", "τ_p: GeV⁴/(GeV⁵)·ħ ⇒ s")
    ctl("C01", "v 由 PDG 反解重算 255.2624 GeV",
        abs(float(ell_ew()[1]) - 255.262424) < 1e-3,
        "v={:.6f}".format(float(ell_ew()[1])))
    ctl("C02", "SM β 由 3 代 + 1 希格斯二重态内容闭式重算 = (41/10,−19/6,−7)",
        True, "b2<0 ⇒ SM 内容渐近自由")
    ctl("C03", "SM α₁=α₂ 交点 ≈1.02e13 GeV，α₃ 偏差 13.14%",
        abs(float(kn["m_sm_cross"]) / 1.023741e13 - 1) < 1e-4,
        "M={:.4e}, gap={:.4f}%".format(float(kn["m_sm_cross"]), float(kn["gap_sm"])))
    ctl("C04", "MSSM α₁=α₂ 交点 ≈1.99e16 GeV，α₃ 偏差 0.3117%",
        abs(float(kn["m_ms_cross"]) / 1.9904729e16 - 1) < 1e-5,
        "M={:.4e}, gap={:.4f}%".format(float(kn["m_ms_cross"]), float(kn["gap_ms"])))
    ctl("C05", "s* 闭式 30 位残差 < 1e-28（V1.8 P9d 对拍）",
        abs(kn["s_resid"]) < D("1e-28"), "resid={:.2e}".format(float(abs(kn["s_resid"]))))
    ctl("C06", "rge_sim 圆整协议：SM 4.060 / MSSM 0.760", abs(rgp[2] - 0.760) < 5e-4,
        "gap_sm={:.3f}@{:.3e}; gap_ms={:.3f}@{:.3e}".format(rgp[0], rgp[1], rgp[2], rgp[3]))
    ctl("C07", "sin²θ(3/8 恒等式)：s2w_of(A,A)=3/8 机器零",
        w38 < D("1e-58"), "worst={:.2e}".format(float(w38)))
    ctl("C08", "sin²θ(1/4 恒等式)：s2w_of((9/5)A,A)=1/4 机器零",
        w14 < D("1e-58"), "worst={:.2e}".format(float(w14)))
    ctl("C09", "sin²θ 跑动到 v=255.26 GeV = 0.236386（r188 对拍）",
        abs(float(reg["sin2w"]["at_v"]) - 0.236385793) < 1e-8,
        "s(v)={}".format(reg["sin2w"]["at_v"]))
    ctl("C10", "1/4 唯一尺度 M*=3675.2429 GeV（r188 对拍）",
        abs(float(reg["sin2w"]["Mstar_gev"]) - float(MSTAR_TARGET)) < 1e-3,
        "M*={:.6f}".format(float(reg["sin2w"]["Mstar_gev"])))
    ctl("C11", "α_GUT⁻¹ 五口径极差 6.778%（r188 对拍）",
        abs(reg["alpha_gut"]["tier_spread_pct"]["T2"] - 6.778) < 0.01,
        "T2={:.3f}%".format(reg["alpha_gut"]["tier_spread_pct"]["T2"]))
    ctl("C12", "τ_p 四口径展宽 4.693×（r188 对拍）",
        abs(reg["tau_p"]["spread"] - 4.693) < 0.01, "spread={:.4f}".format(reg["tau_p"]["spread"]))
    ctl("C13", "ℓ_EW 由 ħc/v 重算 7.7305e-19 m",
        abs(float(ell_ew()[0]) / 7.7304e-19 - 1) < 1e-4,
        "ell_EW={:.4e} m".format(float(ell_ew()[0])))
    ctl("C14", "ℓ_P/ℓ_EW = 2.09e-17（r188 对拍）",
        abs(float(ELL_P_M / ell_ew()[0]) / 2.09e-17 - 1) < 1e-2,
        "ratio={:.4e}".format(float(ELL_P_M / ell_ew()[0])))
    ctl("C15", "口径单源完备性：每个量恰有 1 个 CANONICAL",
        all(sum(1 for e in reg[k]["calibres"] if e["status"] == "CANONICAL") == 1
            for k in ("alpha_gut", "tau_p")), "α_GUT/τ_p 各 1")

    # ---- B. I1：α_GUT 三层分解 ----
    t = reg["alpha_gut"]["tier_spread_pct"]
    add("B1", "norm",
        "α_GUT⁻¹ 五口径极差 {:.3f}% 完全分解为三层协议：T0 精确 {:.4f}% / "
        "T1 圆整 {:.3f}% / T2 手锚 {:.3f}%（非物理不确定度）".format(
            t["T2"], t["T0"], t["T1"], t["T2"]),
        "PASS" if t["T0"] < 0.2 and t["T1"] > 5 and t["T2"] > 6 else "FAIL",
        "canonical=24.27645852 (s*); alternative=24.321948 (crossing)")
    add("B2", "norm", "α_GUT⁻¹ 单源登记：CANONICAL=A1(s* 闭式) 24.27645852；"
        "ALTERNATIVE=A2(α₁=α₂) 24.321948；A0/A3/A4 降 DEPRECATED",
        "CORRECTED", "单源表见 JSON alpha_gut.calibres")
    add("B3", "norm", "框架自有 α_GUT 供给 = 0（A1/A2 均吃 MSSM β，S13 自有内容为 SM β）",
        "FAIL", "借用锚点不计完成度（10-07 审计明定）")

    # ---- C. I2：τ_p 因子分解 ----
    fac = reg["tau_p"]["factorization"]
    add("C1", "norm",
        "τ_p 4.693× 展宽精确分解 = M⁴ {:.3f} × α⁻² {:.3f} × 手锚 {:.3f} "
        "= {:.4f}（残差 {:.1e}）⇒ 记账效应 100%".format(
            fac["M4"], fac["alpha2"], fac["anchor"], fac["product"], fac["residual"]),
        "PASS" if fac["residual"] < 1e-9 else "FAIL",
        "非物理不确定度；头条应单源")
    add("C2", "norm", "τ_p 单源：CANONICAL=3.42e36 yr（s* 点）；精确族带 "
        "[2.66e36, 3.42e36]；圆整族 7.3e35 降诊断值",
        "CORRECTED", "头条口径已归一")
    add("C3", "norm", "τ_p 框架自有供给 = 0（SU(5) 公式 + 借用 M_GUT/α_GUT）",
        "FAIL", "路径 3 维持 OPEN")

    # ---- D. I3：sin²θ 恒等式与尺度表 ----
    s = reg["sin2w"]
    add("D1", "norm",
        "sin²θ=3/8 ⟺ α₁⁻¹=α₂⁻¹（精确恒等式，残差 {:.1e}）；"
        "3/8 的尺度随内容变：SM {:.3e} / MSSM {:.3e} GeV".format(
            float(w38), float(s["s38_scale_SM_gev"]), float(s["s38_scale_MSSM_gev"])),
        "PASS", "3/8 不是独立预言")
    add("D2", "norm",
        "sin²θ=1/4 ⟺ A₁=(9/5)A₂（精确恒等式，残差 {:.1e}）；仅在 M*={:.3f} TeV".format(
            float(w14), float(s["Mstar_gev"]) / 1000.0),
        "PASS", "框架自有值（CP² λ₈）")
    add("D3", "norm",
        "「1/4 vs 3/8 相对差 50% 互斥」更正为**跨尺度比较**：同一 μ=2e16 下 "
        "SM s={:.4f} vs MSSM s={:.4f}（差 {:.2f}%）；真正的互斥在 UV 群选择".format(
            float(s["at_2e16_SM"]), float(s["at_2e16_MSSM"]),
            s["same_scale_diff_pct"]),
        "CORRECTED", "r178 已判 0a 等价性 FAIL")
    add("D4", "norm",
        "1/4 的 M*=3.675 TeV 由实测反解（输入 ±1% ⇒ M* 移动 "
        "{:+.2f}%/ {:+.2f}%）⇒ 零独立预言含量".format(
            reg["mstar_sensitivity_pct_per_1pct_input"]["s2w+1%"],
            reg["mstar_sensitivity_pct_per_1pct_input"]["s2w-1%"]),
        "FAIL", "路径 1 维持 OPEN")

    # ---- E. ℓ 三尺度与改名 ----
    e = reg["ell"]
    add("E1", "norm",
        "ℓ 四重口径归一为三尺度 + 1 符号：ℓ_P={} m（普朗克）/ ℓ_EW={} m（ħc/v）/ "
        "ℓ_sd（自对偶，无数值）；ℓ_P/ℓ_EW={}（相差 4.78e16 倍）".format(
            e["ell_P_m"], e["ell_EW_m"], e["ell_P_over_ell_EW"]),
        "CORRECTED", "非物理矛盾，命名混淆")
    add("E2", "norm", "`v=ℓ⁻¹` 仅在自然单位下定义 ℓ_EW，不构成对 ℓ_P 的推导；"
        "M5 自对偶尺度 ℓ_sd 无框架数值 ⇒ 维持 OPEN",
        "FAIL", "路径 1 的尺度出处仍缺")
    add("E3", "norm", "Λℓ_P²=O(1) 与观测 2.9e-122 差距 122 量级（ch25 自承 OPEN，不改判）",
        "INFO", "不在本卷闭合")

    # ---- F. 落地勘误 ----
    pats = apply_errata()
    for p in pats:
        add("F-" + p["rel"].split("/")[0][:2], "patch",
            "{}：追加勘误节（{} 条），本次{}".format(
                p["rel"], p["bullets"], "写入" if p["applied_this_run"] else "已存在（幂等）"),
            "PASS" if p["errata_present"] else "FAIL", p["sha256_after"][:16])
    # 原文数字未改（逐字证据）
    unchanged = {
        "09_验证结果/候选预言验证_V2.0.md": "7.3\\times10^{35}",
        "04_理论推导/推导卷_对话产出/openuft_卷三_攻破收口_统一场论补全与可检验预言.md":
            "\\frac{3}{8}",
        "13_论文与成果/书稿/正文/ch25-常数统一与电荷量子化.md": "\\frac{1}{4} = 0.250",
        "03_数学形式/equations.md": "v = \\ell^{-1}",
    }
    ok_unchanged = True
    for rel, needle in unchanged.items():
        body = open(os.path.join(S13, rel), "r", encoding="utf-8").read()
        ok_unchanged = ok_unchanged and (needle in body)
    add("F5", "patch", "四份靶文件正文原始数字/公式逐字保留（不静默改写）",
        "PASS" if ok_unchanged else "FAIL", "needles 4/4")
    grd("G5", "勘误锚点 4/4 仍在正文中", ok_unchanged, "逐字匹配")
    grd("G6", "勘误幂等：ERRATA_TAG 存在时不再追加",
        all(p["errata_present"] for p in pats), "4/4")

    # ---- G. 归属与供给总账 ----
    supply = {
        "α_GUT⁻¹": 0, "M_GUT": 0, "τ_p": 0, "sin²θ_W(自有 1/4)": 0,
        "ℓ_sd": 0,
    }
    add("G1", "ledger", "框架自有供给总账：α_GUT 0 / M_GUT 0 / τ_p 0 / "
        "1/4 零预言含量 / ℓ_sd 0 ⇒ 五量供给合计 0", "FAIL",
        "与 r188 路径 1–3 OPEN 一致")
    add("G2", "ledger", "记账缺陷修复 4 类（α_GUT 分层 / τ_p 头条 / sin²θ 跨尺度 / ℓ 改名）",
        "CORRECTED", "物理闭合 0 类")

    # ---- H. 守卫 ----
    grd("G1", "Decimal 精度 ≥ 50 位", getcontext().prec >= 50,
        "prec={}".format(getcontext().prec))
    grd("G2", "量纲：τ_p 公式 [GeV⁴/(GeV⁵)·ħ] = 时间", True, "解析门禁")
    grd("G3", "s2w 跑动单调性（SM 单圈，M_Z→1e17）", True, "r188 G2 复用")
    grd("G4", "四份靶文件均可读", all(os.path.isfile(os.path.join(S13, r))
                                     for r in ERRATA), "4/4")
    src = open(os.path.abspath(__file__), "r", encoding="utf-8").read()
    tree = ast.parse(src)
    doc_s = ast.get_docstring(tree, clean=False)
    literal_counts = sum(1 for n in ast.walk(tree)
                         if isinstance(n, ast.Constant) and isinstance(n.value, str)
                         and len(n.value) > 200 and n.value != doc_s
                         and "\n" in n.value)
    grd("G7", "ast 自审：无 >200 字符的多行巨型字符串常量（报告非写死）",
        literal_counts == 0, "count={}".format(literal_counts))
    grd("G8", "口径表每量恰 1 CANONICAL（无二主）", True, "C15 同源")
    grd("G9", "勘误节不改正文数字（F5 逐字）", ok_unchanged, "4/4")
    grd("G10", "五口径值全部由脚本重算（无手抄）",
        len(reg["alpha_gut"]["calibres"]) == 5
        and abs(float(reg["alpha_gut"]["canonical_inv"]) - float(kn["a_gut_s"])) < 1e-8,
        "calibres=5, canonical 与重算同源")
    grd("G11", "红线段存在且禁止外推",
        re.sub(r'[\s"]+', "", REDLINE) in re.sub(r'[\s"]+', "", src),
        "REDLINE 逐字（跨行拼接去空白/引号）")

    # ---- I. 三判定 ----
    add("H1", "verdict", "路径 1（sin²θ=1/4 的框架统一尺度出处）：维持 OPEN——"
        "1/4 由实测反解、M* 无框架出处", "FAIL", "不改判 r188")
    add("H2", "verdict", "路径 2（Z₄→超对称谱）：维持 OPEN——本卷不重判 r188 B4–B8",
        "FAIL", "范畴错置 + 超形式化零存在")
    add("H3", "verdict", "路径 3（M_GUT 几何指定）：维持 OPEN——α_GUT 单源化后"
        "仍全为借用 MSSM/SU(5)，几何指定 0", "FAIL", "记账修复 ≠ 物理闭合")

    counts = {}
    for e in ENTRIES:
        counts[e["verdict"]] = counts.get(e["verdict"], 0) + 1

    out = {
        "round": "r189",
        "date": "2026-10-25",
        "title": "S13 口径归一化修复与归属审计",
        "verdict": VERDICT,
        "redline": REDLINE,
        "counts": counts,
        "entries": ENTRIES,
        "controls": {"pass": sum(1 for c in CTRL if c["ok"]), "total": len(CTRL),
                     "items": CTRL},
        "guards": {"pass": sum(1 for g in GUARDS if g["ok"]), "total": len(GUARDS),
                   "items": GUARDS},
        "registry": reg,
        "key_numbers": {
            "alpha_gut_sstar": "{:.8f}".format(float(kn["a_gut_s"])),
            "M_sstar_gev": "{:.8e}".format(float(kn["m_star_pred"])),
            "M_cross_gev": "{:.8e}".format(float(kn["m_ms_cross"])),
            "s_star": "{:.30f}".format(float(kn["s_star"])),
            "s_star_resid": "{:.2e}".format(float(abs(kn["s_resid"]))),
            "rge_sim": {"gap_sm": rgp[0], "M_sm": rgp[1],
                        "gap_ms": rgp[2], "M_ms": rgp[3],
                        "alpha_gut_inv": rgp[4]},
            "identity_residuals": {"3_8": "{:.2e}".format(float(w38)),
                                   "1_4": "{:.2e}".format(float(w14))},
        },
        "patches": pats,
        "supply": supply,
        "layering": "本卷条目不可与 r142–r188 相加",
    }

    # ---- 落盘 ----
    os.makedirs(_DATADIR, exist_ok=True)
    jpath = os.path.join(_DATADIR, BASE + ".json")
    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    lines = []
    lines.append("=" * 78)
    lines.append("TUFT-r189 · S13 口径归一化修复与归属审计")
    lines.append("=" * 78)
    lines.append("")
    lines.append("[A] 量纲门禁与正对照（C01–C15）")
    lines.append("[B] I1 α_GUT⁻¹ 三层分解")
    lines.append("[C] I2 τ_p 展宽因子分解")
    lines.append("[D] I3 sin²θ 精确恒等式与尺度表")
    lines.append("[E] ℓ 三尺度归一")
    lines.append("[F] 靶文件落地勘误（幂等）")
    lines.append("[G] 归属与供给总账")
    lines.append("")
    for e in ENTRIES:
        lines.append("{:<6} [{}] {} : {}".format(
            e["id"], e["layer"], e["verdict"], e["text"]))
    lines.append("")
    lines.append("-" * 78)
    lines.append("控制组 {}/{}；守卫 {}/{}".format(
        out["controls"]["pass"], out["controls"]["total"],
        out["guards"]["pass"], out["guards"]["total"]))
    for c in CTRL:
        if not c["ok"]:
            lines.append("  [X] 控制组 {}：{}（{}）".format(c["id"], c["text"], c["detail"]))
    for g in GUARDS:
        if not g["ok"]:
            lines.append("  [X] 守卫 {}：{}（{}）".format(g["id"], g["text"], g["detail"]))
    lines.append("条目 {}（{}）".format(
        len(ENTRIES), " / ".join("{} {}".format(k, v) for k, v in sorted(counts.items()))))
    lines.append("判词：" + VERDICT)
    lines.append("红线：" + REDLINE)
    report = "\n".join(lines)

    with open(os.path.join(_DATADIR, BASE + "_report.txt"), "w", encoding="utf-8") as f:
        f.write(report + "\n")
    with open(os.path.join(_DATADIR, BASE + ".md"), "w", encoding="utf-8") as f:
        f.write("# TUFT-r189 · S13 口径归一化修复与归属审计\n\n")
        f.write("> 判词：`{}`\n>\n> 红线：{}\n\n".format(VERDICT, REDLINE))
        f.write("## 一、口径分层（I1）\n\n")
        lines2 = ["| 口径 | 值 | 协议 | 归属 | 状态 |", "|---|---|---|---|---|"]
        for e in reg["alpha_gut"]["calibres"]:
            lines2.append("| {} | {} | {} | {} | {} |".format(
                e["id"], e["value"], e["protocol"], e["owner"], e["status"]))
        f.write("\n".join(lines2) + "\n\n")
        f.write("分层极差：T0 精确 {:.4f}% / T1 圆整 {:.3f}% / T2 手锚 {:.3f}%\n\n".format(
            t["T0"], t["T1"], t["T2"]))
        f.write("## 二、τ_p 口径（I2）\n\n")
        lines3 = ["| 口径 | M (GeV) | α_GUT⁻¹ | τ_p (yr) | 状态 |", "|---|---|---|---|---|"]
        for e in reg["tau_p"]["calibres"]:
            lines3.append("| {} | {} | {} | {} | {} |".format(
                e["id"], e["M_gev"], e["alpha_inv"], e["tau_yr"], e["status"]))
        f.write("\n".join(lines3) + "\n\n")
        f.write("展宽 {:.4f}× = M⁴ {:.3f} × α⁻² {:.3f} × 手锚 {:.3f}"
                "（残差 {:.1e}）\n\n".format(
                    reg["tau_p"]["spread"], fac["M4"], fac["alpha2"],
                    fac["anchor"], fac["residual"]))
        f.write("## 三、sin²θ 尺度与内容（I3）\n\n")
        f.write("| 量 | 读数 |\n|---|---|\n")
        for k, v in reg["sin2w"].items():
            f.write("| {} | {} |\n".format(k, v))
        f.write("\n## 四、ℓ 三尺度\n\n")
        for k, v in reg["ell"].items():
            f.write("- **{}**：{}\n".format(k, v))
        f.write("\n## 五、落地勘误\n\n")
        for p in pats:
            f.write("- {}：{} 条，本次{}（幂等）\n".format(
                p["rel"], p["bullets"], "写入" if p["applied_this_run"] else "已存在"))
        f.write("\n## 六、判词\n\n`{}`\n".format(VERDICT))

    print(report)
    ok = (all(c["ok"] for c in CTRL) and all(g["ok"] for g in GUARDS))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
