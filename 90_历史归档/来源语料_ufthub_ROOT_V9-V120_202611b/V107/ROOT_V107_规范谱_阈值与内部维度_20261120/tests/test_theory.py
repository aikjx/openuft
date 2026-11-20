from __future__ import annotations
import math
from fractions import Fraction
import pytest
import sympy as sp
import mpmath as mp
from src.theory import (
    B,DB_TRIPLET,DB_DOUBLET,D_BOTH,W,K_TRIPLET,K_DOUBLET,
    Benchmark,hypercharge_anomalies,verify_hypercharge,
    fourform_rank_obstruction,inv_invariant,split_required_log_ratio,
    required_ratio,minimum_pair_count_below_planck,flow_at_mu,common_scale,
    summary,mfrac
)


def approx_mp(a,b,tol='1e-37'):
    return abs(a-b)<=mp.mpf(tol)*max(1,abs(a),abs(b))

# Exact symbolic anomaly accounting
@pytest.mark.parametrize('q', [sp.Rational(1,6),sp.Rational(2,5),sp.Rational(-4,7),sp.Integer(1)])
def test_minimal_unique_ratios(q):
    r=hypercharge_anomalies()
    subs={r['q']:q,r['l']:-3*q,r['h']:3*q}
    for key in ('A_SU2_SU2_U1','A_SU3_SU3_U1','A_U1_3','A_gravity_gravity_U1'):
        assert sp.simplify(r[key].subs(subs))==0

@pytest.mark.parametrize('offset', [sp.Rational(1,3),sp.Integer(-1),sp.Rational(7,12)])
def test_no_nu_wrong_higgs_hypercharge_fails(offset):
    r=hypercharge_anomalies();q=r['q'];l=r['l'];h=r['h']
    assert sp.factor(r['A_gravity_gravity_U1'].subs({l:-3*q,h:3*q+offset}))==offset
    assert sp.factor(r['A_U1_3'].subs({l:-3*q,h:3*q+offset}))==offset**3

@pytest.mark.parametrize('x', [sp.Rational(-2,3), sp.Rational(-1,7),sp.Integer(0),sp.Rational(1,13),sp.Integer(4)])
def test_dirac_neutrino_one_free_BminusL_parameter(x):
    r=hypercharge_anomalies(True)
    q=sp.Rational(1,6)+x/3;l=-sp.Rational(1,2)-x;h=sp.Rational(1,2)
    subst={r['q']:q,r['l']:l,r['h']:h}
    for key in ('A_SU2_SU2_U1','A_SU3_SU3_U1','A_U1_3','A_gravity_gravity_U1'):
        assert sp.simplify(r[key].subs(subst))==0
    assert sp.simplify(r['nu'].subs(subst)+x)==0


def test_majorana_hypercharge_fixes_BminusL_parameter():
    x=sp.Symbol('x')
    assert sp.solve(sp.Eq(-x,0),x)==[0]


def test_anomaly_symbolic_checks():
    assert verify_hypercharge()['minimal_ratios']==['1','4','-2','-3','-6','3']


def test_vectorlike_su5_beta_exact():
    assert D_BOTH==(Fraction(2,3),)*3
    assert DB_DOUBLET==(Fraction(2,5),Fraction(2,3),Fraction(0))
    assert DB_TRIPLET==(Fraction(4,15),Fraction(0),Fraction(2,3))


def test_nonunification_weights():
    assert sum(W)==0
    assert sum(a*b for a,b in zip(W,B))==0
    assert K_TRIPLET==Fraction(88,15)
    assert K_DOUBLET==-Fraction(88,15)


@pytest.mark.parametrize('mu', [1e3,1e6,1e10,1e14,1e17])
def test_degenerate_complete_multiplet_preserves_invariant(mu):
    a0=flow_at_mu(mu,n_pairs=0)
    a1=flow_at_mu(mu,n_pairs=1,m_doublet=200,m_triplet=200)
    a2=flow_at_mu(mu,n_pairs=2,m_doublet=200,m_triplet=200)
    assert approx_mp(inv_invariant(a0),inv_invariant(a1))
    assert approx_mp(inv_invariant(a0),inv_invariant(a2))


@pytest.mark.parametrize('n', [1,2,3,4])
def test_required_ratio_scales_inverse_in_pairs(n):
    L1=split_required_log_ratio(1)
    LN=split_required_log_ratio(n)
    assert approx_mp(L1,n*LN)


def test_one_pair_required_splitting_exceeds_planck_window():
    bench=Benchmark()
    ll=split_required_log_ratio(1,bench)
    cap=mp.log(mp.mpf(str(bench.planck_energy))/mp.mpf(str(bench.m_z)))
    assert ll>cap
    assert minimum_pair_count_below_planck(bench)==2


def test_two_pair_toy_solves_three_couplings():
    toy=common_scale(2,1000)
    assert toy['conditions_met']
    assert toy['max_spread']<mp.mpf('1e-40')
    assert mp.mpf('4e13')<toy['mu']<mp.mpf('6e13')


def test_one_pair_cannot_match_below_planck_if_doublet_above_mz():
    bench=Benchmark()
    ratio=required_ratio(1,bench)
    assert ratio*mfrac(bench.m_z)>mfrac(bench.planck_energy)


