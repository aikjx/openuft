# -*- coding: utf-8 -*-
"""openuft/07_统一场方程 · 编号 41 = 系列 43 · 黑洞观测与量子判决卷锚点
250-digit anchors:
  Schwarzschild radius: r_s = 2 G M / c^2
    SgrA*: M = 4.297e6 M_sun (EHT 2022, cited)
    M87*:  M = 6.5e9 M_sun (EHT 2019, cited)
  Hawking evaporation time: t_ev = 5120*pi*G^2*M^3/(hbar*c^4)
    PBH M = 1e12 kg
Cited: QNM ringdown ~250 Hz (GW150914), BH information paradox / Page curve open.
M_sun = 1.988409870e30 kg (IAU nominal, cited).
Writes 41_blackhole_calc_results.json
"""
import json
import mpmath as mp

mp.mp.dps = 250
res = {}

G = mp.mpf("6.67430e-11")
c = mp.mpf("299792458")
hbar = mp.mpf("1.054571817e-34")
Msun = mp.mpf("1.988409870e30")

def rs(M):
    return 2 * G * M / c**2

res["schwarzschild"] = {
  "r_s(SgrA* = 4.297e6 Msun) [m]": mp.nstr(rs(mp.mpf("4.297e6") * Msun), 250),
  "r_s(SgrA*) [au]": mp.nstr(rs(mp.mpf("4.297e6") * Msun) / mp.mpf("1.495978707e11"), 250),
  "r_s(M87* = 6.5e9 Msun) [m]": mp.nstr(rs(mp.mpf("6.5e9") * Msun), 250),
  "r_s(M87*) [au]": mp.nstr(rs(mp.mpf("6.5e9") * Msun) / mp.mpf("1.495978707e11"), 250),
  "note": "EHT 2022 SgrA* M=4.297e6 Msun、EHT 2019 M87* M=6.5e9 Msun（文献中心值）；r_s=2GM/c² 250 位现算；EHT 阴影√27/2·r_s 已在 31 卷现算",
}

tev = 5120 * mp.pi * G**2 / (hbar * c**4)
res["hawking_evaporation"] = {
  "t_ev(1e12 kg PBH) [s]": mp.nstr(tev * (mp.mpf("1e12") ** 3), 250),
  "t_ev(1e12 kg PBH) [yr]": mp.nstr(tev * (mp.mpf("1e12") ** 3) / mp.mpf("3.1557600e7"), 250),
  "note": "t_ev=5120πG²M³/(ħc⁴)；M=10¹² kg 原初黑洞 t_ev≈2.7×10¹² yr；32 卷太阳质量黑洞 t_ev=2.097×10⁶⁷ yr（M³ 标度自洽）",
}

res["cited_anchors"] = {
  "qnm": "GW150914 后振铃 QNM 基模频率 ≈250 Hz（文献）；LIGO 测量与 GR 一致（21 卷额外偏振被排除）",
  "info_paradox": "黑洞信息悖论：Page 曲线/岛屿公式候选（文献）；信息守恒无实验判决——32 Q6/35 V 的量子引力交叉",
  "tuft": "TUFT'黑洞=曲率挠率双极值'——无 r_s、无 QNM 谱、无蒸发率（23 G1–G5）",
}

print(json.dumps(res, ensure_ascii=False, indent=2))
with open(r"D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\41_blackhole_calc_results.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("\nOK -> 41_blackhole_calc_results.json")
