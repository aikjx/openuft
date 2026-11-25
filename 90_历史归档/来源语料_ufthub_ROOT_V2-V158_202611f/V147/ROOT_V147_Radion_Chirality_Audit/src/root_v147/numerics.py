"""Independent finite-difference checks and spherical harmonic orthogonality."""
from math import sqrt, pi, cos

def legendre(ell,x):
    if ell<0 or type(ell) is not int: raise ValueError('ell nonnegative integer')
    if ell==0:return 1.0
    if ell==1:return x
    p0,p1=1.0,x
    for l in range(2,ell+1):
        p0,p1=p1,((2*l-1)*x*p1-(l-1)*p0)/l
    return p1

def simpson_legendre_inner(l,m,nsteps=2048):
    """∫_{-1}^1 P_l(x)P_m(x) dx numeric; require even nsteps."""
    if nsteps%2 or nsteps<=0:raise ValueError('nsteps even and positive')
    h=2/nsteps
    total=0.
    for i in range(nsteps+1):
        x=-1+i*h
        weight=1 if i in (0,nsteps) else (4 if i%2 else 2)
        total+=weight*legendre(l,x)*legendre(m,x)
    return total*h/3

def numerical_drdC(A,B,C,K4,delta=1e-6):
    from .flux import FluxModel
    up=FluxModel(A,B,C+delta,K4).min().radius
    dn=FluxModel(A,B,C-delta,K4).min().radius
    return (up-dn)/(2*delta)
