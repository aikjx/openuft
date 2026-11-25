"""ROOT V135: physically labelled baseline and *hypothetical* Yukawa models.

Uses SI numbers in numerical astronomy, while field-theory conventions in docs
are c=1 (G and hbar not normalized). No network and no fitted observations.
Standard-library only. All externally adopted numbers have sources in docs.
"""
from __future__ import annotations
from dataclasses import dataclass
import math

G = 6.67430e-11   # NIST CODATA 2022, m^3 kg^-1 s^-2
G_STD_UNC = 0.00015e-11
HBAR = 1.054571817e-34  # J s, SI convention; not set to one
MU_EARTH = 398600.435507e9  # JPL DE440 m^3 s^-2
MU_MOON = 4902.800118e9
R_EARTH_MEAN = 6371e3
R_EARTH_EQUATOR = 6378137.0
R_EARTH_POLAR = 6356752.314245
R_MOON = 1737.4e3
J2_EARTH = 1.08263e-3
OMEGA_EARTH = 7.292115e-5  # rad/s
ROOT_ALPHA = 1.0/3.0
ROOT_LAMBDA = 124600.0

@dataclass(frozen=True)
class Layer:
    inner_m: float
    outer_m: float
    density_kg_m3: float

# V132 inherited *illustrative* five-layer model, not a PREM reconstruction.
EARTH_LAYERS = (
    Layer(0., 1221500., 13000.),
    Layer(1221500., 3480000., 11000.),
    Layer(3480000., 5701000., 5000.),
    Layer(5701000., 6346600., 3800.),
    Layer(6346600., 6371000., 2800.),
)
# Illustrative Moon layers. Not measured lunar density inversion.
MOON_LAYERS = (
    Layer(0., 350000., 5200.),
    Layer(350000., 1400000., 3400.),
    Layer(1400000., 1700000., 3000.),
    Layer(1700000., 1737400., 2800.),
)


def dot(a, b):
    return sum(x*y for x,y in zip(a,b))


def norm(v):
    return math.sqrt(dot(v,v))


def vec_scale(k, v):
    return tuple(k*x for x in v)


def mass_shells(layers):
    return sum(4*math.pi*l.density_kg_m3*(l.outer_m**3-l.inner_m**3)/3 for l in layers)


def check_shells(layers):
    if not layers: raise ValueError('empty layer list')
    last = 0.
    for l in layers:
        if abs(l.inner_m-last)>1e-8 or l.outer_m<=l.inner_m or l.density_kg_m3 <=0:
            raise ValueError('shells must be contiguous, increasing and positive-density')
        last=l.outer_m
    return last


def shell_cumulative_mass(r, layers):
    R=check_shells(layers)
    if r<0 or not math.isfinite(r): raise ValueError('invalid radius')
    if r>=R: return mass_shells(layers)
    total=0.
    for l in layers:
        if r>=l.outer_m:
            total += 4*math.pi*l.density_kg_m3*(l.outer_m**3-l.inner_m**3)/3
        elif r>l.inner_m:
            total += 4*math.pi*l.density_kg_m3*(r**3-l.inner_m**3)/3
            break
        else: break
    return total


def internal_g(r, layers):
    if r==0: return 0.
    return G*shell_cumulative_mass(r,layers)/r**2


def newton_vector(x, mu):
    r=norm(x)
    if r<=0: raise ValueError('point mass field singular at origin')
    return vec_scale(-mu/(r**3),x)


def j2_potential(x):
    r=norm(x)
    if r<=0: raise ValueError('invalid radius')
    cos_theta=x[2]/r
    p2=0.5*(3*cos_theta*cos_theta-1)
    return -MU_EARTH/r * (1-J2_EARTH*(R_EARTH_EQUATOR/r)**2*p2)


def j2_gravity(x):
    xx, yy, zz=x
    r=norm(x)
    if r<=0: raise ValueError('invalid radius')
    z2=5*(zz/r)**2
    c=-1.5*MU_EARTH*J2_EARTH*R_EARTH_EQUATOR**2/r**5
    return (c*xx*(1-z2),c*yy*(1-z2),c*zz*(3-z2))


def earth_gravity(x):
    return tuple(a+b for a,b in zip(newton_vector(x,MU_EARTH),j2_gravity(x)))


