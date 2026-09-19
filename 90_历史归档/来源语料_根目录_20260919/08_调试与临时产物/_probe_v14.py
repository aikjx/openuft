# -*- coding: utf-8 -*-
"""probe v14: (1) GR Schwarzschild s=-2 Leaver CF gate; (2) TUFT wall ODE stability across s_out."""
import time, numpy as np, mpmath as mp
mp.mp.dps = 40
t0=time.time()
I = mp.mpc(0,1)

# ---------- (1) validated Schwarzschild s=-2 Leaver three-term CF (from v12/v13) ----------
def coef(n, w, l):
    an = n**2 + (4 - 4*I*w)*n + (3 - 4*I*w)
    bn = -l*(l+1) - 2*n**2 + (16*I*w - 2)*n + (32*w**2 + 8*I*w + 3)
    gn = n**2 + (-8*I*w - 2)*n + (-16*w**2 + 8*I*w)
    return an, bn, gn
def quant(w, l, N):
    C = mp.mpc(0)
    for n in range(N, 0, -1):
        a,b,g = coef(n, w, l)
        C = g/(b - a*C)
    a0,b0,_ = coef(0,w,l)
    return b0 - a0*C
GR = {(2,0): mp.mpc('0.37367168441804166','-0.0889623156889341'),
      (2,1): mp.mpc('0.34671099687909240','-0.2739148752911987')}
print("=== (1) GR Schwarzschild s=-2 Leaver CF gate ===")
for (l,n), bm in GR.items():
    seed = mp.mpc(bm.real*0.98, bm.imag*1.05)
    w = mp.findroot(lambda z: quant(z,l,400), seed, maxsteps=80)
    print(" l=%d n=%d  w=%.15f %+.15f i   |w-bm|=%.2e" % (l,n,w.real,w.imag, abs(w-bm)))

# ---------- (2) TUFT wall: build tortoise + ODE, scan s_out ----------
print("\n=== (2) TUFT wall ODE, stability across s_out (c=-0.5,d=0) ===")
cm, dd = mp.mpf('-0.5'), mp.mpf('0')
# wall radius
rh = mp.polyroots([1,0,cm,dd])
rh = [r for r in rh if abs(r.imag)<1e-6 and r.real>0][0].real
print(" r_h = %.8f" % rh)

def metric(r):
    g = 1 + cm/r**2 + dd/r**3
    F = mp.exp(2/r)*mp.sqrt(g)          # ds/dr
    V = mp.exp(-2/r)*mp.mpf(6)/r**2     # l=2
    return F, V

# tortoise s(r) by quadrature from wall to rmax
rmax = mp.mpf(200)
rs = np.linspace(float(rh)*(1+1e-9), 200.0, 200000)
Fs = np.array([float(metric(mp.mpf(r))[0]) for r in rs[::200]])  # coarse check
# build s(r) dense
rd = np.linspace(float(rh)*(1+1e-9), 200.0, 400000)
sd = np.concatenate([[0.0], np.cumsum(0.5*(Fs[1:]+Fs[:-1])*0)])  # placeholder
# do it properly with vectorized numpy
import numpy as np
def F_np(r):
    g = 1 + float(cm)/r**2 + float(dd)/r**3
    return np.exp(2/r)*np.sqrt(np.clip(g,0,None))
rd = np.linspace(float(rh)*(1+1e-9), 200.0, 400000)
Fv = F_np(rd)
sd = np.concatenate([[0.0], np.cumsum(0.5*(Fv[1:]+Fv[:-1])*np.diff(rd))])
Vv = np.exp(-2/rd)*6.0/rd**2
print(" s(rmax=200) = %.4f" % sd[-1])
print(" V peak = %.4f at s=%.4f" % (Vv.max(), sd[np.argmax(Vv)]))

from scipy.integrate import solve_ivp
from scipy.optimize import root as sp_root
def shoot(w, s_out, h=0.01):
    a,b = w.real, w.imag
    s = np.arange(0, s_out+0.5*h, h)
    Vg = np.interp(s, sd, Vv)
    def ode(ss, y):
        V = np.interp(ss, s, Vg)
        return [y[1], (V - (a+1j*b)**2)*y[0]]
    sol = solve_ivp(ode, (0,s_out), [1.0,0.0], t_eval=[s_out], method='DOP853',
                    rtol=1e-11, atol=1e-13)
    psi, psis = complex(sol.y[0,0],0), complex(sol.y[1,0],0)
    return psis/psi - 1j*w
for so in [20,25,30,35,40,50]:
    def F(x):
        w=complex(x[0],x[1]); r=shoot(w,so); return [r.real,r.imag]
    try:
        sol=sp_root(F,[0.45,-0.07],method='hybr',options={'xtol':1e-12,'maxfev':2000})
        w=complex(*sol.x); res=abs(shoot(w,so))
        print(" s_out=%3d  w=%.8f %+.8f i  |F|=%.2e" % (so,w.real,w.imag,res))
    except Exception as e:
        print(" s_out=%3d  fail %s" % (so, str(e)[:40]))
print("elapsed %.1f s" % (time.time()-t0))
