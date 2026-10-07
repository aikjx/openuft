# -*- coding: utf-8 -*-
# V3_2_Skyrme_hedgehog玩具.py  —— §7C 支撑（待精修草稿，勿当结论）
# 目的：演示 SU(2) hedgehog 拓扑孤子的拓扑荷 B 与半整数自旋判据。
# 【诚实边界】本脚本手推 Skyrme 能量泛函 ODE，径向轮廓未收敛到干净 F->0 separatrix
# （解渐近到非零常数，需按标准 Skyrme 求解器精校 f_pi/e 标度）。
# 但 §7C 的两个核心结论是严格的、不依赖本脚本轮廓：
#   (1) B = -[F(inf)-F(0)]/pi = F(0)/pi = 1  （端点差拓扑恒等式）
#   (2) Witten 1983: 奇数 B => 集体量子化自旋 s=|B|/2=1/2（费米子）
# 对比 TUFT Q-ball: 目标 C 可缩 pi_3=0 => 无 B => 玻色子。
import numpy as np
from scipy.integrate import solve_ivp
V1,V2=1.2,0.4
def rhs(r,y):
    F,Fp=y
    s2=np.sin(F)**2; s2c=np.sin(2*F); denom=r**2+2*s2
    return [Fp, -(2*r*Fp + 0.5*s2c*(2*Fp**2-1-s2/r**2))/denom]
# 边界（拓扑，精确）
F0=np.pi; Finf=0.0
B=-(Finf-F0)/np.pi
print(f"边界 F(0)=pi, F(inf)=0")
print(f"拓扑荷 B = -[F(inf)-F(0)]/pi = {B}  (整数, 奇数)")
print(f"Witten: B 奇数 => 集体量子化自旋 s=|B|/2 = {B/2} (费米子)")
print("注：径向轮廓打靶未收敛（见 15B §7C.4 诚实边界），待标准 Skyrme 求解器精修。")
