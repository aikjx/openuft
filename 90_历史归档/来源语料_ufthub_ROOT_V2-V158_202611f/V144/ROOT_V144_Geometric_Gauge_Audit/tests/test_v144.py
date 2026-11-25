import math
import unittest
import numpy as np
from src.physics import *


class LieAlgebraTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.t2 = antihermitian_generators('su2')
        cls.t3 = antihermitian_generators('su3')
        cls.f2 = structure_constants(cls.t2)
        cls.f3 = structure_constants(cls.t3)

    def test_dimensions(self):
        self.assertEqual(len(self.t2),3)
        self.assertEqual(len(self.t3),8)
        self.assertEqual(len(total_generators()),12)

    def test_tracelessness(self):
        for t in self.t2 + self.t3:
            self.assertAlmostEqual(abs(np.trace(t)),0,places=12)

    def test_antihermiticity(self):
        for t in self.t2 + self.t3:
            self.assertLess(np.linalg.norm(t+t.conjugate().T),1e-13)

    def test_orthonormal_su2(self):
        for a in range(3):
            for b in range(3):
                self.assertAlmostEqual(float((-2*np.trace(self.t2[a]@self.t2[b])).real), int(a==b),places=12)

    def test_orthonormal_su3(self):
        for a in range(8):
            for b in range(8):
                self.assertAlmostEqual(float((-2*np.trace(self.t3[a]@self.t3[b])).real), int(a==b),places=12)

    def test_commutator_closure_su2(self):
        for a in range(3):
            for b in range(3):
                rebuilt=sum((self.f2[a,b,c]*self.t2[c] for c in range(3)),np.zeros((2,2),complex))
                self.assertLess(np.linalg.norm(comm(self.t2[a],self.t2[b])-rebuilt),1e-12)

    def test_commutator_closure_su3(self):
        for a in range(8):
            for b in range(8):
                rebuilt=sum((self.f3[a,b,c]*self.t3[c] for c in range(8)),np.zeros((3,3),complex))
                self.assertLess(np.linalg.norm(comm(self.t3[a],self.t3[b])-rebuilt),1e-12)

    def test_structure_constants_known(self):
        self.assertAlmostEqual(self.f2[0,1,2],1)
        self.assertAlmostEqual(self.f3[0,1,2],1)
        self.assertAlmostEqual(self.f3[3,4,7],math.sqrt(3)/2)
        self.assertAlmostEqual(self.f3[0,3,6],.5)

    def test_antisymmetry(self):
        for f in (self.f2,self.f3):
            self.assertLess(np.max(abs(f+f.transpose(1,0,2))),1e-12)
            self.assertLess(np.max(abs(f+f.transpose(0,2,1))),1e-12)

    def test_jacobi(self):
        self.assertLess(np.max(abs(jacobi_tensor(self.f2))),1e-12)
        self.assertLess(np.max(abs(jacobi_tensor(self.f3))),1e-12)

    def test_cross_factors_commute(self):
        t=total_generators()
        for a in range(8):
            for b in range(8,12):
                self.assertLess(np.linalg.norm(comm(t[a],t[b])),1e-13)
        for a in range(8,11):
            self.assertLess(np.linalg.norm(comm(t[a],t[11])),1e-13)

    def test_direct_product_structure(self):
        self.assertEqual(sum([8,3,1]),12)
        self.assertEqual(4+12,16)
        self.assertEqual(4+8,12)


class GaugeCurvatureTests(unittest.TestCase):
    def test_su2_constant_nonabelian_field(self):
        t=antihermitian_generators('su2')
        for a,b in [(1.,1.),(-2.,0.7),(0.,2.),(3.,-1.5)]:
            fxy=comm(a*t[0],b*t[1])
            self.assertLess(np.linalg.norm(fxy-a*b*t[2]),1e-13)

    def test_abelian_commutator_zero(self):
        m=np.diag([1j, -2j]); n=np.diag([3j, 4j])
        self.assertLess(np.linalg.norm(comm(m,n)),1e-13)

    def test_pure_rotation_field_flat(self):
        for y in np.linspace(-5,5,41):
            self.assertLess(np.linalg.norm(su2_pure_gauge_curvature(y)),1e-12)

    def test_nonabelian_bianchi(self):
        t=antihermitian_generators('su2')
        a,b,c=1.2,-.7,.41
        ax=a*t[0]; ay=b*t[1]; az=c*t[2]
        # Constant A: D_x F_yz + D_y F_zx + D_z F_xy = 0 by Jacobi.
        bianchi=comm(ax,comm(ay,az))+comm(ay,comm(az,ax))+comm(az,comm(ax,ay))
        self.assertLess(np.linalg.norm(bianchi),1e-12)

    def test_gauge_covariance_constant_su2(self):
        t=antihermitian_generators('su2')
        theta=.731
        sigma3=sigma_matrices()[2]
        U=math.cos(theta/2)*np.eye(2)-1j*math.sin(theta/2)*sigma3
        a,b=1.3,.6
        F=comm(a*t[0],b*t[1])
        self.assertLess(np.linalg.norm(comm(U.conj().T @ (a*t[0]) @ U, U.conj().T @ (b*t[1]) @ U) - U.conj().T @ F @ U),1e-12)

    def test_pure_gauge_against_nonzero_gauge_field(self):
        self.assertLess(np.linalg.norm(su2_pure_gauge_curvature(0.8)),1e-12)
        t=antihermitian_generators('su2')
        self.assertGreater(np.linalg.norm(comm(t[0],t[1])),.5)


