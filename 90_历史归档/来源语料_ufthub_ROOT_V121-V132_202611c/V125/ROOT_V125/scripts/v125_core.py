"""ROOT V125: falsifiability tests of a fixed Yukawa gravity model.

SYNTHETIC / IDEALIZED data only. These are established Helmholtz, potential,
Newtonian harmonic-field identities; NOT a proof of a fifth force or GUT.

Conventions: U(r)=-GM/r*[1+alpha*Phi(R/ell)*exp(-r/ell)] (m^2/s^2),
g_vec=-grad U, and E=grad g_vec (s^-2). The conventional potential Hessian
is -E. In classical vacuum Newtonian gravity, tr(E)=0.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import exp, log, sqrt, pi
import numpy as np

R_EARTH_M = 6_371_000.0
ELL_M = 124_600.0
GM_EARTH = 3.986004418e14
ALPHA_Y = 1.0 / 3.0
EOTVOS = 1e-9
MILLI_EOTVOS = 1e-12


def fayet_phi_scaled(ell_m: float = ELL_M) -> float:
    """Fayet 2026 improved analytic density: Phi(R/ell)*exp(-R/ell).

    Analytic form from V124, made numerically stable for large R/ell. This
    approximate Earth profile is an ASSUMPTION, not geodetic observational data.
    """
    if not np.isfinite(ell_m) or ell_m <= 0:
        raise ValueError('ell_m must be positive and finite')
    x = R_EARTH_M / ell_m
    if x < .02:
        # avoid catastrophic cancellation at low x
        return (1+x*x/12+11*x**4/4032+29*x**6/604800)*exp(-x)
    if x < 40:
        return float(((7*x*x-24)*np.cosh(x)+9*x*np.sinh(x)-4*x*x+24)/(4*x**4)*exp(-x))
    a, b = exp(-x), exp(-2*x)
    return ((7*x*x-24)*(1+b)+9*x*(1-b)+(-8*x*x+48)*a)/(8*x**4)


@dataclass(frozen=True)
class FixedYukawaEarth:
    ell_m: float = ELL_M
    alpha: float = ALPHA_Y
    gm: float = GM_EARTH
    r_earth: float = R_EARTH_M
    source_shape_scaled: float | None = None

    def __post_init__(self):
        if self.ell_m <= 0 or self.gm <= 0 or self.r_earth <= 0 or not np.isfinite(self.alpha):
            raise ValueError('nonphysical parameter')
        if self.source_shape_scaled is not None and self.source_shape_scaled < 0:
            raise ValueError('source_shape_scaled must be nonnegative')

    @property
    def phi_scaled(self):
        if self.source_shape_scaled is not None:
            return self.source_shape_scaled
        if self.r_earth != R_EARTH_M:
            raise ValueError('default form factor calibrated for R_EARTH_M')
        return fayet_phi_scaled(self.ell_m)

    def eps(self, r):
        """Delta K / GM, finite source; r>=r_earth, no double huge exp."""
        arr = np.asarray(r, dtype=float)
        if np.any(arr < self.r_earth) or np.any(~np.isfinite(arr)):
            raise ValueError('all points must be outside the source')
        x = arr/self.ell_m
        return self.alpha*self.phi_scaled*(1+x)*np.exp(-(arr-self.r_earth)/self.ell_m)

    def K(self, r):
        return self.gm*(1+self.eps(r))

    def K_prime(self, r):
        arr=np.asarray(r,dtype=float)
        x=arr/self.ell_m
        return -self.gm*self.eps(r)*x/(self.ell_m*(1+x))

    def g_mag(self, r):
        return self.K(r)/np.asarray(r,dtype=float)**2

    def potential(self,r):
        """Newtonian plus Yukawa potential with U(infty)=0."""
        rr=np.asarray(r,dtype=float)
        return -(self.gm/rr)*(1+self.alpha*self.phi_scaled*np.exp(-(rr-self.r_earth)/self.ell_m))

    def y_potential(self,r):
        rr=np.asarray(r,dtype=float)
        return -(self.gm/rr)*(self.alpha*self.phi_scaled*np.exp(-(rr-self.r_earth)/self.ell_m))

    def accel_divergence(self,r):
        """Trace of acceleration Jacobian E_ij=partial_j g_i (s^-2)."""
        rr=np.asarray(r,dtype=float)
        return -self.K_prime(rr)/rr**2

    def helmholtz_trace(self, r):
        """Exterior Helmholtz identity tr(grad g)=-Laplacian U_Y=-U_Y/ell^2."""
        return -self.y_potential(r)/self.ell_m**2

    def gradient_tensor(self, point_xyz):
        """Exact Euclidean E=Jacobian(g_vec), for spherically symmetric model."""
        xyz=np.asarray(point_xyz,dtype=float)
        if xyz.shape!=(3,):
            raise ValueError('point must be (x,y,z)')
        r=float(np.linalg.norm(xyz))
        n=xyz/r
        k=float(self.K(r))
        kp=float(self.K_prime(r))
        h_potential=(kp/r**2-3*k/r**3)*np.outer(n,n)+(k/r**3)*np.eye(3)
        return -h_potential


def trace_invert_range(r1, t1, r2, t2):
    """ell = (r2-r1)/log(r1*T1/(r2*T2)) for one spherical Yukawa term.

    The trace must be the TRUE, unconstrained low-frequency acceleration-tensor
    trace, not a trace-free projected gravity product. Amplitude cancels,
    including for negative couplings with same-sign T values.
    """
    if r1 <= 0 or r2 <= r1 or t1 == 0 or t2 == 0 or t1*t2 <= 0:
        raise ValueError('requires r2>r1>0 and two nonzero same-sign traces')
    lnratio=log((r1*t1)/(r2*t2))
    if lnratio <= 0:
        raise ValueError('positive decay rate not supported')
    return (r2-r1)/lnratio


def harmonic_quadrupole_potential(xyz, gm=1.0, quad=0.01):
    """Newtonian harmonic multipole U=-gm/r+quad * P2(z/r)/r^3."""
    x,y,z=np.asarray(xyz,dtype=float)
    r=sqrt(x*x+y*y+z*z)
    return -gm/r+quad*(3*z*z-r*r)/(2*r**5)


def cartesian_numeric_laplacian(func, xyz, step):
    x=np.asarray(xyz,dtype=float)
    u0=float(func(x))
    total=0.0
    for a in range(3):
        v=np.zeros(3);v[a]=step
        total+=(float(func(x+v))-2*u0+float(func(x-v)))/step**2
    return total


def newton_n(r, gm=GM_EARTH):
    return sqrt(gm/r**3)


def kepler_radius_over_phase(semi_major_axis_m, eccentricity, n_grid=16384):
    """Mean-anomaly uniform samples, exact Keplerian two-body radial distance."""
    if not 0 <= eccentricity < 1 or n_grid<16:
        raise ValueError('invalid Kepler parameters')
    M=np.arange(n_grid)*2*pi/n_grid
    E=M.copy()
    for _ in range(15):
        step=(E-eccentricity*np.sin(E)-M)/(1-eccentricity*np.cos(E))
        E=E-step
        if np.max(np.abs(step))<1e-14:
            break
    return semi_major_axis_m*(1-eccentricity*np.cos(E))


def orbit_trace_band_diagnostic(model: FixedYukawaEarth,
                                semi_major_axis_m=R_EARTH_M+400_000,
                                eccentricity=0.01, low_hz=0.005,
                                n_grid=16384):
    """Power above the GOCE nominal 5 mHz floor for ideal central Yukawa trace.

    This is only an ideal signal spectrum. It does not model GOCE instrument
    transfer functions, noise, gravity products, or calibration filters.
    """
    r=kepler_radius_over_phase(semi_major_axis_m,eccentricity,n_grid)
    if np.min(r)<=model.r_earth:
        raise ValueError('orbit intersects Earth model')
    t=np.asarray(model.accel_divergence(r),float)
    ac=t-np.mean(t)
    frequencies=np.fft.rfftfreq(n_grid,d=(2*pi/newton_n(semi_major_axis_m))/n_grid)
    power=np.abs(np.fft.rfft(ac))**2
    power[0]=0
    total=float(np.sum(power))
    frac=float(np.sum(power[frequencies>=low_hz])/total) if total else 0.0
    return {'orbital_frequency_hz':newton_n(semi_major_axis_m)/(2*pi),
            'low_frequency_cut_hz':low_hz,
            'peak_to_peak_E':float(np.ptp(t)/EOTVOS),
            'mean_trace_E':float(np.mean(t)/EOTVOS),
            'ac_rms_E':float(np.std(ac)/EOTVOS),
            'fraction_ac_power_at_least_5mHz':frac}


def synthetic_trace_mc(model:FixedYukawaEarth, h1=250_000, h2=400_000,
                       n=10000, rel_sigma=0.05, seed=20261121):
    """Toy independent Gaussian uncertainty on two absolute trace measurements.
    Not a GOCE/GRACE error model: independent, uncorrelated, and unbiased.
    """
    if n<1 or rel_sigma<0:
        raise ValueError('bad MC configuration')
    r1=model.r_earth+h1; r2=model.r_earth+h2
    t1=float(model.accel_divergence(r1)); t2=float(model.accel_divergence(r2))
    rng=np.random.default_rng(seed)
    z1=t1*(1+rng.normal(0,rel_sigma,n));z2=t2*(1+rng.normal(0,rel_sigma,n))
    ratio=r1*z1/(r2*z2)
    good=(z1>0)&(z2>0)&(ratio>1)&np.isfinite(ratio)
    v=(r2-r1)/np.log(ratio[good])
    return {'sigma_fraction':rel_sigma,'n':n,'valid_fraction':float(np.mean(good)),
            'median_km':float(np.median(v)/1000) if len(v) else None,
            'quantiles_2p5_50_97p5_km':(np.quantile(v,[.025,.5,.975])/1000).tolist() if len(v) else None}


def point_source_yukawa_potential(xyz, sources_xyz, strengths, k):
    """Non-spherical source distribution as a sum of Yukawa point monopoles.

    U_Y=-sum C_i exp(-k |x-y_i|)/|x-y_i|. Strengths C_i have units of GM.
    The test point must be outside every source. This is a discrete toy model.
    """
    x=np.asarray(xyz,dtype=float)
    positions=np.asarray(sources_xyz,dtype=float)
    strengths=np.asarray(strengths,dtype=float)
    if x.shape!=(3,) or positions.ndim!=2 or positions.shape[1]!=3 or len(strengths)!=len(positions) or k<=0:
        raise ValueError('invalid source geometry')
    distance=np.linalg.norm(positions-x[None,:],axis=1)
    if np.any(distance<=0):
        raise ValueError('test position at source')
    return float(-np.sum(strengths*np.exp(-k*distance)/distance))


def point_source_yukawa_trace(xyz, sources_xyz, strengths,k):
    """tr(gradient(g_vec))=-k^2 U_Y everywhere away from all sources."""
    return -k*k*point_source_yukawa_potential(xyz,sources_xyz,strengths,k)


def profiled_signal_information(signal, nuisance_design, sigma=1.0):
    """Profiled Gaussian Fisher information for scalar amplitude of a known signal.

    y = amplitude*signal + nuisance_design@beta + Normal(0,sigma^2 I).
    Info = ||(I-P_N)signal||^2/sigma^2; if signal lies in nuisance
    column space, amplitude is NOT IDENTIFIABLE regardless of sample count.
    This model assumes independent, homoscedastic noise for demonstration.
    """
    s=np.asarray(signal,dtype=float)
    n=np.asarray(nuisance_design,dtype=float)
    if s.ndim!=1 or n.ndim!=2 or n.shape[0]!=len(s) or sigma<=0:
        raise ValueError('invalid profiled Fisher inputs')
    coef=np.linalg.lstsq(n,s,rcond=None)[0]
    residual=s-n@coef
    return float(residual@residual/sigma**2)
