"""ROOT V68: auditable toy calculations; NOT a proven unified field theory.
All code: Python 3.10+, standard library unless optional crosschecks are explicitly enabled.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
import math

C = 299792458.0
HBAR = 1.054571817e-34
G_OBS = 6.67430e-11
MZ_GEV = 91.1876
EULER_GAMMA = 0.57721566490153286060651209008
ALPHA_EM_INV = 127.95  # approximate illustrative MSbar input, NOT an original measurement
SIN2_THETA_W = 0.23122
ALPHA_S = 0.118
BETA_SM = (41/10, -19/6, -7)


def helix(radius: float, angle_degrees: float, speed: float=C) -> dict:
    """r(t)=(R cos omega t, R sin omega t, u t); angle measured from transverse plane.
    Signed torsion uses omega>=0 and signed axial velocity u.
    """
    if not (math.isfinite(radius) and radius > 0 and math.isfinite(speed) and speed > 0):
        raise ValueError('radius and speed must be finite and positive')
    if not math.isfinite(angle_degrees) or abs(angle_degrees) > 90:
        raise ValueError('angle must be within [-90,90] degrees')
    angle = math.radians(angle_degrees)
    cs, sn = math.cos(angle), math.sin(angle)
    if abs(angle_degrees) == 90: cs = 0.0  # exact geometric degeneracy, avoid cos(pi/2) rounding
    omega = speed*cs/radius
    return {'omega':omega,'v_theta':speed*cs,'v_z':speed*sn,
            'kappa':cs*cs/radius,'tau':sn*cs/radius,
            'accel':speed*speed*cs*cs/radius,
            'speed':math.hypot(speed*cs,speed*sn)}


def helix_inverse(kappa: float, tau: float, speed: float=C) -> dict:
    if not (math.isfinite(kappa) and kappa > 0 and math.isfinite(tau) and math.isfinite(speed) and speed>0):
        raise ValueError('nondegenerate helix requires kappa>0, finite tau and positive speed')
    d = math.hypot(kappa,tau)
    return {'radius':kappa/d**2, 'omega':speed*d, 'angle_degrees':math.degrees(math.atan2(tau,kappa))}


def dimensional_obstruction() -> dict:
    """Solve b=-1 (M) and a+2b=3 (L); T requires a+b=2."""
    b=-1; a=3-2*b
    return {'a':a,'b':b,'time_required_sum':2,'time_derived_sum':a+b,
            'possible':a+b==2}


def expint_e1(x: float) -> float:
    """E1(x) for x>0: series for x<=1, modified Lentz continued fraction otherwise."""
    if not math.isfinite(x) or x <= 0:
        raise ValueError('E1 needs x>0')
    if x<=1.:
        term=1. # x^k/k! with positive sign, accumulate alternating / k
        total=0.
        for k in range(1,500):
            term*= -x/k
            add= -term/k
            total+=add
            if abs(add) < 1.e-16*max(1.,abs(total)):
                break
        return -EULER_GAMMA - math.log(x)+total
    b=x+1.; c=1e300; d=1./b; h=d
    for i in range(1,500):
        a=-i*i
        b+=2.
        den=a*d+b
        if abs(den)<1e-300: den=1e-300
        d=1./den
        c=b+a/c
        if abs(c)<1e-300: c=1e-300
        delta=c*d; h*=delta
        if abs(delta-1)<3e-15: break
    return h*math.exp(-x)


def heat_kernel_f(mu:float)->float:
    """F(mu)=exp(-mu^2)-mu^2 E1(mu^2)=int_1^inf exp(-mu²t)/t² dt.
    Cutoff-sensitive toy coefficient, not a regulator-independent prediction.
    """
    if not math.isfinite(mu) or mu<0:raise ValueError('mu nonnegative finite')
    if mu==0:return 1.0
    x=mu*mu
    if x>700:return 0.
    return max(0.,math.exp(-x)-x*expint_e1(x))


def induced_inv_g(n:int,xi:float,ell:float,mu:float=0, bare_inv_g:float=0.)->float:
    """1/G_eff=1/G_bare + N(1-6xi)hbar F(mu)/(12 pi c³ ell²).
    Valid ONLY for specified scalar proper-time-cutoff one-loop toy.
    """
    if isinstance(n,bool) or not isinstance(n,int) or n<=0:raise ValueError('N must be positive integer')
    if not (math.isfinite(xi) and math.isfinite(ell) and ell>0 and math.isfinite(bare_inv_g)):
        raise ValueError('invalid parameters')
    return bare_inv_g + n*(1.-6.*xi)*HBAR*heat_kernel_f(mu)/(12*math.pi*C**3*ell**2)


def induced_g(n:int,xi:float,ell:float,mu:float=0, bare_inv_g:float=0.)->float:
    inv=induced_inv_g(n,xi,ell,mu,bare_inv_g)
    if inv<=0:raise ValueError('unphysical nonpositive 1/G_eff in toy sector')
    return 1./inv


def reverse_fitted_length(n:int,xi:float,g:float=G_OBS)->float:
    """Fit length to G: NOT a prediction; massless and bare-free only."""
    if n<=0 or not math.isfinite(g) or g<=0 or not math.isfinite(xi) or xi>=1/6:
        raise ValueError('require N>0, G>0, xi<1/6')
    return math.sqrt(g*n*(1-6*xi)*HBAR/(12*math.pi*C**3))


def planck_length(g:float=G_OBS)->float:
    return math.sqrt(HBAR*g/C**3)


def alpha_inv_at_mz(alpha_em_inv:float=ALPHA_EM_INV,sin2:float=SIN2_THETA_W,alpha_s:float=ALPHA_S):
    if not (alpha_em_inv>0 and 0<sin2<1 and alpha_s>0):raise ValueError('positive couplings and 0<sin²<1')
    return (3/5*(1-sin2)*alpha_em_inv, sin2*alpha_em_inv, 1/alpha_s)


def rge_inv(mu_gev:float, inputs=None):
    if not math.isfinite(mu_gev) or mu_gev<=0: raise ValueError('mu>0')
    if inputs is None: inputs=alpha_inv_at_mz()
    t=math.log(mu_gev/MZ_GEV)
    return tuple(a-b/(2*math.pi)*t for a,b in zip(inputs,BETA_SM))


def pair_intersections(inputs=None)->dict:
    if inputs is None: inputs=alpha_inv_at_mz()
    out={}
    for i,j in [(0,1),(0,2),(1,2)]:
        t=2*math.pi*(inputs[i]-inputs[j])/(BETA_SM[i]-BETA_SM[j])
        out[f'{i+1}-{j+1}']=MZ_GEV*math.exp(t)
    return out


def best_meeting(inputs=None, max_mu:float=1e20)->dict:
    """Minimize sum of squared pairwise differences in inverse couplings over scale."""
    if inputs is None:inputs=alpha_inv_at_mz()
    bs=[-b/(2*math.pi) for b in BETA_SM]
    av=sum(inputs)/3; bv=sum(bs)/3
    num=sum((a-av)*(b-bv) for a,b in zip(inputs,bs))
    den=sum((b-bv)**2 for b in bs)
    t=max(0.,min(math.log(max_mu/MZ_GEV),-num/den))
    vals=[a+t*b for a,b in zip(inputs,bs)]
    return {'mu_GeV':MZ_GEV*math.exp(t),'inv_alphas':vals,'max_gap':max(vals)-min(vals),
            'rms_spread':math.sqrt(sum((v-sum(vals)/3)**2 for v in vals)/3)}


SM_WEYL = (
    ('Q',3,2,Fraction(1,6)),
    ('uc',3,1,Fraction(-2,3)),
    ('dc',3,1,Fraction(1,3)),
    ('L',1,2,Fraction(-1,2)),
    ('ec',1,1,Fraction(1,1)),
)

def anomaly_coefficients(spec=SM_WEYL):
    """All entries are left-handed Weyl reps; color multiplicities used for U(1) anomalies.
    The color anomaly coefficient is 2*3-1*3bar-1*3bar=0 in normalized units.
    """
    u1cube=sum((color*weak*y**3 for _,color,weak,y in spec),Fraction())
    mixed_grav=sum((color*weak*y for _,color,weak,y in spec),Fraction())
    su3u1=sum((weak*y*Fraction(1,2) for name,color,weak,y in spec if color==3),Fraction())
    su2u1=sum((color*y*Fraction(1,2) for name,color,weak,y in spec if weak==2),Fraction())
    return {'U1_cubed':u1cube,'gravity_squared_U1':mixed_grav,
            'SU3_squared_U1':su3u1,'SU2_squared_U1':su2u1,
            'SU2_doublets':sum(color for name,color,weak,y in spec if weak==2)}


def kk_one_form_component(A, dchi):
    """dy+k A dx with y'=y+k chi means A'=A-dchi."""
    return A-dchi


def yukawa_acc_factor(r:float,alpha:float,lam:float,q_source:float=1.,q_test:float=1.)->float:
    if not all(map(math.isfinite,(r,alpha,lam,q_source,q_test))) or r<=0 or lam<=0:
        raise ValueError('positive r, lambda and finite parameters required')
    z=r/lam
    return 1+alpha*q_source*q_test*(1+z)*math.exp(-z) if z < 740 else 1.


def eotvos_eta(r:float,alpha:float,lam:float,q_source:float,q_a:float,q_b:float)->float:
    a=yukawa_acc_factor(r,alpha,lam,q_source,q_a)
    b=yukawa_acc_factor(r,alpha,lam,q_source,q_b)
    if a+b==0:raise ValueError('undefined eta')
    return 2*(a-b)/(a+b)


def microscope_approx_envelope(n_sigma:float=2.)->float:
    """Simple conservative scale, NOT an exact experimental confidence interval."""
    return (1.5+n_sigma*math.hypot(2.3,1.5))*1e-15


def brans_dicke_gamma(omega:float)->float:
    if not math.isfinite(omega) or omega==-2:raise ValueError('invalid omega')
    return (1+omega)/(2+omega)


def model_ledger():
    return {'DERIVED':['helix geometry from explicit parametric curve',
                       'specified one-loop toy inverse-G cutoff expression',
                       'standard-model left-Weyl anomaly cancellations',
                       'SM one-loop running non-coincidence for supplied inputs',
                       '5D U(1) KK differential one-form covariance'],
            'NOT_DERIVED':['UV cutoff length and scalar species from ROOT postulates',
                           'measured G without experimental calibration',
                           'SU3xSU2xU1 and chiral spectrum from one helical field',
                           'UV-complete ghost-free unitary quantum gravity',
                           'novel experimentally detected deviation from GR+SM']}
