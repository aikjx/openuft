"""ROOT V99 numerical audit. All outputs are THEORY, no experiments.

Run from project root: python src/generate_v99.py
"""
import os,sys,json,math,csv
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
from scipy.constants import c
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).resolve().parent))
from coil_model import TwoCoilField
from v98_core import five_turn_3d
from variational import prepare,reduced_finite_difference,reduced_variational
from topology import load_v98_xyz,projected_crossings,fox_determinant,lifted_polygon
ROOT=Path(__file__).resolve().parents[1]
SEED=json.loads((ROOT/'inputs/V98_SUMMARY.json').read_text())

def crossings_from_solution(row):
    sol=row['sol'].sol;T=row['tm_norm'];r0=row['r0_m']
    grid=np.linspace(0,T,6001)
    phase=np.unwrap(np.arctan2(sol(grid)[1],sol(grid)[0]))
    out=[]
    for k in range(1,5):
        kk=k*math.pi;j=np.searchsorted(phase,kk)
        def fn(t):
            angle=float(np.arctan2(sol(t)[1],sol(t)[0]))
            return angle+2*math.pi*round((kk-angle)/(2*math.pi))-kk
        t1=brentq(fn,float(grid[j-1]),float(grid[j]),xtol=1e-13)
        t2=T-t1
        u=sol(t1);v=sol(t2)
        out.append(dict(k=k,phi_rad=kk,t1_norm=float(t1),t2_norm=float(t2),
            separation_m=float(r0*np.linalg.norm(u[:3]-v[:3])),
            velocity_separation_over_v=float(np.linalg.norm(u[3:]-v[3:])),
            radius_m=float(r0*np.linalg.norm(u[:2])), z_m=float(r0*u[2])))
    return out

