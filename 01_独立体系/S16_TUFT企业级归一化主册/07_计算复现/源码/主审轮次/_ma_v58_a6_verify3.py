# -*- coding: utf-8 -*-
import numpy as np
def dphi(u0,c_m,d,n=6000):
    x,w=np.polynomial.legendre.leggauss(n); th=0.25*np.pi*(x+1.0)
    s=np.sin(th); c=np.cos(th)
    num=np.sqrt(1.0+c_m*u0*u0*s*s+d*u0**3*s**3)
    den=np.sqrt(1.0-s*s*np.exp(2.0*u0*(1.0-s)))
    f=np.exp(u0)*c*num/den; val=0.25*np.pi*np.sum(w*f)
    return 2.0*val-np.pi
def A_fit(cm,dval):
    u0s=np.array([0.5e-4,0.75e-4,1.0e-4,1.25e-4,1.5e-4])
    vals=np.array([dphi(u,cm,dval) for u in u0s])
    co=np.polyfit(u0s,vals-np.pi,3)
    return co[2],co[1],co[0]  # descending: c3 A1, c2 A2, c1 A3
a1,a2,a3=A_fit(0.0,0.0)
print(f"GR: A1={a1:.10f} (4) A2={a2:.10f} (scan 3.068582494365693) A3={a3:.10f}")
cm_scan=np.array([-0.369,-0.331,-0.290,-0.249,-0.218,0.0])
A2s=np.array([A_fit(c,-0.05)[1] for c in cm_scan])
k,A20=np.polyfit(cm_scan,A2s,1)
print(f"A2(c_m,d=-0.05): A2_0={A20:.10f} slope={k:.10f}")
print(f"organizer: A2=3.0688962660+0.7855625673c_m+0.0001000236d -> d=-0.05: A2_0=3.0688912648 slope=0.7855625673")
print(f"diff A2_0: {A20-3.0688912648:+.2e}  diff slope: {k-0.7855625673:+.2e}")
