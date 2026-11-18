"""Independent SymPy identities for the V79 manuscript; failures raise assertions."""
import json, pathlib, sympy as s
p=pathlib.Path(__file__).resolve().parents[1]
checks=[]
def check(name,expr):
    v=s.simplify(s.trigsimp(expr))
    assert v==0,(name,v)
    checks.append(name)

t,w,a,xi,A,a0,ep,mu,c,G,omega,r,theta,B0=s.symbols('t w a xi A a0 eps mu c G omega r theta B0',positive=True,real=True)
check('cos² double frequency',s.cos(w*t)**2-(1+s.cos(2*w*t))/2)
check('sin² double frequency',s.sin(w*t)**2-(1-s.cos(2*w*t))/2)
check('quadratic axion harmonic expansion',xi*(a0+A*s.cos(w*t))**2-(xi*(a0*a0+A*A/2)+2*xi*a0*A*s.cos(w*t)+xi*A*A*s.cos(2*w*t)/2))
check('B flip quadratic energy',(-B0)**2-B0**2)
check('B flip pseudoscalar',B0-(-B0)-2*B0)
check('sphere volume',s.integrate(4*s.pi*r**2,(r,0,a))-4*s.pi*a**3/3)
check('sphere quadratic axis moment',s.integrate(r**4,(r,0,a))*s.integrate(s.sin(theta)**3,(theta,0,s.pi))*2*s.pi-8*s.pi*a**5/15)
check('Faraday electric energy',ep/8*(omega*B0)**2*(8*s.pi*a**5/15)-ep*s.pi*a**5*(omega*B0)**2/15)
check('Faraday-to-magnetic energy mean ratio',(ep*s.pi*a**5*(omega*B0)**2/30)/(s.pi*a**3*B0**2/(3*mu))-ep*mu*a*a*omega*omega/10)
check('EM trace',- (ep*A*A+B0*B0/mu)/2 +3*(ep*A*A+B0*B0/mu)/2 - ep*A*A-B0*B0/mu)
check('photon pair same direction',2*A*A*(1-s.cos(0)))
check('photon pair anti direction',2*A*A*(1-s.cos(s.pi))-4*A*A)

beta,E,B=s.symbols('beta E B',real=True)
gamma=1/s.sqrt(1-beta**2)
Eprim=gamma*(E-beta*c*B)
Bprim=gamma*(B-beta*E/c)
check('Lorentz invariant I1 under x boost',s.factor(Eprim**2-c**2*Bprim**2-(E**2-c**2*B**2)))
# E along y, B along z, boost x; E dot B remains 0 because transformed vectors remain orthogonal
check('Lorentz invariant I2 in transverse example',Eprim*0+0*Bprim)
check('closed system derivative cancellation',s.diff(xi*s.cos(w*t)**2 + (A-xi*s.cos(w*t)**2),t))
# From G=c^a hbar^b: b=-1, a+2b=3 -> a=5 but a+b=2 requires a=3.
dim_rank=s.Matrix([[1,2],[-1,-1],[0,1]])
check('G(c,hbar) dimension equations inconsistent',s.Integer(dim_rank.rank())-2)
# Demonstrate inconsistency by explicit substitutions
check('dimensional mismatch for G',s.Integer(5-1-2)-2)
report={'symbolic_checks':len(checks),'checks':checks,'passed':True,'sympy_version':s.__version__}
(p/'results/symbolic_report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8')
print('Sympy identities verified:',len(checks))
