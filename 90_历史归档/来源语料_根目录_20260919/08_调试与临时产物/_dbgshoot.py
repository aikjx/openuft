# -*- coding: utf-8 -*-
"""Debug single shooting integration."""
import numpy as np
from scipy.special import lambertw
from scipy.integrate import solve_ivp

M=1.0; l=2
def r_from_rstar(rstar):
    rstar=np.asarray(rstar,dtype=complex)
    return 2*M*(1+lambertw(rstar/(2*M)-1.0))
def V_rw(r,l=2):
    r=np.asarray(r,dtype=complex); f=1-2*M/r
    return f*(l*(l+1)/r**2-6*M/r**3)

w=0.38-0.09j; w2=w*w
rmax=90.0; rmin=-15.0
psi0=np.exp(1j*w*rmax); dps0=1j*w*psi0
y=np.array([psi0.real,psi0.imag,dps0.real,dps0.imag])
def ode(rs,yy):
    V=complex(V_rw(complex(r_from_rstar(rs)),l))
    psi=complex(yy[0],yy[1]); dps=complex(yy[2],yy[3])
    d2psi=(V-w2)*psi
    return [dps.real,dps.imag,d2psi.real,d2psi.imag]
sol=solve_ivp(ode,(rmax,rmin),y,method="DOP853",rtol=1e-10,atol=1e-12)
print("success",sol.success,"message",sol.message)
print("y shape",np.asarray(sol.y).shape,"nfev",sol.nfev)
yy=np.asarray(sol.y)[:,-1]
psi=complex(yy[0],yy[1]); dps=complex(yy[2],yy[3])
print("psi end",psi,"dps end",dps)
B=0.5*(psi+dps/(1j*w))*np.exp(-1j*w*rmin)
print("B =",B)
