"""Exact symbolic identities. No observational-data or theory-discovery claims."""
from pathlib import Path
import json
import sympy as s
ROOT=Path(__file__).resolve().parent
checks=[]
def ck(label, expr):
    x=s.simplify(expr)
    if isinstance(x,s.MatrixBase):
        good=all(s.simplify(s.expand_complex(item))==0 for item in x)
    else: good=(s.simplify(s.expand_complex(x))==0)
    checks.append({'label':label,'pass':bool(good)})
    if not good: raise AssertionError(f'{label}: residual={x}')

w,beta=s.symbols('w beta', real=True, nonzero=True)
phi=s.symbols('phi',real=True)
a,u=s.symbols('a u',positive=True,real=True)
v2=a*a*w*w+u*u
kappa=a*w*w/v2
tau=u*w/v2
ck('general helix curvature-torsion identity',s.factor(v2*(kappa*kappa+tau*tau)-w*w))
# Correct constrained identity after eliminating u^2 through substitution in the single denominator.
ck('unit speed identity (substitute full v²)',s.factor((a*a*w**4+u*u*w*w)-w*w).subs(u*u,1-a*a*w*w))
R2=s.Matrix([[s.cos(phi),-s.sin(phi)],[s.sin(phi),s.cos(phi)]])
eplus=s.Matrix([1,s.I])/s.sqrt(2)
eminus=s.Matrix([1,-s.I])/s.sqrt(2)
ck('spin1 + rotation eigenvalue',s.trigsimp(R2*eplus-s.exp(-s.I*phi)*eplus))
ck('spin1 - rotation eigenvalue',s.trigsimp(R2*eminus-s.exp(s.I*phi)*eminus))
tp=eplus*eplus.T
tm=eminus*eminus.T
ck('spin2 + rotation eigenvalue',s.trigsimp(R2*tp*R2.T-s.exp(-2*s.I*phi)*tp))
ck('spin2 - rotation eigenvalue',s.trigsimp(R2*tm*R2.T-s.exp(2*s.I*phi)*tm))
ck('spin2 traceless',s.trace(tp))
ck('spin2 polarization normalization',s.trace(s.conjugate(tp).T*tp)-1)
eta=s.diag(-1,1,1,1)
k=s.Matrix([-w,0,0,w]) # covariant wave-vector
ku=eta*k
J=s.symbols('J')
e=s.Matrix([0,1,s.I,0])/s.sqrt(2)
F=s.I*(k*e.T-e*k.T)
ck('Maxwell wave null', (k.T*ku)[0])
ck('Maxwell wave transverse', (ku.T*e)[0])
ck('Maxwell source-free Fourier equation',ku.T*F)
Fshift=s.I*(k*(e+J*k).T-(e+J*k)*k.T)
ck('Maxwell gauge shift F invariant',Fshift-F)
H,X=s.symbols('H X')
h=s.zeros(4)
h[1,1]=H;h[2,2]=-H;h[1,2]=X;h[2,1]=X
trace=(eta*h).trace();kh=ku.T*h
ksq=(k.T*ku)[0]
khk=(ku.T*h*ku)[0]
def einstein(hh):
 tr=(eta*hh).trace(); kk=(ku.T*hh*ku)[0]; kv=ku.T*hh
 return s.simplify(-s.Rational(1,2)*(k*kv+kv.T*k.T-ksq*hh-k*k.T*tr-eta*(kk-ksq*tr)))

def riemann(hh,mu,nu,rho,sigma):
 return -s.Rational(1,2)*(k[rho]*k[nu]*hh[mu,sigma]+k[sigma]*k[mu]*hh[nu,rho]
            -k[sigma]*k[nu]*hh[mu,rho]-k[rho]*k[mu]*hh[nu,sigma])
ck('spin2 TT trace',trace)
ck('spin2 TT divergence',ku.T*h)
ck('spin2 Einstein equations on shell',einstein(h))
xi=s.Matrix(s.symbols('xi0:4'))
shift=k*xi.T+xi*k.T
ck('linearized Einstein gauge invariance',einstein(h+shift)-einstein(h))
ck('linearized Riemann gauge invariance R0101',riemann(h+shift,0,1,0,1)-riemann(h,0,1,0,1))
ck('linearized Riemann gauge invariance R0113',riemann(h+shift,0,1,1,3)-riemann(h,0,1,1,3))
ck('linearized tidal curvature R0101',riemann(h,0,1,0,1)-w*w*H/2)
ck('linearized tidal curvature R0102',riemann(h,0,1,0,2)-w*w*X/2)
ck('Bianchi divergence (TT)',ku.T*einstein(h))
# Explicit TT projection for + and x modes along z (no hidden gauge modes).
P=s.diag(1,1,0)
S=s.Matrix([[s.symbols('Sxx'),s.symbols('Sxy'),s.symbols('Sxz')],
            [s.symbols('Sxy'),s.symbols('Syy'),s.symbols('Syz')],
            [s.symbols('Sxz'),s.symbols('Syz'),s.symbols('Szz')]])
T=P*S*P-s.Rational(1,2)*P*s.trace(P*S)
ck('TT tensor trace',s.trace(T))
ck('TT tensor transverse',T*s.Matrix([0,0,1]))
ck('TT projection eliminates longitudinal terms',T[0,2]+T[1,2]+T[2,2])
results={'model':'ROOT_V152','symbolic_checks':len(checks),'passed':all(z['pass'] for z in checks),'checks':checks,
 'limits':'Only identities of specified Maxwell and linearized-gravity fields; does not derive either from helices.'}
out=ROOT/'results'/'symbolic_audit.json';out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'symbolic_checks':len(checks),'passed':results['passed']}))
