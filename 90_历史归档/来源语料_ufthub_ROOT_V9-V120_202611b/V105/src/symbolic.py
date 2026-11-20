"""Exact symbolic statements. Print count and abort on any failure."""
import sympy as s

def run():
    a,b,theta,f,L,P1,P2,P3,c1,c2,c3 = s.symbols('a b theta f L P1 P2 P3 c1 c2 c3', real=True)
    sx=s.Matrix([[0,1],[1,0]])
    sy=s.Matrix([[0,-s.I],[s.I,0]])
    eye=s.eye(2)
    U=s.cos(a)*eye + s.I*s.sin(a)*sx
    V=s.cos(b)*eye + s.I*s.sin(b)*sy
    W=U*V*U.conjugate().T*V.conjugate().T
    checks={}
    checks['SU2 trace identity']=s.simplify(s.trigsimp(s.expand_trig(s.trace(W)/2 -(1-2*s.sin(a)**2*s.sin(b)**2)))) == 0
    checks['SU2 unitary U']=s.simplify(U*U.conjugate().T-eye)==s.zeros(2)
    checks['SU2 unitary V']=s.simplify(V*V.conjugate().T-eye)==s.zeros(2)
    checks['SU2 determinant U']=s.simplify(s.det(U)-1)==0
    checks['SU2 determinant V']=s.simplify(s.det(V)-1)==0
    checks['SU3 embedded Wilson'] = s.simplify((2*(s.trace(W)/2)+1)/3 - (1-s.Rational(4,3)*s.sin(a)**2*s.sin(b)**2))==0
    checks['commutator nonzero']=sx*sy-sy*sx==2*s.I*s.Matrix([[1,0],[0,-1]])
    checks['U1 commute']=s.simplify(s.exp(s.I*a)*s.exp(s.I*b)-s.exp(s.I*b)*s.exp(s.I*a))==0
    Vtheta=L**4*(1-s.cos(theta))
    checks['periodic potential']=s.simplify(Vtheta.subs(theta,theta+2*s.pi)-Vtheta)==0
    checks['scalar gradient source']=s.simplify(s.diff(Vtheta,theta)-L**4*s.sin(theta))==0
    checks['small fluctuation mass']=s.simplify(s.diff(Vtheta,theta,2).subs(theta,0)/f**2-L**4/f**2)==0
    J=c1*P1+c2*P2+c3*P3
    checks['scalar source derivative']=s.simplify(s.diff(theta*J/s.Integer(4),theta)-J/4)==0
    assert all(checks.values()), [k for k,v in checks.items() if not v]
    return checks

if __name__=='__main__':
    for k,v in run().items():print(f'PASS {k}')
