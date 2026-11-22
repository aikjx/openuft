# -*- coding: utf-8 -*-
"""算法联盟 · 「从第一性原理找 G」可算审计（6 门，每门带负对照）。

核心问题：G 有量纲，「求 G」等价于求一个纯数 α_G = G m_p² /(ħc)，
即 m_p / M_Pl。唯一已知的第一性机制是 QCD 量纲嬗变：
    m_p ∝ Λ_QCD = M_Pl · exp(-2π / (b0 · α_s(M_Pl)))  （单圈示意）
本脚本量化：G 要算准，α_s(M_Pl) 需要给到几位。

非判定册 / 不占 RID / 不写 README。计算 != 证实。外部常数需对照一手来源复核。
用法:  python -I _alg_find_G_first_principles_audit.py
"""
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "数据" / "_ALG_find_G_first_principles_audit_2026-11-22.json"
gates = {}


def gate(name, ok, **kw):
    gates[name] = {"ok": bool(ok), **kw}


# ---------- 外部常数（CODATA 2022 / PDG 2024，需复核） ----------
G = 6.67430e-11; uG = 0.00015e-11          # m^3 kg^-1 s^-2
hbar = 1.054571817e-34; c = 299792458.0
m_p = 1.67262192595e-27                    # kg
GeV = 1.602176634e-10                      # J
M_Pl_GeV = math.sqrt(hbar * c / G) * c ** 2 / GeV
MZ, aZ, u_aZ = 91.1880, 0.1180, 0.0009
m_c, m_b, m_t = 1.27, 4.18, 172.57

# ---------- H1 量纲：{c, ħ} 生成不出 G ----------
# 列: c, hbar, G, m_p ; 行: M, L, T
D = sp.Matrix([[0, 1, -1, 1], [1, 2, 3, 0], [-1, -1, -2, 0]])
rank_c_hbar = D[:, :2].rank()
rank_with_G = D[:, :3].rank()
null_cphG = D[:, :3].nullspace()           # c,ħ,G 的无量纲组合
null_all = D.nullspace()                   # 加 m_p 后
gate("H1_G_not_from_c_hbar",
     rank_c_hbar == 2 and rank_with_G == 3 and len(null_cphG) == 0 and len(null_all) == 1,
     rank_c_hbar=int(rank_c_hbar), rank_c_hbar_G=int(rank_with_G),
     dimensionless_from_c_hbar_G=len(null_cphG),
     negative_control_add_m_p_dimensionless=len(null_all),
     reading="c、ħ 无论怎样组合都得不到 G；c、ħ、G 三者之间没有无量纲组合，G 只定义单位（普朗克单位）。"
             "加入 m_p 才出现唯一纯数 α_G：『求 G』在物理上就是『求 m_p/M_Pl』。")

# ---------- H2 目标纯数 ----------
alpha_G = G * m_p ** 2 / (hbar * c)
ratio = math.sqrt(alpha_G)
gate("H2_target_pure_number",
     5.8e-39 < alpha_G < 6.0e-39,
     alpha_G=alpha_G, m_p_over_M_Pl=ratio, M_Pl_GeV=M_Pl_GeV,
     ln_M_Pl_over_m_p=math.log(1 / ratio),
     reading="α_G ≈ 5.9e-39；ln(M_Pl/m_p) ≈ 44.0。任何『求出 G』的理论，必须给出这个 44 左右的对数，而不是 1 附近的数。")


# ---------- QCD 跑动（1 圈 / 2 圈，连续匹配，MSbar 示意） ----------
def betas(nf):
    b0 = 11 - 2 * nf / 3
    b1 = 102 - 38 * nf / 3
    return b0, b1


def nf_at(mu):
    return 3 if mu < m_c else 4 if mu < m_b else 5 if mu < m_t else 6


