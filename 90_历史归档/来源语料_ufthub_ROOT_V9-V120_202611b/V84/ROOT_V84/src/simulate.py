"""Reproducible only: synthetic double-sensor, real/sham, multi-distance ABBA experiments."""
from __future__ import annotations
import csv,json,random,math,statistics
from pathlib import Path
from .physics import Rig,gravity_readings,common_amplitude,yukawa_amplitude_per_alpha,G_EARTH_REF
from .analysis import corrected,fit_three_parameter,estimate_two_parameter

DISTANCES=(.38,.46,.55,.70,.90,1.20,1.55)
LAM_DEFAULT=.25


def synthetic_trial(rig:Rig, distances=DISTANCES, blocks=56, seed=8401,
                    alpha_injected=0., noise_sigma=8e-10,
                    identical_nuisance=False):
    """All numbers synthetic; include 2 sensor readings per 4-step block and sham arm.

    identical_nuisance: real-arm-only artifact with the EXACT candidate Yukawa distance shape;
    formally unidentifiable from physical alpha at this observation level.
    """
    if blocks<3 or noise_sigma<=0:raise ValueError('need blocks>=3 and positive noise')
    out=[]
    for j,d in enumerate(distances):
        rig.validate(d)
        ynew=yukawa_amplitude_per_alpha(rig,d,LAM_DEFAULT)
        for sham in (False,True):
            rng=random.Random(seed + j*1011 + (7727 if sham else 0))
            for b in range(blocks):
                initial=rng.choice([-1,1]); pattern=[initial,-initial,-initial,initial]
                # source motion actuator is in both channels (sham may have imperfect match in reality)
                actuator=(2.2e-9+0.5e-9*(d/.5))*rng.uniform(.98,1.02)
                sensor_bias_left=3.2e-8 + b*1e-11
                sensor_bias_right=-1.2e-8 + b*1.2e-11
                block_drift=rng.gauss(0.,5e-9)
                slope=rng.gauss(0.,1.2e-9)
                for t,p in enumerate(pattern):
                    g=gravity_readings(rig,d,p) if not sham else {'left':0.,'right':0.}
                    # Differential real-vs-sham p-odd part. Only synthetic model; no hardware claim.
                    add_new=0. if sham else p*(alpha_injected*ynew + (ynew*.08 if identical_nuisance else 0.))
                    tilt=G_EARTH_REF*rng.gauss(0.,2e-11)
                    vibration=rng.gauss(0.,noise_sigma*.12)
                    left=g['left']+add_new+p*actuator+sensor_bias_left+block_drift+slope*(t-1.5)+tilt+vibration+rng.gauss(0.,noise_sigma)
                    right=g['right']+add_new+p*actuator+sensor_bias_right+block_drift+slope*(t-1.5)+tilt+vibration+rng.gauss(0.,noise_sigma)
                    out.append({'scenario':'SYNTHETIC_'+('INJECTED' if alpha_injected else 'NULL')+('_CONFOUNDED' if identical_nuisance else ''),
                                'arm':'SHAM' if sham else 'SOURCE','distance_m':d,'block':b,
                                'step':t,'p':p,'left_m_s2':left,'right_m_s2':right,
                                'common_m_s2':(left+right)/2,'gradient_s2':(right-left)/(2*rig.half_baseline_m),
                                'provenance':'SYNTHETIC_NOT_REAL_DATA'})
    return out


def summarize_trials(rig:Rig, rows, lam=LAM_DEFAULT):
    dist=sorted(set(z['distance_m'] for z in rows))
    estimates=[]
    for d in dist:
        real=[z for z in rows if z['distance_m']==d and z['arm']=='SOURCE']
        sham=[z for z in rows if z['distance_m']==d and z['arm']=='SHAM']
        r=corrected(real,sham)
        r.update({'distance_m':d,'newton_m_s2':common_amplitude(rig,d),
                  'yukawa_alpha1_m_s2':yukawa_amplitude_per_alpha(rig,d,lam),
                  'normalized_newton_ratio':r['signal']/common_amplitude(rig,d)})
        estimates.append(r)
    fits={'newton_plus_offset':estimate_two_parameter(rig,estimates),
          'newton_yukawa_offset':fit_three_parameter(rig,estimates,lam)}
    return {'estimates':estimates,'fits':fits,'lambda_m':lam}


def save_rows(path, rows):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def generate_all(root:Path, blocks=112):
    root=Path(root);rig=Rig()
    scenarios={
        'NULL':synthetic_trial(rig,blocks=blocks,seed=84001,alpha_injected=0.0),
        'INJECTED':synthetic_trial(rig,blocks=blocks,seed=84002,alpha_injected=.08),
        'CONFOUNDED':synthetic_trial(rig,blocks=blocks,seed=84003,identical_nuisance=True)
    }
    result={'version':'ROOT V84','status':'ALL_DATA_SYNTHETIC_NO_HARDWARE',
            'physics_assumptions':{'G_reference_m3_kg_s2':6.67430e-11,'rig':rig.__dict__,
                                   'source':'uniform sphere; sensors outside',
                                   'range_lambda_m':LAM_DEFAULT,'distance_grid_m':DISTANCES},
            'scenarios':{}}
    (root/'data').mkdir(parents=True,exist_ok=True);(root/'results').mkdir(parents=True,exist_ok=True)
    for name,rows in scenarios.items():
        save_rows(root/'data'/f'{name}_SYNTHETIC_ABBA.csv',rows)
        res=summarize_trials(rig,rows)
        result['scenarios'][name]={
            'injected_alpha_truth':{'NULL':0.,'INJECTED':.08,'CONFOUNDED':0.}[name],
            'fake_same_signature_artifact_alpha':.08 if name=='CONFOUNDED' else 0.,
            'raw_records':len(rows), 'fit':res['fits'],'points':res['estimates']}
    (root/'results'/'numerical_summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    # Per-distance analytic curves for plotting and independent audit
    curves=[]
    for i in range(230):
        d=.25+i*(1.65-.25)/229
        curves.append({'distance_m':d,'newton_m_s2':common_amplitude(rig,d),
                       'Yukawa_alpha1_m_s2':yukawa_amplitude_per_alpha(rig,d,LAM_DEFAULT)})
    save_rows(root/'data'/'THEORY_DISTANCE_CURVE.csv',curves)
    return result
