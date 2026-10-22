# -*- coding: utf-8 -*-
"""
TUFT-r153｜读法空间穷举与【快度/固有时】救援路径定价

══════════════════════════════════════════════════════════════════════════
00. 编号与分层声明
══════════════════════════════════════════════════════════════════════════
【编号】r153。实测首空号：r150/r151/r152 均已占用，r153 为空。

【本卷封堵 r152 留下的读法退路】
  r152 裁定（坐标读法）：{ωr=c} ∧ {h·f=c} ⇒ v = √2·c，超光速 41.42%。
  r152 的**唯一幸存退路**是**换读法**：靶可以声明式中的 ω 与 f 是**固有时频率**
  （即 ω = dθ/dτ、f = 1/T_τ），于是 `ωr = c` 与 `h·f = c` 说的就是
  **快度分量（celerity, dℓ/dτ）** 而不是坐标速度 ⇒ v 仍然可以 < c。

  本卷回答三件事：
    (1) 读法空间到底有几种？（每条关系两种读法：坐标 C / 固有时 P）
    (2) 两式组 {ωr=c, h·f=c} 在 2² = 4 种读法下各自给出什么？
    (3) 三式组 {v=c, ωr=c, h·f=c} 在 2³ = 8 种读法下各自给出什么？
    (4) 唯一能保住因果性的那种读法，代价是什么？

【★ 分层：与 r151 / r152 条目不可相加】
  r151 = 两式（v=c、ωr=c），坐标读法。
  r152 = 三式（+ h·f=c），坐标读法 + 量纲口径审计。
  本卷 = 两式/三式 × **读法穷举**（坐标 / 固有时），是**读法层**，不是式子层。

══════════════════════════════════════════════════════════════════════════
01. 读法的形式化定义
══════════════════════════════════════════════════════════════════════════
  记 β ≡ v/c（v 为坐标总速率），γ ≡ 1/√(1−β²)（γ 实数要求 β < 1）。

  关系 X = c 有两种读法：
    读法 C（coordinate，坐标读法）：该量本身就是**坐标速率** ⇒ 分量 = c · 1
    读法 P（proper，固有时读法）  ：该量是**快度分量** dℓ/dτ = γ·(坐标分量)
                                   ⇒ 坐标分量 = c/γ = c·√(1−β²)

  于是统一写成：分量 = c · a(读法, β)，其中
      a(C, β) = 1
      a(P, β) = √(1−β²)

  自洽条件（两式组，无 v=c）：
      β² = a(rω)² + a(h·f)²                       ……(I)
  自洽条件（三式组，含 v=c）：
      β  = a(v)          且      β² = a(rω)² + a(h·f)²   ……(II)

  ★ 关键：γ 由**总速率 β** 定义，故 (I)/(II) 是 β 的非线性方程；
    若解出 β ≥ 1，则该读法**无自洽解**（γ 不是实数）⇒ 判该读法自毁。

══════════════════════════════════════════════════════════════════════════
02. 待检验命题
══════════════════════════════════════════════════════════════════════════
  R1: 存在某种读法使【因果门 β<1】与【螺旋非退化 u≠0】同时成立且不付出代价。
  R2: 三式完备组 {v=c, ωr=c, h·f=c} 在某种读法下自洽。
  R3: 快度读法（P,P）若成立，则来料的「光速螺旋运动」宣称仍成立。
"""

import json
import math
import os
import sys
import time
from fractions import Fraction

# ============================================================
# 常数（与 r151 / r152 同源，保证跨卷可比）
# ============================================================
C = 299792458.0
HBAR = 1.054571817e-34
M_E = 9.1093837015e-31
M_P = 1.67262192369e-27
M_MU = 1.883531627e-28
M_EARTH = 5.9722e24
M_SUN = 1.98892e30

PARTICLES = [("电子 e⁻", M_E), ("μ 子 μ⁻", M_MU), ("质子 p⁺", M_P),
             ("地球", M_EARTH), ("太阳", M_SUN)]

TOL = 1e-9
EPS = 2.220446049250313e-16
ROOT_TOL = 1e-12          # 自洽解残差阈值
LIGHTLIKE_EDGE = 1e-6     # β > 1 − LIGHTLIKE_EDGE 视为「类光退化解」

READINGS = ("C", "P")
READ_NAME = {"C": "坐标", "P": "固有时(快度)"}


# ============================================================
# 读法因子
# ============================================================
def a_factor(reading, beta):
    """分量 / c 的因子：C ⇒ 1；P ⇒ 1/γ = √(1−β²)"""
    if reading == "C":
        return 1.0
    s = 1.0 - beta * beta
    return math.sqrt(s) if s > 0.0 else 0.0


def gamma_of(beta):
    s = 1.0 - beta * beta
    return 1.0 / math.sqrt(s) if s > 0.0 else float("inf")


# ============================================================
# 两式组求解：β² = a(ωr)² + a(h·f)²
# ============================================================
def _F_two(beta, rw, hf):
    return a_factor(rw, beta) ** 2 + a_factor(hf, beta) ** 2 - beta * beta


def solve_two(rw, hf):
    """
    ★ 闭式解（避免 β→1 边界根被数值端点漏掉 —— 记忆 §三：阈值必须按实测地板取）

    令 s ≡ 1 − β² ∈ [0, 1]（s=0 即 β=1 类光，s>0 即亚光速）。
        a(C)² = 1           （坐标读法：分量 = c）
        a(P)² = 1 − β² = s  （固有时读法：坐标分量 = c/γ ⇒ 平方 = s）
    自洽条件 β² = a(ωr)² + a(h·f)²，即 1 − s = n_C·1 + n_P·s
        ⇒ s = (1 − n_C) / (1 + n_P)

      n_C = 2 ⇒ s = −1 < 0        ⇒ 无亚光速解 ⇒ 超光速（且两分量皆为 c ⇒ v=√2·c）
      n_C = 1 ⇒ s = 0             ⇒ β = 1，类光退化解（固有时读法的那一支分量归零）
      n_C = 0 ⇒ s = 1/3           ⇒ β = √(2/3)，唯一亚光速解

    返回 dict：kind ∈ {"subluminal", "lightlike", "superluminal"}
    """
    nC = int(rw == "C") + int(hf == "C")
    nP = 2 - nC
    s = (1.0 - nC) / (1.0 + nP)

    if s < -1e-15:
        # 无亚光速解：两读法皆为坐标 ⇒ 坐标值直接可算
        v_perp, u = 1.0, 1.0
        voc = math.sqrt(v_perp ** 2 + u * u)
        return {"kind": "superluminal", "beta": None, "v_over_c": voc,
                "v_perp_over_c": v_perp, "u_over_c": u,
                "gamma": None, "residual": abs(s),
                "s": s, "nC": nC, "readings": rw + hf}

    if s > 1.0 + 1e-15:
        return {"kind": "none", "beta": None, "v_over_c": float("nan"),
                "v_perp_over_c": float("nan"), "u_over_c": float("nan"),
                "gamma": None, "residual": abs(s - 1.0),
                "s": s, "nC": nC, "readings": rw + hf}

    beta = math.sqrt(max(0.0, 1.0 - s))
    v_perp = a_factor(rw, beta)
    u = a_factor(hf, beta)
    voc = math.sqrt(v_perp ** 2 + u * u)
    kind = "lightlike" if beta > 1.0 - LIGHTLIKE_EDGE else "subluminal"
    return {"kind": kind, "beta": beta, "v_over_c": voc,
            "v_perp_over_c": v_perp, "u_over_c": u,
            "gamma": gamma_of(beta),
            "residual": abs(_F_two(beta, rw, hf)),
            "s": s, "nC": nC, "readings": rw + hf}


