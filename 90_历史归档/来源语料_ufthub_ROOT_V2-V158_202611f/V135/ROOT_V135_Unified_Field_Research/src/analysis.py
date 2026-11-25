"""Generate immutable, self-contained CSV/JSON/SVG outputs; no internet needed."""
from __future__ import annotations
import csv, json, math, pathlib, sys, unittest, datetime
from physics import *

ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'results'
FIG=ROOT/'figures'
OUT.mkdir(exist_ok=True);FIG.mkdir(exist_ok=True)

def write_csv(path,rows):
    with path.open('w',encoding='utf-8',newline='') as f:
        dw=csv.DictWriter(f,fieldnames=list(rows[0]));dw.writeheader();dw.writerows(rows)


def make_svg(path, series, y_title):
    """Simple dependency-free vector graph. Values in series=(name,[(x,y),...],color)."""
    values=[p for _, pts, _ in series for p in pts]
    xmin=min(x for x,y in values); xmax=max(x for x,y in values)
    ymin=min(y for x,y in values); ymax=max(y for x,y in values)
    ymin=min(0,ymin);ymax=ymax if ymax>ymin else ymin+1
    W,H=840,440;L,B,T,R=92,70,50,36
    def px(x):return L+(x-xmin)/(xmax-xmin)*(W-L-R)
    def py(y):return H-B-(y-ymin)/(ymax-ymin)*(H-B-T)
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
       '<rect width="100%" height="100%" fill="#ffffff"/>',
       f'<text x="{L}" y="28" font-family="Arial" font-size="18" font-weight="bold">{y_title}</text>']
    for i in range(6):
        y=ymin+(ymax-ymin)*i/5
        s.extend([f'<path d="M{L},{py(y):.2f} L{W-R},{py(y):.2f}" stroke="#e6e6e6"/>',
            f'<text x="{L-8}" y="{py(y)+4:.2f}" text-anchor="end" font-family="Arial" font-size="12">{y:.3g}</text>'])
    for i in range(6):
        x=xmin+(xmax-xmin)*i/5
        s.append(f'<text x="{px(x):.2f}" y="{H-B+22}" text-anchor="middle" font-family="Arial" font-size="12">{x:.0f}</text>')
    s.append(f'<text x="{W/2}" y="{H-12}" text-anchor="middle" font-family="Arial" font-size="13">Altitude above mean radius (km)</text>')
    for idx,(name,pts,color) in enumerate(series):
        d=' '.join(('M' if i==0 else 'L')+f'{px(x):.2f},{py(y):.2f}' for i,(x,y) in enumerate(pts))
        s.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.5"/>')
        s.append(f'<text x="{W-255}" y="{T+idx*22}" font-family="Arial" font-size="12" fill="{color}">{name}</text>')
    s.append('</svg>')
    path.write_text('\n'.join(s),encoding='utf-8')


