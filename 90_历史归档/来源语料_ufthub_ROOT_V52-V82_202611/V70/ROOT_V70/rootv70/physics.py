"""ROOT V70: conventional physics baselines and explicitly hypothetical tests.
Units SI unless stated. Geocentric spherical approximations; not precision ephemerides.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import pi, exp, sqrt, sin, cos
from typing import Tuple
import numpy as np

G = 6.67430e-11  # CODATA 2022 central value, SI
C = 299792458.0
HBAR = 1.054571817e-34
EARTH_MU = 3.986004418e14
EARTH_A = 6378137.0
EARTH_J2 = 1.08263e-3
EARTH_OMEGA = 7.292115e-5

@dataclass(frozen=True)
class Body:
    name: str
    mass: float
    radius: float
    spin_hours: float
    source_charge_toy: float
    j2: float = 0.0
    gm_override: float | None = None
    @property
    def mu(self): return self.gm_override if self.gm_override is not None else G*self.mass
    @property
    def omega(self): return 2*pi/(self.spin_hours*3600) if self.spin_hours else 0.0
    @property
    def density(self): return 3*self.mass/(4*pi*self.radius**3)
    @property
    def g(self): return self.mu/self.radius**2

# Approximate NASA Planetary Fact Sheet masses/diameters/spin periods. Moon included;
# Earth GM/radius/J2/omega from IERS. Venus retrograde negative spin period.
# Source charges are ARBITRARY dimensionless demonstration inputs, NOT physical charges.
BODIES = {
    'Mercury': Body('Mercury', 0.330e24, 4879e3/2, 1407.6, .50),
    'Venus': Body('Venus', 4.87e24, 12104e3/2, -5832.5, .36),
    'Earth': Body('Earth', 5.9722e24, EARTH_A, 23.9344696, .45, EARTH_J2, EARTH_MU),
    'Moon': Body('Moon', 0.073e24, 3475e3/2, 655.7, .27),
    'Mars': Body('Mars', 0.642e24, 6792e3/2, 24.6, .32),
    'Jupiter': Body('Jupiter', 1898e24, 142984e3/2, 9.9, .13),
    'Saturn': Body('Saturn', 568e24, 120536e3/2, 10.7, .16),
    'Uranus': Body('Uranus', 86.8e24, 51118e3/2, -17.2, .19),
    'Neptune': Body('Neptune', 102e24, 49528e3/2, 16.1, .20),
}

# Arbitrary mathematical composition surrogate Q_A; no connection to actual nuclear physics.
MATERIAL_TOY = {'Ti':0.18,'Pt':0.67,'Al':0.32,'SiO2':0.24,'Fe':0.40}

def norm(v): return float(np.linalg.norm(v))

def gravity_central(mu:float, pos) -> np.ndarray:
    p=np.asarray(pos,dtype=float); r=norm(p)
    if r<=0: raise ValueError('r must be positive')
    return -mu*p/r**3

def gravitational_potential_j2(body:Body, pos) -> float:
    p=np.asarray(pos,dtype=float); r=norm(p)
    if r<=0: raise ValueError('r must be positive')
    z_over_r=p[2]/r
    p2=.5*(3*z_over_r*z_over_r-1)
    return -body.mu/r * (1-body.j2*(body.radius/r)**2*p2)

def gravity_j2(body:Body,pos)->np.ndarray:
    p=np.asarray(pos,dtype=float);r=norm(p)
    if r<=0: raise ValueError('r must be positive')
    x,y,z=p;s=z*z/(r*r)
    factor=1.5*body.j2*body.mu*body.radius**2/r**5
    correction=factor*np.array([x*(5*s-1),y*(5*s-1),z*(5*s-3)])
    return -body.mu*p/r**3+correction

def rotating_apparent(body:Body,pos,vel_rot=(0,0,0))->np.ndarray:
    """Centrifugal + Coriolis in a body-fixed rotating frame. No frame-dragging."""
    omega=np.array([0.,0.,body.omega]); p=np.asarray(pos,dtype=float)
    v=np.asarray(vel_rot,dtype=float)
    return -np.cross(omega,np.cross(omega,p))-2*np.cross(omega,v)

def field_at(body:Body,lat_deg:float,alt:float=0.0):
    if alt<0: raise ValueError('model intended exterior: alt>=0')
    lat=np.deg2rad(lat_deg);r=body.radius+alt
    pos=np.array([r*cos(lat),0.,r*sin(lat)])
    a=gravity_j2(body,pos)
    rot=rotating_apparent(body,pos)
    return {'radius':r,'pos':pos,'gravity_vec':a,'gravity':norm(a),
            'rotation_vec':rot,'effective_vec':a+rot,'effective':norm(a+rot),
            'tidal_radial':2*body.mu/r**3,
            'potential_per_mass':-body.mu/r,
            'redshift_per_meter':body.mu/(r*r*C*C),
            'kretschmann':48*(body.mu/C**2)**2/r**6}

def enclosed_mass_piecewise(r:float,shell_radii, shell_densities)->float:
    """Piecewise uniform spherical shell density; shell radii increasing, in meters."""
    rs=np.asarray(shell_radii,float); ds=np.asarray(shell_densities,float)
    if len(rs)==0 or len(rs)!=len(ds) or np.any(np.diff(rs)<=0) or np.any(ds<0):
        raise ValueError('bad shells')
    if r<0: raise ValueError('negative r')
    inner=0.; mass=0.
    for outer,density in zip(rs,ds):
        stop=min(r,outer)
        if stop>inner:
            mass+=(4*pi/3)*density*(stop**3-inner**3)
        if r<=outer:break
        inner=outer
    return float(mass)

def gravity_piecewise(r:float,shell_radii,shell_densities)->float:
    if r<0: raise ValueError('negative r')
    if r==0:return 0.0
    return G*enclosed_mass_piecewise(r,shell_radii,shell_densities)/r**2

def yukawa_shape(r:float, lam:float)->float:
    """Point-source Yukawa acceleration relative shape, r,lam>0."""
    if r<=0 or lam<=0:raise ValueError('r,lambda positive')
    x=r/lam
    return (1+x)*exp(-x)

def toy_acceleration(body:Body,mat:str,lat=0.,alt=0., strength=0.,lam=1e7)->float:
    """Toy point-source scalar coupling alpha_A=strength*Q_A, alpha_S=Q_S.
    Not a claim about true materials; acceleration magnitude excludes rotation.
    """
    r=body.radius+alt
    return body.mu/r**2*(1+strength*MATERIAL_TOY[mat]*body.source_charge_toy*yukawa_shape(r,lam))

def eotvos(a:float,b:float)->float:
    return 2*(a-b)/(a+b)

def local_boost_kinematics(v:float)->tuple[float,float]:
    """gamma and dτ/dt for timelike worldline in flat space."""
    if abs(v)>=C:raise ValueError('massive-body worldline requires |v|<c')
    gamma=1./sqrt(1-(v/C)**2)
    return gamma,1/gamma

def gravity_clock_shift(body:Body,height:float)->float:
    """Weak-field redshift between radius R and R+h; neglect rotation/velocity."""
    if height<0:raise ValueError('positive height only')
    return (body.mu*height)/(C*C*body.radius*(body.radius+height))

def curvature_length_effect(body:Body,ell:float)->float:
    """Dimensionless toy K*ell^4, not an observed effective interaction."""
    if ell<0:raise ValueError('length >= 0')
    return field_at(body,0)['kretschmann']*ell**4

def helix_kinematics(R:float,omega:float,u:float):
    v=sqrt((R*omega)**2+u**2)
    if R<=0 or v<=0:raise ValueError('R,v must >0')
    return {'v':v,'curvature':R*omega**2/v**2,
            'torsion':u*omega/v**2,
            'acceleration':R*omega**2,'axial_fraction':u/v}
