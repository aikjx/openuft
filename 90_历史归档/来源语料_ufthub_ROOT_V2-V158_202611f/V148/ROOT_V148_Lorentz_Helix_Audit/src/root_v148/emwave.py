"""Exact vacuum Maxwell plane waves; geometrically rotating field vectors, straight energy transport."""
from dataclasses import dataclass
from math import cos,sin,sqrt
from .helix import dot,cross

@dataclass(frozen=True)
class CircularWave:
    k: float = 1.
    amplitude: float = 1.
    handedness: int = 1

    def __post_init__(self):
        if self.k<=0 or self.amplitude<=0 or self.handedness not in (-1,1):
            raise ValueError('Need k>0, amplitude>0 and handedness=+1 or -1')

    def fields(self,t,z):
        s=self.k*(t-z)
        E=(self.amplitude*cos(s),self.handedness*self.amplitude*sin(s),0.)
        B=(-E[1],E[0],0.)
        return E,B

    def derivatives(self,t,z):
        s=self.k*(t-z); k=self.k; a=self.amplitude; h=self.handedness
        dEt=(-a*k*sin(s),h*a*k*cos(s),0.)
        dBt=(-h*a*k*cos(s),-a*k*sin(s),0.)
        dEz=tuple(-x for x in dEt)
        dBz=tuple(-x for x in dBt)
        return dEt,dBt,dEz,dBz

    def maxwell_residuals(self,t,z):
        dEt,dBt,dEz,dBz=self.derivatives(t,z)
        curlE=(-dEz[1],dEz[0],0.)
        curlB=(-dBz[1],dBz[0],0.)
        faraday=tuple(v+w for v,w in zip(dBt,curlE))
        ampere=tuple(v-w for v,w in zip(curlB,dEt))
        return faraday,ampere,0.,0.

    def invariants(self,t,z):
        E,B=self.fields(t,z)
        return dot(E,B),dot(E,E)-dot(B,B)

    def poynting(self,t,z):
        E,B=self.fields(t,z)
        return cross(E,B)

    def boost(self,beta):
        if not abs(beta)<1:
            raise ValueError('Lorentz boost requires |beta|<1')
        factor=(1-beta)/sqrt(1-beta*beta)
        return CircularWave(self.k*factor,self.amplitude*factor,self.handedness)

    def phase_covariance(self,t,z,beta):
        gamma=1/sqrt(1-beta*beta)
        tp=gamma*(t-beta*z)
        zp=gamma*(z-beta*t)
        return self.k*(t-z),self.boost(beta).k*(tp-zp)
