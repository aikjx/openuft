# -*- coding: utf-8 -*-
"""42 期诊断3：Schwarzschild 1PN Binet 方程 u''+u = GM/h^2 + (3GM/c^2)u^2
积分角度域求近点进动，独立验证解析式 6*pi*GM/(c^2*a*(1-e^2))"""
import math
GM = 1.32712440018e20; c = 2.99792458e8
a = 5.7909227e10; e = 0.205630
r_p = a*(1-e); v_p = math.sqrt(GM*(1+e)/(a*(1-e)))
h = r_p*v_p  # 角动量
print("r_p=%.6e v_p=%.6e h=%.6e" % (r_p, v_p, h))
A = GM/(h*h); B = 3*GM/(c*c)
print("GM/h^2=%.6e  3GM/c^2=%.6e" % (A, B))

def f(phi, u, ud):
    return A + B*u*u - u

# RK4 角度域积分
u0 = 1/r_p; ud0 = 0.0
dphi = 0.005
peris = []
u = u0; ud = ud0
prev_u = u
falling = False
u_min = u; phi_min = 0.0
for i in range(int(4*math.pi/dphi)):
    phi = i*dphi
    k1 = f(phi, u, ud)
    k2 = f(phi+dphi/2, u+dphi*ud/2, ud+dphi*k1/2)
    k3 = f(phi+dphi/2, u+dphi*ud/2+dphi*dphi*k1/4, ud+dphi*k2/2)
    k4 = f(phi+dphi, u+dphi*ud+dphi*dphi*k2/2, ud+dphi*k3)
    u += dphi*(ud + dphi*(k1+k2+k3)/6)
    ud += dphi*(k1+2*k2+2*k3+k4)/6
    # u 极小 = 近日点 (u 最大处为近点，因 u=1/r；u 最大=近点)
    # 实际近点 = u 最大
    if u > prev_u:
        falling = True
    elif falling:
        peris.append((phi, u))
        falling = False
    prev_u = u
print("近点（u 极大）相位：", ["%.6f" % p for p, _ in peris])
ds = [peris[i+1][0]-peris[i][0] for i in range(len(peris)-1)]
print("圈进动 =", ["%+.6e" % (d-2*math.pi) for d in ds])
print("解析 6*pi*GM/(c^2*a*(1-e^2)) = %+.6e" % (6*math.pi*GM/(c*c*a*(1-e*e))))
print("解析 6*pi*GM/(c^2*r_p) = %+.6e" % (6*math.pi*GM/(c*c*r_p)))
