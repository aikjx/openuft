"""ROOT V80 astrophysical baselines and *illustrative* new-physics diagnostics.

No calculation in this module constitutes a discovery or independent prediction of G.
GR Schwarzschild formulas are benchmarks for spherical, uncharged, nonrotating exteriors.
Numerical inputs for solar-system bodies are approximate NASA fact-sheet/JPL values;
compact objects are explicitly synthetic reference models.
"""
from dataclasses import dataclass
from math import pi, sqrt, cos, sin, exp, log
from typing import Optional

G = 6.67430e-11                 # CODATA 2022, measured
C = 299_792_458.0              # defined SI exact
HBAR = 1.0545718176461565e-34 # h/(2pi) defined SI
MU0 = 1.0/(8.8541878188e-12*C*C)  # nominal epsilon0, approximate
M_SUN = 1.9885e30
M_E = 9.1093837139e-31
E_CHARGE = 1.602176634e-19

@dataclass(frozen=True)
class Body:
    name: str
    mass_kg: float
    radius_m: float
    b_field_t: Optional[float] = None  # illustration, not a global measured 3D field
    provenance: str = 'NASA/JPL approximate'
    note: str = ''

# Reference surface B values are deliberately rounded scenarios for cross-scale tests;
# do NOT treat them as calibrated measured local fields or spatial profiles.
BODIES = [
    Body('太阳 Sun', 1.9885e30, 6.9634e8, 1e-3, note='B=1 mT is an illustrative region, not a uniform global field'),
    Body('水星 Mercury', 3.3011e23, 2.4397e6, None),
    Body('金星 Venus', 4.8675e24, 6.0518e6, None),
    Body('地球 Earth', 5.9722e24, 6.3710e6, 5e-5, note='B=50 μT representative local magnitude'),
    Body('月球 Moon', 7.342e22, 1.7374e6, None),
    Body('火星 Mars', 6.4171e23, 3.3895e6, None),
    Body('木星 Jupiter', 1.89813e27, 6.9911e7, 4e-4, note='B illustrative, gravity ignores oblateness/rotation'),
    Body('土星 Saturn', 5.6834e26, 5.8232e7, None),
    Body('天王星 Uranus', 8.681e25, 2.5362e7, None),
    Body('海王星 Neptune', 1.02413e26, 2.4622e7, None),
    Body('白矮星 WD（演示）', 0.60*M_SUN, 8e6, 1e3, 'SYNTHETIC', 'mass/radius/B are assumed comparison parameters'),
    Body('中子星 NS（演示）', 1.40*M_SUN, 12e3, 1e8, 'SYNTHETIC', 'spherical Schwarzschild benchmark only; EOS not solved'),
    Body('磁星 Magnetar（演示）', 1.40*M_SUN, 12e3, 1e10, 'SYNTHETIC', '10^10 T illustrative; strong-field QED and EOS corrections omitted'),
]

def mean_density(mass_kg: float, radius_m: float) -> float:
    if mass_kg <= 0 or radius_m <= 0:
        raise ValueError('positive mass and radius required')
    return mass_kg/(4*pi*radius_m**3/3)

def surface_g(mass_kg: float, radius_m: float) -> float:
    return G*mass_kg/radius_m**2

def compactness(mass_kg: float, radius_m: float) -> float:
    return G*mass_kg/(radius_m*C**2)

def schwarzschild_radius(mass_kg: float) -> float:
    return 2*G*mass_kg/C**2

def kretschmann(mass_kg: float, radius_m: float) -> float:
    return 48*(G*mass_kg)**2/(C**4*radius_m**6)

def tidal_max(mass_kg: float, radius_m: float) -> float:
    """Newtonian magnitude of radial tidal-gradient eigenvalue, s^-2."""
    return 2*G*mass_kg/radius_m**3

def magnetic_energy_density(b_t: float) -> float:
    return b_t*b_t/(2*MU0)

def magnetic_rest_ratio(b_t: float, density_kg_m3: float) -> float:
    """Local/representative dimensionless comparison, not total stellar field energy."""
    if density_kg_m3 <= 0:
        raise ValueError('density must be positive')
    return magnetic_energy_density(b_t)/(density_kg_m3*C**2)

