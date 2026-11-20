"""ROOT V110 reproducible toy models, not observed or new fundamental physics.
Natural units: hbar=c=1; all values scaled to one reference frequency.
Conventions: A_h''+[k²+h*g*k*theta_dot] A_h=0, h=+1/-1.
Periodic prescribed theta=theta0*cos(Omega*t). For self-consistent truncation:
L= f² theta_dot²/2 - Lambda4(1-cos(theta))
  + sum_h [A_dot_h²/2 -k² A_h²/2 - h*g*k*theta_dot*A_h²/2].
"""
from dataclasses import dataclass
import math
import numpy as np
from scipy.integrate import solve_ivp

@dataclass(frozen=True)
class P:
    k:float=1.0
    g:float=0.16
    theta0:float=0.35
    Omega:float=2.0

def q(t, h, p):
    return p.k**2 - h*p.g*p.k*p.theta0*p.Omega*np.sin(p.Omega*t)

def propagator(p:P, h:int, *, cycles=1, rtol=3e-11, atol=2e-13, method='DOP853'):
    assert h in (-1,1) and p.k>0 and p.Omega>0 and cycles>=1
    T=2*math.pi*cycles/p.Omega
    def rhs(t, y):
        return np.array([y[2], y[3], -q(t,h,p)*y[0], -q(t,h,p)*y[1]])
    y0=np.array([1.,0.,0.,1.]) # fundamental columns (u,u') = (1,0),(0,1)
    sol=solve_ivp(rhs, (0.,T), y0, method=method, rtol=rtol, atol=atol)
    if not sol.success: raise RuntimeError(sol.message)
    y=sol.y[:,-1]
    return np.array([[y[0],y[1]],[y[2],y[3]]]),sol.nfev

def floquet(p, h=1, **kwargs):
    M,nfev=propagator(p,h,**kwargs)
    tr=float(np.trace(M)); det=float(np.linalg.det(M)); T=2*math.pi/p.Omega
    mu=float(math.acosh(abs(tr)/2)/T) if abs(tr)>2 else 0.
    return {'trace':tr,'det':det,'mu':mu,'stable_band':abs(tr)<2,'nfev':nfev,'M':M}

def leading_mu(p):
    # Resonance center Omega=2*k, |g*theta0| << 1
    return abs(p.g*p.theta0)*p.k/2

def monodromy_scan(g=.16,theta0=.35,k=1.,omega_low=1.55,omega_high=2.45,n=121):
    out=[]
    for Omega in np.linspace(omega_low,omega_high,n):
        p=P(k,g,theta0,float(Omega))
        a=floquet(p,1);b=floquet(p,-1)
        out.append(dict(Omega=float(Omega),mu_plus=a['mu'],mu_minus=b['mu'],
                        trace_plus=a['trace'],trace_minus=b['trace'],
                        det_plus=a['det'],det_minus=b['det']))
    return out

def coupled_rhs(t,y,*,k=1.,g=.22,f=1.,Lambda4=4.):
    theta,theta_dot,Aplus,Vplus,Aminus,Vminus=y
    # f² theta_ddot + Lambda4 sin(theta) = g*k*(Aplus*Vplus - Aminus*Vminus)
    theta_ddot=(-Lambda4*np.sin(theta)+g*k*(Aplus*Vplus-Aminus*Vminus))/f**2
    return np.array([theta_dot,theta_ddot,Vplus,-(k*k+g*k*theta_dot)*Aplus,
                     Vminus,-(k*k-g*k*theta_dot)*Aminus])

def coupled_energy(y,*,k=1.,f=1.,Lambda4=4.):
    y=np.asarray(y)
    theta,theta_dot,Aplus,Vplus,Aminus,Vminus=np.moveaxis(y,0,0)
    eth=.5*f*f*theta_dot**2+Lambda4*(1-np.cos(theta))
    eem=.5*(Vplus**2+Vminus**2+k*k*(Aplus**2+Aminus**2))
    return eth,eem,eth+eem

def run_coupled(duration=180.,nt=1401,*,k=1.,g=.22,f=1.,Lambda4=4.,theta0=.35, aplus=.01,aminus=.009, method='DOP853',rtol=1e-10,atol=1e-12):
    y0=np.array([theta0,0.,aplus,0.,aminus,0.],float)
    t=np.linspace(0,duration,nt)
    args={'k':k,'g':g,'f':f,'Lambda4':Lambda4}
    sol=solve_ivp(lambda t,y:coupled_rhs(t,y,**args),(0,duration),y0,
                  t_eval=t,method=method,rtol=rtol,atol=atol)
    if not sol.success:raise RuntimeError(sol.message)
    eth,eem,etotal=coupled_energy(sol.y,k=k,f=f,Lambda4=Lambda4)
    return {'t':t,'y':sol.y,'Etheta':eth,'Eem':eem,'Etotal':etotal,
            'max_relative_energy_drift':float(np.max(np.abs(etotal-etotal[0]))/etotal[0]),
            'nfev':sol.nfev,'params':dict(k=k,g=g,f=f,Lambda4=Lambda4,theta0=theta0,aplus=aplus,aminus=aminus)}

def no_free_helix(v=0.8,kappa=17.,mass=1.):
    # Constant lab speed timelike worldline in inertial Minkowski frame
    if not(0<v<1):raise ValueError('v/c must be in (0,1)')
    gamma=1/math.sqrt(1-v*v)
    return {'gamma':gamma,'proper_acceleration':gamma*gamma*v*v*kappa,
            'three_acceleration':v*v*kappa,
            'four_velocity_norm_squared':-1.}