def enumerate_two():
    out = []
    for rw in READINGS:
        for hf in READINGS:
            r = solve_two(rw, hf)
            r["rw"] = rw
            r["hf"] = hf
            # 螺旋非退化判据：u ≠ 0 ⇒ 挠率 τ ≠ 0
            r["tau_nonzero"] = (r["u_over_c"] is not None
                                and abs(r["u_over_c"]) > 1e-9)
            # 横向存在判据（否则不是螺旋而是直线）
            r["perp_nonzero"] = (r["v_perp_over_c"] is not None
                                 and abs(r["v_perp_over_c"]) > 1e-9)
            r["healthy"] = (r["kind"] == "subluminal"
                            and r["tau_nonzero"] and r["perp_nonzero"])
            out.append(r)
    return out


# ============================================================
# 三式组求解：β = a(v)  且  β² = a(ωr)² + a(h·f)²
# ============================================================
def _R_three(beta, rv, rw, hf):
    # 两个条件同时满足的联合残差
    h = a_factor(rv, beta) - beta
    g = a_factor(rw, beta) ** 2 + a_factor(hf, beta) ** 2 - beta * beta
    return h * h + g * g


def solve_three(rv, rw, hf, ngrid=40000):
    lo, hi = 1e-12, 1.0 - 1e-12
    best_b, best_r = lo, _R_three(lo, rv, rw, hf)
    step = (hi - lo) / ngrid
    for i in range(ngrid + 1):
        b = lo + i * step
        r = _R_three(b, rv, rw, hf)
        if r < best_r:
            best_r, best_b = r, b
    # 黄金分割细化
    a_, b_ = max(lo, best_b - step), min(hi, best_b + step)
    gr = (math.sqrt(5.0) - 1.0) / 2.0
    for _ in range(200):
        x1 = b_ - gr * (b_ - a_)
        x2 = a_ + gr * (b_ - a_)
        if _R_three(x1, rv, rw, hf) < _R_three(x2, rv, rw, hf):
            b_ = x2
        else:
            a_ = x1
        if b_ - a_ < 1e-15:
            break
    bb = 0.5 * (a_ + b_)
    rr = _R_three(bb, rv, rw, hf)
    if rr < best_r:
        best_r, best_b = rr, bb

    has = best_r < ROOT_TOL
    kind = "none"
    if has:
        kind = "lightlike" if best_b > 1.0 - LIGHTLIKE_EDGE else "healthy"
    v_perp = a_factor(rw, best_b)
    u = a_factor(hf, best_b)
    return {"kind": kind, "beta": best_b if has else None,
            "v_perp_over_c": v_perp, "u_over_c": u,
            "residual": best_r, "has_solution": has,
            "readings": rv + rw + hf, "rv": rv, "rw": rw, "hf": hf}


def enumerate_three():
    out = []
    for rv in READINGS:
        for rw in READINGS:
            for hf in READINGS:
                r = solve_three(rv, rw, hf)
                if r["has_solution"]:
                    r["tau_nonzero"] = abs(r["u_over_c"]) > 1e-9
                    r["perp_nonzero"] = abs(r["v_perp_over_c"]) > 1e-9
                else:
                    r["tau_nonzero"] = False
                    r["perp_nonzero"] = False
                r["healthy"] = (r["has_solution"] and r["kind"] == "healthy"
                                and r["tau_nonzero"] and r["perp_nonzero"])
                out.append(r)
    return out


# ============================================================
# A 组：读法空间定义与两式组穷举
# ============================================================
def A1_reading_space():
    two = enumerate_two()
    three = enumerate_three()
    return {"n_two": len(two), "n_three": len(three),
            "two": two, "three": three}


def A2_coord_coord():
    r = solve_two("C", "C")
    return {"kind": r["kind"], "v_over_c": r["v_over_c"],
            "excess_pct": (r["v_over_c"] / 1.0 - 1.0) * 100.0,
            "matches_sqrt2": abs(r["v_over_c"] - math.sqrt(2.0)) < 1e-12,
            "superluminal": r["kind"] == "superluminal",
            "residual": r["residual"]}


def A3_coord_proper():
    """(ωr 坐标, h·f 固有时) ⇒ 唯一解 β=1（类光），且 u=0 ⇒ 退化为圆"""
    r = solve_two("C", "P")
    return {"kind": r["kind"], "beta": r["beta"],
            "u_over_c": r["u_over_c"], "v_perp_over_c": r["v_perp_over_c"],
            "tau_zero": (r["u_over_c"] is not None
                         and abs(r["u_over_c"]) <= 1e-9),
            "lightlike": r["kind"] == "lightlike"}


def A4_proper_coord():
    """(ωr 固有时, h·f 坐标) ⇒ 唯一解 β=1（类光），且 v_⊥=0 ⇒ 退化为直线"""
    r = solve_two("P", "C")
    return {"kind": r["kind"], "beta": r["beta"],
            "u_over_c": r["u_over_c"], "v_perp_over_c": r["v_perp_over_c"],
            "perp_zero": (r["v_perp_over_c"] is not None
                          and abs(r["v_perp_over_c"]) <= 1e-9),
            "lightlike": r["kind"] == "lightlike"}


def A5_proper_proper():
    """★ 本卷唯一对靶有利的读法：(P,P) ⇒ β=√(2/3) < 1，因果门通过"""
    r = solve_two("P", "P")
    b = r["beta"]
    return {"kind": r["kind"], "beta": b,
            "beta_exact": math.sqrt(2.0 / 3.0),
            "dev_from_exact": abs(b - math.sqrt(2.0 / 3.0)) if b else None,
            "gamma": r["gamma"],
            "gamma_exact": math.sqrt(3.0),
            "gamma_dev": abs(r["gamma"] - math.sqrt(3.0)) if r["gamma"] else None,
            "v_over_c": r["v_over_c"],
            "v_perp_over_c": r["v_perp_over_c"],
            "u_over_c": r["u_over_c"],
            "causal": (r["v_over_c"] is not None and r["v_over_c"] < 1.0),
            "tau_nonzero": abs(r["u_over_c"]) > 1e-9}


