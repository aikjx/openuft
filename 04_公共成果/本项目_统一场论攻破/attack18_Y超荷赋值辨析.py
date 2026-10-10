# -*- coding: utf-8 -*-
"""attack18_Y超荷赋值辨析.py (v2 修正)
算法联盟最高权限 · 独立复算
修正：A_YYY 立方反常必须带手征符号(左手+，右手−)。
正确验证 SM 超荷 {1/6,2/3,-1/3,-1/2,-1} 满足全部反常消去(比例唯一)。
核心辨析仍成立：lambda_8 是色生成元(色T_8荷)，非味超荷。
纯标准库 + numpy + fractions。
"""
from fractions import Fraction as Fr

Y_Q, Y_u, Y_d, Y_L, Y_e = Fr(1,6), Fr(2,3), Fr(-1,3), Fr(-1,2), Fr(-1)

def show(name, expr):
    print(f"    {name} = {expr}  {'PASS(=0)' if expr==0 else 'FAIL(!=0)'}")

print("="*62)
print("attack18 v2 · Y 超荷赋值辨析（修正手征符号）")
print("="*62)

print("\n[1] SM 超荷比例（电荷量子化 Q=T3+Y, Q_u=2/3,Q_d=-1/3,Q_e=-1）:")
print(f"    Y_Q={Y_Q}, Y_u={Y_u}, Y_d={Y_d}, Y_L={Y_L}, Y_e={Y_e}")

print("\n[2] 反常消去（带手征符号: 左手+，右手−）:")

# A_{SU(3)^2 Y}: 左手Q_L(u_L,d_L各色3) +1/2·Y, 右手u_R,d_R -1/2·Y
A33Y = Fr(2)*(Y_Q) - Y_u - Y_d   # 2Y_Q - Y_u - Y_d (公共T2=1/2抽出)
show("A_{SU(3)^2Y} ∝ 2Y_Q - Y_u - Y_d", A33Y)

# A_{SU(2)^2 Y}: 左手弱双态 Q_L(3色), L; 右手单态 T2=0
A22Y = 3*Y_Q + Y_L
show("A_{SU(2)^2Y} ∝ 3Y_Q + Y_L", A22Y)

# A_{Y^3}: 左手[6Y_Q^3+2Y_L^3] − 右手[3Y_u^3+3Y_d^3+Y_e^3]
Ayyy_left  = 6*Y_Q**3 + 2*Y_L**3
Ayyy_right = 3*Y_u**3 + 3*Y_d**3 + Y_e**3
Ayyy = Ayyy_left - Ayyy_right
show("A_{Y^3} = [6Y_Q³+2Y_L³] − [3Y_u³+3Y_d³+Y_e³]", Ayyy)

# A_{Y-grav}: 左手[6Y_Q+2Y_L] − 右手[3Y_u+3Y_d+Y_e]
Ayg_left  = 6*Y_Q + 2*Y_L
Ayg_right = 3*Y_u + 3*Y_d + Y_e
Ayg = Ayg_left - Ayg_right
show("A_{Y-grav} = [6Y_Q+2Y_L] − [3Y_u+3Y_d+Y_e]", Ayg)

print("\n[3] 结果: SM 超荷 {1/6,2/3,-1/3,-1/2,-1} 全部反常消去 PASS")
print("    -> 超荷【比例】由反常消去+电荷量子化唯一确定(一代即消，三代同)")

print("\n[4] 核心辨析(维持 v1): lambda_8 是 su(3) 色生成元(第8生成元)")
print("    Tr(lambda_8)=0, 本征值 {1/√3,1/√3,-2/√3} = 色 T_8 量子数(红/绿/蓝)")
print("    -> 色自由度，非味超荷；SM 每色夸克带相同弱超荷(Y⊗1_3)")

print("\n[5] U(1)_Y 归一化: 比例唯一，但数值归一化是约定")
print("    (Y→λY 同时 g'→g'/λ 保持物理不变)")
print("    lambda_8 色荷(3个: 1/3,1/3,-2/3) vs SM 味超荷(5个: 1/6,2/3,-1/3,-1/2,-1)")
print("    维度不同(3≠5)、空间不同(色 vs 味) -> 不能作为 Y 归一化来源")

print("\n[6] S13 ch23 判定:")
print("    ch23 把 lambda_8 本征值 {1/3,1/3,-2/3} 标为'超荷比例' = 概念混淆")
print("    (那是色 T_8 荷，非味超荷)；弱结构(3=2⊕1)正确，但超荷数值来源未给")

print("="*62)
print("结论：攻破18 修正后——SM 超荷比例唯一(PASS)，但几何归一化缺口仍在。")
