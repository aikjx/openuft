"""Independent SymPy symbolic calculations; limited mathematics, not physical UV proof."""
from pathlib import Path
import json
import sympy as s
p=Path(__file__).resolve().parents[1]
R,omega,u,t=s.symbols('R omega u t',positive=True,real=True)
rad=s.Matrix([R*s.cos(omega*t),R*s.sin(omega*t),u*t]);v=rad.diff(t);acc=v.diff(t);jerk=acc.diff(t)
vnorm2=s.simplify(v.dot(v));cross=v.cross(acc)
kappa=s.simplify(s.sqrt(cross.dot(cross))/vnorm2**s.Rational(3,2))
tau=s.simplify(cross.dot(jerk)/cross.dot(cross))
assert s.simplify(kappa-R*omega**2/vnorm2)==0
assert s.simplify(tau-u*omega/vnorm2)==0
# Explicit 1D static scalar Lagrangian: L=F(chi) R0/2 - (chi')^2/2 - (m² chi²)/2 - lambda chi^4/4
x=s.symbols('x',real=True);chi=s.Function('chi')(x);M2,xi,m2,lam,R0=s.symbols('M2 xi m2 lam R0',real=True)
F=M2+xi*chi**2
L=F*R0/2-s.diff(chi,x)**2/2-m2*chi**2/2-lam*chi**4/4
eom=s.simplify(s.diff(L,chi)-s.diff(s.diff(L,s.diff(chi,x)),x))
expected=s.diff(chi,x,2)+xi*chi*R0-m2*chi-lam*chi**3
assert s.simplify(eom-expected)==0
# U1 gauge invariance dA: Fxy=dx Ay -dy Ax for any smooth chi
xx,yy=s.symbols('xx yy',real=True);Ax=s.Function('Ax')(xx,yy);Ay=s.Function('Ay')(xx,yy);gauge=s.Function('theta')(xx,yy)
Fab=s.diff(Ay,xx)-s.diff(Ax,yy)
Fg=s.diff(Ay+s.diff(gauge,yy),xx)-s.diff(Ax+s.diff(gauge,xx),yy)
assert s.simplify(Fg-Fab)==0
# Abelian KK one-form invariant under y'=y+k chi(x), A'=A - dchi
kk=s.symbols('k',nonzero=True);Ay0,dchi=s.symbols('Ay0 dchi')
assert s.simplify((kk*dchi+kk*(Ay0-dchi))-kk*Ay0)==0
report={'helix_v_squared':str(vnorm2),'curvature':str(kappa),'torsion':str(tau),
        'static_scalar_Euler_Lagrange':str(eom),'static_scalar_expected':str(expected),
        'abelian_gauge_field_strength_invariant':True,'KK_one_form_invariant':True,
        'scope':'selected symbolic identities only; not proof of unified physics','pass':True}
(p/'results/symbolic_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
