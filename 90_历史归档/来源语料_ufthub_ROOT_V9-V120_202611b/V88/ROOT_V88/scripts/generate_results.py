import sys,os,csv,json,math
from pathlib import Path
from dataclasses import replace
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.bmv import *
ROOT=Path(__file__).resolve().parents[1]

def savecsv(name,headers,rows):
 with (ROOT/'data'/name).open('w',encoding='utf-8-sig',newline='') as f:
  writer=csv.writer(f);writer.writerow(headers);writer.writerows(rows)

def main():
 p=Setup();values=simulate(p)
 rates=np.linspace(0,.2,201)
 dec=[]
 for v in rates:
  q=replace(p,gamma1=float(v),gamma2=float(v))
  dec.append([float(v),negativity(density(q)),pure_concurrence(phases(q))/2])
 savecsv('dephasing_scan_SYNTHETIC.csv',['gamma_each_per_s','negativity_2mass_dephased','ideal_negativity_no_dephasing'],dec)
 massvals=np.geomspace(1e-16,5e-14,121)
 rows=[]
 for m in massvals:
  q=replace(p,m1=float(m),m2=float(m),gamma1=.02,gamma2=.02)
  rows.append([float(m),cross_phase(phases(q)),pure_concurrence(phases(q)),negativity(density(q))])
 savecsv('mass_scan_SYNTHETIC.csv',['mass_each_kg','delta_phase_rad','pure_concurrence','dephased_negativity'],rows)
 distancevals=np.linspace(405e-6,1200e-6,161)
 drows=[]
 for d in distancevals:
  q=replace(p,d=float(d),gamma1=.02,gamma2=.02)
  drows.append([float(d),cross_phase(phases(q)),negativity(density(q))])
 savecsv('distance_scan_SYNTHETIC.csv',['center_distance_m','delta_phase_rad','dephased_negativity'],drows)
 qeq=coulomb_equivalent_charge(p)
 cr=[]
 for ratio in [-100,-10,-1,-.1,0,.1,1,10,100]:
  q=replace(p,q1=qeq,q2=qeq*ratio)
  cr.append([ratio,cross_phase(phases(q)),negativity(density(q))])
 savecsv('charge_false_positive_SYNTHETIC.csv',['q1q2_over_gravity_equivalent','total_nonlocal_phase_rad','ideal_negativity'],cr)
 # Find threshold dephasing gamma* with gamma1=gamma2=gamma, assuming monotonic in this channel
 lo,hi=0.0,0.2
 for _ in range(55):
  mid=(lo+hi)/2
  q=replace(p,gamma1=mid,gamma2=mid)
  if negativity(density(q))>1e-13:lo=mid
  else:hi=mid
 threshold=(lo+hi)/2
 summary={**values,
 'critical_local_dephasing_rate_per_mass_per_s_for_1s':threshold,
 'critical_rate_model':'independent local Z-dephasing with coherence factor exp(-gamma*t), frozen paths',
 'charge_equivalence_in_electron_charges':qeq/1.602176634e-19,
 'ideal_phase_formula':'G*m1*m2*t/hbar * [1/r00-1/r01-1/r10+1/r11]',
 'density_matrix':'4x4 local dephasing channel + partial transpose negativity',
 'limitations':['frozen path approximation','no electromagnetic shielding dynamics','no gravity quantization inference','no actual experimental observations'],
 'research_date':'2026-11-18'}
 (ROOT/'results'/'numerical_summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf8')
 plt.rcParams['axes.unicode_minus']=False
 fig,ax=plt.subplots(figsize=(8,4.5));ax.plot(rates,[x[1] for x in dec],label='dephased');ax.plot(rates,[x[2] for x in dec],ls='--',label='no dephasing')
 ax.axvline(threshold,ls=':',label=f'critical gamma={threshold:.4f}/s');ax.set(xlabel='Gamma, each mass (1/s)',ylabel='Negativity',title='Local dephasing can eliminate gravitational entanglement');ax.legend();fig.tight_layout();fig.savefig(ROOT/'results'/'dephasing_threshold.png',dpi=160);plt.close(fig)
 fig,ax=plt.subplots(figsize=(8,4.5));ax.semilogx(massvals,[x[2] for x in rows],label='pure concurrence');ax.semilogx(massvals,[x[3] for x in rows],label='dephased negativity (gamma=0.02/s)');ax.set(xlabel='Mass each (kg)',ylabel='Entanglement measure (different normalizations)',title='Mass dependence, idealized two-mass setup');ax.legend();fig.tight_layout();fig.savefig(ROOT/'results'/'mass_scan.png',dpi=160);plt.close(fig)
 fig,ax=plt.subplots(figsize=(8,4.5));ax.plot(np.array(distancevals)*1e6,[x[1] for x in drows]);ax.set(xlabel='Center distance (micrometers)',ylabel='Nonlocal phase (radians)',title='Phase depends on branch geometry');fig.tight_layout();fig.savefig(ROOT/'results'/'distance_scan.png',dpi=160);plt.close(fig)
 fig,ax=plt.subplots(figsize=(8,4.5));ax.plot([x[0] for x in cr],[x[1] for x in cr],'o-');ax.axhline(cross_phase(phases(p)),linestyle='--',label='gravity only');ax.set(xlabel='q1*q2 / (4 pi eps0 G m1 m2)',ylabel='Total nonlocal phase (rad)',title='Coulomb 1/r is geometrically degenerate with Newton 1/r');ax.legend();fig.tight_layout();fig.savefig(ROOT/'results'/'coulomb_degeneracy.png',dpi=160);plt.close(fig)
 print(json.dumps({'delta':values['nonlocal_phase_rad'],'C':values['ideal_concurrence'],'N':values['ideal_negativity'],'critical_gamma':threshold,'e_charge_ratio':qeq/1.602176634e-19},indent=2))

if __name__=='__main__':main()
