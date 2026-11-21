import math
import sys
from pathlib import Path
import numpy as np
import pytest
import sympy as sp
sys.path.insert(0,str(Path(__file__).resolve().parents[1] / 'scripts'))
from v128_core import *

@pytest.mark.parametrize('ufrac',[0,0.1,0.3,-0.4,0.6,0.8,-0.75])
def test_helix_null_metric_and_geometry(ufrac):
    x=helix_kinematics(ky_electron_frequency(),ufrac*C)
    assert abs((x['R']*x['omega'])**2+(ufrac*C)**2-C*C)/C**2<2e-15
    assert math.isclose(math.hypot(x['kappa'],x['tau']),x['omega']/C, rel_tol=2e-15)

@pytest.mark.parametrize('ufrac',[0,0.1,-0.4,0.6])
@pytest.mark.parametrize('beta',[-0.7,-0.1,0.1,0.6,0.8])
def test_lorentz_boost_null_and_candidate_not_scalar(ufrac,beta):
    omega=2.4e10
    om2,u2,f=boost_helix(omega,ufrac*C,beta)
    a=helix_kinematics(omega,ufrac*C)
    b=helix_kinematics(om2,u2)
    assert math.isclose(a['R'],b['R'],rel_tol=2e-14)
    assert math.isclose(b['candidate_mass']/a['candidate_mass'],mass_candidate_ratio(ufrac,beta),rel_tol=2e-14)
    assert math.isclose((b['R']*om2)**2+u2**2,C*C,rel_tol=2e-14)

def test_fatal_boost_example():
    assert math.isclose(mass_candidate_ratio(0,0.6),0.8,rel_tol=1e-14)

def test_bad_3d_superluminal_model():
    transverse=0.2*C
    longitudinal=C
    assert math.hypot(transverse,longitudinal)>C

@pytest.mark.parametrize('alpha',[0.2,0.4,0.6,0.9])
def test_5d_null_4d_timelike(alpha):
    v3=alpha*C
    vy=math.sqrt(1-alpha*alpha)*C
    assert math.isclose(five_dim_projection(v3,vy),1-alpha*alpha,rel_tol=2e-15)

@pytest.mark.parametrize('a,b,g',[(1,2,.3),(.2,4,.9),(-2,3,1),(.1,-2,2),(0.4,0.7,1.5)])
def test_su2_curvature(a,b,g):
    F,comD,theory=su2_curvature(a,b,g)
    assert np.allclose(F,theory,rtol=0,atol=2e-15)
    assert np.allclose(comD,1j*g*F,rtol=0,atol=2e-15)

@pytest.mark.parametrize('theta',[0,2*math.pi,4*math.pi,6*math.pi])
def test_spinor_2pi_4pi(theta):
    ref=(-1)**round(theta/(2*math.pi))
    assert np.allclose(spinor_rotation(theta),ref*np.eye(2),atol=2e-15)

@pytest.mark.parametrize('i',range(4))
@pytest.mark.parametrize('j',range(4))
def test_dirac_clifford(i,j):
    gam=gamma_matrices()
    ant=gam[i]@gam[j]+gam[j]@gam[i]
    eta=[1,-1,-1,-1]
    assert np.allclose(ant,2*(eta[i] if i==j else 0)*np.eye(4),rtol=0,atol=1e-15)

@pytest.mark.parametrize('p4',[(1,0,0,0),(3,1,2,0),(0.1,0.2,-0.3,2), (17,-4,1,0), (2.1,0,0,2.1)])
def test_dirac_square(p4):
    assert squared_dirac_residual(p4) < 1e-12

def test_sphere_curvature():
    R,Rtheta = sphere_scalar_curvature()
    assert sp.simplify(R-2)==0
    theta=sp.Symbol('theta',real=True,positive=True)
    assert sp.simplify(Rtheta-sp.sin(theta)**2)==0

@pytest.mark.parametrize('g,B,A',[(1,2,3),(-2,.3,1.2),(.5,4,.2),(0,12,3)])
def test_u1_wilson_loop(g,B,A):
    z=winding_wilson_flux(g,B,A)
    assert math.isclose(abs(z),1,rel_tol=1e-15)
    assert abs(z-complex(math.cos(g*B*A),math.sin(g*B*A)))<1e-14

def test_kk_minimal_spectrum_disagrees_with_muon():
    assert abs(MUON_ELECTRON_RATIO-round(MUON_ELECTRON_RATIO))>0.2

def test_mass_frequency_no_proof_of_mass_generation():
    model=helix_kinematics(ky_electron_frequency(),0)
    # It matches exactly only because electron mass was passed into omega.
    assert math.isclose(model['candidate_mass'],ELECTRON_MASS,rel_tol=1e-14)
    second=helix_kinematics(2*ky_electron_frequency(),0)
    assert math.isclose(second['candidate_mass'],2*ELECTRON_MASS,rel_tol=1e-14)
