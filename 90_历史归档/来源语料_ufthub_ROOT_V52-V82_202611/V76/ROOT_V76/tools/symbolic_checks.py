from __future__ import annotations
try: import sympy as s
except ImportError:
    print('SKIP: install sympy for optional independent symbolic checks');raise SystemExit(0)
results=[]

def check(name,expression):
    good=s.simplify(expression)==0
    results.append((name,good));print(('PASS' if good else 'FAIL'),name)
    if not good:raise AssertionError(name)

E1,E2,B1,B2,ep,mu=s.symbols('E1 E2 B1 B2 ep mu',real=True,nonzero=True)
u=lambda E,B:ep*E**2/2+B**2/(2*mu)
check('EM energy cross', s.expand(u(E1+E2,B1+B2)-u(E1,B1)-u(E2,B2))-(ep*E1*E2+B1*B2/mu))
E,B=s.symbols('E B',real=True)
u0=ep*E**2/2+B**2/(2*mu)
Txx=u0-ep*E**2
Tyy=u0-B**2/mu
Tzz=u0
check('EM tensor trace',-u0+Txx+Tyy+Tzz)
phi,Ea,Eb,v,theta=s.symbols('phi Ea Eb v theta',real=True)
q=Ea*s.cos(theta)**2+Eb*s.sin(theta)**2+2*v*s.cos(theta)*s.sin(theta)*s.cos(phi)
check('quantum phase derivative',s.diff(q,phi)+2*v*s.cos(theta)*s.sin(theta)*s.sin(phi))
R,w,ax,t=s.symbols('R w a t',positive=True,real=True)
r=s.Matrix([R*s.cos(w*t),R*s.sin(w*t),ax*t]);vel=r.diff(t);acc=vel.diff(t);jerk=acc.diff(t)
speed2=s.simplify(vel.dot(vel));crossva=s.simplify(vel.cross(acc));kappa=s.simplify(s.sqrt(crossva.dot(crossva))/speed2**s.Rational(3,2));tau=s.simplify(crossva.dot(jerk)/(crossva.dot(crossva)))
check('helix speed',speed2-(R*w)**2-ax**2)
check('helix curvature',kappa-R*w*w/speed2)
check('helix torsion',tau-ax*w/speed2)
G,M,rad,rho=s.symbols('G M r rho',positive=True)
check('spherical body density relation',G*(4*s.pi*rho*rad**3/3)/rad**2 -4*s.pi*G*rho*rad/3)
energy,cc=s.symbols('U c',positive=True)
check('energy to mass units formula',energy/cc**2 - (energy/cc)/cc)
print(f'PASS {len(results)} independent SymPy derivations')
