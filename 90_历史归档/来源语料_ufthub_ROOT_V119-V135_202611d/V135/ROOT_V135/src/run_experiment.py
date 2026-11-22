"""Reproducible lattice topology checks and structured results; only c=1."""
from pathlib import Path
from datetime import datetime,timezone
import json,csv,sys
import numpy as np
from topology import links,plaquette_chern,overlap_index,overlap_index_from_links,overlap_zero_mode_chiralities,abelian_anomaly_coeffs
BASE=Path(__file__).resolve().parents[1]
RESULT=BASE/'results'
RESULT.mkdir(parents=True,exist_ok=True)

rows=[]
for N in range(-4,5):
    u,v=links(8,N)
    ch,p=plaquette_chern(u,v)
    a=overlap_index(8,N)
    zero=overlap_zero_mode_chiralities(8,N)
    rows.append({'flux':N,'chern':ch,'index':a['index'],'zero_mode_count':len(zero),
                 'plus_chirality':sum(z>0 for z in zero),'minus_chirality':sum(z<0 for z in zero),
                 'wilson_gap':a['min_abs_wilson_eigenvalue'],
                 'max_plaq_spread':float(np.std(p))})
with (RESULT/'flux_index.csv').open('w',newline='',encoding='utf-8') as f:
    writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)

rng=np.random.default_rng(20261121)
stress=[]
for scale in [0.0,0.02,0.1,0.3,0.6]:
    successes=0; lattice_agree=0;min_gap=100.;top_values=[]
    for j in range(120):
        u,v=links(6,3)
        u=u*np.exp(1j*rng.normal(0,scale,(6,6)))
        v=v*np.exp(1j*rng.normal(0,scale,(6,6)))
        c,_=plaquette_chern(u,v)
        idx=overlap_index_from_links(u,v)
        top_values.append(round(c))
        successes+=int(round(c)==3 and round(idx)==-3)
        lattice_agree+=int(round(idx)==-round(c))
    stress.append({'phase_noise_std_rad':scale,'repetitions':120,
                   'matches_nominal_flux_and_index':successes,
                   'lattice_index_equals_minus_chern':lattice_agree,
                   'chern_min':min(top_values),'chern_max':max(top_values)})
with (RESULT/'gauge_deformation.csv').open('w',newline='',encoding='utf-8') as f:
    writer=csv.DictWriter(f,fieldnames=stress[0].keys());writer.writeheader();writer.writerows(stress)

charges={'Q_L':(1,6),'u_R':(4,3),'d_R':(-2,3),'L_L':(-3,2),'e_R':(-6,1),'nu_R':(0,1)}
family=[]
for label,(q,dim) in charges.items():
    family.append({'field':label,'q_equals_6Y':q,'representation_dimension':dim,
                   'index_for_flux_3':3*q,'cubic_contribution_for_flux_3':3*dim*q**4,
                   'mixed_grav_contribution_for_flux_3':3*dim*q**2})
with (RESULT/'hypercharge_flux_foil.csv').open('w',newline='',encoding='utf-8') as f:
    writer=csv.DictWriter(f,fieldnames=family[0].keys());writer.writeheader();writer.writerows(family)
co=abelian_anomaly_coeffs(3,[v[0] for v in charges.values()],[v[1] for v in charges.values()])
result={'model':'2D U(1) flux + overlap Wilson Dirac toy compactification',
        'units':'c=1 only; hbar,G,epsilon0 not normalized',
        'lattice':8,'m0':1,'flux_data':rows,'deformations':stress,
        'simple_6D_parent_anomaly':co,
        'limitations':['not a 6D anomaly-free model','not proof of physical generations',
                       'flux and internal space are inputs','does not derive hbar, G, alpha',
                       'lattice index sign chosen by specific gamma5 orientation']}
(RESULT/'numeric_results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
print('Flux study:',[(r['flux'],r['index'],r['zero_mode_count']) for r in rows])
print('Deformations:',stress)
print('Anomaly:',co)
