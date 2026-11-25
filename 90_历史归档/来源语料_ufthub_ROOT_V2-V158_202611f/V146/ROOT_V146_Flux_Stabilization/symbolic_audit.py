#!/usr/bin/env python3
"""Optional exact SymPy audit. Does not set hbar or G to one."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
try:
    import sympy as s
except ImportError:
    print('SymPy not installed: optional exact audit skipped; main 78 tests need no packages')
    raise SystemExit(0)

A,B,C,y,R,K4 = s.symbols('A B C y R K4',positive=True)
K,Lam,chi,n,R0 = s.symbols('K Lam chi n R0',positive=True)
V=A/y-B/y**2+C/y**3
checks={}
checks['dV_dy']=s.simplify(s.diff(V,y)-(-A*y*y+2*B*y-3*C)/y**4)==0
ym=B/(2*A)
checks['Minkowski_stationarity_at_B2eq4AC']=s.simplify(s.diff(V,y).subs(y,ym).subs(C,B**2/(4*A)))==0
checks['Minkowski_vacuum_at_B2eq4AC']=s.simplify(V.subs(y,ym).subs(C,B**2/(4*A)))==0
Rflat_sq=chi*n*n/(4*K)
lam_flat=2*K*K/(chi*n*n)
external=-K/R**2+Lam+chi*n*n/(8*R**4)
internal=Lam-chi*n*n/(8*R**4)
checks['six_dimensional_external_Einstein_eq']=s.simplify(external.subs(R**2,Rflat_sq).subs(Lam,lam_flat))==0
checks['six_dimensional_internal_Einstein_eq']=s.simplify(internal.subs(R**2,Rflat_sq).subs(Lam,lam_flat))==0
v3=(R**2-1)**2/R**6
checks['factorized_n3_potential']=s.simplify(v3-(R**-2-2*R**-4+R**-6))==0
checks['n3_minimum']=s.simplify(s.diff(v3,R).subs(R,1))==0
checks['n3_mass2_K4eq2']=s.simplify(s.diff(v3,R,2).subs(R,1)/(4*2))==1
out='\n'.join(f'{k}: {"PASS" if v else "FAIL"}' for k,v in checks.items())+'\n'
(ROOT/'results'/'symbolic_audit.txt').write_text(out,encoding='utf-8')
print(out)
if not all(checks.values()): raise SystemExit(1)
