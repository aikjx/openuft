"""Independent SymPy checks on symbolic identities. Optional dependency: sympy."""
import json,pathlib
import sympy as s
R,omega,u,t=s.symbols('R omega u t',positive=True,real=True)
G,c,M,r,rho=s.symbols('G c M r rho',positive=True,real=True)
chi,T,m,eta,ell,K=s.symbols('chi T m eta ell K',real=True)
checks={}
x=s.Matrix([R*s.cos(omega*t),R*s.sin(omega*t),u*t]);v=x.diff(t);a=v.diff(t);j=a.diff(t)
v2=s.simplify(v.dot(v));checks['helix_speed_squared']=s.simplify(v2-R**2*omega**2-u**2)==0
checks['orthogonal_v_a']=s.trigsimp(v.dot(a))==0
kappa=s.simplify(v.cross(a).norm()/v2**s.Rational(3,2))
checks['helix_curvature']=s.simplify(kappa-R*omega**2/(R**2*omega**2+u**2))==0
torsion=s.trigsimp((v.cross(a)).dot(j)/(v.cross(a)).dot(v.cross(a)))
checks['helix_torsion']=s.simplify(torsion-u*omega/(R**2*omega**2+u**2))==0
Kexpr=48*G**2*M**2/(c**4*r**6)
checks['surfaceK_fixed_density']=s.simplify(Kexpr.subs({M:4*s.pi*rho*r**3/3})-s.Rational(256,3)*s.pi**2*G**2*rho**2/c**4)==0
g=G*M/r**2
g0=s.symbols('g0',positive=True,real=True)
checks['K_fixed_g']=s.simplify(Kexpr.subs({M:g0*r*r/G})-48*g0**2/(c**4*r**2))==0
h=s.symbols('h',positive=True)
checks['same_g_K_scaling']=s.simplify((Kexpr.subs({M:h*r*r/G}))/ (48*h*h/(c**4*r**2))-1)==0
xv=s.symbols('x')
F=3*(xv*s.cosh(xv)-s.sinh(xv))/xv**3
checks['uniform_ball_smallx']=s.limit(F,xv,0)==1
checks['uniform_ball_second_order']=s.simplify(s.diff(F,xv,2).limit(xv,0)-s.Rational(1,5))==0
# Euler-Lagrange for homogeneous scalar χ(T) with constant external curvature K.
y=s.Function('y')(T)
L=s.diff(y,T)**2/2-m*m*y*y/2+eta*ell*ell*K*y*y/2
EL=s.diff(s.diff(L,s.diff(y,T)),T)-s.diff(L,y)
checks['scalar_GB_homogeneous_EL']=s.simplify(EL-(s.diff(y,T,2)+(m*m-eta*ell*ell*K)*y))==0
Y=[(3,2,s.Rational(1,6)),(3,1,-s.Rational(2,3)),(3,1,s.Rational(1,3)),(1,2,-s.Rational(1,2)),(1,1,s.Integer(1))]
checks['U1_cube_anomaly']=sum([col*wk*hyp**3 for col,wk,hyp in Y])==0
checks['grav_U1_anomaly']=sum([col*wk*hyp for col,wk,hyp in Y])==0
checks['SU3_sq_U1_anomaly']=s.Rational(1,2)*(2*s.Rational(1,6)-s.Rational(2,3)+s.Rational(1,3))==0
checks['SU2_sq_U1_anomaly']=s.Rational(1,2)*(3*s.Rational(1,6)-s.Rational(1,2))==0
report={'checks':{k:bool(v) for k,v in checks.items()},'passed':sum(bool(v) for v in checks.values()),'total':len(checks),'scope':'symbolic necessary checks; no new physics validation'}
path=pathlib.Path(__file__).resolve().parent/'results/symbolic_checks.json'
path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
assert all(checks.values()),'symbolic check failed'
