"""ROOT V72: established comparisons and explicitly hypothetical discriminants."""
from dataclasses import dataclass
from math import sqrt, cos
C=299792458.0
HBAR=1.054571817e-34
G=6.67430e-11 # Measured CODATA input, NEVER a ROOT prediction
EARTH_M=5.9722e24
EARTH_R=6.371e6
EARTH_OMEGA=7.292115e-5
@dataclass(frozen=True)
class Helix:
    radius:float
    omega:float
    axial:float
    @property
    def speed(self):return sqrt((self.radius*self.omega)**2+self.axial**2)
    @property
    def curvature(self):return self.radius*self.omega**2/self.speed**2
    @property
    def torsion(self):return self.axial*self.omega/self.speed**2
    @property
    def acceleration(self):return self.radius*self.omega**2

def gravity(mass,radius):
    if mass<=0 or radius<=0:raise ValueError('positive mass/radius required')
    return G*mass/radius**2

def tidal_gradient(mass,radius):return 2*G*mass/radius**3

def centrifugal(omega,radius,latitude=0.):return omega**2*radius*cos(latitude)

def rot_energy_ratio_uniform(radius,omega):return (radius*omega/C)**2/5

def redshift(g,dh):return g*dh/C**2

def electric_force(charge,E):return tuple(charge*x for x in E)

def dimension_no_go():
    # Suppose [G]=L^3 M^-1 T^-2; [c]=LT^-1; [hbar]=ML^2T^-1.
    # mass b=-1; time a+b=2 => a=3; length a+2b=1 != 3
    return dict(a=3,b=-1,length_predicted=1,length_required=3)

def hypothetical_feature(chi,q_delta,omega_dot_g,omega_ref,g_ref):
    if omega_ref<=0 or g_ref<=0:raise ValueError('positive normalization')
    return chi*q_delta*omega_dot_g/(omega_ref*g_ref)

PLANETS=[('太阳',1.9885e30,6.9634e8,2.865e-6),('地球',EARTH_M,EARTH_R,EARTH_OMEGA),('月球',7.342e22,1.7374e6,2.6617e-6),('火星',6.4171e23,3.3895e6,7.0882e-5),('木星',1.89813e27,6.9911e7,1.7585e-4)]
def environments():
    return [dict(body=n,mass_kg=m,radius_m=r,omega_rad_s=w,g_m_s2=gravity(m,r),centrifugal_m_s2=centrifugal(w,r),tidal_s_minus2=tidal_gradient(m,r),rot_energy_ratio_ideal=rot_energy_ratio_uniform(r,w)) for n,m,r,w in PLANETS]