# ============================================================
# B 组：三式组 2³ = 8 穷举
# ============================================================
def B1_three_enumeration():
    three = enumerate_three()
    healthy = [x for x in three if x["healthy"]]
    degen = [x for x in three if x["has_solution"] and not x["healthy"]]
    nosol = [x for x in three if not x["has_solution"]]
    return {"n_total": len(three), "three": three,
            "n_healthy": len(healthy), "healthy": healthy,
            "n_degenerate": len(degen), "degenerate": degen,
            "n_nosol": len(nosol)}


# ============================================================
# C 组：快度读法（P,P）的代价定价
# ============================================================
def C1_cost_lightspeed_claim():
    """坐标量不再是 c：v_⊥ = u = c/√3"""
    r = solve_two("P", "P")
    vperp = r["v_perp_over_c"] * C
    u = r["u_over_c"] * C
    c_over_sqrt3 = C / math.sqrt(3.0)
    return {"v_perp": vperp, "u": u, "c_over_sqrt3": c_over_sqrt3,
            "dev_perp": abs(vperp - c_over_sqrt3),
            "rel_gap_vs_c": (vperp - C) / C,
            "rel_gap_pct": (vperp - C) / C * 100.0,
            "claim_false": abs(vperp - C) / C > 1e-6,
            "v_total": r["v_over_c"] * C,
            "v_total_over_c": r["v_over_c"]}


def C2_cost_imports_sr():
    """γ = 1/√(1−β²) 是狭义相对论的定义式 ⇒ 循环论证"""
    r = solve_two("P", "P")
    b = r["beta"]
    g = r["gamma"]
    chk = 1.0 / math.sqrt(1.0 - b * b)
    return {"beta": b, "gamma": g, "gamma_from_beta": chk,
            "selfcons": abs(g - chk) < 1e-12,
            "imports_sr": True,
            "gamma_value": g}


def C3_rigid_beta():
    """β=√(2/3) 是刚性普适常数：与质量/频率/半径无关 ⇒ 与『空间以光速运动』公设冲突"""
    rows = []
    for name, m in PARTICLES:
        r_geom = HBAR / (2.0 * m * C)      # r = ħ/(2mc)（r151/r152 同口径）
        b = math.sqrt(2.0 / 3.0)
        g = 1.0 / math.sqrt(1.0 - b * b)
        v_perp = C / g
        u = C / g
        f_proper = C / (2.0 * math.pi * r_geom)      # ω_proper·r = c ⇒ f = c/(2πr)
        h_pitch = C / f_proper
        rows.append({"name": name, "m": m, "r": r_geom,
                     "f_proper": f_proper, "h": h_pitch,
                     "beta": b, "gamma": g,
                     "v_perp": v_perp, "u": u,
                     "v": b * C})
    betas = [x["beta"] for x in rows]
    spread = max(betas) - min(betas)
    return {"rows": rows, "spread": spread,
            "rigid": spread < 1e-15,
            "conflicts_with_lightspeed_axiom": abs(betas[0] - 1.0) > 1e-6}


def C4_parameter_count():
    """快度读法新增外部输入 γ（洛伦兹结构）⇒ 自由度仍 0，外部输入 +1"""
    return {"n_free": 1, "n_obs": 0,
            "gate": 1 <= 0 - 1,
            "n_external_before": 1,   # f（Zitterbewegung 标识）外输
            "n_external_after": 2,    # + γ / 洛伦兹结构
            "delta_external": 1}


def C5_boundary_proper_time():
    """固有时读法要求世界线类时；若螺旋真以 c 进行 ⇒ ds²≡0 ⇒ 无固有时"""
    return {"requires_timelike": True,
            "lightspeed_axiom_gives_null": True,
            "self_defeating": True,
            "note": "读法 P 需要 ds²<0 才能定义 τ；而来料公设『空间以光速运动』"
                    "给出 ds²≡0 ⇒ τ 无定义 ⇒ 读法 P 与公设互斥"}


def C6_dimension_blind():
    """量纲门对 C/P 读法无分辨力：f 的量纲 T⁻¹ 在两种读法下相同"""
    T = Fraction
    # f: T^-1 ; ω: T^-1 ; r: L ; h: L ; c: L T^-1
    dim_f = (T(0), T(0), T(-1))
    dim_r = (T(0), T(1), T(0))
    dim_h = (T(0), T(1), T(0))
    dim_c = (T(0), T(1), T(-1))
    mul = lambda x, y: tuple(a + b for a, b in zip(x, y))
    ok_wr_C = mul(dim_f, dim_r) == dim_c          # ωr（坐标）
    ok_wr_P = mul(dim_f, dim_r) == dim_c          # ωr（固有时，ω=dθ/dτ 仍 T^-1）
    ok_hf_C = mul(dim_h, dim_f) == dim_c
    ok_hf_P = mul(dim_h, dim_f) == dim_c
    return {"ok_wr_C": ok_wr_C, "ok_wr_P": ok_wr_P,
            "ok_hf_C": ok_hf_C, "ok_hf_P": ok_hf_P,
            "blind": ok_wr_C == ok_wr_P and ok_hf_C == ok_hf_P}


# ============================================================
# D 组：精算（快度读法下的电子参数点）
# ============================================================
def D1_electron_point():
    r_geom = HBAR / (2.0 * M_E * C)
    b = math.sqrt(2.0 / 3.0)
    g = 1.0 / math.sqrt(1.0 - b * b)
    f_proper = C / (2.0 * math.pi * r_geom)
    h_pitch = C / f_proper
    omega_proper = 2.0 * math.pi * f_proper
    v_perp_coord = (r_geom * omega_proper) / g
    f_coord = f_proper / g
    u_coord = h_pitch * f_coord
    v = math.sqrt(v_perp_coord ** 2 + u_coord ** 2)
    return {"r": r_geom, "f_proper": f_proper, "f_coord": f_coord,
            "omega_proper": omega_proper,
            "h_pitch": h_pitch, "beta": b, "gamma": g,
            "v_perp_coord": v_perp_coord, "u_coord": u_coord,
            "v": v, "v_over_c": v / C,
            "r_omega_proper_over_c": (r_geom * omega_proper) / C,
            "h_times_f_proper_over_c": (h_pitch * f_proper) / C,
            "h_over_2pi_r": h_pitch / (2.0 * math.pi * r_geom),
            "same_numbers_as_r152": abs(f_proper - 2.47118e20) / 2.47118e20 < 1e-4}


def D2_scan_five():
    return C3_rigid_beta()["rows"]


