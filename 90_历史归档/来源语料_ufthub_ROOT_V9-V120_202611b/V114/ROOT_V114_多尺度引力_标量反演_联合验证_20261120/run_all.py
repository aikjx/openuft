"""Generate fully reproducible ROOT V114 numerical evidence and charts.
Run from any cwd: python /path/to/ROOT_V114/run_all.py
"""
from pathlib import Path
import json,sys,math,csv
import numpy as np
from scipy.optimize import least_squares
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from src.v114 import *
FIG=ROOT/'figures';OUT=ROOT/'results'
FIG.mkdir(exist_ok=True);OUT.mkdir(exist_ok=True)
model=Model(1/3,AU);r1=.5*AU;r2=2*AU
single=[]
for rat in [.5,1,2,5]:
    rr=rat*AU
    gm=float(gamma_local(rr,model));force=float(force_enhancement(rr,model))
    a,lam=infer_one_radius(rr,gm,force)
    single.append({'distance_AU':rat,'gamma_local':gm,'G_force_over_Gstar':force,
                   'G_potential_over_Gstar':float(potential_enhancement(rr,model)),
                   'gamma_fitted_with_local_force_normalization':float(gamma_from_force_reference(rr,model)),
                   'a_inferred':a,'lambda_AU_inferred':lam/AU,
                   'joint_jacobian_det':float(joint_det_closed_form(rr,model)),
                   'joint_jacobian_cond':float(np.linalg.cond(joint_jacobian(rr,model)))})
y1=float(force_excess(r1,model));y2=float(force_excess(r2,model))
a2,lam2=solve_two_scales(r1,r2,y1,y2)
noise=synthetic_noise_demo(model,AU,n=1000,seed=20261120)
shapiro=shapiro_bare_delay_oneway(SUN_MASS,.01*AU,AU)
vals={'version':'ROOT V114','date':'2026-11-20',
      'status':'not a complete unified field theory; toy weak-field scalar--tensor consistency tests',
      'reference_assumptions':{
          'linear_isotropic_metric':True, 'universal_matter_coupling':True,
          'a_alpha_squared':1/3, 'lambda_AU':1,
          'independent_tensor_Gstar_mass_normalization_REQUIRED':True,
          'not_full_Cassini_reanalysis':True,
          'previous_396_issues_unchanged':True},
      'numerical_values':{
          'radii_channels':single,
          'two_scale':{'r1_AU':.5,'r2_AU':2,'force_excess_r1':y1,'force_excess_r2':y2,
                       'ratio':y2/y1,'a_inferred':a2,'lambda_AU_inferred':lam2/AU},
          'mass_energy_eV_for_1AU':scalar_energy_eV(AU),
          'scalar_free_wave_frequency_threshold_Hz':scalar_frequency_threshold_Hz(AU),
          'example_shapiro_oneway_delay_s_fixed_Gstar_M_Sun':shapiro,
          'synthetic_1000_noise_realizations_NOT_DATA':noise},
      'limitations':[
           'gamma_local is local linearized metric ratio, not constant PPN gamma in finite-range gravity',
           'Cassini full path+orbit analysis NOT carried out; no new experimental exclusion bounds',
           'lensing potential at fixed Gstar M cancels scalar, but dynamic mass calibration matters',
           'unknown tensor Gstar and source mass make inversion non-identifiable without external calibration',
           'free scalar wave propagation threshold is necessary, not sufficient for an observable GW signal',
           'no independent derivation of G or Standard Model spectrum or UV completion',
           'historical 396 OPEN issues remain OPEN unless independently proven']}
(OUT/'V114_RESULTS.json').write_text(json.dumps(vals,ensure_ascii=False,indent=2),encoding='utf-8')
with (OUT/'V114_WEAKFIELD_SCAN.csv').open('w',encoding='utf-8',newline='') as f:
    writer=csv.writer(f)
    writer.writerow(['r_AU','gamma_local','G_potential_over_Gstar','G_force_over_Gstar','gamma_from_force_reference'])
    for rat in np.geomspace(.05,30,250):
        r=rat*AU
        writer.writerow([f'{rat:.16g}',f'{float(gamma_local(r,model)):.16g}',
                         f'{float(potential_enhancement(r,model)):.16g}',
                         f'{float(force_enhancement(r,model)):.16g}',
                         f'{float(gamma_from_force_reference(r,model)):.16g}'])

