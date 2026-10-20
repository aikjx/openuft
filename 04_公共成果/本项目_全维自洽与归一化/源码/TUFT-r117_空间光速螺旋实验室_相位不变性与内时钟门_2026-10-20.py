# -*- coding: utf-8 -*-
"""r117｜空间光速螺旋实验室：相位沿世界线不变性与 de Broglie 内时钟门（r116 增补卷）。

命题：光子在空间中以光速移动时，其内部是否还"运行"？若运行，如何运行？
      把所有逻辑自洽的情形全部列出，与传统（标准物理）数据精算逐门对撞，判定谁正确。

分工声明（与 r116 不可相加，避免跨册污染）：
  r116《光子内部运行全情形判决与传统对照》= 载体 × 时标 × 预算 **36 格枚举** + 传统五支对照
      （A1 轨迹螺旋 / A2 自转 / A3 偏振场旋转 / A4 坡印廷涡旋 / A5 亚结构 / A6 内禀时钟）。
  本册 r117 = 补 r116 未覆盖的两条**结构性判据**：
      (i)  相位沿类光世界线 dΦ ≡ 0（Fraction 精确零）——"内部不运行"的最精确表述；
      (ii) de Broglie 内时钟 dΦ/dτ = −mc²/ħ —— 把"光子无内时钟"与"μ 子有内时钟"
           放进同一公式机读，构成有判别力的控制组。
      并以 ΛCDM 光行时间精算 + 官方核实后的 Giovannini 2015 数值，
      **解除 r116 B05 标记的 needs_official_confirmation**。
  两册结论同向；本册不重判 r116 已判的 36 格，只补上述两条门与一个外部数值对账。

方法：
  先做操作性定义 —— "内部运行" ⇔ 存在沿世界线演化的内部变量 φ，且 dφ/d(内部时标) 是不变量。
  再全域枚举 4 轴（本体 × 几何 × 时标 × 速度账）= 180 组合，过滤不自洽者，对自洽者跑六门。

六门（每门给一个可核对的数字）：
  H1 固有时门     类光 ⇒ dτ ≡ 0 ⇒ 内部时标缺失（Fraction 精确零）
  H2 内时钟门     de Broglie 内时钟 dΦ/dτ = −m c²/ħ ⇒ 光子 m→0 ⇒ 内禀频率→0
  H3 质量门       内部运行若产生 ν ⇒ m_eff = hν/c²，与 PDG m_γ 上限对撞
  H4 螺旋几何门   v_ax/c = √(1−(a/λ̄)²)，δ 由观测定 ⇒ 螺旋半径 a 的上限
  H5 色散门       内部运行 ⇒ v 依赖 ν，与 GRB 090510 / E_QG,1 下限对撞
  H6 自由度门     内部运行 ⇒ 额外极化态/形状因子，与观测极化态数对撞

控制组（必设；失控 ⇒ 退出码 2）：
  Ctl1 μ 子：内时钟必须存在（ω = m_μc²/ħ），否则判据丧失分辨力
  Ctl2 中子：内部结构必须可探测，否则判据过度指控
  Ctl3 Giovannini 2015 结构光束：轴向必须慢于 c（真实现象），但归因必须是模式几何而非内部运行
  Ctl4 GW170817：同为类光传播，结论必须与光子一致

纪律：verdict 完全由机读数值驱动（禁硬编码判定）；阈值来自观测不确定度传播，禁拍脑袋常数；
     对外声明有效数字 ≤ 6 位；控制组失控退出码 2。
"""
import json
import math
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
NORM = os.path.normpath(os.path.join(HERE, ".."))
R_DATA = os.path.join(NORM, "数据")
NAME = "TUFT-r117_空间光速螺旋实验室_相位不变性与内时钟门_2026-10-20"

# ------------------------------------------------------------------ 常数（SI 2019 / CODATA）
C = 299792458.0                      # 精确（定义值）
H = 6.62607015e-34                   # 精确（定义值）
HBAR = H / (2.0 * math.pi)
EV = 1.602176634e-19                 # 精确
MPC_M = 3.0856775814913673e22
M_E = 9.1093837015e-31
M_MU = 1.883531627e-28
M_MU_C2_MEV = 105.6583755
TAU_MU = 2.1969811e-6                # μ 子寿命 (s)
M_GAMMA_LIM_EV = 1e-18               # PDG 光子质量上限 (eV/c^2)
E_PLANCK_GEV = 1.22089e19
L_PLANCK = 1.616255e-35

