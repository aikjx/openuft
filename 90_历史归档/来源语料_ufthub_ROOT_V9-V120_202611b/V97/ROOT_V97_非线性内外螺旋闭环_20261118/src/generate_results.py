"""All V97 outputs are THEORY (no experimental measurements)."""
from pathlib import Path
from math import pi
import csv,json,sys,math,hashlib,time
import numpy as np
from scipy.constants import c,e,m_e
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import brentq
from v97_core import (TwoCoilField, circular_reference, trajectory,
    primitive_pythagorean_resonances,tune_radius, five_turn_fixed_time,
    shoot_planar_resonance,independent_planar_apsidal_angle,
    canonical_angular_momentum_relative_error, circular_radiation_per_turn)
ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/'results';PLOT=ROOT/'plots';RES.mkdir(exist_ok=True);PLOT.mkdir(exist_ok=True)

def write_csv(path,records):
    with path.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=records[0].keys());w.writeheader();w.writerows(records)

def main():
    start=time.time()
    model=TwoCoilField(order=21)
    linear_radius=tune_radius(model)
    linear_ref=circular_reference(r0=linear_radius,field=model)
    triples=primitive_pythagorean_resonances(100)
    write_csv(RES/'PYTHAGOREAN_TUNE_CATALOG_THEORY.csv',triples)
    # For each radius, current is re-calibrated to make that r0 a reference circle.
    # This is parameter continuation, not a single fixed field across all radii.
    offsets=[]
    for microns in [2,5,10,20,30,40,80]:
        row=five_turn_fixed_time(model,linear_radius,dx=microns*1e-6,dz=microns*1e-6)
        offsets.append({k:v for k,v in row.items() if k!='end_normalized'})
    write_csv(RES/'FIVE_TURN_NONLINEAR_DETUNING_THEORY.csv',offsets)
    # Invariant z=vz=0 plane; adjust calibrated orbit radius for 4:5 resonance.
    shot=shoot_planar_resonance(model,amplitude=30e-6,linear_root=linear_radius)
    independent=independent_planar_apsidal_angle(model,shot['r0_m'],amplitude=30e-6,quad_n=24)
    canonical_error=canonical_angular_momentum_relative_error(model,shot['r0_m'],shot['orbit'])
    # solve at other amplitudes, verifying continuity and nonlinear radius shift
    tuning=[]
    for microns in [5,10,20,30,40,60]:
        result=shoot_planar_resonance(model,amplitude=microns*1e-6,linear_root=linear_radius)
        tuning.append({'amplitude_um':microns,'linear_radius_mm':linear_radius*1e3,
            'nonlinear_radius_mm':result['r0_m']*1e3,
            'radius_shift_nm':result['nonlinear_shift_m']*1e9,
            'shoot_phase_error_rad':result['phase_error_rad'],
            'section_return_position_m':result['return_position_error_m'],
            'relative_velocity_return':result['return_velocity_relative']})
    write_csv(RES/'NONLINEAR_PLANAR_PERIODIC_FAMILY_THEORY.csv',tuning)
    # independent convergence: source quadrature orders 13,17,21,29
    convergence=[]
    for order in [13,17,21,29]:
        f=TwoCoilField(order=order)
        lr=tune_radius(f)
        s=shoot_planar_resonance(f,amplitude=30e-6,linear_root=lr)
        convergence.append({'source_order':order,'linear_radius_m':lr,
                            'nonlinear_closed_radius_m':s['r0_m'],
                            'phase_residual_rad':s['phase_error_rad'],
                            'section_position_error_m':s['return_position_error_m']})
    write_csv(RES/'SOURCE_QUADRATURE_PERIODIC_CONVERGENCE_THEORY.csv',convergence)
    # trajectory sample for interactive browser visualization, from first max to 4th max
    t_end=shot['time_normalized']
    dense=shot['orbit'].sol
    times=np.linspace(0,t_end,1200)
    states=dense(times)
    sampled=[]
    for tm,y in zip(times,states.T):
        sampled.append({'time_ns':tm*shot['r0_m']/(.1*c)*1e9,
                        'x_mm':float(y[0]*shot['r0_m']*1e3),
                        'y_mm':float(y[1]*shot['r0_m']*1e3),
                        'radius_mm':float(np.hypot(y[0],y[1])*shot['r0_m']*1e3),
                        'z_mm':float(y[2]*shot['r0_m']*1e3)})
    write_csv(RES/'NONCIRCULAR_PLANAR_ORBIT_THEORY.csv',sampled)
    radiation=circular_radiation_per_turn(.1,shot['r0_m'])
    # produce stable JSON without ndarray/solver
    serialized={k:v for k,v in shot.items() if k not in ('orbit','initial_state','final_state')}
    report={
      'provenance':'THEORY_ONLY_NOT_OBSERVATIONS',
      'physical_theory':'Established Maxwell-Lorentz, smooth finite-section current, external ideal power supply',
      'baseline_assumptions':{'beta':.1,'wire_center_radius_m':.01,
         'coil_half_spacing_m':.008,'coil_cross_section_radius_m':.001,
         'field_quadrature_order':21,'electron_rest_mass_kg':m_e,'charge_C':-e},
      'classification':{'number_of_primitive_resonances_N_le_100':len(triples),
        'first_primitive_resonance':triples[0],
        'conditional_theorem':'Both tune ratios rational <=> positive integer Pythagorean triple (under ideal weak focusing)'},
      'linear_reference':{'r0_m':linear_radius,**linear_ref},
      'nonlinear_planar_periodic_orbit':serialized,
      'independent_reduced_action_quadrature':independent,
      'canonical_Pphi_max_dimensionless_residual':canonical_error,
      'fixed_time_detuning':offsets,
      'nonlinear_continuation':tuning,
      'field_quadrature_convergence':convergence,
      'classical_radiation_reference':radiation,
      'limits':[
          'Analytical Pythagorean classification only for small-amplitude weak focusing.',
          'Numerical shooting locates a nearly closed periodic planar orbit, not an interval proof of exact existence.',
          'Source current is recalibrated as reference radius varies; after shooting final field is held fixed.',
          'Planar noncircular orbit is NOT a three-dimensional trefoil knot.',
          'Radiation reaction is neglected, so true electron motion is not forever periodic.',
          'No origin of gravity constant G, Standard Model gauge group, or quantum gravity is derived.'
      ],'elapsed_s':time.time()-start}
    (RES/'NUMERICAL_SUMMARY_THEORY.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    # charts use original matplotlib defaults
    plt.figure(figsize=(9,5))
    plt.loglog([r['amplitude_m']*1e6 for r in offsets],
               [r['position_return_m'] for r in offsets],marker='o')
    plt.xlabel('Equal radial and vertical initial offsets (um)')
    plt.ylabel('5-turn return distance, fixed time (m)')
    plt.title('Finite-amplitude detuning at LINEAR 3:4:5 resonance (THEORY)')
    plt.grid(True,which='both',alpha=.3)
    plt.tight_layout();plt.savefig(PLOT/'01_NONLINEAR_DETUNING_THEORY.png',dpi=155);plt.close()
    plt.figure(figsize=(8,7))
    x=states[0]*shot['r0_m']*1e3;y=states[1]*shot['r0_m']*1e3
    plt.plot(x,y,lw=1.4,label='4 radial oscillations / 5 turns')
    plt.plot([x[0]],[y[0]],marker='o',label='start/end (overlap)')
    plt.gca().set_aspect('equal','box')
    plt.xlabel('x (mm)');plt.ylabel('y (mm)');plt.title('Numerically shot noncircular PLANAR periodic orbit (THEORY)')
    plt.legend();plt.grid(alpha=.25);plt.tight_layout()
    plt.savefig(PLOT/'02_NONCIRCULAR_PLANAR_PERIODIC_THEORY.png',dpi=155);plt.close()
    plt.figure(figsize=(9,5))
    plt.plot([p['amplitude_um'] for p in tuning],
             [p['radius_shift_nm'] for p in tuning],marker='o')
    plt.xlabel('Radial amplitude (um)');plt.ylabel('Required reference-radius correction (nm)')
    plt.title('Retuning the source for nonlinear PLANAR closure (THEORY)')
    plt.grid(alpha=.3);plt.tight_layout();plt.savefig(PLOT/'03_NONLINEAR_SHOOTING_SHIFT_THEORY.png',dpi=155);plt.close()
    print(json.dumps({'linear_r0_mm':linear_radius*1e3,'nonlinear_r0_mm':shot['r0_m']*1e3,
        'nonlinear_shift_nm':shot['nonlinear_shift_m']*1e9,
        'orbit_return_m':shot['return_position_error_m'],
        'canonical_Pphi_max_dimensionless_residual':canonical_error,
        'independent_quadrature_phase_error_rad':independent['four_cycle_phase_error_rad'],
        'first_triplet':triples[0],'radiation_J_turn':radiation['energy_per_turn_J'],
        'elapsed_seconds':report['elapsed_s']},indent=2,ensure_ascii=False))

if __name__=='__main__':main()
