import math
import sys
from pathlib import Path
import pytest
import sympy as s
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import v113 as v

@pytest.mark.parametrize('omega',[-1.5,-1.6,-10])
def test_positive_kinetic_condition(omega):
    with pytest.raises(ValueError):v.alpha2(omega)

@pytest.mark.parametrize('omega',[0,1,10,100,40000,100000])
def test_gamma_from_two_representations(omega):
    assert v.gamma_bd(omega)==pytest.approx(v.gamma_alpha(v.alpha2(omega)),rel=3e-16)

@pytest.mark.parametrize('omega',[0,1,10,100,40000,100000])
def test_gamma_minus_one_stable(omega):
    assert v.gamma_minus_one_bd(omega)==pytest.approx(-1/(omega+2),rel=1e-14)

@pytest.mark.parametrize('omega',[0,1,10,100,40000,100000])
def test_gamma_and_alpha_physical(omega):
    assert 0<v.gamma_bd(omega)<1

@pytest.mark.parametrize('omega',[0,100,39998,100000])
def test_local_massless_limit(omega):
    for rr in [0,1000.,v.AU_M]:
        assert v.gamma_eff(rr,omega,0)==pytest.approx(v.gamma_bd(omega),rel=1e-13)

@pytest.mark.parametrize('omega',[0,10,100,40000])
def test_gamma_eff_large_scalar_mass(omega):
    assert v.gamma_eff(v.AU_M,omega,1e-10)==1.0

@pytest.mark.parametrize('omega',[0,1,10,100,40000])
def test_gamma_eff_monotone(omega):
    r=v.AU_M
    gm=[v.gamma_eff(r,omega,m) for m in [0,1e-19,1e-18,1e-17,1e-16]]
    assert gm==sorted(gm)

@pytest.mark.parametrize('mass',[1e-30,1e-25,1e-20,1e-18,1e-15,1e-10])
def test_range_roundtrip(mass):
    assert v.mass_eV_from_range_m(v.range_m_from_mass_eV(mass))==pytest.approx(mass,rel=1e-15)

@pytest.mark.parametrize('range_m',[1.,100.,1e6,1e11,1e20])
def test_range_to_mass_roundtrip(range_m):
    assert v.range_m_from_mass_eV(v.mass_eV_from_range_m(range_m))==pytest.approx(range_m,rel=1e-15)

@pytest.mark.parametrize('r_m',[1e8,1e10,v.AU_M,5*v.AU_M])
def test_proxy_threshold_is_boundary(r_m):
    m=v.proxy_mass_min_eV(r_m)
    # Under 2sigma one-sided Cassini proxy: gamma-1 >= center-2sigma
    assert v.gamma_eff_minus_one(r_m,0,m)==pytest.approx(v.CASSINI_CENTER-2*v.CASSINI_SIGMA,abs=2e-15)

@pytest.mark.parametrize('omega',[0,1,10,100])
def test_proxy_has_nonnegative_mass(omega):
    assert v.proxy_mass_min_eV(v.AU_M,omega)>=0

@pytest.mark.parametrize('alpha_s',[0,1e-4,0.3,1.])
def test_equal_composition_cancels_eta(alpha_s):
    assert v.eotvos_eta(.5,.5,alpha_s,v.AU_M,0)==pytest.approx(0,abs=0)

@pytest.mark.parametrize('alpha_a,alpha_b,alpha_s',[(.1,.05,.2),(.01,.02,.3),(-.2,.1,.1),(.1,.1,.9)])
def test_massive_eta_smaller_magnitude(alpha_a,alpha_b,alpha_s):
    e1=abs(v.eotvos_eta(alpha_a,alpha_b,alpha_s,v.AU_M,0))
    e2=abs(v.eotvos_eta(alpha_a,alpha_b,alpha_s,v.AU_M,1e-16))
    assert e2<=e1+1e-15

@pytest.mark.parametrize('r',[.5,1,3,10])
def test_yukawa_gradient_massless(r):
    assert v.yukawa_gradient_factor(r,0)==1

@pytest.mark.parametrize('r',[.5,1,3,10])
def test_yukawa_gradient_decreases_with_mass(r):
    assert v.yukawa_gradient_factor(r,1e-8)<1

@pytest.mark.parametrize('range_m',[10,100,1e4,1e10])
def test_two_scale_det_nonzero(range_m):
    det=v.two_scale_det(.1*range_m,1.5*range_m,.25,range_m)
    assert det!=0

@pytest.mark.parametrize('range_m',[10,100,1e4,1e10])
def test_same_r_det_zero(range_m):
    assert v.two_scale_det(range_m,range_m,.25,range_m)==0

