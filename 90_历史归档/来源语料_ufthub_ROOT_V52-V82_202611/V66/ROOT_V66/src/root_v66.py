"""ROOT V66: auditable mathematics and toy models, not a proof of GUT.

All constants from CODATA 2022 (published 2025), where identified.
Toy fifth-force and induction formulas are model-dependent, not observations.
No third-party dependencies for core calculations.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import atan2, cos, exp, isfinite, log, pi, sin, sqrt

C = 299_792_458.0
H = 6.62607015e-34
HBAR = H / (2*pi)
E = 1.602176634e-19
G = 6.67430e-11
EPS0 = 8.8541878188e-12
ALPHA_2022 = 7.2973525643e-3
MASS_RATIO_2022 = 1836.152673426
EARTH_MASS = 5.9722e24  # approximate mass; NOT geodetic truth data
EARTH_RADIUS = 6.371e6
B_EQUATOR_TOY = 31.2e-6


def checked(*values):
    if not all(isfinite(float(v)) for v in values):
        raise ValueError('non-finite parameter')


def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def scale(a,s): return tuple(x*s for x in a)
def norm(a): return sqrt(dot(a,a))


@dataclass(frozen=True)
class Helix:
    radius: float
    omega: float
    axial_speed: float
    tangential_speed: float
    speed: float
    kappa: float
    tau: float
    pitch: float

    def position(self,t):
        q=self.omega*t
        return (self.radius*cos(q),self.radius*sin(q),self.axial_speed*t)

    def velocity(self,t):
        q=self.omega*t
        return (-self.tangential_speed*sin(q),self.tangential_speed*cos(q),self.axial_speed)

    def acceleration(self,t):
        q=self.omega*t
        return (-self.radius*self.omega**2*cos(q),-self.radius*self.omega**2*sin(q),0.0)


def helix_from_radius_pitch(radius, pitch_radians, speed=1.):
    checked(radius,pitch_radians,speed)
    if radius<=0 or speed<=0 or not -pi/2<pitch_radians<pi/2:
        raise ValueError('finite circular helix needs R>0,v>0 and |pitch|<pi/2')
    vtheta=speed*cos(pitch_radians)
    u=speed*sin(pitch_radians)
    omega=vtheta/radius
    kappa=vtheta*vtheta/(radius*speed*speed)
    tau=u*vtheta/(radius*speed*speed)
    return Helix(radius,omega,u,vtheta,speed,kappa,tau,pitch_radians)


def helix_invert(kappa,tau,speed=1.):
    checked(kappa,tau,speed)
    if kappa<=0 or speed<=0: raise ValueError('inverse requires κ>0,v>0')
    d=kappa*kappa+tau*tau
    if d<=0 or not isfinite(d): raise ValueError('invalid geometry')
    return helix_from_radius_pitch(kappa/d,atan2(tau,kappa),speed)


def lorentz_interval(ct,x,y,z):
    checked(ct,x,y,z)
    return ct*ct-x*x-y*y-z*z


def lorentz_z(ct,x,y,z,beta):
    checked(ct,x,y,z,beta)
    if abs(beta)>=1: raise ValueError('Lorentz boost |β|<1')
    gam=1/sqrt((1-beta)*(1+beta))
    return (gam*(ct-beta*z),x,y,gam*(z-beta*ct))


def proper_time_rate(beta):
    checked(beta)
    if abs(beta)>1: raise ValueError('no superluminal timelike worldline')
    return sqrt(max(0,(1-beta)*(1+beta)))


def kg_group_velocity(k,q,mass_inv_length=0.):
    checked(k,q,mass_inv_length)
    if q<0 or mass_inv_length<0: raise ValueError('nonnegative q and mass required')
    d=sqrt(k*k+q*q+mass_inv_length*mass_inv_length)
    if d==0: raise ValueError('zero-mode undefined group velocity')
    return C*k/d


def cutoff_length_from_energy(E_joules):
    checked(E_joules)
    if E_joules<=0: raise ValueError('positive cutoff energy')
    return HBAR*C/E_joules


def planck_length(G_newton=G):
    checked(G_newton)
    if G_newton<=0: raise ValueError('positive Newton coupling')
    return sqrt(HBAR*G_newton/C**3)


def exponential_integral_E1(x):
    """Stable E1 for x>=0, with series x<=1 and continued fraction otherwise.

    Uses E1(x)=exp(-x)*CF(x) for x>1; CF from NR expint algorithm.
    Validated independently against scipy.special.exp1 in the test harness.
    """
    checked(x)
    if x<0: raise ValueError('x>=0')
    if x==0: return float('inf')
    if x<=1:
        term=1.0; sm=0.0
        for k in range(1,512):
            term*= -x/k
            delta=term/k
            sm+=delta
            if abs(delta)<1e-17: break
        return -0.5772156649015329-log(x)-sm
    # Continued fraction from incomplete Gamma Q(a=0,x); Lentz iteration.
    tiny=1e-300
    b=x+1.0
    c=1.0/tiny
    d=1.0/b
    h=d
    for i in range(1,1000):
        a=-float(i*i)
        b+=2.0
        d=a*d+b
        if abs(d)<tiny: d=tiny
        c=b+a/c
        if abs(c)<tiny: c=tiny
        d=1.0/d
        delta=d*c
        h*=delta
        if abs(delta-1)<1e-14: break
    return h*exp(-x)


def threshold_F(mu):
    checked(mu)
    if mu<0: raise ValueError('μ>=0')
    if mu==0: return 1.0
    if mu>30: return 0.0
    x=mu*mu
    return max(0.,exp(-x)-x*exponential_integral_E1(x))


def inverse_G_induced(N,xi,ell_m,mu=0.,bare_inverse_G=0.):
    """One-loop scalar proper-time cutoff, only a scheme-dependent toy.

    1/G_eff = 1/G_bare + N(1-6ξ)ℏ F(μ)/(12π c³ℓ²).
    Not a parameter-free prediction. Negative coefficient possible for ξ>1/6.
    """
    checked(N,xi,ell_m,mu,bare_inverse_G)
    if N<=0 or N!=int(N) or ell_m<=0 or mu<0:
        raise ValueError('N positive integer, ell positive, mu nonnegative')
    return bare_inverse_G+N*(1-6*xi)*HBAR*threshold_F(mu)/(12*pi*C**3*ell_m**2)


def reverse_fit_length(N,xi=0,G_measured=G):
    checked(N,xi,G_measured)
    if N<=0 or 1-6*xi<=0 or G_measured<=0: raise ValueError('invalid inverse fit')
    return sqrt(N*(1-6*xi)*HBAR*G_measured/(12*pi*C**3))


def alpha_candidate(): return 1/(4*pi**3+pi*pi+pi)


def residual_ppm(estimated,reference):
    checked(estimated,reference)
    if reference==0: raise ValueError('nonzero reference')
    return 1e6*(estimated/reference-1)


def spherical_earth_g(altitude):
    checked(altitude)
    if altitude<0: raise ValueError('only exterior spherical model')
    return G*EARTH_MASS/(EARTH_RADIUS+altitude)**2


def dipole_B(latitude_radians,altitude=0.):
    checked(latitude_radians,altitude)
    if altitude<0: raise ValueError('external field only')
    ratio=(EARTH_RADIUS/(EARTH_RADIUS+altitude))**3
    return B_EQUATOR_TOY*ratio*sqrt(1+3*sin(latitude_radians)**2)


def force_classical(position,velocity,mass,charge,E_field=(0.,0.,0.),B_field=(0.,0.,0.)):
    """Spherical Earth + arbitrary fields; nonrelativistic vector force.

    Not a four-force unification: the strong/weak interactions are omitted.
    """
    checked(*position,*velocity,mass,charge,*E_field,*B_field)
    if mass<=0: raise ValueError('mass positive')
    r=norm(position)
    if r<EARTH_RADIUS: raise ValueError('exterior Earth model only')
    fg=scale(position,-G*EARTH_MASS*mass/(r**3))
    fe=scale(E_field,charge)
    fb=scale(cross(velocity,B_field),charge)
    return fg,fe,fb,add(add(fg,fe),fb)


def yukawa_factor(u):
    checked(u)
    if u<0: raise ValueError('u>=0')
    if u>700: return 0.0
    return (1+u)*exp(-u)


def fifth_force_eta(alpha_A,alpha_B,r_over_range):
    """Synthetic test: a_i=g0(1+α_i(1+r/λ)e^(-r/λ))."""
    checked(alpha_A,alpha_B,r_over_range)
    k=yukawa_factor(r_over_range)
    den=2+(alpha_A+alpha_B)*k
    if den<=0: raise ValueError('unphysical acceleration sum')
    return 2*(alpha_A-alpha_B)*k/den


def metric_planck_sq(M0,xi,phi):
    """Jordan F(phi)=M0^2-xi phi^2, natural units."""
    checked(M0,xi,phi)
    return M0*M0-xi*phi*phi


def photon_kinetic_Z(phi,zeta,Lambda):
    """Z(phi)=1+zeta phi/Lambda, natural units."""
    checked(phi,zeta,Lambda)
    if Lambda<=0: raise ValueError('Λ>0')
    return 1+zeta*phi/Lambda


def log_alpha_derivative(phi,zeta,Lambda):
    """d ln alpha_eff / d phi=-Z'/Z, ignoring RG running.

    Only valid if alpha_eff∝1/Z under specified normalization.
    """
    Z=photon_kinetic_Z(phi,zeta,Lambda)
    if Z<=0: raise ValueError('healthy Maxwell kinetic coefficient requires Z>0')
    return -zeta/(Lambda*Z)


def scalar_potential(phi,m2,lam):
    checked(phi,m2,lam)
    return .5*m2*phi**2+.25*lam*phi**4


def scalar_potential_prime(phi,m2,lam):
    checked(phi,m2,lam)
    return m2*phi+lam*phi**3


def vacuum_energy_from_cutoff_energy(Ecut_j):
    """Massless real scalar zero-point density with sharp |k| cutoff.

    rho = Ecut^4/[16π² (ℏ c)^3], J/m^3; enormous and NOT the
    observed cosmological constant nor a solved renormalized prediction.
    """
    checked(Ecut_j)
    if Ecut_j<=0: raise ValueError('positive energy')
    return Ecut_j**4/(16*pi*pi*(HBAR*C)**3)


def eotvos_sigma_total(stat=2.3e-15,syst=1.5e-15):
    checked(stat,syst)
    return sqrt(stat*stat+syst*syst)


def microscope_illustrative_interval(z=1.96):
    checked(z)
    center=-1.5e-15
    s=eotvos_sigma_total()
    return center-z*s,center+z*s


def pass_microscope_toy(alpha_a,alpha_b,r_over_range=0.,z=1.96):
    lo,hi=microscope_illustrative_interval(z)
    return lo<=fifth_force_eta(alpha_a,alpha_b,r_over_range)<=hi


def model_status():
    return {'gr_equations':'established under GR action',
            'micro_helical_KG':'mathematical toy solution',
            'G_first_principles':'OPEN',
            'four_force_derivation':'OPEN',
            'model_predictions':'parameter dependent; not independently confirmed'}


def cavendish_massless_scalar_G(F0,Fprime,K0=1.):
    """Weak-field Cavendish coupling in minimal Jordan scalar-tensor toy.

    S=∫√-g [F(φ)R/2-K(φ)(∂φ)²/2+L_m(g,ψ)].
    Requires non-tachyonic effectively massless scalar, no direct composition
    dependent couplings and background slow variation. Not valid for massive
    scalar, screening or non-minimal EM coupling without further analysis.
    """
    checked(F0,Fprime,K0)
    if F0<=0 or K0<=0:raise ValueError('healthy background input required')
    den=2*K0*F0+3*Fprime*Fprime
    return (2*K0*F0+4*Fprime*Fprime)/den/(8*pi*F0)


def ppn_gamma_massless_scalar(F0,Fprime,K0=1.):
    """PPN gamma weak-field for same minimal Jordan scalar-tensor subclass."""
    checked(F0,Fprime,K0)
    if F0<=0 or K0<=0:raise ValueError('healthy background input required')
    return (K0*F0+Fprime*Fprime)/(K0*F0+2*Fprime*Fprime)


def cassini_illustrative_interval(z=1.96):
    """Simple quoted gamma=1+(2.1±2.3)e-5, illustrative Gaussian zσ."""
    checked(z)
    center=1+2.1e-5
    return center-z*2.3e-5,center+z*2.3e-5


def pass_cassini_toy(F0,Fprime,K0=1.,z=1.96):
    g=ppn_gamma_massless_scalar(F0,Fprime,K0)
    lo,hi=cassini_illustrative_interval(z)
    return lo<=g<=hi
