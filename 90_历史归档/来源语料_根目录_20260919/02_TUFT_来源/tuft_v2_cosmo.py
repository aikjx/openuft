# -*- coding: utf-8 -*-
"""
TUFT v2 宇宙学数值组
A. FLRW 摩擦项 phi 方程 + Friedmann 联立数值积分（对数时间 RK4）
B. NGC3198 MOND 型旋转曲线插值
C. BTFR 拟合
纯 numpy，无 scipy。
"""
import numpy as np

# ---------- 常数 ----------
G  = 6.674e-11
c  = 2.998e8
H0 = 2.27e-18
t0 = 4.35e17
M_SUN = 1.989e30
R_KPC = 3.086e19
rho_crit = 3*H0**2/(8*np.pi*G)
a0_TUFT = c*H0/(2*np.pi)
a0_MOND = 1.2e-10

print("="*70)
print("CONSTANTS CHECK")
print(f"  rho_crit        = {rho_crit:.3e} kg/m^3   (input ~9.9e-27)")
print(f"  a0 (TUFT cH0/2pi) = {a0_TUFT:.4e} m/s^2")
print(f"  a0 (std MOND)     = {a0_MOND:.3e} m/s^2")
print(f"  ratio a0_M/a0_T  = {a0_MOND/a0_TUFT:.3f}")

# ============================================================
# A1/A2: 背景 H(t) 解析 + phi 方程 u=phi_dot 的对数时间 RK4
#   u_dot + 3 H u = 3 H^2   (因为 8piG rho = 3H^2)
# ============================================================
def deriv_u(t, u, H_func):
    H = H_func(t)
    return 3*H*H - 3*H*u

def rk4_u(t, u, dt, H_func):
    k1=deriv_u(t,u,H_func)
    k2=deriv_u(t+dt/2,u+dt/2*k1,H_func)
    k3=deriv_u(t+dt/2,u+dt/2*k2,H_func)
    k4=deriv_u(t+dt,u+dt*k3,H_func)
    return u+dt/6*(k1+2*k2+2*k3+k4)

def integrate_u_log(t_i, t_end, u_i, H_func, N=20000):
    lts = np.linspace(np.log(t_i), np.log(t_end), N)
    ts = np.exp(lts)
    u = np.zeros(N); u[0]=u_i
    phi = np.zeros(N)
    for k in range(1,N):
        dt = ts[k]-ts[k-1]
        u[k] = rk4_u(ts[k-1], u[k-1], dt, H_func)
        phi[k] = phi[k-1] + dt*u[k-1]
    return ts, u, phi

t_i=1.0
print("\n"+"="*70)
print("A1  MATTER-DOMINATED BRANCH (n=3, rho~a^-3)")
H_m = lambda t: 2.0/(3.0*t)
ts_m, u_m, phi_m = integrate_u_log(t_i, t0, 4.0/(3.0*t_i), H_m)
print(f"  background a=(t/t0)^(2/3), H=2/(3t)")
print(f"  t=t0: H={H_m(t0):.4e} s^-1 (H0={H0:.3e})")
print(f"  phi_dot u_num(t0)  = {u_m[-1]:.4e}")
print(f"  analytic 4/(3 t0)  = {4/(3*t0):.4e}  ratio={u_m[-1]/(4/(3*t0)):.4f}")
print(f"  phi(t0)            = {phi_m[-1]:.4f}")
print(f"  phi_dot(t0)/H(t0)  = {u_m[-1]/H_m(t0):.3f}   [E10 H0=phi_dot0 needs 1.000; matter gives {u_m[-1]/H_m(t0):.3f}]")

print("\n"+"="*70)
print("A2  RADIATION-DOMINATED BRANCH (n=4, rho~a^-4)")
H_r = lambda t: 1.0/(2.0*t)
ts_r, u_r, phi_r = integrate_u_log(t_i, t0, 3.0/(2.0*t_i), H_r)
print(f"  background a=(t/t0)^(1/2), H=1/(2t)")
print(f"  phi_dot u_num(t0)  = {u_r[-1]:.4e}")
print(f"  analytic 3/(2 t0)  = {3/(2*t0):.4e}  ratio={u_r[-1]/(3/(2*t0)):.3f}")
print(f"  phi_dot(t0)/H(t0)  = {u_r[-1]/H_r(t0):.3f}")

# ============================================================
# A3: 辐射->物质 联合积分（对数时间 RK4）
# ============================================================
print("\n"+"="*70)
print("A3  RADIATION->MATTER TRANSITION (joined ODE)")
a_eq = 1.0/3400.0
rho_m0 = rho_crit/(1+a_eq)
rho_r0 = rho_m0*a_eq
print(f"  rho_m0={rho_m0:.3e}, rho_r0={rho_r0:.3e}, a_eq={a_eq:.2e}")

