"""Reproduce ROOT V125 tables, figures, and independent noise experiments.

Only synthetic/theory data; no GOCE, GRACE, or Earth observation records loaded.
"""
import sys, json, csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from v125_core import *

ROOT=Path(__file__).resolve().parents[1]
for d in ('results','figures'): (ROOT/d).mkdir(exist_ok=True)
model=FixedYukawaEarth()
heights=[0,50,100,150,200,250,300,350,400,450,500,600,800,1000,1500]
rows=[]
for h_km in heights:
    r=R_EARTH_M+1000*h_km
    eps=float(model.eps(r));g=float(model.g_mag(r));tr=float(model.accel_divergence(r))
    rows.append({'height_km':h_km,'epsilon':eps,'extra_accel_m_s2':eps*GM_EARTH/r**2,
                 'trace_accel_s_inv2':tr,'trace_accel_E':tr/EOTVOS,
                 'newton_g_m_s2':GM_EARTH/r**2,
                 'ratio_trace_to_radial_Newtonian_gradient':tr/(2*GM_EARTH/r**3)})
with open(ROOT/'results'/'trace_by_height_SYNTHETIC.csv','w',newline='',encoding='utf-8') as f:
    writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)

band={f'eccentricity_{e:.3f}':orbit_trace_band_diagnostic(model,eccentricity=e) for e in [0.0,0.005,0.01,0.02]}
mc={f'sigma_{s}':synthetic_trace_mc(model,rel_sigma=s,n=10000,seed=20261121) for s in [0.01,0.05,0.10]}
r1=R_EARTH_M+250_000;r2=R_EARTH_M+400_000
T1=float(model.accel_divergence(r1));T2=float(model.accel_divergence(r2))
rotation=2*newton_n(r2)**2
summary={'version':'ROOT V125','status':'synthetic model only; not actual geodesy evidence',
         'model':{'GM_m3_s2':GM_EARTH,'R_m':R_EARTH_M,'ell_m':ELL_M,'alpha':ALPHA_Y,
                  'phi_scaled':fayet_phi_scaled(ELL_M)},
         'double_altitude_trace':{'r1_m':r1,'r2_m':r2,'T1_E':T1/EOTVOS,'T2_E':T2/EOTVOS,
                  'ratio_r1T1_over_r2T2':r1*T1/(r2*T2),
                  'inverted_ell_m':trace_invert_range(r1,T1,r2,T2)},
         'at_400km':{'Yukawa_trace_E':T2/EOTVOS,
                    'Newtonian_gradient_trace_E':0.0,
                    'orbital_frequency_mHz':1000*newton_n(r2)/(2*np.pi),
                    'example_rotating_frame_2omega2_E':rotation/EOTVOS,
                    'rotating_frame_magnitude_to_Yukawa_trace':rotation/T2},
         'bandwidth':band,'monte_carlo_SYNTHETIC':mc}
with open(ROOT/'results'/'v125_summary_SYNTHETIC.json','w',encoding='utf-8') as f:
    json.dump(summary,f,ensure_ascii=False,indent=2)

x=np.array([r['height_km'] for r in rows]);y=np.array([r['trace_accel_E'] for r in rows])
fig,ax=plt.subplots(figsize=(8,4.5));ax.semilogy(x,y,marker='o',linewidth=1.8)
ax.axhline(0.001,color='gray',linestyle='--',label='1 mE (reference only)')
ax.set_xlabel('Altitude above spherical Earth (km)');ax.set_ylabel('Positive acceleration-gradient trace (E)')
ax.set_title('Fixed Yukawa candidate: ideal vacuum nonzero trace')
ax.legend();ax.grid(alpha=.25);fig.tight_layout()
fig.savefig(ROOT/'figures'/'01_trace_vs_altitude_SYNTHETIC.png',dpi=170);plt.close(fig)

r=r2; J=model.gradient_tensor(np.array([r,0.,0.]));vals=np.linalg.eigvalsh(J)/EOTVOS
fig,ax=plt.subplots(figsize=(7.5,4.3));ax.bar(['tangential 1','tangential 2','radial'],vals)
ax.set_ylabel('Eigenvalue of acceleration Jacobian (E)')
ax.set_title('400 km: sum of 3 eigenvalues = +17.474 E')
ax.grid(axis='y',alpha=.2);fig.tight_layout()
fig.savefig(ROOT/'figures'/'02_gradient_tensor_400km_SYNTHETIC.png',dpi=170);plt.close(fig)

fig,ax=plt.subplots(figsize=(8,4.5))
e=.01; a=r2;r_samples=kepler_radius_over_phase(a,e,16384)
t=np.asarray(model.accel_divergence(r_samples))
freq=np.fft.rfftfreq(len(t),d=2*np.pi/newton_n(a)/len(t))
yfft=np.abs(np.fft.rfft(t-np.mean(t)))
ax.semilogy(freq*1000,yfft/(max(yfft) or 1),marker='.',linewidth=1,markersize=2)
ax.axvline(5,linestyle='--',color='gray',label='5 mHz nominal GOCE MB floor')
ax.set_xlim(0,8);ax.set_ylim(1e-14,2)
ax.set_xlabel('Fourier frequency (mHz)');ax.set_ylabel('Amplitude relative to peak Fourier component')
ax.set_title('Ideal spherical fifth-force modulation: e=0.01 circular-like orbit')
ax.legend();ax.grid(alpha=.2);fig.tight_layout()
fig.savefig(ROOT/'figures'/'03_goce_frequency_band_SYNTHETIC.png',dpi=170);plt.close(fig)

noise=[.01,.05,.10]
qs=[mc[f'sigma_{s}']['quantiles_2p5_50_97p5_km'] for s in noise]
fig,ax=plt.subplots(figsize=(7.5,4.5));xx=np.arange(3)
ax.errorbar(xx,[q[1] for q in qs],yerr=[[q[1]-q[0] for q in qs],[q[2]-q[1] for q in qs]],fmt='o',capsize=5)
ax.axhline(124.6,linestyle='--',color='gray',label='True 124.6 km (input)')
ax.set_xticks(xx,['1% trace noise','5% trace noise','10% trace noise'])
ax.set_ylabel('Recovered range from two traces (km)');ax.set_title('Toy 10,000-replication independent-noise intervals')
ax.legend();ax.grid(alpha=.2);fig.tight_layout()
fig.savefig(ROOT/'figures'/'04_trace_inversion_uncertainty_SYNTHETIC.png',dpi=170);plt.close(fig)
print(json.dumps({'total_rows':len(rows),'T400_E':T2/EOTVOS,'inverse_ell_m':summary['double_altitude_trace']['inverted_ell_m'],
'orbital_frequency_mHz':summary['at_400km']['orbital_frequency_mHz'],
'frequency_band_above_5mHz_e001':band['eccentricity_0.010']['fraction_ac_power_at_least_5mHz'],
'rotation_E':rotation/EOTVOS,'MC_5p':mc['sigma_0.05']['quantiles_2p5_50_97p5_km']},ensure_ascii=False,indent=2))
