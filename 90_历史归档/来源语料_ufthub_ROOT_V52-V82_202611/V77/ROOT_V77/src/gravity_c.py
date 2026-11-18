"""ROOT V77: transparent relations between Newton's constant and c.

This package implements established identities and explicitly labelled hypotheses.
No function here predicts the measured G from the value of c alone.
Only Python standard-library modules are needed.
"""
from __future__ import annotations
import math
from dataclasses import dataclass

C = 299_792_458.0                               # exact by SI definition, m/s
G = 6.67430e-11                                # CODATA 2022, SI
SIGMA_G = 0.00015e-11                          # CODATA 2022 standard uncertainty
H = 6.62607015e-34                            # exact by SI definition, J s
HBAR = H/(2.0*math.pi)
ME = 9.1093837139e-31                          # CODATA 2022 electron mass, kg
MPROTON = 1.67262192595e-27                    # CODATA 2022 proton mass, kg
GM_EARTH = 398600.435507e9                    # JPL DE440, m^3/s^2
GM_SUN = 1.32712440041279419e20              # JPL, m^3/s^2
R_EARTH = 6_371_000.0                        # illustrative mean radius, m


@dataclass(frozen=True)
class Quantity:
    value: float
    sigma: float
    unit: str


def z_from_g(g=G, c=C):
    """Z := G*c/2. This is a new dimensional name, not an independent prediction."""
    return g*c/2.0


def g_from_z(z, c=C):
    return 2*z/c


def schwarzschild_radius(mass, g=G, c=C):
    return 2*g*mass/c**2


def gravitational_radius(mass, g=G, c=C):
    """Half the Schwarzschild radius; valid as geometric length definition."""
    return g*mass/c**2


def g_from_gravitational_radius(radius, mass, c=C):
    return c*c*radius/mass


def reduced_compton_wavelength(mass, hbar=HBAR, c=C):
    return hbar/(mass*c)


def gravitational_alpha(mass, g=G, hbar=HBAR, c=C):
    return g*mass**2/(hbar*c)


def g_from_gravitational_alpha(alpha, mass, hbar=HBAR, c=C):
    return alpha*hbar*c/(mass**2)


def planck_length(g=G, hbar=HBAR, c=C):
    return math.sqrt(hbar*g/c**3)


def g_from_length(length, hbar=HBAR, c=C):
    return c**3 * length**2 / hbar


def planck_mass(g=G, hbar=HBAR, c=C):
    return math.sqrt(hbar*c/g)


def g_from_mass(mass, hbar=HBAR, c=C):
    return hbar*c/mass**2


def einstein_coupling(g=G, c=C):
    """8*pi*G/c^4, unit m/J (T_mu_nu energy density in J/m^3)."""
    return 8*math.pi*g/c**4


def newton_gravity_accel(gm, radius):
    return gm / radius**2


def g_from_surface_accel(accel, radius, mass):
    return accel*radius**2/mass


def z_measured() -> Quantity:
    return Quantity(z_from_g(), C*SIGMA_G/2.0, 'm^4 kg^-1 s^-3')


def relative_g_uncertainty() -> float:
    return SIGMA_G / G


def one_percent_z_hypothesis():
    """Testing the dimensional *numerical* hypothesis Z = 0.0100 in this SI system."""
    g_guess = g_from_z(0.01)
    return {'g_guess': g_guess, 'relative_residual': (g_guess-G)/G,
            'sigma_residual': (g_guess-G)/SIGMA_G}


def earth_geometric_radius():
    """JPL orbit parameter GM/c^2, independent of G but NOT separately of mass."""
    return GM_EARTH/C**2


def earth_mass_inferred(g=G):
    """Derived from JPL GM / measured G; NOT an independent mass measurement."""
    return GM_EARTH/g


def mass_radius_consistency(mass, g=G, c=C, hbar=HBAR):
    rg = gravitational_radius(mass, g, c)
    rc = reduced_compton_wavelength(mass, hbar, c)
    return {'r_g': rg, 'r_C': rc, 'ratio': rg/rc,
            'alpha_g': gravitational_alpha(mass, g, hbar, c)}