def deriv_join(t, y, a_i):
    a,phi,u=y
    a = max(a, a_i*1e-6)
    rho = rho_m0*a**-3 + rho_r0*a**-4
    H = np.sqrt(8*np.pi*G*rho/3.0)
    return np.array([H*a, u, 8*np.pi*G*rho - 3*H*u])

def rk4j(t,y,dt,a_i):
    k1=deriv_join(t,y,a_i); k2=deriv_join(t+dt/2,y+dt/2*k1,a_i)
    k3=deriv_join(t+dt/2,y+dt/2*k2,a_i); k4=deriv_join(t+dt,y+dt*k3,a_i)
    return y+dt/6*(k1+2*k2+2*k3+k4)

lts = np.linspace(np.log(t_i), np.log(t0), 40000)
ts2 = np.exp(lts)

def shoot_log(a_i, u_i):
    y=np.array([a_i,0.0,u_i])
    for k in range(1,len(ts2)):
        dt=ts2[k]-ts2[k-1]
        y=rk4j(ts2[k-1],y,dt,a_i)
    return y

# t=1s 时自洽 H，辐射渐近 u_i = 3 H(t_i)
def H_of_a(a):
    rho = rho_m0*a**-3 + rho_r0*a**-4
    return np.sqrt(8*np.pi*G*rho/3.0)

# 扫描 a_i: 物理上 t=1s 时 a ~ a_eq*(t_i/t_eq)^(1/2)
# t_eq 先估: 物质主导 t=2/(3H_eq), H_eq^2=(8piG/3)*2 rho_m0 a_eq^-3
H_eq0 = np.sqrt(8*np.pi*G*rho_m0*a_eq**-3/3.0*2)
t_eq_est = 2/(3*H_eq0)
a_i_phys = a_eq*np.sqrt(t_i/t_eq_est)
print(f"  est t_eq={t_eq_est:.3e}s={t_eq_est/3.15e7:.0f}yr, est a_i(t=1s)={a_i_phys:.3e}")

for a_i_try in [a_i_phys*0.5, a_i_phys, a_i_phys*2]:
    u_i_try = 3*H_of_a(a_i_try)
    yf = shoot_log(a_i_try, u_i_try)
    rho_now = rho_m0*yf[0]**-3 + rho_r0*yf[0]**-4
    H_now = np.sqrt(8*np.pi*G*rho_now/3)
    print(f"  a_i={a_i_try:.3e} u_i={u_i_try:.3e}: a(t0)={yf[0]:.4f}, H_now={H_now:.4e}, phi_dot(t0)={yf[2]:.4e}")

# 二分 a_i 使 a(t0)=1
lo, hi = a_i_phys*0.1, a_i_phys*10
for _ in range(40):
    mid=(lo+hi)/2
    u_i_mid = 3*H_of_a(mid)
    yf=shoot_log(mid, u_i_mid)
    if yf[0]<1.0: lo=mid
    else: hi=mid
a_i_cal=(lo+hi)/2
u_i_cal = 3*H_of_a(a_i_cal)
yf=shoot_log(a_i_cal,u_i_cal)
rho_now = rho_m0*yf[0]**-3 + rho_r0*yf[0]**-4
H_now = np.sqrt(8*np.pi*G*rho_now/3)
print(f"  calibrated a_i={a_i_cal:.3e} u_i={u_i_cal:.3e} -> a(t0)={yf[0]:.4f}")
print(f"  H(t0)={H_now:.4e} (H0={H0:.3e}), phi_dot(t0)={yf[2]:.4e}")
print(f"  phi_dot(t0)/H(t0) = {yf[2]/H_now:.3f}")
H_eq = np.sqrt(8*np.pi*G*rho_m0*a_eq**-3/3.0*2)
t_eq = 2/(3*H_eq)
print(f"  t_eq~{t_eq:.3e} s = {t_eq/3.15e7:.2f} yr")

# ============================================================
# A4: 稳态分支在摩擦项下的命运
# ============================================================
print("\n"+"="*70)
print("A4  STATIC BRANCH (E8a) UNDER FRICTION")
print("  TUFT strong form E10: H = phi_dot identically.")
print("  Eq: phi_ddot + 3H phi_dot = 8piG rho = 3 H^2")
print("  Substitute phi_dot=H, phi_ddot=Hdot:")
print("      Hdot + 3 H^2 = 3 H^2  =>  Hdot = 0")
print("  => H = const, a = exp(H t)  [de Sitter]")
print("  => small-z Hubble linear, NOT quadratic z~d^2.")
print("  JUDGMENT: E8a quadratic-Hubble branch is REVIVED as de Sitter,")
print("  but at cost of eliminating Big-Bang singularity & matter era.")

