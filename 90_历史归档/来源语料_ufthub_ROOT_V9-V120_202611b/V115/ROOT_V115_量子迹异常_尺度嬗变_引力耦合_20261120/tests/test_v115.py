"""Run: python -m pytest tests/test_v115.py -q. No external network or experiment data."""
import sys, math
from pathlib import Path
import pytest
import numpy as np
import sympy as sp
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src import v115 as m

@pytest.mark.parametrize('nf',range(17))
def test_beta0_positive_with_n_f_below_17(nf):
    assert m.beta0_qcd(nf)>0
    assert m.beta0_qcd(nf)==pytest.approx(11-2*nf/3,abs=1e-14)

@pytest.mark.parametrize('nf',[-3, -1,17,42,3.5,'5'])
def test_invalid_nf_rejected(nf):
    with pytest.raises(ValueError):m.beta0_qcd(nf)

@pytest.mark.parametrize('nf',[0,1,2,3,4,5,6,12,16])
def test_beta_qcd_negative(nf):
    assert m.beta_alpha_qcd(.12,nf)<0

@pytest.mark.parametrize('ratio',[.15,.25,.5,1.,2.,3.,8.,15.,30.])
def test_running_scale_invariant_same_nf(ratio):
    alpha=m.run_alpha_one_loop(m.MZ_GEV*ratio,m.MZ_GEV,m.ALPHA_S_MZ,5)
    Lambda=m.lambda_qcd_one_loop(m.MZ_GEV*ratio,alpha,5)
    assert Lambda==pytest.approx(m.lambda_qcd_one_loop(m.MZ_GEV,m.ALPHA_S_MZ,5),rel=2e-14)

@pytest.mark.parametrize('alpha',[.06,.10,.118,.2,.35])
def test_running_to_reference_point(alpha):
    assert m.run_alpha_one_loop(20,20,alpha,5)==pytest.approx(alpha,rel=5e-15)

@pytest.mark.parametrize('nf',[0,3,5,6,10])
def test_log_running_derivative(nf):
    alpha=.118; mu=m.MZ_GEV; dt=1e-5
    f=lambda x:m.run_alpha_one_loop(mu*math.exp(x),mu,alpha,nf)
    derivative=(f(dt)-f(-dt))/(2*dt)
    assert derivative==pytest.approx(m.beta_alpha_qcd(alpha,nf),rel=2e-9)

@pytest.mark.parametrize('alpha',[.07,.1,.118,.15,.21])
def test_lambda_log_sensitivity_finite_differences(alpha):
    da=1e-6
    ln=lambda a:math.log(m.lambda_qcd_one_loop(m.MZ_GEV,a,5))
    actual=(ln(alpha+da)-ln(alpha-da))/(2*da)
    assert actual==pytest.approx(m.lambda_log_sensitivity(alpha,5),rel=5e-10)

@pytest.mark.parametrize('nf',[0,3,5,6,12])
def test_beta_g_trace_coefficient_same(nf):
    alpha=.118
    g=math.sqrt(4*math.pi*alpha)
    beta_g=-m.beta0_qcd(nf)*g**3/(16*math.pi**2)
    assert (beta_g/(2*g))==pytest.approx(m.qcd_beta_over_2g(alpha,nf),rel=2e-14)

@pytest.mark.parametrize('chargesum',[0.,1.,2.,4.5,7.])
def test_qed_trace_matches_beta_e(chargesum):
    alpha=.0073; e=math.sqrt(4*math.pi*alpha)
    betae=chargesum*e**3/(12*math.pi**2)
    assert betae/(2*e)==pytest.approx(m.qed_beta_over_2e(alpha,chargesum),abs=1e-16)

@pytest.mark.parametrize('zeta',[1.,10.,1e5,1e30,1e38,1e40])
def test_induced_gravity_ratio(zeta):
    scale=.2
    value=m.induced_planck_mass_gev(scale,zeta)
    assert (m.reduced_planck_mass_gev()/value)**2==pytest.approx(m.induced_G_ratio_to_observed(scale,zeta))
    assert m.induced_G_ratio_to_observed(scale,zeta)*zeta==pytest.approx(m.required_induced_zeta(scale),rel=1e-14)

@pytest.mark.parametrize('v',[.05,.1,.2,1.,246.,1e6])
def test_required_zeta_reconstructs_planck(v):
    z=m.required_induced_zeta(v)
    assert m.induced_planck_mass_gev(v,z)==pytest.approx(m.reduced_planck_mass_gev(),rel=1e-13)

@pytest.mark.parametrize('trace',[-1e-5,0.,1e-8,1.,100.])
def test_einstein_trace_only(trace):
    p=m.reduced_planck_mass_gev()
    assert m.einstein_scalar_trace_curvature(trace)==pytest.approx(-trace/p**2)

@pytest.mark.parametrize('nf',[0,1,3,5,6,16])
def test_running_increases_as_mu_decreases_above_lambda(nf):
    a=m.run_alpha_one_loop(25,100,.11,nf)
    assert a>.11

@pytest.mark.parametrize('val',[0.,-1.,float('nan')])
def test_alpha_invalid(val):
    with pytest.raises(ValueError):m.beta_alpha_qcd(val,5)

@pytest.mark.parametrize('v',[0.,-1.])
def test_vev_invalid(v):
    with pytest.raises(ValueError):m.required_induced_zeta(v)


def test_reference_pdg_inputs():
    assert m.ALPHA_S_MZ==0.118
    assert m.ALPHA_S_MZ_SIGMA==.0009
    assert m.MZ_GEV==91.1876


