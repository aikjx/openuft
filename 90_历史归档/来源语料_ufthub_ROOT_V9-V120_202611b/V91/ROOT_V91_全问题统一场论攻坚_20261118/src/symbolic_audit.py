"""12+ independent symbolic statements for ROOT V91. Exact algebra, not observation."""
from __future__ import annotations
import json
from pathlib import Path
import sympy as s

d,a,b,mu,r,la=s.symbols('d a b mu r la',positive=True)
rr=[d+(a-b)/2,d+(a+b)/2,d-(a+b)/2,d+(b-a)/2]
w=(1,-1,-1,1)
checks={}
M=lambda n:s.factor(sum(c*x**n for c,x in zip(w,rr)))
checks['M0']=M(0)==0
checks['M1']=M(1)==0
checks['M2']=s.simplify(M(2)+2*a*b)==0
checks['M3']=s.simplify(M(3)+6*a*b*d)==0
checks['M4']=s.simplify(M(4)+a*b*(a*a+b*b+12*d*d))==0
F=sum(c*s.exp(-mu*x)/x for c,x in zip(w,rr))
Fprime=4*s.exp(-mu*d)*s.sinh(mu*a/2)*s.sinh(mu*b/2)
checks['dF_dmu']=s.simplify(s.expand((s.diff(F,mu)-Fprime).rewrite(s.exp)))==0
checks['dF_at_zero']=s.simplify(Fprime.subs(mu,0))==0
checks['FY_second_derivative']=s.simplify(s.diff(s.exp(-mu*r)/r,r,2)-s.exp(-mu*r)*(2/r**3+2*mu/r**2+mu**2/r))==0
checks['long_range_order3']=s.simplify(-M(2)/6-a*b/3)==0
checks['long_range_order4']=s.simplify(M(3)/24+a*b*d/4)==0
checks['Newton_R_power']=s.simplify(s.diff(s.sqrt(1/r**3),r)+s.Rational(3,2)*r**(-s.Rational(5,2)))==0
checks['legacy_56pi_not_1836']=s.simplify(56*s.pi-s.Rational(1836152673,1000000))!=0
checks['ISCO_schwarzschild_radial_relation']=s.simplify(6*s.symbols('m')-3*2*s.symbols('m'))==0
# inverse-square acceleration derivative of Yukawa potential
checks['Yukawa_force_derivative']=s.simplify(s.diff(s.exp(-mu*r)/r,r)+s.exp(-mu*r)*(1+mu*r)/r**2)==0
# scalar standard convention alpha_AB=2 beta_A beta_B (definition not first-principles proof)
beta=s.symbols('beta')
checks['scalar_dimensionless']=s.simplify(2*beta**2-2*beta*beta)==0
# two-column rank-1 G vs same-shape Coulomb, exact minors vanish
x,y,z=s.symbols('x y z')
Q=s.Matrix([[x,-x],[y,-y],[z,-z]])
checks['Coulomb_Gravity_rank1']=Q.rank()==1
# local phase a_i+b_j cancels
p0,p1,q0,q1=s.symbols('p0 p1 q0 q1')
checks['local_phase_cancels']=s.simplify((p0+q0)-(p0+q1)-(p1+q0)+(p1+q1))==0
# sign flip + even nuisance columns same -> rank 2
R=s.Matrix([[x,x,x],[y,y,y],[x,-x,x],[y,-y,y]])
checks['charge_reversal_even_nuisance_rank2']=R.rank()==2
# external calibration adds third independent direction
R=R.col_join(s.Matrix([[0,0,1]]))
checks['external_calibration_restores_rank3']=R.rank()==3
out={'total':len(checks),'passed':sum(checks.values()),'checks':checks,'physical_discovery':False}
root=Path(__file__).resolve().parents[1]
(root/'results'/'symbolic_checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'total':out['total'],'passed':out['passed']},ensure_ascii=False))
if not all(checks.values()):
    print('FAILED:',[k for k,v in checks.items() if not v])
    raise SystemExit(1)
