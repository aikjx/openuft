# -*- coding: utf-8 -*-
"""42 期诊断2：EIH 1PN 进动随 e 扫描，验证公式实现"""
import math
GM = 1.32712440018e20; c = 2.99792458e8

def acc_eih(x, y, vx, vy):
    r2 = x*x+y*y; r = math.sqrt(r2); r3 = r2*r
    v2 = vx*vx+vy*vy; rv = x*vx+y*vy
    aNx = -GM*x/r3; aNy = -GM*y/r3
    k = GM/(c*c*r3)
    return aNx + k*((4*GM/r-v2)*x+4*rv*vx), aNy + k*((4*GM/r-v2)*y+4*rv*vy)

def acc_newt(x, y, vx, vy):
    r3 = (x*x+y*y)**1.5
    return -GM*x/r3, -GM*y/r3

def rk4(acc, x0, y0, vx0, vy0, T, dt):
    x, y, vx, vy = x0, y0, vx0, vy0
    peris = []; r_prev = math.hypot(x, y); phi_acc = 0.0
    xp, yp = x, y
    n = int(math.ceil(T/dt)); t = 0.0
    falling = False; r_min = r_prev; t_min = t; phi_min = 0.0
    for i in range(n):
        ax1, ay1 = acc(x, y, vx, vy)
        ax2, ay2 = acc(x+dt*vx/2, y+dt*vy/2, vx+dt*ax1/2, vy+dt*ay1/2)
        ax3, ay3 = acc(x+dt*vx/2+dt*dt*ax1/4, y+dt*vy/2+dt*dt*ay1/4, vx+dt*ax2/2, vy+dt*ay2/2)
        ax4, ay4 = acc(x+dt*vx+dt*dt*ax2/2, y+dt*vy+dt*dt*ay2/2, vx+dt*ax3, vy+dt*ay3)
        x += dt*(vx+dt*(ax1+ax2+ax3)/6); y += dt*(vy+dt*(ay1+ay2+ay3)/6)
        vx += dt*(ax1+2*ax2+2*ax3+ax4)/6; vy += dt*(ay1+2*ay2+2*ay3+ay4)/6
        t += dt
        dphi = math.atan2(y*xp-x*yp, x*xp+y*yp); phi_acc += dphi
        xp, yp = x, y
        r = math.hypot(x, y)
        if r < r_prev: falling = True; r_min = r; t_min = t; phi_min = phi_acc
        elif falling: peris.append((t_min, phi_min)); falling = False
        r_prev = r
    return peris

a0 = 5.7909227e10
for e in (0.01, 0.05, 0.1, 0.20563, 0.4, 0.6):
    r_p = a0*(1-e); v_p = math.sqrt(GM*(1+e)/(a0*(1-e)))
    T = 2*math.pi*math.sqrt(a0**3/GM)
    dt = 50.0 if e > 0.3 else 100.0
    pN = rk4(acc_newt, r_p, 0.0, 0.0, v_p, 2.05*T, dt)
    pE = rk4(acc_eih, r_p, 0.0, 0.0, v_p, 2.05*T, dt)
    if len(pN) >= 2 and len(pE) >= 2:
        dN = pN[1][1]-pN[0][1]; dE = pE[1][1]-pE[0][1]
        delta = dE - dN
        analytic = 6*math.pi*GM/(c*c*a0*(1-e*e))
        print("e=%.5f: 数值进动=%+.4e rad/圈  解析=+%.4e  比值=%.3f" % (e, delta, analytic, delta/analytic))
    else:
        print("e=%.5f: 近点不足" % e)
