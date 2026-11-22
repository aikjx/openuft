import math,csv,json, pathlib
import numpy as np
from scipy.optimize import brentq
import mpmath as mp
ROOT=pathlib.Path(__file__).resolve().parents[1]
mp.mp.dps=45
rows=[]
for R,p in [(0.25,0.0),(1.,0.6),(2.,-0.8),(0.8,0.95),(3.,0.999)]:
    omega=math.sqrt(1-p*p)/R
    kappa=R*omega**2; tau=p*omega
    residual=kappa*kappa+tau*tau-omega*omega
    R_back=kappa/(kappa*kappa+tau*tau)
    p_back=tau/math.sqrt(kappa*kappa+tau*tau)
    rows.append(dict(R=R,p=p,omega=omega,kappa=kappa,tau=tau,residual=residual,R_recovered=R_back,p_recovered=p_back))
with open(ROOT/'data'/'helix_checks.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
zeros=[]
for n in range(1,21):
    z=mp.zetazero(n)
    zeros.append(dict(n=n,imaginary_part=mp.nstr(mp.im(z),32),real_part=mp.nstr(mp.re(z),12),zeta_abs=mp.nstr(abs(mp.zeta(z)),8)))
with open(ROOT/'data'/'zeta_zeros.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(zeros[0]));w.writeheader();w.writerows(zeros)
# One-dimensional periodic helix arclength Laplacian: eigenvalues (2pi n/L)^2.
# A constant torsion phase shifts periodic boundary eigenvalues, but is not the zeta spectrum.
L=2*math.pi
spectra=[dict(n=n,laplacian_eigenvalue=n*n,twisted_eigenvalue=(n+0.3)**2) for n in range(-10,11)]
with open(ROOT/'data'/'toy_spectrum.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(spectra[0]));w.writeheader();w.writerows(spectra)
checks={'max_helix_residual':max(abs(r['residual']) for r in rows),'max_R_reconstruction_error':max(abs(r['R']-r['R_recovered']) for r in rows),'max_p_reconstruction_error':max(abs(r['p']-r['p_recovered']) for r in rows),'max_zeta_zero_residual':max(float(mp.mpf(z['zeta_abs'])) for z in zeros),'n_zeros':len(zeros),'zeta_spectrum_identification_proven':False,'four_force_unification_proven':False}
(ROOT/'data'/'summary.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print(json.dumps(checks,indent=2))
assert checks['max_helix_residual']<1e-12
assert checks['max_R_reconstruction_error']<1e-12
assert checks['max_p_reconstruction_error']<1e-12
assert checks['max_zeta_zero_residual']<1e-35