def main():
    for layers in (EARTH_LAYERS,MOON_LAYERS): check_shells(layers)
    heights=[0,50,100,200,400,800,1500,2000,5000,10000]
    rows=[]; plots=[]
    for name,mu,R,layers in [('Earth',MU_EARTH,R_EARTH_MEAN,EARTH_LAYERS),('Moon',MU_MOON,R_MOON,MOON_LAYERS)]:
        series=[]
        for h in heights:
            r=R+h*1000
            g=mu/r**2
            frac=yukawa_accel_ratio(r,layers)
            row={'body':name,'height_km':h,'r_m':r,'g_newton_m_s2':f'{g:.12g}',
                 'hypothesis_alpha':f'{ROOT_ALPHA:.12g}','hypothesis_lambda_km':ROOT_LAMBDA/1000,
                 'yukawa_fraction_dimensionless':f'{frac:.12g}',
                 'yukawa_extra_m_s2':f'{g*frac:.12g}',
                 'g_candidate_total_m_s2':f'{g*(1+frac):.12g}',
                 'data_status':'MODEL_PREDICTION_NOT_OBSERVATION'}
            rows.append(row);series.append((h,100*frac))
        plots.append((name,series,'#2563eb' if name=='Earth' else '#d97706'))
    write_csv(OUT/'earth_moon_altitudes.csv',rows)
    make_svg(FIG/'yukawa_altitude.svg', plots,'ROOT candidate: hypothetical extra acceleration (%)')
    make_svg(FIG/'yukawa_near_earth_moon.svg',[(name,[(x,y) for x,y in series if x<=800],color) for name,series,color in plots],
             'ROOT candidate near Earth/Moon (0-800 km): NOT observed')

    vrows=[]
    for name,p in [('equator',(R_EARTH_EQUATOR,0,0)),('north_pole',(0,0,R_EARTH_POLAR)),
                   ('midlatitude_45',(R_EARTH_EQUATOR/math.sqrt(2),0,R_EARTH_EQUATOR/math.sqrt(2))),
                   ('off_meridian',(4.3e6,3.2e6,4e6))]:
        a=earth_gravity(p);eff=earth_rotating_effective(p)
        vrows.append({'name':name,'x_m':p[0],'y_m':p[1],'z_m':p[2],
                     'ax_m_s2':a[0],'ay_m_s2':a[1],'az_m_s2':a[2],
                     'g_abs_m_s2':norm(a),'effective_g_abs_m_s2':norm(eff),
                     'model':'Earth monopole+J2; effective rotates with Earth; not full EGM2008'})
    write_csv(OUT/'earth_vectors.csv',vrows)

    internal=[]
    for body,layers in [('Earth',EARTH_LAYERS),('Moon',MOON_LAYERS)]:
        R=check_shells(layers)
        for frac in [0.,.05,.1,.2,.3,.45,.55,.7,.85,.95,1.]:
            r=R*frac
            internal.append({'body':body,'fraction_radius':frac,'radius_km':r/1000,
                             'enclosed_mass_kg':shell_cumulative_mass(r,layers),
                             'internal_newton_g_m_s2':internal_g(r,layers),
                             'data_status':'ILLUSTRATIVE_DENSITY_NOT_PREM_GRAIL'})
    write_csv(OUT/'interior_profiles.csv',internal)

    # Cross-check a rounded terrestrial benchmark (not a complete observation fit).
    eqpos=(R_EARTH_EQUATOR,0.,0.)
    baseline_eq=norm(earth_rotating_effective(eqpos))
    ext_frac=yukawa_accel_ratio(R_EARTH_EQUATOR,EARTH_LAYERS)
    new_extra=MU_EARTH/R_EARTH_EQUATOR**2*ext_frac
    benchmark=[{'location':'Earth equator','reference':'NASA Earth Fact Sheet, rounded to 3 decimals',
       'reference_m_s2':9.780,'baseline_J2_rotation_m_s2':baseline_eq,
       'root_extra_m_s2':new_extra,'root_candidate_total_m_s2':baseline_eq+new_extra,
       'baseline_minus_reference_m_s2':baseline_eq-9.780,
       'root_minus_reference_m_s2':baseline_eq+new_extra-9.780,
       'caveat':'Not formal exclusion: indicative discrepancy, no high-degree gravity field, full frame or covariance'}]
    write_csv(OUT/'benchmark_earth_equator.csv',benchmark)

    variants=[]
    last=EARTH_LAYERS[-1]
    different_earth={
       'V132_illustrative':EARTH_LAYERS,
       'uniform_illustrative':(Layer(0,R_EARTH_MEAN,5513),),
       'outer_layer_minus20pct':EARTH_LAYERS[:-1]+(Layer(last.inner_m,last.outer_m,last.density_kg_m3*.8),),
       'outer_layer_plus20pct':EARTH_LAYERS[:-1]+(Layer(last.inner_m,last.outer_m,last.density_kg_m3*1.2),),
    }
    for label,lay in different_earth.items():
        variants.append({'body':'Earth','density_model':label,
            'surface_fraction':yukawa_accel_ratio(R_EARTH_MEAN,lay),
            'surface_extra_m_s2':MU_EARTH/R_EARTH_MEAN**2*yukawa_accel_ratio(R_EARTH_MEAN,lay),
            'observation':'none (model variation only)'})
    for label,lay in {'Moon_illustrative_4layer':MOON_LAYERS,'Moon_uniform':(Layer(0,R_MOON,3344.),)}.items():
        variants.append({'body':'Moon','density_model':label,
            'surface_fraction':yukawa_accel_ratio(R_MOON,lay),
            'surface_extra_m_s2':MU_MOON/R_MOON**2*yukawa_accel_ratio(R_MOON,lay),
            'observation':'none (model variation only)'})
    write_csv(OUT/'density_sensitivity.csv',variants)

    orbit_rows=[]
    for body,mu,R,lay in [('Earth',MU_EARTH,R_EARTH_MEAN,EARTH_LAYERS),('Moon',MU_MOON,R_MOON,MOON_LAYERS)]:
        for h in (0.,50e3,100e3,200e3,400e3,800e3,2000e3):
            r=R+h
            v=near_circular_orbit_frequencies(r,mu,lay)
            orbit_rows.append({'body':body,'height_km':h/1000,
                **v, 'model':'spherical Newton plus hypothetical finite-body Yukawa; NO J2/GR/third-body; not observed'})
    write_csv(OUT/'candidate_near_circular_precession.csv',orbit_rows)

    # Compare analytic and angular+radial Simpson. Independent quadrature convergence.
    comparisons=[]
    for body,layers in [('Earth',EARTH_LAYERS),('Moon',MOON_LAYERS)]:
        anal=yukawa_compensated_mass_analytic(layers,ROOT_LAMBDA)
        for n in (64,128,256,512,1024):
            num=yukawa_compensated_mass_simpson(layers,ROOT_LAMBDA,n)
            comparisons.append({'body':body,'n_per_layer':n,'analytic_compensated_mass_kg':anal,
                                'simpson_compensated_mass_kg':num,'relative_error':(num-anal)/anal})
    write_csv(OUT/'quadrature_convergence.csv',comparisons)

    # Purely synthetic injection/recovery with nuisance GM offset.
    hgrid=[0.,100e3,200e3,400e3,800e3,2000e3]
    R=R_EARTH_MEAN
    shape=[yukawa_accel_ratio(R+h,EARTH_LAYERS,alpha=1.) for h in hgrid]
    beta_true=0.0002; alpha_true=.05
    mock=[beta_true+alpha_true*s for s in shape]
    fit=fit_fractional_offset_and_alpha(hgrid,mock,[1e-5]*len(mock),EARTH_LAYERS)
    run_null=fit_fractional_offset_and_alpha(hgrid,[0.]*len(mock),[1e-5]*len(mock),EARTH_LAYERS)
    metrics={
        'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'type':'NUMERICAL_RESEARCH_NOT_DISCOVERY',
        'assumptions':{'alpha':ROOT_ALPHA,'lambda_m':ROOT_LAMBDA,'earth_layers':'V132 illustrated 5-layer, NOT PREM','moon_layers':'illustrative 4-layer, NOT GRAIL',
                       'mass_parameter_source':'JPL DE440; not independently derived','observational_data_ingested':False},
        'sources':{'JPL_DE440':'https://ssd.jpl.nasa.gov/astro_par.html',
                   'CODATA_2022':'https://physics.nist.gov/cuu/pdf/wall_2022.pdf',
                   'NASA_Earth':'https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html',
                   'NASA_GRAIL':'https://science.nasa.gov/mission/grail/',
                   'ICGEM':'https://icgem.gfz.de/faq'},
        'mass_from_mu_kg':{'Earth':MU_EARTH/G,'Moon':MU_MOON/G},
        'G_relative_standard_uncertainty':G_STD_UNC/G,
        'unscaled_shell_mass_kg':{'Earth':mass_shells(EARTH_LAYERS),'Moon':mass_shells(MOON_LAYERS)},
        'shape_factor_surface_alpha1':{'Earth':yukawa_shape(EARTH_LAYERS,ROOT_LAMBDA),'Moon':yukawa_shape(MOON_LAYERS,ROOT_LAMBDA)},
        'surface_fraction_alpha_1over3':{'Earth':yukawa_accel_ratio(R_EARTH_MEAN,EARTH_LAYERS),
                                           'Moon':yukawa_accel_ratio(R_MOON,MOON_LAYERS)},
        'synthetic_control':{'injected_offset':beta_true,'injected_alpha':alpha_true,
                             'fitted':fit,'zero_control':run_null,
                             'caution':'Synthetic data generated from model; not evidence for fifth force.'},
        'status':{'four_force_unification_proved':False,'new_gravity_detected':False,
                  'real_gravity_coefficient_fit':False,'mathematical_kernel_crosscheck':True}
    }
    (OUT/'summary.json').write_text(json.dumps(metrics,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'surface_Yukawa_Earth':metrics['surface_fraction_alpha_1over3']['Earth'],
                      'surface_Yukawa_Moon':metrics['surface_fraction_alpha_1over3']['Moon'],
                      'Earth_400km_extra':float(next(r['yukawa_extra_m_s2'] for r in rows if r['body']=='Earth' and r['height_km']==400)),
                      'Moon_mass_inferred_kg':metrics['mass_from_mu_kg']['Moon'],
                      'max_numeric_relerr':max(abs(x['relative_error']) for x in comparisons if x['n_per_layer']==1024)},indent=2))

if __name__=='__main__':main()
