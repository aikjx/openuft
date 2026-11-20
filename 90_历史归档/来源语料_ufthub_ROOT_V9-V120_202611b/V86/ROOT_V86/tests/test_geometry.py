import numpy as np
import pytest
from src.geometry import layered_envelope,uniform_2sphere_envelope,uniform_sphere_independent_quadrature
from src.physics import sphere_envelope

@pytest.mark.parametrize('R,r,lam',[(.1,.5,.25),(.2,.9,2.),(.4,2,1.),(.7,1.,.2),(1,3,.04)])
def test_sphere_quadrature(R,r,lam):
    assert sphere_envelope(R,r,lam)==pytest.approx(uniform_sphere_independent_quadrature(R,r,lam),rel=4e-10,abs=1e-18)

@pytest.mark.parametrize('R,r,lam',[(.2,.4,.1),(.2,.4,5),(.5,1,.2),(.8,1,.4)])
def test_layer_uniform_same(R,r,lam):
    shells=[(0.,R/3,3.,1.),(R/3,R/1.4,3.,1.),(R/1.4,R,3.,1.)]
    assert layered_envelope(shells,r,lam)==pytest.approx(sphere_envelope(R,r,lam),rel=3e-12)

def test_layer_composition_matters_even_same_mass():
    A=[(0.,.4,1.,1.),(.4,.6,4.,1.)]
    B=[(0.,.4,1.,10.),(.4,.6,4.,1.)]
    assert layered_envelope(B,.8,.1)>layered_envelope(A,.8,.1)

def test_layer_invalid():
    with pytest.raises(ValueError):layered_envelope([(0,.5,1,1),(.4,1,1,1)],2,1)

def test_two_sphere_point_limit():
    assert uniform_2sphere_envelope(0,0,2,.5)==pytest.approx(np.exp(-4))

@pytest.mark.parametrize('l',[.05,.1,1,10,100])
def test_two_sphere_symmetry(l):
    a=uniform_2sphere_envelope(.3,.6,2,l)
    b=uniform_2sphere_envelope(.6,.3,2,l)
    assert a==pytest.approx(b,rel=2e-10,abs=1e-15)
    assert a>=0

def test_two_sphere_high_range_stable():
    assert np.isfinite(uniform_2sphere_envelope(1,1,2.1,.0001))

def test_two_sphere_overlap_invalid():
    with pytest.raises(ValueError):uniform_2sphere_envelope(1,1,1,.3)
