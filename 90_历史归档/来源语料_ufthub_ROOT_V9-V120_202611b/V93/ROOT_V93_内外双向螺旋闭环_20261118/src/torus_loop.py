"""ROOT V93 — physically labeled closed toroidal helices (theory, not discovery).
All methods are pure mathematical geometry + SR inverse dynamics, no new force law.
SI units: radius R,a [m], phase u [dimensionless], v [m/s].
"""
from __future__ import annotations
from dataclasses import dataclass
from math import cos, sin, sqrt, pi, gcd
import numpy as np
from scipy.integrate import quad, cumulative_trapezoid
from scipy.interpolate import PchipInterpolator

C = 299792458.0
HBAR = 1.054571817e-34
H = 6.62607015e-34
HBAR_EXACT_FROM_H = H/(2*pi)
E = 1.602176634e-19
ME = 9.1093837139e-31  # CODATA 2022 nominal (rounding uncertainty small)
EPS0 = 8.8541878188e-12  # approximately CODATA 2022, not independently fixed

@dataclass(frozen=True)
class TorusLoop:
    R: float = 0.01
    a: float = 0.002
    m: int = 2
    n: int = 3
    def __post_init__(self):
        if not (np.isfinite(self.R) and np.isfinite(self.a) and self.R > self.a > 0):
            raise ValueError('Require R>a>0 finite SI lengths.')
        if type(self.m) is not int or type(self.n) is not int or self.m <= 0 or self.n <= 0:
            raise ValueError('m,n must be positive integers.')
    @property
    def primitive_period(self):
        return 2*pi/gcd(self.m,self.n)

    def pos(self,u):
        u=np.asarray(u)
        rho=self.R+self.a*np.cos(self.n*u)
        return np.stack([rho*np.cos(self.m*u),rho*np.sin(self.m*u),self.a*np.sin(self.n*u)],axis=-1)

    def _components(self,u):
        """d^k r/du^k in moving cylindrical orthonormal basis (e_r,e_theta,e_z)."""
        u=np.asarray(u,dtype=float)
        co=np.cos(self.n*u); si=np.sin(self.n*u)
        R,a,m,n=self.R,self.a,self.m,self.n
        rho=R+a*co
        rup=-a*n*si
        rupp=-a*n*n*co
        ruppp=a*n**3*si
        zp=a*n*co
        zpp=-a*n*n*si
        zppp=-a*n**3*co
        q1=np.stack([rup,m*rho,zp],axis=-1)
        q2=np.stack([rupp-m*m*rho,2*m*rup,zpp],axis=-1)
        q3=np.stack([ruppp-3*m*m*rup,3*m*rupp-m**3*rho,zppp],axis=-1)
        return q1,q2,q3

    def sigma(self,u):
        u=np.asarray(u)
        rho=self.R+self.a*np.cos(self.n*u)
        return np.sqrt((self.a*self.n)**2+(self.m*rho)**2)

    def curvature(self,u):
        q1,q2,_=self._components(u)
        return np.linalg.norm(np.cross(q1,q2),axis=-1)/self.sigma(u)**3

    def torsion(self,u):
        q1,q2,q3=self._components(u)
        cross=np.cross(q1,q2)
        return np.sum(cross*q3,axis=-1)/np.sum(cross*cross,axis=-1)

    def speed_components(self,u,beta=1.0):
        """Return (v_r,v_az,v_z,omega, v_pol) with constant |v|=beta*c."""
        if not 0 < beta <= 1: raise ValueError('beta must be (0,1]')
        u=np.asarray(u); scale=beta*C/self.sigma(u)
        return (-self.a*self.n*np.sin(self.n*u)*scale,
                self.m*(self.R+self.a*np.cos(self.n*u))*scale,
                self.a*self.n*np.cos(self.n*u)*scale,
                self.m*scale,
                self.a*self.n*scale)

    def period(self,beta=1.0):
        return quad(lambda u:float(self.sigma(u)),0,self.primitive_period,epsabs=1e-13,epsrel=2e-13,limit=350)[0]/(beta*C)

    def arc_length(self):
        return self.period(beta=1)*C

    def time_map(self,beta=1.0,N=10001):
        u=np.linspace(0,self.primitive_period,N)
        t=np.r_[0,np.cumsum((self.sigma(u)[1:]+self.sigma(u)[:-1])*np.diff(u)/2)/(beta*C)]
        return u,t

    def phase_at_times(self,t,beta=1.0,N=10001):
        u,tmap=self.time_map(beta,N=N)
        if np.min(t)<0 or np.max(t)>tmap[-1]: raise ValueError('outside single period time')
        return PchipInterpolator(tmap,u)(t)

    def accel_components(self,u,beta=1.0):
        """Physical 3-accel expressed in (e_r,e_theta,e_z); exact constant-speed reparameterization."""
        q1,q2,_=self._components(u)
        s=self.sigma(u); v=beta*C
        dot=np.sum(q1*q2,axis=-1)
        return v*v*(q2/s[...,None]**2-q1*(dot/s**4)[...,None])

    def accel_cartesian(self,u,beta=0.8):
        """Acceleration in fixed lab xyz (as opposed to moving cylindrical basis)."""
        u=np.asarray(u,dtype=float)
        ac=self.accel_components(u,beta)
        phi=self.m*u;co=np.cos(phi);si=np.sin(phi)
        return np.stack([ac[...,0]*co-ac[...,1]*si,ac[...,0]*si+ac[...,1]*co,ac[...,2]],axis=-1)

    def net_impulse_per_unit_mass(self,beta=0.8,samples=16001):
        """Numerical integral ∫a dt in lab Cartesian; should vanish for a smooth periodic velocity."""
        from scipy.integrate import simpson
        u=np.linspace(0,self.primitive_period,samples)
        f=self.accel_cartesian(u,beta)*self.sigma(u)[...,None]/(beta*C)
        return simpson(f,x=u,axis=0)

    def total_curvature(self):
        return quad(lambda u:float(self.curvature(u)*self.sigma(u)),0,self.primitive_period,epsabs=1e-9,limit=350)[0]

    def signed_total_torsion(self):
        return quad(lambda u:float(self.torsion(u)*self.sigma(u)),0,self.primitive_period,epsabs=1e-9,limit=350)[0]

    def wilson_flux(self,B):
        """Line integral A.dl for A=(B*rho/2)e_theta; primitive period (winding m/gcd)."""
        gg=gcd(self.m,self.n)
        return pi*B*(self.m/gg)*(self.R**2+self.a**2/2)

    def numerical_flux(self,B):
        period=self.primitive_period
        return quad(lambda u: B*self.m*(self.R+self.a*cos(self.n*u))**2/2, 0,period,epsabs=1e-13,epsrel=1e-12)[0]

    def ab_phase(self,B,charge=E):
        return charge*self.wilson_flux(B)/HBAR_EXACT_FROM_H

    def relativistic_inverse_force(self,u,beta=0.8,mass=ME):
        """Relativistic three-force magnitude for massive particle with constant speed beta*c.
        F=gamma*m v^2 kappa; inverse local B_min=F/(abs(q)*v), not a global Maxwell field.
        """
        if not 0<beta<1:raise ValueError('massive particle requires beta<1')
        gamma=1/sqrt(1-beta**2)
        k=self.curvature(u)
        force=gamma*mass*(beta*C)**2*k
        B=force/(E*beta*C)
        return force,B

    def classical_radiated_power(self,u,beta=0.8,charge=E):
        """Classical Lienard power for instantaneous acceleration strictly perpendicular to velocity.
        Radiation reaction is NOT included in the inverse dynamics, so this is a diagnostic estimate.
        """
        if not 0<beta<1:raise ValueError('classical massive charge beta<1')
        gamma=1/sqrt(1-beta**2);acc=(beta*C)**2*self.curvature(u)
        return charge**2*gamma**4*acc**2/(6*pi*EPS0*C**3)

    def classical_radiated_energy_one_lap(self,beta=0.8):
        v=beta*C
        return quad(lambda u:float(self.classical_radiated_power(u,beta)*self.sigma(u)/v),
                    0,self.primitive_period,epsabs=1e-26,epsrel=1e-11,limit=350)[0]

    def summary(self,beta=0.8,B=0.001):
        grid=np.linspace(0,self.primitive_period,10001)
        k=self.curvature(grid); tau=self.torsion(grid)
        _,vtheta,_,omega,_=self.speed_components(grid,beta=beta)
        F,Bmin=self.relativistic_inverse_force(grid,beta)
        return {
            'R_m':self.R,'a_m':self.a,'m':self.m,'n':self.n,
            'primitive_phase_period':self.primitive_period,
            'radial_min_m':self.R-self.a,'radial_max_m':self.R+self.a,
            'rho_breathing_cycles':self.n//gcd(self.m,self.n),
            'azimuth_windings':self.m//gcd(self.m,self.n),
            'beta':beta,'physical_speed_m_s':beta*C,
            'arc_length_m':self.arc_length(),
            'travel_period_s':self.period(beta),
            'curvature_range_m_inverse':[float(np.min(k)),float(np.max(k))],
            'torsion_range_m_inverse':[float(np.min(tau)),float(np.max(tau))],
            'omega_range_rad_s':[float(np.min(omega)),float(np.max(omega))],
            'total_curvature_dimensionless':self.total_curvature(),
            'signed_total_torsion_dimensionless':self.signed_total_torsion(),
            'inverse_electron_force_N_range':[float(np.min(F)),float(np.max(F))],
            'inverse_electron_Bmin_T_range':[float(np.min(Bmin)),float(np.max(Bmin))],
            'wilson_flux_Wb':self.wilson_flux(B),
            'AB_phase_rad':self.ab_phase(B),
            'test_B_T':B,
            'classical_radiation_energy_per_lap_J':self.classical_radiated_energy_one_lap(beta),
            'electron_kinetic_energy_J':(1/sqrt(1-beta**2)-1)*ME*C*C,
            'massless_beta1_travel_period_s':self.period(beta=1.0),
            'omega_inside_over_outside':float(self.sigma(0)/self.sigma(pi/self.n)),
            'topology':'coprime m,n>1 gives torus knot T(m,n); gcd>1 means one primitive T(m/g,n/g) component repeated if u runs 0..2pi'}
