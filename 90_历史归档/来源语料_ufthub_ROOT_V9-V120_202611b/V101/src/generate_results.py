"""Rebuild V101 THEORY data and its original analytic/numeric cross-check plots."""
import csv,json,math,sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.constants import e,c,m_e
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE/'src'))
from v101_core import radiation_bounds,magnetic_degeneracy,compute_v100


def main():
    res=HERE/'results';fig=HERE/'figures'
    res.mkdir(exist_ok=True);fig.mkdir(exist_ok=True)
    v100=compute_v100(res/'V100_ORBIT_21Q_INPUT.csv',res/'V100_RADIATION_INPUT.json')
    mag=magnetic_degeneracy()
    # Displaced orbit: tangential vacuum magnetic addition changes the vertical acceleration.
    vr=100.0
    gain=-(e/(m_e*math.sqrt(1-.1**2)))*vr*mag['Bparallel_added_T']
    mag['radial_perturbation_velocity_m_s']=vr
    mag['extra_vertical_acceleration_m_s2']=gain
    b=radiation_bounds(v100['length_m'],.1,e)
    table=[]
    for beta in np.geomspace(.01,.95,100):
        for L in [.05,.161889824039568,.5]:
            row={'beta':float(beta),'length_m':float(L)}
            row.update(radiation_bounds(L,float(beta)))
            table.append(row)
    with (res/'BETA_LENGTH_SCAN_THEORY.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=table[0].keys());w.writeheader();w.writerows(table)
    result={'model':'ROOT V101 | theory, not experimental; not full unification',
        'source':'V100 21Q closed polygon and V100 theoretical radiated energy',
        'v100_independent_geometry_and_radiation':v100,
        'magnetic_field_nonidentifiability_exact_example':mag,
        'static_field_periodic_radiation':'NO-GO for strictly periodic radiating point charge in time-independent E=-grad Phi, B, periodic Schott/bound energy; external nonconservative work required',
        'assumptions':['smooth embedded nontrivial knot for Fary-Milnor floor',
         'prescribed classical point-charge trajectory at constant speed',
         'classical Lienard far-field radiation ignoring self-field trajectory modification',
         'static-field no-go assumes globally single-valued electrostatic potential and periodic near-field energy',
         'V100 knot type has numerical polygon support only, no interval ODE certificate']}
    (res/'V101_NUMERICAL_SUMMARY_THEORY.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    # Curves: topology-dependent radiation floors.
    betas=np.geomspace(.01,.95,200)
    generic=np.array([radiation_bounds(v100['length_m'],b)['ordinary_closed_lower_J'] for b in betas])
    knot=np.array([radiation_bounds(v100['length_m'],b)['knotted_lower_J'] for b in betas])
    fig1,ax=plt.subplots(figsize=(9,5.3))
    ax.loglog(betas,generic,label='Fenchel: any smooth closed curve')
    ax.loglog(betas,knot,label='Fary-Milnor: nontrivial knot')
    ax.scatter([.1],[v100['polygon_radiation_J']],label='V100 closed polygon, model only',zorder=5)
    ax.set_xlabel('beta = v / c');ax.set_ylabel('Emitted energy per loop (J)')
    ax.set_title('ROOT V101 | Geometric lower bounds at L=0.16188 m')
    ax.grid(alpha=.3);ax.legend();fig1.tight_layout()
    fig1.savefig(fig/'01_RADIATION_TOPOLOGY_BOUNDS_THEORY.png',dpi=145);plt.close(fig1)
    # Summary in a single logarithmic comparison.
    labels=['Any closed curve\nlower bound','Knotted curve\nlower bound',
            'V100 measured K\nCauchy bound','V100 polygon\ncomputed emission','V100 historical\nLiénard estimate']
    values=[v100['ordinary_closed_lower_J'],v100['knotted_lower_J'],
            v100['known_total_curvature_lower_J'],v100['polygon_radiation_J'],
            v100['historical_V100_radiation_J']]
    fig2,ax=plt.subplots(figsize=(10,5.3))
    ax.bar(np.arange(len(values)),values)
    ax.set_xticks(np.arange(len(values)),labels);ax.tick_params(axis='x',labelsize=8)
    ax.set_ylabel('Energy per loop (J)');ax.set_title('V100 orbit audit | Numerical estimates, not experiment')
    ax.set_ylim(0,max(values)*1.13);fig2.tight_layout()
    fig2.savefig(fig/'02_V100_INDEPENDENT_CURVATURE_RADIATION_AUDIT.png',dpi=145);plt.close(fig2)
    # Parallel B degeneracy: identical reference orbit but distinct perturbation response.
    cs=np.linspace(-3e-4,3e-4,121)
    resp=-(e/(m_e*math.sqrt(1-.1**2)))*vr*(cs/.005)
    fig3,ax=plt.subplots(figsize=(9,5.0))
    ax.plot(cs/.005,resp/1e14)
    ax.axhline(0,linestyle='--',alpha=.5)
    ax.set_xlabel('Additional tangent B field at the orbit (T)')
    ax.set_ylabel('Extra vertical acceleration for vr=100m/s (1e14 m/s²)')
    ax.set_title('Same reference orbit; different stability response')
    ax.grid(alpha=.3);fig3.tight_layout()
    fig3.savefig(fig/'03_MAXWELL_FIELD_NONIDENTIFIABILITY.png',dpi=145);plt.close(fig3)
    print(json.dumps({'PASS':'V101 data and figures generated',
          'v100_polygon_radiation_J':v100['polygon_radiation_J'],
          'historical_v100_J':v100['historical_V100_radiation_J'],
          'ratio_to_Cauchy_floor':v100['radiation_over_curvature_floor'],
          'relative_error_in_radiation':v100['independent_vs_historical_relative_error'],
          'topology_floor_J':v100['knotted_lower_J'],
          'required_pump_V':v100['required_energy_per_charge_V'],
          'extra_axial_accel_m_s2':gain},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
