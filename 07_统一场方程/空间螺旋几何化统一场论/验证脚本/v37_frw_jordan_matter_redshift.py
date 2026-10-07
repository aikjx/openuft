# -*- coding: utf-8 -*-
"""
37 · 含物质 EF → Jordan 物理时间映射 + 红移观测预言
承接 35 稿（含物质 EF 加速档 g=0.3/m=0.005/f_m=0.3）+ 36 稿（Jordan 物理时间映射）。
本稿：① 含物质 EF 解映射回 Jordan 物理时间，确认含物质时物理加速成立（闭合 35 §4.2/36 §4.1 场景a）；
      ② 构造红移预言 a_J(z)、H_J(z)、w(z)，与 ΛCDM 晚期 w→−1 对照（理论预言形式，非观测拟合）。
EF 中物质最小耦合（35 稿假设）；Jordan 物理量用共形 Ω=(1+gκτ)^{-1/2}。
PARENT 输出到体系根。铁律：数学自洽≠实验证实；EF/物理时间、物质耦合场景另述。
"""
import io, json, os
import numpy as np
from scipy.integrate import solve_ivp
import sympy as sp

PARENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
kap = 8*np.pi

def EF_syms(g, m, eta):
    tau = sp.symbols('tau')
    F = (1 + kap*g*tau)/(2*kap)
    K = (3*g**2*kap + 2*g*kap*tau + 2)/(4*(1 + g*kap*tau)**2)
    U = tau*(2*eta + m**2*tau)/(2*(1 + g*kap*tau)**2)
    Kp = sp.diff(K, tau); Up = sp.diff(U, tau)
    ff = lambda e: sp.lambdify(tau, e, 'numpy')
    return ff(F), ff(K), ff(U), ff(Kp), ff(Up)

def solve_ef_matter(g, m, eta, tau0, f_m, X0=0.0, tmax=120.0):
    """含物质 EF 演化（35 稿）：ρ_m=ρ_m0/a³，ρ_m0 由 f_m 占比固定"""
    Ff, Kf, Uf, Kpf, Upf = EF_syms(g, m, eta)
    K0 = Kf(tau0); U0 = Uf(tau0)
    rho0_field = K0*X0*X0 + U0
    rho_m0 = (f_m/(1.0-f_m))*rho0_field if f_m > 0 else 0.0
    H0 = np.sqrt(kap*(rho0_field + rho_m0)/3.0)
    def rhs(t, y):
        a, H, tau, X = y
        K_ = Kf(tau); U_ = Uf(tau); Kp_ = Kpf(tau); Up_ = Upf(tau)
        rho_m = rho_m0/a**3
        return [a*H, -kap*(K_*X*X + 0.5*rho_m), X,
                -(3.0*H*X + (0.5*Kp_*X*X + Up_)/K_)]
    sol = solve_ivp(rhs, (0.0, tmax), [1.0, H0, tau0, X0], rtol=1e-12, atol=1e-14,
                    max_step=0.05, method='DOP853')
    return sol, rho_m0