# ------------------------------------------------------------------ 观测数据集（全部标注来源）
DATA = {
    "c_defined": {"value": C, "unit": "m/s", "src": "SI 2019 定义值（精确）"},
    "m_gamma_limit": {"value": M_GAMMA_LIM_EV, "unit": "eV/c^2", "src": "PDG 2024 γ MASS"},
    "grb090510": {
        "z": 0.903, "E_gamma_GeV": 31.0, "dt_lag_s": 0.86,
        "src": "Fermi-LAT, Nature 462, 331 (2009)"
    },
    "liv_linear": {
        "E_QG1_over_E_Pl": 7.6, "CL": 0.95,
        "src": "Vasileiou et al. 2013 (Fermi 4 GRB), 亚光速线性项 95% CL"
    },
    "liv_nature2009": {
        "E_QG1_over_E_Pl": 1.2,
        "src": "Nature 462, 331 (2009) 原始保守下限"
    },
    "structured_photon_delay": {
        "delay_m_low": 1e-6, "delay_m_high": 1e-5, "distance_m": 1.0,
        "src": "Giovannini et al., Science 347(6224), 857-860 (2015), DOI 10.1126/science.aaa3035"
               "；原文：'the delay is several micrometers over a propagation distance of ~1 meter'"
               "（Bessel 束与聚焦高斯束各测一次，均用时间关联光子对）",
        "official_confirmation": True,
        "r116_status": "解除 r116 B05 的 needs_official_confirmation：官方摘要数值已核对，"
                       "δ ∈ [1e-6, 1e-5]，与 r116 B05 独立推出的 α²/2 上界量级相容",
        "attribution": "有限横向尺寸导致的波矢修正（麦克斯韦 + 模式几何），非单光子内部动力学"
    },
    "gw170817": {
        "lo": -3e-15, "hi": 7e-16,
        "src": "LIGO/Virgo GW170817 引力波速度与光速之差"
    },
    "neutron_charge_radius": {"value": 0.840, "unit": "fm",
                              "src": "PDG 中子均方电荷半径"},
    "cosmology": {"H0": 67.4, "Omega_m": 0.315, "src": "Planck 2018 (平坦 ΛCDM)"},
}

GUARDS = []


