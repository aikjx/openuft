# -*- coding: utf-8 -*-
"""算法联盟 · 万有引力常数 G 的本质 可算审计（6 门，每门带负对照）。

问题：G「是什么」？本脚本只检验可算、可被数据判负的说法：
  E1 G 的三副面孔（单位 / 耦合 / 时空刚度）是同一个数
  E2 G 耦合的是能量而非质量（光线偏折因子 2）
  E3 G 对所有物质成分普适（含核结合能）
  E4 G 不随宇宙时间变化（排除 Dirac 大数假说）
  E5 诱导引力：G 只能来自普朗克尺度物理
  E6 引力强度随能量平方增长，仅在普朗克能标变强

非判定册 / 不占 RID / 不写 README。计算 != 证实。外部数据需对照一手来源复核。
用法:  python -I _alg_G_essence_audit.py
"""
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "数据" / "_ALG_G_essence_audit_2026-11-22.json"
gates = {}


def gate(name, ok, **kw):
    gates[name] = {"ok": bool(ok), **kw}


G = 6.67430e-11; hbar = 1.054571817e-34; c = 299792458.0
GeV = 1.602176634e-10; MeV = GeV / 1000
M_sun = 1.98840987e30; R_sun = 6.957e8
rad2as = 180 / math.pi * 3600
yr = 365.25 * 86400; Mpc = 3.0856775814913673e22

# ---------- E1 三副面孔是同一个数 ----------
l_P = math.sqrt(hbar * G / c ** 3); t_P = l_P / c; m_P = math.sqrt(hbar * c / G)
E_P = m_P * c ** 2
F_stiff = c ** 4 / G                      # 时空「刚度」（力的量纲）
F_planck = E_P / l_P
F_EH = c ** 4 / (8 * math.pi * G)         # 爱因斯坦方程 G_μν = (8πG/c⁴) T_μν 的倒数系数
neg = (hbar * c / l_P ** 2)               # 第二恒等式：同样相等，说明是定义恒等
neg_wrong = c ** 3 / G                     # 负对照：量纲不同的组合（kg/s），必须不相等
gate("E1_three_faces_one_number",
     abs(F_stiff / F_planck - 1) < 1e-12 and abs(neg / F_stiff - 1) < 1e-12 and abs(neg_wrong / F_stiff - 1) > 0.5,
     negative_control_c3_over_G_ratio=neg_wrong / F_stiff,
     planck_length_m=l_P, planck_time_s=t_P, planck_mass_kg=m_P, planck_energy_GeV=E_P / GeV,
     stiffness_c4_over_G_N=F_stiff, einstein_coefficient_c4_over_8piG_N=F_EH,
     identity="c^4/G = E_P/l_P = ħc/l_P²",
     reading="『普朗克单位』『引力耦合』『时空刚度 c⁴/8πG≈4.8e42 N』是同一个 G 的三种写法；"
             "负对照 ħc/l_P² 也相等，说明这是定义恒等，不是三条独立证据。")

# ---------- E2 G 耦合能量：光线偏折 ----------
defl_GR = 4 * G * M_sun / (c ** 2 * R_sun) * rad2as
defl_newton = defl_GR / 2                   # 负对照：只把光当有质量粒子
gamma_minus_1, u_gamma = 2.1e-5, 2.3e-5      # Cassini 2003
gate("E2_couples_to_energy",
     abs(defl_GR - 1.75) < 0.01 and abs(defl_newton - 0.875) < 0.01 and abs(gamma_minus_1) < 2 * u_gamma,
     deflection_GR_arcsec=defl_GR, negative_control_newtonian_arcsec=defl_newton,
     cassini_gamma_minus_1=gamma_minus_1, cassini_sigma=u_gamma,
     reading="太阳边缘光偏折 1.75″ 是牛顿算法的 2 倍；Cassini 测得 γ−1=(2.1±2.3)e-5。"
             "G 不是『质量之间的系数』，而是能量–动量弯曲时空的系数，连无质量的光也受它支配。")

# ---------- E3 成分普适：核结合能也受同一个 G ----------
BA = {"Ti48": (48, 8.7230), "Pt195": (195, 7.9266)}   # 每核子结合能 MeV
u_MeV = 931.494
frac = {k: b / u_MeV for k, (A, b) in BA.items()}
d_frac = abs(frac["Ti48"] - frac["Pt195"])
eta_bound = 2.7e-15                          # MICROSCOPE 2022 量级（|η| 上限，约 1σ 合成）
coupling_to_binding_bound = eta_bound / d_frac
gate("E3_universal_over_composition",
     d_frac > 5e-4 and coupling_to_binding_bound < 1e-11,
     binding_fraction_Ti=frac["Ti48"], binding_fraction_Pt=frac["Pt195"], difference=d_frac,
     microscope_eta_bound=eta_bound,
     negative_control_eta_if_binding_energy_did_not_gravitate=d_frac,
     bound_on_anomalous_binding_coupling=coupling_to_binding_bound,
     reading="钛与铂的核结合能占比差 8.5e-4；若结合能不受引力，MICROSCOPE 会看到 η≈8.5e-4，实际 η<3e-15。"
             "G 对核能的耦合与对静质量的耦合相同，偏差 <3e-12：G 只认总能量，不认『是什么材料』。")

