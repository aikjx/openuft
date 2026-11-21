import unittest,math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
class TestMath(unittest.TestCase):
 def test_helix(self):
  for R,p in [(1,0),(2,.3),(10,.8),(.25,-.6)]:
   w=math.sqrt(1-p*p)/R;k=R*w*w;t=p*w
   self.assertAlmostEqual(k*k+t*t,w*w,places=12)
   self.assertAlmostEqual(k/(k*k+t*t),R,places=12)
 def test_spectrum(self):
  L=2*math.pi;a=.37
  self.assertAlmostEqual((2*math.pi*2/L+a)-(2*math.pi/L+a),2*math.pi/L)
 def test_rotation(self):
  g=9.80665;R=100;rpm=60/(2*math.pi)*math.sqrt(g/R)
  self.assertAlmostEqual((rpm*2*math.pi/60)**2*R,g)
 def test_yukawa(self):
  a=.01;lam=100
  self.assertAlmostEqual(a*(1+0/lam)*math.exp(0),a)
 def test_energy_scaling(self):
  self.assertAlmostEqual((20/10)**2,4)
if __name__=='__main__':unittest.main()
