"""Dimension audit for attempted G-from-(c,hbar) formulae, not full dynamics."""
import unittest
import sympy as s

class TestGravityDimensions(unittest.TestCase):
    def test_01_no_powers_c_hbar_form_G(self):
        a,b=s.symbols('a b')
        eqs=[b+1, a+2*b-3, -a-b+2]
        self.assertEqual(s.solve(eqs,[a,b]),[])
    def test_02_mass_requirement_in_bare_hbar_c(self):
        a,b=s.symbols('a b')
        self.assertEqual(s.solve([b+1,-a-b+2],[a,b]),{a:3,b:-1})
        # these powers would yield L^(3-2)=L, not required L^3
        self.assertEqual(3+2*(-1),1)
    def test_03_dimensionless_gravitational_alpha(self):
        # alpha_G(E) = G E^2/(hbar c^5) in SI exponents (M,L,T).
        G=s.Matrix([-1,3,-2]); E=s.Matrix([1,2,-2]); hbar=s.Matrix([1,2,-1]); c=s.Matrix([0,1,-1])
        self.assertEqual(G+2*E-hbar-5*c,s.zeros(3,1))
    def test_04_no_claim_of_G_prediction(self):
        # g=xi*hbar*c/m*^2 is a valid expression if m* is an independent mass scale.
        G=s.Matrix([-1,3,-2]);hbar=s.Matrix([1,2,-1]);c=s.Matrix([0,1,-1]);m=s.Matrix([1,0,0])
        self.assertEqual(hbar+c-2*m,G)
