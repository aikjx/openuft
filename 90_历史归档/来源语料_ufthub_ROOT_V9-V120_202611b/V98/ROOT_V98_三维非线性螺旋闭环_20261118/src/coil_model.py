"""ROOT V96: axisymmetric, smooth finite-width toroidal current sources.

All source strengths are *per coil* current [A]. SI units. A continuous
C-infinity current density is represented numerically by Gaussian quadrature
of its circular-filament Biot-Savart kernel; a finite quadrature representation
must NOT itself be claimed to have globally finite magnetic self-energy.
"""
from dataclasses import dataclass
import numpy as np
from scipy.constants import mu_0, c, e, m_e
from scipy.special import ellipk, ellipe
from scipy.integrate import solve_ivp
from numpy.polynomial.legendre import leggauss


def loop_field_cyl(r, z, radius, center_z, current=1.0):
    """Circular filament analytic Biot-Savart field off the conductor.
    r,z can be arrays, broadcasts with source radii/positions.
    """
    r,z,a,h,I=np.broadcast_arrays(np.asarray(r,float), np.asarray(z,float),
                                      np.asarray(radius,float),np.asarray(center_z,float),
                                      np.asarray(current,float))
    zz=z-h
    dp=(a+r)**2+zz**2
    dm=(a-r)**2+zz**2
    k2=4*a*r/dp
    if np.any(dm==0): raise ValueError('point on ideal wire')
    K=ellipk(k2); E=ellipe(k2)
    Bz=mu_0*I/(2*np.pi*np.sqrt(dp))*(K+(a*a-r*r-zz*zz)/dm*E)
    with np.errstate(divide='ignore',invalid='ignore'):
        Br=mu_0*I*zz/(2*np.pi*r*np.sqrt(dp))*(-K+(a*a+r*r+zz*zz)/dm*E)
    if np.any(r<1e-9):
        Br=np.where(r<1e-9,0.,Br)
        Bz=np.where(r<1e-9,mu_0*I*a*a/(2*(a*a+zz*zz)**1.5),Bz)
    return Br, Bz


def smooth_finite_coil_quadrature(radius=.01, z_center=.008, wire_radius=.001, n=13):
    """Quadrature of smooth toroidal J_phi(r,z). Sum(weights)=1 (current fractions).
    Normalized J_phi=I f(s/wire_radius)/integral f(s/wire_radius)dr dz,
    f(u)=exp(-u^2/(1-u^2)) for u<1, zero otherwise.
    """
    if radius <= wire_radius or wire_radius<=0: raise ValueError('invalid conductor geometry')
    nodes,weights=leggauss(n)
    x,y=np.meshgrid(nodes,nodes,indexing='ij')
    rs=x*x+y*y
    profile=np.zeros_like(rs)
    sel=rs<1
    profile[sel]=np.exp(-rs[sel]/(1-rs[sel]))
    raw=(weights[:,None]*weights[None,:])*profile
    weights_normal=raw/raw.sum()
    mask=weights_normal>0
    return radius+wire_radius*x[mask],z_center+wire_radius*y[mask],weights_normal[mask]


@dataclass
class TwoCoilField:
    radius:float=.01
    half_separation:float=.008
    wire_radius:float=.001
    order:int=13
    current:float=1.

    def __post_init__(self):
        a,h,w=smooth_finite_coil_quadrature(self.radius,self.half_separation,self.wire_radius,self.order)
        self.radii=np.concatenate([a,a])
        self.zloc=np.concatenate([h,-h])
        self.fractions=np.concatenate([w,w])

    def unit_field(self,r,z):
        r=np.asarray(r)
        z=np.asarray(z)
        # scalar evaluation or vectorized scalars; quadrature continuous-current approximation
        # original collocation points are strictly separated from the external conductors
        br,bz=loop_field_cyl(np.expand_dims(r,-1),np.expand_dims(z,-1),
                             self.radii,self.zloc,self.fractions)
        return np.sum(br,axis=-1),np.sum(bz,axis=-1)

    def field(self,r,z):
        br,bz=self.unit_field(r,z)
        return self.current*br,self.current*bz

    def field_cart(self,x,y,z):
        r=np.hypot(x,y)
        br,bz=self.field(r,z)
        if r<1e-12: return np.array([0.,0.,float(bz)])
        return np.array([br*x/r,br*y/r,bz],float)

    def index(self,r0,dr=1e-5):
        bz=self.field(r0,0.)[1]
        bp=self.field(r0+dr,0.)[1]
        bm=self.field(r0-dr,0.)[1]
        return -r0/bz*(bp-bm)/(2*dr)

    def vacuum_clearance(self,r0):
        # minimum geometric distance from orbit to wire cross-section
        return np.hypot(self.radius-r0,self.half_separation)-self.wire_radius


