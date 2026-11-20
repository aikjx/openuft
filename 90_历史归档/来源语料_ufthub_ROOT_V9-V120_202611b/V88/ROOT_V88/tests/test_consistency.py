import unittest,json,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class TestOutputs(unittest.TestCase):
 def test_manifest_docs(self):self.assertTrue((ROOT/'README.md').exists())
 def test_scientific_boundaries(self):
  s=(ROOT/'PROOF_STATUS.md').read_text(encoding='utf8')
  self.assertIn('未证明',s)
  self.assertIn('经典',s)
 def test_sources_present(self):self.assertTrue((ROOT/'SOURCES.md').exists())
 def test_browser_offline(self):
  s=(ROOT/'web/index.html').read_text(encoding='utf8')
  self.assertIn('ROOT V88',s);self.assertIn('input',s)
 def test_protocols(self):
  for file in (ROOT/'protocols').glob('*.json'):
   p=json.loads(file.read_text(encoding='utf8'))
   self.assertIn('controls',p)
   self.assertIn('failure_conditions',p)
 def test_data_labels(self):
  s=(ROOT/'scripts/generate_results.py').read_text(encoding='utf8')
  self.assertIn('SYNTHETIC',s)
if __name__=='__main__':unittest.main()
