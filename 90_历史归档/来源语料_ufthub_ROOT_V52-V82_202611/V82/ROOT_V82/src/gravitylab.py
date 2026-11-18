"""ROOT V82: gravity experiment physics and synthetic data. Simulation only.
All SI. No instrument-control functions. Python standard library.
"""
from __future__ import annotations
import csv
import json
import math
import random
from dataclasses import dataclass
from pathlib import Path

G=6.67430e-11
C=299_792_458.0
MU0=1.25663706127e-6  # CODATA 2022, not exactly 4*pi*1e-7 in revised SI
EPS0=1.0/(MU0*C*C)


def gravity_vector(sensor:tuple[float,float,float], mass:float, source:tuple[float,float,float]):
    """Newton point mass; exact externally for a spherical source mass."""
    if not (mass >= 0 and math.isfinite(mass)):
        raise ValueError('mass must be nonnegative and finite')
    dr=[source[i]-sensor[i] for i in range(3)]
    r2=sum(v*v for v in dr)
    if r2 <= 0:
        raise ValueError('sensor cannot be at source center')
    factor=G*mass/(r2*math.sqrt(r2))
    return tuple(factor*v for v in dr)


def sphere_gravity(mass:float, radius:float, distance:float):
    if mass < 0 or radius <= 0 or distance < 0:
        raise ValueError('invalid sphere')
    # Uniform sphere, interior formula. External shell theorem.
    return G*mass*distance/radius**3 if distance < radius else G*mass/distance**2


def em_energy(E:float=0.,B:float=0.,volume:float=1.):
    if volume <= 0 or not all(map(math.isfinite,(E,B,volume))):
        raise ValueError('invalid EM volume or fields')
    return volume*(EPS0*E**2/2+B**2/(2*MU0))


def mass_equivalent(added_energy_joules:float):
    return added_energy_joules/C**2


def monopole_gravity_bound(added_energy_joules:float,radius:float):
    """Magnitude of far-zone 1/r^2 MONOPOLE estimator, not full stress-gravity."""
    if radius <= 0: raise ValueError('radius positive')
    return G*abs(mass_equivalent(added_energy_joules))/radius**2


def field_energy_change(B1:float,B2:float,volume:float):
    return em_energy(B=B2,volume=volume)-em_energy(B=B1,volume=volume)


def relativistic_frequency_shift(g:float,height:float):
    return g*height/C**2


def rotation_effect(omega:float,radius:float):
    return omega**2*radius


def point_mass_uncertainty(mass:float,distance:float,sigma_mass:float,sigma_distance:float,include_G:bool=False):
    if min(mass,distance)<=0 or min(sigma_mass,sigma_distance)<0: raise ValueError('invalid uncertainty')
    rel2=(sigma_mass/mass)**2+(2*sigma_distance/distance)**2
    if include_G: rel2+=(1.5e-15/G)**2
    return math.sqrt(rel2)


def validate_protocol(p:dict):
    if p.get('version')!='ROOT-GCL/1.0': raise ValueError('version mismatch')
    if p.get('data_provenance')!='synthetic': raise ValueError('simulator requires synthetic provenance')
    if p.get('experiment') not in ('source_mass_reversal','em_energy_audit','dummy_null'):
        raise ValueError('unknown experiment')
    params=p.get('parameters',{})
    required = {'source_mass_reversal':('source_mass_kg','source_distance_m'),
                'em_energy_audit':('magnetic_field_t','volume_m3','observation_distance_m'),
                'dummy_null':()}[p['experiment']]
    for k in required:
        if k not in params or not isinstance(params[k],(int,float)) or not math.isfinite(params[k]) or params[k]<=0:
            raise ValueError('invalid '+k)
    n=p.get('design',{}).get('samples')
    if not isinstance(n,int) or n<8 or n>200_000 or n%4:
        raise ValueError('samples must be divisible by 4, from 8 to 200000')
    sigma=p.get('design',{}).get('noise_sigma_m_s2')
    if not isinstance(sigma,(int,float)) or sigma<=0 or not math.isfinite(sigma):
        raise ValueError('invalid noise sigma')
    if p.get('design',{}).get('randomized_blocks') is not True:
        raise ValueError('randomized blocks mandatory')
    return True


