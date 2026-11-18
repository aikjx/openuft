"""Synthetic identifiability exercise, NOT real data or a force detection."""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product
import numpy as np
from .physics import uniform_ratio, layered_ratio, same_mass_layered_shells, homogeneous_shells

# Rounded values from previous V70 reference, for experiment DESIGN illustration only.
BODIES = {
    'Earth': (6_378_137., 3.986004418e14, .42),
    'Moon': (1_737_500., 4.87e12, .28),
    'Mars': (3_396_000., 4.2828e13, .31),
    'Jupiter': (71_492_000., 1.2669e17, .15),
}
MATERIALS = {'Ti':.20,'Pt':.72,'Al':.37,'SiO2':.29,'Fe':.48}


def feature_row(body:str, pair:tuple[str,str], altitude_ratio:float, sidereal_phase:float):
    """Three distinct signatures: finite-source short/long range, angular modulation.
    Each is multiplied by completely synthetic composition contrast and source charge.
    """
    R, mu, source_q=BODIES[body]
    dq=MATERIALS[pair[0]]-MATERIALS[pair[1]]
    h=R*altitude_ratio
    short = dq*source_q*uniform_ratio(R,h,2.0e6,alpha=1.)
    long = dq*source_q*uniform_ratio(R,h,40.0e6,alpha=1.)
    # Hypothetical preferred-frame signature, not a consequence of GR or ROOT.
    sidereal=dq*np.cos(sidereal_phase)*(.7+.3*np.sin(sidereal_phase))
    return np.array([short,long,sidereal],float)


def fixed_design():
    return np.array([feature_row('Earth',(a,'Pt'),0.,0.)
                     for a in ('Ti','Al','SiO2','Fe')])


def mixed_design():
    pairs=[('Ti','Pt'),('Al','Pt'),('Fe','Pt'),('SiO2','Pt')]
    rows=[]; meta=[]
    for body,pair,hfrac,phase in product(BODIES,pairs,(0.,.02,.4),(0.,np.pi/3,np.pi,5*np.pi/3)):
        rows.append(feature_row(body,pair,hfrac,phase))
        meta.append((body,'-'.join(pair),hfrac,phase))
    return np.asarray(rows),meta


def design_diagnostics(X):
    X=np.asarray(X,float)
    if X.ndim!=2:raise ValueError('2-D matrix needed')
    # Column normalization makes rank and conditioning independent of units.
    scales=np.max(np.abs(X),axis=0)
    scales=np.where(scales==0,1.,scales)
    Xn=X/scales
    singular=np.linalg.svd(Xn,compute_uv=False)
    rank=np.linalg.matrix_rank(Xn,tol=max(Xn.shape)*np.finfo(float).eps*singular[0])
    condition=float(singular[0]/singular[-1]) if singular[-1]>0 else float('inf')
    return {'rank':int(rank),'columns':int(X.shape[1]),'n':int(X.shape[0]),
            'svals_normalized':singular.tolist(),'condition_normalized':condition,'column_scales':scales.tolist()}


def fit_synthetic(X,seed=20261117,sigma=2e-16):
    """Artificial signal in dimensionless Eotvos-like units; never observational data."""
    if sigma<=0:raise ValueError('sigma must be positive')
    X=np.asarray(X,float)
    truth=np.array([8e-16,-5e-16,3e-16])
    rng=np.random.default_rng(seed)
    y=X@truth+rng.normal(0,sigma,size=X.shape[0])
    theta,*_=np.linalg.lstsq(X,y,rcond=None)
    # The covariance uses known synthetic Gaussian noise sigma and full-rank design.
    covariance=sigma**2*np.linalg.pinv(X.T@X)
    stderr=np.sqrt(np.diag(covariance))
    return {'seed':seed,'sigma':sigma,'truth':truth.tolist(),
            'fitted':theta.tolist(),'stderr_known_sigma':stderr.tolist(),
            'rms_residual':float(np.sqrt(np.mean((y-X@theta)**2))),
            'observations_synthetic':int(len(y))}
