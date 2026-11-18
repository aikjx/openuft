"""Tests against independent SciPy implementations, and direct quadrature."""
import math,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.root_v67 import threshold_F,expint_e1,Helix
try:
 from scipy.special import exp1,jv,jn_zeros
 from scipy.integrate import quad
 SCIPY=True
except ImportError:
 SCIPY=False

@unittest.skipUnless(SCIPY,'SciPy needed for independent cross-check')
class IndependentTests(unittest.TestCase):
    def test_exponential_integral(self):
        for i in range(1,41):
            x=10**(-5+7*i/40)
            self.assertAlmostEqual(expint_e1(x),exp1(x),delta=2e-12*max(1,abs(exp1(x))))
    def test_threshold_quadrature(self):
        for mu in [0.03,0.1,0.4,0.7,1.,1.8,2.5]:
            x=mu**2
            actual=quad(lambda t:math.exp(-x*t)/t**2,1,math.inf,epsabs=2e-13)[0]
            self.assertAlmostEqual(threshold_F(mu),actual,delta=3e-12)
    def test_kg_disk_Bessel_energy(self):
        j=jn_zeros(1,1)[0]
        a=1.3;ampl=.8;k=.6;mass=.4;q=j/a;Omega=math.sqrt(q*q+k*k+mass*mass)
        exact=2*math.pi*Omega**2*a*a*ampl**2*jv(2,j)**2
        density=lambda r:2*math.pi*r*ampl**2*(Omega**2*jv(1,q*r)**2+q*q*( (jv(0,q*r)-jv(2,q*r))/2)**2+(jv(1,q*r)/r)**2 if r>0 else 0)
        # Better use actual energy density: Omega^2 |psi|² + |partial_r psi|² +n²/r² |psi|² +(k²+mass²)|psi|²
        def integrand(r):
            J1=jv(1,q*r); dJ=q*(jv(0,q*r)-jv(2,q*r))/2
            radial_term=(J1/r)**2 if r>0 else (q/2)**2
            return 2*math.pi*r*ampl**2*((Omega**2+k*k+mass*mass)*J1**2+dJ**2+radial_term)
        computed=quad(integrand,0,a,epsabs=1e-12,epsrel=1e-12)[0]
        self.assertAlmostEqual(computed,exact,delta=1e-11)
        self.assertAlmostEqual(jv(1,j),0,delta=1e-14)
