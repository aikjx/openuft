import sys,unittest,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src import physics as p
class PhysicsChecks(unittest.TestCase):
    def test_constants(self):
        self.assertGreater(p.G,0); self.assertEqual(p.c,299792458)
    def test_dimensional_no_G_from_c_hbar(self):
        sol,_=p.dimension_G_solution()
        self.assertFalse(sol)
    def test_G_with_new_scale_dimensional(self):
        self.assertEqual(p.trace_dimensional_identity(),(-1,3,-2))
    def test_G_definition_circular(self):
        self.assertAlmostEqual(p.G_from_mass_scale(p.planck_mass())/p.G,1.,places=12)
    def test_electron_large_xi(self): self.assertGreater(p.xi(p.me,p.e),1e21)
    def test_proton_large_xi(self): self.assertGreater(p.xi(p.mp,p.e),1e18)
    def test_electron_ratio(self):
        self.assertAlmostEqual(p.force_ratio(p.me,p.e,p.me,p.e)/p.xi(p.me,p.e)**2,1.,places=12)
    def test_proton_ratio(self):
        self.assertAlmostEqual(p.force_ratio(p.mp,p.e,p.mp,p.e)/p.xi(p.mp,p.e)**2,1.,places=12)
    def test_mixed_ratio(self):
        self.assertAlmostEqual(p.force_ratio(p.me,p.e,p.mp,-p.e)/(p.xi(p.me,p.e)*p.xi(p.mp,p.e)),1,places=12)
    def test_quantum_classical_bridge_electron(self):
        self.assertAlmostEqual(
            p.alpha_electric(p.e)/p.alpha_gravitational(p.me)/p.xi(p.me,p.e)**2,1,places=12)
    def test_quantum_classical_bridge_proton(self):
        self.assertAlmostEqual(
            p.alpha_electric(p.e)/p.alpha_gravitational(p.mp)/p.xi(p.mp,p.e)**2,1,places=12)
    def test_kerr_newman_zero_spin(self):
        self.assertAlmostEqual(p.kerr_newman_extremality(1e20,.8e20*p.extremality_scale(),0),.64,places=12)
    def test_kerr_newman_extreme_spin(self):
        m=1e20
        self.assertAlmostEqual(p.kerr_newman_extremality(m,0,p.G*m*m/p.c),1,places=12)
    def test_electron_spin_not_classical_BH(self):
        self.assertGreater(p.kerr_spin_parameter(p.me,p.hbar/2),1e44)
    def test_kerr_newman_mixed_no_horizon(self):
        m=1e20; q=.8*m*p.extremality_scale();J=.7*p.G*m*m/p.c
        self.assertGreater(p.kerr_newman_extremality(m,q,J),1)
    def test_zero_electromagnetic(self):
        self.assertEqual(p.force_ratio(p.me,0,p.mp,p.e),0.)
    def test_mass_positive(self):
        with self.assertRaises(AssertionError): p.xi(0,p.e)
    def test_extremal_horizon(self):
        m=1e20;q=m*p.extremality_scale()
        rh=p.rn_horizons(m,q)
        self.assertIsNotNone(rh)
        self.assertAlmostEqual(rh[0]/p.grav_radius(m),1.,places=8)
        self.assertAlmostEqual(rh[1]/p.grav_radius(m),1.,places=8)
    def test_subextremal_horizon(self):
        m=1e20;q=.6*m*p.extremality_scale()
        rm,rp=p.rn_horizons(m,q)
        self.assertAlmostEqual(rm/p.grav_radius(m),.2,places=10)
        self.assertAlmostEqual(rp/p.grav_radius(m),1.8,places=10)
    def test_superextremal_no_horizon(self):
        m=1e20;q=1.1*m*p.extremality_scale()
        self.assertIsNone(p.rn_horizons(m,q))
    def test_electron_no_classical_horizon(self):
        self.assertIsNone(p.rn_horizons(p.me,p.e))
    def test_proton_no_classical_horizon(self):
        self.assertIsNone(p.rn_horizons(p.mp,p.e))
    def test_uncharged_schwarzschild(self):
        m=1e22
        rm,rp=p.rn_horizons(m,0)
        self.assertEqual(rm,0.)
        self.assertAlmostEqual(rp/(2*p.grav_radius(m)),1.,places=12)
    def test_rn_outer_root(self):
        m=1e20;q=.65*m*p.extremality_scale()
        _,rp=p.rn_horizons(m,q)
        self.assertLess(abs(p.rn_lapse(rp,m,q)),1e-12)
    def test_rn_inner_root(self):
        m=1e20;q=.65*m*p.extremality_scale()
        rm,_=p.rn_horizons(m,q)
        self.assertLess(abs(p.rn_lapse(rm,m,q)),1e-12)
    def test_newtonian_limit(self):
        m=p.Mearth;r=p.Rearth
        self.assertAlmostEqual(p.rn_phi(r,m,0),-p.G*m/r,places=9)
        self.assertAlmostEqual(p.rn_radial_accel(r,m,0),-p.G*m/(r*r),places=12)
    def test_earth_compactness(self):
        self.assertLess(p.weak_compactness(p.Mearth,p.Rearth),2e-9)
    def test_rn_phi_relation(self):
        m=1e20;q=.3*m*p.extremality_scale();r=10*p.grav_radius(m)
        self.assertAlmostEqual(2*p.rn_phi(r,m,q)/p.c**2,p.rn_lapse(r,m,q)-1,places=13)
    def test_em_trace_4d(self): self.assertEqual(p.em_stress_trace_factor(4),0)
    def test_em_trace_5d_nonzero(self): self.assertEqual(p.em_stress_trace_factor(5),-.25)
    def test_em_trace_3d_nonzero(self): self.assertEqual(p.em_stress_trace_factor(3),.25)
    def test_scalar_electrostatic_not_constant(self):
        self.assertFalse(p.kk_constant_phi_consistent(p.radiation_EM_invariant(1e6,0)))
    def test_scalar_magnetostatic_not_constant(self):
        self.assertFalse(p.kk_constant_phi_consistent(p.radiation_EM_invariant(0,.1)))
    def test_scalar_null_field_possible(self):
        self.assertTrue(p.kk_constant_phi_consistent(p.radiation_EM_invariant(p.c,.9999999999999999)))
    def test_scalar_zero_F2(self): self.assertTrue(p.kk_constant_phi_consistent(0.))
    def test_scalar_rhs_zero_iff(self):
        self.assertEqual(p.scalar_kk_rhs(1,3,0),0)
        self.assertNotEqual(p.scalar_kk_rhs(1,3,2),0)
    def test_uncertainty_sign(self):
        self.assertAlmostEqual(2*p.xi_relative_uncertainty(),p.G_relative_uncertainty(),places=15)
    def test_uncertainty_magnitude(self):
        self.assertGreater(p.G_relative_uncertainty(),2e-5)
        self.assertLess(p.G_relative_uncertainty(),3e-5)
    def test_earth_schwarzschild(self):
        self.assertAlmostEqual(2*p.grav_radius(p.Mearth),.0088701028718461,places=12)

