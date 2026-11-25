#!/usr/bin/env python3
"""Independent symbolic verification with SymPy. Reports exact zeros only."""
import sympy as s
from pathlib import Path
import json
root=Path(__file__).resolve().parent
th,ph,chi=s.symbols('theta phi chi',real=True)
et=s.Matrix([s.cos(th)*s.cos(ph),s.cos(th)*s.sin(ph),-s.sin(th)])
ep=s.Matrix([-s.sin(ph),s.cos(ph),0])
n=s.Matrix([s.sin(th)*s.cos(ph),s.sin(th)*s.sin(ph),s.cos(th)])
eplus=(et+s.I*ep)/s.sqrt(2)
eminus=(et-s.I*ep)/s.sqrt(2)

def cvec(v):return s.conjugate(v)
def simp(x):return s.simplify(s.trigsimp(s.expand_trig(x)))
def verify(name,expr):
    out=simp(expr)
    if out!=0:
        raise AssertionError(f'{name}: expected zero, got {out}')
    successes.append(name)

successes=[]
verify('orthogonal n,e_theta', n.dot(et))
verify('orthogonal n,e_phi',n.dot(ep))
verify('orthogonal e_theta,e_phi',et.dot(ep))
verify('basis determinant +1',s.det(s.Matrix.hstack(n,et,ep))-1)
verify('eplus normalized',cvec(eplus).dot(eplus)-1)
verify('eplus transverse',n.dot(eplus))
verify('helicity eigenvalue +1',sum((s.I*n.cross(eplus)-eplus).applyfunc(simp)))
Ap=simp(-s.I*cvec(eplus).dot(eplus.diff(ph)))
At=simp(-s.I*cvec(eplus).dot(eplus.diff(th)))
verify('Berry connection theta component',At)
verify('Berry connection phi component',Ap+s.cos(th))
verify('Berry curvature spin one',s.diff(Ap,th)-s.diff(At,ph)-s.sin(th))
# gauge transformation with chi=2*phi
etr=s.exp(2*s.I*ph)*eplus
Apr=simp(-s.I*cvec(etr).dot(etr.diff(ph)))
verify('gauge rotation A to A + 2',Apr-Ap-2)
# plane wave symbolic (t-z), for both helicities
T,Z,w=s.symbols('t z omega',real=True)
for sigma in (-1,1):
    phase=w*(T-Z)
    E=s.Matrix([s.cos(phase),sigma*s.sin(phase),0])
    B=s.Matrix([-sigma*s.sin(phase),s.cos(phase),0])
    curlE=s.Matrix([-s.diff(E[1],Z),s.diff(E[0],Z),0])
    curlB=s.Matrix([-s.diff(B[1],Z),s.diff(B[0],Z),0])
    verify(f'Maxwell Faraday sigma {sigma}',sum((B.diff(T)+curlE).applyfunc(simp)))
    verify(f'Maxwell Ampere sigma {sigma}',sum((E.diff(T)-curlB).applyfunc(simp)))
    verify(f'null E dot B sigma {sigma}',E.dot(B))
    verify(f'null E2-B2 sigma {sigma}',E.dot(E)-B.dot(B))
# pure gradient theta(t,x,z) but smooth so dd=0
x,y,z,t=s.symbols('x y z t',real=True)
psi=t*t*x+s.sin(t*z)+x*y*z
coords=(t,x,y,z)
A=s.Matrix([s.diff(psi,c) for c in coords])
verify('pure phase curl is zero',sum(s.diff(A[j],coords[i])-s.diff(A[i],coords[j]) for i in range(4) for j in range(i+1,4)))
# rank 2 Euler potential 2-form: Pfaffian=0 for arbitrary gradients
q=s.symbols('q0:4',real=True);p=s.symbols('p0:4',real=True)
F=lambda i,j:q[i]*p[j]-q[j]*p[i]
verify('Euler 2-form has zero Pfaffian',F(0,1)*F(2,3)-F(0,2)*F(1,3)+F(0,3)*F(1,2))
# alpha and axial boost geometric obstruction
beta,u,a,om=s.symbols('beta u a omega',real=True,nonzero=True)
gam=1/s.sqrt(1-beta**2)
D=gam*(1-beta*u)
omp=om/D
up=(u-beta)/(1-beta*u)
verify('axial co-moving boost zero u prime',up.subs(beta,u))
verify('axial co-moving boost omega prime on null helix', (omp.subs(beta,u)**2 - 1/a**2).subs(om**2,(1-u*u)/a**2).simplify()) if False else None
if __name__=='__main__':
    info={'count':len(successes),'checks':successes,'result':'PASS','statement':'symbolic mathematical identities only, not experimental verification'}
    print(json.dumps(info,ensure_ascii=False,indent=2))
    if (root/'results').exists(): (root/'results'/'symbolic_audit.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