def generate():
    row_seed=SEED['source_quadrature_convergence']
    cases=[];final=None
    for sample in row_seed:
        order=sample['quadrature_order']
        field=TwoCoilField(order=order)
        row=five_turn_3d(field,sample['r0_m'],sample['z_amplitude_m'],
                         SEED['conditions']['initial_radial_amplitude_m'],rtol=5e-13,dense=True)
        hits=crossings_from_solution(row)
        cases.append(dict(order=order,return_position_m=row['position_return_error_m'],
            return_velocity_rel=row['velocity_return_error_relative'],
            intersections=hits))
        if order==21:final=row
    model=prepare(SEED)
    fd=[reduced_finite_difference(model,h) for h in (1e-4,3e-5,1e-5,3e-6)]
    variational=[reduced_variational(model,step_m=h,rtol=tol)
             for h,tol in [(1e-6,3e-10),(3e-7,3e-11),(1e-7,3e-12)]]
    raw=load_v98_xyz(ROOT/'inputs/V98_3D_TRAJECTORY.csv')
    topology={ 'raw_projected_crossings_xy':len(projected_crossings(raw)),
      'raw_min_height_gap_m':float(min(abs(item['height_gap_m']) for item in projected_crossings(raw))),
      'raw_knot_invariant_valid':False,'reason':'near-zero height at projected crossings: spatial self-intersections',
      'perturbed_polygon_is_NOT_physical_solution':True,
      'perturbation_amplitude_m':1.5e-7}
    lifted=lifted_polygon(raw,1.5e-7)
    topo_res={}
    for name,view in [('xy',(0,0,1)),('oblique',(.45,.22,.866)),('oblique_2',(.55,.3,.77))]:
        topo_res[name]=fox_determinant(lifted,view,tolerance=1e-10)
    topology['lifted_polygon_knot_determinant_checks']=topo_res
    summary={'classification':'MATHEMATICAL/NUMERICAL AUDIT; NOT EXPERIMENT; NOT FOUR FORCE UNIFICATION',
      'source':'ROOT V98 specified Maxwell-Lorentz test particle in 2 finite-cross-section coils',
      'conditional_theorem':'if reduced r,z even, phi odd, and 5-turn exact periodicity, four distinct-time spatial collision pairs at phi=k*pi for k=1..4',
      'original_v98_trajectory_is_embedded_knot':False,
      'intersection_crosscheck':cases,
      'reduced_map_finite_difference':fd,'reduced_map_variational':variational,
      'topology':topology,
      'open':['No computer-assisted interval existence proof','No certified full nonlinear stability',
            'No knot invariant of the unperturbed self-intersecting orbit',
            'No radiation-reaction or actual-source engineering model',
            'No GR-SM unification or independent prediction of G']}
    (ROOT/'results/V99_NUMERICAL_AUDIT_THEORY.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    with open(ROOT/'results/FOUR_SPATIAL_SELF_INTERSECTIONS.csv','w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=['source_order','k','phi_rad','t1_norm','t2_norm','separation_m','velocity_separation_over_v','radius_m','z_m']);writer.writeheader()
        for case in cases:
            for hit in case['intersections']:writer.writerow({'source_order':case['order'],**hit})
    with open(ROOT/'results/REDUCED_MONODROMY_SENSITIVITY.csv','w',newline='',encoding='utf-8-sig') as f:
        writer=csv.writer(f);writer.writerow(['method','step','trace','det','matrix_00','matrix_01','matrix_10','matrix_11'])
        for r in fd: writer.writerow(['finite_difference',r['step'],r['trace'],r['det'],*sum(r['matrix'],[])])
        for r in variational: writer.writerow(['variational_5point',r['gradient_step_m'],r['trace'],r['det'],*sum(r['matrix'],[])])
    fig=plt.figure(figsize=(10,6));ax=fig.add_subplot(111,projection='3d')
    xyz=raw*1e3
    ax.plot(xyz[:,0],xyz[:,1],xyz[:,2],lw=.9,label='V98 periodic numerical path')
    crosses=cases[-1]['intersections']
    ax.scatter([d['radius_m']*math.cos(d['phi_rad'])*1e3 for d in crosses],
            [d['radius_m']*math.sin(d['phi_rad'])*1e3 for d in crosses],
            [d['z_m']*1e3 for d in crosses],marker='x',s=90,label='four spatial double-points')
    ax.set_xlabel('x (mm)');ax.set_ylabel('y (mm)');ax.set_zlabel('z (mm)')
    ax.set_title('V99: numerical 3D orbit with four spatial double-points')
    ax.legend(loc='upper left');fig.tight_layout();fig.savefig(ROOT/'figures/01_3D_SELF_INTERSECTIONS_THEORY.png',dpi=180);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(11,4.4))
    axes[0].plot(xyz[:,0],xyz[:,1],lw=.9)
    axes[0].scatter([h['radius_m']*math.cos(h['phi_rad'])*1e3 for h in crosses],
        [h['radius_m']*math.sin(h['phi_rad'])*1e3 for h in crosses],s=65,marker='x')
    axes[0].set_aspect('equal');axes[0].set_xlabel('x (mm)');axes[0].set_ylabel('y (mm)');axes[0].set_title('XY projection and double-points')
    hs=[z['gradient_step_m']*1e6 for z in variational]
    axes[1].plot(hs,[z['trace']-2 for z in variational],marker='o',label='trace - 2')
    axes[1].plot(hs,[z['det']-1 for z in variational],marker='s',label='determinant - 1')
    axes[1].axhline(0,lw=.5);axes[1].set_xlabel('field-gradient finite step (um)');axes[1].set_ylabel('deviation')
    axes[1].set_title('Near-parabolic reduced return map');axes[1].legend();fig.tight_layout()
    fig.savefig(ROOT/'figures/02_RETURN_MAP_SENSITIVITY_THEORY.png',dpi=180);plt.close(fig)
    return summary

if __name__=='__main__':
    d=generate();print('V99 generated',len(d['intersection_crosscheck']),'coil orders',len(d['reduced_map_variational']),'variational runs')
