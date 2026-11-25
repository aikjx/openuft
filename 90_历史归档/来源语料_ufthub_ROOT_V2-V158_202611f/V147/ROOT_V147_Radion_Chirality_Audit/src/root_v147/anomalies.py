"""Exact rational 4D anomaly audit. All fields are left-handed Weyl reps."""
from dataclasses import dataclass
from fractions import Fraction as Q

@dataclass(frozen=True)
class Weyl:
    name: str
    d3: int
    d2: int
    Y: Q
    F: Q

BASE=(
    ('Q_L',3,2,Q(1,6)),
    ('u_L^c',3,1,Q(-2,3)),
    ('d_L^c',3,1,Q(1,3)),
    ('L_L',1,2,Q(-1,2)),
    ('e_L^c',1,1,Q(1)),
)

def fields_uniform_family():
    return tuple(Weyl(n,d3,d2,y,Q(1)) for n,d3,d2,y in BASE)


def fields_B_minus_L():
    # Correct chirality convention for conjugate right handed fields.
    charges=(Q(1,3),Q(-1,3),Q(-1,3),Q(-1),Q(1))
    return tuple(Weyl(n,d3,d2,y,q) for (n,d3,d2,y),q in zip(BASE,charges))+(Weyl('N_L^c',1,1,Q(0),Q(1)),)


def anomaly_coefficients(fields):
    out={k:Q(0) for k in (
        'SU3^2-F','SU2^2-F','Y^2-F','Y-F^2','F^3','grav^2-F',
        'Y^3','grav^2-Y','SU3^2-Y','SU2^2-Y')}
    for x in fields:
        mult=x.d3*x.d2
        out['F^3']+=mult*x.F**3
        out['grav^2-F']+=mult*x.F
        out['Y^3']+=mult*x.Y**3
        out['grav^2-Y']+=mult*x.Y
        out['Y^2-F']+=mult*x.Y*x.Y*x.F
        out['Y-F^2']+=mult*x.Y*x.F*x.F
        if x.d3==3:
            out['SU3^2-F']+=Q(x.d2,2)*x.F
            out['SU3^2-Y']+=Q(x.d2,2)*x.Y
        if x.d2==2:
            out['SU2^2-F']+=Q(x.d3,2)*x.F
            out['SU2^2-Y']+=Q(x.d3,2)*x.Y
    return out


def multiply(anomalies,generations):
    if type(generations) is not int or generations < 0: raise ValueError('g>=0 integer')
    return {k:v*generations for k,v in anomalies.items()}


def with_singlets(fields,charges):
    return tuple(fields)+tuple(Weyl('singlet',1,1,Q(0),Q(c)) for c in charges)


def chiral_index(n,charge=1):
    if type(n) is not int or type(charge) is not int:
        raise TypeError('integer magnetic flux and charge')
    return n*charge
