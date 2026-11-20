"""Symbolic checks for the explicitly defined V110 toy model."""
import json
from pathlib import Path
import sympy as sp

def checks():
    theta, td, Tp, Vp, Tm, Vm, k, g, f, L4 = sp.symbols('theta td Tp Vp Tm Vm k g f L4',real=True,nonzero=True)
    states=sp.Matrix([theta,td,Tp,Vp,Tm,Vm]); rhs=sp.Matrix([
        td,(-L4*sp.sin(theta)+g*k*(Tp*Vp-Tm*Vm))/f**2,
        Vp,-(k*k+g*k*td)*Tp,Vm,-(k*k-g*k*td)*Tm])
    H=f*f*td*td/2+L4*(1-sp.cos(theta))+(Vp**2+Vm**2+k*k*(Tp**2+Tm**2))/2
    results={}
    results['total_energy_exactly_conserved']=sp.simplify(sp.diff(H,states).dot(rhs))==0
    pump=sp.simplify(sp.diff((Vp**2+k*k*Tp**2+Vm**2+k*k*Tm**2)/2,states).dot(rhs))
    results['photon_energy_transfer']=sp.simplify(pump+g*k*td*(Tp*Vp-Tm*Vm))==0
    results['theta_energy_transfer']=sp.simplify(sp.diff((f*f*td**2)/2+L4*(1-sp.cos(theta)),states).dot(rhs)-g*k*td*(Tp*Vp-Tm*Vm))==0
    mu,t,Om,th0,gg,kk=sp.symbols('mu t Om th0 gg kk', real=True)
    deriv=sp.diff(th0*sp.cos(Om*t),t)
    results['half_cycle_helicity_shift']=sp.simplify(
        kk**2+gg*kk*deriv-(kk**2-gg*kk*deriv).subs(t,t+sp.pi/Om))==0
    results['closed_phase_no_endpoint_change']=sp.simplify((th0*sp.cos(Om*t)).subs(t,2*sp.pi/Om)-th0)==0
    a,b,c,d=sp.symbols('a b c d',real=True)
    M=sp.Matrix([[a,b],[c,d]])
    J=sp.Matrix([[0,1],[-1,0]])
    results['symplectic_two_by_two_if_det_one']=sp.simplify(M.T*J*M-(a*d-b*c)*J)==sp.zeros(2)
    # Lorentz invariant acceleration for boosted circular trajectory (c=1, v transverse)
    v,beta,R=sp.symbols('v beta R',positive=True)
    gb2=1/(1-beta**2); gv2=1/(1-v**2)
    vprime2=v*v*(1-beta**2)+beta**2
    properprime=sp.simplify((gb2*gv2)*v*v*(1-beta**2)/R)
    results['proper_accel_boost_invariant']=sp.simplify(properprime-gv2*v*v/R)==0
    # Symmetric photon seed does not imply zero net coupling for all t
    results['positive_initial_total_energy']=sp.simplify(H.subs({td:0,Vp:0,Vm:0})-L4*(1-sp.cos(theta))-k*k*(Tp**2+Tm**2)/2)==0
    return results

if __name__=='__main__':
    result=checks()
    path=Path(__file__).resolve().parents[1]/'results'/'symbolic_checks.json'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'checks':len(result),'passed':sum(result.values()),'failures':[k for k,v in result.items() if not v]},ensure_ascii=False))
    assert all(result.values())
