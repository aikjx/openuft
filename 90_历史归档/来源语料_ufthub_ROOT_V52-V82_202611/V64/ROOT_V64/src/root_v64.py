"""ROOT V64 mathematical audit: exact conditional physics, no GUT discovery.

Python 3.10+ standard library only. SI in gravity/helix/induced-G; the
cylindrical KG section adopts dimensionless natural units c=hbar=1.
"""
from __future__ import annotations
from dataclasses import dataclass
import math

C=299792458.0
HBAR=6.62607015e-34/(2*math.pi)
G_OBS=6.67430e-11  # CODATA 2022 input, not predicted
G_SIGMA=0.00015e-11
ALPHA_OBS=7.2973525643e-3 # CODATA 2022 input
J11=3.8317059702075123156 # first positive zero of Bessel J_1


def dot(x,y): return sum(a*b for a,b in zip(x,y))
def cross(x,y): return (x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0])
def norm(x): return math.sqrt(dot(x,x))
def vec_scale(x,s): return tuple(a*s for a in x)

@dataclass(frozen=True)
class Helix:
    radius:float
    angle_deg:float
    speed:float
    angular_rate:float
    axial_speed:float
    tangential_speed:float
    curvature:float
    torsion:float
    centripetal_accel:float

    def position(self,t):
        p=self.angular_rate*t
        return (self.radius*math.cos(p),self.radius*math.sin(p),self.axial_speed*t)
    def velocity(self,t):
        p=self.angular_rate*t
        return (-self.tangential_speed*math.sin(p),self.tangential_speed*math.cos(p),self.axial_speed)
    def acceleration(self,t):
        p=self.angular_rate*t
        return (-self.radius*self.angular_rate**2*math.cos(p),-self.radius*self.angular_rate**2*math.sin(p),0.)
    def frame(self,t):
        if self.curvature<1e-18: raise ValueError('straight-line limit has no unique normal')
        T=vec_scale(self.velocity(t),1/self.speed)
        N=vec_scale(self.acceleration(t),1/norm(self.acceleration(t)))
        return T,N,cross(T,N)

def helix(R=1.,angle_deg=35.,speed=C):
    if R<=0 or speed<=0 or not all(map(math.isfinite,(R,angle_deg,speed))) or not (0<=angle_deg<=90):
        raise ValueError('R>0, speed>0, 0<=angle<=90 required')
    a=math.radians(angle_deg)
    ct=math.cos(a);st=math.sin(a)
    w=speed*ct/R
    return Helix(R,angle_deg,speed,w,speed*st,speed*ct,ct*ct/R,st*ct/R,speed*speed*ct*ct/R)


def j_integer(n,x):
    """Bessel J_n for integer n>=0 via power series, accurate on 0<=x<=~6."""
    if not isinstance(n,int) or n<0 or not math.isfinite(x) or abs(x)>8:
        raise ValueError('0<=n integer, |x|<=8 required')
    term=(x/2)**n/math.factorial(n)
    total=term
    for k in range(1,90):
        term*=-(x*x/4)/(k*(n+k))
        total+=term
        if abs(term)<1e-16*max(1,abs(total)): break
    return total

@dataclass(frozen=True)
class HelicalKGMode:
    """Complex KG mode in a perfectly reflecting cylindrical cavity, natural units.

    phi=A J_1(q*r) exp[i(theta+k*z-omega*t)] ; r in [0,a]
    (-d_t^2 + Laplace - mu^2) phi = 0; Dirichlet at r=a.
    No gravitational coupling is derived here.
    """
    a:float=1.0
    k:float=0.75
    mu:float=0.4
    amplitude:float=1.0
    n:int=1
    @property
    def q(self): return J11/self.a
    @property
    def omega(self): return math.sqrt(self.q*self.q+self.k*self.k+self.mu*self.mu)
    @property
    def axial_group_speed(self): return self.k/self.omega
    def f(self,r): return self.amplitude*j_integer(1,self.q*r)
    def df(self,r): return self.amplitude*self.q*(j_integer(0,self.q*r)-j_integer(2,self.q*r))/2
    def energy_density(self,r):
        """T00 natural units; no 1/2 since complex scalar L=-|dphi|^2-mu²|phi|²."""
        if r<0 or r>self.a: raise ValueError('0<=r<=a')
        f=self.f(r); df=self.df(r)
        angular=self.amplitude*self.q/2 if r==0 else f/r
        return (self.omega*self.omega+self.k*self.k+self.mu*self.mu)*f*f+df*df+angular*angular
    def norm2_exact(self):
        return math.pi*self.a*self.a*self.amplitude**2*j_integer(2,J11)**2
    def energy_per_length_exact(self):
        """E/L =2 omega² ∫cross_section |phi|² d²x by KG eigenmode."""
        return 2*self.omega**2*self.norm2_exact()
    def radial_residual(self,r,dr=1e-4):
        if not (dr<r<self.a-dr): raise ValueError('sample away from boundaries')
        fpp=(self.f(r+dr)-2*self.f(r)+self.f(r-dr))/(dr*dr)
        return fpp+self.df(r)/r-self.f(r)/(r*r)+self.q**2*self.f(r)


