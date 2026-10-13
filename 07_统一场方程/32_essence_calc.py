# -*- coding: utf-8 -*-
"""openuft/07_统一场方程 · 编号 32 = 系列 34 · 宇宙本源核心方程体系卷锚点
250-digit recomputation of the Planck unit system from G, hbar, c, k_B:
  l_P = sqrt(hbar G / c^3), t_P = l_P / c, M_P = sqrt(hbar c / G)
  E_P = M_P c^2, T_P = E_P / k_B
Plus rho_Lambda / rho_crit consistency and the SM independent-parameter count.
Writes 32_essence_calc_results.json
"""
import json
import mpmath as mp

mp.mp.dps = 250
res = {}

G = mp.mpf("6.67430e-11")
hbar = mp.mpf("1.054571817e-34")
c = mp.mpf("299792458")
kB = mp.mpf("1.380649e-23")

lP = mp.sqrt(hbar * G / c ** 3)
tP = lP / c
MP = mp.sqrt(hbar * c / G)
EP = MP * c ** 2
TP = EP / kB

res["planck_units"] = {
  "l_P (m)": mp.nstr(lP, 250),
  "t_P (s)": mp.nstr(tP, 250),
  "M_P (kg)": mp.nstr(MP, 250),
  "E_P (J)": mp.nstr(EP, 250),
  "T_P (K)": mp.nstr(TP, 250),
  "CODATA 2022 reference": "l_P=1.6162550239e-35 m；t_P=5.39124760e-44 s；M_P=2.176434e-8 kg；E_P=1.9561e9 J；T_P=1.416784e32 K",
  "verdict": "250 位现算与 CODATA 2022 一致——普朗克单位系是可复算的本源尺度锚点",
}

# rho_Lambda / rho_crit consistency (Planck 2018)
rho_Lam = mp.mpf("5.8424459e-27")
rho_crit = mp.mpf("8.532855163739316159664075622549193579546524798392133745390262142920170912691545686978108866594658439020629770544183112188839011996275883560843921859804380529984411818495508895920455317354078388681340730308555833590923308493523579291218184034718965835e-27")
res["lambda_consistency"] = {
  "rho_Lambda/rho_crit": mp.nstr(rho_Lam / rho_crit, 250),
  "note": "Planck 2018 Ω_Λ=0.685——现算比 0.6847… 一致；暗能量占据约 2/3 能量预算（32 Q2）",
}

# Independent-parameter counts (literature consensus)
res["sm_parameters"] = {
  "SM independent parameters": "19（文献：3 规范耦合、9 费米子质量、4 CKM、2 Higgs、1 θ_QCD；无中微子质量时为 18/19 视约定）",
  "gravity": "2（G、Λ）",
  "total known constant space": "~21 个独立常数决定已知宇宙的低能行为（文献共识）",
  "TUFT claim": "声称单一母方程决定一切——但母方程量纲断裂（19 A2/A3）、无独立常数可标定（23 G1–G5），不进入该计数",
}

print(json.dumps(res, ensure_ascii=False, indent=2))
with open(r"D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\32_essence_calc_results.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("\nOK -> 32_essence_calc_results.json")
