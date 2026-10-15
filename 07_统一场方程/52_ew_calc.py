# -*- coding: utf-8 -*-
"""openuft/07_统一场方程 · 编号 52 = 系列 54 · 电弱统一与实验对照卷锚点
250-digit anchors (electroweak unification = the ONLY experimentally confirmed
unification):
  M_W = 80.369 GeV, M_Z = 91.1876 GeV (PDG 2024 world averages)
  cosθ_W = M_W / M_Z, sin²θ_W = 1 - (M_W/M_Z)^2   (tree-level / on-shell scheme)
  ρ = M_W^2 / (M_Z^2 cos²θ_W) = 1   (custodial symmetry, exact at tree level)
  α_W = α / sin²θ_W, g = sqrt(4π α_W)   (α = 1/137.035999084, CODATA 2018)
Residual vs PDG on-shell sin²θ_W ~0.22343 (scheme-dependent) reported honestly.
Cited: Glashow-Salam-Weinberg (1979 Nobel), W/Z discovery 1983 (UA1/UA2),
  LEP Z-pole precision, weak neutral currents (Gargamelle 1973);
  TUFT/V50 have no EW unification, no W/Z prediction (23/48/49).
Writes 52_ew_calc_results.json
"""
import json
import mpmath as mp

mp.mp.dps = 250
res = {}

MW = mp.mpf("80.369")
MZ = mp.mpf("91.1876")
alpha_inv = mp.mpf("137.035999084")

cos_th = MW / MZ
sin2_th = 1 - cos_th**2
sin_th = mp.sqrt(sin2_th)
rho = MW**2 / (MZ**2 * cos_th**2)
alpha = 1 / alpha_inv
alpha_W = alpha / sin2_th
g = mp.sqrt(4 * mp.pi * alpha_W)

# PDG on-shell sin²θ_W ~ 0.22343 (scheme-dependent); residual vs tree calc
onshell_obs = mp.mpf("0.22343")
resid = (sin2_th - onshell_obs) / onshell_obs

res["ew_anchors"] = {
  "cos_theta_W = MW/MZ": mp.nstr(cos_th, 250),
  "sin2_theta_W (tree/on-shell)": mp.nstr(sin2_th, 250),
  "sin_theta_W": mp.nstr(sin_th, 250),
  "rho = MW^2/(MZ^2 cos^2)": mp.nstr(rho, 250),
  "alpha_W = alpha/sin2": mp.nstr(alpha_W, 250),
  "g = sqrt(4 pi alpha_W)": mp.nstr(g, 250),
  "resid_vs_PDG_onshell": mp.nstr(resid, 250),
  "note": "树图/on-shell 方案；PDG on-shell ≈0.22343（方案依赖，含辐射修正）——残差如实报告",
}

res["cited_anchors"] = {
  "confirmed": "电弱统一=唯一已被实验证实的统一：中性流（Gargamelle 1973）→ W/Z（UA1/UA2 1983）→ LEP Z 峰精确检验（文献）",
  "bosons": "M_W=80.369、M_Z=91.1876 GeV（PDG 2024 世界均值）；sin²θ_W 方案依赖（MS-bar 0.2312 vs on-shell ~0.2234）",
  "nobel": "1979 诺贝尔物理奖：Glashow、Salam、Weinberg",
  "tuft_v50": "TUFT/V50——无电弱统一、无 W/Z 质量预言、无 Weinberg 角（23/48/49）",
}

print(json.dumps(res, ensure_ascii=False, indent=2))
with open(r"D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\52_ew_calc_results.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("\nOK -> 52_ew_calc_results.json")
