"""Independent symbolic audit of homogeneous scalar and Faraday toy integrals.
Run: python tools/symbolic_checks.py
"""
import sympy as s
T=s.symbols('t',real=True);phi=s.Function('phi')(T)
M,xi,R,m,Lambda,F2=s.symbols('M xi R m Lambda F2',real=True,nonzero=True)
phidot=s.diff(phi,T)
# homogeneous natural units, + kinetic time derivative for (-+++) spacetime
lag=s.Rational(1,2)*(M*M+xi*phi**2)*R+s.Rational(1,2)*phidot**2-s.Rational(1,2)*m**2*phi**2-s.Rational(1,4)*(1+phi/Lambda)*F2
EL=s.simplify(s.diff(s.diff(lag,phidot),T)-s.diff(lag,phi))
assert s.simplify(EL-(s.diff(phi,T,2)+m**2*phi-xi*R*phi+F2/(4*Lambda)))==0
# Space volume of sphere and transverse second moment.
a,r,th,omega,c=s.symbols('a r th omega c',positive=True)
volume=s.integrate(r*r*s.sin(th),(th,0,s.pi),(r,0,a))*2*s.pi
assert s.simplify(volume-4*s.pi*a**3/3)==0
moment=s.integrate(r**4,(r,0,a))*s.integrate(s.sin(th)**3,(th,0,s.pi))*2*s.pi
assert s.simplify(moment/volume-2*a*a/5)==0
mu0,eps0,B0=s.symbols('mu0 eps0 B0',positive=True)
# sin/cos averaged over a full period in phase theta
q=s.symbols('q',real=True)
mean_cos=s.integrate(s.cos(q)**2,(q,0,2*s.pi))/(2*s.pi)
mean_sin=s.integrate(s.sin(q)**2,(q,0,2*s.pi))/(2*s.pi)
assert mean_cos==mean_sin==s.Rational(1,2)
U_B=volume*B0**2/(4*mu0)
U_E=eps0*volume*a*a*omega**2*B0**2/40
ratio=s.simplify(U_E/U_B)
assert s.simplify(ratio-eps0*mu0*a*a*omega**2/10)==0
print('PASS: scalar Euler-Lagrange, sphere volume, r_perp² average, harmonic averaging, Faraday energy ratio (5 checks)')
