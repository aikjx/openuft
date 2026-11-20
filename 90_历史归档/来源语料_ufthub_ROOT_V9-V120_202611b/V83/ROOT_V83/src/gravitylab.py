"""ROOT V83: reproducible SI-unit educational gravitational experiment simulator.
NOT hardware controls. Every observation generated here is synthetic.
"""
from __future__ import annotations
import csv, json, math, random, statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

G = 6.67430e-11   # m^3 kg^-1 s^-2 (CODATA 2022 reference)
G_U = 1.5e-15     # absolute standard uncertainty
C = 299_792_458.0
MU0 = 1.25663706127e-6  # H/m, 2022 approximate, not exact post-2019
G_EARTH = 9.80665 # conventional reference acceleration, NOT local measured g

@dataclass(frozen=True)
class Rig:
    mass_kg: float = 100.
    distance_m: float = 0.5
    baseline_m: float = 0.2
    source_radius_m: float = 0.2
    def validate(self):
        if not (self.mass_kg > 0 and self.distance_m > 0 and self.baseline_m > 0 and self.source_radius_m > 0):
            raise ValueError('geometry and mass must be strictly positive')
        if self.distance_m - self.baseline_m / 2 <= self.source_radius_m:
            raise ValueError('sensor would be inside source sphere; external point-mass model invalid')


def acceleration_x(sensor_x_m: float, source_x_m: float, mass_kg: float) -> float:
    if mass_kg < 0: raise ValueError('negative mass not supported')
    d = source_x_m - sensor_x_m
    if d == 0: raise ValueError('source and sensor coincide')
    return G * mass_kg * d / abs(d)**3


def source_observables(r: Rig, side: int):
    r.validate()
    if side not in (-1, 1): raise ValueError('side must be ±1')
    h = r.baseline_m/2
    left = acceleration_x(-h, side*r.distance_m, r.mass_kg)
    right = acceleration_x(h, side*r.distance_m, r.mass_kg)
    return {'left':left, 'right':right, 'common':(left+right)/2,
            'gradient':(right-left)/r.baseline_m}


def theoretical_signals(r: Rig):
    r.validate()
    a = r.distance_m-r.baseline_m/2
    b = r.distance_m+r.baseline_m/2
    amplitude = G*r.mass_kg*(a**-2+b**-2)/2
    gradient = G*r.mass_kg*(a**-2-b**-2)/r.baseline_m
    return {'common_odd_amplitude':amplitude,
            'common_plus_minus_change':2*amplitude,
            'gradient_even':gradient}


def uncertainty_budget(r: Rig, sigma_mass_kg=0.05, sigma_distance_m=0.001,
                       sigma_baseline_m=0.0002, sigma_tilt_rad=2e-10):
    """First-order independent RSS uncertainties, example assumptions, not instrument characterization."""
    r.validate()
    d=r.distance_m; h=r.baseline_m/2; m=r.mass_kg
    aa=(d-h)**-2; bb=(d+h)**-2
    A=G*m*(aa+bb)/2
    dM=A/m
    dd=-G*m*((d-h)**-3+(d+h)**-3)
    db=G*m*((d-h)**-3-(d+h)**-3) # derivative wrt half-baseline
    terms={'mass_kg':dM*sigma_mass_kg,'distance_m':dd*sigma_distance_m,
           'baseline_m':db*sigma_baseline_m/2,
           'G_reference':A*(G_U/G), 'tilt_projection':G_EARTH*sigma_tilt_rad}
    return {'terms_m_s2':terms,'rss_m_s2':math.sqrt(sum(x*x for x in terms.values())),
            'relative':math.sqrt(sum(x*x for x in terms.values()))/A}


def field_energy_joule(B_tesla:float, volume_m3:float):
    if B_tesla<0 or volume_m3<=0: raise ValueError('B magnitude nonnegative, volume positive')
    return B_tesla**2*volume_m3/(2*MU0)


def energy_mass_kg(energy_joule:float): return energy_joule/C**2


def point_mass_gravity_at_distance(mass_kg:float,distance_m:float):
    if distance_m<=0: raise ValueError('distance must be positive')
    return G*mass_kg/distance_m**2


def abba_sides(blocks=128, seed=8301):
    rng=random.Random(seed)
    rows=[]
    for k in range(blocks):
        f=rng.choice([-1,1])
        rows += [f,-f,-f,f]
    return rows


def generate_mass_run(r:Rig, blocks:int, seed:int, has_mass:bool,
                      noise_sigma=8e-9, actuator_artifact=4.0e-9,
                      linear_drift_total=1e-8, tilt_sigma_rad=8e-11):
    """All values are simulation only. 'dummy' applies actuator artifact but no moving gravity source."""
    r.validate()
    rng=random.Random(seed)
    sides=abba_sides(blocks, seed+12345)
    n=len(sides)
    data=[]
    for i,side in enumerate(sides):
        expected=source_observables(r,side) if has_mass else {'left':0.,'right':0.,'common':0.,'gradient':0.}
        dr=linear_drift_total*(i/(n-1)-.5)
        tilt=rng.gauss(0,tilt_sigma_rad)
        common_noise=rng.gauss(0, noise_sigma*.3)
        left=expected['left']+side*actuator_artifact+dr+G_EARTH*tilt+common_noise+rng.gauss(0,noise_sigma)
        right=expected['right']+side*actuator_artifact+dr+G_EARTH*tilt+common_noise+rng.gauss(0,noise_sigma)
        data.append({'index':i,'block':i//4,'side':side,'left_m_s2':left,'right_m_s2':right,
                     'common_m_s2':(left+right)/2,'gradient_s2':(right-left)/r.baseline_m,
                     'truth_mass_present':int(has_mass), 'provenance':'SYNTHETIC_NOT_OBSERVED'})
    return data


