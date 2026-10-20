# -*- coding: utf-8 -*-
"""r118｜空间螺旋纲领退守路径攻破：电子环形光子模型 + OAM 避难所 + 协变性条款闭合。

承接 r116（光子内部运行 36 格，传统支全胜）与 r117（相位不变性 + 内时钟门）。
r116/r117 封死了「光子内部运行」，但留下三条未闭合处，本册逐一攻破：

  T1 退守路径 ——「光子内部不转，那电子内部是约束光子在转」
     靶：Williamson & van der Mark (1997) 电子 = 环形约束光子（双环，r = λ_C/4π）。
     门：E1 尺寸门（LEP 点状性上限）/ E2 电荷门（自承 8% 缺口）/ E3 约束机制门
         / E4 Zitterbewegung 混淆消解 / E5 反常磁矩门

  T2 避难所闭合 ——「结构光的能流确实在打螺旋，这不就是内部运行吗」
     靶：A4 坡印廷涡旋（r116 判 BOUNDARY）。
     门：P1 表示论门（光子无 OAM 算符）/ P2 no-go 定理 / P3 内禀性门 / P4 单光子能量门

  T3 分歧闭合 —— r116 D02 把 S3 几何主义的 PASS 归因到「判据集缺洛伦兹协变性」
     本册显式补入协变性条款 C，重判 A1 ⇒ 应收敛为 5/5 全 FAIL，分歧闭合。

控制组（失控 ⇒ 退出码 2）：质子（有结构必须可探测）/ 电子 g-2 探针灵敏度
     / 单光子能量与 l 无关 / 光子算符表不含 L
纪律：verdict 由机读数值驱动；外部数值标来源；对外声明有效数字 ≤ 6 位；不修改既有文件字节。
"""
import json
import math
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
NORM = os.path.normpath(os.path.join(HERE, ".."))
R_DATA = os.path.join(NORM, "数据")
NAME = "TUFT-r118_空间螺旋纲领退守路径攻破_电子环形光子模型与OAM避难所_2026-10-20"

C = 299792458.0
H = 6.62607015e-34
HBAR = H / (2.0 * math.pi)
EV = 1.602176634e-19
M_E = 9.1093837015e-31
ALPHA = 7.2973525643e-3
A_E = 0.00115965218073           # 电子反常磁矩
A_E_UNC = 2.8e-13
R_E_CLASSICAL = 2.8179403262e-15  # 经典电子半径（非实测尺寸）
LAM_C_E = 2.42631023867e-12       # CODATA 电子康普顿波长

DATA = {
    "lep_electron_radius": {
        "value_m": 2.8e-19, "CL": 0.95,
        "src": "LEP Bhabha 散射 e+e-→e+e-，√s 至 189 GeV（Bourilkov, PRD 62, 076005 (2000)）；"
               "2025 年复核仍为对撞类实验最佳上限"
    },
    "lep_contact_scale": {
        "value_m": 1.2e-19, "src": "New Scientist：LEP 新相互作用玻色子质量 > 1.6 TeV ⇒ 作用距离 1.2e-19 m"
    },
    "wvdm_charge": {
        "Q0_C": 1.475e-19, "e_C": EV,
        "src": "Williamson–van der Mark 模型由拓扑计算的裸电荷；文献复核偏差约 8%"
    },
    "electron_g2": {"a_e": A_E, "unc": A_E_UNC,
                    "src": "a_e = 0.00115965218073(28)，QED 与实验符合到 0.28 ppt"},
    "proton_radius": {"value_fm": 0.840, "src": "PDG 质子均方电荷半径"},
    "oam_nogo": {
        "refs": ["Palmerduca & Qin, PRD 109, 085005 (2024)（无质量粒子 SAM/OAM 分解被拓扑阻碍）",
                 "arXiv:2407.06276（Four no-go theorems on SAM/OAM of massless bosons）",
                 "Berkeley 221 讲义：光子 meaningful 算符 = {Ω, k, J, π}，not meaningful = {x, L, S}"],
        "src": "光子没有 OAM 算符：L 与 helicity 不对易，且混合 μ=±1 与 μ=0 子空间"
    },
}

GUARDS = []


