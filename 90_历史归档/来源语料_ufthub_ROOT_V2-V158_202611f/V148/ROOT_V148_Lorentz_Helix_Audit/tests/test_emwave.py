import unittest,math
from root_v148.emwave import CircularWave
from root_v148.helix import dot,norm

class ElectromagneticTests(unittest.TestCase):
    def setUp(self): self.w=CircularWave(3,2,1)
    def test_fields_transverse(self):
        for t in [0,.2,1.1]:
            E,B=self.w.fields(t,.3);self.assertEqual(E[2],0);self.assertEqual(B[2],0)
    def test_field_orthogonality(self):
        for t in [-2,0,.4]:
            E,B=self.w.fields(t,.2);self.assertAlmostEqual(dot(E,B),0)
    def test_equal_magnitude(self):
        for t in [-.9,0,.2,2.4]:
            E,B=self.w.fields(t,0);self.assertAlmostEqual(norm(E),norm(B))
    def test_invariants_zero(self):
        for t in [0,.2,1.4]:
            v=self.w.invariants(t,.5)
            for x in v:self.assertAlmostEqual(x,0,places=11)
    def test_poynting(self):
        for t in [-2,0,1.7]:
            x,y,z=self.w.poynting(t,.4)
            self.assertAlmostEqual(x,0);self.assertAlmostEqual(y,0);self.assertAlmostEqual(z,4)
    def test_maxwell_faraday(self):
        for t in [0,.3,1]:
            residual=self.w.maxwell_residuals(t,.4)[0]
            for v in residual:self.assertAlmostEqual(v,0,places=11)
    def test_maxwell_ampere(self):
        for t in [0,.3,1]:
            residual=self.w.maxwell_residuals(t,.4)[1]
            for v in residual:self.assertAlmostEqual(v,0,places=11)
    def test_divergence_zero(self):self.assertEqual(self.w.maxwell_residuals(.2,.4)[2:],(0,0))
    def test_negative_helicity_maxwell(self):
        w=CircularWave(3,2,-1)
        for v in w.maxwell_residuals(.5,.9)[:2]:
            for x in v:self.assertAlmostEqual(x,0,places=12)
    def test_negative_helicity_propagates_forward(self):self.assertAlmostEqual(CircularWave(2,3,-1).poynting(.2,.4)[2],9)
    def test_amplitude_lorentz_doppler(self):
        beta=.3; b=self.w.boost(beta)
        self.assertAlmostEqual(b.amplitude/self.w.amplitude,math.sqrt((1-beta)/(1+beta)))
    def test_k_lorentz_doppler(self):
        beta=.8; b=self.w.boost(beta)
        self.assertAlmostEqual(b.k/self.w.k,1/3)
    def test_frequency_and_energy_transform_same_way(self):
        for beta in [-.95,-.4,0,.2,.8]:
            b=self.w.boost(beta)
            self.assertAlmostEqual(b.amplitude/self.w.amplitude,b.k/self.w.k)
    def test_phase_covariance(self):
        for beta in [-.8,-.3,0,.7,.95]:
            for t,z in [(.2,.4),(-1.,1.),(3.,-.1)]:
                p,q=self.w.phase_covariance(t,z,beta)
                self.assertAlmostEqual(p,q,places=11)
    def test_helix_vs_wave_doppler_distinct(self):
        from root_v148.helix import NullHelix
        h=NullHelix(.6,1,.8)
        self.assertNotAlmostEqual(h.boost(.3).omega/h.omega,self.w.boost(.3).k/self.w.k)
    def test_steady_energy_direction(self):
        w=CircularWave(4,2,1)
        self.assertAlmostEqual(w.poynting(0,0)[2],w.poynting(.55,.4)[2])
    def test_invalid_handedness(self):
        with self.assertRaises(ValueError):CircularWave(1,1,0)
    def test_invalid_k(self):
        with self.assertRaises(ValueError):CircularWave(-1,1,1)
    def test_invalid_boost(self):
        with self.assertRaises(ValueError):self.w.boost(-1)
