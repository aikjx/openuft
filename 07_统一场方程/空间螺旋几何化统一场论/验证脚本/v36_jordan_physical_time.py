# -*- coding: utf-8 -*-
"""
36 · EF→Jordan 物理时间映射：确认 EF 判定加速在物理时间是否成立
承接 34 稿 EF 复核（EF 时间 ≠ 物理时间，加速判定需共形映射确认）。
从 EF 解 {ã,H̃,τ,X̃} 用共形因子 Ω=(1+gκτ)^{-1/2} 反推 Jordan 物理时间
t_J=∫Ω dt̃、尺度因子 a_J=Ω ã、Hubble H_J、态方程 w_J，判物理加速。
PARENT 输出到体系根。铁律：数学自洽≠实验证实；本册闭合物理时间映射，含物质共形耦合另述。
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

def solve_ef(g, m, eta, tau0, X0, tmax=60.0):
    Ff, Kf, Uf, Kpf, Upf = EF_syms(g, m, eta)
    U0 = Uf(tau0); K0 = Kf(tau0)
    H0 = np.sqrt(kap*(K0*X0*X0 + U0)/3.0)
    def rhs(t, y):
        a, H, tau, X = y
        K_ = Kf(tau); U_ = Uf(tau); Kp_ = Kpf(tau); Up_ = Upf(tau)
        return [a*H, -kap*K_*X*X, X, -(3.0*H*X + (0.5*Kp_*X*X + Up_)/K_)]
    sol = solve_ivp(rhs, (0.0, tmax), [1.0, H0, tau0, X0], rtol=1e-12, atol=1e-14,
                    max_step=0.05, method='DOP853')
    return sol

def jordan_map(g, m, eta, tau0, X0=0.0, tmax=60.0):
    """EF 解 → Jordan 物理量（物理时间 t_J）"""
    sol = solve_ef(g, m, eta, tau0, X0, tmax)
    t = sol.t; a = sol.y[0]; H = sol.y[1]; tau = sol.y[2]; X = sol.y[3]
    # 共形因子 Ω=(1+gκτ)^{-1/2}（EF→Jordan：a_J=Ω a_EF, dt_J=Ω dt̃）
    Omega = (1.0 + g*kap*tau)**(-0.5)
    dO = -0.5*g*kap*(1.0+g*kap*tau)**(-1.5)*X  # dΩ/dt̃
    # 物理时间累积
    dt = np.diff(t); t_J = np.concatenate([[0.0], np.cumsum(Omega[1:]*dt)])
    a_J = Omega*a
    # Jordan Hubble：H_J = (H_EF + Ω̇/Ω)/Ω
    H_J = (H + dO/Omega)/Omega
    # 数值求 Ḣ_J（对 t_J）与 w_J
    dHdt = np.gradient(H_J, t_J)
    w_J = -1.0 - (2.0/3.0)*(dHdt/H_J**2)
    # 加速判定量：ä>0 ⇔ 2Ḣ+3H²>0（因 2Ḣ+3H²=-κwρ，w<-1/3 ⇔ 该量>0）
    accel_J = 2.0*dHdt + 3.0*H_J**2
    # EF 侧 w（对照）
    Ff, Kf, Uf, Kpf, Upf = EF_syms(g, m, eta)
    w_EF = np.array([(Kf(tau[i])*X[i]**2 - Uf(tau[i]))/(Kf(tau[i])*X[i]**2 + Uf(tau[i])) for i in range(len(t))])
    return dict(t=t, t_J=t_J, a_J=a_J, H_J=H_J, w_J=w_J, accel_J=accel_J,
                w_EF=w_EF, Omega=Omega, tau=tau)

def summarize(g, m, eta, tau0):
    r = jordan_map(g, m, eta, tau0)
    wj = r['w_J']; wE = r['w_EF']
    # 末期（取尾部均值，避免边界数值抖动）
    n = len(wj)
    late = slice(max(0,n-15), n)
    wj_late = float(np.mean(wj[late])); wE_late = float(np.mean(wE[late]))
    # 加速：ä>0 ⇔ 2Ḣ+3H²>0（因 2Ḣ+3H²=-κwρ，w<-1/3 ⇔ 该量>0）
    acc_J = bool(np.mean(r['accel_J'][late]) > 0.0)
    Om_min = float(np.min(r['Omega']))
    # EF 加速判定用 EF w
    acc_E = bool(wE_late < -1.0/3.0 + 1e-4)
    tJ_end = float(r['t_J'][-1]); aJ_end = float(r['a_J'][-1])
    return dict(g=g, m=m, eta=eta, tau0=tau0,
                w_EF_late=wE_late, accel_EF=acc_E,
                w_Jordan_late=wj_late, accel_Jordan=acc_J,
                accel2_J_late=float(np.mean(r['accel_J'][late])),
                Omega_min=Om_min, t_Jordan_end=tJ_end,
                a_Jordan_end=aJ_end, tau_late=float(r['tau'][-1]),
                n_pts=len(r['t']))

def main():
    cases = [
        dict(g=0.3, m=0.005, eta=0.0, tau0=1.0),
        dict(g=0.2, m=0.01,  eta=0.0, tau0=0.6),
        dict(g=0.1, m=0.01,  eta=0.0, tau0=0.8),
        dict(g=0.0, m=0.01,  eta=0.0, tau0=0.5),
    ]
    out = {}
    print("== EF→Jordan 物理时间映射：物理加速是否成立 ==")
    for c in cases:
        r = summarize(c['g'], c['m'], c['eta'], c['tau0'])
        print(f"g={c['g']:<4} m={c['m']:<5} tau0={c['tau0']} | "
              f"EF: w={r['w_EF_late']:+.3f} acc={r['accel_EF']} | "
              f"Jordan: w={r['w_Jordan_late']:+.3f} acc(2Ḣ+3H²)={r['accel_Jordan']} (val={r['accel2_J_late']:+.3g}) | "
              f"Ωmin={r['Omega_min']:.3f} tJ_end={r['t_Jordan_end']:.1f} aJ_end={r['a_Jordan_end']:.3f}")
        out[f"g{c['g']}_m{c['m']}"] = r
    with io.open(os.path.join(PARENT, "V3_13_jordan_physical_time.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nsaved V3_13_jordan_physical_time.json")

if __name__ == "__main__":
    main()
