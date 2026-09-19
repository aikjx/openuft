# -*- coding: utf-8 -*-
import numpy as np
from scipy.special import lambertw
from scipy.integrate import solve_ivp
M=1.0; l=2
def r_from_rstar(rstar):
    rstar=np.asarray(rstar,dtype=complex); return 2*M*(1+lambertw(rstar/(2*M)-1.0))
def V_rw(r,l=2):
    r=np.asarray(r,dtype=complex); f=1-2*M/r; return f*(l*(l+1)/r**2-6*M/r**3)
def integrate(w, rs, re_, y0):
    w2=w*w
    def ode(t,yy):
        V=complex(V_rw(complex(r_from_rstar(t)),l))
        psi=complex(yy[0],yy[1]); dp=complex(yy[2],yy[3]); d2=(V-w2)*psi
        return [dp.real,dp.imag,d2.real,d2.imag]
    sol=solve_ivp(ode,(rs,re_),y0,method="DOP853",rtol=1e-11,atol=1e-13)
    yy=np.asarray(sol.y); return (yy[:,-1] if yy.ndim==2 else yy)
w=0.37367-0.08896j
# infinity side to rp=0
p0=np.exp(1j*w*90); d0=1j*w*p0
yi=integrate(w,90.0,0.0,np.array([p0.real,p0.imag,d0.real,d0.imag]))
psi_i=complex(yi[0],yi[1]); dp_i=complex(yi[2],yi[3])
print("INF side at r*=0: psi=",psi_i," |psi|=",abs(psi_i)," dp=",dp_i," |dp|=",abs(dp_i))
# horizon side to rp=0
ph=np.exp(-1j*w*(-15)); dh=-1j*w*ph
yh=integrate(w,-15.0,0.0,np.array([ph.real,ph.imag,dh.real,dh.imag]))
psi_h=complex(yh[0],yh[1]); dp_h=complex(yh[2],yh[3])
print("HOR side at r*=0: psi=",psi_h," |psi|=",abs(psi_h)," dp=",dp_h," |dp|=",abs(dp_h))
# log derivatives
print("Linf=",dp_i/psi_i, " Lh=",dp_h/psi_h)
