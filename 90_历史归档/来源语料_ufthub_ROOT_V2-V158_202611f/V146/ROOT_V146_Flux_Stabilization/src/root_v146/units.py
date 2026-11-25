"""Symbolic dimensions using independent action S (hbar) and length L, c=1."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Dim:
    s: int = 0
    l: int = 0
    def __mul__(self, other):
        return Dim(self.s+other.s,self.l+other.l)
    def __truediv__(self,other):
        return Dim(self.s-other.s,self.l-other.l)
    def __pow__(self, power: int):
        return Dim(self.s*power,self.l*power)

S = Dim(1,0)
L = Dim(0,1)
HBAR = S
G = (L**2)/S
K6 = S/(L**4)
LAM6 = S/(L**6)
CHI6 = S/(L**2)
R6 = L**-2
F_SQUARED = L**-4
K4 = S/(L**2)
V4 = S/(L**4)
A = LAM6 * L**4
B = K6 * L**4
C = CHI6 * L**4
RADION = Dim(1, -1)  # sqrt(K4) has noninteger exponents; use phi^2=K4.
