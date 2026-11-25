"""Symbolic, independent differentiation: scalar-based A and h are pure gauge."""
import json
from pathlib import Path
import sympy as s

coords = s.symbols('t x y z', real=True)
t,x,y,z=coords
# Includes both traveling helix-like phase and a nonplanar smooth distortion.
theta = s.sin(2*(t-z))*s.cos(x) + s.exp(y)*s.cos(t+x)
A = [s.diff(theta, q) for q in coords]
F = s.Matrix(4, 4, lambda i,j: s.simplify(s.diff(A[j],coords[i])-s.diff(A[i],coords[j])))
assert F==s.zeros(4), 'A=dtheta has nonzero curvature!'
h = s.Matrix(4,4,lambda i,j:s.diff(theta,coords[i],coords[j]))
# R_mnrs = 1/2 (d_r d_n h_ms + d_s d_m h_nr - d_r d_m h_ns - d_s d_n h_mr)
checks=0
for m in range(4):
    for n in range(4):
        for r in range(4):
            for q in range(4):
                value=s.diff(h[m,q],coords[r],coords[n])+s.diff(h[n,r],coords[q],coords[m])-s.diff(h[n,q],coords[r],coords[m])-s.diff(h[m,r],coords[q],coords[n])
                assert s.simplify(value)==0, (m,n,r,q)
                checks+=1
# A concrete nonpure-gauge transverse wave A_x=cos(t-z), A_y=sin(t-z)
a = [s.Integer(0),s.cos(t-z),s.sin(t-z),s.Integer(0)]
f = s.Matrix(4,4,lambda i,j:s.diff(a[j],coords[i])-s.diff(a[i],coords[j]))
eta=s.diag(-1,1,1,1)
div=[s.trigsimp(sum(eta[i,i]*s.diff(f[i,j],coords[i]) for i in range(4))) for j in range(4)]
assert div==[0]*4
assert f[0,1]!=0 and f[0,2]!=0
# Real TT wave h_11=cos(t-z), h_22=-cos(t-z).
hTT=s.zeros(4); hTT[1,1]=s.cos(t-z);hTT[2,2]=-s.cos(t-z)
r0101=s.simplify(s.diff(hTT[0,1],t,x) - s.Rational(1,2)*s.diff(hTT[1,1],t,2) -s.Rational(1,2)*s.diff(hTT[0,0],x,2))
assert s.simplify(r0101-s.cos(t-z)/2)==0
report={'scalar_phase_curvature_F_zeros':16,'scalar_phase_riemann_zero_components':checks,
        'real_transverse_Maxwell_divergence_zero':True,
        'TT_wave_R0101':'cos(t-z)/2',
        'hypotheses':'Smooth scalar phase; flat spacetime; local ansatz A=dtheta, h=Hessian(theta).'}
path=Path(__file__).resolve().parent/'results'/'symbolic.json'
path.parent.mkdir(exist_ok=True)
path.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
print('SYMBOLIC AUDIT OK:',report)
