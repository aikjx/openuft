"""Numerical wave audit for a *prescribed*, spatially homogeneous pseudoscalar.

Units: hbar=c=1; time and inverse frequencies dimensionless after a chosen
reference scale. No measurement, no claimed ROOT-specific new physics.

Action conventions: S = integral [-1/4 F^2 - lam/4 theta F Fdual
+ f^2/2 (partial theta)^2 - V(theta)] with metric (+---).
For one consistent circular-basis convention:
A_h'' + (k*k + h*lam*k*theta') A_h = 0, h=+1,-1.
The reported rotation is minus one half of the relative wave phase,
which tends to lam*(theta(T)-theta(0))/2 in the adiabatic limit.
"""
from dataclasses import dataclass
import numpy as np
from scipy.integrate import solve_ivp

@dataclass(frozen=True)
class Profile:
    amplitude: float = .4
    omega: float = .7
    phase: float = 0.
    offset: float = 0.
    def value(self, t):
        return self.offset + self.amplitude * np.sin(self.omega*t + self.phase)
    def derivative(self, t):
        return self.amplitude * self.omega * np.cos(self.omega*t + self.phase)
    def second(self, t):
        return -self.amplitude * self.omega**2 * np.sin(self.omega*t + self.phase)


def wkb_angle(lam, profile, duration):
    """Leading WKB rotation, sign fixed by the circular basis above."""
    return .5 * lam * (profile.value(duration) - profile.value(0.))


def mode_frequency_squared(t, k, lam, profile, helicity):
    assert k>0 and helicity in (-1,1)
    return k*k + helicity * lam * k * profile.derivative(t)


def integrate_mode(k, lam, profile, duration, helicity, *, rtol=2e-10, atol=2e-12):
    """Integrate complex mode with local positive-frequency adiabatic initial data."""
    w2=mode_frequency_squared(0.,k,lam,profile,helicity)
    if w2<=0:
        raise ValueError('initial mode frequency imaginary; WKB vacuum invalid')
    w0=np.sqrt(w2)
    wprime=helicity*lam*k*profile.second(0.)/(2*w0)
    a0=1/np.sqrt(2*w0)
    da0=(-1j*w0-wprime/(2*w0))*a0
    def f(t,y):
        return np.asarray([y[1],-mode_frequency_squared(t,k,lam,profile,helicity)*y[0]],dtype=complex)
    sol=solve_ivp(f,(0.,duration),np.array([complex(a0),complex(da0)]),method='DOP853',rtol=rtol,atol=atol)
    if not sol.success:
        raise RuntimeError(sol.message)
    return complex(sol.y[0,-1]),complex(sol.y[1,-1]),sol.nfev


def exact_rotation(k, lam, profile, duration, *, rtol=2e-10, atol=2e-12):
    plus,_,npn=integrate_mode(k,lam,profile,duration,1,rtol=rtol,atol=atol)
    minus,_,nmn=integrate_mode(k,lam,profile,duration,-1,rtol=rtol,atol=atol)
    # Angle is measured modulo pi, as appropriate to a linear-polarization axis.
    angle=-.5*np.angle(plus*np.conj(minus))
    return dict(angle=float(angle),wkb=float(wkb_angle(lam,profile,duration)),
                phase_difference=float(np.angle(plus*np.conj(minus))),
                relative_amplitude=float(abs(plus)/abs(minus)),
                nfev=npn+nmn,
                adiabatic_upper=float(max_adiabatic(k,lam,profile,duration)))


def max_adiabatic(k,lam,profile,duration,points=512):
    t=np.linspace(0,duration,points)
    best=0.
    for h in (-1,1):
        w2=mode_frequency_squared(t,k,lam,profile,h)
        if np.min(w2)<=0: return float('inf')
        wp=np.abs(h*lam*k*profile.second(t))/(2*np.power(w2,1.5))
        best=max(best,float(np.max(wp)))
    return best


def fisher_jacobian_single(lam,delta_theta):
    return np.array([[delta_theta/2,lam/2]])


def constrained_bound(sigma_chi, delta_theta, z=1.96):
    """Conditional null-signal sensitivity, only when delta theta is independent/known."""
    if abs(delta_theta)<1e-14:
        return float('inf')
    return float(2*z*sigma_chi/abs(delta_theta))


def observed_mode_proxies(k, lam, profile, duration, *, rtol=2e-10, atol=2e-12):
    """Phase-axis angles and circular Stokes V proxy of ideal mode variables.

    The A-proxy is not an experimental polarimeter. In adiabatic propagation
    the E=-A' proxy approaches the same leading WKB rotation. In nonadiabatic
    settings the polarization ellipse requires full field reconstruction.
    """
    a, da, _=integrate_mode(k,lam,profile,duration,+1,rtol=rtol,atol=atol)
    b, db, _=integrate_mode(k,lam,profile,duration,-1,rtol=rtol,atol=atol)
    return dict(A_phase_axis=float(-.5*np.angle(a*np.conj(b))),
                E_phase_axis=float(-.5*np.angle(da*np.conj(db))),
                A_circular_stokes_v=float((abs(a)**2-abs(b)**2)/(abs(a)**2+abs(b)**2)),
                E_circular_stokes_v=float((abs(da)**2-abs(db)**2)/(abs(da)**2+abs(db)**2)))


def one_loop_identifiability(lam, dtheta):
    """Rank 1 for one angle measurement, two free quantities (lam, Delta theta)."""
    jac=fisher_jacobian_single(lam,dtheta)
    null=np.array([lam,-dtheta])
    return dict(rank=int(np.linalg.matrix_rank(jac)), null_residual=float(np.linalg.norm(jac@null)))
