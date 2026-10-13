# -*- coding: utf-8 -*-
"""openuft/07_统一场方程 · 编号 34 = 系列 36 · 五大量级问题卷锚点
250-digit recomputation of the order-of-magnitude gaps behind unsolved puzzles:
  U2 hierarchy: log10(M_Pl / m_H), M_Pl=1.220910e19 GeV, m_H=125.10 GeV
  U5 fermion mass spectrum: log10(m_t / m_e)
  U1 Hubble tension: H0_SH0ES / H0_Planck ratio
  U6 extra: log10(M_Pl / Lambda_QCD)
Cited: U3 Lambda problem log10=122.9456 (24/32); U4 strong-CP theta<1e-10.
Writes 34_orders_calc_results.json
"""
import json
import mpmath as mp

mp.mp.dps = 250
res = {}

M_Pl_GeV = mp.mpf("1.220910e19")
m_H = mp.mpf("125.10")
m_t = mp.mpf("172.69")
m_e = mp.mpf("5.1099895e-4")          # 0.51099895 MeV in GeV
Lambda_QCD = mp.mpf("0.213")          # GeV, MSbar 3-flavor ~213 MeV (PDG range 200-230)

res["u2_hierarchy"] = {
  "M_Pl (GeV)": mp.nstr(M_Pl_GeV, 250),
  "m_H (GeV)": mp.nstr(m_H, 250),
  "M_Pl/m_H": mp.nstr(M_Pl_GeV / m_H, 250),
  "log10(M_Pl/m_H)": mp.nstr(mp.log10(M_Pl_GeV / m_H), 250),
  "note": "层次问题：Higgs 质量比普朗克尺度小 17 个量级，无原理解释（SUSY/复合/多重宇宙候选）",
}

res["u5_mass_spectrum"] = {
  "m_t (GeV)": mp.nstr(m_t, 250),
  "m_e (GeV)": mp.nstr(m_e, 250),
  "m_t/m_e": mp.nstr(m_t / m_e, 250),
  "log10(m_t/m_e)": mp.nstr(mp.log10(m_t / m_e), 250),
  "note": "费米子质量谱跨 5.5 个量级，三代质量无生成原理（Yukawa 是输入）",
}

res["u1_hubble"] = {
  "H0_SH0ES (km/s/Mpc)": "73.04 +/- 1.04（文献 2024）",
  "H0_Planck (km/s/Mpc)": "67.4 +/- 0.5（文献 2018）",
  "ratio": mp.nstr(mp.mpf("73.04") / mp.mpf("67.4"), 250),
  "significance": "~5.1 sigma（文献综合，各方法 4-6 sigma）",
  "note": "Hubble tension：局域测量与 CMB 推断不一致，~5 sigma；开放=系统误差或新物理",
}

res["u6_planck_qcd"] = {
  "Lambda_QCD (GeV)": mp.nstr(Lambda_QCD, 250),
  "M_Pl/Lambda_QCD": mp.nstr(M_Pl_GeV / Lambda_QCD, 250),
  "log10(M_Pl/Lambda_QCD)": mp.nstr(mp.log10(M_Pl_GeV / Lambda_QCD), 250),
}

res["cited_anchors"] = {
  "u3_lambda": "log10(rho_Pl/rho_Lambda)=122.9456339700…（24 H2/H3；32 卷重算）——123 量级问题",
  "u4_strong_cp": "theta_bar < 1e-10（中子 EDM 上限，文献）——为什么 θ̄≈0（轴子候选）",
  "u6_tuft": "TUFT 声称解释全部量级差——母方程无量级结构、无常数可标定（23 G1–G5），无法进入任何一行",
}

print(json.dumps(res, ensure_ascii=False, indent=2))
with open(r"D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\34_orders_calc_results.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("\nOK -> 34_orders_calc_results.json")
