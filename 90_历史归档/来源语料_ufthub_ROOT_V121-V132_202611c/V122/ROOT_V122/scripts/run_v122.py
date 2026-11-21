"""Reproduce ROOT V122 model forecasts, synthetic identifiability and figures.

All model outputs are hypothetical. This does not download or fit observed data.
"""
from __future__ import annotations
import json, csv, sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from rootv120 import R_EARTH,C_LIGHT,MU_EARTH_REF
from rootv122 import (ELL,EPS0,epsilon,frequencies,scalar_metric_potentials,
                      scalaron,potential,central_orbit_precession,
                      profile_diagnostic,five_height_hankel_trap)

ROOT=Path(__file__).resolve().parents[1]
res=ROOT/'results'; fig=ROOT/'figures';res.mkdir(exist_ok=True);fig.mkdir(exist_ok=True)
hs=np.arange(0,1001,50,dtype=float)*1000
rows=[]
for h in hs:
    r=R_EARTH+h
    ep=epsilon(r)
    fr=frequencies(r)
    metric=scalar_metric_potentials(r)
    rows.append(dict(height_km=h/1000,epsilon=ep,
                     delta_g_m_s2=MU_EARTH_REF/r**2*ep,
                     Omega_rad_s=float(np.sqrt(fr['Omega2'])),
                     kappa_rad_s=float(np.sqrt(fr['kappa2'])),
                     S_d_ln_K_d_ln_r=fr['S'],
                     extra_precession_rad_per_radial_period=fr['periapsis'],
                     gamma_slip=metric['gamma'],
                     eta_potential=metric['eta'],
                     dynamical_lensing_ratio=metric['dynamical_to_lensing_mass']))
with (res/'V122_static_spherical_predictions_SYNTHETIC.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,rows[0].keys());w.writeheader();w.writerows(rows)

orbit=central_orbit_precession(e=5e-5)
profiles={}
for sigma_ind,sigma_common in [(1e-5,0.),(1e-5,1e-3),(1e-6,0.)]:
    k=f'noise_{sigma_ind:g}_common_{sigma_common:g}'
    profiles[k]={"common_GM_only":profile_diagnostic([250e3,300e3,350e3,400e3,450e3,500e3],sigma_ind,sigma_common),
                 "common_GM_plus_altitude_slope":profile_diagnostic([250e3,300e3,350e3,400e3,450e3,500e3],sigma_ind,sigma_common,True)}
summary={
 'version':'ROOT V122',
 'status':'MATHEMATICAL AND SYNTHETIC TESTS ONLY; NOT A GRAND UNIFICATION OR FIFTH FORCE OBSERVATION',
 'fixed_hypothesis':dict(alpha=1/3,ell_m=ELL,Earth_radius_m=R_EARTH,Earth_density_model='V120 improved analytic'),
 'scaler':scalaron(),
 'epsilon_ground':EPS0,
 'ground_to_400km_extra_clock_fraction':(potential(R_EARTH+4e5)-potential(R_EARTH))/C_LIGHT**2 -
                                        (-(MU_EARTH_REF/(R_EARTH+4e5)) + MU_EARTH_REF/R_EARTH)/C_LIGHT**2,
 'h_400km':[r for r in rows if r['height_km']==400.][0],
 'h_250km':[r for r in rows if r['height_km']==250.][0],
 'orbit_integration':orbit,
 'hankel_fake_solution':five_height_hankel_trap(),
 'projected_statistics_synthetic':profiles,
 'limitations':['Not observational data','Earth is treated spherically and static',
                'Clock shift static weak-field only',
                'No full orbit fit, gravity harmonics, tides, drag, clock or pointing systematics',
                'Fifth force does not prove the four-force unification'],
}
(res/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')

fig1,ax=plt.subplots(figsize=(9,5))
ax.plot([r['height_km'] for r in rows],[100*r['epsilon'] for r in rows],label='Yukawa anomalous acceleration (%)')
ax.set(xlabel='Height (km)',ylabel='Extra acceleration / Newtonian (%)',
       title='ROOT V122 fixed Yukawa candidate (synthetic prediction only)')
ax.grid(alpha=.25);ax.legend();fig1.tight_layout();fig1.savefig(fig/'extra_accel_vs_height.png',dpi=145);plt.close(fig1)

fig2,ax2=plt.subplots(figsize=(9,5))
ax2.plot([r['height_km'] for r in rows],[r['extra_precession_rad_per_radial_period']*180/np.pi for r in rows],
         label='Near-circular advance (degree per radial period)')
ax2.set(xlabel='Height (km)',ylabel='Excess precession (degrees)',
        title='Static spherical Yukawa model: epicyclic result, not orbital observations')
ax2.grid(alpha=.25);ax2.legend();fig2.tight_layout();fig2.savefig(fig/'precession_vs_height.png',dpi=145);plt.close(fig2)

fig3,ax3=plt.subplots(figsize=(9,5))
ax3.plot([r['height_km'] for r in rows],[1-r['gamma_slip'] for r in rows],label='1 - potential ratio Psi/Phi')
ax3.plot([r['height_km'] for r in rows],[r['epsilon'] for r in rows],label='dynamical/lensing mass ratio -1')
ax3.set(xlabel='Height (km)',ylabel='Dimensionless weak-field deviation',
        title='Metric scalar slip versus dynamical Yukawa excess (theory only)')
ax3.grid(alpha=.25);ax3.legend();fig3.tight_layout();fig3.savefig(fig/'slip_vs_dynamics.png',dpi=145);plt.close(fig3)

print(json.dumps({"ground_epsilon":EPS0,"400km":summary['h_400km'],
                  "orbit":orbit,"profiles":profiles},ensure_ascii=False,indent=2))
