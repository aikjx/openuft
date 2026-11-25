"""ROOT V137: exact model identities, nuisance degeneracy, covariance-aware tests.

NOTICE: all generated cases in this module are SYNTHETIC, not measurements.
Astronomical lengths/gravitational accelerations are in SI. Theoretical
manuscript convention is c=1 with G and hbar independent/dimensional.
Dependencies: Python standard library only.
"""
from __future__ import annotations
import math
import pathlib
import random
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'legacy'/'ROOT_V136_Unification_Research'/'src'))
import v136_physics as v136
old = v136.old


def unit_shape(r, layers, lam=old.ROOT_LAMBDA):
    """Exact external Yukawa gY/gN per unit alpha, sphere of shells."""
    return old.yukawa_accel_ratio(r, layers, alpha=1.0, lam=lam)


def gravity(r, mu, layers, alpha=old.ROOT_ALPHA, lam=old.ROOT_LAMBDA):
    if r < old.check_shells(layers) or mu <= 0 or not math.isfinite(mu):
        raise ValueError('outside sphere and positive GM required')
    return mu/r**2 * (1+alpha*unit_shape(r,layers,lam))


def fitted_mu_at_anchor(anchor_r, mu, layers, alpha=old.ROOT_ALPHA, lam=old.ROOT_LAMBDA):
    """Newton-model estimated GM from g(anchor)*anchor^2 for a Yukawa world."""
    return gravity(anchor_r,mu,layers,alpha,lam) * anchor_r**2


def residual_after_mu_fit(r, anchor_r, layers, alpha=old.ROOT_ALPHA, lam=old.ROOT_LAMBDA):
    """(measured g - Newton g with fit GM)/Newton fit g, exact identity."""
    if r < old.check_shells(layers) or anchor_r < old.check_shells(layers):
        raise ValueError('exterior radii required')
    return (alpha*(unit_shape(r,layers,lam)-unit_shape(anchor_r,layers,lam)) /
            (1+alpha*unit_shape(anchor_r,layers,lam)))


def three_shape_direct(radii, layers, alpha=old.ROOT_ALPHA, lam=old.ROOT_LAMBDA):
    if len(radii)!=3: raise ValueError('need 3 radii')
    if alpha==0: raise ValueError('undefined ratio in strict null model')
    return v136.three_altitude_shape_ratio(*radii,layers=layers,alpha=alpha,lam=lam)


