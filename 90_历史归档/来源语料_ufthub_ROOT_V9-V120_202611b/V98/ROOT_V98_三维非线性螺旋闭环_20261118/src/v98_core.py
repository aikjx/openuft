"""ROOT V98: finite-amplitude 3D periodic trajectories in V97 coil fields.

Model: relativistic electron TEST PARTICLE; external smooth finite-cross-section
axisymmetric static current; no radiation reaction or self-fields.
Numbers are simulations, not experimental measurements or proofs of exact roots.
"""
from __future__ import annotations
import math
import numpy as np
from scipy.optimize import root, brentq
from scipy.integrate import solve_ivp, trapezoid
from scipy.constants import c,e,m_e, epsilon_0
from numpy.polynomial.legendre import leggauss
from coil_model import TwoCoilField,circular_reference,normalized_rhs
from v97_core import radial_max_event, tune_radius

BETA=.1
AMPL_R=60e-6
BASE_H=.008


def five_turn_3d(field, r0, az, ar=AMPL_R, beta=BETA, rtol=2e-11, dense=False):
    """Return at 4th post-launch radial maximum; angle target 5*2*pi.

    The symmetry section is dr/dt=0, with initial dz/dt=0. We solve
    phi(T)=10*pi and vz(T)=0. For a positive-z same-side return,
    conserved energy and P_phi then constrain z(T) near z(0).
    """
    circular_reference(beta=beta,r0=r0,field=field)
    y0=np.array([1+ar/r0,0.,az/r0,0.,1.,0.],float)
    sol=solve_ivp(normalized_rhs,(0.,35.),y0,
           args=(field,beta,r0),events=radial_max_event,dense_output=dense,
           method='DOP853',rtol=rtol,atol=max(1e-14,rtol/40),max_step=.35)
    if not sol.success:raise RuntimeError(sol.message)
    future=[(float(t),yy) for t,yy in zip(sol.t_events[0],sol.y_events[0]) if t>1e-6]
    if len(future)<4:raise RuntimeError(f'Only {len(future)} future radial maxima')
    tm,yend=future[3]
    phi=float(np.arctan2(yend[1],yend[0]))
    phi+=2*math.pi*round((tm-phi)/(2*math.pi))
    return {
      'r0_m':float(r0),'ar_m':float(ar),'az_m':float(az),'beta':float(beta),
      'tm_norm':tm,'period_s':tm*r0/(beta*c), 'phi_rad':phi,
      'phi_residual_rad':phi-10*math.pi, 'vz_residual_dimensionless':float(yend[5]),
      'z_return_error_m':float(r0*yend[2]-az),
      'position_return_error_m':float(r0*np.linalg.norm(yend[:3]-y0[:3])),
      'velocity_return_error_relative':float(np.linalg.norm(yend[3:]-y0[3:])),
      'field_I_A_per_coil':float(field.current),
      'reference_B_T':float(field.field(r0,0.)[1]),
      'end':yend,'initial':y0,'sol':sol,'field':field}


def shoot_3d(order=21, beta=BETA, ar=AMPL_R, half_separation=BASE_H,
             guess_r=None, guess_z=8.84e-6, rtol=1e-10):
    """Local 2D shooting plus independent residual and sign-bracket audit.

    This computes a numerical candidate, not rigorous root existence.
    Flat functions can cause scipy root.success=False despite small residual;
    we report BOTH solver status and verified residuals honestly.
    """
    field=TwoCoilField(half_separation=half_separation,order=order)
    center=float(tune_radius(field))-.33e-6 if guess_r is None else guess_r
    calls=[0]
    def obj(x):
        calls[0]+=1
        rr=center+x[0]*1e-6;az=guess_z+x[1]*1e-6
        row=five_turn_3d(field,rr,az,ar,beta,rtol)
        return [row['phi_residual_rad'],row['vz_residual_dimensionless']*1e6]
    sol=root(obj,[0.,0.],method='hybr', options={'eps':1e-4,'xtol':1e-8})
    rr=center+sol.x[0]*1e-6;az=guess_z+sol.x[1]*1e-6
    result=five_turn_3d(field,rr,az,ar,beta,rtol,dense=True)
    verified=(abs(result['phi_residual_rad'])<1e-8 and
        abs(result['vz_residual_dimensionless'])<1e-9 and
        abs(result['z_return_error_m'])<1e-9 and 1e-7<az<2e-4)
    if not verified:raise RuntimeError('Unverified 3D numerical shooting candidate: '+str(sol.message))
    result['root_success']=bool(sol.success)
    result['residual_verified']=bool(verified)
    result['root_message']=str(sol.message)
    result['root_calls']=int(calls[0]);result['source_order']=order
    return result

def independent_fixed_time_orbit(row, rtol=3e-12):
    """Independent non-event integration to the determined return time."""
    f=row['field']
    rr=row['r0_m'];beta=row['beta'];yy=row['initial']
    solution=solve_ivp(normalized_rhs,(0,row['tm_norm']),yy,args=(f,beta,rr),
             method='DOP853',rtol=rtol,atol=rtol/30,max_step=.25)
    if not solution.success:raise RuntimeError(solution.message)
    return {'position_error_m':rr*np.linalg.norm(solution.y[:3,-1]-yy[:3]),
      'velocity_error':np.linalg.norm(solution.y[3:,-1]-yy[3:]),
      'max_speed_relative_drift':float(np.max(np.abs(np.linalg.norm(solution.y[3:,:],axis=0)-1))),
      'ode_steps':len(solution.t), 'return':solution.y[:,-1]}


