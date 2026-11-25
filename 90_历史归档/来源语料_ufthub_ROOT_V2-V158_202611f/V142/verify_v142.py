"""ROOT V142: symbolic checks and reproducible SI predictions. Python 3.10+, sympy."""
import sympy as s
from decimal import Decimal as D, getcontext
import csv, json
from pathlib import Path
from fractions import Fraction as F
getcontext().prec=70
out=Path(__file__).resolve().parent
checks=[]
def check(name, condition):
    if not bool(condition): raise AssertionError(name)
    checks.append(name)
a,b,d,B,t,w,k=s.symbols('a b d B t omega k', real=True)
ex,ey,ez,bx,by,bz=s.symbols('ex ey ez bx by bz',real=True)
X=t*t*(ex**2+ey**2+ez**2)-(t*t*(bx**2+by**2)+(B+t*bz)**2)
Y=t*(ex*t*bx+ey*t*by+ez*(B+t*bz))
L=X/2+a*X**2+b*Y**2+d*X*Y
L2=s.expand(L).coeff(t,2)
C=1-4*a*B**2
expected=C*(ex**2+ey**2+ez**2-bx**2-by**2-bz**2)/2+4*a*B**2*bz**2+b*B**2*ez**2-d*B**2*(ex*bx+ey*by+ez*bz+2*bz*ez)
check('quadratic action expansion',s.expand(L2-expected)==0)
Ay,Az=s.symbols('Ay Az',real=True)
M=s.hessian(L2.subs({ex:0,bx:0,ey:w*Ay,ez:w*Az,by:-k*Az,bz:k*Ay}),(Ay,Az))
M0=s.Matrix([[C*w*w-(C-8*a*B**2)*k*k,-2*d*B**2*w*k],[-2*d*B**2*w*k,(C+2*b*B**2)*w*w-C*k*k]])
check('wave matrix from Hessian',s.simplify(M-M0)==s.zeros(2))
check('Maxwell limit',s.simplify(M.subs({a:0,b:0,d:0})-(w*w-k*k)*s.eye(2))==s.zeros(2))
check('perpendicular dispersion',s.simplify(M[0,0].subs(w,k*s.sqrt((C-8*a*B**2)/C)))==0)
check('parallel dispersion',s.simplify(M[1,1].subs(w,k*s.sqrt(C/(C+2*b*B**2))))==0)
x,y=s.symbols('X Y',real=True)
lag=x/2+a*x*x+b*y*y+d*x*y
trace=4*(lag-x*s.diff(lag,x)-y*s.diff(lag,y))
check('metric trace by scaling',s.expand(trace+4*(a*x*x+b*y*y+d*x*y))==0)
check('null field trace',trace.subs({x:0,y:0})==0)
check('magnetic field trace',s.expand(trace.subs({x:-B**2,y:0})+4*a*B**4)==0)
# linear-order index matrix, compare characteristic polynomial after scaling omega/k=1-B² r
r,z=s.symbols('r z',real=True)
N=M.subs({k:1,w:1-z*r,B:s.sqrt(z)})
Nlead=N.applyfunc(lambda v:s.expand(v).coeff(z,1)/2)
check('leading index matrix',s.simplify(Nlead-s.Matrix([[4*a-r,-d],[-d,b-r]]))==s.zeros(2))
check('leading squared splitting',s.expand((4*a+b)**2-4*(4*a*b-d*d)-((4*a-b)**2+4*d*d))==0)
# Exact rational scan in weak field, only parity-even model. Not independent experiments.
for ia in range(0,11):
 for ib in range(0,11):
  for B2 in [F(0),F(1,100),F(1,10),F(1)]:
   aa,bb=F(ia,1000),F(ib,1000)
   cc=1-4*aa*B2
   vp=(cc-8*aa*B2)/cc; vl=cc/(cc+2*bb*B2)
   check(f'positive and <=1 {ia},{ib},{B2}',0<vp<=1 and 0<vl<=1)
# SI numerical data using representative Ae and mu0; not measurements
Ae=D('1.32e-24'); mu0=D('1.25663706212e-6'); G=D('6.67430e-11'); c=D(299792458)
pi=D('3.14159265358979323846264338327950288419716939937510')
lam=D('1064e-9'); length=D(1)
rows=[]
for field in map(D,['0','1','2.5','5','10','20']):
  xx=Ae*field**2; cc=1-4*xx
  nperp=(cc/(cc-8*xx)).sqrt(); npar=((cc+14*xx)/cc).sqrt()
  dn=3*xx; phase=2*pi*length*dn/lam
  rho=field**2/(2*mu0); U4=Ae*field**4/mu0
  R=32*pi*G*U4/c**4
  if field: check(f'weak field limit {field}',abs((npar-nperp)/dn-1)<D('1e-18'))
  rows.append(dict(B_T=str(field),n_perp_minus1=str(4*xx),n_parallel_minus1=str(7*xx),delta_n=str(dn),phase_rad=str(phase),ellipticity_rad_45deg=str(phase/2),maxwell_energy_J_m3=str(rho),quartic_L_J_m3=str(U4),ricci_scalar_contribution_m_minus2=str(R)))
with (out/'qed_benchmark.csv').open('w',encoding='utf-8',newline='') as f:
 wr=csv.DictWriter(f,fieldnames=rows[0].keys());wr.writeheader();wr.writerows(rows)
# A single splitting measurement cannot determine all 3 coefficients.
check('degenerate splitting example', (7-4)**2 == (4-4)**2+4*F(3,2)**2)
result={'checks_passed':len(checks),'checks':checks,'benchmark_5T':rows[3],'limitations':['symbolic and rational tests, not experiments','fixed magnetic background, transverse propagation, quartic EFT only','no independent prediction of G or four-force unification']}
(out/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'checks_passed':len(checks),'benchmark_5T':rows[3]},indent=2))
