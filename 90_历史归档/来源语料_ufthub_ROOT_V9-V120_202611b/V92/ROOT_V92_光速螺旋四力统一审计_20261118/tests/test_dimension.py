import unittest
from src.dimension_audit import build
class TestDimensions(unittest.TestCase):
 def test_full_audit(self):
  info=build()
  self.assertEqual(info['base_catalog'],26)
  self.assertGreater(info['pairwise_collisions'],500)
  self.assertGreaterEqual(info['dimension_failures'],5)
  self.assertNotEqual(info['Z_dimension'],info['Zprime_dimension'])
if __name__=='__main__':unittest.main()
