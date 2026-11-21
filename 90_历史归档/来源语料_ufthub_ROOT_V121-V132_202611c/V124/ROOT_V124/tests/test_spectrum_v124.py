import math
import numpy as np
import pytest
from spectrum_v124 import *

R=R_EARTH
D=50_000.

@pytest.mark.parametrize('ell',[10_000.,50_000.,124_600.,300_000.,1_000_000.])
def test_exact_prony_five(ell):
    vals=exact_K_decimal(R,D,ell,A="0" if ell<20_000 else "1")
    ret=prony_five_decimal(vals,R,D)
    assert ret['ell_m']==pytest.approx(ell,rel=3e-12)
    assert abs(ret['shape_residual'])<1e-30
    assert abs(ret['recurrence_residual_D3'])<1e-40

@pytest.mark.parametrize('u,v',[('0.01','0.0002'),('0.02','-0.0003'),('-0.01','0.0001')])
def test_fake_prony_passes_repeated_root_fails_yukawa(u,v):
    vals=fake_prony_decimal(R,D,ELL,u=u,v=v)
    out=prony_five_decimal(vals,R,D)
    assert out['ell_m']==pytest.approx(ELL,rel=1e-12)
    assert abs(out['recurrence_residual_D3'])<1e-40
    assert abs(out['shape_residual'])>0.01

@pytest.mark.parametrize('alpha',[1/3,0.1,0.7])
def test_density_factor_consistency(alpha):
    h=np.array([0.,100_000.,400_000.])
    p=point_source_profile(h,alpha=alpha)
    ex=earth_profile(h,alpha=alpha)
    assert np.allclose(ex/p,phi_earth_analytic(),rtol=1e-13)

@pytest.mark.parametrize('height',[0.,50_000.,100_000.,400_000.,1000_000.])
def test_source_profile_positive_decreasing(height):
    assert float(earth_profile(height))>0
    assert float(earth_profile(height+1000))<float(earth_profile(height))

@pytest.mark.parametrize('r1,r2',[([ELL,300_000.],[0.6,0.4]),([100_000.,500_000.],[0.1,0.9]),([50_000.,70_000.,400_000.],[0.3,0.3,0.4])])
def test_mixed_spectrum_positive_curvature(r1,r2):
    m=moments_at_height(0.,r1,r2)
    assert m['curvature']>0
    assert m['dk_effective_dr']<0
    assert m['variance_k']>0
    f=ideal_F_at_height(np.array([0.,D,2*D]),r1,r2)
    assert spectral_hankel_3(*f)>0

@pytest.mark.parametrize('ell',[1e4,ELL,3e5,1e7])
def test_single_spectrum_zero_curvature(ell):
    m=moments_at_height(0.,[ell],[1.])
    assert m['curvature']==pytest.approx(0,abs=1e-25)
    assert m['ell_effective_m']==pytest.approx(ell,rel=1e-13)

@pytest.mark.parametrize('h',[0.,50_000.,200_000.,500_000.,1_000_000.])
def test_effective_ell_increases_with_height(h):
    m=moments_at_height(h,[ELL,300_000.],[0.6,0.4])
    n=moments_at_height(h+200.,[ELL,300_000.],[0.6,0.4])
    assert n['ell_effective_m']>m['ell_effective_m']

@pytest.mark.parametrize('noise',[1e-4,1e-3,1e-2])
def test_mc_reproducible(noise):
    a=spectral_mc(n=4000,noise=noise)
    b=spectral_mc(n=4000,noise=noise)
    assert a==b
    assert 0<=a['single']['fraction_H_positive']<=1
    assert 0<=a['double']['fraction_H_positive']<=1

@pytest.mark.parametrize('invalid',[[0,ELL],[-5,ELL]])
def test_reject_nonpositive_range(invalid):
    with pytest.raises(ValueError):ideal_F_at_height([0,10],invalid,[.5,.5])

def test_reject_five_short_input():
    with pytest.raises(ValueError):prony_five_decimal(['1','2','3'],R,D)

def test_reject_negative_height():
    with pytest.raises(ValueError):earth_profile(-100)


def test_unresolvable_short_range_rounds_to_constant():
    vals=exact_K_decimal(R,D,10000.,A="1",dps=110)
    assert vals == ["1.0"]*5
    with pytest.raises(ValueError):prony_five_decimal(vals,R,D)

@pytest.mark.parametrize('ell',[ELL,300_000.])
def test_derivative_geometry_matches_K(ell):
    # Differentiate a K-function numerically; the equivalent F weight is B*k² exp(-k*r).
    k=1/ell;B=phi_earth_analytic()/3;rad=R+200_000.;step=5.
    Kleft=model_K([rad-step],1.,[(B,k)])[0]
    Kright=model_K([rad+step],1.,[(B,k)])[0]
    Fnum=-(Kright-Kleft)/(2*step*rad)
    Ftrue=B*k*k*math.exp(-k*rad)
    assert Fnum==pytest.approx(Ftrue,rel=1e-7)

@pytest.mark.parametrize('h',[0.,100_000.,400_000.])
def test_variance_pairwise_identity(h):
    rr=np.array([ELL,200_000.,300_000.]); ww=np.array([.2,.3,.5])
    x=moments_at_height(h,rr,ww)
    ff=ww*np.exp(-h/rr);kk=1/rr
    s=sum(ff[i]*ff[j]*(kk[i]-kk[j])**2 for i in range(3) for j in range(i+1,3))
    assert x['curvature']==pytest.approx(s,rel=1e-10)

@pytest.mark.parametrize('noise',[1e-4,1e-3])
def test_single_spectrum_sign_is_not_evidence(noise):
    mc=spectral_mc(n=4000,noise=noise)
    assert 0.45<mc['single']['fraction_H_positive']<0.55

@pytest.mark.parametrize('ell',[1.,100.,1000.,10_000.,100_000.])
def test_stable_source_factor_extreme_short_range(ell):
    s=phi_earth_scaled(ell)
    pred=float(earth_profile(0,ell))
    assert math.isfinite(s) and s>0
    assert math.isfinite(pred) and pred>0
    if ell<1000:
        assert pred<1e-3

@pytest.mark.parametrize('ell',[1e10,1e12,1e15])
def test_phi_long_range_recovers_point_mass(ell):
    assert phi_earth_analytic(ell)==pytest.approx(1.,rel=1e-6)
    ratio=float(earth_profile(0,ell)/point_source_profile(0,ell))
    assert ratio==pytest.approx(1.,rel=1e-6)

def test_unscaled_phi_has_clear_overflow_error():
    with pytest.raises(OverflowError):phi_earth_analytic(1000)


def test_finite_source_never_identical_to_point_at_ell10Mm():
    # finite-size correction still 3.4% even for ell=10,000 km
    assert phi_earth_analytic(1e7)==pytest.approx(1.0342773935987575,rel=1e-9)
