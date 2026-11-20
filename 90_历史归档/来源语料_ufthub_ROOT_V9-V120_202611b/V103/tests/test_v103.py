import math,json
from pathlib import Path
import numpy as np
import pytest
from scipy.constants import c,e,m_e
from src.v103_core import *
from src.symbolic import audit
ROOT=Path(__file__).resolve().parents[1]

def test_circle_energy_formula():
    R=.005; b=.1;g=discrete_geometry(circle(R,N=5000))
    analytic=curve_radiation(2*math.pi/R,b)
    assert abs(curve_radiation(g['K2'],b)/analytic-1)<1e-6

def test_trefoil_total_curvature():
    g=discrete_geometry(trefoil_torus(N=6000))
    assert g['K']>4*math.pi
    assert g['K2']*g['L']>=g['K']**2-1e-10

def test_topological_floor():
    geom=discrete_geometry(trefoil_torus(N=4000)); b=.1
    assert curve_radiation(geom['K2'],b)>=knot_energy_floor(geom['L'],b)

def test_v100_input_reproduction():
    p=np.loadtxt(ROOT/'data/V100_ORBIT_21Q_INPUT_THEORY.csv',skiprows=1,delimiter=',')
    geom=discrete_geometry(p);v=supply_budget(geom['L'],geom['K2'],.1)
    assert abs(geom['L']/.1618828928-1)<1e-7
    assert abs(v['energy_rad_J']/(9.56759915e-28)-1)<1e-6
    assert 6<v['ratio_to_floor']<7

def test_power_budget():
    geom=discrete_geometry(circle(R=.01,N=2000))
    d=supply_budget(geom['L'],geom['K2'],.1)
    assert math.isclose(d['avg_power_W'],d['energy_rad_J']/d['period_s'],rel_tol=1e-13)
    assert math.isclose(d['compensation_voltage_V']*e,d['energy_rad_J'],rel_tol=1e-13)

def test_boosted_circle_is_helix():
    d=boosted_circle()
    assert d['lab_torsion_inv_m']==0
    assert abs(d['boosted_torsion_inv_m'])>0
    assert d['invariant_relative_error']<1e-12

@pytest.mark.parametrize('boost',[-.8,-.5,-.3,.0,.3,.5,.8])
def test_proper_accel_invariant(boost):
    d=boosted_circle(beta_particle=.6,beta_boost=boost)
    assert d['invariant_relative_error']<2e-12

@pytest.mark.parametrize('beta',[.001,.01,.1,.2,.4,.6,.8,.95])
def test_positive_floor(beta):
    assert knot_energy_floor(.15,beta)>0

@pytest.mark.parametrize('beta',[.02,.1,.4,.7])
def test_scaling_L_floor(beta):
    a=knot_energy_floor(.1,beta)
    b=knot_energy_floor(.2,beta)
    assert math.isclose(a,2*b,rel_tol=2e-14)

def test_symbolic():
    assert len(audit())==9

def test_failure_inputs():
    with pytest.raises(ValueError):gamma_beta(1)
    with pytest.raises(ValueError):knot_energy_floor(-1,.1)
    with pytest.raises(ValueError):knot_energy_floor(1,.1,0)

def test_saved_summary():
    d=json.loads((ROOT/'results/V103_THEORY_SUMMARY.json').read_text(encoding='utf-8'))
    assert d['model']=='CLASSICAL_THEORY_ONLY'
    assert d['radiation_and_power']['energy_rad_J']>0
