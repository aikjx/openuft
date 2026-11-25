"""c=1 kinematic geometry and CODATA reference audit.
SI numbers below are used only when comparing to published SI measurements;
the theoretical unit convention sets ONLY c=1, retaining hbar and G.
"""
from dataclasses import dataclass
import math

# NIST CODATA 2022, source links in REFERENCES.md.
ALPHA = 7.2973525643e-3
ALPHA_STD = 1.1e-12
G_SI = 6.67430e-11
G_SI_STD = 0.00015e-11
H_SI = 6.62607015e-34
HBAR_SI = H_SI / (2.0 * math.pi)
C_SI_TO_CONVERT = 299792458.0  # SI conversion ONLY: theoretical calculations use c=1.
ME_SI = 9.1093837139e-31


@dataclass(frozen=True)
class Helix:
    a: float
    omega: float
    u: float

    def __post_init__(self):
        if not (math.isfinite(self.a) and math.isfinite(self.omega) and math.isfinite(self.u)):
            raise ValueError('non-finite helix parameter')
        if self.a <= 0.0 or self.omega <= 0.0:
            raise ValueError('require nondegenerate a>0 and omega>0')
        if abs(self.speed2() - 1.0) > 5e-11:
            raise ValueError('not a null (c=1) spatial-speed helix')
        if abs(self.u) >= 1.0:
            raise ValueError('axial speed must be subluminal')

    def speed2(self) -> float:
        return (self.a * self.omega) ** 2 + self.u**2

    def tangent(self, t: float):
        return (-self.a * self.omega * math.sin(self.omega*t),
                 self.a * self.omega * math.cos(self.omega*t), self.u)

    def position(self, t: float):
        return (self.a * math.cos(self.omega*t), self.a * math.sin(self.omega*t), self.u*t)

    def acceleration(self,t:float):
        return (-self.a*self.omega**2*math.cos(self.omega*t),
                -self.a*self.omega**2*math.sin(self.omega*t),0.0)

    def curvature(self) -> float:
        return self.a * self.omega**2

    def torsion(self) -> float:
        return self.u*self.omega

    def alpha_proxy(self) -> float:
        k, t = self.curvature(), self.torsion()
        return k*k/(k*k+t*t)

    def boost_z(self,beta:float):
        if not (-1 < beta < 1):
            raise ValueError('beta must be subluminal')
        gamma=1.0/math.sqrt((1-beta)*(1+beta))
        denom=gamma*(1-beta*self.u)
        return Helix(self.a,self.omega/denom,(self.u-beta)/(1-beta*self.u))


def helix_for_alpha(target:float=ALPHA,omega:float=1.0) -> Helix:
    if not (0.0 < target < 1.0) or omega <= 0.0:
        raise ValueError('target in (0,1) and omega > 0 needed')
    return Helix(math.sqrt(target)/omega, omega, math.sqrt(1.0-target))


def gravitational_fine_structure_electron():
    """G*m_e^2/(hbar*c_SI), matching G*m_e^2/hbar in c=1 units."""
    return G_SI*ME_SI**2/(HBAR_SI*C_SI_TO_CONVERT)


def q_ed_relation():
    """HL normalization in c=1: charge coupling square / hbar = 4*pi*alpha."""
    return 4*math.pi*ALPHA


def wave(t,z,k=2.0,amplitude=1.0):
    """Exact +z circularly polarized Maxwell plane wave in Heaviside-Lorentz c=1."""
    p=k*(t-z)
    e=(amplitude*math.cos(p),amplitude*math.sin(p),0.0)
    b=(-amplitude*math.sin(p),amplitude*math.cos(p),0.0)
    return e,b


def wave_residuals(t,z,k=2.0,amplitude=1.0):
    """Return analytic Faraday and Ampere-Maxwell residuals, and invariants."""
    p=k*(t-z)
    # time derivative B; curl E for functions depending on z only
    dtb=(-amplitude*k*math.cos(p),-amplitude*k*math.sin(p),0.)
    curl_e=(amplitude*k*math.cos(p),amplitude*k*math.sin(p),0.)
    dte=(-amplitude*k*math.sin(p),amplitude*k*math.cos(p),0.)
    curl_b=(-amplitude*k*math.sin(p),amplitude*k*math.cos(p),0.)
    e,b=wave(t,z,k,amplitude)
    faraday=tuple(x+y for x,y in zip(dtb,curl_e))
    ampere=tuple(x-y for x,y in zip(dte,curl_b))
    dot=sum(x*y for x,y in zip(e,b))
    i1=sum(x*x for x in b)-sum(x*x for x in e)
    flux=e[0]*b[1]-e[1]*b[0]
    return faraday,ampere,dot,i1,flux


def diagnostic():
    h=helix_for_alpha()
    hp=h.boost_z(h.u)
    g=gravitational_fine_structure_electron()
    return {
        'units':'c=1 only; hbar and G dimensional and independent',
        'CODATA_2022_alpha':ALPHA,
        'CODATA_2022_alpha_std':ALPHA_STD,
        'CODATA_2022_inverse_alpha':1/ALPHA,
        'fit_input_alpha':ALPHA,
        'fit_helix_a_L':h.a,
        'fit_helix_u':h.u,
        'lab_kappa_Linverse':h.curvature(),
        'lab_tau_Linverse':h.torsion(),
        'lab_alpha_proxy':h.alpha_proxy(),
        'axial_comoving_beta':h.u,
        'boost_kappa_Linverse':hp.curvature(),
        'boost_tau_Linverse':hp.torsion(),
        'boost_omega_Linverse':hp.omega,
        'boost_alpha_proxy':hp.alpha_proxy(),
        'alpha_proxy_frame_change':hp.alpha_proxy()-h.alpha_proxy(),
        'electron_gravity_dimensionless_c1':g,
        'alpha_to_electron_gravity_ratio':ALPHA/g,
        'one_half_of_alpha_g_KK':4*g,
        'alpha_to_simple_4alpha_g_KK_ratio':ALPHA/(4*g),
        'QED_4pi_alpha_hbar_normalized':q_ed_relation(),
        'physical_status':'Mathematical counterexample, not an experimental test of ROOT.'
    }
