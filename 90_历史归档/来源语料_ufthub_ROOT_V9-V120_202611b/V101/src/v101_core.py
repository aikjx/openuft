"""ROOT V101 | auditable consequences of classical radiation and knot curvature.

Every numerical orbit is THEORY. This does not establish quantum gravity,
four-force unification, autonomous self-sustained radiation, or a new force.
"""
from __future__ import annotations
import math
from pathlib import Path
import numpy as np
from scipy.constants import c, epsilon_0, e, m_e, mu_0


def gamma_beta(beta: float) -> float:
    if not (0 < beta < 1):
        raise ValueError('beta must be in (0, 1)')
    return 1.0/math.sqrt(1-beta*beta)


def radiation_coefficient(q_c:float, beta:float) -> float:
    """C in E_rad = C * integral(kappa^2 ds) [J*m]."""
    return q_c*q_c*gamma_beta(beta)**4*beta**3/(6*math.pi*epsilon_0)


def radiation_bounds(L:float, beta:float=.1, q_c:float=e,
                     total_curvature:float|None=None) -> dict:
    if L <= 0 or q_c == 0:
        raise ValueError('L and |q| must be positive')
    C=radiation_coefficient(q_c,beta)
    ordinary=C*4*math.pi**2/L
    knotted=C*16*math.pi**2/L
    result=dict(C_J_m=C, ordinary_closed_lower_J=ordinary,
                knotted_lower_J=knotted, knotted_over_ordinary=knotted/ordinary,
                knot_voltage_lower_V=knotted/abs(q_c),
                knot_mean_parallel_E_lower_V_m=knotted/(abs(q_c)*L))
    if total_curvature is not None:
        if total_curvature < 0:
            raise ValueError('curvature cannot be negative')
        result['known_total_curvature_lower_J']=C*total_curvature**2/L
    return result


def polygon_geometry(points:np.ndarray) -> dict:
    """Closed polygon approximation to length, total curvature and ∫κ²ds.

    N vertices are distinct samples at equal-ish parametric increments; last
    vertex is NOT an extra duplicate of the first. Uses exterior angles.
    Not an interval certificate of the smooth underlying curve.
    """
    p=np.asarray(points,dtype=float)
    if p.ndim!=2 or p.shape[1]!=3 or len(p)<10:
        raise ValueError('require at least 10 3D vertices')
    ds_vec=np.roll(p,-1,axis=0)-p
    ds=np.linalg.norm(ds_vec,axis=1)
    if ds.min()<=0:
        raise ValueError('zero edge length')
    t=ds_vec/ds[:,None]
    turning=np.arccos(np.clip((t*np.roll(t,1,axis=0)).sum(axis=1),-1,1))
    dual=.5*(ds+np.roll(ds,1))
    curvature=turning/dual
    L=float(ds.sum())
    K=float(turning.sum())
    K2=float(np.dot(curvature*curvature,dual))
    return dict(length_m=L, total_curvature=K, curvature_squared_integral_per_m=K2,
                min_curvature_per_m=float(curvature.min()),
                max_curvature_per_m=float(curvature.max()),
                cauchy_ratio=K2*L/(K*K), samples=len(p))


def torus_knot_polygon(P:int,Q:int,num:int=4000,R:float=.01,a:float=.002):
    if P<1 or Q<1 or math.gcd(P,Q)!=1 or not R>a>0:
        raise ValueError('expected coprime knot winding and R>a>0')
    t=np.linspace(0,2*math.pi,num,endpoint=False)
    rho=R+a*np.cos(Q*t)
    return np.column_stack((rho*np.cos(P*t),rho*np.sin(P*t),a*np.sin(Q*t)))


def circular_trajectory(num:int=1000,r:float=.01):
    t=np.linspace(0,2*math.pi,num,endpoint=False)
    return np.column_stack((r*np.cos(t),r*np.sin(t),np.zeros_like(t)))


def magnetic_degeneracy(beta:float=.1,r:float=.005,
                        C_T_m:float=1.e-4) -> dict:
    """Exact local vacuum field ambiguity on annulus r>0.

    B^(1)=B0 e_z; B^(2)=B0 e_z+(C/r)e_phi.
    Both have div=curl=0 in the annulus. For v=v e_phi, the new
    component is parallel to the orbit velocity and leaves q v×B unchanged.
    B0 set to sustain a circular negative charge trajectory.
    """
    if r<=0:
        raise ValueError('r must be positive')
    v=beta*c
    B0=gamma_beta(beta)*m_e*v/(e*r)
    phi=0.8
    er=np.array([math.cos(phi),math.sin(phi),0.])
    et=np.array([-math.sin(phi),math.cos(phi),0.])
    ez=np.array([0.,0.,1.])
    vel=v*et
    B1=B0*ez
    B2=B1+C_T_m/r*et
    F1=-e*np.cross(vel,B1)
    F2=-e*np.cross(vel,B2)
    ac=-gamma_beta(beta)*m_e*v*v/r*er
    return dict(B0_T=B0,Bparallel_added_T=C_T_m/r,
                force1_N=F1.tolist(),force2_N=F2.tolist(),
                centripetal_N=ac.tolist(),
                relative_force_ambiguity=float(np.linalg.norm(F1-F2)/np.linalg.norm(F1)),
                field_energy_density_difference_at_orbit_J_m3=float(((np.dot(B2,B2)-np.dot(B1,B1))/(2*mu_0))),
                equivalent_on_axis_current_A=float(2*math.pi*C_T_m/mu_0))


def compute_v100(input_csv: str|Path, baseline_json: str|Path) -> dict:
    import json
    points=np.loadtxt(input_csv,delimiter=',',skiprows=1)
    g=polygon_geometry(points)
    b=radiation_bounds(g['length_m'],.1,e,g['total_curvature'])
    C=b['C_J_m']
    rad_est=C*g['curvature_squared_integral_per_m']
    baseline=json.loads(Path(baseline_json).read_text(encoding='utf-8'))
    published=baseline['energy_loss_J_per_period']
    g.update(b)
    g.update(polygon_radiation_J=rad_est,
             historical_V100_radiation_J=published,
             independent_vs_historical_relative_error=abs(rad_est-published)/published,
             radiation_over_knot_floor=rad_est/b['knotted_lower_J'],
             radiation_over_curvature_floor=rad_est/b['known_total_curvature_lower_J'],
             required_energy_per_charge_V=published/e,
             minimum_avg_tangential_E_V_m=published/(e*g['length_m']),
             original_model_label='V100 classical prescribed trajectory; NOT a real experiment',
             knot_certification='NOT interval-certified for smooth continuum field; numerical polygon only')
    return g
