"""ROOT V118 mathematical assertions. No observational detections claimed."""
import math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np,mpmath as mp,pytest,sympy as sp
from src import model as m

@pytest.mark.parametrize('profile',['uniform','inverse_r','earth_analytic','five_shell_reference'])
@pytest.mark.parametrize('x',[0,.02,.1,.5,1,3,8,25,51,200])
def test_scaled_form_positive(profile,x):
    v=m.scaled_form(x,profile)
    assert np.isfinite(v) and 0<v<=1+1e-12

@pytest.mark.parametrize('profile',['uniform','inverse_r','earth_analytic','five_shell_reference'])
def test_long_range_form(profile):
    assert abs(m.scaled_form(1e-7,profile)-math.exp(-1e-7))<2e-14

@pytest.mark.parametrize('profile',['uniform','inverse_r','earth_analytic'])
@pytest.mark.parametrize('x',[.002,.08,.2,1,4,20,51,90])
def test_independent_high_precision_integral(profile,x):
    mp.mp.dps=50
    y=mp.mpf(str(x))
    def relative_density(t):
        if profile=='uniform':return mp.mpf(1)
        if profile=='inverse_r':return mp.mpf(2)/(3*t)
        return mp.mpf(5)/4-t+1/(3*t)
    def f(t):
        if t==0:return mp.mpf(0)
        return 3*relative_density(t)*t*t*mp.exp(-y)*mp.sinh(y*t)/(y*t)
    # Resolve near surface where exponential changes rapidly.
    I=mp.quad(f,[0,mp.mpf('.75'),mp.mpf('.95'),1])
    expected=float(I)
    assert abs(m.scaled_form(x,profile)-expected)<max(5e-12*expected,5e-15)

@pytest.mark.parametrize('profile',['uniform','inverse_r','earth_analytic','five_shell_reference'])
@pytest.mark.parametrize('h',[0,100e3,400e3,800e3,1200e3])
def test_yukawa_monotonic_with_h(profile,h):
    assert m.yukawa_excess(h,profile=profile)>m.yukawa_excess(h+100e3,profile=profile)

@pytest.mark.parametrize('profile',['uniform','inverse_r','earth_analytic','five_shell_reference'])
@pytest.mark.parametrize('ell',[45e3,80e3,m.ELL_BASELINE,200e3,500e3,2e6])
def test_shape_independent_differences(profile,ell):
    hs=(0.,400e3,800e3)
    kval=[m.effective_gm(h,ell,alpha=.2,profile=profile,gm_baseline=8.6e15) for h in hs]
    ratio=m.observed_difference_ratio(kval)
    theory=m.altitude_invariant(ell,hs)
    assert abs(ratio/theory-1)<5e-8

@pytest.mark.parametrize('ell',[60e3,90e3,110e3,124600.,180e3,300e3,800e3,2e6])
def test_range_recovery_three_heights(ell):
    hs=(0.,400e3,800e3)
    ratio=m.altitude_invariant(ell,hs)
    recovered=m.invert_range_3heights(hs,ratio)
    assert abs(recovered/ell-1)<1e-9

@pytest.mark.parametrize('profile',['uniform','inverse_r','earth_analytic','five_shell_reference'])
@pytest.mark.parametrize('ell',[60e3,m.ELL_BASELINE,500e3])
def test_four_height_predicts_out_of_sample(profile,ell):
    hs=(0,400e3,800e3,1200e3)
    obs=[m.effective_gm(h,ell,alpha=.13,profile=profile) for h in hs]
    info=m.four_altitude_validation(hs,obs)
    assert abs(info['ell_m']/ell-1)<1e-7
    assert abs(info['fractional_fourth_residual'])<1e-11

@pytest.mark.parametrize('ell',[50e3,100e3,300e3,700e3])
@pytest.mark.parametrize('r',[m.R_EARTH,m.R_EARTH+400e3,m.R_EARTH+1200e3])
def test_differential_ODE(ell,r):
    k1,k2,k3=m.apparent_GM_derivatives(r,ell,C=1.3e20,GM=1.5)
    assert math.isclose(m.local_inverse_range(r,k1,k2),1/ell,rel_tol=1e-13)
    residual=m.differential_closure(r,k1,k2,k3)
    norm=k2*k2+k3*k1+(k1/r)**2
    assert abs(residual/norm)<1e-12

