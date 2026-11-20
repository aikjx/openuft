"""ROOT V92 reproducible THEORY calculations: no synthetic data is observational."""
import csv
import json
import math
from pathlib import Path
import numpy as np
from src.helix_physics import (
 C, HBAR, M_E, E_CHARGE, Helix, cyclotron_helix, lorentz_force_magnitude_constant_speed,
 magnetic_force, field_inferred_from_helix, check_dimensions, dimension_dict, reproduce_constants_example
)

ROOT=Path(__file__).resolve().parents[1]

def efield_straight_analytic(t,E=1e5,charge=E_CHARGE,mass=M_E):
    """Flat 1D electron acceleration by a constant electric field: p=qEt, v<c.
    Sign given by charge; uses positive q to focus on magnitude.
    """
    mom=charge*E*t
    gamma=math.hypot(1., mom/(mass*C))
    speed=mom/(gamma*mass)
    x=(mass*C*C/(charge*E))*( (mom/(mass*C))**2/(1+gamma))  # stable sqrt(1+x²)-1
    return dict(time_s=t,E_V_per_m=E,momentum_kg_m_per_s=mom,
                gamma=gamma,speed_m_s=speed,position_m=x,
                field_force_N=charge*E,spatial_curvature_inverse_m=0)


def rk4_magnetic(B, mass=M_E, charge=E_CHARGE, beta=0.8, pitch_deg=30., steps=10000):
    """Independent ODE integration of dp/dt=q(v×B), constant energy.
    Computes signed angular motion (electron charge represented by positive q here).
    State=(x,y,z,px,py,pz); B=B zhat.
    """
    angle=math.radians(pitch_deg)
    speed=beta*C; gamma=1/math.sqrt(1-beta*beta)
    omega=abs(charge)*B/(gamma*mass)
    T=2*math.pi/omega
    dt=T/steps
    y=np.array([0.,0.,0.,gamma*mass*speed*math.cos(angle),0.,gamma*mass*speed*math.sin(angle)],dtype=float)
    def deriv(y):
        p=y[3:]
        gam=math.sqrt(1+float(np.dot(p,p))/(mass*C)**2)
        v=p/(gam*mass)
        d_p=np.array([charge*v[1]*B,-charge*v[0]*B,0.0])
        return np.r_[v,d_p]
    pnorm0=float(np.linalg.norm(y[3:]))
    for _ in range(steps):
        k1=deriv(y); k2=deriv(y+dt*k1/2); k3=deriv(y+dt*k2/2); k4=deriv(y+dt*k3)
        y+=dt*(k1+2*k2+2*k3+k4)/6
    radius=speed*math.cos(angle)/omega
    # initial v along +x, positive charge B+z -> center on -y
    expected=np.array([0.,-0.,speed*math.sin(angle)*T])
    return dict(B_T=B,beta=beta,pitch_deg=pitch_deg,steps=steps,time_s=T,
                position_m=[float(a) for a in y[:3]],
                expected_position_m=[float(a) for a in expected],
                displacement_error_m=float(np.linalg.norm(y[:3]-expected)),
                error_in_radii=float(np.linalg.norm(y[:3]-expected)/radius),
                momentum_rel_drift=abs(float(np.linalg.norm(y[3:]))/pnorm0-1))


