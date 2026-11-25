"""Independent SymPy checks: 5D Ricci scalar, helicity, Maxwell plane-wave and scalar obstruction.

Requires sympy (listed in requirements.txt).
"""
import json
import sympy as s


def five_d_curvature_test():
    """Exact 5D Ricci scalar for g4=flat and A_y=B*x, g55=R².

    Expected R5=-R² k² B² / 2 = - R² k² F² / 4 (since F²=2B²).
    """
    t, x, y, z, phi=s.symbols('t x y z phi',real=True)
    B,R,k=s.symbols('B R k',positive=True,real=True)
    P=R**2*k*B*x
    g=s.Matrix([[-1,0,0,0,0],
                [0,1,0,0,0],
                [0,0,1+R**2*(k*B*x)**2,0,P],
                [0,0,0,1,0],
                [0,0,P,0,R**2]])
    inv=s.simplify(g.inv())
    cs=[t,x,y,z,phi]
    n=5
    # Constant-coordinate derivatives other than x are exactly zero.
    def diff(expr,i):
        return s.diff(expr,x) if i==1 else s.S.Zero
    gamma=[[[s.simplify(sum(inv[i,l]*(diff(g[l,b],a)+diff(g[l,a],b)-diff(g[a,b],l))/2
                            for l in range(n))) for b in range(n)] for a in range(n)] for i in range(n)]
    ric=s.zeros(n)
    for a in range(n):
        for b in range(n):
            ric[a,b]=s.simplify(sum(
                diff(gamma[l][a][b],l)-diff(gamma[l][a][l],b)
                +sum(gamma[l][a][b]*gamma[j][l][j]-gamma[l][a][j]*gamma[j][l][b]
                     for j in range(n)) for l in range(n)))
    curv=s.factor(s.trace(inv*ric))
    expected=-R**2*k**2*B**2/2
    return {'ricci_scalar':str(curv),'expected':str(expected),
            'difference':str(s.simplify(curv-expected)),
            'passed':s.simplify(curv-expected)==0}


def polarization_test():
    """Two arbitrary helicity amplitudes and exact source-free Maxwell equations."""
    t,x,y,z=s.symbols('t x y z',real=True)
    a,b,w=s.symbols('a b w',real=True,nonzero=True)
    phase=w*(t-z)
    A=s.Matrix([0,a*s.cos(phase),b*s.sin(phase),0])
    cs=[t,x,y,z]
    g=s.diag(-1,1,1,1)
    F=s.Matrix(4,4,lambda i,j:s.diff(A[j],cs[i])-s.diff(A[i],cs[j]))
    Fu=g*F*g
    div=[s.simplify(sum(s.diff(Fu[i,j],cs[i]) for i in range(4))) for j in range(4)]
    bianchi=[]
    for i in range(4):
        for j in range(i+1,4):
            for l in range(j+1,4):
                bianchi.append(s.simplify(s.diff(F[j,l],cs[i])+s.diff(F[l,i],cs[j])+s.diff(F[i,j],cs[l])))
    # With wave 4-vector k=(w,0,0,w), A0=Az=0 => two physical transverse modes.
    return {'divergence':[str(q) for q in div], 'bianchi':[str(q) for q in bianchi],
            'two_transverse_amplitudes':['a','b'],
            'passed':all(v==0 for v in div+bianchi)}


def scalar_radius_variation():
    # In the 4D Jordan-frame reduced action (up to boundary terms),
    # L ~ rho [R4 - (rho²k²/4)F²].  Variation w.r.t rho generates an F² source.
    rho,k,R4,F2=s.symbols('rho k R4 F2',real=True)
    integrand=rho*(R4-rho**2*k**2*F2/4)
    eq=s.diff(integrand,rho)
    expected=R4-3*rho**2*k**2*F2/4
    return {'radion_equation':str(eq),'difference':str(s.simplify(eq-expected)),
            'passed':s.simplify(eq-expected)==0}


def main():
    data={'fiveD_Ricci':five_d_curvature_test(),
          'source_free_4D_photon':polarization_test(),
          'radius_variation':scalar_radius_variation()}
    if not all(v['passed'] for v in data.values()):
        raise AssertionError(data)
    return data

if __name__=='__main__':
    print(json.dumps(main(),ensure_ascii=False,indent=2))
