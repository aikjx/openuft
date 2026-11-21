import math,json
from pathlib import Path
G=6.67430e-11;c=299792458.;mu0=4*math.pi*1e-7;g=9.80665
out={'constants_SI':{'G':G,'c':c,'mu0_approx':mu0},'gravity':{},'rotation':{},'magnet':{}}
for r in [1,10,100]:out['gravity'][str(r)]={'mass_kg':g*r*r/G,'rest_energy_J':g*r*r/G*c*c}
for r in [1,10,100,1000]:out['rotation'][str(r)]={'rpm_1g':60/(2*math.pi)*math.sqrt(g/r)}
for B in [1,10,30]:
 V=4*math.pi/3;E=B*B/(2*mu0)*V
 out['magnet'][str(B)]={'field_energy_J':E,'energy_equivalent_mass_kg':E/c**2,'point_mass_approx_g_at_1m':G*E/c**2}
# 1D Dirac on circle with periodic bc: gauge holonomy invariant under a->a+2pi/L
L=7.3;a=.4; shift=2*math.pi/L
lambdas=lambda aa:sorted([(2*math.pi*n/L+aa)**2 for n in range(-25,26)])[:10]
# compare spectral sets over sufficiently large truncation with margin
err=max(abs(x-y) for x,y in zip(lambdas(a),lambdas(a+shift)))
out['spectral']={'L':L,'a':a,'holonomy_real':math.cos(a*L),'holonomy_imag':math.sin(a*L),'gauge_shift':shift,'first_10_squared_eigenvalues_truncated_set_max_diff':err}
# standard speed helix: kappa=R*w*w, tau=p*w; p=sqrt(1-(R*w)^2)
rows=[]
for R,w in [(1,.2),(2,.3),(.7,.8),(3,.1)]:
 p=math.sqrt(1-(R*w)**2);k=R*w*w;t=p*w
 rows.append({'R':R,'omega':w,'p':p,'kappa':k,'tau':t,'identity_residual':k*k+t*t-w*w})
out['helix']=rows
Path(__file__).resolve().parents[1].joinpath('data/results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'spectral_error':err,'max_helix_residual':max(abs(x['identity_residual']) for x in rows)},indent=2))
