# -*- coding: utf-8 -*-
"""openuft/07_统一场方程 · 编号 44 = 系列 46 · 中微子振荡全景卷锚点
250-digit anchors:
  mass-squared ratio: d23 / d21 = 2.453e-3 / 7.53e-5 (PDG, cited)
  sin(theta13) = sqrt(sin^2 theta13), sin^2 theta13 = 0.02203 (PDG, cited)
Cited: solar/atmospheric/reactor/accelerator oscillation evidence,
  Sum m_nu < 0.12 eV (DESI+Planck 2024, vol 38), hierarchy / Majorana open,
  TUFT no neutrino mass (vol 23).
Writes 44_nu_calc_results.json
"""
import json
import mpmath as mp

mp.mp.dps = 250
res = {}

d21 = mp.mpf("7.53e-5")
d23 = mp.mpf("2.453e-3")
res["oscillation_anchors"] = {
  "Delta m2_23 / Delta m2_21": mp.nstr(d23 / d21, 250),
  "sin(theta13) = sqrt(0.02203)": mp.nstr(mp.sqrt(mp.mpf("0.02203")), 250),
  "note": "PDG 中心值：Δm²₂₁=7.53e-5 eV²、Δm²₃₂=2.453e-3 eV²、sin²θ₁₃=0.02203；比值与 sinθ₁₃ 为 250 位现算",
}

res["cited_anchors"] = {
  "evidence": "振荡已证：太阳（MSW）、大气、反应堆、加速器四类实验（文献）",
  "sum": "Σm_ν<0.12 eV（DESI+Planck 2024，38 卷 Y4）——绝对质量上限",
  "hierarchy": "质量层级：正常（m₁&lt;m₂&lt;m₃）vs 倒置（m₃&lt;m₁≈m₂）——开放（JUNO/DUNE 窗口）",
  "majorana": "马约拉纳 vs 狄拉克：0νββ 探测——开放（无中微子双 β 衰变）",
  "tuft": "TUFT——无中微子质量机制、无振荡预言（23 G1–G5）",
}

print(json.dumps(res, ensure_ascii=False, indent=2))
with open(r"D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\44_nu_calc_results.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("\nOK -> 44_nu_calc_results.json")
