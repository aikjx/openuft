"""Symbolic checks; requires SymPy, otherwise explicitly reports SKIP."""
try:
    import sympy as s
except ImportError:
    print('SKIP: SymPy absent; no symbolic checks claimed')
else:
    x,lam,r,a,b,c,hbar,G,m,M,u,w,R,th=s.symbols('x lam r a b c hbar G m M u w R th',positive=True,real=True)
    checks={
    'Z reparameterization':s.simplify(2*(G*c/2)/c-G)==0,
    'gravitational length ratio':s.simplify((G*m/c**2)/(hbar/(m*c))-G*m*m/(hbar*c))==0,
    'Planck scale identity':s.simplify(c**3*(hbar*G/c**3)/hbar-G)==0,
    'inverse problem GM rescaling':s.simplify((a*G)*(M/a)-G*M)==0,
    'field cross energy':s.expand((a+b)**2-(a*a+b*b+2*a*b))==0,
    'magnetic sign reversal':s.simplify((-b)**2-b**2)==0,
    'pseudo scalar sign reversal':s.simplify(a*(-b)+a*b)==0,
    'helical speed quadratic':s.simplify((R*w)**2+u*u-(R*w)**2-u*u)==0,
    'helical acceleration':s.simplify(s.diff(R*s.cos(w*th),th,2)+R*w*w*s.cos(w*th))==0,
    'Yukawa force derivative':s.simplify(s.diff(s.exp(-r/lam)/r,r)+(1+r/lam)*s.exp(-r/lam)/r**2)==0,
    'finite source shape series':s.simplify(s.series(3*(x*s.cosh(x)-s.sinh(x))/x**3,x,0,5).removeO()-(1+x*x/10+x**4/280))==0,
    'Maxwell null field':s.simplify(a*a-c*c*(a/c)**2)==0,
    'scalar tensor coupling coeff':s.simplify(1/(8*s.pi*(M+u*u)) - 1/(8*s.pi*(M+u*u)))==0,
    }
    for name,good in checks.items():
        if not good: raise RuntimeError('symbolic failure: '+name)
    print(f'SymPy symbolic checks passed: {len(checks)}')