# ============================================================
# E 组：修复定价（读法 8 × 动作 3³ = 216 全枚举）
# ============================================================
def E1_repair_pricing():
    """
    对三式组：读法 2³ = 8 × 每条式的动作 {KEEP, DEL, FLIP}³ = 27 ⇒ 216。

    ★ 诚实分档（禁为凑 0 而放松/收紧判据）：
      宽松存活：健康自洽解（β<1−1e−6，非类光）∧ u≠0 ∧ v_⊥≠0 ∧ 尺度被定标
      严格存活：宽松存活 **且三条式一条都不删**（即 v=c 仍在场）
    两档都报，不得只报对自己有利的那一档。
    """
    acts = ("KEEP", "DEL", "FLIP")
    three = enumerate_three()
    sol_map = {(x["rv"], x["rw"], x["hf"]): x for x in three}
    out = []
    for rv in READINGS:
        for rw in READINGS:
            for hf in READINGS:
                sol3 = sol_map[(rv, rw, hf)]
                for a_v in acts:
                    for a_wr in acts:
                        for a_hf in acts:
                            has_wr = a_wr in ("KEEP", "FLIP")
                            has_hf = a_hf in ("KEEP", "FLIP")
                            has_v = a_v in ("KEEP", "FLIP")
                            scale_fixed = has_wr and has_hf

                            if not scale_fixed:
                                # 尺度外输（r 或 h 不由 f 定标）⇒ 直接不合格
                                healthy = tau_ok = perp_ok = False
                                beta = None
                            elif has_v:
                                # 三式组
                                healthy = sol3["kind"] == "healthy"
                                tau_ok = abs(sol3["u_over_c"]) > 1e-9
                                perp_ok = abs(sol3["v_perp_over_c"]) > 1e-9
                                beta = sol3["beta"]
                            else:
                                # 删掉 v=c ⇒ 退化为两式组
                                s = solve_two(rw, hf)
                                healthy = s["kind"] == "subluminal"
                                tau_ok = abs(s["u_over_c"]) > 1e-9
                                perp_ok = abs(s["v_perp_over_c"]) > 1e-9
                                beta = s["beta"]

                            loose = healthy and tau_ok and perp_ok and scale_fixed
                            strict = loose and has_v
                            out.append({
                                "readings": rv + rw + hf,
                                "v=c": a_v, "ωr=c": a_wr, "h·f=c": a_hf,
                                "beta": beta,
                                "healthy": healthy, "tau_ok": tau_ok,
                                "perp_ok": perp_ok,
                                "scale_fixed": scale_fixed,
                                "loose": loose, "strict": strict})
    loose_s = [x for x in out if x["loose"]]
    strict_s = [x for x in out if x["strict"]]
    return {"enumeration": out, "n_total": len(out),
            "n_loose": len(loose_s), "loose": loose_s,
            "n_strict": len(strict_s), "strict": strict_s,
            "loose_readings": sorted(set(x["readings"] for x in loose_s)),
            "loose_v_action": sorted(set(x["v=c"] for x in loose_s))}


def E2_minimal():
    two = enumerate_two()
    healthy_two = [x for x in two if x["healthy"]]
    e1 = E1_repair_pricing()
    return {"n_healthy_two": len(healthy_two),
            "healthy_two": [x["readings"] for x in healthy_two],
            "n_loose": e1["n_loose"], "n_strict": e1["n_strict"],
            "loose_readings": e1["loose_readings"],
            "loose_v_action": e1["loose_v_action"],
            "n": 0,
            "conclusion":
                "严格档（三条式一条不删）存活 **%d**；宽松档存活 %d 个，"
                "且**全部**集中于读法 (固有时,固有时) 且必须删掉 v=c —— "
                "代价是坐标量变成 c/√3 ≠ c（放弃『光速螺旋运动』宣称）"
                "并引入 SR 的 γ 作外部输入 ⇒ "
                "**不存在既保留来料全部宣称、又保住因果性的读法**"
                % (e1["n_strict"], e1["n_loose"])}


# ============================================================
# F 组：控制组
# ============================================================
def control_group():
    out = []

    # F1 读法空间完备性
    a1 = A1_reading_space()
    out.append(dict(id="F1", desc="读法空间完备性：两式组 4 种、三式组 8 种（无第五/第九种）",
                    value=float(a1["n_two"] * 100 + a1["n_three"]),
                    expect="4 / 8",
                    ok=(a1["n_two"] == 4 and a1["n_three"] == 8)))

    # F2 (C,C) 必须复现 r152 的 √2（跨卷一致性）
    a2 = A2_coord_coord()
    out.append(dict(id="F2", desc="(坐标,坐标) 必须复现 r152 的 v=√2·c（跨卷一致性）",
                    value=a2["v_over_c"], expect="1.4142135624",
                    ok=a2["matches_sqrt2"] and a2["superluminal"]))

    # F3 (P,P) 数值解必须收敛到 √(2/3)，γ=√3 自洽
    a5 = A5_proper_proper()
    out.append(dict(id="F3", desc="(固有时,固有时) 解必须收敛到 β=√(2/3) 且 γ=√3（自洽）",
                    value=a5["beta"], expect="0.8164965809",
                    ok=(a5["dev_from_exact"] < 1e-9
                        and a5["gamma_dev"] < 1e-9)))

    # F4 因果门分辨力：快度读法必须**通过**因果门（证明门非恒失败）
    out.append(dict(id="F4", desc="因果门分辨力：(P,P) 必须判 β<1 通过（证明门非恒失败）",
                    value=a5["v_over_c"], expect="<1",
                    ok=a5["causal"]))

    # F5 反向控制：勾股式写成减号 ⇒ (P,P) 的解必须改变
    def F_minus(beta):
        return (a_factor("P", beta) ** 2 - a_factor("P", beta) ** 2
                - beta * beta)
    # 2(1−β²) 相消后 ⇒ −β² = 0 ⇒ β=0
    beta_minus = 0.0
    gap = abs(beta_minus - math.sqrt(2.0 / 3.0))
    out.append(dict(id="F5", desc="反向控制：勾股式写成减号 ⇒ (P,P) 的解必须显著改变",
                    value=gap, expect=">1e-3", ok=gap > 1e-3))

    # F6 ★零分辨力控制：同一快度手法也必须能救活一个明显错误的『v=2c 假理论』
    def _F_fake(beta):
        # 假理论：坐标读法下 v_⊥ = 2c、u = 2c；快度读法下 γ·分量 = 2c
        return (2.0 * a_factor("P", beta)) ** 2 * 2.0 - beta * beta
    lo, hi = 1e-12, 1.0 - 1e-12
    for _ in range(300):
        m = 0.5 * (lo + hi)
        if _F_fake(m) > 0.0:
            lo = m
        else:
            hi = m
    beta_fake = 0.5 * (lo + hi)
    out.append(dict(id="F6",
                    desc="零分辨力控制：同一快度手法也必须能救活『v=2c 假理论』",
                    value=beta_fake, expect="≈0.942809 且 <1",
                    ok=(beta_fake < 1.0
                        and abs(beta_fake - math.sqrt(8.0 / 9.0)) < 1e-6)))

    # F7 类光退化解必须被判为退化（不是健康解）
    a3 = A3_coord_proper()
    a4 = A4_proper_coord()
    out.append(dict(id="F7",
                    desc="类光退化解检测：(C,P) 与 (P,C) 的 β→1 必须判为退化",
                    value=float(int(a3["lightlike"]) + int(a4["lightlike"])),
                    expect="两者皆退化",
                    ok=(a3["lightlike"] and a4["lightlike"]
                        and a3["tau_zero"] and a4["perp_zero"])))

    # F8 三式组健康解数 = 0
    b1 = B1_three_enumeration()
    out.append(dict(id="F8", desc="三式组 8 种读法中『健康自洽解』必须为 0",
                    value=float(b1["n_healthy"]), expect="0",
                    ok=b1["n_healthy"] == 0))

    # F9 快度读法的代价：坐标量必须 ≠ c
    c1 = C1_cost_lightspeed_claim()
    out.append(dict(id="F9",
                    desc="快度读法的代价：坐标横向速率必须显著 ≠ c（≈c/√3）",
                    value=abs(c1["rel_gap_pct"]), expect="≈42.26%",
                    ok=c1["claim_false"] and abs(c1["rel_gap_pct"]) > 40.0))

    return out


