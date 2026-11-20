#!/usr/bin/env python3
"""Reproducible symbolic and high-precision checks for a 6D Einstein-Maxwell sphere-flux toy model.
Normalization: c=hbar=1, S=integral sqrt(-G)[(M6^4/2)(R6-2Lambda6)-F^2/(4*g6^2)],
flux integral F=2*pi*N; alpha4=g6^2/(16*pi^2*r^2)."""
import sympy as s
import mpmath as mp
import json, csv
from pathlib import Path
OUT=Path(__file__).parent
mp.mp.dps=70
pi=s.pi
M,g,r,r0,La,N=s.symbols('M g r r0 La N', positive=True, finite=True)
xi, x=s.symbols('xi x', positive=True)
rs=N/(2*g*M**2)
Las=2*g**2*M**4/N**2
Ext=M**4*(La-1/r**2)+N**2/(8*g**2*r**4)
Int=M**4*La-N**2/(8*g**2*r**4)
checks={}
def check(name,expr):
  res=s.simplify(s.factor(expr)); checks[name]={'pass':res==0,'residual':str(res)}
  assert res==0, f'{name}: {res}'
check('six_dimensional_external_equation', Ext.subs({r:rs,La:Las}))
check('six_dimensional_internal_equation', Int.subs({r:rs,La:Las}))
check('flux_quantization',4*pi*N/2-2*pi*N) # integral Ftheta_phi dtheta dphi = 4pi*N/2
alpha_from_radius=g**2/(16*pi**2*r**2)
alpha_on_shell=g**4*M**4/(4*pi**2*N**2)
check('4d_gauge_coupling',alpha_from_radius.subs(r,rs)-alpha_on_shell)
check('dimensionless_xi',alpha_on_shell - (g**2*M**2)**2/(4*pi**2*N**2))
M4sq=4*pi*M**4*r**2
GN=1/(8*pi*M4sq)
check('on_shell_radius_from_4d_newton', (r**2/GN).subs(r,rs)-N**2/(2*alpha_on_shell))
# Einstein-frame radion potential; phi=2*M4*ln(r/r0), M4^2=4*pi*M^4*r0^2
VE=4*pi*(r0/r)**4*(-M**4+M**4*La*r**2+N**2/(8*g**2*r**2))
subvac={La:1/(2*r0**2), N**2/(8*g**2):M**4*r0**2/2}
# direct replacement uses N^2 and g terms handled via q symbol for exact on-shell potential
Q=s.symbols('Q',positive=True)
VEQ=4*pi*(r0/r)**4*(-M**4+M**4*La*r**2+Q/r**2)
VEvac=s.factor(VEQ.subs({La:1/(2*r0**2),Q:M**4*r0**2/2}))
Vexpected=2*pi*M**4*(r0/r)**4*(r/r0-r0/r)**2
check('radion_potential_positive_factorization',VEvac-Vexpected)
check('radion_stationary', s.diff(VEvac,r).subs(r,r0))
check('radion_zero_vacuum_energy',VEvac.subs(r,r0))
check('radion_mass_sqr_equals_1_over_radius_sqr',
 (r0**2/(4*(4*pi*M**4*r0**2)))*s.diff(VEvac,r,2).subs(r,r0)-1/r0**2)
X=s.symbols('X',positive=True)
U=s.factor((VEvac/(4*pi*M**4)).subs(r,X*r0))
check('universal_potential', U-(X**2-1)**2/(2*X**6))
check('barrier_stationary_at_sqrt3',s.diff(U,X).subs(X,s.sqrt(3)))
check('barrier_height',U.subs(X,s.sqrt(3))-s.Rational(2,27))
# 2-torus: R2=0 and flux nonzero, external/internal Einstein eq demand opposite Lambda
Qdens=s.symbols('Qdens',positive=True)
La_t=s.symbols('La_t',real=True)
Et_ext=M**4*La_t+Qdens
Et_int=M**4*La_t-Qdens
check('torus_no_Mink_solution_flux_nonzero',Et_ext-Et_int-2*Qdens)
# numeric (not fit predictions): CODATA alpha is used ONLY for a posteriori comparison
alpha_inv=mp.mpf('137.035999177')
alpha_exp=1/alpha_inv
Gsi=mp.mpf('6.67430e-11'); hbar=mp.mpf('1.054571817646156391262428003302280744722826178529e-34'); c=mp.mpf('299792458')
lp=mp.sqrt(Gsi*hbar/c**3)
GeV_J=mp.mpf('1.602176634e-10')
rows=[]
for n in (1,2,3,4,10,30,100):
 n=mp.mpf(n)
 xi_fit=2*mp.pi*n*mp.sqrt(alpha_exp)
 rr_lp=n/mp.sqrt(2*alpha_exp)
 r_m=rr_lp*lp
 M6r=mp.sqrt(n)/(mp.power(64*mp.pi**2*alpha_exp,mp.mpf('0.25')))
 KK_eV=hbar*c/r_m/mp.mpf('1.602176634e-19')
 rows.append({"N":int(n),"xi_required_by_measured_alpha":mp.nstr(xi_fit,22),
              "radius_in_planck_lengths_if_fitted":mp.nstr(rr_lp,22),
              "radius_m_if_fitted":mp.nstr(r_m,22),
              "M6_r_if_fitted":mp.nstr(M6r,22),
              "KK_mass_GeV_if_fitted":mp.nstr(KK_eV/mp.mpf('1e9'),22),
              "radion_mass_GeV_if_fitted":mp.nstr(KK_eV/mp.mpf('1e9'),22)})
