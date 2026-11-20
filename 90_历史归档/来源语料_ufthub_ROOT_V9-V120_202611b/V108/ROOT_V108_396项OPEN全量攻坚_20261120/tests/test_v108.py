"""Executable assertions: conditional models, not discovery of physics."""
import csv, math
from pathlib import Path
import numpy as np
import mpmath as mp
import sympy as sp
import pytest
from src import theory
from src.ledger import build, INPUT, OUTPUT, SPECIAL
from legacy.v107_theory import summary as v107_summary

@pytest.mark.parametrize('n',range(1,13))
def test_threshold_rank(n):
    a=theory.threshold_design(n)
    assert a.shape==(3,4)
    assert a.rank()==3
    assert len(a.nullspace())==1

@pytest.mark.parametrize('n',range(1,13))
def test_mass_rescaling_exact_null(n):
    M=theory.threshold_design(n)
    assert M*sp.Matrix([sp.Rational(2*n,3),0,1,1])==sp.zeros(3,1)

@pytest.mark.parametrize('n',range(1,8))
def test_threshold_fit_cannot_independently_predict(n):
    M=theory.threshold_design(n)
    assert M.rank()<M.cols
    # rank argument leaves one continuously free parameter for mass scale.

@pytest.mark.parametrize('delta',[-7,-1,sp.Rational(1,2),1,3,20])
def test_exact_observation_invariant_under_common_threshold_shift(delta):
    M=theory.threshold_design(2)
    base=sp.Matrix([sp.Rational(71),sp.Rational(38),sp.Rational(4),sp.Rational(23)])
    shifted=base+delta*sp.Matrix([sp.Rational(4,3),0,1,1])
    assert M*base == M*shifted

def test_fixed_mass_three_params_mathematically_fit_three_values():
    assert theory.threshold_design(2)[:,[0,1,3]].det()==sp.Rational(176,15)

def test_threshold_complete_multiplet_equal_shifts():
    assert [theory.DB_D[i]+theory.DB_T[i] for i in range(3)]==[sp.Rational(2,3)]*3

@pytest.mark.parametrize('rho', [0.1,1,2,5,10])
def test_bpst_total_charge_independent_scale(rho):
    mp.mp.dps=50
    val=theory.bpst_radial_integral(mp.inf,mp.mpf(str(rho)),precision=50)
    assert abs(val-1)<mp.mpf('1e-42')

@pytest.mark.parametrize('rho', [0.2,1,3])
@pytest.mark.parametrize('k',[0.1,0.3,1.0,2.0,10.0])
def test_bpst_cumulative_matches_independent_quadrature(rho,k):
    mp.mp.dps=50
    upper=mp.mpf(str(rho))*mp.mpf(str(k))
    q=theory.bpst_cumulative(upper,mp.mpf(str(rho)))
    num=theory.bpst_radial_integral(upper,mp.mpf(str(rho)),precision=50)
    assert abs(q-num)<mp.mpf('1e-42')

def test_bpst_boundary_values():
    assert theory.bpst_cumulative(0)==0
    assert abs(theory.bpst_cumulative(1)-mp.mpf('0.5'))<1e-13

@pytest.mark.parametrize('rho',[0.1,0.8,1,100])
def test_bpst_density_positive(rho):
    assert all(theory.bpst_density(r,rho)>0 for r in (0,0.1,1,100))

def test_bpst_symbolic_integral():
    assert theory.bpst_normalization_symbolic()==1

def test_bpst_full_field_strength_18_component_identity():
    assert theory.bpst_field_strength_identity()==18

@pytest.mark.parametrize('n',[1,2,3,4,5,8])
def test_torus_translations_commute(n):
    c=theory.compact_torus_translation_commutator(n)
    assert len(c)==n**3
    assert all(v==0 for v in c.values())

def test_dimension_c_hbar_cannot_make_G():
    d=theory.g_dimension_exponents()
    assert not d['without_curvature']
    assert d['with_curvature']==[{sp.Symbol('a'):3,sp.Symbol('b'):-1,sp.Symbol('d'):-2}]

