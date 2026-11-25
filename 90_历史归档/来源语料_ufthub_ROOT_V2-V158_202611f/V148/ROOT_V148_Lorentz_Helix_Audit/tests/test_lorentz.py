import unittest,math
from root_v148.helix import NullHelix

class LorentzTests(unittest.TestCase):
    def setUp(self): self.h=NullHelix(.6,1,.8)
    def test_beta_zero(self): self.assertEqual(self.h.boost(0),self.h)
    def test_gamma_time_factor(self): self.assertAlmostEqual(self.h.doppler_particle(.3),(1-.24)/math.sqrt(.91))
    def test_boost_sample_freq(self): self.assertAlmostEqual(self.h.boost(.8).omega,5/3)
    def test_boost_sample_axis(self): self.assertAlmostEqual(self.h.boost(.8).u,0)
    def test_boost_sample_curvature(self): self.assertAlmostEqual(self.h.boost(.8).curvature(),5/3)
    def test_boost_sample_torsion(self): self.assertAlmostEqual(self.h.boost(.8).torsion(),0)
    def test_boost_changes_spatial_geometry(self): self.assertNotAlmostEqual(self.h.boost(.3).torsion(),self.h.torsion())
    def test_spatial_radius_invariant_axis_boost(self): self.assertEqual(self.h.boost(.3).a,self.h.a)
    def test_null_after_boost(self):
        for beta in [-.95,-.8,-.2,0,.2,.3,.8,.95]:
            self.assertAlmostEqual(self.h.boost(beta).speed(),1,places=11)
    def test_inverse_boost(self):
        for beta in [-.8,-.3,.4,.95]:
            hh=self.h.boost(beta).boost(-beta)
            self.assertAlmostEqual(hh.omega,self.h.omega,places=11)
            self.assertAlmostEqual(hh.u,self.h.u,places=11)
    def test_worldline_transform(self):
        beta=.3;hb=self.h.boost(beta)
        for t in [-10,-1,0,.25,7]:
            tp,xp,yp,zp=self.h.coordinate_boost(t,beta)
            x,y,z=hb.position(tp)
            for a,b in zip((xp,yp,zp),(x,y,z)):self.assertAlmostEqual(a,b,places=11)
    def test_spatial_speed_norm_grid(self):
        for u in [-.95,-.8,-.1,0,.1,.8,.95]:
            for beta in [-.9,-.25,0,.2,.75,.9]:
                h=NullHelix.from_u_omega(u,1.3).boost(beta)
                self.assertAlmostEqual(h.speed(),1,places=11)
    def test_boost_omega_from_time(self):
        for beta in [-.8,0,.3,.8]:
            h=self.h.boost(beta); self.assertAlmostEqual(h.omega*self.h.doppler_particle(beta),self.h.omega,places=11)
    def test_energy_momentum_transformation(self):
        # Four-momentum tangent to the null trajectory, at a given instant.
        beta=.3;gamma=1/math.sqrt(1-beta*beta)
        E=7.;pz=E*self.h.u
        self.assertAlmostEqual(gamma*(E-beta*pz)/E,self.h.doppler_particle(beta))
    def test_energy_helix_freq_product(self):
        for beta in [-.7,0,.3,.8]:
            D=self.h.doppler_particle(beta)
            self.assertAlmostEqual((D)*(1/D),1,places=11)
    def test_energy_helix_freq_ratio_mismatch(self):
        D=self.h.doppler_particle(.3)
        self.assertNotAlmostEqual(D,1/D)
        self.assertAlmostEqual(D/(1/D),D*D)
    def test_rest_axis_ratio(self): self.assertAlmostEqual(self.h.doppler_particle(.8)**2,.36)
    def test_curvature_and_torsion_not_scalars(self):
        new=self.h.boost(.3)
        self.assertGreater(abs(new.curvature()-self.h.curvature()),.01)
        self.assertGreater(abs(new.torsion()-self.h.torsion()),.01)
    def test_relativistic_velocity_formula(self): self.assertAlmostEqual(self.h.boost(.3).u, (.8-.3)/(1-.24))
    def test_negative_rotation_sign(self):
        h=NullHelix(.6,-1,.8)
        self.assertLess(h.boost(.3).torsion(),0)
    def test_invalid_beta(self):
        with self.assertRaises(ValueError):self.h.boost(1)
    def test_invalid_beta_minus(self):
        with self.assertRaises(ValueError):self.h.doppler_particle(-1)
