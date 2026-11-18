"""ROOT V75: transparent SI Einstein-Maxwell energy-budget calculations.

Only energy-equivalence and far-field spherical toy approximations are implemented;
not a full nonlinear Einstein-Maxwell solver. All physical assumptions documented.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import pi, cos, sin, sqrt

# CODATA 2022 values, rounded to published digits (G and mu0 experimental).
C = 299_792_458.0
G = 6.67430e-11
MU0 = 1.25663706127e-6
EPS0 = 1 / (MU0 * C*C)
EARTH_G = 9.80665  # conventional acceleration, not a fitted gravitational constant


def energy_density(E: float = 0.0, B: float = 0.0) -> float:
    """Electromagnetic energy density [J/m3] in local flat-space frame."""
    return .5*(EPS0*E*E + B*B/MU0)


def volume_sphere(radius: float) -> float:
    if radius <= 0:
        raise ValueError('radius must be positive')
    return (4*pi/3)*radius**3


def energy_sphere(radius: float, E: float = 0., B: float = 0.) -> float:
    """Ideal energy within region. This ignores field outside and source hardware."""
    return volume_sphere(radius)*energy_density(E, B)


def equivalent_mass(energy_joule: float) -> float:
    """Energy equivalent [kg], NOT an independent G prediction."""
    return energy_joule/(C*C)


def toy_external_gravity_from_energy(energy_joule: float, r: float) -> float:
    """Spherically symmetric far-field energy-equivalent g [m/s2], r>source size.

    WARNING: assumes balanced, isolated total source with modeled added net energy.
    It is not a complete local Einstein-Maxwell stress analysis.
    """
    if r <= 0:
        raise ValueError('r must be positive')
    return G*equivalent_mass(energy_joule)/r**2


def toy_metric_h00(energy_joule: float, r: float) -> float:
    """Magnitude |h00| = 2 G U/(c4 r) for weak static point monopole."""
    if r <= 0:
        raise ValueError('r must be positive')
    return 2*G*energy_joule/(C**4*r)


def faraday_azimuthal_e(r_perp: float, db_dt: float) -> float:
    """Quasi-static axial B(t) -> induced azimuthal E = -r_perp/2 dB/dt."""
    if r_perp < 0:
        raise ValueError('r_perp must be nonnegative')
    return -.5*r_perp*db_dt


def quasi_static_sphere_energies(B_peak: float, f_hz: float, radius: float, t_s: float) -> dict:
    """Axial B=B0 cos(2pi f t) in ideal spherical region.

    Faraday E(r_perp)= -r_perp/2 * Bdot. Spatial integral of E^2 is analytic.
    Only meaningful in quasi-static regime 2pi*f*radius/c << 1; excludes hardware,
    external fields, currents and radiation losses.
    """
    if f_hz < 0:
        raise ValueError('frequency must be nonnegative')
    vol = volume_sphere(radius)
    omega = 2*pi*f_hz
    b = B_peak*cos(omega*t_s)
    bdot = -omega*B_peak*sin(omega*t_s)
    ub = vol*b*b/(2*MU0)
    ue = EPS0*vol*radius**2*bdot**2/20
    return dict(B_tesla=b, dB_dt_tesla_per_s=bdot,
                U_B_joule=ub, U_E_induced_joule=ue,
                U_total_joule=ub+ue, quasistatic_parameter=omega*radius/C)


def quasi_static_average(B_peak: float, f_hz: float, radius: float) -> dict:
    if f_hz < 0:
        raise ValueError('frequency must be nonnegative')
    vol=volume_sphere(radius)
    om=2*pi*f_hz
    ub=vol*B_peak**2/(4*MU0)
    ue=EPS0*vol*radius**2*om**2*B_peak**2/40
    return dict(average_B_energy_joule=ub,
                average_induced_E_energy_joule=ue,
                average_total_joule=ub+ue,
                ratio_induced_to_B=(om*radius/C)**2/10 if B_peak else 0.,
                quasistatic_parameter=om*radius/C)


def em_invariants_si(evec: tuple, bvec: tuple) -> dict:
    """I1 = 2(B²-E²/c²) in Tesla²; pseudoscalar P=E·B/c in Tesla².
    I1=0=P for null electromagnetic waves, even when energy density >0.
    """
    if len(evec)!=3 or len(bvec)!=3:
        raise ValueError('expect 3-vectors')
    e2=sum(a*a for a in evec); b2=sum(a*a for a in bvec)
    dot=sum(a*b for a,b in zip(evec,bvec))
    return {'I1_T2': 2*(b2-e2/(C*C)), 'P_T2':dot/C,
            'u_J_m3':.5*(EPS0*e2+b2/MU0)}


def scalar_photon_equation_source(F_squared_natural: float, Lambda: float) -> float:
    """RHS F_mu_nu F^mu_nu/(4 Lambda) for scalar EFT, natural units."""
    if Lambda == 0:
        raise ValueError('Lambda nonzero')
    return F_squared_natural/(4*Lambda)


def scalar_static_homogeneous_phi(F_squared_natural: float, Lambda: float, m: float) -> float:
    """Toy static/constant solution at R=0: phi=-F²/(4 Lambda m²).
    Discards gradients, boundaries and source stress. Not a parameter prediction.
    """
    if m <= 0:
        raise ValueError('mass must be positive')
    return -scalar_photon_equation_source(F_squared_natural,Lambda)/(m*m)


def grav_coupling_ratio(phi: float, xi: float, Mstar: float=1.) -> float:
    """Effective tensor action coefficient ratio; NOT laboratory Cavendish G."""
    F=Mstar*Mstar+xi*phi*phi
    if F <= 0:
        raise ValueError('nonpositive graviton kinetic coefficient')
    return Mstar*Mstar/F
