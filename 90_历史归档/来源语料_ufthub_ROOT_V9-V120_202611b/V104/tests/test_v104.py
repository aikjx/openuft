import math
from pathlib import Path
import numpy as np
import pytest
from src.v104_core import (C,skew_cross,lorentz_design,lorentz_observations,reconstruct_fields,
    exact_rank,dimensionless_field_example,lorentz_trajectory_force,boost_circle_axis,
    wavy_planar_total_curvature,bound_radiation_nontrivial_knot,ELEM_CHARGE)
from src.dimensions import scan
from src.audit import triage

ROOT=Path(__file__).resolve().parents[1]

@pytest.mark.parametrize('v',[(1,2,3),(0,0,0),(-1,0,4),(0.1,-3,9)])
def test_cross(v):
    b=np.array([3.1,-2.5,1.7])
    assert np.allclose(skew_cross(v)@b,np.cross(v,b))

@pytest.mark.parametrize('n,expect',[(1,3),(2,5),(3,6)])
def test_rank(n,expect):
    bb=np.array([[0.1,0.2,0.3],[-0.2,0.1,0.1],[0.0,-0.2,0.3]])[:n]
    assert exact_rank(bb)==expect

@pytest.mark.parametrize('seed',range(16))
def test_generic_3_probes_full_rank(seed):
    rng=np.random.default_rng(seed)
    b=rng.uniform(-0.35,0.35,size=(3,3))
    assert exact_rank(b)==6

@pytest.mark.parametrize('seed',range(16))
def test_distinct_2_probes_rank5(seed):
    rng=np.random.default_rng(seed)
    b=rng.uniform(-0.35,0.35,size=(2,3))
    assert exact_rank(b)==5

@pytest.mark.parametrize('theta', [0.1,0.3,0.7,1.3])
def test_collinear_velocity_difference(theta):
    a=np.array([[0.0,0.0,0.2],[theta*0.2,0.0,0.2],[theta*0.4,0.0,0.2]])
    assert exact_rank(a)==5

@pytest.mark.parametrize('seed',range(12))
def test_fields_reconstructed(seed):
    rng=np.random.default_rng(seed)
    v=rng.uniform(-0.22,0.22,size=(4,3))
    E=rng.uniform(-3,3,size=3)
    B=rng.uniform(-1e-8,1e-8,size=3)
    fit=reconstruct_fields(v,lorentz_observations(v,E,B))
    assert np.allclose(fit['E_V_per_m'],E,rtol=0,atol=1e-13)
    assert np.allclose(fit['B_T'],B,rtol=0,atol=5e-22)
    assert fit['residual_norm']<1e-12


def test_single_velocity_nullspace():
    b=np.array([0.1,0.2,-0.3]); dB=np.array([3e-9,2e-9,-1e-9]); dE=-np.cross(b,C*dB)
    assert np.linalg.norm(lorentz_design([b])@np.r_[dE,C*dB])<1e-14


def test_two_velocity_nullvector():
    v=np.array([[0.1,0.2,0.3],[-0.2,0.1,0.1]])
    dB=v[1]-v[0]
    dE=-np.cross(v[0],dB)
    assert np.linalg.norm(lorentz_design(v)@np.r_[dE,dB])<1e-13


def test_underidentified_rejected():
    with pytest.raises(ValueError): reconstruct_fields([[0.1,0.2,0.3]],np.zeros(3))


def test_superluminal_rejected():
    with pytest.raises(ValueError): lorentz_design([[0,0,1]])


def test_force_frenet_components():
    m=1.2;v=0.6*C; a=12.0;kappa=0.02
    T=np.array([1.,0.,0.]);N=np.array([0.,1.,0.]);g=1/math.sqrt(1-0.6**2)
    F=lorentz_trajectory_force(m,v,a,kappa,T,N)
    assert math.isclose(F[0],g**3*m*a,rel_tol=1e-14)
    assert math.isclose(F[1],g*m*v*v*kappa,rel_tol=1e-14)


def test_force_straight_tangential_nonzero():
    v=0.1*C
    F=lorentz_trajectory_force(1.0,v,1e4,0,[1,0,0],[0,1,0])
    assert F[0]>0 and F[1]==0


@pytest.mark.parametrize('u',[-0.7*C,-0.4*C,0.0,0.1*C,0.4*C,0.8*C])
def test_proper_acceleration_invariant(u):
    r=boost_circle_axis(0.01,0.6*C,u)
    assert math.isclose(r['proper_acc_original'],r['proper_acc_boost'],rel_tol=2e-14)
    if u!=0: assert abs(r['torsion_boost'])>0


@pytest.mark.parametrize('k,a',[(5,0.2),(7,0.2),(8,0.2),(10,0.2)])
def test_planar_unknot_curvature_above_fourpi(k,a):
    r=wavy_planar_total_curvature(k,a)
    assert r['total_curvature']>4*math.pi
    assert 'UNKNOT' in r['topology']


def test_radiation_bound_scaling():
    d1=bound_radiation_nontrivial_knot(ELEM_CHARGE,0.1*C,.16)
    d2=bound_radiation_nontrivial_knot(ELEM_CHARGE,0.1*C,.32)
    assert math.isclose(d1['E_min_J']/d2['E_min_J'],2)
    assert math.isclose(d1['P_min_W']/d2['P_min_W'],4)
    assert math.isclose(d1['E_min_J']/d1['T_s'],d1['P_min_W'])


def test_dimensions_has_expected_invalids():
    a=scan();wrong=[x for x in a if not x['passes']]
    assert len(a)>=12 and len(wrong)==5
    assert 'incorrect E = B' in {x['label'] for x in wrong}


def test_ledger369_integrity(tmp_path):
    orig=ROOT/'ledger/LEGACY_369_ORIGINAL.csv'
    counts=triage(orig,tmp_path/'review.csv')
    assert sum(counts.values())==369
    import csv
    rows=list(csv.DictReader(open(tmp_path/'review.csv',encoding='utf-8-sig')))
    assert len(rows)==369
    assert len({x['canonical_id'] for x in rows})==369
    r={x['id']:x for x in rows}
    assert r['A01']['new_evidence_class']=='DIAGNOSTIC_CLOSED_GOAL_OPEN'
    assert r['V103-369']['new_evidence_class']=='OPEN_FOUNDATIONAL'


def test_previous_dataset_exists_and_finite():
    pts=np.loadtxt(ROOT/'data/V100_ORBIT_21Q_INPUT_THEORY.csv',delimiter=',',skiprows=1)
    assert pts.shape==(1201,3) and np.isfinite(pts).all()


def test_force_field_observations():
    v,E,B,y=dimensionless_field_example()
    assert np.allclose(y.reshape(3,3)[0],E+np.cross(v[0],C*B))
    fit=reconstruct_fields(v,y)
    assert np.linalg.norm(fit['E_V_per_m']-E)<1e-13