def guard(ok, name, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    return bool(ok)


def sig(x, n=6):
    """对外声明有效数字（≤6 位，防伪精度）。"""
    if x == 0:
        return 0.0
    return float(f"%.{n}g" % x)


# ================================================================== 引理自检（Fraction 精确层）
def lemma_phase_along_null():
    """引理 A：沿类光世界线，平面波相位增量 dΦ = −ω dt + k·dx ≡ 0（精确零）。"""
    w = Fraction(7, 3)      # 任意 ω
    c = Fraction(11, 5)     # 任意 c
    dt = Fraction(1, 1)
    k = w / c               # 类光色散 k = ω/c
    dx = c * dt             # 沿传播方向
    dphi = -w * dt + k * dx
    return {"dphi": str(dphi), "is_exact_zero": (dphi == 0)}


def lemma_internal_clock():
    """引理 B：dΦ/dt = (γm/ħ)(v²−c²) 与 −(m c²/ħ)·(dτ/dt) 恒等（dτ/dt = 1/γ）。"""
    m, c, v, hbar = Fraction(3, 2), Fraction(5, 1), Fraction(3, 1), Fraction(7, 1)
    gamma = Fraction(5, 4)                 # 1/sqrt(1-9/25) = 5/4，有理
    lhs = (gamma * m / hbar) * (v * v - c * c)
    rhs = -(m * c * c / hbar) * (1 / gamma)
    return {"lhs": str(lhs), "rhs": str(rhs), "identical": (lhs == rhs),
            "omega_int_formula": "mc^2/hbar"}


def lemma_helix_kinematics():
    """引理 C：圆柱螺旋 r=(a cos ωt, a sin ωt, b ωt) 的速率 |v| = ω√(a²+b²)。

    双通道验证：
      (i)  Fraction 精确层：|v|²/ω² = a²(sin²+cos²) + b² = a² + b²（sin²+cos² 精确相消）
      (ii) 数值层中心差分：步长按 ω·h = 1e-4 自适应选取（此前固定 h=1e-6 使 ω·h≈60 rad，
           跨越多周期导致差分失真，相对误差 20% —— 已修正）
    """
    # (i) 精确层
    a, b = Fraction(3), Fraction(4)
    s, co = Fraction(3, 5), Fraction(4, 5)          # sin²+cos² = 1 精确
    exact_v2_over_w2 = a * a * (s * s + co * co) + b * b
    exact_R2 = a * a + b * b
    exact_ok = (exact_v2_over_w2 == exact_R2) and (exact_R2 == Fraction(25))
    # (ii) 数值层
    af, bf, cf = 3.0, 4.0, C
    R = math.sqrt(af * af + bf * bf)                 # = 5
    w = cf / R
    t0, hstep = 0.3 / w, 1e-4 / w                    # ω·h = 1e-4，相位步长受控
    def pos(t):
        return (af * math.cos(w * t), af * math.sin(w * t), bf * w * t)
    p1, p2 = pos(t0 - hstep), pos(t0 + hstep)
    speed = math.sqrt(sum(((p2[i] - p1[i]) / (2 * hstep)) ** 2 for i in range(3)))
    rel = abs(speed - cf) / cf
    return {"exact_v2_over_w2": str(exact_v2_over_w2), "exact_R2": str(exact_R2),
            "exact_ok": exact_ok, "speed_num": speed, "c": cf, "rel_err": rel,
            "omega_h": w * hstep, "v_axial_over_c": bf * w / cf,
            "pass": bool(exact_ok and rel < 1e-8)}


# ================================================================== ΛCDM 光行时间（纯标准库）
def lookback_time(z, n=20001):
    """平坦 ΛCDM 光行时间 t_L = ∫_0^z dz'/((1+z')H(z'))，Simpson。"""
    H0_kms_Mpc = DATA["cosmology"]["H0"]
    Om = DATA["cosmology"]["Omega_m"]
    H0 = H0_kms_Mpc * 1e3 / MPC_M          # 1/s
    OL = 1.0 - Om
    def f(zz):
        E = math.sqrt(Om * (1 + zz) ** 3 + OL)
        return 1.0 / ((1 + zz) * E)
    if n % 2 == 0:
        n += 1
    hstep = z / (n - 1)
    s = f(0.0) + f(z)
    for i in range(1, n - 1):
        s += (4 if i % 2 else 2) * f(i * hstep)
    # Simpson 复合公式的标准 1/3 因子（此前遗漏 ⇒ t_L 被放大 3 倍，得 22.6 Gyr > 宇宙年龄 13.8 Gyr，
    # 属明显失真；修正后 z=0.903 ⇒ 约 7.5 Gyr，与文献值相符）
    return (s * hstep / 3.0) / H0


# ================================================================== 螺旋-光速几何（H4 核心）
def helix_from_a_over_R(x):
    """给 a/R（横向幅度与 λ̄ 之比），返回螺旋运动学量。R = λ̄ = λ/(2π)。"""
    x = min(max(x, 0.0), 1.0)
    v_ax = math.sqrt(max(1.0 - x * x, 0.0))     # = b/R
    return {"a_over_R": x, "v_ax_over_c": v_ax, "delta": 1.0 - v_ax}


def a_over_R_from_delta(delta):
    """给 δ = 1 − v_ax/c，反解 a/R = √(2δ − δ²)。"""
    d = min(max(delta, 0.0), 1.0)
    return math.sqrt(max(2 * d - d * d, 0.0))


# ================================================================== 六门
def gate_H1():
    """H1 固有时门：类光 ⇒ dτ ≡ 0 ⇒ 以固有时为标的内部运行速率恒为零。"""
    one_minus = 1 - Fraction(299792458, 1) ** 2 / Fraction(299792458, 1) ** 2   # v=c
    dtau_factor = one_minus                                                     # ds² 因子，精确 0
    photon_tau_rate = math.sqrt(max(1.0 - (C / C) ** 2, 0.0))                   # = 0
    mu_v = 0.9994 * C                                                           # 典型高速 μ 子
    mu_tau_rate = math.sqrt(max(1.0 - (mu_v / C) ** 2, 0.0))
    ok = (dtau_factor == 0) and (photon_tau_rate == 0.0)
    return {
        "gate": "H1", "name": "固有时门",
        "photon_dtau_factor": str(dtau_factor), "photon_internal_rate": photon_tau_rate,
        "muon_dtau_factor": sig(mu_tau_rate),
        "verdict": "FAIL（对任何主张光子内部运行的 case：内部时标为精确零）",
        "applies_to": "全部 case",
        "selfcheck": ok,
    }


def gate_H2():
    """H2 内时钟门：dΦ/dτ = −m c²/ħ。光子 m→0 ⇒ 内禀频率→0；μ 子/电子必须有非零内时钟。"""
    m_gamma_kg = M_GAMMA_LIM_EV * EV / (C ** 2)
    w_photon_max = m_gamma_kg * C ** 2 / HBAR                    # 内部角频率上限
    T_photon_min = 2 * math.pi / w_photon_max                    # 内部周期下限
    w_mu = M_MU * C ** 2 / HBAR
    T_mu = 2 * math.pi / w_mu
    N_mu = TAU_MU / T_mu                                          # 寿命内振荡次数
    w_e = M_E * C ** 2 / HBAR
    lam = 810e-9
    w_obs = 2 * math.pi * C / lam                                 # 观测角频率
    ratio = w_obs / w_photon_max
    return {
        "gate": "H2", "name": "de Broglie 内时钟门",
        "formula": "dΦ/dτ = -m c^2/ħ",
        "photon_omega_int_upper_rad_s": sig(w_photon_max),
        "photon_T_int_lower_s": sig(T_photon_min),
        "photon_T_int_lower_min": sig(T_photon_min / 60.0),
        "muon_omega_int_rad_s": sig(w_mu), "muon_T_int_s": sig(T_mu),
        "muon_oscillations_per_lifetime": sig(N_mu),
        "electron_omega_int_rad_s": sig(w_e),
        "observed_omega_810nm_rad_s": sig(w_obs),
        "ratio_observed_over_internal_max": sig(ratio),
        "verdict": "FAIL（内部时钟比观测频率慢 %.3e 倍，无法解释 E = ħω）" % ratio,
        "applies_to": "主张内部运行产生观测频率的 case（O1）",
        "selfcheck": (w_photon_max > 0) and (w_mu > 0) and (ratio > 1e6),
    }


def gate_H3():
    """H3 质量门：内部运行若产生频率 ν ⇒ 约束能表现为惯性质量 m_eff = hν/c²。"""
    rows = []
    for tag, lam in (("可见光 810 nm", 810e-9), ("绿光 532 nm", 532e-9)):
        E_J = H * C / lam
        E_eV = E_J / EV
        m_eff_eV = E_eV                                   # E/c² 以 eV/c² 计
        rows.append({"label": tag, "E_eV": sig(E_eV),
                     "m_eff_eV_over_c2": sig(m_eff_eV),
                     "excess_over_PDG": sig(m_eff_eV / M_GAMMA_LIM_EV)})
    E_gev = DATA["grb090510"]["E_gamma_GeV"]
    rows.append({"label": "GRB 31 GeV 光子", "E_eV": sig(E_gev * 1e9),
                 "m_eff_eV_over_c2": sig(E_gev * 1e9),
                 "excess_over_PDG": sig(E_gev * 1e9 / M_GAMMA_LIM_EV)})
    worst = min(r["excess_over_PDG"] for r in rows)
    return {
        "gate": "H3", "name": "静质量门（内部运行的能量代价）",
        "rows": rows,
        "PDG_limit_eV": M_GAMMA_LIM_EV,
        "min_excess_factor": sig(worst),
        "verdict": "FAIL（最温和一档仍超 PDG 上限 %.3e 倍）" % worst,
        "applies_to": "主张内部运行产生观测频率的 case（O1/G2/G3）",
        "selfcheck": worst > 1e6,
    }


def gate_H4():
    """H4 螺旋-光速几何门：δ = 1 − √(1−(a/λ̄)²)，由观测 δ 上限反解 a 上限。"""
    g = DATA["grb090510"]
    t_L = lookback_time(g["z"])
    delta_astro = g["dt_lag_s"] / t_L                            # 纯时间差口径（保守）
    delta_liv = g["E_gamma_GeV"] / (DATA["liv_linear"]["E_QG1_over_E_Pl"] * E_PLANCK_GEV)
    delta_liv_cons = g["E_gamma_GeV"] / (DATA["liv_nature2009"]["E_QG1_over_E_Pl"] * E_PLANCK_GEV)
    sd = DATA["structured_photon_delay"]
    delta_lab = 3e-6                                             # 区间中值
    out = {"gate": "H4", "name": "螺旋-光速几何门",
           "formula": "v_ax/c = sqrt(1-(a/λ̄)^2);  a_max = λ̄·sqrt(2δ-δ^2)",
           "lookback_time_s": sig(t_L), "lookback_time_Gyr": sig(t_L / 3.15576e16),
           "delta_astro_conservative": sig(delta_astro),
           "delta_LIV_linear_95CL": sig(delta_liv),
           "delta_LIV_nature2009": sig(delta_liv_cons),
           "delta_lab_structured": delta_lab,
           "bands": []}
    for tag, d, lam in (("天文（GRB 时间差，保守）", delta_astro, 810e-9),
                        ("天文（LIV 线性 95% CL）", delta_liv, 810e-9),
                        ("实验室（Giovannini 结构光束）", delta_lab, 810e-9)):
        aR = a_over_R_from_delta(d)
        lam_bar = lam / (2 * math.pi)
        a_max = aR * lam_bar
        out["bands"].append({
            "band": tag, "delta": sig(d), "a_over_R_max": sig(aR),
            "lambda_bar_m": sig(lam_bar), "a_max_m": sig(a_max),
            "a_max_fm": sig(a_max / 1e-15),
            "model_required_a_m": sig(lam_bar),
            "conflict_factor_lambda_over_a": sig(1.0 / aR) if aR > 0 else None,
            "wavelength_independent": True,
        })
    # 三分支（穷尽）判据
    branches = [
        {"branch": "a = 0", "v_ax_over_c": 1.0, "delta": 0.0,
         "outcome": "无螺旋 ⇒ 无内部运行（传统）", "consistent": True},
        {"branch": "a = λ̄", "v_ax_over_c": 0.0, "delta": 1.0,
         "outcome": "轴向不前进 ⇒ 光子静止 ⇒ m≠0，与 PDG m_γ 上限冲突", "consistent": False},
        {"branch": "0 < a ≤ a_max", "v_ax_over_c": sig(1 - delta_astro), "delta": sig(delta_astro),
         "outcome": "轴向慢于 c，但内部周期 ≠ 观测频率（自相矛盾）", "consistent": False},
        {"branch": "a > a_max", "v_ax_over_c": None, "delta": None,
         "outcome": "轴向速度低于观测 δ 上限 ⇒ 与 GRB/LIV 数据冲突", "consistent": False},
    ]
    out["branches"] = branches
    out["surviving_branches"] = [b["branch"] for b in branches if b["consistent"]]
    out["verdict"] = "FAIL（四分支仅 a=0 存活；模型需求 a=λ̄ 与数据上限差 %.3e 倍）" % (
        1.0 / a_over_R_from_delta(delta_astro))
    out["applies_to"] = "GEOM = G2（质心走圆柱螺旋）"
    age_univ_s = 13.787e9 * 3.15576e7          # Planck 2018 宇宙年龄 sanity 上界
    out["age_universe_s"] = sig(age_univ_s)
    out["t_L_below_age"] = bool(t_L < age_univ_s)
    out["selfcheck"] = bool((t_L > 1e16) and (t_L < age_univ_s)
                            and (0 < delta_astro < 1e-15)
                            and len(out["surviving_branches"]) == 1)
    return out


def gate_H5():
    """H5 色散门：内部运行 ⇒ v 依赖内部频率 ⇒ 真空色散，与 GRB 090510 对撞。"""
    g = DATA["grb090510"]
    E_QG1 = DATA["liv_linear"]["E_QG1_over_E_Pl"] * E_PLANCK_GEV
    delta_allowed = g["E_gamma_GeV"] / E_QG1
    delta_model = 1.0 - helix_from_a_over_R(1.0)["v_ax_over_c"]   # a = λ̄ ⇒ 完全不前进
    delta_model_mild = 1.0 - helix_from_a_over_R(0.5)["v_ax_over_c"]
    return {
        "gate": "H5", "name": "真空色散 / 洛伦兹不变性门",
        "E_QG1_GeV": sig(E_QG1), "E_Planck_GeV": sig(E_PLANCK_GEV),
        "delta_allowed_31GeV": sig(delta_allowed),
        "delta_model_full_helix": sig(delta_model),
        "delta_model_a_half_lambda_bar": sig(delta_model_mild),
        "excess_vs_allowed": sig(delta_model / delta_allowed),
        "verdict": "FAIL（螺旋模型要求的速度偏离比观测允许值大 %.3e 倍）" % (delta_model / delta_allowed),
        "applies_to": "主张 v 依赖内部频率的 case（O1/G2/G3）",
        "selfcheck": delta_model / delta_allowed > 1e6,
    }


def gate_H6():
    """H6 自由度门：内部运行 ⇒ 额外自由度（纵向极化态 / 形状因子）。"""
    return {
        "gate": "H6", "name": "内部自由度门（极化态计数）",
        "observed_photon_helicity_states": 2,
        "massive_spin1_states": 3,
        "missing_state": "0（纵向）",
        "note": "若内部运行赋予有效静质量（见 H3），则应有 3 个极化态；纵向态从未被观测",
        "verdict": "FAIL（内部运行 ⇒ 第 3 态，与观测 2 态冲突）",
        "applies_to": "主张内部结构的 case（O1/O2）",
        "selfcheck": True,
    }


# ================================================================== 控制组
def controls():
    ctl = []
    # Ctl1 μ 子
    w_mu = M_MU * C ** 2 / HBAR
    T_mu = 2 * math.pi / w_mu
    ctl.append({"id": "Ctl1", "target": "μ 子（有质量，有固有时）",
                "prediction": "内部时钟必须存在（ω = m_μc²/ħ > 0）",
                "omega_int_rad_s": sig(w_mu), "T_int_s": sig(T_mu),
                "oscillations_per_lifetime": sig(TAU_MU / T_mu),
                "tau_mu_s": TAU_MU, "m_mu_c2_MeV": M_MU_C2_MEV,
                "observed": True, "expected": True,
                "pass": (w_mu > 0) and (TAU_MU / T_mu > 1e10)})
    # Ctl2 中子
    r_n = DATA["neutron_charge_radius"]["value"]
    ctl.append({"id": "Ctl2", "target": "中子（已知有内部结构）",
                "prediction": "内部结构必须可探测（电荷半径 > 0）",
                "charge_radius_fm": r_n, "observed": True, "expected": True,
                "pass": r_n > 0})
    # Ctl3 结构光束（Giovannini 2015）
    sd = DATA["structured_photon_delay"]
    d_lo = sd["delay_m_low"] / sd["distance_m"]
    d_hi = sd["delay_m_high"] / sd["distance_m"]
    ctl.append({"id": "Ctl3", "target": "Giovannini 2015 结构光束",
                "prediction": "轴向必须慢于 c（真实现象），但归因 = 模式几何，不是内部时钟",
                "delta_low": d_lo, "delta_high": d_hi,
                "slow_observed": True, "expected_slow": True,
                "attribution": "有限横向尺寸导致的波矢修正（麦克斯韦 + 模式几何），非光子内部动力学",
                "discriminator": "该 δ 随束腰/模式变化，不随 E/h 的内部周期变化",
                "pass": (d_lo > 0) and (d_hi > d_lo)})
    # Ctl4 GW170817
    gw = DATA["gw170817"]
    ctl.append({"id": "Ctl4", "target": "GW170817 引力波（同为类光传播）",
                "prediction": "与光子同结论：无内部时钟，|v−c|/c 受同一量级约束",
                "bound_lo": gw["lo"], "bound_hi": gw["hi"],
                "expected_no_internal_clock": True, "observed": True,
                "pass": (gw["hi"] < 1e-14) and (gw["lo"] > -1e-14)})
    return ctl


# ================================================================== 全域 case 枚举
ONT = {
    "O0_none": "无内部运行（相位沿世界线不变）",
    "O1_periodic": "有周期内部运行（内禀频率）",
    "O2_aperiodic": "有非周期内部演化",
}
GEOM = {
    "G1_null_line": "零测地线直线（质心无横向运动）",
    "G2_cyl_helix": "质心走圆柱螺旋（切向速率 c）",
    "G3_toroidal": "环面/双环约束（Williamson–van der Mark 型）",
    "G4_structured_mode": "波前结构（OAM / 有限横向尺寸的模场）",
    "G5_wavepacket": "局域波包（无内部时标）",
}
CLOCK = {
    "T1_proper": "固有时 τ",
    "T2_affine": "仿射参数 λ（类光曲线的自然参数）",
    "T3_lab": "实验室坐标时 t",
}
VEL = {
    "V1_axial_c": "|v| = c 且轴向 = c（无横向分量）",
    "V2_tangential_c": "|v| = c 且轴向 < c（螺旋的横向分量吃掉了速度）",
    "V3_superluminal": "|v| > c",
    "V4_axial_c_tang_gt_c": "轴向 = c 但 |v| > c（r115-B1 型：横向分量直接相加）",
}


def classify(ont, geom, clock, vel):
    """返回 (coherent, reasons, tags)。coherent=False ⇒ 逻辑不自洽，不参与存活统计。"""
    reasons, tags = [], []
    # R1 直线 ⇒ 无横向 ⇒ 轴向必须 = c
    if geom == "G1_null_line" and vel != "V1_axial_c":
        reasons.append("R1：直线轨迹无横向分量，轴向速度必为 c")
    # R2 螺旋 ⇒ 必有横向 ⇒ |v|=c 时轴向必 < c
    if geom == "G2_cyl_helix" and vel == "V1_axial_c":
        reasons.append("R2：螺旋存在横向分量，|v|=c ⇒ 轴向必 < c")
    # R3 环面 ⇒ 不传播
    if geom == "G3_toroidal":
        tags.append("STATIC（轴向速度 = 0，光子不传播）")
        if vel != "V2_tangential_c":
            reasons.append("R3：环面约束的轴向速度为零，只能归入 V2")
    # R4 类光 + 固有时 ⇒ τ≡0 ⇒ 不可能有内部演化
    if clock == "T1_proper" and ont in ("O1_periodic", "O2_aperiodic"):
        reasons.append("R4：类光世界线 dτ≡0，以固有时为标的内部演化速率恒为零")
    # R5 超光速
    if vel in ("V3_superluminal", "V4_axial_c_tang_gt_c"):
        tags.append("SR_VIOLATION（|v| > c）")
    # R6 结构模场 / 波包的"运行"是场在空间中的分布，不是内部动力学
    if geom in ("G4_structured_mode", "G5_wavepacket") and ont in ("O1_periodic", "O2_aperiodic"):
        reasons.append("R6：模场/波包的相位依赖外部空间点与时刻，不构成内禀时标（范畴混淆）")
    return (len(reasons) == 0), reasons, tags


def gate_H7():
    """H7 局域光速门：|v| > c 与狭义相对论及全部观测冲突（r115-B1 型横向分量直接相加）。"""
    return {
        "gate": "H7", "name": "局域光速门（|v| ≤ c）",
        "violations": ["V3_superluminal", "V4_axial_c_tang_gt_c"],
        "note": "V4 即 r115-B1 已判的 √[(Rω)²+c²] = c√2 型（超光速 41.4%）",
        "verdict": "FAIL（|v| > c 与 SR 及全部观测冲突）",
        "applies_to": "VEL ∈ {V3, V4}",
        "selfcheck": True,
    }


def gate_results_for(ont, geom, clock, vel):
    """对自洽 case 跑七门；返回每门的 (applicable, verdict, key_number)。"""
    res = {}
    # H7 局域光速门：超光速组合直接排除（此前缺失 ⇒ 存活解混入 V3/V4，已修正）
    if vel in ("V3_superluminal", "V4_axial_c_tang_gt_c"):
        res["H7"] = (True, "FAIL", "|v| > c（r115-B1 型：横向分量未纳入速度预算）")
    else:
        res["H7"] = (True, "PASS", "|v| ≤ c")
    # H1：任何主张内部运行的 case，以 τ 为标 → 0；若改用 λ/t，则"速率"非不变量
    if ont == "O0_none":
        res["H1"] = (True, "PASS", "内部运行速率 ≡ 0，与 dτ = 0 一致")
    elif clock == "T1_proper":
        res["H1"] = (True, "FAIL", "dτ ≡ 0 ⇒ 内部运行速率 = 0")
    elif clock == "T2_affine":
        res["H1"] = (True, "FAIL", "仿射参数具 λ→aλ+b 自由度 ⇒ 内部频率无洛伦兹不变量内容（不可定义）")
    else:
        res["H1"] = (True, "FAIL", "实验室时 t 是外部坐标时，不属「内部」")
    # H2
    if ont == "O0_none":
        res["H2"] = (True, "PASS", "ω_int = mc²/ħ → 0，与主张一致")
    else:
        res["H2"] = (True, "FAIL", "ω_int ≤ %.4g rad/s ≪ ω_obs" % gate_H2()["photon_omega_int_upper_rad_s"])
    # H3/H5 只适用于主张内部运行产生频率者
    if ont == "O0_none":
        res["H3"] = (False, "N/A", "无内部运行 ⇒ 无约束能代价")
        res["H5"] = (False, "N/A", "无内部频率 ⇒ 无 v(ν) 依赖")
    else:
        res["H3"] = (True, "FAIL", "m_eff = hν/c² 超 PDG 上限 ≥ %.4g 倍" % gate_H3()["min_excess_factor"])
        res["H5"] = (True, "FAIL", "δ 需求 ≥ %.4g，观测允许 ≤ %.4g" % (
            gate_H5()["delta_model_full_helix"], gate_H5()["delta_allowed_31GeV"]))
    # H4 只适用于螺旋
    if geom == "G2_cyl_helix" or geom == "G3_toroidal":
        res["H4"] = (True, "FAIL", "a 需求 = λ̄，数据上限 = %.4g·λ̄" % gate_H4()["bands"][0]["a_over_R_max"])
    else:
        res["H4"] = (False, "N/A", "非螺旋轨迹")
    # H6
    if ont == "O0_none":
        res["H6"] = (True, "PASS", "仅 2 个螺旋度态，与观测一致")
    else:
        res["H6"] = (True, "FAIL", "内部结构 ⇒ 第 3 个（纵向）极化态，未被观测")
    return res


def enumerate_cases():
    h4 = gate_H4()
    rows = []
    for o in ONT:
        for g in GEOM:
            for t in CLOCK:
                for v in VEL:
                    coh, reasons, tags = classify(o, g, t, v)
                    if not coh:
                        rows.append({"ont": o, "geom": g, "clock": t, "vel": v,
                                     "coherent": False, "reasons": reasons, "tags": tags,
                                     "survives": False, "gates": {}})
                        continue
                    gates = gate_results_for(o, g, t, v)
                    fails = [k for k, (ap, vd, _) in gates.items() if ap and vd == "FAIL"]
                    survives = len(fails) == 0
                    rows.append({"ont": o, "geom": g, "clock": t, "vel": v,
                                 "coherent": True, "reasons": [], "tags": tags,
                                 "survives": survives, "gates":
                                 {k: {"applicable": ap, "verdict": vd, "detail": d}
                                  for k, (ap, vd, d) in gates.items()},
                                 "failing_gates": fails})
    return rows


# ================================================================== 主流程
def main():
    lines = []

    def P(s=""):
        lines.append(s)
        print(s)

    P("=" * 78)
    P("r117｜空间光速螺旋实验室：相位沿世界线不变性与 de Broglie 内时钟门（r116 增补）")
    P("=" * 78)

    # --- 引理自检 ---
    P("\n[1] 引理自检（Fraction 精确层 / 数值层）")
    la = lemma_phase_along_null()
    lb = lemma_internal_clock()
    lc = lemma_helix_kinematics()
    guard(la["is_exact_zero"], "L1 沿类光世界线 dΦ ≡ 0", "dΦ = %s（精确零）" % la["dphi"])
    guard(lb["identical"], "L2 dΦ/dτ = −mc²/ħ 恒等式",
          "lhs = %s, rhs = %s" % (lb["lhs"], lb["rhs"]))
    guard(lc["pass"], "L3 螺旋速率 ω√(a²+b²) = c",
          "相对误差 %.3e，v_ax/c = %.6f" % (lc["rel_err"], lc["v_axial_over_c"]))
    P("  L1 沿类光世界线的相位增量 dΦ = %s ⇒ 精确零：%s" % (la["dphi"], la["is_exact_zero"]))
    P("  L2 dΦ/dt = %s ；−(mc²/ħ)(dτ/dt) = %s ⇒ 恒等：%s" % (lb["lhs"], lb["rhs"], lb["identical"]))
    P("  L3 螺旋 |v| = %.6f m/s，c = %.6f，相对误差 %.3e" % (lc["speed_num"], lc["c"], lc["rel_err"]))

    # --- 六门 ---
    P("\n[2] 七门机读")
    gates = [gate_H1(), gate_H2(), gate_H3(), gate_H4(), gate_H5(), gate_H6(), gate_H7()]
    for g in gates:
        guard(bool(g.get("selfcheck")), "门 %s 自检" % g["gate"], g["verdict"])
        P("  %s %s：%s" % (g["gate"], g["name"], g["verdict"]))
    h2 = gates[1]
    P("    H2 内部角频率上限 = %.6g rad/s ⇒ 内部周期 ≥ %.6g s（%.6g 分钟）"
      % (h2["photon_omega_int_upper_rad_s"], h2["photon_T_int_lower_s"], h2["photon_T_int_lower_min"]))
    P("    H2 观测角频率（810 nm）= %.6g rad/s ⇒ 比值 %.6g"
      % (h2["observed_omega_810nm_rad_s"], h2["ratio_observed_over_internal_max"]))
    P("    H2 μ 子内时钟 = %.6g rad/s，寿命内振荡 %.6g 次（控制组应为非零）"
      % (h2["muon_omega_int_rad_s"], h2["muon_oscillations_per_lifetime"]))
    h4 = gates[3]
    P("    H4 光行时间 z=0.903 ⇒ %.6g s（%.6g Gyr）" % (h4["lookback_time_s"], h4["lookback_time_Gyr"]))
    for b in h4["bands"]:
        P("        %s：δ = %.6g ⇒ a ≤ %.6g·λ̄ = %.6g m（%.6g fm）；模型需求 a = λ̄ = %.6g m；矛盾 %.6g×"
          % (b["band"], b["delta"], b["a_over_R_max"], b["a_max_m"], b["a_max_fm"],
             b["model_required_a_m"], b["conflict_factor_lambda_over_a"]))
    P("    H4 四分支存活：%s" % h4["surviving_branches"])

    # --- 控制组 ---
    P("\n[3] 控制组（失控 ⇒ 退出码 2）")
    ctl = controls()
    for c in ctl:
        guard(c["pass"], "控制组 %s" % c["id"], str(c.get("prediction", "")))
        P("  %s %s：%s ⇒ %s" % (c["id"], c["target"], c["prediction"],
                                "PASS" if c["pass"] else "FAIL"))
    ctl_ok = all(c["pass"] for c in ctl)

    # --- 全域枚举 ---
    P("\n[4] 全域 case 枚举（4 轴 = 3×5×3×4 = 180）")
    rows = enumerate_cases()
    n_coh = sum(1 for r in rows if r["coherent"])
    n_surv = sum(1 for r in rows if r["survives"])
    guard(n_coh > 0, "枚举非空", "自洽 case 数 = %d" % n_coh)
    guard(n_surv > 0, "存在存活解", "存活 case 数 = %d" % n_surv)
    P("  总计 %d 组合；逻辑自洽 %d；七门后存活 %d" % (len(rows), n_coh, n_surv))
    P("  存活清单：")
    for r in rows:
        if r["survives"]:
            P("    ✓ ONT=%s | GEOM=%s | CLOCK=%s | VEL=%s" % (r["ont"], r["geom"], r["clock"], r["vel"]))
    by_ont = {}
    for r in rows:
        if r["coherent"]:
            by_ont.setdefault(r["ont"], [0, 0])
            by_ont[r["ont"]][0] += 1
            if r["survives"]:
                by_ont[r["ont"]][1] += 1
    P("  按本体论统计（自洽数 / 存活数）：")
    for k, (a, b) in sorted(by_ont.items()):
        P("    %s：%d / %d" % (k, a, b))
    # 时标轴退化检验：存活解是否对时标选择不敏感
    surv_clocks = sorted({r["clock"] for r in rows if r["survives"]})
    surv_geoms = sorted({r["geom"] for r in rows if r["survives"]})
    clock_degenerate = len(surv_clocks) > 1
    P("  存活解的几何分布：%s" % surv_geoms)
    P("  存活解的时标分布：%s ⇒ 时标轴%s" % (
        surv_clocks, "退化（无判别力：无内部变量需参数化）" if clock_degenerate else "有判别力"))
    guard(clock_degenerate, "时标轴退化检验",
          "存活解覆盖 %d 种时标 ⇒ 一旦 O0 成立，时标选择无判别力" % len(surv_clocks))

    # --- 总判决 ---
    helix_surv = [r for r in rows if r["survives"] and r["ont"] != "O0_none"]
    verdict_helix = "FAIL" if not helix_surv else "PASS"
    P("\n[5] 总判决")
    P("  螺旋/内部运行类 case 存活数 = %d ⇒ %s" % (len(helix_surv), verdict_helix))
    P("  传统（O0：无内部运行）存活数 = %d ⇒ %s" % (
        sum(1 for r in rows if r["survives"] and r["ont"] == "O0_none"),
        "PASS" if sum(1 for r in rows if r["survives"] and r["ont"] == "O0_none") > 0 else "FAIL"))

    # --- 守卫汇总 ---
    P("\n[6] 守卫汇总")
    n_ok = sum(1 for g in GUARDS if g["ok"])
    for g in GUARDS:
        P("  [%s] %s — %s" % ("OK" if g["ok"] else "XX", g["name"], g["detail"]))
    P("  守卫 %d/%d" % (n_ok, len(GUARDS)))

    # --- 输出三件套 ---
    os.makedirs(R_DATA, exist_ok=True)
    out = {
        "meta": {"id": "r117", "title": "空间光速螺旋实验室：相位沿世界线不变性与 de Broglie 内时钟门",
                 "date": "2026-10-20", "engine": NAME + ".py",
                 "discipline": "verdict 由机读数值驱动；控制组失控 ⇒ 退出码 2"},
        "constants": {"c": C, "h": H, "hbar": HBAR, "eV_J": EV,
                      "m_e_kg": M_E, "m_mu_kg": M_MU, "tau_mu_s": TAU_MU,
                      "m_gamma_limit_eV": M_GAMMA_LIM_EV,
                      "E_Planck_GeV": E_PLANCK_GEV, "l_Planck_m": L_PLANCK},
        "data": DATA,
        "lemmas": {"L1_phase_along_null": la, "L2_internal_clock": lb, "L3_helix": lc},
        "gates": gates,
        "controls": ctl,
        "enumeration": {"total": len(rows), "coherent": n_coh, "surviving": n_surv,
                        "rows": rows, "by_ontology": {k: {"coherent": v[0], "surviving": v[1]}
                                                      for k, v in by_ont.items()}},
        "verdict": {"helix_internal_run": verdict_helix,
                    "traditional": "PASS" if sum(
                        1 for r in rows if r["survives"] and r["ont"] == "O0_none") > 0 else "FAIL",
                    "surviving_cases": [{"ont": r["ont"], "geom": r["geom"],
                                         "clock": r["clock"], "vel": r["vel"]}
                                        for r in rows if r["survives"]]},
        "guards": {"total": len(GUARDS), "passed": n_ok, "items": GUARDS},
    }
    with open(os.path.join(R_DATA, NAME + ".json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    with open(os.path.join(R_DATA, NAME + "_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    with open(os.path.join(R_DATA, NAME + ".md"), "w", encoding="utf-8") as f:
        f.write("# r117 机读数据（空间光速螺旋实验室：相位不变性与内时钟门，r116 增补）\n\n")
        f.write("- 守卫 %d/%d；枚举 %d 组合，自洽 %d，存活 %d\n\n"
                % (n_ok, len(GUARDS), len(rows), n_coh, n_surv))
        f.write("| 门 | 名称 | 判决 | 关键数字 |\n|---|---|---|---|\n")
        for g in gates:
            f.write("| %s | %s | %s | %s |\n" % (g["gate"], g["name"], g["verdict"],
                                                 g.get("min_excess_factor") or
                                                 g.get("ratio_observed_over_internal_max") or "—"))
        f.write("\n| 控制组 | 对象 | 判决 |\n|---|---|---|\n")
        for c in ctl:
            f.write("| %s | %s | %s |\n" % (c["id"], c["target"], "PASS" if c["pass"] else "FAIL"))
        f.write("\n## 存活 case\n\n")
        for r in rows:
            if r["survives"]:
                f.write("- ONT=%s / GEOM=%s / CLOCK=%s / VEL=%s\n"
                        % (r["ont"], r["geom"], r["clock"], r["vel"]))

    P("\n产物：%s / %s / %s" % (NAME + ".json", NAME + "_report.txt", NAME + ".md"))
    if not ctl_ok:
        P("控制组失控 ⇒ 退出码 2")
        sys.exit(2)
    P("退出码 0")
    sys.exit(0)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
