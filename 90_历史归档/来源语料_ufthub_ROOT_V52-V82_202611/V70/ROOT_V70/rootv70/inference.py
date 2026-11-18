"""Identifiability demonstrations on SYNTHETIC, arbitrary surrogate charges.
Not measured data and not a calibrated physical exclusion model.
"""
from __future__ import annotations
import numpy as np
from .physics import BODIES,MATERIAL_TOY,field_at,yukawa_shape

def feature_row(body_name:str,mat_a:str,mat_b:str,lat:float,alt:float,lam:float=1.0e7)->np.ndarray:
    body=BODIES[body_name]; dQ=MATERIAL_TOY[mat_a]-MATERIAL_TOY[mat_b]
    f=field_at(body,lat,alt)
    k_ref=field_at(BODIES['Earth'],0.,0.)['kretschmann']
    # 3 phenomenological features: Yukawa-source dependence, curvature,
    # and rotating-frame amplitude. None represents a derived new theory.
    xs=[dQ*body.source_charge_toy*yukawa_shape(f['radius'],lam),
        dQ*f['kretschmann']/k_ref,
        dQ*body.omega**2*body.radius*np.cos(np.deg2rad(lat))**2/(body.mu/body.radius**2)]
    return np.asarray(xs,float)

def fixed_earth_design()->np.ndarray:
    return np.asarray([feature_row('Earth',a,b,0,0) for a,b in
                       [('Ti','Pt'),('Al','Pt'),('SiO2','Fe'),('Ti','Fe')]])

def multi_body_design()->tuple[np.ndarray,list]:
    x=[];labels=[]
    for body in BODIES:
        for lat in (0,30,60):
            for height_fraction in (0.,0.08):
                for a,b in [('Ti','Pt'),('Al','Pt'),('SiO2','Fe')]:
                    x.append(feature_row(body,a,b,lat,BODIES[body].radius*height_fraction))
                    labels.append((body,lat,height_fraction,a,b))
    return np.asarray(x), labels

def rank_report(x)->dict:
    x=np.asarray(x,float)
    s=np.linalg.svd(x,compute_uv=False)
    tol=max(x.shape)*np.finfo(float).eps*s[0]
    rank=int(sum(s>tol))
    return {'n':int(len(x)),'columns':int(x.shape[1]),'rank':rank,
            'singular_values':[float(i) for i in s],
            'condition':float(s[0]/s[-1]) if s[-1]>0 else float('inf')}

def synthetic_fit(seed:int=20261117, sigma:float=2e-16)->dict:
    x,labels=multi_body_design()
    # Hypothetical coefficients. NOT inferred from any observations.
    theta=np.array([.50e-15,-.30e-15,.20e-15])
    rng=np.random.default_rng(seed)
    y=x@theta+rng.normal(0,sigma,len(x))
    # scale parameters in 1e-15 units for conditioning/readability
    fit_units=np.linalg.lstsq(x,y/1e-15,rcond=None)[0]
    fit=fit_units*1e-15
    cov=(sigma**2)*np.linalg.inv(x.T@x)
    return {'seed':seed,'noise_sigma':sigma,'truth':theta.tolist(),
            'estimate':fit.tolist(), 'standard_error':np.sqrt(np.diag(cov)).tolist(),
            'design':rank_report(x), 'rms_residual':float(np.sqrt(np.mean((y-x@fit)**2))),
            'measurements_synthetic':len(y)}
