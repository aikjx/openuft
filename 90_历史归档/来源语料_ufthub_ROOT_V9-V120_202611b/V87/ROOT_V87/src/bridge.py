"""ROOT V87: established low-energy bridges + explicitly marked toy models.

SI units everywhere. No claim of UV-complete quantum gravity or an independent G prediction.
"""
from __future__ import annotations
import math
from dataclasses import dataclass

C = 299_792_458.0
H = 6.626_070_15e-34
HBAR = H/(2*math.pi)
G = 6.67430e-11 # NIST/CODATA 2022, not derived
M_EARTH = 5.9722e24  # reference value, not independent G input
R_EARTH = 6.371e6
M_SUN = 1.9885e30
M_RB87 = 1.44316060e-25  # approximate single-atom mass, illustrative
G_STD = 9.80665


def positive(**params):
    for k,v in params.items():
        if not math.isfinite(v) or v <= 0:
            raise ValueError(f'{k} must be positive finite, got {v}')


def finite(**params):
    for k,v in params.items():
        if not math.isfinite(v):
            raise ValueError(f'{k} must be finite')


def potential(M, r):
    positive(M=M, r=r)
    return -G*M/r


def acceleration(M, r):
    positive(M=M, r=r)
    return G*M/r**2


def potential_difference(M, r_low, r_high):
    positive(M=M, r_low=r_low, r_high=r_high)
    # Stable against cancellation for r_high close to r_low.
    return G*M*(r_high-r_low)/(r_low*r_high)


def schwarzschild_radius(M):
    positive(M=M)
    return 2*G*M/C**2


def compactness(M,r):
    positive(M=M,r=r)
    return G*M/(r*C*C)


def redshift_static(M, r_emit, r_receive):
    """Static Schwarzschild observers, nu_received / nu_emitted, both outside horizon."""
    positive(M=M, r_emit=r_emit, r_receive=r_receive)
    rs=schwarzschild_radius(M)
    if r_emit<=rs or r_receive<=rs: raise ValueError('static observers require r > r_s')
    return math.sqrt((1-rs/r_emit)/(1-rs/r_receive))


def hover_proper_acceleration(M,r):
    """Acceleration to hover at fixed Schwarzschild radius; not free-fall acceleration."""
    positive(M=M,r=r)
    rs=schwarzschild_radius(M)
    if r<=rs: raise ValueError('no static hover at or under horizon')
    return acceleration(M,r)/math.sqrt(1-rs/r)


def phase_from_potential_difference(m, delta_phi_potential, T):
    """Upper-minus-lower quantum phase of two held branches; delta V = m delta Phi."""
    positive(m=m, T=T)
    finite(delta_phi_potential=delta_phi_potential)
    return -m*delta_phi_potential*T/HBAR


def phase_uniform(m, g, height, T):
    positive(m=m,T=T)
    finite(g=g,height=height)
    return phase_from_potential_difference(m, g*height, T)


def phase_spherical(m, M, r_lower, r_upper, T):
    return phase_from_potential_difference(m,potential_difference(M,r_lower,r_upper),T)


def phase_shape_ratio(R,h):
    """Exact Newtonian spherical potential difference normalized by g(R)*h.

    h>0; normalized ratio = R/(R+h), independent of G and M.
    """
    positive(R=R,h=h)
    return R/(R+h)


def potential_yukawa(M,r,alpha,lamb):
    positive(M=M,r=r,lamb=lamb)
    finite(alpha=alpha)
    return -G*M/r*(1+alpha*math.exp(-r/lamb))


def acceleration_yukawa(M,r,alpha,lamb):
    positive(M=M,r=r,lamb=lamb)
    finite(alpha=alpha)
    return acceleration(M,r)*(1+alpha*(1+r/lamb)*math.exp(-r/lamb))


def shape_yukawa(r,alpha,lamb):
    positive(r=r,lamb=lamb)
    finite(alpha=alpha)
    x=r/lamb
    y=alpha*math.exp(-x)
    denom=1+y*(1+x)
    if abs(denom)<1e-15: raise ValueError('vanishing effective acceleration')
    return 1+y*x*x/(2*denom)


def phase_yukawa(m,M,r_low,r_high,T,alpha,lamb):
    positive(m=m,T=T)
    ph=potential_yukawa(M,r_high,alpha,lamb)-potential_yukawa(M,r_low,alpha,lamb)
    return phase_from_potential_difference(m,ph,T)


def normalized_yukawa_shape(M,r_low,r_high,alpha,lamb):
    positive(r_low=r_low,r_high=r_high)
    if r_low == r_high: raise ValueError('different radii required')
    delta=potential_yukawa(M,r_high,alpha,lamb)-potential_yukawa(M,r_low,alpha,lamb)
    acc=acceleration_yukawa(M,r_low,alpha,lamb)
    if acc == 0: raise ValueError('zero acceleration')
    return delta/(acc*(r_high-r_low))


