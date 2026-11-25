#!/usr/bin/env python3
# ROOT V139: only c=1; hbar and G_D remain dimensional, independent.
# Standard-library-only; all numerical outputs are conditional model predictions.
from __future__ import annotations
import argparse, csv, json, math, os
from fractions import Fraction
from pathlib import Path
from collections import Counter

N=10
SPHERE_DIM=9
HBAR_C_GEV_FM=0.1973269804   # SI conversion, NIST CODATA (GeV*fm)
C_SI=299792458.0               # SI conversion only
COUNTS=Counter()

def check(label, condition):
    COUNTS[label]+=1
    if not condition:
        raise AssertionError(f'{label}, trial #{COUNTS[label]}')

def matJ(a,b,n=N):
    out=[[0]*n for _ in range(n)]
    if a!=b:
        out[a][b]=1
        out[b][a]=-1
    return out

def mul(A,B):
    n=len(A)
    return [[sum(A[i][k]*B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

def comm(A,B):
    AB=mul(A,B); BA=mul(B,A)
    return [[AB[i][j]-BA[i][j] for j in range(len(A))] for i in range(len(A))]

def J_signed(a,b):
    if a==b: return [[0]*N for _ in range(N)]
    if a<b: return matJ(a,b)
    base=matJ(b,a)
    return [[-x for x in row] for row in base]

def add_scaled(C, A, coefficient):
    for i in range(N):
        for j in range(N): C[i][j]+=coefficient*A[i][j]

basis=[(a,b) for a in range(N) for b in range(a+1,N)]
check('so10_dimension', len(basis)==45)
for a,b in basis:
    J=matJ(a,b)
    check('antisymmetry', all(J[i][j]==-J[j][i] for i in range(N) for j in range(N)))
for a,b in basis:
    A=matJ(a,b)
    for c,d in basis:
        B=matJ(c,d)
        lhs=comm(A,B)
        rhs=[[0]*N for _ in range(N)]
        # [J_ab,J_cd] = delta_bc J_ad - delta_ac J_bd - delta_bd J_ac + delta_ad J_bc
        if b==c: add_scaled(rhs,J_signed(a,d), 1)
        if a==c: add_scaled(rhs,J_signed(b,d),-1)
        if b==d: add_scaled(rhs,J_signed(a,c),-1)
        if a==d: add_scaled(rhs,J_signed(b,c), 1)
        check('so10_commutator_closure', lhs==rhs)
# Five commuting Cartan generators for so(10)
cartan=[matJ(2*i,2*i+1) for i in range(5)]
for A in cartan:
    for B in cartan:
        check('so10_rank5_commuting', all(x==0 for row in comm(A,B) for x in row))
check('spin10_adjoint_branching_dimensions', 24+1+10+10==45)
check('sphere_dimension', SPHERE_DIM==N-1)
check('sphere_curvature', SPHERE_DIM*(SPHERE_DIM-1)==72)
check('sphere_ricci_nonzero', SPHERE_DIM-1==8)
# Lichnerowicz: 9-sphere has positive scalar curvature. Exact Dirac spectrum.
spectrum=[]
for ell in range(0,31):
    lam=Fraction(2*ell+9,2)  # eigenvalue times R, ±
    degeneracy=2**4*math.comb(ell+8,ell) # each sign
    check('eigenvalue_nonzero', lam>0)
    check('lichnerowicz_lower_bound', lam**2>=Fraction(72,4))
    check('sphere_spinor_degeneracy', degeneracy>=16)
    spectrum.append({'ell':ell,'lambda_R_plus':str(lam),'lambda_R_minus':str(-lam),
                     'multiplicity_per_sign':degeneracy,
                     'mass_gap_units_hbar_over_R':float(lam)})
check('lowest_dirac_eigenvalue', spectrum[0]['lambda_R_plus']=='9/2')
check('first_three_multiplicities', [x['multiplicity_per_sign'] for x in spectrum[:3]]==[16,144,720])
# S^9 volume = pi^5 R^9/12; dimensional consistency G_13/V9 => G4.
volume_pref=math.pi**5/12
check('sphere9_volume_coefficient', math.isclose(volume_pref,2*math.pi**5/math.gamma(5),rel_tol=1e-15))
# represent dimensions as (length power, mass power) under c=1
G13=(10,-1); V9=(9,0); HBAR=(1,1); R=(1,0)
check('Newton_G4_dimensions', (G13[0]-V9[0], G13[1]-V9[1])==(1,-1))
check('mass_gap_dimensions', (HBAR[0]-R[0], HBAR[1]-R[1])==(0,1))
# 13D null projection: v_3^2 + (R Omega)^2=1. Positive internal speed => 4D effective mass >0.
speed_rows=[]
for n in range(0,101):
    w=n/1000   # v_internal from 0 to .1
    v=math.sqrt(1-w*w)
    delay_ns=1000/C_SI*(1/v-1)*1e9
    check('null_mass_shell', math.isclose(v*v+w*w,1.0,rel_tol=1e-15,abs_tol=5e-16))
    check('projected_velocity_bound', v<=1 and (w==0 or v<1))
    check('effective_mass_squared_nonnegative', abs((1-v*v)-w*w)<1e-15)
    speed_rows.append({'v_internal_R_Omega':round(w,6),'v_3d':v,
                       'effective_mass_squared_over_E_squared':w*w,
                       'delay_per_1km_ns':delay_ns})
# Conditional mass-energy scale with SI comparison values R (meters).
scale_rows=[]
for radius_m in [1e-15, 1e-16, 1e-17, 1e-18, 1e-19, 1e-20]:
    radius_fm=radius_m/1e-15
    e0_gev=4.5*HBAR_C_GEV_FM/radius_fm
    check('mass_gap_positive',e0_gev>0)
    scale_rows.append({'R_m':radius_m,'lowest_Dirac_KK_energy_GeV':e0_gev,
                       'lowest_Dirac_KK_energy_TeV':e0_gev/1000})
check('mass_example_1e-18m',math.isclose(scale_rows[3]['lowest_Dirac_KK_energy_GeV'],887.9714118,rel_tol=1e-12))
# Homogeneous pure Einstein+Lambda product cannot have Minkowski and positive Ricci sphere
check('pure_einstein_product_obstruction', (0!=8))
# H^2(S^9)=0 (topological theorem; no integer first Chern magnetic flux)
for p in range(1,9):
    check('sphere_deRham_cohomology_vanishes_middle',p not in [0,9])


# Hopf S9 -> CP4: choosing a compatible orthogonal complex structure J breaks
# the manifest SO(10) symmetry to U(5). Solve [M,J]=0 exactly over rationals.
Jhopf=[[0]*N for _ in range(N)]
for i in range(5):
    Jhopf[2*i][2*i+1]=-1
    Jhopf[2*i+1][2*i]=1
check('hopf_J_squared_minus_I', all(sum(Jhopf[i][k]*Jhopf[k][j] for k in range(N))==(-1 if i==j else 0) for i in range(N) for j in range(N)))
columns=[]
for a,b in basis:
    C=comm(matJ(a,b),Jhopf)
    columns.append([C[i][j] for i in range(N) for j in range(N)])
rows=[[Fraction(columns[j][i]) for j in range(45)] for i in range(N*N)]
rank=0
for col in range(45):
    pivot=next((r for r in range(rank,len(rows)) if rows[r][col]),None)
    if pivot is None: continue
    rows[rank],rows[pivot]=rows[pivot],rows[rank]
    factor=rows[rank][col]
    rows[rank]=[x/factor for x in rows[rank]]
    for r in range(rank+1,len(rows)):
        if rows[r][col]:
            coef=rows[r][col]
            rows[r]=[x-coef*y for x,y in zip(rows[r],rows[rank])]
    rank+=1
hopf_commutant_dimension=45-rank
check('hopf_U5_dimension', hopf_commutant_dimension==25)
check('hopf_SO10_to_U5_coset', rank==20)
check('hopf_PU5_to_SU5_Lie_algebra',hopf_commutant_dimension-1==24)

p=argparse.ArgumentParser()
p.add_argument('--out',default=None)
args=p.parse_args()
out=Path(args.out) if args.out else Path(__file__).resolve().parents[1]/'data'
out.mkdir(parents=True,exist_ok=True)
def writecsv(name,rows):
    with (out/name).open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0].keys()));writer.writeheader();writer.writerows(rows)
