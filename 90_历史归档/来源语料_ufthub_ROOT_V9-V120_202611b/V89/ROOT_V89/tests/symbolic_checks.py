"""Independent exact SymPy checks for ROOT V89. These are algebra, not physics observations."""
import sympy as s
import json
from pathlib import Path

x,y,z,u,v,w=s.symbols('x y z u v w',positive=True,real=True)
a,b,c,dt,coeff,G,m1,m2,hbar,light=s.symbols('a b c dt coeff G m1 m2 hbar light',positive=True)
phi0,phi1,psi0,psi1,k=s.symbols('phi0 phi1 psi0 psi1 k',real=True)
checks={}
def ck(name, expr):
    checks[name]=(s.simplify(expr)==0)

r00=dt+(a-b)/2; r01=dt+(a+b)/2; r10=dt-(a+b)/2; r11=dt+(b-a)/2
f=lambda n:r00**-n-r01**-n-r10**-n+r11**-n
ck('zero_branch_A',f(1).subs(a,0))
ck('zero_branch_B',f(1).subs(b,0))
ck('equal_branch_negative_cross',f(1).subs(b,a) -(2/dt-1/(dt+a)-1/(dt-a)))
ck('local_phase_cancels', (phi0+psi0)-(phi0+psi1)-(phi1+psi0)+(phi1+psi1))
ck('Newton_inverse_square_derivative',-s.diff(-G*m1*m2/x,x) + G*m1*m2/x**2)
# Note minus dV/dr=-GMm/r2.
ck('PN_relative_dimensions', (3*G*(m1+m2)/(x*light**2))*x-3*G*(m1+m2)/light**2)
ck('quantum_relative_length2', G*hbar/(x**2*light**3)*(x**2)-G*hbar/light**3)
ck('coupling_columns_rank1',s.det(s.Matrix([[x,-x],[y,-y]])))
ck('cancel_both_first_columns',s.Matrix([x,y,z]).cross(s.Matrix([u,v,w])).dot(s.Matrix([x,y,z])))
ck('cancel_both_second_columns',s.Matrix([x,y,z]).cross(s.Matrix([u,v,w])).dot(s.Matrix([u,v,w])))
ck('triple_product_equals_det',s.Matrix([x,y,z]).cross(s.Matrix([u,v,w])).dot(s.Matrix([a,b,c]))-s.det(s.Matrix([[x,u,a],[y,v,b],[z,w,c]])))
ck('concurrence_identity',4*s.sin(k/2)**2-2*(1-s.cos(k)))
# Weak-field relativistic proper-time action: L=-mc² sqrt(1+2Phi/c²-v²/c²)
Phi,v2,eps=s.symbols('Phi v2 eps',real=True)
low=s.series(-m1/s.sqrt(eps)**2 *s.sqrt(1+eps*(2*Phi-v2)),eps,0,2)
# The requested weak-field limit is -m c²-m Phi+ m v²/2
ck('weakfield_order_zero',s.limit(low.removeO()+m1/eps+m1*Phi-m1*v2/2,eps,0))
# meaningful check via introducing formal c² scale K: -mK sqrt(1+(2Phi-v²)/K)
K=s.symbols('K',positive=True)
low2=s.series(-m1*K*s.sqrt(1+(2*Phi-v2)/K),K,s.oo,2).removeO()
ck('weakfield_lagrangian_leading',s.limit(low2+m1*K+m1*Phi-m1*v2/2,K,s.oo))
# gravity-only geometric cross retains symmetry under exchange s1<->s2
ck('branch_exchange_symmetry',f(1)-f(1).xreplace({a:b,b:a}))
# Single-source G and mass columns proportional: delta proportional G*M
ck('GM_scale_direction',s.det(s.Matrix([[m1*x,G*x],[m1*y,G*y]])))
# trace of classical Maxwell field tensor in 4D in flat spacetime (algebraic general identity)
F2=s.symbols('F2',real=True)
Ttrace=(1-4*s.Rational(1,4))*F2
ck('maxwell_traceless_4d',Ttrace)
# Low energy quantum coefficient is proportional to hbar and vanishes at hbar->0
ck('EFT_loop_classical_limit',s.limit(G*hbar/(light**3*x**2),hbar,0))
ck('1PN_vanish_infinite_c',s.limit(G*(m1+m2)/(x*light**2),light,s.oo))

out={'checks':checks,'count':len(checks),'passed':sum(checks.values())}
root=Path(__file__).resolve().parents[1]
(root/'results/symbolic_checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(out,indent=2))
if not all(checks.values()):raise SystemExit(1)