def map_and_predict(g, m, eta, tau0, f_m, tmax=120.0):
    sol, rho_m0 = solve_ef_matter(g, m, eta, tau0, f_m, tmax=tmax)
    t = sol.t; a = sol.y[0]; H = sol.y[1]; tau = sol.y[2]; X = sol.y[3]
    Ff, Kf, Uf, Kpf, Upf = EF_syms(g, m, eta)
    # 共形 Jordan 映射
    Omega = (1.0+g*kap*tau)**(-0.5)
    f = -g*kap/(2.0*(1.0+g*kap*tau))      # d lnΩ/dτ
    a_J = Omega*a
    H_J = (H + f*X)/Omega
    dt = np.diff(t); t_J = np.concatenate([[0.0], np.cumsum(Omega[1:]*dt)])
    # 解析 Ḣ_J（避免 np.gradient 噪声）：H_J=(H+fX)/Ω
    # Ḣ_EF = -κ(KX²+½ρ_m), Ẋ=-(3HX+(½K'X²+U')/K), Ω̇=fXΩ
    K_ = np.array([Kf(ti) for ti in tau]); Kp_ = np.array([Kpf(ti) for ti in tau])
    U_ = np.array([Uf(ti) for ti in tau]); Up_ = np.array([Upf(ti) for ti in tau])
    rho_m = rho_m0/a**3
    Hd = -kap*(K_*X**2 + 0.5*rho_m)
    Xd = -(3.0*H*X + (0.5*Kp_*X**2 + Up_)/K_)
    df = g*g*kap*kap/(2.0*(1.0+g*kap*tau)**2)
    G = H + f*X
    Gd = Hd + df*X**2 + f*Xd
    Omegad = f*X*Omega
    dHJ_dt = (Gd*Omega - G*Omegad)/Omega**2     # dH_J/dt̃
    HJd = dHJ_dt/Omega                            # dH_J/dt_J
    accel_J = 2.0*HJd + 3.0*H_J**2
    # EF w（τ 场态方程）
    w_EF = (K_*X**2 - U_)/(K_*X**2 + U_)
    # 红移
    z = 1.0/a_J - 1.0
    # 末期状态
    n = len(t); late = slice(max(0,n-20), n)
    acc_J_late = float(np.mean(accel_J[late]))
    w_EF_late = float(np.mean(w_EF[late]))
    return dict(t=t, t_J=t_J, a_J=a_J, H_J=H_J, z=z, w_EF=w_EF, accel_J=accel_J,
                Omega=Omega, tau=tau)

def summarize(g, m, eta, tau0, f_m):
    r = map_and_predict(g, m, eta, tau0, f_m)
    n = len(r['t']); late = slice(max(0,n-20), n)
    accJ = float(np.mean(r['accel_J'][late]))
    wE = float(np.mean(r['w_EF'][late]))
    aJ0 = float(r['a_J'][0]); aJ_end = float(r['a_J'][-1])
    z0 = float(r['z'][0]); z_end = float(r['z'][-1])
    H_J0 = float(r['H_J'][0]); H_Jend = float(r['H_J'][-1])
    # z 采样（约 25 点）
    idx = np.linspace(0, n-1, 25).astype(int)
    hz = [dict(z=float(r['z'][i]), H_J=float(r['H_J'][i]),
               w_EF=float(r['w_EF'][i]), acc2=float(r['accel_J'][i])) for i in idx]
    return dict(g=g, m=m, eta=eta, tau0=tau0, f_m=f_m,
                w_EF_late=wE, accel_Jordan_2H3H2=accJ,
                accel_Jordan=bool(accJ > 0.0),
                a_J0=aJ0, a_Jend=aJ_end, z0=z0, z_end=z_end,
                H_J0=H_J0, H_Jend=H_Jend,
                Omega0=float(r['Omega'][0]), tau_late=float(r['tau'][-1]),
                redshift_sample=hz)

def main():
    cases = [
        dict(g=0.3, m=0.005, eta=0.0, tau0=1.0, f_m=0.3),
        dict(g=0.3, m=0.005, eta=0.0, tau0=1.0, f_m=0.0),
        dict(g=0.2, m=0.01,  eta=0.0, tau0=0.6, f_m=0.3),
    ]
    out = {}
    print("== 含物质 EF→Jordan 物理时间 + 红移预言 ==")
    for c in cases:
        r = summarize(**c)
        print(f"g={c['g']:<4} m={c['m']:<5} tau0={c['tau0']} f_m={c['f_m']} | "
              f"EF w={r['w_EF_late']:+.3f} | Jordan acc(2Ḣ+3H²)={r['accel_Jordan_2H3H2']:+.3g} "
              f"acc={r['accel_Jordan']} | a_J: {r['a_J0']:.3f}->{r['a_Jend']:.3f} | "
              f"z: {r['z0']:.3f}->{r['z_end']:.3f} | H_J: {r['H_J0']:.3g}->{r['H_Jend']:.3g}")
        out[f"g{c['g']}_m{c['m']}_f{c['f_m']}"] = r
    with io.open(os.path.join(PARENT, "V3_14_jordan_matter_redshift.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nsaved V3_14_jordan_matter_redshift.json")

if __name__ == "__main__":
    main()
