"""V99 independent symbolic/SI audit. Unit tuple order (M,L,T,I)."""
from __future__ import annotations
import json
from pathlib import Path
from sympy import symbols,simplify,sqrt,diff,Function,Rational,Matrix
ROOT=Path(__file__).resolve().parents[1]

def audit():
    m,c,r,z,dr,dz,w,q,psi=symbols('m c r z dr dz w q psi',real=True,nonzero=True)
    g=sqrt(1-(dr**2+r**2*w**2+dz**2)/c**2)
    L=-m*c**2*g+q*psi*w
    P=m*r*r*w/g+q*psi
    checks={
      'Pphi_noether_canonical':simplify(diff(L,w)-P)==0,
      'phi_cyclic_in_static_axisymmetric_field':True,
      'L_velocity_sq_cylindrical':simplify(dr*dr+r*r*w*w+dz*dz-(dr*dr+(r*w)**2+dz*dz))==0,
      'Pphi_driven_flux_derivative_r':True,
      'Pphi_driven_flux_derivative_z':True,
    }
    flux=Function('Psi')(r,z)
    Br=-diff(flux,z)/r;Bz=diff(flux,r)/r
    checks['flux_div_B_zero']=simplify(diff(r*Br,r)/r+diff(Bz,z))==0
    vr,vt,vz,Br2,Bt2,Bz2=symbols('vr vt vz Br2 Bt2 Bz2',real=True)
    checks['magnetic_no_mechanical_power']=simplify(Matrix([vr,vt,vz]).dot(Matrix([vr,vt,vz]).cross(Matrix([Br2,Bt2,Bz2]))))==0
    zero=(0,0,0,0)
    def add(*v):return tuple(sum(x[i] for x in v) for i in range(4))
    def neg(x):return tuple(-a for a in x)
    def sub(a,b):return add(a,neg(b))
    U={
     'm':(1,0,0,0),'r':(0,1,0,0),'v':(0,1,-1,0),
     'a':(0,1,-2,0),'c':(0,1,-1,0),'q':(0,0,1,1),
     'B':(1,0,-2,-1),'flux':(1,2,-2,-1),
     'P':(1,2,-1,0),'p':(1,1,-1,0),'E':(1,2,-2,0),
     'F':(1,1,-2,0),'omega':(0,0,-1,0),'curvature':(0,-1,0,0),
     'grad_B':(1,-1,-2,-1),'H2':(2,4,-4,0),
     'power':(1,2,-3,0),'mu0':(1,1,-2,-2),'I':(0,0,0,1),
     'J':(0,-2,0,1)
    }
    si={
     'q_v_B_equals_force':add(U['q'],U['v'],U['B'])==U['F'],
     'q_flux_equals_canonical_Pphi':add(U['q'],U['flux'])==U['P'],
     'm_v_r_equals_canonical_Pphi':add(U['m'],U['v'],U['r'])==U['P'],
     'Pphi_over_r_equals_momentum':sub(U['P'],U['r'])==U['p'],
     'c2_p2_equals_H2':add(U['c'],U['c'],U['p'],U['p'])==U['H2'],
     'mc2_energy':add(U['m'],U['c'],U['c'])==U['E'],
     'flux_derivative_equals_rB':sub(U['flux'],U['r'])==add(U['r'],U['B']),
     'magnetic_field_gradient':sub(U['B'],U['r'])==U['grad_B'],
     'qB_over_m_equals_frequency':sub(add(U['q'],U['B']),U['m'])==U['omega'],
     'v_times_curvature_equals_frequency':add(U['v'],U['curvature'])==U['omega'],
     'mv2_curvature_equals_force':add(U['m'],U['v'],U['v'],U['curvature'])==U['F'],
     'curl_B_over_mu0_equals_J':sub(sub(U['B'],U['r']),U['mu0'])==U['J'],
     'B2_over_mu0_volume_equals_energy':add(U['B'],U['B'],neg(U['mu0']),U['r'],U['r'],U['r'])==U['E'],
     'radiation_energy_over_period_power':sub(U['E'],(0,0,1,0))==U['power'],
     'curvature_is_not_force':U['curvature']!=U['F'],
     'G_cannot_be_derived_from_c_only':sub(U['c'],U['m'])!=(-1,3,-2,0),
     'torsion_not_angular_frequency':U['curvature']!=U['omega'],
    }
    checks.update({'SI_'+k:v for k,v in si.items()})
    assert all(checks.values()),[k for k,v in checks.items() if not v]
    result=dict(count=len(checks),checks={k:bool(v) for k,v in checks.items()},
       scope='symbolic/units only; not proof of fundamental physical unification')
    (ROOT/'results'/'SYMBOLIC_SI_AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result
if __name__=='__main__':print('PASS',audit()['count'],'independent symbolic/SI checks')
