#!/usr/bin/env python3
"""Optional plots. Run after python run_all.py. No external data."""
import csv
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
rows=[]
with (BASE/'results'/'coupled_helical_mode.csv').open(newline='',encoding='utf-8') as f:
    rows=[{k:float(v) for k,v in row.items()} for row in csv.DictReader(f)]

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

T=[r['t'] for r in rows]
fig,ax=plt.subplots(figsize=(8,4.4),layout='constrained')
ax.plot(T,[r['photon_energy'] for r in rows],label='helical gauge-mode energy')
ax.plot(T,[r['scalar_energy'] for r in rows],label='internal-phase energy')
ax.plot(T,[r['energy'] for r in rows],label='total energy (conserved)',ls='--')
ax.set(xlabel='dimensionless time t/L0',ylabel='dimensionless density E / (hbar/L0^4)',title='Coupled helical mode: energy exchange and conservation')
ax.grid(True,alpha=.22)
ax.legend(fontsize=8)
fig.savefig(BASE/'figures'/'energy_exchange.png',dpi=160)
fig.savefig(BASE/'figures'/'energy_exchange.svg')
plt.close(fig)
fig,ax=plt.subplots(figsize=(8,4.4),layout='constrained')
ax.plot(T,[r['a'] for r in rows],label='helical mode amplitude a')
ax.plot(T,[r['w'] for r in rows],label='phase angular speed dtheta/dt')
ax.set(xlabel='dimensionless time t/L0',ylabel='dimensionless normalized values',title='Coupled field response (illustrative model)')
ax.legend(fontsize=8)
ax.grid(True,alpha=.22)
fig.savefig(BASE/'figures'/'mode_dynamics.png',dpi=160)
fig.savefig(BASE/'figures'/'mode_dynamics.svg')
plt.close(fig)
print('Generated four charts into figures/.')
