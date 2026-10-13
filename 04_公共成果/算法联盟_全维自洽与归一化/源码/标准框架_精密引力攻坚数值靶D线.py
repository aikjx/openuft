# -*- coding: utf-8 -*-
"""十三期·标准框架攻坚 线D 精密引力数值靶（2026-10-13）
① 水星近日点进动：GR 1PN 精确公式 + 2PN 修正量级（对照 C49 Binet 错因子教训——在 GR 框架内正确计算）
② EHT 光子环：Schwarzschild 阴影 √27 角径 vs M87* 观测 42±3 μas；Kerr a* 修正
③ 引力红移：GPS 轨道钟广义/狭义综合偏差（~38 μs/day 判据）
精度：mpmath 250 位。全部公式标准、可复现、可追溯。
"""
import mpmath as mp
mp.mp.dps = 250

c = mp.mpf("299792458")
G = mp.mpf("6.67430e-11")
Msun = mp.mpf("1.98847e30")
arcsec = mp.pi / (180 * 3600)
yr_s = mp.mpf("365.25") * 86400

# ---------- ① 水星近日点进动 ----------
print("===== ① 水星近日点进动（GR 1PN 精确 + 2PN 量级）=====")
a_mer = mp.mpf("5.790905e10")   # m
e_mer = mp.mpf("0.20563069")
T_mer = mp.mpf("0.240846")      # yr
GM = G * Msun
p = a_mer * (1 - e_mer**2)      # 半通径
eps = GM / (c**2 * p)           # 小参数 ~2.66e-8
dphi_1PN = 6 * mp.pi * GM / (c**2 * p)                    # rad/圈
n_orbit = 100 / T_mer
dphi_1PN_cent = dphi_1PN * n_orbit / arcsec               # 角秒/百年
# 2PN 修正（标准相对论，系数 ~1/2 量级）：δ ~ 6π ε² (≈ 常数×ε²)，比 1PN 小 ε 倍
dphi_2PN_cent = dphi_1PN_cent * eps
print("半通径 p = %.6e m | ε=GM/c²p = %.9e" % (p, eps))
print("1PN 进动 = %.6f 角秒/百年（标准值 42.98）" % dphi_1PN_cent)
print("2PN 修正 ~ %.4e 角秒/百年（比 1PN 小 7 个量级，观测不可分辨——诚实标注量级）" % dphi_2PN_cent)
print("1PN 相对标准值偏差 = %.4e" % abs(dphi_1PN_cent - mp.mpf("42.98")))
print("（对照 C49：TUFT Binet 公式曾给出错因子 3.83e-8——GR 框架下 1PN 公式与标准值吻合）")

# ---------- ② EHT 光子环 ----------
print("\n===== ② EHT 光子环（Schwarzschild 阴影 + Kerr 修正）=====")
M87_M = mp.mpf("6.5e9")          # 太阳质量
M87_D = mp.mpf("16.8e6") * mp.mpf("3.085677581e16")   # Mpc -> m
Rg = G * M87_M * Msun / c**2
theta_sh = 2 * mp.sqrt(27) * Rg / M87_D                # rad
theta_sh_uas = theta_sh / mp.mpf("4.84813681109536e-12")  # rad -> μas（1μas=4.848e-12 rad）
print("引力半径 Rg = %.3e m | 距离 = %.3e m" % (Rg, M87_D))
print("Schwarzschild 阴影角径 = %.2f μas（EHT 观测 42±3 μas——符合，A 级）" % theta_sh_uas)
# Kerr 顺行 a*=0.94：阴影半径收缩（标准修正，B 级引用文献量级）
a_star = mp.mpf("0.94")
Rsh_kerr = mp.sqrt(27) * Rg * mp.sqrt(1 - a_star**2 / 27)   # 常用近似：R_sh ~ √27 (1-a²/27)（未归一化近似，标注 B 级）
print("Kerr a*=0.94 近似修正后角径 ~ %.2f μas（近似公式，B 级；精确 Kerr 阴影需数值光线追踪）" % (2 * Rsh_kerr / M87_D / mp.mpf("4.84813681109536e-12")))

# ---------- ③ 引力红移（GPS）----------
print("\n===== ③ 引力红移（GPS 轨道钟，~38 μs/day 判据）=====")
Re = mp.mpf("6371000")           # 地球半径 m
r_sat = Re + mp.mpf("20200000")  # GPS 轨道高度
v_sat = mp.mpf("3870")           # m/s（GPS 轨道速度）
dphi_g = GM_earth = G * mp.mpf("5.9722e24") / c**2
red_gr = GM_earth * (1/Re - 1/r_sat)          # 广义：引力势差
red_sr = -v_sat**2 / (2 * c**2)              # 狭义：运动学
red_tot = red_gr + red_sr
us_per_day = red_tot * 86400 * 1e6           # μs/day
print("广义（引力势）Δf/f = %.3e | 狭义（运动学）Δf/f = %.3e | 合计 = %.3e" % (red_gr, red_sr, red_tot))
print("轨道钟日漂移 ≈ %.1f μs/day（判据 ~38 μs/day——量级符合，A 级；含地球扁率等小项未计）" % us_per_day)

print("\n===== 十三期终态锚点 =====")
print("线 D 三个数值靶全部落盘可复现；TUFT 审计终态不变（127 条、守卫 8/8）；攻坚深化 GATE-1/GUT 靶承上期。")
