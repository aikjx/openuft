"""Established formulas separated from explicitly speculative couplings.
Units SI except dimensionless toy RGE / helix tests. No independent G prediction.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from math import pi, sin, cos, sqrt, sinh, cosh, exp, log
from typing import Sequence

C=299_792_458.0
HBAR=1.054571817e-34
G_EXP=6.67430e-11  # CODATA 2022, experimental input, NOT predicted
M_EARTH=5.9722e24
R_EARTH=6_371_000.0
M_SUN=1.9884e30
R_SUN=695_700_000.0

@dataclass(frozen=True)
class Body:
    name: str
    mass: float
    radius: float
    notes: str='spherical, nonrotating reference'
    @property
    def density(self) -> float:
        return 3*self.mass/(4*pi*self.radius**3)
    @property
    def gravity(self)->float:
        return G_EXP*self.mass/self.radius**2
    @property
    def tidal(self)->float:
        return 2*G_EXP*self.mass/self.radius**3
    @property
    def kretschmann(self)->float:
        return 48*(G_EXP*self.mass/(C*C))**2/self.radius**6

BODIES={
    'Earth': Body('Earth', M_EARTH,R_EARTH),
    'Moon': Body('Moon',7.342e22,1_737_400),
    'Mars': Body('Mars',6.4171e23,3_389_500),
    'Jupiter': Body('Jupiter',1.89813e27,69_911_000),
    'Sun': Body('Sun',M_SUN,R_SUN),
    'WhiteDwarf_demo':Body('WhiteDwarf_demo',0.6*M_SUN,7_000_000,'hypothetical representative not an observed star'),
    'NeutronStar_demo':Body('NeutronStar_demo',1.4*M_SUN,12_000,'hypothetical nonrotating 1.4 solar mass 12km radius; exterior Schwarzschild only'),
}

def g_newton(mass:float, radius:float)->float:
    return G_EXP*mass/radius**2

def kretschmann(mass:float,r:float)->float:
    return 48*(G_EXP*mass/C**2)**2/r**6

def kretschmann_from_density(density:float)->float:
    return (256*pi*pi/3)*(G_EXP*density/(C*C))**2

def g_from_mean_density(density:float,radius:float)->float:
    return 4*pi*G_EXP*density*radius/3

def helix(R:float,omega:float,u:float)->dict:
    assert R>0
    speed=sqrt((R*omega)**2+u*u)
    assert speed>0
    # speed is unconstrained unless user imposes =c
    return {'speed':speed,'curvature':R*omega**2/speed**2,
            'torsion':u*omega/speed**2,
            'acceleration':R*omega**2,
            'dot_v_a':0.0}

def dimension_G_can_be_built_with_c_hbar()->bool:
    # M: b=-1, T: -(a+b)=-2 -> a=3; L: a+2b = 1, not 3
    a,b=3,-1
    return (a+2*b)==3

def rg_generated_scale(mu:float,g:float,b0:float)->float:
    """Toy one-loop asymptotically free scale; all parameters are inputs."""
    assert mu>0 and g>0 and b0>0
    return mu*exp(-8*pi*pi/(b0*g*g))

def sm_anomalies()->dict:
    """Exact rational anomalies per SM generation using left-handed Weyl fermions."""
    F=Fraction
    # Representation: (color multiplicity, SU2 multiplicity, Y)
    species=[(3,2,F(1,6)),(3,1,F(-2,3)),(3,1,F(1,3)),
             (1,2,F(-1,2)),(1,1,F(1))]
    u1cube=sum((color*weak*y**3 for color,weak,y in species),F(0))
    grav=sum((color*weak*y for color,weak,y in species),F(0))
    su3=2*F(1,6)*F(1,2)+F(-2,3)*F(1,2)+F(1,3)*F(1,2)
    su2=3*F(1,6)*F(1,2)+F(-1,2)*F(1,2)
    return {'U1_cube':u1cube,'grav_U1':grav,'SU3_sq_U1':su3,'SU2_sq_U1':su2}

def gauge_running(alpha_em_inverse=127.95,sin2theta=0.23122,alpha_s=0.118,mz=91.1876)->dict:
    """SM one-loop, GUT SU5 hypercharge normalization. Inputs are illustrative, not fits."""
    a=[(3/5)*(1-sin2theta)*alpha_em_inverse,
       sin2theta*alpha_em_inverse,
       1/alpha_s]
    b=[41/10,-19/6,-7]
    crossings=[]
    for i,j in ((0,1),(0,2),(1,2)):
        L=2*pi*(a[i]-a[j])/(b[i]-b[j])
        crossings.append({'pair':f'{i+1}-{j+1}','log_mu_over_mz':L,'mu_GeV':mz*exp(L)})
    a_bar=sum(a)/3;b_bar=sum(b)/3
    Lopt=2*pi*sum((ai-a_bar)*(bi-b_bar) for ai,bi in zip(a,b))/sum((bi-b_bar)**2 for bi in b)
    evolved=[ai-bi*Lopt/(2*pi) for ai,bi in zip(a,b)]
    return {'alpha_inverse_at_MZ':a,'beta_coefficients':b,'crossings':crossings,
            'best_mu_GeV':mz*exp(Lopt),'best_alpha_inverse':evolved,
            'max_minus_min_at_best':max(evolved)-min(evolved)}

def _uniform_shape(x:float)->float:
    if x < .05:
        return 1 +x*x/10+x**4/280+x**6/15120+x**8/1330560
    return 3*(x*cosh(x)-sinh(x))/x**3

def _weighted_ball(radius:float,range_m:float,observation_r:float)->float:
    """R^3 * exp(-r/lambda) * F(R/lambda), computed stably for r >= R."""
    if radius==0:return 0.0
    assert radius>0 and range_m>0 and observation_r>=radius
    x=radius/range_m
    if x<.05:
        return radius**3 * exp(-observation_r/range_m)*_uniform_shape(x)
    if x<=40:
        return radius**3 * exp(-observation_r/range_m)*_uniform_shape(x)
    return 1.5*range_m**3*((x-1)*exp(-(observation_r-radius)/range_m) + (x+1)*exp(-(observation_r+radius)/range_m))

def uniform_yukawa_ratio(radius:float,observation_r:float,range_m:float,alpha:float=1.0,source_charge=1.0,target_charge=1.0)->float:
    """g_Y/g_Newton for uniform ball source (linear Yukawa with charges)."""
    assert 0<radius<=observation_r and range_m>0
    return alpha*source_charge*target_charge*(1+observation_r/range_m)*_weighted_ball(radius,range_m,observation_r)/radius**3

@dataclass(frozen=True)
class Shell:
    outer_radius:float
    density:float
    source_charge:float=1.0

def layered_yukawa_ratio(shells:Sequence[Shell],observation_r:float,range_m:float,alpha=1.0,target_charge=1.0)->float:
    """Piecewise constant spherical density/charge shells; relative to total Newtonian mass."""
    assert shells and range_m>0
    rprev=0.0; mass_weight=0.0; source_weight=0.0
    for s in shells:
        assert s.outer_radius>rprev and s.density>0
        mass_weight+=s.density*(s.outer_radius**3-rprev**3)
        source_weight+=s.density*s.source_charge*(_weighted_ball(s.outer_radius,range_m,observation_r)-_weighted_ball(rprev,range_m,observation_r))
        rprev=s.outer_radius
    assert observation_r>=rprev
    return alpha*target_charge*(1+observation_r/range_m)*source_weight/mass_weight

def eotvos_eta(delta_a:float,delta_b:float)->float:
    """a_i=g*(1+delta_i), Eotvos eta=2(a_i-a_j)/(a_i+a_j)."""
    return 2*(delta_a-delta_b)/(2+delta_a+delta_b)

def proxy_charge_Z_over_A(atomic_Z:float,atomic_mass_u:float)->float:
    assert atomic_mass_u>0
    return atomic_Z/atomic_mass_u

def miniature_eta_bound(eta_center:float,stat:float,syst:float,
                        shape_factor:float,source_charge:float,delta_target_charge:float)->float:
    """Illustrative conservative magnitude bound using |central|+1.96*quadrature-sigma, linear regime.
       NOT a full likelihood or a model-independent bound.
    """
    from math import hypot
    return (abs(eta_center)+1.96*hypot(stat,syst))/abs(shape_factor*source_charge*delta_target_charge)

def curvature_toy_delta_mass2(mass:float,radius:float,length_scale:float,xi:float)->float:
    """Toy EFT in geometrical (inverse-length) mass^2 units: Δm²=xi*l²*K."""
    return xi*length_scale**2*kretschmann(mass,radius)