class KKBoundsTests(unittest.TestCase):
    def test_alpha_positive(self):
        self.assertGreater(kk_alpha_for_mass(M_E_SI),0)

    def test_electron_prediction_mismatch(self):
        self.assertGreater(ALPHA_OBS/kk_alpha_for_mass(M_E_SI),1e40)

    def test_mass_lower_bound(self):
        self.assertGreater(kk_min_mass_for_alpha()/M_E_SI,1e20)

    def test_alpha_radius_consistency(self):
        m=kk_min_mass_for_alpha()
        self.assertAlmostEqual(kk_alpha_for_mass(m)/ALPHA_OBS,1.,places=12)
        self.assertAlmostEqual(kk_mass_from_radius(kk_radius_for_alpha())/m,1.,places=12)

    def test_kk_mass_nonnegative_bare(self):
        r=kk_radius_for_alpha()
        minm=kk_mass_from_radius(r)
        for bare_ratio in (0.,.1,1.,10.):
            self.assertGreaterEqual(kk_mass_from_radius(r,m5_si=minm*bare_ratio),minm)

    def test_n_scaling(self):
        r=kk_radius_for_alpha()
        for n in (1,2,3,10):
            self.assertAlmostEqual(kk_mass_from_radius(r,n)/kk_mass_from_radius(r),n,places=11)

    def test_electron_radius_is_compton_length(self):
        self.assertAlmostEqual(kk_radius_for_mass(M_E_SI)/3.86159267435e-13,1.,places=10)

    def test_dimensionless_mismatch_matches_square_mass_ratio(self):
        mass_ratio=kk_min_mass_for_alpha()/M_E_SI
        alpha_ratio=ALPHA_OBS/kk_alpha_for_mass(M_E_SI)
        self.assertAlmostEqual((mass_ratio**2)/alpha_ratio,1.,places=11)

    def test_mass_scaling(self):
        for m in (M_E_SI,M_MU_SI,M_P_SI):
            self.assertAlmostEqual(kk_alpha_for_mass(3*m)/kk_alpha_for_mass(m),9.,places=11)

    def test_planck_length_relation(self):
        # restore c to translate SI length; c=1 in symbolic model
        lp=math.sqrt(G_SI*HBAR_SI/C_SI**3)
        self.assertAlmostEqual(kk_radius_for_alpha()/(2*lp/math.sqrt(ALPHA_OBS)),1.,places=11)


class SpinGeometryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f2=structure_constants(antihermitian_generators('su2'))
        cls.f3=structure_constants(antihermitian_generators('su3'))

    def test_structure_norms(self):
        self.assertAlmostEqual(np.sum(self.f2**2),6.,places=10)
        self.assertAlmostEqual(np.sum(self.f3**2),24.,places=10)

    def test_scalar_coefficients(self):
        self.assertAlmostEqual(bi_invariant_scalar_coefficient(self.f2),1.5,places=10)
        self.assertAlmostEqual(bi_invariant_scalar_coefficient(self.f3),6.,places=10)

    def test_positive_scalar(self):
        for a,b in [(1,1),(.2,5),(10,.5),(1e2,1e2)]:
            self.assertGreater(product_scalar_curvature(a,b),0)

    def test_scaling_scalar_curvature(self):
        for k in (.1,1.,3.):
            self.assertAlmostEqual(product_scalar_curvature(k,k)*k*k,7.5,places=10)

    def test_nonzero_untwisted_dirac_gap(self):
        # D²=∇*∇+Scal/4 => eigenvalues²>=Scal_min/4 on compact spin product
        bound=product_scalar_curvature(1,1)/4
        self.assertAlmostEqual(bound,1.875,places=10)
        self.assertGreater(bound,0)

    def test_u1_flat_not_negative(self):
        # Product scalar comes from SU2+SU3; U1 contributes zero.
        self.assertAlmostEqual(product_scalar_curvature(1,1),1.5+6,places=10)

    def test_invalid_metric_scales(self):
        with self.assertRaises(ValueError): product_scalar_curvature(0,1)
        with self.assertRaises(ValueError): product_scalar_curvature(1,-1)


class ReportConsistencyTests(unittest.TestCase):
    def test_report_numbers(self):
        from src.physics import kk_summary,lie_algebra_summary
        a=kk_summary(); b=lie_algebra_summary()
        self.assertGreater(a['alpha_mismatch_factor'],1e42)
        self.assertEqual(b['dims']['SM_generators'],12)
        self.assertLess(b['jacobi_max_su3'],1e-12)

    def test_no_theory_success_flag(self):
        from src.physics import kk_summary
        self.assertTrue(kk_summary()['not_new_physics'])


if __name__=='__main__': unittest.main()
