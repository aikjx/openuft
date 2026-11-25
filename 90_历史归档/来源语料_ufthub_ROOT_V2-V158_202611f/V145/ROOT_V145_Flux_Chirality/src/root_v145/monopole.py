"""Unit-charge Dirac monopole on a round S2. Connection convention: holonomy exp(i integral A)."""
import cmath
import math
from math import factorial


def a_north_phi(theta: float, n: int) -> float:
    return (n/2)*(1-math.cos(theta))


def a_south_phi(theta: float, n: int) -> float:
    return -(n/2)*(1+math.cos(theta))


def f_theta_phi(theta: float, n: int) -> float:
    return (n/2)*math.sin(theta)


def transition_phase(phi: float, n: int) -> complex:
    return cmath.exp(1j*n*phi)


def analytical_flux(n: int) -> float:
    return 2*math.pi*n


def simpson_flux(n: int, steps: int = 4096) -> float:
    """Integrate F_theta_phi dtheta dphi by composite Simpson; phi integral exact."""
    if steps < 2 or steps % 2:
        raise ValueError('steps must be positive and even')
    h = math.pi/steps
    acc = f_theta_phi(0,n)+f_theta_phi(math.pi,n)
    for i in range(1,steps):
        acc += (4 if i%2 else 2)*f_theta_phi(i*h,n)
    return 2*math.pi*h*acc/3


def chern_number(n: int) -> int:
    if not isinstance(n,int):
        raise TypeError('quantized first Chern number must be an integer')
    return n


def section_norm_squared(n: int, k: int, radius: float = 1.0) -> float:
    """L2 norm of z^k in positive zero-mode bundle O(n-1), for round S2."""
    if not (n>0 and 0<=k<n and isinstance(k,int)):
        raise ValueError('require n>0, integer k in [0,n-1]')
    if radius<=0:
        raise ValueError('radius must be positive')
    return 4*math.pi*radius**2*factorial(k)*factorial(n-k-1)/factorial(n)


def section_norm_squared_simpson(n: int, k: int, radius: float = 1.0, steps: int = 4096) -> float:
    if not (n>0 and 0<=k<n):
        raise ValueError('invalid mode')
    if steps<2 or steps%2:
        raise ValueError('steps must be even')
    h=1/steps
    def integrand(s):
        return (s**k)*((1-s)**(n-k-1))
    total=integrand(0)+integrand(1)
    for j in range(1,steps):
        total+=(4 if j%2 else 2)*integrand(j*h)
    return 4*math.pi*radius**2*total*h/3
