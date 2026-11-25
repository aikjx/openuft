import unittest
import sympy as sp
class TestHelix(unittest.TestCase):
    def test_01_identity(self):
        a,w,u=sp.symbols('a w u', positive=True)
        k=a*w*w/(a*a*w*w+u*u)
        tau=u*w/(a*a*w*w+u*u)
        self.assertEqual(sp.factor((k*k+tau*tau-w*w).subs(u*u,1-a*a*w*w)),0)
    def test_02_reconstruction(self):
        k=sp.Rational(3,5); tau=sp.Rational(4,5)
        w=sp.sqrt(k*k+tau*tau); a=k/w**2; u=tau/w
        self.assertEqual(w,1);self.assertEqual(a,sp.Rational(3,5));self.assertEqual(u,sp.Rational(4,5))
    def test_03_norm(self):
        a=sp.Rational(3,5);w=1;u=sp.Rational(4,5)
        self.assertEqual(a*a*w*w+u*u,1)
    def test_04_rotation_components(self):
        k=sp.Rational(3,5);tau=sp.Rational(4,5)
        self.assertEqual(sp.sqrt(k*k+tau*tau),1)
    def test_05_nonunique_dimensionless_ratio(self):
        # continuum of k/tau ratios possible, so alpha_em cannot be fixed by kinematics alone
        for q in (sp.Rational(1,10),sp.Rational(1,137),sp.Integer(1),sp.Integer(10)):
            u=1/sp.sqrt(1+q*q); a=q/sp.sqrt(1+q*q)
            self.assertEqual(sp.simplify(a*a+u*u),1)
            self.assertEqual(sp.simplify(a/u),q)

if __name__=='__main__':unittest.main()
