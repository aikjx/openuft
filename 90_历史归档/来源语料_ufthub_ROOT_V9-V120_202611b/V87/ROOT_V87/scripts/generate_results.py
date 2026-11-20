"""Deterministic computations and *synthetic* data; no experimental observations."""
from pathlib import Path
import sys,math,csv,json,datetime
root=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(root/'src'))
import bridge as b
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.integrate import quad

out=root/'results';out.mkdir(exist_ok=True)

def savecsv(name,header,rows):
    with (root/'data'/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(header);w.writerows(rows)

# 1: Physically meaningful example calculations.
M=100.;R=.30;T=1.;m=b.M_RB87
phase100nm=abs(b.phase_uniform(m,b.G_STD,1e-7,.001))
q=b.source_phase_design(M,R,.01,T,m,phase_noise_rad=.01)
clock_earth=b.clock_high_over_low_fractional(b.M_EARTH,b.R_EARTH,b.R_EARTH+1)
grad=b.consistency_triangle(b.M_EARTH,b.R_EARTH,b.R_EARTH+10,m,.01)

physical={
 'status':'THEORY_AND_SYNTHETIC_ONLY',
 'constants_source':'CODATA 2022 G and defined c,h; other masses illustrative',
 'planck_length_m':b.planck_length(),
 'planck_mass_kg':b.planck_mass(),
 'earth_newton_g_m_s2':b.acceleration(b.M_EARTH,b.R_EARTH),
 'earth_static_clock_1m_fractional':clock_earth,
 'earth_1m_redshift_weak_approx':b.acceleration(b.M_EARTH,b.R_EARTH)/b.C**2,
 'rb87_phase_for_100nm_1ms_earth_rad':phase100nm,
 'rb87_spherical_phase_source_100kg_0p3m_0p01m_1s':q,
 'earth_10m_phase_clock_triangle':grad,
 'mercury_precession_rad_orbit':b.perihelion_advance_rad(b.M_SUN,5.790905e10,.205630),
 'mercury_precession_arcsec_orbit':b.perihelion_advance_rad(b.M_SUN,5.790905e10,.205630)*180/math.pi*3600,
 'gaussian_SN_toy_mass_1e_minus_16_kg_radius_m':b.sn_variational_radius(1e-16),
 'earth_quantum_gravity_parameter_at_1m':b.epsilon_quantum_gravity(1),
 'electron_dimensionless_gravity_coupling':b.alpha_gravity(9.1093837139e-31),
 'source_phase_phase_noise_assumed_rad':.01,
 'source_phase_noise_assumed_not_instrument_verified':True,
 'physical_unification_proven':False,
 'G_independently_derived':False,
 'quantum_gravity_observed_in_this_package':False,
}
(out/'numerical_summary.json').write_text(json.dumps(physical,ensure_ascii=False,indent=2),encoding='utf8')

heights=np.geomspace(1e-8,.05,180)
phase_rows=[]
for h in heights:
    phase=b.phase_spherical(m,M,R,R+h,T)
    uni=b.phase_uniform(m,b.acceleration(M,R),h,T)
    phase_rows.append([float(h),phase,uni,phase/uni,b.phase_shape_ratio(R,float(h)),b.clock_high_over_low_fractional(b.M_EARTH,b.R_EARTH,b.R_EARTH+h)])
savecsv('phase_height_theory.csv',['height_m','rb87_source_phase_rad','uniform_approx_phase_rad','ratio_numeric','ratio_exact','earth_static_clock_fractional'],phase_rows)

# 2: Yukawa candidate relative ratio (not a measurement).
radii=np.linspace(.12,1.2,150)
ys=[]
for r in radii:
    ys.append([float(r),b.shape_yukawa(float(r),0,.35),b.shape_yukawa(float(r),.20,.35),
               b.acceleration_yukawa(100,float(r),.2,.35)/b.acceleration(100,float(r))])
savecsv('yukawa_candidate_curve.csv',['radius_m','Q_newton','Q_yukawa_alpha0p2_lambda0p35','g_ratio_candidate'],ys)

# 3: SN Gaussian ansatz, no claim of particle structure.
mtoy=1e-16; a0=b.sn_variational_radius(mtoy)
aa=a0*np.geomspace(.3,4,140)
snrows=[]
for a in aa:
    ke=b.gaussian_quantum_kinetic(mtoy,float(a));u=b.gaussian_grav_self_energy(mtoy,float(a))
    snrows.append([float(a),ke,u,ke+u,(ke+u)/abs(b.gaussian_grav_self_energy(mtoy,a0))])
savecsv('gaussian_SN_toy.csv',['a_m','kinetic_J','self_gravity_J','total_J','normalized_total'],snrows)

# 4: source-switching synthetic records with common-mode vibrational drift.
rng=np.random.default_rng(8701)
blocks=80
source_g=b.acceleration(M,R)
noise_floor=1.5e-9 # synthetic acceleration channel
rows=[]
for k in range(blocks):
    state=1 if rng.random()>.5 else -1
    sham=1 if rng.random()>.5 else -1
    # mechanical artifact deliberately correlated with a state, cancelled by sham only in ideal randomized model
    drift=2e-9*math.sin(2*math.pi*k/17.)
    noise=rng.normal(0,noise_floor)
    meas=state*source_g+drift+sham*.8e-9+noise
    rows.append([k,state,sham,meas,source_g*state,drift,noise,'SYNTHETIC'])
savecsv('synthetic_source_switch.csv',['block','source_state','sham_state','acceleration_m_s2','injected_gravity_m_s2','injected_drift_m_s2','noise_m_s2','provenance'],rows)

# 5: independent gaussian integral demonstration
mass_integral=mtoy*quad(lambda x:4/math.sqrt(math.pi)*x*x*math.exp(-x*x),0,15,epsabs=1e-13,epsrel=1e-13)[0]
u_integral=-(2/math.sqrt(math.pi))*b.G*mtoy*mtoy/a0*quad(lambda x:x*math.exp(-x*x)*math.erf(x),0,15,epsabs=1e-13,epsrel=1e-13)[0]
check={'normalization':mass_integral/mtoy,
       'gaussian_self_energy_ratio':u_integral/b.gaussian_grav_self_energy(mtoy,a0),
       'phase_exact_to_uniform':q['phase_rad']/q['uniform_approx_phase_rad'],
       'G_M_rank_deficiency':0.0,
       'all_results_theory_or_synthetic':True}
(out/'independent_integral_check.json').write_text(json.dumps(check,indent=2),encoding='utf8')

# Plot static curves, no forced colors.
plt.figure(figsize=(8.0,4.6));plt.semilogx(heights,[row[3] for row in phase_rows],label='Exact spherical phase / uniform phase')
plt.axhline(1,linestyle='--',label='Uniform approximation');plt.xlabel('Height separation (m)');plt.ylabel('Ratio');plt.title('Spherical source phase geometry (M=100 kg, R=0.30 m)');plt.legend();plt.tight_layout();plt.savefig(out/'phase_shape.png',dpi=150);plt.close()
plt.figure(figsize=(8.0,4.6));plt.plot(radii,[row[1] for row in ys],label='Newton Q=1');plt.plot(radii,[row[2] for row in ys],label='Hypothetical Yukawa Q, alpha=0.2, lambda=0.35 m')
plt.xlabel('Radius (m)');plt.ylabel('Radial shape Q');plt.title('Model discrimination — not observed data');plt.legend();plt.tight_layout();plt.savefig(out/'yukawa_shape.png',dpi=150);plt.close()
plt.figure(figsize=(8.0,4.6));plt.semilogx(aa/a0,[row[4] for row in snrows],label='Gaussian SN toy energy')
plt.axvline(1,linestyle='--',label='Variational extremum');plt.xlabel('Gaussian width a / a*');plt.ylabel('Energy / |W(a*)|');plt.title('Conditional Gaussian mean-field toy — not a particle prediction');plt.legend();plt.tight_layout();plt.savefig(out/'SN_variational_toy.png',dpi=150);plt.close()
plt.figure(figsize=(8.0,4.6));plt.plot([r[0] for r in rows],[r[3] for r in rows],label='Synthetic reading');plt.plot([r[0] for r in rows],[r[4] for r in rows],label='Injected source signal',alpha=.8)
plt.xlabel('Randomized block');plt.ylabel('Acceleration (m/s^2)');plt.title('SYNTHETIC randomized source-switch stress test');plt.legend();plt.tight_layout();plt.savefig(out/'synthetic_switch.png',dpi=150);plt.close()
print(json.dumps({'summary':physical,'independent_integral_check':check,'data_rows':{'phase':len(phase_rows),'yukawa':len(ys),'sn':len(snrows),'synthetic':len(rows)}},indent=2,ensure_ascii=False))
