"""JPL DE440 empirical GM baseline only; never a derivation of G from ROOT."""
from dataclasses import dataclass
from math import sqrt

@dataclass(frozen=True)
class SphereReference:
    name: str
    GM_SI: float
    radius_m: float

    def g(self,h=0.):
        r=self.radius_m+h
        if r<=0: raise ValueError('Outside reference sphere r>0 only')
        return self.GM_SI/r**2

    def acceleration(self,xyz):
        r=sqrt(sum(x*x for x in xyz))
        if r<self.radius_m: raise ValueError('Spherical exterior reference only')
        return tuple(-self.GM_SI*x/(r**3) for x in xyz)

    def distance_ratio(self,h1,h2):
        r1=self.radius_m+h1;r2=self.radius_m+h2
        return (r1*r1*self.g(h1))/(r2*r2*self.g(h2))

EARTH=SphereReference('Earth (JPL DE440 GM)',398600.435507e9,6371000.)
MOON=SphereReference('Moon (JPL DE440 GM)',4902.800118e9,1737400.)
