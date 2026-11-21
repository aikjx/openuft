import sympy as sp

def test_yukawa_radius_derivative():
    k,r=sp.symbols('k r',positive=True)
    y=(1+k*r)*sp.exp(-k*r)
    assert sp.simplify(sp.diff(y,r)+k*k*r*sp.exp(-k*r))==0

def test_helix_curvature_torsion_analytic():
    R,w,u,t=sp.symbols('R w u t',positive=True,real=True)
    x=sp.Matrix([R*sp.cos(w*t),R*sp.sin(w*t),u*t])
    v=x.diff(t); a=v.diff(t); j=a.diff(t)
    cross=v.cross(a)
    speed2=R**2*w**2+u**2
    curvature=sp.simplify(sp.sqrt(cross.dot(cross))/speed2**sp.Rational(3,2))
    torsion=sp.simplify(cross.dot(j)/cross.dot(cross))
    assert sp.simplify(curvature-R*w*w/speed2)==0
    assert sp.simplify(torsion-u*w/speed2)==0

def test_kg_to_schrodinger_envelope_exact_rearrangement():
    t,x=sp.symbols('t x',real=True)
    m,c,h=sp.symbols('m c h',positive=True,real=True)
    phi=sp.Function('phi')(t,x)
    psi=sp.exp(-sp.I*m*c*c*t/h)*phi
    KG=sp.diff(psi,t,2)/c**2-sp.diff(psi,x,2)+(m*c/h)**2*psi
    transformed=sp.simplify(KG*sp.exp(sp.I*m*c*c*t/h))
    expected=sp.diff(phi,t,2)/c**2-2*sp.I*m*sp.diff(phi,t)/h-sp.diff(phi,x,2)
    assert sp.simplify(transformed-expected)==0

def test_minimal_coupling_gauge_covariance():
    x=sp.symbols('x',real=True);q,h=sp.symbols('q h',real=True,nonzero=True)
    psi=sp.Function('psi')(x);chi=sp.Function('chi')(x);A=sp.Function('A')(x)
    transformed_wave=sp.exp(sp.I*q*chi/h)*psi
    transformed_A=A-sp.diff(chi,x)
    transformed_D=sp.diff(transformed_wave,x)+sp.I*q*transformed_A*transformed_wave/h
    covariant_target=sp.exp(sp.I*q*chi/h)*(sp.diff(psi,x)+sp.I*q*A*psi/h)
    assert sp.simplify(transformed_D-covariant_target)==0

def test_c_and_G_do_not_dimensionally_determine_hbar():
    a,b=sp.symbols('a b',real=True)
    # c^a G^b dimensions L^(a+3b) M^(-b) T^(-a-2b), target hbar = M L^2 T^-1
    solution=sp.solve([a+3*b-2, -b-1, -a-2*b+1],[a,b])
    assert solution==[]

def test_classical_helix_plus_compton_requires_quantum_postulate():
    m,c,h,R,w=sp.symbols('m c h R w',positive=True)
    # If, additionally, E=ħω=mc² and ω=c/R, then R=ħ/(mc).
    assert sp.simplify((h*w-m*c*c).subs(w,c/R).subs(R,h/(m*c)))==0
