"""ROOT V63 minimal scientific computation (Python >=3.10, no dependencies).

Definitions and status:
  - helix_*: exact Euclidean curve kinematics for prescribed speed c;
    this is NOT a relativistic material-particle worldline.
  - cylindrical_wave_mode: massless/massive free-field dispersion on an
    idealized cylindrical shell, NOT an established space-grain model.
  - induced_G: one-loop, sharp proper-time cutoff, scalar only, Euclidean
    curvature coefficient, with ZERO bare 1/G assumed by default.
    Scheme dependent: never interpret as a model-independent prediction.
  - Yukawa: separately postulated phenomenological fifth-force benchmark.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
import math

C = 299_792_458.0                       # exact m/s
H = 6.626_070_15e-34                    # exact J s
HBAR = H/(2*math.pi)                  # exact from h, pi
G_CODATA_2022 = 6.67430e-11           # measurement m^3 kg^-1 s^-2
G_STD = 0.00015e-11                  # CODATA 2022 standard uncertainty
M_EARTH = 5.9722e24                 # illustrative Earth mass, kg
R_EARTH = 6_371_000.0                # illustrative mean spherical radius, m
B_EQUATOR = 31.2e-6                  # reference dipole equatorial B, T (toy)


def dot(a, b):
    return sum(x*y for x,y in zip(a,b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])


def norm(a):
    return math.sqrt(dot(a,a))


@dataclass(frozen=True)
class Helix:
    radius_m: float
    angle_rad: float
    omega_rad_s: float
    axial_m_s: float
    azimuthal_m_s: float
    curvature_m_inv: float
    torsion_m_inv: float
    acceleration_m_s2: float

    def position(self, t_s: float):
        a = self.omega_rad_s * t_s
        return (self.radius_m * math.cos(a), self.radius_m * math.sin(a), self.axial_m_s*t_s)

    def velocity(self, t_s: float):
        a = self.omega_rad_s * t_s
        return (-self.azimuthal_m_s*math.sin(a), self.azimuthal_m_s*math.cos(a), self.axial_m_s)

    def acceleration(self, t_s: float):
        a = self.omega_rad_s * t_s
        return (-self.radius_m*self.omega_rad_s**2*math.cos(a),
                -self.radius_m*self.omega_rad_s**2*math.sin(a),0.)


def helix(radius_m: float, angle_deg: float, speed_m_s: float=C) -> Helix:
    if not (radius_m>0 and math.isfinite(radius_m)):
        raise ValueError('radius must be finite and positive')
    if not (math.isfinite(angle_deg) and 0 <= angle_deg <= 90):
        raise ValueError('angle must be in [0,90] degrees')
    if not (speed_m_s>0 and math.isfinite(speed_m_s)):
        raise ValueError('speed must be finite and positive')
    a=math.radians(angle_deg)
    omega=speed_m_s*math.cos(a)/radius_m
    vz=speed_m_s*math.sin(a)
    vp=speed_m_s*math.cos(a)
    # κ=Rω²/v², τ=vz ω/v² for constant speed v.
    return Helix(radius_m,a,omega,vz,vp,
                 math.cos(a)**2/radius_m,
                 math.sin(a)*math.cos(a)/radius_m,
                 speed_m_s**2*math.cos(a)**2/radius_m)


@dataclass(frozen=True)
class CylindricalWaveMode:
    radius_m: float
    winding_n: int
    axial_wavenumber_inv_m: float
    rest_mass_kg: float
    omega_rad_s: float
    energy_j: float
    group_v_phi_m_s: float
    group_v_z_m_s: float
    group_speed_m_s: float
    phase_pitch_rad: float


def cylindrical_wave_mode(radius_m: float, winding_n: int, k_z_inv_m: float,
                          rest_mass_kg: float=0.) -> CylindricalWaveMode:
    """Toy field on an idealized cylindrical 2D shell.

    Ω²=c²[(n/R)²+k_z²+(mc/ℏ)²].
    v_phi is an effective semiclassical derivative of the dispersion wrt
    continuous transverse wavenumber. n itself is discrete.
    """
    if radius_m<=0 or not math.isfinite(radius_m):
        raise ValueError('invalid radius')
    if not isinstance(winding_n,int) or winding_n==0:
        raise ValueError('integer winding n must be nonzero')
    if not math.isfinite(k_z_inv_m) or rest_mass_kg<0 or not math.isfinite(rest_mass_kg):
        raise ValueError('invalid k_z or rest mass')
    q_phi=winding_n/radius_m
    q_m=rest_mass_kg*C/HBAR
    q=math.sqrt(q_phi*q_phi+k_z_inv_m*k_z_inv_m+q_m*q_m)
    om=C*q
    vp=C*q_phi/q
    vz=C*k_z_inv_m/q
    return CylindricalWaveMode(radius_m,winding_n,k_z_inv_m,rest_mass_kg,
                               om,HBAR*om,vp,vz,math.hypot(vp,vz),
                               math.atan2(k_z_inv_m,q_phi))


def proper_time_mass_factor(mu: float, steps: int=2000) -> float:
    """F(mu)=∫_0^1 exp[-mu^2/t] dt, mu=m*c*ell/hbar.
    For mu=0 exactly F=1. Simpson quadrature on a dimensionless interval.
    This is equivalent to ∫_{1/Λ²}^∞ exp(-m²s) ds/s² / Λ².
    """
    if mu<0 or not math.isfinite(mu):
        raise ValueError('mu must be nonnegative finite')
    if not isinstance(steps,int) or steps<2 or steps%2:
        raise ValueError('steps must be a positive even integer')
    if mu==0:
        return 1.
    def f(t):
        if t==0: return 0.
        return math.exp(-mu*mu/t)
    s=f(0)+f(1)
    for j in range(1,steps):
        s+=(4 if j%2 else 2)*f(j/steps)
    return s/(3*steps)


def planck_length_m(G: float=G_CODATA_2022) -> float:
    if G<=0: raise ValueError('G must be positive')
    return math.sqrt(HBAR*G/C**3)


def cutoff_energy_j(ell_m: float) -> float:
    if ell_m<=0: raise ValueError('ell must be positive')
    return HBAR*C/ell_m


def cutoff_length_m(E_j: float) -> float:
    if E_j<=0: raise ValueError('energy must be positive')
    return HBAR*C/E_j


def induced_inverse_G(N: int, ell_m: float, xi: float=0., mu: float=0.,
                      bare_inverse_G: float=0.) -> float:
    """1/G_ren = 1/G_bare + N (1-6xi) hbar F(mu)/(12 pi c^3 ell²).
    Pure scalar in one sharp proper-time cutoff scheme. No prediction of N,
    ell, xi, regulator or bare coupling is made by this function.
    """
    if not isinstance(N,int) or N<=0:
        raise ValueError('N must be a positive integer')
    if ell_m<=0 or not math.isfinite(ell_m):
        raise ValueError('ell must be finite and positive')
    if not math.isfinite(xi) or not math.isfinite(bare_inverse_G):
        raise ValueError('invalid xi or bare coupling')
    scalar_weight=1-6*xi
    if abs(scalar_weight)<1e-14: scalar_weight=0.
    return (bare_inverse_G + N*scalar_weight*HBAR*proper_time_mass_factor(mu)/
            (12*math.pi*C**3*ell_m**2))


def induced_G(N: int, ell_m: float, xi: float=0., mu: float=0.,
              bare_inverse_G: float=0.) -> float:
    inv=induced_inverse_G(N,ell_m,xi,mu,bare_inverse_G)
    return math.copysign(math.inf,inv) if inv==0 else 1./inv


def calibrated_length_m(G_target: float=G_CODATA_2022,
                        N: int=1, xi: float=0.) -> float:
    """Inverse fit to G_target, NOT a prediction. Only massless, bare=0."""
    if not G_target>0 or not N>0 or not (1-6*xi)>0:
        raise ValueError('requires G>0, N>0, xi<1/6')
    return math.sqrt(G_target*N*(1-6*xi)*HBAR/(12*math.pi*C**3))


def vacuum_energy_magnitude_j_m3(ell_m: float) -> float:
    """Formal leading |one-loop scalar vacuum density| in sharp cutoff.
    Depends on regulator and counterterms; NOT an observed energy density.
    """
    if ell_m<=0: raise ValueError('invalid ell')
    return HBAR*C/(64*math.pi**2*ell_m**4)


def earth_g_m_s2(altitude_m: float=0.) -> float:
    if R_EARTH+altitude_m<=0: raise ValueError('invalid radius')
    return G_CODATA_2022*M_EARTH/(R_EARTH+altitude_m)**2


def dipole_B_tesla(position_m):
    """Aligned Earth toy dipole, NOT IGRF; z-axis magnetic north dipole."""
    r=norm(position_m)
    if r<=0: raise ValueError('invalid position')
    z=(0.,0.,1.)
    rhat=tuple(x/r for x in position_m)
    mproj=dot(z,rhat)
    k=B_EQUATOR*(R_EARTH/r)**3
    return tuple(k*(3*mproj*rhat[i]-z[i]) for i in range(3))


def lorentz_force(v, B, charge_c):
    return tuple(charge_c*x for x in cross(v,B))


def yukawa_relative_accel(alpha_y: float,r_m: float,range_m: float) -> float:
    """Separate phenomenological benchmark: (g_Y - g_Newton)/g_Newton.
    g_Y=g_N [1+alpha(1+r/ell)exp(-r/ell)]. NOT deduced from helix.
    """
    if r_m<0 or range_m<=0: raise ValueError('invalid distance/range')
    u=r_m/range_m
    return alpha_y*(1+u)*math.exp(-u)


def old_alpha_guess() -> float:
    return 1./(4*math.pi**3+math.pi**2+math.pi)


def old_mass_ratio_guess() -> float:
    return 2*math.pi*3**3+2*math.pi


def frenet_frame(h: Helix, t_s: float=0.):
    """Return orthonormal Frenet T,N,B of a nonstraight constant-speed helix.
    At zero curvature N and B are undefined (mathematical singularity).
    """
    if h.curvature_m_inv < 1e-28:
        raise ValueError('straight line has undefined normal and binormal')
    v=h.velocity(t_s); a=h.acceleration(t_s)
    T=tuple(x/norm(v) for x in v)
    N=tuple(x/norm(a) for x in a)
    B=cross(T,N)
    return T,N,B


def lorentz_boost_z(ct: float,z: float,beta: float):
    """One-dimensional Lorentz boost in length units (ct,z), |beta|<1.
    Demonstrates invariant interval; not a dynamical derivation of SR.
    """
    if not math.isfinite(beta) or abs(beta)>=1.:
        raise ValueError('beta must be in (-1,1)')
    gamma=1./math.sqrt(1-beta**2)
    return gamma*(ct-beta*z),gamma*(z-beta*ct)


def electromagnetic_plane_wave(z_m:float,t_s:float,amplitude_v_m:float,
                                wavelength_m:float):
    """Exactly solvable vacuum Maxwell plane wave, propagation +z.
    E=(0,E0*cos(kz-wt),0), B=(-E0/c*cos(...),0,0).
    This is NOT generated by the ROOT geometric conjecture.
    """
    if wavelength_m<=0 or not math.isfinite(wavelength_m):
        raise ValueError('wavelength must be positive and finite')
    if not all(map(math.isfinite,(z_m,t_s,amplitude_v_m))):
        raise ValueError('inputs must be finite')
    theta=2*math.pi*(z_m/wavelength_m-C*t_s/wavelength_m)
    val=amplitude_v_m*math.cos(theta)
    return (0.,val,0.),(-val/C,0.,0.)
