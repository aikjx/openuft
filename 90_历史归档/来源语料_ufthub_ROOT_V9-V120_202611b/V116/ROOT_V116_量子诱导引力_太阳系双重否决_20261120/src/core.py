"""ROOT V116. SI constants, natural-unit QCD and scalar-tensor audit.
Hypotheses: Jordan matter minimally/universally coupled, canonical scalar kinetic,
F(phi)=M0**2 + xi*phi**2, light scalar unless explicitly finite range.
No prediction of G or claim of a new unified field theory.
"""
import math
G_SI=6.67430e-11
C=299792458.0
HBAR=1.054571817e-34
GEV_J=1.602176634e-10
MZ=91.1876
ALPHA_S=0.1180
SIGMA_ALPHA_S=0.0009
NF=5
CASSINI_CENTRAL=2.1e-5
CASSINI_SIGMA=2.3e-5
AU_M=149597870700.0

def b0(nf=NF):
    return 11.0-2.0*nf/3

def lambda_one_loop(alpha=ALPHA_S, mu=MZ, nf=NF):
    if min(alpha,mu)<=0: raise ValueError('positive coupling and energy scale required')
    return mu*math.exp(-2*math.pi/(b0(nf)*alpha))

def Mplbar_observed():
    return math.sqrt(HBAR*C/(8*math.pi*G_SI))*C*C/GEV_J

def xi_eh_match(v=None):
    if v is None: v=lambda_one_loop()
    return (Mplbar_observed()/v)**2

def F_value(xi, v, M0sq=0.0):
    if xi<=0 or v<=0 or M0sq<0: raise ValueError('xi, v positive, bare scale squared >= 0')
    return M0sq+xi*v*v

def bd_omega(xi,v,M0sq=0.):
    F=F_value(xi,v,M0sq)
    return F/(4*xi*xi*v*v)

def alpha2_massless(xi,v,M0sq=0.):
    """Scalar-to-tensor Newton strength ratio = 1/(2omega+3)."""
    F=F_value(xi,v,M0sq)
    return 2*xi*xi*v*v/(F+6*xi*xi*v*v)

def gamma_massless(xi,v,M0sq=0.):
    a=alpha2_massless(xi,v,M0sq)
    return (1-a)/(1+a)

def gamma_from_bd(omega):
    return (omega+1)/(omega+2)

def grav_newton_F_ratio(xi,v,M0sq=0.):
    """Ratio G_N / G_* for weakly coupled universal matter, long range."""
    return 1+alpha2_massless(xi,v,M0sq)

def F_inferred_from_measured_GN(alpha2):
    """A light scalar shifts Newton calibration: F=(1+a^2)Mplbar(obs)^2."""
    return (1+alpha2)*Mplbar_observed()**2

def cassini_min_gamma(n_sigma=2.):
    return 1+CASSINI_CENTRAL-n_sigma*CASSINI_SIGMA

def cassini_delta_lower(n_sigma=2.):
    return max(0.,1-cassini_min_gamma(n_sigma))

def xi_cassini_pure_massless_bound(delta=None):
    if delta is None: delta=cassini_delta_lower()
    if delta<=0 or delta>=.5: raise ValueError('Require 0<delta<0.5')
    return delta/(4-8*delta)

def omega_cassini_bound(delta=None):
    if delta is None: delta=cassini_delta_lower()
    return 1/delta-2

def alpha2_from_omega(omega):
    return 1/(2*omega+3)

def alpha2_cassini_bound(delta=None):
    if delta is None: delta=cassini_delta_lower()
    return delta/(2-delta)

def minimal_vev_for_pure_massless_cassini(delta=None):
    """Minimum scalar VEV when it supplies all F and G_N matches measurement.
    Requires xi<=Cassini bound and universal long-range single scalar.
    """
    if delta is None: delta=cassini_delta_lower()
    xi=xi_cassini_pure_massless_bound(delta)
    a2=2*xi/(1+6*xi)
    return Mplbar_observed()*math.sqrt((1+a2)/xi)