@pytest.mark.parametrize('scale',[1e12,5.053091634e13,1e15,1e16,1e17])
def test_proton_lifetime_scaling(scale):
    expected=8e34*(scale/1e16)**4
    assert theory.lifetime_from_gauge_scale(scale)==expected

def test_proton_bound_is_conditional():
    data=theory.proton_audit(5.053091634e13)
    assert data['conditional_exclusion'] is True
    assert data['bound_to_model_ratio']>1e8
    assert 7e15<data['illustrative_MX_min_GeV']<8e15
    assert theory.proton_audit(5.053091634e13,mx_equals_mu=False)['conditional_exclusion'] is None

def test_lifetime_rejects_nonphysical_values():
    with pytest.raises(ValueError):theory.lifetime_from_gauge_scale(-2)

@pytest.mark.parametrize('mass',[1,2,10,1e5])
@pytest.mark.parametrize('lam',[0,0.01,1])
def test_decoupled_scalar_has_identical_classical_vacuum(mass,lam):
    z=theory.hidden_scalar_vacuum(mass,lam)
    assert z['V_at_zero']==0
    assert z['dV_at_zero']==0
    assert z['mass_squared']==sp.sympify(mass)**2

def test_hidden_scalar_invalid_unstable_example():
    with pytest.raises(ValueError):theory.hidden_scalar_vacuum(0)
    with pytest.raises(ValueError):theory.hidden_scalar_vacuum(1,-1)

def test_v107_toy_benchmark_reproduced():
    old=v107_summary(prec=50)
    assert old['two_pairs_toy']['ordering_ok']
    mu=mp.mpf(old['two_pairs_toy']['mu_unify_GeV'])
    assert mp.mpf('5.04e13')<mu<mp.mpf('5.07e13')

def test_input_ledger_396_unique_and_unchanged_provenance():
    stat=build()
    assert stat['total']==stat['unique_ids']==396
    assert set(stat['focused_ids'])==set(SPECIAL)
    with INPUT.open(encoding='utf-8-sig',newline='') as f: original=list(csv.DictReader(f))
    with OUTPUT.open(encoding='utf-8-sig',newline='') as f: audited=list(csv.DictReader(f))
    assert [(x['canonical_id'],x['evidence_state'],x['acceptance']) for x in original]==[(x['canonical_id'],x['evidence_state'],x['acceptance']) for x in audited]
    assert all(x['v108_original_goal_closed'] in ('NO','NOT_A_NEW_GOAL') for x in audited)

@pytest.mark.parametrize('id,expected',[('U107-05','ONE_LOOP_FIT_NOT_PREDICTION'),('U107-06','CONDITIONALLY_RULED_OUT_SIMPLE_GUT'),('U107-09','BPST_MATH_EXAMPLE_DONE_ROOT_ORIGIN_OPEN'),('U107-10','OPEN_GAUGE_ORIGIN'),('U107-11','OPEN_G_ORIGIN'),('U107-12','OPEN_EMPIRICAL')])
def test_critical_open_issue_was_not_silently_closed(id,expected):
    with OUTPUT.open(encoding='utf-8-sig',newline='') as f: entries={row['canonical_id']:row for row in csv.DictReader(f)}
    assert entries[id]['v108_status']==expected
    assert entries[id]['v108_original_goal_closed']=='NO'

@pytest.mark.parametrize('negative',[(-1,1),(1,-1)])
def test_bpst_reject_invalid_radius(negative):
    r,rho=negative
    with pytest.raises(ValueError): theory.bpst_density(r,rho)

@pytest.mark.parametrize('seed',range(20))
def test_bpst_increasing_charge(seed):
    a=0.05+seed*0.21
    assert theory.bpst_cumulative(a)<theory.bpst_cumulative(a+0.15)


def test_bpst_cumulative_infinite_limit():
    assert theory.bpst_cumulative(mp.inf)==1
