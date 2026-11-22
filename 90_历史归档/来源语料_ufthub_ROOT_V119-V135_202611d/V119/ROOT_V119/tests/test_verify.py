import math, unittest
class TestHelix(unittest.TestCase):
    def test_geometric_identity(self):
        for R,p in [(0.25,0),(1,.6),(2,-.8),(.8,.95),(3,.999)]:
            w=math.sqrt(1-p*p)/R
            k=R*w*w; t=p*w
            self.assertAlmostEqual(k*k+t*t,w*w,places=12)
            self.assertAlmostEqual(k/(k*k+t*t),R,places=12)
    def test_free_scale(self):
        # For fixed p, every positive R satisfies normalization after adjusting omega.
        for R in [.1,1,100]:
            p=.6;w=math.sqrt(1-p*p)/R
            self.assertAlmostEqual((R*w)**2+p*p,1)
if __name__=='__main__':unittest.main()
