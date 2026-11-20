"""Correlated-noise generalized least squares, identifiability, rank-one bootstrap.
Synthetic toy inference, no real astrophysical measurements.
"""
import numpy as np
from scipy.linalg import solve_triangular
from scipy.optimize import least_squares

def gls_fit(X, y, cov):
    X=np.asarray(X,float);y=np.asarray(y,float);cov=np.asarray(cov,float)
    L=np.linalg.cholesky(cov)
    A=solve_triangular(L,X,lower=True)
    b=solve_triangular(L,y,lower=True)
    U,s,Vt=np.linalg.svd(A,full_matrices=False)
    cutoff=max(A.shape)*np.finfo(float).eps*s[0]
    rank=int(sum(s>cutoff))
    coef=np.linalg.lstsq(A,b,rcond=None)[0]
    chi2=float(np.sum((A@coef-b)**2))
    covariance=np.linalg.pinv(A.T@A)
    cond=float(s[0]/s[-1]) if s[-1]>0 else float('inf')
    return dict(coef=coef, chi2=chi2, covariance=covariance, rank=rank, condition=cond,
                singular_values=s)

def correlated_cov(n,sigma,rho=.5,common=.4):
    if n<=0 or sigma<=0 or not 0<=rho<1 or common<0:
        raise ValueError('invalid covariance parameters')
    x=np.arange(n)
    return sigma**2*(rho**np.abs(x[:,None]-x[None,:])+common**2)

def fit_shape_profiles(r, g, cov, lengths, radius=0.,j2=0.,theta=np.pi/2):
    """Scan lambda; GLS fits mu and mu*alpha; mass G degeneracy retained.
    Test charge factors set to 1; no discovery claimed.
    """
    from .physics import sphere_envelope, j2_relative
    r=np.asarray(r,float);g=np.asarray(g,float)
    if np.any(r<=0) or len(r)!=len(g): raise ValueError('invalid radial data')
    table=[]
    for length in lengths:
        if length<=0:raise ValueError('range must be positive')
        base=np.array([(1+j2_relative(radius,float(t),j2,theta))/t**2 for t in r])
        yp=np.array([(1+t/length)*sphere_envelope(radius,float(t),length)/t**2 for t in r])
        fit=gls_fit(np.column_stack([base,yp]),g,cov)
        mu,b=fit['coef'];alpha=float(b/mu) if mu!=0 else float('nan')
        table.append(dict(length=float(length),mu=float(mu),alpha=alpha,
                          chi2=fit['chi2'],condition=fit['condition'],
                          singular_values=fit['singular_values'].tolist()))
    return table

def _rankfit(data,cov):
    """Compute rank-one GLS fit with covariance on row-major flattened matrix."""
    obs=np.asarray(data,float)
    m,n=obs.shape
    L=np.linalg.cholesky(cov)
    u,s,vt=np.linalg.svd(obs,full_matrices=False)
    left=u[:,0]*np.sqrt(s[0]);right=vt[0,:]*np.sqrt(s[0])
    def resid(z):
        mat=np.outer(z[:m],z[m:])
        return solve_triangular(L,(mat-obs).reshape(-1),lower=True)
    sol=least_squares(resid,np.r_[left,right],max_nfev=150,ftol=1e-10,xtol=1e-10)
    fit=np.outer(sol.x[:m],sol.x[m:])
    return float(np.dot(sol.fun,sol.fun)),fit

def rank_one_bootstrap(observed,cov,B=120,seed=20261118):
    obs=np.asarray(observed,float)
    if obs.ndim!=2 or min(obs.shape)<2 or B<20:raise ValueError('rank experiment needs 2x2+ and bootstrap >=20')
    if np.shape(cov)!=(obs.size,obs.size):raise ValueError('covariance shape mismatch')
    chisq,fitted=_rankfit(obs,cov)
    rng=np.random.default_rng(seed)
    L=np.linalg.cholesky(cov)
    null=[]
    for _ in range(B):
        mock=fitted+(L@rng.normal(size=obs.size)).reshape(obs.shape)
        test,_=_rankfit(mock,cov)
        null.append(test)
    p=(1+sum(x>=chisq for x in null))/(B+1)
    return {'chi2':chisq,'bootstrap_p':float(p),'null_chi2_median':float(np.median(null)),
            'fitted_rank_one':fitted,'singular_values':np.linalg.svd(obs,compute_uv=False),
            'n_bootstrap':B,'rng_seed':seed}
