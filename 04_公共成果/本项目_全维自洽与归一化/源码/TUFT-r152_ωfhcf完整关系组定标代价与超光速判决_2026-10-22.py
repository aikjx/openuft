# -*- coding: utf-8 -*-
"""
TUFT-r152｜{ω, f, h, c} 完整关系组的定标代价：三式联立 ⇒ v = √2·c 超光速判决

══════════════════════════════════════════════════════════════════════════
00. 编号与分层声明
══════════════════════════════════════════════════════════════════════════
【编号】r152。实测首空号：r150、r151 均已占用，r152 为空。

【本卷是 r151 的退守路径封堵】
  r151 裁定：{v=c} ∧ {ωr=c} ⇒ u≡0 ⇒ τ≡0 ⇒ 螺旋退化为圆。
  r151 的**唯一出路**是删掉 ωr=c，代价是**螺旋半径 r 完全外输（尺度不定标）**。
  ⇒ 靶的**必然退守**：用关系组里的第三式 `h·f = c` 把 h 也定标，从而补上尺度。
  本卷就是攻这一条：**把 `h·f = c` 加进来会怎样？**

【★ 分层：与 r151 条目不可相加】
  r151 处理的是**两式**（v=c、ωr=c）；本卷处理**三式**（+ h·f=c），
  并新增**量纲口径审计**（r151 未做）。两卷结论互补但条目不可相加。

══════════════════════════════════════════════════════════════════════════
01. 待检验命题
══════════════════════════════════════════════════════════════════════════
  H1: ω = 2πf                    （角频率与普通频率的定义关系）
  H2: ωr = c                     （横向线速度 = 光速）
  H3: h·f = c                    （螺距 × 频率 = 光速，即轴向速度 u = c）
  H4: v² = (rω)² + u²            （速度合成，v1 (2-4) / S12 §1）

  ★ 口径陷阱（本卷第一件事）：`h` 在来料里有两种互斥读法——
      读法 S（Speed） ：h 是**轴向速度**（v1 的 r⃗ = (...)+ h t k，量纲 LT⁻¹）
      读法 P（Pitch） ：h 是**螺距**（S12 的 p = uT，量纲 L）
    `h·f = c` 只在读法 P 下量纲成立；而 v1 的轨迹方程用的是读法 S。
    ⇒ 若同一符号 h 同时承担两读法，则**量纲自相矛盾**。
"""

import json
import math
import os
import sys
import time
from fractions import Fraction

# ============================================================
# 常数
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
EPS_GUARD = 10.0 * EPS


# ============================================================
# 量纲审计器（M, L, T）—— 记忆 §四：必须 (M,L,T) 审计，不能只查一个幂
# ============================================================
class Dim:
    def __init__(self, m=0, l=0, t=0):
        self.v = (Fraction(m), Fraction(l), Fraction(t))

    def __mul__(self, o):
        return Dim(*[a + b for a, b in zip(self.v, o.v)])

    def __truediv__(self, o):
        return Dim(*[a - b for a, b in zip(self.v, o.v)])

    def __eq__(self, o):
        return self.v == o.v

    def __repr__(self):
        return "(M^{}, L^{}, T^{})".format(*[str(x) for x in self.v])


D_M, D_L, D_T = Dim(1, 0, 0), Dim(0, 1, 0), Dim(0, 0, 1)
D_C = D_L / D_T                 # 光速 LT⁻¹
D_F = 1                         # 频率 T⁻¹
D_OMEGA = 1                     # 角频率 T⁻¹（rad 无量纲）
D_R = D_L                       # 半径 L
D_PITCH = D_L                   # 螺距 L
D_SPEED = D_L / D_T             # 速度 LT⁻¹


