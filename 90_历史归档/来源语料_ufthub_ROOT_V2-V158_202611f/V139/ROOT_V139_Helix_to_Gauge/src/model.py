"""ROOT V139 mathematical discriminants. c=1; hbar and G independent.
No claim that a real force or unification was established.
Pure Python stdlib, deterministic numerical verification.
"""
from __future__ import annotations
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class LightHelix:
    radius: float
    omega: float
    axial: float

    def __post_init__(self):
        if not (math.isfinite(self.radius) and math.isfinite(self.omega) and math.isfinite(self.axial)):
            raise ValueError('All parameters must be finite')
        if self.radius <= 0 or self.omega <= 0:
            raise ValueError('radius and angular frequency must be positive')
        if not math.isclose(self.radius**2*self.omega**2 + self.axial**2,1.,rel_tol=1e-11,abs_tol=1e-11):
            raise ValueError('c=1 null spatial speed constraint violated')

    @classmethod
    def from_curvature_torsion(cls, curvature:float, torsion:float)->'LightHelix':
        if not all(map(math.isfinite,[curvature,torsion])) or curvature <= 0:
            raise ValueError('For Frenet frame: curvature must be positive')
        om=math.hypot(curvature,torsion)
        return cls(curvature/om**2,om,torsion/om)

    @property
    def transverse(self): return self.radius*self.omega
    @property
    def curvature(self): return self.radius*self.omega*self.omega
    @property
    def torsion(self): return self.axial*self.omega
    @property
    def pitch(self): return 2*math.pi*self.axial/self.omega
    @property
    def frequency(self): return self.omega/(2*math.pi)
    def position(self,t):
        a=self.omega*t
        return (self.radius*math.cos(a),self.radius*math.sin(a),self.axial*t)
    def velocity(self,t):
        a=self.omega*t
        return (-self.transverse*math.sin(a),self.transverse*math.cos(a),self.axial)
    def acceleration(self,t):
        a=self.omega*t
        return (-self.radius*self.omega**2*math.cos(a),-self.radius*self.omega**2*math.sin(a),0.)
    def frame(self,t):
        T=self.velocity(t)
        a=self.omega*t
        N=(-math.cos(a),-math.sin(a),0.)
        B=cross(T,N)
        return T,N,B
    def darboux(self,t):
        T,N,B=self.frame(t)
        return add(scale(self.torsion,T),scale(self.curvature,B))
    def boost_along_axis(self,beta):
        if abs(beta)>=1 or not math.isfinite(beta): raise ValueError('invalid boost speed')
        gamma=1/math.sqrt(1-beta**2)
        doppler=gamma*(1-beta*self.axial)
        axial_new=(self.axial-beta)/(1-beta*self.axial)
        om_new=self.omega/doppler
        return LightHelix(self.radius,om_new,axial_new),doppler
    def transverse_force(self,t,energy):
        # spatial momentum p=E*T; constant-energy null point needs a transverse interaction
        if energy<0: raise ValueError('Energy must be nonnegative')
        T,N,B=self.frame(t)
        return scale(energy*self.curvature,N)

def dot(x,y): return sum(a*b for a,b in zip(x,y))
def cross(x,y): return (x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0])
def scale(q,x): return tuple(q*y for y in x)
def add(x,y): return tuple(a+b for a,b in zip(x,y))
def norm(x): return math.sqrt(dot(x,x))


def berry_connection_theta_phi(theta:float,winding:int=1):
    """For z=(cos(theta/2), exp(i*winding*phi)*sin(theta/2))."""
    return winding*(1-math.cos(theta))/2

def berry_curvature_theta_phi(theta:float,winding:int=1):
    return winding*math.sin(theta)/2

def orientation(theta,phi,winding:int=1):
    ph=winding*phi
    return (math.sin(theta)*math.cos(ph),math.sin(theta)*math.sin(ph),math.cos(theta))

def berry_curvature_via_n(theta,phi,winding=1):
    """1/2 n dot (∂theta n × ∂phi n)."""
    ph=winding*phi
    st,ct=math.sin(theta),math.cos(theta)
    cp,sp=math.cos(ph),math.sin(ph)
    n=(st*cp,st*sp,ct)
    nt=(ct*cp,ct*sp,-st)
    np=(-winding*st*sp,winding*st*cp,0.)
    return dot(n,cross(nt,np))/2

def berry_flux_analytic(winding:int=1): return 2*math.pi*winding

def berry_flux_midpoint(n_theta=300,n_phi=320,winding:int=1):
    """Midpoint quadrature of closed sphere Berry curvature."""
    if n_theta<2 or n_phi<2: raise ValueError('too few cells')
    dtheta=math.pi/n_theta
    dphi=2*math.pi/n_phi
    return sum(berry_curvature_theta_phi((i+.5)*dtheta,winding) for i in range(n_theta))*dtheta*dphi*n_phi

def spacetime_berry_field(theta,theta_gradient,phi_gradient,winding=1):
    """F_mu_nu=(winding/2)sin(theta)(∂mu theta ∂nu phi - ∂nu theta ∂mu phi)."""
    if len(theta_gradient)!=len(phi_gradient): raise ValueError('gradient dimension mismatch')
    d=len(theta_gradient)
    q=winding*math.sin(theta)/2
    return [[q*(theta_gradient[i]*phi_gradient[j]-theta_gradient[j]*phi_gradient[i]) for j in range(d)] for i in range(d)]

def stueckelberg_B(theta_gradient,A):
    if len(theta_gradient)!=len(A): raise ValueError('vector length mismatch')
    return tuple(t-a for t,a in zip(theta_gradient,A))

def stueckelberg_gauge_transform(theta_gradient,A,chi_gradient):
    if not (len(theta_gradient)==len(A)==len(chi_gradient)): raise ValueError('vector length mismatch')
    return tuple(t+c for t,c in zip(theta_gradient,chi_gradient)),tuple(a+c for a,c in zip(A,chi_gradient))

def vector_inverse_length_mass(gauge_coupling:float,f_inv_length:float):
    """mu=|g f|, energy gap= hbar*mu (c=1)."""
    return abs(gauge_coupling*f_inv_length)

def relative_dispersion(k:float,g:float,f_inv_length:float):
    """omega^2=k^2+(g f)^2, in units c=1."""
    return math.hypot(k,vector_inverse_length_mass(g,f_inv_length))


def pfaffian4(F):
    """Pfaffian of antisymmetric 4x4 two-form F. For F=dtheta ^ dphi, identically zero."""
    if len(F)!=4 or any(len(row)!=4 for row in F): raise ValueError('Require 4x4')
    return F[0][1]*F[2][3]-F[0][2]*F[1][3]+F[0][3]*F[1][2]

def invariant_E_dot_B_proxy(F):
    """Up to a sign/convention, Pfaffian equals E·B for a spacetime EM two-form."""
    return pfaffian4(F)


def sum_two_forms(F1,F2):
    if len(F1)!=len(F2) or any(len(x)!=len(y) for x,y in zip(F1,F2)):
        raise ValueError('Two-form shapes must match')
    return [[x+y for x,y in zip(r1,r2)] for r1,r2 in zip(F1,F2)]
