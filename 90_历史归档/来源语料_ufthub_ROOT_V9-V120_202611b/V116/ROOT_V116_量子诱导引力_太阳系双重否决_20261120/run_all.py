"""Recompute V116 constants, hypotheses and plots. Run from any current directory."""
import sys, json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from src import core as c
FIG=ROOT/'figures'; FIG.mkdir(exist_ok=True)
RESULT=ROOT/'results';RESULT.mkdir(exist_ok=True)
summary=c.summary()
(RESULT/'V116_SUMMARY.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
xs=np.logspace(-9,42,1000)
plt.figure(figsize=(9,5))
plt.semilogx(xs,[c.gamma_massless(float(x),1.) for x in xs],label='massless induced scalar: gamma(xi)')
plt.axhline(c.cassini_min_gamma(),ls='--',label='Cassini lower 2-sigma reference')
plt.axvline(c.xi_cassini_pure_massless_bound(),ls=':',label='max xi in this model')
plt.axvline(c.xi_eh_match(),ls='-.',label='xi from QCD scale (EH coefficient only)')
plt.ylim(.46,1.02);plt.xlabel('xi (dimensionless)');plt.ylabel('PPN gamma')
plt.title('Induced gravity: scale match versus Cassini constraint');plt.legend();plt.grid(alpha=.2);plt.tight_layout()
plt.savefig(FIG/'01_ppn_nogo.png',dpi=160);plt.close()
vals=np.logspace(-4,4,800)
plt.figure(figsize=(8,5))
plt.semilogx(vals,[c.gamma_radius(1/3,float(x)) for x in vals],label='local metric potential ratio')
plt.semilogx(vals,[c.gamma_fit_orbit_calibrated(1/3,float(x)) for x in vals],label='light deflection calibrated by orbit at r')
plt.axhline(c.cassini_min_gamma(),ls='--',label='Cassini reference (not a mass limit)')
plt.xlabel('r / lambda');plt.ylabel('gamma-like ratio');plt.title('Finite-range scalar: observation calibration matters')
plt.grid(alpha=.2);plt.legend();plt.tight_layout();plt.savefig(FIG/'02_finite_range_observer.png',dpi=160);plt.close()
vs=np.logspace(-3,20,400)
plt.figure(figsize=(8,5))
plt.loglog(vs,[(c.Mplbar_observed()/v)**2 for v in vs],label='xi for EH coefficient alone')
plt.axhline(c.xi_cassini_pure_massless_bound(),ls='--',label='max massless xi')
plt.axvline(c.lambda_one_loop(),ls=':',label='QCD one-loop exemplar')
plt.xlabel('hypothesized scalar VEV v (GeV)');plt.ylabel('xi')
plt.title('Scale hierarchy and PPN compatibility');plt.grid(alpha=.2);plt.legend();plt.tight_layout()
plt.savefig(FIG/'03_scale_coupling.png',dpi=160);plt.close()
coefs=np.logspace(-8,41,400)
plt.figure(figsize=(8,5))
plt.loglog(coefs,[min(x/c.xi_eh_match(),1) for x in coefs],label='formal induced fraction if fixed F=Mpl^2')
plt.axvline(c.conservative_bare_plus_induced_xi_bound(),ls='--',label='max xi (Cassini + bare EH)')
plt.axhline(c.max_induced_fraction_bound(),ls=':',label='maximum conservative induced fraction')
plt.xlabel('xi');plt.ylabel('xi v^2 / F');plt.title('Bare gravity term: scalar fraction constrained')
plt.grid(alpha=.2);plt.legend();plt.tight_layout();plt.savefig(FIG/'04_fraction_bound.png',dpi=160);plt.close()
print(json.dumps({'v_GeV':summary['v_QCD_one_loop_GeV'],
                  'xi_EH_only':summary['naive_xi_from_EH_coefficient'],
                  'xi_corrected':summary['xi_match_correcting_GN_light_scalar'],
                  'gamma_long_range':summary['gamma_long_range'],
                  'xi_cassini_max':summary['cassini_two_sigma_xi_max_pure'],
                  'fraction_max':summary['bare_plus_induced_induced_fraction_bound']},indent=2))
