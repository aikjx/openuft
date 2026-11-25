"""c=1 dimension algebra with independent length L and mass M exponents.
Time has dimension L, so [hbar] = M*L and [G] = L/M.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Dim:
    mass:int=0
    length:int=0
    def __mul__(self,other):return Dim(self.mass+other.mass,self.length+other.length)
    def __truediv__(self,other):return Dim(self.mass-other.mass,self.length-other.length)
    def __pow__(self,p):return Dim(self.mass*p,self.length*p)

ONE=Dim(); M=Dim(mass=1); L=Dim(length=1)
hbar=M*L; G=L/M; curvature=L**-2; F=L**-2; d4x=L**4
EinsteinAction=curvature/G*d4x
MaxwellAction=hbar*(F**2)*d4x
helix_kappa=L**-1; helix_omega=L**-1
