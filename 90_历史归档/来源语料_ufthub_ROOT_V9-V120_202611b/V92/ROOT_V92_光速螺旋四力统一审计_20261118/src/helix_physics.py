"""ROOT V92: falsifiable 3-D helix kinematics, SR dynamics, dimensions.
No implementation here constitutes a new law or establishes four-force unification.
CODATA 2022 reference values; h, c, e exact in SI, G/me measured.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
from typing import Dict

C = 299792458.0
H = 6.62607015e-34
HBAR = H / (2 * math.pi)
E_CHARGE = 1.602176634e-19
M_E = 9.1093837139e-31  # CODATA 2022
G = 6.67430e-11


@dataclass(frozen=True)
class Helix:
    radius: float  # metres
    omega: float   # signed radians per second
    p: float       # axial speed metres per second

    def __post_init__(self):
        if self.radius <= 0 or self.omega == 0 or not all(map(math.isfinite, (self.radius,self.omega,self.p))):
            raise ValueError('non-degenerate helix requires finite radius>0, omega !=0')

    @property
    def v_perp(self):
        return abs(self.radius * self.omega)

    @property
    def speed(self):
        return math.hypot(self.radius * self.omega, self.p)

    @property
    def kappa(self):
        return self.radius * self.omega**2 / self.speed**2

    @property
    def tau(self):
        return self.p * self.omega / self.speed**2

    @property
    def frequency(self):
        return abs(self.omega)/(2*math.pi)

    def gamma(self):
        if self.speed >= C:
            raise ValueError('massive-particle gamma is undefined at or beyond c')
        return 1 / math.sqrt((1-self.speed/C)*(1+self.speed/C))

    def location(self,t):
        return (self.radius*math.cos(self.omega*t),self.radius*math.sin(self.omega*t),self.p*t)

    def velocity(self,t):
        return (-self.radius*self.omega*math.sin(self.omega*t),self.radius*self.omega*math.cos(self.omega*t),self.p)

    def acceleration(self,t):
        return (-self.radius*self.omega**2*math.cos(self.omega*t), -self.radius*self.omega**2*math.sin(self.omega*t),0.0)

    def transformed_axial_boost(self,u):
        """Exact SR Lorentz boost along helix axis, |u|<c.
        t' = gamma_u*(1-u*p/c²)t; z' = gamma_u*(p-u)t
        """
        if abs(u)>=C: raise ValueError('|boost| must be below c')
        gb = 1/math.sqrt((1-u/C)*(1+u/C))
        factor = gb*(1-u*self.p/C**2)
        return Helix(self.radius,self.omega/factor,(self.p-u)/(1-u*self.p/C**2))


def helix_from_kappa_tau_speed(kappa,tau,v):
    if kappa<=0 or v<=0 or not all(map(math.isfinite,(kappa,tau,v))):
        raise ValueError('kappa,v must positive finite')
    magnitude = math.hypot(kappa,tau)
    omega=v*magnitude
    radius=kappa/magnitude**2
    p=v*tau/magnitude
    return Helix(radius,omega,p)


def cyclotron_helix(B, beta, pitch_angle_deg, mass=M_E, charge=E_CHARGE):
    """Uniform B along z, no E; initial v_perp = v cos(angle), v_parallel=v sin(angle).
    Uses B magnitude and |charge|; handedness may be encoded separately.
    """
    if B<=0 or mass<=0 or charge==0 or not (0<beta<1): raise ValueError('invalid massive-particle parameters')
    a=math.radians(pitch_angle_deg)
    if abs(math.cos(a))<1e-12: raise ValueError('parallel straight path has undefined helix curvature/torsion')
    v=beta*C
    gamma=1/math.sqrt((1-beta)*(1+beta))
    omega=abs(charge)*B/(gamma*mass)
    return Helix(v*abs(math.cos(a))/omega,omega,v*math.sin(a))


def lorentz_force_magnitude_constant_speed(mass,helix):
    """Magnitude of transverse lab 3-force for massive constant-speed helix."""
    return helix.gamma()*mass*helix.speed**2*helix.kappa


def magnetic_force(B,helix,charge=E_CHARGE):
    """Independent Lorentz force q v×B (magnitude, B axial)."""
    return abs(charge)*helix.v_perp*B


def field_inferred_from_helix(helix, mass=M_E, charge=E_CHARGE):
    """Only valid AFTER assuming relativistic charge in uniform axial B."""
    return helix.gamma()*mass*helix.speed*math.hypot(helix.kappa,helix.tau)/abs(charge)


def massless_free_helix_violation(helix):
    """Acceleration magnitude; nonzero means not an affine straight Minkowski null geodesic."""
    return helix.radius*helix.omega**2


def dimension_dict():
    """SI base dimensions (M,L,T,I). Angle in rad dimensionless."""
    return {
        'mass m': (1,0,0,0),
        'length R':(0,1,0,0), 'time t':(0,0,1,0),
        'speed v, c, p':(0,1,-1,0),
        'angular frequency omega':(0,0,-1,0),
        'frequency f':(0,0,-1,0),
        'curvature kappa':(0,-1,0,0),
        'torsion tau':(0,-1,0,0),
        'acceleration a':(0,1,-2,0),
        'force F':(1,1,-2,0),
        'energy E':(1,2,-2,0),
        'angular momentum J / hbar':(1,2,-1,0),
        'G':(-1,3,-2,0),
        'charge q':(0,0,1,1),
        'current I':(0,0,0,1),
        'electric field Efield':(1,1,-3,-1),
        'magnetic field Bfield':(1,0,-2,-1),
        'permittivity epsilon0':(-1,-3,4,2),
        'permeability mu0':(1,1,-2,-2),
        'scalar potential Phi':(0,2,-2,0),
        'GR Riemann curvature':(0,-2,0,0),
        'field energy density':(1,-1,-2,0),
        'stress-energy tensor (SI)':(1,-1,-2,0),
        'Einstein tensor Gmunu':(0,-2,0,0),
        'coupling q/m':(-1,0,1,1),
        'Planck length squared':(0,2,0,0),
    }


def dimensional_product(*args):
    return tuple(sum(a[i] for a in args) for i in range(4))


def dimensional_power(vec,power):
    return tuple(k*power for k in vec)


def check_dimensions():
    D=dimension_dict()
    return {
        'v=R omega': D['speed v, c, p']==dimensional_product(D['length R'],D['angular frequency omega']),
        'omega=v kappa': D['angular frequency omega']==dimensional_product(D['speed v, c, p'],D['curvature kappa']),
        'accel=v² kappa': D['acceleration a']==dimensional_product(dimensional_power(D['speed v, c, p'],2),D['curvature kappa']),
        'force=m v² kappa':D['force F']==dimensional_product(D['mass m'],dimensional_power(D['speed v, c, p'],2),D['curvature kappa']),
        'energy=hbar omega':D['energy E']==dimensional_product(D['angular momentum J / hbar'],D['angular frequency omega']),
        'G=c³/(hbar kappa²)':D['G']==dimensional_product(dimensional_power(D['speed v, c, p'],3),dimensional_power(D['angular momentum J / hbar'],-1),dimensional_power(D['curvature kappa'],-2)),
        'Einstein source=G T /c4': D['Einstein tensor Gmunu']==dimensional_product(D['G'], D['stress-energy tensor (SI)'], dimensional_power(D['speed v, c, p'],-4)),
        'Lorentz force=q v B':D['force F']==dimensional_product(D['charge q'],D['speed v, c, p'],D['magnetic field Bfield']),
        'electric force=q Efield':D['force F']==dimensional_product(D['charge q'],D['electric field Efield']),
        'energy density Efield² epsilon0': D['field energy density']==dimensional_product(dimensional_power(D['electric field Efield'],2),D['permittivity epsilon0']),
        'energy density Bfield²/mu0': D['field energy density']==dimensional_product(dimensional_power(D['magnetic field Bfield'],2),dimensional_power(D['permeability mu0'],-1)),
        'Riemann curvature ~ kappa²':D['GR Riemann curvature']==dimensional_power(D['curvature kappa'],2),
    }


def scale_from_assumed_kappa(kappa):
    """Dimensional construction ONLY; not a prediction of G!"""
    return C**3/(HBAR*kappa*kappa)


def reproduce_constants_example():
    return {'c':C,'h':H,'hbar':HBAR,'me':M_E,'e':E_CHARGE,'G_INPUT':G,
            'planck_length_FROM_MEASURED_G':math.sqrt(HBAR*G/C**3),
            'planck_mass_FROM_MEASURED_G':math.sqrt(HBAR*C/G),
            'electron_compton_radius':HBAR/(M_E*C)}
