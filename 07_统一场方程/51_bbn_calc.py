# -*- coding: utf-8 -*-
"""openuft/07_统一场方程 · 编号 51 = 系列 53 · 大爆炸核合成卷锚点
250-digit anchors (simplified freeze-out estimate, honest residual vs obs.):
  Q = 1.293332 MeV   (neutron-proton mass difference, CODATA)
  kT_f = 0.8 MeV     (freeze-out temperature, simplified)
  (n/p)_f = exp(-Q/kT_f)
  neutron decay until deuterium bottleneck t_nuc ~ 180 s, tau_n = 879.4 s (PDG)
  (n/p)_eff = (n/p)_f * exp(-t_nuc/tau_n)
  Y_p_est = 2*(n/p)_eff/(1+(n/p)_eff)
  observed Y_p = 0.247 (literature) -> residual exposed, not hidden
Cited: BBN timeline (t~1 s to ~20 min), light element abundances D/H, 4He,
  7Li (literature); TUFT has no BBN (vol 23).
Writes 51_bbn_calc_results.json
"""
import json
import mpmath as mp

mp.mp.dps = 250
res = {}

Q = mp.mpf("1.293332")
kT_f = mp.mpf("0.8")
t_nuc = mp.mpf("180")
tau_n = mp.mpf("879.4")

np_f = mp.exp(-Q / kT_f)
decay = mp.exp(-t_nuc / tau_n)
np_eff = np_f * decay
Yp_est = 2 * np_eff / (1 + np_eff)
Yp_obs = mp.mpf("0.247")
resid_rel = (Yp_est - Yp_obs) / Yp_obs

res["bbn_anchors"] = {
  "np_freeze (exp(-Q/kTf))": mp.nstr(np_f, 250),
  "neutron_decay (exp(-180/879.4))": mp.nstr(decay, 250),
  "np_effective": mp.nstr(np_eff, 250),
  "Yp_simplified_est": mp.nstr(Yp_est, 250),
  "Yp_observed": "0.247（文献）",
  "Yp_relative_residual": mp.nstr(resid_rel, 250),
  "note": "简化冻结近似：kT_f=0.8 MeV、t_nuc=180 s——非完整 BBN 数值模拟；残差如实暴露",
}

res["cited_anchors"] = {
  "timeline": "BBN：t≈1 s（弱作用冻结）→ 180 s（氘门）→ ~20 min（核合成停止）；T 从 ~1 MeV 降到 ~0.1 MeV（文献）",
  "abundances": "观测：Y_p=0.247、D/H≈2.5×10⁻⁵、⁷Li/H≈1.6×10⁻¹⁰（文献）；BBN 已证（轻元素丰度+CMB 交叉，46 卷）",
  "baryon_density": "η=6.1×10⁻¹⁰（CMB 定标，38 卷宇宙起源）",
  "tuft": "TUFT——无 BBN、无轻元素合成（23）",
}

print(json.dumps(res, ensure_ascii=False, indent=2))
with open(r"D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\51_bbn_calc_results.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("\nOK -> 51_bbn_calc_results.json")
