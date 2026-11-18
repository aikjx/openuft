"""ROOT V67 audit engine: established equations and explicitly tagged toy models.
All SI unless individual function specifies natural units. Pure stdlib Python 3.10+.
No function purports to derive or predict fundamental G.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import pi, sqrt, sin, cos, exp, log, atan2, isfinite

C = 299792458.0
HBAR = 1.054571817e-34
G = 6.67430e-11
E_CHARGE = 1.602176634e-19
ME = 9.1093837139e-31
MP = 1.67262192595e-27
M_EARTH = 5.9722e24
R_EARTH = 6.371e6
MU0 = 1.25663706127e-6  # approximate CODATA 2022
GAMMA_E = 0.5772156649015328606


def dot(a,b):
    return sum(x*y for x,y in zip(a,b))

def cross(a,b):
    return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])

def norm(a):
    return sqrt(dot(a,a))

@dataclass(frozen=True)
class Helix:
    radius: float
    omega: float
    axial_speed: float
    def __post_init__(self):
        if self.radius <= 0 or self.omega <= 0:
            raise ValueError('radius and omega must be positive')
    @property
    def speed(self):
        return sqrt((self.radius*self.omega)**2+self.axial_speed**2)
    @property
    def kappa(self):
        return self.radius*self.omega**2/self.speed**2
    @property
    def torsion(self):
        return self.axial_speed*self.omega/self.speed**2
    @property
    def pitch_angle(self):
        return atan2(self.axial_speed,self.radius*self.omega)
    def position(self,t):
        p=self.omega*t
        return (self.radius*cos(p),self.radius*sin(p),self.axial_speed*t)
    def velocity(self,t):
        p=self.omega*t
        return (-self.radius*self.omega*sin(p),self.radius*self.omega*cos(p),self.axial_speed)
    def acceleration(self,t):
        p=self.omega*t
        return (-self.radius*self.omega**2*cos(p),-self.radius*self.omega**2*sin(p),0.0)
    def third_derivative(self,t):
        p=self.omega*t
        return (self.radius*self.omega**3*sin(p),-self.radius*self.omega**3*cos(p),0.0)
    def invariant_checks(self,t):
        v=self.velocity(t);a=self.acceleration(t);j=self.third_derivative(t)
        cross_va=cross(v,a)
        return {
            'v_dot_a':dot(v,a),
            'kappa_direct':norm(cross_va)/self.speed**3,
            'torsion_direct':dot(cross_va,j)/norm(cross_va)**2,
            'normal_acceleration':norm(a),
            'speed_sq':dot(v,v),
        }
    def particle_worldline_admissible(self):
        return self.speed<C


def inverse_helix(kappa,torsion,speed):
    if kappa<=0 or speed<=0:
        raise ValueError('inversion only for positive curvature and speed')
    denom=sqrt(kappa*kappa+torsion*torsion)
    return Helix(kappa/denom**2,speed*denom,speed*torsion/denom)


def minkowski_interval(ct,x,y,z):
    return -ct*ct+x*x+y*y+z*z

def lorentz_boost_x(ct,x,beta):
    if abs(beta)>=1:
        raise ValueError('beta must be subluminal')
    gamma=1/sqrt(1-beta*beta)
    return gamma*(ct-beta*x),gamma*(x-beta*ct)

def electromagnetic_force(q,velocity,electric,magnetic):
    vxb=cross(velocity,magnetic)
    return tuple(q*(electric[i]+vxb[i]) for i in range(3))

def central_gravity(position,mass=M_EARTH):
    r=norm(position)
    if r<=0: raise ValueError('point mass model singular at origin')
    return tuple(-G*mass*x/(r**3) for x in position)

def gravity_magnitude(r,mass=M_EARTH):
    if r<=0:raise ValueError('r must be positive')
    return G*mass/(r*r)

def dipole_magnetic(position,moment):
    r=norm(position)
    if r<=0: raise ValueError('dipole singular at origin')
    nhat=tuple(x/r for x in position)
    proj=dot(moment,nhat)
    factor=MU0/(4*pi*r**3)
    return tuple(factor*(3*proj*nhat[i]-moment[i]) for i in range(3))

def earth_dipole_moment(eq_field_tesla=31.2e-6):
    return (0.0,0.0,eq_field_tesla*4*pi*R_EARTH**3/MU0)

def schwarzschild_radius(mass):
    return 2*G*mass/C**2

def schwarzschild_isco_radius(mass):
    return 6*G*mass/C**2

def mass_ratio():
    return MP/ME

def g_from_length_cutoff(ell,N=1,xi=0):
    """Toy induced gravity assuming zero bare inverse G, mu=0. Not a G prediction."""
    if ell<=0 or N<=0 or 1-6*xi<=0:raise ValueError('requires ell>0,N>0,(1-6xi)>0')
    return 12*pi*C**3*ell**2/(N*(1-6*xi)*HBAR)

def cutoff_length_fitted_to_G(N=1,xi=0):
    return sqrt(G*N*(1-6*xi)*HBAR/(12*pi*C**3))

def planck_length():
    return sqrt(HBAR*G/C**3)


def expint_e1(x):
    """Exponential integral E1(x), for x>0, pure Python.
    Power series x<=1, Lentz continued fraction x>1 (NR form).
    """
    if x<=0:raise ValueError('x must be positive')
    if x<=1:
        term=-x
        summation=term
        for k in range(2,500):
            term*=(-x)*(k-1)/(k*k)
            summation+=term
            if abs(term)<1e-16*max(1,abs(summation)):break
        return -GAMMA_E-log(x)-summation
    b=x+1.0
    c=1e300
    d=1/b
    h=d
    for i in range(1,600):
        a=-i*i
        b+=2
        d=1/(a*d+b)
        c=b+a/c
        delta=c*d
        h*=delta
        if abs(delta-1)<2e-15:break
    return h*exp(-x)

def threshold_F(mu):
    """F(mu)=integral_1^infinity exp(-mu^2*t)/t^2 dt, mu>=0."""
    if mu<0:raise ValueError('mu must be nonnegative')
    if mu==0:return 1.0
    if mu>26:return 0.0 # exp(-mu^2) far below double precision
    z=mu*mu
    return max(0.0,exp(-z)-z*expint_e1(z))

def inverse_g_induced_delta(length,N=1,xi=0,mu=0):
    """Scheme-dependent 1-loop scalar leading term in SI; no bare term included."""
    if length<=0 or N<0: raise ValueError('invalid length/N')
    return N*(1-6*xi)*HBAR/(12*pi*C**3*length**2)*threshold_F(mu)

def _sm_inverses(alpha_em_inv=127.95,sin2=0.23122,alpha3=0.118):
    if min(alpha_em_inv,sin2,alpha3)<=0 or sin2>=1:raise ValueError('invalid EW inputs')
    return ((3/5)*(1-sin2)*alpha_em_inv, sin2*alpha_em_inv, 1/alpha3)

BETA_SM=(41/10,-19/6,-7)

def gauge_inverse_at_mu(mu_gev,mz_gev=91.1876,alpha_em_inv=127.95,sin2=0.23122,alpha3=0.118):
    if mu_gev<=0 or mz_gev<=0:raise ValueError('energy must be positive')
    base=_sm_inverses(alpha_em_inv,sin2,alpha3)
    t=log(mu_gev/mz_gev)
    return tuple(base[i]-BETA_SM[i]*t/(2*pi) for i in range(3))

def gauge_pair_intersection(i,j,mz_gev=91.1876,alpha_em_inv=127.95,sin2=0.23122,alpha3=0.118):
    if i==j or min(i,j)<0 or max(i,j)>2:raise ValueError('distinct indices 0..2 required')
    base=_sm_inverses(alpha_em_inv,sin2,alpha3)
    logratio=(base[i]-base[j])*2*pi/(BETA_SM[i]-BETA_SM[j])
    return mz_gev*exp(logratio)

def kk_gauge_transform(A,dLambda):
    """Coordinate y'=y-k*Lambda implies A'=A+dLambda; dy'+kA'=dy+kA."""
    return tuple(x+y for x,y in zip(A,dLambda))

def kk_one_form(dy,k,A,dx):
    return dy+k*dot(A,dx)

def yukawa_relative_accel(alpha,r,lam):
    """Toy universally coupled fifth force, delta g/g_Newton."""
    if r<0 or lam<=0:raise ValueError('r>=0, lambda>0')
    z=r/lam
    return alpha*(1+z)*exp(-z)

def comp_dependent_eta(betaE,betaA,betaB,r,lam):
    """Toy composition-dependent Yukawa couplings; Eotvos ratio with full denominator."""
    h=yukawa_relative_accel(1.0,r,lam)
    a=1+betaE*betaA*h
    b=1+betaE*betaB*h
    return 2*(a-b)/(a+b)

def scalar_tensor_ppn(F,K,Fprime):
    """Dimensionally normalized scalar field convention in V66 massless ST candidate.
    Requires 2KF+3F'^2>0 and F>0; finite unscreened scalar range.
    """
    if F<=0 or 2*K*F+3*Fprime*Fprime<=0:
        raise ValueError('invalid scalar tensor kinetic health conditions')
    gamma=(K*F+Fprime**2)/(K*F+2*Fprime**2)
    g_ratio=(2*K*F+4*Fprime**2)/(2*K*F+3*Fprime**2)
    return gamma,g_ratio

def star_cosmic_regime(quantity):
    return {'value':quantity,'interpretation':'calculated within an assumed theory; no independent proof of ROOT'}


def standard_model_one_generation_anomalies():
    """Exact rational chiral anomaly traces for one SM generation, LH Weyl fields.
    Hypercharges: Q_L=1/6, u^c=-2/3, d^c=1/3, L_L=-1/2, e^c=1.
    No right-handed neutrino is required for these gauge anomalies.
    """
    from fractions import Fraction as Q
    fields=[(6,Q(1,6)),(3,Q(-2,3)),(3,Q(1,3)),(2,Q(-1,2)),(1,Q(1))]
    cubic=sum((multiplicity*Y**3 for multiplicity,Y in fields),Q(0))
    gravitational=sum((multiplicity*Y for multiplicity,Y in fields),Q(0))
    su2su2u1=Q(1,2)*(3*Q(1,6)+Q(-1,2))
    su3su3u1=Q(1,2)*(2*Q(1,6)+Q(-2,3)+Q(1,3))
    su3_cubic=2-1-1 # color triplets Q_L doublet and two anti-triplet LH conjugates
    return {'U1_cubed':cubic,'gravity_U1':gravitational,'SU2_squared_U1':su2su2u1,
            'SU3_squared_U1':su3su3u1,'SU3_cubed':su3_cubic}


def electroweak_tree_masses(g,g_prime,vev):
    """SM tree level, natural units; no loop-level corrections."""
    if min(g,g_prime,vev)<=0:raise ValueError('couplings and vev must be positive')
    return (g*vev/2,sqrt(g*g+g_prime*g_prime)*vev/2)


def charged_pair_force_ratio(mass_a,mass_b,charge_a=E_CHARGE,charge_b=E_CHARGE,eps0=8.8541878188e-12):
    """Absolute |F_electric|/|F_gravity| for two point charges at any same r."""
    return abs(charge_a*charge_b)/(4*pi*eps0*G*mass_a*mass_b)
