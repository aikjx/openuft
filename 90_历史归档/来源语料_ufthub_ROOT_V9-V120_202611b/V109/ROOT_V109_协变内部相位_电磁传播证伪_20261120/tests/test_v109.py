"""Controlled theoretical tests; no test here demonstrates a new force."""
import json, csv, pathlib
import numpy as np
import pytest
from src.axion_em import (Profile,wkb_angle,mode_frequency_squared,integrate_mode,
                          exact_rotation,max_adiabatic,observed_mode_proxies,
                          fisher_jacobian_single,one_loop_identifiability,constrained_bound)
from src.symbolic_audit import run_symbolic_checks
ROOT=pathlib.Path(__file__).resolve().parents[1]

@pytest.mark.parametrize('amp',[0, .01, .2, .4, 1., -1.])
def test_profile_value_at_zero(amp):
    p=Profile(amplitude=amp)
    assert p.value(0.)==pytest.approx(0)

@pytest.mark.parametrize('time',[0.,.1,.5,2.,5.,10.])
def test_profile_derivative_central_difference(time):
    p=Profile(amplitude=.21,omega=.87,phase=.12)
    h=1.e-5
    assert (p.value(time+h)-p.value(time-h))/(2*h)==pytest.approx(p.derivative(time),abs=1.e-10)

@pytest.mark.parametrize('time',[0.,.1,.5,2.,5.,10.])
def test_profile_second_central_difference(time):
    p=Profile(amplitude=.21,omega=.87,phase=.12)
    h=1.e-5
    assert (p.derivative(time+h)-p.derivative(time-h))/(2*h)==pytest.approx(p.second(time),abs=1.e-10)

@pytest.mark.parametrize('offset',[-1.,0.,.25,1.,10.])
def test_theta_constant_offset_has_no_wave_effect(offset):
    p=Profile(amplitude=0.,offset=offset)
    assert wkb_angle(.3,p,5)==pytest.approx(0,abs=1e-16)
    assert exact_rotation(7,.3,p,3)['angle']==pytest.approx(0,abs=1e-12)

@pytest.mark.parametrize('lam',[-1.,0.,.1,.2,.5])
def test_lambda_zero_or_constant_phase_and_vacuum_symmetry(lam):
    p=Profile(amplitude=0.)
    r=exact_rotation(10,lam,p,2)
    assert abs(r['angle'])<1e-12
    assert r['relative_amplitude']==pytest.approx(1,abs=1e-12)

@pytest.mark.parametrize('k',[5,10,20,40,80,120])
def test_wkb_converges_at_high_k(k):
    p=Profile()
    r=exact_rotation(k,.08,p,5)
    assert abs(r['angle']-r['wkb']) < .001/(k*k) + 8.e-9

@pytest.mark.parametrize('k',[5,10,20,40,80])
def test_circular_parity(k):
    p=Profile()
    pos=exact_rotation(k,.08,p,5)['angle']
    neg=exact_rotation(k,-.08,p,5)['angle']
    assert pos==pytest.approx(-neg,abs=1e-10)

@pytest.mark.parametrize('duration',[.5,1.,2.,3.,4.,5.])
def test_wkb_endpoint_difference(duration):
    p=Profile(amplitude=.4,omega=.7)
    expected=.5*.08*.4*np.sin(.7*duration)
    assert wkb_angle(.08,p,duration)==pytest.approx(expected,abs=1e-15)

@pytest.mark.parametrize('k',[10,20,40,80])
def test_e_field_and_a_field_wkb_limit(k):
    p=Profile()
    r=observed_mode_proxies(k,.08,p,5)
    w=wkb_angle(.08,p,5)
    assert abs(r['A_phase_axis']-w)<.002/(k*k)
    assert abs(r['E_phase_axis']-w)<.002/(k*k)

@pytest.mark.parametrize('phase',[0.,.4,1.,2.])
def test_zero_coupling_gives_zero_rotation_with_arbitrary_profile(phase):
    p=Profile(amplitude=1.,omega=.8,phase=phase)
    assert abs(exact_rotation(7,0.,p,2)['angle'])<1e-12

@pytest.mark.parametrize('lam,dtheta',[(.1,.2),(.4,1.),(-.2,.3),(.6,-.5)])
def test_parameter_degeneracy_jacobian(lam,dtheta):
    d=one_loop_identifiability(lam,dtheta)
    assert d['rank']==1
    assert d['null_residual']<1.e-14

@pytest.mark.parametrize('sigma',[.0001,.0005,.001,.003])
def test_bound_monotone(sigma):
    assert constrained_bound(2*sigma,.4)==pytest.approx(2*constrained_bound(sigma,.4))

@pytest.mark.parametrize('lam',[0.,.1,.6])
def test_zero_delta_theta_no_constraint(lam):
    assert np.isinf(constrained_bound(.001,0.))
    assert np.isinf(constrained_bound(.001,1.e-18))

@pytest.mark.parametrize('h',[-1,1])
def test_mode_frequency_sign(h):
    p=Profile(amplitude=.8,omega=1.)
    k=3.;lam=.1;t=.3
    expect=k*k+h*lam*k*p.derivative(t)
    assert mode_frequency_squared(t,k,lam,p,h)==pytest.approx(expect)

@pytest.mark.parametrize('k',[1,2,3])
def test_nonadiabatic_endpoint_counterexample(k):
    p=Profile(amplitude=1.,omega=1.)
    r=exact_rotation(k,.3,p,2*np.pi)
    assert abs(r['wkb'])<1.e-14
    # finite wave-scale corrections invalidate an unconditional endpoint formula
    assert abs(r['angle'])>1.e-8

@pytest.mark.parametrize('time',[0.,.5,1.,3.,5.])
def test_adiabaticity_nonnegative(time):
    p=Profile(amplitude=.4,omega=.7)
    assert max_adiabatic(10,.08,p,time)>=0.


def test_nonadiabatic_case_large_error():
    r=exact_rotation(.8,.35,Profile(amplitude=1.,omega=1.),2.5)
    assert abs(r['angle']-r['wkb'])>.1
    assert r['adiabatic_upper']>.1


def test_symbolic_all_true():
    checks=run_symbolic_checks()
    assert len(checks)>=10 and all(checks.values())


def test_same_geometry_weak_coupling_scales_linearly():
    p=Profile()
    a=wkb_angle(.1,p,4)
    b=wkb_angle(.2,p,4)
    assert b==pytest.approx(2*a)


def test_ledger_keeps_396_unique_ids():
    p=ROOT/'ledger'/'V108_ALL_396_AUDITED.csv'
    rows=list(csv.DictReader(p.open(encoding='utf-8-sig',newline='')))
    assert len(rows)==396
    assert len({r['canonical_id'] for r in rows})==396


def test_open_questions_never_falsely_closed():
    with (ROOT/'results'/'V109_AUDIT_RESULTS.json').open(encoding='utf-8') as f:
        d=json.load(f)
    assert d['unified_theory_proven'] is False
    assert d['new_experiment'] is False
    assert d['root_specific_prediction'] is False