def earth_rotating_effective(x):
    a=earth_gravity(x)
    return (a[0]+OMEGA_EARTH**2*x[0],a[1]+OMEGA_EARTH**2*x[1],a[2])


def gradient_numeric(f,x,step=1.):
    out=[]
    for i in range(len(x)):
        p=list(x); m=list(x)
        p[i]+=step; m[i]-=step
        out.append((f(p)-f(m))/(2*step))
    return tuple(out)


def yukawa_compensated_mass_analytic(layers, lam):
    """Q exp(-R/lam) for outside spherical source (kg).

    With Q = 4pi int rho(s) s^2 sinh(s/lam)/(s/lam) ds.
    Evaluates stable exponentials with R shift; reliable for lam << R.
    For long lambda, use quadrature to avoid cancellation of large terms.
    """
    R=check_shells(layers)
    if lam<=0 or not math.isfinite(lam): raise ValueError('positive finite range required')
    if lam>R*0.9:
        return yukawa_compensated_mass_simpson(layers,lam,256)
    acc=0.
    for lay in layers:
        a,b,rho=lay.inner_m,lay.outer_m,lay.density_kg_m3
        def prim(x):
            return ((x-lam)*math.exp(-(R-x)/lam)+
                    (x+lam)*math.exp(-(R+x)/lam))
        acc+=2*math.pi*rho*lam**2*(prim(b)-prim(a))
    return acc


def yukawa_compensated_mass_simpson(layers, lam, n=1024):
    R=check_shells(layers)
    if lam<=0 or n<=0 or n%2: raise ValueError('invalid quadrature')
    total=0.
    for lay in layers:
        h=(lay.outer_m-lay.inner_m)/n
        subtotal=0.
        for i in range(n+1):
            s=lay.inner_m+h*i
            # Numerically stable angular integration.
            weighted=0.5*lam*s*(math.exp(-(R-s)/lam)-math.exp(-(R+s)/lam))
            subtotal+=(1 if i==0 or i==n else 4 if i%2 else 2)*weighted
        total+=4*math.pi*lay.density_kg_m3*h*subtotal/3
    return total


def yukawa_shape(layers,lam):
    """Unit-alpha exterior acceleration fraction at the source surface r=R."""
    R=check_shells(layers)
    return yukawa_compensated_mass_analytic(layers,lam)/mass_shells(layers)*(1+R/lam)


def yukawa_accel_ratio(r, layers, alpha=ROOT_ALPHA, lam=ROOT_LAMBDA):
    """F_Y/F_N: same underlying spherical density; r >= R."""
    R=check_shells(layers)
    if r<R or not math.isfinite(r): raise ValueError('exterior field only')
    C=yukawa_compensated_mass_analytic(layers,lam)
    return alpha*(C/mass_shells(layers))*(1+r/lam)*math.exp(-(r-R)/lam)


def yukawa_accel_ratio_numeric(r,layers,alpha=ROOT_ALPHA,lam=ROOT_LAMBDA):
    R=check_shells(layers)
    if r<R: raise ValueError('exterior only')
    C=yukawa_compensated_mass_simpson(layers,lam)
    return alpha*C/mass_shells(layers)*(1+r/lam)*math.exp(-(r-R)/lam)


def yukawa_vector(x,mu,layers,alpha=ROOT_ALPHA,lam=ROOT_LAMBDA):
    r=norm(x)
    return vec_scale(yukawa_accel_ratio(r,layers,alpha,lam),newton_vector(x,mu))


def point_yukawa_ratio(r,alpha=ROOT_ALPHA,lam=ROOT_LAMBDA):
    return alpha*(1+r/lam)*math.exp(-r/lam)


def dipole_field(x, magnetic_moment=(0.,0.,1.)):
    """Field in arbitrary common units (geometric direction only)."""
    r=norm(x)
    if r<=0: raise ValueError('origin')
    nhat=vec_scale(1/r,x)
    d=dot(nhat,magnetic_moment)
    return tuple((3*d*nhat[i]-magnetic_moment[i])/r**3 for i in range(3))


def helix(t,a,omega,u):
    return (a*math.cos(omega*t),a*math.sin(omega*t),u*t)


def helix_velocity(t,a,omega,u):
    return (-a*omega*math.sin(omega*t),a*omega*math.cos(omega*t),u)


def helix_acceleration(t,a,omega,u):
    return (-a*omega*omega*math.cos(omega*t),-a*omega*omega*math.sin(omega*t),0.)


