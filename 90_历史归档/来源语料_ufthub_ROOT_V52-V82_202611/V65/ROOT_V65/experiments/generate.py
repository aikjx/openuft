#!/usr/bin/env python3
"""Generate reproducible ROOT V65 TOY model plots/CSV/JSON; no measured field data."""
from __future__ import annotations
import csv,json,math,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root))
from src import root_v65 as m
D=root/'data';R=root/'results';D.mkdir(exist_ok=True);R.mkdir(exist_ok=True)

def table(name,fields,rows):
    with (D/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

helix=[]
for theta in range(-85,86):
    h=m.helix_from_radius_angle(1.,math.radians(theta),1.)
    helix.append(dict(angle_deg=theta,kappa_per_m=h.curvature,torsion_per_m=h.torsion,
                      vtheta_over_v=h.tangential_speed/h.speed,vz_over_v=h.axial_speed/h.speed,
                      reconstructed_R_m=h.radius))
table('MATH_helix_angular_scan.csv',list(helix[0]),helix)

mass=[]
try:
    from scipy.special import exp1
    scipy=True
except ImportError:scipy=False
for j in range(201):
    mu=j*0.02
    f=m.cutoff_threshold(mu)
    cross=float(math.exp(-mu*mu)-mu*mu*exp1(mu*mu)) if scipy and mu>0 else (1. if mu==0 else None)
    mass.append(dict(mu_dimensionless=mu,F_proper_time=f,F_scipy_optional=cross,
                     abs_crosscheck_error=(abs(f-cross) if cross is not None else 'NA')))
table('TOY_mass_cutoff_scan.csv',list(mass[0]),mass)

fit=m.inverse_fit_cutoff(1)
scan=[]; lp=m.planck_length()
for n in [1,2,4,8,16,32,64]:
    for frac in [.1,.15,.2,.3,.5,1,1.5,2,3,5]:
        ell=lp*frac;coeff=m.induced_scalar_coefficient(n,0,ell)
        g=1/coeff
        scan.append(dict(N_scalar_species=n,ell_over_lp_from_Gobs=frac,
                         G_ind_over_Gobs=g/m.G_CODATA_2022,
                         uses_observed_G_for_lp=True))
table('FIT_NOT_PREDICTION_induced_G_scan.csv',list(scan[0]),scan)

r=m.EARTH_RADIUS
eps=[];f=m.yukawa_shape(r,r)
for i in range(-120,121):
    delta_alpha=i*1e-16
    eta=m.eotvos_eta(delta_alpha/2,-delta_alpha/2,r,r)
    lo,hi=m.microscope_interval()
    eps.append(dict(delta_alpha_TOY=delta_alpha,eta_predicted_TOY=eta,
                    within_illustrative_95pct_interval=lo<=eta<=hi,
                    MICROSCOPE_eta_central_observed=m.MICROSCOPE_ETA))
table('TOY_Microscope_Eotvos_sensitivity.csv',list(eps[0]),eps)

earth=[]
for alt_km in range(0,2001,25):
    xyz=(m.EARTH_RADIUS+alt_km*1000,0,0)
    earth.append(dict(altitude_km=alt_km,g_norm_m_s2=m.norm(m.gravity_acceleration(xyz)),
                      B_equator_T=m.norm(m.toy_magnetic_field(xyz)),
                      data_type='TOY: spherical Earth plus aligned dipole'))
table('TOY_Earth_g_dipole_altitude.csv',list(earth[0]),earth)

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams['font.size']=11
    fig,ax=plt.subplots(figsize=(9,4.7))
    ax.plot([x['angle_deg'] for x in helix],[x['kappa_per_m'] for x in helix],label='curvature 1/m')
    ax.plot([x['angle_deg'] for x in helix],[x['torsion_per_m'] for x in helix],label='signed torsion 1/m')
    ax.set(xlabel='Pitch angle (deg)',ylabel='1 / m',title='ROOT V65: ideal circular helix, R = 1m')
    ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(R/'MATH_helix_inverse.png',dpi=140);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,4.7))
    ax.plot([v['mu_dimensionless'] for v in mass],[v['F_proper_time'] for v in mass],label='proper-time threshold F')
    ax.set(xlabel='mass/cutoff ratio',ylabel='F',title='Conditional scalar proper-time cutoff: regulator dependent')
    ax.grid(alpha=.2);fig.tight_layout();fig.savefig(R/'TOY_cutoff_threshold.png',dpi=140);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,4.7))
    for n in [1,4,16,64]:
        sub=[v for v in scan if v['N_scalar_species']==n]
        ax.loglog([v['ell_over_lp_from_Gobs'] for v in sub],[v['G_ind_over_Gobs'] for v in sub],marker='o',label=f'N={n}')
    ax.axhline(1,ls=':',color='black',label='G_ind/G_obs=1 (fit target)')
    ax.set(xlabel='cutoff length / Planck length computed using observed G',ylabel='G_ind / G_obs',
           title='Reverse calibration degeneracy: NOT a prediction')
    ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(R/'FIT_induced_G_degeneracy.png',dpi=140);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,4.7))
    ax.plot([v['delta_alpha_TOY'] for v in eps],[v['eta_predicted_TOY'] for v in eps],label='toy eta')
    lo,hi=m.microscope_interval();ax.axhspan(lo,hi,alpha=.2,label='approx. 95% illustrative MICROSCOPE interval')
    ax.set(xlabel='alpha_A - alpha_B (invented candidate coupling)',ylabel='eta',
           title='Composition-dependent fifth-force benchmark, not a data fit')
    ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(R/'TOY_Eotvos_bound.png',dpi=140);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,4.7))
    ax.plot([v['altitude_km'] for v in earth],[v['g_norm_m_s2'] for v in earth],label='spherical gravity m/s²')
    ax.set(xlabel='Altitude above spherical Earth (km)',ylabel='Gravity (m/s²)',
           title='Toy Earth only — not EGM2008 or measured data')
    ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(R/'TOY_Earth_gravity.png',dpi=140);plt.close(fig)
    plots='generated (matplotlib)'
except ImportError:
    plots='not generated (matplotlib absent)'

summary={'project':'ROOT_V65','release_date':'2026-11-17',
         'scientific_status':'CONDITIONAL_DERIVATIONS_ONLY; G and four-force unification OPEN',
         'data_provenance':'All CSVs are generated from equations; MICROSCOPE central value only is observed input',
         'G_OBS_SI':m.G_CODATA_2022,'G_sigma_SI':m.G_STD_UNCERTAINTY,
         'l_planck_from_observed_G_m':lp,'one_scalar_reverse_fit_cutoff_m':fit,
         'earth_surface_spherical_g_m_s2':earth[0]['g_norm_m_s2'],
         'microscope_eta_observed':m.MICROSCOPE_ETA,
         'microscope_illustrative95_range':m.microscope_interval(),
         'mass_threshold_crosschecked_with_scipy':scipy,
         'max_mass_threshold_abs_error_vs_scipy':max([v['abs_crosscheck_error'] for v in mass if v['abs_crosscheck_error']!='NA'],default=None),
         'generated_csv_files':5,'plot_status':plots}
(R/'v65_numerical_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
