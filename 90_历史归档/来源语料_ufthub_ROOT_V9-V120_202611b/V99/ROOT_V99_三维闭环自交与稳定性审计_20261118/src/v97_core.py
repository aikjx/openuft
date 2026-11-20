"""ROOT V97: conditional resonances and nonlinear planar closed trajectories.
Physics: standard relativistic Lorentz motion in a prescribed smooth external
magnetostatic Maxwell field. All outputs are theoretical, not observations.
"""
from __future__ import annotations
from math import gcd, sqrt, pi
from dataclasses import dataclass
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
from numpy.polynomial.legendre import leggauss
from scipy.constants import e, m_e, c
from coil_model import TwoCoilField, circular_reference, normalized_rhs, trajectory


def primitive_pythagorean_resonances(max_denominator=120):
    """All positive primitive weak-focusing tune triples with N<=bound."""
    triples=[]
    for n in range(1,int(sqrt(max_denominator))+2):
        for m in range(n+1,int(sqrt(max_denominator))+2):
            if gcd(m,n)>1 or (m-n)%2==0: continue
            a=m*m-n*n; b=2*m*n; N=m*m+n*n
            if N>max_denominator:continue
            a,b=sorted((a,b))
            triples.append({'a':a,'b':b,'N':N,'nu_r':b/N,'nu_z':a/N,
                            'n_index':(a/N)**2,'triple':f'{b}:{a}:{N}'})
    return sorted(triples,key=lambda x:(x['N'],x['b']))


def tune_radius(field:TwoCoilField,n_target=9/25,bracket=(.004,.0065)):
    return brentq(lambda r:float(field.index(r))-n_target,*bracket,xtol=1e-14)


def five_turn_fixed_time(field,r0,dx=10e-6,dz=10e-6,beta=.1,rtol=4e-11):
    circular_reference(beta=beta,r0=r0,field=field)
    sol=trajectory(field,beta=beta,r0=r0,turns=5,dx=dx,dz=dz,
                   rtol=rtol,atol=rtol*0.005)
    if not sol.success: raise RuntimeError(sol.message)
    error=sol.y[:,-1]-sol.y[:,0]
    return {'amplitude_m':dx,'vertical_amplitude_m':dz,
            'position_return_m':float(r0*np.linalg.norm(error[:3])),
            'relative_velocity_return':float(np.linalg.norm(error[3:])),
            'step_count':len(sol.t),'end_normalized':sol.y[:,-1].tolist()}


def radial_max_event(t,y,*unused):
    # rdot=0 in the planar invariant z=v_z=0 submanifold
    return (y[0]*y[3]+y[1]*y[4])/np.hypot(y[0],y[1])
radial_max_event.direction=-1
radial_max_event.terminal=False


def planar_return(field,r0,amplitude=30e-6,beta=.1,cycles=4,rtol=3e-11,
                  max_step=.30):
    """Track N radial maxima after t=0; calculate unwrapped azimuthal phase.
    The return is a Poincare-section event, not a fixed-time comparison.
    """
    ref=circular_reference(beta=beta,r0=r0,field=field)
    y0=np.array([1+amplitude/r0,0,0,0,1,0],float)
    sol=solve_ivp(normalized_rhs,(0,43),y0,args=(field,beta,r0),
                  events=radial_max_event,method='DOP853',rtol=rtol,
                  atol=rtol*.006,max_step=max_step,dense_output=True)
    if not sol.success:raise RuntimeError(sol.message)
    future=[(float(t),y) for t,y in zip(sol.t_events[0],sol.y_events[0]) if t>1e-6]
    if len(future)<cycles:raise RuntimeError(f'Only {len(future)} extrema')
    tm,yend=future[cycles-1]
    angle=float(np.arctan2(yend[1],yend[0]))
    angle+=2*pi*round((tm-angle)/(2*pi))
    target=2*pi*5
    phase_error=angle-target
    # rotate final transverse state backwards by 5 revolutions (same coordinates)
    full_state_err= np.linalg.norm(yend-y0)
    return {'r0_m':float(r0),'initial_radial_offset_m':amplitude,'reference':ref,
        'time_normalized':tm,'t_seconds':tm*r0/(beta*c),
        'phi_radians':angle,'target_phi_radians':target,
        'phase_error_rad':phase_error,'phase_error_per_turn_rad':phase_error/5,
        'return_position_error_m':float(r0*np.linalg.norm(yend[:3]-y0[:3])),
        'return_velocity_relative':float(np.linalg.norm(yend[3:]-y0[3:])),
        'return_state_normalized':yend.tolist(),
        'number_of_future_radial_maxima':len(future),'ode_steps':len(sol.t),
        'orbit':sol, 'initial_state':y0,'final_state':yend}


