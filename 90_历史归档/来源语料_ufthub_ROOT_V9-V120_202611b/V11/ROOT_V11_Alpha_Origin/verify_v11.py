#!/usr/bin/env python3
"""ROOT V11: independent algebraic, numerical and identifiability audits.
Mathematical reparameterizations of measured alpha are NOT alpha predictions.
"""
from pathlib import Path
import json
import numpy as np
import mpmath as mp
import sympy as sp

OUT=Path(__file__).resolve().parent
mp.mp.dps=90
pi=mp.pi
alpha_inv_obs=mp.mpf('137.035999177')
alpha_inv_sigma=mp.mpf('0.000000021')
alpha=1/alpha_inv_obs
c=mp.mpf('299792458');h=mp.mpf('6.62607015e-34');e=mp.mpf('1.602176634e-19')
me=mp.mpf('9.1093837139e-31') # CODATA 2022 approximate center; see output note
hbar=h/(2*pi)
eps0=e*e/(4*pi*hbar*c*alpha)
mu0=1/(eps0*c*c)
Zvac=mu0*c
RK=h/(e*e)
rc=hbar/(me*c)
a0=rc/alpha
re=alpha*rc
Eelec_at_rc=alpha*me*c*c
Es=mp.mpf('1.602176634e-19')

# Exact symbolic identities with symbols independent (alpha relation must be supplied)
r,ee,eeps,hh,cc,mm=sp.symbols('r e eps h c m',positive=True)
hhb=hh/(2*sp.pi)
aa=ee**2/(4*sp.pi*eeps*hhb*cc)
Z=1/(eeps*cc);R=hh/ee**2
checks={
 'impedance':sp.simplify(aa-Z/(2*R)),
 'energy_ratio':sp.simplify(aa-(ee**2/(4*sp.pi*eeps*r))/(hhb*cc/r)),
 'compton_bohr':sp.simplify(aa-(hhb/(mm*cc))/(4*sp.pi*eeps*hhb**2/(mm*ee**2))),
 'classical_compton':sp.simplify(aa-(ee**2/(4*sp.pi*eeps*mm*cc**2))/(hhb/(mm*cc))),
}
assert all(val==0 for val in checks.values())

# Free abelian gauge vacuum action in 4D S = -1/(4g^2) int F^2;
# delta S -> 1/g² ∂F =0, does not select g.
g=sp.symbols('g',positive=True)
w0=sp.symbols('w0',positive=True)
gauge_factor=sp.simplify(g**2*(1/g**2)*w0-w0)
assert gauge_factor==0

# Helix continuum: angle s in (0,1), gives arbitrary kappa/tau, with v=c.
# Four model couplings differ but same normalized dispersion q²+kz²=k0².
rng=np.random.default_rng(20261031)
s=rng.uniform(1e-5,0.9999,50000)
k0=rng.uniform(1e-4,3e4,50000)
q=s*k0
kz=np.sqrt(1-s*s)*k0
dispersion_error=np.max(np.abs((q/k0)**2+(kz/k0)**2-1))
assert dispersion_error <1e-14
# fixed normalized wavelength, spatial helical ratios are free, not gauge-coupling selectors.
helix_a=rng.uniform(0.0001,0.9999,50000)
helix_b=np.sqrt(1-helix_a**2)
kap=helix_a
tau=helix_b
geom_err=np.max(np.abs(kap/tau-helix_a/helix_b))

# Post-hoc 2026 alpha candidates – compare shared asymptotic skeleton
A=4*pi**3+pi**2+pi
b1=mp.mpf(1)/24
b2=mp.mpf(3)/(8*pi**3)
c4=pi/12
P=lambda x:1-A*x+b1*x*x+b2*x**3-c4*x**4
quartic_root=mp.findroot(P,(mp.mpf('0.007'),mp.mpf('0.008')))
quartic_inv=1/quartic_root
# Shared backbone: y=A- b1/y -b2/y^2 +c4/y^3
quartic_newton_res=quartic_inv-(A-b1/quartic_inv-b2/quartic_inv**2+c4/quartic_inv**3)
assert abs(quartic_newton_res) < mp.mpf('1e-80')
# Li et al 2026 conditional infinite series as reported in V10
li_sum=mp.nsum(lambda k: (k+6)/(k+4) * A**(-2*k-1),[1,mp.inf])
li_inv=A-1/(24*A)-li_sum

# Sensitivity quartic coefficient b1. Root implicit function
# P(y)= y4 -A y3 + b1 y2+b2 y-c4, dy/db1= -y²/(4y³-3A y²+2b1 y+b2)
y=quartic_inv
slope_b1=-y*y/(4*y**3-3*A*y*y+2*b1*y+b2)
needed_db1=alpha_inv_sigma/abs(slope_b1)
# delta correction quadrature checking via finite differencing
D=mp.mpf('1e-7')
fun=lambda bv: 1/mp.findroot(lambda x:1-A*x+bv*x*x+b2*x**3-c4*x**4,(mp.mpf('0.007'),mp.mpf('0.008')))
fd=(fun(b1+D)-fun(b1-D))/(2*D)
assert abs((fd-slope_b1)/slope_b1)<mp.mpf('1e-9')

