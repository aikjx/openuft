import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
import pytest
from scipy.constants import c, mu_0
from finite_tube import TubeModel
from symbolic_audit import checks
from dimension_audit import audit

@pytest.fixture(scope='module')
def model():return TubeModel(samples=1800)

def test_symbolic():assert checks()['cylindrical_divB']=='0'
def test_dimensions():
    rows=audit(); assert len(rows)==24
    assert sum(x['pass'] for x in rows)==20

def test_initial_geometry(model):
    o=model.length_integrals(144)
    assert abs(o['length_m']-.13129865944448835)<1e-12
    assert 5e-10<o['period_s']<6e-10
    assert abs(o['radiation_energy_j']-8.147688736589692e-25)/o['radiation_energy_j']<1e-10

@pytest.mark.parametrize('u',[0,.1,.3,.5,1,1.7,2.4,3.1,4.3,5.6,6.2])
def test_axis_field(model,u):
    X,T,K,B0,*_=model.geometry(u)
    assert abs(np.dot(T,B0))<1e-12
    assert np.linalg.norm(model.field(X)-B0)<1e-8
    assert np.linalg.norm(model.field_chart(u,np.zeros(3))-B0)<1e-12
    assert np.linalg.norm(np.cross(T,B0)*model.charge*model.v-model.gamma*model.mass*model.v**2*K)<1e-9

@pytest.mark.parametrize('u,frac,ang',[(0,.2,.4),(.4,.5,1.2),(1.2,.7,2),(2,.6,3), (2.8,.4,4),(4.6,.8,5.2)])
def test_curl_divergence(model,u,frac,ang):
    X,T,K,B0,*_=model.geometry(u)
    N=K/np.linalg.norm(K); H=np.cross(T,N)
    x=X+model.eps*frac*(N*np.cos(ang)+H*np.sin(ang))
    fld=model.field(x)
    assert np.linalg.norm(fld-model.curl_potential_numeric(x,h=1e-7))<1e-6
    assert abs(model.divergence_B_numeric(x,h=1e-7))<1.0 # T/m, numerical finite difference

@pytest.mark.parametrize('u',[0,.3,1.1,2.4,4,5.5])
def test_zero_outside(model,u):
    X,T,K,B0,*_=model.geometry(u)
    N=K/np.linalg.norm(K)
    x=X+1.1*model.eps*N
    assert np.linalg.norm(model.field(x))<1e-15
    assert np.linalg.norm(model.potential(x))<1e-15

@pytest.mark.parametrize('eps',[.00015,.00025,.0003,.0004,.0006])
def test_finite_energy(eps):
    model=TubeModel(eps=eps,samples=800)
    U=model.energy(nu=96,nr=20,nphi=30)
    assert 0<U<.01
    assert abs(U/eps**2-4329)<45 # J/m², leading small-tube scaling

@pytest.mark.parametrize('u',[.01,.34,1.1,2.2,3.7,5.1])
def test_random_shape_axis(u):
    for m,n in [(1,2),(2,3),(3,2),(3,5)]:
        model=TubeModel(m=m,n=n,eps=.00008,samples=300)
        X,T,K,B0,*_=model.geometry(u)
        assert np.allclose(model.field_chart(u,np.zeros(3)),B0,atol=1e-14)

def test_exact_orbit(model):
    out=model.trajectory()
    assert out['success']
    assert out['position_error_m']<1e-8
    assert out['tangent_error']<1e-7
    assert out['speed_drift']<1e-8

def test_perturbed_orbit_escape(model):
    out=model.trajectory([2e-6,0,0])
    assert out['success']
    assert out['position_error_m']>1e-3

def test_radiation_positive(model):
    x=model.length_integrals()
    assert x['radiation_energy_j']>0
    assert x['radiation_energy_j']<x['kinetic_j']

@pytest.mark.parametrize('m,n',[(1,2),(2,3),(3,2),(3,4),(4,3),(3,5)])
def test_new_shapes_axis_field(m,n):
    md=TubeModel(m=m,n=n,eps=.00004,samples=500)
    for u in [0.,.49,1.47,2.71]:
        X,T,K,B0,*_=md.geometry(u)
        assert np.linalg.norm(md.field_chart(u,np.zeros(3))-B0)<1e-12

@pytest.mark.parametrize('eps',[.0001,.00015,.00022,.0003])
def test_asymptotic_energy(eps):
    from asymptotic import coefficient
    md=TubeModel(eps=eps,samples=600)
    U=md.energy(nu=88,nr=22,nphi=24)
    assert abs(U/(coefficient(md)*eps**2)-1)<.002

def test_analytic_bump_integral():
    from asymptotic import radial_integral
    assert abs(radial_integral()-.5)<2e-13
