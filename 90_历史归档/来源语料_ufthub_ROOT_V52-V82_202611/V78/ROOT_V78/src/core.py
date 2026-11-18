"""Audited SI physics formulas; no claim of an independent prediction of G.

The weak-field point mass estimate assumes a complete isolated source and r
much larger than source dimensions; the ideal EM slab is only a bookkeeping
model, NOT a Maxwell-consistent coil or complete gravitating apparatus.
"""
from __future__ import annotations
import math
from dataclasses import dataclass

C = 299_792_458.0
H = 6.626_070_15e-34
HBAR = H / (2.0 * math.pi)
G_CODATA = 6.67430e-11
G_STANDARD_UNCERTAINTY = 1.5e-15
MU0 = 1.256_637_062_12e-6  # CODATA 2018 reference; not SI exact after 2019
EPS0 = 1.0 / (MU0*C*C)
EARTH_MU = 3.986_004_418e14  # illustrative reference m^3/s^2
EARTH_R = 6_371_000.0


def z_from_g(G=G_CODATA, c=C):
    return G*c/2


def g_from_z(z: float, c=C):
    if c <= 0: raise ValueError('c must be positive')
    return 2*z/c


def alpha_grav(m, G=G_CODATA, c=C):
    return G*m*m/(HBAR*c)


def planck_length(G=G_CODATA, c=C):
    return math.sqrt(HBAR*G/c**3)


def grav_parameter(G, M):
    return G*M


def mass_from_orbit(mu, G):
    if G <= 0: raise ValueError('G must be positive')
    return mu/G


def mag_energy_density(B, mu0=MU0):
    return B*B/(2*mu0)


def elec_energy_density(E, eps0=EPS0):
    return 0.5*eps0*E*E


def em_energy_density(E, B):
    """E,B can be scalar magnitudes or 3-element vector inputs."""
    def norm2(x):
        return sum(v*v for v in x) if isinstance(x,(tuple,list)) else x*x
    return EPS0*norm2(E)/2 + norm2(B)/(2*MU0)


def dot(a, b):
    return sum(x*y for x,y in zip(a,b))


def add(a, b):
    return tuple(x+y for x,y in zip(a,b))


def e_cross_energy(E1, E2):
    return EPS0*dot(E1,E2)


def b_cross_energy(B1, B2):
    return dot(B1,B2)/MU0


