"""Independently testable toy models. No prediction of G or new-force discovery.
Units: SI unless *_gev variables, which are in GeV in natural units.
"""
from __future__ import annotations
import itertools
import math
from dataclasses import dataclass
import numpy as np

C = 299_792_458.0
HBAR = 1.054571817e-34
G_OBS = 6.67430e-11
G_STD = 1.5e-15 + 1.96*math.hypot(2.3e-15,1.5e-15)  # conservative illustration
MPL_REDUCED_GEV = 2.435e18  # rounded reference, NOT an independent prediction
EARTH_R = 6_371_000.0


def helix_parameters(radius: float, omega: float, axial: float):
    if radius<=0: raise ValueError('radius must be positive')
    speed=math.hypot(radius*omega, axial)
    if speed<=0: raise ValueError('zero speed')
    kappa=radius*omega*omega/(speed*speed)
    torsion=axial*omega/(speed*speed)
    return {'speed':speed,'curvature':kappa,'torsion':torsion,
            'acceleration':radius*omega*omega, 'pitch_per_turn':2*math.pi*axial/abs(omega) if omega else math.inf}


def scale_from_rg(mu_gev: float, g: float, b0: float=7.0) -> float:
    """One-loop dimensional transmutation Lambda=mu exp(-8pi²/(b0*g²))."""
    if min(mu_gev,g,b0)<=0: raise ValueError('positive parameters required')
    return mu_gev*math.exp(-8*math.pi**2/(b0*g*g))


def coupling_for_scale(mu_gev: float, target_gev: float,b0:float=7.0)->float:
    if not 0<target_gev<mu_gev: raise ValueError('0 < target < mu')
    return math.sqrt(8*math.pi**2/(b0*math.log(mu_gev/target_gev)))


def rg_beta(g:float,b0:float=7.0)->float:
    return -b0*g**3/(16*math.pi**2)


def rg_scale_sensitivity(g:float,b0:float=7.0)->float:
    """d ln(Lambda)/dg (dimensionless g), fixed mu,b0."""
    return 16*math.pi**2/(b0*g**3)


def inferred_species_count(cutoff_gev:float, mp_reduced_gev:float=MPL_REDUCED_GEV)->float:
    """Conditional one-loop induced-gravity toy model Mbar_P²=N*LambdaUV²/(96pi²)."""
    return 96*math.pi**2*(mp_reduced_gev/cutoff_gev)**2


def grav_dimensional_residual(a:float,b:float):
    """Exponents for c^a*hbar^b against G dimensions (L^3 M^-1 T^-2)."""
    return np.array([a+2*b-3,b+1,-a-b+2],dtype=float)


def _uniform_sphere_scaled(x:float)->float:
    """S(x)=3(x cosh x-sinh x)exp(-x)/x^3. Stable small/large x."""
    if x < 0: raise ValueError('negative radius/range')
    if x < .12:
        # F(x)=1+x²/10+x⁴/280+x⁶/15120+x⁸/1330560+...
        xx=x*x
        F=1+xx*(1/10+xx*(1/280+xx*(1/15120+xx/1330560)))
        return F*math.exp(-x)
    return 1.5*((x-1)+(x+1)*math.exp(-2*x))/(x**3)


def uniform_yukawa_factor(radius:float, lam:float, altitude:float=0.0)->float:
    """Outer acceleration shape (gY/gN)/alpha for uniform ball, no source/test charge factors."""
    if radius<=0 or lam<=0 or altitude<0:raise ValueError('invalid geometry')
    x=radius/lam
    z=altitude/lam
    return _uniform_sphere_scaled(x)*(1+x+z)*math.exp(-z)


def point_yukawa_factor(radius:float,lam:float,altitude:float=0.0)->float:
    if min(radius,lam)<=0 or altitude<0:raise ValueError('invalid geometry')
    y=(radius+altitude)/lam
    return (1+y)*math.exp(-y)


def _primitive_fofx(x:float)->float:
    """x cosh(x)-sinh(x), evaluated in moderately sized x (<= 300 for our tests)."""
    if abs(x)<.03:
        return x**3/3 + x**5/30 + x**7/840 + x**9/45360
    return x*math.cosh(x)-math.sinh(x)


