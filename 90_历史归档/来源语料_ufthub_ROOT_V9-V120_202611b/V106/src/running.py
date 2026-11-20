"""One-loop minimal SM coupling flow with SU(5)-normalized hypercharge.
All benchmark inputs are illustrative MSbar numbers, not new measurements.
No thresholds, two-loop terms, Planck-scale claims or fitted BSM spectra.
"""
from dataclasses import dataclass
import math
import numpy as np

B = np.array([41/10, -19/6, -7.0], dtype=float)

@dataclass(frozen=True)
class Benchmark:
    m_z_gev: float=91.1876
    alpha_em_inv: float=127.930
    sin2_theta: float=.23122
    alpha_s: float=.1180

    def validate(self):
        if min(self.m_z_gev,self.alpha_em_inv,self.alpha_s)<=0 or not(0<self.sin2_theta<1):
            raise ValueError('invalid benchmark inputs')

    def inv_couplings(self):
        self.validate()
        ai=self.alpha_em_inv; ss=self.sin2_theta
        return np.array([3/5*(1-ss)*ai, ss*ai, 1/self.alpha_s])


def inverse_at(t, bench=Benchmark()):
    """t=log(mu/MZ)."""
    return bench.inv_couplings() - B*(t/(2*math.pi))


def intersection(i,j,bench=Benchmark()):
    if not 0<=i<3 or not 0<=j<3 or i==j: raise ValueError('use distinct indices 0,1,2')
    v=bench.inv_couplings()
    t=2*math.pi*(v[i]-v[j])/(B[i]-B[j])
    return {'log_mu_over_mz':t,'mu_gev':bench.m_z_gev*math.exp(t), 'inv_at_scale':inverse_at(t,bench).tolist()}


def invariant(bench=Benchmark()):
    """I is exactly independent of scale at 1loop with these fixed beta coefficients.
    I=0 iff three lines intersect at one point, since all beta coefficients distinct.
    """
    a=bench.inv_couplings()
    return float((B[1]-B[2])*a[0]+(B[2]-B[0])*a[1]+(B[0]-B[1])*a[2])


def optimal_spread(bench=Benchmark()):
    a=bench.inv_couplings(); slope=B/(2*math.pi)
    ac=a-a.mean(); sc=slope-slope.mean()
    t=float(np.dot(ac,sc)/np.dot(sc,sc))
    af=inverse_at(t,bench)
    return {'t':t,'mu_gev':bench.m_z_gev*math.exp(t),'inverse':af.tolist(),
            'standard_deviation':float(np.std(af)),'range':float(np.ptp(af))}


def benchmark_scan(n=1001, seed=106):
    """Toy input-variation exercise (not complete uncertainty/theory-error model)."""
    if n<1: raise ValueError('n must be positive')
    rng=np.random.default_rng(seed)
    alphas=rng.normal(.1180,.0009,n)
    sin2=rng.normal(.23122,.00005,n)
    em=rng.normal(127.930,.008,n)
    vals=np.array([invariant(Benchmark(alpha_em_inv=float(e), sin2_theta=float(s), alpha_s=float(a)))
                   for e,s,a in zip(em,sin2,alphas)])
    return {'n':n,'seed':seed,'quantiles_2_50_98':np.quantile(vals,[.02,.5,.98]).tolist(),
            'all_negative':bool(np.all(vals<0)), 'mean':float(vals.mean())}