def cross_product(a,b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def poynting(E,B):
    return tuple(v/MU0 for v in cross_product(E,B))


def magnetic_maxwell_stress(B):
    """Spatial electromagnetic stress sigma_ij for E=0 in SI (Maxwell stress)."""
    B2=dot(B,B)
    return tuple(tuple((B[i]*B[j] - (B2/2 if i==j else 0))/MU0
                     for j in range(3)) for i in range(3))


def wave_invariants(E,B):
    # Lab frame forms proportional to the two Lorentz scalar EM invariants.
    return dot(E,E)-C*C*dot(B,B), dot(E,B)


def em_equivalent_mass(E_total_joule):
    return E_total_joule/C**2


def far_field_monopole_g(E_added_joule, r, G=G_CODATA):
    if r <= 0: raise ValueError('r>0')
    return G * em_equivalent_mass(E_added_joule)/(r*r)


def magnetic_energy(B, volume_m3):
    if volume_m3 < 0: raise ValueError('volume>=0')
    return mag_energy_density(B)*volume_m3


def photon_system_mass(energies_joule, directions):
    """Photon-system invariant mass: stable sum of pairwise angular differences.

    M^2 c^4 = 2 sum_{i<j} E_i E_j (1 - n_i dot n_j).
    Valid only for positive energies and unit directions; avoids subtracting
    two nearly equal large squares for collinear photons.
    """
    if len(energies_joule)!=len(directions): raise ValueError('length mismatch')
    for en,n in zip(energies_joule,directions):
        if en<0 or not math.isclose(dot(n,n),1,abs_tol=1e-12):
            raise ValueError('energies >=0 and each direction unit length required')
    msq=0.0
    for i in range(len(energies_joule)):
        for j in range(i+1,len(energies_joule)):
            msq += 2*energies_joule[i]*energies_joule[j]*max(0.0,1-dot(directions[i],directions[j]))
    return math.sqrt(msq)/C**2


def induction_energy_ratio_sphere(angular_frequency, radius):
    """Quasistatic ideal uniform time-varying B filling a sphere, cycle average.
    Induced E_phi=-rho/2 * dB/dt. This is not an exactly isolated finite
    Maxwell field solution; boundary currents and displacement current omitted.
    """
    return (angular_frequency*radius/C)**2/10.0


def yukawa_shape_factor(x):
    """Uniform spherical source factor; may overflow at x>~700.
    Use yukawa_ratio_sphere for large x instead.
    """
    if x < 0: raise ValueError('x>=0')
    if x == 0: return 1.0
    if x < 0.1:
        return 1.0 + x*x/10.0 + x**4/280.0 + x**6/15120.0 + x**8/1330560.0
    return 3*(x*math.cosh(x)-math.sinh(x))/x**3


def yukawa_ratio_point(alpha, r, lam):
    if r < 0 or lam<=0: raise ValueError('r>=0 and lam>0')
    return alpha*(1+r/lam)*math.exp(-r/lam)


def yukawa_ratio_sphere(alpha, R, r, lam):
    """Uniform sphere Yukawa/Newtonian force ratio, exterior r>=R.

    Stable form: for x=R/lam, y=r/lam,
    exp(-y)*3(x cosh x -sinh x)/x^3
    = 3[(x-1)exp(-y+x)+(x+1)exp(-y-x)]/(2x^3).
    Near x=0 use Taylor to avoid catastrophic cancellation.
    """
    if lam<=0 or R<0 or r<R: raise ValueError('lam>0, 0<=R<=r')
    if R==0: return yukawa_ratio_point(alpha,r,lam)
    x=R/lam; y=r/lam
    if x<0.08:
        return yukawa_ratio_point(alpha,r,lam)*yukawa_shape_factor(x)
    fexp=(3/(2*x**3))*((x-1)*math.exp(-(r-R)/lam)+(x+1)*math.exp(-(r+R)/lam))
    return alpha*(1+y)*fexp


def gravitational_redshift_small_height(g,h):
    return g*h/C**2


def instrument_gap(signal_m_s2, resolution_m_s2):
    if resolution_m_s2<=0: raise ValueError('resolution>0')
    return resolution_m_s2/abs(signal_m_s2) if signal_m_s2 else math.inf


def field_pseudoscalar(E,B):
    return dot(E,B)


def odd_b_residual_magnetic(B):
    """Ideal pure-magnetic reversal, Einstein-Maxwell stress-energy proxy."""
    Bneg=tuple(-x for x in B)
    return mag_energy_density(math.sqrt(dot(B,B)))-mag_energy_density(math.sqrt(dot(Bneg,Bneg)))


def scalar_tensor_tensor_G(Mstar_sq, xi, phi0):
    """Toy-model tensor coefficient in natural units only; NOT Cavendish G."""
    F=Mstar_sq+xi*phi0*phi0
    if F<=0: raise ValueError('positive F required')
    return 1/(8*math.pi*F)


def rank_design(rows, tol=1e-12):
    """Gaussian elimination on dimensionless design matrix (no numpy needed)."""
    if not rows: return 0
    m=[list(map(float,row)) for row in rows]
    n=len(m);p=len(m[0]);rank=0
    for col in range(p):
        pivot=max(range(rank,n),key=lambda i: abs(m[i][col])) if rank<n else None
        if pivot is None or abs(m[pivot][col])<tol: continue
        m[rank],m[pivot]=m[pivot],m[rank]
        scale=m[rank][col];m[rank]=[v/scale for v in m[rank]]
        for i in range(n):
            if i!=rank:
                factor=m[i][col]
                m[i]=[m[i][j]-factor*m[rank][j] for j in range(p)]
        rank+=1
    return rank


@dataclass(frozen=True)
class ClosedEnergyLedger:
    initial_battery:float
    transferred:float
    heat:float
    def check(self):
        if self.transferred<0 or self.heat<0 or self.transferred+self.heat>self.initial_battery:
            raise ValueError('invalid ledger inputs')
        before=self.initial_battery
        after=(self.initial_battery-self.transferred-self.heat)+self.transferred+self.heat
        return before, after, after-before


def experiment_synthetic_beta(seed=20261117, n=24, sigma_rel=1e-5, beta=2e-4):
    """Illustrative two-parameter regression: y/Gref = intercept + slope*x.
    Deliberately seeded from CODATA G, so NOT an experimental G prediction.
    """
    import random
    rng=random.Random(seed)
    xs=[-1+2*i/(n-1) for i in range(n)]
    ys=[1 + beta*x+rng.gauss(0,sigma_rel) for x in xs]
    mx=sum(xs)/n;my=sum(ys)/n
    slope=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs)
    intercept=my-slope*mx
    return {'n':n,'seed':seed,'beta_injected':beta,'beta_fitted':slope/intercept,
            'G_fitted':intercept*G_CODATA,'full_rank':rank_design([[1,x] for x in xs]),
            'fixed_rank':rank_design([[1,1]]*n)}


def maxwell_stress(E,B):
    """SI Maxwell stress for simultaneous E and B fields, in Cartesian lab frame."""
    E2=dot(E,E);B2=dot(B,B)
    return tuple(tuple(EPS0*(E[i]*E[j]-(E2/2 if i==j else 0))
                      +(B[i]*B[j]-(B2/2 if i==j else 0))/MU0
                      for j in range(3)) for i in range(3))


def parity_candidate_F_difference(xi, phi_background, induced_phi):
    """Toy scalar tensor coefficient F(phi)=Mstar²+xi*phi², difference B+ - B-.
    The induced pseudoscalar reverses sign when ideal E·B reverses.
    Values use dimensionless/natural-unit toy parameters, NOT observed physics.
    """
    return xi*((phi_background+induced_phi)**2-(phi_background-induced_phi)**2)