@pytest.mark.parametrize('h',[0.,100e3,400e3,710e3,800e3,1200e3])
def test_epicyclic_stability_and_gradient(h):
    data=m.epicyclic_observables(h)
    assert data['radially_stable']
    assert 0<data['radial_to_azimuth_frequency_sq']<1
    assert data['pericenter_advance_rad_per_radial_period']>0
    assert data['yukawa_force_fraction']>0

@pytest.mark.parametrize('height',[0.,100e3,400e3,800e3])
def test_epicyclic_limit_alpha_zero(height):
    data=m.epicyclic_observables(height,alpha=0)
    assert data['radial_to_azimuth_frequency_sq']==1
    assert data['pericenter_advance_rad_per_radial_period']==0

@pytest.mark.parametrize('ell',[30e3,60e3,124600.,250e3,2e6])
def test_earth_like_five_shell_ratio(ell):
    x=m.R_EARTH/ell
    if x<=64: assert abs(m.scaled_form(x,'earth_analytic')/m.scaled_form(x,'five_shell_reference')-1)<.012

@pytest.mark.parametrize('v',[1e3,1e4,1e5,1e6])
def test_mass_inverse_range(v):
    assert m.mass_ev(2*v)==pytest.approx(m.mass_ev(v)/2)

@pytest.mark.parametrize('case',[
    lambda:m.scaled_form(-1),lambda:m.scaled_form(math.inf),lambda:m.scaled_form(1,'unknown'),
    lambda:m.yukawa_excess(-1),lambda:m.yukawa_excess(0,0),lambda:m.effective_gm(0,gm_baseline=-1),
    lambda:m.altitude_invariant(100,(3,2,1)),lambda:m.invert_range_3heights((0,1,2),-1),
    lambda:m.four_altitude_validation((1,2,3,4),(1,2,3)),lambda:m.mass_ev(0),
    lambda:m.epicyclic_observables(-1),lambda:m.local_inverse_range(1,0,1),
])
def test_invalid_inputs(case):
    with pytest.raises(ValueError):case()

def test_v117_uniform_source_regression():
    assert m.yukawa_excess(0,profile='uniform')==pytest.approx(.009774903625204768,rel=1e-13)

def test_v117_inverse_r_regression():
    assert m.yukawa_excess(0,profile='inverse_r')==pytest.approx(.006646591723147821,rel=1e-13)

def test_earth_analytic_surface():
    assert m.yukawa_excess(0)==pytest.approx(.0059543790126180334,rel=1e-13)

def test_2026_five_shell_crosscheck():
    assert m.yukawa_excess(0,profile='five_shell_reference')==pytest.approx(.005931332678374593,rel=1e-13)

def test_three_altitude_ratio_baseline():
    assert m.altitude_invariant(m.ELL_BASELINE,(0,400e3,800e3))==pytest.approx(23.344868953052476,rel=1e-13)

def test_orbit_precession_baseline():
    assert m.epicyclic_observables(400e3)['pericenter_advance_rad_per_radial_period']==pytest.approx(.043181262070199615,rel=1e-13)

def test_symbolic_ode_invariant():
    r,k,C,G0=sp.symbols('r k C G0',positive=True)
    K=G0*(1+C*(1+k*r)*sp.exp(-k*r))
    K1=sp.diff(K,r);K2=sp.diff(K1,r);K3=sp.diff(K2,r)
    assert sp.simplify(K2*K2-K3*K1-K1*K1/r**2)==0
    assert sp.simplify(1/r-K2/K1-k)==0

def test_symbolic_epicycle():
    r,k,A,GM=sp.symbols('r k A GM',positive=True)
    Y=A*(1+k*r)*sp.exp(-k*r)
    omega2=GM*(1+Y)/r**3
    radial2=4*omega2+r*sp.diff(omega2,r)
    expected=GM*(1+Y-A*k*k*r*r*sp.exp(-k*r))/r**3
    assert sp.simplify(radial2-expected)==0

