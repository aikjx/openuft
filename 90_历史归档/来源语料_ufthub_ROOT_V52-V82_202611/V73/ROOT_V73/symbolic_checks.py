"""Independent symbolic checks with SymPy. Requires sympy (optional)."""
import json
from pathlib import Path
import sympy as sp
R,omega,u=sp.symbols('R omega u', real=True,positive=True)
t=sp.symbols('t',real=True)
r=sp.Matrix([R*sp.cos(omega*t),R*sp.sin(omega*t),u*t])
v=sp.diff(r,t);a=sp.diff(v,t);j=sp.diff(a,t)
speed2=sp.simplify(v.dot(v))
kappa=sp.simplify(sp.sqrt((v.cross(a)).dot(v.cross(a)))/speed2**sp.Rational(3,2))
torsion=sp.simplify((v.cross(a)).dot(j)/(v.cross(a)).dot(v.cross(a)))
checks={}
def record(name,expr):
 val=(expr == sp.zeros(*expr.shape)) if isinstance(expr,sp.MatrixBase) else bool(sp.simplify(sp.expand(sp.expand_trig(expr).rewrite(sp.exp)))==0)
 checks[name]=val
 if not val:raise AssertionError((name,expr))
record('螺旋速度平方',speed2-(R*omega)**2-u**2)
record('螺旋曲率',kappa-R*omega**2/speed2)
record('螺旋挠率',torsion-u*omega/speed2)
record('速度垂直加速度',v.dot(a))
x=sp.symbols('x',positive=True)
F=3*(x*sp.cosh(x)-sp.sinh(x))/x**3
S=sp.Rational(3,2)*((x-1)+(x+1)*sp.exp(-2*x))/x**3
record('指数缩放恒等式',sp.exp(-x)*F-S)
record('小球展开到x4',sp.series(F,x,0,6).removeO()-(1+x**2/sp.Integer(10)+x**4/sp.Integer(280)))
b0,g,mu=sp.symbols('b0 g mu',positive=True)
Lambda=mu*sp.exp(-8*sp.pi**2/(b0*g**2))
record('RG尺度灵敏度',sp.diff(sp.log(Lambda),g)-16*sp.pi**2/(b0*g**3))
record('RG beta与尺度导数',sp.diff(sp.log(Lambda),g)*(-b0*g**3/(16*sp.pi**2)) + 1)
# Gauge invariance of a 1+1 U(1) field strength under A -> A + dchi
xx,tt=sp.symbols('xx tt')
At=sp.Function('At')(xx,tt);Ax=sp.Function('Ax')(xx,tt);chi=sp.Function('chi')(xx,tt)
strength=sp.diff(Ax,tt)-sp.diff(At,xx)
transformed=sp.diff(Ax+sp.diff(chi,xx),tt)-sp.diff(At+sp.diff(chi,tt),xx)
record('U1电磁场强不变',transformed-strength)
# Variational derivative for pseudoscalar kinetic + quadratic mass + imposed topological source I
field=sp.Function('phi')(xx,tt)
m,q=sp.symbols('m q',real=True)
source=sp.Function('I')(xx,tt)
Lag=sp.Rational(1,2)*sp.diff(field,tt)**2-sp.Rational(1,2)*sp.diff(field,xx)**2-sp.Rational(1,2)*m**2*field**2-q*field*source
EL=sp.diff(Lag,field)-sp.diff(sp.diff(Lag,sp.diff(field,tt)),tt)-sp.diff(sp.diff(Lag,sp.diff(field,xx)),xx)
expected=-sp.diff(field,tt,2)+sp.diff(field,xx,2)-m*m*field-q*source
record('赝标量欧拉拉格朗日方程',EL-expected)
# Exact orthogonality of Walsh-Hadamard matrix
from itertools import product
rows=[]
for h,r,s in product((-1,1),repeat=3):rows.append([1,h,r,s,h*r,h*s,r*s,h*r*s])
H=sp.Matrix(rows)
record('八态Hadamard正交',H.T*H-8*sp.eye(8))
result={'checks':len(checks),'passed':sum(checks.values()),'details':checks,'sympy_version':sp.__version__}
Path(__file__).parent.joinpath('results','symbolic_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('Symbolic checks:',result['passed'],'/',result['checks'])
