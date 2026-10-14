# -*- coding: utf-8 -*-
"""openuft/07_统一场方程 · 编号 43 = 系列 45 · 引力波频谱全景卷锚点
250-digit anchors: wavelength per band lambda = c / f
  PTA   f = 1e-8 Hz  (NANOGrav 2023)
  LISA  f = 3e-3 Hz  (space interferometer sweet spot)
  LIGO  f = 100 Hz   (ground interferometer typical)
  CMB B f = 1e-17 Hz (primordial, r < 0.036)
Cited: r<0.036 (BICEP/Keck 2021), GW150914 (21), GW170817 (42), NANOGrav 2023 (42).
Writes 43_gwspectrum_calc_results.json
"""
import json
import mpmath as mp

mp.mp.dps = 250
res = {}
c = mp.mpf("299792458")

def lam(f):
    return c / f

bands = [
  ("PTA", "1e-8", mp.mpf("1e-8")),
  ("LISA", "3e-3", mp.mpf("3e-3")),
  ("LIGO", "100", mp.mpf("100")),
  ("CMB B-mode", "1e-17", mp.mpf("1e-17")),
]
res["wavelengths"] = {}
for name, flab, f in bands:
    l = lam(f)
    res["wavelengths"][name] = {
      "f (Hz)": flab,
      "lambda (m)": mp.nstr(l, 250),
      "lambda (log10 m)": mp.nstr(mp.log10(l), 250),
    }

res["cited_anchors"] = {
  "r": "<0.036（BICEP/Keck 2021，文献）——原初张量-标量比上限：CMB B 模未探测，原初 GW 窗口开放（31 卷）",
  "gw150914": "GW150914 啁啾 28.0955558 M_sun（21 卷现算）；后振铃 QNM ≈250 Hz（41 卷）",
  "gw170817": "GW170817 多信使：双中子星合并+kilonova；Λ₁.₄=190–640（42 卷）",
  "nanograv": "NANOGrav 2023 PTA：纳赫兹随机背景信号（42 卷）；来源开放",
  "tuft": "TUFT'引力=螺旋收敛'——无 GW 频谱、无色偏振、无频段预言（23 G1–G5）",
}

print(json.dumps(res, ensure_ascii=False, indent=2))
with open(r"D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\43_gwspectrum_calc_results.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("\nOK -> 43_gwspectrum_calc_results.json")