def test_one_loop_lambda_5_reference():
    assert m.lambda_qcd_one_loop(91.1876,.118,5)==pytest.approx(.08782708014552353,rel=1e-13)


def test_induced_zeta_imbalance():
    lam=m.lambda_qcd_one_loop(m.MZ_GEV,m.ALPHA_S_MZ,5)
    assert 7e38<m.required_induced_zeta(lam)<8e38


def test_classical_maxwell_trace_vs_quantum_anomaly():
    d=4
    assert 1-d/4 ==0
    assert m.qed_beta_over_2e(m.ALPHA_EM_LOW)>0
    assert m.qcd_beta_over_2g(.118,5)<0


def test_lambda_not_constant_if_change_nf_without_threshold_matching():
    mu0=m.MZ_GEV;alpha0=.118;mu2=1000
    alpha_wrong=m.run_alpha_one_loop(mu2,mu0,alpha0,6)
    Lambda_wrong=m.lambda_qcd_one_loop(mu2,alpha_wrong,5)
    Lambda_right=m.lambda_qcd_one_loop(mu0,alpha0,5)
    assert abs(Lambda_wrong/Lambda_right-1)>.1


def test_one_loop_strong_coupling_pole_is_not_physical_mass_gap():
    Lambda=m.lambda_qcd_one_loop(m.MZ_GEV,.118,5)
    with pytest.raises(ValueError):m.run_alpha_one_loop(.5*Lambda,m.MZ_GEV,.118,5)


def test_fixed_coupling_with_scaled_reference_has_scaled_lambda():
    l1=m.lambda_qcd_one_loop(100,.118,5)
    l2=m.lambda_qcd_one_loop(200,.118,5)
    assert l2==pytest.approx(2*l1)


def test_QCD_and_QED_coefficient_ratio_identity():
    s=.12;a=.008
    expected=-(3*m.beta0_qcd(5)*s)/(4*a)
    assert m.qcd_trace_coefficient_ratio(s,5,a,1)==pytest.approx(expected)


def test_QCD_and_QED_ratio_not_observable_without_operator_matrix_elements():
    # A coefficient ratio of G^2 and F^2 is a purely algebraic ratio;
    # the routine cannot calculate hadronic matrix elements or an experiment.
    assert m.qcd_trace_coefficient_ratio(.12,5,.008,2)==pytest.approx(
        m.qcd_trace_coefficient_ratio(.12,5,.008,1)/2)


def test_planck_mass_from_measured_G():
    assert 2.43e18<m.reduced_planck_mass_gev()<2.44e18
    assert m.induced_planck_mass_gev(m.reduced_planck_mass_gev(),1)==pytest.approx(m.reduced_planck_mass_gev())


def test_geV_conversion():
    assert m.GEV_MASS_KG==pytest.approx(1.7826619216e-27,rel=2e-10)


def test_lagrangian_does_not_predict_G_without_zeta_v():
    v=.1
    assert m.induced_G_ratio_to_observed(v,1)/m.induced_G_ratio_to_observed(v,4)==pytest.approx(4)


def test_sympy_rg_invariant_exact():
    x,b,a,u=sp.symbols('x b a u',positive=True)
    alpha=1/(1/a+b*x/(2*sp.pi))
    logL=sp.log(u)+x-2*sp.pi/(b*alpha)
    assert sp.simplify(sp.diff(logL,x))==0


def test_sympy_trace_coefficient_qcd():
    gs,b=sp.symbols('gs b',positive=True)
    alpha=gs**2/(4*sp.pi)
    assert sp.simplify((-b*gs**3/(16*sp.pi**2))/(2*gs)+b*alpha/(8*sp.pi))==0


def test_sympy_trace_coefficient_qed():
    e=sp.symbols('e',positive=True)
    alpha=e**2/(4*sp.pi)
    assert sp.simplify((e**3/(12*sp.pi**2))/(2*e)-alpha/(6*sp.pi))==0


def test_sympy_lambda_derivative():
    alpha,b=sp.symbols('alpha b',positive=True)
    logL=-2*sp.pi/(b*alpha)
    assert sp.simplify(sp.diff(logL,alpha)-2*sp.pi/(b*alpha**2))==0


def test_sympy_gravity_G_zeta_degeneracy():
    v,zeta,s=sp.symbols('v zeta s',positive=True)
    G=1/(8*sp.pi*zeta*v*v)
    # zeta->s^2 zeta, v->v/s, G unchanged.
    assert sp.simplify(G.subs({zeta:s*s*zeta,v:v/s},simultaneous=True)-G)==0


def test_sympy_dimensional_transmutation_needs_boundary_data():
    mu,a,b,s=sp.symbols('mu a b s',positive=True)
    Lam=mu*sp.exp(-2*sp.pi/(b*a))
    assert sp.simplify(Lam.subs(mu,mu*s)/Lam-s)==0


def test_sympy_classical_EM_trace_D():
    d,f2=sp.symbols('d f2')
    T=(1-d/4)*f2
    assert T.subs(d,4)==0
    assert sp.simplify(T.subs(d,5)+f2/4)==0


def test_sympy_QCD_beta_n_f():
    nf=sp.symbols('nf')
    b=11-sp.Rational(2,3)*nf
    assert b.subs(nf,5)==sp.Rational(23,3)
    assert b.subs(nf,6)==7


def test_sympy_reduced_planck_relation():
    v,z,G=sp.symbols('v z G',positive=True)
    mbar=sp.sqrt(z)*v
    assert sp.simplify(1/(8*sp.pi*mbar**2)-1/(8*sp.pi*z*v*v))==0
