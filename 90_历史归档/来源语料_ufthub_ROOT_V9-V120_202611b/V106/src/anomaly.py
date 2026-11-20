"""Exact rational Standard Model single generation anomaly checks; not an origin derivation."""
from fractions import Fraction as Q
from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class Weyl:
    name: str
    color_dim: int
    weak_dim: int
    y: Q
    color_anti: bool=False

STATES: Tuple[Weyl,...] = (
    Weyl('Q_L',3,2,Q(1,6)),
    Weyl('u^c_L',3,1,Q(-2,3),True),
    Weyl('d^c_L',3,1,Q(1,3),True),
    Weyl('L_L',1,2,Q(-1,2)),
    Weyl('e^c_L',1,1,Q(1,1)),
)

def anomaly_coefficients(states=STATES):
    c3 = sum(w.weak_dim * (-1 if w.color_anti else 1) for w in states if w.color_dim==3)
    c3c3y = sum(Q(w.weak_dim,2)*w.y for w in states if w.color_dim==3)
    c2c2y = sum(Q(w.color_dim,2)*w.y for w in states if w.weak_dim==2)
    y3 = sum(w.color_dim*w.weak_dim*w.y**3 for w in states)
    grav_y = sum(w.color_dim*w.weak_dim*w.y for w in states)
    doublets = sum(w.color_dim for w in states if w.weak_dim==2)
    return {'SU3^3':c3,'SU3^2-U1':c3c3y,'SU2^2-U1':c2c2y,
            'U1^3':y3,'grav^2-U1':grav_y,'SU2_doublets':doublets,
            'Witten_SU2_obstruction':doublets%2}


def su5_hypercharge_generator():
    return tuple([Q(-1,3)]*3 + [Q(1,2)]*2)


def su5_normalization():
    eig=su5_hypercharge_generator()
    trace=sum(eig)
    trace2=sum(x*x for x in eig)
    # canonical T= sqrt(3/5)*Y5 has Tr(T²)=1/2.
    return {'trace':trace,'trace_Y_squared':trace2, 'normalization_squared':Q(3,5),
            'normalized_trace_squared':Q(3,5)*trace2}