# ---------- E4 时间恒定：排除 Dirac 大数假说 ----------
H0 = 70.0 * 1000 / Mpc * yr                  # 每年
Gdot, u_Gdot = 7.1e-14, 7.6e-14              # LLR (Hofmann & Müller 2018)，每年
dirac = -H0                                  # 负对照：Dirac 假说 Ġ/G = −H0
n_sigma_dirac = abs(dirac - Gdot) / u_Gdot
gate("E4_constant_in_time",
     abs(Gdot) < 2 * u_Gdot and n_sigma_dirac > 100,
     H0_per_yr=H0, LLR_Gdot_over_G_per_yr=Gdot, LLR_sigma=u_Gdot,
     bound_relative_to_H0=(abs(Gdot) + 2 * u_Gdot) / H0,
     negative_control_dirac_excluded_sigma=n_sigma_dirac,
     reading="月球激光测距给出 Ġ/G=(7±8)e-14 /年，与 0 相容；变化率小于哈勃率的约 0.3%%。"
             "Dirac『G 随宇宙年龄衰减』被排除约 %.0fσ。" % n_sigma_dirac)

# ---------- E5 诱导引力（Sakharov）：G 来自截断尺度 ----------
# 单圈示意：1/(16πG) ≈ N Λ² /(96π²)（自然单位，系数依赖正规化）⇒ N ≈ 6π (M_P/Λ)²
M_P_GeV = E_P / GeV
cuts = {"Planck": M_P_GeV, "GUT_2e16": 2e16, "TeV": 1e3}
N_need = {k: 6 * math.pi * (M_P_GeV / L) ** 2 for k, L in cuts.items()}
scaling = N_need["GUT_2e16"] / N_need["Planck"] / (M_P_GeV / 2e16) ** 2
gate("E5_induced_gravity_scale",
     abs(scaling - 1) < 1e-12 and N_need["TeV"] > 1e30 and N_need["Planck"] < 100,
     fields_needed=N_need, negative_control_scaling_N_propto_Lambda_minus2=scaling,
     reading="若 G 由量子涨落『诱导』，所需场数 N≈6π(M_P/Λ)²：截断在普朗克能标只需约 19 个场，"
             "在 TeV 需要 1e33 个。G 的小，等价于『引力的源头物理在约 1e19 GeV』。系数依赖正规化，只取量级。")

# ---------- E6 强度随能量：g(E) = (E/E_P)² ----------
scales = {"1 eV（化学）": 1e-9, "1 GeV（质子）": 1.0, "13.6 TeV（LHC）": 1.36e4, "E_P": M_P_GeV}
g_E = {k: (E / M_P_GeV) ** 2 for k, E in scales.items()}
alpha_em = 1 / 137.035999
cross = M_P_GeV * math.sqrt(alpha_em)
gate("E6_strength_runs_with_energy_squared",
     abs(g_E["E_P"] - 1) < 1e-12 and g_E["13.6 TeV（LHC）"] < 1e-29,
     dimensionless_gravity_strength=g_E, energy_where_gravity_equals_alpha_em_GeV=cross,
     negative_control="若引力像电磁一样无量纲耦合，g 应与能量无关；此处 g(E_P)/g(1GeV) = %.3e" % (g_E["E_P"] / g_E["1 GeV（质子）"]),
     reading="引力的无量纲强度是 (E/E_P)²：在 LHC 也只有 1e-30，到约 1e18 GeV 才追上电磁力。"
             "引力『弱』不是因为耦合小，而是因为我们所处的能量远低于普朗克能标。")

n_ok = sum(g["ok"] for g in gates.values())
verdict = ("G-ESSENCE--GATES-%d-OF-%d--ONE-NUMBER-THREE-FACES--COUPLES-TO-ENERGY--UNIVERSAL-3E-12"
           "--CONSTANT-0.3PCT-H0--PLANCK-SCALE-ORIGIN--VALUE-UNEXPLAINED--UFT-NOT-BROKEN--NEW-PREDICTION-0") % (n_ok, len(gates))
out = {"title": "万有引力常数 G 的本质 可算审计", "date": "2026-11-22",
       "nature": "非判定册 / 不占 RID / 不写 README", "verdict": verdict,
       "n_gate_ok": n_ok, "n_gates": len(gates), "gates": gates,
       "sources": ["https://physics.nist.gov/cuu/Constants/",
                   "https://doi.org/10.1038/nature01997",
                   "https://arxiv.org/abs/2209.15487",
                   "https://doi.org/10.1088/1361-6382/aad6a2",
                   "https://www.nndc.bnl.gov/"]}
payload = json.dumps(out, ensure_ascii=False, indent=2, default=float)
OUT.write_text(payload, encoding="utf-8")
print(verdict)
for k, g in gates.items():
    print(("OK  " if g["ok"] else "FAIL"), k)
for k, g in gates.items():
    print(k, {kk: vv for kk, vv in g.items() if kk not in ("reading", "ok", "identity", "negative_control")})
print("JSON", len(payload.encode("utf-8")), "B sha256", hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16])
