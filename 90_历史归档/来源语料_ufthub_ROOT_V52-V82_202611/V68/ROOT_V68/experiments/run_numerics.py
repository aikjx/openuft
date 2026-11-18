"""Generate ROOT V68 numeric results, plots and independent SciPy crosschecks.
Run: python experiments/run_numerics.py (from package root)
"""
import csv,json, math, pathlib, sys
from statistics import mean
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.root_v68 import *
from scipy.special import exp1
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT=ROOT/'results'; DAT=ROOT/'data'
OUT.mkdir(exist_ok=True);DAT.mkdir(exist_ok=True)

def save_csv(name,headers,rows):
    p=DAT/name
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(headers);w.writerows(rows)

def plot_save(filename, title, xlabel, ylabel, curves, logx=False,logy=False):
    fig,ax=plt.subplots(figsize=(9,5.4))
    for x,y,label in curves:ax.plot(x,y,label=label)
    ax.set(title=title,xlabel=xlabel,ylabel=ylabel)
    if logx:ax.set_xscale('log')
    if logy:ax.set_yscale('log')
    ax.grid(True,alpha=.25);ax.legend();fig.tight_layout()
    fig.savefig(OUT/filename,dpi=155);plt.close(fig)

# 1. gauge running and distinct pairwise intersections
scales=np.geomspace(MZ_GEV,1e19,240)
rg=np.array([rge_inv(float(s)) for s in scales])
save_csv('sm_one_loop_running.csv',('mu_GeV','alpha1_inverse','alpha2_inverse','alpha3_inverse'),
         ((float(x),*map(float,y)) for x,y in zip(scales,rg)))
plot_save('one_loop_running.png','Standard Model one-loop running (illustrative inputs)',
          'Energy scale (GeV)','Inverse gauge coupling',
          [(scales,rg[:,j],r'$\alpha_{%d}^{-1}$'%(j+1)) for j in range(3)],logx=True)

# 2. proper-time cutoff threshold; independent source: scipy.special.exp1
ms=np.concatenate(([0],np.geomspace(1e-5,8,220)))
fs=np.array([heat_kernel_f(float(m)) for m in ms]); fref=np.array([1 if m==0 else math.exp(-m*m)-m*m*exp1(m*m) for m in ms])
err=float(np.max(np.abs(fs-fref)))
save_csv('heat_kernel_threshold.csv',('mu_dimensionless','F_root','F_scipy','absolute_error'),
         ((float(m),float(y),float(z),float(abs(y-z))) for m,y,z in zip(ms,fs,fref)))
plot_save('heat_kernel_threshold.png','Proper-time regulator: scalar threshold function',
          'Mass × cutoff length (dimensionless)','F(mu)',[(ms,fs,'F(mu)')])

# 3. G degeneracy exact N=1..100, xi=0, bare term zero, m=0
Ns=np.arange(1,101,dtype=int)
lengths=np.array([reverse_fitted_length(int(n),0) for n in Ns])
Gpred=np.array([induced_g(int(n),0,float(e)) for n,e in zip(Ns,lengths)])
save_csv('induced_gravity_inverse_fit.csv',('N','fitted_length_m','G_reconstructed_SI','G_ratio'),
         ((int(n),float(e),float(g),float(g/G_OBS)) for n,e,g in zip(Ns,lengths,Gpred)))
plot_save('induced_gravity_degeneracy.png','Different N and fitted cutoff lengths reproduce the same G',
          'N (toy scalar species)','Cutoff length / Planck length',[(Ns,lengths/planck_length(),'Fitted length')])

# 4. helix geometry, fixed R=1, speed=1 in dimensionless units
angles=np.linspace(-85,85,171)
ks=np.array([helix(1,float(a),1)['kappa'] for a in angles]);taus=np.array([helix(1,float(a),1)['tau'] for a in angles])
save_csv('helix_geometry.csv',('lambda_degrees','curvature_per_R','torsion_per_R'),
         ((float(a),float(k),float(t)) for a,k,t in zip(angles,ks,taus)))
plot_save('helix_geometry.png','Exact helix geometry (R=1, v=1)',
          'Helix angle (degrees)','Inverse length',[(angles,ks,'Curvature'),(angles,taus,'Signed torsion')])

# 5. illustrative composition-dependent Yukawa field: not fit to real satellite orbit
lam=1.0e7;r=7.1e6;alpha_grid=np.linspace(-1e-13,1e-13,301)
qA=1.;qB=.8;qS=1.
etas=np.array([eotvos_eta(r,float(a),lam,qS,qA,qB) for a in alpha_grid])
bound=microscope_approx_envelope(2)
save_csv('illustrative_eotvos_yukawa.csv',('alpha_dimensionless','eta_toy','abs_eta_toy','illustrative_2sigma_envelope'),
         ((float(a),float(e),float(abs(e)),bound) for a,e in zip(alpha_grid,etas)))
plot_save('yukawa_eotvos_toy.png','Toy composition-sensitive fifth force vs reference sensitivity',
          'Toy coupling alpha','Illustrative Eotvos ratio',[(alpha_grid,etas,'eta toy'),
          (alpha_grid,alpha_grid*0+bound,'approx +2sigma envelope'),
          (alpha_grid,alpha_grid*0-bound,'approx -2sigma envelope')])

# 6. BD gamma with omega>0; use Cassini source only as approximate reference
oms=np.geomspace(.1,1e7,220)
gamdiff=np.array([abs(brans_dicke_gamma(float(w))-1) for w in oms])
save_csv('brans_dicke_gamma.csv',('omega_BD','abs_gamma_minus_one'),
         ((float(w),float(x)) for w,x in zip(oms,gamdiff)))
plot_save('brans_dicke_gamma.png','Massless Brans-Dicke PPN gamma (conditional model)',
          'omega_BD','|gamma-1|',[(oms,gamdiff,'BD prediction'),
          (oms,oms*0+2.3e-5,'Cassini 1-sigma reported uncertainty')],logx=True,logy=True)

check={
 'project':'ROOT V68',
 'result_status':'No proof of four-force unification; conditional and negative tests only',
 'G_CODATA2022_SI':G_OBS,
 'planck_length_from_measured_G_m':planck_length(),
 'inverse_fitted_cutoff_N1_xi0_m':reverse_fitted_length(1,0),
 'cutoff_length_is_reverse_fit':True,
 'one_loop_SM_pair_intersections_GeV':pair_intersections(),
 'one_loop_SM_best_least_squares_meeting':best_meeting(),
 'one_loop_SM_input_is_illustrative':True,
 'anomaly_coefficients':{k:str(v) for k,v in anomaly_coefficients().items()},
 'exact_standard_model_one_generation_anomaly_cancellation':True,
 'anomaly_cancellation_does_not_derive_particle_spectrum':True,
 'heat_kernel_max_absolute_discrepancy_from_scipy':err,
 'heat_kernel_uses_cutoff_and_no_bare_einstein_hilbert_term_if_fit':True,
 'approx_microscope_two_sigma_envelope_not_confidence_interval':bound,
 'new_experimental_detection':False,
 'original_G_prediction_without_empirical_parameters':False,
 'gauge_group_derived_from_helix_kinematics':False,
 'UV_complete_quantum_gravity_proven':False,
}
(OUT/'numerical_summary.json').write_text(json.dumps(check,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(check,indent=2,ensure_ascii=False))