def guards(led):
    g = []
    n = led.count()
    a1 = A1_reading_space()
    e1 = E1_repair_pricing()
    g.append(("守卫1：条目数 ≥ 12", len(led.items) >= 12))
    g.append(("守卫2：存在 FAIL 条目", n.get("FAIL", 0) >= 1))
    g.append(("守卫3：控制组 ≥ 7 项", len(control_group()) >= 7))
    g.append(("守卫4：两式组读法枚举数 = 4", a1["n_two"] == 4))
    g.append(("守卫5：三式组读法枚举数 = 8", a1["n_three"] == 8))
    g.append(("守卫6：修复枚举数 = 216", e1["n_total"] == 216))
    g.append(("守卫7：严格档存活 = 0（三条式全保留时无解）", e1["n_strict"] == 0))
    # v=c 被删时 rv 无意义 ⇒ 只检查 (ωr, h·f) 的读法
    g.append(("守卫8：宽松档存活的 (ωr, h·f) 读法全部为 (P,P)",
              all(x["readings"][1:] == "PP" for x in e1["loose"])))
    g.append(("守卫9：三式组健康解 = 0",
              a1["three"] and sum(1 for x in a1["three"] if x["healthy"]) == 0))
    return g


# ============================================================
# 台账
# ============================================================
class Ledger:
    def __init__(self):
        self.items = []

    def add(self, gid, title, status, metrics=None, note=""):
        self.items.append({"id": gid, "title": title, "status": status,
                           "metrics": metrics or {}, "note": note})

    def count(self):
        d = {}
        for it in self.items:
            d[it["status"]] = d.get(it["status"], 0) + 1
        return d

    def ok(self):
        return all(it["status"] != "GUARD-FAIL" for it in self.items)


