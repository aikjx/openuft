"""Generate numerical tables and figures for ROOT V71, without using external data feeds."""
from pathlib import Path
import csv,json, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from rootv71.physics import *
from rootv71.inference import *
P=Path(__file__).resolve().parent
for sub in ('results','plots','data'): (P/sub).mkdir(exist_ok=True)

def write_csv(name,rows):
    if not rows:return
    with (P/'data'/name).open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)

R=EARTH_R
lams=np.geomspace(1e3,1e9,151)
ratios=[]
for lam in lams:
    point=point_ratio(R,0.,lam)
    uniform=uniform_ratio(R,0.,lam)
    layered=layered_ratio(same_mass_layered_shells(R),0.,lam)
    ratios.append({'lambda_m':float(lam),'lambda_over_R':float(lam/R),
                   'point_source_ratio_alpha1':point,'finite_uniform_ratio_alpha1':uniform,
                   'finite_two_layer_ratio_alpha1':layered,'layered_over_uniform':layered/uniform})
write_csv('有限尺寸与点源对照_151组.csv',ratios)

alts=np.linspace(0,3e6,121)
altrows=[]
for h in alts:
    s=uniform_ratio(R,float(h),1e6)
    l=uniform_ratio(R,float(h),1e7)
    altrows.append({'altitude_m':h,'source_g_newton':central_gravity(EARTH_MU,R+h),
                    'finite_ratio_lambda_1000km_alpha1':s,
                    'finite_ratio_lambda_10000km_alpha1':l,
                    'gravitational_redshift':redshift_height(EARTH_MU,R,h)})
write_csv('地球高度扫描_121组.csv',altrows)

X,metadata=mixed_design()
features=[]
for i,(body,pair,alt,phase) in enumerate(metadata):
    features.append({'idx':i,'body':body,'material_pair':pair,'altitude_R':alt,'phase_radian':phase,
                     'Yukawa_short_feature':X[i,0], 'Yukawa_long_feature':X[i,1],
                     'preferred_frame_toy_feature':X[i,2], 'synthetic_only':True})
write_csv('合成实验矩阵_192行_非观测数据.csv',features)

scales=np.geomspace(1e9,1e19,121)
rgrows=[]
for q in scales:
    v=gauge_inverse_alphas(float(q))
    rgrows.append({'Q_GeV':q,'alpha1_inv':v[0],'alpha2_inv':v[1],'alpha3_inv':v[2]})
write_csv('标准模型一圈RG演示_121组.csv',rgrows)

# Plots: matplotlib defaults; no imposed colors/styles.
fig,ax=plt.subplots(figsize=(8.3,4.9))
ax.loglog([r['lambda_over_R'] for r in ratios],[max(r['finite_uniform_ratio_alpha1'],1e-300) for r in ratios],label='Finite uniform sphere')
ax.loglog([r['lambda_over_R'] for r in ratios],[max(r['point_source_ratio_alpha1'],1e-300) for r in ratios],label='Point-source approximation')
ax.loglog([r['lambda_over_R'] for r in ratios],[max(r['finite_two_layer_ratio_alpha1'],1e-300) for r in ratios],label='Same-mass two-layer sphere')
ax.set_xlabel('Yukawa range / Earth reference radius')
ax.set_ylabel('|Delta g / g_N| for alpha=1, surface')
ax.set_title('Hypothetical finite-range force: source size matters')
ax.grid(True,which='both',alpha=.2);ax.legend(fontsize=8)
fig.tight_layout();fig.savefig(P/'plots'/'01_finite_vs_point.png',dpi=150);plt.close(fig)

fig,ax=plt.subplots(figsize=(8.3,4.9))
ax.semilogx([r['lambda_over_R'] for r in ratios],[r['layered_over_uniform'] for r in ratios])
ax.set_xlabel('Yukawa range / Earth reference radius')
ax.set_ylabel('Two-layer / uniform external response')
ax.set_title('Same total mass, different finite-range response')
ax.grid(True,alpha=.2);fig.tight_layout();fig.savefig(P/'plots'/'02_density_profile.png',dpi=150);plt.close(fig)

fig,ax=plt.subplots(figsize=(8.3,4.9))
ax.plot([r['altitude_m']/1000 for r in altrows],[r['finite_ratio_lambda_1000km_alpha1'] for r in altrows],label='lambda = 1000 km')
ax.plot([r['altitude_m']/1000 for r in altrows],[r['finite_ratio_lambda_10000km_alpha1'] for r in altrows],label='lambda = 10000 km')
ax.set_xlabel('Altitude above spherical Earth (km)');ax.set_ylabel('Delta g / g_N for alpha=1')
ax.set_title('Hypothetical finite-range response versus altitude')
ax.grid(True,alpha=.2);ax.legend();fig.tight_layout();fig.savefig(P/'plots'/'03_altitude.png',dpi=150);plt.close(fig)

