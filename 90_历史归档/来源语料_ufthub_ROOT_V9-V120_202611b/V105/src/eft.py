"""Natural-unit gauge-singlet compact-phase toy EFT checks (not a unified theory)."""
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class PhaseEFT:
    f_GeV: float
    Lambda_GeV: float
    c1: float = 0.0
    c2: float = 0.0
    c3: float = 0.0

    def __post_init__(self):
        if self.f_GeV <= 0 or self.Lambda_GeV < 0:
            raise ValueError('Healthy kinetic normalization f>0 and Lambda>=0 required.')

    def potential_GeV4(self, theta: float):
        return self.Lambda_GeV**4*(1-math.cos(theta))

    def potential_prime_GeV4(self, theta: float):
        return self.Lambda_GeV**4*math.sin(theta)

    def canon_mass_GeV(self):
        return self.Lambda_GeV**2/self.f_GeV

    def source_GeV4(self, P1=0, P2=0, P3=0):
        """Pj = tr(F_j tilde F_j), all in GeV^4 convention."""
        return (self.c1*P1+self.c2*P2+self.c3*P3)/4

    def theta_acceleration_GeV2(self, theta, P1=0,P2=0,P3=0):
        """Minkowski, homogeneous theta, t unit GeV^-1, theta'' GeV^2."""
        return -(self.potential_prime_GeV4(theta) + self.source_GeV4(P1,P2,P3))/self.f_GeV**2


def dimension_is_valid(lhs, rhs):
    return tuple(lhs) == tuple(rhs)

# Canonical mass exponent in natural units (M).
DIMENSIONS = {
 'theta':0, 'f':1, 'Lambda':1, 'partial_mu':1,
 'F_mu_nu':2, 'Fdual_mu_nu':2, 'lagrangian_density':4,
 'sqrt_minus_g':0, 'd4x':-4, 'fourD_action':0,
 'Frenet_curvature':1, 'Riemann_curvature':2,
 'gauge_connection':1, 'gauge_curvature':2,
 'Newton_G':-2,
}
