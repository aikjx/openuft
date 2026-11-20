"""Truly separate numerical quadrature of 3D spherical Yukawa kernel, outside sphere.
Normalized source uses uniform mass/charge, direct 2D Gauss-Legendre integration.
"""
from pathlib import Path
import json,sys,math
import numpy as np
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from src.physics import finite_envelope

a=.09;r=.28;lam=.16
N=120
x,w=np.polynomial.legendre.leggauss(N)
s=.5*a*(x+1);ws=.5*a*w
v=x;wv=w
rr=np.sqrt(r*r+s[:,None]**2-2*r*s[:,None]*v[None,:])
k=np.exp(-rr/lam)/rr
I=np.sum((s*s*ws)[:,None]*wv[None,:]*k)
# For potential phi=-G M/r * finite_envelope, direct uniform sphere integral ratio:
# (rho 2pi integral ds s^2 dt k)/(rho 4pi a^3/3 / r) = 3r/(2a^3) * I
numeric=3*r/(2*a**3)*I
analytic=finite_envelope(a,r,lam)
relative=abs(numeric-analytic)/analytic
report={'model':'uniform Yukawa source spherical volume integration','n_gauss_each_dimension':N,'analytic':analytic,'direct_2D_quadrature':numeric,'relative_error':relative,'status':'independent mathematical model check, not experiment'}
(root/'results'/'independent_volume_integral.json').write_text(json.dumps(report,indent=2))
print(report)
assert relative < 1e-11
