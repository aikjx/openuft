"""ROOT V102. Conditional classical Lorentz/Frenet/Lienard consequences.

NOT a proof of unification, quantum gravity, or a new force.
"""
from __future__ import annotations
import math
import numpy as np
from scipy.constants import c, epsilon_0, e, m_e


def gamma(beta: float) -> float:
    if not 0.0 < beta < 1.0:
        raise ValueError("beta must lie strictly between 0 and 1")
    return (1.0 - beta**2) ** (-0.5)


def orbit_prefactor(beta: float, mass: float = m_e, charge: float = e) -> float:
    """T*m = (gamma*m*v/|q|), magnetic strength / curvature."""
    if not mass > 0 or not abs(charge) > 0:
        raise ValueError("mass and |charge| must be positive")
    return gamma(beta) * mass * beta*c / abs(charge)


def curvature_from_polygon(points: np.ndarray) -> dict:
    """Discrete closed polygon: no last=end-point duplicate permitted."""
    p=np.asarray(points,float)
    if p.ndim!=2 or p.shape[1]!=3 or len(p)<20 or not np.isfinite(p).all():
        raise ValueError("finite Nx3 points, N>=20 required")
    ds_vec=np.roll(p,-1,axis=0)-p
    ds=np.linalg.norm(ds_vec,axis=1)
    if np.min(ds)<=0: raise ValueError("duplicate consecutive vertex")
    t=ds_vec/ds[:,None]
    cosang=np.clip((t*np.roll(t,1,axis=0)).sum(axis=1),-1.0,1.0)
    ang=np.arccos(cosang)
    dual=.5*(ds+np.roll(ds,1))
    kappa=ang/dual
    L=float(ds.sum()); K=float(ang.sum()); K2=float(np.dot(kappa*kappa,dual))
    return {"length_m":L,"total_curvature":K,"curvature_squared_integral_inv_m":K2,
            "kappa_per_m":kappa,"dual_lengths_m":dual,
            "cum_arc_m":np.cumsum(ds)-.5*ds,"min_kappa":float(np.min(kappa)),
            "max_kappa":float(np.max(kappa)),"point_count":len(p)}


def field_and_radiation(geometry: dict, beta=.1, mass=m_e, charge=e) -> dict:
    L,K,K2=(geometry[k] for k in ("length_m","total_curvature","curvature_squared_integral_inv_m"))
    if L<=0 or K2<0 or K<0: raise ValueError("bad geometric integrals")
    fac=orbit_prefactor(beta,mass,charge)
    Bavg=fac*K/L
    Brms=fac*math.sqrt(K2/L)
    variance=max(0.0,Brms**2-Bavg**2)
    Cv2=K2*L/K**2-1 if K>0 else float('nan')
    C=(charge**2*gamma(beta)**4*beta**3)/(6*math.pi*epsilon_0)
    # Exact conditional re-expression via B_perp(s) [tesla]:
    C_B=(charge**4*gamma(beta)**2*(beta*c))/(6*math.pi*epsilon_0*mass**2*c**3)
    E_kappa=C*K2
    E_field=C_B*(fac**2*K2)
    return {"beta":beta,"gamma":gamma(beta),"length_m":L,"K":K,"K2_inv_m":K2,
            "field_factor_T_m":fac,"B_mean_T":Bavg,"B_rms_T":Brms,
            "B_sd_T":math.sqrt(variance),"B_cv":math.sqrt(max(Cv2,0.0)),
            "B_knot_lower_T":fac*(4*math.pi)/L,
            "B_closed_lower_T":fac*(2*math.pi)/L,
            "B_rms_over_knot_floor":Brms/(fac*4*math.pi/L),
            "Cauchy_ratio":K2*L/K**2,
            "E_rad_from_kappa_J":E_kappa,
            "E_rad_from_B_J":E_field,
            "E_K_only_lower_J":C*K*K/L,
            "E_knot_lower_J":C*(4*math.pi)**2/L,
            "E_Cauchy_gap_J":E_kappa-C*K*K/L,
            "radiation_identity_relative":abs(E_field-E_kappa)/E_kappa,
            "B_profile_T":(fac*geometry['kappa_per_m']).tolist()}


def torus_knot(P:int,Q:int,R=.01,a=.002,num=5000) -> np.ndarray:
    if P<1 or Q<1 or math.gcd(P,Q)!=1 or R<=a or a<=0: raise ValueError("invalid torus geometry")
    s=np.arange(num)*2*math.pi/num
    rho=R+a*np.cos(Q*s)
    return np.column_stack([rho*np.cos(P*s),rho*np.sin(P*s),a*np.sin(Q*s)])


def circle(radius=.01,num=1000) -> np.ndarray:
    theta=np.arange(num)*2*math.pi/num
    return np.column_stack([radius*np.cos(theta),radius*np.sin(theta),np.zeros_like(theta)])


def local_required_B(tangent, normal, curvature:float, beta=.1, q=-e,
                     mass=m_e, B_longitudinal=0.) -> np.ndarray:
    """Algebraic required B at one point of curve, NOT a global Maxwell solution."""
    t=np.array(tangent,float); n=np.array(normal,float)
    if abs(q)<=0 or mass<=0 or curvature<0: raise ValueError("invalid parameters")
    if not np.isclose(t@t,1,atol=1e-10) or not np.isclose(n@n,1,atol=1e-10) or not np.isclose(n@t,0,atol=1e-10):
        raise ValueError("Frenet tangent and normal must be orthonormal")
    fac_signed=gamma(beta)*mass*(beta*c)/q
    binormal=np.cross(t,n)
    return -(fac_signed*curvature)*binormal+B_longitudinal*t


def local_force_error(tangent, normal, curvature, B, beta=.1, q=-e, mass=m_e) -> float:
    t=np.asarray(tangent,float); n=np.asarray(normal,float); B=np.asarray(B,float)
    v=beta*c
    f_expected=gamma(beta)*mass*v*v*curvature*n
    f_lorentz=q*np.cross(v*t,B)
    return float(np.linalg.norm(f_expected-f_lorentz)/(np.linalg.norm(f_expected)+1e-300))


def recover_components(tangent, normal, B) -> dict:
    t=np.asarray(tangent,float); n=np.asarray(normal,float); b=np.cross(t,n)
    B=np.asarray(B,float)
    return {"B_parallel_T":float(B@t),"B_binormal_T":float(B@b),"B_normal_T":float(B@n)}
