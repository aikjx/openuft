import numpy as np
import pytest
from src.v111 import Params,rhs,observables,simulate,analytic_bounds
from src.symbolic_audit import checks

@pytest.fixture(scope='module')
def cases():
    return {
       'potential': simulate(Params(),[.35,0,.01,0,.009,0,0],duration=50,steps=351),
       'massless': simulate(Params(g=.5,L4=0),[.35,.7,.05,0,.04,0,0],duration=40,steps=301),
       'tachyon': simulate(Params(g=.5,L4=0),[.35,3,.018,0,.05,0,0],duration=35,steps=301)
    }

@pytest.mark.parametrize('k,g,f,L4',[ (1,.22,1,4),(.5,.01,2,0),(3,2,1,.01),(.1,0,1,3),(1,0.5,1,0)])
def test_valid_parameters(k,g,f,L4):Params(k,g,f,L4).validate()

@pytest.mark.parametrize('k,f,L4',[(-1,1,0),(0,1,0),(1,0,0),(1,-1,0),(1,1,-.1)])
def test_invalid_parameters(k,f,L4):
    with pytest.raises(ValueError):Params(k,.22,f,L4).validate()

@pytest.mark.parametrize('name',['potential','massless','tachyon'])
def test_conservation_of_energy(cases,name):assert cases[name]['energy_rel_drift']<4e-8

@pytest.mark.parametrize('name',['potential','massless','tachyon'])
def test_extended_noether_invariant(cases,name):assert cases[name]['noether_absolute_drift']<2e-8

@pytest.mark.parametrize('name',['massless','tachyon'])
def test_q_constant_if_shift_symmetric(cases,name):assert cases[name]['q_absolute_range']<2e-8

def test_q_not_constant_with_potential(cases):assert cases['potential']['q_absolute_range']>.05

def test_backreaction_tames_phase(cases):assert np.min(cases['tachyon']['obs']['td'])<2.0

def test_backreaction_transfers_energy(cases):
    x=cases['tachyon']['obs']['Eem'];assert np.max(x)>3*np.min(x)

@pytest.mark.parametrize('name',['potential','massless','tachyon'])
def test_energy_positive(cases,name):assert np.min(cases[name]['obs']['H'])>0

@pytest.mark.parametrize('name',['potential','massless','tachyon'])
def test_pointwise_noether_energy_bound(cases,name):
    p=Params(**cases[name]['params']);o=cases[name]['obs']
    assert np.max(np.abs(o['Q']-p.f*p.f*o['td'])-abs(p.g)*o['H']/p.k)<1e-10

@pytest.mark.parametrize('name',['potential','massless','tachyon'])
def test_pointwise_theta_speed_bound(cases,name):
    p=Params(**cases[name]['params']);o=cases[name]['obs']
    assert np.max(abs(o['td'])-np.sqrt(2*o['H'])/p.f)<1e-9

@pytest.mark.parametrize('name',['potential','massless','tachyon'])
def test_mode_energy_nonnegative(cases,name):assert np.min(cases[name]['obs']['Eem'])>=0

@pytest.mark.parametrize('name',['potential','massless','tachyon'])
def test_conservation_balance_derivative(cases,name):
    o=cases[name]['obs'];t=cases[name]['t']; y=cases[name]['y'];p=Params(**cases[name]['params'])
    # Test exact equation locally, not noisy differencing.
    for j in [5,55,155]:
        r=rhs(t[j],y[:,j],p)
        ap,vp,am,vm=y[2,j],y[3,j],y[4,j],y[5,j]
        dQ=p.f*p.f*r[1]-p.g*p.k*(ap*vp-am*vm)
        assert abs(dQ+p.L4*np.sin(y[0,j]))<1e-12

@pytest.mark.parametrize('i',list(range(15)))
def test_exact_symbolic_invariant(i):
    c=checks();assert list(c.values())[i],list(c)[i]

@pytest.mark.parametrize('e',[0,.001,1,100])
def test_analytic_bound_nonnegative(e):
    out=analytic_bounds(Params(g=.5,L4=0),e,1)
    assert out['charge_momentum_correction_bound']>=0

@pytest.mark.parametrize('value',[-1,-.001])
def test_analytic_bound_invalid_energy(value):
    with pytest.raises(ValueError):analytic_bounds(Params(),value)

def test_monotonic_sufficient_condition():
    p=Params(g=.5,L4=0); out=analytic_bounds(p,.24705,.7)
    assert out['monotonic_positive_sufficient']
    assert out['theta_velocity_from_Q_min']>0

def test_tachyon_criteria_never_implies_floquet_stability():
    p=Params(g=.22); b=analytic_bounds(p,.243)
    assert b['sufficient_no_instantaneous_tachyon']
    # This only addresses instantaneous coefficient signs, not Floquet stability.

def test_all_zero_photons_decouple():
    p=Params(L4=0);r=rhs(0,[0,.5,0,0,0,0,0],p)
    assert r[1]==0 and r[3]==0 and r[5]==0

def test_g_zero_decouples():
    p=Params(g=0,L4=0);r=rhs(0,[0,.5,.1,.2,.3,.4,0],p)
    assert r[1]==0

def test_independent_dop853_rk45_short_run():
    p=Params(g=.5,L4=0);y=[.35,3,.018,0,.05,0,0]
    a=simulate(p,y,duration=12,steps=91,method='DOP853',rtol=2e-11,atol=1e-13)
    b=simulate(p,y,duration=12,steps=91,method='RK45',rtol=2e-11,atol=1e-13)
    assert np.max(abs(a['y']-b['y']))<2e-8

def test_theta_dot_not_identical_for_two_helicities():
    p=Params(g=.5,L4=0);y=[.35,2,.01,.02,.03,.04,0]
    x=rhs(0,y,p);assert abs(x[1])>0

def test_zero_coupling_q_equals_f2_thetadot():
    p=Params(g=0,f=2,L4=0)
    o=observables([.5,.75,.2,0,.3,0,0],p)
    assert o['Q']==pytest.approx(3.)

def test_wrong_initial_integral_does_not_change_q_but_changes_n():
    p=Params(L4=4);a=observables([0,0,.1,0,.1,0,0],p)
    b=observables([0,0,.1,0,.1,0,1],p)
    assert a['Q']==b['Q'] and abs(b['N']-a['N']-4)<1e-10

def test_noether_equality_upper_bound():
    p=Params(g=1,k=1,L4=0)
    x=observables([0,0,1,0,0,0,0],p)
    assert abs(abs(x['Q'])-abs(p.g)*x['H']/p.k)<1e-12

@pytest.mark.parametrize('i',list(range(9)))
def test_metric_and_compact_phase_symbolic(i):
    from src.gravity_metric import checks
    c=checks()
    assert list(c.values())[i],list(c)[i]

def test_positive_stiffness_but_floquet_unstable():
    from src.floquet_counterexample import compute
    a=compute()
    assert a['min_coefficient']>0.88
    assert a['trace']< -2.0
    assert a['floquet_mu']>0.027
    assert abs(a['det']-1)<2e-10

def test_independent_floquet_integrators_agree():
    from src.floquet_counterexample import compute
    a=compute(method='DOP853');b=compute(method='RK45')
    assert abs(a['trace']-b['trace'])<1e-9
