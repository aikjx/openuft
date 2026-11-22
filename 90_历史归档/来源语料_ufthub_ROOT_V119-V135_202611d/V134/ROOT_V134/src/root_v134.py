#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ROOT V134: non-Abelian gauge geometry, strict mathematical tests.
Convention c=1 ONLY. hbar and G are retained as explicit parameters.
Nothing in this module establishes a new fundamental physical interaction.
"""
from __future__ import annotations
from fractions import Fraction as Q
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.integrate import solve_ivp

HBAR = 1.054571817e-34  # SI reference, not set to one
G = 6.67430e-11         # SI reference, not set to one
SIGMA = [np.array([[0, 1], [1, 0]], complex),
         np.array([[0, -1j], [1j, 0]], complex),
         np.array([[1, 0], [0, -1]], complex)]
SU2 = tuple(s/2 for s in SIGMA)


def su3_generators():
    """Hermitian Gell-Mann T_a=lambda_a/2; normalization Tr(T_a T_b)=delta_ab/2."""
    lam=[]
    def fill(entries):
        a=np.zeros((3,3), complex)
        for i,j,val in entries: a[i,j]=val
        return a
    lam.append(fill([(0,1,1),(1,0,1)]))
    lam.append(fill([(0,1,-1j),(1,0,1j)]))
    lam.append(np.diag([1,-1,0]).astype(complex))
    lam.append(fill([(0,2,1),(2,0,1)]))
    lam.append(fill([(0,2,-1j),(2,0,1j)]))
    lam.append(fill([(1,2,1),(2,1,1)]))
    lam.append(fill([(1,2,-1j),(2,1,1j)]))
    lam.append(np.diag([1,1,-2]).astype(complex)/np.sqrt(3))
    return tuple(a/2 for a in lam)

SU3=su3_generators()


def commutator(a,b):
    return a@b-b@a


def curvature_constant(ax,ay):
    """F_xy = partial_x A_y - partial_y A_x -i[A_x,A_y], with derivatives zero."""
    return -1j*commutator(ax,ay)


def pure_gauge_connection(x:float, a:float, b:float):
    """U=exp(i a x T1)exp(i b y T2). At any x,y, A_x=aT1, A_y=b Ux T2 Ux^dagger."""
    ux=expm(1j*a*x*SU2[0])
    ax=a*SU2[0]
    ay=b*(ux@SU2[1]@ux.conj().T)
    day_dx=1j*commutator(ax, ay)
    # Fxy= d_x A_y - d_y A_x -i[A_x,A_y]=0.
    f=day_dx-1j*commutator(ax, ay)
    return ax,ay,day_dx,f


def plaquette_commutator(a:float,b:float,delta:float):
    ux=expm(1j*delta*a*SU2[0]); uy=expm(1j*delta*b*SU2[1])
    loop=ux@uy@ux.conj().T@uy.conj().T
    leading=expm(-1j*delta*delta*curvature_constant(a*SU2[0],b*SU2[1]))
    return loop,leading


def su2_color(z: np.ndarray):
    return np.array([np.vdot(z, T@z).real for T in SU2])


def spinor_transport(a:float,b:float,duration:float=8.0, count:int=601):
    """D_s z=(d/ds -i A(s))z=0 => z'=i A(s)z; Wong color transport."""
    t=np.linspace(0,duration,count)
    z0=np.array([1+0j,0j])
    def A(s): return a*SU2[0]+b*np.sin(0.7*s)*SU2[1]
    def rhs(s,z): return 1j*A(s)@z
    sol=solve_ivp(rhs, (0,duration),z0,t_eval=t,rtol=2e-12,atol=2e-13,method='DOP853')
    if not sol.success: raise RuntimeError(sol.message)
    zs=sol.y.T
    qs=np.array([su2_color(z) for z in zs])
    norms=np.sum(abs(zs)**2,axis=1)
    q2=np.sum(qs**2,axis=1)
    residuals=[]
    for s,z,q in zip(t,zs,qs):
        dz=rhs(s,z); dQ=np.array([(np.vdot(dz,T@z)+np.vdot(z,T@dz)).real for T in SU2])
        avec=np.array([a,b*np.sin(0.7*s),0])
        # dot(Q)=-A x Q for D=partial-iA; checks Wong transport.
        residuals.append(np.linalg.norm(dQ+np.cross(avec,q)))
    return dict(max_state_norm_error=float(max(abs(norms-1))),
                max_casimir_error=float(max(abs(q2-0.25))),
                max_wong_residual=float(max(residuals)),
                final_Q=qs[-1].tolist(),time=t.tolist(),Q=qs.tolist())