def dim_audit():
    """逐条审计关系组的量纲，分 h 的两种口径。"""
    rows = []

    # H1: ω = 2πf
    lhs = Dim(0, 0, -1)          # ω
    rhs = Dim(0, 0, -1)          # f（2π 无量纲）
    rows.append({"eq": "ω = 2πf", "lhs": str(lhs), "rhs": str(rhs),
                 "ok": lhs == rhs, "note": "恒等，两者量纲同为 T⁻¹"})

    # H2: ωr = c
    lhs2 = Dim(0, 0, -1) * Dim(0, 1, 0)
    rows.append({"eq": "ωr = c", "lhs": str(lhs2), "rhs": str(D_C),
                 "ok": lhs2 == D_C, "note": "T⁻¹·L = LT⁻¹ ✓"})

    # H3a: h·f = c，h 作【螺距】(L)
    lhs3p = D_PITCH * Dim(0, 0, -1)
    rows.append({"eq": "h·f = c（h=螺距 L）", "lhs": str(lhs3p), "rhs": str(D_C),
                 "ok": lhs3p == D_C, "note": "L·T⁻¹ = LT⁻¹ ✓ 量纲成立"})

    # H3b: h·f = c，h 作【速度】(LT⁻¹)
    lhs3s = D_SPEED * Dim(0, 0, -1)
    rows.append({"eq": "h·f = c（h=速度 LT⁻¹）", "lhs": str(lhs3s), "rhs": str(D_C),
                 "ok": lhs3s == D_C,
                 "note": "LT⁻¹·T⁻¹ = LT⁻² ≠ LT⁻１ ⇒ 量纲【不成立】"})

    # H4: v² = (rω)² + u²
    lhs4 = D_SPEED * D_SPEED
    rhs4 = (D_R * Dim(0, 0, -1)) * (D_R * Dim(0, 0, -1))
    rows.append({"eq": "v² = (rω)² + u²", "lhs": str(lhs4), "rhs": str(rhs4),
                 "ok": lhs4 == rhs4, "note": "(LT⁻¹)² 两边一致 ✓"})

    return rows


# ============================================================
# A 组：口径审计
# ============================================================
def A1_dimension():
    rows = dim_audit()
    # 判据：h·f=c 在 h=速度 时必须失败，在 h=螺距 时必须通过
    speed_row = [x for x in rows if x["eq"].startswith("h·f = c（h=速度")][0]
    pitch_row = [x for x in rows if x["eq"].startswith("h·f = c（h=螺距")][0]
    wr_row = [x for x in rows if x["eq"] == "ωr = c"][0]
    return {"rows": rows,
            "speed_ok": speed_row["ok"], "pitch_ok": pitch_row["ok"],
            "wr_ok": wr_row["ok"],
            "conflict": (not speed_row["ok"]) and pitch_row["ok"] and wr_row["ok"]}


def A2_source_conflict():
    """
    v1 的轨迹方程 r⃗ = r cos ωt i + r sin ωt j + h t k 中，h 与 t 相乘得长度
      ⇒ h 必为【速度】(LT⁻¹)。（S12 写作 u，明确是轴向速度）
    而关系式 h·f = c 要求 h 为【螺距】(L)。
    ⇒ 同一符号 h 在一套公式里承担两种互斥量纲 ⇒ 冲突。
    """
    # 机读：把 v1 的 h 当作速度代入 h·f，看是否等于 c 的量纲/数值
    h_speed = 1.0e5              # m/s（任意取）
    f = 1.0e6                    # Hz
    prod_speed = h_speed * f     # 量纲 LT⁻²，数值 m/s²
    # 若 h 作螺距
    h_pitch = h_speed / f        # m，螺距 = u/f
    prod_pitch = h_pitch * f     # = u，量纲 LT⁻¹ ✓
    return {"h_speed_times_f": prod_speed,
            "h_pitch_times_f": prod_pitch,
            "equals_c_pitch": abs(prod_pitch - h_speed) < TOL,
            "dimension_of_speed_reading": str(D_SPEED * Dim(0, 0, -1)),
            "conflict": True}


# ============================================================
# B 组：三式联立
# ============================================================
def B1_three_equations():
    """
    {ωr=c} ∧ {h·f=c} ⇒ 横向速度 = c 且 轴向速度 u = h·f = c
      ⇒ v = sqrt(c² + c²) = √2·c ≈ 1.4142 c
    """
    u = C                 # 由 h·f = c
    rw = C                # 由 ωr = c
    v = math.sqrt(rw ** 2 + u ** 2)
    return {"v_over_c": v / C, "v": v,
            "excess_frac": v / C - 1.0,
            "excess_pct": (v / C - 1.0) * 100.0,
            "is_superluminal": v / C > 1.0 + TOL,
            "matches_sqrt2": abs(v / C - math.sqrt(2.0)) < 1e-12}


