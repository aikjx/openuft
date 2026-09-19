# -*- coding: utf-8 -*-
"""Debug: cross-check the real standing-wave IVP with scipy solve_ivp (rtol 1e-12)
and print endpoint components, to locate why arg R sat at -pi/2 everywhere."""
import sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
import numpy as np
from scipy.integrate import solve_ivp
def run(L,WB,VB,w,sout_extra=25.0):
    smax=L+WB+sout_extra
    def V(s): return VB if (L<=s<=L+WB) else 0.0
    def rhs(s,y): return [y[1],(V(s)-w*w)*y[0]]
    sol=solve_ivp(rhs,[0,smax],[1.0,0.0],dense_output=True,rtol=1e-12,atol=1e-13,
                  max_step=0.01,method="DOP853")
    for spt in [0.0,L,L+WB,smax]:
        psi,p=sol.sol(spt)
        print("   s=%7.3f  psi=% .6e  p=% .6e  p/(w psi)=% .5e"%(spt,psi,p,p/(w*psi)))
    psi,p=sol.sol(smax)
    Cp=(psi-p/(1j*w))/2; Cm=(psi+p/(1j*w))/2
    print("   C+=(% .6e %+.6e)  C-=(% .6e %+.6e)  |Cp/Cm|=%.8f arg=%.5f"%(
        Cp.real,Cp.imag,Cm.real,Cm.imag,abs(Cp/Cm),np.angle(Cp/Cm)))
    # also evaluate R at a few far points to see phase rotation with s
    print("   arg R at far points s=smax-3..smax (should rotate with s if free):")
    for spt in [smax-3,smax-2,smax-1,smax]:
        psi,p=sol.sol(spt); Cp=(psi-p/(1j*w))/2; Cm=(psi+p/(1j*w))/2
        print("     s=%7.3f arg(C+/C-)=%.5f"%(spt,np.angle(Cp/Cm)))
for w in [0.6,1.07,1.5]:
    print("TOY w=%.3f (L=2.93,WB=1.5,Vb=3.0):"%w); run(2.93,1.5,3.0,w)
