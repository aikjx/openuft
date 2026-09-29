# -*- coding: utf-8 -*-
"""
TUFT 双分量干涉屏蔽因子：全维求导、归一化、量纲与联合约束门禁。

范围：核验候选
    r = tau/kappa
    s(r) = r/(1+r)
    F_g(r) = 1-s(r)^2
    F_d(r) = (1-r)/(1+r)
是否能在保持公理 A 与现有 EC-TUFT 方程不变时同时通过电子 g-2 与 EDM。

红线：代数可拟合不等于第一性预言；条件二能级模型不等于已存在的场解；
本脚本不新增场、不拟合新常数，也不覆盖 OPEN5/OPEN6 历史判定。
"""
from __future__ import print_function

import math
import os
import sys
from collections import Counter

import mpmath as mp
import sympy as sp

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
RUNLOG = os.path.normpath(os.path.join(HERE, "..", "..", "09_验证结果", "原始运行记录"))
REPORT_PATH = os.path.join(
    RUNLOG if os.path.isdir(RUNLOG) else HERE,
    "tuft_v2screen_双分量二次型_量纲与归一化门禁_report.txt",
)

G2_EXP_TEXT = "0.00231930436"
G2_EXP = mp.mpf(G2_EXP_TEXT)
R_OLD = mp.mpf("0.00202")
ALPHA = mp.mpf("7.2973525693e-3")
M_E = mp.mpf("9.1093837139e-31")
C_LIGHT = mp.mpf("299792458")
E_CHARGE = mp.mpf("1.602176634e-19")
HBAR = mp.mpf("1.054571817e-34")
EDM_ACME_ECM = mp.mpf("1.1e-29")


class Report(object):
    def __init__(self):
        self.rows = []
        self.lines = []

    def echo(self, text=""):
        print(text)
        self.lines.append(text)

    def section(self, title):
        self.echo("")
        self.echo("=" * 78)
        self.echo(title)
        self.echo("=" * 78)

    def add(self, sec, name, verdict, detail=""):
        self.rows.append((sec, name, verdict, detail))
        line = "  [" + verdict + "] " + name
        if detail:
            line += "  |  " + detail
        self.echo(line)

    def summary(self):
        counts = Counter(row[2] for row in self.rows)
        self.section("汇总")
        for verdict in ["PASS", "FAIL", "BOUNDARY", "INFO"]:
            self.echo("  %-9s = %d" % (verdict, counts.get(verdict, 0)))
        self.echo("")
        self.echo("  结论：候选函数的代数根存在，但旧分支不被屏蔽；EDM 量纲与联合约束失败；")
        self.echo("        公理 A/稳态条件只给恒等约束，不能导出双分量振幅、相位或屏蔽函数。")
        return counts

    def dump(self):
        with open(REPORT_PATH, "w", encoding="utf-8") as handle:
            handle.write("\n".join(self.lines) + "\n")
        print("\n  [report] " + REPORT_PATH)


def mp_text(value, digits=16):
    return mp.nstr(value, digits)


def candidate_values(r_value):
    s_value = r_value / (1 + r_value)
    f_g_value = 1 - s_value ** 2
    f_d_value = (1 - r_value) / (1 + r_value)
    g_value = 2 * r_value * f_g_value
    return s_value, f_g_value, f_d_value, g_value


