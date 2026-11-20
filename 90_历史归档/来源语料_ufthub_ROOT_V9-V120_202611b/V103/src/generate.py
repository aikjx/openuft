from pathlib import Path
import json,csv,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.constants import c,m_e
from .v103_core import *

ROOT=Path(__file__).resolve().parents[1]

def generate():
    orbit_path=ROOT/'data/V100_ORBIT_21Q_INPUT_THEORY.csv'
    pts=np.loadtxt(orbit_path,skiprows=1,delimiter=',')
    g=discrete_geometry(pts)
    beta=.1
    budget=supply_budget(g['L'],g['K2'],beta)
    Kinetic=(gamma_beta(beta)-1)*m_e*c*c
    boost=boosted_circle()
    ans={'model':'CLASSICAL_THEORY_ONLY','baseline':'V102 historical V100 polygon; sampled geometry NOT certified embedding',
         'numerical_geometry':g,'radiation_and_power':budget,'kinetic_J':Kinetic,
         'loss_fraction_per_period':budget['energy_rad_J']/Kinetic,
         'boost_counterexample':boost,
         'conclusion':'Static globally conservative E and static B cannot replenish a positive per-cycle radiative loss on a strictly periodic orbit.'}
    (ROOT/'results/V103_THEORY_SUMMARY.json').write_text(json.dumps(ans,indent=2,ensure_ascii=False),encoding='utf-8')
    speeds=np.linspace(.01,.8,120)
    rows=[]
    for b in speeds:
        v=supply_budget(g['L'],g['K2'],float(b))
        rows.append([float(b),v['energy_rad_J'],v['topological_energy_floor_J'],v['avg_power_W'],v['minimum_power_W']])
    with (ROOT/'results/SPEED_SCAN_THEORY.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['beta','E_rad_J','knot_E_floor_J','P_mean_W','P_knot_floor_W']);w.writerows(rows)
    fig,ax=plt.subplots(figsize=(8,4.7))
    ax.plot(speeds,[r[1] for r in rows],label='V100 sampled-orbit model (geometry fixed)')
    ax.plot(speeds,[r[2] for r in rows],label='Conditional nontrivial-knot floor',linestyle='--')
    ax.set_yscale('log'); ax.set_xlabel('Particle speed / c'); ax.set_ylabel('Radiation energy per closed period (J)')
    ax.set_title('ROOT V103 | Conditional energy budget (not an experiment)')
    ax.grid(True,alpha=.25);ax.legend(fontsize=8);fig.tight_layout()
    fig.savefig(ROOT/'figures/01_RADIATIVE_ENERGY_THEORY.png',dpi=180);plt.close(fig)
    boosts=np.linspace(-.8,.8,161)
    data=[boosted_circle(beta_particle=.6,beta_boost=float(u)) for u in boosts]
    fig,ax=plt.subplots(figsize=(8,4.7))
    ax.plot(boosts,[d['boosted_curvature_inv_m'] for d in data],label='3D curvature')
    ax.plot(boosts,[d['boosted_torsion_inv_m'] for d in data],label='3D torsion')
    ax.axhline(0,linewidth=.8,linestyle=':')
    ax.set_xlabel('Axial observer boost / c');ax.set_ylabel('Inverse length (1/m)')
    ax.set_title('ROOT V103 | 3D torsion changes with observer')
    ax.legend();ax.grid(True,alpha=.25);fig.tight_layout()
    fig.savefig(ROOT/'figures/02_OBSERVER_TORSION_THEORY.png',dpi=180);plt.close(fig)
    return ans
if __name__=='__main__':
    print(json.dumps(generate(),indent=2,ensure_ascii=False))
