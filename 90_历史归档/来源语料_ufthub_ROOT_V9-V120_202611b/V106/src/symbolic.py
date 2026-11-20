"""SymPy exact symbolic audits; distinct from finite precision unit tests."""
import sympy as s

def run():
    th,ph,x,y,L=s.symbols('theta phi x y L', positive=True)
    a1,a2,a3,b1,b2,b3,t=s.symbols('a1 a2 a3 b1 b2 b3 t',real=True)
    sx=s.Matrix([[0,1],[1,0]])
    sy=s.Matrix([[0,-s.I],[s.I,0]])
    sz=s.diag(1,-1)
    X=s.I*sx/2; Y=s.I*sy/2
    Z=-s.I*sz/2
    checks={}
    checks['nonabelian_commutator_exact'] = X*Y-Y*X == Z
    checks['one_phase_wedge_zero'] = s.diff(th,x)*s.diff(th,y)-s.diff(th,y)*s.diff(th,x)==0
    checks['two_phase_curvature_component'] = X*Y-Y*X==Z
    checks['SU2_antihermitian'] = (X+X.conjugate().T==s.zeros(2))
    I=(b2-b3)*a1+(b3-b1)*a2+(b1-b2)*a3
    J=s.expand(I.subs({a1:a1-b1*t,a2:a2-b2*t,a3:a3-b3*t}))
    checks['rge_invariant'] = s.simplify(J-I)==0
    checks['rge_slope_sum'] = s.simplify((b2-b3)+(b3-b1)+(b1-b2))==0
    checks['rge_slope_dot'] = s.expand((b2-b3)*b1+(b3-b1)*b2+(b1-b2)*b3)==0
    checks['su5_normalized_trace'] = s.Rational(3,5)*(3*s.Rational(1,9)+2*s.Rational(1,4))==s.Rational(1,2)
    theta, ff, lam, jj=s.symbols('theta f lambda J', real=True)
    V=lam**4*(1-s.cos(theta))
    checks['theta_periodicity_potential'] = s.simplify(V.subs(theta,theta+2*s.pi)-V)==0
    checks['theta_source_derivative'] = s.diff(-theta*jj/s.Integer(4),theta)==-jj/4
    checks['theta_small_mass'] = s.simplify(s.diff(V,theta,2).subs(theta,0)/ff**2 - lam**4/ff**2)==0
    ga,gb=s.symbols('ga gb')
    checks['no_G_from_only_c_and_hbar']=s.solve([gb+1,ga+2*gb-3,-ga-gb+2],[ga,gb])==[]
    Gvec=s.Matrix([-1,3,-2]); Evec=s.Matrix([1,2,-2]); Hvec=s.Matrix([1,2,-1]); Cvec=s.Matrix([0,1,-1])
    checks['alpha_gravity_dimensionless']=Gvec+2*Evec-Hvec-5*Cvec==s.zeros(3,1)
    from .anomaly import anomaly_coefficients
    aa=anomaly_coefficients()
    for key in ['SU3^3','SU3^2-U1','SU2^2-U1','U1^3','grav^2-U1','Witten_SU2_obstruction']:
        checks['anomaly_'+key]=aa[key]==0
    assert all(checks.values()),{k:v for k,v in checks.items() if not v}
    return checks
