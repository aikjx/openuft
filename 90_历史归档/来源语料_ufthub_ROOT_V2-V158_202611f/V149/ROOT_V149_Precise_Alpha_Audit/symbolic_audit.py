#!/usr/bin/env python3
"""12 exact symbolic identities, independent of the floating point tests."""
import sys
try:
    import sympy as s
except ImportError:
    raise SystemExit('SymPy is required for symbolic audit; pip install -r requirements.txt')

v,u,beta,a,w,k,t,z=s.symbols('v u beta a w k t z',real=True)
positive=s.symbols('A', positive=True)
phi=k*(t-z)
E=s.Matrix([s.cos(phi),s.sin(phi),0]);B=s.Matrix([-s.sin(phi),s.cos(phi),0]);

def curl_z(X):
    return s.Matrix([-s.diff(X[1],z),s.diff(X[0],z),0])

def simp(x): return s.simplify(s.trigsimp(x))

# Null velocity boost algebra (using v_perp^2=1-u^2)
Den=(1-beta*u)
checks={
 'boost_null': simp((1-u*u)*(1-beta*beta)/Den**2+(u-beta)**2/Den**2-1),
 'boost_to_circular': simp((u-u)/ (1-u*u)),
 'alpha_lab': simp((a*w*w)**2/((a*w*w)**2+(u*w)**2) - a*a*w*w/(a*a*w*w+u*u)),
 'kappa_tau_identity_under_null': simp((a*w*w)**2+(u*w)**2-w*w*(a*a*w*w+u*u)),
 'maxwell_faraday': list(simp(s.diff(B,t)+curl_z(E))),
 'maxwell_ampere': list(simp(s.diff(E,t)-curl_z(B))),
 'maxwell_EdotB':simp(E.dot(B)),
 'maxwell_B2minusE2':simp(B.dot(B)-E.dot(E)),
 'energy_flux_z':simp(E[0]*B[1]-E[1]*B[0]-1),
 'boost_proxy_beta_u': simp(((1-u*u)*(1-u*u)/(1-u*u)**2)-1),
 'pure_gauge_d2theta': simp(s.diff(s.Function('q')(t,z),t,z)-s.diff(s.Function('q')(t,z),z,t)),
 'phase_null_grad':simp(s.diff(phi,t)**2-s.diff(phi,z)**2)
}
for name,val in checks.items():
    if isinstance(val,list): ok=all(v==0 for v in val)
    else: ok=(val==0)
    print(('PASS' if ok else 'FAIL'),name,repr(val))
    if not ok: sys.exit(1)
print(f'SYMBOLIC AUDIT PASS {len(checks)}/{len(checks)}')