def q_ed_critical_field() -> float:
    """Electron QED critical magnetic field [T]: cyclotron quantum ~ m_e c^2."""
    return M_E*M_E*C*C/(E_CHARGE*HBAR)

def orbital_frequency(gm: float, radius_m: float) -> float:
    return sqrt(gm/radius_m**3)

def circular_orbit_period(gm: float, radius_m: float) -> float:
    return 2*pi/orbital_frequency(gm, radius_m)

def mercury_precession_arcsec_century() -> float:
    """1PN pericenter shift, only GR correction, no planetary perturbations."""
    mu_sun = 1.32712440041279419e20  # JPL ephemeris
    a = 57.90905e9                     # m; rounded orbital semimajor axis
    e = 0.205630
    P_days = 87.9691
    dphi_per_orbit_rad = 6*pi*mu_sun/(a*(1-e*e)*C*C)
    return dphi_per_orbit_rad*(180/pi)*3600*(36525/P_days)

def redshift_surface_to_infinity(mass_kg: float, radius_m: float) -> float:
    """z = (1-2GM/(rc²))^-1/2 -1; invalid inside Schwarzschild horizon."""
    chi = compactness(mass_kg, radius_m)
    if 2*chi >= 1: raise ValueError('surface at or within Schwarzschild horizon')
    return 1/sqrt(1-2*chi)-1

def gr_isco(mass_kg: float) -> float:
    return 6*G*mass_kg/C**2

def gr_photon_sphere(mass_kg: float) -> float:
    return 3*G*mass_kg/C**2

def candidate_field_dependent_fraction(b_t: float, density: float, beta: float) -> float:
    """HYPOTHESIS: ΔG/G = beta * u_B/(ρc²); not derived or measured."""
    return beta*magnetic_rest_ratio(b_t, density)

def scalar_g_c_no_go() -> dict:
    """Solve dimension constraints for G=c^a ℏ^b; show inconsistency."""
    # M: b=-1, L: a+2b=3 gives a=5, T exponent then -a-b=-4 != -2.
    return {'a_from_mass_and_length':5, 'b_from_mass':-1, 'time_exponent_predicted':-4, 'time_exponent_required':-2, 'consistent':False}

def g_versus_c_reparam(c:float, z:float)->float:
    if c<=0: raise ValueError('c>0 required')
    return 2*z/c

def gravitational_mu_identifiability(g: float, mass:float, fraction:float)->tuple[float,float]:
    """Same μ=GM despite different G and M; fraction >0."""
    if fraction<=0: raise ValueError('positive fraction required')
    return g*fraction, mass/fraction

def photon_zero_invariant_nonzero_energy(e_v_m: float)->dict:
    """Plane wave in vacuum: B=E/c, E·B=0, field invariants vanish."""
    b=e_v_m/C
    u=8.8541878188e-12*e_v_m*e_v_m
    return {'b_t':b,'electric_minus_c2magnetic':e_v_m*e_v_m-C*C*b*b,'e_dot_b':0.0,'energy_j_m3':u}

def body_report(body:Body)->dict:
    m,r=body.mass_kg,body.radius_m
    rho=mean_density(m,r)
    row={'name':body.name,'mass_kg':m,'radius_m':r,'mean_density_kg_m3':rho,
         'newtonian_g_m_s2':surface_g(m,r),'compactness':compactness(m,r),
         'surface_tidal_s2':tidal_max(m,r),'schwarzschild_K_m4':kretschmann(m,r),
         'redshift_to_infinity':redshift_surface_to_infinity(m,r),
         'assumed_B_T':body.b_field_t,'provenance':body.provenance,'limitations':body.note}
    if body.b_field_t is not None:
        row['magnetic_energy_J_m3']=magnetic_energy_density(body.b_field_t)
        row['magnetic_to_mean_rest_energy_ratio']=magnetic_rest_ratio(body.b_field_t,rho)
        row['B_over_QED_critical']=body.b_field_t/q_ed_critical_field()
    else:
        row['magnetic_energy_J_m3']=None
        row['magnetic_to_mean_rest_energy_ratio']=None
        row['B_over_QED_critical']=None
    return row
