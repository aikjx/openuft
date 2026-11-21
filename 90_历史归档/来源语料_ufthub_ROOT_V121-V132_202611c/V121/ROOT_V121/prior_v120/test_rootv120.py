import math
import numpy as np
from rootv120 import (
 R_EARTH, ground_fraction, apparent_gm, finite_spectrum,
 relative_yukawa, two_range_gm, fit_profile_gls, formfactor_times_exp,
 near_circular_precession_rad, extra_clock_shift)

ELL=124600.
STEP=50000.
HEIGHTS=np.arange(7)*STEP
EPS=ground_fraction()

def test_uniform_and_improved_formfactor():
    assert abs(ground_fraction(model='uniform') - 0.009774944408993123) < 1e-13
    assert abs(EPS - 0.005954404898918548) < 1e-13
    assert formfactor_times_exp(R_EARTH/ELL, 'improved') > 0

def test_five_height_prony_high_precision():
    # Avoid subtractive cancellation from float K~1 by independent mpmath reference.
    import mpmath as mp
    mp.mp.dps=90
    ell=mp.mpf(124600); step=mp.mpf(50000); r=mp.mpf(6371000)
    q=mp.exp(-step/ell)
    K=[mp.mpf(1)+mp.mpf('0.005954404898918548')*
       (1+(r+n*step)/ell)/(1+r/ell)*mp.exp(-n*step/ell) for n in range(6)]
    D=[K[n+1]-K[n] for n in range(5)]
    H=D[0]*D[2]-D[1]**2; J=D[0]*D[3]-D[1]*D[2]
    assert abs(J/(2*H)-q) < mp.mpf('1e-70')
    assert abs(D[0]*J**2-4*D[1]*J*H+4*D[2]*H*H)<mp.mpf('1e-70')

def test_five_height_float_noise_free():
    K=apparent_gm(HEIGHTS,ELL,epsilon_ground=EPS)
    s=finite_spectrum(K,STEP)
    assert all(s.H < 0)
    assert abs(s.ell_five_m/ELL-1)<1e-7
    assert abs(s.ell_six_m/ELL-1)<1e-7
    assert abs(s.yukawa_shape_residual)<1e-4  # near-cancellation in binary64

def test_needs_six_for_h_ratio():
    s=finite_spectrum(apparent_gm(HEIGHTS[:5],ELL,epsilon_ground=EPS),STEP)
    assert math.isnan(s.ell_six_m)
    assert math.isfinite(s.ell_five_m)

def test_general_repeated_root_not_same_as_yukawa():
    q=math.exp(-STEP/ELL)
    n=np.arange(6)
    K=1+(0.006+0.0004*n)*q**n
    s=finite_spectrum(K,STEP)
    assert abs(s.ell_five_m/ELL-1)<1e-6
    assert abs(s.yukawa_shape_residual)>1 # Only the broader family passes.

def test_two_range_counterexample():
    K=two_range_gm(HEIGHTS,ELL,300000.,epsilon_ground=EPS)
    s=finite_spectrum(K,STEP)
    assert s.H[0]>0

def test_exact_profile_fit():
    K=apparent_gm(HEIGHTS,ELL,epsilon_ground=EPS)
    fit=fit_profile_gls(K,HEIGHTS)
    assert abs(fit['ell_m']-ELL)<0.5
    assert abs(fit['A']-1)<1e-8

def test_dynamic_precession_and_clocks():
    d=near_circular_precession_rad(400000.,ELL,EPS)
    assert abs(d-0.043181850686491004)<1e-12
    clock=extra_clock_shift(0.,400000.,ELL,EPS)
    assert abs(clock-7.649235793665662e-14)<1e-22

def test_zero_amplitude_unidentifiable():
    K=np.ones(6)
    s=finite_spectrum(K,STEP)
    assert math.isnan(s.ell_five_m)

def test_invalid_five_samples():
    import pytest
    with pytest.raises(ValueError):
        finite_spectrum(np.ones(4),STEP)

def test_fixed_confirmatory_model_does_not_refit_alpha_or_lambda():
    from rootv120 import fixed_hypothesis_gls
    h=np.arange(6)*STEP
    k=apparent_gm(h,ELL,epsilon_ground=EPS)
    result=fixed_hypothesis_gls(k,h,1e-14*np.eye(len(h)))
    assert result['fixed_candidate']['chi2']<1e-10
    assert result['newtonian_null']['chi2']>1e8
    null=fixed_hypothesis_gls(np.ones_like(k),h,1e-14*np.eye(len(h)))
    assert null['newtonian_null']['chi2']<1e-10
    assert null['fixed_candidate']['chi2']>1e8
