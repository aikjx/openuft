"""Compute fully labelled theoretical/synthetic diagnostic outputs."""
import csv
import json
import pathlib
from v137_diagnostics import *


def run():
    res=ROOT/'results'
    res.mkdir(exist_ok=True)
    bodies={'earth':(old.EARTH_LAYERS,old.MU_EARTH),
            'moon':(old.MOON_LAYERS,old.MU_MOON)}
    with (res/'earth_moon_mu_anchor.csv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['body','height_m','g_newton_m_s2',
                                           'delta_g_yukawa_m_s2','root_to_newton_ratio',
                                           'fractional_after_high_anchor'])
        writer.writeheader()
        for name,(layers,mu) in bodies.items():
            for row in surface_diagnostic(layers,mu):writer.writerow({'body':name,**row})
    heights=[i*100e3 for i in range(11)]
    injected=[.002,1/3,.0003]
    X,y,C=simulate(heights,injected,seed=233)
    fit=gls_fit(X,y,C)
    no_signal=[.002,0.,.0003]
    xn,yn,Cn=simulate(heights,no_signal,seed=233)
    nullfit=gls_fit(xn,yn,Cn)
    mc=monte_carlo_coverage(heights,injected,n=300,seed=471)
    weak=noisy_three_altitude([0,200e3,400e3],1e-5,trials=1000)
    strong=noisy_three_altitude([0,200e3,400e3],1/3,trials=1000)
    out={'metadata':{'data_type':'SYNTHETIC_AND_THEORETICAL_ONLY',
                     'external_satellite_observations_loaded':False,
                     'input_Yukawa_alpha':old.ROOT_ALPHA,
                     'input_Yukawa_lambda_m':old.ROOT_LAMBDA,
                     'mass_layers':'V135 inherited illustrative, not reconstructed PREM/GRAIL'},
         'theory':{'earth_surface_eps':old.ROOT_ALPHA*unit_shape(old.check_shells(old.EARTH_LAYERS),old.EARTH_LAYERS),
                   'moon_surface_eps':old.ROOT_ALPHA*unit_shape(old.check_shells(old.MOON_LAYERS),old.MOON_LAYERS),
                   'earth_surface_after_1600km_GM_fit':residual_after_mu_fit(old.check_shells(old.EARTH_LAYERS),old.check_shells(old.EARTH_LAYERS)+1600e3,old.EARTH_LAYERS)},
         'synthetic_injection':{'true_params_offset_alpha_nuisance':injected,
                                 'fit':fit,'null_true_params':no_signal,'null_fit':nullfit,
                                 'mc_95pct_coverage':mc},
         'three_altitude_noise':{'weak_signal_alpha_1e-5':weak,'strong_signal_alpha_1over3':strong}}
    (res/'summary_v137.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    with (res/'synthetic_heights_observations_NOT_REAL.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['height_m','synthetic_fractional_residual','synthetic_sigma_fractional'])
        for h,yi in zip(heights,y):w.writerow([int(h),yi,2e-6])
    print(json.dumps({'surface_eps_earth':out['theory']['earth_surface_eps'],
                      'surface_eps_moon':out['theory']['moon_surface_eps'],
                      'after_anchor_surface_eps':out['theory']['earth_surface_after_1600km_GM_fit'],
                      'synthetic_fit_alpha':fit['beta'][1],
                      'synthetic_alpha_sigma':fit['standard_errors'][1],
                      'mc_coverage':mc['coverage'],
                      'weak_ratio_median_abs_error':weak['median_abs_error'],
                      'strong_ratio_median_abs_error':strong['median_abs_error']},indent=2))
if __name__=='__main__':run()