def part1_candidate_algebra(rep):
    rep.section("§1 候选函数的符号求导、唯一根与旧分支回代")
    r, g_star = sp.symbols("r g_star", positive=True)
    s = r / (1 + r)
    f_g = sp.factor(1 - s ** 2)
    f_d = (1 - r) / (1 + r)
    g_map = sp.factor(2 * r * f_g)
    dg = sp.factor(sp.diff(g_map, r))
    df_g = sp.factor(sp.diff(f_g, r))

    rep.echo("  s(r)   = %s" % s)
    rep.echo("  F_g(r) = %s" % f_g)
    rep.echo("  F_d(r) = %s" % f_d)
    rep.echo("  G(r)   = 2rF_g = %s" % g_map)
    rep.echo("  G'(r)  = %s" % dg)
    rep.echo("  F_g'(r)= %s" % df_g)

    algebra_ok = sp.simplify(f_g - (1 + 2 * r) / (1 + r) ** 2) == 0
    rep.add("D1", "候选 F_g 化简", "PASS" if algebra_ok else "FAIL",
            "F_g=(1+2r)/(1+r)^2=1-r^2/(1+r)^2")

    derivative_ok = sp.simplify(dg - (2 + 6 * r) / (1 + r) ** 3) == 0
    rep.add("D2", "G'(r)>0，正根至多一个", "PASS" if derivative_ok else "FAIL",
            "r>0 时 (2+6r)/(1+r)^3>0；G(0)=0，G(∞)=4")

    mp.mp.dps = 80
    a = 4 - G2_EXP
    b = 2 - 2 * G2_EXP
    root = (-b + mp.sqrt(b * b + 4 * a * G2_EXP)) / (2 * a)
    s_root, f_g_root, f_d_root, g_root = candidate_values(root)
    residual = abs(g_root - G2_EXP)
    rep.echo("  唯一正根 r*       = " + mp_text(root, 30))
    rep.echo("  F_g(r*)           = " + mp_text(f_g_root, 30))
    rep.echo("  1-F_g(r*)         = " + mp_text(1 - f_g_root, 12))
    rep.echo("  |G(r*)-g_exp|     = " + mp_text(residual, 8))
    rep.add("D3", "候选方程的实验匹配根", "PASS" if residual < mp.mpf("1e-70") else "FAIL",
            "r*=0.0011596537358879，但 F_g=0.9999986583，屏蔽仅 1.34e-6")

    s_old, f_g_old, _, g_old = candidate_values(R_OLD)
    required_f = G2_EXP / (2 * R_OLD)
    required_s_unnormalized = mp.sqrt(1 - required_f)
    rep.echo("  旧 r0=0.00202: s=%.12f, F_g=%.12f, G=%.12f" % (
        float(s_old), float(f_g_old), float(g_old)))
    rep.echo("  旧 r0 若靠 1-s^2 匹配实验，需 s=%.9f" % float(required_s_unnormalized))
    old_fails = abs(g_old - G2_EXP) / G2_EXP > mp.mpf("0.5")
    rep.add("D4", "候选函数不能屏蔽旧 r0 分支", "FAIL" if old_fails else "PASS",
            "G(r0)=0.0040399836，仍比实验高 74.2%；匹配来自重定 r，不来自屏蔽")

    is_derivative = sp.simplify(df_g - f_d) == 0
    rep.add("D5", "EDM 因子 F_d 是否为 F_g 的导数", "PASS" if is_derivative else "FAIL",
            "dF_g/dr=-2r/(1+r)^3，与 (1-r)/(1+r) 不同；F_d 是第二个独立 ansatz")

    return root, f_d_root


def part2_normalized_two_component(rep):
    rep.section("§2 归一化双分量二次型与相位自由度")
    q, phi = sp.symbols("q phi", real=True)
    norm = sp.sqrt(1 + q ** 2)
    psi = sp.Matrix([1 / norm, q * (sp.cos(phi) + sp.I * sp.sin(phi)) / norm])
    sigma1 = sp.Matrix([[0, 1], [1, 0]])
    sigma2 = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    sigma3 = sp.Matrix([[1, 0], [0, -1]])

    state_norm = sp.simplify((sp.conjugate(psi).T * psi)[0].rewrite(sp.exp))
    exp1 = sp.simplify((sp.conjugate(psi).T * sigma1 * psi)[0].rewrite(sp.exp))
    exp2 = sp.simplify((sp.conjugate(psi).T * sigma2 * psi)[0].rewrite(sp.exp))
    exp3 = sp.simplify((sp.conjugate(psi).T * sigma3 * psi)[0].rewrite(sp.exp))
    expected1 = 2 * q * sp.cos(phi) / (1 + q ** 2)
    expected2 = 2 * q * sp.sin(phi) / (1 + q ** 2)
    expected3 = (1 - q ** 2) / (1 + q ** 2)
    pauli_ok = (sp.simplify(state_norm - 1) == 0 and
                sp.trigsimp(exp1 - expected1) == 0 and
                sp.trigsimp(exp2 - expected2) == 0 and
                sp.simplify(exp3 - expected3) == 0)
    rep.add("N1", "归一化二分量的 Pauli 二次型", "PASS" if pauli_ok else "FAIL",
            "<σ1>=2s cosφ/(1+s²)，<σ2>=2s sinφ/(1+s²)，<σ3>=(1-s²)/(1+s²)")

    proposal = 1 - q ** 2
    normalized = expected3
    hidden_norm = sp.simplify(proposal - normalized)
    rep.echo("  提案 F_g - 归一化相反流因子 = %s" % hidden_norm)
    rep.add("N2", "提案 F_g=1-s² 的归一化守恒", "FAIL" if hidden_norm != 0 else "PASS",
            "A+=1、A-=s 时总范数=1+s²；固定总范数后应为 (1-s²)/(1+s²)")

    rep.add("N3", "EDM 与相对相位的条件关系", "BOUNDARY",
            "若 CP-odd 算符映为 σ2，则实驻波 φ=0/π 给 EDM=0；但该算符映射尚未由 TUFT 作用量推出")


