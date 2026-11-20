"""Independent Hill-equation counterexample: positive instantaneous stiffness != Floquet stability."""
from math import pi,sin,cos,acosh
import numpy as np
from scipy.integrate import solve_ivp

def compute(*,k=1.,g=.16,theta0=.35,omega=2.,method='DOP853'):
    if k<=0 or omega<=0:raise ValueError('k and omega must be positive')
    t_end=2*pi/omega
    def coeff(t):return k**2-g*k*theta0*omega*sin(omega*t)
    def rhs(t,y):
        a,b,c,d=y
        w=coeff(t)
        return np.array([c,d,-w*a,-w*b])
    out=solve_ivp(rhs,(0,t_end),[1.,0.,0.,1.],method=method,rtol=3e-12,atol=2e-14)
    if not out.success:raise RuntimeError(out.message)
    m=np.array([[out.y[0,-1],out.y[1,-1]],[out.y[2,-1],out.y[3,-1]]])
    trace=float(np.trace(m))
    return dict(min_coefficient=k**2-abs(g*k*theta0*omega),trace=trace,
                det=float(np.linalg.det(m)),floquet_mu=float(acosh(abs(trace)/2)/t_end) if abs(trace)>2 else 0,
                tperiod=t_end,nfev=int(out.nfev))
