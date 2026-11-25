"""ROOT V146: 6D Einstein-Maxwell flux compactification, homogeneous radion.
All coefficients are expressed in one consistent c=1 unit system.  hbar and G
are *not* assigned numerical values or set to one.  Numerical examples are
explicitly dimensionless ratios, not predictions for the observed universe.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import pi, sqrt, isfinite, sin


@dataclass(frozen=True)
class SixDimensional:
    K6: float
    Lambda6: float
    chi6: float
    R0: float
    n: int

    def __post_init__(self):
        if self.K6 <= 0 or self.chi6 <= 0 or self.Lambda6 < 0 or self.R0 <= 0:
            raise ValueError('K6, chi6, R0 must be positive; Lambda6 >= 0')
        if type(self.n) is not int:
            raise TypeError('topological charge n must be an integer')

    def reduce(self) -> 'Potential':
        R04 = self.R0 ** 4
        K4 = 4 * pi * self.K6 * self.R0**2
        A = 4 * pi * self.Lambda6 * R04
        B = 4 * pi * self.K6 * R04
        C = (pi / 2) * self.chi6 * self.n**2 * R04
        return Potential(A, B, C, K4)

    def G4(self) -> float:
        """From K4/2 = 1/(16*pi*G4), NOT an independent prediction of G."""
        return 1.0 / (8 * pi * self.reduce().K4)

    def minkowski_einstein_residuals(self, R: float) -> dict[str, float]:
        """6D Einstein equations for flat M4 x round S2, in tensor coefficients.

        external: -K6/R^2 + Lambda6 + chi6 n^2/(8 R^4) = 0
        internal: Lambda6 - chi6 n^2/(8 R^4) = 0
        Both zero is necessary & sufficient for this direct-product background.
        """
        _require_r(R)
        flux = self.chi6 * self.n**2 / (8 * R**4)
        return {
            'external': -self.K6/R**2 + self.Lambda6 + flux,
            'internal': self.Lambda6 - flux,
        }

    def maxwell_monopole_flux_density(self, R: float) -> float:
        """sqrt(g_S2) F^{theta phi} = n/(2 R^2), independent of theta."""
        _require_r(R)
        return self.n/(2*R**2)

    def flux(self) -> float:
        return 2 * pi * self.n

    def f_theta_phi(self, theta: float) -> float:
        return self.n * sin(theta) / 2

    def f_squared(self, R: float) -> float:
        _require_r(R)
        return self.n**2 / (2 * R**4)

    def jordan_potential(self, R: float) -> float:
        _require_r(R)
        return (4*pi*self.Lambda6*R**2 - 4*pi*self.K6
                + pi*self.chi6*self.n**2/(2*R**2))

    def einstein_potential_direct(self, R: float) -> float:
        return self.jordan_potential(R) * (self.R0 / R)**4


def _require_r(R: float) -> None:
    if not isfinite(R) or R <= 0:
        raise ValueError('radius must be finite and positive')


@dataclass(frozen=True)
class Extremum:
    radius: float
    kind: str  # minimum, maximum, degenerate
    value: float
    mass2_homogeneous: float

    def as_dict(self) -> dict:
        return dict(radius=self.radius, kind=self.kind, value=self.value,
                    mass2_homogeneous=self.mass2_homogeneous)


@dataclass(frozen=True)
class Potential:
    A: float
    B: float
    C: float
    K4: float

    def __post_init__(self):
        if self.A < 0 or self.B <= 0 or self.C < 0 or self.K4 <= 0:
            raise ValueError('require A >= 0, B > 0, C >= 0, K4 > 0')

    def v(self, R: float) -> float:
        _require_r(R)
        return self.A/R**2 - self.B/R**4 + self.C/R**6

    def dv(self, R: float) -> float:
        _require_r(R)
        return -2*self.A/R**3 + 4*self.B/R**5 - 6*self.C/R**7

    def d2v(self, R: float) -> float:
        _require_r(R)
        return 6*self.A/R**4 - 20*self.B/R**6 + 42*self.C/R**8

    def derivative_y(self, y: float) -> float:
        if y <= 0:
            raise ValueError('y=R^2 > 0')
        return -self.A/y**2 + 2*self.B/y**3 - 3*self.C/y**4

    def discriminant(self) -> float:
        return self.B**2 - 3*self.A*self.C

    def mass2(self, R: float) -> float:
        """Canonical radion phi = 2 sqrt(K4) ln(R/R0). Valid at extrema."""
        return R**2 * self.d2v(R) / (4 * self.K4)

    def extrema(self) -> list[Extremum]:
        # No local minimum for zero flux. The positive stationary point at
        # A>0,C=0 is an unstable maximum; R=0 is not in moduli space.
        if self.A == 0:
            if self.C == 0:
                return []
            radii = [sqrt(3*self.C/(2*self.B))]
        elif self.C == 0:
            radii = [sqrt(2*self.B/self.A)]
        else:
            disc = self.discriminant()
            # Numerically critical point is not automatically a stable vacuum.
            tolerance = 1e-13 * max(self.B**2, 3*self.A*self.C)
            if disc < -tolerance:
                return []
            if abs(disc) <= tolerance:
                radii = [sqrt(self.B/self.A)]
            else:
                delta = sqrt(disc)
                # Stable expression avoids catastrophic cancellation at C << B²/A.
                yminus = 3*self.C/(self.B+delta)
                yplus = (self.B+delta)/self.A
                radii = [sqrt(yminus), sqrt(yplus)]
        ans = []
        for R in radii:
            curvature = self.d2v(R)
            scale = max(abs(self.A/R**4), abs(self.B/R**6), abs(self.C/R**8))
            if abs(curvature) <= 1e-10 * scale:
                kind = 'degenerate'
            else:
                kind = 'minimum' if curvature > 0 else 'maximum'
            ans.append(Extremum(R, kind, self.v(R), self.mass2(R)))
        return ans

    def stable(self) -> Extremum | None:
        return next((e for e in self.extrema() if e.kind == 'minimum'), None)

    def minkowski_tuning_residual(self) -> float:
        """B^2-4AC = 0 for a flat stable minimum if A,B,C>0."""
        return self.B**2 - 4*self.A*self.C


def illustrative_six_d(n: int = 3) -> SixDimensional:
    """Chosen solely so n=3 gives A=1,B=2,C=1,K4=2 (R0=1).

    No coupling is derived from microscopic helicity or observation.
    """
    return SixDimensional(K6=1/(2*pi), Lambda6=1/(4*pi),
                          chi6=2/(9*pi), R0=1.0, n=n)


def theoretical_minkowski_parameters(n: int, K6: float, chi6: float, R0: float) -> SixDimensional:
    if n == 0:
        raise ValueError('nonzero flux required for this Minkowski solution')
    lam = 2*K6*K6/(chi6*n*n)
    return SixDimensional(K6,lam,chi6,R0,n)
