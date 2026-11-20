from dataclasses import replace
from decimal import Decimal
import math
import numpy as np
import pytest
from src.quantum_gravity_audit import (Config,G,HBAR,C,E_CHARGE,EPS0,KE,PLANCK_LENGTH_SQUARED,EFT_LOOP_C,
    branch_distances,geom,cross,scale_terms,phases,pure_concurrence,rho_dephased,negativity,
    partial_transpose,locc_correlated_phase_state,q_equivalent,two_coupling_design,
    sphere_radius,scaled_design,null_projection,decimal_null_determinant,stats)

P=Config(); D=(450e-6,600e-6,850e-6)

def close(a,b,rtol=1e-11,atol=0):return math.isclose(a,b,rel_tol=rtol,abs_tol=atol)

def test_constants():
    assert C==299792458 and G==6.67430e-11
    assert 1e-35 < math.sqrt(PLANCK_LENGTH_SQUARED)<2e-35

def test_branch_matrix():
    r=branch_distances(P)
    assert r.shape==(2,2)
    assert np.allclose(r*1e6,[[450,650],[250,450]],rtol=1e-14,atol=1e-12)

def test_geometric_cross():
    r=branch_distances(P)
    assert close(geom(P,1),cross(1/r))
    assert geom(P,1)<0

def test_phase_agrees_catalog():
    assert close(cross(phases(P)), -0.06923945973538509)
    assert close(pure_concurrence(phases(P)),0.03461281484279082)

def test_phase_decomposition():
    terms=scale_terms(P)
    assert close(terms['newton'],cross(phases(P)))
    assert close(terms['one_pn_potential'],-2.3942485079357935e-38)
    assert close(terms['eft_loop_potential'],-9.859101158802694e-64)
    assert close(terms['eft_over_newton'],1.4239136464209242e-62)

def test_only_newton_beyond_eft_float_resolvable():
    assert np.array_equal(phases(P,include_pn=True,include_eft=True),phases(P))
    assert scale_terms(P)['eft_loop_potential']!=0

def test_two_body_phase_hermiticity():
    r=rho_dephased(P)
    assert np.allclose(r,r.conj().T)
    assert close(np.trace(r).real,1)
    assert np.linalg.eigvalsh(r).min()>-1e-14

def test_max_entangled_pure_state_formula():
    assert close(negativity(rho_dephased(P)),pure_concurrence(phases(P))/2)

def test_partial_transpose_involutive():
    rho=rho_dephased(P)
    assert np.allclose(partial_transpose(partial_transpose(rho)),rho)

def test_zero_time():
    p=replace(P,t=0)
    assert close(cross(phases(p)),0,atol=1e-16)
    assert negativity(rho_dephased(p))<1e-12

def test_mass_time_scaling():
    assert close(cross(phases(replace(P,m1=2e-14))),2*cross(phases(P)))
    assert close(cross(phases(replace(P,t=3))),3*cross(phases(P)))

def test_s1_zero():
    assert close(geom(replace(P,s1=0),1),0,atol=2e-12)

def test_s2_zero():
    assert close(geom(replace(P,s2=0),1),0,atol=2e-12)

def test_symmetry_of_masses():
    assert close(cross(phases(replace(P,m1=2e-14,m2=1e-14))),cross(phases(replace(P,m1=1e-14,m2=2e-14))))

def test_dephasing_reduces_negativity():
    p2=replace(P,gamma1=.05,gamma2=.05)
    assert 0<=negativity(rho_dephased(p2))<=negativity(rho_dephased(P))

def test_large_dephasing_separable():
    assert negativity(rho_dephased(replace(P,gamma1=100,gamma2=100)))<1e-12

def test_classical_mixture_separable():
    r=locc_correlated_phase_state(n=100,seed=123)
    assert negativity(r)<1e-12
    assert np.linalg.eigvalsh(r).min()>-1e-13

def test_charge_equality_cancels():
    q=q_equivalent(P)
    assert close(q,8.617517200509683e-25)
    assert abs(cross(phases(replace(P,q1=q,q2=q))))<2e-15

def test_opposite_charges_double():
    q=q_equivalent(P)
    assert close(cross(phases(replace(P,q1=q,q2=-q))),2*cross(phases(P)))

def test_1PN_and_EFT_units():
    T=scale_terms(P)
    assert close(T['pn_length_m']/P.d,9.901547025491554e-38)
    assert close(T['eft_length_squared_m2']/P.d**2,1.6835605183098466e-63)

def test_spherical_source_nonoverlap():
    r=sphere_radius(P.m1,P.rho1)
    assert 1e-7<r<2e-6
    assert min(branch_distances(P).reshape(-1))>2*r

