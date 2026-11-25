"""Round S2 Dirac spectrum with monopole integer flux.
For k>=1: eigenvalues +/-sqrt(k(k+|m|))/R with per-sign degeneracy |m|+2k.
At k=0, there are |m| zero modes of chirality sign(m), or none when m=0.
"""
import math
from dataclasses import dataclass

@dataclass(frozen=True)
class Level:
    flux: int
    level: int
    eigenvalue_abs_per_length: float
    degeneracy_per_sign: int
    zero_mode: bool


def index(flux: int, charge: int = 1) -> int:
    if not isinstance(flux,int) or not isinstance(charge,int):
        raise TypeError('flux and integer-normalized charge must be integers')
    return flux*charge


def chiral_zero_modes(flux: int, charge: int = 1) -> tuple[int,int]:
    # Choose internal D+ convention in which positive index counts positive chirality.
    m=index(flux,charge)
    return max(m,0),max(-m,0)


def sphere_spectrum(flux: int, radius: float = 1.0, max_level: int = 3, charge: int = 1) -> list[Level]:
    if radius<=0 or max_level<0:
        raise ValueError('radius>0 and max_level>=0 required')
    m=index(flux,charge)
    result=[]
    if m:
        result.append(Level(m,0,0.0,abs(m),True))
    for k in range(1,max_level+1):
        result.append(Level(m,k,math.sqrt(k*(k+abs(m)))/radius,abs(m)+2*k,False))
    return result


def first_massive_gap_per_length(flux: int, radius: float = 1.0, charge: int = 1) -> float:
    if radius<=0:
        raise ValueError('radius must be positive')
    return math.sqrt(1+abs(index(flux,charge)))/radius


def holomorphic_basis_count(flux: int) -> int:
    """H^0(CP1,O(n-1)), for n>0. Negative flux modes are anti-holomorphic."""
    return max(flux,0)


def all_chiral_modes_for_6d_dirac(flux: int) -> tuple[int,int]:
    """A complete 6D Dirac spinor contains both 6D Weyl sectors: vectorlike 4D pair."""
    return abs(flux),abs(flux)