def perihelion_advance_rad(M,a,e):
    positive(M=M,a=a)
    if not math.isfinite(e) or not 0<=e<1: raise ValueError('0<=e<1')
    return 6*math.pi*G*M/(a*(1-e*e)*C*C)


def planck_length(): return math.sqrt(HBAR*G/C**3)

def planck_mass(): return math.sqrt(HBAR*C/G)

def alpha_gravity(m):
    positive(m=m)
    return G*m*m/(HBAR*C)

def epsilon_quantum_gravity(r):
    positive(r=r)
    return (planck_length()/r)**2


def gaussian_density(M,a,r):
    positive(M=M,a=a)
    if not math.isfinite(r) or r<0: raise ValueError('radius must be >=0')
    return M*math.exp(-(r/a)**2)/(math.pi**1.5*a**3)


def gaussian_potential(M,a,r):
    """Newtonian potential of Gaussian rho=M/(pi^3/2 a^3) exp(-r²/a²)."""
    positive(M=M,a=a)
    if not math.isfinite(r) or r<0: raise ValueError('radius must be >=0')
    if r==0: return -2*G*M/(math.sqrt(math.pi)*a)
    return -G*M*math.erf(r/a)/r


def gaussian_grav_self_energy(m,a):
    """Mean-field gravitational self-energy, including half-counting."""
    positive(m=m,a=a)
    return -G*m*m/(math.sqrt(2*math.pi)*a)


def gaussian_quantum_kinetic(m,a):
    """For normalized wavefunction psi=(pi^-3/4 a^-3/2) exp(-r²/(2a²))."""
    positive(m=m,a=a)
    return 3*HBAR*HBAR/(4*m*a*a)


def sn_gaussian_toy_energy(m,a):
    """Nonfundamental Schrödinger-Newton Gaussian variational toy energy."""
    return gaussian_quantum_kinetic(m,a)+gaussian_grav_self_energy(m,a)


def sn_variational_radius(m):
    positive(m=m)
    return 3*math.sqrt(2*math.pi)*HBAR**2/(2*G*m**3)


def branch_entangling_phase(m1,m2,dist_00,dist_01,dist_10,dist_11,T):
    """Newtonian 4-path gravitational phase invariant; not automatically a proof of quantized gravity."""
    positive(m1=m1,m2=m2,dist_00=dist_00,dist_01=dist_01,dist_10=dist_10,dist_11=dist_11,T=T)
    return G*m1*m2*T/HBAR*(1/dist_00+1/dist_11-1/dist_01-1/dist_10)


def em_energy_mass(U):
    finite(U=U)
    return U/C**2


def numerical_gradient(fun, x, relative_step=1e-5):
    positive(x=x,relative_step=relative_step)
    h=x*relative_step
    return (fun(x+h)-fun(x-h))/(2*h)


def source_phase_design(M,R,h,T,m=M_RB87,phase_noise_rad=0.01):
    """Toy signal-to-noise, ignoring complex interferometer systematics."""
    positive(M=M,R=R,h=h,T=T,m=m,phase_noise_rad=phase_noise_rad)
    phase=phase_spherical(m,M,R,R+h,T)
    return {'phase_rad':phase,'phase_snr':abs(phase)/phase_noise_rad,
            'shape_ratio':phase_shape_ratio(R,h),
            'uniform_approx_phase_rad':phase_uniform(m,acceleration(M,R),h,T)}

def clock_high_over_low_fractional(M,r_low,r_high):
    """Static Schwarzschild clock-rate ratio high/low minus 1, stable for 1 m on Earth.

    Assumes identical static clocks and R_high>R_low>r_s.
    """
    positive(M=M,r_low=r_low,r_high=r_high)
    rs=schwarzschild_radius(M)
    if r_low <= rs or r_high <= rs or r_high <= r_low:
        raise ValueError('require r_high > r_low > r_s')
    rel = (rs*(r_high-r_low)/(r_low*r_high))/(1-rs/r_low)
    return math.expm1(0.5*math.log1p(rel))


def consistency_triangle(M,r_low,r_high,m,T):
    """Cross-check Newtonian phase potential vs GR static clock redshift.

    Clocks: identical static, weak-field; phase: two *held* branches without trap/laser
    phases. Difference is a known relativistic correction, not predicted new physics.
    """
    ph=phase_spherical(m,M,r_low,r_high,T)
    dp=-HBAR*ph/(m*T)
    dz=C*C*clock_high_over_low_fractional(M,r_low,r_high)
    return {'phase_potential_m2s2':dp,'clock_potential_m2s2':dz,
            'fractional_difference':(dp-dz)/dp}


def kretschmann_schwarzschild(M,r):
    """Exterior Schwarzschild curvature scalar K=48G²M²/(c⁴r⁶)."""
    positive(M=M,r=r)
    return 48*G*G*M*M/(C**4*r**6)
