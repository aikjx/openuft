"""Symbolic dimensions in units c=1; hbar and G always remain dimensional."""
from dataclasses import dataclass
from fractions import Fraction

@dataclass(frozen=True)
class Dim:
    S: Fraction = Fraction(0)
    L: Fraction = Fraction(0)
    def __mul__(self,other): return Dim(self.S+other.S,self.L+other.L)
    def __truediv__(self,other): return Dim(self.S-other.S,self.L-other.L)
    def __rtruediv__(self,other):
        if other!=1: raise TypeError("Only 1/Dim supported")
        return Dim(-self.S,-self.L)
    def __pow__(self,p):
        p=Fraction(p)
        return Dim(self.S*p,self.L*p)

S=Dim(S=Fraction(1))
L=Dim(L=Fraction(1))
hbar=S
G4=L**2/S
K6=S/L**4
Lambda6=S/L**6
chi6=S/L**2
K4=S/L**2
V4=S/L**4