def part3_joint_constraint(rep, root, f_d_root):
    rep.section("§3 g−2 与 OPEN6 EDM 的联合约束 no-go（针对本候选）")
    lambda_c = HBAR / (M_E * C_LIGHT)
    edm_open6 = ALPHA * (lambda_c * 100) / (2 * mp.sqrt(1 + ALPHA ** 2))
    f_d_required = EDM_ACME_ECM / edm_open6
    screened_edm = edm_open6 * abs(f_d_root)
    over = screened_edm / EDM_ACME_ECM
    r_edm = (1 - f_d_required) / (1 + f_d_required)
    _, _, _, g_at_edm = candidate_values(r_edm)

    rep.echo("  OPEN6 基线 EDM       = %s e·cm" % mp_text(edm_open6, 12))
    rep.echo("  ACME 所需 |F_d|      <= %s" % mp_text(f_d_required, 12))
    rep.echo("  g−2 唯一根上的 F_d  = %s" % mp_text(f_d_root, 12))
    rep.echo("  屏蔽后 EDM            = %s e·cm" % mp_text(screened_edm, 12))
    rep.echo("  仍超 ACME             = %s 倍" % mp_text(over, 12))
    rep.echo("  若令 F_d 达 ACME，r   = %s" % mp_text(r_edm, 35))
    rep.echo("  该 r 下 G(r)          = %s（实验值的 %s 倍）" % (
        mp_text(g_at_edm, 16), mp_text(g_at_edm / G2_EXP, 12)))

    joint_fails = abs(f_d_root) > f_d_required and abs(g_at_edm - G2_EXP) > G2_EXP
    rep.add("J1", "候选 F_g、F_d 是否存在共同 r", "FAIL" if joint_fails else "PASS",
            "G 严格单调使 g−2 根唯一；该根 F_d=0.997683，而 EDM 要求 ≤7.81e-17")
    rep.add("J2", "EDM 零点与 g−2 根分离", "INFO",
            "F_d 的零点 r=1；该处提案 G=1.5，约为实验值 647 倍")


def part4_dimension_gate(rep, root):
    rep.section("§4 EDM 量纲账本、代数化简与最有利尺度修复")
    dim_kappa_tau = (0, -2)
    dim_e_hbar_over_mc = (1, 1)
    got = (dim_kappa_tau[0] + dim_e_hbar_over_mc[0],
           dim_kappa_tau[1] + dim_e_hbar_over_mc[1])
    expected = (1, 1)
    gamma_needed = (expected[0] - got[0], expected[1] - got[1])
    rep.echo("  维度元组按 (C指数, L指数) 记：")
    rep.echo("  [κτ]=" + str(dim_kappa_tau) + "，[eħ/(m_ec)]=" + str(dim_e_hbar_over_mc))
    rep.echo("  乘积=" + str(got) + "；EDM 应为=" + str(expected) + "；故 [γ]=" + str(gamma_needed))
    rep.add("U1", "EDM 量纲账本", "PASS" if gamma_needed == (0, 2) else "FAIL",
            "γ 必须具有 L²；无量纲 γ 的候选式结果为 C/m")
    rep.add("U2", "无量纲 γ 的 EDM 公式", "FAIL" if got != expected else "PASS",
            "与 EDM 的 C·m 量纲不符，不能和 ACME 上限比较")

    r = sp.symbols("r", positive=True)
    right_factor = r * (1 - r) / ((1 + r ** 2) * (1 + r))
    claimed_factor = r * (1 - r) / (1 + r) ** 3
    ratio = sp.factor(right_factor / claimed_factor)
    algebra_differs = sp.simplify(right_factor - claimed_factor) != 0
    rep.echo("  正确无量纲因子 = r(1-r)/[(1+r²)(1+r)]")
    rep.echo("  提案所写因子   = r(1-r)/(1+r)^3")
    rep.echo("  正确/提案比值  = %s" % ratio)
    rep.add("U3", "代入公理 A 后的 EDM 化简", "PASS" if algebra_differs else "FAIL",
            "提案把 (1+r²)(1+r) 错化为 (1+r)^3；两式并不恒等")

    lambda_c = HBAR / (M_E * C_LIGHT)
    f_d = (1 - root) / (1 + root)
    right_numeric = root * (1 - root) / ((1 + root ** 2) * (1 + root))
    coeff_c_per_m = M_E * C_LIGHT * E_CHARGE / HBAR
    unclosed_value = coeff_c_per_m * right_numeric
    edm_gamma_lc2_ecm = lambda_c * 100 * right_numeric
    over = edm_gamma_lc2_ecm / EDM_ACME_ECM
    gamma_max = EDM_ACME_ECM * E_CHARGE / 100 / unclosed_value
    gamma_ratio = gamma_max / lambda_c ** 2
    rep.echo("  m_ec e/ħ              = %s C/m" % mp_text(coeff_c_per_m, 12))
    rep.echo("  F_d(r*)               = %s" % mp_text(f_d, 12))
    rep.echo("  γ=λ_C² 时 EDM         = %s e·cm" % mp_text(edm_gamma_lc2_ecm, 12))
    rep.echo("  超 ACME               = %s 倍" % mp_text(over, 12))
    rep.echo("  达标需 γ              < %s m²" % mp_text(gamma_max, 12))
    rep.echo("  即 γ/λ_C²             < %s" % mp_text(gamma_ratio, 12))
    rep.add("U4", "用既有康普顿尺度补齐 γ 后的 EDM", "FAIL" if over > 1 else "PASS",
            "仍超 ACME 4.06e15 倍；需另加 2.46e-16 的面积抑制")