def run(a0, mu0, mu1, loops, n=40000):
    """在 t = ln μ 上用 RK4 积分 dα/dt = -b0 α²/2π - b1 α³/(8π²)。"""
    t0, t1 = math.log(mu0), math.log(mu1)
    h = (t1 - t0) / n
    a, t = a0, t0

    def f(t, a):
        b0, b1 = betas(nf_at(math.exp(t)))
        r = -b0 * a * a / (2 * math.pi)
        if loops == 2:
            r -= b1 * a ** 3 / (8 * math.pi ** 2)
        return r

    for _ in range(n):
        k1 = f(t, a); k2 = f(t + h / 2, a + h * k1 / 2)
        k3 = f(t + h / 2, a + h * k2 / 2); k4 = f(t + h, a + h * k3)
        a += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        t += h
        if a > 1.0 or a <= 0:
            return a, math.exp(t)
    return a, math.exp(t)


def scale_where_alpha_is_one(a_pl, loops):
    """从 M_Pl 向下跑，返回 α_s=1 的能标（强耦合标度的代理）。"""
    a, mu = run(a_pl, M_Pl_GeV, 0.05, loops, n=80000)
    return mu


# ---------- H3 由数据上跑得到 α_s(M_Pl)，并检查跑回自洽 ----------
a_pl_1, _ = run(aZ, MZ, M_Pl_GeV, 1)
a_pl_2, _ = run(aZ, MZ, M_Pl_GeV, 2)
a_back, _ = run(a_pl_2, M_Pl_GeV, MZ, 2)
a_pl_neg, _ = run(aZ + 0.01, MZ, M_Pl_GeV, 2)          # 负对照：输入改 0.01，必须可分辨
gate("H3_alpha_s_at_planck",
     abs(a_back - aZ) < 1e-9 and abs(1 / a_pl_neg - 1 / a_pl_2) > 0.5,
     inv_alpha_s_MPl_1loop=1 / a_pl_1, inv_alpha_s_MPl_2loop=1 / a_pl_2,
     loop_order_shift_in_inv_alpha=1 / a_pl_2 - 1 / a_pl_1,
     roundtrip_residual=abs(a_back - aZ),
     negative_control_inv_alpha_shift_for_dalpha_0p01=1 / a_pl_2 - 1 / a_pl_neg,
     reading="α_s(M_Pl) 不是被预言的，而是从 M_Z 处的测量值往上跑出来的；单圈与双圈之间就差约 1 个单位的 1/α。")

# ---------- H4 指数敏感度：δ(1/α_s(M_Pl)) → δ ln α_G ----------
eps = 0.05
L0 = scale_where_alpha_is_one(a_pl_2, 2)
Lp = scale_where_alpha_is_one(1 / (1 / a_pl_2 + eps), 2)
dlnL_dinv = (math.log(Lp) - math.log(L0)) / eps      # d ln Λ / d(1/α(M_Pl))
dlnaG_dinv = 2 * dlnL_dinv                            # α_G ∝ m_p² ∝ Λ²（M_Pl 固定）
analytic_nf3 = -2 * math.pi / betas(3)[0]             # 单圈 nf=3 解析值 −2π/9
need_inv = (uG / G) / abs(dlnaG_dinv)                 # 达到 CODATA 精度所需 δ(1/α)
need_rel = need_inv * a_pl_2
factor_per_unit = math.exp(abs(dlnaG_dinv))
gate("H4_exponential_sensitivity",
     abs(dlnL_dinv - analytic_nf3) / abs(analytic_nf3) < 0.2 and factor_per_unit > 2,
     confinement_proxy_scale_GeV=L0,
     dlnLambda_dinvalpha_numeric=dlnL_dinv, dlnLambda_dinvalpha_analytic_1loop_nf3=analytic_nf3,
     dln_alphaG_dinvalpha=dlnaG_dinv, G_factor_per_unit_inv_alpha=factor_per_unit,
     G_relative_uncertainty_CODATA=uG / G,
     required_abs_precision_inv_alpha_MPl=need_inv, required_rel_precision_alpha_MPl=need_rel,
     negative_control="若 α_G 对 1/α 线性而非指数依赖，单位变化只改 O(1) 而非倍数；数值 factor_per_unit 必须 > 2",
     reading="1/α_s(M_Pl) 每变 1，G 就变好几倍。要把 G 算到 CODATA 的 2.2e-5，就要把 α_s(M_Pl) 给到约 7 位有效数字；"
             "这比现在任何理论或测量都精确 4–5 个数量级。")

