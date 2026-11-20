"""Optional numerical cross-check with NumPy quadrature and WLS independent of core solver."""
from pathlib import Path
import json,sys,math
import numpy as np
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P))
from src.physics import G_REF,Rig,yukawa_form_factor,common_amplitude,yukawa_amplitude_per_alpha
J=json.loads((P/'results'/'numerical_summary.json').read_text(encoding='utf8'))
rig=Rig();a=rig.source_radius_m;M=rig.mass_kg;lam=.25;r=.52
nodes,weights=np.polynomial.legendre.leggauss(80)
y=(nodes+1)*a/2;wy=weights*a/2
mu=nodes;wmu=weights
s=np.sqrt(r*r+y[:,None]**2-2*r*y[:,None]*mu[None,:])
rho=3*M/(4*math.pi*a**3)
U_num=-G_REF*2*math.pi*rho*np.sum(wy*y*y*np.sum(wmu[None,:]*np.exp(-s/lam)/s,axis=1))
U_analytic=-G_REF*M/r*yukawa_form_factor(a/lam)*math.exp(-r/lam)
rel_err=abs(U_num/U_analytic-1)
checks={'finite_sphere_yukawa_volume_integration':rel_err<2e-11}
for name,scenario in J['scenarios'].items():
    pts=scenario['points']; x=np.array([[common_amplitude(rig,z['distance_m'])/1e-8,yukawa_amplitude_per_alpha(rig,z['distance_m'],lam)/1e-8,1.] for z in pts]);
    ys=np.array([z['signal']/1e-8 for z in pts]);ws=np.array([1e-8/z['sem'] for z in pts]);
    val=np.linalg.lstsq(x*ws[:,None],ys*ws,rcond=None)[0];formal=scenario['fit']['newton_yukawa_offset']
    checks[f'np_wls_{name}']=abs(val[0]-formal['beta_G_ratio'])<1e-8 and abs(val[1]-formal['alpha_yukawa'])<1e-8 and abs(val[2]*1e-8-formal['offset_m_s2'])<1e-17
output={'checks':{k:bool(v) for k,v in checks.items()},'pass':bool(all(checks.values())),'finite_sphere_yukawa_potential_numeric':float(U_num),'finite_sphere_yukawa_potential_analytic':float(U_analytic),'relative_error':float(rel_err),'matrix_rank_3_parameter':int(np.linalg.matrix_rank(x)),'note':'independent numerical calculation, NOT empirical observation'}
(P/'results'/'independent_reference.json').write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf8')
print('INDEPENDENT NUMERIC CHECKS:',sum(checks.values()),'/',len(checks),'relative_error=',rel_err)
if not output['pass']:raise SystemExit(1)