def part5_axiom_and_freedom(rep):
    rep.section("§5 公理 A、稳态条件与功能自由度")
    x = sp.symbols("x", real=True)
    omega = sp.symbols("Omega", positive=True, constant=True)
    q = sp.Function("r")(x)
    kappa = omega / sp.sqrt(1 + q ** 2)
    tau = omega * q / sp.sqrt(1 + q ** 2)
    axiom_residual = sp.simplify(kappa ** 2 + tau ** 2 - omega ** 2)
    steady_residual = sp.simplify(kappa * sp.diff(kappa, x) + tau * sp.diff(tau, x))
    rep.echo("  κ=Ω/sqrt(1+r²)，τ=Ωr/sqrt(1+r²)")
    rep.echo("  公理 A 残差                    = %s" % axiom_residual)
    rep.echo("  κ∂κ+τ∂τ（允许 r=r(x)）残差    = %s" % steady_residual)
    rep.add("A1", "公理 A 在 r 参数化下严格成立", "PASS" if axiom_residual == 0 else "FAIL",
            "对任意 r 恒等成立，故不能反向选择某个 r")
    rep.add("A2", "稳态梯度条件严格成立", "PASS" if steady_residual == 0 else "FAIL",
            "Ω 固定时即使 r 随位置变化也恒为 0；它是公理 A 的微分推论")

    z = sp.symbols("z", positive=True)
    candidates = [z / (1 + z), sp.tanh(z), z / sp.sqrt(1 + z ** 2)]
    limits = [sp.limit(item, z, 0, dir="+") for item in candidates]
    monotone = [sp.simplify(sp.diff(item, z)) for item in candidates]
    rep.echo("  同样满足 s(0)=0 且单调的无参数候选：")
    for index, item in enumerate(candidates):
        rep.echo("    s%d=%s，s%d(0+)=%s，s%d'=%s" % (
            index + 1, item, index + 1, limits[index], index + 1, monotone[index]))
    nonunique = len(set(str(item) for item in candidates)) == 3 and all(value == 0 for value in limits)
    rep.add("A3", "s(r)=r/(1+r) 的唯一可导出性", "FAIL" if nonunique else "PASS",
            "至少三种无参数函数满足同一极限与单调性；无场方程/边界条件不能唯一选择")


def part6_cross_checks(rep):
    rep.section("§6 场内容、β 跑动与 ringdown 的跨册边界")
    rep.add("X1", "不改现有 EC-TUFT 作用量时的第二传播模", "BOUNDARY",
            "当前 EC 挠率为代数约束；T² 不含 ∂T。新增连续 Ψ− 须先指出既有物质表示或修改动力学")
    rep.add("X2", "固定 r 对 β 跑动的影响", "INFO",
            "r 与 F_g(r) 均不含重整化能标 μ，故 μ·dr/dμ=0、β_r=0；不能补定理 N 的 M1/M2")
    rep.add("X3", "电子 r 向黑洞 QNM 的迁移", "INFO",
            "缺少 r 到反射壁位置/反射率/有效势的映射；OPEN_v3/v4 的 5.74σ 与尺度冲突结论不变")


def main():
    rep = Report()
    rep.echo("=" * 78)
    rep.echo("TUFT 双分量屏蔽因子：全维求导、归一化、量纲与联合约束门禁")
    rep.echo("run at: 2026-09-30")
    rep.echo("=" * 78)
    rep.echo("判据：只核验给定候选；不把数值拟合、函数选择或条件二能级模型冒充场方程推导。")

    root, f_d_root = part1_candidate_algebra(rep)
    part2_normalized_two_component(rep)
    part3_joint_constraint(rep, root, f_d_root)
    part4_dimension_gate(rep, root)
    part5_axiom_and_freedom(rep)
    part6_cross_checks(rep)
    rep.summary()
    rep.echo("")
    rep.echo("红线：本报告给出的是针对所提交 ansatz 的 no-go 与条件定理，不是否定所有可能的")
    rep.echo("双分量场模型。若未来从作用量唯一导出第二模、相位与流算符，必须作为新模型重新盲验。")
    rep.dump()


if __name__ == "__main__":
    main()
