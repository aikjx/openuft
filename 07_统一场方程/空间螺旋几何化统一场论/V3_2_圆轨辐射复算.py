# -*- coding: utf-8 -*-
# TUFT V3.2 —— 横向（圆轨）加速源 LW 远场辐射功率数值复算
# 结论（对照同目录 15B 文档 §6A）：圆轨 LW 积分收敛到标准点电荷圆轨 Larmor P=(Q0²/6πε0c³)γ⁴a²，
# 而非稿内 P0=γ⁶a²；形状修正 (1+C)≈13.8 不进入刚体 LW 读数 => 「P_num→P0(1+C)」互洽主张判否。
# 复算：β=0.7, 64×128 采样, P_num/P(γ⁴a²)=1.00004。
import numpy as np
c = 299792458.0
eps0 = 8.8541878128e-12
Q0 = 201.32736762132487   # 15B §3 主根复算值

beta = 0.7
R_orbit = 1.0e9
omega = beta*c/R_orbit
v = omega*R_orbit
a_c = v**2/R_orbit
gamma = 1/np.sqrt(1-beta**2)

def X(t): return np.array([R_orbit*np.cos(omega*t), R_orbit*np.sin(omega*t), 0.0])
def V(t): return np.array([-omega*R_orbit*np.sin(omega*t), omega*R_orbit*np.cos(omega*t), 0.0])
def A(t): return np.array([-omega**2*R_orbit*np.cos(omega*t), -omega**2*R_orbit*np.sin(omega*t), 0.0])

def retarded_time(x, t):
    tr = t - np.linalg.norm(x - X(t))/c
    for _ in range(60):
        rv = x - X(tr); nrm = np.linalg.norm(rv)
        g = nrm - c*(t-tr); nhat = rv/nrm
        dg = -np.dot(nhat, V(tr)) + c; tr2 = tr - g/dg
        if abs(tr2-tr) < 1e-14*abs(tr)+1e-18: tr=tr2; break
        tr = tr2
    return tr

def Erad_field(x, t):
    tr = retarded_time(x, t); Xr=X(tr); Vr=V(tr); Ar=A(tr)
    rv = x - Xr; R = np.linalg.norm(rv); n = rv/R
    beta_v = Vr/c; beta_n = np.dot(beta_v, n)
    cross1 = np.cross((n-beta_v), Ar); cross2 = np.cross(n, cross1)
    return Q0/(4*np.pi*eps0*c**2)*cross2/(R*(1-beta_n)**3)

R_far = 1e12
def integrate_P(R_far, t_obs, n_th, n_ph):
    P = 0.0
    for i in range(n_th):
        th = (i+0.5)*np.pi/n_th
        for j in range(n_ph):
            ph = j*2*np.pi/n_ph
            x = R_far*np.array([np.sin(th)*np.cos(ph), np.sin(th)*np.sin(ph), np.cos(th)])
            E = Erad_field(x, t_obs)
            dOmega = np.sin(th)*(np.pi/n_th)*(2*np.pi/n_ph)
            P += eps0*c*np.dot(E,E)*R_far**2*dOmega
    return P

Pg4 = Q0**2/(6*np.pi*eps0*c**3)*gamma**4*a_c**2   # 标准圆轨 Larmor
Pg6 = Q0**2/(6*np.pi*eps0*c**3)*gamma**6*a_c**2   # 稿内 P0 形式
for n in [8,16,32,64]:
    P_num = integrate_P(R_far, 0.0, n, 2*n)
    print(f"采样 {n}x{2*n}: P_num={P_num:.6e}  P(γ⁴a²)={Pg4:.6e}  ratio={P_num/Pg4:.6f}  P_num/P(γ⁶a²)={P_num/Pg6:.6f}")
