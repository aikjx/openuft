"""Illustrative 4D anomalies for a proposed gauged U(1)_F.

All LEFT-handed Standard Model Weyl representations, including conjugates,
are assigned family charge +1. This is a conditional toy assignment, NOT a
claim about a compulsory anomaly in every flux compactification.
"""
from fractions import Fraction

# (representation name, SU(3) dimension, SU(2) dimension, hypercharge Y)
REPS = (
    ('Q_L', 3, 2, Fraction(1,6)),
    ('u_L^c', 3, 1, Fraction(-2,3)),
    ('d_L^c', 3, 1, Fraction(1,3)),
    ('L_L', 1, 2, Fraction(-1,2)),
    ('e_L^c', 1, 1, Fraction(1)),
)


def index(q: int, n: int) -> int:
    if type(q) is not int or type(n) is not int:
        raise TypeError('integrally quantized charges and flux required')
    return q*n


def zero_mode_count(q: int, n: int) -> int:
    return abs(index(q,n))


def anomalies_U1F(generations: int, family_charge: int = 1) -> dict[str, Fraction]:
    if type(generations) is not int or generations < 0:
        raise ValueError('nonnegative integer number of generations')
    q = Fraction(family_charge)
    f3 = Fraction(0)
    fgr = Fraction(0)
    su3su3f = Fraction(0)
    su2su2f = Fraction(0)
    y2f = Fraction(0)
    for _name,d3,d2,y in REPS:
        mult = d3*d2
        f3 += mult*q**3
        fgr += mult*q
        y2f += mult*y**2*q
        if d3 == 3:
            su3su3f += d2*Fraction(1,2)*q
        if d2 == 2:
            su2su2f += d3*Fraction(1,2)*q
    return {
        'F^3': f3*generations,
        'grav^2 F': fgr*generations,
        'SU3^2 F': su3su3f*generations,
        'SU2^2 F': su2su2f*generations,
        'Y^2 F': y2f*generations,
    }


def sm_hypercharge_anomalies_per_generation() -> dict[str, Fraction]:
    cubic = sum((d3*d2*y**3 for _,d3,d2,y in REPS), Fraction())
    mixed_grav = sum((d3*d2*y for _,d3,d2,y in REPS), Fraction())
    su3 = sum((d2*Fraction(1,2)*y for _,d3,d2,y in REPS if d3==3), Fraction())
    su2 = sum((d3*Fraction(1,2)*y for _,d3,d2,y in REPS if d2==2), Fraction())
    return {'Y^3': cubic, 'grav^2 Y': mixed_grav, 'SU3^2 Y': su3, 'SU2^2 Y':su2}