def estimate_odd_abba(records:list[dict], key='common_m_s2'):
    """Blockwise lock-in cancels each block's constant and linear-in-time background."""
    if not records or len(records)%4: raise ValueError('ABBA blocks of exactly 4 required')
    vals=[]
    for k in range(0,len(records),4):
        block=records[k:k+4]
        sides=[int(row['side']) for row in block]
        if sides not in ([1,-1,-1,1],[-1,1,1,-1]):
            raise ValueError('invalid ABBA/BAAB block order')
        vals.append(sum(int(row['side'])*float(row[key]) for row in block)/4)
    mean=statistics.mean(vals)
    se=statistics.stdev(vals)/math.sqrt(len(vals)) if len(vals)>1 else float('nan')
    return {'amplitude':mean,'standard_error':se,'blocks':len(vals), 'block_estimates':vals}


def estimate_even_gradient(records:list[dict]):
    vals=[sum(float(z['gradient_s2']) for z in records[i:i+4])/4 for i in range(0,len(records),4)]
    return {'gradient_mean_s2':statistics.mean(vals),
            'gradient_se_s2':statistics.stdev(vals)/math.sqrt(len(vals)) if len(vals)>1 else float('nan')}


def compare_mass_dummy(mass_records, dummy_records):
    m=estimate_odd_abba(mass_records); d=estimate_odd_abba(dummy_records)
    signal=m['amplitude']-d['amplitude']
    se=math.hypot(m['standard_error'],d['standard_error'])
    return {'mass_amplitude':m['amplitude'],'dummy_amplitude':d['amplitude'],
            'adjusted_amplitude':signal,'standard_error':se,'statistical_z':signal/se,
            'note':'synthetic result; z is conditional on specified simulation, not experimental evidence'}


def generate_em_run(blocks=128, seed=83, B_tesla=.1, volume_m3=.001,
                    net_energy_injected=False, sensor_distance_m=.2,
                    artifact=2.5e-9, noise_sigma=3e-9,
                    has_em_artifact=True):
    sides=abba_sides(blocks,seed+100)
    rng=random.Random(seed)
    g=point_mass_gravity_at_distance(energy_mass_kg(field_energy_joule(B_tesla,volume_m3)),sensor_distance_m)
    data=[]; n=len(sides)
    for i,s in enumerate(sides):
        # Side states are conceptual on/off contrast; s=+1 means 'on' / s=-1 means off.
        true_odd=(g/2 if net_energy_injected else 0.)*s
        common_art=(artifact*s if has_em_artifact else 0.)
        reading=true_odd+common_art+2e-9*(i/(n-1)-.5)+rng.gauss(0,noise_sigma)
        data.append({'index':i,'block':i//4,'side':s,'signal_m_s2':reading,
                     'predicted_net_added_gravity_m_s2':g if net_energy_injected else 0.,
                     'energy_accounting':'net_added' if net_energy_injected else 'internal_transfer',
                     'provenance':'SYNTHETIC_NOT_OBSERVED'})
    return data


def save_csv(path, rows):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    with open(path,'w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def generate_all(root:Path):
    root=Path(root)
    r=Rig()
    mass=generate_mass_run(r,128,83011,True)
    dummy=generate_mass_run(r,128,83022,False)
    em=generate_em_run(seed=83033,has_em_artifact=True)
    emdummy=generate_em_run(seed=83044,has_em_artifact=True)
    for name,rows in [('source_mass_SYNTHETIC.csv',mass),('dummy_motion_SYNTHETIC.csv',dummy),
                      ('em_switch_SYNTHETIC.csv',em),('em_dummy_SYNTHETIC.csv',emdummy)]:
        save_csv(root/'data'/name,rows)
    baseline=theoretical_signals(r)
    est=compare_mass_dummy(mass,dummy)
    even=estimate_even_gradient(mass)
    em_est=estimate_odd_abba(em,'signal_m_s2'); em_dummy=estimate_odd_abba(emdummy,'signal_m_s2')
    em_delta=em_est['amplitude']-em_dummy['amplitude']
    em_delta_se=math.hypot(em_est['standard_error'],em_dummy['standard_error'])
    energy=field_energy_joule(.1,.001)
    result={'version':'ROOT V83','data_provenance':'SYNTHETIC_NOT_OBSERVED',
            'rig':r.__dict__, 'theory':baseline,'uncertainty_assumptions':uncertainty_budget(r),
            'synthetic_mass_estimate':{k:v for k,v in est.items() if k!='block_estimates'},
            'synthetic_gradient_estimate':even,
            'electromagnetic':{'B_T':.1,'volume_m3':.001,'energy_J':energy,
                               'mass_equivalent_kg':energy_mass_kg(energy),
                               'monopole_delta_g_if_net_added_m_s2':point_mass_gravity_at_distance(energy_mass_kg(energy),.2),
                               'monopole_delta_g_if_only_internal_transfer_m_s2':0.,
                               'em_on_artifact_estimated_odd_m_s2':em_est['amplitude'],
                               'dummy_artifact_estimated_odd_m_s2':em_dummy['amplitude'],
                               'em_minus_dummy_odd_m_s2':em_delta,
                               'em_minus_dummy_standard_error_m_s2':em_delta_se,
                               'caution':'EM on/off at finite distance may redistribute multipoles; do not interpret zero monopole as zero local gravitational effect'},
            'is_hardware_control':False}
    (root/'results').mkdir(exist_ok=True,parents=True)
    (root/'results'/'numeric_summary.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    return result
