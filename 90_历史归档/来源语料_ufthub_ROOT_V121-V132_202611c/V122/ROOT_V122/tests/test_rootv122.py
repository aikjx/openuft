"""ROOT V122: math identities and synthetic test fixtures only."""
import math
import numpy as np
import pytest
from scipy.integrate import quad
from rootv120 import R_EARTH, MU_EARTH_REF, C_LIGHT, near_circular_precession_rad, ground_fraction
from rootv122 import (ELL, EPS0, epsilon,K,potential,g_radial, frequencies,
                      scalar_metric_potentials,clock_shift_from_integral,
                      central_orbit_precession, expected_profiled_null_chi2,
                      expected_projection_with_nuisances,profile_diagnostic,scalaron,
                      five_height_hankel_trap,noise_correlation_matrix)

@pytest.mark.parametrize('h',[0.,1e5,2.5e5,4e5,1e6])
def test_K_is_r2_g(h):
    r=R_EARTH+h
    assert abs(K(r)-r*r*g_radial(r))/K(r)<1e-13

@pytest.mark.parametrize('h',[0.,1e5,2.5e5,4e5,1e6])
def test_potential_derivative_matches_acceleration(h):
    r=R_EARTH+h
    dr=5.
    calc=((-3*potential(r)+4*potential(r+dr)-potential(r+2*dr))/(2*dr) if h==0 else
          (potential(r+dr)-potential(r-dr))/(2*dr))
    assert math.isclose(calc,g_radial(r),rel_tol=2e-8)

@pytest.mark.parametrize('h',[0.,1e5,2.5e5,4e5,1e6])
def test_epicyclic_matches_radial_frequency_derivative(h):
    r=R_EARTH+h
    dr=5.
    omega2=lambda x:K(x)/x**3
    deriv=((-3*omega2(r)+4*omega2(r+dr)-omega2(r+2*dr))/(2*dr) if h==0 else
           (omega2(r+dr)-omega2(r-dr))/(2*dr))
    radial=4*omega2(r)+r*deriv
    assert math.isclose(frequencies(r)['kappa2'],radial,rel_tol=5e-10)

@pytest.mark.parametrize('h',[0.,1e5,2.5e5,4e5,1e6])
def test_scalar_lensing_sum_cancels(h):
    m=scalar_metric_potentials(R_EARTH+h)
    assert math.isclose(m['lensing_sum'],m['lensing_GR_sum'],rel_tol=1e-14)
    assert math.isclose(m['dynamical_to_lensing_mass'],1+epsilon(R_EARTH+h),rel_tol=1e-14)
    assert 0<m['gamma']<1

@pytest.mark.parametrize('h',[0.,1e5,2.5e5,4e5,1e6])
def test_precession_matches_v120(h):
    assert math.isclose(frequencies(R_EARTH+h)['periapsis'],
                        near_circular_precession_rad(h,ELL,EPS0),rel_tol=1e-8)

@pytest.mark.parametrize('a,b',[(0.,4e5),(1e5,5e5),(2.5e5,6e5)])
def test_clock_radial_integral_matches_potential_diff(a,b):
    r1,r2=R_EARTH+a,R_EARTH+b
    exact=(potential(r2)-potential(r1))/C_LIGHT**2
    numerical=clock_shift_from_integral(r1,r2)
    assert math.isclose(exact,numerical,rel_tol=3e-12)

def test_scalaron_fixed_alpha_free_mass():
    s=scaler=scalaron()
    assert math.isclose(s['alpha_yukawa'],1/3,rel_tol=1e-15)
    assert math.isclose(s['a_m2'],ELL*ELL/6,rel_tol=1e-15)
    assert 1.58e-12<s['mass_energy_eV']<1.59e-12
    assert s['is_a_free_parameter']

@pytest.mark.parametrize('ell',[1e3,1e5,1e7])
def test_scalaron_equivalence_all_scales(ell):
    s=scalaron(ell)
    assert math.isclose(s['ell_m'], math.sqrt(6*s['a_m2']),rel_tol=1e-14)
    assert math.isclose(s['alpha_yukawa'],1/3,rel_tol=1e-15)

@pytest.mark.parametrize('e',[1e-3,2e-4,5e-5])
def test_numeric_orbit_epicyclic_agreement(e):
    pred=central_orbit_precession(e=e)
    assert pred['n_apoapses']>=4
    assert abs(pred['precession']-pred['epicycle'])<4e-5


def test_no_fifth_force_limit():
    for h in (0.,250000.,400000.):
        assert frequencies(R_EARTH+h,eps0=0)['periapsis']==0
        assert scalar_metric_potentials(R_EARTH+h,eps0=0)['gamma']==1


def test_hankel_false_positive_for_yukawa():
    p=five_height_hankel_trap()
    assert abs(p['ell_m']-ELL)<2
    assert abs(p['repeated_root_residual'])<2e-13
    assert abs(p['physical_shape_residual'])>10
    assert p['H0']<0


def test_asimov_and_covariance_properties():
    hs=np.array([0.,1e5,2e5,3e5,4e5])
    y=1+np.array([epsilon(R_EARTH+h) for h in hs])
    C=noise_correlation_matrix(5,1e-5,0.)
    a=expected_profiled_null_chi2(y,C)
    b=expected_profiled_null_chi2(y,noise_correlation_matrix(5,1e-5,3e-3))
    assert a>0
    assert abs(a-b)/a<1e-8


def test_adding_nuisance_cannot_increase_information():
    hs=np.array([2.5e5,3e5,3.5e5,4e5,4.5e5,5e5])
    x=(hs-hs.mean())/(hs.max()-hs.min())
    y=1+np.array([epsilon(R_EARTH+h) for h in hs])
    C=noise_correlation_matrix(len(hs),1e-5,0.)
    base=expected_projection_with_nuisances(y,C,np.ones((len(hs),1)))
    more=expected_projection_with_nuisances(y,C,np.column_stack((np.ones(len(hs)),x)))
    assert 0<=more<=base+1e-8
    assert more<base


def test_unidentifiable_if_fit_exact_yukawa_template_as_nuisance():
    hs=np.array([0,1e5,2e5,3e5,4e5],dtype=float)
    ep=np.array([epsilon(R_EARTH+h) for h in hs])
    y=1+ep
    C=noise_correlation_matrix(len(hs),1e-5,0.)
    X=np.column_stack((np.ones(len(hs)),ep))
    assert expected_projection_with_nuisances(y,C,X)<1e-12


def test_covariance_validation():
    with pytest.raises(ValueError):
        noise_correlation_matrix(1,1e-5,0)
    with pytest.raises(ValueError):
        expected_profiled_null_chi2([1.,2.],np.eye(3))
    with pytest.raises(ValueError):
        expected_projection_with_nuisances([1.,2.],np.eye(2),np.ones((3,1)))