# Counterexample gauge coupling: all identical source-free plane waves
couplings=[mp.mpf('0.002'),mp.mpf('0.00729735256433'),mp.mpf('0.05'),mp.mpf('0.5')]
# S-dependent energy prefactor changes but vacuum equations don't.

# RG illustration 1 Dirac fermion, assumes arbitrary boundary alpha_ref at mu0 (not alpha(0)=alpha(m_e) physically).
mu_ratios=[mp.mpf('1'),mp.mpf('10'),mp.mpf('100')]
rg=[1/(1/alpha-(2/(3*pi))*mp.log(rt)) for rt in mu_ratios]

r0={
 'reference':{'alpha_inv':str(alpha_inv_obs),'uncertainty_alpha_inv':str(alpha_inv_sigma),'alpha':mp.nstr(alpha,30)},
 'three_faces':{
 'Zvac_ohm':mp.nstr(Zvac,30),'RK_ohm':mp.nstr(RK,30),
 'Zvac_div_2RK':mp.nstr(Zvac/(2*RK),30),
 're_m':mp.nstr(re,25), 'lambdaC_reduced_m':mp.nstr(rc,25),'a0_m':mp.nstr(a0,25),
 're_div_lambdaC':mp.nstr(re/rc,30),'lambdaC_div_a0':mp.nstr(rc/a0,30),
 'electrostatic_energy_at_lambdaC_eV':mp.nstr(Eelec_at_rc/Es,20)},
 'sympy_identities':{k:str(val) for k,val in checks.items()},
 'geometric_nonuniqueness':{'random_cases':len(s),'max_norm_dispersion_error':float(dispersion_error),'max_geom_ratio_error':float(geom_err), 'couplings_same_vacuum_equations':[str(z) for z in couplings]},
 'candidate_equations':{
 'A_pi':mp.nstr(A,60),'quartic_alpha':mp.nstr(quartic_root,60), 'quartic_alpha_inv':mp.nstr(quartic_inv,60),
 'quartic_inverse_difference_CODATA':mp.nstr(quartic_inv-alpha_inv_obs,30),
 'quartic_sigma_difference':mp.nstr((quartic_inv-alpha_inv_obs)/alpha_inv_sigma,22),
 'li_alpha_inv':mp.nstr(li_inv,60),
 'li_sigma_difference':mp.nstr((li_inv-alpha_inv_obs)/alpha_inv_sigma,22),
 'two_candidates_sigma_separation':mp.nstr((quartic_inv-li_inv)/alpha_inv_sigma,22),
 'quartic_implicit_reciprocal_residual':mp.nstr(quartic_newton_res,4),
 'quartic_d_inv_db1':mp.nstr(slope_b1,24),
 'delta_b1_for_one_sigma':mp.nstr(needed_db1,24),
 'relative_change_b1_for_one_sigma':mp.nstr(needed_db1/b1,24),
 'finite_difference_derivative_check':mp.nstr(fd,24)
 },
 'one_loop_rg_demo':{'model':'one Dirac fermion, simple MS-like running with alpha(mu0)=CODATA for algebra only, NOT a precision physical running prediction','mu_ratio':[str(z) for z in mu_ratios],'alpha_mu':[mp.nstr(z,20) for z in rg]}
}
(OUT/'results.json').write_text(json.dumps(r0,indent=2,ensure_ascii=False),encoding='utf-8')
for key,val in r0.items():print(key, json.dumps(val,ensure_ascii=False)[:1600])
print('ALL CHECKS PASSED')

# Make distinct separate plots without manually selecting colors or seaborn.
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.family']='DejaVu Sans'
fig,ax=plt.subplots(figsize=(9,5))
# For an arbitrary q, geometry has normalized unconstrained continuum
angles=np.linspace(0.0001,0.3,1000)
ax.plot(angles, np.tan(angles),label='helix curvature/torsion ratio = tan(theta)')
ax.axhline(float(alpha),linestyle='--',label='observed alpha (reference only)')
ax.set_xlabel('helix angle theta (radians)');ax.set_ylabel('dimensionless ratio');ax.set_title('Infinitely many equally valid helix ratios')
ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(OUT/'geometry_continuum.png',dpi=160);plt.close(fig)

fig,ax=plt.subplots(figsize=(9,5))
labels=['4pi^3+pi^2+pi','2026 conditional series','2026 quartic model']
yd=[(A-alpha_inv_obs)/alpha_inv_sigma, (li_inv-alpha_inv_obs)/alpha_inv_sigma,(quartic_inv-alpha_inv_obs)/alpha_inv_sigma]
# symlog shows differences across >1e5 span
ax.bar(labels,[float(v) for v in yd])
ax.set_yscale('symlog',linthresh=.1)
ax.axhline(1,linestyle='--',linewidth=1,label='+1 sigma')
ax.axhline(-1,linestyle='--',linewidth=1,label='-1 sigma')
ax.set_ylabel('deviation from CODATA 2022 in sigma (symmetric log scale)')
ax.set_title('Numerical agreement does not establish physical derivation');ax.tick_params(axis='x',labelrotation=8)
ax.legend();fig.tight_layout();fig.savefig(OUT/'candidate_sigma.png',dpi=160);plt.close(fig)