def predict(p:dict):
    validate_protocol(p)
    params=p['parameters']
    exp=p['experiment']
    if exp=='source_mass_reversal':
        A=G*params['source_mass_kg']/params['source_distance_m']**2
        return {'amplitude_m_s2':A,'switch_difference_m_s2':2*A,
                'interpretation':'newtonian source-mass gravity in x direction'}
    if exp=='em_energy_audit':
        u=em_energy(B=params['magnetic_field_t'],volume=params['volume_m3'])
        return {'added_energy_J':u,'mass_equivalent_kg':u/C**2,
                'far_field_monopole_m_s2':monopole_gravity_bound(u,params['observation_distance_m']),
                'interpretation':'far-field illustrative monopole only if NET energy is imported to system; internal redistributions have no mass monopole change'}
    return {'amplitude_m_s2':0.,'interpretation':'null dummy, should return zero modulation'}


def solve_linear(A:list[list[float]],b:list[float]):
    # Pivoted linear solver, for small matrices; singular designs are explicitly rejected.
    n=len(b); a=[list(row)+[b[i]] for i,row in enumerate(A)]
    for k in range(n):
        piv=max(range(k,n),key=lambda j:abs(a[j][k]))
        if abs(a[piv][k]) < 1e-12: raise ValueError('rank deficient design')
        a[k],a[piv]=a[piv],a[k]
        d=a[k][k]
        for j in range(k,n+1): a[k][j]/=d
        for i in range(n):
            if i==k: continue
            fac=a[i][k]
            for j in range(k,n+1): a[i][j]-=fac*a[k][j]
    return [a[i][-1] for i in range(n)]


def fit_switch(rows:list[dict],noise_sigma:float):
    """Fit y= b0 + A*switch + b_t*time via scaled regression."""
    n=len(rows)
    times=[(r['i']-(n-1)/2)/n for r in rows]
    X=[[1.,float(r['switch']),times[i]] for i,r in enumerate(rows)]
    # scale response 1e-8 to avoid very small normal equations.
    scale=1e-8
    Xty=[sum(row[j]*r['measurement_m_s2']/scale for row,r in zip(X,rows)) for j in range(3)]
    XtX=[[sum(row[i]*row[j] for row in X) for j in range(3)] for i in range(3)]
    betas=solve_linear(XtX,Xty)
    # uncertainty of A under an ASSUMED known white sigma.
    basis=solve_linear(XtX,[0.,1.,0.]); stderr=noise_sigma*math.sqrt(basis[1])
    resid=[r['measurement_m_s2']-scale*sum(x*b for x,b in zip(row,betas)) for row,r in zip(X,rows)]
    return {'fitted_amplitude_m_s2':scale*betas[1], 'white_noise_standard_error_m_s2':stderr,
            'z_white_noise_assumption':(scale*betas[1])/stderr,
            'residual_rms_m_s2':math.sqrt(sum(v*v for v in resid)/len(resid))}


def simulate(p:dict):
    """SYNTHETIC data only; reproducible balanced/randomized blocks."""
    validate_protocol(p)
    A=predict(p).get('amplitude_m_s2',0.0)
    if p['experiment']=='em_energy_audit':
        # Explicitly DO NOT inject tiny GR signal as if measurable; this is a null design for identifying nuisance.
        A=0.0
    n=p['design']['samples']; sigma=float(p['design']['noise_sigma_m_s2'])
    seed=int(p['design'].get('seed',2026)); rng=random.Random(seed)
    states=[]
    # balanced randomized four-state blocks, reduces correlation with drift.
    for block in range(n//4):
        b=[1.,1.,-1.,-1.]; rng.shuffle(b); states.extend(b)
    drift=float(p['design'].get('linear_drift_total_m_s2',1e-8))
    magnetic_leak=float(p['design'].get('switch_correlated_artifact_m_s2',0.0))
    rows=[]
    for i,s in enumerate(states):
        y=A*s + drift*(i-(n-1)/2)/n+magnetic_leak*s+rng.gauss(0.,sigma)
        rows.append({'i':i,'block':i//4,'switch':int(s),'measurement_m_s2':y,
                     'provenance':'SYNTHETIC - NOT AN OBSERVATION'})
    result=fit_switch(rows,sigma)
    result.update({'experiment':p['experiment'],'samples':n,'seed':seed,'input_amplitude_m_s2':A,
                   'switch_correlated_artifact_m_s2':magnetic_leak,
                   'status':'synthetic model and software check only; does not establish new gravity'})
    return rows,result


def export_csv(path:str|Path,rows:list[dict]):
    with open(path,'w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)


def structural_degeneracy():
    """y = gravity * state + nuisance * state has rank 1 and is unidentifiable."""
    return {'columns':['candidate_gravity','switch_correlated_artifact'], 'rank':1,
            'conclusion':'perfectly confounded if both columns track the same switch; add independent physics or controls'}