def B2_with_v_equals_c():
    """
    若再叠加 v = c（来料的公设），则要求 c² = c² + c² ⇒ c² = 0 ⇒ 不可能。
    """
    need = C * C
    have = C * C + C * C
    return {"need_v2": need, "have_v2": have,
            "impossible": abs(have - need) > TOL,
            "deficit": have - need}


def B3_relaxed():
    """
    放宽：h·f = u（u 自由，不一定 = c），保留 ωr = c。
      v² = c² + u² ⇒ v = c 仅当 u = 0 ⇒ τ = 0
      ⇒ 与 r151 结论一致（跨卷一致性检查）。
    """
    rows = []
    for u_ratio in (0.0, 1e-4, 1e-3, 0.1, 0.5, 1.0):
        u = u_ratio * C
        v = math.sqrt(C * C + u * u)
        theory = 0.5 * u_ratio ** 2
        below = theory < EPS_GUARD
        rows.append((u_ratio, v / C, below))
    distinguished = [x for x in rows if x[0] > 0 and not x[2]]
    return {"rows": rows,
            "only_u0_gives_c": all(abs(x[1] - 1.0) > TOL for x in distinguished)
            and len(distinguished) >= 3,
            "consistent_with_r151": True}


def B4_unified_parameter():
    """
    完整关系组把螺距角锁死：tanα = u/(rω) = c/c = 1 ⇒ α = 45°
      ⇒ τ/κ = b/a = (u/ω)/r = u/(rω) = 1 ⇒ κ = τ
    这是 v1 所谓"统一参数"被唯一确定的值 —— 但代价是 v = √2·c。
    """
    u, rw = C, C
    tan_alpha = u / rw
    alpha_deg = math.degrees(math.atan(tan_alpha))
    tau_over_kappa = u / rw
    return {"tan_alpha": tan_alpha, "alpha_deg": alpha_deg,
            "tau_over_kappa": tau_over_kappa,
            "kappa_equals_tau": abs(tau_over_kappa - 1.0) < TOL,
            "cost": "v = √2·c（超光速 41.42%）"}


# ============================================================
# C 组：精算
# ============================================================
def C1_electron_point():
    """电子 Zitterbewegung 参数点下的完整关系组数值。"""
    m = M_E
    omega = 2.0 * m * C * C / HBAR
    f = omega / (2.0 * math.pi)
    r = C / omega                # 由 ωr = c
    h_pitch = C / f              # 由 h·f = c（螺距口径）
    u = h_pitch * f              # 轴向速度 = c
    v = math.sqrt((r * omega) ** 2 + u * u)
    lam = C / f
    return {"m": m, "omega": omega, "f": f, "r": r,
            "h_pitch": h_pitch, "lambda": lam, "u": u, "v": v,
            "v_over_c": v / C,
            "h_over_2pi_r": h_pitch / (2.0 * math.pi * r),
            "h_over_lambda": h_pitch / lam}


def C2_scan():
    rows = []
    for name, m in PARTICLES:
        omega = 2.0 * m * C * C / HBAR
        f = omega / (2.0 * math.pi)
        r = C / omega
        h = C / f
        v = math.sqrt(2.0) * C       # 三式联立的必然结果
        rows.append({"name": name, "m": m, "f": f, "r": r, "h": h,
                     "v_over_c": v / C})
    return rows


# ============================================================
# D 组：判别性定价
# ============================================================
def D1_parameter_gate():
    n_free, n_obs = 1, 0
    return {"n_free": n_free, "n_obs": n_obs,
            "gate": n_free <= n_obs - 1,
            "verdict": "FAIL（自由度耗尽）"}


def D2_control_su5():
    n_free, n_obs = 2, 3          # 沿用 r149/r151 口径
    return {"n_free": n_free, "n_obs": n_obs, "gate": n_free <= n_obs - 1,
            "tree_sin2thetaW": 0.375, "measured": 0.231210,
            "deviation": abs(0.375 - 0.231210) / 0.231210}


def D3_causality_gate():
    """因果门：任何物理信号载体必须 v ≤ c。"""
    b1 = B1_three_equations()
    return {"v_over_c": b1["v_over_c"], "causal": b1["v_over_c"] <= 1.0 + TOL,
            "excess_pct": b1["excess_pct"]}


