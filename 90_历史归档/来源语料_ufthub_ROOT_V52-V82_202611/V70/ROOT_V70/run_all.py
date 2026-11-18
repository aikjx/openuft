"""Run unit tests and generate results. Dependencies: Python, numpy, matplotlib.
Use 'python run_all.py' from this directory.
"""
from __future__ import annotations
import csv,json,subprocess,sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from rootv70.physics import BODIES,C,EARTH_MU,EARTH_A,G,field_at,gravity_clock_shift,yukawa_shape,MATERIAL_TOY
from rootv70.inference import fixed_earth_design,multi_body_design,rank_report,synthetic_fit,feature_row
BASE=Path(__file__).resolve().parent
RES=BASE/'results';RES.mkdir(exist_ok=True)
PLOTS=BASE/'plots';PLOTS.mkdir(exist_ok=True)
DATA=BASE/'data';DATA.mkdir(exist_ok=True)

def writecsv(file,header,rows):
    with open(file,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(header);w.writerows(rows)

def main():
    # Real authoritative / rounded reference inputs; no claim of exact geodetic data.
    rows=[]
    for b in BODIES.values():
        f=field_at(b,0)
        rows.append([b.name,b.mass,b.radius,b.mu,b.density,b.omega,b.g,f['gravity'],f['effective'],f['tidal_radial'],f['kretschmann'],f['redshift_per_meter'],b.source_charge_toy])
    cols=['body','mass_kg','reference_radius_m','GM_m3_s2','mean_density_kg_m3','spin_rad_s','central_surface_g_m_s2','modeled_g_m_s2','modeled_equatorial_effective_g_m_s2','radial_tidal_gradient_s2','Kretschmann_m4_inverse','clock_fraction_per_m','source_charge_ARBITRARY_TOY']
    writecsv(DATA/'planetary_reference_and_calculations.csv',cols,rows)
    writecsv(DATA/'toy_material_surrogates_NOT_REAL.csv',['material','arbitrary_Q_NOT_EMPIRICAL'],list(MATERIAL_TOY.items()))
    cases=[]
    for body in BODIES:
        b=BODIES[body]
        for lat in [0,45,90]:
            for altitude in [0.,.1*b.radius]:
                f=field_at(b,lat,altitude)
                cases.append([body,lat,altitude,f['gravity'],f['effective'],f['tidal_radial'],f['redshift_per_meter'],f['kretschmann'],b.density])
    writecsv(DATA/'planet_latitude_altitude_54_scenarios.csv',
             ['body','geocentric_lat_deg','altitude_m','gravity_m_s2','effective_m_s2','radial_tidal_s_minus2','redshift_per_m','K_m_minus4','mean_density_kg_m3'],cases)
    features,labels=multi_body_design()
    design_rows=[]
    for (body,lat,h,a,b),x in zip(labels,features):
        design_rows.append([body,lat,h,a,b,*x])
    writecsv(DATA/'SYNTHETIC_design_162_rows.csv',
             ['body','lat_deg','height_fraction','material_a_TOY','material_b_TOY','x_yukawa_TOY','x_curvature_TOY','x_rotation_TOY'],design_rows)
    # Comparisons along altitude, model only
    heights=np.linspace(0.,8e5,161)
    e=BODIES['Earth']
    g=np.array([field_at(e,0,h)['gravity'] for h in heights])
    tide=np.array([field_at(e,0,h)['tidal_radial'] for h in heights])
    clock=np.array([gravity_clock_shift(e,h) for h in heights])
    writecsv(DATA/'earth_altitude_curve.csv',['altitude_m','g_m_s2','radial_tidal_s_minus2','fractional_clock_shift'],zip(heights,g,tide,clock))
    plt.figure(figsize=(8,4.5));plt.plot(heights/1e3,g);plt.xlabel('Altitude (km)');plt.ylabel('Gravity acceleration (m/s^2)');plt.title('Earth: spherical J2 geocentric equator model');plt.tight_layout();plt.savefig(PLOTS/'earth_gravity_vs_altitude.png',dpi=160);plt.close()
    plt.figure(figsize=(8,4.5));plt.plot(heights/1e3,tide);plt.xlabel('Altitude (km)');plt.ylabel('Radial tidal gradient (s^-2)');plt.title('Earth: radial tidal gradient');plt.tight_layout();plt.savefig(PLOTS/'tidal_gradient_vs_altitude.png',dpi=160);plt.close()
    plt.figure(figsize=(8,4.5));plt.plot(heights/1e3,clock);plt.xlabel('Altitude (km)');plt.ylabel('Fractional clock rate difference');plt.title('Earth: weak-field redshift (non-rotating approximation)');plt.tight_layout();plt.savefig(PLOTS/'clock_shift_vs_altitude.png',dpi=160);plt.close()
    body_names=list(BODIES)
    g0=[BODIES[n].g for n in body_names]
    rho=[BODIES[n].density for n in body_names]
    plt.figure(figsize=(8,5));plt.scatter(rho,g0)
    for n,x,y in zip(body_names,rho,g0):plt.annotate(n,(x,y),xytext=(5,3),textcoords='offset points',fontsize=8)
    plt.xlabel('Mean density (kg/m^3)');plt.ylabel('GM/R^2 (m/s^2)');plt.title('Gravity depends on density AND radius');plt.tight_layout();plt.savefig(PLOTS/'density_vs_gravity.png',dpi=160);plt.close()
    # Proof of under-identifiability in a fixed environment and rank restoration
    fig,axes=plt.subplots(1,2,figsize=(9,4))
    for ax,xx,title in zip(axes,[fixed_earth_design(),features],['Fixed Earth environment','Cross-body factorial design']):
        s=np.linalg.svd(xx,compute_uv=False)
        ax.bar(np.arange(1,4),s);ax.set_yscale('log');ax.set_xticks([1,2,3]);ax.set_xlabel('Singular value index');ax.set_title(title)
        ax.set_ylabel('Singular value')
    plt.tight_layout();plt.savefig(PLOTS/'identifiability_rank.png',dpi=160);plt.close()
    lam=np.logspace(3,9,160);shape=np.array([yukawa_shape(e.radius,ll) for ll in lam])
    plt.figure(figsize=(8,4.5));plt.semilogx(lam,shape);plt.xlabel('Toy Yukawa range lambda (m)');plt.ylabel('Point-source force factor');plt.title('Toy scalar correction: not real Earth bounds');plt.tight_layout();plt.savefig(PLOTS/'toy_yukawa_sensitivity.png',dpi=160);plt.close()
    summary={
      'title':'ROOT V70 conditional calculations and experimental design; NO CLAIM OF NEW FORCE',
      'version':'70.0','source_data':'NASA fact sheet rounded mass/diameter/spin; Earth GM/R/J2/IERS; all source charges and material Q are ARBITRARY synthetic inputs',
      'planet_count':len(BODIES),'physical_scenario_count':len(cases),
      'synthetic_feature_rows':len(features),
      'earth_g_at_equator':field_at(e,0)['gravity'],
      'earth_effective_equator':field_at(e,0)['effective'],
      'earth_tidal_radial_s_minus2':field_at(e,0)['tidal_radial'],
      'earth_grav_redshift_1mm':gravity_clock_shift(e,.001),
      'earth_curvature_K_m_minus4':field_at(e,0)['kretschmann'],
      'atmosphere_magnetic_moon_geoid_not_modeled':True,
      'fixed_environment_identifiability':rank_report(fixed_earth_design()),
      'cross_body_identifiability':rank_report(features),
      'synthetic_parameter_fit':synthetic_fit(),
      'not_proven':['independent prediction of G','four-force unification','existence of new scalar fifth force','composition dependence of G','quantum UV completion']
    }
    (RES/'numerical_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
    report=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=BASE,capture_output=True,text=True)
    (RES/'tests_verbose.txt').write_text(report.stdout+'\n'+report.stderr,encoding='utf-8')
    out={'success':report.returncode==0,'tail':report.stderr.splitlines()[-6:],'returncode':report.returncode}
    (RES/'verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k in ['earth_g_at_equator','earth_tidal_radial_s_minus2','earth_grav_redshift_1mm','earth_curvature_K_m_minus4','planet_count','physical_scenario_count','synthetic_feature_rows']},indent=2))
    print('\n'.join(out['tail']))
    if report.returncode:sys.exit(report.returncode)
if __name__=='__main__':main()
