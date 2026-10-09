# -*- coding: utf-8 -*-
# 第5层：Kaluza-Klein 大统一方向精算（重建版）
import math

G = 6.67430e-11
hbar = 1.054571817e-34
c = 2.99792458e8
alpha = 0.0072973525693

print('='*72)
print('第5层 一、5维度量分解（几何化U(1)）')
print('  G_AB(15) = g_μν(10) + A_μ(4) + φ(1)  ✓ 分量守恒')
print('  => 5维纯几何自动包含引力+电磁（真实的部分统一）')

print('='*72)
print('第5层 二、电荷量子化 = 第5维动量')
print('  p5 = n*hbar/R (n=0,±1,...)')
print('  => 电荷是基本单位的整数倍（几何来源）')

print('='*72)
print('第5层 三、经典KK半径（修正：sqrt）')
num = G*hbar/(math.pi*alpha*c**3)
R_KK = math.sqrt(num)
l_Pl = math.sqrt(G*hbar/c**3)
print(f'  R_KK = √(Gℏ/(παc³)) = {R_KK:.4e} m')
print(f'  错误公式 Gℏ/(παc³) = {num:.4e} m²（量纲m²，已修正）')
print(f'  普朗克长度 l_Pl = {l_Pl:.4e} m, R_KK/l_Pl = {R_KK/l_Pl:.2f}')

print('='*72)
print('第5层 四、KK质量塔')
J_to_GeV = 1/1.602176634e-10
M1_GeV = hbar*c/R_KK * J_to_GeV
M_Pl = math.sqrt(hbar*c/G)*c**2*J_to_GeV
print(f'  M_1 = ℏc/R_KK = {M1_GeV:.4e} GeV')
print(f'  M_Pl = √(ℏc/G)·c² = {M_Pl:.4e} GeV, M_1/M_Pl = {M1_GeV/M_Pl:.3f}')

print('='*72)
print('第5层 五、对撞机约束 -> R 上界')
R_1TeV = hbar*c/(1e12*1.602176634e-19)
print(f'  ℏc/(1TeV) = {R_1TeV:.4e} m')
print(f'  LHC保守(M₁>1TeV): R < {R_1TeV:.4e} m')
print(f'  LEP精密(M₁>5TeV): R < {R_1TeV/5:.4e} m')
print(f'  LHC综合(M₁>10TeV): R < {R_1TeV/10:.4e} m')
print(f'  => 实验上界(~1e-20m)比经典R_KK({R_KK:.2e}m)大15个量级 → 经典KK已被排除')

print('='*72)
print('第5层 六、规范群与所需维度')
print('  U(1)→5D S¹ · SU(2)→6D S² · SU(3)→8D CP² · 完整SM→10D Calabi-Yau/11D G₂-M')
print('  => 5维仅统一引力+电磁；弱/强需完整弦论机制')

print('='*72)
print('结论：0·1·∞"纯几何统一四力"在正确物理中最远只能走到')
print('  引力+电磁的5维几何统一(已被实验排除) 或 10维弦论(未完成、未验证)')
print('='*72)
