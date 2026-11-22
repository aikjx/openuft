"""2D U(1) torus background and Hermitian Wilson--Dirac index demonstration.
No physical constants are set to 1 except c; matrices/links are dimensionless
through the physical combination q A / hbar.
"""
import numpy as np

SX=np.array([[0,1],[1,0]],dtype=complex)
SY=np.array([[0,-1j],[1j,0]],dtype=complex)
SZ=np.array([[1,0],[0,-1]],dtype=complex)


def links(nside:int, flux:int):
    """Periodically identified NxN lattice links with Chern number flux."""
    if nside<3 or abs(flux)>=nside*nside//2:
        raise ValueError('invalid lattice size or inadmissible flux')
    n=nside
    ux=np.empty((n,n),complex)
    uy=np.ones((n,n),complex)
    for x in range(n):
        for y in range(n):
            ux[x,y]=np.exp(-2j*np.pi*flux*y/(n*n))
            if y==n-1: uy[x,y]=np.exp(2j*np.pi*flux*x/n)
    return ux,uy


def plaquette_chern(ux,uy):
    n=ux.shape[0]
    phases=[]
    for x in range(n):
        for y in range(n):
            p=ux[x,y]*uy[(x+1)%n,y]*np.conj(ux[x,(y+1)%n])*np.conj(uy[x,y])
            phases.append(np.angle(p))
    return sum(phases)/(2*np.pi),np.array(phases)


def wilson_from_links(ux,uy,m0:float=1.0):
    """Wilson kernel for user-provided U(1) link arrays."""
    """2D Wilson operator r=1, lattice spacing one, negative Wilson mass -m0."""
    n=ux.shape[0]; ns=n*n
    assert ux.shape == (n,n) and uy.shape == (n,n)
    d=np.zeros((2*ns,2*ns),complex)
    g=[SX,SY]
    eye=np.eye(2)
    def ix(x,y):return x*n+y
    for x in range(n):
        for y in range(n):
            s=ix(x,y); d[2*s:2*s+2,2*s:2*s+2]+=(2-m0)*eye
            for mu,(dx,dy),u in [(0,(1,0),ux),(1,(0,1),uy)]:
                xplus=(x+dx)%n;yplus=(y+dy)%n
                xminus=(x-dx)%n;yminus=(y-dy)%n
                sp=ix(xplus,yplus);sm=ix(xminus,yminus)
                d[2*s:2*s+2,2*sp:2*sp+2]+=-0.5*(eye-g[mu])*u[x,y]
                d[2*s:2*s+2,2*sm:2*sm+2]+=-0.5*(eye+g[mu])*np.conj(u[xminus,yminus])
    gamma5=np.kron(np.eye(ns),SZ)
    h=gamma5@d
    return d,h,gamma5


def wilson_dirac(nside:int,flux:int,m0:float=1.0):
    ux,uy=links(nside,flux)
    return wilson_from_links(ux,uy,m0)

def overlap_index(nside:int,flux:int,m0:float=1.0):
    d,h,g5=wilson_dirac(nside,flux,m0)
    eig=np.linalg.eigvalsh(h)
    if np.min(np.abs(eig))<1e-8: raise ArithmeticError('Wilson kernel crosses zero; index ambiguous')
    index=-0.5*float(np.sign(eig).sum())
    return {"index":index,"min_abs_wilson_eigenvalue":float(np.min(np.abs(eig))),
            "hermiticity_residual":float(np.linalg.norm(h-h.conj().T)),
            "gamma5_hermiticity_residual":float(np.linalg.norm(d.conj().T-g5@d@g5))}


def overlap_index_from_links(ux,uy,m0:float=1.0):
    d,h,g5=wilson_from_links(ux,uy,m0)
    eig=np.linalg.eigvalsh(h)
    if np.min(np.abs(eig))<1e-8:raise ArithmeticError('zero Wilson kernel')
    return -0.5*float(np.sign(eig).sum())


def overlap_zero_mode_chiralities(nside, flux, tolerance=1e-8):
    """Explicit chiral zero modes of D_ov=I+gamma5 sign(H_W)."""
    d,h,g5=wilson_dirac(nside,flux)
    ev,v=np.linalg.eigh(h)
    signh=(v*np.sign(ev))@v.conj().T
    Dov=np.eye(len(ev))+g5@signh
    u,s,vh=np.linalg.svd(Dov)
    kernel=vh.conj().T[:,s<tolerance]
    if kernel.shape[1]==0:return []
    return sorted(float(z.real) for z in np.linalg.eigvalsh(kernel.conj().T@g5@kernel))


def abelian_anomaly_coeffs(flux, charges, dimensions=None):
    """4D anomaly of one common 6D-chirality parent per charged multiplet.
    Charges and dimensions are integer-normalized; coefficients are toy diagnostics.
    """
    dimensions=dimensions if dimensions is not None else [1]*len(charges)
    if len(charges)!=len(dimensions):raise ValueError('mismatched lists')
    return {'cubic':sum(flux*d*q**4 for q,d in zip(charges,dimensions)),
            'mixed_gravity':sum(flux*d*q**2 for q,d in zip(charges,dimensions))}


def c1_index(flux,charge_integer):
    """Index on an orientable compact spin 2-manifold, degree-q line bundle."""
    if not (isinstance(flux,int) and isinstance(charge_integer,int)):
        raise TypeError('flux and charge must be integers in the chosen unit')
    return flux*charge_integer


def no_flux_sphere_zero_modes(radius:float):
    """Untwisted S2 Dirac with positive scalar curvature has no harmonic spinors."""
    if radius<=0: raise ValueError('radius>0')
    return 2/(radius*radius)>0


def effective_newton(Ghigher:float,volume:float):
    """Unwarped 6D product compactification, G4=G6/V2."""
    if Ghigher<=0 or volume<=0:raise ValueError('positive volume, coupling required')
    return Ghigher/volume

if __name__=='__main__':
    for n in range(-3,4):
        ux,uy=links(8,n)
        c,phis=plaquette_chern(ux,uy)
        d=overlap_index(8,n)
        print(n,c,d)
