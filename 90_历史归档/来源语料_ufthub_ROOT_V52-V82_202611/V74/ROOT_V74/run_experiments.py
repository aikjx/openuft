#!/usr/bin/env python3
"""Reproducible V74 numerics. Observations vs synthetic assumptions are explicitly labeled."""
import csv, json, math, pathlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from rootv74.physics import *
OUT=pathlib.Path(__file__).resolve().parent
D=OUT/'data';P=OUT/'figures';R=OUT/'results'
for directory in (D,P,R): directory.mkdir(parents=True,exist_ok=True)

def emit_csv(name,rows):
    with (D/name).open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)

bodies=[]
for b in BODIES.values():
    bodies.append({'body':b.name,'mass_kg':b.mass,'radius_m':b.radius,'mean_density_kg_m3':b.density,
                   'g_Newton_m_s2':b.gravity,'tidal_gradient_s-2':b.tidal,
                   'K_external_Schwarzschild_m-4':b.kretschmann,'curvature_length_m':b.kretschmann**(-.25),
                   'source_note':b.notes})
emit_csv('01_celestial_surface_invariants.csv',bodies)

rho=5000.0; R1=2e6;R2=6e6
same_density=[]
for rad in (R1,R2):
    mass=4*math.pi*rho*rad**3/3
    same_density.append({'mean_density_kg_m3':rho,'radius_m':rad,'mass_kg':mass,'g_m_s2':g_newton(mass,rad),'K_m-4':kretschmann(mass,rad)})
emit_csv('02_same_density_different_radius.csv',same_density)

fixedg=10.;same_g=[]
for rad in (R1,R2):
    mass=fixedg*rad*rad/G_EXP
    same_g.append({'g_m_s2':fixedg,'radius_m':rad,'mass_kg':mass,'mean_density_kg_m3':3*mass/(4*math.pi*rad**3),'K_m-4':kretschmann(mass,rad)})
emit_csv('03_same_g_different_curvature.csv',same_g)

ranges=np.logspace(3,10,110)
r=R_EARTH+710e3
rho_ref=BODIES['Earth'].density
rho_core=2*rho_ref
core=.55*R_EARTH
rho_mantle=(rho_ref*R_EARTH**3-rho_core*core**3)/(R_EARTH**3-core**3)
layers=[Shell(core,rho_core,1.),Shell(R_EARTH,rho_mantle,1.)]
assert abs((rho_core*core**3+rho_mantle*(R_EARTH**3-core**3))/R_EARTH**3/rho_ref-1)<1e-12
sample=[]
for lam in ranges:
    finite=uniform_yukawa_ratio(R_EARTH,r,float(lam))
    layered=layered_yukawa_ratio(layers,r,float(lam))
    point=(1+r/lam)*math.exp(-r/lam)
    sample.append({'lambda_m':float(lam),'point_ratio_alpha1':point,'uniform_ratio_alpha1':finite,
                   'layered_equal_mass_ratio_alpha1':layered,'finite_over_point': finite/point if point>1e-290 else None})
emit_csv('04_finite_size_yukawa_scan_alpha1.csv',sample)

micro=[]
for wavelength in (1e5,1e6,1e7,1e8,1e9):
    shape=uniform_yukawa_ratio(R_EARTH,R_EARTH+710e3,wavelength)
    qTi=proxy_charge_Z_over_A(22.,47.867)
    qPt=proxy_charge_Z_over_A(78.,195.084)
    qE=.5 # deliberately invented illustrative source charge, not empirical Earth composition measurement
    bound=miniature_eta_bound(-1.5e-15,2.3e-15,1.5e-15,shape,qE,qTi-qPt)
    micro.append({'lambda_m':wavelength,'shape':shape,'assumed_source_charge':qE,
                  'proxy_Q_Ti':qTi,'proxy_Q_Pt':qPt,'illustrative_abs_alpha_bound_95pct':bound,
                  'caution':'conditional Z/A proxy, not a model-independent exclusion'})
emit_csv('05_microscope_conditional_proxy.csv',micro)

rge=[]
for g in np.linspace(.35,1.4,120):
    scale=rg_generated_scale(1e19,float(g),7.)
    rge.append({'uv_coupling_input':float(g),'generated_scale_GeV':scale,
                'log10_scale':math.log10(scale),'note':'toy 1loop with independent UV coupling'})