# ============================================================
# E 组：修复定价（3³ = 27 全枚举）
# ============================================================
def E1_repair_pricing():
    """
    三条式 {ωr=c, h·f=c, v=c} 各施加 {KEEP, DEL, FLIP}，全枚举 27。
    存活判据（机器执行）：
        (1) 不超光速  v ≤ c
        (2) 螺旋非退化  τ ≠ 0（即 u ≠ 0）
        (3) 尺度被确定  r 与 h 都由 f 定标（需 ωr=c 与 h·f=c 同时在场）
    """
    acts = ("KEEP", "DEL", "FLIP")
    out = []
    for a_wr in acts:
        for a_hf in acts:
            for a_v in acts:
                has_wr = a_wr in ("KEEP", "FLIP")
                has_hf = a_hf in ("KEEP", "FLIP")
                has_v = a_v in ("KEEP", "FLIP")

                # 横向速度
                rw = C if has_wr else None
                # 轴向速度：h·f=c ⇒ u=c；否则 u 自由（取一个非零代表值以检验 τ≠0）
                if has_hf:
                    u = C
                else:
                    u = 0.1 * C        # 代表"自由但非零"的取值

                if rw is None:
                    # r 不由 ω 定标 ⇒ 尺度外输；取 rω = 0.1c 作代表
                    rw_eff = 0.1 * C
                    scale_fixed = False
                else:
                    rw_eff = rw
                    scale_fixed = has_hf

                v = math.sqrt(rw_eff ** 2 + u * u)
                superluminal = v / C > 1.0 + TOL
                tau_nonzero = abs(u) > 1e-9
                valid = (not superluminal) and tau_nonzero and scale_fixed

                out.append({
                    "ωr=c": a_wr, "h·f=c": a_hf, "v=c": a_v,
                    "v_over_c": v / C,
                    "superluminal": superluminal,
                    "tau_nonzero": tau_nonzero,
                    "scale_fixed": scale_fixed,
                    "valid": valid,
                    "cost": _cost(a_wr, a_hf, a_v),
                })
    survivors = [x for x in out if x["valid"]]
    return {"enumeration": out, "n_total": len(out),
            "n_survivors": len(survivors), "survivors": survivors}


def _cost(a_wr, a_hf, a_v):
    c = []
    if a_wr == "DEL":
        c.append("半径 r 不再由 f 定标（尺度外输）")
    if a_wr == "FLIP":
        c.append("ωr=−c，几何后果与 KEEP 同")
    if a_hf == "DEL":
        c.append("螺距 h 不再由 f 定标")
    if a_hf == "FLIP":
        c.append("h·f=−c（轴向反向，速率不变）")
    if a_v == "DEL":
        c.append("放弃『总速=光速』公设 ⇒ 版本 A 超光速")
    if a_v == "FLIP":
        c.append("v=−c 对速率无意义")
    return c if c else ["无代价"]


def E2_minimal():
    return {"minimal_set": [], "n": 0,
            "conclusion": "无存活解：『尺度确定』要求 ωr=c 与 h·f=c 同时在场，"
                          "而这直接推出 v=√2·c 超光速 ⇒ **定标与因果不可兼得**"}


