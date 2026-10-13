# -*- coding: utf-8 -*-
"""openuft/07_统一场方程 · 编号 33 = 系列 35 · 宇宙本质本源定理卷锚点
250-digit recomputation of the universe's Planck-scale extent:
  t_Universe (s) = 13.8e9 yr * 3.15576e7 s  ->  t_U / t_P
  R_obs (m) = 46.5 Gpc  ->  R / l_P
Writes 33_essence_units_calc_results.json
"""
import json
import mpmath as mp

mp.mp.dps = 250
res = {}

c = mp.mpf("299792458")
yr = mp.mpf("3.1557600e7")
Gpc = mp.mpf("3.0856775814913673e25")

# Universe age
t_U = mp.mpf("13.8e9") * yr
tP = mp.mpf("5.391246446661943879471493582391407615849609975031677403587289463127210659426461690752053069279120160912276195317156529014809052144471688669715416300668183506058503721103884160637677982304016795719328796815236742285867419617333402312921566807674400748e-44")
tU_over_tP = t_U / tP

# Observable universe radius ~46.5 Gpc
R_obs = mp.mpf("46.5") * Gpc
lP = mp.mpf("1.616255023928550050684814801996345607235474332756065196684491525708406850273259820513393858185631721117246802969018445404097924143041338657704734813270581775676336722351879905864836329727401698461981458107422394821792732389197800084893641674483921864e-35")
R_over_lP = R_obs / lP

res["planck_extent"] = {
  "t_Universe (s)": mp.nstr(t_U, 250),
  "t_U / t_P": mp.nstr(tU_over_tP, 250),
  "log10(t_U/t_P)": mp.nstr(mp.log10(tU_over_tP), 250),
  "R_obs (m, 46.5 Gpc)": mp.nstr(R_obs, 250),
  "R_obs / l_P": mp.nstr(R_over_lP, 250),
  "log10(R_obs/l_P)": mp.nstr(mp.log10(R_over_lP), 250),
  "note": "宇宙时空在普朗克尺度上的跨度 ~10^60（时间与空间一致）——本源尺度的两端锚点",
}

# Reference anchors (literature / earlier volumes)
res["reference_anchors"] = {
  "alpha_inv": "137.035999084（文献，精细结构常数倒数）",
  "sm_parameters": "19（文献）",
  "gravity_parameters": "2（G、Λ）",
  "generator_principles": "4：最小作用量、规范对称、量子化、统计律（本卷 T2 定义）",
  "open_essence": "5 项缺失本源（32 S6）：量子引力动力学、Λ 起源、重子不对称、暗物质粒子、暴胀势",
  "verdict": "本质本源=四层结构：4 原理 → 4 方程族 → 21 常数 → 5 缺失；单一母方程不成立（19 A2/A3、31 P5）",
}

print(json.dumps(res, ensure_ascii=False, indent=2))
with open(r"D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\33_essence_units_calc_results.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("\nOK -> 33_essence_units_calc_results.json")