# ============================================================
# A5: 晚期加速 / 暗能量
# ============================================================
print("\n"+"="*70)
print("A5  LATE-TIME ACCELERATION / DARK ENERGY")
ratio_matter = u_m[-1]/H_m(t0)
print(f"  Matter-only integration: phi_dot(t0)/H(t0) = {ratio_matter:.3f}")
print(f"  Combined rad+mat:        phi_dot(t0)/H(t0) = {yf[2]/H_now:.3f}")
print("  E10 requires phi_dot=H. Matter era gives ratio~2 (not 1).")
print("  If E10 enforced strictly -> pure de Sitter (no BBN, no structure).")
print("  If E10 is today-only boundary condition -> lambda term still needed")
print("    for a(t)~t^(2/3) over 13.8 Gyr + late acceleration.")
print("  CONCLUSION: TUFT v2 does NOT by itself produce standard LCDM.")
print("  Natural acceleration only under strong E10, which overshoots.")

# ============================================================
# B. NGC3198 ROTATION CURVE
# ============================================================
print("\n"+"="*70)
print("B  NGC3198 ROTATION CURVE  (M_b=3e10 Msun)")
M_b = 3e10*M_SUN
print(f"  M_b = {M_b:.3e} kg")

def solve_g(gN, a0):
    lo, hi = 1e-15, max(gN*10, a0*100)
    for _ in range(200):
        mid=(lo+hi)/2
        if mid*(1-np.exp(-mid/a0)) < gN:
            lo=mid
        else:
            hi=mid
    return (lo+hi)/2

rs = np.array([1,2,3,5,8,10,15,20,30,40,50,70])*R_KPC
print(f"\n  {'r[kpc]':>8} {'gN[m/s2]':>12} {'v_N[km/s]':>10} {'v_TUFT[km/s]':>12} {'v_MOND[km/s]':>12}")
for r in rs:
    gN = G*M_b/r**2
    gT = solve_g(gN, a0_TUFT)
    gM = solve_g(gN, a0_MOND)
    vN = np.sqrt(gN*r)/1000
    vT = np.sqrt(gT*r)/1000
    vM = np.sqrt(gM*r)/1000
    print(f"  {r/R_KPC:8.1f} {gN:12.3e} {vN:10.1f} {vT:12.1f} {vM:12.1f}")
v_flat_tuft = (G*M_b*a0_TUFT)**0.25/1000
v_flat_mond = (G*M_b*a0_MOND)**0.25/1000
print(f"\n  v_flat (TUFT) = {v_flat_tuft:.1f} km/s")
print(f"  v_flat (MOND) = {v_flat_mond:.1f} km/s")
print(f"  observed v_flat ~ 150 km/s")
print(f"  deviation TUFT: {(v_flat_tuft-150)/150*100:+.1f}%")
print(f"  deviation MOND: {(v_flat_mond-150)/150*100:+.1f}%")

# ============================================================
# C. BTFR FIT
# ============================================================
print("\n"+"="*70)
print("C  BARYONIC TULLY-FISHER RELATION")
samples = [
    ("M31",       10.0, 250),
    ("M33",        0.5, 120),
    ("NGC2403",    0.4, 130),
    ("NGC3198",    3.0, 150),
    ("Milky Way",  6.0, 220),
]
print(f"  {'galaxy':<12}{'Mobs[1e10Ms]':>14}{'v[km/s]':>9}{'M_TUFT[1e10Ms]':>16}{'logMobs':>9}{'logMpred':>9}")
for name, Mb10, vkms in samples:
    v = vkms*1000.0
    M_pred = v**4/(G*a0_TUFT)/M_SUN/1e10
    print(f"  {name:<12}{Mb10:14.2f}{vkms:9d}{M_pred:16.2f}{np.log10(Mb10):9.3f}{np.log10(M_pred):9.3f}")

logv = np.log10([s[2] for s in samples])
logM = np.log10([s[1] for s in samples])
slope, intercept = np.polyfit(logv, logM, 1)
pred = slope*logv+intercept
ss_res=np.sum((logM-pred)**2); ss_tot=np.sum((logM-logM.mean())**2)
r2=1-ss_res/ss_tot
print(f"\n  Observed fit: log10(M_b/1e10Msun) = {slope:.3f} log10(v) + {intercept:.3f}")
print(f"  Theoretical TUFT slope = 4.000")
print(f"  R^2 = {r2:.3f}")
offset = np.mean(logM - 4*logv)
print(f"  Mean offset from v^4 line (at slope=4): {offset:.3f} dex")
# 理论截距: M=v^4/(G a0_TUFT), log10(M/1e10Msun) = 4 log10 v - log10(G a0_TUFT M_sun 1e10)
theo_int = -np.log10(G*a0_TUFT*M_SUN*1e10)
print(f"  Theoretical intercept (slope=4): {theo_int:.3f}")
print(f"  Observed intercept (slope=4):  {offset:.3f}")
print(f"  Offset discrepancy: {offset-theo_int:.3f} dex")

print("\n"+"="*70)
print("DONE")
