"""ROOT V90: independently reproducible toy-model analysis, NOT a unified-field proof.

Units: SI. Geometries are one-dimensional, fixed-path, nonoverlapping ideal point centers.
F_n= sum_{i,j=0}^1 (-1)^(i+j) r_ij^(-n).
Signs: attractive Newton potential gives theta_ij=+G*mA*mB*t/(hbar*r_ij).
Yukawa alpha is an extra gravitational-strength multiple; Coulomb charge product gives negative theta.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import exp, expm1, fsum, factorial, pi, sin, sqrt
from typing import Sequence

import numpy as np

G = 6.67430e-11
C = 299_792_458.0
HBAR = 6.62607015e-34 / (2*pi)  # exact SI h, computed hbar; matches V89 benchmark
EPS0 = 8.8541878128e-12
E = 1.602176634e-19
K_E = 1 / (4*pi*EPS0)

@dataclass(frozen=True)
class Geometry:
    d: float = 450e-6
    s_a: float = 200e-6
    s_b: float = 200e-6

    def distances(self) -> tuple[float, float, float, float]:
        if self.d <= 0 or self.s_a < 0 or self.s_b < 0:
            raise ValueError('All distances positive and displacements nonnegative')
        if self.d <= (self.s_a+self.s_b)/2:
            raise ValueError('All four branches must have strictly positive center distances')
        a,b,d=self.s_a,self.s_b,self.d
        return (d+(a-b)/2, d+(a+b)/2, d-(a+b)/2, d+(b-a)/2)

    @property
    def min_distance(self) -> float:
        return min(self.distances())

    def require_spheres_nonoverlap(self, radius_a: float, radius_b: float):
        if min(radius_a, radius_b) <= 0 or self.min_distance <= radius_a+radius_b:
            raise ValueError('Uniform spheres must have positive radius and never overlap')

SIGNS=(1,-1,-1,1)

def power_kernel(g: Geometry,n: int=1) -> float:
    if n < 0: raise ValueError('nonnegative power required')
    return fsum(sign/r**n for sign,r in zip(SIGNS,g.distances()))

def yukawa_kernel_naive(g: Geometry, lam: float) -> float:
    if lam<=0: raise ValueError('lambda must be positive')
    return fsum(s*exp(-r/lam)/r for s,r in zip(SIGNS,g.distances()))

def yukawa_delta_series(g: Geometry, lam: float, terms: int=26) -> float:
    """Compute F_Y-F_1 without subtractive cancellation in long-range regime.
    Taylor expansion converges at all finite r/lambda, but use only when lambda >= 5*max(r)
    to keep truncation error negligible with 26 or more terms.
    """
    if lam<=0: raise ValueError('lambda must be positive')
    if lam < 5*max(g.distances()):
        raise ValueError('Long range series requires lambda >= 5*max branch radius')
    if terms<5: raise ValueError('at least 5 terms required')
    rs=g.distances()
    # n=1 and n=2 vanish exactly due to affine annihilation; n starts at 3.
    return fsum(((-1)**n)*fsum(s*(r/lam)**(n-1) for s,r in zip(SIGNS,rs)) /
                (factorial(n)*lam) for n in range(3,terms+1))

def yukawa_kernel(g: Geometry, lam: float) -> float:
    if lam<=0: raise ValueError('lambda must be positive')
    if lam >= 5*max(g.distances()):
        return power_kernel(g,1)+yukawa_delta_series(g,lam)
    return yukawa_kernel_naive(g,lam)

def yukawa_kernel_derivative_lambda(g: Geometry, lam: float) -> float:
    if lam<=0: raise ValueError('lambda must be positive')
    return fsum(s*exp(-r/lam)/(lam**2) for s,r in zip(SIGNS,g.distances()))

def leading_delta(g: Geometry, lam: float) -> float:
    """F_Y-F1 = a*b/(3lambda^3) - d*a*b/(4lambda^4)+O(lambda^-5)."""
    return g.s_a*g.s_b/(3*lam**3) - g.d*g.s_a*g.s_b/(4*lam**4)

def mixed_curvature_integral(g: Geometry, derivative_2, n: int=60) -> float:
    """Gauss-Legendre quadrature of exact identity F_f=-int_A int_B f''(d+b-a)."""
    nodes, weights=np.polynomial.legendre.leggauss(n)
    alphas=nodes*g.s_a/2
    betas=nodes*g.s_b/2
    acc=0.0
    for x,wx in zip(alphas,weights):
        for y,wy in zip(betas,weights):
            acc += wx*wy*derivative_2(g.d+y-x)
    return -g.s_a*g.s_b*acc/4

def yukawa_curvature(r: float,lam:float) -> float:
    return exp(-r/lam)*(2/r**3+2/(lam*r**2)+1/(lam**2*r))

def sphere_radius(m:float,density:float) -> float:
    if m<=0 or density<=0: raise ValueError('positive mass and density required')
    return (3*m/(4*pi*density))**(1/3)

def sphere_yukawa_form_factor(x:float) -> float:
    """f(x)=3(x*cosh(x)-sinh(x))/x^3, valid for a uniform sphere at exterior points.
    A convergent Taylor series avoids cancellation for small x; x<=1 is intended.
    """
    from math import cosh,sinh
    if x<0: raise ValueError('nonnegative x')
    if x<0.3:
        # coefficients =6*(k+1)/(2k+3)! * 3? direct expansion: 1+x²/10+x⁴/280+x⁶/15120...
        return 1+x*x/10+x**4/280+x**6/15120+x**8/1330560
    return 3*(x*cosh(x)-sinh(x))/x**3

def interaction_phases(g: Geometry,m_a=1e-14,m_b=1e-14,t=1.0,
                       alpha=0.0,lam=1e-3,q_a=0.0,q_b=0.0):
    if min(m_a,m_b,t)<=0: raise ValueError('masses and duration must be positive')
    fn=power_kernel(g)
    fy=yukawa_kernel(g,lam) if alpha else 0.
    a=G*m_a*m_b*t/HBAR
    e=K_E*q_a*q_b*t/HBAR
    return {'newton':a*fn,'yukawa':alpha*a*fy,'coulomb':-e*fn,
            'total':(a-e)*fn+alpha*a*fy}

def pure_concurrence(delta:float) -> float:
    return abs(sin(delta/2))

def charge_parity_projector(positive:Sequence[float],negative:Sequence[float]):
    if len(positive)!=len(negative): raise ValueError('same number of observations')
    return (np.array(positive,dtype=float)+np.array(negative,dtype=float))/2, (np.array(positive,dtype=float)-np.array(negative,dtype=float))/2

def newton_nulled_weights(g1:Geometry,g2:Geometry):
    return np.array([1.0,-power_kernel(g1)/power_kernel(g2)])

def newton_nulled_signal(g1:Geometry,g2:Geometry,lam:float,alpha:float=1.0,
                        m_a:float=1e-14,m_b:float=1e-14,t:float=1.0) -> float:
    a=G*m_a*m_b*t/HBAR
    w=newton_nulled_weights(g1,g2)
    # cancel exact Newton algebraically, not by subtracting large rounded phases
    v=np.array([yukawa_kernel(g1,lam)-power_kernel(g1),
                yukawa_kernel(g2,lam)-power_kernel(g2)])
    return float(alpha*a*np.dot(w,v))

def design_matrix(ds,sa,sb,lam):
    gs=[Geometry(float(d),sa,sb) for d in ds]
    return np.column_stack([[power_kernel(g) for g in gs],
                            [yukawa_kernel(g,lam) for g in gs]])

def identifiability(ds,sa,sb,lam):
    m=design_matrix(ds,sa,sb,lam)
    sv=np.linalg.svd(m,compute_uv=False)
    return {'singular_values':sv.tolist(),
            'condition_number':float(sv[0]/sv[-1]) if sv[-1] else float('inf'),
            'normalised_separation':float(sv[-1]/sv[0]) if sv[0] else 0.0,
            'rank_numpy_default':int(np.linalg.matrix_rank(m))}

def residual_charge_equivalent(m_a:float,m_b:float) -> float:
    return sqrt(G*m_a*m_b/K_E)

def eft_phase_components(g:Geometry,m_a:float,m_b:float,t:float) -> dict:
    a=G*m_a*m_b*t/HBAR
    lp2=G*HBAR/C**3
    return {'newton':a*power_kernel(g,1),
            '1pn_potential_convention':a*3*G*(m_a+m_b)/C**2*power_kernel(g,2),
            'eft_one_loop_potential_convention':a*41/(10*pi)*lp2*power_kernel(g,3),
            'planck_length_squared_m2':lp2}

def synthetic_parity_observations(ds,sa,sb,lam,alpha,electric_fraction,
                                  noise_sigma=0.,seed=20261118):
    """Charge-even/odd *unwrapped phase* toy. Electric amplitude is dimensionless proxy,
    not a physically attainable continuous electrical charge on an isolated sphere.
    """
    rng=np.random.default_rng(seed)
    gs=[Geometry(float(d),sa,sb) for d in ds]
    a=G*(1e-14)**2/HBAR
    even_true=np.array([a*(power_kernel(g)+alpha*yukawa_kernel(g,lam)) for g in gs])
    electric=np.array([electric_fraction*a*power_kernel(g) for g in gs])
    y_plus=even_true+electric+rng.normal(0,noise_sigma,len(gs))
    y_minus=even_true-electric+rng.normal(0,noise_sigma,len(gs))
    even,odd=charge_parity_projector(y_plus,y_minus)
    return {'even_true':even_true,'electric_true':electric,'plus':y_plus,'minus':y_minus,
            'even':even,'odd':odd}
