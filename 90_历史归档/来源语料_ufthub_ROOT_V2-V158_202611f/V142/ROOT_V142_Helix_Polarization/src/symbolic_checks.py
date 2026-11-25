"""Reproducible SymPy computations: pure gauge SO(3), geometric projection, Maxwell equations."""
import json
import sympy as sp


def run_symbolic():
    x,y,t,z,alpha,beta,k=sp.symbols('x y t z alpha beta k',real=True)
    Rz=sp.Matrix([[sp.cos(beta*y),-sp.sin(beta*y),0],
                  [sp.sin(beta*y),sp.cos(beta*y),0],[0,0,1]])
    Ry=sp.Matrix([[sp.cos(alpha*x),0,sp.sin(alpha*x)],
                  [0,1,0],[-sp.sin(alpha*x),0,sp.cos(alpha*x)]])
    R=Rz*Ry
    inv=R.T
    W_x=sp.simplify(inv*sp.diff(R,x))
    W_y=sp.simplify(inv*sp.diff(R,y))
    curvature=sp.diff(W_y,x)-sp.diff(W_x,y)+W_x*W_y-W_y*W_x
    curvature=curvature.applyfunc(sp.trigsimp)
    if curvature != sp.zeros(3):
        raise AssertionError('Maurer-Cartan curvature should vanish')
    n=R*sp.Matrix([0,0,1])
    proj=sp.trigsimp((n.dot(sp.diff(n,x).cross(sp.diff(n,y))))/2)
    if sp.trigsimp(proj-alpha*beta*sp.sin(alpha*x)/2)!=0:
        raise AssertionError('projection curvature mismatch')
    phase=k*(t-z)
    E=sp.Matrix([sp.cos(phase),sp.sin(phase),0])
    B=sp.Matrix([-sp.sin(phase),sp.cos(phase),0])
    Bwrong=-B
    def curl_zdep(v):
        return sp.Matrix([-sp.diff(v[1],z),sp.diff(v[0],z),0])
    faraday=sp.simplify(sp.diff(B,t)+curl_zdep(E))
    ampere=sp.simplify(sp.diff(E,t)-curl_zdep(B))
    assert faraday == sp.zeros(3,1) and ampere == sp.zeros(3,1)
    wrong_faraday=sp.simplify(sp.diff(Bwrong,t)+curl_zdep(E))
    wrong_ampere=sp.simplify(sp.diff(E,t)-curl_zdep(Bwrong))
    assert sp.simplify(wrong_faraday-2*k*E) == sp.zeros(3,1)
    assert sp.simplify(wrong_ampere-2*k*sp.diff(E,t)/k)==sp.zeros(3,1)
    result={
        'pure_gauge_curvature_zero':str(curvature==sp.zeros(3)),
        'projected_curvature_Fxy':str(proj),
        'maxwell_faraday_residual':str(faraday),
        'maxwell_ampere_residual':str(ampere),
        'wrong_sign_faraday_residual':str(wrong_faraday),
        'wrong_sign_ampere_residual':str(wrong_ampere),
        'symbolic_assertions_passed':True
    }
    return result

if __name__=='__main__':
    print(json.dumps(run_symbolic(),ensure_ascii=False,indent=2))
