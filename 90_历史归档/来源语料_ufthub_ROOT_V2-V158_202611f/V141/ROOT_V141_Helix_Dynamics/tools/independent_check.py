#!/usr/bin/env python3
"""Optional SciPy DOP853 and native RK4 comparison for V141."""
import json
import sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE))
from src.coupled import Params, integrate, rhs, diagnostic_summary


def main():
    try:
        from scipy.integrate import solve_ivp
    except ImportError:
        print('SciPy optional; skipped independent DOP853 comparison.')
        return 0
    p=Params()
    initial=(0.3,0.2,0.0,0.3)
    reference=solve_ivp(lambda t,y: rhs(y,p),(0,80),initial,
                        method='DOP853',rtol=1e-12,atol=1e-13,dense_output=True)
    if not reference.success:
        raise RuntimeError(reference.message)
    comparison={
       'method_a':'project RK4 dt=0.005',
       'method_b':'SciPy solve_ivp DOP853 rtol=1e-12 atol=1e-13',
       'method_b_success':bool(reference.success),
       'method_b_steps':len(reference.t),
    }
    coarse=integrate(initial,t_max=80,dt=.005,p=p)
    fine=integrate(initial,t_max=80,dt=.0025,p=p)
    ya=[coarse[-1][k] for k in ('a','v','theta','w')]
    yb=[fine[-1][k] for k in ('a','v','theta','w')]
    yc=reference.y[:,-1]
    comparison['max_final_RK4_0.005_vs_DOP853']=max(abs(x-y) for x,y in zip(ya,yc))
    comparison['max_final_RK4_0.0025_vs_DOP853']=max(abs(x-y) for x,y in zip(yb,yc))
    comparison['max_final_RK4_0.005_vs_0.0025']=max(abs(x-y) for x,y in zip(ya,yb))
    comparison['fine_energy_relative_error']=diagnostic_summary(fine,p)['max_relative_energy_drift']
    comparison['note']='Independent numerical solution of an assumed ODE; not an independent physics experiment.'
    with (BASE/'results'/'independent_integrator_check.json').open('w',encoding='utf-8') as f:
        json.dump(comparison,f,ensure_ascii=False,indent=2)
    print(json.dumps(comparison,indent=2,ensure_ascii=False))
    if comparison['max_final_RK4_0.005_vs_DOP853']>=1e-7:
        raise AssertionError('independent numerical solver mismatch')
    return 0

if __name__=='__main__':
    sys.exit(main())
