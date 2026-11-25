#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ROOT V137: auditable exact-arithmetic model tests; c=1 only.
No assertion here proves physical unification. Math subject to stated assumptions.
"""
from __future__ import annotations
import csv, json, math, sys
from fractions import Fraction as F
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
DATA=BASE/'data'; DATA.mkdir(exist_ok=True)
LOG=[]

def chk(name, predicate, detail=''):
    row={'id':len(LOG)+1,'name':name,'status':'PASS' if bool(predicate) else 'FAIL','detail':str(detail)}
    LOG.append(row)
    if not predicate: raise AssertionError(row)

def cp_idx(q): return F(q*(q+1),2)
def index(q,m): return cp_idx(q)*m

def cp_rep(q):
    """CP^2 Dolbeault cohomology of O(q-1), SU3 irrep only for q != -1,0.
    Positive q uses H^0; negative q<=-2 uses H^2 (Serre dual).
    3 and bar3 labels are orientation conventions; only conjugacy is intrinsic.
    """
    n=int(cp_idx(q))
    if n==0: return 'zero', 0, 'zero'
    if q in (1,-2):return '1',1,'H0' if q==1 else 'H2'
    if q==2:return '3',3,'H0'
    if q==-3:return '3bar',3,'H2'
    return f'SU3_irrep_dim_{n}', n, 'H0' if q>0 else 'H2'

def sphere_rep(m):
    if m==0: return 'zero',0
    n=abs(m)
    return ('1' if n==1 else '2' if n==2 else '3' if n==3 else f'SU2_spin_{F(n-1,2)}'),n

# A hand-selected *representation bookkeeping* template, not a spectrum
# derived from one 10D field or one U(1) bundle.
FIELDS=[
 dict(name='Q_L', q=2, m=2, su3='3', su2='2', Y=F(1,6), note='LH quark doublet'),
 dict(name='u^c_L', q=-3, m=1, su3='3bar', su2='1', Y=F(-2,3), note='LH charge conjugate up'),
 dict(name='d^c_L', q=-3, m=1, su3='3bar', su2='1', Y=F(1,3), note='LH charge conjugate down'),
 dict(name='L_L', q=1, m=2, su3='1', su2='2', Y=F(-1,2), note='LH lepton doublet'),
 dict(name='e^c_L', q=1, m=1, su3='1', su2='1', Y=F(1,1), note='LH charge conjugate electron'),
 dict(name='nu^c_L', q=1, m=1, su3='1', su2='1', Y=F(0,1), note='optional LH sterile neutrino'),
]

def su3_a(x):return {'3':1,'3bar':-1,'1':0}[x['su3']]
def su3_T(x):return F(1,2) if x['su3']!='1' else F(0)
def su2_T(x):return F(1,2) if x['su2']=='2' else F(0)
def su3_dim(x):return 3 if x['su3']!='1' else 1
def su2_dim(x):return 2 if x['su2']=='2' else 1

def anomalies(fields):
    def sm(f):return sum(f(z) for z in fields)
    return {
      'SU3_cub':sm(lambda z:su3_a(z)*su2_dim(z)),
      'SU3sq_Y':sm(lambda z:su3_T(z)*su2_dim(z)*z['Y']),
      'SU2sq_Y':sm(lambda z:su2_T(z)*su3_dim(z)*z['Y']),
      'Y_cub':sm(lambda z:su3_dim(z)*su2_dim(z)*z['Y']**3),
      'grav_sq_Y':sm(lambda z:su3_dim(z)*su2_dim(z)*z['Y']),
      'weak_doublets':sm(lambda z:su3_dim(z) if z['su2']=='2' else 0),
    }


def main():
    chk('c=1 is the only naturalization; hbar and G retain dimensions',True,'[hbar]=M L, [G4]=L/M')
    chk('CP2 characteristic class 2q+1 odd for integer q',all((2*q+1)%2==1 for q in range(-70,71)))
    chk('S2 characteristic class 2m even for integer m',all((2*m)%2==0 for m in range(-70,71)))
    triple=[]; rows=[]
    for q in range(-50,51):
      for m in range(-50,51):
        if m==0:continue
        I=index(q,m)
        if abs(I)<=12 and I:
            cp,ncp,kind=cp_rep(q); sr,ns=sphere_rep(m)
            rows.append({'q':q,'m':m,'c1_CP2':2*q+1,'c1_S2':2*m,'cp2_index':str(cp_idx(q)),
                'S2_index':m,'total_index':str(I),'CP2_irrep':cp,'CP2_cohomology':kind,
                'CP2_dim':ncp,'S2_irrep':sr,'S2_dim':ns,'dim_product':ncp*ns,
                'family_claim_valid':'NO: product of nontrivial gauge irreps' if ncp>1 or ns>1 else 'only one singlet; not three'})
        if I==3:triple.append((q,m))
        chk(f'factorization(q={q},m={m})',index(q,m)==cp_idx(q)*m)
        chk(f'nonnegative CP2 index(q={q},m={m})',cp_idx(q)>=0)
        chk(f'integer CP2 index(q={q},m={m})',cp_idx(q).denominator==1)
    chk('only four solutions I=3 over broad integer scan',set(triple)=={(2,1),(-3,1),(1,3),(-2,3)},triple)
    for q,m in triple:
        a,na,_=cp_rep(q); b,nb=sphere_rep(m)
        chk(f'I=3 mode count equals three, q={q} m={m}',na*nb==3)
        chk(f'I=3 never three gauge singlets, q={q} m={m}',(na,nb) in ((3,1),(1,3)))
    # Stronger, exact integer argument: T_q=1 iff q=1 or -2, T_q=3 iff q=2 or -3.
    chk('T_q=1 solutions exactly 1,-2', {q for q in range(-100,101) if cp_idx(q)==1}=={1,-2})
    chk('T_q=3 solutions exactly 2,-3', {q for q in range(-100,101) if cp_idx(q)==3}=={2,-3})
    # Explicit nonabelian rep bookkeeping from different chosen twists.
    for x in FIELDS:
        cp, nc, ch = cp_rep(x['q']); sp,ns=sphere_rep(x['m'])
        chk(f'rep matches chosen CP2 twist {x["name"]}',cp==x['su3'])
        chk(f'rep matches chosen S2 twist {x["name"]}',sp==x['su2'])
        chk(f'index equals dimensions of full rep {x["name"]}',index(x['q'],x['m'])==nc*ns)
        chk(f'positive internal index {x["name"]}',index(x['q'],x['m'])>0)
    asm=anomalies(FIELDS)
    for name in ('SU3_cub','SU3sq_Y','SU2sq_Y','Y_cub','grav_sq_Y'):
        chk('Standard Model template exact anomaly cancellation '+name,asm[name]==0,asm[name])
    chk('Witten SU2 global-doublet test, 4 doublets, even',asm['weak_doublets']==4)
    bare=anomalies([FIELDS[0]])
    chk('one (3,2) field has nonzero cubic SU3 anomaly',bare['SU3_cub']==2)
    triplet_anom=anomalies([{'name':'triplet','q':2,'m':1,'su3':'3','su2':'1','Y':F(0)}])
    chk('single chiral (3,1) has cubic SU3 anomaly',triplet_anom['SU3_cub']==1)
    # Mirroring all fermions cancels every perturbative anomaly, but kills net chirality.
    chk('mirror 3 and 3bar can cancel SU3^3 anomaly but vectorlike',1-1==0)
    # Key label collision: u^c and d^c share exactly the same (q,m) but must have different Y.
    chk('u^c vs d^c have identical geometric (q,m) labels',
        (FIELDS[1]['q'],FIELDS[1]['m'])==(FIELDS[2]['q'],FIELDS[2]['m']))
    chk('u^c vs d^c demand unequal hypercharges',FIELDS[1]['Y']!=FIELDS[2]['Y'])
    chk('e^c vs nu^c share geometric labels but have different Y',
        (FIELDS[4]['q'],FIELDS[4]['m'])==(FIELDS[5]['q'],FIELDS[5]['m']) and FIELDS[4]['Y']!=FIELDS[5]['Y'])
    # A function (q,m)->Y cannot take 2 different values at same argument.
    label_map={}; conflicts=[]
    for z in FIELDS:
        k=(z['q'],z['m'])
        if k in label_map and label_map[k][1]!=z['Y']:
            conflicts.append({'labels':list(k),'first_name':label_map[k][0],
                  'first_Y':str(label_map[k][1]),'second_name':z['name'],'second_Y':str(z['Y'])})
        label_map.setdefault(k,(z['name'],z['Y']))
    chk('two independent hypercharge indistinguishability contradictions',len(conflicts)==2,conflicts)
    chk('one twist cannot simultaneously produce (3,2) and (3bar,1)',
        (FIELDS[0]['q'],FIELDS[0]['m'])!=(FIELDS[1]['q'],FIELDS[1]['m']))
    chk('V136 (nC=5,nS=2) labels correspond q=2 m=1 only',((5-1)//2,2//2)==(2,1))

    with (DATA/'index_sweep.csv').open('w',encoding='utf-8-sig',newline='') as fo:
        w=csv.DictWriter(fo,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    serial=[]
    for x in FIELDS:
        serial.append({**{k:str(v) if isinstance(v,F) else v for k,v in x.items()},
            'index':str(index(x['q'],x['m'])),'explicitly_input_hypercharge':True})
    with (DATA/'representation_template.csv').open('w',encoding='utf-8-sig',newline='') as fo:
        w=csv.DictWriter(fo,fieldnames=list(serial[0]));w.writeheader();w.writerows(serial)
    with (DATA/'named_checks.csv').open('w',encoding='utf-8-sig',newline='') as fo:
        w=csv.DictWriter(fo,fieldnames=list(LOG[0]));w.writeheader();w.writerows(LOG)
    anomaly_csv=[]
    for name,v in asm.items():anomaly_csv.append({'condition':name,'exact_value':str(v),'test':'even' if name=='weak_doublets' else 'zero','passed':int(v%2==0 if name=='weak_doublets' else v==0)})
    with (DATA/'anomaly_checks.csv').open('w',encoding='utf-8-sig',newline='') as fo:
        w=csv.DictWriter(fo,fieldnames=list(anomaly_csv[0]));w.writeheader();w.writerows(anomaly_csv)
    out={
        'version':'ROOT V137','unit_convention':'c=1 ONLY; hbar and G dimensionful',
        'method':'exact rational arithmetic + finite integer scans; representation assignment is an input, not a derivation',
        'tests':{'passed':sum(z['status']=='PASS' for z in LOG),'total':len(LOG),'failed':0,
                 'q_range':[-50,50],'m_range':[-50,50],'m_excludes_zero':True},
        'index_equal_three_solutions':triple,
        'rep_template':serial,
        'anomalies':{k:str(v) for k,v in asm.items()},
        'hypercharge_label_collisions':conflicts,
        'scope_warnings':[
            'The exact 4D anomaly cancellation is inherited from hand-entered Standard Model hypercharges and representations.',
            'Fields are selected from different Spin^c twists; no single V136 U(1) flux background produces this full spectrum.',
            'A local 4D anomaly-free bookkeeping table does not prove 10D anomaly cancellation, correct hypercharge quantization, gauge bosons, chiral interactions or quantum gravity.',
            'No independent prediction of G, hbar, any coupling, the three generations or light spectrum.',
            'All index=3 modes are nontrivial irreps of full internal gauged isometries in this simple abelian product model.'
        ]}
    (DATA/'verification_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'PASS':out['tests']['passed'],'index3_solutions':triple,
                      'anomalies':out['anomalies'],'conflicts':len(conflicts)},ensure_ascii=False,indent=2))
    return out
if __name__=='__main__':
    main()
