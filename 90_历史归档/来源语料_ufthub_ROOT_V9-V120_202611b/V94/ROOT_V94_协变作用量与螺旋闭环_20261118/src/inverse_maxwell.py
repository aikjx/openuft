"""ROOT V94: exact inverse Lorentz-force drive for a prescribed smooth torus-knot path.

IMPORTANT: externally sourced and spatially unbounded ideal EM background; not a
self-consistent finite-energy solution of Maxwell-Lorentz point-particle dynamics.
All 3-vectors are laboratory-frame SI quantities. Massive test particle beta<1.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from scipy.integrate import solve_ivp
from src.v93_reference import TorusLoop, C, E, ME, EPS0


def as_cart(loop: TorusLoop, u, cylindrical):
    angle=loop.m*np.asarray(u)
    cs, sn=np.cos(angle), np.sin(angle)
    vec=np.asarray(cylindrical)
    return np.stack([vec[...,0]*cs-vec[...,1]*sn,
                     vec[...,0]*sn+vec[...,1]*cs,
                     vec[...,2]],axis=-1)

@dataclass(frozen=True)
class InverseDrive:
    loop:TorusLoop=TorusLoop()
    beta:float=0.8
    mass:float=ME
    charge:float=-E
    def __post_init__(self):
        if not (0 < self.beta < 1): raise ValueError('massive test particle beta must lie between 0 and 1')
        if not (self.mass>0 and np.isfinite(self.mass) and self.charge!=0 and np.isfinite(self.charge)):
            raise ValueError('mass>0, finite nonzero charge required')

    @property
    def v0(self): return self.beta*C
    @property
    def gamma0(self): return 1/np.sqrt(1-self.beta**2)
    @property
    def period(self): return self.loop.period(self.beta)

    def curve_state(self,u):
        P,Q,W=self.loop._components(u)
        s=self.loop.sigma(u)
        p=as_cart(self.loop,u,P)
        q=as_cart(self.loop,u,Q)
        w=as_cart(self.loop,u,W)
        v=self.v0*p/s[...,None]
        PQ=np.sum(p*q,axis=-1)
        a=self.v0**2*(q/s[...,None]**2-p*PQ[...,None]/s[...,None]**4)
        # d/du of constant-speed acceleration, followed by d/dt=(v0/s)d/du.
        deriv=(w/s[...,None]**2 -3*q*PQ[...,None]/s[...,None]**4
               -p*(np.sum(q*q,axis=-1)+np.sum(p*w,axis=-1))[...,None]/s[...,None]**4
               +4*p*PQ[...,None]**2/s[...,None]**6)
        j=self.v0**3*deriv/s[...,None]
        return self.loop.pos(u),v,a,j

    def B_and_dotB(self,u):
        x,v,a,j=self.curve_state(u)
        coeff=self.gamma0*self.mass/(self.charge*self.v0**2)
        B=coeff*np.cross(a,v)
        dotB=coeff*np.cross(j,v)
        return B,dotB

    def fields(self,u,x):
        """B is uniform in space at each prescribed laboratory time.
        E(x,t)=-1/2 (dB/dt) cross (x-r(t)); E=0 on r(t).
        """
        r,*_=self.curve_state(u)
        B,db=self.B_and_dotB(u)
        Efield=-0.5*np.cross(db, np.asarray(x)-r)
        return Efield,B

    def potentials(self,u,x):
        r,v,*_=self.curve_state(u)
        B,_=self.B_and_dotB(u)
        dx=np.asarray(x)-r
        A=0.5*np.cross(B,dx)
        phi=0.5*np.sum(np.cross(B,v)*dx,axis=-1)
        return phi,A

    def charge_density(self,u,x): return 0.0

    def current_density(self,u,x,du=1e-4):
        """J = -eps0 * partial_t E at fixed x, with curl B = 0.
        ddot B from centered finite difference in phase (for source diagnostic only).
        """
        r,v,*_=self.curve_state(u)
        _,db=self.B_and_dotB(u)
        dbp=self.B_and_dotB(u+du)[1]
        dbm=self.B_and_dotB(u-du)[1]
        ddB=(dbp-dbm)/(2*du)*self.v0/self.loop.sigma(u)
        return EPS0/2*(np.cross(ddB,np.asarray(x)-r)-np.cross(db,v))

    def field_force_residual(self,u):
        r,v,a,_=self.curve_state(u)
        Ef,B=self.fields(u,r)
        F=self.charge*(Ef+np.cross(v,B))
        expected=self.gamma0*self.mass*a
        return F-expected

    def rhs_phase(self,u,y):
        """dimensionless state y = (x/R, v/v0), independent variable phase u.
        Exact target follows the ODE; stability of deviations is not assumed.
        """
        x=y[:3]*self.loop.R
        vv=y[3:]*self.v0
        frac=np.dot(vv,vv)/(C*C)
        if frac>=1:
            # A physical solution must not reach this; controlled failure in tests.
            raise ValueError('numerical trajectory reached |v|>=c')
        gg=1/np.sqrt(1-frac)
        ef,bf=self.fields(u,x)
        lorentz_a=self.charge/(gg*self.mass)*(ef+np.cross(vv,bf)-np.dot(vv,ef)*vv/(C*C))
        dtdu=self.loop.sigma(u)/self.v0
        return np.r_[vv*dtdu/self.loop.R,lorentz_a*dtdu/self.v0]

    def integrated_orbit(self, perturb=None, rtol=2e-11,atol=2e-12, samples=501):
        x0,v0,_,_=self.curve_state(0.0)
        y0=np.r_[x0/self.loop.R,v0/self.v0]
        if perturb is not None: y0=y0+np.asarray(perturb)
        if np.dot(y0[3:],y0[3:])*self.beta**2>=1: raise ValueError('initial |v|>=c')
        us=np.linspace(0,self.loop.primitive_period,samples)
        sol=solve_ivp(self.rhs_phase,(0,self.loop.primitive_period),y0,
                      method='DOP853',atol=atol,rtol=rtol,t_eval=us,max_step=0.07)
        if not sol.success:raise RuntimeError(sol.message)
        true_x,true_v,*_=self.curve_state(us)
        ref=np.column_stack([true_x/self.loop.R,true_v/self.v0])
        err=np.linalg.norm((sol.y.T-ref),axis=1)
        return {'phases':us,'solution':sol.y.T,'reference':ref,
                'max_scaled_state_error':float(np.max(err)),
                'terminal_scaled_state_error':float(err[-1]),
                'final_scaled_state':sol.y[:,-1],
                'init_scaled_state':y0,
                'rhs_calls':sol.nfev}

    def monodromy_estimate(self,step=1e-6):
        """Finite-difference linearized one-period map, conditional on inverse drive.
        Floating point and tolerances limit interpretation (not formal stability).
        """
        base=self.integrated_orbit(samples=9,rtol=1e-11,atol=1e-12)['final_scaled_state']
        mat=np.empty((6,6))
        for k in range(6):
            h=np.zeros(6);h[k]=step
            yp=self.integrated_orbit(perturb=h,samples=9,rtol=1e-11,atol=1e-12)['final_scaled_state']
            ym=self.integrated_orbit(perturb=-h,samples=9,rtol=1e-11,atol=1e-12)['final_scaled_state']
            mat[:,k]=(yp-ym)/(2*step)
        vals=np.linalg.eigvals(mat)
        return {'matrix':mat,'eigenvalues':vals,
                'spectral_radius':float(np.max(np.abs(vals))),
                'determinant':float(np.linalg.det(mat)),
                'baseline_terminal':base}


def lorentz_frame_displacement(T, boost_beta):
    """Events same laboratory position separated by time T. Boost along x."""
    if abs(boost_beta)>=1:raise ValueError('boost speed must be subluminal')
    g=1/np.sqrt(1-boost_beta**2)
    return {'delta_t_prime_s':float(g*T),
            'delta_x_prime_m':float(-g*boost_beta*C*T)}


def uniform_static_B_trajectory(v_perp,v_parallel,B,q=-E,mass=ME, t=None):
    """Analytic exact SR motion in static B along +z (signed cyclotron omega)."""
    if t is None:t=np.linspace(0,3e-9,100)
    t=np.asarray(t)
    speed=np.hypot(v_perp,v_parallel)
    if not 0<=speed<C:raise ValueError('massive test particle v<c')
    gamma=1/np.sqrt(1-speed**2/C**2)
    omega=q*B/(gamma*mass)
    # v(0)=(vperp,0,vparallel): acceleration(0)=(0,-omega*vperp,0)
    if omega==0: return np.stack([v_perp*t,np.zeros_like(t),v_parallel*t],axis=-1)
    return np.stack([v_perp*np.sin(omega*t)/omega,
                     v_perp*(np.cos(omega*t)-1)/omega,
                     v_parallel*t],axis=-1)
