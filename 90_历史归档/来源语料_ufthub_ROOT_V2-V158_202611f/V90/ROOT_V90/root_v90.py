"""ROOT V90 small reproducibility toolkit. Standard library only."""
import math

def make_weight_matrix(a1, a2, a3):
    """Return w solving w^T a1=0, w^T a2=0, w^T a3=1 for 3x3 A.

    The vectors are columns of A. Gaussian elimination is used to solve
    A^T w = [0, 0, 1]. Raises ValueError if singular.
    """
    n = len(a1)
    if n != 3 or len(a2) != 3 or len(a3) != 3:
        raise ValueError("This demo requires three 3-component basis vectors.")
    M = [[a1[i], a2[i], a3[i]] for i in range(3)]
    # Solve M^T w = e3.
    MT = [[M[j][i] for j in range(3)] for i in range(3)]
    b = [0.0, 0.0, 1.0]
    for k in range(3):
        pivot = max(range(k, 3), key=lambda r: abs(MT[r][k]))
        if abs(MT[pivot][k]) < 1e-14:
            raise ValueError("Singular/near-singular basis.")
        MT[k], MT[pivot] = MT[pivot], MT[k]
        b[k], b[pivot] = b[pivot], b[k]
        piv = MT[k][k]
        MT[k] = [v/piv for v in MT[k]]
        b[k] /= piv
        for r in range(3):
            if r != k:
                f = MT[r][k]
                MT[r] = [MT[r][c]-f*MT[k][c] for c in range(3)]
                b[r] -= f*b[k]
    return b

def weighted_variance(w, sigma):
    """w^T Sigma w; Sigma supplied as a square matrix."""
    return sum(w[i]*sigma[i][j]*w[j] for i in range(len(w)) for j in range(len(w)))

def phase_delta(m1, m2, r00, r01, r10, r11, duration, G, hbar):
    """Branch-combination Newton phase in SI, fixed distances and duration."""
    if min(r00, r01, r10, r11) <= 0 or duration < 0:
        raise ValueError("Distances must be positive and duration nonnegative.")
    V=lambda r: -G*m1*m2/r
    return (V(r00)+V(r11)-V(r01)-V(r10))*duration/hbar

def relative_residual(target, nuisance):
    """Norm of target after orthogonal projection onto nuisance columns.

    target: list; nuisance: list of column vectors (each same length).
    """
    # Gram-Schmidt orthogonalization, then subtract projections.
    v=[float(x) for x in target]
    orth=[]
    for col in nuisance:
        u=[float(x) for x in col]
        for q in orth:
            dot=sum(u[i]*q[i] for i in range(len(u)))
            u=[u[i]-dot*q[i] for i in range(len(u))]
        norm=math.sqrt(sum(x*x for x in u))
        if norm>1e-14:
            orth.append([x/norm for x in u])
    for q in orth:
        dot=sum(v[i]*q[i] for i in range(len(v)))
        v=[v[i]-dot*q[i] for i in range(len(v))]
    return math.sqrt(sum(x*x for x in v))