def _boris_rotate(v,magnetic,dt,q_over_gamma_m):
    t=q_over_gamma_m*magnetic*dt*.5
    s=2*t/(1+np.dot(t,t))
    vp=v+np.cross(v,t)
    return v+np.cross(vp,s)


def boris_independent(row,nsteps=4000):
    """Separate, second-order time-centered Boris magnetic orbit."""
    f=row['field'];rr=row['r0_m'];beta=row['beta']
    gamma=1/math.sqrt(1-beta**2)
    qm=-e/(gamma*m_e)
    x=row['initial'][:3]*rr
    v=row['initial'][3:]*beta*c
    x0=x.copy();v0=v.copy()
    dt=row['period_s']/nsteps
    vh=_boris_rotate(v, f.field_cart(*x),dt*.5,qm)
    for _ in range(nsteps):
        x=x+dt*vh
        vh=_boris_rotate(vh,f.field_cart(*x),dt,qm)
    vend=_boris_rotate(vh,f.field_cart(*x),-dt*.5,qm)
    return {'dt_s':dt,'nsteps':nsteps,
       'position_difference_m':float(np.linalg.norm(x-x0)),
       'velocity_difference_relative':float(np.linalg.norm(vend-v0)/(beta*c)),
       'speed_relative_difference':abs(np.linalg.norm(vend)/(beta*c)-1)}


def vacuum_maxwell_residuals(field,r0,z=.00023,h=4e-6):
    """Finite difference cylindrical divergence and curl_theta of B,
    each normalized by B0/r0; vacuum region only."""
    r=r0
    brp,bzp=field.field(r+h,z);brm,bzm=field.field(r-h,z)
    brzplus,bzzplus=field.field(r,z+h)
    brzminus,bzzminus=field.field(r,z-h)
    br,bz=field.field(r,z)
    div=((r+h)*brp-(r-h)*brm)/(2*h*r)+(bzzplus-bzzminus)/(2*h)
    curl=(brzplus-brzminus)/(2*h)-(bzp-bzm)/(2*h)
    ref=abs(bz)/r
    return {'div_T_per_m':float(div),'curl_theta_T_per_m':float(curl),
       'div_normalized':abs(float(div))/ref,'curl_normalized':abs(float(curl))/ref}


def canonical_invariant_error(row,sample_count=37,quad_order=50):
    """Axisymmetric canonical P_phi conservation, using flux from 0 to r.
    psi(r,z)= integral_0^r rho B_z(rho,z) drho, with A_phi=psi/r.
    """
    f=row['field'];rr=row['r0_m'];beta=row['beta']; gamma=1/math.sqrt(1-beta**2)
    dense=row['sol'].sol
    times=np.linspace(0,row['tm_norm'],sample_count)
    points=dense(times)
    x,y,z,vx,vy,vz=points
    radii=np.hypot(x,y)*rr
    zloc=z*rr
    mech=x*vy-y*vx
    nodes,weights=leggauss(quad_order)
    psi=[]
    for radius,axial in zip(radii,zloc):
        rho=radius*(nodes+1)*.5
        bb=f.field(rho,np.full_like(rho,axial))[1]
        psi.append(float(radius*.5*np.dot(weights,rho*bb)))
    psi=np.asarray(psi)
    pphi_norm=mech+(-e)*(psi-psi[0])/(gamma*m_e*beta*c*rr)
    # initial reference flux constant removed, pphi comparisons unaffected
    return {'max_delta_Pphi_relative':float(np.max(abs(pphi_norm-pphi_norm[0]))),
      'max_speed_relative_drift':float(np.max(abs(np.linalg.norm(points[3:],axis=0)-1))),
      'sample_count':sample_count,'flux_integral_order':quad_order}


def classical_radiation(row, sample_count=250):
    """Liénard radiation of prescribed path, ignoring reaction. Perpendicular a/v."""
    f=row['field']; beta=row['beta'];rr=row['r0_m']
    gamma=1/math.sqrt(1-beta**2);v=beta*c
    times=np.linspace(0,row['tm_norm'],sample_count)
    y=row['sol'].sol(times)
    powers=[]
    for coords,vn in zip(y[:3].T,y[3:].T):
        b=f.field_cart(*(coords*rr))
        acc=(-e)*np.cross(vn*v,b)/(gamma*m_e)
        powers.append(e**2*gamma**4*np.dot(acc,acc)/(6*math.pi*epsilon_0*c**3))
    energy=float(trapezoid(powers, times)*rr/v)
    return {'energy_J_per_period':energy,'min_power_W':float(min(powers)),
      'max_power_W':float(max(powers)),'electron_kinetic_J':float((gamma-1)*m_e*c*c),
      'radiation_to_kinetic':energy/((gamma-1)*m_e*c*c),
      'approximation':'prescribed-trajectory Lienard; not self-consistent radiation reaction'}


def orbit_samples(row,n=1100):
    rr=row['r0_m'];beta=row['beta']
    tt=np.linspace(0,row['tm_norm'],n)
    ys=row['sol'].sol(tt)
    return {'t_ns':tt*rr/(beta*c)*1e9,
      'x_mm':ys[0]*rr*1e3,'y_mm':ys[1]*rr*1e3,'z_um':ys[2]*rr*1e6,
      'radius_mm':np.hypot(ys[0],ys[1])*rr*1e3,'speed_ratio':np.linalg.norm(ys[3:],axis=0)}
