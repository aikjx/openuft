"""Formal dimensions under c=1. M and L independent, T=L, hbar=M*L, G=L/M."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Dim:
    m:int=0
    l:int=0
    def __mul__(self,other):return Dim(self.m+other.m,self.l+other.l)
    def __truediv__(self,other):return Dim(self.m-other.m,self.l-other.l)
    def __pow__(self,p):return Dim(self.m*p,self.l*p)

ONE=Dim(); MASS=Dim(1,0); LENGTH=Dim(0,1)
HBAR=Dim(1,1); G=Dim(-1,1)
CURVATURE=Dim(0,-1); TORSION=CURVATURE; OMEGA=CURVATURE

def dimension_audit():
    return {
        'hbar':HBAR == MASS*LENGTH,
        'G':G == LENGTH/MASS,
        'Gm2_over_hbar_dimensionless':G*MASS*MASS/HBAR == ONE,
        'G_hbar_is_length_squared':G*HBAR == LENGTH**2,
        'curvature_torsion_frequency_same_dimension':CURVATURE == TORSION == OMEGA,
        'kappa2_over_omega2_dimensionless':CURVATURE**2 / OMEGA**2 == ONE,
        'h_not_just_curvature':HBAR != CURVATURE,
    }