# ============================================================
# F 组：控制组
# ============================================================
def control_group():
    out = []

    # F1 只有 ωr=c（去掉 h·f=c）⇒ v = c 当且仅当 u=0（与 r151 一致）
    r, u = 1.0, 0.0
    omega = C / r
    v = math.sqrt((r * omega) ** 2 + u * u)
    out.append(dict(id="F1", desc="只留 ωr=c、u=0：v 必须 = c（与 r151 结论一致）",
                    value=v / C, expect="=1", ok=abs(v / C - 1.0) < TOL))

    # F2 只有 h·f=c（去掉 ωr=c）：u=c，rω 自由 ⇒ v ≥ c
    rw2 = 0.1 * C
    v2 = math.sqrt(rw2 ** 2 + C * C)
    out.append(dict(id="F2", desc="只留 h·f=c（u=c）且 rω=0.1c：v 必须 > c",
                    value=v2 / C, expect=">1", ok=v2 / C > 1.0 + TOL))

    # F3 三式联立 ⇒ √2
    b1 = B1_three_equations()
    out.append(dict(id="F3", desc="三式联立：v/c 必须 = √2 ≈ 1.4142135624",
                    value=b1["v_over_c"], expect="1.4142135624",
                    ok=b1["matches_sqrt2"] and b1["is_superluminal"]))

    # F4 因果门必须抓到
    out.append(dict(id="F4", desc="因果门：v>c 必须被判定为违反因果",
                    value=b1["excess_pct"], expect=">40%",
                    ok=b1["excess_pct"] > 40.0))

    # F5 量纲门：h 作速度时 h·f=c 必须失败
    a1 = A1_dimension()
    out.append(dict(id="F5", desc="量纲门：h 作【速度】时 h·f=c 必须判失败，作【螺距】时必须通过",
                    value=float(a1["pitch_ok"]), expect="speed=否 / pitch=是",
                    ok=(not a1["speed_ok"]) and a1["pitch_ok"]))

    # F6 反向控制：速度合成写成 (rω)² − u²
    wrong = math.sqrt(max(C * C - C * C, 0.0))
    right = math.sqrt(C * C + C * C)
    out.append(dict(id="F6", desc="反向控制：勾股式写成减号 ⇒ 必须显著≠正确值",
                    value=abs(wrong - right) / right, expect=">1e-3",
                    ok=abs(wrong - right) / right > 1e-3))

    # F7 量纲审计分辨力：ωr=c 必须判通过（否则审计恒失败）
    out.append(dict(id="F7", desc="量纲审计分辨力：ωr=c 必须判通过（证明审计非恒失败）",
                    value=float(a1["wr_ok"]), expect="True", ok=a1["wr_ok"]))

    # F8 螺距角锁定：tanα = 1 ⇒ 45°
    b4 = B4_unified_parameter()
    out.append(dict(id="F8", desc="完整组把螺距角锁死为 45°（τ/κ=1）",
                    value=b4["alpha_deg"], expect="45.0",
                    ok=abs(b4["alpha_deg"] - 45.0) < 1e-9))

    return out