fig,ax=plt.subplots(figsize=(8.3,4.9))
for key in ('alpha1_inv','alpha2_inv','alpha3_inv'):
    ax.semilogx([r['Q_GeV'] for r in rgrows],[r[key] for r in rgrows],label=key)
ax.set_xlabel('Renormalization scale Q (GeV)');ax.set_ylabel('1 / alpha_i')
ax.set_title('SM one-loop only: no exact three-way crossing')
ax.grid(True,alpha=.2);ax.legend();fig.tight_layout();fig.savefig(P/'plots'/'04_gauge_running.png',dpi=150);plt.close(fig)

fig,ax=plt.subplots(figsize=(7.8,4.7))
f=design_diagnostics(fixed_design());m=design_diagnostics(X)
a=np.arange(1,4)
ax.semilogy(a,[max(x,1e-18) for x in f['svals_normalized']],marker='o',label='Fixed Earth, only materials')
ax.semilogy(a,m['svals_normalized'],marker='s',label='Mixed bodies/altitude/phase')
ax.set_xticks([1,2,3]);ax.set_xlabel('Singular value number');ax.set_ylabel('Normalized singular value')
ax.set_title('Structural identifiability != experimental detection')
ax.grid(True,alpha=.2);ax.legend();fig.tight_layout();fig.savefig(P/'plots'/'05_design_rank.png',dpi=150);plt.close(fig)

fig,ax=plt.subplots(figsize=(8.3,4.9))
ax.loglog([r['lambda_over_R'] for r in ratios],[abs(r['finite_uniform_ratio_alpha1']-r['finite_two_layer_ratio_alpha1']) for r in ratios])
ax.set_xlabel('Yukawa range / Earth reference radius');ax.set_ylabel('Absolute profile difference, alpha=1')
ax.set_title('Finite-range sensitivity to internal stratification')
ax.grid(True,which='both',alpha=.2);fig.tight_layout();fig.savefig(P/'plots'/'06_profile_difference.png',dpi=150);plt.close(fig)

summary={
    'version':'71.0', 'generated_dataset_type':'ANALYTIC + SYNTHETIC ONLY, NO EXPERIMENTAL DETECTION',
    'baseline_G_SI_INPUT':G,
    'central_earth_gravity':central_gravity(EARTH_MU,R),
    'earth_1mm_gravitational_redshift':redshift_height(EARTH_MU,R,.001),
    'yukawa_table_count':len(ratios),
    'altitude_table_count':len(altrows),
    'RG_table_count':len(rgrows),
    'toy_design_count':len(X),
    'short_range_1000km':{'point':point_ratio(R,0.,1e6), 'finite_uniform':uniform_ratio(R,0.,1e6),
                           'finite_two_layer':layered_ratio(same_mass_layered_shells(R),0.,1e6)},
    'short_range_1km':{'point_underflow_to_zero':point_ratio(R,0.,1000.),
                       'finite_uniform':uniform_ratio(R,0.,1000.),
                       'finite_two_layer':layered_ratio(same_mass_layered_shells(R),0.,1000.)},
    'finite_layers_vs_uniform_at_1km':layered_ratio(same_mass_layered_shells(R),0.,1000.)/uniform_ratio(R,0.,1000.),
    'gauge_pair_crossings_GeV':gauge_pair_crossings(),
    'gauge_best_fit':gauge_best_fit(),
    'anomaly_sums':{k:str(v) for k,v in anomaly_sums().items()},
    'dimensions_G_from_c_hbar':{'least_squares':dimensions_G_from_c_hbar()[0].tolist(),
                                  'nonzero_residual':dimensions_G_from_c_hbar()[1]},
    'fixed_design':f,'mixed_design':m,
    'synthetic_fit':fit_synthetic(X),
    'unproven':['G from microscopic helical postulates','derivation of gauge group and full particle spectrum',
                'new field detection','quantum UV completion','full four-force unification'],
}
(P/'results'/'numerical_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
print(json.dumps({'status':'OK','rows':len(ratios),'fixed_rank':f['rank'],'mixed_rank':m['rank'],'best_RGE_GeV':gauge_best_fit()['q']},ensure_ascii=False))
