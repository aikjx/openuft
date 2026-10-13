# -*- coding: utf-8 -*-
"""openuft/07_统一场方程 · 编号 36 = 系列 38 · 暗物质候选全景卷锚点
250-digit anchors:
  axion: m_a = 5.7 ueV (10^12 GeV / f_a)  ->  de Broglie frequency nu_a = m_a c^2 / h
  local DM density: 0.3 GeV/cm^3 -> kg/m^3 (1 GeV/c^2 = 1.78266192e-27 kg)
  Omega_DM/Omega_b from volume 32 (recomputed there)
Cited: Planck 2018 Omega_DM h^2 = 0.1200; LZ / XENONnT / ADMX status (literature).
Writes 36_darkmatter_calc_results.json
"""
import json
import mpmath as mp

mp.mp.dps = 250
res = {}

# QCD axion: m_a = 5.7 ueV * (10^12 GeV / f_a)
m_a = mp.mpf("5.7e-6")                      # eV, f_a = 1e12 GeV
h_eVs = mp.mpf("4.135667696e-15")           # h in eV*s (CODATA 2022)
nu_a = m_a / h_eVs                          # Hz
res["axion"] = {
  "m_a (eV, f_a=1e12 GeV)": mp.nstr(m_a, 250),
  "nu_a = m_a c^2/h (Hz)": mp.nstr(nu_a, 250),
  "nu_a (GHz)": mp.nstr(nu_a * mp.mpf("1e-9"), 250),
  "note": "QCD 轴子窗口 m_a~5.7 ueV(10^12 GeV/f_a)（文献）；ADMX 谐振腔探测窗口 ~GHz",
}

# Local DM density conversion
GeV2kg = mp.mpf("1.78266192e-27")
rho_cgs = mp.mpf("0.3")                     # GeV/cm^3
rho_kg_m3 = rho_cgs * GeV2kg * mp.mpf("1e6")  # per m^3
res["local_dm"] = {
  "rho_DM (GeV/cm^3)": mp.nstr(rho_cgs, 250),
  "rho_DM (kg/m^3)": mp.nstr(rho_kg_m3, 250),
  "note": "局域暗物质密度标准值 0.3 GeV/cm^3（文献）；换算 kg/m^3 见左",
}

res["omega_ratio"] = {
  "Omega_DM/Omega_b": "5.3752535497…（32 卷 250 位现算，Omega_DM=0.2645/Omega_b=0.0492 类基准）",
  "Omega_DM h^2": "0.1200（Planck 2018，文献）",
}

res["cited_anchors"] = {
  "wimp": "LZ/XENONnT：1 TeV WIMP 截面上限 ~1e-47 cm^2 量级（文献 2023-2024）；弱作用窗口持续收缩",
  "axion_search": "ADMX：探测 ~GHz 谐振腔窗口（文献）；QCD 轴子与强 CP（34 U4）同一机制候选",
  "alternatives": "MOND：RAR 17-sigma 排除（22）；原初黑洞：微透镜/蒸发约束（文献）",
  "tuft": "TUFT 声称'暗物质=时空挠率全域耦合'——无质量谱、无探测预言（22/23 G1-G5）",
  "verdict": "暗物质粒子身份=32 Q1 开放项；候选均有判决窗口（31 P 系列）",
}

print(json.dumps(res, ensure_ascii=False, indent=2))
with open(r"D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\36_darkmatter_calc_results.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("\nOK -> 36_darkmatter_calc_results.json")