def circular_reference(beta=.1,r0=.005,field=None):
    field=field or TwoCoilField()
    v=beta*c
    gamma=1/(1-beta*beta)**.5
    b_required=gamma*m_e*v/(e*r0)
    b_peramp=field.unit_field(r0,0.)[1]
    field.current=float(b_required/b_peramp)
    n=float(field.index(r0))
    omega=v/r0
    return {'beta':beta,'r0':r0,'v':v,'gamma':gamma,'B0':float(b_required),
            'I_per_coil':field.current,'n':n,'nu_r':float(np.sqrt(1-n)) if n<1 else None,
            'nu_z':float(np.sqrt(n)) if n>0 else None,
            'omega':omega,'T':2*np.pi/omega,'clearance':field.vacuum_clearance(r0)}


def normalized_rhs(t,y,field,beta,r0):
    # x/r0, v/(beta*c); t in r0/(beta*c), |velocity| is constant
    V=y[3:]
    xyz=y[:3]*r0
    B=field.field_cart(*xyz)
    gamma=1/(1-beta*beta)**.5
    coeff=(-e)*r0/(gamma*m_e*beta*c)
    return np.concatenate((V,coeff*np.cross(V,B)))


def trajectory(field,beta=.1,r0=.005,turns=10,dx=0.,dz=0.,dv=0.,rtol=2e-10,atol=3e-12,points=0):
    initial=np.array([1+dx/r0,0.,dz/r0,0.,1+dv,0.])
    times=(0.,turns*2*np.pi)
    t_eval=np.linspace(*times,int(points)) if points else None
    return solve_ivp(normalized_rhs,times,initial,args=(field,beta,r0),
                     method='DOP853',rtol=rtol,atol=atol,t_eval=t_eval)


def jacobian_return(field,beta=.1,r0=.005,h=2e-6):
    # derivatives of fixed-time flow in normalized position/velocity variables
    t_end=2*np.pi
    def integrate(y):
        return solve_ivp(normalized_rhs,(0,t_end),y,args=(field,beta,r0),
                         method='DOP853',rtol=3e-12,atol=1e-13).y[:,-1]
    y0=np.array([1.,0.,0.,0.,1.,0.]); center=integrate(y0)
    jac=np.empty((6,6))
    for i in range(6):
        xp=y0.copy();xm=y0.copy();xp[i]+=h;xm[i]-=h
        jac[:,i]=(integrate(xp)-integrate(xm))/(2*h)
    return center,jac


def direct_biot_savart_ring(x,y,z,a,h,I,num=32768):
    """Independent angular trapezoidal Biot-Savart for a single loop."""
    angle=(np.arange(num)+.5)*(2*np.pi/num)
    pos=np.stack((a*np.cos(angle),a*np.sin(angle),np.full(num,h)),axis=1)
    dl=np.stack((-a*np.sin(angle),a*np.cos(angle),np.zeros(num)),axis=1)
    R=np.array([x,y,z])[None,:]-pos
    integrand=np.cross(dl,R)/(np.linalg.norm(R,axis=1)**3)[:,None]
    return mu_0*I/(4*np.pi)*integrand.sum(axis=0)*(2*np.pi/num)
