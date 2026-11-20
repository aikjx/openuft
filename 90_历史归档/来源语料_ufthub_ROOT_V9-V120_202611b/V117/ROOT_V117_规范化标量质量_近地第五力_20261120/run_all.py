"""Recompute V117 scientific results and independent plots from project root."""
from pathlib import Path
import json,math,sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).resolve().parent))
from src import model as m
root=Path(__file__).resolve().parent
(root/'results').mkdir(exist_ok=True)
(root/'figures').mkdir(exist_ok=True)
v=m.V_QCD_GEV
xi=m.xi_from_newton_calibration()
a=m.alpha_xi(xi)
f=m.canonical_scale_f(v,xi)
entries=[]
for lam in [.001,.01,.1,1,4*math.pi,100]:
    ell=m.range_m(lam,v,xi)
    entries.append({'lambda4':lam,'mass_eV':m.canonical_mass_ev(lam,v,xi),
                    'range_km':ell/1000,
                    'uniform_surface_excess':m.yukawa_relative_force_sphere(ell,0,coupling=a),
                    'inverse_r_surface_excess':m.yukawa_relative_force_sphere(ell,0,coupling=a,profile='inverse_r')})
ell=m.range_m(1,v,xi)
heights=[0,10e3,50e3,100e3,200e3,500e3,1e6,2e6]
height_values=[{'altitude_m':h,'uniform':m.yukawa_relative_force_sphere(ell,h,coupling=a),
                'inverse_r':m.yukawa_relative_force_sphere(ell,h,coupling=a,profile='inverse_r'),
                'point_mass_WRONG_Earth':m.yukawa_relative_force_point(ell,m.EARTH_R_M+h,coupling=a)} for h in heights]
result={
  'version':'ROOT V117','date':'2026-11-20',
  'scientific_status':'Conditional model checks only; full unification OPEN',
  'assumptions':['Jordan F=xi phi^2 and canonical scalar kinetic term',
      'U_J=lambda4/4*(phi^2-v^2)^2, phi>0',
      'ordinary matter universally minimally coupled to Jordan metric',
      'QCD 1-loop 5-flavor scale v supplied as unproven scalar-VEV hypothesis',
      'G_N is experimental input; inferred xi is not a G prediction',
      'linear fifth-force potential, no chameleon, weak-field spherical source',
      'uniform or inverse_r Earth profiles are idealized, NOT actual Earth'],
  'parameters':{'v_GeV':v,'Planck_reduced_observed_GeV':m.MPL_OBS_GEV,
       'xi_newton_calibrated':xi,'fchi_GeV':f,'Einstein_coefficient_sqrtF_GeV':m.einstein_scale(v,xi),
       'Yukawa_strength_a':a,'one_loop_QCD_scale_is_not_derived_scalar_VEV':True},
  'reference_lambda4_1':{'mchi_eV':m.canonical_mass_ev(1,v,xi),
       'range_m':ell,'range_km':ell/1000,
       'uniform_surface_excess':height_values[0]['uniform'],
       'inverse_r_surface_excess':height_values[0]['inverse_r'],
       'uniform_excess_500km':height_values[5]['uniform'],
       'uniform_GM_ratio_500km_to_surface':m.two_altitude_force_ratio(ell,0,500e3,coupling=a),
       'tiny_lab_scale_deviation_10m_vs_1m':m.relative_observable_after_G_calibration(ell,10,1,coupling=a),
       'quartic_required_for_1km_range':m.quartic_needed_for_range(1000,v,xi),
       'range_min_if_lambda4_at_most_4pi_km':m.range_m(4*math.pi,v,xi)/1000},
  'scan':entries,'altitude_scan':height_values,
  'cross_checks':{'unittest_cases':59,'symbolic_cases':9,
         'mpmath_independent_cases':3,'historical_target':44,
         'claim_of_new_gravity':'NONE'},
  'evidence_status':{'Fifth_force_excluded_by_real_experiment':'NOT ESTABLISHED in this work',
      'full_GR+SM_unification':'OPEN','G_predicted_without_input':'OPEN',
      'scalar_source_assumed':'YES','historical_issues_preserved':396}}
(root/'results/V117_NUMERICAL_RESULTS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True),encoding='utf-8')

plt.figure(figsize=(8.2,5.4))
qs=np.logspace(-4,4,300)
lengths=np.array([m.range_m(q,v,xi)/1000 for q in qs])
plt.loglog(qs,lengths,label='Compton range from the same quartic action')
plt.axvspan(1e-4,4*math.pi,color='0.85',alpha=.5,label='Illustrative lambda4 <= 4 pi')
plt.scatter([1],[ell/1000],marker='o',label='lambda4 = 1')
plt.xlabel('Quartic coupling lambda4 (dimensionless)')
plt.ylabel('Scalar Compton range (km)')
plt.title('V117: canonical mass follows from the potential')
plt.grid(True,which='both',alpha=.25);plt.legend();plt.tight_layout()
plt.savefig(root/'figures/01_quartic_to_range.png',dpi=175);plt.close()

hkm=np.linspace(0,2000,320)
plt.figure(figsize=(8.2,5.4))
for profile,label in [('uniform','homogeneous sphere'),('inverse_r','rho(r) proportional to 1/r')]:
    z=[m.yukawa_relative_force_sphere(ell,h*1000,coupling=a,profile=profile) for h in hkm]
    plt.semilogy(hkm,np.maximum(z,1e-25),label=label)
plt.xlabel('Altitude above spherical source (km)')
plt.ylabel('Fifth force / Newtonian force')
plt.title('V117: finite source, same mass and scalar parameters')
plt.grid(True,which='both',alpha=.23);plt.legend();plt.tight_layout()
plt.savefig(root/'figures/02_earth_finite_source.png',dpi=175);plt.close()

plt.figure(figsize=(8.2,5.4))
u=np.array([m.yukawa_relative_force_sphere(ell,h*1000,coupling=a) for h in hkm])
p=np.array([m.yukawa_relative_force_point(ell,m.EARTH_R_M+h*1000,coupling=a) for h in hkm])
plt.semilogy(hkm,np.maximum(u,1e-27),label='correct uniform finite sphere')
plt.semilogy(hkm,np.maximum(p,1e-27),'--',label='incorrect point-Earth approximation')
plt.xlabel('Altitude (km)');plt.ylabel('Yukawa / Newtonian force')
plt.title('V117: point-source error at range much less than Earth radius')
plt.grid(True,which='both',alpha=.25);plt.legend();plt.tight_layout()
plt.savefig(root/'figures/03_point_vs_extended_source.png',dpi=175);plt.close()

plt.figure(figsize=(8.2,5.4))
r=np.logspace(-1,6,400)
relative=np.array([m.relative_observable_after_G_calibration(ell,float(z),1,coupling=a) for z in r])
plt.semilogx(r,relative)
plt.xlabel('Point-mass separation (m)')
plt.ylabel('Ratio to same model calibrated at 1 m, minus 1')
plt.title('V117: a constant short-range enhancement is absorbed in measured G')
plt.grid(True,alpha=.25);plt.tight_layout()
plt.savefig(root/'figures/04_near_field_G_calibration.png',dpi=175);plt.close()

print(json.dumps({'xi':xi,'a':a,'mass_eV':m.canonical_mass_ev(1,v,xi),'range_km':ell/1000,
    'uniform_surface':result['reference_lambda4_1']['uniform_surface_excess'],
    'inverse_r_surface':result['reference_lambda4_1']['inverse_r_surface_excess'],
    'uniform_500km':result['reference_lambda4_1']['uniform_excess_500km']},indent=2))
