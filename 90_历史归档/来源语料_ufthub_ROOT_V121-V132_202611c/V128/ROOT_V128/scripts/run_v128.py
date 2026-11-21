from pathlib import Path
import sys,json,math,csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).parent))
from v128_core import *
base=Path(__file__).resolve().parents[1]
(base/'results').mkdir(exist_ok=True)
(base/'figures').mkdir(exist_ok=True)
rows=[]
for u in [0,0.3,0.6]:
    for beta in np.linspace(-0.8,0.8,81):
        rows.append(dict(axis_speed_fraction=u,boost_beta=float(beta),mass_candidate_ratio=mass_candidate_ratio(u,float(beta))))
with (base/'results'/'lorentz_boost_SYNTHETIC.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
for u in [0,0.3,0.6]:
    arr=[r for r in rows if r['axis_speed_fraction']==u]
    plt.plot([r['boost_beta'] for r in arr],[r['mass_candidate_ratio'] for r in arr],label=f'u/c={u}')
plt.axhline(1,color='k',ls='--',lw=1)
plt.xlabel('Lorentz boost along helix axis, β')
plt.ylabel("Inferred m' / m from geometric frequency")
plt.title('ROOT V128: coordinate-time helix frequency is not invariant')
plt.legend();plt.tight_layout()
plt.savefig(base/'figures'/'lorentz_noninvariance_SYNTHETIC.png',dpi=160)
plt.close()
R,Rcomponent=sphere_scalar_curvature()
res={
 'version':'ROOT V128',
 'science_status':'conditional math and standard field theory verification; NOT proven four-force unification',
 'helix_boost_u0_beta0.6_mass_ratio':mass_candidate_ratio(0,0.6),
 'boost_u0.3_beta0.6_mass_ratio':mass_candidate_ratio(0.3,0.6),
 '5d_null_projection_v3_0.6c':five_dim_projection(0.6*C,0.8*C),
 'two_sphere_scalar_curvature':str(R),
 'electron_rest_frequency_s_inv':ky_electron_frequency(),
 'muon_electron_mass_ratio_input':MUON_ELECTRON_RATIO,
 'muon_nearest_integer':round(MUON_ELECTRON_RATIO),
 'mutual_difference_from_integer':abs(MUON_ELECTRON_RATIO-round(MUON_ELECTRON_RATIO)),
 'observational_measurements_included':False,
 'notes':['Dirac and SU(2) demonstrations test known mathematical identities','Coordinate-time helix mass proxy fails Lorentz scalar test','5D embedding is an ansatz with unpredicted radius/spectrum']
}
(base/'results'/'audit_results.json').write_text(json.dumps(res,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(res,ensure_ascii=False,indent=2))
