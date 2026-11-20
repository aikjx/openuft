"""Independent numerical/symbolic checks for ROOT V114 restricted scalar model."""
import math
import numpy as np
import pytest
import sympy as s
from src.v114 import (
    Model, AU, C, HBAR, E_CHARGE, SUN_MASS, GSTAR,
    gamma_local, potential_enhancement, force_enhancement, force_excess,
    lensing_sum, gamma_from_force_reference, local_gamma_excess,
    infer_one_radius, two_scale_ratio_from_m, two_scale_logderivative,
    force_ratio_two_radii, solve_two_scales, joint_jacobian,
    joint_det_closed_form, scalar_energy_eV, scalar_frequency_threshold_Hz,
    scalar_group_velocity_fraction, shapiro_bare_delay_oneway,
    synthetic_noise_demo
)

@pytest.mark.parametrize('a',[0,1e-5,1/3,0.7,2.0])
def test_a_zero_or_positive(a): assert Model(a, AU).validate()
@pytest.mark.parametrize('a,lam', [(-1,AU),(float('nan'),AU),(1/3,0),(1/3,-1),(1/3,float('nan'))])
def test_model_invalid(a,lam):
    with pytest.raises(ValueError):Model(a,lam).validate()

@pytest.mark.parametrize('r_AU',[.1,.2,.5,1,2,5,10,30])
def test_potentials_recombine(r_AU):
    model=Model(1/3,AU)
    rr=r_AU*AU
    x=model.a*math.exp(-r_AU)
    assert math.isclose(float(gamma_local(rr,model)),(1-x)/(1+x),rel_tol=1e-13)
    assert math.isclose(float(potential_enhancement(rr,model)),1+x,rel_tol=1e-13)

@pytest.mark.parametrize('r_AU',[.01,.1,.5,1,2,5,10])
def test_force_is_derivative_of_potential(r_AU):
    model=Model(1/3,AU)
    x=r_AU*AU
    f=lambda r:float(potential_enhancement(r,model))/r
    h=x*1e-5
    # -d(U)/dr, U = Gstar M f; magnitude = -d(f)/dr, positive
    fd=-(f(x+h)-f(x-h))/(2*h)*x*x
    assert math.isclose(fd,float(force_enhancement(x,model)),rel_tol=1e-9)

@pytest.mark.parametrize('r_AU',[.05,.2,.5,1,2,3,8])
def test_joint_one_scale_inversion(r_AU):
    model=Model(1/3,AU)
    r=r_AU*AU
    a,lam=infer_one_radius(r,float(gamma_local(r,model)),float(force_enhancement(r,model)))
    assert a==pytest.approx(model.a,rel=2e-11)
    assert lam==pytest.approx(model.lam,rel=2e-11)

@pytest.mark.parametrize('a,lambda_AU',[(.01,.15),(.03,.5),(.1,1),(.3333,1),(.5,3),(.8,8)])
def test_two_scale_identification(a,lambda_AU):
    model=Model(a,lambda_AU*AU)
    r1=.5*AU;r2=2*AU
    aa,ll=solve_two_scales(r1,r2,float(force_excess(r1,model)),float(force_excess(r2,model)))
    assert aa==pytest.approx(a,rel=3e-9)
    assert ll==pytest.approx(lambda_AU*AU,rel=3e-9)

@pytest.mark.parametrize('lambda_AU',[.05,.1,.5,1,2,10])
def test_two_scale_ratio_monotonic(lambda_AU):
    m=1/(lambda_AU*AU);r1=.5*AU;r2=2*AU
    ratio=two_scale_ratio_from_m(r1,r2,m)
    assert 0<ratio<1
    assert two_scale_logderivative(r1,r2,m)<0
    step=m*1e-4
    numerical=(math.log(two_scale_ratio_from_m(r1,r2,m+step))-
               math.log(two_scale_ratio_from_m(r1,r2,m-step)))/(2*step)
    assert numerical==pytest.approx(two_scale_logderivative(r1,r2,m),rel=5e-7)