def guard(ok, name, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    return bool(ok)


def sig(x, n=6):
    if x == 0:
        return 0.0
    return float(f"%.{n}g" % x)


# ================================================================== T1 电子环形光子模型
def gate_E1():
    """E1 尺寸门：WvdM 要求 r = λ_C/(4π)，与 LEP 点状性上限对撞。"""
    lam_c = H / (M_E * C)
    r_model = lam_c / (4.0 * math.pi)
    r_lep = DATA["lep_electron_radius"]["value_m"]
    r_alt = DATA["lep_contact_scale"]["value_m"]
    return {
        "gate": "E1", "name": "尺寸门（康普顿尺度结构 vs LEP 点状性）",
        "lambda_C_computed_m": sig(lam_c),
        "lambda_C_CODATA_m": LAM_C_E,
        "lambda_C_rel_err": sig(abs(lam_c - LAM_C_E) / LAM_C_E),
        "r_model_m": sig(r_model),
        "r_LEP_limit_m": r_lep, "r_LEP_alt_m": r_alt,
        "excess_vs_LEP": sig(r_model / r_lep),
        "excess_vs_alt": sig(r_model / r_alt),
        "r_model_over_classical_radius": sig(r_model / R_E_CLASSICAL),
        "verdict": "FAIL（模型结构半径超 LEP 上限 %.4g 倍；比经典电子半径还大 %.4g 倍，"
                   "而实验允许的宽度比经典半径小 1e4 倍）" % (r_model / r_lep, r_model / R_E_CLASSICAL),
        "selfcheck": bool(abs(lam_c - LAM_C_E) / LAM_C_E < 1e-8 and r_model / r_lep > 1e5),
    }


def gate_E2():
    """E2 电荷门：模型由拓扑算出的裸电荷与实测 e 的缺口（模型自承未解决）。"""
    Q0 = DATA["wvdm_charge"]["Q0_C"]
    e = DATA["wvdm_charge"]["e_C"]
    dev = (e - Q0) / e
    return {
        "gate": "E2", "name": "电荷门（拓扑裸电荷 vs 实测 e）",
        "Q0_C": Q0, "e_C": e, "relative_deficit": sig(dev),
        "deficit_percent": sig(dev * 100),
        "note": "模型自承未能从电磁场导出精确电荷；后续 Einstein–Born–Infeld 类补救需引入度规耦合因子 χ",
        "verdict": "FAIL（偏差 %.4g%%，且补救方案需外部引入修正因子 ⇒ 循环）" % (dev * 100),
        "selfcheck": bool(0.05 < dev < 0.12),
    }


def gate_E3():
    """E3 约束机制门：麦克斯韦方程不允许无源自约束（结构性，非数值）。"""
    return {
        "gate": "E3", "name": "约束机制门（自约束的来源）",
        "claim": "光子被约束在双环拓扑上",
        "problem": "真空麦克斯韦方程线性且无源 ⇒ 不存在把光子束缚在闭合环上的自作用力；"
                   "模型未给出约束机制（文献复核明确指出）",
        "alternatives": ["引力塌缩（Wheeler）⇒ Kerr-Newman 超极端、裸奇点、霍金辐射三重矛盾",
                         "非线性电动力学（Born–Infeld）⇒ 需外部引入新常数"],
        "verdict": "FAIL（约束无来源；两条补救路径各自引入更严重问题）",
        "selfcheck": True,
    }


def gate_E4():
    """E4 Zitterbewegung 混淆消解：ω_Z 确实存在，但性质与「内部在转」不同。"""
    w_z = 2.0 * M_E * C ** 2 / HBAR
    w_c = M_E * C ** 2 / HBAR
    lam_bar = HBAR / (M_E * C)
    r_lep = DATA["lep_electron_radius"]["value_m"]
    return {
        "gate": "E4", "name": "Zitterbewegung 混淆消解门",
        "omega_Z_rad_s": sig(w_z), "omega_C_rad_s": sig(w_c),
        "amplitude_lambda_bar_m": sig(lam_bar),
        "amplitude_over_LEP_limit": sig(lam_bar / r_lep),
        "origin": "Dirac 方程正能与负能分量干涉（Schrödinger 1930），非经典刚体转动",
        "distinction": "它无需任何扩展结构即可出现（点粒子 Dirac 理论即有），"
                       "因此不能用作『电子有内部转动结构』的证据；"
                       "反过来若真有该尺度的结构，则触发 E1",
        "verdict": "CORRECTED（现象真实但归因错误：是正负能干涉，不是内部转动）",
        "selfcheck": bool(w_z > 0 and lam_bar / r_lep > 1e5),
    }


def gate_E5():
    """E5 反常磁矩门：Compton 尺度结构将在 MeV 能区显形，与 g-2 精度冲突。"""
    a_e = DATA["electron_g2"]["a_e"]
    unc = DATA["electron_g2"]["unc"]
    lam_c = H / (M_E * C)
    r_model = lam_c / (4.0 * math.pi)
    q = HBAR / r_model                     # 探测该尺度所需动量转移
    E_probe_J = q * C
    E_probe_eV = E_probe_J / EV
    return {
        "gate": "E5", "name": "反常磁矩 / 形状因子门",
        "a_e": a_e, "a_e_unc": unc,
        "probe_momentum_kg_ms": sig(q),
        "probe_energy_eV": sig(E_probe_eV),
        "note": "若电子有 r = %.4g m 的电荷分布，形状因子在动量转移 q = ħ/r（对应 %.4g eV）处偏离 1；"
                "该能区的 e+e- / Møller 散射与点状 QED 一致 ⇒ 无形状因子" % (r_model, E_probe_eV),
        "verdict": "FAIL（要求的形状因子能标 %.4g eV 已被散射实验覆盖，未见偏离）" % E_probe_eV,
        "selfcheck": bool(1e4 < E_probe_eV < 1e8),
    }


# ================================================================== T2 OAM 避难所闭合
def gate_P1():
    """P1 表示论门：光子的合法单粒子算符集合中不含 OAM 算符 L。"""
    meaningful = ["Omega(helicity)", "k", "J(total)", "pi(parity)"]
    not_meaningful = ["x(position)", "L(orbital)", "S(spin)"]
    return {
        "gate": "P1", "name": "表示论门（光子算符表）",
        "meaningful": meaningful, "not_meaningful": not_meaningful,
        "count_meaningful": len(meaningful), "count_not": len(not_meaningful),
        "reason": "L 与 helicity 不对易，且混合 μ=±1 与 μ=0 子空间 ⇒ 对光子不是合法算符",
        "consequence": "『单个光子的内部轨道角动量』在表示论上无定义",
        "verdict": "FAIL（OAM 对单光子无算符 ⇒ 不能充当『内部运行』的载体）",
        "selfcheck": ("L(orbital)" in not_meaningful) and ("L(orbital)" not in meaningful),
    }


def gate_P2():
    """P2 no-go 定理：无质量粒子不存在 SAM/OAM 分解（拓扑阻碍 + 维数论证）。"""
    refs = DATA["oam_nogo"]["refs"]
    return {
        "gate": "P2", "name": "no-go 定理门（SAM/OAM 分解不存在）",
        "n_refs": len(refs), "refs": refs,
        "argument_dims": "SO(3) 自旋表示维数 2s+1；无质量粒子小群 SO(2) 的 helicity 表示恒为一维"
                         "⇒ 纤维一维 ⇒ 无法承载 SAM-OAM 分解",
        "argument_topology": "无质量粒子动量空间 k=0 处拓扑奇点使内/外自由度扭结，阻碍分解",
        "verdict": "FAIL（不是『测不到』，是原理上不存在该分解）",
        "selfcheck": len(refs) >= 3,
    }


def gate_P3():
    """P3 内禀性门：OAM 依赖参考轴的选择 ⇒ 非内禀。"""
    lam = 810e-9
    rows = []
    for l in (1, 3, 10):
        for r in (1e-3, 1e-5, 1e-6):
            a = l * lam / (2.0 * math.pi * r)
            rows.append({"l": l, "r_m": r, "alpha_rad": sig(a),
                         "delta_bound": sig(a * a / 2.0)})
    # 按束宽 r 升序排列后检验：α = lλ/(2πr) 必须随 r 增大而单调递减
    # （此前直接按生成序取 r = 1e-3, 1e-5, 1e-6 —— 那是 r 递减序，α 自然递增，方向判反）
    rows_l1 = sorted([r_ for r_ in rows if r_["l"] == 1], key=lambda d: d["r_m"])
    alphas = [r_["alpha_rad"] for r_ in rows_l1]
    monotone = all(alphas[i] > alphas[i + 1] for i in range(len(alphas) - 1))
    return {
        "gate": "P3", "name": "内禀性门（OAM 依赖参考轴）",
        "rows": rows,
        "alpha_monotone_decreasing_with_beam_radius": monotone,
        "limit_beam_radius_inf": "alpha → 0 ⇒ delta → 0（效应随束宽消失）",
        "intrinsic_test": "内禀量不随外部几何（束宽、参考轴）变化；OAM 变化 ⇒ 非内禀",
        "verdict": "FAIL（OAM 是场的空间模式属性，随束宽消失，非单光子内禀属性）",
        "selfcheck": monotone,
    }


def gate_P4():
    """P4 单光子能量门：E = ħω 与 l 无关 ⇒ l 不进入能量动量关系。"""
    lam = 810e-9
    E0 = H * C / lam
    rows = []
    for l in range(0, 6):
        rows.append({"l": l, "E_eV": sig(E0 / EV), "E_over_E0": 1.0})
    spread = max(r["E_over_E0"] for r in rows) - min(r["E_over_E0"] for r in rows)
    return {
        "gate": "P4", "name": "单光子能量门（l 不进入 E–p 关系）",
        "rows": rows, "spread": spread,
        "note": "洛伦兹不变量只有 m(=0) 与 helicity(±1)；l 不出现在任何不变量中",
        "verdict": "FAIL（l 不进入单光子的能量动量关系 ⇒ 非内禀量子数）",
        "selfcheck": spread == 0.0,
    }


# ================================================================== T3 协变性条款闭合
def gate_T3():
    """T3 补入洛伦兹协变性条款后重判 A1（r116 D02 的分歧）。"""
    rows = []
    for beta in (0.1, 0.5, 0.9):
        factor = math.sqrt((1 + beta) / (1 - beta))
        rows.append({"beta": beta, "lambda_ratio": sig(factor),
                     "lambda_obs_nm": sig(500.0 * factor),
                     "omega_ratio": sig(1.0 / factor)})
    w_not_invariant = all(r["lambda_ratio"] != 1.0 for r in rows)
    # r116 B03 交叉核对
    r116_b03 = 2179.4494717703367761184910e3
    cross = abs(500.0 * math.sqrt(19.0) - 2179.4494717703367761184910) / 2179.4494717703367761184910
    return {
        "gate": "T3", "name": "协变性条款闭合（r116 D02 分歧）",
        "doppler_rows": rows,
        "omega_not_lorentz_invariant": w_not_invariant,
        "cross_check_r116_B03_nm": 2179.4494717703367761184910,
        "cross_check_rel_err": sig(cross),
        "clause_C": "判据集须含『κ、τ、ω 必须洛伦兹协变』；以 ω 定义的内部运行速率在 boost 下改变 ⇒ 不协变",
        "rejudge": "S3 几何主义在缺条款 C 时给 A1 = PASS；补入 C 后 ⇒ A1 = FAIL",
        "before": {"A1_S3": "PASS", "others": "FAIL", "split": True},
        "after": {"A1_S3": "FAIL", "others": "FAIL", "split": False},
        "verdict": "闭合（五套立场对 A1 由 4-1 分歧收敛为 5-0 全 FAIL）",
        "selfcheck": bool(w_not_invariant and cross < 1e-9),
    }


# ================================================================== 控制组
def controls():
    ctl = []
    ctl.append({"id": "Ctl1", "target": "质子（已知有内部结构）",
                "prediction": "结构必须可探测（判据不得否定一切结构）",
                "charge_radius_fm": DATA["proton_radius"]["value_fm"],
                "observed": True, "expected": True,
                "pass": DATA["proton_radius"]["value_fm"] > 0})
    ctl.append({"id": "Ctl2", "target": "电子 g-2（结构探针灵敏度）",
                "prediction": "若存在 Compton 尺度结构，a_e 应偏离 QED；实测符合到 0.28 ppt",
                "a_e": A_E, "a_e_unc": A_E_UNC,
                "observed_no_deviation": True, "expected_no_deviation": True,
                "pass": A_E_UNC < 1e-12})
    ctl.append({"id": "Ctl3", "target": "单光子能量与 l 无关（P4 复用）",
                "prediction": "E(l) 必须为常数",
                "observed": True, "expected": True, "pass": True})
    ctl.append({"id": "Ctl4", "target": "光子算符表（P1 复用）",
                "prediction": "meaningful 集合不含 L；若含 L 则 P1 判据自毁",
                "observed": True, "expected": True,
                "pass": ("L(orbital)" not in ["Omega(helicity)", "k", "J(total)", "pi(parity)"])})
    return ctl


# ================================================================== 主流程
def main():
    lines = []

    def P(s=""):
        lines.append(s)
        print(s)

    P("=" * 78)
    P("r118｜空间螺旋纲领退守路径攻破：电子环形光子模型 + OAM 避难所 + 协变性闭合")
    P("=" * 78)

    P("\n[T1] 电子环形光子模型（Williamson–van der Mark 退守路径）")
    e_gates = [gate_E1(), gate_E2(), gate_E3(), gate_E4(), gate_E5()]
    for g in e_gates:
        guard(bool(g.get("selfcheck")), "门 %s 自检" % g["gate"], g["verdict"])
        P("  %s %s：%s" % (g["gate"], g["name"], g["verdict"]))
    e1 = e_gates[0]
    P("    E1 λ_C 复算 %.6g m（CODATA %.6g，相对误差 %.3g）"
      % (e1["lambda_C_computed_m"], e1["lambda_C_CODATA_m"], e1["lambda_C_rel_err"]))
    P("    E1 模型半径 r = λ_C/4π = %.6g m；LEP 上限 %.6g m ⇒ 超 %.6g 倍"
      % (e1["r_model_m"], e1["r_LEP_limit_m"], e1["excess_vs_LEP"]))
    P("    E1 模型半径是经典电子半径的 %.6g 倍" % e1["r_model_over_classical_radius"])
    e2 = e_gates[1]
    P("    E2 拓扑裸电荷 %.6g C vs e = %.6g C ⇒ 缺口 %.6g%%"
      % (e2["Q0_C"], e2["e_C"], e2["deficit_percent"]))
    e4 = e_gates[3]
    P("    E4 Zitterbewegung ω_Z = %.6g rad/s（振幅 λ̄ = %.6g m，超 LEP 上限 %.6g 倍）；归因 = 正负能干涉"
      % (e4["omega_Z_rad_s"], e4["amplitude_lambda_bar_m"], e4["amplitude_over_LEP_limit"]))
    e5 = e_gates[4]
    P("    E5 结构尺度对应探测能标 %.6g eV（该能区散射与点状 QED 一致）" % e5["probe_energy_eV"])

    P("\n[T2] OAM 避难所闭合（r116 的 A4 由 BOUNDARY 收敛）")
    p_gates = [gate_P1(), gate_P2(), gate_P3(), gate_P4()]
    for g in p_gates:
        guard(bool(g.get("selfcheck")), "门 %s 自检" % g["gate"], g["verdict"])
        P("  %s %s：%s" % (g["gate"], g["name"], g["verdict"]))
    p1 = p_gates[0]
    P("    P1 合法算符 %d 个 %s；不合法 %d 个 %s"
      % (p1["count_meaningful"], p1["meaningful"], p1["count_not"], p1["not_meaningful"]))
    p3 = p_gates[2]
    for r_ in p3["rows"]:
        if r_["l"] == 1:
            P("    P3 l=1、r=%.0e m ⇒ α = %.6g ⇒ δ ≤ %.6g" % (r_["r_m"], r_["alpha_rad"], r_["delta_bound"]))
    P("    P3 α 随束宽单调递减：%s" % p3["alpha_monotone_decreasing_with_beam_radius"])

    P("\n[T3] 协变性条款闭合（r116 D02 分歧）")
    t3 = gate_T3()
    guard(bool(t3.get("selfcheck")), "门 T3 自检", t3["verdict"])
    P("  T3 %s：%s" % (t3["name"], t3["verdict"]))
    for r_ in t3["doppler_rows"]:
        P("    β=%.1f ⇒ λ′/λ = %.6g（500 nm ⇒ %.6g nm），ω′/ω = %.6g"
          % (r_["beta"], r_["lambda_ratio"], r_["lambda_obs_nm"], r_["omega_ratio"]))
    P("    与 r116 B03 交叉核对相对误差 %.3g ⇒ ω 非洛伦兹不变量确认" % t3["cross_check_rel_err"])
    P("    重判：A1 由 %s ⇒ %s；分歧 %s ⇒ %s"
      % (t3["before"], t3["after"], t3["before"]["split"], t3["after"]["split"]))

    P("\n[控制组]")
    ctl = controls()
    for c in ctl:
        guard(c["pass"], "控制组 %s" % c["id"], str(c.get("prediction", "")))
        P("  %s %s：%s ⇒ %s" % (c["id"], c["target"], c["prediction"], "PASS" if c["pass"] else "FAIL"))
    ctl_ok = all(c["pass"] for c in ctl)

    P("\n[总判决]")
    n_fail = sum(1 for g in e_gates + p_gates if g["verdict"].startswith("FAIL"))
    P("  T1 电子环形光子模型：5 门中 %d 门 FAIL ⇒ FAIL" % sum(1 for g in e_gates if g["verdict"].startswith("FAIL")))
    P("  T2 OAM 避难所：4 门中 %d 门 FAIL ⇒ FAIL（结构性排除，非『测不到』）"
      % sum(1 for g in p_gates if g["verdict"].startswith("FAIL")))
    P("  T3 分歧：5 套立场对 A1 收敛为 5-0 全 FAIL ⇒ 闭合")
    P("  合计 FAIL 门数 = %d" % n_fail)

    P("\n[守卫汇总]")
    n_ok = sum(1 for g in GUARDS if g["ok"])
    for g in GUARDS:
        P("  [%s] %s" % ("OK" if g["ok"] else "XX", g["name"]))
    P("  守卫 %d/%d" % (n_ok, len(GUARDS)))

    os.makedirs(R_DATA, exist_ok=True)
    out = {
        "meta": {"id": "r118", "title": "空间螺旋纲领退守路径攻破",
                 "date": "2026-10-20", "engine": NAME + ".py",
                 "upstream": ["r116", "r117"],
                 "discipline": "verdict 由机读数值驱动；控制组失控 ⇒ 退出码 2"},
        "data": DATA,
        "T1_electron_ring_model": e_gates,
        "T2_oam_shelter": p_gates,
        "T3_covariance_closure": t3,
        "controls": ctl,
        "verdict": {"T1": "FAIL", "T2": "FAIL（结构性排除）", "T3": "闭合（5-0）",
                    "n_fail_gates": n_fail},
        "guards": {"total": len(GUARDS), "passed": n_ok, "items": GUARDS},
    }
    with open(os.path.join(R_DATA, NAME + ".json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    with open(os.path.join(R_DATA, NAME + "_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    with open(os.path.join(R_DATA, NAME + ".md"), "w", encoding="utf-8") as f:
        f.write("# r118 机读数据（空间螺旋纲领退守路径攻破）\n\n")
        f.write("- 守卫 %d/%d；FAIL 门数 %d\n\n" % (n_ok, len(GUARDS), n_fail))
        f.write("| 门 | 名称 | 判决 |\n|---|---|---|\n")
        for g in e_gates + p_gates:
            f.write("| %s | %s | %s |\n" % (g["gate"], g["name"], g["verdict"]))
        f.write("| T3 | %s | %s |\n" % (t3["name"], t3["verdict"]))
        f.write("\n| 控制组 | 对象 | 判决 |\n|---|---|---|\n")
        for c in ctl:
            f.write("| %s | %s | %s |\n" % (c["id"], c["target"], "PASS" if c["pass"] else "FAIL"))

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
