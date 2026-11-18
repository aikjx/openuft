"""Deterministic reproducible numerical outputs; Python3 + numpy/matplotlib."""
import sys, pathlib, json, csv, math, platform, datetime
root=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'src'))
from em_gravity import *
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
out=root/'results';out.mkdir(exist_ok=True)

def write_csv(name,rows):
    with (root/'data'/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
        w.writeheader();w.writerows(rows)

rows=[]
for R in (.1,1.,10.):
    for B in (.00005,1.,10.,30.,50.):
        U=energy_sphere(R,B=B)
        rows.append({'radius_m':R,'B_tesla':B,'u_J_m3':energy_density(B=B),'U_joule':U,'mass_eq_kg':equivalent_mass(U),'g_at_2R_m_s2':toy_external_gravity_from_energy(U,2*R),'metric_h00_at_2R':toy_metric_h00(U,2*R),'model':'spherical energy-only far-field toy; NOT coil+power-source exact GR'})
write_csv('磁场_引力等效_参数扫描.csv',rows)
field_sweeps=[]
for E in [0,1e3,1e5,1e6,1e8]:
 for B in [0,.00005,1.,10.,50.]:
  field_sweeps.append(dict(E_V_m=E,B_T=B,u_J_m3=energy_density(E,B),equivalent_mass_density_kg_m3=energy_density(E,B)/C**2))
write_csv('电磁场能量密度_双参数扫描.csv',field_sweeps)
B0=10; R=1; f=50
T=1/f
t=np.linspace(0,T,1001)
times=[]
for tt in t:
 d=quasi_static_sphere_energies(B0,f,R,float(tt))
 times.append(dict(t_s=tt,B_T=d['B_tesla'],U_B_J=d['U_B_joule'],U_induced_E_J=d['U_E_induced_joule'],U_total_J=d['U_total_joule'],g_energy_at_2R_m_s2=toy_external_gravity_from_energy(d['U_total_joule'],2*R)))
write_csv('交变磁场_准静态时间序列.csv',times)

plt.figure(figsize=(9,5));
for r in [.1,1,10]:
 ss=[x for x in rows if x['radius_m']==r]
 plt.loglog([d['B_tesla'] for d in ss],[d['g_at_2R_m_s2'] for d in ss],marker='o',label=f'R={r:g} m, probe=2R')
plt.xlabel('B (tesla)');plt.ylabel('Energy-equivalent g (m/s^2)');plt.title('Toy far-field monopole from added magnetic energy');plt.legend();plt.grid(alpha=.3);plt.tight_layout();plt.savefig(out/'图1_磁场能量等效引力.png',dpi=150);plt.close()

plt.figure(figsize=(9,5));
plt.plot(t,[x['U_B_J']/1e6 for x in times],label='U_B (MJ)')
plt.plot(t,[x['U_induced_E_J']/1e6 for x in times],label='U_E induced (MJ)')
plt.plot(t,[x['U_total_J']/1e6 for x in times],linestyle='--',label='U_total (MJ)')
plt.xlabel('Time (s)');plt.ylabel('Field energy in ideal R=1m sphere (MJ)');plt.title('50 Hz, B_peak=10 T; quasi-static local idealization');plt.legend();plt.grid(alpha=.3);plt.tight_layout();plt.savefig(out/'图2_交变磁场能量.png',dpi=150);plt.close()

freqs=np.logspace(-3,8,150)
ratios=np.array([quasi_static_average(10,float(ff),1)['ratio_induced_to_B'] for ff in freqs])
plt.figure(figsize=(9,5));plt.loglog(freqs,ratios);plt.axvline(C/(2*math.pi),linestyle='--',label='omega R/c = 1 (approximation invalid)');plt.xlabel('f (Hz)');plt.ylabel('<U_induced_E>/<U_B>');plt.title('Faraday induction contribution (ONLY quasistatic valid region)');plt.legend();plt.grid(alpha=.3);plt.tight_layout();plt.savefig(out/'图3_准静态近似有效范围.png',dpi=150);plt.close()

# Null wave example: F²=0 while u>0. Nonzero pure static B also gravitating.
wave=em_invariants_si((1e6,0,0),(0,1e6/C,0))
main_energy=energy_sphere(1,B=10)
avg=quasi_static_average(10,50,1)
report={
 'version':'ROOT V75',
 'constants_source':'NIST CODATA 2022',
 'constants':{'c_m_s':C,'G_m3_kg_s2':G,'mu0_H_m':MU0,'eps0_F_m':EPS0},
 'model':'SI electromagnetic field energy, and explicitly labeled spherical far-field energy equivalence, NOT full self-consistent Einstein-Maxwell solution',
 'example_10T_1m':{'magnetic_energy_density_J_m3':energy_density(B=10),
   'ideal_sphere_energy_J':main_energy,'mass_equivalent_kg':equivalent_mass(main_energy),
   'toy_g_at_r_1m_m_s2':toy_external_gravity_from_energy(main_energy,1),
   'toy_g_at_r_2m_m_s2':toy_external_gravity_from_energy(main_energy,2),
   'toy_metric_h00_at_r_2m':toy_metric_h00(main_energy,2),
   'g_at_r_1m_over_standard_g':toy_external_gravity_from_energy(main_energy,1)/EARTH_G},
 'example_1MV_per_m':{'u_J_m3':energy_density(E=1e6),'mass_density_eq_kg_m3':energy_density(E=1e6)/C**2},
 '50Hz_quasistatic':avg,
 'null_wave':wave,
 'flags':{'no_new_G_predicted':True,'induction_field_B_only_inconsistent':True,'closed_system_monopole_energy_conserved':True,'scalar_model_hypothetical':True,'experimental_new_gravity_discovery':False},
 'data_rows':{'magnetic_scan':len(rows),'em_scan':len(field_sweeps),'time_series':len(times)},
 'methodology':'Numerical generated outputs reproducible from tools/generate_results.py; no external dataset or actual detector readings used.'
}
(out/'numerical_summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report['example_10T_1m'],indent=2))
print('average 50Hz:',avg)
