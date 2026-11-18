"""ROOT V69: checked standard-physics benchmarks + explicitly hypothetical extensions.

Scope: Newtonian monopole, Earth's J2 (external), simplified layered spherical interior,
rotating observer, tidal acceleration, weak-field GR indicators, composition-coupled
Yukawa fifth-force *toy*. Not a unified field theory or precision ephemeris.
No numpy or external deps required.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import json, math

C = 299792458.0
G = 6.67430e-11  # CODATA 2022 value; measured, NOT derived
HBAR = 1.054571817e-34
EARTH_OMEGA = 7.292115e-5
AU = 149597870700.0
Z_A = {"H": (1, 1.008), "He":(2,4.0026), "C":(6,12.011),
       "O":(8,15.999), "Mg":(12,24.305), "Si":(14,28.085),
       "Fe":(26,55.845), "Ti":(22,47.867), "Pt":(78,195.084)}

@dataclass(frozen=True)
class Body:
    key: str
    name: str
    mass_kg: float
    mean_radius_m: float
    rotation_hours: float
    observed_g_approx: float
    classification: str = ""
    composition_label: str = ""
    color: str = "#7799bb"
    equatorial_radius_m: float|None = None
    polar_radius_m: float|None = None
    J2: float = 0.0
    GM_ref_m3_s2: float|None = None
    inertia_ratio: float = 0.4

    @property
    def mu(self):
        # One must not use the published mass + published GM as independent G evidence.
        return self.GM_ref_m3_s2 if self.GM_ref_m3_s2 is not None else G*self.mass_kg

    @property
    def density(self):
        return self.mass_kg/(4/3*math.pi*self.mean_radius_m**3)

    @property
    def omega(self):
        return 0.0 if self.rotation_hours==0 else 2*math.pi/(self.rotation_hours*3600)


def load_bodies(path: Path|None=None) -> dict[str,Body]:
    if path is None: path=Path(__file__).resolve().parents[1]/'data/bodies.json'
    raw=json.loads(Path(path).read_text(encoding='utf-8'))
    return {row['key']: Body(**row) for row in raw['bodies']}


def norm(v): return math.sqrt(sum(x*x for x in v))
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def mul(s,a): return tuple(s*x for x in a)
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])


def point_accel(mu:float, r:tuple[float,float,float]):
    rr=norm(r)
    if rr<=0: raise ValueError('point-mass acceleration undefined at origin')
    return mul(-mu/rr**3,r)


def point_potential(mu:float, r):
    rr=norm(r)
    if rr<=0: raise ValueError('point-mass potential undefined at origin')
    return -mu/rr


def j2_potential(body:Body, r):
    """External geocentric potential. Body must have nonzero J2 and equatorial radius."""
    rr=norm(r)
    a=body.equatorial_radius_m or body.mean_radius_m
    if rr < a*0.99: raise ValueError('external J2 not appropriate deep inside body')
    return -body.mu/rr*(1-body.J2*(a/rr)**2*(3*(r[2]/rr)**2-1)/2)


def j2_accel(body:Body, r):
    """External acceleration -grad Phi for degree-2 zonal harmonic, axis along +z."""
    rr=norm(r); a=body.equatorial_radius_m or body.mean_radius_m
    if rr < a*0.99: raise ValueError('external J2 not appropriate deep inside body')
    z2=(r[2]/rr)**2
    k=1.5*body.J2*(a/rr)**2
    cxy=-body.mu/rr**3*(1-k*(5*z2-1))
    cz=-body.mu/rr**3*(1-k*(5*z2-3))
    return (cxy*r[0],cxy*r[1],cz*r[2])


def ecef_geodetic_earth(lat_deg:float, lon_deg:float=0., altitude_m:float=0., body:Body|None=None):
    b=body or load_bodies()['Earth']
    if b.equatorial_radius_m is None or b.polar_radius_m is None: raise ValueError('requires oblate Earth-like ellipsoid')
    if not (-90<=lat_deg<=90 and math.isfinite(altitude_m) and altitude_m>=0):
        raise ValueError('latitude [-90,90] altitude >=0')
    a,bb=b.equatorial_radius_m,b.polar_radius_m
    e2=1-(bb/a)**2; p=math.radians(lat_deg);l=math.radians(lon_deg)
    N=a/math.sqrt(1-e2*math.sin(p)**2)
    return ((N+altitude_m)*math.cos(p)*math.cos(l),
            (N+altitude_m)*math.cos(p)*math.sin(l),
            (N*(1-e2)+altitude_m)*math.sin(p))


def centrifugal_accel(omega:float,r): return (omega*omega*r[0],omega*omega*r[1],0.)


def coriolis_accel(omega:float,v_rot):
    return mul(-2.,cross((0.,0.,omega),v_rot))


def earth_surface_field(lat_deg:float,alt_m:float=0,lon_deg:float=0., include_J2:bool=True, rotating_frame:bool=True):
    b=load_bodies()['Earth'];r=ecef_geodetic_earth(lat_deg,lon_deg,alt_m,b)
    g=j2_accel(b,r) if include_J2 else point_accel(b.mu,r)
    eff=add(g,centrifugal_accel(EARTH_OMEGA,r)) if rotating_frame else g
    radial=mul(1/norm(r),r)
    # magnitude not identical to radial component on an oblate/rotating Earth
    return {'r_m':norm(r),'g_gravity_m_s2':norm(g),'g_effective_m_s2':norm(eff),
            'gravity_vector_m_s2':g,'effective_vector_m_s2':eff,
            'gravity_radial_m_s2':-dot(g,radial),'effective_radial_m_s2':-dot(eff,radial)}


def surface_stats(b:Body):
    r=b.mean_radius_m
    return {'key':b.key,'name':b.name,'mass_kg':b.mass_kg,'mean_radius_m':r,
        'mean_density_kg_m3':b.density,'g_spherical_m_s2':b.mu/r**2,
        'v_escape_m_s':math.sqrt(2*b.mu/r),'v_circular_m_s':math.sqrt(b.mu/r),
        'v_equatorial_rotation_m_s':abs(b.omega)*r,'centrifugal_equator_m_s2':b.omega**2*r,
        'compactness_rs_over_R':2*b.mu/(C*C*r),
        'redshift_schwarzschild_static_approx':math.sqrt(max(0,1-2*b.mu/(C*C*r))),
        'observed_g_approx':b.observed_g_approx}


@dataclass(frozen=True)
class Shell:
    r_outer:float
    density:float

class LayeredSphere:
    def __init__(self,shells:Iterable[Shell]):
        self.shells=tuple(shells)
        if not self.shells or self.shells[0].r_outer<=0: raise ValueError('invalid shells')
        if any(x.density<=0 for x in self.shells):raise ValueError('densities positive')
        if any(self.shells[i].r_outer<=self.shells[i-1].r_outer for i in range(1,len(self.shells))):raise ValueError('outer radii ascending')

    @property
    def radius(self):return self.shells[-1].r_outer

    def enclosed_mass(self,r:float):
        if r<0 or not math.isfinite(r):raise ValueError('invalid r')
        m=0.;a=0.
        for shell in self.shells:
            b=min(max(r,a),shell.r_outer)
            m+=4*math.pi/3*shell.density*(b**3-a**3)
            a=shell.r_outer
        return m

    @property
    def mass(self):return self.enclosed_mass(self.radius)

    def accel(self,r:float):
        if r<0:raise ValueError('r>=0')
        if r==0:return 0.
        return G*self.enclosed_mass(r)/r**2

    def density_at(self,r:float):
        if r<0:raise ValueError('r>=0')
        for shell in self.shells:
            if r<=shell.r_outer:return shell.density
        return 0.

    def hydrostatic_pressure(self, n:int=5000):
        """Integrate dP/dr=-rho*g from R to 0 for chosen NON-EOS mass profile."""
        if n<=0:raise ValueError('n positive')
        dr=self.radius/n;p=0.
        for i in range(n):
            r=self.radius-(i+0.5)*dr
            p+=self.density_at(r)*self.accel(r)*dr
        return p


def earth_toy_layers(earth:Body|None=None):
    """Piecewise constant densities renormalized to Earth mass; NOT PREM."""
    b=earth or load_bodies()['Earth']
    rad=b.mean_radius_m
    sh=[Shell(1221.5e3,13000),Shell(3480e3,11000),
        Shell(5701e3,4900),Shell(rad,3300)]
    model=LayeredSphere(sh);scale=b.mass_kg/model.mass
    return LayeredSphere([Shell(s.r_outer,s.density*scale) for s in sh])


def uniform_sphere_accel(m:float,R:float,r:float):
    if m<=0 or R<=0 or r<0:raise ValueError('invalid sphere')
    return G*m*r/R**3 if r<=R else G*m/r**2


def density_gravity(rho:float,R:float):
    if rho<=0 or R<=0:raise ValueError('rho,R positive')
    return 4*math.pi*G*rho*R/3


def tidal_relative_accel(mu_ext:float, center_to_ext, r_local):
    """External point-source acceleration at offset minus acceleration at center."""
    u=sub(center_to_ext,r_local)
    if min(norm(u),norm(center_to_ext))<=0:raise ValueError('overlap with external point')
    return sub(mul(mu_ext/norm(u)**3,u), mul(mu_ext/norm(center_to_ext)**3,center_to_ext))


def lense_thirring_precession(body:Body,r_vec):
    r=norm(r_vec)
    if r<=0:raise ValueError('r>0')
    J=body.inertia_ratio*body.mass_kg*body.mean_radius_m**2*body.omega
    n=mul(1/r,r_vec);jv=(0.,0.,J)
    return mul(G/(C*C*r**3),sub(mul(3*dot(jv,n),n),jv))


def z_over_a(element:str):
    z,a=Z_A[element];return z/a


def yukawa_factor(r:float,lam:float):
    if r<0 or lam<=0:raise ValueError('r>=0 lambda>0')
    return (1+r/lam)*math.exp(-r/lam)


def yukawa_accel(mu:float,r:float,alpha:float,charge_source:float,charge_test:float,lam:float):
    if r<=0:raise ValueError('r>0')
    return mu/r**2*(1+alpha*charge_source*charge_test*yukawa_factor(r,lam))


def eotvos_yukawa(r:float,lam:float,alpha:float,charge_source:float=0.49,
                  charge_A:float|None=None,charge_B:float|None=None):
    qa=z_over_a('Ti') if charge_A is None else charge_A
    qb=z_over_a('Pt') if charge_B is None else charge_B
    f=yukawa_factor(r,lam)
    a=1+alpha*charge_source*qa*f
    b=1+alpha*charge_source*qb*f
    return 2*(a-b)/(a+b)


def alpha_bound_toy(eta_bound:float,charge_source:float=0.49,
                    charge_A:float|None=None,charge_B:float|None=None):
    qa=z_over_a('Ti') if charge_A is None else charge_A
    qb=z_over_a('Pt') if charge_B is None else charge_B
    return eta_bound/(abs(charge_source)*abs(qa-qb))


def gravitational_energy_eV(mass_kg:float,height_m:float,g:float=9.81):
    return mass_kg*g*height_m/1.602176634e-19


def gravitational_redshift_fraction(g:float,height_m:float):
    """Weak field, small constant-g altitude difference"""
    return g*height_m/C**2


def helix(radius:float,angle_degrees:float,speed:float=C):
    if radius<=0 or speed<=0 or abs(angle_degrees)>90:raise ValueError('invalid helix')
    l=math.radians(angle_degrees)
    cs=0. if abs(angle_degrees)==90 else math.cos(l)
    sn=math.sin(l)
    omega=speed*cs/radius
    return {'omega':omega,'axial_speed':speed*sn,'transverse_speed':speed*cs,
            'curvature':cs*cs/radius,'torsion':cs*sn/radius,
            'acceleration':speed*speed*cs*cs/radius}


def dimension_G_obstruction():
    # c^a hbar^b: M=b=-1, L=a+2b=3 =>a=5; T=-(a+b)=-2 => a+b=2, but 4!=2
    return {'a':5,'b':-1,'a_plus_b_derived':4,'a_plus_b_required':2,'constructible':False}


def gm_degeneracy(g:float,m:float,k:float):
    if k<=0: raise ValueError('k positive')
    return ((g*k)*(m/k))/(g*m)



def orbital_energy_per_mass(r, v, mu:float):
    rr=norm(r)
    if rr<=0 or mu<=0: raise ValueError('valid r and mu')
    return 0.5*dot(v,v)-mu/rr


def kepler_verlet_step(r,v,mu:float,dt:float):
    """Second-order symplectic velocity Verlet; central Newtonian point field only.
    This is not a GR, N-body, J2, dissipative or stochastic integrator.
    """
    if mu<=0 or not math.isfinite(dt):raise ValueError('invalid mu/dt')
    a=point_accel(mu,r)
    rn=add(add(r,mul(dt,v)),mul(0.5*dt*dt,a))
    an=point_accel(mu,rn)
    vn=add(v,mul(0.5*dt,add(a,an)))
    return rn,vn


def earth_tidal_gradient_radial(mu:float,r:float,length:float):
    if r<=0 or length<0:raise ValueError('invalid r/length')
    return 2*mu*length/r**3


def source_energy_density_from_field(E:float=0.,B:float=0.):
    eps0=8.8541878188e-12
    mu0=1/(eps0*C*C)
    return 0.5*(eps0*E*E+B*B/mu0)
