"""ROOT V89: gravity-mediated two-qubit phase, EFT scale and identifiability.

Research/educational model only. No gravitational entanglement observations or G prediction.
Newtonian frozen paths; displayed 1PN/EFT terms are conventional representative
scattering-matched potential coefficients, NOT gauge-invariant stand-alone observable.
"""
from __future__ import annotations
from dataclasses import dataclass, replace
from decimal import Decimal, localcontext
import math
import numpy as np

G=6.67430e-11
C=299792458.0
HBAR=6.62607015e-34/(2*math.pi)
EPS0=8.8541878188e-12
KE=1/(4*math.pi*EPS0)
E_CHARGE=1.602176634e-19
PLANCK_LENGTH_SQUARED=G*HBAR/C**3
EFT_LOOP_C=41/(10*math.pi)
PI80='3.14159265358979323846264338327950288419716939937510582097494459230781640628620899'

@dataclass(frozen=True)
class Config:
    m1:float=1e-14
    m2:float=1e-14
    d:float=450e-6
    s1:float=200e-6
    s2:float=200e-6
    t:float=1.0
    q1:float=0.0
    q2:float=0.0
    gamma1:float=0.0
    gamma2:float=0.0
    rho1:float=3500.0
    rho2:float=3500.0

    def valid(self)->'Config':
        from dataclasses import fields
        if not all(math.isfinite(getattr(self,f.name)) for f in fields(self)):
            raise ValueError('all parameters must be finite')
        if min(self.m1,self.m2,self.d,self.rho1,self.rho2)<=0:
            raise ValueError('masses/distances/densities must be positive')
        if min(self.s1,self.s2,self.t,self.gamma1,self.gamma2)<0:
            raise ValueError('branch separations, time, dephasing must be nonnegative')
        if self.d<=(self.s1+self.s2)/2:
            raise ValueError('position branches cross: need d>(s1+s2)/2')
        # for uniform solid spheres the actual bodies must not geometrically overlap
        if float(np.min(branch_distances_unchecked(self)))<=sphere_radius(self.m1,self.rho1)+sphere_radius(self.m2,self.rho2):
            raise ValueError('two finite spheres overlap in a branch')
        return self

def sphere_radius(m:float,density:float)->float:
    return (3*m/(4*math.pi*density))**(1/3)

def branch_distances_unchecked(p:Config)->np.ndarray:
    a=np.array([-p.s1/2,p.s1/2])
    b=p.d+np.array([-p.s2/2,p.s2/2])
    return b[None,:]-a[:,None]

def branch_distances(p:Config)->np.ndarray:
    p.valid()
    return branch_distances_unchecked(p)

def cross(A)->float:
    z=np.asarray(A,dtype=float)
    if z.shape!=(2,2): raise ValueError('cross requires 2x2 matrix')
    return float(z[0,0]-z[0,1]-z[1,0]+z[1,1])

def geom(p:Config,exponent:int)->float:
    if exponent<1: raise ValueError('positive inverse power only')
    return cross(branch_distances(p)**(-exponent))

def scale_terms(p:Config)->dict:
    p.valid()
    pn_length=3*G*(p.m1+p.m2)/C**2
    quantum_length2=EFT_LOOP_C*PLANCK_LENGTH_SQUARED
    A=G*p.m1*p.m2*p.t/HBAR
    n=A*geom(p,1)
    pn=A*pn_length*geom(p,2)
    q=A*quantum_length2*geom(p,3)
    coulomb=-KE*p.q1*p.q2*p.t/HBAR*geom(p,1)
    return dict(newton=n,one_pn_potential=pn,eft_loop_potential=q,coulomb=coulomb,
                total=n+pn+q+coulomb,planck_length=math.sqrt(PLANCK_LENGTH_SQUARED),
                pn_length_m=pn_length,eft_length_squared_m2=quantum_length2,
                pn_over_newton=pn/n if n else 0.0,
                eft_over_newton=q/n if n else 0.0)

def phases(p:Config, include_pn=False, include_eft=False, include_coulomb=True)->np.ndarray:
    r=branch_distances(p)
    A=G*p.m1*p.m2*p.t/HBAR
    res=A/r
    if include_pn: res=res+A*(3*G*(p.m1+p.m2)/C**2)/r**2
    if include_eft: res=res+A*(EFT_LOOP_C*PLANCK_LENGTH_SQUARED)/r**3
    if include_coulomb: res=res-KE*p.q1*p.q2*p.t/(HBAR*r)
    return res

def pure_concurrence(phi)->float:
    return abs(math.sin(cross(phi)/2))

def rho_dephased(p:Config,include_coulomb=True)->np.ndarray:
    v=np.exp(1j*phases(p,include_coulomb=include_coulomb).reshape(4))/2
    r=np.outer(v,v.conj())
    a=math.exp(-p.gamma1*p.t);b=math.exp(-p.gamma2*p.t)
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    r[2*i+j,2*k+l]*=(a if i!=k else 1)*(b if j!=l else 1)
    return r

def partial_transpose(rho):
    a=np.asarray(rho,dtype=complex)
    if a.shape!=(4,4):raise ValueError('requires 4x4 density')
    return a.reshape(2,2,2,2).transpose(0,3,2,1).reshape(4,4)

def negativity(rho)->float:
    ev=np.linalg.eigvalsh(partial_transpose(rho))
    return max(0.0,float(-ev[ev<0].sum()))

def locc_correlated_phase_state(n=512,seed=8719)->np.ndarray:
    if n<1:raise ValueError('n must be >=1')
    rng=np.random.default_rng(seed)
    result=np.zeros((4,4),complex)
    for z in rng.normal(size=n):
        a=np.array([1,np.exp(1j*z)],complex)/math.sqrt(2)
        b=np.array([1,np.exp(-1j*z)],complex)/math.sqrt(2)
        psi=np.kron(a,b)
        result+=np.outer(psi,psi.conj())/n
    return result

