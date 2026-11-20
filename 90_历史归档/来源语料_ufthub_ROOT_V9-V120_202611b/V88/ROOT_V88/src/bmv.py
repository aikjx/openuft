"""ROOT V88: two-body Newtonian quantum phase, dephasing, and model discrimination.
All input values in SI. Idealized frozen-path two-level model, not measured data.
"""
from __future__ import annotations
import math
from dataclasses import dataclass
import numpy as np

G=6.67430e-11
HBAR=1.0545718176461565e-34
C=299792458.0
EPS0=8.8541878188e-12
PI=math.pi

@dataclass(frozen=True)
class Setup:
    m1: float=1e-14
    m2: float=1e-14
    d: float=450e-6
    s1: float=200e-6
    s2: float=200e-6
    t: float=1.0
    gamma1: float=0.0
    gamma2: float=0.0
    q1: float=0.0
    q2: float=0.0

    def validate(self):
        items = (self.m1,self.m2,self.d,self.s1,self.s2,self.t,self.gamma1,self.gamma2,self.q1,self.q2)
        if not all(math.isfinite(z) for z in items): raise ValueError('all parameters must be finite')
        if self.m1<=0 or self.m2<=0 or self.d<=0 or self.t<0 or self.s1<0 or self.s2<0: raise ValueError('invalid masses/distances/time')
        if self.gamma1<0 or self.gamma2<0: raise ValueError('dephasing rates must be non-negative')
        if self.d<=(self.s1+self.s2)/2: raise ValueError('branches collide/cross')
        return self


def distances(p:Setup):
    p.validate()
    # branches i=0,1 correspond x1=-s1/2,+s1/2; likewise x2=d + (-s2/2,+s2/2)
    x1=np.array([-p.s1/2,p.s1/2]); x2=p.d+np.array([-p.s2/2,p.s2/2])
    return x2[None,:]-x1[:,None]


def phases(p:Setup,gravity=True,coulomb=True):
    r=distances(p)
    k=0.0
    if gravity: k+=G*p.m1*p.m2/HBAR
    if coulomb: k-=p.q1*p.q2/(4*PI*EPS0*HBAR)
    return (k*p.t)/r


def cross_phase(ph):
    a=np.asarray(ph,dtype=float)
    if a.shape!=(2,2):raise ValueError('requires 2x2 branch phases')
    return float(a[0,0]-a[0,1]-a[1,0]+a[1,1])


def pure_state(ph):
    arr=np.asarray(ph,dtype=float)
    if arr.shape!=(2,2):raise ValueError('requires 2x2 phases')
    return np.exp(1j*arr.reshape(4))/2


def pure_concurrence(ph):
    return abs(math.sin(cross_phase(ph)/2))


def density(p:Setup,gravity=True,coulomb=True):
    v=pure_state(phases(p,gravity,coulomb))
    rho=np.outer(v,v.conj())
    # local pure dephasing channel: basis coherence |0><1| scaled e^-gamma*t
    e1=math.exp(-p.gamma1*p.t); e2=math.exp(-p.gamma2*p.t)
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    rho[2*i+j,2*k+l]*=(e1 if i!=k else 1)*(e2 if j!=l else 1)
    return rho


def partial_transpose(rho):
    rho=np.asarray(rho, dtype=complex)
    if rho.shape!=(4,4):raise ValueError('requires 4x4 density matrix')
    return np.transpose(rho.reshape(2,2,2,2),(0,3,2,1)).reshape(4,4)


def negativity(rho):
    eig=np.linalg.eigvalsh(partial_transpose(rho))
    return max(0.0,float(-np.sum(eig[eig<0])))


def linear_entropy(rho):
    return float(1-np.trace(rho@rho).real)


def mass_coefficient(p:Setup):
    # d Δ/dG = t*m1*m2/hbar * geometry; nonzero unless branches degenerate
    geo=cross_phase(1/distances(p))
    return p.m1*p.m2*p.t*geo/HBAR


def coulomb_equivalent_charge(p:Setup):
    # |q1*q2| that exactly matches |G m1 m2| in a 1/r potential
    return math.sqrt(4*PI*EPS0*G*p.m1*p.m2)


def classical_channel_state(p:Setup,n=1000,seed=20261118):
    """Mixture of product states after correlated random LOCAL Z phases;
    cannot generate entanglement (one explicit LOCC countermodel).
    """
    p.validate()
    rng=np.random.default_rng(seed)
    sigma=1.0
    rho=np.zeros((4,4),complex)
    for _ in range(n):
        z=rng.normal(0,sigma)
        a=np.array([1,np.exp(1j*z)],complex)/math.sqrt(2)
        b=np.array([1,np.exp(-1j*z)],complex)/math.sqrt(2)
        v=np.kron(a,b)
        rho+=np.outer(v,v.conj())/n
    return rho


def simulate(p:Setup):
    p.validate()
    th=phases(p)
    rho=density(p)
    dphi=cross_phase(th)
    return {
      'setup':p.__dict__,
      'distance_matrix_m':distances(p).tolist(),
      'phase_matrix_rad':th.tolist(),
      'nonlocal_phase_rad':dphi,
      'ideal_concurrence':pure_concurrence(th),
      'ideal_negativity':pure_concurrence(th)/2,
      'dephased_negativity':negativity(rho),
      'dephased_linear_entropy':linear_entropy(rho),
      'equivalent_equal_residual_charge_C':coulomb_equivalent_charge(p),
      'd_nonlocal_phase_dG':mass_coefficient(p),
      'classical_local_phase_channel_negativity':negativity(classical_channel_state(p,n=256)),
      'status':'SYNTHETIC / THEORETICAL ONLY - NOT AN EXPERIMENT',
    }
