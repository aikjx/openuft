"""Newton/J2/Yukawa weak-field and composition diagnostics.

Not a theory predicting G, a completed unification, or a report of observed fifth force.
Distances outside the spherical source; J2 radial field at fixed colatitude.
"""
import math

G = 6.67430e-11
G_U = 1.5e-15
C = 299792458.0
HBAR = 6.62607015e-34/(2*math.pi)
EARTH_R = 6378137.0
EARTH_J2 = 1.08262617385222e-3
EARTH_MU = 3.986004418e14

def check(*args):
    if not all(math.isfinite(float(x)) for x in args):
        raise ValueError('non-finite numerical parameter')

def positive(*args):
    check(*args)
    if not all(x>0 for x in args): raise ValueError('positive parameters required')

def p2(theta):
    check(theta)
    return (3*math.cos(theta)**2-1)/2

def point_envelope(r, length):
    positive(r,length)
    z=r/length
    if z>740: return 0.
    return math.exp(-z)

def sphere_envelope(radius,r,length):
    """F(R/lambda)*exp(-r/lambda) for r>=R, stable even R/lambda>>700."""
    check(radius,r,length)
    positive(r,length)
    if radius<0 or r<radius: raise ValueError('outside finite sphere required')
    if radius==0: return point_envelope(r,length)
    x=radius/length
    if x < .2:
        xx=x*x
        form=1+xx*(1/10+xx*(1/280+xx*(1/15120+xx/1330560)))
        return form*point_envelope(r,length)
    return 1.5/x**3*((x-1)*math.exp(-(r-radius)/length)
                       +(x+1)*math.exp(-(r+radius)/length))

def newton_g(mu,r):
    positive(mu,r)
    return mu/r**2

def j2_relative(radius,r,j2,theta):
    check(radius,r,j2,theta)
    positive(r)
    if radius<0 or r<radius:raise ValueError('outside source required')
    return -3*j2*(radius/r)**2*p2(theta)

def gravity(mu,r,radius=0.,j2=0.,theta=math.pi/2,
            alpha=0.,length=1.,q_source=1.,q_test=1.,u=0.):
    positive(mu,r,length)
    check(radius,j2,theta,alpha,q_source,q_test,u)
    if radius<0 or r<radius:raise ValueError('outside source required')
    y=j2_relative(radius,r,j2,theta)
    yuk=alpha*q_source*q_test*(1+r/length)*sphere_envelope(radius,r,length)
    return newton_g(mu,r)*(1+u+y+yuk)

def q_shape(mu,r,radius=0.,j2=0.,theta=math.pi/2,
            alpha=0.,length=1.,q_source=1.,q_test=1.,u=0.):
    """Q=-r g'(r)/(2g); radial g at FIXED theta, Newton+J2+Yukawa.

    Known J2 alone modifies Q. u assumed constant in r.
    """
    positive(mu,r,length)
    check(radius,j2,theta,alpha,q_source,q_test,u)
    if radius<0 or r<radius:raise ValueError('outside source required')
    y=j2_relative(radius,r,j2,theta)
    f=sphere_envelope(radius,r,length)
    A=alpha*q_source*q_test
    den=1+u+y+A*(1+r/length)*f
    if abs(den)<1e-14: raise ValueError('zero acceleration: Q undefined')
    return 1+(y+.5*A*(r/length)**2*f)/den

def normalized_D(q_source,q_i,q_j,alpha,r,length,radius=0.):
    """(a_i-a_j)/a_Newton; exact one-mediator separability in specified model."""
    positive(r,length)
    check(q_source,q_i,q_j,alpha,radius)
    return alpha*q_source*(q_i-q_j)*(1+r/length)*sphere_envelope(radius,r,length)

def eotvos_eta(q_source,q_i,q_j,alpha,r,length,radius=0.,universal=0.):
    """2(a_i-a_j)/(a_i+a_j), NOT generally rank-1 across sources/material pairs."""
    positive(r,length)
    check(q_source,q_i,q_j,alpha,radius,universal)
    h=(1+r/length)*sphere_envelope(radius,r,length)
    k=alpha*q_source*h
    den=2*(1+universal)+k*(q_i+q_j)
    if abs(den)<1e-14: raise ValueError('Eotvos ratio undefined')
    return 2*k*(q_i-q_j)/den

def gr_coupling_z(G_value=G):
    positive(G_value)
    return G_value*C/2

def gravitational_alpha(m,G_value=G):
    positive(m,G_value)
    return G_value*m*m/(HBAR*C)

def ratio_universal_GM(mu,source_mass,G_value=G):
    positive(mu,source_mass,G_value)
    return mu/(G_value*source_mass)