@pytest.mark.parametrize('r',[10,100,1e4,1e10])
def test_gamma_jacobian_finite_difference(r):
    a=.2;R=2*r
    da,dl=v.local_gamma_jacobian(r,a,R)
    delta=1e-5
    def f(aa,rr):
        u=aa*math.exp(-r/rr)
        return (1-u)/(1+u)
    da_fd=(f(a+delta,R)-f(a-delta,R))/(2*delta)
    dl_fd=(f(a,R*(1+delta))-f(a,R*(1-delta)))/(2*delta*R)
    assert da==pytest.approx(da_fd,rel=1e-8)
    assert dl==pytest.approx(dl_fd,rel=1e-8)

@pytest.mark.parametrize('j,g,m2',[(1,2,3),(-2,1,10),(.01,.001,1e4),(100,-3,100)])
def test_eliminate_torsion(j,g,m2):
    s0=v.algebraic_torsion_solution(j,g,m2)
    assert v.torsion_lagrangian(s0,j,g,m2)==pytest.approx(v.torsion_effective_contact(j,g,m2))

@pytest.mark.parametrize('mass',[-1,-1e-20])
def test_invalid_scalar_mass(mass):
    with pytest.raises(ValueError):v.gamma_eff(v.AU_M,0,mass)

@pytest.mark.parametrize('mass',[-1,0])
def test_invalid_range(mass):
    with pytest.raises(ValueError):v.range_m_from_mass_eV(mass)

@pytest.mark.parametrize('radius',[-1,0])
def test_invalid_proxy_radius(radius):
    with pytest.raises(ValueError):v.proxy_mass_min_eV(radius)

@pytest.mark.parametrize('r1,r2',[(1.,2.),(1e7,3e8),(1e9,3e10)])
def test_two_scale_det_formula(r1,r2):
    a=.3;R=r2
    da1,_=v.local_gamma_jacobian(r1,a,R)
    da2,_=v.local_gamma_jacobian(r2,a,R)
    predicted=da1*da2*a*(r2-r1)/R**2
    assert v.two_scale_det(r1,r2,a,R)==pytest.approx(predicted,rel=5e-14)

# Exact symbolic identities; all use exact fractions/rationals rather than floating-point values.
def test_symbolic_bd_gamma():
    w=s.symbols('w')
    a=1/(2*w+3)
    assert s.simplify((1-a)/(1+a)-(w+1)/(w+2))==0

def test_symbolic_bran_dicke_effective_action_omega0():
    phi,R,F,k=s.symbols('phi R F k')
    lag=phi*R-k*k*phi**3*F/4
    assert s.diff(lag,phi).subs(F,0)==R
    assert s.simplify(s.diff(lag,phi) - (R-3*k*k*phi**2*F/4)) == 0

def test_symbolic_two_scale_det():
    a,r1,r2,l,y1,y2=s.symbols('a r1 r2 l y1 y2', positive=True)
    deriv1=-2*y1/(1+a*y1)**2
    deriv2=-2*y2/(1+a*y2)**2
    mat=s.Matrix([[deriv1,deriv1*a*r1/l**2],
                  [deriv2,deriv2*a*r2/l**2]])
    expected=deriv1*deriv2*a*(r2-r1)/l**2
    assert s.factor(mat.det()-expected)==0

def test_symbolic_torsion_elimination():
    S,J,g,M=s.symbols('S J g M',nonzero=True,real=True)
    L= -M*M*S*S/2+g*S*J
    sol=s.solve(s.diff(L,S),S)[0]
    assert s.simplify(sol-g*J/M**2)==0
    assert s.simplify(L.subs(S,sol)-g*g*J*J/(2*M*M))==0

def test_symbolic_eotvos_zero_for_universal():
    a,b,src,Y=s.symbols('a b src Y')
    delta_a=a*src*Y;delta_b=b*src*Y
    eta=2*(delta_a-delta_b)/(2+delta_a+delta_b)
    assert s.simplify(eta.subs(b,a))==0

def test_symbolic_massive_gamma_formula():
    a,y=s.symbols('a y')
    g=(1-a*y)/(1+a*y)
    assert s.simplify(g-1+2*a*y/(1+a*y))==0

def test_symbolic_omega0():
    assert s.Rational(0+1,0+2)==s.Rational(1,2)

def test_symbolic_cassini_omega_lower_bound():
    d=s.Rational(25,1_000_000)
    assert s.solve(s.Eq(-1/(s.Symbol('omega')+2),-d),s.Symbol('omega'))==[39998]

@pytest.mark.parametrize('omega,scale',[(0,.5),(0,2),(0,100),(10,1e-7),(40000,1000)])
def test_newton_G_scaling_degeneracy(omega,scale):
    a=v.measured_newton_G(6.6743e-11,1,omega)
    b=v.measured_newton_G(6.6743e-11*scale,scale,omega)
    assert a==pytest.approx(b,rel=5e-15)

def test_omega_zero_G_factor():
    assert v.measured_newton_G(1,1,0)==pytest.approx(4/3)

def test_symbolic_G_degeneracy():
    G,phi,omega,k=s.symbols('G phi omega k', positive=True)
    expression=(G/phi)*(2*omega+4)/(2*omega+3)
    assert s.cancel(expression.subs({G:G*k,phi:phi*k})-expression)==0