# Chart 1: gamma vs distance for fixed coupling and different ranges
X=np.geomspace(.05,10,250)
plt.figure(figsize=(8,5))
for l in [.1,.5,1,5,1e5]:
    gg=gamma_local(X*AU,Model(1/3,l*AU))
    plt.semilogx(X,gg,label=('massless limit' if l==1e5 else f'lambda={l:g} AU'))
plt.xlabel('distance (AU)');plt.ylabel('local gamma = Psi/U')
plt.title('Scale-dependent metric ratio in restricted massive scalar gravity')
plt.ylim(.48,1.03);plt.grid(alpha=.25);plt.legend();plt.tight_layout()
plt.savefig(FIG/'01_local_gamma_scale.png',dpi=165);plt.close()

# Chart 2: one model, three different physical coefficients
plt.figure(figsize=(8,5))
plt.semilogx(X,potential_enhancement(X*AU,model),label='G_potential/Gstar')
plt.semilogx(X,force_enhancement(X*AU,model),label='G_force/Gstar')
plt.semilogx(X,2/(1+force_excess(X*AU,model))-1,label='gamma Shapiro toy-fit normalized by force')
plt.semilogx(X,gamma_local(X*AU,model),label='gamma local = Psi/U')
plt.xlabel('distance (AU)');plt.ylabel('dimensionless coefficient')
plt.title('Potential, force and finite-range metric ratio are NOT identical')
plt.grid(alpha=.25);plt.legend(fontsize=8);plt.tight_layout()
plt.savefig(FIG/'02_three_observable_separation.png',dpi=165);plt.close()

# Chart 3: ratio of two force-excess values uniquely resolves range in the model
L=np.geomspace(.05,100,300)
R=np.array([two_scale_ratio_from_m(r1,r2,1/(l*AU)) for l in L])
plt.figure(figsize=(8,5));plt.semilogx(L,R)
plt.axhline(y2/y1,ls='--',lw=1,label='synthetic observed ratio')
plt.axvline(1,ls=':',lw=1,label='true lambda=1AU')
plt.xlabel('scalar range lambda (AU)');plt.ylabel('Y(2 AU)/Y(0.5 AU)')
plt.title('Ratio eliminates coupling a, but loses sensitivity when range is huge')
plt.grid(alpha=.25);plt.legend();plt.tight_layout()
plt.savefig(FIG/'03_two_scale_inversion.png',dpi=165);plt.close()

# Chart 4: same-distance cross-channel Jacobian condition number
ls=np.geomspace(.025,500,350)
cond=np.array([np.linalg.cond(joint_jacobian(AU,Model(1/3,l*AU))) for l in ls])
plt.figure(figsize=(8,5));plt.loglog(ls,cond)
plt.xlabel('scalar range lambda (AU)');plt.ylabel('Jacobian condition number')
plt.title('Formal identifiability does not imply stable noisy inference')
plt.grid(alpha=.25);plt.tight_layout()
plt.savefig(FIG/'04_inverse_condition_number.png',dpi=165);plt.close()

# Chart 5: conformal scalar cancellation in lensing potential with independent tensor normalization
plt.figure(figsize=(8,5))
Z=np.geomspace(.05,10,250)
z=model.a*np.exp(-Z)
plt.semilogx(Z,1+z,label='temporal potential U / (Gstar M/r)')
plt.semilogx(Z,1-z,label='spatial potential Psi / (Gstar M/r)')
plt.semilogx(Z,np.full_like(Z,2),label='(U+Psi)/(Gstar M/r) = 2')
plt.xlabel('distance (AU)');plt.ylabel('normalized weak-field coefficient')
plt.title('Photon conformal cancellation at fixed tensor Gstar M')
plt.grid(alpha=.25);plt.legend();plt.tight_layout()
plt.savefig(FIG/'05_lensing_potential_cancellation.png',dpi=165);plt.close()

print(json.dumps({'a':a2,'lambda_AU':lam2/AU,'ratio':y2/y1,
    'single_radius_1AU_gamma':single[1]['gamma_local'],
    'single_radius_1AU_force':single[1]['G_force_over_Gstar'],
    'single_radius_1AU_gamma_fit':single[1]['gamma_fitted_with_local_force_normalization'],
    'scalar_mass_eV':scalar_energy_eV(AU),'threshold_Hz':scalar_frequency_threshold_Hz(AU),
    'noise_5_50_95_lambda_AU':noise['lam_AU_quantiles']},indent=2))
