"""Compute self-contained predictions and explicit scientific-evidence audit."""
import csv
import datetime
import json
import math
import pathlib
import sys
from v136_physics import *

ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'results'
FIG=ROOT/'figures'
OUT.mkdir(exist_ok=True);FIG.mkdir(exist_ok=True)

def csv_write(path,rows):
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
        w.writeheader();w.writerows(rows)

def main():
    alt=(0,100,200,400,800,2000)
    outputs=[]
    for name,mu,R,layers in [('Earth',old.MU_EARTH,old.R_EARTH_MEAN,old.EARTH_LAYERS),('Moon',old.MU_MOON,old.R_MOON,old.MOON_LAYERS)]:
        for h in alt:
            r=R+h*1000
            e=eps_at(r,layers)
            oe=epicycle_from_eps_gradient(r,mu,layers)
            outputs.append({'body':name,'altitude_km':h,'distance_m':r,
                'newton_g_m_s2':f'{mu/r**2:.15g}',
                'candidate_fraction':f'{e:.15g}',
                'candidate_extra_g_m_s2':f'{mu/r**2*e:.15g}',
                'GM_normalized_deviation_surface_to_altitude':f'{relative_force_deviation(R,r,layers):.15g}',
                'near_circular_precession_rad_per_rev':f'{oe["precession"]:.15g}' if oe['stable'] else 'UNSTABLE',
                'label':'MODEL_PREDICTION_NOT_OBSERVATION'})
    csv_write(OUT/'height_diagnostics.csv',outputs)
    triple=[]
    for name,R,layers in [('Earth',old.R_EARTH_MEAN,old.EARTH_LAYERS),('Moon',old.R_MOON,old.MOON_LAYERS)]:
        for spacing in (50,100,200,400):
            triple.append({'body':name,'spacing_km':spacing,'height_triplet_km':f'0/{spacing}/{2*spacing}',
                'alpha_GM_density_independent_ratio':f'{three_altitude_shape_ratio(R,R+spacing*1000,R+2*spacing*1000,layers):.15g}',
                'lambda_km':old.ROOT_LAMBDA/1000,
                'status':'MODEL_SHAPE_NO_OBSERVATIONAL_FIT'})
    csv_write(OUT/'three_altitude_shape.csv',triple)
    lambda_scan=[]
    for lam_km in (50.,75.,100.,124.6,175.,250.,400.,1000.):
        lam=lam_km*1000
        for name,R,layers in [('Earth',old.R_EARTH_MEAN,old.EARTH_LAYERS),('Moon',old.R_MOON,old.MOON_LAYERS)]:
            e0=eps_at(R,layers,lam=lam)
            e4=eps_at(R+400e3,layers,lam=lam)
            lambda_scan.append({'body':name,'lambda_km':lam_km,'coupling_alpha_assumed':old.ROOT_ALPHA,
               'surface_fraction':f'{e0:.15g}','400km_fraction':f'{e4:.15g}',
               'GM_free_surface_400km_difference':f'{relative_force_deviation(R,R+400e3,layers,lam=lam):.15g}',
               'status':'PARAMETER_SCAN_NOT_OBSERVATION'})
    csv_write(OUT/'range_sensitivity.csv',lambda_scan)
    # A model-independent mathematical counterexample to universal three-force orthogonality.
    E=(0.,0.,4.);B=(0.,0.,3.)
    E2,B2=lorentz_boost_fields(E,B,(.5,0.,0.))
    theory_tests={
        'parallel_E_B_dot_not_zero':dot3(E,B),
        'parallel_E_B_cross_is_zero':cross3(E,B),
        'boosted_E_B_dot':dot3(E2,B2),
        'arbitrary_helix_tau_over_kappa_possible':True,
        'free_null_helix_is_geodesic':False,
        'general_unification_proof':False,
    }
    (OUT/'geometry_counterexamples.json').write_text(json.dumps(theory_tests,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    ee=eps_at(old.R_EARTH_MEAN,old.EARTH_LAYERS)
    me=eps_at(old.R_MOON,old.MOON_LAYERS)
    normalized=relative_force_deviation(old.R_EARTH_MEAN,old.R_EARTH_MEAN+400e3,old.EARTH_LAYERS)
    result={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'research_state':'CANDIDATE_HYPOTHESIS_NOT_PROVEN',
        'earth_surface_extra_fraction':ee,'moon_surface_extra_fraction':me,
        'earth_surface_to_400km_GM_independent_deviation':normalized,
        'earth_400km_candidate_precession_rad_per_revolution':epicycle_from_eps_gradient(old.R_EARTH_MEAN+400e3,old.MU_EARTH,old.EARTH_LAYERS)['precession'],
        'parameter_source':'V132/V135 inherited alpha=1/3; lambda=124.6 km: arbitrary test inputs, NOT derived.',
        'data_source':'JPL baseline mass parameters, ILLUSTRATIVE_LAYER_DENSITIES. No external raw satellite data.',
        'claims':{'fifth_force_detected':False,'theory_confirmed':False,'all_cases_verified':False,
            'observed_earth_moon_residuals_fit':False,'four_forces_unified':False,
            'new_parameter_free_lambda_prediction':False,'new_null_tests_derived':True,
            'program_tested':True},
        'hard_open_questions':['derive true ROOT action without inserting gauge groups','derive coupling constants and mass spectrum','source-independent physical G prediction','experimental covariance-weighted Earth/Moon tests','quantum/GR consistency of null helix']}
    (OUT/'summary_v136.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    # Standalone svg, using altitudes on horizontal axis and percentage extra force on vertical.
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="860" height="440" viewBox="0 0 860 440">',
      '<rect width="860" height="440" fill="white"/>',
      '<text x="65" y="32" font-family="sans-serif" font-size="19" font-weight="bold">Hypothetical ROOT Yukawa fractional gravity (NOT observations)</text>',
      '<line x1="70" y1="380" x2="800" y2="380" stroke="#333"/><line x1="70" y1="55" x2="70" y2="380" stroke="#333"/>',
      '<text x="360" y="423" font-family="sans-serif" font-size="13">Height above surface (km)</text>',
      '<text x="77" y="65" font-family="sans-serif" font-size="12">Extra acceleration (%)</text>']
    for name,R,layers,color in [('Earth',old.R_EARTH_MEAN,old.EARTH_LAYERS,'#2476a3'),('Moon',old.R_MOON,old.MOON_LAYERS,'#be6d18')]:
      points=[]
      for h in range(0,801,10):
        e=eps_at(R+h*1000,layers)
        points.append(f'{70+h/800*730:.2f},{380-e*100/3.5*300:.2f}')
      svg.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="3"/>')
      svg.append(f'<text x="640" y="{82 if name=="Earth" else 104}" font-family="sans-serif" fill="{color}" font-size="13">{name}</text>')
    for h in (0,200,400,600,800):
      svg.append(f'<text x="{70+h/800*730:.1f}" y="400" font-family="sans-serif" font-size="12" text-anchor="middle">{h}</text>')
    svg.append('</svg>')
    (FIG/'earth_moon_candidate.svg').write_text('\n'.join(svg)+'\n',encoding='utf-8')
    print(json.dumps({'result':'MODEL_ONLY','Earth_surface_fraction':ee,'Moon_surface_fraction':me,
                      'Earth_GM_free_diagnostic_0_400km':normalized,
                      'Earth_precession_rad_per_rev_400km':result['earth_400km_candidate_precession_rad_per_revolution']},indent=2))
if __name__=='__main__':main()
