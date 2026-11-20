import sys,math,json
from pathlib import Path
import numpy as np
import pytest
from scipy.constants import c,e
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from v101_core import *
from symbolic_checks import run_symbolic

@pytest.mark.parametrize('beta',[.01,.1,.2,.5,.9])
def test_gamma(beta):
    assert gamma_beta(beta)>1

def test_gamma_rejects():
    for x in [0,1,1.1,-1]:
        with pytest.raises(ValueError):gamma_beta(x)

def test_knot_factor_four():
    for beta in [.01,.1,.9]:
        b=radiation_bounds(.16,beta)
        assert b['knotted_lower_J']==pytest.approx(4*b['ordinary_closed_lower_J'],rel=1e-14)

def test_symmetric_radiation_charge():
    assert radiation_coefficient(e,.1)==radiation_coefficient(-e,.1)

def test_radiation_speed_scaling():
    vals=[radiation_bounds(.16,b)['knotted_lower_J'] for b in [.01,.1,.5]]
    assert vals[0]<vals[1]<vals[2]

def test_radiation_length_scaling():
    a=radiation_bounds(.1)['knotted_lower_J']
    b=radiation_bounds(.2)['knotted_lower_J']
    assert a==pytest.approx(2*b)

def test_circular_fenchel_bound():
    g=polygon_geometry(circular_trajectory(4000))
    assert abs(g['total_curvature']-2*math.pi)<1e-6
    assert g['cauchy_ratio']>=1-1e-10
    assert abs(g['cauchy_ratio']-1)<1e-8

@pytest.mark.parametrize('p,q',[(2,3),(3,4),(2,5),(3,5)])
def test_torus_nontrivial_knots_curvature(p,q):
    g=polygon_geometry(torus_knot_polygon(p,q,num=6000))
    assert g['total_curvature']>4*math.pi
    assert g['cauchy_ratio']>=1-1e-12

def test_maxwell_parallel_component_invisible_to_orbit():
    for C in [-1e-4,0,1e-4,3e-4]:
        a=magnetic_degeneracy(C_T_m=C)
        assert np.allclose(a['force1_N'],a['force2_N'],rtol=1e-14,atol=1e-26)
        assert np.allclose(a['force1_N'],a['centripetal_N'],rtol=1e-14,atol=1e-26)

def test_parallel_field_changes_energy_density():
    a=magnetic_degeneracy(C_T_m=1e-4)
    assert a['field_energy_density_difference_at_orbit_J_m3']>0

def test_v100_archive_independent_radiation():
    g=compute_v100(ROOT/'results/V100_ORBIT_21Q_INPUT.csv',ROOT/'results/V100_RADIATION_INPUT.json')
    assert g['total_curvature']>4*math.pi
    assert g['polygon_radiation_J']>g['known_total_curvature_lower_J']
    assert g['radiation_over_knot_floor']>6
    assert g['independent_vs_historical_relative_error']<1e-3
    assert abs(g['radiation_over_curvature_floor']-1)<1e-3

def test_v100_pumping_positive():
    g=compute_v100(ROOT/'results/V100_ORBIT_21Q_INPUT.csv',ROOT/'results/V100_RADIATION_INPUT.json')
    assert g['required_energy_per_charge_V']>0
    assert g['minimum_avg_tangential_E_V_m']>0

def test_invalid_parameters():
    with pytest.raises(ValueError): radiation_bounds(-1)
    with pytest.raises(ValueError): magnetic_degeneracy(r=0)

def test_symbolic_checks_all_pass():
    assert all(run_symbolic().values())
