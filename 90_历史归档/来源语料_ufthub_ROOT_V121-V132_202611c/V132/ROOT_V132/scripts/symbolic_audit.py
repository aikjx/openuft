"""Independent symbolic audit with SymPy; geometry only; c=1 convention."""
import sympy as s
from pathlib import Path
r,w,u,t,beta=s.symbols('R omega u t beta',real=True,positive=True)
# allow signed axial velocity separately for boost algebra
v2=r*r*w*w+u*u
x=s.Matrix([r*s.cos(w*t),r*s.sin(w*t),u*t])
x1=x.diff(t);x2=x1.diff(t);x3=x2.diff(t)
cr=s.simplify(x1.cross(x2))
triple=s.trigsimp(s.expand(cr.dot(x3)))
crosssq=s.simplify(s.trigsimp(cr.dot(cr)))
spd2=s.simplify(s.trigsimp(x1.dot(x1)))
assert s.simplify(spd2-v2)==0
assert s.simplify(crosssq-r*r*w**4*v2)==0
assert s.simplify(triple-u*r*r*w**5)==0
kappa_formula=r*w*w/v2
tau_formula=u*w/v2
assert s.simplify((kappa_formula*kappa_formula+tau_formula*tau_formula)-w*w/v2)==0
# under normalization, h_geo = u is exact
assert s.simplify((tau_formula*s.sqrt(v2)/w)-u/s.sqrt(v2))==0
# nonlinear boost formula and normalization
nu=s.symbols('U',real=True)
gamma=1/s.sqrt(1-beta**2)
wp=w/(gamma*(1-beta*nu))
up=(nu-beta)/(1-beta*nu)
vperp=s.sqrt(1-nu**2)/(gamma*(1-beta*nu))
assert s.simplify(vperp*vperp+up*up-1)==0
assert s.simplify((up-nu)-beta*(nu**2-1)/(1-beta*nu))==0
# symbolic derivatives for uncertainty propagation
alpha=s.symbols('alpha',positive=True)
f=alpha/s.sqrt(1-alpha**2)
assert s.simplify(s.diff(f,alpha)-(1-alpha**2)**s.Rational(-3,2))==0
log='''ROOT V132 Symbolic audit: PASS
1. Velocity squared = R^2 omega^2 + u^2
2. Frenet cross squared = R^2 omega^4 v^2
3. Triple determinant = u R^2 omega^5
4. kappa = R omega^2/v^2, tau = u omega/v^2
5. kappa^2+tau^2 = omega^2/v^2
6. h_geo = u/v; under v=1, h_geo=u
7. Axial Lorentz boost preserves null speed
8. Under boost h_geo changes unless beta=0 or |u|=1
9. d[alpha/sqrt(1-alpha^2)]/d alpha=(1-alpha^2)^(-3/2)
Pass: all symbolic checks.
'''
root=Path(__file__).resolve().parents[1]
(root/'evidence/symbolic_audit.txt').write_text(log,encoding='utf-8')
print(log)
