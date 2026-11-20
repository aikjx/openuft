"""Proper energy / Pphi reduced event-map linearization.

Two tangent vectors evolved jointly with the physical 6D ODE. Event-time
correction removes flow-direction displacement. Pphi held fixed by solving
initial-radius implicit function. No stability certification claimed.
"""
import json, math
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.constants import m_e,e,c
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from coil_model import TwoCoilField, circular_reference,normalized_rhs
from v97_core import radial_max_event


def prepare(seed,source_order=21,flux_quad=50):
    r0=seed['orbit']['reference_radius_m'];z0=seed['conditions']['initial_vertical_amplitude_m'];
    ar=seed['conditions']['initial_radial_amplitude_m'];beta=seed['conditions']['beta']
    v=beta*c;gamma=1/math.sqrt(1-beta*beta);q=-e
    field=TwoCoilField(order=source_order)
    circular_reference(field=field,beta=beta,r0=r0)
    r_init=r0+ar
    nodes,ws=leggauss(flux_quad)
    def flux(r,z):
        rho=(nodes+1)*r*.5
        _,Bz=field.field(rho,np.full_like(rho,z))
        return float(.5*r*np.dot(ws,rho*Bz))
    P=gamma*m_e*r_init*v+q*flux(r_init,z0)
    def ini(z_n,vz_n):
        z=z_n*r0;vz=vz_n*v
        vt=math.sqrt(v*v-vz*vz)
        def eq(r):return gamma*m_e*r*vt+q*flux(r,z)-P
        r=brentq(eq,r_init-5e-5,r_init+5e-5,xtol=8e-16)
        return np.array([r/r0,0.,z_n,0.,vt/v,vz_n])
    Br,Bz=field.field(r_init,z0)
    drdz=q*r_init*Br/(gamma*m_e*v+q*r_init*Bz)
    y0=ini(z0/r0,0.)
    return dict(field=field,r0=r0,beta=beta,initial=y0,drdz=drdz,flux=flux,
        init_on_section=ini,canonical_angular_momentum=P)


def section_map(model, coords, rtol=2e-12):
    y0=model['init_on_section'](*coords)
    sol=solve_ivp(normalized_rhs,(0,35),y0,args=(model['field'],model['beta'],model['r0']),
        method='DOP853',events=radial_max_event,rtol=rtol,atol=rtol/40,max_step=.25)
    if not sol.success:raise RuntimeError(sol.message)
    events=[(t,y) for t,y in zip(sol.t_events[0],sol.y_events[0]) if t>1e-6]
    if len(events)<4:raise RuntimeError('insufficient radial maxima')
    tm,last=events[3]
    return np.array([last[2],last[5]]),tm


def reduced_finite_difference(model,h=1e-5,rtol=3e-12):
    u=np.array([model['initial'][2],0.])
    center,T=section_map(model,u,rtol=rtol)
    J=np.empty((2,2))
    for j in range(2):
        off=np.zeros(2);off[j]=h
        plus=section_map(model,u+off,rtol=rtol)[0]
        minus=section_map(model,u-off,rtol=rtol)[0]
        J[:,j]=(plus-minus)/(2*h)
    return dict(step=h,trace=float(np.trace(J)),det=float(np.linalg.det(J)),
        return_residual=float(np.linalg.norm(center-u)),matrix=J.tolist(),period_norm=float(T))


def reduced_variational(model,step_m=3e-7,rtol=3e-11):
    field=model['field'];r0=model['r0'];beta=model['beta'];v=beta*c
    coeff=(-e)*r0/(m_e*v/math.sqrt(1-beta**2))
    y0=model['initial']
    dinit=np.zeros((6,2));dinit[0,0]=model['drdz'];dinit[2,0]=1.;dinit[5,1]=1.
    def rhs(t,aug):
        state=aug[:6];J=aug[6:].reshape(6,2)
        X=state[:3]*r0; V=state[3:];B=field.field_cart(*X)
        grad=np.empty((3,3))
        for axis in range(3):
            dx=np.zeros(3);dx[axis]=step_m
            bpp=field.field_cart(*(X+2*dx));bp=field.field_cart(*(X+dx))
            bm=field.field_cart(*(X-dx));bmm=field.field_cart(*(X-2*dx))
            grad[:,axis]=r0*(-bpp+8*bp-8*bm+bmm)/(12*step_m)
        dstate=np.r_[V,coeff*np.cross(V,B)]
        dJ=np.zeros((6,2));dJ[:3]=J[3:]
        for j in range(2):
            dJ[3:,j]=coeff*(np.cross(J[3:,j],B)+np.cross(V,grad@J[:3,j]))
        return np.r_[dstate,dJ.ravel()]
    def event(t,y):return radial_max_event(t,y[:6])
    event.direction=radial_max_event.direction;event.terminal=False
    result=solve_ivp(rhs,(0,35),np.r_[y0,dinit.ravel()],method='DOP853',
        events=event,rtol=rtol,atol=rtol/40,max_step=.3)
    if not result.success:raise RuntimeError(result.message)
    ev=[(t,y) for t,y in zip(result.t_events[0],result.y_events[0]) if t>1e-6]
    if len(ev)<4:raise RuntimeError('missing event')
    T,aug=ev[3];Y=aug[:6];D=aug[6:].reshape(6,2)
    d_g=np.array([Y[3],Y[4],0,Y[0],Y[1],0])
    F=rhs(T,aug)[:6]
    corrected=D-np.outer(F,(d_g@D)/(d_g@F))
    J=corrected[[2,5],:]
    return dict(gradient_step_m=step_m,rtol=rtol,trace=float(np.trace(J)),
        det=float(np.linalg.det(J)),matrix=J.tolist(),eig_abs=[float(abs(x)) for x in np.linalg.eigvals(J)],
        return_residual=float(np.linalg.norm(Y-y0)),integration_steps=int(len(result.t)))
