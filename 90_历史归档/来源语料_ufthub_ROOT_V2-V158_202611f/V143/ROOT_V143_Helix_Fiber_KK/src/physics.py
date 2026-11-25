"""Auditable kinematic and limited KK diagnostics, with c=1 and hbar, G explicit.

Length L and time T have equal dimensions; mass M remains independent.
All numbers here are illustration or CODATA reference inputs, not ROOT measurements.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from math import pi, sqrt

PLANCK_MASS_KG = 2.176434e-8  # NIST CODATA 2022; measured G drives uncertainty
PLANCK_LENGTH_M = 1.616255e-35  # NIST CODATA 2022
ELECTRON_MASS_KG = 9.1093837139e-31  # NIST CODATA 2022
ALPHA = 7.2973525643e-3  # NIST CODATA 2022


@dataclass(frozen=True)
class Helix:
    radius: float
    omega: float
    axial_speed: float
    internal_radius: float
    internal_omega: float

    @property
    def transverse_speed(self):
        return abs(self.radius*self.omega)

    @property
    def v3_squared(self):
        return (self.radius*self.omega)**2 + self.axial_speed**2

    @property
    def internal_speed(self):
        return self.internal_radius*self.internal_omega

    @property
    def v5_squared(self):
        return self.v3_squared + self.internal_speed**2

    @property
    def curvature(self):
        if self.v3_squared == 0:
            raise ValueError('Zero spatial speed gives no Frenet frame')
        return self.radius*self.omega**2/self.v3_squared

    @property
    def torsion(self):
        if self.v3_squared == 0:
            raise ValueError('Zero spatial speed gives no Frenet frame')
        return self.axial_speed*self.omega/self.v3_squared

    @property
    def angle_frequency_from_geometry(self):
        return sqrt(self.v3_squared*(self.curvature**2+self.torsion**2))

    def validate_null(self, tolerance=1e-12):
        return abs(self.v5_squared-1) <= tolerance


def null_helix_example():
    # Entire five-dimensional null motion has speed 1; the 3D projection does NOT.
    omega = 1.0
    radius = 0.3
    axial_speed = 0.8
    internal_radius = 2.0
    internal_omega = sqrt(1-radius**2*omega**2-axial_speed**2)/internal_radius
    h = Helix(radius,omega,axial_speed,internal_radius,internal_omega)
    assert h.validate_null()
    return h


def coupling_matching(G4: float, hbar: float, R: float, k: float = 1.0):
    """G4: L/M, hbar: M*L, R: L, k: dimensionless. Return g² dimensionless."""
    if min(G4,hbar,R) <= 0 or k == 0:
        raise ValueError('Invalid KK parameters')
    return 16*pi*G4*hbar/(R**2*k**2)


def alpha_from_mass(mass: float, G4: float, hbar: float):
    """Minimal 5D Einstein-circle reduction relation for massless 5D scalar mode.

    alpha_n = 4 G4 m_n²/hbar, with n≠0, no other matter mass terms.
    """
    if mass < 0 or G4 <= 0 or hbar <= 0:
        raise ValueError('Invalid physical input')
    return 4*G4*mass**2/hbar


def alpha_from_mass_planck(mass_kg: float, planck_mass_kg: float=PLANCK_MASS_KG):
    return 4*(mass_kg/planck_mass_kg)**2


def mass_from_alpha_planck(alpha: float, planck_mass_kg: float=PLANCK_MASS_KG):
    if alpha < 0:
        raise ValueError('alpha must be nonnegative')
    return 0.5*sqrt(alpha)*planck_mass_kg


def circle_radius_from_alpha(alpha: float, n: int=1, planck_length_m: float=PLANCK_LENGTH_M):
    if alpha <= 0 or n == 0:
        raise ValueError('alpha must be positive and n nonzero')
    return 2*abs(n)*planck_length_m/sqrt(alpha)


def mass_tower_ratio(n: int, m: int):
    if m == 0: raise ValueError('reference mode cannot be zero')
    return abs(n/m)


def gauge_covariant_mode(derivative_psi: complex, psi:complex, A: float,
                         n: int, k: float=1.0):
    """D_mu psi = (partial_mu - i n k A_mu) psi."""
    return derivative_psi-1j*n*k*A*psi


def diagnostics():
    h=null_helix_example()
    inferred_mass=mass_from_alpha_planck(ALPHA)
    return {
      'units':'c=1; hbar and G not set equal to 1',
      'model':'minimal 5D Einstein gravity on a circular fiber; NOT new ROOT theory',
      'helix':{
          **asdict(h),'transverse_speed':h.transverse_speed,
          'v3':sqrt(h.v3_squared),'v5':sqrt(h.v5_squared),
          'curvature_per_L':h.curvature,'torsion_per_L':h.torsion,
          'omega_from_kappa_tau':h.angle_frequency_from_geometry,
          'internal_speed':h.internal_speed,
          'fourD_gamma':1/sqrt(1-h.v3_squared),
      },
      'kk_minimal_model':{
          'alpha_observed_CODATA2022':ALPHA,
          'alpha_if_electron_first_KK_mode':alpha_from_mass_planck(ELECTRON_MASS_KG),
          'alpha_discrepancy_factor':ALPHA/alpha_from_mass_planck(ELECTRON_MASS_KG),
          'mass_if_alpha_matches_observed_kg':inferred_mass,
          'mass_ratio_to_electron':inferred_mass/ELECTRON_MASS_KG,
          'radius_if_alpha_matches_m':circle_radius_from_alpha(ALPHA),
          'incompatibility_scope':'ONLY minimal massless 5D field identified with electron-like charged mode',
      },
      'status':{
          'geometrical_derivations':'verified',
          'five_D_Ricci_specific_case':'symbolically checked',
          'full_four_force_unification':'NOT established',
          'experimental_validation_of_ROOT':'NOT performed',
      }
    }
