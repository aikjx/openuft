# -*- coding: utf-8 -*-
"""openuft/07_统一场方程 · 编号 31 = 系列 33 · 第一性原理推导总卷锚点
250-digit recomputation of first-principle derivation anchors:
  R2: surface gravity g = G M_earth / R_earth^2
  R3: Mercury perihelion precession dphi = 6 pi G M_sun / (c^2 a (1-e^2))
      -> arcsec/orbit, orbits/century (T=87.969 d), arcsec/century
  R3: solar light deflection theta = 4 G M_sun / (c^2 R_sun)
Writes 31_firstprinciples_calc_results.json
"""
import json
import mpmath as mp

mp.mp.dps = 250
res = {}

c = mp.mpf("299792458")
c2 = c ** 2
pi = mp.pi

# --- R2 surface gravity ---
GM_earth = mp.mpf("3.986004418e14")   # m^3/s^2 (standard gravitational parameter)
R_earth = mp.mpf("6.378137e6")        # m
g_surf = GM_earth / R_earth ** 2
res["r2_surface_g"] = {
  "GM_earth (m^3/s^2)": mp.nstr(GM_earth, 250),
  "R_earth (m)": mp.nstr(R_earth, 250),
  "g = GM/R^2 (m/s^2)": mp.nstr(g_surf, 250),
  "verdict": "与 9.798 m/s^2（纬度 45 海平面实测）一致；牛顿势 ∇²Φ=4πGρ → Φ=−GM/r 的第一性导出得到同一 g",
}

# --- R3 Mercury perihelion precession ---
GM_sun = mp.mpf("1.32712440018e20")
AU = mp.mpf("1.495978707e11")
a_merc = mp.mpf("0.387098") * AU       # semi-major axis, m
e_merc = mp.mpf("0.205630")
dphi_rad = 6 * pi * GM_sun / (c2 * a_merc * (1 - e_merc ** 2))
arcsec = mp.mpf("206264.806247096355156473357330778613196659700879311329135046572266904327")
dphi_as_orbit = dphi_rad * arcsec
orbits_cy = mp.mpf("100") * mp.mpf("365.25") / mp.mpf("87.969")   # orbits per century
dphi_as_cy = dphi_as_orbit * orbits_cy
res["r3_mercury"] = {
  "a (m)": mp.nstr(a_merc, 250),
  "e": "0.205630",
  "dphi (rad/orbit)": mp.nstr(dphi_rad, 250),
  "dphi (arcsec/orbit)": mp.nstr(dphi_as_orbit, 250),
  "orbits/century": mp.nstr(orbits_cy, 250),
  "dphi (arcsec/century)": mp.nstr(dphi_as_cy, 250),
  "verdict": "文献值 42.98″/cy；GR 第一性推导（史瓦西测地线 + 变分）吻合",
}

# --- R3 solar light deflection ---
R_sun = mp.mpf("6.957e8")              # m
theta_rad = 4 * GM_sun / (c2 * R_sun)
theta_as = theta_rad * arcsec
res["r3_deflection"] = {
  "R_sun (m)": mp.nstr(R_sun, 250),
  "theta (rad)": mp.nstr(theta_rad, 250),
  "theta (arcsec)": mp.nstr(theta_as, 250),
  "verdict": "文献值 1.75″；GR 第一性推导（弱场度规 g_00=1−2GM/(c²r)）吻合",
}

# --- Cross-volume anchors (previously computed, cited) ---
res["cross_volume_anchors"] = {
  "r4_gw_chirp": "GW150914 啁啾质量 28.0955558 M☉（21 D3，250 位）",
  "r5_ew": "M_W/M_Z=cosθ_W=0.88144660（17，250 位）",
  "r6_running": "SM 三耦合 L=25.451/28.607/34.590 互异（25 I2）；MSSM 共点 M_GUT=2.009×10¹⁶ GeV、α_G=0.0411477（25 I1）",
  "r7_qg": "弦临界维 c=D−26=0 / c=(3/2)D−15=0 → D=26/10（26 J1）；LQG A_min=1.350373420…×10⁻⁶⁹ m²（30，250 位）",
  "r8_verdict": "判决窗口全部锚点见 31（可证伪预言卷）",
}

print(json.dumps(res, ensure_ascii=False, indent=2))
with open(r"D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\31_firstprinciples_calc_results.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("\nOK -> 31_firstprinciples_calc_results.json")
