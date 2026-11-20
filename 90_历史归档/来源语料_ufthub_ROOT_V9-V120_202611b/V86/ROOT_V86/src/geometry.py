"""Extended spherical sources for finite-range Yukawa signals.
The nuclear/composition "charge" density is an additional model input; neither
standard gravity nor scalar theory requires it to equal the ordinary mass density.
"""
import math
from scipy.integrate import quad
from .physics import check,positive,sphere_envelope

def layered_envelope(shells,r,length):
    """[(inner_radius, outer_radius, density, charge_per_mass), ...].
    Returns mass-normalized external charge Yukawa envelope; source total mass is
    the ordinary mass of the shells, not their scalar charge total.
    """
    positive(r,length)
    total=0.;weighted=0.;last=0.
    for inner,outer,density,charge in shells:
        check(inner,outer,density,charge)
        if inner<0 or inner!=last or outer<=inner or density<=0 or r<outer:
            raise ValueError('contiguous, strictly positive shells inside evaluation radius required')
        mass_core=outer**3-inner**3
        total+=density*mass_core
        # Difference of enclosing sphere integrals; shell has constant charge density.
        weighted+=density*charge*(outer**3*sphere_envelope(outer,r,length)
                                  -inner**3*sphere_envelope(inner,r,length))
        last=outer
    if total<=0:raise ValueError('no source matter')
    return weighted/total

def uniform_2sphere_envelope(radius1,radius2,separation,length):
    """F(R1/lam)*F(R2/lam)*exp(-d/lam), nonoverlapping homogeneous spheres.
    Uses exponential cancellation-free formula for x1,x2>0.2.
    """
    check(radius1,radius2,separation,length)
    positive(separation,length)
    if radius1<0 or radius2<0 or separation<radius1+radius2:
        raise ValueError('requires disjoint spheres')
    x1=radius1/length;x2=radius2/length
    if x1<=.2 or x2<=.2:
        def small_f(x):return 1+x*x/10+x**4/280+x**6/15120+x**8/1330560
        if x1<=.2 and x2<=.2: return small_f(x1)*small_f(x2)*math.exp(-separation/length)
        if x1<=.2: return small_f(x1)*sphere_envelope(radius2,separation,length)
        return small_f(x2)*sphere_envelope(radius1,separation,length)
    t=0.
    for a,sign1 in ((x1-1,1),(x1+1,-1)):
        for b,sign2 in ((x2-1,1),(x2+1,-1)):
            t+=a*b*math.exp(-(separation-sign1*radius1-sign2*radius2)/length)
    return 9*t/(4*x1**3*x2**3)

def uniform_sphere_independent_quadrature(radius,r,length):
    """Independent radial integration of spherical charge distribution.
    Integrand normalized by M. Appropriate for r>=radius.
    """
    positive(radius,r,length)
    if r<radius:raise ValueError('external field only')
    def f(s):
        if s==0:return 0.
        z=s/length
        return s*s*math.exp(-r/length)*(math.sinh(z)/z)
    if radius/length>400:raise ValueError('quadrature reference restricted to moderate source range')
    result,_=quad(f,0,radius,epsabs=1e-14,epsrel=1e-12)
    return 3*result/radius**3
