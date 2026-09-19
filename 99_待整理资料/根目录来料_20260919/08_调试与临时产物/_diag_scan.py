# -*- coding: utf-8 -*-
import numpy as np
from scipy.integrate import solve_ivp

def V_RW(r, ell=2):
    f = 1.0 - 2.0/r
    return f*(ell*(ell+1)/r**2 - 6.0/r**3)

def shoot_inward(w, ell=2, r_max=200.0, r_end=2.0001):
    rstar_max = r_max + 2*np.log(r_max/2 - 1)
    u0 = np.exp(1j*w*rstar_max)
    up0 = 1j*w*u0
    def ode(r, y):
        f = 1.0 - 2.0/r
        V = V_RW(r, ell)
        return [y[1]/f, (V - w*w)*y[0]/f]
    sol = solve_ivp(ode, (r_max, r_end), [u0, up0], t_eval=[r_end],
                    method="DOP853", rtol=1e-11, atol=1e-13)
    ulast = sol.y[0,-1]; up_last = sol.y[1,-1]
    return up_last + 1j*w*ulast

# 扫描
print("Scanning |residual| near expected root:")
print("w_R range [0.35,0.40], w_I range [-0.12,-0.05]")
best = (1e9, None)
for wr in np.linspace(0.35, 0.40, 21):
    row = []
    for wi in np.linspace(-0.12, -0.05, 15):
        w = complex(wr, wi)
        try:
            r = shoot_inward(w)
            row.append(f"{abs(r):.1e}")
            if abs(r) < best[0]:
                best = (abs(r), w)
        except Exception:
            row.append("  inf ")
    print(f"wr={wr:.3f}: " + " ".join(row))
print(f"\nBest: w={best[1]}, |res|={best[0]:.3e}")
