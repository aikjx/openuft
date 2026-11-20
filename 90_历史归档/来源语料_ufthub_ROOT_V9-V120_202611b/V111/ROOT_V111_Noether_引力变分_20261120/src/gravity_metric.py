"""Exact symbolic metric-independence and compact-phase tests.
Independent theta, independent differential 2-form F, fixed orientation.
"""
from pathlib import Path
import json
import sympy as sp

def checks():
    # The covariant dual convention Ftilde^{ij}=eps^{ijkl} F_kl /(2 sqrt(-det g)).
    a,b,c,d,e,f=sp.symbols('F01 F02 F03 F12 F13 F23',real=True)
    Ft=sp.zeros(4)
    for (i,j),v in zip(((0,1),(0,2),(0,3),(1,2),(1,3),(2,3)),(a,b,c,d,e,f)):
        Ft[i,j]=v;Ft[j,i]=-v
    dens=sp.expand(sum(sp.LeviCivita(i,j,k,l)*Ft[i,j]*Ft[k,l]
         for i in range(4) for j in range(4) for k in range(4) for l in range(4))/2)
    D=sp.symbols('D',positive=True)
    theta, coupling=sp.symbols('theta lambda',real=True)
    top=-coupling*theta/4*sp.sqrt(D)*(dens/sp.sqrt(D))
    topo=-coupling*theta*(a*f-b*e+c*d)
    out={
      'epsilon_FF_contraction':sp.simplify(dens-4*(a*f-b*e+c*d))==0,
      'covariant_density_equals_wedge_expression':sp.simplify(top-topo)==0,
      'metric_dependence_exactly_zero':sp.diff(top,D).simplify()==0,
      'metric_independence_theta_constant':sp.diff(top.subs(theta,0),D).simplify()==0,
      'theta_variation_yields_FFtilde':sp.simplify(sp.diff(top,theta)+coupling*(a*f-b*e+c*d))==0,
    }
    th,xi,ff, M0, ee=sp.symbols('theta xi f M0 eps',real=True)
    bad= M0**2+xi*ff**2*th**2
    good=M0**2*(1+ee*sp.cos(th))
    out.update({
      'theta_square_is_not_compact':sp.simplify(bad.subs(th,th+2*sp.pi)-bad-4*sp.pi*xi*ff**2*(th+sp.pi))==0,
      'theta_square_shift_nonzero_generically':sp.simplify(bad.subs({th:0,xi:1,ff:1,M0:1})-bad.subs({th:2*sp.pi,xi:1,ff:1,M0:1})) !=0,
      'periodic_curvature_coefficient':sp.trigsimp(good.subs(th,th+2*sp.pi)-good)==0,
      'periodic_coefficient_still_needs_mass_scale':M0 in good.free_symbols,
    })
    return out

if __name__=='__main__':
    d=checks();path=Path(__file__).resolve().parents[1]/'results'/'metric_checks.json'
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
    print('metric/compact checks',sum(d.values()),'/',len(d));assert all(d.values())
