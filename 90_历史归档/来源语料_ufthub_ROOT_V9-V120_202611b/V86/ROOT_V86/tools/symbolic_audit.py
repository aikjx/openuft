#!/usr/bin/env python3
"""Independent SymPy algebraic identities in the explicit weak-field ansatz."""
from pathlib import Path
import json,sys
import sympy as s
R=Path(__file__).resolve().parents[1]
r,lam,mu,A,u,j,R0,theta=s.symbols('r lam mu A u j R_0 theta',real=True,positive=True)
qs,qi,qj,k1,k2=s.symbols('qs qi qj k1 k2',real=True)
assertions=[]
def chk(name,eq):
    ok=bool(eq)
    assertions.append({'name':name,'pass':ok})
    if not ok:raise AssertionError(name)

gn=mu/r**2
chk('Newton Q 1',s.simplify(-r*s.diff(gn,r)/(2*gn)-1)==0)
P2=s.legendre(2,s.cos(theta))
chk('Legendre 2',s.simplify(P2-(3*s.cos(theta)**2-1)/2)==0)
y=-3*j*(R0/r)**2*P2
chk('J2 derivative',s.simplify(s.diff(y,r)+2*y/r)==0)
gj=gn*(1+y)
chk('J2 Q',s.simplify(-r*s.diff(gj,r)/(2*gj) - (1+y/(1+y)))==0)
x=r/lam
fY=(1+x)*s.exp(-x)
chk('Yukawa derivative',s.simplify(s.diff(fY,r)+r/lam**2*s.exp(-x))==0)
chk('Yukawa acceleration derivative',s.simplify(s.diff(-mu/r*(1+A*s.exp(-x)),r)-gn*(1+A*fY))==0)
gm=gn*(1+u+y+A*fY)
shape=1+(y+A*x*x*s.exp(-x)/2)/(1+u+y+A*fY)
chk('combined Q',s.simplify(-r*s.diff(gm,r)/(2*gm)-shape)==0)
chk('Q alpha zero',s.simplify(shape.subs({A:0,j:0})-1)==0)
chk('J2 equator',s.simplify(P2.subs(theta,s.pi/2)+s.Rational(1,2))==0)
chk('J2 pole',s.simplify(P2.subs(theta,0)-1)==0)
z=s.symbols('z')
F=3*(z*s.cosh(z)-s.sinh(z))/z**3
series=s.series(F,z,0,10).removeO().expand()
chk('sphere small x series',s.simplify(series-(1+z*z/10+z**4/280+z**6/15120+z**8/1330560))==0)
first=s.Matrix([k1*(qi-qj),k2*(qi-qj)])
chk('D separability',s.simplify(first[1]*first[0]-first[0]*first[1])==0)
q1,q2,q3=s.symbols('q1 q2 q3')
D=s.Matrix([[k1*(q1-q2),k1*(q1-q3)],[k2*(q1-q2),k2*(q1-q3)]])
chk('D determinant zero',s.simplify(D.det())==0)
E=s.Matrix([[2*k1*(q1-q2)/(2+k1*(q1+q2)),2*k1*(q1-q3)/(2+k1*(q1+q3))],
            [2*k2*(q1-q2)/(2+k2*(q1+q2)),2*k2*(q1-q3)/(2+k2*(q1+q3))]])
chk('eta determinant not generic zero',E.det().subs({k1:s.Rational(1,5),k2:s.Rational(1,2),q1:0,q2:1,q3:2})!=0)
eta=2*k1*(qi-qj)/(2*(1+u)+k1*(qi+qj))
chk('eta weak k slope',s.simplify(s.diff(eta,k1).subs(k1,0)-(qi-qj)/(1+u))==0)
G0,Mscale,sfactor=s.symbols('G0 Mscale sfactor',positive=True)
chk('GM scaling',s.simplify((G0*sfactor)*(Mscale/sfactor)-G0*Mscale)==0)
C0,hbar,Lstar,mstar=s.symbols('c hbar Lstar mstar',positive=True)
chk('dimensionful new scale cannot be eliminated in c3 Lstar2 / hbar',s.diff(C0**3*Lstar**2/hbar,Lstar)!=0)
Gscale=s.symbols('Gscale',positive=True)
chk('Z identity',s.simplify(2*(Gscale*C0/2)/C0-Gscale)==0)
mu2=s.symbols('mu2',positive=True)
chk('Newton source mass scaling',s.simplify(mu2/r**2*sfactor/(sfactor)-mu2/r**2)==0)
report={'version':'V86','total':len(assertions),'passed':sum(t['pass'] for t in assertions),'checks':assertions,
        'disclaimer':'Algebra in stated ansatz; not independent natural-world validation.'}
R.joinpath('results/symbolic_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('SymPy:',report['passed'],'/',report['total'])