emit_csv('06_rg_dimensional_transmutation_toy.csv',rge)

from rootv74.physics import gauge_running
unif=gauge_running();anomalies={k:str(v) for k,v in sm_anomalies().items()}

# Plot 1: g and K compared across bodies (no artificial error bars)
fig,ax=plt.subplots(figsize=(9,5))
x=np.arange(len(bodies));label=[row['body'] for row in bodies]
ax.plot(x,[row['g_Newton_m_s2'] for row in bodies],marker='o')
ax.set_xticks(x,label,rotation=30,ha='right');ax.set_yscale('log');ax.set_ylabel('g (m/s^2)');ax.set_title('Spherical exterior reference: surface gravity')
fig.tight_layout();fig.savefig(P/'01_gravity_across_bodies.png',dpi=150);plt.close(fig)
fig,ax=plt.subplots(figsize=(9,5))
ax.plot(x,[row['K_external_Schwarzschild_m-4'] for row in bodies],marker='o')
ax.set_xticks(x,label,rotation=30,ha='right');ax.set_yscale('log');ax.set_ylabel('K (m^-4)');ax.set_title('Spherical exterior reference: curvature invariant')
fig.tight_layout();fig.savefig(P/'02_curvature_across_bodies.png',dpi=150);plt.close(fig)
fig,ax=plt.subplots(figsize=(8.5,5))
ax.loglog(ranges,[max(v['point_ratio_alpha1'],1e-300) for v in sample],label='Point mass')
ax.loglog(ranges,[max(v['uniform_ratio_alpha1'],1e-300) for v in sample],label='Uniform finite sphere')
ax.loglog(ranges,[max(v['layered_equal_mass_ratio_alpha1'],1e-300) for v in sample],label='Layered same-mass sphere')
ax.set_xlabel('Hypothetical range lambda (m)');ax.set_ylabel('gY/gN for toy alpha=1');ax.set_title('Toy Yukawa predictions, not measured forces');ax.legend();fig.tight_layout();fig.savefig(P/'03_yukawa_finite_size.png',dpi=150);plt.close(fig)
fig,ax=plt.subplots(figsize=(8.5,5))
ax.plot([v['uv_coupling_input'] for v in rge],[v['log10_scale'] for v in rge]);ax.set_xlabel('Input UV coupling g');ax.set_ylabel('log10 Lambda (GeV)');ax.set_title('One-loop dimensional transmutation still needs input g');fig.tight_layout();fig.savefig(P/'04_scale_parameter_sensitivity.png',dpi=150);plt.close(fig)

summary={
 'release':'ROOT_V74', 'date':'2026-11-17',
 'scientific_status':'NO FOUR-FORCE UNIFICATION PROOF, NO INDEPENDENT G PREDICTION',
 'grounded_physical_constants':'CODATA 2022 G is external experimental input',
 'bodies':bodies,'same_density_pair':same_density,'same_g_pair':same_g,
 'yukawa_demo_at_1e6m':min(sample,key=lambda a:abs(a['lambda_m']-1e6)),
 'yukawa_layers_demo':{'core_fraction':core/R_EARTH,'core_density':rho_core,'mantle_density':rho_mantle,
                         'same_total_mass':True},
 'microscope_conditional_proxy':micro,'gauge_running':unif,'sm_anomalies':anomalies,
 'tests':'run with python run_tests.py; verification report has result',
 'new_testable_hypothesis':'Delta m_eff^2 = xi l_*^2 K for a hypothetical helical scalar mode. xi,l_* free; no empirical confirmation.',
 'source_urls':[
 'https://physics.nist.gov/cuu/Constants/',
 'https://pdg.lbl.gov/2026/',
 'https://pubmed.ncbi.nlm.nih.gov/36179190/',
 'https://nssdc.gsfc.nasa.gov/planetary/factsheet/sunfact.html?level=1',
 'https://www.damtp.cam.ac.uk/user/tong/gr/grhtml/S6.html'
 ]}
(R/'numerical_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print('Generated 6 CSV, 4 figures and numerical_summary.json')
for b in bodies:
 print(f"{b['body']:20s} g={b['g_Newton_m_s2']:.8g} K={b['K_external_Schwarzschild_m-4']:.5e} rho={b['mean_density_kg_m3']:.5g}")
print('SM minimum coupling mismatch alpha-inverse=',unif['max_minus_min_at_best'])