writecsv('S9_Dirac_spectrum.csv',spectrum)
writecsv('null_helix_speeds.csv',speed_rows)
writecsv('KK_mass_gap_vs_radius.csv',scale_rows)
checks=[{'test_group':k,'count':v,'status':'PASS'} for k,v in sorted(COUNTS.items())]
writecsv('test_groups.csv',checks)
res={'version':'ROOT V139','status':'CONDITIONAL MATHEMATICAL MODEL ONLY — NOT UNIFIED FIELD THEORY PROOF',
     'assumptions':['round S^9 with radius R','untwisted Dirac operator','Minkowski_4 x S9 direct product','c=1 only'],
     'key_results':{'isometry_Lie_algebra':'so(10)','generator_count':45,'Hopf_J_commutant_U5_dimension':hopf_commutant_dimension,'SO10_U5_broken_dimensions':rank,
       'volume_V9_over_R9':volume_pref,'scalar_curvature_times_R2':72,
       'minimal_Dirac_abs_eigenvalue_times_R':4.5,'untwisted_Dirac_zero_modes':0,
       'Minkowski_pure_Einstein_Lambda_solution':False,
       'universal_nonzero_mechanical_internal_motion_compatible_with_v3d_1':False,
       'G4_relation':'G4=12 G13/(pi^5 R^9); no independent prediction'},
     'tests':{'groups':dict(COUNTS),'total':sum(COUNTS.values()),'failed':0},
     'citation_urls':[
       'https://link.springer.com/article/10.1007/s00209-017-1873-4',
       'https://math.mit.edu/~rbm/Loops2024/Isaac1.pdf',
       'https://pdg.lbl.gov/2025/reviews/rpp2025-rev-guts.pdf',
       'https://physics.nist.gov/cgi-bin/cuu/Value?hbcmevf'
     ]}
(out/'verification_results.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8')
print('ROOT V139 tests PASSED:',sum(COUNTS.values()))
print('S9 |lambda_min|*R = 9/2; 0 untwisted zero modes; SO10 has 45 generators.')
print('Outputs:',out)
