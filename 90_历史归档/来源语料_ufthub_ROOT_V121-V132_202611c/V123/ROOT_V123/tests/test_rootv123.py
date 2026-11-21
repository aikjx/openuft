"""Scientific unit tests: mathematical identities and SYNTHETIC observations only."""
import math
import numpy as np
import pytest
from scipy.integrate import quad
from rootv120 import R_EARTH, ELL_PRE_REGISTERED, ground_fraction, relative_yukawa
from rootv122 import epsilon
from rootv123 import (weighted_offset_fraction, adjacent_difference_ratio,
                       ratio_from_three,three_height_shape_bounds,
                       invert_three_heights, synthetic_three,recover_windows,
                       gaussian_ratio_uncertainty,inverse_condition_number,
                       synthetic_mc,compare_synthetic_single_double,
                       orbit_comparison)

@pytest.mark.parametrize('z',[0.,1e-10,1e-6,1e-4,.01,.1,.6,1.,10.,100.,700.])
def test_weight_mean_range(z):
    t=weighted_offset_fraction(z)
    assert 0<=t<=.5

@pytest.mark.parametrize('z',[.0001,.01,.2,1.,3.,12.])
def test_weight_mean_matches_quadrature(z):
    a=quad(lambda t:math.exp(-z*t),0,1)[0]
    b=quad(lambda t:t*math.exp(-z*t),0,1)[0]
    assert math.isclose(weighted_offset_fraction(z),b/a,rel_tol=4e-11,abs_tol=1e-12)

@pytest.mark.parametrize('ell',[3e4,7e4,124600.,3e5,1e6,1e7])
@pytest.mark.parametrize('step',[5e4,1e5])
def test_integral_ratio_with_relative_shape(ell,step):
    r=R_EARTH;d=step
    vals=synthetic_three(r,d,ell,amplitude=.015)
    Q=ratio_from_three(vals)
    assert math.isclose(Q,adjacent_difference_ratio(1/ell,r,d),rel_tol=2e-8)

@pytest.mark.parametrize('ell',[3e4,7e4,124600.,3e5,1e6,1e7])
@pytest.mark.parametrize('step',[5e4,1e5])
@pytest.mark.parametrize('amplitude',[.005,-.04])
def test_three_height_inverse_unique(ell,step,amplitude):
    r=R_EARTH
    vals=synthetic_three(r,step,ell,amplitude=amplitude)
    fit=invert_three_heights(vals,r,step)
    assert math.isclose(fit['ell_m'],ell,rel_tol=4e-8)
    assert fit['ell_lower']<ell<fit['ell_upper']

@pytest.mark.parametrize('ell',[3e4,1.246e5,1e6])
def test_ratio_monotonic(ell):
    k=1/ell;r=R_EARTH;d=5e4
    assert adjacent_difference_ratio(k*.99,r,d)>adjacent_difference_ratio(k,r,d)
    assert adjacent_difference_ratio(k*1.01,r,d)<adjacent_difference_ratio(k,r,d)

@pytest.mark.parametrize('r',[1e6,R_EARTH,1e8])
def test_ratio_endpoints(r):
    d=100000.
    Q0=adjacent_difference_ratio(0,r,d)
    assert math.isclose(Q0,(r+1.5*d)/(r+.5*d),rel_tol=1e-14)
    assert adjacent_difference_ratio(10/d,r,d)<Q0

@pytest.mark.parametrize('triple',[ [1.,1.,1.], [1.,2.,1.],[1.,1.,2.],[1.,1.0001,.9999]])
def test_invalid_triples(triple):
    with pytest.raises(ValueError):
        invert_three_heights(triple,R_EARTH,5e4)

@pytest.mark.parametrize('ratio',[-1.,0.,1.1,100.])
def test_invalid_ratio_bounds(ratio):
    with pytest.raises(ValueError):
        three_height_shape_bounds(ratio,R_EARTH,50000.)

@pytest.mark.parametrize('r,d',[(R_EARTH,5e4),(R_EARTH,1e5),(1.5e6,1e5)])
def test_bounds_width_is_amplitude_independent(r,d):
    K=synthetic_three(r,d,ELL_PRE_REGISTERED,amplitude=.02)
    q=ratio_from_three(K)
    b=three_height_shape_bounds(q,r,d)
    assert b['ell_lower']<ELL_PRE_REGISTERED<b['ell_upper']
    assert b['ell_upper']-b['ell_lower']>0


def test_windows_constant_single():
    h=np.arange(8)*5e4
    data=1+ground_fraction()*relative_yukawa(h,ELL_PRE_REGISTERED)
    fits=recover_windows(data,R_EARTH,5e4)
    assert len(fits)==6
    assert max(abs(x-ELL_PRE_REGISTERED) for x in fits)<.01


