#!/usr/bin/env python3
"""Recompute deterministic data and figures. No external datasets downloaded."""
import csv,sys,json
from pathlib import Path
from math import pi,sin,cos,sqrt
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'src'))
from root_v151.core import *
from root_v151.core import electromagnetic_invariants,photon_dof_count
(root/'figures').mkdir(exist_ok=True);(root/'results').mkdir(exist_ok=True)

res={'version':'V151','unit_convention':'only c=1; hbar and G retain dimensions',
     'status':'Mathematical tests only; no new four-force proof',
     'Berry_momentum_space':{'flux_plus':berry_flux_numeric(60,1),
        'flux_minus':berry_flux_numeric(60,-1),
        'chern_plus':chern_number_numeric(60,1),
        'chern_minus':chern_number_numeric(60,-1),
        'hemisphere_cap_theta_pi_3':cap_phase(pi/3,1)},
     'photon_dof':photon_dof_count(),
     'alpha_2022_observed_not_derived':photon_alpha_reference(),
     'helix_example':helix_data(.6,1.,.8)}
for sigma in (-1,1):
    w=plane_wave(2.,1.,sigma)
    E,B=w.fields(0.31,0.08)
    res[f'wave_helicity_{sigma}']={'E':E.tolist(),'B':B.tolist(),'E_dot_B':float(E@B),
             'B_squared_minus_E_squared':float(B@B-E@E),
             'Poynting_z':float(np.cross(E,B)[2]),'maxwell_residuals':{k:(v.tolist() if isinstance(v,np.ndarray) else v) for k,v in w.maxwell_residuals(.31,.08).items()}}
(root/'results'/'main_metrics.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

with (root/'results'/'angular_scan.csv').open('w',newline='',encoding='utf-8') as f:
    wr=csv.writer(f);wr.writerow(['theta_rad','Aphi_plus','Ftheta_phi_plus','Aphi_minus','Ftheta_phi_minus','cap_berry_phase_plus_rad'])
    for theta in np.linspace(.001,pi-.001,401):
        wr.writerow([f'{theta:.14g}',f'{berry_connection(theta,1)[1]:.14g}',f'{berry_curvature_theta(theta,1):.14g}',f'{berry_connection(theta,-1)[1]:.14g}',f'{berry_curvature_theta(theta,-1):.14g}',f'{cap_phase(theta,1):.14g}'])
with (root/'results'/'boost_scan.csv').open('w',newline='',encoding='utf-8') as f:
    wr=csv.writer(f);wr.writerow(['beta','doppler_factor','omega_prime_over_omega','amp_prime_over_amp','helicity'])
    wave=plane_wave(1.,1.,1)
    for beta in np.linspace(-.95,.95,191):
        wp,D=wave.boost_z(float(beta));wr.writerow([f'{beta:.14g}',f'{D:.14g}',f'{wp.omega:.14g}',f'{wp.amp:.14g}',wp.sigma])

fig,ax=plt.subplots(figsize=(8.0,4.4))
thetas=np.linspace(.01,pi-.01,400)
ax.plot(thetas,[berry_connection(th,1)[1] for th in thetas],label='Berry A_phi (+)')
ax.plot(thetas,[berry_curvature_theta(th,1) for th in thetas],label='Berry F_theta,phi (+)')
ax.plot(thetas,[berry_curvature_theta(th,-1) for th in thetas],linestyle='--',label='Berry F_theta,phi (-)')
ax.set_xlabel('Propagation polar angle theta (rad)');ax.set_ylabel('dimensionless angular components')
ax.set_title('Photon momentum-space Berry connection and curvature')
ax.grid(alpha=.2);ax.legend();fig.tight_layout();fig.savefig(root/'figures'/'berry_connection_curvature.png',dpi=170);plt.close(fig)

fig,ax=plt.subplots(figsize=(7.6,4.5))
th=np.linspace(0,pi,401)
ax.plot(th,[cap_phase(v,1)/(2*pi) for v in th],label='Capped Berry flux / 2pi (+)')
ax.plot(th,[cap_phase(v,-1)/(2*pi) for v in th],label='Capped Berry flux / 2pi (-)')
ax.set_xlabel('Cap polar angle theta (rad)');ax.set_ylabel('Chern flux accumulated')
ax.set_title('Quantized ±2 total Berry Chern numbers')
ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(root/'figures'/'chern_cap_flux.png',dpi=170);plt.close(fig)

fig=plt.figure(figsize=(8.0,5.2));ax=fig.add_subplot(111,projection='3d')
z=np.linspace(0,4*pi,320);wave=plane_wave(1.,1.,1)
E=np.asarray([wave.fields(0,float(zz))[0] for zz in z]);B=np.asarray([wave.fields(0,float(zz))[1] for zz in z])
ax.plot(E[:,0],E[:,1],z,label='E tip (field direction)',linewidth=1.9)
ax.plot(B[:,0],B[:,1],z,label='B tip (field direction)',linewidth=1.2)
ax.plot(np.zeros_like(z),np.zeros_like(z),z,linestyle=':',label='straight ray +z')
ax.set(xlabel='x component',ylabel='y component',zlabel='z coordinate')
ax.set_title('Rotating field vectors do NOT mean a helical photon worldline')
ax.legend(loc='upper left',fontsize=8);fig.tight_layout();fig.savefig(root/'figures'/'wave_vs_trajectory.png',dpi=170);plt.close(fig)
print('Generated 2 CSV, 1 main JSON, 3 PNG figures.')
