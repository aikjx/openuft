"""Regenerate numeric tables and plots. All synthetic observations are labeled synthetic."""
from __future__ import annotations
import csv, json, math
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from rootv73.models import *
ROOT=Path(__file__).resolve().parent
(ROOT/'data').mkdir(exist_ok=True)
(ROOT/'plots').mkdir(exist_ok=True)
(ROOT/'results').mkdir(exist_ok=True)

def csv_write(name,head,rows):
    with open(ROOT/'data'/name,'w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(head);w.writerows(rows)

# one-loop RG scale (calibrated to an illustrative target, not a UV prediction)
uv=2.435e18
couplings=np.linspace(.42,.66,121)
rg_rows=[[float(g),scale_from_rg(uv,float(g)),float(rg_scale_sensitivity(float(g)))] for g in couplings]
csv_write('01_RG尺度对UV耦合敏感性.csv',['g_UV (input)','Lambda_GeV (toy)','dlnLambda_dg'],rg_rows)
fig,ax=plt.subplots(figsize=(8,4.5));ax.semilogy([r[0] for r in rg_rows],[r[1] for r in rg_rows]);ax.axhline(.2,linestyle='--');ax.set_xlabel('UV coupling g (fixed b0=7)');ax.set_ylabel('Induced RG scale Lambda (GeV)');ax.set_title('Dimensional transmutation: parameter sensitivity');fig.tight_layout();fig.savefig(ROOT/'plots'/'01_RG尺度敏感性.png',dpi=150);plt.close(fig)

lambdas=np.geomspace(2e4,1e9,150)
geom_rows=[]
for lam in lambdas:
    geom_rows.append([float(lam),point_yukawa_factor(EARTH_R,float(lam)),uniform_yukawa_factor(EARTH_R,float(lam)),layered_yukawa_factor(EARTH_R,float(lam),earth_two_layer_model())])
csv_write('02_地球点源有限球分层球对比.csv',['lambda_m','point_source_factor','uniform_ball_factor','two_layer_ball_factor'],geom_rows)
fig,ax=plt.subplots(figsize=(8,4.5))
for i,label in [(1,'Point approximation'),(2,'Finite uniform sphere'),(3,'Two-layer sphere')]:
    ax.loglog([r[0] for r in geom_rows],[r[i] for r in geom_rows],label=label)
ax.set_xlabel('Yukawa range (m)');ax.set_ylabel('(delta g / gN) / alpha');ax.legend();ax.set_title('Finite source effect: same total mass, different profiles');fig.tight_layout();fig.savefig(ROOT/'plots'/'02_有限尺寸与密度对比.png',dpi=150);plt.close(fig)

bound_rows=[[float(lam),float(eotvos_alpha_bound(float(lam))),float(uniform_yukawa_factor(EARTH_R,float(lam)))] for lam in lambdas]
csv_write('03_材料依赖第五力条件上界.csv',['lambda_m','conditional_abs_alpha_bound','earth_geometry_factor'],bound_rows)
fig,ax=plt.subplots(figsize=(8,4.5));ax.loglog([r[0] for r in bound_rows],[r[1] for r in bound_rows]);ax.set_xlabel('Yukawa range (m)');ax.set_ylabel('Illustrative upper |alpha|');ax.set_title('Toy material charges Z/A; MICROSCOPE-based 95%-style illustration');fig.tight_layout();fig.savefig(ROOT/'plots'/'03_材料依赖假设模型界限.png',dpi=150);plt.close(fig)

# Eight-factor contrast exact algebra and a cross-environment synthetic experiment
H=hadamard_design(); coeff=np.array([.1,.04,.08,.02,.003,-.006,.007,.01])
single_y=H@coeff
csv_write('04_三重反转8状态演示.csv',['h','r','s','synthetic_y','hrs_weight'],[[*sign_states()[i],float(single_y[i]),int(H[i,-1])] for i in range(8)])
x=np.linspace(-1,1,24)
rng=np.random.default_rng(73)
sigma=3e-5; nuisance=1.2e-3; beta=4e-4
measured=nuisance+beta*x+rng.normal(0,sigma,size=len(x))
fit=fit_cross_env(x,measured)
csv_write('05_跨环境三重反转合成数据.csv',['environment_feature','synthetic_contrast','true_nuisance','true_beta'],[[float(xi),float(yi),nuisance,beta] for xi,yi in zip(x,measured)])
fig,ax=plt.subplots(figsize=(8,4.5));ax.scatter(x,measured,s=22,label='Synthetic observations');ax.plot(x,fit['nuisance']+fit['beta']*x,label='Fit');ax.set_xlabel('Environmental feature X (artificial)');ax.set_ylabel('Triple-contrast signal (arbitrary units)');ax.legend();ax.set_title('Three-reversal eight-state design, synthetic only');fig.tight_layout();fig.savefig(ROOT/'plots'/'04_三重反转合成恢复.png',dpi=150);plt.close(fig)

# Confounder with exactly same dependence is fully unidentified
Xconf=np.column_stack([np.ones(len(x)),x,x]);rank=int(np.linalg.matrix_rank(Xconf))

def tofloat(x):
    if isinstance(x,(np.floating,np.integer)):return x.item()
    return x

summary={
 'version':'ROOT V73',
 'scope':'Mathematical and synthetic validation only; no new empirical discoveries',
 'rg_calibration':dimensional_scale_hierarchy(),
 'source_shape':{'range_m':1e6,'point_approx':point_yukawa_factor(EARTH_R,1e6),
                 'uniform_sphere':uniform_yukawa_factor(EARTH_R,1e6),
                 'two_layer_sphere_same_mass':layered_yukawa_factor(EARTH_R,1e6,earth_two_layer_model()),
                 'uniform_over_point_ratio':uniform_yukawa_factor(EARTH_R,1e6)/point_yukawa_factor(EARTH_R,1e6)},
 'conditional_microscope':{'data_type':'real published uncertainty used as input + toy Z/A charges',
  'eta_conservative_approx_95_bound':G_STD,'source_ZA_assumed':.5,
  'bound_alpha_lambda_1e7m':eotvos_alpha_bound(1e7)},
 'triple_contrast':{'true_beta_synthetic':beta,'fitted_beta_synthetic':fit['beta'],
  'true_nuisance_synthetic':nuisance,'fitted_nuisance_synthetic':fit['nuisance'],
  'hadamard_orthogonal':bool(np.array_equal(H.T@H,8*np.eye(8))),
  'unidentifiable_same_signature_rank':rank,'fully_contrast_noise_std_factor':1/math.sqrt(8)},
 'disclaimer':'No independent prediction G, gauge group, or empirical evidence of unification.'}
(ROOT/'results'/'numerical_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2,default=tofloat),encoding='utf-8')
print(json.dumps({'results':'OK','plots':4,'numeric_tables':5,'rg_g':summary['rg_calibration']['g_uv_fitted'],
  'shape_ratio':summary['source_shape']['uniform_over_point_ratio'],
  'triple_fit':fit['beta'],'degenerate_rank':rank},ensure_ascii=False,indent=2))
