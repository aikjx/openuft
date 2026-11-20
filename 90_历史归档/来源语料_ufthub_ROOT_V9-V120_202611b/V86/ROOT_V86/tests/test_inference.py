import numpy as np
import pytest
from src.inference import gls_fit,correlated_cov,fit_shape_profiles,rank_one_bootstrap
from src.physics import gravity

def test_gls_known():
    X=np.array([[1.,0.],[1.,1.],[1.,2.],[1.,3.]])
    y=X@np.array([2.,3.])
    out=gls_fit(X,y,np.eye(4))
    assert out['coef']==pytest.approx([2,3])
    assert out['chi2']<1e-25

def test_gls_correlated_matches_solve():
    rng=np.random.default_rng(0)
    X=rng.normal(size=(15,3));y=rng.normal(size=15)
    cov=correlated_cov(15,.1,.8,1)
    out=gls_fit(X,y,cov)
    manual=np.linalg.solve(X.T@np.linalg.solve(cov,X),X.T@np.linalg.solve(cov,y))
    assert out['coef']==pytest.approx(manual,abs=1e-9)

def test_cov_spd():
    assert np.linalg.eigvalsh(correlated_cov(30,.1,.9,.2)).min()>0

@pytest.mark.parametrize('n,sig,rho,common',[(0,1,.3,.3),(2,-1,.3,.3),(2,1,1,.3),(2,1,.3,-1)])
def test_cov_invalid(n,sig,rho,common):
    with pytest.raises(ValueError):correlated_cov(n,sig,rho,common)

def test_profile_recovers_shape():
    mu=4.;alpha=.1;lam=.6
    r=np.linspace(.4,2.,12)
    y=np.array([gravity(mu,t,alpha=alpha,length=lam) for t in r])
    cov=np.diag((y*.001)**2)
    out=fit_shape_profiles(r,y,cov,[.2,.6,10])
    row=out[1]
    assert row['alpha']==pytest.approx(alpha,rel=1e-6)
    assert row['mu']==pytest.approx(mu,rel=1e-6)
    assert row['chi2']<1e-15

def test_profile_bad_range():
    with pytest.raises(ValueError):fit_shape_profiles([1,2],[1,2],np.eye(2),[-1])

def test_rank_bootstrap_null_repeatable():
    rng=np.random.default_rng(20)
    truth=np.outer([.7,1.,1.2],[.2,.7,1.,1.3])
    cov=np.eye(truth.size)*(.07**2)
    obs=truth+rng.normal(0,.07,truth.shape)
    a=rank_one_bootstrap(obs,cov,B=25,seed=7)
    b=rank_one_bootstrap(obs,cov,B=25,seed=7)
    assert a['bootstrap_p']==b['bootstrap_p']
    assert .0<a['bootstrap_p']<=1
    assert a['chi2']>=0

def test_rank_invalid():
    with pytest.raises(ValueError):rank_one_bootstrap(np.ones((1,2)),np.eye(2))

def test_rank_cov_invalid():
    with pytest.raises(ValueError):rank_one_bootstrap(np.ones((2,2)),np.eye(3))
