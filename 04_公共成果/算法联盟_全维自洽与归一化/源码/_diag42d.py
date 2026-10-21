# -*- coding: utf-8 -*-
"""42 期诊断4：Binet 1PN 进动，抛物线插值精确定位近点相位"""
import math
GM = 1.32712440018e20; c = 2.99792458e8
a = 5.7909227e10; e = 0.205630
r_p = a*(1-e); v_p = math.sqrt(GM*(1+e)/(a*(1-e)))
h = r_p*v_p
A = GM/(h*h); B = 3*GM/(c*c)

def f(phi, u, ud):
    return A + B*u*u - u

def integrate(N_circles, dphi):
    u = 1/r_p; ud = 0.0
    # 记录 u 的局部极大（近点）列表：(phi, u)
    maxima = []
    prev_u = u; rising = False
    # 第一次：u 从近点出发下降；先找远点（u 极小）再找近点
    for i in range(int(N_circles*2*math.pi/dphi)):
        phi = i*dphi
        k1 = f(phi, u, ud)
        k2 = f(phi+dphi/2, u+dphi*ud/2, ud+dphi*k1/2)
        k3 = f(phi+dphi/2, u+dphi*ud/2+dphi*dphi*k1/4, ud+dphi*k2/2)
        k4 = f(phi+dphi, u+dphi*ud+dphi*dphi*k2/2, ud+dphi*k3)
        u += dphi*(ud + dphi*(k1+k2+k3)/6)
        ud += dphi*(k1+2*k2+2*k3+k4)/6
        if u < prev_u:
            rising = True
        elif rising:
            # u 从降转升 = u 极小 = 远日点；下一个转折是 u 极大 = 近日点
            rising = False
        if u > prev_u and not rising:
            # 记录上升段，等极大
            rising = True
        # 检测 u 极大：u 曾上升现下降
        # 简化：保存每步，最后扫
    return maxima

# 直接每步记录，事后扫局部极大
def run(N_circles, dphi):
    u = 1/r_p; ud = 0.0
    phis = []; us = []
    for i in range(int(N_circles*2*math.pi/dphi)):
        phi = i*dphi
        k1 = f(phi, u, ud)
        k2 = f(phi+dphi/2, u+dphi*ud/2, ud+dphi*k1/2)
        k3 = f(phi+dphi/2, u+dphi*ud/2+dphi*dphi*k1/4, ud+dphi*k2/2)
        k4 = f(phi+dphi, u+dphi*ud+dphi*dphi*k2/2, ud+dphi*k3)
        u += dphi*(ud + dphi*(k1+k2+k3)/6)
        ud += dphi*(k1+2*k2+2*k3+k4)/6
        phis.append(phi+dphi); us.append(u)
    maxima = []
    for j in range(1, len(us)-1):
        if us[j] > us[j-1] and us[j] > us[j+1]:
            maxima.append((phis[j], us[j]))
    # 抛物线插值：围绕极大 (x0,y0) 三点拟合
    refined = []
    for j in range(1, len(us)-1):
        if us[j] > us[j-1] and us[j] > us[j+1]:
            x0, y0, ym, yp = phis[j], us[j], us[j-1], us[j+1]
            dx = dphi
            # 抛物线 y = y0 + c2*(x-x0)^2 + c1*(x-x0)
            c1 = (yp-ym)/(2*dx)
            c2 = (yp+ym-2*y0)/(2*dx*dx)
            xm = x0 - c1/(2*c2)
            refined.append((xm, y0 - c1*c1/(4*c2)))
    return refined

for dphi in (0.01, 0.002, 0.0005):
    maxima = run(3.05, dphi)
    ds = [maxima[i+1][0]-maxima[i][0] for i in range(len(maxima)-1)]
    print("dphi=%g: 近点相位=%s" % (dphi, ["%.9f" % m[0] for m in maxima]))
    print("  圈进动=%s" % (["%+.6e" % (d-2*math.pi) for d in ds]))
print("解析=+% .6e rad/圈" % (6*math.pi*GM/(c*c*a*(1-e*e))))
