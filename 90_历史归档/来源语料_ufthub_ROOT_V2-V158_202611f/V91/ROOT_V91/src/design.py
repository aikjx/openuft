import numpy as np
from itertools import combinations

def fisher(y_template, background, covariance, tol=1e-11):
    q=np.asarray(y_template,float).reshape(-1)
    B=np.asarray(background,float)
    S=np.asarray(covariance,float)
    if B.ndim==1: B=B[:,None]
    n=q.size
    if B.shape[0]!=n or S.shape!=(n,n) or not np.allclose(S,S.T,atol=1e-12,rtol=1e-10): raise ValueError('dimension or symmetry')
    L=np.linalg.cholesky(S)
    qw=np.linalg.solve(L,q); Bw=np.linalg.solve(L,B)
    u,s,_=np.linalg.svd(Bw,full_matrices=False)
    rank=int(np.sum(s>tol*s[0])) if len(s) and s[0]>0 else 0
    residual=qw-u[:,:rank]@(u[:,:rank].T@qw)
    information=float(residual@residual)
    return {'information':information,'sigma_amplitude':float(1/np.sqrt(information)) if information>1e-25 else float('inf'),'rank_background':rank,'relative_residual':float(np.linalg.norm(residual)/np.linalg.norm(qw)) if np.linalg.norm(qw)>0 else 0.0}

def templates(r,delta):
    r=np.asarray(r,float)
    if np.any(r<=0) or delta<=0: raise ValueError('positive distances')
    def diff(n): return r**(-n)-2*(r+delta)**(-n)+(r+2*delta)**(-n)
    return np.stack([diff(1),diff(2),diff(3)],axis=1)

def design_search(grid,delta,n_points=5,noise=1e-5,extra_background=False):
    grid=np.asarray(grid,float)
    best=None
    for inds in combinations(range(len(grid)),n_points):
        r=grid[list(inds)]
        T=templates(r,delta)
        # scale columns to avoid artificial numerical rank loss
        T=T/np.linalg.norm(T,axis=0)
        B=T[:,:2]
        if extra_background: B=np.column_stack([B,T[:,2]])
        fit=fisher(T[:,2],B,np.eye(n_points)*noise**2)
        if best is None or fit['information']>best['information']:
            best={'radii_m':r.tolist(),**fit}
    return best