@pytest.mark.parametrize('r_AU',[.01,.05,.2,.5,1,2,5,10])
def test_jacobian_determinant(r_AU):
    model=Model(1/3,AU)
    mat=joint_jacobian(r_AU*AU,model)
    assert np.linalg.det(mat)==pytest.approx(joint_det_closed_form(r_AU*AU,model),rel=1e-12)
    assert np.linalg.det(mat)>0

@pytest.mark.parametrize('r_AU',[.05,.25,1,2,5])
def test_joint_jacobian_finite_differences(r_AU):
    model=Model(.3,AU)
    r=r_AU*AU
    eps=1e-6
    # Numerical derivative w.r.t a
    am=Model(model.a-eps,model.lam); ap=Model(model.a+eps,model.lam)
    # Numerical derivative w.r.t ln(lam)
    lm=Model(model.a,model.lam*math.exp(-eps));lp=Model(model.a,model.lam*math.exp(eps))
    fun=lambda m: np.array([float(gamma_local(r,m)),float(force_excess(r,m))])
    fda=(fun(ap)-fun(am))/(2*eps)
    fdloglam=(fun(lp)-fun(lm))/(2*eps)
    analytical=joint_jacobian(r,model)
    assert np.allclose(np.column_stack([fda,fdloglam]),analytical,atol=1e-10,rtol=1e-7)

@pytest.mark.parametrize('bad', [(-1,.5,1.1),(.5,2,1.1),(.5,.5,1.2),(.5,.7,1.01)])
def test_invalid_one_scale_measurement(bad):
    r,gm,force=bad
    with pytest.raises(ValueError):infer_one_radius(r,gm,force)

@pytest.mark.parametrize('r1,r2,y1,y2',[(1,2,1,.0),(2,1,1,.5),(1,2,.5,.7),(1,2,-.5,-.7)])
def test_bad_two_scale_data(r1,r2,y1,y2):
    with pytest.raises(ValueError):solve_two_scales(r1,r2,y1,y2)

def test_zero_scalar_cannot_recover_mass():
    model=Model(0,AU)
    assert gamma_local(AU,model)==1
    assert force_enhancement(AU,model)==1
    with pytest.raises(ValueError):infer_one_radius(AU,1,1)

def test_short_range_gr_limit():
    model=Model(1/3,.001*AU)
    assert abs(float(gamma_local(AU,model))-1)<1e-12
    assert abs(float(force_enhancement(AU,model))-1)<1e-12

def test_long_range_gamma_half():
    model=Model(1/3,1e12*AU)
    assert float(gamma_local(AU,model))==pytest.approx(.5,abs=1e-12)

def test_nonconstant_gamma_and_force_disagree():
    model=Model(1/3,AU)
    assert not math.isclose(float(gamma_local(AU,model)),float(gamma_from_force_reference(AU,model)),rel_tol=1e-2)

def test_lensing_conformal_scalar_cancellation():
    M=SUN_MASS
    model=Model(1/3,AU);r=AU
    raw=GSTAR*M/r
    U=raw*potential_enhancement(r,model)
    psi=raw*(1-model.a*math.exp(-r/model.lam))
    assert U+psi==pytest.approx(lensing_sum(r,GSTAR*M),rel=1e-13)

def test_shapiro_delay_only_bare_GM():
    b=.01*AU;L=AU
    result=shapiro_bare_delay_oneway(SUN_MASS,b,L)
    assert result>0
    # Direct numerical line integral of U+Psi normalized by c^3
    from scipy.integrate import quad
    integral=quad(lambda z:2*GSTAR*SUN_MASS/C**3 /math.hypot(z,b),-L,L,epsrel=2e-12)[0]
    assert integral==pytest.approx(result,rel=1e-11)

def test_lambda_and_scalar_mass_consistency():
    m=scalar_energy_eV(AU)
    f=scalar_frequency_threshold_Hz(AU)
    assert m==pytest.approx(1.3190493916461636e-18,rel=1e-11)
    assert (m*E_CHARGE)/(2*math.pi*HBAR)==pytest.approx(f,rel=1e-12)

