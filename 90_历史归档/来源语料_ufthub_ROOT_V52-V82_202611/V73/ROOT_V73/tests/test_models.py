import math
import unittest
import numpy as np
from rootv73.models import *

class V73Tests(unittest.TestCase):
    def test_helix_standard(self):
        d=helix_parameters(2.,3.,4.)
        self.assertAlmostEqual(d['speed'],math.sqrt(52))
        self.assertAlmostEqual(d['curvature'],18/52)
        self.assertAlmostEqual(d['torsion'],12/52)
    def test_helix_zeroomega(self):
        d=helix_parameters(1,0,3)
        self.assertEqual(d['curvature'],0)
        self.assertEqual(d['torsion'],0)
    def test_helix_sign_torsion(self):
        self.assertAlmostEqual(helix_parameters(2,3,4)['torsion'],-helix_parameters(2,3,-4)['torsion'])
    def test_helix_speed_c(self):
        R=15; theta=.2; d=helix_parameters(R,C*math.cos(theta)/R,C*math.sin(theta))
        self.assertAlmostEqual(d['speed']/C,1,places=14)
    def test_helix_invalid(self):
        with self.assertRaises(ValueError):helix_parameters(0,2,1)
    def test_rg_beta_negative(self):self.assertLess(rg_beta(.5),0)
    def test_rg_positive(self): self.assertGreater(scale_from_rg(100,.5),0)
    def test_rg_monotone_g(self): self.assertGreater(scale_from_rg(100,1),scale_from_rg(100,.8))
    def test_rg_monotone_mu(self):self.assertAlmostEqual(scale_from_rg(200,.5)/scale_from_rg(100,.5),2)
    def test_rg_calibration(self):
        g=coupling_for_scale(2.435e18,.2)
        self.assertAlmostEqual(scale_from_rg(2.435e18,g)/.2,1,places=12)
    def test_rg_hierarchy(self):self.assertGreater(dimensional_scale_hierarchy()['log_hierarchy'],40)
    def test_rg_sensitivity(self):
        g=.55; eps=1e-6; numeric=(math.log(scale_from_rg(1e8,g+eps))-math.log(scale_from_rg(1e8,g-eps)))/(2*eps)
        self.assertAlmostEqual(numeric/rg_scale_sensitivity(g),1,places=9)
    def test_rg_invalid(self):
        with self.assertRaises(ValueError):scale_from_rg(-1,.5)
    def test_rg_bad_target(self):
        with self.assertRaises(ValueError):coupling_for_scale(100,100)
    def test_species_n2_scaling(self):self.assertAlmostEqual(inferred_species_count(2)/inferred_species_count(1),.25)
    def test_species_hierarchy(self): self.assertGreater(inferred_species_count(.2),1e35)
    def test_dimensional_incompatible(self):
        # minimize over 2 free exponents: inconsistent system has nonzero residual
        matrix=np.array([[1,2],[0,1],[-1,-1]],float); target=np.array([3,-1,-2],float)
        x=np.linalg.lstsq(matrix,target,rcond=None)[0]
        self.assertGreater(np.linalg.norm(grav_dimensional_residual(*x)),.1)
    def test_dimensional_mass_time(self):
        self.assertEqual(grav_dimensional_residual(5,-1)[1],0)
        self.assertEqual(grav_dimensional_residual(5,-1)[0],0)
        self.assertNotEqual(grav_dimensional_residual(5,-1)[2],0)
    def test_uniform_longrange(self):self.assertAlmostEqual(uniform_yukawa_factor(6.3e6,1e16),1,places=8)
    def test_uniform_smallx(self):
        self.assertAlmostEqual(uniform_yukawa_factor(1,.01+100),point_yukawa_factor(1,100.01),delta=5e-5)
    def test_uniform_short(self):self.assertGreater(uniform_yukawa_factor(EARTH_R,1e6),point_yukawa_factor(EARTH_R,1e6))
    def test_uniform_huge(self):
        val=uniform_yukawa_factor(EARTH_R,1e3)
        self.assertGreaterEqual(val,0)
        self.assertTrue(math.isfinite(val))
    def test_uniform_1000km(self):self.assertAlmostEqual(uniform_yukawa_factor(EARTH_R,1e6),.2294,delta=.0004)
    def test_uniform_height_decline(self):self.assertGreater(uniform_yukawa_factor(EARTH_R,1e6),uniform_yukawa_factor(EARTH_R,1e6,1e6))
    def test_uniform_invalid_range(self):
        with self.assertRaises(ValueError):uniform_yukawa_factor(EARTH_R,0)
    def test_uniform_invalid_altitude(self):
        with self.assertRaises(ValueError):uniform_yukawa_factor(EARTH_R,1e6,-1)
    def test_layer_matches_uniform(self):
        R=EARTH_R; lam=1.5e6
        got=layered_yukawa_factor(R,lam,[(0,R,5513.4)])
        ref=uniform_yukawa_factor(R,lam)
        self.assertAlmostEqual(got/ref,1,places=12)
    def test_layer_split_uniform(self):
        R=EARTH_R; lam=1e6
        lay=[(0,R/2,5000),(R/2,R,5000)]
        self.assertAlmostEqual(layered_yukawa_factor(R,lam,lay),uniform_yukawa_factor(R,lam),places=10)
    def test_layer_different_density(self):
        self.assertGreater(abs(layered_yukawa_factor(EARTH_R,1e6,earth_two_layer_model())-uniform_yukawa_factor(EARTH_R,1e6)),.0005)
    def test_layer_invalid(self):
        with self.assertRaises(ValueError):layered_yukawa_factor(EARTH_R,1e6,[(1,EARTH_R,5000)])
    def test_layer_bad_density(self):
        with self.assertRaises(ValueError):layered_yukawa_factor(EARTH_R,1e6,[(0,EARTH_R,-1)])
    def test_eotvos_positive(self):self.assertGreater(eotvos_alpha_bound(1e7),0)
    def test_eotvos_material_difference(self):self.assertGreater(charge_fraction(22,47.867),charge_fraction(78,195.084))
    def test_eotvos_weak_shorter(self):self.assertGreater(eotvos_alpha_bound(1e6),eotvos_alpha_bound(1e7))
    def test_eotvos_invalidcharge(self):
        with self.assertRaises(ValueError):charge_fraction(0,1)
    def test_hadamard(self):
        H=hadamard_design(); self.assertTrue(np.array_equal(H.T@H,8*np.eye(8)))
    def test_hadamard_balanced(self):self.assertEqual(int(np.sum(hadamard_design()[:,-1])),0)
    def test_eight_coefficients_recovered(self):
        coef=np.array([1,2,3,4,5,6,7,8],float)
        y=generate_eight_states(coef,seed=42)
        self.assertTrue(np.allclose(hadamard_design().T@y/8,coef))
    def test_triple_only(self):
        y=generate_eight_states([0,1,2,3,4,5,6,7]);self.assertAlmostEqual(triple_contrast(y),7)
    def test_triple_independent_offsets(self):
        y=generate_eight_states([18,1,2,3,4,5,6,0]);self.assertAlmostEqual(triple_contrast(y),0)
    def test_triple_badshape(self):
        with self.assertRaises(ValueError):triple_contrast([0,1])
    def test_triple_noise_variance(self):
        rng=np.random.default_rng(1); s=.4; vals=[triple_contrast(rng.normal(0,s,8)) for _ in range(2500)]
        self.assertAlmostEqual(np.std(vals),s/math.sqrt(8),delta=.012)
    def test_crossenv_identification(self):
        x=np.linspace(-1,1,12); y=.02+.5*x; ret=fit_cross_env(x,y)
        self.assertEqual(ret['rank'],2)
        self.assertAlmostEqual(ret['beta'],.5)
        self.assertAlmostEqual(ret['nuisance'],.02)
    def test_crossenv_rank1(self):self.assertEqual(fit_cross_env([1,1,1],[1,1,1])['rank'],1)
    def test_crossenv_bad(self):
        with self.assertRaises(ValueError):fit_cross_env([1],[1])
    def test_crossenv_confounded(self):
        x=np.linspace(0,1,10); true_beta=.2; instrumental_beta=.3
        self.assertAlmostEqual(fit_cross_env(x,(true_beta+instrumental_beta)*x)['beta'],.5)
    def test_axion_const_vanishes(self):self.assertEqual(abelian_axion_bulk_correction(0,2,3),0)
    def test_axion_gradient_sign(self): self.assertEqual(abelian_axion_bulk_correction(1,2,3),-abelian_axion_bulk_correction(-1,2,3))
    def test_axion_linear(self): self.assertEqual(abelian_axion_bulk_correction(2,2,3),2*abelian_axion_bulk_correction(1,2,3))

if __name__=='__main__':unittest.main()