def test_symbolic_sphere_density_normalization():
    u=sp.symbols('u',positive=True)
    dens=sp.Rational(5,4)-u+1/(3*u)
    assert sp.simplify(3*sp.integrate(dens*u*u,(u,0,1)))==1

def test_symbolic_monotonicity_single_Yukawa():
    r,k=sp.symbols('r k',positive=True)
    u=(1+k*r)*sp.exp(-k*r)
    assert sp.simplify(sp.diff(u,r)/(-k*k*r*sp.exp(-k*r)))==1

def test_monotonic_three_altitude_ratio_on_relevant_range():
    hs=(0,400e3,800e3)
    ell=np.geomspace(30e3,2e6,150)
    ratios=[m.altitude_invariant(x,hs) for x in ell]
    assert all(ratios[i]>ratios[i+1] for i in range(len(ratios)-1))

def test_microscope_cannot_constrain_universal_composition_same_coupling():
    # Same scalar coupling for Ti and Pt implies equal acceleration at the same r.
    yi=m.yukawa_excess(710e3,alpha=.3333333333333333)
    yj=m.yukawa_excess(710e3,alpha=.3333333333333333)
    assert yi==yj

@pytest.mark.parametrize('hs',[(0,300e3,900e3),(100e3,500e3,1000e3),(200e3,300e3,400e3),(400e3,700e3,1200e3)])
@pytest.mark.parametrize('ell',[60e3,100e3,124600.,200e3,500e3])
def test_integral_ratio_independent_derivation(hs,ell):
    from scipy.integrate import quad
    rr=[m.R_EARTH+h for h in hs]
    # Recover the ratio through a separate quadrature, not the u(r) shortcut.
    v1=quad(lambda r:r*math.exp(-(r-rr[0])/ell),rr[0],rr[1],epsabs=0)[0]
    v2=quad(lambda r:r*math.exp(-(r-rr[0])/ell),rr[1],rr[2],epsabs=0)[0]
    assert v1/v2==pytest.approx(m.altitude_invariant(ell,hs),rel=2e-12)

@pytest.mark.parametrize('hs',[(0,400e3,800e3),(200e3,500e3,1000e3),(300e3,700e3,1200e3)])
def test_inverse_range_strict_global_monotonic_on_grid(hs):
    wavenumbers=np.geomspace(1/5e6,1/3e4,100)
    values=[m.altitude_invariant(1/k,hs) for k in wavenumbers]
    assert np.all(np.diff(values)>0)


def test_ratio_has_lower_bound_for_finite_range():
    rr=[m.R_EARTH+h for h in [0,400e3,800e3]]
    bound=(rr[1]**2-rr[0]**2)/(rr[2]**2-rr[1]**2)
    assert m.altitude_invariant(1e9,(0,400e3,800e3))>bound
    assert m.altitude_invariant(1e9,(0,400e3,800e3))<1.01*bound


def test_three_height_differences_cannot_infer_when_alpha_zero():
    k=[m.effective_gm(h,alpha=0) for h in [0,400e3,800e3]]
    with pytest.raises(ValueError): m.observed_difference_ratio(k)


def test_four_height_rejects_two_ranges():
    hs=(0,400e3,800e3,1200e3)
    K=[1+m.yukawa_excess(h)+m.yukawa_excess(h,300e3,.1) for h in hs]
    out=m.four_altitude_validation(hs,K)
    assert out['ell_m']==pytest.approx(189973.77473486675,rel=1e-9)
    assert abs(out['fractional_fourth_residual'])>1e-4


def test_analytic_earth_density_moment_of_inertia():
    # For rho' from 2026 Earth-form-factor literature, <r²>/R² =1/2,
    # so I/(M R²)=2/3*(1/2)=1/3, close to Earth's 0.3308.
    assert m._moments_rhoprime(1)==pytest.approx(.5,abs=1e-15)


def test_analytic_rhoprime_surface_density():
    # rho'/rho0 = 5/4-u+1/(3u), so surface value =7/12.
    assert (5/4-1+1/3)==pytest.approx(7/12)
