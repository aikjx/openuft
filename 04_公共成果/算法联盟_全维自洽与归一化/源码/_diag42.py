# -*- coding: utf-8 -*-
"""42 期诊断：检查数值轨道与 (a,e) 一致性 + 近点进动逐圈分解"""
import math
GM = 1.32712440018e20; c = 2.99792458e8
a = 5.7909227e10; e = 0.205630
r_p = a*(1-e); v_p = math.sqrt(GM*(1+e)/(a*(1-e)))
T = 2*math.pi*math.sqrt(a**3/GM)
print("r_p=%.6e v_p=%.6e T=%.4e" % (r_p, v_p, T))

def acc(x, y, vx, vy):
    r2 = x*x+y*y; r = math.sqrt(r2); r3 = r2*r
    v2 = vx*vx+vy*vy; rv = x*vx+y*vy
    aNx = -GM*x/r3; aNy = -GM*y/r3
    k = GM/(c*c*r3)
    return aNx + k*((4*GM/r-v2)*x+4*rv*vx), aNy + k*((4*GM/r-v2)*y+4*rv*vy)

def rk4(acc, x0, y0, vx0, vy0, T, dt):
    x, y, vx, vy = x0, y0, vx0, vy0
    peris = []; r_prev = math.hypot(x, y); phi_acc = 0.0
    xp, yp = x, y
    n = int(math.ceil(T/dt)); t = 0.0
    falling = False; r_min = r_prev; t_min = t; phi_min = 0.0; r_max = r_prev
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
        if r > r_max: r_max = r
        if r < r_prev: falling = True; r_min = r; t_min = t; phi_min = phi_acc
        elif falling: peris.append((t_min, phi_min)); falling = False
        r_prev = r
    if falling: peris.append((t_min, phi_min))
    return peris, r_max, r_min

# peris 明细：dt=100s，2.5 圈
peris, r_max, r_min = rk4(acc, r_p, 0.0, 0.0, v_p, 2.5*T, 100.0)
for i, (tt, pp) in enumerate(peris):
    print("peris[%d]: t=%.4e phi=%.9f phi-2pi*k=%+.3e" % (i, tt, pp, pp-2*math.pi*(i+1)))

dt = 200.0
x, y, vx, vy = r_p, 0.0, 0.0, v_p
xp, yp = x, y
n = int(math.ceil(1.2*T/dt)); phi_acc = 0.0
rows = []
for i in range(n):
    ax1, ay1 = acc(x, y, vx, vy)
    ax2, ay2 = acc(x+dt*vx/2, y+dt*vy/2, vx+dt*ax1/2, vy+dt*ay1/2)
    ax3, ay3 = acc(x+dt*vx/2+dt*dt*ax1/4, y+dt*vy/2+dt*dt*ay1/4, vx+dt*ax2/2, vy+dt*ay2/2)
    ax4, ay4 = acc(x+dt*vx+dt*dt*ax2/2, y+dt*vy+dt*dt*ax2/2, vx+dt*ax3, vy+dt*ay3)
    x += dt*(vx+dt*(ax1+ax2+ax3)/6); y += dt*(vy+dt*(ay1+ay2+ay3)/6)
    vx += dt*(ax1+2*ax2+2*ax3+ax4)/6; vy += dt*(ay1+2*ay2+2*ay3+ay4)/6
    dphi = math.atan2(y*xp-x*yp, x*xp+y*yp); phi_acc += dphi
    xp, yp = x, y
    r = math.hypot(x, y)
    if i % 200 == 0:
        rows.append((i*dt, r, phi_acc))
for t, r, ph in rows:
    print("t=%.2e r=%.6e phi_acc=%.6f" % (t, r, ph))
print("末态: t=%.2e r=%.6e phi=%.6f" % (n*dt, math.hypot(x, y), phi_acc))

