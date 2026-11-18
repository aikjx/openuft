"""Exact symbolic checks for reduced toy Lagrangian variations, not full GR tensor variation."""
import json
from pathlib import Path
import sympy as sp
R=Path(__file__).resolve().parents[1]
t,x=sp.symbols('t x',real=True)
m,g=sp.symbols('m g',real=True)
phi=sp.Function('phi')(t,x)
Q=sp.Function('Q')(t,x)
L=sp.Rational(1,2)*sp.diff(phi,t)**2-sp.Rational(1,2)*sp.diff(phi,x)**2-sp.Rational(1,2)*m*m*phi**2-sp.Rational(1,4)*g*phi*Q
EL=sp.diff(L,phi)-sp.diff(sp.diff(L,sp.diff(phi,t)),t)-sp.diff(sp.diff(L,sp.diff(phi,x)),x)
expected=-sp.diff(phi,t,2)+sp.diff(phi,x,2)-m*m*phi-sp.Rational(1,4)*g*Q
assert sp.simplify(EL-expected)==0
# U(1) gauge symmetry as exact equality of antisymmetric tensor in 1+1 dimensions
A0=sp.Function('A0')(t,x);A1=sp.Function('A1')(t,x);lam=sp.Function('lambda')(t,x)
F01=sp.diff(A1,t)-sp.diff(A0,x)
F01_g=sp.diff(A1+sp.diff(lam,x),t)-sp.diff(A0+sp.diff(lam,t),x)
assert sp.simplify(F01_g-F01)==0
report={'reduced_chi_EL':str(EL),'expected_chi_EL':str(expected),'EL_identity':True,
        'Abelian_gauge_transformation_exact':True,
        'scope':'Reduced scalar toy with prescribed FtildeF source Q; does not prove full Einstein or unified force origin.'}
(R/'results'/'symbolic_variation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
