"""ROOT V84. SI reference physics. ALL observations generated elsewhere are synthetic.
No controls for real instruments. This is not a discovery of new gravity.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import cosh, sinh, exp, sqrt, isfinite
G_REF = 6.67430e-11  # m3 kg-1 s-2, CODATA 2022
G_UNCERTAINTY = 1.5e-15  # standard uncertainty, absolute
C_LIGHT = 299792458.0
G_EARTH_REF = 9.80665

@dataclass(frozen=True)
class Rig:
    mass_kg: float = 100.0
    half_baseline_m: float = 0.10
    source_radius_m: float = 0.12
    def validate(self, distance_m=None):
        if not all(isfinite(z) and z > 0 for z in (self.mass_kg,self.half_baseline_m,self.source_radius_m)):
            raise ValueError('positive finite rig parameters required')
        if distance_m is not None:
            if not isfinite(distance_m) or distance_m <= self.half_baseline_m + self.source_radius_m:
                raise ValueError('both sensors must lie outside source sphere')


def sphere_newton_acceleration(x_sensor, x_source, mass_kg, sphere_radius_m):
    if mass_kg < 0 or sphere_radius_m <= 0: raise ValueError('invalid mass or radius')
    dx=x_source-x_sensor
    rr=abs(dx)
    if rr==0: return 0.0
    if rr>=sphere_radius_m: return G_REF*mass_kg*dx/rr**3
    # Uniform sphere interior, acceleration points toward sphere center
    return G_REF*mass_kg*dx/sphere_radius_m**3


def gravity_readings(rig:Rig, d:float, side:int):
    rig.validate(d)
    if side not in (-1,1): raise ValueError('side must be +/- 1')
    xs=(-rig.half_baseline_m,rig.half_baseline_m)
    vals=[sphere_newton_acceleration(x,side*d,rig.mass_kg,rig.source_radius_m) for x in xs]
    return {'left':vals[0], 'right':vals[1], 'common':sum(vals)/2,
            'gradient':(vals[1]-vals[0])/(2*rig.half_baseline_m)}


def common_amplitude(rig:Rig,d:float):
    rig.validate(d)
    s=rig.half_baseline_m
    return G_REF*rig.mass_kg/2*((d-s)**-2+(d+s)**-2)


def even_gradient(rig:Rig,d:float):
    rig.validate(d)
    s=rig.half_baseline_m
    return G_REF*rig.mass_kg/(2*s)*((d-s)**-2-(d+s)**-2)


def partials_common(rig:Rig,d:float):
    rig.validate(d);s=rig.half_baseline_m; gm=G_REF*rig.mass_kg
    return {'mass_kg':common_amplitude(rig,d)/rig.mass_kg,
            'distance_m':-gm*((d-s)**-3+(d+s)**-3),
            'half_baseline_m':gm*((d-s)**-3-(d+s)**-3)}


def yukawa_form_factor(x:float):
    """Uniform sphere F(x) = 3(x cosh x - sinh x)/x^3; small x series."""
    if not isfinite(x) or x<0: raise ValueError('x nonnegative finite')
    if x<0.02:
        return 1 + x*x/10 + x**4/280 + x**6/15120
    if x>690: raise OverflowError('use yukawa_kernel_product for large x')
    return 3*(x*cosh(x)-sinh(x))/(x*x*x)


def yukawa_kernel_product(source_radius:float, r:float, lam:float):
    """Stable F(a/lambda)*exp(-r/lambda) for external point r>=a."""
    if not all(isfinite(z) for z in (source_radius,r,lam)) or source_radius<=0 or lam<=0 or r<source_radius:
        raise ValueError('requires 0<a<=r and lambda>0')
    x=source_radius/lam
    if x<0.02: return yukawa_form_factor(x)*exp(-r/lam)
    return 1.5/(x**3)*((x-1)*exp(-(r-source_radius)/lam)+(x+1)*exp(-(r+source_radius)/lam))


def yukawa_amplitude_per_alpha(rig:Rig,d:float,lam:float):
    """Yukawa correction amplitude for alpha=1 for uniform sphere, external points."""
    rig.validate(d)
    if lam<=0: raise ValueError('positive range needed')
    s=rig.half_baseline_m
    out=0.0
    for rr in (d-s,d+s):
        out+=G_REF*rig.mass_kg/2 /rr**2*(1+rr/lam)*yukawa_kernel_product(rig.source_radius_m,rr,lam)
    return out


def source_geometry_uncertainty(rig:Rig,d:float,mass_sigma=.05,d_sigma=.001,baseline_sigma=.0002,tilt_sigma=2e-10):
    """RSS first-order budget under independence; baseline_sigma is full separation uncertainty."""
    p=partials_common(rig,d)
    terms={'mass':p['mass_kg']*mass_sigma,
           'distance':p['distance_m']*d_sigma,
           'baseline':p['half_baseline_m']*baseline_sigma/2,
           'tilt':G_EARTH_REF*tilt_sigma,
           'reference_G':common_amplitude(rig,d)*G_UNCERTAINTY/G_REF}
    return {'terms_m_s2':terms,'rss_m_s2':sqrt(sum(v*v for v in terms.values())),'relative_rss':sqrt(sum(v*v for v in terms.values()))/common_amplitude(rig,d)}


def em_stored_energy(B_tesla:float, volume_m3:float,mu0=1.25663706127e-6):
    if not all(isfinite(z) for z in (B_tesla,volume_m3,mu0)) or volume_m3<=0 or mu0<=0: raise ValueError('invalid EM inputs')
    return B_tesla**2*volume_m3/(2*mu0)


def net_added_mass_kg(energy_j:float):return energy_j/C_LIGHT**2
