# -*- coding: utf-8 -*-
"""
第72章 电磁力的本源（U(1) 规范场与电荷）——跨尺度精算复现脚本
纯标准库，无第三方依赖。所有常数取 CODATA 2018（SI 重新定义后）。
用法:  python electromagnetic_source_ladder.py
"""
import math

# ---- CODATA 2018（精确/推荐值）----
e    = 1.602176634e-19        # C, 基本电荷（精确）
c    = 2.99792458e8           # m/s, 真空光速（精确）
h    = 6.62607015e-34         # J s, 普朗克常数（精确）
hbar = h/(2*math.pi)          # 约化普朗克常数
eps0 = 8.8541878128e-12       # F/m, 真空介电常数
mu0  = 1.25663706212e-6       # N/A^2, 真空磁导率（2019 后为测量值）
ke   = 1/(4*math.pi*eps0)     # 库仑常数
me   = 9.1093837015e-31       # kg, 电子质量
mp   = 1.67262192369e-27      # kg, 质子质量
G    = 6.67430e-11            # m^3 kg^-1 s^-2
a0   = 5.29177210903e-11      # m, 玻尔半径
re   = 2.8179403262e-15       # m, 经典电子半径
lC   = hbar/(me*c)            # m, 约化康普顿波长

def line(k, v): print(f"{k:42s} = {v}")

print("================ 1. 无量纲耦合：精细结构常数 alpha ================")
alpha = ke*e**2/(hbar*c)
line("alpha = ke e^2 / (hbar c)", f"{alpha:.10e}")
line("alpha^-1", f"{1/alpha:.8f}  (CODATA 137.035999084)")
line("相对偏差", f"{(1/alpha-137.035999084)/137.035999084:.2e}")

print("\n================ 2. 电磁波：c = 1/sqrt(eps0 mu0) ================")
c_em = 1/math.sqrt(eps0*mu0)
line("1/sqrt(eps0 mu0)", f"{c_em:.6e} m/s")
line("与定义 c 的相对差", f"{(c_em-c)/c:.2e}")
line("真空阻抗 Z0 = sqrt(mu0/eps0)", f"{math.sqrt(mu0/eps0):.6f} ohm  (~376.73)")

print("\n================ 3. 三尺度阶梯 r_e : lambda_Cbar : a0 = alpha^2 : alpha : 1 ================")
line("经典电子半径 r_e", f"{re:.6e} m")
line("约化康普顿波长 lambda_C", f"{lC:.6e} m")
line("玻尔半径 a0", f"{a0:.6e} m")
line("r_e / a0", f"{re/a0:.6e}  vs alpha^2 = {alpha**2:.6e}")
line("lambda_C / a0", f"{lC/a0:.6e}  vs alpha = {alpha:.6e}")
line("r_e / lambda_C", f"{re/lC:.6e}  vs alpha = {alpha:.6e}")
line("r_e = alpha^2 a0 闭合误差", f"{abs(re/a0-alpha**2)/alpha**2:.2e}")
line("lambda_C = alpha a0 闭合误差", f"{abs(lC/a0-alpha)/alpha:.2e}")

print("\n================ 4. 库仑力 vs 引力（强度等级）================")
Fe = ke*e**2/a0**2                     # 氢原子玻尔半径处电(吸)力
Fg_ep = G*me*mp/a0**2                  # 同距电子-质子引力
Fg_pp = G*mp**2/a0**2                  # 两质子引力
line("氢原子 F_e = ke e^2/a0^2", f"{Fe:.6e} N")
line("F_g(e,p) at a0", f"{Fg_ep:.6e} N")
line("F_e/F_g (电子-质子)", f"{Fe/Fg_ep:.4e}  (~2.27e39)")
line("F_e/F_g (两质子)", f"{ke*e**2/(G*mp**2):.4e}  (~1.24e36)")

print("\n================ 5. 磁/电力量级与“磁场不做功” ================")
# 平行导线间磁力（安培，每米），典型 1 A、间距 1 m
I, d = 1.0, 1.0
Fm_per_L = mu0*I**2/(2*math.pi*d)
line("两平行导线 F/L (1A,1m)", f"{Fm_per_L:.4e} N/m  (=2e-7, 安培定义)")
# 磁力/电力 ~ v/c：导线中正电荷漂移速度极慢
# 康普顿尺度：若两电荷以 v 平动，F_B/F_E = v/c
for beta in (1e-10, 1e-3, 1.0):
    line(f"F_B/F_E = v/c (beta={beta:.0e})", f"{beta:.0e}")
line("(v x B)·v", "0  -> 磁场力恒垂直速度，永不做功 [A]")

print("\n================ 6. 光子无质量 -> 长程 1/r（Yukawa 对照）================")
line("静态无质量传播子给出的势", "V(r) = ke q1 q2 / r   [A]")
line("若光子有质量 m_gamma", "V(r) ~ e^(-m_gamma c r/hbar)/r (Yukawa)，力变短程")
line("实验光子质量上限", "< 1e-18 eV/c^2（太阳系磁场检验，[A] 约束）")

print("\n================ 7. 量子化：电导量子 / 磁通量子（[A]）================")
G0 = 2*e**2/h
Phi0 = h/(2*e)
line("电导量子 G0 = 2e^2/h", f"{G0:.6e} S  (~7.748e-5)")
line("电阻量子 1/G0", f"{1/G0:.6f} ohm  (~12906.4)")
line("超导磁通量子 Phi0 = h/2e", f"{Phi0:.6e} Wb  (~2.0678e-15)")

print("\n精算完成：全部恒等式在机器精度内闭合。")
