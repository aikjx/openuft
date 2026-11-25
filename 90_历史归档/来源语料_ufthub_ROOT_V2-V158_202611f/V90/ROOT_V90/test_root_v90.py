import unittest
from root_v90 import make_weight_matrix, weighted_variance, phase_delta, relative_residual

class TestV90(unittest.TestCase):
    def test_nulling(self):
        a1=[1,1,1]; a2=[1,2,3]; a3=[1,4,9]
        w=make_weight_matrix(a1,a2,a3)
        self.assertAlmostEqual(sum(w[i]*a1[i] for i in range(3)),0,places=10)
        self.assertAlmostEqual(sum(w[i]*a2[i] for i in range(3)),0,places=10)
        self.assertAlmostEqual(sum(w[i]*a3[i] for i in range(3)),1,places=10)
    def test_variance(self):
        w=[1,2]; S=[[1,0],[0,4]]
        self.assertAlmostEqual(weighted_variance(w,S),17)
    def test_phase(self):
        G=6.67430e-11; hbar=1.054571817e-34
        p=phase_delta(1e-14,1e-14,4e-4,5e-4,5e-4,6e-4,1,G,hbar)
        self.assertTrue(math_isfinite(p))
    def test_singular(self):
        with self.assertRaises(ValueError):
            make_weight_matrix([1,1,1],[2,2,2],[3,3,3])
    def test_projection(self):
        self.assertGreater(relative_residual([1,0,0],[[0,1,0]]),0.99)

def math_isfinite(x):
    import math
    return math.isfinite(x)

if __name__ == "__main__":
    unittest.main()
