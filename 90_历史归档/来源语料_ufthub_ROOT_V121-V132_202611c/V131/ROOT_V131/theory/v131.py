"""ROOT V131: one-loop step-threshold inverse problems.

Research and falsification tooling, NOT a validated GUT or quantum gravity model.
Units GeV; SU(5)-normalized U(1); illustrative M_Z MS-bar-like inputs.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import log, exp, pi
from typing import Iterable

MZ = 91.1876
A_EM_INV=127.955
SIN2=0.23122
ALPHA_S=0.1180
B_SM=(41/10,-19/6,-7.)
TRIPLET=(0.,4/3,0.) # one Majorana/Weyl (1,3,0)
OCTET=(0.,0.,2.)    # one Majorana/Weyl (8,1,0)


def a_at_mz(a_em_inv=A_EM_INV,sin2=SIN2,alpha_s=ALPHA_S):
    if not (a_em_inv>0 and 0<sin2<1 and alpha_s>0): raise ValueError('bad low-energy inputs')
    return ((3/5)*(1-sin2)*a_em_inv, sin2*a_em_inv, 1/alpha_s)


def differences(v): return (v[0]-v[1], v[0]-v[2])


def b_threshold(group):
    if group=='triplet': return TRIPLET
    if group=='octet': return OCTET
    raise ValueError('unknown representation')


def inv_couplings(mu, masses=(), a0=None):
    """Piecewise one-loop evolution. masses iterable of (mass, delta b tuple)."""
    if mu<=0: raise ValueError('energy scale must be positive')
    a0=a_at_mz() if a0 is None else tuple(a0)
    if len(a0)!=3: raise ValueError('three low-energy couplings required')
    t=log(mu/MZ)
    result=[a0[i]-B_SM[i]*t/(2*pi) for i in range(3)]
    for mass,db in masses:
        if mass < MZ or len(db)!=3: raise ValueError('threshold below input or malformed')
        if mu>=mass:
            s=log(mu/mass)
            for i in range(3): result[i]-=db[i]*s/(2*pi)
    return tuple(result)


def unification_det_at_mz(a0=None,b=B_SM):
    a=a_at_mz() if a0 is None else a0
    return (a[0]-a[1])*(b[1]-b[2])-(a[1]-a[2])*(b[0]-b[1])


def crossing_t(i,j,a0=None,b=B_SM):
    a=a_at_mz() if a0 is None else a0
    if i==j or b[i]==b[j]: raise ValueError('degenerate slopes')
    return 2*pi*(a[i]-a[j])/(b[i]-b[j])


def one_triplet_solution(a0=None):
    a=a_at_mz() if a0 is None else a0
    t=crossing_t(0,2,a)
    mu=MZ*exp(t)
    a_running=inv_couplings(mu,a0=a)
    # At MU a2_baseline must be lowered to a1 baseline by new triplet
    s=(a_running[1]-a_running[0])*2*pi/TRIPLET[1]
    mass=mu*exp(-s)
    if not 0<=s<=t: raise ValueError('no physical triplet threshold')
    au=inv_couplings(mu,[(mass,TRIPLET)],a0=a)
    return {'MU_GeV':mu,'Mtriplet_GeV':mass,'alphaU_inverse':sum(au)/3,
            'alphaU':1/(sum(au)/3),'t':t,'s_triplet':s,
            'residual_max_inverse':max(au)-min(au)}


def triplet_octet_at_scale(MU,a0=None):
    a=a_at_mz() if a0 is None else a0
    if MU<=MZ: raise ValueError('MU must be above MZ')
    t=log(MU/MZ)
    # exact two differences: threshold triplet affects 1-2 only;
    # octet affects 1-3 only.
    sT=((B_SM[0]-B_SM[1])*t-2*pi*(a[0]-a[1]))/TRIPLET[1]
    sO=((B_SM[0]-B_SM[2])*t-2*pi*(a[0]-a[2]))/OCTET[2]
    MT=MU*exp(-sT);MO=MU*exp(-sO)
    valid=0<=sT<=t and 0<=sO<=t
    vals=inv_couplings(MU,[(MT,TRIPLET),(MO,OCTET)],a0=a) if valid else None
    return {'MU_GeV':MU,'Mtriplet_GeV':MT,'Moctet_GeV':MO,
            't':t,'s_triplet':sT,'s_octet':sO,
            'physical_thresholds':valid,
            'alphaU_inverse':sum(vals)/3 if valid else None,
            'residual_max_inverse':(max(vals)-min(vals)) if valid else None}


def triplet_octet_unification_range(a0=None):
    a=a_at_mz() if a0 is None else a0
    # s_T>=0 needs t>=t12; s_O>=0 needs t>=t13
    lower=max(crossing_t(0,1,a),crossing_t(0,2,a),0)
    # s_T<=t, s_O<=t: masses >=MZ
    b12=B_SM[0]-B_SM[1]
    b13=B_SM[0]-B_SM[2]
    upper=min(2*pi*(a[0]-a[1])/(b12-TRIPLET[1]),
              2*pi*(a[0]-a[2])/(b13-OCTET[2]))
    return {'lower_GeV':MZ*exp(lower),'upper_GeV':MZ*exp(upper),
            'lower_t':lower,'upper_t':upper,'nonempty':upper>=lower}


def beta_weyl_majorana(dynkin_index): return 2/3*dynkin_index


def complete_multiplet_differences(delta):
    """True iff differences vanish. Degenerate complete GUT multiplet has equal delta b_i."""
    if len(delta)!=3: raise ValueError('triplet beta vector expected')
    return abs(delta[0]-delta[1])<1e-13 and abs(delta[1]-delta[2])<1e-13


def proton_decay_relative(MX,MX_ref=1e16,alpha=0.025,alpha_ref=0.04):
    """Dimension-six scaling only, requires same flavor/hadronic factors and matching."""
    if min(MX,MX_ref,alpha,alpha_ref)<=0: raise ValueError('positive inputs required')
    return (MX/MX_ref)**4*(alpha_ref/alpha)**2


def seesaw_yukawa(m_triplet_gev,m_nu_ev=0.05,v_gev=246.0):
    """Toy mnu = y^2 v^2/(2M); ignores matrices/group-normalization differences."""
    from math import sqrt
    if min(m_triplet_gev,m_nu_ev,v_gev)<=0: raise ValueError('positive inputs required')
    return sqrt(2*m_triplet_gev*m_nu_ev*1e-9)/v_gev


def main_result():
    import datetime
    single=one_triplet_solution()
    ran=triplet_octet_unification_range()
    mu_list=[2.5e14,5e14,1e15,1.5e15,2e15,2.5e15,3e15,5e15,1e16]
    scan=[triplet_octet_at_scale(mu) for mu in mu_list]
    single['neutrino_yukawa_0p05eV']=seesaw_yukawa(single['Mtriplet_GeV'])
    single['p_decay_relative_ref_1e16']=proton_decay_relative(single['MU_GeV'],alpha=single['alphaU'])
    return {'inputs':{'MZ_GeV':MZ,'alpha_em_inv_MZ':A_EM_INV,'sin2_MSbar_MZ':SIN2,'alpha_s_MZ':ALPHA_S},
            'SM_U_determinant':unification_det_at_mz(),
            'single_triplet':single,'triplet_octet_allowed':ran,
            'triplet_octet_scan':scan,'assumptions':['one-loop only','step thresholds','illustrative uncorrelated central inputs',
            'one Weyl triplet and/or octet','no two-loop matching','not a complete GUT']}

if __name__=='__main__':
    import json
    print(json.dumps(main_result(),indent=2,ensure_ascii=False))
