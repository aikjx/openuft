#!/usr/bin/env python3
"""Optional SymPy independent symbolic checks; not required by run_all.py."""
import sympy as s
R,y,A,B,C,K4,d,n,kappa,chi,lam=s.symbols('R y A B C K4 d n kappa chi lam', positive=True)
V=A/R**2-B/R**4+C/R**6
V_y=A/y-B/y**2+C/y**3
D=B**2-3*A*C
ystar=(B-s.sqrt(D))/A
checks={}
checks['dV/dR'] = s.simplify(s.diff(V,R)-(-2*A/R**3+4*B/R**5-6*C/R**7))
checks['dV/dy'] = s.simplify(s.diff(V_y,y)-(-A*y**2+2*B*y-3*C)/y**4)
checks['root_polynomial']=s.simplify((A*ystar**2-2*B*ystar+3*C).subs(C,(B**2-d**2)/(3*A)).subs(s.sqrt(D),d))
checks['mass2_min']=s.simplify((s.diff(V,R,2)*R**2/(4*K4) - 2*s.sqrt(D)/(K4*R**4)).subs(R,s.sqrt(ystar)).subs(C,(B**2-d**2)/(3*A)).subs(s.sqrt(D),d))
checks['dy/dC']=s.simplify(s.diff(ystar,C)-s.Rational(3,2)/s.sqrt(D))
checks['dR/dC']=s.simplify(s.diff(s.sqrt(ystar),C)-s.Rational(3,4)/(s.sqrt(ystar)*s.sqrt(D)))
checks['n_reflection']=s.simplify((chi*n*n/R**6)-(chi*(-n)**2/R**6))
checks['n3_factorized']=s.simplify(V.subs({A:1,B:2,C:1})-(R*R-1)**2/R**6)
checks['n3_barrier']=s.simplify(V.subs({A:1,B:2,C:1,R:s.sqrt(3)})-s.Rational(4,27))
checks['flat_tuning_condition']=s.simplify((B*B-4*A*C).subs(C,B*B/(4*A)))
checks['Minkowski_radius_formula']=s.simplify(V_y.subs(y,B/(2*A)).subs(C,B*B/(4*A)))
checks['KK_scalar_laplacian_ell0']=s.simplify((0*(0+1))/R**2)
failed={k:s.simplify(v) for k,v in checks.items() if s.simplify(v)!=0}
for k,v in checks.items(): print(f'{k}: {"PASS" if k not in failed else f"FAIL: {v}"}')
print(f'{len(checks)-len(failed)}/{len(checks)} symbolic checks passed')
raise SystemExit(1 if failed else 0)
