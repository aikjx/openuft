#!/usr/bin/env python3
"""Generate deterministic, synthetic ROOT V121 calculations; not real data analysis."""
from __future__ import annotations
from pathlib import Path
import csv, json, hashlib, math, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import rootv121 as m
from rootv120 import ELL_PRE_REGISTERED, ground_fraction, apparent_gm

ROOT=Path(__file__).resolve().parent.parent
RES=ROOT/'results'; FIG=ROOT/'figures'
RES.mkdir(exist_ok=True); FIG.mkdir(exist_ok=True)

def dumpcsv(path,items):
    if not items:return
    with path.open('w',encoding='utf8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(items[0]))
        writer.writeheader();writer.writerows(items)

def noise_mc(N=12000,seed=20261121):
    rng=np.random.default_rng(seed)
    h=np.arange(6)*50000.
    base=apparent_gm(h,ELL_PRE_REGISTERED)
    rows=[]
    for sd in [1e-9,1e-8,1e-7]:
        for corr_name in ['independent','common_mode_80pct','AR1_80pct']:
            if corr_name=='independent':corr=np.eye(6)
            elif corr_name=='common_mode_80pct':corr=.2*np.eye(6)+.8*np.ones((6,6))
            else:corr=.8**np.abs(np.subtract.outer(np.arange(6),np.arange(6)))
            zz=rng.normal(size=(N,6))@np.linalg.cholesky(corr).T
            K=base+sd*zz
            D=np.diff(K,axis=1)
            H=np.array([D[:,i]*D[:,i+2]-D[:,i+1]**2 for i in range(3)]).T
            J=D[:,0]*D[:,3]-D[:,1]*D[:,2]
            q=np.divide(J,2*H[:,0],out=np.full(N,np.nan),where=H[:,0]!=0)
            flags=(q>0)&(q<1)
            p5=D[:,0]*J*J-4*D[:,1]*J*H[:,0]+4*D[:,2]*H[:,0]**2
            rows.append({'noise_std':sd,'correlation':corr_name,'trials':N,
                         'H0_wrong_positive_frequency':float(np.mean(H[:,0]>0)),
                         'three_H_negative_frequency':float(np.mean(np.all(H<0,axis=1))),
                         'five_point_0_q_1_frequency':float(np.mean(flags)),
                         'median_abs_P5':float(np.median(abs(p5))),
                         'mean_sample_correlation_off_diag':float(np.mean(corr[np.triu_indices(6,1)]))})
    return rows


def main():
    h=[0,50000,100000,150000,200000,250000,300000,400000,500000,710000,1000000]
    pred=m.fixed_prediction_table(h)
    dumpcsv(RES/'fixed_candidate_altitudes.csv',pred)
    ratios=[{'first_altitude_km':a/1000,'second_altitude_km':b/1000,
             'K_ratio_minus_1':m.mu_free_altitude_ratio(a,b)-1}
            for a,b in [(0,400000),(250000,400000),(250000,500000),
                        (400000,500000),(400000,710000)]]
    dumpcsv(RES/'normalization_free_ratios.csv',ratios)
    double=m.two_scale_counterexamples()
    dumpcsv(RES/'double_range_counterexamples.csv',double)
    mc=noise_mc()
    dumpcsv(RES/'correlated_noise_monte_carlo.csv',mc)
    stats={'study_id':'ROOT-V121-2026-11-21',
           'status':'NO GRAND UNIFICATION PROOF; NO REAL FIFTH FORCE DATA',
           'measurements':'SYNTHETIC ONLY',
           'source_density':'Fayet 2026 simplified radial density model',
           'alpha_y':m.ALPHA_PRE_REGISTERED,'ell_m':m.ELL_PRE_REGISTERED,
           'epsilon_surface':ground_fraction(),
           'ratio_250_400_minus_1':m.mu_free_altitude_ratio(250000,400000)-1,
           'slope_400':m.log_slope_K(400000),
           'precession_400_rad':m.precession_from_slope(m.log_slope_K(400000)),
           'extra_clock_ground_to_400':m.extra_clock_shift(0,400000,m.ELL_PRE_REGISTERED,ground_fraction()),
           'alpha_identity_audit':m.alpha_numerology_audit(),
           'proton_ratio_audit':m.proton_ratio_audit(),
           'kk_mass_example_gap':m.proton_ratio_audit()['gap_to_integer'],
           'fifth_force_two_range_examples':double,
           'mc_parameters':{'n_per_case':12000,'seed':20261121,'covariance_cases':3,'noise_levels':[1e-9,1e-8,1e-7]}}
    (RES/'summary.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf8')
    x=np.linspace(0,1200e3,251)
    fig,ax=plt.subplots(figsize=(9,5));ax.semilogy(x/1000,100*m.yukawa_epsilon(x))
    ax.set_xlabel('Height above assumed Earth radius (km)');ax.set_ylabel('Predicted extra radial acceleration (%)')
    ax.set_title('ROOT V121: preregistered Yukawa candidate (NOT observations)')
    ax.grid(True,alpha=.4);fig.tight_layout();fig.savefig(FIG/'altitude_fraction.png',dpi=180);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,5));ax.plot(x/1000,[m.log_slope_K(v) for v in x]);
    ax.set_xlabel('Height above assumed Earth radius (km)');ax.set_ylabel('S = d ln K / d ln r')
    ax.set_title('A normalization-invariant radial slope forecast (NOT observed)')
    ax.grid(True,alpha=.4);fig.tight_layout();fig.savefig(FIG/'radial_log_slope.png',dpi=180);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,5))
    labs=['independent','common_mode_80pct','AR1_80pct']; xx=np.arange(3)
    for sd in [1e-9,1e-8,1e-7]:
        sample=[q['H0_wrong_positive_frequency'] for q in mc if q['noise_std']==sd]
        ax.plot(xx,sample,marker='o',label=f'noise={sd:.0e}')
    ax.set_xticks(xx,labs);ax.set_ylabel('Fraction of trials: H0 > 0 (wrong sign)')
    ax.set_title('Synthetic Monte Carlo / 12,000 trials per configuration')
    ax.grid(True,alpha=.4);ax.legend();fig.tight_layout();fig.savefig(FIG/'noise_correlation_stress.png',dpi=180);plt.close(fig)
    print(json.dumps({'generated':str(RES), 'candidate_eps_400':float(m.yukawa_epsilon(400000)),
                      'altitude_ratio_250_400':stats['ratio_250_400_minus_1'],
                      'slope_400':stats['slope_400'],
                      'precession_400':stats['precession_400_rad'],
                      'fine_structure_sigma':stats['alpha_identity_audit']['difference_in_CODATA_std'],
                      'monte_carlo_rows':len(mc)},indent=2))

if __name__=='__main__':main()
