"""V111 finite-mode axion-Maxwell mathematics (not a new unified field theory).
Dimensionless time and natural units; gauge-fixed finite-dimensional truncation.
L=f^2 theta_dot^2/2 - L4(1-cos theta) + sum_h (Ah_dot^2-k^2 Ah^2-h*g*k*theta_dot*Ah^2)/2.
"""
from dataclasses import dataclass
import numpy as np
from scipy.integrate import solve_ivp

@dataclass(frozen=True)
class Params:
    k: float=1.0
    g: float=0.22
    f: float=1.0
    L4: float=4.0

    def validate(self):
        if self.k<=0 or self.f<=0 or self.L4<0:
            raise ValueError('Need k>0, f>0, Lambda4>=0')


def rhs(t, y, p):
    th, td, ap, vp, am, vm, iss = y
    dtd = (-p.L4*np.sin(th)+p.g*p.k*(ap*vp-am*vm))/p.f**2
    return np.array([td,dtd,vp,-(p.k**2+p.g*p.k*td)*ap,
                     vm,-(p.k**2-p.g*p.k*td)*am,np.sin(th)])


def observables(y,p):
    th,td,ap,vp,am,vm,iss=np.asarray(y)
    Etheta=.5*p.f**2*td**2+p.L4*(1-np.cos(th))
    Eem=.5*(vp**2+vm**2+p.k**2*(ap**2+am**2))
    H=Etheta+Eem
    Q=p.f**2*td-.5*p.g*p.k*(ap**2-am**2)
    N=Q+p.L4*iss
    Hright_bound=abs(p.g)*H/p.k
    return dict(Etheta=Etheta,Eem=Eem,H=H,Q=Q,N=N,
                helicity_surrogate=ap**2-am**2,
                td=td,Hright_bound=Hright_bound)


def simulate(p=Params(), y0=None, duration=120., steps=1201,
             method='DOP853', rtol=1e-10, atol=1e-12):
    p.validate()
    if y0 is None:
        y0=[.35,0.,.01,0.,.009,0.,0.]
    y0=np.asarray(y0,float)
    if y0.shape!=(7,): raise ValueError('y0 must be seven scalars, last one integral of sin theta')
    if duration<=0 or steps<2: raise ValueError('invalid integration interval')
    t_eval=np.linspace(0,float(duration),steps)
    sol=solve_ivp(lambda t,y:rhs(t,y,p),(0,float(duration)),y0,
                  method=method,rtol=rtol,atol=atol,t_eval=t_eval)
    if not sol.success: raise RuntimeError(sol.message)
    obs=observables(sol.y,p)
    H=np.asarray(obs['H']); N=np.asarray(obs['N']); Q=np.asarray(obs['Q'])
    return dict(t=sol.t,y=sol.y,obs=obs, energy_rel_drift=float(np.max(abs(H-H[0]))/H[0]),
                noether_absolute_drift=float(np.max(abs(N-N[0]))),
                q_absolute_range=float(np.ptp(Q)),nfev=sol.nfev,
                params=p.__dict__,method=method)


def analytic_bounds(p,H,Q=None):
    """Bound for full closed finite-mode dynamical system: |Q-f² theta_dot|<=|g|H/k."""
    p.validate()
    if H<0: raise ValueError('H must be nonnegative')
    out=dict(energy=H,charge_momentum_correction_bound=abs(p.g)*H/p.k,
             theta_velocity_abs_bound=(2*H)**.5/p.f,
             sufficient_no_instantaneous_tachyon=(abs(p.g)*(2*H)**.5/p.f < p.k))
    if Q is not None:
        b=abs(p.g)*H/p.k
        out.update(theta_velocity_from_Q_min=(Q-b)/p.f**2,
                   theta_velocity_from_Q_max=(Q+b)/p.f**2,
                   monotonic_positive_sufficient=Q>b,
                   monotonic_negative_sufficient=Q< -b)
    return out
