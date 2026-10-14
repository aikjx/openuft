# -*- coding: utf-8 -*-
"""openuft/07_统一场方程 · 编号 47 = 系列 49 · 黑洞热力学全景卷锚点
250-digit anchors for Sgr A* (M = 4.297e6 M_sun, cited; r_s from vol 41):
  T_H = hbar c^3 / (8 pi G M k_B)
  S / k_B = A / (4 l_P^2),  A = 4 pi r_s^2,  r_s = 2 G M / c^2
Constants: CODATA 2022 (cited): hbar, c, G, k_B; M_sun = 1.98847e30 kg
Cited: 4 laws of BH thermodynamics, information paradox open (vol 41),
  TUFT no BH thermodynamics (vol 23).
Writes 47_bhth_calc_results.json
"""
import json
import mpmath as mp

mp.mp.dps = 250
res = {}

hbar = mp.mpf("1.054571817e-34")
c = mp.mpf("299792458")
G = mp.mpf("6.67430e-11")
kB = mp.mpf("1.380649e-23")
Msun = mp.mpf("1.988409870e30")
M = mp.mpf("4.297e6") * Msun

rs = 2 * G * M / c**2
A = 4 * mp.pi * rs**2
lP = mp.sqrt(hbar * G / c**3)
TH = hbar * c**3 / (8 * mp.pi * G * M * kB)
S_kB = A / (4 * lP**2)

res["bhth_anchors"] = {
  "M (kg)": mp.nstr(M, 250),
  "r_s (m)": mp.nstr(rs, 250),
  "T_Hawking (K)": mp.nstr(TH, 250),
  "S/k_B (A/(4 lP^2))": mp.nstr(S_kB, 250),
  "note": "SgrA*：M=4.297×10⁶ M_sun；T_H=ħc³/(8πGMk_B)、S/k_B=A/(4l_P²)；r_s 与 41 卷一致",
}

res["cited_anchors"] = {
  "four_laws": "黑洞热力学四定律：κ∝T、A∝S、dM=TdS（文献）",
  "hawking": "霍金辐射：蒸发时间 t_ev∝M³（41 卷 PBH 现算）",
  "information": "信息悖论：纯态→混合态？——开放（Page 曲线未测）",
  "entropy": "黑洞熵=引力最大熵载体（A/4l_P²）——引力与热力学最深联系",
  "tuft": "TUFT——无温度、无熵、无热力学（23 G1–G5）",
}

print(json.dumps(res, ensure_ascii=False, indent=2))
with open(r"D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\47_bhth_calc_results.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("\nOK -> 47_bhth_calc_results.json")
