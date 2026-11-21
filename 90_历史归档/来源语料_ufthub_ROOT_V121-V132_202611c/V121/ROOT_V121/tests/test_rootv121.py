"""Physics/mathematics guardrail tests for ROOT V121. No real observations."""
import os, sys, math
import numpy as np
import pytest
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','scripts'))
import rootv121 as r
from rootv120 import (R_EARTH, ELL_PRE_REGISTERED, apparent_gm,
                      ground_fraction, finite_spectrum, two_range_gm,
                      extra_clock_shift, relative_yukawa)

H=np.arange(6)*50000.
EPS=ground_fraction()

@pytest.mark.parametrize('h', [0,50000,100000,200000,400000,710000,1000000])
def test_slope_precession_independent_derivations(h):
    expected=r.precession_from_fixed_model(h)
    actual=r.precession_from_slope(r.log_slope_K(h))
    assert abs(actual-expected) < 3e-14

@pytest.mark.parametrize('h', [0,200000,400000,710000])
def test_log_slope_matches_finite_difference(h):
    f=lambda x: math.log(float(1+r.yukawa_epsilon(x)))
    dr=100.0
    numeric=(f(h+dr)-f(h-dr))/(2*dr)*(R_EARTH+h)
    assert abs(numeric-r.log_slope_K(h))<5e-8

def test_ratio_cancels_unknown_common_gm():
    a,b=250000,400000
    ka=apparent_gm(np.array([a,b],float),ELL_PRE_REGISTERED,mu=1.)
    kb=apparent_gm(np.array([a,b],float),ELL_PRE_REGISTERED,mu=1e18)
    assert abs(ka[0]/ka[1]-kb[0]/kb[1])<1e-14
    assert abs(ka[0]/ka[1]-r.mu_free_altitude_ratio(a,b))<1e-14

def test_250_400_signal_is_nonzero_and_large_in_candidate():
    assert 0.0005 < r.mu_free_altitude_ratio(250000,400000)-1 < 0.0007

def test_three_height_exact_recovery():
    h=np.array([0,100000,200000])
    k=apparent_gm(h,ELL_PRE_REGISTERED,mu=1.000003)
    ell=r.recover_ell_three(0,100000,k)
    assert abs(ell-ELL_PRE_REGISTERED)<1e-3

def test_three_height_shape_monotonic():
    ells=[65000,125000,250000,500000]
    ratios=[r.three_height_ratio(0,50000,ell) for ell in ells]
    assert all(ratios[i]>ratios[i+1] for i in range(len(ratios)-1))

def test_three_height_recovery_rejects_invalid_ratio():
    assert math.isnan(r.recover_ell_three(0,100000,np.array([1,2,3])))

def test_three_height_input_validation():
    with pytest.raises(ValueError):r.recover_ell_three(0,0,[1,2,3])
    with pytest.raises(ValueError):r.recover_ell_three(0,100,[1,2])


def test_five_height_repeat_root_constraint():
    k=apparent_gm(H,ELL_PRE_REGISTERED)
    s=r.five_height_prony(k[:5],50000.)
    assert s['H0']<0
    assert abs(s['ell_m']/ELL_PRE_REGISTERED-1)<1e-7
    # Absolute residual is tiny; relative residual is roughly at float roundoff.
    assert abs(s['P5'])<1e-20


def test_five_height_non_yukawa_false_positive():
    n=np.arange(5)
    q=math.exp(-50000/ELL_PRE_REGISTERED)
    K=1+(0.006+0.0004*n)*q**n
    s=r.five_height_prony(K,50000.)
    assert s['H0']<0 and 0<s['q']<1
    shape=finite_spectrum(K,50000.)
    assert abs(shape.yukawa_shape_residual)>1


def test_two_range_sign_is_not_universal():
    examples=r.two_scale_counterexamples()
    assert examples[0]['H0']<0
    assert examples[2]['H0']>0
    assert all(math.isfinite(x['recovered_ell_m']) for x in examples)


def test_precession_400km_reference():
    assert abs(r.precession_from_slope(r.log_slope_K(400000))-0.043181850686491)<1e-12


def test_clock_extra_reference():
    assert abs(extra_clock_shift(0,400000,ELL_PRE_REGISTERED,EPS)-7.649235793665662e-14)<1e-21


def test_alpha_numerology_is_falsified_against_CODATA2022():
    a=r.alpha_numerology_audit()
    assert a['difference_in_CODATA_std']>10000
    assert 2<a['relative_error_ppm']<3


def test_proton_relation_is_arithmetically_false():
    p=r.proton_ratio_audit()
    assert abs(p['expression_2pi_3cubed_plus_2pi']-56*math.pi)<1e-12
    assert abs(p['difference'])>1600


def test_simple_single_radius_kk_integer_mass_ratio_does_not_match_proton():
    p=r.proton_ratio_audit()
    assert abs(r.kk_mass_level_ratio(1,1836)-p['CODATA2022_mp_over_me'])>0.1
    assert p['gap_to_integer']>0.15


def test_helix_violation_for_c_transverse_plus_nonzero_axial():
    c=r.C_LIGHT
    assert r.helix_speed(c,0)==c
    assert r.helix_speed(c,0.3*c)>c


def test_helix_closure_enforced():
    c=r.C_LIGHT
    for beta in [0.,.2,.5,.9]:
        vth=c*math.sqrt(1-beta*beta)
        assert abs(r.helix_speed(vth,beta*c)/c-1)<1e-14


def test_unphysical_slope_flagged():
    assert math.isnan(r.precession_from_slope(-1))


def test_fixed_template_rejects_newtonian_synthetic():
    h=H
    cov=1e-14*np.eye(len(h))
    null=r.gaussian_chi2_null_vs_fixed(h,np.ones_like(h),cov)
    assert null['newtonian_null']['chi2']<1e-7
    assert null['fixed']['chi2']>1e5


def test_fixed_template_matches_yukawa_synthetic():
    h=H
    cov=1e-14*np.eye(len(h))
    a=r.gaussian_chi2_null_vs_fixed(h,apparent_gm(h,ELL_PRE_REGISTERED),cov)
    assert a['fixed']['chi2']<1e-7
    assert a['newtonian_null']['chi2']>1e5


def test_correlated_covariance_whitening_works():
    h=H
    C=1e-12*(0.5*np.eye(len(h))+0.5*np.ones((len(h),len(h))))
    template=1+r.yukawa_epsilon(h)
    noise=np.array([0,1,-1,2,-2,1])*1e-7
    z=r.whitened_model_residuals(template+noise,template,C)
    assert len(z)==len(h)
    assert np.all(np.isfinite(z))


def test_predictions_decrease_with_height():
    v=r.fixed_prediction_table([0,100000,250000,400000,1000000])
    assert all(v[i]['epsilon']>v[i+1]['epsilon'] for i in range(len(v)-1))
    assert all(x['d_lnK_d_lnr']<0 for x in v)


def test_invalid_five_height_length():
    with pytest.raises(ValueError):r.five_height_prony(np.ones(6),50000)