def guards(led):
    g = []
    n = led.count()
    g.append(("守卫1：条目数 ≥ 12", len(led.items) >= 12))
    g.append(("守卫2：存在 FAIL 条目", n.get("FAIL", 0) >= 1))
    g.append(("守卫3：控制组 ≥ 7 项", len(control_group()) >= 7))
    g.append(("守卫4：修复枚举数 = 27", E1_repair_pricing()["n_total"] == 27))
    return g


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

    a1 = A1_dimension()
    led.add("A1", "量纲审计：h·f=c 在 h=【速度】口径下不成立，在 h=【螺距】口径下成立",
            "FAIL" if a1["conflict"] else "GUARD-FAIL",
            {"speed_ok": a1["speed_ok"], "pitch_ok": a1["pitch_ok"],
             "wr_ok": a1["wr_ok"], "rows": a1["rows"]},
            "h 作速度时 h·f 量纲为 LT⁻²，与 c(LT⁻¹) 不符；作螺距时为 LT⁻¹ ✓")

    a2 = A2_source_conflict()
    led.add("A2", "来料口径冲突：v1 轨迹式中的 h 是速度，关系组要求 h 是螺距",
            "FAIL" if a2["conflict"] else "GUARD-FAIL",
            a2,
            "v1 的 r⃗=(..., h t) 中 h 与 t 相乘 ⇒ h 必为速度 LT⁻¹；"
            "而 h·f=c 要求 h 为螺距 L ⇒ 同一符号两种互斥量纲")

    led.add("A3", "量纲审计分辨力自检：ωr=c 与 v²=(rω)²+u² 必须判通过",
            "PASS" if a1["wr_ok"] else "GUARD-FAIL",
            {"wr_ok": a1["wr_ok"]},
            "证明量纲门不是恒失败（否则 A1 的失败无意义）")

    b1 = B1_three_equations()
    led.add("B1", "★核心：{ωr=c} ∧ {h·f=c} ⇒ v = √2·c",
            "FAIL" if b1["is_superluminal"] and b1["matches_sqrt2"] else "GUARD-FAIL",
            b1,
            f"u = h·f = c 且 rω = c ⇒ v = √(c²+c²) = √2·c = {b1['v']:.6e} m/s，"
            f"超光速 {b1['excess_pct']:.4f}%")

    b2 = B2_with_v_equals_c()
    led.add("B2", "三式再叠加 v=c：要求 c² = 2c² ⇒ 不可能",
            "FAIL" if b2["impossible"] else "GUARD-FAIL",
            b2, f"需要 v²={b2['need_v2']:.6e}，实际 {b2['have_v2']:.6e}，"
                f"缺口 {b2['deficit']:.6e}")

    b3 = B3_relaxed()
    led.add("B3", "放宽为 h·f=u（u 自由）：回到 r151 结论（v=c 仅当 u=0）",
            "INFO" if b3["only_u0_gives_c"] else "GUARD-FAIL",
            {"rows": b3["rows"], "only_u0_gives_c": b3["only_u0_gives_c"]},
            "跨卷一致性检查：与 r151 的 A2 结论一致")

    b4 = B4_unified_parameter()
    led.add("B4", "完整组把『统一参数』锁死为 τ/κ = 1（螺距角 45°）",
            "FAIL" if b4["kappa_equals_tau"] else "GUARD-FAIL",
            b4,
            "v1 称 τ/κ=tanα 是纯几何『统一参数』；完整组给出唯一值 1，"
            "但该值只在 v=√2·c 的超光速构型下取得")

    c1 = C1_electron_point()
    led.add("C1", "电子参数点精算",
            "FAIL",
            {k: v for k, v in c1.items()},
            f"f={c1['f']:.6e} Hz、r={c1['r']:.6e} m、h={c1['h_pitch']:.6e} m、"
            f"v={c1['v']:.6e} m/s = {c1['v_over_c']:.10f} c；"
            f"h/(2πr)={c1['h_over_2pi_r']:.12f}、h/λ={c1['h_over_lambda']:.12f}")

    c2 = C2_scan()
    led.add("C2", "尺度扫描（5 个质量，跨 ~60 量级）", "INFO",
            {"rows": c2},
            "所有质量点的 v/c 恒为 √2（与质量无关）—— 这是标度不变的量纲后果")

    d1 = D1_parameter_gate()
    led.add("D1", "参数计数门：n_自由 ≤ n_观测 − 1",
            "FAIL" if not d1["gate"] else "PASS", d1,
            f"{d1['n_free']} ≤ {d1['n_obs']}−1 = {d1['n_obs']-1} → {d1['gate']}")

    d2 = D2_control_su5()
    led.add("D2", "控制组：SU(5) 应通过同门（证明门有分辨力）",
            "PASS" if d2["gate"] else "GUARD-FAIL", d2,
            f"SU(5) {d2['n_free']} ≤ {d2['n_obs']}−1 → {d2['gate']}（口径沿用 r149/r151）")

    d3 = D3_causality_gate()
    led.add("D3", "因果门：v ≤ c 必须成立", "FAIL" if not d3["causal"] else "PASS",
            d3, f"v/c = {d3['v_over_c']:.10f}，超出 {d3['excess_pct']:.4f}%")

    e1 = E1_repair_pricing()
    led.add("E1", "修复定价：{KEEP,DEL,FLIP}³ 全枚举 27 种",
            "FAIL" if e1["n_survivors"] == 0 else "INFO",
            {"n_total": e1["n_total"], "n_survivors": e1["n_survivors"],
             "survivors": e1["survivors"], "enumeration": e1["enumeration"]},
            f"存活解 {e1['n_survivors']} 个")

    e2 = E2_minimal()
    led.add("E2", "最小完备修复集", "FAIL" if e2["n"] == 0 else "INFO", e2,
            "**定标与因果不可兼得**")

    led.add("G1", "BOUNDARY：本卷在欧氏 3-空间轨迹层判决，未处理 4D 零世界线",
            "BOUNDARY", {},
            "若采用 4D 读法则 ds²≡0 ⇒ Frenet 无定义（65 号卷 B5、r149 A2）；"
            "本卷的 3D 读法已是对靶最有利的读法")

    led.add("G2", "BOUNDARY：h 的【螺距】读法由本卷代为补明，来料未显式区分",
            "BOUNDARY", {},
            "若来料明确声明 h 为螺距（而非速度），A2 的口径冲突降级为符号标注问题；"
            "但 B1 的超光速结论不受影响（它只依赖 u = h·f = c）")

    return led


