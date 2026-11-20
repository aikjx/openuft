import math
import numpy as np
import pytest
from src.v110 import (P,propagator,floquet,leading_mu,monodromy_scan,
                      run_coupled,coupled_rhs,coupled_energy,no_free_helix)
from src.symbolic_audit import checks

@pytest.mark.parametrize('p',[
    P(1,.16,.35,2),P(1,.04,.3,2),P(.75,.07,.25,1.5),
    P(1,.16,.35,1.7),P(1,.16,.35,2.3)
])
def test_symplectic_det(p):
    for h in (-1,1):
        r=floquet(p,h)
        assert abs(r['det']-1)<2e-9

@pytest.mark.parametrize('Om',[1.4,1.65,1.9,2,2.1,2.3,2.7])
def test_helicities_same_trace(Om):
    p=P(1,.14,.3,Om)
    a=floquet(p,1);b=floquet(p,-1)
    assert abs(a['trace']-b['trace'])<3e-8
    assert abs(a['mu']-b['mu'])<3e-8

@pytest.mark.parametrize('lam,theta0',[(.03,.2),(.08,.2),(.15,.12),(.2,.12)])
def test_center_weak_resonance(lam,theta0):
    p=P(1,lam,theta0,2)
    r=floquet(p)
    assert r['mu']>0
    assert abs(r['mu']-leading_mu(p))/leading_mu(p)<.007

@pytest.mark.parametrize('Om',[.9,1.2,1.55,2.7,3.5])
def test_stable_far_from_resonance(Om):
    assert abs(floquet(P(1,.1,.2,Om))['trace'])<2

def test_narrow_secondary_resonance_near_omega_equals_k():
    # A weak second-order parametric tongue: deliberately not counted as broadly stable.
    r=floquet(P(1,.1,.2,1.))
    assert r['trace']>2
    assert r['mu']>0

def test_zero_coupling_neutral():
    for Om in [1.2,1.9,2.0,2.4]:
        r=floquet(P(1,0,.25,Om))
        assert r['mu']<1e-6
        assert abs(r['det']-1)<1e-9

def test_zero_amplitude_neutral():
    assert floquet(P(1,.2,0,2))['mu']<1e-6

def test_instability_on_same_theta_endpoint():
    p=P(1,.16,.35,2)
    assert math.cos(p.Omega*(2*math.pi/p.Omega))==pytest.approx(1,abs=1e-14)
    assert floquet(p)['mu']>.02

def test_floquet_trace_and_det_numeric():
    r=floquet(P())
    assert r['trace']==pytest.approx(-2.00773707202,abs=1e-8)
    assert r['det']==pytest.approx(1.,abs=5e-10)

def test_independent_dop853_radau():
    p=P()
    Ma,_=propagator(p,1,method='DOP853')
    Mb,_=propagator(p,1,method='Radau',rtol=2e-10,atol=2e-12)
    assert np.linalg.norm(Ma-Mb,ord=np.inf)<1e-8

@pytest.mark.parametrize('t',[0,.1,1.7,4.,18.])
def test_symbolic_energy_transfer_derivative_numeric(t):
    y=np.array([.25,.1,.3,.08,-.05,.17]);k=1;g=.12;f=1.2;L4=3.9
    dydt=coupled_rhs(t,y,k=k,g=g,f=f,Lambda4=L4)
    x,xd,ap,vp,am,vm=y
    dHtheta=f*f*xd*dydt[1]+L4*np.sin(x)*xd
    dHem=vp*dydt[3]+vm*dydt[5]+k*k*(ap*dydt[2]+am*dydt[4])
    assert abs(dHtheta+dHem)<1e-12

@pytest.fixture(scope='module')
def slow_result():
    return run_coupled(duration=160,nt=601)

def test_backreaction_energy(slow_result):
    assert slow_result['max_relative_energy_drift']<5e-8

def test_backreaction_energy_exchange(slow_result):
    assert slow_result['Eem'].max()>slow_result['Eem'][0]*20
    assert slow_result['Etheta'].min()<slow_result['Etheta'][0]*.6

def test_backreaction_positive(slow_result):
    assert np.min(slow_result['Etheta'])>=-1e-13
    assert np.min(slow_result['Eem'])>=0

def test_bound_on_photon_amplitude(slow_result):
    E0=slow_result['Etotal'][0]
    limit=(2*E0)**.5 # k=1
    assert max(np.max(np.abs(slow_result['y'][2])),np.max(np.abs(slow_result['y'][4])))<=limit*(1+1e-7)

@pytest.mark.parametrize('f,L4',[(1,4),(2,3),(1.2,.8)])
def test_energy_formula_nonnegative(f,L4):
    y=np.array([.5,.3,.2,.2,.4,.4])
    a,b,c=coupled_energy(y,f=f,Lambda4=L4)
    assert a>=0 and b>=0 and c>=0 and c==pytest.approx(a+b)

@pytest.mark.parametrize('v,kappa',[(.2,3),(.8,17),(.95,.3)])
def test_proper_acceleration(v,kappa):
    r=no_free_helix(v,kappa)
    assert r['proper_acceleration']==pytest.approx(r['gamma']**2*r['three_acceleration'])
    assert r['four_velocity_norm_squared']==-1

def test_invalid_v():
    with pytest.raises(ValueError):no_free_helix(1.0)

@pytest.mark.parametrize('beta',[.1,.4,.8])
def test_proper_acceleration_axial_boost(beta):
    v=.6;R=.01
    old=(v*v/R)/(1-v*v)
    vp2=v*v*(1-beta*beta)+beta*beta
    # gamma' = gamma_v * gamma_beta (boost orthogonal to original v)
    new=(v*v*(1-beta*beta)/R)/((1-v*v)*(1-beta*beta))
    assert new==pytest.approx(old,rel=2e-14)

@pytest.mark.parametrize('g',[-.15,-.02,.02,.15])
def test_coupling_sign_invariance_mu(g):
    assert floquet(P(1,g,.2,2))['mu']==pytest.approx(floquet(P(1,-g,.2,2))['mu'],abs=1e-8)

def test_scan_size_and_positivity():
    v=monodromy_scan(n=9)
    assert len(v)==9
    assert all(row['mu_plus']>=0 for row in v)

def test_symbolic_audit():
    assert all(checks().values())
