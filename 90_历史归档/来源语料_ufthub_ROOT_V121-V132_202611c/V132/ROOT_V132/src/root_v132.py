"""ROOT V132 - tests of speed-one helix geometry vs fine structure.
Physics convention throughout proofs: c=1, while hbar and G remain independent.
SI c is used ONLY for reporting measured lengths/energies in SI units.
"""
from __future__ import annotations
import math
from dataclasses import dataclass

ALPHA_INV_CODATA22 = 137.035999177
ALPHA_INV_SIGMA = 0.000000021
ALPHA_CODATA22 = 1.0 / ALPHA_INV_CODATA22
HBAR_SI = 1.0545718176461565e-34  # h/(2pi) J s, exact under defined h
H_PLANCK_SI = 6.62607015e-34
C_FOR_SI_CONVERSIONS = 299792458.0
M_E_SI = 9.1093837139e-31
E_CHARGE = 1.602176634e-19
EPS0_SI_2022_APPROX = 8.8541878188e-12

@dataclass(frozen=True)
class Helix:
    radius: float
    omega: float
    axial_speed: float

    def __post_init__(self):
        assert self.radius > 0 and self.omega > 0

    @property
    def total_speed(self):
        return math.hypot(self.radius*self.omega, self.axial_speed)

    @property
    def kappa(self):
        return self.radius*self.omega*self.omega / (self.total_speed**2)

    @property
    def tau(self):
        return self.axial_speed*self.omega / (self.total_speed**2)

    @property
    def omega_geometry(self):
        return self.total_speed*math.hypot(self.kappa, self.tau)

    @property
    def h_geo(self):
        return self.tau/math.hypot(self.kappa, self.tau)

    @property
    def normalized_curvature(self):
        return self.kappa/math.hypot(self.kappa, self.tau)

    @property
    def pitch(self):
        return 2*math.pi*self.axial_speed/self.omega

    @property
    def length_per_turn(self):
        return 2*math.pi*self.total_speed/self.omega

    @property
    def curvature_per_turn(self):
        return self.kappa*self.length_per_turn

    @property
    def torsion_per_turn(self):
        return self.tau*self.length_per_turn

    def boosted_axial(self, beta:float) -> 'Helix':
        """Boost applied to a null 3D trajectory; not a mass-bearing worldline."""
        assert abs(beta)<1
        assert abs(self.total_speed-1)<1e-11
        new_u=(self.axial_speed-beta)/(1-beta*self.axial_speed)
        new_omega=self.omega*math.sqrt(1-beta*beta)/(1-beta*self.axial_speed)
        # transverse radius unchanged under boost parallel to axis
        return Helix(self.radius,new_omega,new_u)


def from_kappa_tau(kappa:float,tau:float) -> Helix:
    """Inverse geometry for a speed-one right-handed helix; no new dynamics."""
    assert kappa>0
    omega=math.hypot(kappa,tau)
    radius=kappa/(omega*omega)
    return Helix(radius,omega,tau/omega)


def helix_for_geo_alpha(alpha:float, radius:float=1.0, mapping:str='axial') -> Helix:
    """Fine structure value *inserted* as a kinematic ratio, not predicted."""
    assert 0<alpha<1 and radius>0
    if mapping=='axial':
        u=alpha
        vt=math.sqrt(1-alpha*alpha)
    elif mapping=='transverse':
        u=math.sqrt(1-alpha*alpha)
        vt=alpha
    else: raise ValueError(mapping)
    return Helix(radius,vt/radius,u)


def bohr_radius_si():
    return HBAR_SI/(M_E_SI*C_FOR_SI_CONVERSIONS*ALPHA_CODATA22)


def reduced_compton_si():
    return HBAR_SI/(M_E_SI*C_FOR_SI_CONVERSIONS)


def bohr_energy_ev():
    return 0.5*M_E_SI*C_FOR_SI_CONVERSIONS**2/E_CHARGE*ALPHA_CODATA22**2


def h_geometry_action(h_geo:float, hbar:float=HBAR_SI):
    """Illustrative action construction. Explicitly imports hbar; not its derivation."""
    return 2*math.pi*hbar*h_geo


def quantum_wire_geometric_potential(mass_kg:float, curvature_inv_m:float):
    """da Costa constrained nondegenerate scalar curve mode (SI for numerical report)."""
    return -(HBAR_SI**2 * curvature_inv_m**2)/(8*mass_kg)


def alpha_from_charge_si():
    return E_CHARGE**2/(4*math.pi*EPS0_SI_2022_APPROX*HBAR_SI*C_FOR_SI_CONVERSIONS)


def standard_born_spectrum_ratio(alpha:float):
    """Fine structure relative scale in hydrogenic perturbation theory ~alpha^2."""
    return alpha*alpha


def velocity_addition(u:float,beta:float):
    return (u-beta)/(1-beta*u)


def interval_for_alpha_inv():
    """One-sigma α interval from inverse CODATA one-sigma value."""
    return 1/(ALPHA_INV_CODATA22+ALPHA_INV_SIGMA),1/(ALPHA_INV_CODATA22-ALPHA_INV_SIGMA)


def wilson_link(tau:float, length:float, mode_charge:int=1) -> complex:
    """Wilson phase only if waveguide supports an applicable (degenerate) mode."""
    z=mode_charge*tau*length
    return complex(math.cos(z),math.sin(z))


if __name__=='__main__':
    h=helix_for_geo_alpha(ALPHA_CODATA22)
    print('alpha=',ALPHA_CODATA22,'kappa=',h.kappa,'tau=',h.tau)
    print('bohr radius SI=',bohr_radius_si(),'reduced Compton=',reduced_compton_si())
