"""ROOT V147: exact algebra and numerical model diagnostics; no experimental refit."""
from fractions import Fraction as F
from decimal import Decimal, localcontext
from pathlib import Path
import csv,json,math,random
P=Path(__file__).resolve().parent
counts={}
def check(group,cond):
    if not cond: raise AssertionError(group)
    counts[group]=counts.get(group,0)+1
# Exact tests: positive bulk mass adds to KK energy squared. Values are scaled by KK mass squared.
for n in range(1,101):
    for bulk2 in (F(0),F(1,100),F(1),F(100)):
        mass2=bulk2+n*n
        check('KK mass inequality',mass2>=n*n)
        check('KK mass equality iff bulk mass zero',(mass2==n*n)==(bulk2==0))
# Linear scalar tensor response: coefficients of G_* M/r in time/spatial potentials.
for a in (F(0),F(1,100),F(1,3),F(1)):
    gamma=(1-a)/(1+a)
    check('metric ratio identity',1-gamma==2*a/(1+a))
check('massless radion PPN gamma',(1-F(1,3))/(1+F(1,3))==F(1,2))
check('massless radion Newton coupling',1+F(1,3)==F(4,3))
# Two-term stabilization V=A/phi+B/phi^6. At any positive stationary radius
# B=-A*phi^5/6; V=5A/(6phi), V''=-5A/phi^3. No nontrivial stationary Minkowski.
for j in range(1,41):
    x=F(j,7)
    for A in (F(-2),F(0),F(3)):
        B=-A*x**5/6
        V=A/x+B/x**6
        dV=-A/x**2-6*B/x**7
        ddV=2*A/x**3+42*B/x**8
        check('potential stationary',dV==0)
        check('potential value',V==5*A/(6*x))
        check('potential Hessian',ddV==-5*A/x**3)
        check('Minkowski forces zero coefficients',(V==0)==(A==0 and B==0))
# Four-point double-copy algebra. Arbitrary Jacobi-compatible rational numerators are algebra
# test vectors, not evaluated Yang-Mills amplitudes. All momenta convention: s+t+u=0.
rng=random.Random(147)
for _ in range(500):
    s=F(rng.randint(2,100)); t=-s*F(rng.randint(1,99),100); u=-s-t
    d=(s,t,u)
    a,b,c,e=[F(rng.randint(-50,50),7) for _ in range(4)]
    n=(a,b,-a-b); nt=(c,e,-c-e)
    chi=F(rng.randint(-10,10),11); psi=F(rng.randint(-10,10),13)
    nn=tuple(x+chi*y for x,y in zip(n,d)); tt=tuple(x+psi*y for x,y in zip(nt,d))
    amp=lambda x,y:sum((i*j/k for i,j,k in zip(x,y,d)),F(0))
    check('Jacobi under shift',sum(nn)==sum(tt)==0)
    check('double-copy first shift',amp(nn,nt)==amp(n,nt))
    check('double-copy both shifts',amp(nn,tt)==amp(n,nt))
# Real reference values. SI for numerical conversion ONLY; theory c=1, hbar retained.
with localcontext() as ctx:
    ctx.prec=60
    D=Decimal
    pi=D('3.14159265358979323846264338327950288419716939937510582097494')
    c=D('299792458'); h=D('6.62607015e-34'); hb=h/(2*pi)
    G=D('6.67430e-11'); me=D('9.1093837139e-31'); alpha=D('7.2973525643e-3'); ev=D('1.602176634e-19')
    ag=G*me*me/(hb*c); ratio=(alpha/(4*ag)).sqrt(); MP=(hb*c/G).sqrt()
    mass=alpha.sqrt()/2*MP; R=hb/(mass*c)
    Gstar=G*3/4; agstar=Gstar*me*me/(hb*c)
    values={'alpha_G_e_using_GN':str(ag),'KK_min_mass_GeV_Gstar_equal_GN':str(mass*c*c/ev/D(10)**9), 'KK_min_mass_to_electron':str(ratio),'KK_min_mass_squared_ratio':str(ratio**2),'KK_radius_m':str(R),'KK_mass_ratio_if_massless_radion_Gstar_3GN_over_4':str((alpha/(4*agstar)).sqrt()), 'G_required_SI':str(alpha*hb*c/(4*me*me))}
    check('SI inverse formula',abs(D(values['G_required_SI'])/G-ratio**2)/ratio**2<D('1e-58'))
# Diagnostic not a Cassini refit. A massive scalar has position-dependent metric ratio, not constant PPN gamma.
with (P/'radion_screening.csv').open('w',newline='') as f:
    w=csv.writer(f); w.writerow(['r_over_range','scalar_to_tensor_potential','gamma_local_ratio','one_minus_gamma'])
    for x in (0,.01,.1,1,2,5,8,9,10,12,15,20,30,50):
        a=math.exp(-x)/3; delta=2*a/(1+a)
        w.writerow([x,a,1-delta,delta]); check('massive diagnostic range',0<=delta<=.5)
# Published Cassini central and standard uncertainty. No raw tracking data.
values.update({'Cassini_gamma_minus_one':2.1e-5,'Cassini_sigma':2.3e-5,'massless_radion_gamma':.5,'massless_radion_discrepancy_over_reported_sigma':(.5+2.1e-5)/2.3e-5})
(P/'results.json').write_text(json.dumps({'checks':counts,'total':sum(counts.values()),'values':values,'limitations':'Exact algebra, reference constant calculation, model diagnostics; not raw data reanalysis or unified theory proof.'},indent=2),encoding='utf-8')
print(json.dumps({'checks':counts,'total':sum(counts.values()),'values':values},indent=2))