def q_equivalent(p:Config)->float:
    p.valid()
    return math.sqrt(G*p.m1*p.m2/KE)

def two_coupling_design(p:Config,ds:tuple[float,...])->np.ndarray:
    """Columns dDelta / d(grav_strength), dDelta / d(coulomb_strength).
    Coupling units: both have J*m, so dPhi= (t/hbar)*F1*(g-k).
    """
    if len(ds)<2:raise ValueError('at least two separations')
    f=np.array([p.t/HBAR*geom(replace(p,d=float(d)),1) for d in ds])
    return np.column_stack((f,-f))

def scaled_design(p:Config,ds:tuple[float,...],L:float=1e-3)->np.ndarray:
    if L<=0 or not math.isfinite(L):raise ValueError('L must be positive')
    return np.array([[geom(replace(p,d=float(d)),k)*L**k for k in (1,2,3)] for d in ds])

def null_projection(p:Config,ds:tuple[float,float,float],L:float=1e-3)->dict:
    """3-distance filter cancels 1/r and 1/r²; diagnostics only, NOT an experiment.

    Columns are dimensionless and normalized separately for a stable definition.
    W is a unit vector perpendicular to first two geometry columns.
    """
    if len(ds)!=3:raise ValueError('exactly three distances')
    X=scaled_design(p,ds,L)
    a=X[:,0]/np.linalg.norm(X[:,0]);b=X[:,1]/np.linalg.norm(X[:,1])
    w=np.cross(a,b)
    sin_angle=float(np.linalg.norm(w))
    if sin_angle<=1e-13: raise ValueError('nearly collinear columns')
    w=w/sin_angle
    cn=float(w@X[:,2]);
    coeff=G*p.m1*p.m2*p.t/HBAR
    projected_eft=coeff*(EFT_LOOP_C*PLANCK_LENGTH_SQUARED/L**3)*cn
    v1=X[:,0]/L;v2=X[:,1]/L**2;v3=X[:,2]/L**3
    measured=coeff*(v1+(3*G*(p.m1+p.m2)/C**2)*v2+(EFT_LOOP_C*PLANCK_LENGTH_SQUARED)*v3)
    naive=float(w@measured)  # rounding can bury EFT signal by ~50 orders of magnitude
    return dict(weights=w.tolist(),geometry=np.asarray(X).tolist(),angle_sine=sin_angle,
                cancellation_1=float(w@X[:,0]),cancellation_2=float(w@X[:,1]),
                loop_projection_analytic=projected_eft,naive_float_projection=naive,
                float_false_signal_ratio=abs(naive/projected_eft) if projected_eft else None)

def decimal_null_determinant(p:Config,ds:tuple[float,float,float],prec=90)->dict:
    """Unnormalized exact-decimal wedge (a x b) dot c.

    Point: avoid catastrophic cancellation of 10^-63 EFT signal from 10^-2 Newton phases.
    """
    if len(ds)!=3:raise ValueError('three separations needed')
    p.valid()
    with localcontext() as ctx:
        ctx.prec=prec
        D=lambda x:Decimal(str(x))
        dd=[D(x) for x in ds]
        s1,s2=D(p.s1),D(p.s2)
        L=Decimal('0.001')
        aa=[];bb=[];cc=[]
        for d in dd:
            r=[d+(s1-s2)/2,d+(s1+s2)/2,d-(s1+s2)/2,d+(s2-s1)/2]
            if min(r)<=0:raise ValueError('invalid branch geometry')
            fx=lambda k:1/r[0]**k-1/r[1]**k-1/r[2]**k+1/r[3]**k
            aa.append(fx(1)*L);bb.append(fx(2)*L**2);cc.append(fx(3)*L**3)
        w=[aa[1]*bb[2]-aa[2]*bb[1],aa[2]*bb[0]-aa[0]*bb[2],aa[0]*bb[1]-aa[1]*bb[0]]
        dot=lambda x:sum((w[i]*x[i] for i in range(3)),Decimal(0))
        grav=D(G)*D(p.m1)*D(p.m2)*D(p.t)/D(HBAR)
        loop=D('41')/(D(10)*Decimal(PI80)) * D(G)*D(HBAR)/D(C)**3
        pn=D(3)*D(G)*(D(p.m1)+D(p.m2))/D(C)**2
        pred=grav*(dot(aa)/L+pn*dot(bb)/L**2+loop*dot(cc)/L**3)
        pure_loop=grav*loop*dot(cc)/L**3
        return dict(null_newton=str(dot(aa)),null_pn=str(dot(bb)),
                    surviving_cubic=str(dot(cc)),total_projection=str(pred),
                    quantum_only_projection=str(pure_loop),precision=prec)

def stats(p:Config)->dict:
    T=scale_terms(p); R=branch_distances(p)
    r1=sphere_radius(p.m1,p.rho1);r2=sphere_radius(p.m2,p.rho2)
    rp=rho_dephased(p)
    return dict(setup=p.__dict__,separations_m=R.tolist(),sphere_radii_m=[r1,r2],
                phase_terms=T,concurrence=pure_concurrence(phases(p)),
                negativity=negativity(rp),linear_entropy=float(1-np.trace(rp@rp).real),
                charge_equiv_C=q_equivalent(p),electron_charge_fraction=q_equivalent(p)/E_CHARGE,
                classical_local_channel_negativity=negativity(locc_correlated_phase_state()),
                labels=['THEORETICAL','SYNTHETIC','NO_REAL_GRAVITY_MEASUREMENT'])
