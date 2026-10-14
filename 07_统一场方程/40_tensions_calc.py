# -*- coding: utf-8 -*-
"""openuft/07_统一场方程 · 编号 40 = 系列 42 · 宇宙学张力全景卷锚点
250-digit anchors:
  Hubble tension: (H0_SH0ES - H0_Planck)/H0_Planck, SH0ES 73.04 vs Planck 67.36
  S8 tension: (S8_Planck - S8_DES)/S8_DES, Planck 0.776 vs DES 0.74
Cited: CMB dipole 3.362 mK, LambdaCDM six parameters (Planck 2018), TUFT no H0.
Writes 40_tensions_calc_results.json
"""
import json
import mpmath as mp

mp.mp.dps = 250
res = {}

h0s = mp.mpf("73.04")
h0p = mp.mpf("67.36")
res["hubble_tension"] = {
  "H0 SH0ES (km/s/Mpc)": mp.nstr(h0s, 250),
  "H0 Planck (km/s/Mpc)": mp.nstr(h0p, 250),
  "difference (%)": mp.nstr(100 * (h0s - h0p) / h0p, 250),
  "note": "SH0ES 73.04±1.04 vs Planck 67.36±0.54（文献）；现算百分比差=8.4325…%（本卷 250 位）；36 卷 Hubble 8.4% 偏离=同一数值",
}

s8p = mp.mpf("0.776")
s8d = mp.mpf("0.74")
res["s8_tension"] = {
  "S8 Planck": mp.nstr(s8p, 250),
  "S8 DES": mp.nstr(s8d, 250),
  "difference (%)": mp.nstr(100 * (s8p - s8d) / s8d, 250),
  "note": "Planck 0.776±0.017 vs DES 0.74±0.015（文献）；现算百分比差=4.8648…%（本卷 250 位）",
}

res["cited_anchors"] = {
  "cmb_dipole": "3.362 mK（文献）——CMB 偶极；宇宙超偶极异常（类轴子候选）开放",
  "lcdm_six": "ΛCDM 六参数基准：Ω_b h²=0.0224、Ω_c h²=0.120、h=0.6736、n_s=0.9649、σ₈=0.811、τ=0.0544（Planck 2018）",
  "desi": "DESI 2024 BAO：w≈−1 一致但允许偏离——暗能量动力学窗口开放（24 卷 w 判定扩展）",
  "tuft": "TUFT'频率升高解释膨胀'——无 H₀ 值、无 σ₈、无参数；对张力问题零贡献（23 G1–G5）",
}

print(json.dumps(res, ensure_ascii=False, indent=2))
with open(r"D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\40_tensions_calc_results.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("\nOK -> 40_tensions_calc_results.json")