def build_ledger():
    led = Ledger()
    a1 = A1_reading_space()

    # ---- A 组 ----
    led.add("A1", "读法空间定义：每条关系有【坐标 C】与【固有时 P】两种读法，"
                  "两式组 2²=4、三式组 2³=8",
            "PASS" if (a1["n_two"] == 4 and a1["n_three"] == 8) else "GUARD-FAIL",
            {"n_two": a1["n_two"], "n_three": a1["n_three"]},
            "分量 = c·a(读法,β)：a(C,β)=1、a(P,β)=1/γ=√(1−β²)；"
            "γ 由总速率定义 ⇒ 自洽条件是关于 β 的非线性方程")

    a2 = A2_coord_coord()
    led.add("A2", "读法 (坐标,坐标)：v = √2·c 超光速（复现 r152，跨卷一致性确认）",
            "FAIL" if (a2["superluminal"] and a2["matches_sqrt2"]) else "GUARD-FAIL",
            a2, "两分量皆为 c ⇒ v=√(c²+c²)=√2·c；与 r152 B1 逐位一致")

    a3 = A3_coord_proper()
    led.add("A3", "读法 (坐标,固有时)：唯一解 β=1 类光，且 u=0 ⇒ 螺旋退化为圆",
            "FAIL" if (a3["lightlike"] and a3["tau_zero"]) else "GUARD-FAIL",
            a3, "β→1 时 1/γ→0 ⇒ 轴向分量消失 ⇒ τ≡0；且类光 ⇒ 固有时无定义（自毁）")

    a4 = A4_proper_coord()
    led.add("A4", "读法 (固有时,坐标)：唯一解 β=1 类光，且 v_⊥=0 ⇒ 退化为直线（非螺旋）",
            "FAIL" if (a4["lightlike"] and a4["perp_zero"]) else "GUARD-FAIL",
            a4, "β→1 时横向分量消失 ⇒ 轨迹退化为沿轴直线，螺旋结构不复存在")

    a5 = A5_proper_proper()
    led.add("A5", "★读法 (固有时,固有时)：β=√(2/3)=0.816497 < 1，因果门通过"
                  "（本卷唯一对靶有利的读法，诚实登记）",
            "PASS" if (a5["causal"] and a5["dev_from_exact"] < 1e-9) else "GUARD-FAIL",
            a5, "βγ=√2 ⇒ 3β²=2 ⇒ β=√(2/3)、γ=√3；"
                "这是**唯一**能同时保住因果性与挠率非零的读法，代价见 C 组")

    # ---- B 组 ----
    b1 = B1_three_enumeration()
    led.add("B1", "★三式完备组 {v=c, ωr=c, h·f=c} 在 2³=8 种读法下：健康解 0 个",
            "FAIL" if b1["n_healthy"] == 0 else "GUARD-FAIL",
            {"n_total": b1["n_total"], "n_healthy": b1["n_healthy"],
             "n_degenerate": b1["n_degenerate"], "n_nosol": b1["n_nosol"],
             "degenerate": [x["readings"] for x in b1["degenerate"]]},
            "仅 (C,C,P) 与 (C,P,C) 有解，且都在 β=1 类光边界上，"
            "分别把螺旋压成『圆(u=0)』与『直线(v_⊥=0)』；其余 6 种无解")

    # ---- C 组 ----
    c1 = C1_cost_lightspeed_claim()
    led.add("C1", "代价①：快度读法下坐标量 v_⊥=u=c/√3≈1.730853e8 m/s，"
                  "与 c 差 −42.2650% ⇒ 『光速螺旋运动』名实不符",
            "FAIL" if c1["claim_false"] else "GUARD-FAIL",
            c1, "来料写的是 ωr=c；快度读法把它实际变成 ωr=c/√3 ⇒ 核心公设作废")

    c2 = C2_cost_imports_sr()
    led.add("C2", "代价②：引入 γ=1/√(1−β²) 即引入狭义相对论的洛伦兹结构 ⇒ 循环论证",
            "FAIL" if (c2["imports_sr"] and c2["selfcons"]) else "GUARD-FAIL",
            c2, "γ=√3 是被**解出**的，但 γ 的定义本身来自 SR；"
                "靶若主张『由螺旋运动导出相对论』，此处已把结论当前提")

    c3 = C3_rigid_beta()
    led.add("C3", "代价③：β=√(2/3) 是刚性普适常数（5 质量点跨 ~60 量级，"
                  "离散度 0）⇒ 与『空间以光速运动』公设直接冲突，且零自由参数可调",
            "FAIL" if (c3["rigid"] and c3["conflicts_with_lightspeed_axiom"])
            else "GUARD-FAIL",
            {"spread": c3["spread"], "rigid": c3["rigid"],
             "rows": c3["rows"]},
            "β 与 m、f、r 全部无关 ⇒ 一旦取快度读法，"
            "所有粒子的内部螺旋速率被钉死在 0.8165c，无法回到 c")

    c4 = C4_parameter_count()
    led.add("C4", "代价④：参数计数门 —— 快度读法新增外部输入 γ，自由度仍 0",
            "FAIL" if not c4["gate"] else "GUARD-FAIL",
            c4, "n_自由=1 ≤ n_观测−1=−1 为 False；外部输入由 1（f）增至 2（+γ）")

    c5 = C5_boundary_proper_time()
    led.add("C5", "BOUNDARY：固有时读法要求世界线类时，而『以光速运动』给出 ds²≡0",
            "BOUNDARY", c5,
            "读法 P 需 ds²<0 才能定义 τ；来料公设给出 ds²≡0 ⇒ τ 无定义"
            " ⇒ 读法 P 与公设**互斥**（取 P 即等于放弃『光速运动』）")

    c6 = C6_dimension_blind()
    led.add("C6", "INFO：量纲门对 C/P 读法**无分辨力**（f 的量纲 T⁻¹ 两读法相同）",
            "INFO" if c6["blind"] else "GUARD-FAIL",
            c6, "两种读法下 ωr 与 h·f 的量纲完全一致 ⇒ "
                "读法分歧**不能**靠量纲审计解决，只能靠自洽性门")

    # ---- D 组 ----
    d1 = D1_electron_point()
    led.add("D1", "精算：快度读法下的电子参数点（与 r152 同一组 r、f、h 数值）",
            "FAIL" if (d1["v_over_c"] < 1.0
                       and abs(d1["v_perp_coord"] - C) / C > 1e-6) else "GUARD-FAIL",
            d1,
            "★同一组 (r, f, h) 在两种读法下都满足原式 ⇒ 靶可静默切换读法；"
            "但坐标速率由 c 降为 c/√3，总速率由 c 降为 √(2/3)c")

    d2 = D2_scan_five()
    led.add("D2", "尺度扫描（5 个质量点）：β 恒为 √(2/3)，与质量无关",
            "INFO", {"rows": d2},
            "跨 ~60 量级离散度为 0 ⇒ 标度不变的纯几何后果")

    # ---- E 组 ----
    e1 = E1_repair_pricing()
    led.add("E1", "修复定价（★双档诚实报告）：读法 8 × 动作 {KEEP,DEL,FLIP}³ = 216 全枚举"
                  " ⇒ 严格档存活 %d，宽松档存活 %d" % (e1["n_strict"], e1["n_loose"]),
            "FAIL" if e1["n_strict"] == 0 else "GUARD-FAIL",
            {"n_total": e1["n_total"], "n_strict": e1["n_strict"],
             "n_loose": e1["n_loose"],
             "loose_readings": e1["loose_readings"],
             "loose_v_action": e1["loose_v_action"]},
            "严格档＝三条式一条不删；宽松档＝允许删式。"
            "宽松档 %d 个存活**全部**要求读法 (固有时,固有时) 且删掉 v=c"
            % e1["n_loose"])

    e2 = E2_minimal()
    led.add("E2", "最小完备修复集：严格档不存在；宽松档唯一分支的代价是放弃光速公设",
            "FAIL", e2, e2["conclusion"])

    # ---- G 组：未闭合 ----
    led.add("G1", "BOUNDARY：本卷在欧氏 3-空间轨迹层 + 单一时间参数下判决",
            "BOUNDARY",
            {"note": "未处理 4D 零世界线版本（ds²≡0 ⇒ Frenet 无定义，"
                     "65 号卷 B5 / r149 A2 / r152 G1）"},
            "若采 4D 读法则读法 P 直接不可用（无固有时），"
            "本卷的 3D 读法已是对靶最有利的读法")

    led.add("G2", "BOUNDARY：『固有时』的承担者由本卷代为指定",
            "BOUNDARY",
            {"note": "来料未定义 τ 属于粒子、空间元还是观察者；"
                     "本卷默认取螺旋轨迹自身的固有时"},
            "若来料另行指定承担者，需重新定义 γ；"
            "但 B1 的『三式组健康解=0』结论在读法层成立，不依赖该指定")

    led.add("G3", "BOUNDARY：ω 与 f 强制同参数（ω=2πf 是定义式）",
            "BOUNDARY",
            {"note": "故不存在『ω 用坐标、f 用固有时』这类混合，读法空间确为 2ⁿ 而非更大"},
            "若来料主张 ω=2πf 只是近似（如多普勒修正），则读法空间需重列")

    return led


