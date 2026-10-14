# -*- coding: utf-8 -*-
"""openuft/07_统一场方程 · 编号 50 = 系列 52 · 恒星能量与太阳全景卷锚点
250-digit anchors:
  dm/dt = L / c^2  (mass-energy conversion), L_sun = 3.828e26 W (IAU 2015),
  c = 299792458 m/s
  per_year = dm/dt * 3.15576e7 s (Julian year)
  fraction = per_year / M_sun, M_sun = 1.988409870e30 kg (vol 41 source)
Cited: pp chain / CNO, core T 15.7 MK, solar neutrinos (SSM),
  stellar final states (white dwarf / NS vol 42 / BH vol 41),
  TUFT no stellar physics (vol 23).
Writes 50_sun_calc_results.json
"""
import json
import mpmath as mp

mp.mp.dps = 250
res = {}

L = mp.mpf("3.828e26")
c = mp.mpf("299792458")
yr = mp.mpf("3.15576e7")
Msun = mp.mpf("1.988409870e30")

dm_dt = L / c**2
per_year = dm_dt * yr
fraction = per_year / Msun

res["sun_anchors"] = {
  "dm_dt (kg/s) = L/c^2": mp.nstr(dm_dt, 250),
  "per_year (kg/yr)": mp.nstr(per_year, 250),
  "fraction_of_Msun_per_yr": mp.nstr(fraction, 250),
  "note": "L=3.828×10²⁶ W（IAU 2015 标称太阳光度）、c=299792458；M_sun 与 41/47 卷同源",
}

res["cited_anchors"] = {
  "energy_source": "pp 链主导（~99%），CNO 分支 ~1%；核心 T≈15.7 MK（标准太阳模型，文献）",
  "lifetime": "主序寿命 ~10 Gyr（文献）；已耗 ~46 亿年",
  "neutrinos": "太阳中微子通量=SSM 预言，已被实验证实（pp 通量，文献）",
  "final_state": "终局：白矮星（&lt;~8 M_sun 前身）→ 中子星（42 卷）/ 黑洞（41 卷）",
  "tuft": "TUFT——无核聚变、无恒星结构、无演化（23 G1–G5）",
}

print(json.dumps(res, ensure_ascii=False, indent=2))
with open(r"D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\50_sun_calc_results.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("\nOK -> 50_sun_calc_results.json")
