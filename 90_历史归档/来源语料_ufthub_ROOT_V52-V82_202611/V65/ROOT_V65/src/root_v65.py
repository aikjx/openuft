"""ROOT V65: mathematical audit tools, not an established four-force unification.

Standard library only. In helices, use v as an arbitrary speed; v=c is
mathematical, NOT the worldline of a massive particle.
G_ind is a model/scheme-dependent one-loop scalar example, not a prediction.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import pi, sin, cos, sqrt, exp, log, isfinite

C = 299792458.0
HBAR = 6.62607015e-34 / (2*pi)
G_CODATA_2022 = 6.67430e-11
G_STD_UNCERTAINTY = 0.00015e-11
EARTH_MASS = 5.9722e24  # illustrative nominal input, not precision geopotential
EARTH_RADIUS = 6.371e6
B_EQUATOR = 31.2e-6     # synthetic aligned-dipole toy, not an IGRF coefficient


def _finite(*x):
    if not all(isfinite(float(v)) for v in x):
        raise ValueError('nonfinite input')


def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def vadd(a,b): return tuple(x+y for x,y in zip(a,b))
def vmul(a,c): return tuple(x*c for x in a)
def norm(a): return sqrt(dot(a,a))


@dataclass(frozen=True)
class ReconstructedHelix:
    radius:float
    angular_rate:float
    axial_speed:float
    tangential_speed:float
    pitch_angle_rad:float
    curvature:float
    torsion:float
    speed:float

    def position(self, t):
        _finite(t)
        return (self.radius*cos(self.angular_rate*t),
                self.radius*sin(self.angular_rate*t), self.axial_speed*t)
    def velocity(self,t):
        a=self.angular_rate*t
        return (-self.tangential_speed*sin(a), self.tangential_speed*cos(a), self.axial_speed)
    def acceleration(self,t):
        a=self.angular_rate*t
        return (-self.radius*self.angular_rate**2*cos(a), -self.radius*self.angular_rate**2*sin(a), 0.)


def helix_from_curvature_torsion(kappa,tau,speed=1.):
    """Inverse Frenet for *circular* helix; κ>0, τ signed, v>0.

    R=κ/(κ²+τ²), omega=v sqrt(κ²+τ²),
    u=v τ/sqrt(κ²+τ²), vtheta=v κ/sqrt(κ²+τ²).
    Straight-line κ=0 has no unique radius/axis and is deliberately excluded.
    """
    _finite(kappa,tau,speed)
    if kappa<=0 or speed<=0:raise ValueError('kappa and speed must be positive')
    d=kappa*kappa+tau*tau
    if not isfinite(d) or d==0:raise ValueError('unrepresentable curvature')
    # atan2 assures correct handedness: signed torsion is physically a coordinate orientation.
    from math import atan2
    return ReconstructedHelix(kappa/d, speed*sqrt(d), speed*tau/sqrt(d),
                              speed*kappa/sqrt(d), atan2(tau,kappa), kappa, tau, speed)


def helix_from_radius_angle(radius, angle_rad, speed=1.):
    _finite(radius,angle_rad,speed)
    if radius<=0 or speed<=0 or not (-pi/2<angle_rad<pi/2):
        raise ValueError('R>0, v>0, angle in (-pi/2,pi/2)')
    return helix_from_curvature_torsion(cos(angle_rad)**2/radius,
                                       sin(angle_rad)*cos(angle_rad)/radius,speed)


def lorentz_interval(ct,x,y,z): return ct*ct-x*x-y*y-z*z

def boost_z(ct,x,y,z,beta):
    _finite(ct,x,y,z,beta)
    if abs(beta)>=1:raise ValueError('beta must be subluminal')
    gamma=1/sqrt((1-beta)*(1+beta))
    return (gamma*(ct-beta*z), x,y, gamma*(z-beta*ct))


def massive_proper_time_rate(v_over_c):
    _finite(v_over_c)
    if abs(v_over_c)>1:raise ValueError('superluminal worldline')
    return sqrt(max(0.,(1-v_over_c)*(1+v_over_c)))


def kg_group_velocity(k_z,q_r,mass_param=0.,c=C):
    """c*k/sqrt(k²+q²+mass_param²) for a relativistic KG mode;
    mass_param=m*c/hbar (inverse length), q_r transverse wavenumber.
    """
    _finite(k_z,q_r,mass_param,c)
    if q_r<0 or mass_param<0 or c<=0:raise ValueError('positive dispersion input required')
    den=sqrt(k_z*k_z+q_r*q_r+mass_param*mass_param)
    if den==0:raise ValueError('undefined massless zero mode')
    return c*k_z/den


def cutoff_length(energy_joules):
    _finite(energy_joules)
    if energy_joules<=0:raise ValueError('energy must be positive')
    return HBAR*C/energy_joules


def planck_length(g=G_CODATA_2022):
    _finite(g)
    if g<=0:raise ValueError('positive G')
    return sqrt(HBAR*g/C**3)


def induced_scalar_coefficient(N,xi,ell_m,mass_ratio=0.,bare_inverse_g=0.):
    """1/G_eff, SI, sharp proper-time regulator, N real scalars.
    mass_ratio = m_phys*c*ell/hbar. Running/higher order/other species omitted.
    """
    _finite(N,xi,ell_m,mass_ratio,bare_inverse_g)
    if int(N)!=N or N<=0 or ell_m<=0 or mass_ratio<0:raise ValueError('bad scalar EFT inputs')
    return (bare_inverse_g + N*(1-6*xi)*HBAR*cutoff_threshold(mass_ratio)/(12*pi*C**3*ell_m**2))


def cutoff_threshold(mu):
    """F(mu)=exp(-mu²)-mu² E1(mu²) = ∫_0^1 exp(-mu²/t)dt.

    Uses a convergent E1 series for mu<=1 and adaptive Simpson for mu>1;
    no SciPy runtime dependency. At mu=0 the continuous limit is 1.
    """
    _finite(mu)
    if mu<0:raise ValueError('mu>=0')
    if mu==0:return 1.
    if mu>30:return 0.
    x=mu*mu
    if x<=1:
        # E1(x)=-EulerGamma-ln(x)-sum_{k>=1} (-x)^k/(k*k!)
        summ=0.; term=1.
        for k in range(1,300):
            term*=(-x/k)
            add=term/k
            summ+=add
            if abs(add)<1e-16:break
        e1=-0.5772156649015328606-log(x)-summ
        return exp(-x)-x*e1
    # For x>1, smooth integrand supports highly accurate adaptive quadrature.
    def f(t):return 0. if t<=0 else exp(-x/t)
    def simp(a,b,fa,fb,fc):return (b-a)*(fa+4*fc+fb)/6
    def split(a,b,fa,fb,fc,whole,eps,depth):
        c=(a+b)/2;d=(a+c)/2;e=(c+b)/2
        fd=f(d);fe=f(e)
        l=simp(a,c,fa,fc,fd);r=simp(c,b,fc,fb,fe)
        if depth<=0 or abs(l+r-whole)<15*eps:
            return l+r+(l+r-whole)/15
        return (split(a,c,fa,fc,fd,l,eps/2,depth-1)+
                split(c,b,fc,fb,fe,r,eps/2,depth-1))
    fa,fb,fc=f(0),f(1),f(.5)
    return split(0,1,fa,fb,fc,simp(0,1,fa,fb,fc),1e-13,24)


def scalar_cutoff_rank_log_jacobian(N,ell):
    """Jacobian d log(N/ell²) / d(logN,logell) is rank 1 row (1,-2)."""
    _finite(N,ell)
    if N<=0 or ell<=0:raise ValueError('N,ell>0')
    return (1.,-2.)


def inverse_fit_cutoff(N,xi=0.,g_observed=G_CODATA_2022):
    """Algebraic reverse fit, not a first-principles G prediction."""
    _finite(N,xi,g_observed)
    if N<=0 or 1-6*xi<=0 or g_observed<=0:raise ValueError('positive induced correction required')
    return sqrt(N*(1-6*xi)*HBAR*g_observed/(12*pi*C**3))


def gravity_acceleration(r_xyz):
    """Point-mass spherical Earth toy; excludes oblateness/rotation/local anomalies."""
    r=norm(r_xyz)
    if r<EARTH_RADIUS:raise ValueError('outside Earth only')
    return vmul(r_xyz,-G_CODATA_2022*EARTH_MASS/r**3)


def toy_magnetic_field(r_xyz):
    """Centered, aligned dipole, B_equator at Earth radius. NOT IGRF!"""
    r=norm(r_xyz)
    if r<EARTH_RADIUS:raise ValueError('outside Earth only')
    n=vmul(r_xyz,1./r); cz=n[2]
    return vmul((3*cz*n[0],3*cz*n[1],3*cz*n[2]-1),B_EQUATOR*(EARTH_RADIUS/r)**3)


def test_body_force(r_xyz,v_xyz,mass_kg,charge_c,e_xyz=(0.,0.,0.)):
    _finite(mass_kg,charge_c,*r_xyz,*v_xyz,*e_xyz)
    if mass_kg<=0:raise ValueError('mass must be positive')
    g=gravity_acceleration(r_xyz)
    b=toy_magnetic_field(r_xyz)
    return vadd(vmul(g,mass_kg),vmul(vadd(e_xyz,cross(v_xyz,b)),charge_c))


def yukawa_shape(r,ell):
    _finite(r,ell)
    if r<0 or ell<=0:raise ValueError('r>=0, ell>0')
    u=r/ell
    return (1+u)*exp(-u) if u<700 else 0.


def eotvos_eta(alpha_a,alpha_b,r,ell):
    """η=2(a_A−a_B)/(a_A+a_B), a_i=g_N(1+α_i f(r/ell)).
    Simplified composition-dependent Yukawa surrogate, NOT a fit to MICROSCOPE.
    """
    _finite(alpha_a,alpha_b)
    f=yukawa_shape(r,ell)
    den=2+(alpha_a+alpha_b)*f
    if den<=0:raise ValueError('invalid acceleration denominator')
    return 2*(alpha_a-alpha_b)*f/den


MICROSCOPE_ETA=-1.5e-15
MICROSCOPE_STAT=2.3e-15
MICROSCOPE_SYST=1.5e-15

def microscope_interval(z=1.96):
    """Illustrative Gaussian combined-error interval, not collaboration CL product."""
    sigma=sqrt(MICROSCOPE_STAT**2+MICROSCOPE_SYST**2)
    return MICROSCOPE_ETA-z*sigma,MICROSCOPE_ETA+z*sigma
