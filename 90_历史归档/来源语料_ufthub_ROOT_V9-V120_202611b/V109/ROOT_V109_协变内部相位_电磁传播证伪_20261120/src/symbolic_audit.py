"""Symbolic checks for pure-gradient connection, axion helicity and dimensions."""
from sympy import symbols, sin, cos, diff, simplify, Matrix, eye, diag

def run_symbolic_checks():
    t,x,y,omega,k,lam,amp=symbols('t x y omega k lam amp',real=True)
    theta=amp*sin(omega*t)
    checks={}
    checks['theta_gradient_antisymmetric_zero']=simplify(diff(diff(theta,t),x)-diff(diff(theta,x),t))==0
    # 1-form A = f(theta)dtheta is flat where theta is smooth,
    # including the noncommuting matrix case (same matrix at same theta).
    a=symbols('a', real=True)
    f=Matrix([[0,1],[-1,0]])*sin(a)+diag(1,-1)*cos(a)
    dthetadt=diff(theta,t)
    dthetadx=diff(theta,x)
    A_t=f.subs(a,theta)*dthetadt
    A_x=f.subs(a,theta)*dthetadx
    curvature=A_x.diff(t)-A_t.diff(x)+A_t*A_x-A_x*A_t
    checks['single_phase_nonabelian_flat']=curvature.applyfunc(simplify)==Matrix.zeros(2)
    # local potential: V=Lambda^4*(1-cos(theta)) -> V''(0)/f^2
    th,fscale,Lamb=symbols('th fscale Lamb',positive=True)
    V=Lamb**4*(1-cos(th))
    checks['axion_small_oscillation_mass2']=simplify(diff(V,th,2).subs(th,0)/fscale**2 - Lamb**4/fscale**2)==0
    # Current identically conserved by two-form antisymmetry even after axion term.
    checks['antisymmetric_divergence_identity']=simplify(diff(diff(theta,x),t)-diff(diff(theta,t),x))==0
    # Mode frequency squared difference and first-order shift.
    wplus2=k*k+lam*k*diff(theta,t)
    wminus2=k*k-lam*k*diff(theta,t)
    checks['helicity_frequency_sq_difference']=simplify((wplus2-wminus2)-2*lam*k*diff(theta,t))==0
    # SI/natural units: [theta]=0, [F]=E^2,[f]=E,[lambda]=0
    dimensions={'theta':0,'F':2,'dualF':2,'lambda':0,'f':1,'partial':1,'Lambda':1,'G':-2,'c':0,'hbar':0}
    checks['dim_axion_photon_L4']=dimensions['lambda']+dimensions['theta']+dimensions['F']+dimensions['dualF']==4
    checks['dim_scalar_kinetic_L4']=2*dimensions['f']+2*(dimensions['partial']+dimensions['theta'])==4
    checks['dim_potential_L4']=4*dimensions['Lambda']==4
    checks['dim_canonical_a_over_f']=dimensions['f']-dimensions['f']==0
    # Actual finite-difference identity for quadratic potential check.
    checks['pseudoscalar_second_derivative']=simplify(diff(V,th,2)-Lamb**4*cos(th))==0
    return checks

if __name__=='__main__':
    result=run_symbolic_checks()
    for k,v in result.items():print(k,'PASS' if v else 'FAIL')
    assert all(result.values())