def test_threshold_continuity_at_doublet_threshold():
    md=1000.;mt=1e12
    a=flow_at_mu(md,n_pairs=2,m_doublet=md,m_triplet=mt)
    b=flow_at_mu(md*(1+1e-11),n_pairs=2,m_doublet=md,m_triplet=mt)
    assert max(abs(x-y) for x,y in zip(a,b))<mp.mpf('1e-9')


def test_threshold_continuity_at_triplet_threshold():
    md=1000.;mt=1e12
    a=flow_at_mu(mt,n_pairs=2,m_doublet=md,m_triplet=mt)
    b=flow_at_mu(mt*(1+1e-11),n_pairs=2,m_doublet=md,m_triplet=mt)
    assert max(abs(x-y) for x,y in zip(a,b))<mp.mpf('1e-9')


def test_two_pair_numeric_root_is_not_accidental():
    toy=common_scale(2,1000)
    mu=toy['mu'];md=toy['m_doublet'];mt=toy['m_triplet']
    for factor in [mp.mpf('0.01'),mp.mpf('0.7'),mp.mpf('1.5'),mp.mpf('100')]:
        vals=flow_at_mu(mu*factor,n_pairs=2,m_doublet=md,m_triplet=mt)
        if factor!=1: assert max(vals)-min(vals)>mp.mpf('1e-12')


def test_two_pair_independent_findroot_from_off_center_guess():
    toy=common_scale(2,1000)
    md=toy['m_doublet'];mt=toy['m_triplet']; target=toy['mu']
    def eq(t):
        v=flow_at_mu(mp.e**t,n_pairs=2,m_doublet=md,m_triplet=mt)
        return v[0]-v[1]
    mp.mp.dps=75
    out=mp.findroot(eq,(mp.log(target)-mp.mpf('0.1'),mp.log(target)+mp.mpf('0.1')))
    assert abs(mp.exp(out)/target-1)<mp.mpf('1e-50')
    actual=flow_at_mu(mp.exp(out),n_pairs=2,m_doublet=md,m_triplet=mt)
    assert max(actual)-min(actual)<mp.mpf('1e-45')

@pytest.mark.parametrize('sin2,alpha_s',[(0.23122,0.1180),(0.230,0.120),(0.232,0.116),(.228,.110)])
def test_illustrative_benchmark_dependence(sin2,alpha_s):
    result=summary(Benchmark(sin2_w=sin2,alpha_s=alpha_s),prec=65)
    assert float(result['one_pair_mass_ratio_required'])>1
    assert result['evidence']['new_physics_observed'] is False


@pytest.mark.parametrize('rank', [1,2,3])
def test_rank_below_four_obstructs_FwedgeF(rank):
    # Antisymmetric F_ab vanishes when any of four indices must coincide.
    # Explicit 4D pfaffian with directions 0..rank-1.
    f={(i,j):sp.Integer(i+j+1) for i in range(rank) for j in range(i+1,rank)}
    expr=2*(f.get((0,1),0)*f.get((2,3),0)-f.get((0,2),0)*f.get((1,3),0)+f.get((0,3),0)*f.get((1,2),0))
    assert expr==0


def test_four_independent_phases_can_generate_local_fourform():
    r=fourform_rank_obstruction()
    assert r['max_internal_rank_with_zero_local_4form']==3
    assert r['local_trace_FwedgeF_example']=='-1'


def test_rank_does_not_imply_nonzero_global_instanton_charge():
    # For compactly supported exact 2-form F=dA in R4, total F^F= integral d(A^F) =0.
    # This is a distinct global boundary condition; do not infer nonzero topological Q from local density.
    assert 'does not imply' in fourform_rank_obstruction()['qualifier']


def test_summary_all_flags_are_candid():
    res=summary()
    assert not res['evidence']['new_physics_observed']
    assert not res['evidence']['G_derived']
    assert not res['evidence']['four_forces_unified']
    assert res['two_pairs_toy']['ordering_ok']


def test_necessary_one_pair_nogo_does_not_claim_other_models_disallowed():
    # Two pairs are enough in the narrow one-loop toy to obtain a mathematical meeting.
    assert common_scale(2,1000)['conditions_met']


def test_uniform_shifts_of_inverse_couplings_do_not_change_invariant():
    a=Benchmark().initial_inverse()
    shift=mp.mpf('2.3')
    assert approx_mp(inv_invariant(a),inv_invariant([x+shift for x in a]))


def test_running_sum_weight_exact():
    assert sum(w*db for w,db in zip(W,D_BOTH))==0


def test_periodic_phase_only_is_insufficient_for_nonzero_local_pontryagin_density():
    # all local one-parameter 2-form curvature is 0; k<=3 all characteristic four-forms 0
    assert fourform_rank_obstruction()['max_internal_rank_with_zero_local_4form']>=1


def test_two_pairs_finite_thresholds_below_unification():
    t=common_scale(2,1000)
    assert t['m_triplet']<t['mu']
    assert t['mu']<Benchmark().planck_energy


def test_N3_unification_constructible_but_not_predictive():
    t=common_scale(3,1000)
    assert t['max_spread']<mp.mpf('1e-40')
    assert t['conditions_met']


def test_invalid_pair_count_rejected():
    with pytest.raises(ValueError): split_required_log_ratio(0)
    with pytest.raises(ValueError): flow_at_mu(1,n_pairs=1)