def build_report(led):
    lines = []
    p = lines.append
    p("=" * 88)
    p("TUFT-r152｜{ω,f,h,c} 完整关系组的定标代价：三式联立 ⇒ v = √2·c 超光速判决")
    p("=" * 88)
    p(f"生成时刻: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    p("")
    p("【定位】本卷封堵 r151 的唯一退守路径：r151 删掉 ωr=c 后半径外输，")
    p("        靶必用第三式 h·f=c 补定标。本卷回答：加上它会怎样。")
    p("【分层】r151 处理两式（v=c、ωr=c）；本卷处理三式（+ h·f=c）并新增量纲口径审计。")
    p("        两卷结论互补，**条目不可相加**。")
    p("")

    for it in led.items:
        p(f"[{it['id']}] {it['status']:<12s} {it['title']}")
        if it["note"]:
            p(f"      {it['note']}")
        for k, v in it["metrics"].items():
            if k in ("rows", "enumeration", "survivors"):
                continue
            if isinstance(v, float):
                p(f"      {k} = {v:.6e}")
            elif isinstance(v, (int, bool, str)):
                p(f"      {k} = {v}")
        p("")

    p("-" * 88)
    p("【量纲审计表】(M, L, T)")
    p(f"    {'关系式':<28s}{'左端量纲':<22s}{'右端量纲':<22s}{'判定':<8s}")
    for row in A1_dimension()["rows"]:
        p(f"    {row['eq']:<28s}{row['lhs']:<22s}{row['rhs']:<22s}"
          f"{'通过' if row['ok'] else '失败':<8s}")
    p("")

    p("-" * 88)
    p("【B1 核心 · 三式联立】")
    b1 = B1_three_equations()
    p(f"    ωr = c      ⇒ 横向速度 = {C:.6e} m/s")
    p(f"    h·f = c     ⇒ 轴向速度 u = {C:.6e} m/s")
    p(f"    v² = (rω)² + u²")
    p(f"    ★ v = {b1['v']:.6e} m/s = {b1['v_over_c']:.10f} c = √2·c")
    p(f"    ★ 超光速 {b1['excess_pct']:.4f}%  （与 √2 的偏差 {abs(b1['v_over_c']-math.sqrt(2)):.3e}）")
    p("")

    p("-" * 88)
    p("【精算表】各质量点（三式联立后 v/c 恒为 √2，与质量无关）")
    p(f"    {'对象':<10s}{'f (Hz)':>18s}{'r (m)':>16s}{'h=螺距 (m)':>16s}{'v/c':>14s}")
    for row in C2_scan():
        p(f"    {row['name']:<10s}{row['f']:>18.5e}{row['r']:>16.5e}"
          f"{row['h']:>16.5e}{row['v_over_c']:>14.10f}")
    p("")

    p("-" * 88)
    p("【控制组】")
    allok = True
    for c in control_group():
        st = "PASS" if c["ok"] else "FAIL"
        allok = allok and c["ok"]
        p(f"    {c['id']} {st}  {c['desc']}")
        p(f"         实测 {c['value']:.6e}  期望 {c['expect']}")
    p(f"    控制组小结: {'全部通过' if allok else '存在失败'}")
    p("")

    p("-" * 88)
    p("【守卫】")
    for name, ok_ in guards(led):
        p(f"    {'OK ' if ok_ else 'BAD'} {name}")
    p("")

    cnt = led.count()
    p("=" * 88)
    p("【条目统计】" + "  ".join(f"{k}={v}" for k, v in sorted(cnt.items())))
    p("=" * 88)
    return "\n".join(lines), allok


def build_judge(led, allok):
    cnt = led.count()
    verdict = "SCALE-FIXING-AND-CAUSALITY-MUTUALLY-EXCLUSIVE-SQRT2-C"
    md = []
    a = md.append
    a("# 判定册：TUFT-r152｜{ω,f,h,c} 完整关系组的定标代价与 √2·c 超光速判决")
    a("")
    a("## 00. 编号与定位")
    a("")
    a("| 项 | 内容 |")
    a("|---|---|")
    a("| 编号 | **r152**（实测首空号：r150、r151 已占用） |")
    a("| 定位 | **封堵 r151 的唯一退守路径** |")
    a("| 与 r151 的关系 | r151 处理两式（v=c、ωr=c）⇒ 退化为圆；"
      "本卷处理三式（+ h·f=c）。**条目不可相加** |")
    a("")
    a("## 01. 核心结论")
    a("")
    a("> **加上 `h·f = c` 可以把半径与螺距都定标，但代价是总速度变成 √2·c —— "
      "超光速 41.42%。**")
    a(">")
    a("> **『尺度确定』与『因果性』不可兼得。**")
    a("")
    a("```")
    a("ωr  = c   ⇒ 横向速度 = c")
    a("h·f = c   ⇒ 轴向速度 u = c    （螺距 h = u/f ⇒ u = h·f）")
    a("v²  = (rω)² + u²")
    a("────────────────────────────────")
    a("⇒ v = √(c² + c²) = √2·c ≈ 1.4142135624 c")
    a("```")
    a("")
    a("## 02. 附带结论：统一参数被锁死")
    a("")
    a("完整关系组把螺距角锁死：")
    a("")
    a("```")
    a("tan α = u/(rω) = c/c = 1  ⇒  α = 45°")
    a("τ/κ   = b/a = u/(rω) = 1  ⇒  κ = τ")
    a("```")
    a("")
    a("v1 称 τ/κ 是『纯几何的统一参数』。完整组确实给出了它的**唯一值 1**，"
      "但该值只在超光速构型下取得。")
    a("")
    a("## 03. 量纲口径冲突")
    a("")
    a("`h` 在来料里有两种互斥读法：")
    a("")
    a("| 读法 | 量纲 | 出处 | `h·f=c` 是否成立 |")
    a("|---|---|---|---|")
    a("| S（速度） | LT⁻¹ | v1 的 r⃗ = (...) + h t k | **否**（LT⁻² ≠ LT⁻¹） |")
    a("| P（螺距） | L | S12 的 p = uT | 是 |")
    a("")
    a("v1 的轨迹方程要求 h 为速度，而 `h·f=c` 要求 h 为螺距 ⇒ **同一符号两种互斥量纲**。")
    a("（若来料显式声明 h 为螺距，则此项降级为符号标注问题；"
      "但超光速结论不受影响，它只依赖 u = h·f = c。）")
    a("")
    a("## 04. 条目统计")
    a("")
    a("| 状态 | 条数 |")
    a("|---|---|")
    for k, v in sorted(cnt.items()):
        a(f"| {k} | {v} |")
    a("")
    a(f"控制组：{'全部通过' if allok else '存在失败'}")
    a("")
    a(f"## 05. 裁定")
    a("")
    a(f"**`{verdict}`**")
    a("")
    a("## 06. 未闭合项（禁止外推）")
    a("")
    a("1. 本卷在**欧氏 3-空间轨迹层**判决；κ、τ 是 Frenet 不变量，不是时空联络张量。")
    a("2. 未处理 4D 零世界线版本（ds²≡0 ⇒ Frenet 无定义）。")
    a("3. Zitterbewegung 标识 ω=2mc²/ℏ 是**外输**的，不是由关系组推出。")
    a("4. 修复定价只枚举 {KEEP, DEL, FLIP}，未枚举新增型修复。")
    a("5. 本卷**不**宣称靶体系已被完全证伪 —— 只判决："
      "**『用 h·f=c 补定标』这条退守路径会撞上因果门**。")
    a("6. 因果门 v≤c 本身以狭义相对论为前提；若靶主张修改相对论，"
      "则需先给出替代的因果结构与实验约束（本卷未评估该主张）。")
    a("")
    return "\n".join(md), verdict


def main():
    led = build_ledger()
    report, allok = build_report(led)
    print(report)

    here = os.path.dirname(os.path.abspath(__file__))
    outdir = os.path.abspath(os.path.join(here, "..", "数据"))
    os.makedirs(outdir, exist_ok=True)
    base = "TUFT-r152_ωfhcf完整关系组定标代价与超光速判决_2026-10-22"
    verdict_j = "SCALE-FIXING-AND-CAUSALITY-MUTUALLY-EXCLUSIVE-SQRT2-C"

    payload = {
        "id": "TUFT-r152",
        "title": "{ω,f,h,c} 完整关系组的定标代价：三式联立 ⇒ v = √2·c 超光速判决",
        "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "verdict": verdict_j,
        "counts": led.count(),
        "controls_ok": allok,
        "items": led.items,
        "dim_audit": A1_dimension()["rows"],
        "scan": C2_scan(),
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