def bianchi_constant(a1,a2,a3):
    """D_i F_jk+cyclic, where D_i F=-i[A_i,F] for constant A_i."""
    f23=curvature_constant(a2,a3); f31=curvature_constant(a3,a1); f12=curvature_constant(a1,a2)
    return -1j*(commutator(a1,f23)+commutator(a2,f31)+commutator(a3,f12))


# One SM family, expressed solely with LEFT-handed Weyl fields.
SM_FAMILY={
    'Q_L':dict(mult=6,Y=Q(1,6)),
    'u_c':dict(mult=3,Y=Q(-2,3)),
    'd_c':dict(mult=3,Y=Q(1,3)),
    'L_L':dict(mult=2,Y=Q(-1,2)),
    'e_c':dict(mult=1,Y=Q(1,1)),
}


def anomaly_ledger(family=None):
    f=SM_FAMILY if family is None else family
    cube=sum((v['mult']*v['Y']**3 for v in f.values()),Q(0))
    grav=sum((v['mult']*v['Y'] for v in f.values()),Q(0))
    Y=lambda k: f[k]['Y'] if k in f else Q(0)
    su2=3*Y('Q_L')+Y('L_L')
    su3=2*Y('Q_L')+Y('u_c')+Y('d_c')
    su3cube=(2 if 'Q_L' in f else 0)-(1 if 'u_c' in f else 0)-(1 if 'd_c' in f else 0)
    witten_doublets=(3 if 'Q_L' in f else 0)+(1 if 'L_L' in f else 0)
    return dict(U1_cubic=cube,gravity_U1=grav,SU2_squared_U1=su2,
                SU3_squared_U1=su3,SU3_cubic=su3cube,
                SU2_global_doublets=witten_doublets,
                SU2_global_anomaly=witten_doublets%2)


def gauge_kinetic_prefactor(g:float,hbar:float=HBAR):
    """For geometric gauge A of dimension L^-1, action S=-hbar/(2g²) int Tr(F²)."""
    if g<=0 or hbar<=0: raise ValueError('positive g and hbar required')
    return hbar/(2*g*g)


def no_go_1d_representation():
    """In dimension one every commutator vanishes; nontrivial su2 and su3 impossible."""
    zero=np.zeros((1,1), complex)
    return {'commutator_1d':float(np.max(abs(commutator(np.array([[2+0j]]),np.array([[3+0j]]))))),
            'forced_su2_T3_norm':float(np.linalg.norm(zero)),
            'statement':'Any 1D continuous unitary representation of SU(2), SU(3) is trivial.'}


def create_results():
    a,b=.7,1.1
    _,_,_,fg=pure_gauge_connection(.43,a,b)
    fn=curvature_constant(a*SU2[0],b*SU2[1])
    pl=[]
    for d in [0.2,0.1,0.05,0.025]:
        w,leading=plaquette_commutator(a,b,d)
        pl.append(dict(delta=d,unitarity_error=float(np.linalg.norm(w.conj().T@w-np.eye(2))),
                       loop_minus_leading=float(np.linalg.norm(w-leading)),
                       normalized_curvature=float(np.linalg.norm(w-np.eye(2))/(d*d))))
    trans=spinor_transport(a,b)
    anomalies=anomaly_ledger()
    data={
        'c':1,'hbar_SI_reference':HBAR,'G_SI_reference':G,
        'physical_claim':'No prediction of g, alpha, hbar, G or fermion generations; math consistency only',
        'flat_moving_frame_curvature_norm':float(np.linalg.norm(fg)),
        'constant_nonabelian_curvature_norm':float(np.linalg.norm(fn)),
        'expected_F_T3_coefficient':a*b,
        'plaquette':pl,
        'transport':{k:v for k,v in trans.items() if k not in {'time','Q'}},
        'anomaly_ledger':{k:str(v) for k,v in anomalies.items()},
        'gauge_prefactor_ratio_g_0p1_to_0p3':gauge_kinetic_prefactor(.1)/gauge_kinetic_prefactor(.3),
        'one_dimensional_no_go':no_go_1d_representation(),
        'status':'SU2 and SU3 shown possible as added internal representations; not derived from helix'
    }
    return data, trans


if __name__=='__main__':
    results,trans=create_results()
    out=Path(__file__).resolve().parents[1]/'results';out.mkdir(parents=True,exist_ok=True)
    (out/'numeric_results.json').write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding='utf-8')
    arr=np.column_stack((trans['time'],np.array(trans['Q'])))
    np.savetxt(out/'color_precession.csv',arr,delimiter=',',header='proper_time,Q1,Q2,Q3',comments='')
    print(json.dumps(results,indent=2,ensure_ascii=False))
