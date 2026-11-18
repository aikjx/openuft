"""Produce deterministic synthetic observations, analytic checks, plots and JSON results."""
from pathlib import Path
import json,csv,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from rootv72.physics import environments,C,HBAR,G
from rootv72.experiment import generate,fit,null_false_positive_trial_count,four_state_drift_quadratic
from rootv72.holonomy import su2,plaquette,curvature
BASE=Path(__file__).resolve().parent
for dirn in ['data','results','plots']: (BASE/dirn).mkdir(exist_ok=True)

def csvwrite(name,rows):
    if not rows:return
    with (BASE/'data'/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

rows=generate()
result=fit(rows)
envs=environments()
csvwrite('V72_合成双反转观测_不是实测.csv',rows)
csvwrite('V72_星体引力与自转近似.csv',envs)
A,B=su2();F=curvature(A,B)
errs=[]
for size in np.geomspace(.005,.3,40):
    err=float(np.linalg.norm((plaquette(A,B,size)-np.eye(2))/size**2-F))
    errs.append({'edge':float(size),'curvature_error':err})
csvwrite('V72_微环路曲率收敛.csv',errs)
# N scalar fields, minimal coupling, cutoff scale inferred FROM measured G, NOT G prediction.
scales=[]
for n in [1,2,3,4,8,16,32,64,128]:
    ell=math.sqrt(n*HBAR*G/(12*math.pi*C**3))
    scales.append({'N_scalar':n,'calibrated_length_m':ell})
csvwrite('V72_诱导引力反向标定_不是预测.csv',scales)
false_count=null_false_positive_trial_count()
output={'status':'CONDITIONAL_MODEL_NOT_PROOF','n_synthetic_measurements':len(rows)*4,
 'number_of_contrasts':len(rows),'injected_beta':3e-15,'estimated_beta':result.beta,
 'estimated_hs_artifact':result.nuisance_hs,'one_sigma_se_known_noise':result.se,
 'z_injected_synthetic':result.z,'p_injected_synthetic':result.p_two_sided,
 'rank':result.rank,'condition':result.condition,'null_false_positives_120_trials':false_count,
 'null_false_positive_fraction':false_count/120,
 'quadratic_time_drift_fakes_hs_contrast':four_state_drift_quadratic(1e-15),
 'holonomy_error_edge_0_005':errs[0]['curvature_error'],
 'holonomy_error_edge_0_3':errs[-1]['curvature_error'],
 'G_measured_input':G,'planets':envs,'induced_gravity_fitted_scales':scales,
 'scientific_limitations':['synthetic experiment only','not a measurement of fifth force',
 'holonomy is a geometric unification of notation, not dynamics','G not predicted',
 'unknown hs-dependent systematic tracking X is unidentifiable']}
(BASE/'results'/'numerical_summary.json').write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf-8')

plt.figure(figsize=(8,4.6))
group={}
for v in rows:group.setdefault(v['x'],[]).append(v['contrast'])
xs=np.array(sorted(group));ys=np.array([np.mean(group[x]) for x in xs]);ses=np.array([np.std(group[x],ddof=1)/np.sqrt(len(group[x])) for x in xs])
plt.errorbar(xs,ys*1e15,yerr=ses*1e15,fmt='o',label='synthetic contrasts')
plt.plot(xs,(result.nuisance_hs+result.beta*xs)*1e15,label='OLS fit')
plt.xlabel('synthetic environment feature X');plt.ylabel('double-reversal contrast (1e-15)');plt.title('ROOT V72: simulated injection/recovery ONLY');plt.legend();plt.tight_layout();plt.savefig(BASE/'plots'/'01_double_reversal_synthetic.png',dpi=160);plt.close()
plt.figure(figsize=(7,4.5));plt.loglog([v['edge'] for v in errs],[v['curvature_error'] for v in errs]);plt.xlabel('plaquette edge');plt.ylabel('norm error in curvature approximation');plt.title('SO(3)/SU(2) holonomy convergence (toy math)');plt.tight_layout();plt.savefig(BASE/'plots'/'02_holonomy_convergence.png',dpi=160);plt.close()
plt.figure(figsize=(7,4.5));plt.bar(['Sun','Earth','Moon','Mars','Jupiter'],[v['g_m_s2'] for v in envs]);plt.ylabel('spherical g (m/s^2)');plt.title('Model body gravity: G supplied from CODATA');plt.tight_layout();plt.savefig(BASE/'plots'/'03_planet_gravity.png',dpi=160);plt.close()
plt.figure(figsize=(7,4.5));plt.plot([v['N_scalar'] for v in scales],[v['calibrated_length_m']/1e-35 for v in scales],'o-');plt.xlabel('hypothetical number of scalar fields N');plt.ylabel('calibrated cutoff length (10^-35 m)');plt.title('G back-fitting degeneracy — NOT an independent prediction');plt.tight_layout();plt.savefig(BASE/'plots'/'04_G_degeneracy.png',dpi=160);plt.close()
print(json.dumps({k:output[k] for k in ('estimated_beta','one_sigma_se_known_noise','null_false_positive_fraction','number_of_contrasts','rank')},ensure_ascii=False,indent=2))
