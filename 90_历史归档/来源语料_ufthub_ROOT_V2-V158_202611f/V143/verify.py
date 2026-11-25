from pathlib import Path
import csv,json,math,itertools,hashlib
import sympy as s
P=Path(__file__).resolve().parent
checks=[]
def ck(name,condition):
    assert condition,name
    checks.append(name)
# curvature convention R_0i0j=(-2,1,1) q; q factored out
eta=[-1,1,1,1]
D={(0,1):-2,(0,2):1,(0,3):1,(1,2):-1,(1,3):-1,(2,3):2}
def R(a,b,c,d):
    if a==b or c==d or sorted((a,b))!=sorted((c,d)): return 0
    return D[tuple(sorted((a,b)))]*(1 if a<b else -1)*(1 if c<d else -1)
for a,b,c,d in itertools.product(range(4),repeat=4):
    ck(f'R symmetry {a}{b}{c}{d}', R(a,b,c,d)==R(c,d,a,b)==-R(b,a,c,d))
    ck(f'Bianchi {a}{b}{c}{d}', R(a,b,c,d)+R(a,c,d,b)+R(a,d,b,c)==0)
for b,d in itertools.product(range(4),repeat=2):
    ck(f'Ricci {b}{d}',sum(eta[a]*R(a,b,a,d) for a in range(4))==0)
ck('Kretschmann',sum(eta[a]*eta[b]*eta[c]*eta[d]*R(a,b,c,d)**2 for a,b,c,d in itertools.product(range(4),repeat=4))==48)
t=s.symbols('t', real=True); n=[1,s.cos(t),s.sin(t),0]; e=[ [0,-s.sin(t),s.cos(t),0],[0,0,0,1] ]
Q=s.Matrix(2,2,lambda i,j:s.trigsimp(sum(R(a,b,c,d)*n[a]*e[i][b]*n[c]*e[j][d] for a,b,c,d in itertools.product(range(4),repeat=4))))
expected=s.diag(-3*s.sin(t)**2,3*s.sin(t)**2)
ck('screen tensor symbolic',all(s.trigsimp(z)==0 for z in Q-expected))
# Exact rational direction sampling, independent of trigonometric simplification
from fractions import Fraction as F
for i in range(-50,51):
    z=F(i,17); x=(1-z*z)/(1+z*z); y=2*z/(1+z*z); k=[1,x,y,0]; E=[[0,-y,x,0],[0,0,0,1]]
    for a,b in itertools.product(range(2),repeat=2):
        val=sum(R(j,l,m,p)*k[j]*E[a][l]*k[m]*E[b][p] for j,l,m,p in itertools.product(range(4),repeat=4))
        ck(f'screen {i} {a}{b}',val== (0 if a!=b else (-1 if a==0 else 1)*3*y*y))
# dimensionless weak-field path integral with t=z/b; analytic infinite integral 4/3
z=s.symbols('z',real=True); primitive=z/s.sqrt(1+z*z)-z**3/(3*(1+z*z)**s.Rational(3,2))
ck('path antiderivative',s.simplify(s.diff(primitive,z)-(1+z*z)**s.Rational(-5,2))==0)
ck('path integral',s.limit(primitive,z,s.oo)-s.limit(primitive,z,-s.oo)==s.Rational(4,3))
N=20000; h=40/N; vals=[(1+(-20+i*h)**2)**(-2.5) for i in range(N+1)]
quad=h/3*(vals[0]+vals[-1]+4*sum(vals[1:-1:2])+2*sum(vals[2:-1:2])); exact=float(2*primitive.subs(z,20))
ck('independent Simpson integration',abs(quad-exact)<1e-11)
alpha=7.2973525643e-3; le=3.8615926744e-13; xi=alpha*le**2/(360*math.pi); c=299792458.; gm_s=1.3271244e20/c**2; gm_e=3.986004418e14/c**2; wavelength=550e-9
cases=[('Earth surface exterior',gm_e,6.371e6),('Sun photosphere exterior',gm_s,6.957e8),('10 solar mass BH photon sphere',10*gm_s,30*gm_s),('1e6 solar mass BH photon sphere',1e6*gm_s,3e6*gm_s)]
rows=[]
for name,mu,r in cases:
    q=mu/r**3; dn=24*xi*q; rows.append(dict(case=name,mu_m=mu,r_m=r,q_m_inv2=q,K_m_inv4=48*q*q,delta_n_tangential=dn,phase_per_local_m_rad=2*math.pi/wavelength*dn))
    ck('positive splitting '+name,dn>0)
with (P/'local.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
paths=[]
for name,mu,b in cases[:2]:
    optical=32*xi*mu/b**2; phase=2*math.pi/wavelength*optical
    paths.append(dict(case=name,impact_m=b,delta_optical_length_m=optical,phase_rad=phase,delay_s=optical/c,xi_for_1urad_m2=1e-6*wavelength*b*b/(64*math.pi*mu)))
with (P/'paths.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=paths[0]);w.writeheader();w.writerows(paths)
results=dict(checks_passed=len(checks),check_names=checks,xi_qed_abs_m2=xi,screen=str(Q),simpson=quad,simpson_exact=exact,local=rows,paths=paths,scope='Mathematical checks only, no measured birefringence; fixed Ricci-flat background; weak-field straight paths only for Earth/Sun.')
(P/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in results.items() if k!='check_names'},indent=2))
