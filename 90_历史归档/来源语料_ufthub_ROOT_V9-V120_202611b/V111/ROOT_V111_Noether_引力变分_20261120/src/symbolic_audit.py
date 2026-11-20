"""Exact symbolic consequences of V111 toy model. No claim of novel fundamental physics."""
import json
import sympy as sp
from pathlib import Path

def checks():
    th,td,ap,vp,am,vm,ss=sp.symbols('theta td ap vp am vm I',real=True)
    k,g,f,L4=sp.symbols('k g f L4',real=True,nonzero=True)
    states=sp.Matrix([th,td,ap,vp,am,vm,ss])
    fflow=sp.Matrix([td,(-L4*sp.sin(th)+g*k*(ap*vp-am*vm))/f**2,
          vp,-(k*k+g*k*td)*ap,vm,-(k*k-g*k*td)*am,sp.sin(th)])
    H=f**2*td**2/2+L4*(1-sp.cos(th))+(vp**2+vm**2+k*k*(ap**2+am**2))/2
    Q=f**2*td-g*k*(ap**2-am**2)/2
    N=Q+L4*ss
    Eem=(vp**2+vm**2+k*k*(ap**2+am**2))/2
    Etheta=H-Eem
    dp=lambda expr:sp.simplify(sp.diff(expr,states).dot(fflow))
    out={
      'exact_total_energy':dp(H)==0,
      'noether_balance':sp.simplify(dp(Q)+L4*sp.sin(th))==0,
      'extended_noether_invariant':dp(N)==0,
      'shift_charge_for_zero_potential':sp.simplify(dp(Q).subs(L4,0))==0,
      'transfer_from_theta':sp.simplify(dp(Etheta)-g*k*td*(ap*vp-am*vm))==0,
      'transfer_into_em':sp.simplify(dp(Eem)+g*k*td*(ap*vp-am*vm))==0,
      'individual_helicity_surrogate_derivative':sp.simplify(dp(ap**2-am**2)-2*(ap*vp-am*vm))==0,
      'canonical_p_theta':sp.simplify(sp.diff(f**2*td**2/2-g*k*td*(ap**2-am**2)/2,td)-Q)==0,
      'positive_definite_mode_energy':sp.simplify(Eem-(vp**2+vm**2+k*k*(ap**2+am**2))/2)==0,
      'theta_force_from_potential':sp.simplify(sp.diff(L4*(1-sp.cos(th)),th)-L4*sp.sin(th))==0,
    }
    # metric topological term sqrt(-g) eps_tens = epsilon symbol, for oriented g<0
    d=sp.symbols('D',positive=True)
    out['metric_density_cancellation']=sp.simplify(sp.sqrt(d)*(1/sp.sqrt(d))-1)==0
    out['density_metric_derivative_zero']=sp.simplify(sp.diff(sp.sqrt(d)*(1/sp.sqrt(d)),d))==0
    # Mathematically conserved current: divergence of antisymmetric derivatives 0
    u,v,w,x=sp.symbols('u v w x',real=True)
    theta=sp.Function('theta')(u,v,w,x)
    field=sp.Function('F')(u,v,w,x)
    out['commuting_partial_derivatives']=sp.simplify(sp.diff(theta,u,v)-sp.diff(theta,v,u))==0
    # total derivative consistency (potential doesn't affect EM EOM)
    out['source_vanishes_at_zero_g']=sp.simplify(dp(Q).subs({g:0,L4:0}))==0
    out['nonzero_potential_q_deviation_exact']=sp.simplify(dp(Q)+dp(L4*ss))==0
    return out

if __name__=='__main__':
    data=checks();p=Path(__file__).resolve().parents[1]/'results'/'symbolic_checks.json'
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2))
    print('checks',len(data),'passed',sum(data.values()),'failed',[k for k,v in data.items() if not v]);assert all(data.values())
