"""Coupled, gauge-invariant Maxwell + dynamical phase toy model.

From S/hbar = int [ -F^2/(4g^2) -f^2(dtheta)^2/2
                    - lam*theta F*Fdual/4 ].
Take a real, standing helical Beltrami field (not a traveling photon):
  A=(0,a(t)cos(kz),-a(t)sin(kz),0), curl(A)=k A.
The reduced lagrangian density divided by hbar is
 L=(v*v-k*k*a*a)/(2*g*g)+f*f*w*w/2-lam*k*theta*a*v,
where v=a', w=theta'. Equations:
 a''= -k^2*a +g^2*lam*k*w*a
 theta''= -lam*k*a*v/f^2.
Energy: E=(v^2+k^2 a^2)/(2g^2)+f^2 w^2/2.
Shift charge: Q=f^2*w+lam*k*a^2/2.
All numerical quantities in reference-length L0 units; physical
energy density= hbar/L0^4 * E.
"""
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Params:
    k: float = 1.0
    g: float = 1.0
    f: float = 1.0
    lam: float = 0.6

    def validate(self):
        if self.k <= 0 or self.g <= 0 or self.f <= 0:
            raise ValueError('k, g, f must all be strictly positive')
        if not all(math.isfinite(x) for x in (self.k, self.g, self.f, self.lam)):
            raise ValueError('parameters must be finite')


def rhs(state, p: Params):
    a, v, theta, w = state
    return (v, -p.k*p.k*a + p.g*p.g*p.lam*p.k*w*a,
            w, -p.lam*p.k*a*v/(p.f*p.f))


def energy(state,p: Params):
    a,v,theta,w=state
    return (v*v+p.k*p.k*a*a)/(2*p.g*p.g)+p.f*p.f*w*w/2


def photon_energy(state,p: Params):
    a,v,_,_=state
    return (v*v+p.k*p.k*a*a)/(2*p.g*p.g)


def scalar_energy(state,p: Params):
    return 0.5*p.f*p.f*state[3]*state[3]


def shift_charge(state,p: Params):
    a,_,_,w=state
    return p.f*p.f*w+0.5*p.lam*p.k*a*a


def rk4_step(y,dt,p):
    k1=rhs(y,p)
    k2=rhs(tuple(yi+dt*ki/2 for yi,ki in zip(y,k1)),p)
    k3=rhs(tuple(yi+dt*ki/2 for yi,ki in zip(y,k2)),p)
    k4=rhs(tuple(yi+dt*ki for yi,ki in zip(y,k3)),p)
    return tuple(yi+(dt/6)*(j1+2*j2+2*j3+j4)
                 for yi,j1,j2,j3,j4 in zip(y,k1,k2,k3,k4))


def integrate(initial=(0.3,0.2,0.0,0.3), t_max=80., dt=0.005,
              p=Params(), keep_every=20):
    p.validate()
    if t_max <= 0 or dt <= 0:
        raise ValueError('t_max and dt must be positive')
    count=round(t_max/dt)
    if not math.isclose(count*dt,t_max,rel_tol=1e-10,abs_tol=1e-10):
        raise ValueError('t_max must be a multiple of dt')
    if len(initial) != 4 or not all(math.isfinite(x) for x in initial):
        raise ValueError('initial must be four finite values')
    state=tuple(float(x) for x in initial)
    output=[]
    for idx in range(count+1):
        if idx%keep_every==0 or idx==count:
            output.append({'t':idx*dt, 'a':state[0], 'v':state[1],
                           'theta':state[2], 'w':state[3],
                           'energy':energy(state,p),
                           'photon_energy':photon_energy(state,p),
                           'scalar_energy':scalar_energy(state,p),
                           'shift_charge':shift_charge(state,p)})
        if idx<count:
            state=rk4_step(state,dt,p)
    return output


def diagnostic_summary(rows,p):
    e0=rows[0]['energy'];q0=rows[0]['shift_charge']
    return {
      'method':'fixed-step RK4, analytic invariants, independent RK4 convergence',
      'steps_recorded':len(rows),
      'time_final':rows[-1]['t'],
      'initial_energy':e0,
      'max_absolute_energy_drift':max(abs(r['energy']-e0) for r in rows),
      'max_relative_energy_drift':max(abs(r['energy']/e0-1) for r in rows),
      'max_absolute_shift_charge_drift':max(abs(r['shift_charge']-q0) for r in rows),
      'photon_energy_min':min(r['photon_energy'] for r in rows),
      'photon_energy_max':max(r['photon_energy'] for r in rows),
      'scalar_energy_min':min(r['scalar_energy'] for r in rows),
      'scalar_energy_max':max(r['scalar_energy'] for r in rows),
      'final_state':[rows[-1][key] for key in ('a','v','theta','w')],
      'p':vars(p),
    }


def local_omega_squared(p,theta_dot,helicity):
    """Adiabatic external theta_dot approximation for circular traveling modes.
    The background is NOT treated as an exact solution of the coupled ODE.
    """
    if helicity not in (-1,1):
        raise ValueError('helicity must be +1/-1')
    return p.k*p.k - helicity*p.k*p.g*p.g*p.lam*theta_dot
