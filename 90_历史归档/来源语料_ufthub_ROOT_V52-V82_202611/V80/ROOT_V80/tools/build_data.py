import sys,csv,json,math
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE))
from src.cosmos import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

rows=[body_report(b) for b in BODIES]
p=BASE/'data'/'astro_reference.csv'
with p.open('w',newline='',encoding='utf-8-sig') as f:
    wr=csv.DictWriter(f,fieldnames=list(rows[0].keys()));wr.writeheader();wr.writerows(rows)

ref={
 'G_SI_CODATA_2022':G,'c_SI_exact':C,'QED_critical_B_T':q_ed_critical_field(),
 'Mercury_GR_1PN_arcsec_per_century':mercury_precession_arcsec_century(),
 'G_dimensions_no_go':scalar_g_c_no_go(),
 'magnetar_synthetic':rows[-1],
 'earth_approx':rows[3],
 'sources':'see SOURCES.md; not raw observational astrophysical data',
 'success_status':'UNPROVEN: no model-independent G prediction or four-force derivation'
}
(BASE/'results'/'summary.json').write_text(json.dumps(ref,ensure_ascii=False,indent=2),encoding='utf-8')

plt.rcParams.update({'font.size':11})
labels=['Sun','Earth','Jupiter','White dwarf*','Neutron star*','Magnetar*']
sel=[rows[i] for i in [0,3,6,10,11,12]]
fig,ax=plt.subplots(figsize=(10,5.7));ax.bar(labels,[r['compactness'] for r in sel]);ax.set_yscale('log');ax.set_ylabel('GM / (R c²)');ax.set_title('Compactness across illustrative astrophysical environments');ax.grid(axis='y',alpha=.25);fig.tight_layout();fig.savefig(BASE/'charts'/'compactness.png',dpi=170);plt.close(fig)
fig,ax=plt.subplots(figsize=(10,5.7));ax.bar(labels,[r['magnetic_to_mean_rest_energy_ratio'] for r in sel]);ax.set_yscale('log');ax.set_ylabel('B² / (2 μ₀ ρ_mean c²)');ax.set_title('Local illustrative magnetic / mean rest-energy density ratio');ax.grid(axis='y',alpha=.25);fig.tight_layout();fig.savefig(BASE/'charts'/'magnetic_ratio.png',dpi=170);plt.close(fig)
fig,ax=plt.subplots(figsize=(10,5.7));ax.bar(labels,[r['schwarzschild_K_m4'] for r in sel]);ax.set_yscale('log');ax.set_ylabel('K [m^-4]');ax.set_title('Spherical Schwarzschild exterior curvature benchmark');ax.grid(axis='y',alpha=.25);fig.tight_layout();fig.savefig(BASE/'charts'/'curvature.png',dpi=170);plt.close(fig)

beta_values=[0,1,1e3,1e6]
scan=[]
for obj in [BODIES[3],BODIES[10],BODIES[11],BODIES[12]]:
    r=body_report(obj)
    for beta in beta_values:
        scan.append({'body':obj.name,'beta_hypothetical':beta,'field_to_rest_ratio':r['magnetic_to_mean_rest_energy_ratio'],'delta_G_over_G_hypothetical':candidate_field_dependent_fraction(obj.b_field_t,r['mean_density_kg_m3'],beta),'note':'synthetic ansatz; not fitted/validated'})
with (BASE/'data'/'hypothesis_scan.csv').open('w',newline='',encoding='utf-8-sig') as f:
    wr=csv.DictWriter(f,fieldnames=list(scan[0]));wr.writeheader();wr.writerows(scan)
print('Generated',len(rows),'bodies and',len(scan),'hypothetical scans')
print('Mercury GR precession',ref['Mercury_GR_1PN_arcsec_per_century'])
