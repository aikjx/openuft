"""Mathematical/unit tests on SYNTHETIC Yukawa and Newtonian scenarios."""
import math
import numpy as np
import pytest
from v125_core import (
  FixedYukawaEarth, R_EARTH_M, ELL_M, GM_EARTH, EOTVOS,
  fayet_phi_scaled, trace_invert_range, harmonic_quadrupole_potential,
  cartesian_numeric_laplacian, orbit_trace_band_diagnostic,
  synthetic_trace_mc, newton_n, point_source_yukawa_potential, point_source_yukawa_trace,
)

M=FixedYukawaEarth()
HEIGHTS=[0,50_000,100_000,200_000,250_000,300_000,400_000,500_000,600_000,1_000_000]

@pytest.mark.parametrize('h',HEIGHTS)
def test_helmholtz_equals_divergence(h):
    r=R_EARTH_M+h
    assert float(M.accel_divergence(r))==pytest.approx(float(M.helmholtz_trace(r)),rel=2e-14)

@pytest.mark.parametrize('h',HEIGHTS)
def test_trace_of_accel_tensor(h):
    r=R_EARTH_M+h
    xyz=np.array([.6*r,.8*r,0.0])
    assert float(np.trace(M.gradient_tensor(xyz)))==pytest.approx(float(M.accel_divergence(r)),rel=2e-13)

@pytest.mark.parametrize('h',HEIGHTS)
def test_radial_scalar_dK_closed_form(h):
    r=R_EARTH_M+h
    expected=-M.gm*float(M.eps(r))*(r/M.ell_m)/(M.ell_m*(1+r/M.ell_m))
    assert float(M.K_prime(r))==pytest.approx(expected,rel=1e-14)

@pytest.mark.parametrize('h',HEIGHTS)
def test_trace_positive_and_decay(h):
    t=float(M.accel_divergence(R_EARTH_M+h))
    assert t>0
    assert t<float(M.accel_divergence(R_EARTH_M)) if h else True

@pytest.mark.parametrize('h1,h2',[(0,50_000),(0,400_000),(50_000,400_000),(100_000,500_000),(250_000,400_000),(400_000,500_000),(500_000,1_000_000)])
def test_two_trace_exact_range_inversion(h1,h2):
    r1=R_EARTH_M+h1;r2=R_EARTH_M+h2
    assert trace_invert_range(r1,float(M.accel_divergence(r1)),r2,float(M.accel_divergence(r2)))==pytest.approx(ELL_M,rel=1e-12)

@pytest.mark.parametrize('alpha',[0.01,0.05,1/3,0.6,1.0,-0.05,-1/3])
def test_source_amplitude_cancels_in_range(alpha):
    mm=FixedYukawaEarth(alpha=alpha)
    r1=R_EARTH_M+250_000;r2=R_EARTH_M+400_000
    assert trace_invert_range(r1,float(mm.accel_divergence(r1)),r2,float(mm.accel_divergence(r2)))==pytest.approx(ELL_M,rel=1e-12)

@pytest.mark.parametrize('ell',[10_000,50_000,124_600,200_000,300_000,1_000_000])
def test_different_length_inversion(ell):
    mm=FixedYukawaEarth(ell_m=ell)
    r1=R_EARTH_M+250_000;r2=R_EARTH_M+400_000
    t1=float(mm.accel_divergence(r1));t2=float(mm.accel_divergence(r2))
    assert trace_invert_range(r1,t1,r2,t2)==pytest.approx(ell,rel=1e-12)

@pytest.mark.parametrize('shape_scale',[0.25,0.5,1.0,2.0,3.0])
def test_density_form_factor_normalization_cancels(shape_scale):
    mm=FixedYukawaEarth(source_shape_scaled=shape_scale*fayet_phi_scaled())
    r1=R_EARTH_M+250_000;r2=R_EARTH_M+400_000
    assert trace_invert_range(r1,float(mm.accel_divergence(r1)),r2,float(mm.accel_divergence(r2)))==pytest.approx(ELL_M,rel=1e-12)

@pytest.mark.parametrize('point',[(1.0,.2,.3),(1.2,-.4,1.5),(.7,.9,1.1),(-.8,-1.5,.6)])
def test_newtonian_quadrupole_is_harmonic(point):
    lap=cartesian_numeric_laplacian(harmonic_quadrupole_potential,point,.001)
    assert abs(lap)<2e-6

def test_newtonian_trace_exact_zero():
    mm=FixedYukawaEarth(alpha=0.0)
    assert np.trace(mm.gradient_tensor([R_EARTH_M+400_000,0,0]))==pytest.approx(0,abs=1e-20)

@pytest.mark.parametrize('h',[0,100_000,400_000,1_000_000])
def test_yukawa_sign_follows_alpha(h):
    mplus=FixedYukawaEarth(alpha=1/3)
    mminus=FixedYukawaEarth(alpha=-1/3)
    r=R_EARTH_M+h
    assert float(mplus.accel_divergence(r))==pytest.approx(-float(mminus.accel_divergence(r)),rel=1e-14)

@pytest.mark.parametrize('e',[0.0,.005,.01,.02])
def test_orbit_bandwidth_low(e):
    out=orbit_trace_band_diagnostic(M,eccentricity=e)
    assert out['orbital_frequency_hz']<.0002
    assert out['fraction_ac_power_at_least_5mHz']<1e-19

