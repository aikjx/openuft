"""Produce transparent benchmark numbers, CSV and JSON. No input data here are observational residuals."""
from pathlib import Path
import csv, json, sys, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.physics import *
from src.simulation import *
OUT=ROOT/'data';RES=ROOT/'results';OUT.mkdir(exist_ok=True);RES.mkdir(exist_ok=True)

# GM data: JPL DE440 selected celestial objects, m^3/s^2.
# Radii are approximate conventional radii for illustration, not independent G measurements.
bodies=[
 ('Earth',3.98600435507e14,6.3710e6,'JPL DE440 Earth GM; mean radius approximated'),
 ('Moon',4.902800118e12,1.7374e6,'JPL DE440 Moon GM; mean radius approximated'),
 ('Sun',1.32712440041279419e20,6.9570e8,'JPL DE440 heliocentric GM; photospheric nominal radius'),
 ('Jupiter_system_approx',1.267127641e17,6.9911e7,'JPL DE440 Jupiter SYSTEM GM; Jupiter mean radius; only approximate pairing'),
 ('White_dwarf_example',G_REF*0.7*1.98847e30,8.0e6,'MODEL ASSUMPTION M=0.7 solar mass R=8000 km'),
 ('Neutron_star_example',G_REF*1.4*1.98847e30,1.2e4,'MODEL ASSUMPTION M=1.4 solar mass R=12 km'),
]
with (OUT/'celestial_GM_benchmarks.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f);w.writerow(['body','mu_GM_m3_s2','radius_m','surface_g_m_s2','compactness_GM_Rc2','Schwarzschild_K_m-4','notes'])
    for name,mu,r,note in bodies:
        w.writerow([name,f'{mu:.15g}',f'{r:.15g}',f'{newton_acceleration(mu,r):.14g}',f'{compactness(mu,r):.14g}',f'{kretschmann(mu,r):.14g}',note])

radii=np.geomspace(.12,3.5,120)
alpha=.15;lam=.35
with (OUT/'distance_shape_diagnostic_SYNTHETIC.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f);w.writerow(['r_m','Q_Newton','Q_Yukawa_hypothesis_alpha_0p15_lambda_0p35','force_factor_Yukawa','data_type'])
    for r in radii:
        w.writerow([f'{r:.10g}',1,f'{radial_shape_point(r,alpha,lam):.14g}',f'{point_yukawa_acceleration(1,r,alpha,lam)/newton_acceleration(1,r):.14g}','SYNTHETIC_MODEL'])

sources=[(.85,.30,.05),(-.65,.45,.08),(1.2,.62,.11),(.38,.9,.14)]
pairs=[(1,.5),(-.3,.7),(1.4,.2),(.1,.9)]
one=exact_factor_matrix(sources,pairs,.075,.3)
source2=[(.85,.2,.3,.05),(-.65,.9,.45,.08),(1.2,-.6,.62,.11),(.38,.8,.9,.14)]
pairs2=[(1,.5,.4,.9),(-.3,.7,.6,.1),(1.4,.2,-.3,.5),(.1,.9,-.8,.6)]
two=two_mediator_matrix(source2,pairs2,.075,.3,.12,.72)
noise=gaussian_noisy(one,.0004,20261118)
with (OUT/'cross_source_material_matrix_SYNTHETIC.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f);w.writerow(['scenario','source','pair','normalized_difference','data_type'])
    for label,m in [('one_mediator',one),('two_mediator',two),('one_mediator_with_noise',noise)]:
        for si,row in enumerate(m):
            for tj,val in enumerate(row):w.writerow([label,f'S{si+1}',f'P{tj+1}',f'{val:.14g}','SYNTHETIC_MODEL'])

s1=singular_values(one);s2=singular_values(two);sn=singular_values(noise)
summary={
    'project':'ROOT V85','generated_at':'2026-11-18','data_status':'SYNTHETIC MODEL + JPL REFERENCE PARAMETERS; NOT NEW OBSERVATIONS',
    'G_input_m3_kg-1_s-2':G_REF,
    'Z_from_G_input':z_from_G(),
    'G_relative_standard_uncertainty':G_STD/G_REF,
    'scalar_hypothesis_example':{'alpha':alpha,'range_m':lam,'Q_at_0p35m':radial_shape_point(.35,alpha,lam),'Q_at_10m':radial_shape_point(10,alpha,lam)},
    'cross_source':{'single_mediator_singular_values':s1,'two_mediator_singular_values':s2,'noisy_single_mediator_singular_values':sn,
                    'two_mediator_ratio_s2_s1':s2[1]/s2[0],'noise_sd':0.0004,'seed':20261118},
    'microscope_combined_standard_uncertainty':math.hypot(2.3e-15,1.5e-15),
    'microscope_illustrative_abs_central_plus_1p96sig':conservative_95_eta_bound(),
    'constraints_caveat':'MICROSCOPE applies to a particular Earth-source/test-material combination; not a universal alpha bound.',
    'celestial_bodies':[{'name':name,'g_m_s2':newton_acceleration(mu,r),'compactness':compactness(mu,r),'K_m-4':kretschmann(mu,r)} for name,mu,r,note in bodies]
}
(RES/'numerical_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')

# Independent visualizations, model-labelled axes
fig,ax=plt.subplots(figsize=(8,4.5))
ax.semilogx(radii,[radial_shape_point(float(r),alpha,lam) for r in radii],label='Yukawa (hypothetical)')
ax.axhline(1,ls='--',label='Newton / constant source G')
ax.set(xlabel='radius r [m]',ylabel='Q = -r/(2g) dg/dr',title='Radial shape: independent of absolute GM normalization');ax.legend();ax.grid(alpha=.2)
fig.tight_layout();fig.savefig(RES/'radial_shape.png',dpi=160);plt.close(fig)
fig,ax=plt.subplots(figsize=(8,4.5))
ax.bar(['single mediator','two mediators','one + noise'],[s1[1]/s1[0],s2[1]/s2[0],sn[1]/sn[0]])
ax.set(yscale='log',ylabel='second / first singular value',title='Synthetic rank-one consistency vs failure (not real data)');ax.grid(axis='y',alpha=.2)
fig.tight_layout();fig.savefig(RES/'rank_one_falsification.png',dpi=160);plt.close(fig)
fig,ax=plt.subplots(figsize=(8,4.5))
ax.imshow(np.array(one),aspect='auto');ax.set(xlabel='test material pair',ylabel='source body',title='SYNTHETIC normalized free-fall difference: one mediator')
ax.set_xticks(range(len(pairs)),[f'P{i+1}' for i in range(len(pairs))]);ax.set_yticks(range(len(sources)),[f'S{i+1}' for i in range(len(sources))]);fig.colorbar(ax.images[0],ax=ax,label='D_ij^A')
fig.tight_layout();fig.savefig(RES/'one_mediator_matrix.png',dpi=160);plt.close(fig)
print(json.dumps({'G':G_REF,'Q_at_lambda':summary['scalar_hypothesis_example']['Q_at_0p35m'],'svals1':s1,'svals2':s2,'svals_noise':sn},indent=2))