def run():
    from matplotlib import pyplot as plt
    (ROOT/'results').mkdir(exist_ok=True); (ROOT/'figures').mkdir(exist_ok=True)
    rows=[]
    for B in (.3,.5,.7):
        for beta in (.2,.5,.8,.95,.99):
            h=cyclotron_helix(B,beta,30)
            boosted=h.transformed_axial_boost(h.p)
            rows.append({
                'type':'THEORY_NOT_OBSERVED', 'B_T':B,'v_over_c':beta,
                'radius_m':h.radius,'pitch_per_turn_m':2*math.pi*h.p/h.omega,
                'omega_rad_s':h.omega,'freq_Hz':h.frequency,
                'kappa_inverse_m':h.kappa,'tau_inverse_m':h.tau,
                'v_total_m_s':h.speed,'force_geometry_N':lorentz_force_magnitude_constant_speed(M_E,h),
                'force_Lorentz_N':magnetic_force(B,h), 'inferred_B_T':field_inferred_from_helix(h),
                'boosted_tau_inverse_m':boosted.tau,'boosted_kappa_inverse_m':boosted.kappa,
                'boosted_v_over_c':boosted.speed/C
            })
    csvfile=ROOT/'results'/'magnetic_helix_CODATA2022_THEORY.csv'
    with csvfile.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    electric=[efield_straight_analytic(t) for t in (1e-12,1e-11,1e-10,1e-9,1e-8)]
    with (ROOT/'results'/'electric_straight_COUNTEREXAMPLE.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(electric[0]));w.writeheader();w.writerows(electric)
    h=cyclotron_helix(.5,.8,30)
    boost=h.transformed_axial_boost(h.p)
    independent=rk4_magnetic(.5,steps=12000)
    constants=reproduce_constants_example()
    metrics={'label':'THEORY_AND_NUMERICAL_ONLY_NOT_AN_EXPERIMENT',
      'baseline_constants':constants,
      'n_cases_helix':len(rows),
      'electron_B_0p5T_beta_0p8_pitch30':rows[7],
      'axial_boost_comparison':{'original_tau_per_m':h.tau, 'boosted_tau_per_m':boost.tau,'original_kappa_per_m':h.kappa,'boosted_kappa_per_m':boost.kappa,'boosted_beta':boost.speed/C},
      'magnetic_independent_rk4':independent,
      'straight_electric_counterexample':electric,
      'dimension_checks':check_dimensions(),
      'dimension_catalog_entries':len(dimension_dict()),
      'status':'These are known kinematics, SR, and counterexamples; no four-force unified dynamics has been derived.'}
    (ROOT/'results'/'NUMERICAL_SUMMARY_THEORY.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
    # Kinematics visualization. No observational points.
    from mpl_toolkits.mplot3d import Axes3D  # noqa F401
    t=np.linspace(0,4*math.pi/h.omega,700)
    x=h.radius*np.cos(h.omega*t);y=h.radius*np.sin(h.omega*t);z=h.p*t
    fig=plt.figure(figsize=(9,6.3)); ax=fig.add_subplot(111,projection='3d')
    ax.plot(x*1000,y*1000,z*1000,label='Electron 0.8c, 0.5T, pitch 30deg')
    ax.set(xlabel='x [mm]',ylabel='y [mm]',zlabel='z [mm]',title='ROOT V92: charged-particle helix (THEORY)')
    ax.legend();fig.tight_layout();fig.savefig(ROOT/'figures'/'magnetic_helix_THEORY.png',dpi=155);plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,5)); b=np.linspace(.05,.999,500)
    gam=1/np.sqrt(1-b*b)
    ax.plot(b,gam);ax.set(xlabel='v/c',ylabel='Lorentz gamma',title='Massive particle: gamma diverges as v approaches c (THEORY)')
    ax.grid(True,alpha=.3);ax.set_ylim(0,25);fig.tight_layout();fig.savefig(ROOT/'figures'/'gamma_limit_THEORY.png',dpi=155);plt.close(fig)
    # Axial boost series: torsion is observer dependent.
    us=np.linspace(-.6*C,.6*C,400)
    h2=cyclotron_helix(.5,.8,30)
    boosted=[h2.transformed_axial_boost(u) for u in us]
    fig,ax=plt.subplots(figsize=(8,5));ax.plot(us/C,[v.tau for v in boosted],label='tau measured in boosted frame')
    ax.axvline(h2.p/C,ls='--',label='boost u = original axial speed')
    ax.axhline(0,ls=':');ax.set(xlabel='axial boost u/c',ylabel='spatial torsion tau [1/m]',title='Spatial torsion is not a Lorentz invariant (THEORY)')
    ax.grid(True,alpha=.3);ax.legend();fig.tight_layout();fig.savefig(ROOT/'figures'/'boost_torsion_THEORY.png',dpi=155);plt.close(fig)
    return metrics

if __name__=='__main__':
    print(json.dumps(run(),ensure_ascii=False,indent=2))