def layered_yukawa_factor(radius:float,lam:float,layers:list[tuple[float,float,float]],altitude:float=0.0)->float:
    """layers (inner_radius, outer_radius, mass_density), sorted contiguous, outermost=radius.
       Valid for moderate x<300 (sufficient for package's scanned range).
    """
    if radius<=0 or lam<=0 or altitude<0:raise ValueError('invalid geometry')
    if not layers or abs(layers[0][0])>radius*1e-12 or abs(layers[-1][1]-radius)>radius*1e-10:
        raise ValueError('layers must span 0..radius')
    mass_norm=0.0; weighted=0.0; prev=0
    X=radius/lam
    def scaled_primitive(x):
        return .5*((x-1)*math.exp(x-X)+(x+1)*math.exp(-x-X))
    for inner,outer,rho in layers:
        if rho<=0 or outer<=inner or abs(inner-prev)>radius*1e-11:raise ValueError('invalid layers')
        mass_norm+=rho*(outer**3-inner**3)/3
        if X>=250:
            weighted+=rho*lam**3*(scaled_primitive(outer/lam)-scaled_primitive(inner/lam))
        else:
            weighted+=rho*lam**3*(_primitive_fofx(outer/lam)-_primitive_fofx(inner/lam))
        prev=outer
    return (weighted/mass_norm) * (1+(radius+altitude)/lam)*math.exp(-altitude/lam if X>=250 else -(radius+altitude)/lam)


def earth_two_layer_model(core_fraction:float=.546, mantle_density:float=4500.0):
    """Returns two-layer Earth with same total mass as uniform reference g/rho, for controlled comparison."""
    R=EARTH_R; rho_mean=5513.4
    Rc=R*core_fraction
    rho_core=(rho_mean*R**3 - mantle_density*(R**3-Rc**3))/Rc**3
    return [(0.,Rc,rho_core),(Rc,R,mantle_density)]


def charge_fraction(Z:float,atomic_weight:float)->float:
    """Z/A is ONLY a simple phenomenological source-charge proxy."""
    if Z<=0 or atomic_weight<=0: raise ValueError('invalid material')
    return Z/atomic_weight


def eotvos_alpha_bound(lam:float,source_charge:float=.5,eta_limit:float=G_STD)->float:
    """Illustrative conditional bound for alpha in a composition-dependent Yukawa toy model."""
    qTi=charge_fraction(22,47.867)
    qPt=charge_fraction(78,195.084)
    difference=abs(qTi-qPt)
    f=uniform_yukawa_factor(EARTH_R,lam)
    return eta_limit/(source_charge*difference*f)


def sign_states():
    return list(itertools.product((-1,1),repeat=3))


def hadamard_design():
    """Columns: 1,H,R,S,HR,HS,RS,HRS. All rows represent fully crossed signs."""
    return np.array([[1,h,r,s,h*r,h*s,r*s,h*r*s] for h,r,s in sign_states()],dtype=float)


def triple_contrast(observations):
    """Simple eight-state fully balanced estimate. Observations in sign_states() order."""
    y=np.asarray(observations,dtype=float)
    if y.shape!=(8,):raise ValueError('eight measurements required')
    return float((hadamard_design()[:,-1]@y)/8)


def generate_eight_states(coefficients, noise_sigma:float=0,seed:int=73):
    coef=np.asarray(coefficients,dtype=float)
    if coef.shape!=(8,):raise ValueError('eight coefficients required')
    rng=np.random.default_rng(seed)
    return hadamard_design()@coef+rng.normal(0,noise_sigma,size=8)


def fit_cross_env(X,contrasts):
    """d_e = nuisance_constant + beta*X_e, OLS design and condition diagnostics."""
    x=np.asarray(X,float); y=np.asarray(contrasts,float)
    if len(x)!=len(y) or len(x)<2:raise ValueError('at least 2 matched environments')
    design=np.column_stack([np.ones(len(x)),x])
    rank=int(np.linalg.matrix_rank(design))
    if rank<2: return {'rank':rank,'beta':None,'nuisance':None,'condition_number':math.inf}
    coeff=np.linalg.lstsq(design,y,rcond=None)[0]
    return {'rank':rank,'beta':float(coeff[1]),'nuisance':float(coeff[0]),
            'condition_number':float(np.linalg.cond(design))}


def dimensional_scale_hierarchy(uv_gev:float=2.435e18, ir_gev:float=.2, b0:float=7.):
    """Calibrated one-loop exercise, NOT a prediction of either scale."""
    g=coupling_for_scale(uv_gev,ir_gev,b0)
    return {'uv_GeV':uv_gev,'ir_GeV':ir_gev,'g_uv_fitted':g,'alpha_uv_fitted':g*g/(4*math.pi),
            'log_hierarchy':math.log(uv_gev/ir_gev),
            'species_for_IR_as_gravity_cutoff':inferred_species_count(ir_gev)}


def abelian_axion_bulk_correction(axion_gradient:float, magnetic_field:float,coupling:float):
    """An illustrative magnitude proportional to (∂a) · dual(F), zero for constant a.
       Not an SI Maxwell current; arbitrary normalized toy units.
    """
    return coupling*axion_gradient*magnetic_field