@pytest.mark.parametrize('f_fraction',[.01,.5,.999,1])
def test_scalar_does_not_propagate_below_threshold(f_fraction):
    f0=scalar_frequency_threshold_Hz(AU)
    assert scalar_group_velocity_fraction(f_fraction*f0,AU)==0

@pytest.mark.parametrize('f_fraction',[1.001,1.01,2,10,1e3])
def test_scalar_propagating_above_threshold(f_fraction):
    f0=scalar_frequency_threshold_Hz(AU)
    assert scalar_group_velocity_fraction(f_fraction*f0,AU)==pytest.approx(math.sqrt(1-1/f_fraction**2))

def test_synthetic_noise_reproducible():
    model=Model(1/3,AU)
    d1=synthetic_noise_demo(model,AU,n=1000)
    d2=synthetic_noise_demo(model,AU,n=1000)
    assert d1==d2
    assert d1['n_identifiable']>=995
    assert d1['a_quantiles'][0] < model.a < d1['a_quantiles'][2]
    assert d1['lam_AU_quantiles'][0] <1<d1['lam_AU_quantiles'][2]

# Exact symbolic proofs, not float-only tests.
def test_sympy_force_derivative():
    r,lam,a=s.symbols('r lam a',positive=True)
    f=(1+a*s.exp(-r/lam))/r
    exact=1+a*(1+r/lam)*s.exp(-r/lam)
    assert s.simplify(-r*r*s.diff(f,r)-exact)==0

def test_sympy_lensing_sum():
    a,x,G,M,r=s.symbols('a x G M r')
    U=G*M/r*(1+a*s.exp(-x))
    Psi=G*M/r*(1-a*s.exp(-x))
    assert s.simplify(U+Psi-2*G*M/r)==0

def test_sympy_dual_inversion():
    a,x=s.symbols('a x',positive=True)
    z=a*s.exp(-x);gamma=(1-z)/(1+z);Y=z*(1+x)
    identity=s.simplify(Y/((1-gamma)/(1+gamma))-1-x)
    assert identity==0

def test_sympy_two_scale_mass_monotone():
    r1,r2,m=s.symbols('r1 r2 m',positive=True)
    ratio=(1+m*r2)/(1+m*r1)*s.exp(-m*(r2-r1))
    derivative=s.factor(s.diff(s.log(ratio),m))
    target=-(r2-r1)*m*(r1+r2+m*r1*r2)/((1+m*r1)*(1+m*r2))
    assert s.simplify(derivative-target)==0

def test_sympy_jacobian_determinant():
    a,x=s.symbols('a x',positive=True)
    z=a*s.exp(-x)
    g=(1-z)/(1+z);Y=z*(1+x)
    # Work with ln lambda; since d/dlnlambda=-x*d/dx.
    J=s.Matrix([[s.diff(g,a),-x*s.diff(g,x)],
                [s.diff(Y,a),-x*s.diff(Y,x)]])
    assert s.simplify(J.det()-2*a*x*s.exp(-2*x)/(1+z)**2)==0

def test_sympy_long_range_ratio_series():
    r1,r2,m=s.symbols('r1 r2 m',positive=True)
    ratio=(1+m*r2)/(1+m*r1)*s.exp(-m*(r2-r1))
    assert s.simplify(s.diff(ratio,m).subs(m,0))==0
    assert s.simplify(s.diff(ratio,m,2).subs(m,0)+(r2*r2-r1*r1))==0

def test_sympy_GM_scaling_invariance():
    G,M,sf,r=s.symbols('G M sf r',positive=True)
    U=G*M/r
    assert s.simplify(U.subs({G:sf*G,M:M/sf}, simultaneous=True)-U)==0

def test_sympy_one_scale_jacobian_rank():
    a,x=s.symbols('a x',positive=True)
    z=a*s.exp(-x)
    determinant=2*a*x*s.exp(-2*x)/(1+z)**2
    assert s.simplify(determinant)>0  # assumptions ensure positivity
