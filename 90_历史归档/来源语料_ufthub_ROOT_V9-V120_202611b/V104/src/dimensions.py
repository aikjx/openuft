"""Dimension vector uses SI base L,M,T,I exponents; checks are necessary not sufficient."""
from fractions import Fraction
from collections import OrderedDict

def d(L=0,M=0,T=0,I=0): return (L,M,T,I)
def mul(*factors): return tuple(sum(v[i] for v in factors) for i in range(4))
def powr(a,n): return tuple(v*n for v in a)
def div(a,b): return mul(a,powr(b,-1))
L=d(L=1); M=d(M=1); T=d(T=1); I=d(I=1)
velocity=div(L,T); curvature=powr(L,-1); omega=powr(T,-1)
force=mul(M,L,powr(T,-2)); charge=mul(I,T)
B=mul(M,powr(T,-2),powr(I,-1))
E=div(force,charge)
c=velocity; hbar=mul(M,powr(L,2),powr(T,-1))
G=mul(powr(L,3),powr(M,-1),powr(T,-2))
epsilon0=mul(powr(I,2),powr(T,4),powr(M,-1),powr(L,-3))
energy=mul(force,L); power=div(energy,T)
riemann=powr(L,-2)

TESTS=OrderedDict([
('omega = c*kappa', (omega,mul(c,curvature))),
('Lorentz magnetic force q*v*B', (force,mul(charge,velocity,B))),
('Lorentz electric force q*E', (force,mul(charge,E))),
('geometric normal force gamma*m*v²*kappa', (force,mul(M,powr(velocity,2),curvature))),
('radiation energy coefficient', (energy,mul(powr(charge,2),powr(velocity,3),powr(epsilon0,-1),powr(c,-3),curvature))),
('radiation minimum q²*v³/(eps*c³*L)', (energy,mul(powr(charge,2),powr(velocity,3),powr(epsilon0,-1),powr(c,-3),powr(L,-1)))),
('radiative Pmin Emin*v/L', (power,mul(energy,velocity,powr(L,-1)))),
('grav constant gamma*hbar*c/mstar²', (G,mul(hbar,c,powr(M,-2)))),
('grav constant gamma*c³/(hbar*kappa²)', (G,div(powr(c,3),mul(hbar,powr(curvature,2))))),
('Einstein Riemann vs Frenet curvature is different dimension', (riemann,curvature)),
('incorrect G = c', (G,c)),
('incorrect E = B', (E,B)),
('incorrect force = m*omega', (force,mul(M,omega))),
('incorrect B = c*kappa', (B,mul(c,curvature))),
])

def scan():
    return [{'label':key, 'lhs':lhs, 'rhs':rhs,'passes':lhs==rhs} for key,(lhs,rhs) in TESTS.items()]