def helix_curvature_torsion(a,omega,u):
    v2=(a*omega)**2+u*u
    if a<=0 or omega==0 or v2<=0: raise ValueError('regular nonzero-curvature helix required')
    return a*omega*omega/v2, u*omega/v2


def fit_fractional_offset_and_alpha(height_m, y, sigma_y, layers, lam=ROOT_LAMBDA):
    """Weighted linear fit: y_i = beta + alpha * H_i (fractional acceleration).
    Here y are supplied dimensionless residuals, errors are dimensionless sigma.
    No genuine observation data are bundled; run with synthetic checks.
    """
    if len(height_m)!=len(y) or len(y)!=len(sigma_y) or len(y)<2:
        raise ValueError('need matching arrays with at least two points')
    R=check_shells(layers)
    hval=[yukawa_accel_ratio(R+h,layers,alpha=1.,lam=lam) for h in height_m]
    W=[1/s**2 if s>0 else math.nan for s in sigma_y]
    if not all(math.isfinite(w) for w in W): raise ValueError('positive finite error needed')
    s0=sum(W); s1=sum(w*z for w,z in zip(W,hval))
    s2=sum(w*z*z for w,z in zip(W,hval))
    t0=sum(w*v for w,v in zip(W,y))
    t1=sum(w*z*v for w,z,v in zip(W,hval,y))
    det=s0*s2-s1*s1
    # Numerically meaningful rank guard.
    if det<=1e-14*max(s0*s2,1.):
        raise ValueError('non-identifiable: heights do not separate offset from range-dependence')
    beta=(t0*s2-t1*s1)/det
    alpha=(t1*s0-t0*s1)/det
    sigma_alpha=math.sqrt(s0/det)
    return {'beta':beta,'alpha':alpha,'sigma_alpha':sigma_alpha,
            'chi2':sum(w*(v-beta-alpha*z)**2 for w,v,z in zip(W,y,hval)),
            'dof':len(y)-2}


def yukawa_potential_per_kg(r, mu, layers, alpha=ROOT_ALPHA, lam=ROOT_LAMBDA):
    """Exterior Yukawa specific potential [m^2/s^2] (mass anchor is mu/G)."""
    R=check_shells(layers)
    if r<R: raise ValueError('exterior only')
    q=yukawa_compensated_mass_analytic(layers,lam)/mass_shells(layers)
    return -mu*alpha*q*math.exp(-(r-R)/lam)/r


def gravitational_specific_potential(r,mu):
    if r<=0: raise ValueError('positive radius needed')
    return -mu/r


def uniform_sphere_yukawa_shape(R,lam):
    """Stable unit-alpha surface shape, independent check for homogeneous sphere."""
    x=R/lam
    if not (0<x<60): raise ValueError('x in (0,60) for direct check')
    # Q/M = 3*(x*cosh(x)-sinh(x))/x^3, multiplied by (1+x)*exp(-x).
    return (3*(x*math.cosh(x)-math.sinh(x))/x**3)*(1+x)*math.exp(-x)


def near_circular_orbit_frequencies(r, mu, layers, alpha=ROOT_ALPHA, lam=ROOT_LAMBDA):
    """Newton+Yukawa only, spherical body. Returns Ω², κ_r², Δϖ radians/revolution.

    Ω²=Φ'(r)/r, κ_r²=Φ''(r)+3Φ'(r)/r.
    Not a full GR/J2/tidal orbit solution. Uses perturbation of a nearly circular orbit.
    """
    R=check_shells(layers)
    if r<R: raise ValueError('exterior only')
    C=yukawa_compensated_mass_analytic(layers,lam)
    s=alpha*(C/mass_shells(layers))*math.exp(-(r-R)/lam)
    xi=s*(1+r/lam)
    omega2=mu/r**3*(1+xi)
    kr2=mu/r**3*(1+xi-s*(r/lam)**2)
    if omega2<=0 or kr2<=0:
        return {'Omega2_s_minus2':omega2,'kappa2_s_minus2':kr2,'precession_rad_per_rev':None,
                'stable':False}
    return {'Omega2_s_minus2':omega2,'kappa2_s_minus2':kr2,
            'precession_rad_per_rev':2*math.pi*(math.sqrt(omega2/kr2)-1),
            'stable':True}
