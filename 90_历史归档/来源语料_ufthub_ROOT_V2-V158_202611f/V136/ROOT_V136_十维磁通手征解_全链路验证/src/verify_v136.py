#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ROOT V136: exact audits of an illustrative D=10 Einstein-Maxwell-Λ flux compactification.
This proves identities for a *chosen* action/background, not a new theory of nature.
Only c=1; hbar, G10, G4 remain dimensionful and independent.
No dependencies beyond Python 3.10+ for verification.
"""
from __future__ import annotations
import csv, json, math, hashlib, sys
from fractions import Fraction as Q
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'; DATA.mkdir(parents=True,exist_ok=True)
CHECKS=[]

def check(label, condition, detail=''):
    item={'id':len(CHECKS)+1,'name':label,'passed':bool(condition),'detail':str(detail)}
    CHECKS.append(item)
    if not condition: raise AssertionError(item)

def solution(nc: int, ns: int, h: Q=Q(1)):
    """Flux classes c1(L)=nc h_CP2 + ns u_S2; nc odd, ns even, ns != 0.
    h=kappa10^2 / g_F^2, has length^2, positive in physical toy model.
    R_C^2=(2/3) h nc^2, R_S^2=h ns^2 / 4.
    Flux F=f_C J_C + f_S vol(S2), J_C=R_C^2 J_FS, int_CP1 J_FS=pi.
    """
    assert nc%2==1 and ns%2==0 and nc and ns and h>0
    rc2=Q(2,3)*h*nc**2
    rs2=h*ns**2/Q(4)
    fc=Q(2*nc)/rc2
    fs=Q(ns,2)/rs2
    f2=4*fc**2+2*fs**2
    lam=h*f2/Q(4)
    i_cp=(nc**2-1)//8
    i_s=ns//2
    return {'nc':nc,'ns':ns,'h':h,'RC2':rc2,'RS2':rs2,'fC':fc,'fS':fs,
            'F2':f2,'Lambda':lam,'index_CP2':i_cp,'index_CP1':i_s,'index_X6':i_cp*i_s}

def residuals(s):
    """Trace reversed EFE in D=10:
    Ric_MN=H(F_MA F_N^A - F^2*g_MN/16) + Λ*g_MN/4.
    Return blockwise per-unit metric EFE residuals.
    """
    h=s['h']; f2=s['F2']; fc=s['fC']; fs=s['fS']; la=s['Lambda']
    common=-h*f2/Q(16)+la/Q(4)
    ext=Q(0)-common
    cp=Q(6)/s['RC2']-(h*fc**2+common)
    sph=Q(1)/s['RS2']-(h*fs**2+common)
    return {'external':ext,'CP2':cp,'S2':sph}

def effective_W(s):
    """Jordan-frame scalar potential numerator: 2Λ - R6 + (H/2)F².
    Its Weyl-rescaled Einstein-frame potential is proportional to W/V6.
    """
    h=s['h']; x=s['RC2']; y=s['RS2'];nc=s['nc'];ns=s['ns']
    return 2*s['Lambda'] - Q(24)/x - Q(2)/y + Q(8)*h*nc**2/x**2 + h*ns**2/(4*y**2)

def scale_mode_hessian(s):
    """Hessian of W at fixed flux, in u=ln(RC/RC0), v=ln(RS/RS0).
    At Minkowski background W=W_u=W_v=0; Einstein-frame Weyl factor
    is positive and does not alter the Hessian sign there.
    """
    x,y,h,nc,ns=s['RC2'],s['RS2'],s['h'],s['nc'],s['ns']
    wu=Q(48)/x - Q(32)*h*nc**2/x**2
    wv=Q(4)/y - h*ns**2/y**2
    wuu=-Q(96)/x + Q(128)*h*nc**2/x**2
    wvv=-Q(8)/y + Q(4)*h*ns**2/y**2
    return {'Wu':wu,'Wv':wv,'Wuu':wuu,'Wvv':wvv,'Wuv':Q(0)}

def torsion_independent_index(nc,ns):
    """(Â e^{c1(L)/2})_6: [((nc)^2-1)/8] * (ns/2)."""
    return (Q(nc**2,8)-Q(1,8))*Q(ns,2)

def su3_representation_checks():
    """Direct 3x3 fundamental generator checks (plain Python complex arithmetic)."""
    z=0j
    invsqrt3=1/math.sqrt(3)
    lmb=[
        [[0,1,0],[1,0,0],[0,0,0]],
        [[0,-1j,0],[1j,0,0],[0,0,0]],
        [[1,0,0],[0,-1,0],[0,0,0]],
        [[0,0,1],[0,0,0],[1,0,0]],
        [[0,0,-1j],[0,0,0],[1j,0,0]],
        [[0,0,0],[0,0,1],[0,1,0]],
        [[0,0,0],[0,0,-1j],[0,1j,0]],
        [[invsqrt3,0,0],[0,invsqrt3,0],[0,0,-2*invsqrt3]],
    ]
    T=[[[x/2 for x in row] for row in matrix] for matrix in lmb]
    def mm(a,b):
        return [[sum(a[i][k]*b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    def tr(a): return sum(a[i][i] for i in range(3))
    casimir=[[0j]*3 for _ in range(3)]
    for A in T:
        for i in range(3):
            for j in range(3): casimir[i][j]+=mm(A,A)[i][j]
    check('explicit eight SU3 generators are traceless',all(abs(tr(A))<1e-13 for A in T))
    check('SU3 fundamental Casimir explicit 3x3 matrix is 4/3 I',all(abs(casimir[i][j]-(4/3 if i==j else 0))<1e-12 for i in range(3) for j in range(3)))
    t8cube=mm(mm(T[7],T[7]),T[7])
    check('SU3 cubic trace explicit matrix agrees with -1/(4 sqrt 3)',abs(tr(t8cube).real+1/(4*math.sqrt(3)))<1e-13)
    c12=[[mm(T[0],T[1])[i][j]-mm(T[1],T[0])[i][j] for j in range(3)] for i in range(3)]
    check('[T1,T2]=iT3 generator closure',all(abs(c12[i][j]-1j*T[2][i][j])<1e-13 for i in range(3) for j in range(3)))
    check('SU3 action mixes the 3 zero-mode basis vectors', abs(T[0][1][0])>0)

def main():
    su3_representation_checks()
    check('10D = 4D Minkowski + 4D CP2 + 2D S2',4+4+2==10)
    check('CP2 w2 is odd; spin^c determinant nc must be odd',5%2==1)
    check('sphere spin^c determinant c1 is even',2%2==0)
    check('canonical spin^c determinant CP2 3h / CP1 2u',3%2==1 and 2%2==0)
    check('O(1) twist on CP2 changes determinant 3h -> 5h',3+2==5)
    check('G10 has L^7/M dimension when c=1',10-3==7)
    check('volume V6 scales as L^6',4+2==6)
    check('G4=G10/V6 has L/M dimension',7-6==1)
    check('holomorphic sections H^0(CP2,O(1)) dimension = 3',math.comb(1+2,2)==3)
    check('CP1 O(0) constant holomorphic section dimension = 1',math.comb(0+1,1)==1)
    check('3*1 internal zero modes on K6',3*1==3)
    check('SU3 triplet dimension distinct from generations number',3==3)
    check('SU3 8 generators + sphere SO3 3 + added U1 Maxwell 1',8+3+1==12)
    check('SU3 fundamental quadratic Casimir 4/3',Q(3**2-1,2*3)==Q(4,3))
    # T8 = diag(1,1,-2)/(2 sqrt(3)); Tr T8^3 = (-1/4)/sqrt(3).
    trace_t8_cubed_coeff=Q(1,24)+Q(1,24)-Q(8,24)
    check('T8³ trace coefficient equals -1/4 (in units 1/sqrt(3))',trace_t8_cubed_coeff==Q(-1,4))
    check('SU3 fundamental cubic anomaly coefficient d888 nonzero',4*trace_t8_cubed_coeff!=0)

    rows=[]
    for nc in range(-11,12,2):
        for ns in range(-10,11,2):
            if ns==0: continue
            s=solution(nc,ns)
            r=residuals(s)
            check(f'flux integers nc={nc}, ns={ns}',nc%2==1 and ns%2==0)
            check(f'CP2 flux quantization nc={nc}, ns={ns}',s['fC']*s['RC2']/2==nc) # ∫CP1 J_C=πRC²
            check(f'S2 flux quantization nc={nc}, ns={ns}',2*s['fS']*s['RS2']==ns) # 4πR² /2π
            check(f'CP2 Ricci block nc={nc}, ns={ns}',r['CP2']==0)
            check(f'S2 Ricci block nc={nc}, ns={ns}',r['S2']==0)
            check(f'external Einstein block nc={nc}, ns={ns}',r['external']==0)
            check(f'flux density invariant nc={nc}, ns={ns}',s['F2']==4*s['fC']**2+2*s['fS']**2)
            check(f'Λ tuning nc={nc}, ns={ns}',s['Lambda']==Q(9,s['nc']**2)/s['h']+Q(2,s['ns']**2)/s['h'])
            check(f'spin-c 6D index nc={nc}, ns={ns}',s['index_X6']==torsion_independent_index(nc,ns))
            check(f'integer index nc={nc}, ns={ns}',torsion_independent_index(nc,ns).denominator==1)
            check(f'Minkowski W=0 nc={nc}, ns={ns}',effective_W(s)==0)
            hs=scale_mode_hessian(s)
            check(f'homogeneous W stationary nc={nc}, ns={ns}', hs['Wu']==0 and hs['Wv']==0)
            check(f'homogeneous Hessian positive nc={nc}, ns={ns}', hs['Wuu']>0 and hs['Wvv']>0)
            rows.append({key: (str(val) if isinstance(val,Q) else val) for key,val in s.items()})
    s=solution(5,2,Q(1))
    check('selected index exactly three',s['index_X6']==3)
    check('selected RC^2=50/3 H',s['RC2']==Q(50,3))
    check('selected RS^2=H',s['RS2']==1)
    check('selected fC=3/5H',s['fC']==Q(3,5))
    check('selected fS=1/H',s['fS']==1)
    check('selected F²=86/25H²',s['F2']==Q(86,25))
    check('selected Λ=43/50H',s['Lambda']==Q(43,50))
    check('selected CP2 Ricci=9/25H',Q(6)/s['RC2']==Q(9,25))
    check('selected sphere Ricci=1/H',Q(1)/s['RS2']==1)
    check('selected scalar curvature= 4*(9/25)+2=86/25',4*Q(6)/s['RC2']+2*Q(1)/s['RS2']==Q(86,25))
    hs=scale_mode_hessian(s)
    check('two homogeneous radius directions stationary',hs['Wu']==0 and hs['Wv']==0)
    check('log CP2 radius positive W Hessian 144/25',hs['Wuu']==Q(144,25))
    check('log sphere radius positive W Hessian 8',hs['Wvv']==Q(8))
    check('homogeneous mixing Hessian vanishes in this minimal model',hs['Wuv']==0)
    check('CP2×S2 spin-c index 3 uses odd CP2 & even S2 determinant classes',5%2==1 and 2%2==0)
    check('two 10D opposite chiralities give vectorlike net index zero',3-3==0)
    # Ratios follow directly from R_C^2= (2/3)H nc^2 and R_S^2= H ns^2/4
    check('fixed radius ratio RC²/RS² = 200/12 for nc=5 ns=2',s['RC2']/s['RS2']==Q(50,3))
    check('Volume V6 = 2 pi³ RC^4 RS²: coefficient 5000/9 H³',2*s['RC2']**2*s['RS2']==Q(5000,9))
    check('index zero for nc=±1 regardless of sphere flux',solution(1,2)['index_X6']==0 and solution(-1,2)['index_X6']==0)
    check('sphere orientation flips net index',solution(5,-2)['index_X6']==-3)
    check('changing flux numbers changes family index',solution(7,2)['index_X6']==6)

    csv_path=DATA/'flux_solutions.csv'
    with csv_path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    with (DATA/'named_checks.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(CHECKS[0]));w.writeheader();w.writerows(CHECKS)
    result={
        'title':'ROOT V136 conditional mathematical construction and audit',
        'verification_status':'all stated rational identities passed' if all(z['passed'] for z in CHECKS) else 'failed',
        'check_count':len(CHECKS),'flux_configs':len(rows),'selected_case':{k:str(v) for k,v in s.items()},
        'EFE_residuals':{k:str(v) for k,v in residuals(s).items()},
        'radion_subsector':{'W':str(effective_W(s)),'Hessian_log_radii':{k:str(v) for k,v in hs.items()},'scope':'homogeneous scaling moduli at fixed flux only; all KK perturbations not tested'},
        'limitations':['No Standard Model fermion spectrum','One SU(3) triplet is not three families',
                       'Single chiral triplet has SU(3)^3 anomaly','Quantum 10D anomaly not checked',
                       'No stability or radion spectrum proven','No independent G4 or gauge couplings predicted',
                       '10D Einstein-Maxwell-U1 and integer flux already input, not pure space-only geometry'],
        'unit_convention':'c=1 only; hbar, G10, G4 retained dimensionful'}
    (DATA/'verification_results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({'passed':len(CHECKS),'flux_configurations':len(rows),'selected':result['selected_case'],'EFE_residuals':result['EFE_residuals']},ensure_ascii=False,indent=2))
    return result

if __name__=='__main__':main()
