"""ROOT V90 reproducible illustrative point-mass branch phase model. SI values.
No claim that the separate potential terms are gauge-invariant observables.
"""
import math
G=6.67430e-11
HBAR=1.054571817e-34
C=299792458.0
KQ=41/(10*math.pi)

def second_difference(f,r,delta):
    return f(r)-2*f(r+delta)+f(r+2*delta)

def phase_terms(m=1e-14,r=2e-4,delta=1e-5,t=1.0):
    """Identical masses; branches with distances r,r+d,r+d,r+2d.
    PN coefficient 6 is illustrative for equal masses; not a universal 1PN observable.
    """
    if min(m,r,delta,t)<=0: raise ValueError('all parameters must be positive')
    a=G*m*m*t/HBAR
    fN=lambda x: 1/x
    fPN=lambda x: (6*G*m/C**2)/x**2
    fQ=lambda x: (KQ*G*HBAR/C**3)/x**3
    return {'newton_rad':a*second_difference(fN,r,delta),
            'pn_illustrative_rad':a*second_difference(fPN,r,delta),
            'eft_illustrative_rad':a*second_difference(fQ,r,delta)}

def weights(radii):
    """Weights null 1/r and 1/r², normalize response to 1/r³ to unity."""
    import numpy as np
    rr=np.asarray(radii,float)
    if len(rr)!=3 or np.any(rr<=0) or len(set(rr))!=3: raise ValueError('3 distinct positive radii required')
    a=np.array([[1/x for x in rr],[1/x**2 for x in rr],[1/x**3 for x in rr]])
    return np.linalg.solve(a,np.array([0.,0.,1.]))

def diagnostic(radii,observations):
    import numpy as np
    return float(weights(radii)@np.asarray(observations,float))
