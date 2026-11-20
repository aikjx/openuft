"""ROOT V113 reproducible numerical tables and scientific figures.
Usage: python run_all.py (no network; all source data explicit).
"""
import sys, json, math, csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
import v113 as v
OUT=ROOT/'results'; FIG=ROOT/'figures'
OUT.mkdir(exist_ok=True);FIG.mkdir(exist_ok=True)
summary=v.wrap_summary()

# Benchmark at 2 distinct radii: mathematical local gamma proxy, not Cassini path fit.
a=1/3
lam=v.AU_M
r1=v.AU_M
r2=2*v.AU_M
j=np.array([v.local_gamma_jacobian(r1,a,lam),v.local_gamma_jacobian(r2,a,lam)],float)
# Normalize lambda column by lambda to compute dimensionless sensitivity.
j_scaled=j*np.array([1.,lam])[None,:]
sv=np.linalg.svd(j_scaled,compute_uv=False)
summary.update({'local_two_scale_example':{'radii_AU':[1,2], 'alpha2':a,'range_AU':1,
                       'Jacobian_scaled':j_scaled.tolist(),
                       'det_scaled':float(np.linalg.det(j_scaled)),
                       'singular_values':sv.tolist(),
                       'condition_number':float(sv[0]/sv[-1])},
               'counterexample_eotvos':{
                  'alphaA':1/3,'alphaB':1/3,'alphaS':1/3,
                  'eta_universal_exactly':v.eotvos_eta(1/3,1/3,1/3,v.AU_M,0),
                  'gamma_massless':v.gamma_bd(0)},
               'metadata':{'source':'published Cassini 2003 and MICROSCOPE 2022 numbers; conditional simple models',
                           'science_level':'model math verified; quantum four-force unification OPEN',
                           'caveat':'mass threshold at 1AU is a local gamma(r) proxy, NOT observational Cassini mass exclusion'}})
(OUT/'V113_RESULTS.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')

# 1 gamma of massless Brans-Dicke and Cassini two sigma band.
omegas=np.geomspace(1e-2,1e6,700)
dev=np.array([abs(v.gamma_minus_one_bd(w)) for w in omegas])
plt.figure(figsize=(9,5))
plt.loglog(omegas,dev,label=r'Brans-Dicke $|\gamma-1|$')
plt.axhline(2*v.CASSINI_SIGMA-v.CASSINI_CENTER,linestyle='--',label='Cassini 2-sigma one-sided magnitude (model gamma<=1)')
plt.axvline(v.omega_min_at_sigma(2),linestyle=':',label='omega threshold 39998')
plt.scatter([1e-2],[abs(v.gamma_minus_one_bd(0))],marker='o',label='KK omega=0 at left edge (true gamma=0.5)')
plt.xlabel('omega_BD (log scale; omega=0 shown at 0.01)')
plt.ylabel('absolute gamma-1')
plt.title('Massless KK scalar vs Cassini PPN gamma')
plt.grid(True,which='both',alpha=.2);plt.legend(fontsize=8);plt.tight_layout()
plt.savefig(FIG/'01_CASSINI_SCALAR_NO_GO.png',dpi=170);plt.close()

# 2 massive scalar range impact. This is model local gamma only.
masses=np.logspace(-22,-13,600)
plt.figure(figsize=(9,5))
for dist in [.01,1.,10.]:
    y=np.array([abs(v.gamma_eff_minus_one(dist*v.AU_M,0,m)) for m in masses])
    plt.semilogx(masses,np.maximum(y,1e-25),label=f'r = {dist:g} AU (local proxy)')
plt.axhline(2*v.CASSINI_SIGMA-v.CASSINI_CENTER,linestyle='--',label='Cassini numerical reference, not a full fit')
plt.axvline(v.proxy_mass_min_eV(v.AU_M),linestyle=':',label='1 AU toy threshold')
plt.yscale('log');plt.ylim(1e-25,1)
plt.xlabel('Scalar mass (eV)');plt.ylabel('Local model |gamma(r)-1|')
plt.title('Illustrative scalar Yukawa suppression: not real Cassini constraints')
plt.grid(True,which='both',alpha=.2);plt.legend(fontsize=9);plt.tight_layout()
plt.savefig(FIG/'02_SCALAR_RANGE_TOY.png',dpi=170);plt.close()

# 3 EP: composition dependence affects eta whereas universal coupling gives exactly zero.
deltas=np.logspace(-17,-6,400)
alphaS=.3; alphaB=.01
etas=np.array([abs(v.eotvos_eta(alphaB+delta,alphaB,alphaS,v.AU_M,0)) for delta in deltas])
plt.figure(figsize=(9,5))
plt.loglog(deltas,etas,label='Toy predicted |eta|, massless alphaS=0.3')
plt.axhline(v.microscope_conservative_abs_band(),linestyle='--',label='MICROSCOPE illustrative 2sigma abs envelope')
plt.xlabel('Composition-dependent scalar coupling |alphaA-alphaB|')
plt.ylabel('Absolute Eotvos eta (dimensionless)')
plt.title('Universal vs non-universal fifth-force EP signatures')
plt.grid(True,which='both',alpha=.2);plt.legend(fontsize=9);plt.tight_layout()
plt.savefig(FIG/'03_MICROSCOPE_COMPOSITION.png',dpi=170);plt.close()

# 4 two scale identifiability. Both parameters are dimensionless (alpha^2, log lambda).
ratios=np.geomspace(1.001,100,400)
conds=[];detvalues=[]
for t in ratios:
    jj=np.array([v.local_gamma_jacobian(v.AU_M,a,lam),v.local_gamma_jacobian(t*v.AU_M,a,lam)])
    jj[:,1]*=lam
    sing=np.linalg.svd(jj,compute_uv=False)
    conds.append(float(sing[0]/sing[-1]) if sing[-1] else math.inf)
    detvalues.append(float(np.linalg.det(jj)))
plt.figure(figsize=(9,5))
plt.loglog(ratios,conds,label='Two-radii dimensionless Jacobian condition number')
plt.axvline(2,linestyle=':',label='r2/r1 = 2 benchmark')
plt.xlabel('Ratio of two independent radii r2/r1')
plt.ylabel('Condition number (lower means more identifiable)')
plt.title('Two distinct measurement scales remove exact degeneracy, not noise')
plt.grid(True,which='both',alpha=.2);plt.legend(fontsize=9);plt.tight_layout()
plt.savefig(FIG/'04_TWO_SCALE_IDENTIFIABILITY.png',dpi=170);plt.close()

# Numeric CSV of omega and gamma, for audits.
with (OUT/'gamma_ppn_scan.csv').open('w',encoding='utf-8',newline='') as f:
    wr=csv.writer(f);wr.writerow(['omega','gamma','gamma_minus_one','Cassini_z'])
    for w in [0,1,10,100,1000,10000,39998,40000,50000,100000]:
        wr.writerow([w,format(v.gamma_bd(w),'.17g'),format(v.gamma_minus_one_bd(w),'.17g'),format(v.zscore_cassini(v.gamma_bd(w)),'.17g')])
print(json.dumps(summary,ensure_ascii=False,indent=2))
