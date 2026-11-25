"""ROOT V148: ideal null-speed spatial helix in flat Minkowski spacetime.
All kinematic quantities here have c=1. No assumption hbar=1 or G=1.
"""
from dataclasses import dataclass
from math import cos, sin, sqrt, isclose, pi


def dot(a, b):
    return sum(x*y for x,y in zip(a,b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def norm(v):
    return sqrt(dot(v,v))


@dataclass(frozen=True)
class NullHelix:
    a: float
    omega: float
    u: float

    def __post_init__(self):
        if self.a <= 0 or self.omega == 0 or not abs(self.u) < 1:
            raise ValueError('Nondegenerate helix requires a>0, omega!=0, |u|<1')
        if not isclose(self.a**2*self.omega**2+self.u**2,1,rel_tol=1e-11,abs_tol=1e-11):
            raise ValueError('Null-speed condition a^2 omega^2+u^2=1 violated')

    @classmethod
    def from_u_omega(cls, u, omega):
        if not abs(u)<1 or omega==0:
            raise ValueError('Need |u|<1 and nonzero omega')
        return cls(sqrt(1-u*u)/abs(omega), omega, u)

    def position(self,t):
        p=self.omega*t
        return (self.a*cos(p),self.a*sin(p),self.u*t)

    def velocity(self,t):
        p=self.omega*t
        return (-self.a*self.omega*sin(p),self.a*self.omega*cos(p),self.u)

    def acceleration(self,t):
        p=self.omega*t
        return (-self.a*self.omega**2*cos(p),-self.a*self.omega**2*sin(p),0.)

    def jerk(self,t):
        p=self.omega*t
        return (self.a*self.omega**3*sin(p),-self.a*self.omega**3*cos(p),0.)

    def curvature(self):
        return self.a*self.omega**2

    def torsion(self):
        return self.u*self.omega

    def speed(self):
        return sqrt(self.a**2*self.omega**2+self.u**2)

    def four_position(self,t):
        return (t,*self.position(t))

    def four_tangent(self,t):
        return (1.,*self.velocity(t))

    def four_second(self,t):
        return (0.,*self.acceleration(t))

    def null_norm(self,t):
        q=self.four_tangent(t)
        return -q[0]*q[0]+dot(q[1:],q[1:])

    def four_second_norm(self,t):
        q=self.four_second(t)
        return -q[0]*q[0]+dot(q[1:],q[1:])

    def frenet(self,t):
        T=self.velocity(t)
        acc=self.acceleration(t)
        N=tuple(v/norm(acc) for v in acc)
        B=cross(T,N)
        return T,N,B

    def pitch(self):
        return 2*pi*self.u/abs(self.omega)

    def boost(self,beta):
        if not abs(beta)<1:
            raise ValueError('Lorentz boost requires |beta|<1')
        d=self.doppler_particle(beta)
        new_omega=self.omega/d
        new_u=(self.u-beta)/(1-beta*self.u)
        return NullHelix(self.a,new_omega,new_u)

    def doppler_particle(self,beta):
        if not abs(beta)<1:
            raise ValueError('Lorentz boost requires |beta|<1')
        return (1-beta*self.u)/sqrt(1-beta*beta)

    def coordinate_boost(self,t,beta):
        x,y,z=self.position(t)
        gamma=1/sqrt(1-beta*beta)
        return (gamma*(t-beta*z),x,y,gamma*(z-beta*t))


def ratio_to_u(ratio):
    """For omega>0, r=tau/kappa runs through all real values as u varies."""
    return ratio/sqrt(1+ratio*ratio)