with (OUT/'flux_sweep.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
# independent xi values for SAME fixed N but different microscopic 6d coupling theories
nonuniqueness=[]
for n in (1,3):
 for k in ('0.5','1.0','1.5','2.0'):
  xi_v=mp.mpf(k); av=xi_v**2/(4*mp.pi**2*n**2)
  nonuniqueness.append({'N':n,'xi':k,'alpha':mp.nstr(av,24),'alpha_inverse':mp.nstr(1/av,24)})
# compare symbolic potential at random points via 70 digit mpmath
R0=mp.mpf('1.37');Mnum=mp.mpf('0.83');num_res=[]
for i in range(500):
 xx=mp.mpf('0.4')+mp.mpf(i+1)/mp.mpf(160)
 A=4*mp.pi*(R0/(xx*R0))**4*(-Mnum**4+Mnum**4/(2*R0**2)*(xx*R0)**2+Mnum**4*R0**2/(2*(xx*R0)**2))
 B=2*mp.pi*Mnum**4*(R0/(xx*R0))**4*(xx-1/xx)**2
 num_res.append(abs(A-B)/(1+abs(B)))
res={'description':'6D Einstein-Maxwell sphere compactification: derivations, limitations, checks',
     'model':'Minkowski4 x S2 with fixed flux N, independent 6d U(1) gauge field, positive cosmological constant tuned to Minkowski',
     'symbolic_checks':checks,
     'CODATA_alpha_inv_input_only_for_comparison':mp.nstr(alpha_inv,18),
     'CODATA_alpha_input_only_for_comparison':mp.nstr(alpha_exp,22),
     'planck_length_m_approx':mp.nstr(lp,20),
     'geometry_flux_sweep_using_alpha_as_fit':rows,
     'fixed_topology_free_coupling_counterexamples':nonuniqueness,
     'random_numeric_potential_checks_n':len(num_res),
     'max_relative_potential_factorization_residual':mp.nstr(max(num_res),20),
     'radion_u_normalized':'(x^2-1)^2/(2*x^6)',
     'barrier_radius_over_r0':'sqrt(3)', 'barrier_U':'2/27',
     'conclusion':'No parameter-free prediction of alpha: xi=g6^2 M6^2 remains continuous; N integer alone insufficient; 4d flat vacuum requires positive tuned 6d cosmological constant; pure gravity cannot supply independent gauge field.'}
(OUT/'results.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf8')
log=['ROOT V15 - model checks','Symbolic tests:']
log += [f'{k}: {"PASS" if v["pass"] else "FAIL"}' for k,v in checks.items()]
log += [f'Numeric potential checks: {len(num_res)}',f'Max rel residual: {mp.nstr(max(num_res),20)}', f'alpha_exp (comparison only): {mp.nstr(alpha_exp,20)}', 'Sample sweep N=3: '+str(rows[2]), 'No alpha first-principles prediction.']
(OUT/'run_log.txt').write_text('\n'.join(log)+'\n',encoding='utf8')
# plot functions using plain matplotlib no selected colors
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
xx=np.linspace(0.65,4.2,600)
y=(xx**2-1)**2/(2*xx**6)
plt.figure(figsize=(9,5.2));plt.plot(xx,y,label='6D flux compactification radion potential')
plt.axvline(1,linestyle='--',label='Stable radius r / r* = 1')
plt.axvline(np.sqrt(3),linestyle=':',label='Barrier at sqrt(3)')
plt.ylim(0,0.55);plt.xlim(0.65,4.2);plt.xlabel('r / r*');plt.ylabel('V_E /(4 pi M6^4)');plt.title('ROOT V15 | Sphere flux radion potential (Minkowski tuned)');plt.grid(alpha=.25);plt.legend();plt.tight_layout();plt.savefig(OUT/'radion_potential.png',dpi=170);plt.close()
ns=np.arange(1,51)
for kval in [0.5,1.0,1.5,2.0]:
 vals=np.array([float((mp.mpf(str(kval))**2/(4*mp.pi**2*int(n)**2))) for n in ns])
 plt.plot(ns,vals,label=f'xi={kval}')
plt.yscale('log');plt.xlabel('Integer flux N');plt.ylabel('4D alpha predicted conditional on xi');plt.title('Flux discreteness does not fix gauge coupling')
plt.legend();plt.grid(alpha=.25);plt.tight_layout();plt.savefig(OUT/'coupling_families.png',dpi=170);plt.close()
print('\n'.join(log))
