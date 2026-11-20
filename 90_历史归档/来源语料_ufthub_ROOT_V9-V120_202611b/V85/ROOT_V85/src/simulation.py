"""Synthetic-only matrix simulations and analysis; noise is not real observational data."""
import math, random
from .physics import normalized_material_difference


def exact_factor_matrix(sources, pairs, alpha, lam):
    """sources iterable (qsource, r, radius); pairs iterable (qi,qj)."""
    return [[normalized_material_difference(qs,qi,qj,alpha,r,lam,rad)
             for qi,qj in pairs] for qs,r,rad in sources]


def two_mediator_matrix(sources, pairs, alpha1,lam1,alpha2,lam2):
    """Two independent charge channels; qsource and qtest given in different tuples."""
    one=exact_factor_matrix([(a[0],a[2],a[3]) for a in sources],
                            [(p[0],p[1]) for p in pairs],alpha1,lam1)
    two=exact_factor_matrix([(a[1],a[2],a[3]) for a in sources],
                            [(p[2],p[3]) for p in pairs],alpha2,lam2)
    return [[a+b for a,b in zip(x,y)] for x,y in zip(one,two)]


def gaussian_noisy(matrix, sigma, seed=20261118):
    rng=random.Random(seed)
    return [[x+rng.gauss(0,sigma) for x in row] for row in matrix]


def singular_values(matrix):
    import numpy as np
    return [float(v) for v in np.linalg.svd(np.array(matrix,float),compute_uv=False)]


def illustrative_threshold_for_MICROSCOPE(charge_product=1.0):
    from .physics import conservative_95_eta_bound
    if charge_product==0: return math.inf
    return conservative_95_eta_bound()/abs(charge_product)
