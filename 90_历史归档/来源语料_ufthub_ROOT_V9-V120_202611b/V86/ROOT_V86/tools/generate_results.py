#!/usr/bin/env python3
"""Reproducible V86 model experiments: SYNTHETIC data only."""
from pathlib import Path
import sys,csv,json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.physics import G, EARTH_R, EARTH_MU, EARTH_J2,gravity,q_shape,eotvos_eta,normalized_D
from src.geometry import layered_envelope
from src.inference import correlated_cov,fit_shape_profiles,rank_one_bootstrap,gls_fit
P=ROOT/'results';P.mkdir(exist_ok=True)
D=ROOT/'data';D.mkdir(exist_ok=True)
SEED=20261118
rng=np.random.default_rng(SEED)

def jsave(name, obj):
    def clean(a):
        if isinstance(a,np.ndarray): return a.tolist()
        if isinstance(a,np.generic):return a.item()
        if isinstance(a,dict):return {k:clean(v) for k,v in a.items()}
        if isinstance(a,list):return [clean(v) for v in a]
        if isinstance(a,tuple):return [clean(v) for v in a]
        return a
    (P/name).write_text(json.dumps(clean(obj),ensure_ascii=False,indent=2,allow_nan=False),encoding='utf8')

def csvsave(name,head,rows):
    with (D/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(head);w.writerows(rows)

# 1 Earth J2 versus false Yukawa shape at exactly one surface point.
r=EARTH_R;mu=EARTH_MU
q_eq=q_shape(mu,r,r,EARTH_J2,math.pi/2)
q_pole=q_shape(mu,r,r,EARTH_J2,0)
alpha_mimic=brentq(lambda a:q_shape(mu,r,alpha=a,length=r)-q_eq,0,.1)
q_pole_mimic=q_shape(mu,r,alpha=alpha_mimic,length=r)
jsave('j2_false_positive.json',{'type':'known_J2_model_not_new_force','Earth_J2':EARTH_J2,
    'Earth_R_m':EARTH_R,'q_equator':q_eq,'q_pole':q_pole,'Yukawa_alpha_matching_single_equator_Q':alpha_mimic,
    'Yukawa_Q_pole_prediction':q_pole_mimic,'warning':'Equivalent Q at one point is NOT equivalent to same angular response'})
xs=np.linspace(1.0,4.0,150)
qeq=[q_shape(mu,float(t*r),r,EARTH_J2,math.pi/2) for t in xs]
qp=[q_shape(mu,float(t*r),r,EARTH_J2,0) for t in xs]
qy=[q_shape(mu,float(t*r),alpha=alpha_mimic,length=r) for t in xs]
csvsave('J2_false_positive_SYNTHETIC.csv',['r_over_R','Q_equator_J2','Q_pole_J2','Q_fitted_Yukawa'],zip(xs,qeq,qp,qy))
fig,ax=plt.subplots(figsize=(8.7,4.7));ax.plot(xs,qeq,label='Known Earth J2: equatorial ray');ax.plot(xs,qp,label='Known Earth J2: polar ray');ax.plot(xs,qy,'--',label='Fitted point Yukawa at r=R, one ray');ax.axhline(1,color='grey',ls=':');ax.set(xlabel='r / Earth equatorial radius',ylabel='Radial shape Q',title='One-point Q can be mimicked; angular check breaks this example');ax.legend(fontsize=8);ax.grid(alpha=.2);fig.tight_layout();fig.savefig(P/'earth_J2_fake_yukawa.png',dpi=145);plt.close(fig)

# 2 Rank-one D versus exact eta: direct counterexample.
qs=[.2,.5,1.1]
pairs=[(.2,.7),(.2,1.4),(.5,1.7)]
Dd=np.array([[normalized_D(qs_,qi,qj,1.1,1,1) for qi,qj in pairs] for qs_ in qs])
Et=np.array([[eotvos_eta(qs_,qi,qj,1.1,1,1) for qi,qj in pairs] for qs_ in qs])
sd=np.linalg.svd(Dd,compute_uv=False);se=np.linalg.svd(Et,compute_uv=False)
jsave('normalization_counterexample.json',{'q_sources':qs,'material_pairs':pairs,
    'D_exact_matrix':Dd,'eta_exact_matrix':Et,'D_singular_values':sd,'eta_singular_values':se,
    'note':'Exact eta is nonlinear in pair sum. Rank(D)<=1, but rank(eta) may exceed 1.'})
csvsave('rank_vs_eta_SYNTHETIC.csv',['source','D_a','D_b','D_c','eta_a','eta_b','eta_c'],[[i,*Dd[i],*Et[i]] for i in range(len(qs))])
fig,axes=plt.subplots(1,2,figsize=(9,4));im=axes[0].imshow(Dd,cmap='viridis');axes[0].set_title('Exact normalized D (rank 1)');fig.colorbar(im,ax=axes[0]);im2=axes[1].imshow(Et,cmap='viridis');axes[1].set_title('Exact Eotvos eta (not rank 1)');fig.colorbar(im2,ax=axes[1]);fig.tight_layout();fig.savefig(P/'D_vs_eta_rank.png',dpi=145);plt.close(fig)

# 3 Rank bootstrap with correlated, known covariance; synthetic null and two-mediator alt.
u=np.array([.65,1.,1.4]);v=np.array([.35,.9,-.25,1.2]);true1=np.outer(u,v)
u2=np.array([1.1,-.6,.8]);v2=np.array([.4,-.7,.6,.3]);true2=true1+.6*np.outer(u2,v2)
noise_sigma=.025;nobs=true1.size
correl=correlated_cov(nobs,noise_sigma,.35,common=.4)
L=np.linalg.cholesky(correl)
# identical randomized noise for sharp model contrast, known covariance
noise=(L@rng.normal(size=nobs)).reshape(true1.shape)
observed_null=true1+noise; observed_two=true2+noise
boot_null=rank_one_bootstrap(observed_null,correl,B=160,seed=12)
boot_two=rank_one_bootstrap(observed_two,correl,B=160,seed=12)
jsave('rank_bootstrap_SYNTHETIC.json',{'seed':SEED,'null':{k:v for k,v in boot_null.items() if k!='fitted_rank_one'},
  'two_mediator':{k:v for k,v in boot_two.items() if k!='fitted_rank_one'},
  'noise_covariance':correl,'observed_null':observed_null,'observed_two_mediator':observed_two,
  'not_a_real_experiment':True})
csvsave('rank_correlated_noise_SYNTHETIC.csv',['source_idx','pair_idx','null','two_mediator','truth_null','truth_two'],
    [[i,j,observed_null[i,j],observed_two[i,j],true1[i,j],true2[i,j]] for i in range(3) for j in range(4)])

# 4 Profile lambda scans with covariant noise; mu and Yukawa amplitude jointly fitted.
radius=.04
rs=np.array([.15,.19,.24,.30,.39,.51,.65,.84,1.08,1.38,1.8])
mu_true=G*100.; alpha_true=.06; length_true=.38
truth=np.array([gravity(mu_true,float(rr),radius=radius,alpha=alpha_true,length=length_true) for rr in rs])
# Gaussian model correlated in absolute acceleration; no hardware claim
cov=correlated_cov(len(rs),6e-11,.55,.25)
measure=truth+np.linalg.cholesky(cov)@rng.normal(size=len(rs))
lengths=np.logspace(-2,2,70)
profile=fit_shape_profiles(rs,measure,cov,lengths,radius=radius)
# Null model fit contains only standard Newton model amplitude
null=gls_fit((1/rs**2)[:,None],measure,cov)
best=min(profile,key=lambda x:x['chi2'])
jsave('range_profile_SYNTHETIC.json',{'rng_seed':SEED,'truth':{'M_kg':100,'mu':mu_true,'alpha':alpha_true,'lambda_m':length_true},
 'null_newton_chi2':null['chi2'],'best_profile':best,'warning':'scanned lambda; naive fixed-lambda chi-squared p-values invalid without trials correction',
 'range_table':profile,'all_data_are_synthetic':True})
csvsave('range_profile_SYNTHETIC.csv',['lambda_m','mu_fit','alpha_fit','chi2','condition'],
        [[p[k] for k in ['length','mu','alpha','chi2','condition']] for p in profile])
csvsave('raw_radial_measurements_SYNTHETIC.csv',['r_m','g_truth_ms2','g_mock_ms2','noise_std_ms2'],
    zip(rs,truth,measure,np.sqrt(np.diag(cov))))
fig,ax=plt.subplots(figsize=(8.6,4.6));ax.plot(lengths,[p['chi2'] for p in profile]);ax.axhline(null['chi2'],ls='--',label='Newton-only fit chi²');ax.axvline(length_true,ls=':',label='Injected range (synthetic)');ax.set_xscale('log');ax.set(xlabel='Hypothetical interaction range lambda (m)',ylabel='GLS profile chi-square',title='Joint nuisance scale fit, with correlated synthetic noise');ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(P/'range_GLS_profile.png',dpi=145);plt.close(fig)

# 5 layered form factor, independent from arbitrary source q_src fixed.
shells1=[(0,.03,5,1),(.03,.06,2,1)]
shells2=[(0,.03,5,3),(.03,.06,2,.4)]
lamgrid=np.logspace(-2,1,100)
la=[layered_envelope(shells1,.1,float(l)) for l in lamgrid]
lb=[layered_envelope(shells2,.1,float(l)) for l in lamgrid]
jsave('layered_source_example.json',{'shells_uniform_charge':shells1,'shells_composition_gradient':shells2,
 'r_m':.1,'lambda_m':.05,'envelopes_at_5cm':{'uniform':layered_envelope(shells1,.1,.05),
 'stratified':layered_envelope(shells2,.1,.05)},'warning':'synthetic model charges not measured compositions'})
csvsave('layered_source_SYNTHETIC.csv',['lambda_m','uniform_charge','stratified_charge'],zip(lamgrid,la,lb))
fig,ax=plt.subplots(figsize=(8,4.5));ax.loglog(lamgrid,la,label='Charge follows mass in shells');ax.loglog(lamgrid,lb,label='Different hypothetical scalar charges');ax.set(xlabel='Hypothetical range lambda (m)',ylabel='Normalized Yukawa envelope',title='Equal mass profile, different hypothetical source charges');ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(P/'layered_source_effect.png',dpi=145);plt.close(fig)

# 6 Experimental constraints metadata, not fit to original raw data
jsave('reference_constraints.json',{'type':'published_reference_NOT_a_fit_to_raw_data',
   'NIST_G_2022':{'value':G,'standard_uncertainty':1.5e-15,'unit':'m3 kg-1 s-2', 'url':'https://physics.nist.gov/cuu/Constants/'},
   'MICROSCOPE_TiPt_eta':{'estimate':-1.5e-15,'stat_sigma':2.3e-15,'syst_sigma':1.5e-15,
    'url':'https://pubmed.ncbi.nlm.nih.gov/36179190/'},
   'PDG_2026_LLR_Gdot_over_G':{'estimate':-5e-15,'uncertainty':9.6e-15,'unit':'yr-1',
    'source':'PDG 2026 Experimental Tests of Gravitational Theory, eq. 21.56'},
   'Nature_2024_mass_attraction':{'measurement':33.3,'stat_sigma':5.6,'syst_sigma':2.7,
    'unit':'nm/s2','url':'https://www.nature.com/articles/s41586-024-07561-3'}})
summary={'version':'V86','status':'mathematical methods & synthetic simulations only',
  'Earth_J2_Q_eq':q_eq,'Earth_J2_Q_pole':q_pole,'Yukawa_alpha_single_equator_mimic':alpha_mimic,
  'D_singular_ratio_2_1':float(sd[1]/sd[0]),'eta_singular_ratio_2_1':float(se[1]/se[0]),
  'bootstrap_null_p':boot_null['bootstrap_p'],'bootstrap_two_mediator_p':boot_two['bootstrap_p'],
  'profile_best_length':best['length'],'profile_true_length':length_true,
  'profile_best_chi2':best['chi2'],'profile_null_chi2':null['chi2'],
  'note':'All detector outputs are fixed-seed synthetic. No new-force measurement, no independent G or four-force proof.'}
jsave('numerical_summary.json',summary)
print(json.dumps(summary,indent=2))