def test_coulomb_and_G_rank1():
    mat=two_coupling_design(P,D)
    assert mat.shape==(3,2)
    assert np.linalg.matrix_rank(mat)==1
    assert np.array_equal(mat[:,0],-mat[:,1])

def test_null_filter():
    f=null_projection(P,D)
    assert abs(f['cancellation_1'])<1e-12
    assert abs(f['cancellation_2'])<1e-12
    assert 0<f['angle_sine']<1
    assert f['float_false_signal_ratio']>1e30

def test_90digit_recovery():
    d=decimal_null_determinant(P,D,prec=90)
    total=Decimal(d['total_projection']);loop=Decimal(d['quantum_only_projection'])
    assert abs((total-loop)/loop)<Decimal('1e-20')
    assert abs(Decimal(d['null_newton']))<Decimal('1e-85')
    assert abs(Decimal(d['null_pn']))<Decimal('1e-85')

def test_unequal_branches_decimal_geometry():
    p=replace(P,s1=100e-6,s2=175e-6)
    dd=decimal_null_determinant(p,D,prec=90)
    assert abs(Decimal(dd['null_newton']))<Decimal('1e-85')
    assert abs(Decimal(dd['null_pn']))<Decimal('1e-85')

def test_concurrence_local_phases():
    z=np.array([[0.1,0.3],[0.7,0.9]])
    assert pure_concurrence(z)<1e-14

def test_total_pn_loop_not_resolved_at_binary64():
    T=scale_terms(P)
    assert T['total']==T['newton']

def test_report_labels():
    r=stats(P)
    assert 'SYNTHETIC' in r['labels']
    assert r['negativity']>0
    assert r['sphere_radii_m'][0]<P.d

@pytest.mark.parametrize('mass', [1e-17,1e-16,1e-15,1e-14,1e-13,1e-12])
def test_mass_squared_scaling(mass):
    p=replace(P,m1=mass,m2=mass)
    r=replace(P,m1=mass*2,m2=mass*2)
    assert close(geom(p,1),geom(r,1))
    assert close(cross(phases(r)),4*cross(phases(p)))

@pytest.mark.parametrize('t', [0,0.001,0.01,0.1,0.7,3,10])
def test_time_scaling(t):
    p=replace(P,t=t)
    assert close(cross(phases(p)),t*cross(phases(P)),atol=1e-15)

@pytest.mark.parametrize('d', [300e-6,400e-6,450e-6,600e-6,1000e-6,1.5e-3])
def test_monotone_distance(d):
    v=abs(cross(phases(replace(P,d=d))))
    v2=abs(cross(phases(replace(P,d=d*1.2))))
    assert v>v2

@pytest.mark.parametrize('gamma', [0.001,.005,.015,.025,.04,.06,.2,1.0])
def test_dephasing_psd(gamma):
    p=replace(P,gamma1=gamma,gamma2=gamma)
    r=rho_dephased(p)
    assert close(float(np.trace(r).real),1)
    assert np.linalg.eigvalsh(r).min()>-1e-14
    assert negativity(r)>=0

@pytest.mark.parametrize('bad', [
    dict(m1=0),dict(m2=-1),dict(d=0),dict(d=1e-6),dict(d=1e-4),
    dict(s1=-1),dict(s2=-1),dict(t=-1),dict(gamma1=-1),dict(gamma2=-1),
    dict(rho1=0),dict(rho2=-1),dict(q1=float('nan')),dict(m1=float('inf')),
])
def test_invalid_parameter_rejected(bad):
    with pytest.raises(ValueError): replace(P,**bad).valid()

def test_overlap_sphere_rejected():
    with pytest.raises(ValueError):replace(P,d=205e-6,m1=1e-8,m2=1e-8).valid()

def test_wrong_shape_rejected():
    with pytest.raises(ValueError):cross(np.zeros((3,3)))
    with pytest.raises(ValueError):partial_transpose(np.eye(3))

def test_invalid_inverse_power():
    with pytest.raises(ValueError):geom(P,0)

def test_invalid_distance_list():
    with pytest.raises(ValueError):two_coupling_design(P,(450e-6,))
    with pytest.raises(ValueError):null_projection(P,(450e-6,600e-6))

def test_invalid_L():
    with pytest.raises(ValueError):scaled_design(P,D,0)
    with pytest.raises(ValueError):scaled_design(P,D,-1)

def test_null_filter_degenerate():
    with pytest.raises(ValueError):null_projection(P,(450e-6,)*3)