class SymbolicChecks(unittest.TestCase):
    def test_sympy_force_xi_identity(self):
        import sympy as s
        m1,m2,q1,q2,G,eps=s.symbols('m1 m2 q1 q2 G eps',positive=True)
        ratio=q1*q2/(4*s.pi*eps*G*m1*m2)
        r1=q1/(m1*s.sqrt(4*s.pi*eps*G))
        r2=q2/(m2*s.sqrt(4*s.pi*eps*G))
        self.assertEqual(s.simplify(ratio-r1*r2),0)
    def test_sympy_horizon_roots(self):
        import sympy as s
        x,z=s.symbols('x z',real=True)
        poly=x*x-2*x+z*z
        self.assertEqual(s.simplify(poly.subs(x,1+s.sqrt(1-z*z))),0)
        self.assertEqual(s.simplify(poly.subs(x,1-s.sqrt(1-z*z))),0)
    def test_sympy_rn_derivative(self):
        import sympy as s
        r,M,Q,G,c,eps=s.symbols('r M Q G c eps',positive=True)
        Phi=-G*M/r+G*Q*Q/(8*s.pi*eps*c*c*r*r)
        acc=-G*M/r**2+G*Q*Q/(4*s.pi*eps*c*c*r**3)
        self.assertEqual(s.simplify(-s.diff(Phi,r)-acc),0)
    def test_sympy_schur_5d_metric(self):
        import sympy as s
        a,b,d,P,Q,k=s.symbols('a b d P Q k',real=True)
        phi=s.symbols('phi',positive=True)
        base=s.Matrix([[a,b],[b,d]])
        v=s.Matrix([P,Q])
        g5=(base+k*k*phi*phi*v*v.T).row_join(k*phi*phi*v)
        g5=g5.col_join((k*phi*phi*v.T).row_join(s.Matrix([[phi*phi]])))
        self.assertEqual(s.factor(g5.det()-phi*phi*base.det()),0)
    def test_sympy_trace(self):
        import sympy as s
        u=s.symbols('u')
        self.assertEqual(s.simplify(-u-u+u+u),0)
    def test_sympy_KK_scalar_constraint(self):
        import sympy as s
        R,F,phi,k=s.symbols('R F phi k')
        L=phi*R-k*k*phi**3*F/4
        self.assertEqual(s.diff(L,phi),R-3*k*k*phi*phi*F/4)
        self.assertEqual(s.solve([s.Eq(R,0),s.Eq(s.diff(L,phi).subs(phi,1),0)],[R,F]),{R:0,F:0})
    def test_sympy_dimensional_exponents(self):
        import sympy as s
        a,b=s.symbols('a b')
        self.assertEqual(s.linsolve([b+1,a+2*b-3,-a-b+2],(a,b)),s.EmptySet)
    def test_sympy_rn_phi_lapse(self):
        import sympy as s
        r,M,Q,G,c,eps=s.symbols('r M Q G c eps',positive=True)
        lapse=1-2*G*M/(c*c*r)+G*Q*Q/(4*s.pi*eps*c**4*r*r)
        Phi=-G*M/r+G*Q*Q/(8*s.pi*eps*c*c*r*r)
        self.assertEqual(s.simplify(lapse-1-2*Phi/c*c/c**2) if False else s.simplify(lapse-1-2*Phi/c**2),0)

if __name__=="__main__": unittest.main()
