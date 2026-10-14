# -*- coding: utf-8 -*-
"""openuft/07_统一场方程 · 编号 42 = 系列 44 · 中子星与致密天体全景卷锚点
250-digit anchors:
  Schwarzschild radii: r_s = 2 G M / c^2 for NS masses 1.4 / 2.08 / 2.1 M_sun
  Compactness: r_s(2.08 M_sun) / R (R = 12.39 km NICER 2021 for PSR J0740+6620)
Cited: GW170817 Lambda_1.4 (literature), NICER radius, NANOGrav 2023 PTA, NS mass range.
M_sun = 1.988409870e30 kg (IAU nominal).
Writes 42_ns_calc_results.json
"""
import json
import mpmath as mp

mp.mp.dps = 250
res = {}

G = mp.mpf("6.67430e-11")
c = mp.mpf("299792458")
Msun = mp.mpf("1.988409870e30")

def rs(M):
    return 2 * G * M / c**2

res["ns_schwarzschild"] = {
  "r_s(1.4 M_sun) [km]": mp.nstr(rs(mp.mpf("1.4") * Msun) / 1000, 250),
  "r_s(2.08 M_sun) [km]": mp.nstr(rs(mp.mpf("2.08") * Msun) / 1000, 250),
  "r_s(2.1 M_sun) [km]": mp.nstr(rs(mp.mpf("2.1") * Msun) / 1000, 250),
  "note": "r_s=2GM/c² 250 位现算；中子星质量范围 1.4–2.1 M_sun（文献）；r_s 4.1–6.2 km 远小于 NS 半径 10–13 km",
}

res["compactness"] = {
  "r_s(2.08 M_sun) / R(12.39 km)": mp.nstr(rs(mp.mpf("2.08") * Msun) / mp.mpf("12.39e3"), 250),
  "note": "PSR J0740+6620：M=2.08 M_sun、R=12.39 km（NICER 2021，文献）；紧凑度≈0.50——强场 GR 检验区",
}

res["cited_anchors"] = {
  "gw170817": "GW170817 多信使：双中子星合并+短暴+kilonova（文献）；潮汐形变 Λ₁.₄≈190–640（文献，方程依赖）——物态方程约束",
  "nicer": "NICER 半径：PSR J0030 R=12.71 km、PSR J0740 R=12.39 km（文献）",
  "nanograv": "NANOGrav 2023 脉冲星计时阵列：纳赫兹随机引力波背景信号（文献）；SMBHB 来源或新物理——开放",
  "tuft": "TUFT'挠率自旋引力'——无 NS 物态方程、无潮汐形变 Λ、无 PTA 预言（23 G1–G5）",
}

print(json.dumps(res, ensure_ascii=False, indent=2))
with open(r"D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\42_ns_calc_results.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("\nOK -> 42_ns_calc_results.json")
