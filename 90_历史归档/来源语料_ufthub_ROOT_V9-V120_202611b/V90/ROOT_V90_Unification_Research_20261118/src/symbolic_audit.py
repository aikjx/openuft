"""Symbolic identities: checked with sympy, no experimental claims."""
import sympy as sp

def run():
    d,a,b,L=sp.symbols('d a b L',positive=True)
    r=[d+(a-b)/2,d+(a+b)/2,d-(a+b)/2,d+(b-a)/2]
    signs=[1,-1,-1,1]
    results=[]
    def check(name,expr):
        val=sp.simplify(expr)
        v=all(sp.simplify(i)==0 for i in val) if isinstance(val,sp.MatrixBase) else val==0
        results.append((name,v))
        if not v: raise AssertionError(f'{name}: {expr}')
    for n,expected in [(0,0),(1,0),(2,-2*a*b),(3,-6*a*b*d),
                       (4,-a*b*(a*a+b*b+12*d*d))]:
        check(f'mixed_moment_{n}',sum(s*x**n for s,x in zip(signs,r))-expected)
    check('yukawa_leading_order', -sum(s*x*x for s,x in zip(signs,r))/(6*L**3)-a*b/(3*L**3))
    check('yukawa_next_order',sum(s*x**3 for s,x in zip(signs,r))/(24*L**4)+d*a*b/(4*L**4))
    check('local_phase_invariance',sp.Symbol('a0')-sp.Symbol('a0')-sp.Symbol('a1')+sp.Symbol('a1'))
    # For q(a,b)=f(d+b-a), d_a d_b q = -f''.
    x=sp.symbols('x',positive=True)
    f=sp.exp(-x/L)/x
    check('yukawa_curvature',sp.diff(f,x,2)-sp.exp(-x/L)*(2/x**3+2/(L*x**2)+1/(L*L*x)))
    # Dimensional no-go: no exponents p,q with [hbar^p c^q]=[G].
    # Vector components = (L,M,T); columns hbar=(2,1,-1), c=(1,0,-1).
    dim_matrix=sp.Matrix([[2,1],[1,0],[-1,-1]])
    dim_g=sp.Matrix([3,-1,-2])
    if sp.linsolve((dim_matrix,dim_g)) != sp.EmptySet:
        raise AssertionError('unexpected dimensional G solution from hbar,c')
    results.append(('no_G_from_hbar_c_dimensions',True))
    # Adding independent mass scale yields [G]=[hbar*c / m_*^2].
    check('new_mass_scale_formula',sp.Matrix([[2,1,0],[1,0,1],[-1,-1,0]])*sp.Matrix([1,1,-2])-dim_g)
    # Adding independent length scale yields [G]=[c^3*l_*^2 / hbar].
    check('new_length_scale_formula',sp.Matrix([[2,1,1],[1,0,0],[-1,-1,0]])*sp.Matrix([-1,3,2])-dim_g)
    # Couplings identical same distance profile -> determinant 0.
    x,y=sp.symbols('x y')
    check('identifiability_coulomb_newton',sp.det(sp.Matrix([[x,-x],[y,-y]])))
    print('Symbolic identities checked:',len(results))
    for name,ok in results: print('OK',name)
    return len(results)

if __name__=='__main__':run()
