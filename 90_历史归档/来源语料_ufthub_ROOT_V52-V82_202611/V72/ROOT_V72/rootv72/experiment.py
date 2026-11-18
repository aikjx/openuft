"""Four-state difference-in-differences. Every trial here is synthetic."""
from dataclasses import dataclass,asdict
from math import erfc,sqrt
import numpy as np
@dataclass
class Fit:
    beta:float
    nuisance_hs:float
    se:float
    z:float
    p_two_sided:float
    rank:int
    condition:float

def contrast(pp,pm,mp,mm):return (pp-pm-mp+mm)/4

def generate(seed=72,beta=3e-15,nuisance=-5e-16,noise=1.2e-15,repeats=24):
    """x=q*cos(angle), with synthetic 'material contrast' q and physical angle.
    h,s are binary reversals; a term proportional to hs survives the contrast.
    """
    rng=np.random.default_rng(seed)
    result=[]
    i=0
    for q in [0.0,.4,.9]:
        for c in [-.95,-.4,.4,.95]:
            x=q*c
            for repeat in range(repeats):
                vals={}
                for h in [1,-1]:
                    for s in [1,-1]:
                        # common background, independent h-only and s-only systematics
                        y=2.5e-11+h*1.1e-13+s*(-2.7e-13)+h*s*(nuisance+beta*x)+rng.normal(0,noise)
                        vals[(h,s)]=y
                d=contrast(vals[(1,1)],vals[(1,-1)],vals[(-1,1)],vals[(-1,-1)])
                result.append(dict(row=i,q_synthetic=q,cos_angle=c,x=x,repeat=repeat,
                   ypp=vals[(1,1)],ypm=vals[(1,-1)],ymp=vals[(-1,1)],ymm=vals[(-1,-1)],contrast=d))
                i+=1
    return result

def fit(rows,noise=1.2e-15):
    x=np.asarray([v['x'] for v in rows],float)
    y=np.asarray([v['contrast'] for v in rows],float)
    mat=np.column_stack([np.ones(len(x)),x])
    rank=int(np.linalg.matrix_rank(mat))
    if rank<2:raise ValueError('feature not identifiable: rank deficient')
    coeff=np.linalg.lstsq(mat,y,rcond=None)[0]
    # independent known per-state gaussian noise sigma; contrast noise = sigma/2
    se=noise/2/np.sqrt(np.sum((x-x.mean())**2))
    z=float(coeff[1]/se)
    return Fit(float(coeff[1]),float(coeff[0]),float(se),z,float(erfc(abs(z)/sqrt(2))),rank,float(np.linalg.cond(mat)))

def fisher_information(rows,noise=1.2e-15):
    xs=np.asarray([v['x'] for v in rows]);return float(np.sum((xs-xs.mean())**2)/(noise/2)**2)

def four_state_drift_quadratic(amplitude=1e-15):
    # (h,s) order (++,+-,-+,--), times t=0,1,2,3; quadratic drift leaks into hs channel
    ts=np.arange(4,dtype=float)
    return contrast(*(amplitude*ts**2))

def null_false_positive_trial_count(n_trials=120,noise=1.2e-15):
    count=0
    for seed in range(300,300+n_trials):
        f=fit(generate(seed=seed,beta=0,noise=noise,repeats=4),noise=noise)
        if abs(f.z)>1.96:count+=1
    return count
