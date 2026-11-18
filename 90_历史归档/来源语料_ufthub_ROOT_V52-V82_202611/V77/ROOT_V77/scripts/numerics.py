"""Generate numerical CSV/JSON and optional PNG plots. Never claims new experiments."""
from __future__ import annotations
import csv,json,math,sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE))
from src.gravity_c import *

r=BASE/'results';d=BASE/'data'; fig=BASE/'figures'
r.mkdir(exist_ok=True);d.mkdir(exist_ok=True);fig.mkdir(exist_ok=True)

(r/'numerical_summary.json').write_text(json.dumps(summary(),indent=2,ensure_ascii=False),encoding='utf-8')

with (d/'conditional_c_scaling.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f); w.writerow(['c_ratio','c_hypothetical_m_per_s','G_fixed','G_if_Z_fixed','G_if_r_g_and_M_fixed','G_if_lP_hbar_fixed','status'])
    for i in range(51):
        factor=0.5+0.02*i
        values=c_scaling_models(factor)
        w.writerow([f'{factor:.10f}',f'{factor*C:.10f}',*[f'{x:.15e}' for x in values.values()], 'conditional toy only'])

masses=[('electron',ME),('proton',MPROTON),('Planck_scale_mass_derived_from_G',planck_mass())]
with (d/'mass_length_comparison.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f);w.writerow(['mass_type','mass_kg','r_g_m','reduced_Compton_m','r_g_div_rC_alpha_g','mass_independent_of_G'])
    for name,m in masses:
        s=mass_radius_consistency(m)
        w.writerow([name,f'{m:.15e}',f"{s['r_g']:.15e}",f"{s['r_C']:.15e}",f"{s['alpha_g']:.15e}",name!='Planck_scale_mass_derived_from_G'])

with (d/'earth_GM_degeneracy.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f);w.writerow(['G_scale_assumed','G_assumed_SI','inferred_Earth_mass_kg','GM_product_m3_s2','orbital_g_at_mean_Earth_radius_m_s2'])
    for factor in [0.01,.1,.25,.5,1,2,4,10,100]:
        g=factor*G;m=GM_EARTH/g
        w.writerow([factor,f'{g:.15e}',f'{m:.15e}',f'{g*m:.15e}',f'{newton_gravity_accel(GM_EARTH,R_EARTH):.15f}'])

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    xs=np.linspace(.5,1.5,200)
    plt.figure(figsize=(8.3,4.8))
    for key,name in [('fixed_G','G constant'),('fixed_Z','Z held constant'),
                     ('fixed_gravitational_radius_and_mass','r_g and M held constant'),
                     ('fixed_planck_length_and_hbar','l_P and hbar held constant')]:
        plt.plot(xs,[c_scaling_models(x)[key]/G for x in xs],label=name)
    plt.xlabel('Hypothetical c / measured c (not observed)')
    plt.ylabel('Conditional G / measured G')
    plt.title('Same identities, different held-fixed assumptions')
    plt.grid(alpha=.25);plt.legend(fontsize=8);plt.tight_layout()
    plt.savefig(fig/'01_conditional_G_vs_c.png',dpi=150);plt.close()

    plt.figure(figsize=(8.3,4.8))
    labels=[name for name,_ in masses]; yy=[gravitational_alpha(m) for _,m in masses]
    plt.bar(labels,yy)
    plt.yscale('log');plt.ylabel('alpha_g(m) = G*m^2/(hbar*c)')
    plt.title('Gravity coupling spans ~45 orders of magnitude')
    plt.grid(axis='y',alpha=.25);plt.tight_layout()
    plt.savefig(fig/'02_gravitational_alpha.png',dpi=150);plt.close()

    mm=np.logspace(-32,-6,250)
    plt.figure(figsize=(8.3,4.8))
    plt.loglog(mm,[gravitational_radius(m) for m in mm],label='gravitational radius GM/c²')
    plt.loglog(mm,[reduced_compton_wavelength(m) for m in mm],label='reduced Compton wavelength')
    plt.axvline(planck_mass(),linestyle='--',label='crossing at Planck mass')
    plt.xlabel('Mass (kg)');plt.ylabel('Length (m)');plt.title('Length scales coincide only at m_P')
    plt.legend(fontsize=8);plt.grid(alpha=.25);plt.tight_layout()
    plt.savefig(fig/'03_gravity_vs_compton_lengths.png',dpi=150);plt.close()
    print('PNG plots generated: 3')
except ImportError:
    print('Optional matplotlib/numpy absent: CSV/JSON done, plots skipped')

print('Saved summary, 3 data tables')
