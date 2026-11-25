"""Dimension exponents (M,L) with c=1; G, hbar NOT normalized to one."""
from fractions import Fraction
HBAR=(Fraction(1),Fraction(1))    # M L
G=(Fraction(-1),Fraction(1))      # L/M
KAPPA=(Fraction(0),Fraction(-1))  # 1/L
OMEGA=(Fraction(0),Fraction(-1))  # 1/L
ENERGY=(Fraction(1),Fraction(0))  # M


def multiply(*dims):
    return tuple(sum(v[i] for v in dims) for i in range(2))

def inverse(d):
    return tuple(-x for x in d)

def power(d,p):
    return tuple(x*p for x in d)

PLANCK_MASS=power(multiply(HBAR,inverse(G)),Fraction(1,2))
PHOTON_ENERGY=multiply(HBAR,OMEGA)
CURVATURE_ENERGY=multiply(HBAR,KAPPA)
GRAVITATIONAL_ACTION=multiply(power((Fraction(0),Fraction(1)),4),power((Fraction(0),Fraction(-1)),2),inverse(G))
