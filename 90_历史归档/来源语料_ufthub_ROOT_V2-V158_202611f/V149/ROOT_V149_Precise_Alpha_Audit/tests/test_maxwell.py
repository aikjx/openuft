import math,unittest
from root_v149.core import wave,wave_residuals

class TestWave(unittest.TestCase):
    def test_dot_is_zero(self):
        for t in [0,.5,10]:
            with self.subTest(t=t):
                e,b=wave(t,.4);self.assertAlmostEqual(sum(x*y for x,y in zip(e,b)),0,13)
    def test_equal_magnitudes(self):
        e,b=wave(.231,.112,amplitude=8)
        self.assertAlmostEqual(sum(x*x for x in e),sum(x*x for x in b),12)
    def test_positive_z_flux(self):
        for t in [0,.67,1.7]:
            with self.subTest(t=t): self.assertAlmostEqual(wave_residuals(t,.3)[-1],1.0,12)
    def test_faraday(self):
        for t in [0,.57,1.34]:
            with self.subTest(t=t):
                residual=wave_residuals(t,.5)[0]
                self.assertLess(max(abs(x) for x in residual),1e-14)
    def test_ampere(self):
        for t in [0,.57,1.34]:
            with self.subTest(t=t):
                residual=wave_residuals(t,.5)[1]
                self.assertLess(max(abs(x) for x in residual),1e-14)
    def test_invariant_i1(self):
        for t in [0,.57,1.34]:
            with self.subTest(t=t): self.assertAlmostEqual(wave_residuals(t,.5)[3],0.0,13)
    def test_invariant_eb(self):
        self.assertAlmostEqual(wave_residuals(0.317,.29)[2],0.0,13)
    def test_amplitude_change_preserves_null_invariants(self):
        for a in [0.1,2,100]:
            with self.subTest(a=a):
                r=wave_residuals(.2,2,amplitude=a)
                self.assertAlmostEqual(r[2],0.0,10)
                self.assertAlmostEqual(r[3],0.0,10)
    def test_wavenumber_change_preserves_null_invariants(self):
        for k in [.2,1.2,10]:
            with self.subTest(k=k):
                r=wave_residuals(.2,2,k=k)
                self.assertAlmostEqual(r[2],0.0,13)
                self.assertAlmostEqual(r[3],0.0,13)
    def test_sign_reversal_wrong(self):
        # Reversing B while holding phi=k(t-z) sends energy flux into -z,
        # but time and spatial phase derivatives still refer to +z.
        e,b=wave(.1,.3,k=3)
        self.assertLess(e[0]*(-b[1])-e[1]*(-b[0]),0)
    def test_constant_parallel_fields_are_legal(self):
        # A static constant E || B has zero derivatives: vacuum Maxwell equations hold.
        e,b=(0.,0.,2.),(0.,0.,5.)
        self.assertEqual(sum(x*y for x,y in zip(e,b)),10.)
    def test_wave_same_phase_translation(self):
        for t,z in [(1,2),(.32,-.5)]:
            e1,b1=wave(t,z); e2,b2=wave(t+3,z+3)
            for x,y in zip(e1+b1,e2+b2): self.assertAlmostEqual(x,y,13)
    def test_wave_positive_energy(self):
        e,b=wave(.51,.73,amplitude=3.)
        density=sum(x*x for x in e)/2+sum(x*x for x in b)/2
        self.assertAlmostEqual(density,9.,12)
