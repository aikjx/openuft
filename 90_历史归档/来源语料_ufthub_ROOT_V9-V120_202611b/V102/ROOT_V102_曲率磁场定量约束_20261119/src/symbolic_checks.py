"""Symbolic and dimension checks; 0 exceptions means pass."""
from __future__ import annotations
import sympy as s

def audit():
    K,L,m,v,gam,q,eps,c,kap,B=s.symbols('K L m v gamma q epsilon c kappa B',nonzero=True, real=True)
    checks={}
    # B = -gamma*m*v*kappa/q (binormal sign is frame-dependent)
    checks['Bforce_identity']=s.simplify(q*v*(-gam*m*v*kap/q)-(-gam*m*v*v*kap))==0
    # Radiation coefficient equality under B^2 = (gamma m v/q)^2 kappa^2
    E_B=q**4*gam**2*v/(6*s.pi*eps*m**2*c**3)*B**2
    E_k=q**2*gam**4*v**3/(6*s.pi*eps*c**3)*kap**2
    checks['radiation_field_curvature_exact']=s.simplify(E_B.subs(B,gam*m*v*kap/q)-E_k)==0
    # Variance identity (Cauchy gap)
    K2=s.symbols('K2',positive=True)
    checks['variance_identity']=s.simplify(K2/L-(K/L)**2-(K2*L-K**2)/L**2)==0
    checks['four_pi_square']=s.simplify((4*s.pi)**2-4*(2*s.pi)**2)==0
    # SI dimensional exponents vector (M,L,T,I)
    M=s.Matrix([1,0,0,0]); Len=s.Matrix([0,1,0,0]); T=s.Matrix([0,0,1,0]); I=s.Matrix([0,0,0,1])
    d_q=I+T; d_eps=2*I+4*T-M-3*Len; d_v=Len-T; d_c=d_v; d_k=-Len; d_m=M; d_B=M-I-2*T
    checks['B_SI_dimension']=d_m+d_v+d_k-d_q==d_B
    checks['Ecurv_SI_dimension']=2*d_q-d_eps+3*d_v-3*d_c+2*d_k+Len==M+2*Len-2*T
    checks['Efield_SI_dimension']=4*d_q+ d_v+2*d_B+Len-d_eps-2*d_m-3*d_c==M+2*Len-2*T
    checks['B_rms_lower_dimension']=d_m+d_v-d_q-Len==d_B
    checks['Cauchy_gap_dimension']=2*d_k*0 + 2*d_k+Len == -Len # ∫ k² ds
    assert all(bool(x) for x in checks.values()), checks
    return {k:bool(v) for k,v in checks.items()}

if __name__=='__main__':
    import json
    print(json.dumps(audit(),indent=2))
