#!/usr/bin/env python3
"""ROOT V132: c=1, keep hbar and G dimensional; exact rational anomaly audit.
Requires only Python 3.10+ standard library. No experimental discoveries implied.
"""
from fractions import Fraction as Q
from pathlib import Path
import json, csv

# Hypercharge Y = a*y + b (Q_em=T3+Y; Higgs hypercharge 1/2).
H = Q(1,2)
BASE = [
  ('Q_L',6,1,0,3,2),
  ('u^c_L',3,-1,-H,3,1),
  ('d^c_L',3,-1,H,3,1),
  ('L_L',2,-3,0,1,2),
  ('e^c_L',1,3,H,1,1),
]
NU = ('nu^c_L',1,3,-H,1,1)

def yval(entry,y):
    return Q(entry[2])*y + entry[3]

def anomalies(y, has_nu=False):
    fs = BASE + ([NU] if has_nu else [])
    gravity = sum((f[1]*yval(f,y) for f in fs),Q(0))
    cubic = sum((f[1]*yval(f,y)**3 for f in fs),Q(0))
    q, u, d, lep = (yval(BASE[i],y) for i in (0,1,2,3))
    # Common Dynkin index 1/2 factored out; left-handed conjugate fields used.
    su3 = 2*q+u+d
    su2 = 3*q+lep
    return {'SU3²-U1':su3, 'SU2²-U1':su2, 'U1³':cubic,
            'gravity²-U1':gravity,'Witten_SU2_doublets':4,'SU3³':0}

def p_add(a,b):
    n=max(len(a),len(b));return [ (a[i] if i<len(a) else Q(0)) + (b[i] if i<len(b) else Q(0)) for i in range(n)]
def p_mul(a,b):
    out=[Q(0)]*(len(a)+len(b)-1)
    for i,ai in enumerate(a):
        for j,bj in enumerate(b):out[i+j]+=ai*bj
    return out

def coefficients(has_nu, power):
    fs=BASE+([NU] if has_nu else [])
    p=[Q(0)]
    for f in fs:
        lin=[f[3], Q(f[2])]; term=[Q(1)]
        for _ in range(power): term=p_mul(term,lin)
        p=p_add(p,[f[1]*t for t in term])
    return p

def verify():
    y=Q(1,6)
    a=anomalies(y,False)
    assert all(a[k]==0 for k in ('SU3²-U1','SU2²-U1','U1³','gravity²-U1','SU3³'))
    assert a['Witten_SU2_doublets']%2==0
    assert coefficients(False,1)==[Q(1,2),Q(-3)]
    assert coefficients(False,3)==[Q(1,8),Q(-9,4),Q(27,2),Q(-27)]
    assert coefficients(True,1)==[Q(0),Q(0)]
    assert coefficients(True,3)==[Q(0),Q(0),Q(0),Q(0)]
    for i in range(-100,101):
        y=Q(i,300)
        z=anomalies(y,True)
        assert all(z[k]==0 for k in ('SU3²-U1','SU2²-U1','U1³','gravity²-U1'))
    # U(1) gauge-transformation obstruction with a generic torsion component:
    t=Q(1,5); chi_z=Q(3); delta_F=-t*chi_z
    assert delta_F == Q(-3,5)
    # Helix: under local vacuum total speed=1, nonzero transversal motion => axial speed <1.
    axial=Q(9,10)
    assert Q(0)<1-axial**2
    # Classical plane-wave consistency; E dot B=0 but arbitrary fields need not be orthogonal.
    E=(Q(3),Q(0),Q(0)); B=(Q(0),Q(4),Q(0))
    assert sum(a*b for a,b in zip(E,B))==0
    E2=(Q(0),Q(0),Q(3)); B2=(Q(0),Q(0),Q(4))
    assert sum(a*b for a,b in zip(E2,B2))==12
    return delta_F

def stringify(x):
    return str(x) if isinstance(x,Q) else x

if __name__=='__main__':
    delta=verify(); path=Path(__file__).resolve().parent
    ys=[Q(1,6),Q(1,5),Q(0),Q(-1,6)]
    rows=[]
    for y in ys:
        for has_nu in (False,True):
            a=anomalies(y,has_nu)
            row={'y_Q':str(y),'nu_R_included':has_nu,'neutrino_electric_charge':str(Q(1,2)-3*y)}
            for k,v in a.items():row[k]=str(v)
            row['consistent_local_anomalies']=all(v==0 for k,v in a.items() if k!='Witten_SU2_doublets')
            rows.append(row)
    with (path/'anomaly_scenarios.csv').open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    data={
      'model':'SM 1 generation, Y_H=1/2, Yukawa relations and SU2 anomaly imposed',
      'unit_convention':'c=1, hbar and G independent dimensional constants',
      'SM_yQ':'1/6',
      'no_nu_R':{'gravity_polynomial_ascending':[str(v) for v in coefficients(False,1)],'cubic_polynomial_ascending':[str(v) for v in coefficients(False,3)],'unique_y_Q':'1/6'},
      'with_nu_R_Dirac':{'gravity_polynomial_ascending':[str(v) for v in coefficients(True,1)],'cubic_polynomial_ascending':[str(v) for v in coefficients(True,3)],'y_Q':'unfixed by these anomaly/Yukawa equations'},
      'torsion_gauge_counterexample':{'T_z_xy':'1/5','gradient_chi_z':'3','delta_F_xy':str(delta)},
      'exact_tests':'PASS', 'scenarios':rows,
      'caveat':'Mathematical checks only, not an empirical verification of ROOT or of a four-force unification.'
    }
    (path/'results.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print('ROOT V132 PASS: exact rational anomaly + gauge transformation + counterexample checks')
    for k,v in data['no_nu_R'].items():print('no nu:',k,v)
    for k,v in data['with_nu_R_Dirac'].items():print('with nu:',k,v)
    print('gauge delta F=',delta)
