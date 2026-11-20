"""Generate only THEORY or SYNTHETIC records. No real experiment is performed."""
from pathlib import Path
import json, csv, math
import numpy as np
import mpmath as mp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.root_v91 import (Geometry,G,HBAR, newton_kernel,yukawa_delta_integral,
                          rigorous_delta_bounds, derivative_mu,
                          stable_shape_separation,polynomial_nuisance_projection,
                          nuisance_marginalized_fisher,legacy_audit,scalar_force_relative)

ROOT=Path(__file__).resolve().parents[1]
mp.mp.dps=100
def exact_high_precision(d,a,b,lam):
    md,ma,mb,ml=(mp.mpf(str(v)) for v in (d,a,b,lam))
    rr=[md+(ma-mb)/2,md+(ma+mb)/2,md-(ma+mb)/2,md+(mb-ma)/2]
    w=(1,-1,-1,1)
    fn=mp.fsum(s/r for s,r in zip(w,rr))
    fy=mp.fsum(s*mp.exp(-r/ml)/r for s,r in zip(w,rr))
    return fy-fn

geo=Geometry(450e-6,200e-6,200e-6)
lam_list=[1e-4,3e-4,1e-3,1e-2,1e-1,1.,1e2,1e6]
precision=[]
for lam in lam_list:
    stable=yukawa_delta_integral(geo,lam,96)
    independent=exact_high_precision(geo.d,geo.a,geo.b,lam)
    rel=float(abs((mp.mpf(str(stable))-independent)/independent))
    lo,hi=rigorous_delta_bounds(geo,lam)
    precision.append(dict(lambda_m=lam,stable_double=stable,independent_100_digits=mp.nstr(independent,65),
                          relative_disagreement=rel,lower_bound=lo,upper_bound=hi,
                          inside_analytic_bounds=lo*(1-1e-11)<=stable<=hi*(1+1e-11)))
    if rel>2e-10:raise AssertionError(f'100 digit cross validation failed: {lam} rel={rel}')
(ROOT/'results/independent_100_digit_precision.json').write_text(json.dumps({'precision_digits':100,'data_type':'THEORY',
    'data':precision,'max_relative_disagreement':max(p['relative_disagreement'] for p in precision)},indent=2,ensure_ascii=False),encoding='utf-8')

ds=np.array([450,550,650,850,1100,1300,1700])*1e-6
factor=G*(1e-14)**2/HBAR
sig_noise=1e-4
rho=0.35
cov=sig_noise**2*((1-rho)*np.eye(len(ds))+rho*np.ones((len(ds),len(ds))))

scan=[]
for lam in np.geomspace(8e-5,10.,151):
    vals=[]
    gs=[Geometry(float(d),200e-6,200e-6) for d in ds]
    signal=factor*np.array([yukawa_delta_integral(g,float(lam)) for g in gs])
    newton=factor*np.array([newton_kernel(g) for g in gs])
    for deg in [-1,0,1,2]:
        residual,_=polynomial_nuisance_projection(ds,200e-6,200e-6,float(lam),deg)
        # Use explicit physical column scaling: GLS whitened nuisance, float stable when lam large
        B=[newton]
        z=(ds-ds.mean())/np.ptp(ds)
        for k in range(deg+1):B.append(z**k)
        B=np.column_stack(B)
        fisher=nuisance_marginalized_fisher(signal,B,cov)
        vals.append((residual,math.sqrt(fisher)))
    sep,_,_=stable_shape_separation(ds,200e-6,200e-6,float(lam))
    scan.append(dict(lambda_m=float(lam),shape_ratio=sep,degree_minus1_residual=vals[0][0],
       degree0_residual=vals[1][0],degree1_residual=vals[2][0],degree2_residual=vals[3][0],
       degree_minus1_SNR_alpha1=vals[0][1],degree0_SNR_alpha1=vals[1][1],
       degree1_SNR_alpha1=vals[2][1],degree2_SNR_alpha1=vals[3][1]))
