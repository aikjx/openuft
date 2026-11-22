#!/usr/bin/env python3
"""Generate self-contained model illustrations; not empirical data."""
from pathlib import Path
import csv,sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
import root_v133 as M
P=Path(__file__).resolve().parents[1]
(P/'plots').mkdir(exist_ok=True)
(P/'results').mkdir(exist_ok=True)
# The charge/mass tower is a synthetic model example.
h=M.HBAR_SI;t0=1.0;I=10*h*t0;m0=100*h/t0
lam=M.lambda_for_alpha(1/M.ALPHA_INV_0)
ns=np.arange(-5,6)
tower=[M.rotor_spectrum(int(n),I,lam,m0) for n in ns]
with (P/'results'/'toy_rotor_tower.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(tower[0].keys()))
    w.writeheader();w.writerows(tower)
plt.figure(figsize=(8,4.8))
plt.plot(ns,[(t['mass']-m0)/(h/t0) for t in tower],marker='o',label='internal mass shift / (hbar/t0)')
plt.plot(ns,[t['charge']/(lam*h) for t in tower],marker='s',label='charge / q0')
plt.xlabel('compact winding quantum number n')
plt.ylabel('synthetic normalized quantities')
plt.title('Compact internal phase: distinct mass and charge laws')
plt.legend();plt.grid(alpha=.25);plt.tight_layout()
plt.savefig(P/'plots'/'01_toy_charge_mass_spectrum.png',dpi=160)
plt.close()
# RK numerical integration vs analytic cyclotron orbit
orbit=M.relativistic_magnetic_orbit(1.0,0.3,0.1,0.8,2.,1800)
plt.figure(figsize=(5.7,5.7))
plt.plot(orbit['x'],orbit['y'],label='relativistic ODE')
plt.plot(orbit['x_exact'][::50],orbit['y_exact'][::50],'.',label='analytic reference',markersize=3)
plt.axis('equal');plt.xlabel('x in toy length units');plt.ylabel('y in toy length units')
plt.title('Magnetic Lorentz dynamics (c=1)');plt.legend();plt.grid(alpha=.25);plt.tight_layout()
plt.savefig(P/'plots'/'02_lorentz_orbit_validation.png',dpi=160)
plt.close()
# Lorentz boost breaks external pitch-angle alpha identification
u=np.linspace(-.8,.8,400)
for beta in [0.,.3,.6]:
    arr=np.array([M.boost_axis_velocity(float(x),beta) for x in u])
    plt.plot(u,arr,label=f'boost beta={beta}')
plt.axvline(1/M.ALPHA_INV_0,linestyle=':',label='alpha(0)')
plt.xlabel('external axial speed u');plt.ylabel('transformed u_prime')
plt.title('External helix speed is not Lorentz invariant')
plt.legend();plt.grid(alpha=.25);plt.tight_layout()
plt.savefig(P/'plots'/'03_boost_counterexample.png',dpi=160)
plt.close()
# Parametric degeneracy: variable lambda fits any alpha0
lratio=np.logspace(-1,1,200)
alpha_model=(lratio**2)/M.ALPHA_INV_0
plt.figure(figsize=(8,4.8))
plt.loglog(lratio,alpha_model,label='alpha(lambda) = lambda^2 hbar/(4 pi epsilon0)')
plt.axhline(1/M.ALPHA_INV_0,linestyle='--',label='CODATA alpha(0) used as reference')
plt.xlabel('lambda / lambda fitted from alpha(0)');plt.ylabel('alpha_n=1')
plt.title('Continuous coupling freedom: no alpha prediction')
plt.legend();plt.grid(alpha=.25);plt.tight_layout()
plt.savefig(P/'plots'/'04_unconstrained_alpha.png',dpi=160)
plt.close()
print('Generated 4 scientific synthetic plots and CSV.')
