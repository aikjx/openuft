"""Deterministic analyses using saved V100 theoretical polygon + independent controls."""
from __future__ import annotations
import csv,json,math
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.constants import e, m_e, c
from src.v102_core import curvature_from_polygon,field_and_radiation,circle,torus_knot
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'; OUT=ROOT/'results'; FIG=ROOT/'figures'

def main():
    pts=np.loadtxt(DATA/'V100_ORBIT_21Q_INPUT_THEORY.csv',delimiter=',',skiprows=1)
    g=curvature_from_polygon(pts)
    data=field_and_radiation(g)
    B_profile=data.pop('B_profile_T')
    baseline=json.loads((DATA/'V100_RADIATION_INPUT_THEORY.json').read_text(encoding='utf8'))
    old=baseline['energy_loss_J_per_period']
    data.update({"historical_V100_radiation_J":old,"relative_radiation_reconstruction_error":abs(data['E_rad_from_kappa_J']-old)/old,
                 "source":"V100 saved 1201-point theoretical polygon, NOT experimental data",
                 "claim_limit":"Conditioned on a smooth closed embedded nontrivial knot ONLY for the 4pi topological floor; embedding of continuum V100 orbit NOT interval certified",
                 "global_Maxwell_field_reconstructed":False,"force_unification_proven":False})
    (OUT/'V102_SUMMARY_THEORY.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    with (OUT/'V100_RECONSTRUCTED_B_PROFILE_THEORY.csv').open('w',encoding='utf8',newline='') as f:
        w=csv.writer(f);w.writerow(['arc_position_m','curvature_inv_m','required_Bperp_T'])
        w.writerows(zip(g['cum_arc_m'],g['kappa_per_m'],B_profile))
    plt.figure(figsize=(9,4.5))
    plt.plot(g['cum_arc_m'],B_profile,lw=1.1,label='Required transverse magnetic field (T)')
    plt.axhline(data['B_mean_T'],ls='--',alpha=.7,label='Length-weighted mean')
    plt.xlabel('Path arc length (m)');plt.ylabel('B perpendicular (T)');plt.title('ROOT V102 | V100 trajectory: field reconstructed from curvature')
    plt.grid(alpha=.25);plt.legend();plt.tight_layout();plt.savefig(FIG/'01_MAGNETIC_PROFILE_THEORY.png',dpi=150);plt.close()
    rows=[]
    for beta in [.02,.05,.1,.2,.5,.8]:
        row=field_and_radiation(g,beta=beta);row.pop('B_profile_T');rows.append({"beta":beta,"B_mean_T":row['B_mean_T'],"B_knot_lower_T":row['B_knot_lower_T'],"E_rad_J":row['E_rad_from_kappa_J']})
    with (OUT/'BETA_SCAN_THEORY.csv').open('w',encoding='utf8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    plt.figure(figsize=(8,4.5))
    plt.plot([r['beta'] for r in rows],[r['B_mean_T'] for r in rows],marker='o',label='Required B mean')
    plt.plot([r['beta'] for r in rows],[r['B_knot_lower_T'] for r in rows],marker='s',label='Knot lower bound (conditional)')
    plt.xlabel('v / c');plt.ylabel('Magnetic field (T)');plt.title('ROOT V102 | Same geometry, variable particle speed')
    plt.grid(alpha=.25);plt.legend();plt.tight_layout();plt.savefig(FIG/'02_SPEED_SCAN_THEORY.png',dpi=150);plt.close()
    controls=[]
    for label,p in [('Circle',circle(.01,1800)),('Torus_2_3',torus_knot(2,3,num=3500)),('Torus_3_5',torus_knot(3,5,num=3500)),('V100_numerical',pts)]:
        gg=curvature_from_polygon(p)
        r=field_and_radiation(gg);r.pop('B_profile_T')
        controls.append({"name":label,"L_m":gg['length_m'],"total_curvature":gg['total_curvature'],"Cauchy_ratio":r['Cauchy_ratio'],"B_mean_T":r['B_mean_T'],"B_rms_T":r['B_rms_T'],"Erad_J":r['E_rad_from_kappa_J']})
    with (OUT/'INDEPENDENT_GEOMETRY_CONTROLS_THEORY.csv').open('w',encoding='utf8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(controls[0]));w.writeheader();w.writerows(controls)
    return data

if __name__=='__main__':
    print(json.dumps(main(),indent=2,ensure_ascii=False))