def conservative_bare_plus_induced_xi_bound(v=None,delta=None):
    """Massless scalar and measured G_N: F <= (1+A)*Mplobs**2."""
    if v is None: v=lambda_one_loop()
    if delta is None: delta=cassini_delta_lower()
    A=alpha2_cassini_bound(delta)
    return math.sqrt(A*(1+A)*Mplbar_observed()**2/((2-6*A)*v*v))

def max_induced_fraction_bound(v=None,delta=None):
    """Conservative bound f=xi*v^2/F <= xi_bound*v^2/Mplobs^2."""
    if v is None: v=lambda_one_loop()
    return conservative_bare_plus_induced_xi_bound(v,delta)/xi_eh_match(v)

def gamma_radius(alpha2, ratio_r_to_lambda):
    return (1-alpha2*math.exp(-ratio_r_to_lambda))/(1+alpha2*math.exp(-ratio_r_to_lambda))

def effective_orbit_G_ratio(alpha2,ratio_r_to_lambda):
    x=ratio_r_to_lambda
    return 1+alpha2*(1+x)*math.exp(-x)

def gamma_fit_orbit_calibrated(alpha2,ratio_r_to_lambda):
    """Lensing normalized by Newton mass inferred at r_cal, not exact Cassini estimator."""
    t=alpha2*(1+ratio_r_to_lambda)*math.exp(-ratio_r_to_lambda)
    return (1-t)/(1+t)

def illustrative_lambda_max_over_r(alpha2,delta=None):
    """Local metric-ratio benchmark only, NOT Cassini full light path limit."""
    if delta is None: delta=cassini_delta_lower()
    if alpha2<=0: raise ValueError('alpha2>0')
    threshold=delta/(alpha2*(2-delta))
    if threshold>=1: return math.inf
    return 1/math.log(1/threshold)

def illustrative_scalar_mass_min_eV(alpha2,r_m=AU_M,delta=None):
    lam=illustrative_lambda_max_over_r(alpha2,delta)*r_m
    if math.isinf(lam): return 0.0
    return (HBAR*C/GEV_J)*1e9/lam

def solve_pure_massless_xi_match(v=None):
    """Use high precision to solve xi*v^2=(1+alpha2(xi))*Mpl(obs)^2.
    mpmath avoids loss of low digits in xi~1e39."""
    import mpmath as mp
    mp.mp.dps=75
    V=mp.mpf(str(lambda_one_loop() if v is None else v))
    Mp=mp.mpf(str(Mplbar_observed()))
    R=(Mp/V)**2
    # 6 xi^2+(1-8R)xi-R = 0; use stable rearranged positive root.
    A=8*R-1
    return (A+mp.sqrt(A*A+24*R))/12

def summary():
    v=lambda_one_loop(); xi=xi_eh_match(v); xi_limit=xi_cassini_pure_massless_bound()
    ab=alpha2_massless(xi,v)
    xi_corr=solve_pure_massless_xi_match(v)
    return dict(v_QCD_one_loop_GeV=v, Mplbar_from_measured_G_GeV=Mplbar_observed(),
        naive_xi_from_EH_coefficient=xi, alpha2_of_massless_pure_model=ab,
        omega_BD=bd_omega(xi,v),gamma_long_range=gamma_massless(xi,v),
        cassini_two_sigma_delta=cassini_delta_lower(),
        cassini_two_sigma_omega_min=omega_cassini_bound(),
        cassini_two_sigma_xi_max_pure=xi_limit,
        xi_match_correcting_GN_light_scalar=str(xi_corr),
        minimal_vev_massless_pure_Cassini_GeV=minimal_vev_for_pure_massless_cassini(),
        mass_scale_gap_xi_ratio=xi/xi_limit,
        bare_plus_induced_xi_bound=conservative_bare_plus_induced_xi_bound(v),
        bare_plus_induced_induced_fraction_bound=max_induced_fraction_bound(v),
        illustrative_1AU_lambda_over_r=illustrative_lambda_max_over_r(ab),
        illustrative_1AU_mass_lower_eV=illustrative_scalar_mass_min_eV(ab),
        experiment_kind='Cassini gamma measurement used only for MASSLESS BD 2sigma model',
        theory_status='OPEN: no independent G prediction and no unified field theory')
