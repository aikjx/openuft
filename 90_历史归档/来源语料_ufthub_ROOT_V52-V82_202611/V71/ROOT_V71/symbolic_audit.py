"""Independent symbolic audits with SymPy, not empirical evidence."""
import json
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent
x,R,r,L,alpha,M,G=s.symbols('x R r L alpha M G',positive=True)
F=3*(x*s.cosh(x)-s.sinh(x))/x**3
series=s.series(F,x,0,10).removeO()
expected=1+x**2/s.Integer(10)+x**4/s.Integer(280)+x**6/s.Integer(15120)+x**8/s.Integer(1330560)
assert s.simplify(series-expected)==0
pot=-G*alpha*M*F.subs(x,R/L)*s.exp(-r/L)/r
force_ratio=s.simplify(s.diff(pot,r)*r*r/(G*M))
assert s.simplify(force_ratio-alpha*F.subs(x,R/L)*s.exp(-r/L)*(1+r/L))==0
srad=s.symbols('srad',positive=True)
radial_integral=s.integrate(srad*s.sinh(srad/L),(srad,0,R))
assert s.simplify(radial_integral-L**2*((R/L)*s.cosh(R/L)-s.sinh(R/L)))==0
# Dimensional inconsistency: A*[a,b]=[3,-1,-2] over (L,M,T), no exact solution.
a,b=s.symbols('a b')
assert s.solve([a+2*b-3,b+1,-a-b+2],[a,b])==[]
# Check exact hypercharge sums without floating-point errors
Q=[(6,s.Rational(1,6)),(3,s.Rational(-2,3)),(3,s.Rational(1,3)),(2,s.Rational(-1,2)),(1,s.Integer(1))]
assert sum(n*q for n,q in Q)==0
assert sum(n*q**3 for n,q in Q)==0
# Helical Frenet kappa/tau via determinant formula
T,w,u=s.symbols('T w u',real=True,nonzero=True)
RR=s.symbols('RR',positive=True)
v=s.Matrix([-RR*w*s.sin(w*T),RR*w*s.cos(w*T),u]);acc=s.diff(v,T);jerk=s.diff(acc,T)
cross=s.simplify(v.cross(acc)); v2=RR**2*w**2+u*u
k2=s.simplify(cross.dot(cross)/v2**3)
tors=s.simplify(s.det(s.Matrix.hstack(v,acc,jerk))/cross.dot(cross))
assert s.simplify(k2-(RR*w*w/v2)**2)==0
assert s.simplify(tors-u*w/v2)==0
out={'status':'passed','symbolic_checks':8,'finite_sphere_series':str(series),
     'force_ratio':str(force_ratio),'radial_integral':str(radial_integral),'torsion':str(tors),
     'G_dimensional_no_solution':True,'exact_SM_U1_anomalies':True}
(P/'results'/'symbolic_audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print('SymPy audits: 8 passed')
