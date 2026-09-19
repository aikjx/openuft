# -*- coding: utf-8 -*-
"""Two-sided shooting QNM: match log-derivative at barrier peak."""
import numpy as np
from scipy.special import lambertw
from scipy.integrate import solve_ivp
from scipy.optimize import root

M=1.0; l=2
def r_from_rstar(rstar):
    rstar=np.asarray(rstar,dtype=complex)
    return 2*M*(1+lambertw(rstar/(2*M)-1.0))
def V_rw(r,l=2):
    r=np.asarray(r,dtype=complex); f=1-2*M/r
    return f*(l*(l+1)/r**2-6*M/r**3)

def integrate(w, rstart, rend, y0):
    w2=w*w
    def ode(rs,yy):
        V=complex(V_rw(complex(r_from_rstar(rs)),l))
        psi=complex(yy[0],yy[1]); dps=complex(yy[2],yy[3])
        d2=(V-w2)*psi
        return [dps.real,dps.imag,d2.real,d2.imag]
    sol=solve_ivp(ode,(rstart,rend),y0,method="DOP853",rtol=1e-10,atol=1e-12,
                  dense_output=False)
    yy=np.asarray(sol.y)
    return yy[:,-1] if yy.ndim==2 else yy

def match_residual(w, r_peak=0.0, r_inf=90.0, r_hor=-15.0):
    w=complex(w)
    # infinity side: outgoing e^{+i w r*}
    psi0=np.exp(1j*w*r_inf); dps0=1j*w*psi0
    y_inf=integrate(w, r_inf, r_peak, np.array([psi0.real,psi0.imag,dps0.real,dps0.imag]))
    psi_inf=complex(y_inf[0],y_inf[1]); dps_inf=complex(y_inf[2],y_inf[3])
    Linf=dps_inf/psi_inf
    # horizon side: ingoing e^{-i w r*}
    psih=np.exp(-1j*w*r_hor); dpsh=-1j*w*psih
    y_h=integrate(w, r_hor, r_peak, np.array([psih.real,psih.imag,dpsh.real,dpsh.imag]))
    psi_h=complex(y_h[0],y_h[1]); dps_h=complex(y_h[2],y_h[3])
    Lh=dps_h/psi_h
    res=Linf-Lh
    return res

def find_qnm(w0):
    def F(x):
        r=match_residual(complex(x[0],x[1]))
        return [r.real,r.imag]
    s=root(F,[w0.real,w0.imag],method="hybr",tol=1e-11,
           options={"xtol":1e-11,"maxfev":2000})
    return complex(s.x[0],s.x[1]), s

if __name__=="__main__":
    for guess in [0.38-0.09j, 0.37-0.08j, 0.4-0.12j]:
        w,s=find_qnm(guess)
        print(f"guess {guess} -> w={w.real:.6f}{w.imag:+.6f}i success={s.success}")
