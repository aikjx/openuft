"""ROOT V112: reference Einstein-Maxwell, RN, dimensional and KK consistency checks.
All numerical constants explicit; no claim of new physical theory. SI unless indicated.
"""
import math
from dataclasses import dataclass
G=6.67430e-11
uG=0.00015e-11
c=299792458.0
eps0=8.8541878128e-12
hbar=1.054571817e-34
e=1.602176634e-19
me=9.1093837139e-31
mp=1.67262192595e-27
Mearth=5.9722e24
Rearth=6.371e6

def extremality_scale():
    return math.sqrt(4*math.pi*eps0*G)
def xi(mass,charge):
    assert mass>0
    return abs(charge)/(mass*extremality_scale())
def force_ratio(m1,q1,m2,q2):
    assert m1>0 and m2>0
    return abs(q1*q2)/(4*math.pi*eps0*G*m1*m2)
def grav_radius(mass):
    return G*mass/c**2
def charge_length_sq(charge):
    return G*charge**2/(4*math.pi*eps0*c**4)
def rn_horizons(mass,charge):
    """RN exterior of classical asymptotically flat spherical electrovac.
    Return None if superextremal; invalid as elementary-particle quantum model.
    """
    rg=grav_radius(mass)
    z=xi(mass,charge)
    if z>1.0+8*math.ulp(1.0): return None
    d=math.sqrt(max(0.,1.0-min(z,1.0)**2))
    outer=rg*(1.0+d)
    inner=rg*z*z/(1.0+d)  # stable when charge is small
    return (inner,outer)
def rn_lapse(r,mass,charge):
    rg=grav_radius(mass)
    return 1.-2*rg/r+charge_length_sq(charge)/r**2
def rn_phi(r,mass,charge):
    """Weak-field coordinate potential only, from g_tt=-(1+2 Phi/c^2)."""
    return -G*mass/r+G*charge**2/(8*math.pi*eps0*c**2*r*r)
def rn_radial_accel(r,mass,charge):
    return -G*mass/r**2+G*charge**2/(4*math.pi*eps0*c**2*r**3)
def weak_compactness(mass,r):
    return 2*G*mass/(c*c*r)
def planck_mass():
    """Derived from measured G: this is NOT a prediction of G."""
    return math.sqrt(hbar*c/G)
def G_from_mass_scale(mass):
    return hbar*c/(mass*mass)
def alpha_electric(charge):
    """Dimensionless electromagnetic charge strength in vacuum."""
    return charge*charge/(4*math.pi*eps0*hbar*c)
def alpha_gravitational(mass):
    """Dimensionless Newton gravitational strength at mass scale m."""
    return G*mass*mass/(hbar*c)
def kerr_spin_parameter(mass,J):
    """a/r_g = c|J|/(G M^2), for KN classical horizon audit."""
    assert mass>0
    return abs(J)*c/(G*mass*mass)
def kerr_newman_extremality(mass,charge,J):
    """xi^2 + (cJ/(GM^2))^2; classical KN horizon requires <=1."""
    return xi(mass,charge)**2+kerr_spin_parameter(mass,J)**2

def gravity_force(m1,m2,r):
    return G*m1*m2/(r*r)
def radiation_EM_invariant(E,B):
    """F_mu_nu F^mu_nu in SI-like normalization, metric -+++."""
    return 2*(B*B-(E/c)**2)
def scalar_kk_rhs(phi,kappa,F2):
    """Toy homogeneous scalar equation Box(phi)=kappa^2 phi^3 F^2/4."""
    return kappa*kappa*phi**3*F2/4.
def kk_constant_phi_consistent(F2,phi=1.,kappa=1.):
    if phi==0 or kappa==0: return True
    return abs(F2)<1e-15
def em_stress_trace_factor(d):
    """For L=-F^2/4, T^mu_mu=(1-D/4)F^2, in natural units."""
    return 1-d/4
def G_relative_uncertainty():
    return uG/G
def xi_relative_uncertainty():
    return uG/(2*G)

def dimension_G_solution():
    """Solve [c]^a[hbar]^b = [G] via the independent M,L,T equations."""
    import sympy as s
    a,b=s.symbols('a b')
    eq=[s.Eq(b,-1),s.Eq(a+2*b,3),s.Eq(-a-b,-2)]
    return s.solve(eq,[a,b]),eq
def trace_dimensional_identity():
    """Check dimension of hbar*c/m**2 equals G dimension."""
    return tuple((1,2,-1)[j]+(0,1,-1)[j]-2*(1,0,0)[j] for j in range(3))
