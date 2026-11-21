"""Generate ROOT V127 quantum mathematics diagnostics, all SYNTHETIC calculations."""
from pathlib import Path
import sys, json, csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from quantum_core import *

root=Path(__file__).resolve().parents[1]
(root/'results').mkdir(exist_ok=True)
(root/'figures').mkdir(exist_ok=True)
q=electron_quantities()
q={k:float(v) for k,v in q.items()}
q['eV_fine_structure_test']=float(1/alpha_fs)
q['electron_spin_g_naive_classical']=1.
q['electron_spin_g_CODATA_abs']=float(abs(q['g_e']))
q['naive_orbital_L_over_hbar']=float(assumed_compton_orbit_L_over_hbar())
q['spin_half_magnitude_over_hbar']=float(np.sqrt(.75))
q['electron_orbital_spin_projection_ratio']=2.0
q['kk_muon_nearest_integer']=int(round(q['muon_electron_ratio']))
q['kk_muon_fractional_distance']=float(q['muon_electron_ratio']-round(q['muon_electron_ratio']))
q['example_slit_electron_v_m_s']=1e6
q['example_slit_wavelength_m']=float(de_broglie_wavelength(1e6))
q['example_slit_fringe_spacing_m']=float(interference_fringe_spacing(1e6,1e-6,1))

T=(0.,1.,2.,4.)
fig,ax=plt.subplots(figsize=(8,4.8))
rows=[]
for t in T:
    r=free_gaussian(t=t)
    rows.append(dict(time=float(t),norm=float(r['norm']),xmean=float(r['mean']),
                     predicted_xmean=float(r['expected_mean']),stddev=float(r['sigma']),
                     predicted_stddev=float(r['expected_sigma'])))
    ax.plot(r['x'],r['probability'],label=f't={t:g}')
ax.set(xlim=(-12,10),xlabel='x (dimensionless)',ylabel='|ψ|² (dimensionless)',
       title='Free Gaussian quantum packet — unitary spreading (SYNTHETIC)')
ax.legend()
fig.tight_layout();fig.savefig(root/'figures/01_free_gaussian_SYNTHETIC.png',dpi=170);plt.close(fig)

u=np.linspace(.005,.8,200) # beta=v/c from momentum/(mc) converted through beta=eta/sqrt(1+eta^2)
eta=u/np.sqrt(1-u*u)
exact=np.sqrt(1+eta**2)
second=1+eta**2/2
fourth=second-eta**4/8
fig,ax=plt.subplots(figsize=(8,4.8))
ax.semilogy(u,abs(second-exact)/exact,label='nonrel kinetic only')
ax.semilogy(u,abs(fourth-exact)/exact,label='including p⁴ correction')
ax.set(xlabel='v/c',ylabel='Relative error in total E',
       title='Relativistic dispersion versus low-momentum expansion (SYNTHETIC)')
ax.legend();ax.grid(alpha=.2)
fig.tight_layout();fig.savefig(root/'figures/02_relativistic_limit_SYNTHETIC.png',dpi=170);plt.close(fig)

x=np.linspace(0,2*np.pi,800)
fig,ax=plt.subplots(figsize=(8,4.7))
for a in (.5,1.,2.):
    ax.plot(x,np.cos(x/a),label=f'phase scale ℏ_eff={a:g}')
ax.set(xlabel='Classical action S (arbitrary units)',ylabel='Re exp(i S/ℏ_eff)',
       title='Same classical action, different quantum interference (ILLUSTRATION)')
ax.legend();fig.tight_layout()
fig.savefig(root/'figures/03_hbar_identifiability_ILLUSTRATION.png',dpi=170);plt.close(fig)

with (root/'results/gaussian_wavepacket_SYNTHETIC.csv').open('w',newline='',encoding='utf-8') as f:
    writer=csv.DictWriter(f,fieldnames=['time','norm','xmean','predicted_xmean','stddev','predicted_stddev'])
    writer.writeheader();writer.writerows(rows)
q['fft_max_norm_drift']=float(max(abs(r['norm']-1) for r in rows))
q['fft_max_sigma_abs_error']=float(max(abs(r['stddev']-r['predicted_stddev']) for r in rows))
q['fft_max_mean_abs_error']=float(max(abs(r['xmean']-r['predicted_xmean']) for r in rows))
with (root/'results/quantum_checks_SYNTHETIC.json').open('w',encoding='utf-8') as f:
    json.dump(q,f,indent=2,ensure_ascii=False)
print(json.dumps(q,indent=2,ensure_ascii=False))
