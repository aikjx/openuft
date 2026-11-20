"""Generate stable, labelled THEORY artifacts and full 369-row scientific-status review."""
from pathlib import Path
import json,csv,math,sys
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.v104_core import *
from src.dimensions import scan
from src.audit import triage,SCOPE_NOTE
ROOT=Path(__file__).resolve().parents[1]

def run():
    for p in ('results','figures','ledger'): (ROOT/p).mkdir(parents=True,exist_ok=True)
    counts=triage(ROOT/'ledger/LEGACY_369_ORIGINAL.csv',ROOT/'ledger/ALL_369_AUDITED.csv')
    with open(ROOT/'ledger/EVIDENCE_STATUS_COUNTS.json','w',encoding='utf-8') as f:
        json.dump({'review_kind':SCOPE_NOTE,'total':369,'classification_counts':dict(counts)},f,indent=2,ensure_ascii=False)
    v,E,B,y=dimensionless_field_example()
    d=lorentz_design(v)
    fit=reconstruct_fields(v,y)
    angles=np.array([.1,.2,.5,1,2,5,10,15,30,45,60,90])
    rows=[]
    for theta in angles:
        th=math.radians(theta)
        vv=np.array([[0,0,.2],[.2,0,.2],[.2*math.cos(th),.2*math.sin(th),.2]])
        s=np.linalg.svd(lorentz_design(vv),compute_uv=False)
        rows.append([theta,s[0]/s[-1],s[-1]])
    with open(ROOT/'results/VELOCITY_GEOMETRY_CONDITION_THEORY.csv','w',newline='') as f:
        wr=csv.writer(f);wr.writerow(['opening_angle_deg','condition_number','sigma_min']);wr.writerows(rows)
    fig,ax=plt.subplots(figsize=(8.4,4.5)); ax.semilogy(angles,[x[1] for x in rows],marker='o')
    ax.set(xlabel='Angle between two probe-velocity differences (degrees)', ylabel='Condition number',title='EM field inversion: probe geometry vs conditioning (THEORY)')
    ax.grid(True,which='both',alpha=.3);fig.tight_layout();fig.savefig(ROOT/'figures/01_INVERSE_CONDITION_THEORY.png',dpi=155);plt.close(fig)
    k=np.arange(4,13)
    curve=[wavy_planar_total_curvature(int(ki),.2)['total_curvature'] for ki in k]
    fig,ax=plt.subplots(figsize=(8.4,4.5));ax.plot(k,np.array(curve)/math.pi,'o-',label='Planar unknots with oscillating radius')
    ax.axhline(4,ls='--',label='4π threshold')
    ax.set(xlabel='Radial wave number k',ylabel='Total curvature / π',title='Large total curvature does NOT prove a knot (THEORY)')
    ax.legend();ax.grid(True,alpha=.3);fig.tight_layout();fig.savefig(ROOT/'figures/02_PLANAR_UNKNOT_COUNTEREXAMPLE_THEORY.png',dpi=155);plt.close(fig)
    with open(ROOT/'results/DIMENSION_AUDIT.json','w',encoding='utf-8') as f: json.dump(scan(),f,indent=2,ensure_ascii=False)
    pts=np.loadtxt(ROOT/'data/V100_ORBIT_21Q_INPUT_THEORY.csv',delimiter=',',skiprows=1)
    # Use original path approximation from 1201 sample points; does not certify a continuous knot.
    lengths=np.linalg.norm(np.roll(pts,-1,axis=0)-pts,axis=1)
    L=float(lengths.sum())
    b=bound_radiation_nontrivial_knot(ELEM_CHARGE,.1*C,L)
    boost=boost_circle_axis(.01,.6*C,.4*C)
    results={'notice':'ALL NUMBERS ARE MODEL-ONLY THEORETICAL, NOT EXPERIMENTAL.',
      'source_historical_369':dict(counts),'accepted_new_theorems':[
       'Pointwise Lorentz inverse has nullity 3 from one probe',
       'Two distinct velocities have rank 5, three non-collinear velocity differences rank 6',
       'Planar unknot can have total curvature >4pi',
       'Curvature of spatial path differs from spacetime Riemann curvature',
       'Lorentz force longitudinal and normal Frenet components are different'],
      'inverse_example':{'betas':v.tolist(),'true_E_Vm':E.tolist(),'true_B_T':B.tolist(),
       'recovered_E_Vm':fit['E_V_per_m'].tolist(),'recovered_B_T':fit['B_T'].tolist(),
       'matrix_rank':int(np.linalg.matrix_rank(d)),'condition_number':fit['condition_number'],
       'residual_Vm':fit['residual_norm']},
      'simple_unknot_high_curvature':wavy_planar_total_curvature(5,.2),
      'historical_V100_sampled_polygon_length_m':L,
      'conditional_radiation_bound_if_true_smooth_knot':b,
      'boost_demo':boost,
      'dimension_check':{'total':len(scan()),'pass':sum(x['passes'] for x in scan()),'fail':sum(not x['passes'] for x in scan())},
      'physical_unification_solved':False,
      'exact_V100_continuous_periodic_orbit_certified':False,
      'knot_topology_certified_from_finite_samples':False}
    with open(ROOT/'results/ROOT_V104_THEORY_SUMMARY.json','w',encoding='utf-8') as f:json.dump(results,f,indent=2,ensure_ascii=False)
    print(json.dumps({'counts':dict(counts),'inverse_rank':results['inverse_example']['matrix_rank'], 'sampled_path_length_m':L, 'dimension_check':results['dimension_check']},ensure_ascii=False,indent=2))
    return results
if __name__=='__main__':run()