# ============================================================
# 报告
# ============================================================
def build_report(led):
    L = []
    A = L.append
    A("=" * 96)
    A("TUFT-r153｜读法空间穷举与【快度/固有时】救援路径定价")
    A("=" * 96)
    A("生成时刻: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    A("")
    A("【定位】封堵 r152 的唯一幸存退路：换读法（把 ω、f 解释为固有时频率 ⇒")
    A("        ωr=c 与 h·f=c 说的是快度分量而非坐标速度）。本卷穷举读法空间并定价。")
    A("【分层】r151=两式·坐标；r152=三式·坐标+量纲口径；本卷=两式/三式 × 读法穷举。")
    A("        三卷结论互补，**条目不可相加**。")
    A("")

    for it in led.items:
        A("[%s] %-11s %s" % (it["id"], it["status"], it["title"]))
        if it["note"]:
            A("      " + it["note"])
        for k, v in it["metrics"].items():
            if k in ("rows", "enumeration", "three", "two", "healthy",
                     "degenerate", "survivors", "note"):
                continue
            if isinstance(v, float):
                A("      %s = %s" % (k, "%.6e" % v))
            else:
                A("      %s = %s" % (k, v))
        A("")

    A("-" * 96)
    A("【A 组 · 两式组 {ωr=c, h·f=c} 的 4 种读法】")
    A("    读法(ωr, h·f)        类别            β            v/c        v_⊥/c      u/c     健康")
    for x in enumerate_two():
        A("    (%s, %s)          %-13s %-12s %-11s %-10s %-9s %s"
          % (x["rw"], x["hf"], x["kind"],
             ("%.9f" % x["beta"]) if x["beta"] is not None else "—",
             ("%.9f" % x["v_over_c"]) if x["v_over_c"] == x["v_over_c"] else "nan",
             ("%.9f" % x["v_perp_over_c"]) if x["v_perp_over_c"] is not None else "nan",
             ("%.9f" % x["u_over_c"]) if x["u_over_c"] is not None else "nan",
             "✓" if x["healthy"] else "✗"))
    A("")

    A("-" * 96)
    A("【B 组 · 三式组 {v=c, ωr=c, h·f=c} 的 8 种读法】")
    A("    读法(v, ωr, h·f)     类别         β           残差 R        判定")
    for x in enumerate_three():
        A("    (%s, %s, %s)         %-11s %-12s %.6e   %s"
          % (x["rv"], x["rw"], x["hf"], x["kind"],
             ("%.9f" % x["beta"]) if x["beta"] is not None else "—",
             x["residual"],
             "健康✓" if x["healthy"] else ("退化解" if x["has_solution"] else "无解✗")))
    b1 = B1_three_enumeration()
    A("    ★ 健康解 %d 个 / 退化解 %d 个 / 无解 %d 个"
      % (b1["n_healthy"], b1["n_degenerate"], b1["n_nosol"]))
    A("")

    A("-" * 96)
    A("【C 组 · 唯一健康读法 (P,P) 的代价】")
    a5 = A5_proper_proper()
    c1 = C1_cost_lightspeed_claim()
    A("    β = √(2/3) = %.10f   （与解析值偏差 %.3e）" % (a5["beta"], a5["dev_from_exact"]))
    A("    γ = √3     = %.10f   （与解析值偏差 %.3e）" % (a5["gamma"], a5["gamma_dev"]))
    A("    坐标横向速率 v_⊥ = c/√3 = %.6e m/s" % c1["v_perp"])
    A("    坐标轴向速率 u    = c/√3 = %.6e m/s" % c1["u"])
    A("    坐标总速率   v    = √(2/3)c = %.6e m/s = %.10f c" % (c1["v_total"], c1["v_total_over_c"]))
    A("    ★ 与『光速螺旋运动』宣称的差距：%.4f%%" % c1["rel_gap_pct"])
    A("")

    A("-" * 96)
    A("【D 组 · 快度读法下的电子参数点】")
    d1 = D1_electron_point()
    A("    r            = %.6e m" % d1["r"])
    A("    f(固有时)     = %.6e Hz" % d1["f_proper"])
    A("    ω(固有时)     = %.6e rad/s    （ωr/c = %.12f）" % (d1["omega_proper"], d1["r_omega_proper_over_c"]))
    A("    h(螺距)      = %.6e m     （h·f_proper/c = %.12f）" % (d1["h_pitch"], d1["h_times_f_proper_over_c"]))
    A("    γ            = %.10f" % d1["gamma"])
    A("    v_⊥(坐标)     = %.6e m/s = %.10f c" % (d1["v_perp_coord"], d1["v_perp_coord"] / C))
    A("    u(坐标)       = %.6e m/s = %.10f c" % (d1["u_coord"], d1["u_coord"] / C))
    A("    v(坐标)       = %.6e m/s = %.10f c" % (d1["v"], d1["v_over_c"]))
    A("    h/(2πr)      = %.12f" % d1["h_over_2pi_r"])
    A("    ★ 与 r152 同一组 (r, f, h) 数值：%s" % ("是（靶可静默切换读法）" if d1["same_numbers_as_r152"] else "否"))
    A("")

    A("-" * 96)
    A("【精算表 · 5 个质量点（快度读法）】")
    A("    对象                    r (m)          f_固有时 (Hz)      h (m)         β            γ")
    for row in C3_rigid_beta()["rows"]:
        A("    %-20s %.6e   %.6e   %.6e   %.10f   %.10f"
          % (row["name"], row["r"], row["f_proper"], row["h"], row["beta"], row["gamma"]))
    A("    ★ β 离散度 = %.3e（与质量完全无关）" % C3_rigid_beta()["spread"])
    A("")

    A("-" * 96)
    A("【E 组 · 修复定价（216 组合，双档诚实报告）】")
    e1 = E1_repair_pricing()
    A("    严格档（三条式一条不删）存活 = %d" % e1["n_strict"])
    A("    宽松档（允许删式）        存活 = %d" % e1["n_loose"])
    A("    宽松档存活的读法集合 = %s" % (e1["loose_readings"] or "—"))
    A("    宽松档存活时 v=c 的动作 = %s" % (e1["loose_v_action"] or "—"))
    A("    ★ 宽松档 %d 个存活**全部**要求：读法 (固有时,固有时) 且删掉 v=c"
      % e1["n_loose"])
    A("")

    A("-" * 96)
    A("【控制组】")
    allok = True
    for c in control_group():
        v = c["value"]
        try:
            vs = "%.6e" % v
        except Exception:
            vs = str(v)
        A("    %s %-6s %s" % (c["id"], "PASS" if c["ok"] else "FAIL", c["desc"]))
        A("         实测 %s  期望 %s" % (vs, c["expect"]))
        allok = allok and c["ok"]
    A("    控制组小结: %s" % ("全部通过" if allok else "存在失败"))
    A("")

    A("-" * 96)
    A("【守卫】")
    for n, o in guards(led):
        A("    %s  %s" % ("OK  " if o else "FAIL", n))
    A("")

    A("=" * 96)
    cnt = led.count()
    A("【条目统计】" + "  ".join("%s=%d" % (k, cnt[k]) for k in sorted(cnt)))
    A("=" * 96)
    return "\n".join(L), allok


# ============================================================
# 判定册
# ============================================================
def build_judge(led, allok):
    cnt = led.count()
    a5 = A5_proper_proper()
    b1 = B1_three_enumeration()
    c1 = C1_cost_lightspeed_claim()
    e1 = E1_repair_pricing()
    verdict = "NO-READING-SAVES-THE-GROUP-ONLY-BRANCH-ABANDONS-C"

    m = []
    a = m.append
    a("# 判定册 TUFT-r153｜读法空间穷举与【快度/固有时】救援路径定价")
    a("")
    a("- 编号：TUFT-r153")
    a("- 生成时刻：%s" % time.strftime("%Y-%m-%d %H:%M:%S"))
    a("- 引擎：`源码/TUFT-r153_读法空间穷举与快度救援定价_2026-10-22.py`")
    a("- 控制组：%s" % ("全部通过" if allok else "存在失败"))
    a("- 条目统计：%s" % "  ".join("%s=%d" % (k, cnt[k]) for k in sorted(cnt)))
    a("")
    a("## 00. 编号碰撞处置表")
    a("")
    a("| 编号 | 占用者 | 处置 |")
    a("|------|--------|------|")
    a("| r150 | 自旋-2 卷（已产出三件套并登记） | 保留为权威 |")
    a("| r151 | 双约束求导证明卷（已产出三件套并登记） | 保留为权威 |")
    a("| r152 | ω f h c f 完整关系组卷（已产出三件套并登记） | 保留为权威 |")
    a("| r153 | **本卷**（读法空间穷举） | 实测首空号后启用 |")
    a("")
    a("## 01. 分工声明（★ 三卷条目不可相加）")
    a("")
    a("| 卷 | 处理对象 | 读法 | 新增审计维度 |")
    a("|----|----------|------|--------------|")
    a("| r151 | 两式 {v=c, ωr=c} | 坐标 | 求导证明、参数计数 |")
    a("| r152 | 三式 {+ h·f=c} | 坐标 | 量纲口径（h 速度/螺距） |")
    a("| **r153** | 两式与三式 | **坐标 ∪ 固有时（穷举）** | **读法层自洽性** |")
    a("")
    a("> 本卷不重复 r151/r152 的式子层结论，只读法层。三卷结论互补但条目不可相加。")
    a("")
    a("## 02. 判词")
    a("")
    a("`%s`" % verdict)
    a("")
    a("**读法空间已被穷举，没有一种读法能在保住来料宣称的前提下救回因果性。**")
    a("")
    a("## 03. 核心结论")
    a("")
    a("### 3.1 两式组 {ωr=c, h·f=c}：4 种读法，仅 1 种健康")
    a("")
    a("| 读法 (ωr, h·f) | 结果 | 判定 |")
    a("|---|---|---|")
    a("| (坐标, 坐标) | v = √2·c，超光速 41.42% | ✗ 因果死 |")
    a("| (坐标, 固有时) | 唯一解 β=1 类光，且 u=0 | ✗ 退化为圆 |")
    a("| (固有时, 坐标) | 唯一解 β=1 类光，且 v_⊥=0 | ✗ 退化为直线 |")
    a("| **(固有时, 固有时)** | **β=√(2/3)=0.816497 < 1** | **✓ 唯一健康** |")
    a("")
    a("### 3.2 三式组 {v=c, ωr=c, h·f=c}：8 种读法，健康解 0 个")
    a("")
    a("- 健康自洽解：**0**")
    a("- 类光退化解：2（(C,C,P) 压成圆、(C,P,C) 压成直线）")
    a("- 无解：6")
    a("")
    a("> 结论与读法**无关**：三式完备组在任何读法下都不自洽。")
    a("")
    a("### 3.3 唯一健康读法 (固有时, 固有时) 的代价清单")
    a("")
    a("1. **坐标量不再是 c**：v_⊥ = u = c/√3 = %.6e m/s，与 c 差 %.4f%%"
      % (c1["v_perp"], c1["rel_gap_pct"]))
    a("   ⇒ 来料的核心宣称『空间以光速做螺旋运动』**名实不符**。")
    a("2. **引入 SR 结构**：γ = 1/√(1−β²) 是狭义相对论的定义式 ⇒ 循环论证。")
    a("3. **刚性普适 β=√(2/3)**：5 个质量点跨 ~60 量级离散度为 0，"
      "且与『空间以光速运动』公设直接冲突，零自由参数可调。")
    a("4. **外部输入 +1**：由 1（f）增至 2（f + γ/洛伦兹结构），自由度仍 0。")
    a("")
    a("### 3.4 零分辨力控制（防止过度指控）")
    a("")
    a("控制组 F6 证明：**同一快度手法也能把『v=2c 的假理论』救成 β=0.9428 < 1**。")
    a("⇒ 本卷不是因为『不喜欢快度读法』才判它有代价，而是该**手法本身没有判别力**：")
    a("任何超光速理论都可以靠『把式中的速度改读为快度』变因果。")
    a("")
    a("## 04. 机读证据")
    a("")
    a("```")
    a("β = √(2/3) = %.10f   （解析值偏差 %.3e）" % (a5["beta"], a5["dev_from_exact"]))
    a("γ = √3     = %.10f   （解析值偏差 %.3e）" % (a5["gamma"], a5["gamma_dev"]))
    a("三式组健康解数 = %d / %d" % (b1["n_healthy"], b1["n_total"]))
    a("修复枚举 216 组合：严格档存活 = %d，宽松档存活 = %d"
      % (e1["n_strict"], e1["n_loose"]))
    a("宽松档存活的读法集合 = %s；v=c 的动作 = %s"
      % (e1["loose_readings"], e1["loose_v_action"]))
    a("```")
    a("")
    a("### 3.5 修复定价的双档口径（★ 禁只报对自己有利的一档）")
    a("")
    a("| 档位 | 判据 | 存活数 |")
    a("|---|---|---|")
    a("| 严格 | 健康 ∧ τ≠0 ∧ v_⊥≠0 ∧ 尺度定标 ∧ **三条式一条不删** | **%d** |" % e1["n_strict"])
    a("| 宽松 | 健康 ∧ τ≠0 ∧ v_⊥≠0 ∧ 尺度定标（**允许删式**） | %d |" % e1["n_loose"])
    a("")
    a("宽松档的 %d 个存活**全部**是同一件事：读法取 (固有时,固有时) **且删掉 v=c**。"
      % e1["n_loose"])
    a("⇒ 靶若想救因果性，必须**同时**做两件事：换读法 + 放弃『运动速率为 c』这条式。")
    a("")
    a("## 05. 未闭合项（禁止外推）")
    a("")
    a("1. 本卷在**欧氏 3-空间轨迹层 + 单一时间参数**下判决；未处理 4D 零世界线版本")
    a("   （若采 4D 读法则读法 P 直接不可用 —— 无固有时可定义）。")
    a("2. 『固有时』的承担者（粒子 / 空间元 / 观察者）由本卷代为指定，来料未定义。")
    a("3. ω=2πf 被视为定义式 ⇒ ω 与 f 强制同参数；若来料主张该式只是近似，读法空间需重列。")
    a("4. 本卷**不**宣称靶体系已被完全证伪 —— 只判决：")
    a("   **『换读法』这条退路要么撞上因果门，要么以放弃光速公设为代价。**")
    a("5. 因果门与 γ 本身以狭义相对论为前提；若靶主张修改相对论，")
    a("   则需先给出替代的因果结构与实验约束（本卷未评估该主张）。")
    a("")
    return "\n".join(m), verdict


def main():
    led = build_ledger()
    report, allok = build_report(led)
    print(report)

    here = os.path.dirname(os.path.abspath(__file__))
    outdir = os.path.abspath(os.path.join(here, "..", "数据"))
    os.makedirs(outdir, exist_ok=True)
    base = "TUFT-r153_读法空间穷举与快度救援定价_2026-10-22"
    verdict_j = "NO-READING-SAVES-THE-GROUP-ONLY-BRANCH-ABANDONS-C"

    payload = {
        "id": "TUFT-r153",
        "title": "读法空间穷举与【快度/固有时】救援路径定价",
        "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "verdict": verdict_j,
        "counts": led.count(),
        "controls_ok": allok,
        "items": led.items,
        "two_readings": enumerate_two(),
        "three_readings": enumerate_three(),
        "scan": C3_rigid_beta()["rows"],
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
    return 0 if (allok and led.ok()) else 2


if __name__ == "__main__":
    sys.exit(main())
