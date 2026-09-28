# -*- coding: utf-8 -*-
import numpy as np
def dphi(u0,c_m,d,n=8000):
    x,w=np.polynomial.legendre.leggauss(n); th=0.25*np.pi*(x+1.0)
    s=np.sin(th); c=np.cos(th)
    num=np.sqrt(1.0+c_m*u0*u0*s*s+d*u0**3*s**3)
    den=np.sqrt(1.0-s*s*np.exp(2.0*u0*(1.0-s)))
    f=np.exp(u0)*c*num/den; val=0.25*np.pi*np.sum(w*f)
    return 2.0*val-np.pi
# quadratic fit dphi = pi + A1 u + A2 u^2 on small-u0 window
def A2_fit(cm,dval):
    u0s=np.array([0.3e-4,0.5e-4,0.7e-4,0.9e-4,1.1e-4,1.3e-4])
    vals=np.array([dphi(u,cm,dval) for u in u0s])
    co=np.polyfit(u0s,vals-np.pi,2)
    return co[1],co[0]   # A1,A2
a1,a2=A2_fit(0.0,0.0)
print(f"GR small-window: A1={a1:.9f} A2={a2:.9f} (org scan A2=3.0685824944)")
cm_scan=np.array([-0.369,-0.331,-0.290,-0.249,-0.218,0.0])
A2s=np.array([A2_fit(c,-0.05)[1] for c in cm_scan])
k,A20=np.polyfit(cm_scan,A2s,1)
print(f"A2(c_m,d=-0.05) small-window: A2_0={A20:.9f} slope={k:.9f}")
print(f"organizer: A2_0(d=-0.05)=3.0688912648 slope=0.7855625673")
print(f"diff: {A20-3.0688912648:+.1e} slope diff {k-0.7855625673:+.1e}")
