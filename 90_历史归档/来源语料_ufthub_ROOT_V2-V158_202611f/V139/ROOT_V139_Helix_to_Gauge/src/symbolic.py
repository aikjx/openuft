"""Symbolic proof checks; needs sympy as optional dependency."""
import json
import sympy as sp
from pathlib import Path

def calculate():
    a,w,u,k,tau,th,ph,m=sp.symbols('a w u k tau th ph m', real=True)
    s=sp.symbols('s',positive=True)
    # null condition u²+a²ω²=1, forward/inverse geometric equivalence
    w2=k*k+tau*tau
    inverse_a=k/w2
    inverse_u=tau/sp.sqrt(w2)
    inverse_w=sp.sqrt(w2)
    checks={
      'reconstruction_speed': sp.simplify(inverse_a**2*inverse_w**2+inverse_u**2-1),
      'reconstruction_curvature': sp.simplify(inverse_a*inverse_w**2-k),
      'reconstruction_torsion': sp.simplify(inverse_u*inverse_w-tau),
      'berry_curvature':sp.simplify(sp.diff(m*(1-sp.cos(th))/2,th)-m*sp.sin(th)/2),
      'chern_flux':sp.simplify(sp.integrate(m*sp.sin(th)/2,(th,0,sp.pi))*sp.integrate(1,(ph,0,2*sp.pi))-2*sp.pi*m)
    }
    # Differential geometric identity of the coordinate map n(θ,φ)
    n=sp.Matrix([sp.sin(th)*sp.cos(m*ph),sp.sin(th)*sp.sin(m*ph),sp.cos(th)])
    q=sp.trigsimp(sp.expand_trig(n.dot(n.diff(th).cross(n.diff(ph)))/2)-m*sp.sin(th)/2)
    checks['orientation_pullback']=sp.simplify(q)
    # Single-orientation Berry pullback is a simple 2-form and F∧F=0,
    # which forbids F·tilde(F)≠0 and hence forbids generic E·B≠0 fields.
    dt=sp.symbols('t0:4',real=True)
    dp=sp.symbols('p0:4',real=True)
    F=lambda i,j:dt[i]*dp[j]-dt[j]*dp[i]
    checks['simple_two_form_pfaffian']=sp.expand(F(0,1)*F(2,3)-F(0,2)*F(1,3)+F(0,3)*F(1,2))
    # Two independent simple 2-forms can have a nonzero Pfaffian.
    J=lambda i,j,k,l: sp.Integer(1) if (i,j)==(k,l) else (sp.Integer(-1) if (i,j)==(l,k) else sp.Integer(0))
    F1=lambda i,j:J(i,j,0,1)
    F2=lambda i,j:J(i,j,2,3)
    Fs=lambda i,j:F1(i,j)+F2(i,j)
    checks['two_textures_pfaffian_minus_one']=sp.expand(Fs(0,1)*Fs(2,3)-Fs(0,2)*Fs(1,3)+Fs(0,3)*Fs(1,2)-1)
    # fixed speed: power E κ N · T = 0
    T=sp.Matrix([-a*w*sp.sin(w*s),a*w*sp.cos(w*s),u])
    N=sp.Matrix([-sp.cos(w*s),-sp.sin(w*s),0])
    checks['force_zero_power']=sp.trigsimp(T.dot(N))
    return {key:str(value) for key,value in checks.items()}

if __name__=='__main__':
    result=calculate()
    output=Path(__file__).resolve().parents[1]/'results'/'symbolic.json'
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(result,indent=2,ensure_ascii=False))
    if any(v!='0' for v in result.values()): raise SystemExit('SYMBOLIC CHECK FAILED')
    print('All symbolic identities verified')