def integrate_radial(mode:HelicalKGMode,samples=4000):
    """Trapezoidal 2π∫ r T00 dr. Returns (radial samples, cumulative fractions, E/L).

    Source is classical, normalized to an externally supplied line mass when
    converting to SI gravity. This does NOT predict a mass or Newton's G.
    """
    if samples<20: raise ValueError('samples too small')
    dr=mode.a/samples
    radii=[dr*i for i in range(samples+1)]
    rad_int=[2*math.pi*r*mode.energy_density(r) for r in radii]
    cumulative=[0.]
    for i in range(samples):
        cumulative.append(cumulative[-1]+(rad_int[i]+rad_int[i+1])*dr/2)
    energy=cumulative[-1]
    return radii,[v/energy for v in cumulative],energy


def line_gravity(mass_per_length_kg_m,radius_m,inside_fraction=1.,G=G_OBS):
    """Infinite line/cylindrical matter: g(r)=2 G mu_enclosed(r)/r, input G.
    Approaches 1/r outside cylinder, NOT point-source 1/r².
    """
    if mass_per_length_kg_m<0 or radius_m<=0 or G<=0 or not 0<=inside_fraction<=1:
        raise ValueError('positive r,G; nonnegative line mass; fraction in [0,1]')
    return 2*G*mass_per_length_kg_m*inside_fraction/radius_m


def planck_length(G=G_OBS):
    if G<=0: raise ValueError('G>0')
    return math.sqrt(HBAR*G/C**3)

def cutoff_length(energy_j):
    if energy_j<=0: raise ValueError('E>0')
    return HBAR*C/energy_j

def cutoff_energy(ell_m):
    if ell_m<=0: raise ValueError('ell>0')
    return HBAR*C/ell_m

def proper_time_factor(mu,steps=4000):
    """F(mu)=∫0¹ exp(-mu²/t)dt. mu is m c ell/hbar for mass in kg."""
    if mu<0 or not math.isfinite(mu) or steps<10 or steps%2:
        raise ValueError('mu>=0 and even steps >=10')
    if mu==0: return 1.
    def f(t): return 0. if t==0 else math.exp(-mu*mu/t)
    total=f(0)+f(1)
    for i in range(1,steps): total+=(4 if i%2 else 2)*f(i/steps)
    return total/(3*steps)

def inverse_G_induced(N,ell_m,xi=0,mu=0,bare_inverse_G=0):
    """1/G_ren=1/G_bare+N(1-6xi)hbar/(12pi c³ ell²) F(mu).
    Scalar one loop with sharp proper-time cutoff (scheme dependent).
    """
    if N<=0 or not isinstance(N,int) or ell_m<=0 or not all(map(math.isfinite,(ell_m,xi,mu,bare_inverse_G))):
        raise ValueError('invalid parameters')
    return bare_inverse_G + N*(1-6*xi)*HBAR*proper_time_factor(mu)/(12*math.pi*C**3*ell_m**2)

def inverse_fit_length(N=1,xi=0,G_target=G_OBS):
    """Uses observed G (reverse calibration, never an independent prediction)."""
    if N<=0 or (1-6*xi)<=0 or G_target<=0:raise ValueError('positive inputs, xi<1/6')
    return math.sqrt(N*(1-6*xi)*HBAR*G_target/(12*math.pi*C**3))


def yukawa_g_ratio(alpha,r,ell):
    """Postulated fifth-force benchmark: Δg/g_N=α (1+r/ell) exp(-r/ell)."""
    if r<0 or ell<=0:raise ValueError('bad r/ell')
    u=r/ell
    return alpha*(1+u)*math.exp(-u)

def yukawa_potential(alpha,r,ell,G=G_OBS,m1=1,m2=1):
    if r<=0 or ell<=0: raise ValueError('positive r,ell')
    return -G*m1*m2/r*(1+alpha*math.exp(-r/ell))

def bad_alpha_guess():return 1/(4*math.pi**3+math.pi**2+math.pi)
def bad_mass_ratio_guess():return 56*math.pi

def lorentz_boost(ct,z,beta):
    if abs(beta)>=1 or not math.isfinite(beta):raise ValueError('|beta|<1')
    gamma=1/math.sqrt(1-beta*beta)
    return gamma*(ct-beta*z),gamma*(z-beta*ct)


def maxwell_plane_wave(z_m,t_s,amplitude_v_m,wavelength_m):
    """Exact classical vacuum wave along +z: E_y, B_-x; NOT ROOT prediction."""
    if wavelength_m<=0: raise ValueError('positive wavelength')
    k=2*math.pi/wavelength_m
    E=amplitude_v_m*math.cos(k*(z_m-C*t_s))
    return (0.,E,0.),(-E/C,0.,0.)


def su2_commutator():
    """[sigma_x,sigma_y] - 2i sigma_z; 2x2 complex matrix demo."""
    sx=((0j,1+0j),(1+0j,0j))
    sy=((0j,-1j),(1j,0j))
    sz=((1+0j,0j),(0j,-1+0j))
    def mm(a,b):
        return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))
    ab=mm(sx,sy);ba=mm(sy,sx)
    residual=max(abs(ab[i][j]-ba[i][j]-2j*sz[i][j]) for i in range(2) for j in range(2))
    noncommuting=max(abs(ab[i][j]-ba[i][j]) for i in range(2) for j in range(2))
    return residual,noncommuting


def scalar_tensor_effective_M2(M0_squared,xi,psi_abs_squared):
    """Toy EFT coefficient M_eff² = M0² - 2xi|psi|² (natural units)."""
    if M0_squared<=0 or psi_abs_squared<0 or not all(map(math.isfinite,(M0_squared,xi,psi_abs_squared))):
        raise ValueError('invalid coefficient')
    return M0_squared-2*xi*psi_abs_squared