with (ROOT/'results/151_point_IDENTIFIABILITY_THEORY.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(scan[0].keys()));writer.writeheader();writer.writerows(scan)

plt.figure(figsize=(8,5))
for deg,key in [(-1,'degree_minus1_residual'),(0,'degree0_residual'),(1,'degree1_residual'),(2,'degree2_residual')]:
    plt.loglog([p['lambda_m'] for p in scan],[p[key] for p in scan],label=f'nuisance degree {deg}')
plt.xlabel('Yukawa range λ (m)')
plt.ylabel('Residual kernel norm (m⁻¹)')
plt.title('ROOT V91: nuisance projection suppresses the long-range signal')
plt.legend();plt.grid(True,which='both',alpha=.25)
plt.tight_layout();plt.savefig(ROOT/'plots/polynomial_nuisance_scaling_THEORY.png',dpi=160);plt.close()

plt.figure(figsize=(8,5))
for deg,key in [(-1,'degree_minus1_SNR_alpha1'),(0,'degree0_SNR_alpha1'),(1,'degree1_SNR_alpha1'),(2,'degree2_SNR_alpha1')]:
    plt.loglog([p['lambda_m'] for p in scan],[max(p[key],1e-25) for p in scan],label=f'nuisance degree {deg}')
plt.axhline(1,linestyle='--',alpha=.7,label='SNR=1 (toy model)')
plt.xlabel('Yukawa range λ (m)')
plt.ylabel('Assumed SNR for α=1, correlated σ=1e−4 rad')
plt.title('ROOT V91: illustrative synthetic Fisher sensitivity (NOT apparatus)')
plt.legend();plt.grid(True,which='both',alpha=.25)
plt.tight_layout();plt.savefig(ROOT/'plots/synthetic_noise_fisher_THEORY.png',dpi=160);plt.close()

# Predefined scoped candidate scalar: universal Einstein-frame field; no fitted/excluded parameters asserted.
scalar=[]
for beta in [0.,0.01,0.05,0.1]:
    alpha=2*beta**2
    for r in [1e-4,3e-4,1e-3,1e-2]:
        scalar.append(dict(beta=beta,alpha=alpha,r_m=r,lambda_m=1e-3,force_over_Newton=scalar_force_relative(alpha,r,1e-3),type='THEORY'))
with (ROOT/'results/scalar_candidate_THEORY.csv').open('w',encoding='utf-8-sig',newline='') as f:
    wr=csv.DictWriter(f,fieldnames=list(scalar[0].keys()));wr.writeheader();wr.writerows(scalar)

summary={'date':'2026-11-18','stage':'ROOT V91 model-level new theorem and repairs, not four-force unification',
    'source':'ROOT V90 uploaded archive and V89 session transcript',
    'real_measurements':0, 'independent_precision_digits':100,
    'precision_cases':len(precision),'max_relative_precision_disagreement':max(p['relative_disagreement'] for p in precision),
    'scanned_ranges':len(scan),'hypothetical_noise_sigma_rad':sig_noise,
    'hypothetical_noise_common_correlation':rho,
    'hypothetical_scatter_model':'Gaussian correlated phase observations; no real device specification',
    'example_lambda_1mm':min(scan,key=lambda p:abs(p['lambda_m']-1e-3)),
    'legacy_equation_audit':legacy_audit(),
    'theory_claims':{'exact_yukawa_monotonicity':True,'exact_yukawa_gap_bound':True,
     'nuisance_degree_asymptotic_suppression':True,
     'proved_four_force_unification':False,'derived_G_without_experimental_input':False,
     'observed_quantum_gravity':False,'observed_fifth_force':False}}
(ROOT/'results/numerical_summary_THEORY.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'precision':len(precision),'max_rel':summary['max_relative_precision_disagreement'],
                  'lambda_scan':len(scan),'real_measurements':0},ensure_ascii=False))
