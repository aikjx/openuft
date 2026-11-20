import math, numpy as np, pytest
from scipy.constants import e,m_e,c
from src.v102_core import *
from src.symbolic_checks import audit

@pytest.mark.parametrize('beta',[.01,.02,.1,.2,.5,.8,.95,.99])
def test_field_force_algebra(beta):
    t=[1,0,0]; n=[0,1,0]; kap=50.
    B=local_required_B(t,n,kap,beta=beta)
    assert local_force_error(t,n,kap,B,beta=beta)<1e-13

@pytest.mark.parametrize('Bpar',[-100,-1,0,1,100])
def test_longitudinal_invisibility(Bpar):
    t=[1,0,0];n=[0,1,0]
    B=local_required_B(t,n,curvature=14.,B_longitudinal=Bpar)
    assert local_force_error(t,n,14.,B)<1e-13
    assert abs(recover_components(t,n,B)['B_parallel_T']-Bpar)<1e-12

@pytest.mark.parametrize('beta',[.05,.1,.2,.5,.9])
def test_identical_radiation_integrals(beta):
    g=curvature_from_polygon(torus_knot(2,3,num=1200))
    res=field_and_radiation(g,beta=beta)
    assert res['radiation_identity_relative']<5e-15

@pytest.mark.parametrize('n',[300,600,1200,2400])
def test_exact_circle_discrete(n):
    R=.02
    g=curvature_from_polygon(circle(R,n))
    r=field_and_radiation(g)
    assert abs(g['length_m']/(2*math.pi*R)-1)<1e-4
    assert abs(g['total_curvature']/(2*math.pi)-1)<1e-10
    assert abs(r['Cauchy_ratio']-1)<5e-11
    assert abs(r['B_mean_T']/(orbit_prefactor(.1)/R)-1)<1e-3

@pytest.mark.parametrize('pair',[(2,3),(3,5),(4,5),(5,7)])
def test_knot_total_curvature_floor(pair):
    g=curvature_from_polygon(torus_knot(*pair,num=2500))
    assert g['total_curvature']>4*math.pi
    r=field_and_radiation(g)
    assert r['B_mean_T']>r['B_knot_lower_T']
    assert r['E_rad_from_kappa_J']>r['E_knot_lower_J']

@pytest.mark.parametrize('v',[.01,.1,.4,.7])
def test_cauchy_exact_gap_relation(v):
    g=curvature_from_polygon(torus_knot(2,5,num=900))
    r=field_and_radiation(g,beta=v)
    assert math.isclose(r['Cauchy_ratio'],1+r['B_cv']**2,rel_tol=1e-12)
    assert math.isclose(r['B_rms_T']**2,r['B_mean_T']**2+r['B_sd_T']**2,rel_tol=1e-12)
    assert r['E_Cauchy_gap_J']>=-1e-40

@pytest.mark.parametrize('bad',[-1.,0.,1.,float('nan')])
def test_invalid_beta(bad):
    with pytest.raises(ValueError):gamma(bad)

@pytest.mark.parametrize('m,q',[(-1.,e),(m_e,0)])
def test_invalid_mass_and_charge(m,q):
    with pytest.raises(ValueError):orbit_prefactor(.1,m,q)

def test_bad_geometry_duplicate():
    p=circle(num=50);p[4]=p[3]
    with pytest.raises(ValueError):curvature_from_polygon(p)

def test_invalid_torus():
    with pytest.raises(ValueError):torus_knot(2,4)

def test_nonunit_tangent():
    with pytest.raises(ValueError):local_required_B([2,0,0],[0,1,0],1.)

def test_symbolic_audit():
    checks=audit()
    assert len(checks)==9 and all(checks.values())

def test_existing_v100_theory_data():
    from pathlib import Path
    root=Path(__file__).resolve().parents[1]
    p=np.loadtxt(root/'data/V100_ORBIT_21Q_INPUT_THEORY.csv',delimiter=',',skiprows=1)
    gg=curvature_from_polygon(p);r=field_and_radiation(gg)
    assert len(p)==1201
    assert abs(gg['total_curvature']-31.41592113104642)<1e-6
    assert abs(r['B_mean_T']-.033245322449709847)<1e-8
    assert r['radiation_identity_relative']<1e-14
    assert abs(r['Cauchy_ratio']-1)<2e-5
