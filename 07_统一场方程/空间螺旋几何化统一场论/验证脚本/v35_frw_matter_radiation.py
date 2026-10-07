# -*- coding: utf-8 -*-
"""
35 · EF 暗能量机制 含物质/辐射背景 现象学对照
承接 34 稿（v34_frw_einstein_frame.py）：EF 纯挠率场 w_eff∈(-1,-1/3)。
本轮加入无压物质 + 辐射背景，检验含真实宇宙成分时 g≠0 的 τ 场是否仍驱动晚期加速，
输出 w_tot(a) 演化与末期状态。PARENT 输出到体系根。
铁律：机制可行 ≠ 已证暗能量；EF 时间 ≠ 物理时间，共形对应另需确认。
"""
import io, json, os
import numpy as np
from scipy.integrate import solve_ivp
import sympy as sp

PARENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------- EF 符号量（同 34 稿） ----------
def EF_syms(g, m, eta, kap):
    tau = sp.symbols('tau')
    F = (1 + kap*g*tau)/(2*kap)
    K = (3*g**2*kap + 2*g*kap*tau + 2)/(4*(1 + g*kap*tau)**2)
    U = tau*(2*eta + m**2*tau)/(2*(1 + g*kap*tau)**2)
    Kp = sp.diff(K, tau); Up = sp.diff(U, tau)
    ff = lambda e: sp.lambdify(tau, e, 'numpy')
    return ff(F), ff(K), ff(U), ff(Kp), ff(Up)

def EF_g0_syms(m, eta, kap):
    tau = sp.symbols('tau')
    F = sp.Rational(1,2)/kap
    K = sp.Rational(1,2)
    U = tau*(2*eta + m**2*tau)/2
    Kp = sp.S.Zero; Up = sp.diff(U, tau)
    ff = lambda e: sp.lambdify(tau, e, 'numpy')
    return ff(F), ff(K), ff(U), ff(Kp), ff(Up)

def build_rhs(g, m, eta, kap, rho_m0, rho_r0):
    Ff, Kf, Uf, Kpf, Upf = (EF_syms(g, m, eta, kap) if g != 0 else EF_g0_syms(m, eta, kap))
    # 物质/辐射能量守恒：rho_m = rho_m0/a^3, rho_r = rho_r0/a^4（rho_m0 固定，非动态比例）
    def rhs(t, y):
        a, H, tau, X = y
        K_ = Kf(tau); U_ = Uf(tau); Kp_ = Kpf(tau); Up_ = Upf(tau)
        rho_m = rho_m0 / a**3
        rho_r = rho_r0 / a**4
        # EOM
        dad = a*H
        dHd = -kap*(K_*X*X + 0.5*rho_m + (2.0/3.0)*rho_r)
        dtaud = X
        dXd = -(3.0*H*X + (0.5*Kp_*X*X + Up_)/K_)
        return [dad, dHd, dtaud, dXd]
    return rhs, Ff

def solve_one(g, m, eta, kap, f_m, tau0, with_rad=False, tmax=600.0, a_stop=1e4):
    X0 = 0.0
    Ff, Kf, Uf, Kpf, Upf = (EF_syms(g, m, eta, kap) if g != 0 else EF_g0_syms(m, eta, kap))
    K0 = Kf(tau0); U0 = Uf(tau0)
    r0 = 0.0001 if with_rad else 0.0
    rho0_field = K0*X0*X0 + U0
    rho_m0 = (f_m/(1.0-f_m-r0)) * rho0_field if f_m>0 else 0.0
    rho_r0 = (r0/(1.0-f_m-r0)) * rho0_field if r0>0 else 0.0
    H0 = np.sqrt(kap*(rho0_field + rho_m0 + rho_r0)/3.0)
    if rho0_field + rho_m0 + rho_r0 <= 0:
        return None
    rhs, _ = build_rhs(g, m, eta, kap, rho_m0, rho_r0)
    events = [lambda t,y: y[0]-a_stop]
    events[0].terminal = True
    sol = solve_ivp(rhs, (0.0, tmax), [1.0, H0, tau0, X0], rtol=1e-11, atol=1e-13,
                    max_step=1.0, method='DOP853', events=events)
    t = sol.t; a = sol.y[0]; H = sol.y[1]; tau = sol.y[2]; X = sol.y[3]
    # 约束残差 + w_tot 序列（rho_m0/rho_r0 固定）
    w_seq = []; cons_seq = []
    for i in range(len(t)):
        K_ = Kf(tau[i]); U_ = Uf(tau[i])
        rho_m = rho_m0 / a[i]**3
        rho_r = rho_r0 / a[i]**4
        rho_t = K_*X[i]**2 + U_ + rho_m + rho_r
        p_t = K_*X[i]**2 - U_ + rho_r/3.0
        w_seq.append(p_t/rho_t)
        cons_seq.append(3*H[i]**2 - kap*rho_t)
    w = np.array(w_seq); cons = np.array(cons_seq)
    late = w[-1] if len(w) else np.nan
    accelerate = bool(late < -1.0/3.0 + 1e-6)
    return dict(g=g, m=m, eta=eta, f_m=f_m, with_rad=with_rad, tau0=tau0,
                w_late=float(late), accelerate=accelerate,
                tau_late=float(tau[-1]), a_end=float(a[-1]),
                t_end=float(t[-1]), cons_max=float(np.max(np.abs(cons))),
                cons_last=float(np.abs(cons[-1])),
                w_seq=[float(x) for x in w[::max(1,len(w)//40)]],
                a_seq=[float(x) for x in a[::max(1,len(a)//40)]])

def main():
    kap = 8*np.pi
    cases = [
        dict(g=0.3, m=0.005, eta=0.0, tau0=1.0, f_m=0.3),
        dict(g=0.3, m=0.005, eta=0.0, tau0=1.0, f_m=0.0),
        dict(g=0.3, m=0.005, eta=0.0, tau0=1.0, f_m=0.6),
        dict(g=0.2, m=0.01,  eta=0.0, tau0=0.6, f_m=0.3),
        dict(g=0.1, m=0.01,  eta=0.0, tau0=0.8, f_m=0.3),
        dict(g=0.1, m=0.02,  eta=0.0, tau0=0.3, f_m=0.3),
        dict(g=0.0, m=0.01,  eta=0.0, tau0=0.5, f_m=0.3),
        dict(g=0.3, m=0.005, eta=0.0, tau0=1.0, f_m=0.3, with_rad=True),
    ]
    out = {}
    print("== EF 含物质/辐射：w_tot 末期、是否加速 ==")
    for c in cases:
        g=c['g']; m=c['m']; eta=c['eta']; f_m=c['f_m']; tau0=c['tau0']
        wr = c.get('with_rad', False)
        try:
            r = solve_one(g, m, eta, kap, f_m, tau0, with_rad=wr)
        except Exception as e:
            print(f"g={g} m={m} eta={eta} f_m={f_m} rad={wr} tau0={tau0} | ERR {e}")
            continue
        tag = ("rad" if wr else "matter")
        print(f"g={g:<4} m={m:<5} eta={eta} f_m={f_m:<4} tau0={tau0} | "
              f"w_late={r['w_late']:.4f} acc={r['accelerate']} tau_late={r['tau_late']:.4f} "
              f"a_end={r['a_end']:.3g} cons_max={r['cons_max']:.2g} | {tag}")
        key = f"g{g}_m{m}_f{f_m}_rad{int(wr)}"
        out[key] = r
    with io.open(os.path.join(PARENT, "V3_12_frw_matter_radiation.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nsaved V3_12_frw_matter_radiation.json")

if __name__ == "__main__":
    main()