def shoot_planar_resonance(field,amplitude=30e-6,beta=.1,linear_root=None,
                           bracket_span=70e-6,rtol=3e-11):
    r_lin=tune_radius(field) if linear_root is None else linear_root
    def residual(r):
        return planar_return(field,r,amplitude,beta=beta,rtol=rtol)['phase_error_rad']
    lo,hi=r_lin-bracket_span,r_lin+bracket_span
    f0,f1=residual(lo),residual(hi)
    if f0*f1>=0:
        raise RuntimeError('Could not bracket nonlinear planar resonance')
    root=brentq(residual,lo,hi,xtol=1e-14)
    result=planar_return(field,root,amplitude,beta=beta,rtol=rtol)
    result.update({'linear_root_m':r_lin,'nonlinear_shift_m':root-r_lin,
                  'bracket_m':[lo,hi],'bracket_phase_rad':[f0,f1],
                  'note':'Numerically located periodic planar orbit of the fixed prescribed field model. Not an interval-arithmetic proof.'})
    return result


def canonical_angular_momentum_relative_error(field, r0, sol, beta=.1, num=31):
    """Relative canonical Pphi variation, avoiding axis flux gauge constant.
    Delta Pphi / (gamma*m*v0*r0) = Delta(r*vphi)/(r0*v0)
        + q/(gamma*m*v0*r0)*int_{r_initial}^r (rho Bz(rho,0)) drho.
    """
    xx,yy,vx,vy=sol.y[0],sol.y[1],sol.y[3],sol.y[4]
    rr=np.hypot(xx,yy)*r0
    lnorm=(xx*vy-yy*vx)
    init=rr[0]
    gamma=1/sqrt(1-beta**2)
    q=-e
    xg,wg=leggauss(num)
    vals=[]
    for rad,angular in zip(rr,lnorm):
        radius=(rad+init)/2 + (rad-init)/2*xg
        bz=field.field(radius,np.zeros_like(radius))[1]
        flux=(rad-init)/2 * np.dot(wg,radius*bz)
        vals.append(float((angular-lnorm[0]) + q*flux/(gamma*m_e*beta*c*r0)))
    return max(abs(x) for x in vals)


def circular_radiation_per_turn(beta,r0):
    from scipy.constants import epsilon_0
    gamma=1/sqrt(1-beta**2);v=beta*c
    acc=v*v/r0
    power=e**2*gamma**4*acc**2/(6*pi*epsilon_0*c**3)
    time=2*pi*r0/v
    return {'radiated_power_W':float(power),'energy_per_turn_J':float(power*time),
            'electron_kinetic_energy_J':float((gamma-1)*m_e*c*c),
            'fraction_of_kinetic_per_turn':float(power*time/((gamma-1)*m_e*c*c)),
            'warning':'Liénard formula on prescribed circular motion; back-reaction omitted'}


def independent_planar_apsidal_angle(field,r0,amplitude=30e-6,beta=.1,quad_n=70):
    """Independent 1-DOF canonical-momentum quadrature (no ODE).
    Plane z=0 is invariant by mirror symmetry. Returns azimuthal advance
    after one radial oscillation, and radial turning points.
    """
    ref=circular_reference(beta=beta,r0=r0,field=field)
    rp=r0+amplitude
    Bref=ref['B0']
    xq,wq=leggauss(28)
    def flux_between(x):
        rr=(rp+x)*.5 + (rp-x)*.5*xq
        bz=field.field(rr,np.zeros_like(rr))[1]
        return float((rp-x)*.5*np.dot(wq,rr*bz))
    def g(x):
        return (rp-flux_between(x)/(Bref*r0))/x
    # locate nontrivial inner turning point, preserving g(rp)=1
    lower=rp-3*amplitude
    upper=rp-0.25*amplitude
    if not (g(lower)>1 and g(upper)<1):
        raise ValueError(f'Unexpected inner turning-point bracket: {g(lower)}, {g(upper)}')
    rm=brentq(lambda r:g(r)-1,lower,upper,xtol=1e-14)
    xx,ww=leggauss(quad_n)
    theta=(xx+1)*pi/4
    radii=rm+(rp-rm)*np.sin(theta)**2
    drdtheta=2*(rp-rm)*np.sin(theta)*np.cos(theta)
    gg=np.array([g(r) for r in radii])
    if np.any(gg**2>=1):
        raise ValueError('Numerical quadrature sampled a forbidden radial state')
    integrand=2*(gg/(radii*np.sqrt(1-gg**2)))*drdtheta
    angle=float(np.dot(ww,integrand)*pi/4)
    return {'inner_turning_m':float(rm),'outer_turning_m':float(rp),
            'azimuth_per_radial_cycle_rad':angle,
            'four_cycle_phi_rad':4*angle,'four_cycle_phase_error_rad':4*angle-10*pi,
            'quadrature_points':quad_n}