def test_windows_double_drift_and_no_same_scale():
    z=compare_synthetic_single_double()
    single=np.asarray(z['single_ell_windows_m'])
    double=np.asarray(z['double_ell_windows_m'])
    assert np.max(np.abs(single-ELL_PRE_REGISTERED))<.01
    assert np.max(double)-np.min(double)>4e4
    assert np.all(np.diff(double)>0)


def test_bare_exponential_three_point_false_positive():
    # Yukawa-like triple inverse is NOT a proof of the underlying model.
    r=R_EARTH;d=5e4;q=.6
    values=1+.002*q**np.arange(6)
    fits=recover_windows(values,r,d)
    assert np.all(np.isfinite(fits))
    assert max(fits)-min(fits)>.5


def test_ratio_gradient_matches_finite_differences():
    y=synthetic_three(R_EARTH,1e5,ELL_PRE_REGISTERED,.006)
    C=np.diag([1e-12]*3)
    grad=np.asarray(gaussian_ratio_uncertainty(y,C)['gradient'])
    grad_fd=[]
    for i in range(3):
        e=np.zeros(3);e[i]=1e-8
        grad_fd.append((ratio_from_three(y+e)-ratio_from_three(y-e))/(2e-8))
    assert np.allclose(grad,grad_fd,rtol=5e-7)
    assert abs(sum(grad))<1e-9


def test_exact_shared_additive_shift_cancels():
    y=synthetic_three(R_EARTH,1e5,ELL_PRE_REGISTERED,.006)
    assert math.isclose(ratio_from_three(y), ratio_from_three(y+.00001),rel_tol=1e-11)


def test_delta_method_matches_mc_scale():
    r=R_EARTH;d=1e5;sig=1e-7
    y=synthetic_three(r,d,ELL_PRE_REGISTERED,ground_fraction())
    lin=inverse_condition_number(y,r,d,np.eye(3)*sig**2)
    sim=synthetic_mc(r,d,n=800,noise_sigma=sig,seed=20261121)
    width=(sim['p2_5_p50_p97_5_m'][2]-sim['p2_5_p50_p97_5_m'][0])/2
    assert .7 < width/(1.96*lin['sigma_ell_m_linear']) <1.3


def test_orbit_gr_comparison_and_noninterchangeable_j2():
    d=orbit_comparison()
    assert .04<d['yukawa_spherical_epicycle_rad']<.05
    assert 1e-8<d['Schwarzschild_GR_periapsis_rad']<2e-8
    assert d['different_apsidal_conventions_warning']


def test_explicitly_disallow_nonpositive_scale():
    with pytest.raises(ValueError):weighted_offset_fraction(-.1)
    with pytest.raises(ValueError):adjacent_difference_ratio(-.1,R_EARTH,5e4)
    with pytest.raises(ValueError):adjacent_difference_ratio(.1,0.,5e4)
    with pytest.raises(ValueError):ratio_from_three([1.,2.])


def test_fixed_prediction_matches_previous_v122():
    ell=ELL_PRE_REGISTERED
    y=synthetic_three(R_EARTH,1e5,ell,ground_fraction())
    assert math.isclose(y[0]-1,epsilon(R_EARTH),rel_tol=1e-10)


def test_correct_range_wrong_coupling_is_exposed():
    from rootv123 import amplitude_sign_and_fixed_alpha_test
    h=np.arange(6)*50000.
    y=1+.25*ground_fraction()*relative_yukawa(h,ELL_PRE_REGISTERED)
    fit=recover_windows(y,R_EARTH,50000.)
    assert max(abs(v-ELL_PRE_REGISTERED) for v in fit)<.01
    a=amplitude_sign_and_fixed_alpha_test(y,h)
    assert math.isclose(a['epsilon_inferred']/a['epsilon_fixed_expected'],.25,rel_tol=1e-11)
    assert a['attractive_source_sign_passes']
    assert a['max_abs_holdout_error']<1e-13


def test_repulsive_sign_is_not_fixed_attractive_scalaron():
    from rootv123 import amplitude_sign_and_fixed_alpha_test
    h=np.arange(6)*50000.
    y=1-ground_fraction()*relative_yukawa(h,ELL_PRE_REGISTERED)
    a=amplitude_sign_and_fixed_alpha_test(y,h)
    assert a['epsilon_inferred']<0
    assert not a['attractive_source_sign_passes']


def test_three_layers_all_hold_for_fixed_candidate_synthetic():
    from rootv123 import amplitude_sign_and_fixed_alpha_test
    h=np.arange(6)*50000.
    y=1+ground_fraction()*relative_yukawa(h,ELL_PRE_REGISTERED)
    a=amplitude_sign_and_fixed_alpha_test(y,h)
    assert abs(a['fixed_alpha_fractional_mismatch'])<1e-10
    assert a['max_abs_holdout_error']<1e-13
    assert a['n_holdout']==4