def cholesky(a):
    n=len(a)
    if not n or any(len(row)!=n for row in a):raise ValueError('square covariance')
    L=[[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1):
            s=sum(L[i][k]*L[j][k] for k in range(j))
            if i==j:
                x=a[i][i]-s
                if not math.isfinite(x) or x<=0:raise ValueError('covariance not positive definite')
                L[i][j]=math.sqrt(x)
            else: L[i][j]=(a[i][j]-s)/L[j][j]
    return L


def solve_lower(L, b):
    return _lower(L, b)


def _lower(L,b):
    x=[]
    for i in range(len(L)):
        x.append((b[i]-sum(L[i][j]*x[j] for j in range(i)))/L[i][i])
    return x


def linear_solve(a,b):
    n=len(b)
    M=[list(a[i])+[b[i]] for i in range(n)]
    for k in range(n):
        p=max(range(k,n),key=lambda i:abs(M[i][k]))
        if abs(M[p][k])<1e-12:raise ValueError('rank deficient; cannot identify couplings')
        M[k],M[p]=M[p],M[k]
        piv=M[k][k]
        for j in range(k,n+1):M[k][j]/=piv
        for i in range(n):
            if i==k:continue
            s=M[i][k]
            for j in range(k,n+1):M[i][j]-=s*M[k][j]
    return [M[i][-1] for i in range(n)]


def correlated_cov(sigmas,correlation=0.3):
    if not -1/(len(sigmas)-1) < correlation <1:raise ValueError('invalid equicorrelation')
    if any(s<=0 or not math.isfinite(s) for s in sigmas):raise ValueError('positive errors')
    return [[si*sj*(1 if i==j else correlation) for j,sj in enumerate(sigmas)]
            for i,si in enumerate(sigmas)]


def gls_fit(design,y,cov):
    """Covariance-aware generalized least squares, full rank, no third parties.

    Fits column-scaled, whitened regression. Returns estimates and covariance
    from the declared covariance (not posterior empirical residual uncertainty).
    """
    n=len(y)
    if n<2 or len(design)!=n or len(cov)!=n:raise ValueError('bad dimensions')
    k=len(design[0])
    if not k or n<k+1 or any(len(row)!=k for row in design):
        raise ValueError('need residual dof and rectangular design')
    L=cholesky(cov)
    yw=_lower(L,list(y))
    Xw=[_lower(L,[design[i][j] for i in range(n)]) for j in range(k)]
    scales=[math.sqrt(sum(z*z for z in col)) for col in Xw]
    if any(v==0 for v in scales):raise ValueError('zero design column')
    xn=[[z/s for z in col] for col,s in zip(Xw,scales)]
    gram=[[sum(a*b for a,b in zip(xn[i],xn[j])) for j in range(k)] for i in range(k)]
    target=[sum(a*b for a,b in zip(xn[j],yw)) for j in range(k)]
    q=linear_solve(gram,target)
    coefs=[q[j]/scales[j] for j in range(k)]
    inv=[[linear_solve(gram,[1.0 if i==j else 0.0 for i in range(k)])[p]
          for j in range(k)] for p in range(k)]
    covariance=[[inv[i][j]/scales[i]/scales[j] for j in range(k)] for i in range(k)]
    res=[yw[i]-sum(coefs[j]*Xw[j][i] for j in range(k)) for i in range(n)]
    return {'beta':coefs,'covariance':covariance,'standard_errors':
            [math.sqrt(covariance[j][j]) for j in range(k)],
            'chi2':sum(e*e for e in res),'dof':n-k}


def design_heights(heights,layers=old.EARTH_LAYERS,lam=old.ROOT_LAMBDA,
                   include_nuisance=True):
    """Toy nuisance ~ (R/r)^2 radial shape, NOT a full J2 Earth model."""
    R=old.check_shells(layers)
    return [[1.,unit_shape(R+h,layers,lam)] + ([(R/(R+h))**2] if include_nuisance else [])
            for h in heights]


def simulate(heights,coeffs,sigma=2e-6,correlation=0.25,seed=137,
             layers=old.EARTH_LAYERS,lam=old.ROOT_LAMBDA):
    X=design_heights(heights,layers,lam,len(coeffs)==3)
    if len(coeffs) not in (2,3):raise ValueError('2 or 3 coeffs')
    covariance=correlated_cov([sigma]*len(X),correlation)
    L=cholesky(covariance)
    random_gen=random.Random(seed)
    z=[random_gen.gauss(0,1) for _ in heights]
    noise=[sum(L[i][j]*z[j] for j in range(i+1)) for i in range(len(X))]
    obs=[sum(a*b for a,b in zip(row,coeffs))+e for row,e in zip(X,noise)]
    return X,obs,covariance


def monte_carlo_coverage(heights,coeffs,n=200,seed=3701):
    rng=random.Random(seed)
    covers=0
    estimates=[]
    for _ in range(n):
        X,y,C=simulate(heights,coeffs,seed=rng.randrange(1,2**31-1))
        res=gls_fit(X,y,C)
        a=res['beta'][1]
        estimates.append(a)
        covers+=abs(a-coeffs[1])<=1.96*res['standard_errors'][1]
    return {'n':n,'coverage':covers/n,'mean_alpha':sum(estimates)/n,
            'min_alpha':min(estimates),'max_alpha':max(estimates)}


def noisy_three_altitude(heights,alpha,relative_noise=1e-7,trials=1000,seed=137):
    """Naive 3-height ratio with multiplicative errors in A=r²g; null breaks."""
    if len(heights)!=3:raise ValueError('three heights required')
    R=old.check_shells(old.EARTH_LAYERS)
    r=[R+h for h in heights]
    q=three_shape_direct(r,old.EARTH_LAYERS,alpha=1)
    true=[1+alpha*unit_shape(x,old.EARTH_LAYERS) for x in r]
    rng=random.Random(seed)
    vals=[]
    for _ in range(trials):
        z=[a*(1+rng.gauss(0,relative_noise)) for a in true]
        den=z[1]-z[2]
        if den:vals.append((z[0]-z[1])/den)
    ordered=sorted(abs(x-q) for x in vals if math.isfinite(x))
    return {'expected_q_for_nonzero_alpha':q,'alpha':alpha,
            'trials':trials,'median_abs_error':ordered[len(ordered)//2],
            'p95_abs_error':ordered[int(len(ordered)*.95)],
            'negative_ratio_share':sum(x<0 for x in vals)/len(vals)}


def helix_kinematics(a,omega,u):
    return v136.helix_geometry(a,omega,u)


def surface_diagnostic(layers,mu,heights=(0,200e3,400e3,800e3,1600e3)):
    R=old.check_shells(layers)
    anchor=R+heights[-1]
    rows=[]
    for h in heights:
        r=R+h
        rows.append({'height_m':h,'g_newton_m_s2':mu/r**2,
                     'delta_g_yukawa_m_s2':mu/r**2*old.ROOT_ALPHA*unit_shape(r,layers),
                     'root_to_newton_ratio':old.ROOT_ALPHA*unit_shape(r,layers),
                     'fractional_after_high_anchor':residual_after_mu_fit(r,anchor,layers)})
    return rows
