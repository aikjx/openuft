"""Two-qubit branch-phase model; no inference of graviton detection."""
import numpy as np
from .v90_model import G,HBAR

def phases(m1=1e-14,m2=1e-14,r=2e-4,d=1e-5,t=1):
    if min(m1,m2,r,d,t)<=0: raise ValueError('positive inputs required')
    distances=np.array([r,r+d,r+d,r+2*d])
    return G*m1*m2*t/(HBAR*distances)

def state(phi):
    p=np.asarray(phi,float)
    if p.shape!=(4,):raise ValueError('four phases required')
    return np.exp(1j*p)/2

def density(phi,visibility=1):
    if not 0<=visibility<=1:raise ValueError('visibility must be in [0,1]')
    psi=state(phi); rho=np.outer(psi,psi.conj())
    # independent phase-flip channels, off-diagonal coherence multiplied by v per differing qubit
    for i in range(4):
        for j in range(4):
            h=((i>>1)!=(j>>1))+((i&1)!=(j&1))
            rho[i,j]*=visibility**h
    return rho

def partial_transpose(rho):
    return np.asarray(rho).reshape(2,2,2,2).transpose(0,3,2,1).reshape(4,4)

def negativity(rho):
    eig=np.linalg.eigvalsh(partial_transpose(rho))
    return float(max(0.,-eig[eig<0].sum()))

def delta_phase(phi):
    p=np.asarray(phi)
    return float(p[0]-p[1]-p[2]+p[3])

def pure_negativity(phi):
    return abs(np.sin(delta_phase(phi)/2))/2

def classical_shared_phase_mixture(n=64):
    """Correlated shared random local phases: separable by construction."""
    rho=np.zeros((4,4),complex)
    for angle in np.linspace(0,2*np.pi,n,endpoint=False):
        a=np.array([1,np.exp(1j*angle)])/np.sqrt(2)
        b=np.array([1,np.exp(-1j*angle)])/np.sqrt(2)
        v=np.kron(a,b);rho+=np.outer(v,v.conj())/n
    return rho
