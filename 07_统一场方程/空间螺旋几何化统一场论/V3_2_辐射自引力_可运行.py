# -*- coding: utf-8 -*-
# TUFT V3.2 统一场攻坚（完整闭环）——可运行化整理版
# 整理说明（相对用户原始攻坚稿仅做以下三类修改，物理框架不变）：
#   1) 常量字面量 "4*mp.pi*10**-7" 改为可解析的 mp 运算式（原串 mp.mpf 无法解析）；
#   2) LaTeX 标识符 \mathcal C 改写为 Cshape（Python 标识符不允许反斜杠）；
#   3) ODE 势项符号按【题述方程与能量泛函】取 psi'' = -(2/r)psi' - V1 psi^3 + V2 psi^5，
#      与原始攻坚稿代码内 "+V1 psi^3 - V2 psi^5" 相差一个整体符号（详见同目录整理文档 §9 边界2）。
#      注意：当前仍为一维共线源，LW 辐射项 n_cross_ab = n*a - a*n 恒为 0（§9 边界3）。
# 归入 openuft/07_统一场方程/空间螺旋几何化统一场论/。
import mpmath as mp
mp.mp.dps = 50  # 整理稿复算采用 50 位；原始稿 250 位（多精度 ODE 极慢）

V1 = mp.mpf("1.2")
V2 = mp.mpf("0.4")
q0 = mp.mpf("1.0")
c = mp.mpf("299792458")
eps0 = mp.mpf("8.8541878128e-12")
mu0 = mp.mpf(4) * mp.pi * mp.mpf(10)**-7
r_max = mp.mpf(40)

# 稳态孤子径向 ODE: -psi'' - (2/r) psi' = V1 psi^3 - V2 psi^5
# => psi'' = -(2/r) psi' - V1 psi^3 + V2 psi^5
def ode(r, state):
    psi, dpsi = state
    if r < mp.mpf("1e-30"):
        return [mp.mpf(0), mp.mpf(0)]
    d2psi = -(2/r)*dpsi - V1 * psi**3 + V2 * psi**5
    return [dpsi, d2psi]

def shoot(psi0):
    sol = mp.odefun(ode, 0, [psi0, mp.mpf(0)], r_max)
    return sol(r_max)[0]

psi0_root = mp.findroot(shoot, mp.mpf("0.75"))
print(f"孤子中心振幅 psi0 = {psi0_root}")
sol_sol = mp.odefun(ode, 0, [psi0_root, mp.mpf(0)], r_max)

def N_integrand(r):
    psi, _ = sol_sol(r)
    return 4 * mp.pi * r**2 * mp.Abs(psi)**2
N = mp.quad(N_integrand, [0, r_max])
print(f"守恒模 N = {N}")

def E0_integrand(r):
    psi, dpsi = sol_sol(r)
    return 4 * mp.pi * r**2 * (mp.mpf("0.5")*dpsi**2 + V1/4*psi**4 - V2/6*psi**6)
E0 = mp.quad(E0_integrand, [0, r_max])
M = E0 / c**2
print(f"孤子静能 E0 = {E0}")
print(f"孤子静质量 M = {M}")

def Cshape_integrand(r):
    psi, _ = sol_sol(r)
    psi2 = mp.Abs(psi)**2
    return 4 * mp.pi * r**2 * (psi2 * (3*V1*psi2 - 5*V2*psi2**2) * r**2)
Cshape = mp.quad(Cshape_integrand, [0, r_max]) / N
print(f"辐射修正系数 C = {Cshape}")

omega0 = mp.mpf("0.2")
Q0 = q0 * omega0 * N
print(f"孤子总电荷 Q0 = {Q0}")

# 匀加速孤子源（双曲世界线）
a_acc = mp.mpf("1e12")
def X_sol(t):
    tau = c/a_acc * mp.asinh(a_acc*t/c)
    return c**2/a_acc * (mp.cosh(a_acc*tau/c) - 1)
def u_sol(t):
    return mp.diff(X_sol, t)
def gamma_sol(t):
    return 1/mp.sqrt(1 - u_sol(t)**2/c**2)

def retarded_time(x, t):
    def eq(tr):
        return mp.Abs(x - X_sol(tr)) - c*(t - tr)
    return mp.findroot(eq, t - mp.Abs(x)/c)

def LW_fields(x, t):
    tr = retarded_time(x, t)
    Xr, ur, gr = X_sol(tr), u_sol(tr), gamma_sol(tr)
    R_vec = x - Xr
    R = mp.Abs(R_vec)
    n = R_vec / R
    beta = ur / c
    beta_n = beta * n
    denom = 4*mp.pi*eps0 * R * (1 - beta_n)
    phi = Q0 / denom
    A = Q0 * ur / (c * denom)
    a_r = mp.diff(u_sol, tr)
    n_cross_ab = n * a_r - a_r * n          # 1D 共线下恒为 0
    E_vel = Q0*(1 - beta**2)*(n - beta) / (4*mp.pi*eps0 * R**2 * (1 - beta_n)**3)
    E_rad = Q0/(4*mp.pi*eps0 * c**2 * R * (1 - beta_n)**3) * (n_cross_ab)
    B_rad = n * E_rad / c
    return E_vel, E_rad, B_rad, R

def integrate_radiation_power(R_far, t):
    theta_vals = [mp.pi*i/100 for i in range(1, 100)]
    d_theta = mp.pi/100
    P_tot = mp.mpf(0)
    for th in theta_vals:
        x_sphere = R_far * mp.cos(th)
        _, E_rad, B_rad, _ = LW_fields(x_sphere, t)
        S = (1/mp.mu0) * (E_rad * B_rad)
        dA = 2*mp.pi * R_far**2 * mp.sin(th) * d_theta
        P_tot += S * dA
    return P_tot

R_far = mp.mpf("1e6")
t_obs = mp.mpf("1e-6")
P_num = integrate_radiation_power(R_far, t_obs)

gr_obs = gamma_sol(t_obs)
P0 = Q0**2 * gr_obs**6 * a_acc**2 / (6*mp.pi*eps0*c**3)
P_analytic = P0 * (1 + Cshape)
print("\n===== 辐射功率对比 =====")
print(f"零阶Larmor功率 P0          = {P0}")
print(f"TUFT解析总功率 P_analytic = {P_analytic}")
print(f"LW数值积分功率 P_num      = {P_num}")
if P_analytic != 0:
    print(f"相对偏差 = {mp.Abs(P_num - P_analytic)/P_analytic}")
