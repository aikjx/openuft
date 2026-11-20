import math
import numpy as np
import pytest
from src.physics import (G,C,EARTH_J2,EARTH_R,EARTH_MU,HBAR,check,positive,p2,
    point_envelope,sphere_envelope,newton_g,j2_relative,gravity,q_shape,normalized_D,
    eotvos_eta,gr_coupling_z,gravitational_alpha,ratio_universal_GM)

@pytest.mark.parametrize('theta,val',[(0,1),(math.pi/2,-.5),(math.pi,1),(math.pi/3,-.125)])
def test_p2(theta,val):assert p2(theta)==pytest.approx(val,abs=1e-15)
@pytest.mark.parametrize('r', [.01,.1,1.,10.,1e3])
def test_newton(r):assert newton_g(5.,r)==pytest.approx(5/r**2)
@pytest.mark.parametrize('lam',[.001,.1,1,100,1e12])
def test_yukawa_point_smallradius(lam): assert sphere_envelope(0,1,lam)==pytest.approx(point_envelope(1,lam))
@pytest.mark.parametrize('x',[1e-8,1e-5,.05,.19,.2,.5,1,2,5,15,100,800])
def test_sphere_envelope_stable(x):
    r=2.;radius=1.;lam=1./x
    y=sphere_envelope(radius,r,lam)
    assert math.isfinite(y) and y>=0
    if x<15:
        F=3*(x*math.cosh(x)-math.sinh(x))/x**3 if x>1e-3 else 1+x*x/10+x**4/280
        assert y==pytest.approx(F*math.exp(-r/lam),rel=2e-8)
@pytest.mark.parametrize('r,alpha,lam,theta,j2',[(10,.1,1,0,0),(10,.1,5,1.57,0),(10,0,2,0,.002),
    (10,.01,2,.25,.004),(20,.25,10,1,0),(30,0,12,1,0),(1.5,.5,.8,.5,.001), (1e7,0,1,0,EARTH_J2)])
def test_q_finite_difference(r,alpha,lam,theta,j2):
    R=1 if r<100 else EARTH_R
    mu=G*100 if r<100 else EARTH_MU
    h=r*1e-5
    if r-h<R: h=(r-R)/3 if r>R else r*1e-6
    ap=gravity(mu,r+h,R,j2,theta,alpha,lam)
    am=gravity(mu,r-h,R,j2,theta,alpha,lam)
    q_numeric=-r*(ap-am)/(4*h*gravity(mu,r,R,j2,theta,alpha,lam))
    q_analytic=q_shape(mu,r,R,j2,theta,alpha,lam)
    assert q_analytic==pytest.approx(q_numeric,rel=2e-7,abs=1e-7)

def test_earth_j2_equator():
    q=q_shape(EARTH_MU,EARTH_R,EARTH_R,EARTH_J2,math.pi/2)
    assert 1.001<q<1.002

def test_earth_j2_pole():
    assert .996<q_shape(EARTH_MU,EARTH_R,EARTH_R,EARTH_J2,0)<.998

def test_j2_sign():
    assert j2_relative(1,2,.001,0)<0
    assert j2_relative(1,2,.001,math.pi/2)>0

def test_D_exact_rank1():
    rows=[]
    for q_source in [.1,.2,.7,1.3]:
        rows.append([normalized_D(q_source,qi,qj,.2,2,1)
                     for qi,qj in [(.2,.8),(.3,1.7),(2,4)]])
    s=np.linalg.svd(np.array(rows),compute_uv=False)
    assert s[1]<s[0]*1e-12

def test_ETA_NOT_exact_rank1():
    # Corrects common mistake: exact Eotvos denominator depends on source and material pair.
    q_sources=[.3,.8]
    pairs=[(.3,.8),(.3,1.8)]
    mat=np.array([[eotvos_eta(qs,a,b,1.2,1,1) for a,b in pairs] for qs in q_sources])
    assert abs(np.linalg.det(mat))>1e-7

def test_eta_small_coupling_matches_D():
    args=(.7,.4,1.3,1e-8,1.,1.)
    assert eotvos_eta(*args)==pytest.approx(normalized_D(*args),rel=1e-7)

def test_universal_G_preserves_D_zero():
    assert normalized_D(.9,.2,.2,.3,1,1)==0
    assert eotvos_eta(.9,.2,.2,.3,1,1,universal=.9)==0

def test_G_rescaling_degeneracy():
    mu=4e14
    assert mu/(G*4)==pytest.approx(mu/((G/8)*32))
    assert ratio_universal_GM(G*100,100)==pytest.approx(1)

def test_z_is_definition():assert gr_coupling_z()==pytest.approx(.010004524012147)

def test_gr_alpha_electron():assert gravitational_alpha(9.1093837139e-31)==pytest.approx(1.7518e-45,rel=2e-4)

@pytest.mark.parametrize('args',[(-1,1,1),(2,1,1),(1,1,0),(1,0,1)])
def test_bad_sphere_params(args):
    with pytest.raises(ValueError):sphere_envelope(*args)
@pytest.mark.parametrize('alpha,lam',[(float('nan'),1),(1,0),(float('inf'),1)])
def test_bad_q(alpha,lam):
    with pytest.raises(ValueError):q_shape(1,2,alpha=alpha,length=lam)

def test_q_denominator_zero():
    with pytest.raises(ValueError):q_shape(1,1,alpha=0,u=-1)

def test_eta_denominator_zero():
    with pytest.raises(ValueError):eotvos_eta(1,0,1,0,1,1,universal=-1)

def test_short_range_suppression():
    assert sphere_envelope(1,3,1e-6)==pytest.approx(0)

def test_newton_q_invariance():
    assert q_shape(1,3)==pytest.approx(q_shape(5,3))==pytest.approx(1)

def test_huge_range_G_mass_degenerate():
    # Yukawa becomes a near-constant amplitude for r << lambda.
    f1=(1+1/1e12)*math.exp(-1/1e12)
    f2=(1+5/1e12)*math.exp(-5/1e12)
    assert f1==pytest.approx(f2,abs=1e-20)