def test_400km_trace_eotvos():
    trace=float(M.accel_divergence(R_EARTH_M+400_000))/EOTVOS
    assert trace==pytest.approx(17.47359298995668,rel=1e-12)

def test_400km_rotation_scales_are_bigger():
    r=R_EARTH_M+400_000
    apparent_rotational_trace_mag=2*newton_n(r)**2
    assert apparent_rotational_trace_mag/float(M.accel_divergence(r))>100

def test_mc_5percent_reproduces_range_interval():
    out=synthetic_trace_mc(M,n=10_000,rel_sigma=.05,seed=20261121)
    lo,med,hi=out['quantiles_2p5_50_97p5_km']
    assert lo<124.6<hi
    assert 123<med<126
    assert out['valid_fraction']>.999

@pytest.mark.parametrize('bad_args',[(2,1,1.,1.),(1,2,0.,1.),(1,2,1.,0.),(1,2,-1.,1.),(1,2,1.,10.)])
def test_trace_inverter_rejects_nonphysical(bad_args):
    with pytest.raises(ValueError):
        trace_invert_range(*bad_args)

@pytest.mark.parametrize('invalid_ell',[0,-1,float('inf'),float('nan')])
def test_bad_formfactor_length_rejected(invalid_ell):
    with pytest.raises(ValueError):
        fayet_phi_scaled(invalid_ell)


def test_finite_difference_hessian_trace():
    r=R_EARTH_M+400_000
    pt=np.array([r,0.,0.])
    lap=cartesian_numeric_laplacian(lambda xyz: float(M.potential(np.linalg.norm(xyz))),pt,1000.)
    expected=-float(M.accel_divergence(r))
    assert lap==pytest.approx(expected,rel=.0002)


def test_pointwise_traces_dont_depend_on_common_GM_ratio():
    a=FixedYukawaEarth(gm=GM_EARTH)
    b=FixedYukawaEarth(gm=1.25*GM_EARTH)
    r1=R_EARTH_M+250_000;r2=R_EARTH_M+400_000
    ratio_a=float(r1*a.accel_divergence(r1)/(r2*a.accel_divergence(r2)))
    ratio_b=float(r1*b.accel_divergence(r1)/(r2*b.accel_divergence(r2)))
    assert ratio_a==pytest.approx(ratio_b,rel=1e-14)


def test_non_yukawa_power_trace_does_not_look_exponential():
    # A false vacuum divergence T~r^-3 produces a different apparent length
    r1=R_EARTH_M+250_000;r2=R_EARTH_M+400_000;r3=R_EARTH_M+500_000
    t=lambda r: r**-3
    a=trace_invert_range(r1,t(r1),r2,t(r2))
    b=trace_invert_range(r2,t(r2),r3,t(r3))
    assert abs(a-b)>1_000


@pytest.mark.parametrize('point',[(2.0,1.0,-.5),(3.0,-1.0,1.0),(-1.0,3.0,2.0)])
def test_helmholtz_trace_nonspherical_multisource(point):
    pos=np.array([[0,0,0],[.3,0,0],[0,.6,-.3],[-.2,-.1,.1]],float)
    strengths=np.array([1.0,.25,.35,.6])
    k=1.2
    tr=point_source_yukawa_trace(point,pos,strengths,k)
    lap=cartesian_numeric_laplacian(lambda xyz:point_source_yukawa_potential(xyz,pos,strengths,k),point,.001)
    assert tr>0
    assert lap==pytest.approx(-tr,rel=1e-6)


def test_nonspherical_positive_source_strength_trace_positive():
    src=np.array([[0.,0,0],[.1,.2,0],[.1,-.2,.1]])
    for position in ([2,1,3],[-2,-1,2],[1,3,2]):
        assert point_source_yukawa_trace(position,src,[1.,2.,3.],.5)>0


def test_dc_yukawa_trace_undetectable_with_free_constant_bias():
    from v125_core import profiled_signal_information
    t=np.linspace(0,2*np.pi,128,endpoint=False)
    signal=np.full(128,17.47359)
    nuisance=np.ones((128,1))
    assert profiled_signal_information(signal,nuisance,sigma=.1)<1e-22


def test_sinusoidal_trace_amplitude_identifiable_if_only_bias_free():
    from v125_core import profiled_signal_information
    t=np.linspace(0,2*np.pi,128,endpoint=False)
    signal=np.sin(t)
    nuisance=np.ones((128,1))
    assert profiled_signal_information(signal,nuisance,sigma=.1)>6000


def test_sinusoid_degenerate_if_correlated_nuisance_included():
    from v125_core import profiled_signal_information
    t=np.linspace(0,2*np.pi,128,endpoint=False)
    signal=np.sin(t)
    nuisance=np.column_stack([np.ones(128),np.sin(t),np.cos(t)])
    assert profiled_signal_information(signal,nuisance,sigma=.1)<1e-22


def test_projection_invariant_under_nuisance_column_rescaling():
    from v125_core import profiled_signal_information
    t=np.linspace(0,2*np.pi,128,endpoint=False)
    signal=np.sin(t)+0.1*np.sin(2*t)
    n1=np.column_stack([np.ones(128),np.sin(t)])
    n2=n1*np.array([1e-2,1e3])
    assert profiled_signal_information(signal,n1)==pytest.approx(profiled_signal_information(signal,n2),rel=1e-12)
