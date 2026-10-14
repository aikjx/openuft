# -*- coding: utf-8 -*-
"""openuft/07_统一场方程 · 编号 46 = 系列 48 · CMB 物理全景卷锚点
250-digit anchors (Wien displacement, CODATA constants, cited):
  nu_max = b' * T,  b' = 5.878925757e10 Hz/K, T_CMB = 2.72548 K (Planck)
  lambda_max = b / T,  b = 2.897771955e-3 m K
Cited: FIRAS blackbody (deviation < 1e-5), dipole 3.362 mK (vol 40),
  Delta T/T ~ 1.1e-5, E-mode measured (Planck), B-mode r<0.036 (vol 43),
  TUFT no CMB prediction (vol 23).
Writes 46_cmb_calc_results.json
"""
import json
import mpmath as mp

mp.mp.dps = 250
res = {}

T = mp.mpf("2.72548")
bp = mp.mpf("5.878925757e10")
b = mp.mpf("2.897771955e-3")
res["cmb_anchors"] = {
  "nu_max (Hz) = b'*T": mp.nstr(bp * T, 250),
  "lambda_max (m) = b/T": mp.nstr(b / T, 250),
  "T_CMB (K)": mp.nstr(T, 250),
  "note": "维恩位移：ν_max=b'·T（b'=5.878925757×10¹⁰ Hz/K）、λ_max=b/T（b=2.897771955×10⁻³ m·K）；T=2.72548 K（Planck）",
}

res["cited_anchors"] = {
  "blackbody": "COBE/FIRAS：CMB 黑体偏差&lt;10⁻⁵——完美黑体已证（文献）",
  "anisotropy": "偶极 3.362 mK（40 卷 AA）；涨落 ΔT/T≈1.1×10⁻⁵（Planck）",
  "polarization": "E 模已测（Planck）；B 模 r&lt;0.036 未测（43 卷 DD4）",
  "tuft": "TUFT——无 CMB 谱、无极化、无涨落预言（23 G1–G5）",
}

print(json.dumps(res, ensure_ascii=False, indent=2))
with open(r"D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\46_cmb_calc_results.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("\nOK -> 46_cmb_calc_results.json")