def c_scaling_models(c_factor):
    """Mutually incompatible conditional toy models; not physical varying-c theories."""
    if c_factor <= 0:
        raise ValueError('c_factor must be positive')
    return {'fixed_G': G,
            'fixed_Z': G/c_factor,
            'fixed_gravitational_radius_and_mass': G*c_factor**2,
            'fixed_planck_length_and_hbar': G*c_factor**3}


def dimensional_power(symbol):
    """Dimensions (L, M, T) as integer powers."""
    lookup = {'G': (3,-1,-2), 'c': (1,0,-1),
              'hbar': (2,1,-1), 'mass': (0,1,0), 'length': (1,0,0),
              'Z': (4,-1,-3), 'alpha_g': (0,0,0),
              'r_g': (1,0,0), 'r_C': (1,0,0),
              'kappa_E': (-1,-1,2)}
    # kappa_E=8piG/c^4: dim L^-1 M^-1 T^2.
    return lookup[symbol]


def dim_mul(*pairs):
    """Each pair is ('symbol', exponent)."""
    dims = [0,0,0]
    for name, power in pairs:
        for i, exponent in enumerate(dimensional_power(name)):
            dims[i] += power*exponent
    return tuple(dims)


def dimensional_no_go_c_hbar():
    """Proof using dimensional equations. No real a,b solve c^a*hbar^b=[G]."""
    # M requires b=-1; L requires a+2*b=3 hence a=5.
    # T then requires -(a+b)=-2, but -(5-1)=-4.
    a, b = 5, -1
    return {'a_for_L_and_M': a, 'b_for_M': b,
            'time_exponent_required': -2, 'time_exponent_obtained': -a-b,
            'possible': False}


def g_to_ratio(c_factor, exponent):
    return c_factor**exponent


def dimensionless_variation(g_fraction=0.0, m_fraction=0.0,
                            hbar_fraction=0.0, c_fraction=0.0):
    """First-order dln alpha_G, contrasts units/convention-dependent dlnG."""
    return g_fraction+2*m_fraction-hbar_fraction-c_fraction


def summary():
    z=z_measured()
    el=mass_radius_consistency(ME)
    pr=mass_radius_consistency(MPROTON)
    p=planck_mass()
    return {
        'constants': {'G_SI':G, 'u_G_SI':SIGMA_G, 'c_SI':C, 'h_SI':H,
                      'hbar_SI':HBAR, 'm_e_kg':ME, 'm_p_kg':MPROTON,
                      'GM_Earth_m3_s2':GM_EARTH},
        'quantities': {
          'Z_SI': z.value, 'u_Z_SI': z.sigma,
          'G_over_c_SI': G/C, 'G_over_c2_SI': G/C**2,
          'G_over_c4_SI': G/C**4, 'Einstein_kappa_m_per_J': einstein_coupling(),
          'Planck_length_m':planck_length(), 'Planck_mass_kg':p,
          'G_relative_uncertainty':relative_g_uncertainty(),
          'gravitational_alpha_electron': el['alpha_g'],
          'gravitational_alpha_proton': pr['alpha_g'],
          'electron_r_g_m':el['r_g'], 'electron_r_C_m':el['r_C'],
          'proton_r_g_m':pr['r_g'], 'proton_r_C_m':pr['r_C'],
          'Earth_GM_over_c2_m':earth_geometric_radius(),
          'Earth_mass_inferred_kg':earth_mass_inferred(),
          'Earth_spherical_g_m_s2':newton_gravity_accel(GM_EARTH,R_EARTH),
          'Earth_schwarzschild_radius_from_GM_m':2*GM_EARTH/C**2,
          'Z_equals_0p01_hypothesis':one_percent_z_hypothesis(),
        },
        'provenance': 'NIST CODATA 2022 and JPL DE440; stated numeric values of G and masses are measured, not predicted',
        'theory_status': 'No independent prediction of G from c alone'
    }
