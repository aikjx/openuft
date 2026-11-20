"""ROOT V115: auditable one-loop QCD/QED trace anomaly and induced gravity.
Natural units hbar=c=1 for RG and field theory. GeV denotes energy, not SI mass.
Model examples are established EFT identities, NOT derivation of unified gravity.
"""
from dataclasses import dataclass
import math

# 2025 Particle Data Group alpha_s(M_Z)=0.1180±0.0009; these are INPUTS.
ALPHA_S_MZ = 0.1180
ALPHA_S_MZ_SIGMA = 0.0009
MZ_GEV = 91.1876
HBAR_SI = 1.054571817e-34
C_SI = 299792458.0
G_SI = 6.67430e-11
GEV_J = 1.602176634e-10
GEV_MASS_KG = GEV_J / C_SI**2
ALPHA_EM_LOW = 1 / 137.035999084  # separate low-energy example, not matched at M_Z


def beta0_qcd(nf: int) -> float:
    if not isinstance(nf, int) or nf < 0 or nf > 16:
        raise ValueError('nf must be integer from 0 to 16 for asymptotic freedom')
    return 11.0 - 2.0 * nf/3.0


def beta_alpha_qcd(alpha: float, nf: int) -> float:
    if not math.isfinite(alpha) or alpha <= 0:
        raise ValueError('alpha must be finite positive')
    return -beta0_qcd(nf)*alpha*alpha/(2*math.pi)


def run_alpha_one_loop(mu: float, mu0: float, alpha0: float, nf: int) -> float:
    """One-loop fixed-nf MS-like toy running (no heavy-quark threshold matching)."""
    if min(mu,mu0,alpha0) <= 0 or not all(map(math.isfinite,[mu,mu0,alpha0])):
        raise ValueError('mu, mu0, alpha0 must be positive and finite')
    inverse = 1/alpha0 + beta0_qcd(nf)/(2*math.pi)*math.log(mu/mu0)
    if inverse <= 0: raise ValueError('one-loop Landau-analogue pole / outside perturbative branch')
    return 1.0/inverse


def lambda_qcd_one_loop(mu: float, alpha: float, nf: int) -> float:
    """One-loop integration constant, scheme and threshold dependent. Not a hadron mass!"""
    if mu <= 0 or not math.isfinite(mu) or alpha<=0 or not math.isfinite(alpha):
        raise ValueError('invalid scale or coupling')
    return mu*math.exp(-2*math.pi/(beta0_qcd(nf)*alpha))


def lambda_log_sensitivity(alpha: float, nf: int) -> float:
    """d log Lambda / d alpha at fixed mu, nf."""
    if alpha <= 0: raise ValueError('alpha positive')
    return 2*math.pi/(beta0_qcd(nf)*alpha**2)


def qcd_beta_over_2g(alpha: float, nf: int) -> float:
    """Gauge-field trace anomaly coefficient (canonical G^2), leading loop."""
    if alpha<=0: raise ValueError('positive alpha required')
    return -beta0_qcd(nf)*alpha/(8*math.pi)


def qed_beta_over_2e(alpha: float, sum_charges_squared: float=1.0) -> float:
    """One-loop pure QED, Dirac species; convention Ttrace=(beta/2e) F^2."""
    if alpha<=0 or sum_charges_squared<0: raise ValueError('invalid QED inputs')
    return alpha*sum_charges_squared/(6*math.pi)


def beta_alpha_qed(alpha: float, sum_charges_squared: float=1.0) -> float:
    if alpha<=0 or sum_charges_squared<0: raise ValueError('invalid QED inputs')
    return 2*sum_charges_squared*alpha**2/(3*math.pi)


def qcd_trace_coefficient_ratio(alpha_s:float,nf:int,alpha_em:float,sumq2:float=1.) -> float:
    """Toy ratio of coefficients of differently normalized operators G^2 and F^2,
    NOT a physical hadron-to-photon scattering ratio. Both couplings must be
    supplied at common scale in the same toy gauge theory with active matter.
    """
    return qcd_beta_over_2g(alpha_s,nf)/qed_beta_over_2e(alpha_em,sumq2)


def reduced_planck_mass_kg() -> float:
    """Derived from MEASURED G, not predicted. 0 / Mbar_P^2 = 8*pi*G / (hbar*c)."""
    return math.sqrt(HBAR_SI*C_SI/(8*math.pi*G_SI))


def reduced_planck_mass_gev() -> float:
    return reduced_planck_mass_kg()/GEV_MASS_KG


def induced_planck_mass_gev(v_gev:float,zeta:float) -> float:
    """For effective action sqrt(-g)*(zeta/2)*phi^2 R, <phi>=v."""
    if v_gev<=0 or zeta<=0: raise ValueError('positive scalar scale and nonminimal coupling')
    return math.sqrt(zeta)*v_gev


def required_induced_zeta(v_gev:float) -> float:
    if v_gev<=0: raise ValueError('positive scalar VEV required')
    return (reduced_planck_mass_gev()/v_gev)**2


def induced_G_ratio_to_observed(v_gev:float,zeta:float) -> float:
    """Dimensionless G_effective/G_measured at same unit conventions."""
    return (reduced_planck_mass_gev()/induced_planck_mass_gev(v_gev,zeta))**2


def einstein_scalar_trace_curvature(trace_gev4:float,planck_reduced_gev:float=None) -> float:
    """Trace Einstein equation with cosmological constant=0: R=-T/Mbar^2.
    This is not full Einstein field equation; can be zero while Ricci nonzero.
    """
    p = reduced_planck_mass_gev() if planck_reduced_gev is None else planck_reduced_gev
    if p<=0: raise ValueError('Planck scale >0')
    return -trace_gev4/p**2


def scalar_mass_gev_from_renormalized_coupling(mu0:float,alpha0:float,nf:int, kappa:float):
    """Toy dynamical scale v=kappa Lambda. kappa is an independent free factor."""
    if kappa<=0: raise ValueError('kappa positive')
    return kappa*lambda_qcd_one_loop(mu0,alpha0,nf)


def example_inputs():
    n=5; al=ALPHA_S_MZ
    lam=lambda_qcd_one_loop(MZ_GEV,al,n)
    return {
        'nf_fixed':n,'mu0_GeV':MZ_GEV,'alpha_s_input':al,
        'alpha_s_input_sigma':ALPHA_S_MZ_SIGMA,
        'b0':beta0_qcd(n),'one_loop_Lambda5_GeV':lam,
        'one_loop_QCD_beta_alpha':beta_alpha_qcd(al,n),
        'one_loop_QCD_trace_G2_coeff':qcd_beta_over_2g(al,n),
        'one_Dirac_low_energy_QED_trace_F2_coeff':qed_beta_over_2e(ALPHA_EM_LOW),
        'Mbar_pl_from_G_GeV_not_a_prediction':reduced_planck_mass_gev(),
        'required_zeta_if_v_eq_one_loop_Lambda5':required_induced_zeta(lam),
        'predicted_G_over_measured_if_zeta_1_and_v_eq_Lambda5':induced_G_ratio_to_observed(lam,1.0),
        'RG_scale_log_sensitivity_dlnLambda_dalpha':lambda_log_sensitivity(al,n),
        'one_sigma_rel_linear_Lambda_uncertainty':lambda_log_sensitivity(al,n)*ALPHA_S_MZ_SIGMA,
    }