# ---------- H5 数据层：α_s(M_Z) 的误差如何传到 G ----------
a_pl_hi, _ = run(aZ + u_aZ, MZ, M_Pl_GeV, 2)
d_inv = abs(1 / a_pl_hi - 1 / a_pl_2)
G_factor_from_alphas = math.exp(abs(dlnaG_dinv) * d_inv)
gate("H5_alpha_s_error_propagation",
     G_factor_from_alphas > 1.05,
     d_inv_alpha_MPl_from_u_alphaZ=d_inv, G_spread_factor=G_factor_from_alphas,
     reading="即使 QCD 机制完全正确，仅 α_s(M_Z) 的 0.76%% 测量误差就让『预言的 G』浮动约 %.0f%%；"
             "而 G 的测量误差只有 0.0022%%。" % ((G_factor_from_alphas - 1) * 100))

# ---------- H6 实验侧：G 的测量自身也有张力 ----------
meas = {"BIPM 2013 (Quinn)": 6.67545e-11, "LENS 2014 原子干涉 (Rosi)": 6.67191e-11,
        "HUST 2018 TOS (Li)": 6.674184e-11, "HUST 2018 AAF (Li)": 6.674484e-11}
v = np.array(list(meas.values()))
spread_rel = float((v.max() - v.min()) / G)
gate("H6_G_measurement_tension",
     spread_rel > 10 * uG / G,
     measurements=meas, spread_relative=spread_rel, codata_relative=uG / G,
     negative_control="若各测量一致，spread 应 ≲ 2–3 倍 CODATA 不确定度",
     reading="各实验之间相差约 5e-4，是 CODATA 给出误差的约 24 倍。G 是最不准的基本常数，"
             "但即便如此，它也比任何『理论推出的 G』准 4 个数量级以上。")

n_ok = sum(g["ok"] for g in gates.values())
verdict = ("FIND-G--GATES-%d-OF-%d--G-NOT-FROM-C-HBAR--TARGET-ALPHA_G-5.9E-39--ONLY-MECHANISM-DIM-TRANSMUTATION"
           "--ALPHA_S-MPL-IS-INPUT-NOT-OUTPUT--NEED-7-DIGITS--UFT-NOT-BROKEN--NEW-PREDICTION-0") % (n_ok, len(gates))
out = {"title": "从第一性原理找 G 可算审计", "date": "2026-11-22",
       "nature": "非判定册 / 不占 RID / 不写 README", "verdict": verdict,
       "n_gate_ok": n_ok, "n_gates": len(gates), "gates": gates,
       "sources": ["https://physics.nist.gov/cuu/Constants/", "https://pdg.lbl.gov/",
                   "https://doi.org/10.1038/s41586-018-0431-5", "https://doi.org/10.1038/nature13433",
                   "https://doi.org/10.1103/PhysRevLett.111.101102"]}
payload = json.dumps(out, ensure_ascii=False, indent=2, default=float)
OUT.write_text(payload, encoding="utf-8")
print(verdict)
for k, g in gates.items():
    print(("OK  " if g["ok"] else "FAIL"), k)
print(json.dumps({k: {kk: vv for kk, vv in g.items() if isinstance(vv, (int, float)) and not isinstance(vv, bool)}
                  for k, g in gates.items()}, indent=1, default=float))
print("JSON", len(payload.encode("utf-8")), "B sha256", hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16])
