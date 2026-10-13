# -*- coding: utf-8 -*-
"""二十四期·标准框架攻坚 线D深化 黑洞光子环数值靶（2026-10-14）
Schwarzschild/Kerr 光子球与阴影解析；M87*/Sgr A* 阴影角径 vs EHT 观测；光子环分辨判据。
标准 GR 解析公式（A 级）。mpmath 250 位。
"""
import mpmath as mp
mp.mp.dps = 250
mp.pretty = True

c = mp.mpf("299792458")           # m/s
G = mp.mpf("6.67430e-11")         # m³/(kg·s²)
Msun = mp.mpf("1.98847e30")       # kg
Mpc = mp.mpf("3.0856775814913673e22")   # m
kpc = mp.mpf("3.0856775814913673e19")   # m
muas_rad = mp.mpf("4.84813681109536e-12")  # 1 μas in rad（1 arcsec=4.848e-6 rad）

print("===== 线D深化 黑洞光子环数值靶（250 位）=====")

# ① Schwarzschild 光子球/阴影解析
print("\n① Schwarzschild 解析（A 级公式）")
rph_s = mp.mpf(3) * G / c**2          # 光子球半径（每单位质量）
bc_s  = mp.mpf(3) * mp.sqrt(mp.mpf(3)) * G / c**2  # 临界冲击参数 b_c=3√3 GM/c²
print("  光子球 r_ph = 3 GM/c² = 3.000000 M（每单位质量）")
print("  阴影 b_c     = 3√3 GM/c² = %.6f M" % (bc_s / (G/c**2)))

# ② Kerr 光子球范围（极坐标轨道）
print("\n② Kerr 光子球范围（a* 从 0 到 1）")
def r_ph_kerr(a):
    # r_ph± = 2M[1+cos(2/3·arccos(∓a))]，a=a*/M
    cos1 = mp.cos(mp.mpf(2)/mp.mpf(3) * mp.acos(-a))
    cos2 = mp.cos(mp.mpf(2)/mp.mpf(3) * mp.acos( a))
    return mp.mpf(2)*(1+cos1), mp.mpf(2)*(1+cos2)
for a in (mp.mpf("0"), mp.mpf("0.5"), mp.mpf("0.94"), mp.mpf("1")):
    rp, rm = r_ph_kerr(a)
    print("  a*=%.2f → r_ph ∈ [%.4f M, %.4f M]" % (a, rp, rm))

# ③ M87* 阴影角径（M=6.5e9 M_sun，D=16.8 Mpc）
print("\n③ M87*（EHT 2019：M=6.5e9 M_sun，D=16.8 Mpc）")
M87 = mp.mpf("6.5e9") * Msun
D87 = mp.mpf("16.8") * Mpc
GM87 = G * M87 / c**2
ang87_s = mp.mpf(2) * bc_s * M87 / D87   # 注意 bc_s 含 GM/c²，直接乘 M 后除以 D：2·b_c·(GM/c²)/D
# 更直接：b_c 是"每单位质量"的冲击参数，实际 b = b_c·(GM/c²)/1? 标准：b_c = 3√3 GM/c²（量纲长度）
b87 = mp.mpf(3)*mp.sqrt(mp.mpf(3)) * GM87      # 临界冲击参数（m）
ang87 = mp.mpf(2)*b87 / D87                    # 阴影角径（rad）
print("  GM/c² = %.4e m = %.4e km" % (GM87, GM87/1000))
print("  b_c   = %.4e m" % b87)
print("  阴影角径 = %.4f μas（Schw；历期 Kerr a*=0.94 → 39.03 μas）" % (ang87/muas_rad))
print("  EHT 2019 观测 = 42±3 μas —— Schw 理论符合（A 级）")

# ④ Sgr A* 阴影角径（M=4.154e6 M_sun，D=8.178 kpc）
print("\n④ Sgr A*（GRAVITY/EHT：M=4.154e6 M_sun，D=8.178 kpc）")
Sgr = mp.mpf("4.154e6") * Msun
Dsgr = mp.mpf("8.178") * kpc
GMsgr = G * Sgr / c**2
bsgr = mp.mpf(3)*mp.sqrt(mp.mpf(3)) * GMsgr
angsgr = mp.mpf(2)*bsgr / Dsgr
print("  GM/c² = %.4e m；b_c = %.4e m" % (GMsgr, bsgr))
print("  阴影角径 = %.4f μas" % (angsgr/muas_rad))
print("  EHT 2022 观测 = 51.8±2.3 μas（A 级）—— 理论符合")

# ⑤ 光子环结构与分辨判据
print("\n⑤ 光子环结构与分辨判据（C 级待部署）")
print("  光子环：光子绕行 n 圈后到达——n=1 环位于阴影边缘，宽度 ~ O(M)；亮度随 n 指数衰减")
print("  M87* 上光子环特征尺度 ~ 数 μas；EHT 230 GHz 分辨率 ~25 μas 仅见阴影")
print("  ngEHT/黑洞相机目标分辨率 ~10-20 μas → 分辨光子环子结构（GR 与修正引力判决实验）")
print("  光子环直接成像可检验：无标度性质（光子环不依赖黑洞质量）、环位置编码 a*/自旋")

print("\n-- 结论 --")
print("GR 光子球/阴影解析与 EHT 观测（M87* 42±3、Sgr A* 51.8±2.3 μas）符合（A 级）；")
print("光子环直接分辨是 GR 判决实验（C 级，待 ngEHT）——引力本源仍无统一（诚实红线不变）。")
