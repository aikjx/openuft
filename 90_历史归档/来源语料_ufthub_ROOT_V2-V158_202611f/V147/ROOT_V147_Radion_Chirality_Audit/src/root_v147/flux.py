"""Six-dimensional Einstein-Maxwell-sphere toy model. c=1; hbar,G independent.

A,B,C are dimensionFUL in a chosen common length/action system: [A]=S/L^2,
[B]=S, [C]=S L^2, [K4]=S/L^2.  The sample data use normalized
reference length/action and are NOT experimental measurements.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import pi, sqrt, isfinite


def positive(r):
    if not isfinite(r) or r <= 0:
        raise ValueError('radius must be finite and >0')

@dataclass(frozen=True)
class Vacuum:
    radius: float
    energy: float
    radial_mass2: float   # L^-2; physical particle mass = hbar * sqrt(radial_mass2)
    kind: str

@dataclass(frozen=True)
class FluxModel:
    A: float
    B: float
    C: float
    K4: float

    def __post_init__(self):
        if not all(isfinite(x) for x in (self.A,self.B,self.C,self.K4)):
            raise ValueError('finite coefficients required')
        if self.A <= 0 or self.B <= 0 or self.C < 0 or self.K4 <= 0:
            raise ValueError('require A,B,K4>0,C>=0')

    def v(self,r):
        positive(r)
        return self.A/r**2 - self.B/r**4 + self.C/r**6

    def dv(self,r):
        positive(r)
        return -2*self.A/r**3 + 4*self.B/r**5-6*self.C/r**7

    def d2v(self,r):
        positive(r)
        return 6*self.A/r**4 -20*self.B/r**6+42*self.C/r**8

    @property
    def D(self):
        return self.B*self.B-3*self.A*self.C

    def stationary(self):
        if self.C==0:
            r=sqrt(2*self.B/self.A)
            return [Vacuum(r,self.v(r),self.mass2_direct(r),'maximum')]
        # exclude nearly-degenerate numerical roots from classification
        tol=1e-13 * max(self.B*self.B,3*self.A*self.C)
        if self.D < -tol:
            return []
        if abs(self.D) <= tol:
            r=sqrt(self.B/self.A)
            return [Vacuum(r,self.v(r),0.,'degenerate')]
        d=sqrt(self.D)
        y_min=3*self.C/(self.B+d)    # avoid cancellation for small C
        y_max=(self.B+d)/self.A
        return [Vacuum(sqrt(y_min),self.v(sqrt(y_min)),
                       2*d/(self.K4*y_min*y_min),'minimum'),
                Vacuum(sqrt(y_max),self.v(sqrt(y_max)),
                       -2*d/(self.K4*y_max*y_max),'maximum')]

    def min(self):
        return next((v for v in self.stationary() if v.kind=='minimum'),None)

    def mass2_direct(self,r):
        """at a stationary radius; canonical phi =2 sqrt(K4) ln(R/R0)."""
        return r*r*self.d2v(r)/(4*self.K4)

    def drdC_at_min(self):
        """Exact derivative dR_min/dC at fixed A,B,K4 (noncritical only)."""
        minimum=self.min()
        if minimum is None:
            raise ValueError('no isolated positive-flux minimum')
        return 3/(4*minimum.radius*sqrt(self.D))


def six_d_coefficients(K6, Lambda6, chi6, n, R0):
    if not (K6>0 and Lambda6>0 and chi6>0 and R0>0 and isinstance(n,int)):
        raise ValueError('invalid six-dimensional input')
    return FluxModel(4*pi*Lambda6*R0**4,4*pi*K6*R0**4,
                     pi*chi6*n*n*R0**4/2,4*pi*K6*R0**2)


def illustrated(n):
    return six_d_coefficients(1/(2*pi),1/(4*pi),2/(9*pi),n,1.0)


def tuned_flat_vacuum(n,K6=1.5,chi6=.7):
    """Constructively illustrates free parameter tuning for ANY nonzero integer n.
    R0 chosen at vacuum, which identifies 4D Einstein-frame Newton constant.
    """
    if type(n) is not int or not n or K6<=0 or chi6<=0:
        raise ValueError('nonzero integer n and positive couplings required')
    lam=2*K6*K6/(chi6*n*n)
    r=abs(n)*sqrt(chi6/K6)/2
    p=six_d_coefficients(K6,lam,chi6,n,r)
    return dict(n=n,Lambda6=lam,Rstar=r,K4=p.K4,
                G4=1/(8*pi*p.K4),V=p.v(r),m2=p.mass2_direct(r))


def scalar_test_mass_squared(ell,r,m6_sq=0.0):
    """Neutral, minimally coupled TEST scalar on fixed M4xS2, not coupled KK metric spectrum."""
    if type(ell) is not int or ell<0 or m6_sq<0:
        raise ValueError('ell integer >=0; m6_sq>=0')
    positive(r)
    return m6_sq+ell*(ell+1)/(r*r)


def degeneracy(ell):
    if type(ell) is not int or ell<0: raise ValueError('ell >= 0')
    return 2*ell+1


def scalar_beta_brane():
    """Dimensionless coupling Mpl*d ln A(phi)/dphi: A=exp[-phi/(2 Mpl)]."""
    return -0.5


def scalar_strength_brane():
    """2*beta**2, relative to bare tensor Newton coupling; conditional brane matter."""
    return 2*scalar_beta_brane()**2


def yukawa_potential_fraction(distance,lambda_range,alpha=None):
    if distance<0: raise ValueError('distance >= 0')
    positive(lambda_range)
    from math import exp
    if alpha is None: alpha=scalar_strength_brane()
    return alpha*exp(-distance/lambda_range)


def yukawa_force_fraction(distance,lambda_range,alpha=None):
    if distance<0: raise ValueError('distance >= 0')
    positive(lambda_range)
    from math import exp
    if alpha is None: alpha=scalar_strength_brane()
    x=distance/lambda_range
    return alpha*(1+x)*exp(-x)
