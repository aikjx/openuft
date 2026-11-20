"""Reproduce ROOT V115 figures and numerical JSON, no network access required."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.v115 import (example_inputs,ALPHA_S_MZ,ALPHA_S_MZ_SIGMA,MZ_GEV,
                      lambda_qcd_one_loop,run_alpha_one_loop,required_induced_zeta,
                      qcd_beta_over_2g, reduced_planck_mass_gev,beta0_qcd,
                      lambda_log_sensitivity)

ROOT=Path(__file__).resolve().parent
FIG=ROOT/'figures';RES=ROOT/'results'
FIG.mkdir(exist_ok=True);RES.mkdir(exist_ok=True)
inputs=example_inputs()
scales=np.geomspace(15,10000,250)
alpha=np.array([run_alpha_one_loop(float(mu),MZ_GEV,ALPHA_S_MZ,5) for mu in scales])
lambda_back=np.array([lambda_qcd_one_loop(float(mu),float(a),5) for mu,a in zip(scales,alpha)])
alpha_grid=np.linspace(.06,.22,220)
Lambda_alpha=np.array([lambda_qcd_one_loop(MZ_GEV,float(a),5) for a in alpha_grid])
scales_vev=np.geomspace(.05,1e19,230)
zeta_grid=np.array([required_induced_zeta(float(v)) for v in scales_vev])

rng=np.random.default_rng(20261120)
input_samples=rng.normal(ALPHA_S_MZ,ALPHA_S_MZ_SIGMA,size=5000)
lam_samples=np.array([lambda_qcd_one_loop(MZ_GEV,float(a),5) for a in input_samples if a>0])
inputs['independent_regression']={
    'RG_invariant_max_relative_deviation':float(np.max(np.abs(lambda_back-lambda_back[0]))/lambda_back[0]),
    'sampled_input_only_Lambda5_5_50_95_percentile_GeV':np.quantile(lam_samples,[.05,.5,.95]).tolist(),
    'sampled_input_only_N':int(len(lam_samples)),
    'quantum_source_warning':'operator beta coefficient does not fix expectation value of G^2 or actual Ricci scalar',
}
(RES/'V115_NUMERICAL_SUMMARY.json').write_text(json.dumps(inputs,ensure_ascii=False,indent=2),encoding='utf-8')
with (RES/'RG_RUN_SAMPLES.csv').open('w',encoding='utf-8') as f:
    f.write('mu_GeV,alpha_s_one_loop,Lambda5_one_loop_GeV\n')
    for mu,a,lam in zip(scales,alpha,lambda_back): f.write(f'{mu:.15g},{a:.15g},{lam:.15g}\n')

fig,ax=plt.subplots(figsize=(8.2,5.2))
ax.semilogx(scales,alpha,label=r'$\alpha_s(\mu)$ one-loop, fixed $n_f=5$')
ax.axvline(MZ_GEV,ls='--',lw=1.3,label=r'$M_Z$ input')
ax.set(xlabel='Renormalization scale mu (GeV)',ylabel='Strong coupling alpha_s',title='One-loop QCD coupling running (toy fixed-five-flavor model)')
ax.grid(alpha=.22);ax.legend();fig.tight_layout();fig.savefig(FIG/'01_QCD_running.png',dpi=160);plt.close(fig)

fig,ax=plt.subplots(figsize=(8.2,5.2))
ax.semilogx(scales,lambda_back,label=r'$\Lambda_5^{(1)}(\mu)$ reconstructed')
ax.axhline(float(lambda_back[0]),ls='--',lw=1.1,label='same RG integration constant')
ax.ticklabel_format(axis='y',style='plain',useOffset=False)
ax.set(xlabel='mu (GeV)',ylabel='Reconstructed one-loop Lambda (GeV)',title='RG invariance is not an input-free mass prediction')
ax.grid(alpha=.22);ax.legend();fig.tight_layout();fig.savefig(FIG/'02_RG_invariant.png',dpi=160);plt.close(fig)

fig,ax=plt.subplots(figsize=(8.2,5.2))
ax.plot(alpha_grid,Lambda_alpha,label='fixed-nf one-loop integration constant')
ax.axvline(ALPHA_S_MZ,ls='--',label='PDG 2025 input alpha_s')
ax.axvspan(ALPHA_S_MZ-ALPHA_S_MZ_SIGMA, ALPHA_S_MZ+ALPHA_S_MZ_SIGMA,alpha=.15,label='input ±0.0009')
ax.set(xlabel='Input alpha_s(M_Z)',ylabel='Lambda_5^(1) (GeV)',title='Dimensional transmutation: sensitivity to boundary coupling')
ax.grid(alpha=.22);ax.legend();fig.tight_layout();fig.savefig(FIG/'03_transmutation_sensitivity.png',dpi=160);plt.close(fig)

fig,ax=plt.subplots(figsize=(8.2,5.2))
ax.loglog(scales_vev,zeta_grid,label=r'Required $\zeta=\bar M_P^2/v^2$')
ax.axhline(1,ls='--',label=r'$\zeta=1$')
ax.axvline(inputs['one_loop_Lambda5_GeV'],ls=':',label='one-loop Lambda5 toy value')
ax.set(xlabel='Inducing scalar vacuum scale v (GeV)',ylabel='Required nonminimal coupling zeta',title='Single-scale induced-gravity hierarchy')
ax.grid(alpha=.22);ax.legend();fig.tight_layout();fig.savefig(FIG/'04_induced_gravity_hierarchy.png',dpi=160);plt.close(fig)

fig,ax=plt.subplots(figsize=(8.2,5.2))
co=np.array([qcd_beta_over_2g(float(a),5) for a in alpha_grid])
ax.plot(alpha_grid,co,label=r'QCD gauge trace coefficient $\beta(g)/(2g)$')
ax.axvline(ALPHA_S_MZ,ls='--',label='reference input')
ax.set(xlabel='Strong coupling alpha_s',ylabel='Coefficient of renormalized G^a_mn G^(a,mn)',
       title='One-loop QCD trace anomaly: operator coefficient, not a proton mass fraction')
ax.grid(alpha=.22);ax.legend();fig.tight_layout();fig.savefig(FIG/'05_trace_anomaly_coefficient.png',dpi=160);plt.close(fig)

print(json.dumps({'one_loop_Lambda5_GeV':inputs['one_loop_Lambda5_GeV'],
                  'Mbar_from_measured_G_GeV':inputs['Mbar_pl_from_G_GeV_not_a_prediction'],
                  'required_induced_zeta':inputs['required_zeta_if_v_eq_one_loop_Lambda5'],
                  'RG_max_recompute_error':inputs['independent_regression']['RG_invariant_max_relative_deviation'],
                  'status':'all five fundamental OPEN remain OPEN'},ensure_ascii=False,indent=2))
