"""Release readiness checks on equations, data provenance and machine-readable experiments."""
from pathlib import Path
import csv,json,unittest
R=Path(__file__).resolve().parent.parent

class TestProjectCatalog(unittest.TestCase):
    def test_equation_catalog_exists(self):self.assertTrue((R/'data/equation_catalog.csv').is_file())
    def test_equations_provenance(self):
        with (R/'data/equation_catalog.csv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
        self.assertGreaterEqual(len(rows),70)
        self.assertEqual(len({v['id'] for v in rows}),len(rows))
        self.assertTrue(all(v['equation'] and v['proof_status'] and v['assumptions'] for v in rows))
    def test_open_problem_not_marked_proven(self):
        with (R/'data/equation_catalog.csv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
        for v in rows:
            if v['name'] in ('completed universal quantum gravity','completed strong/weak/gravity GUT'):
                self.assertEqual(v['proof_status'],'O')
    def test_method_catalog_exists(self):
        with (R/'data/method_matrix.csv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
        self.assertGreaterEqual(len(rows),36)
    def test_distinct_statuses(self):
        with (R/'data/equation_catalog.csv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
        self.assertTrue({'E','C','H','O','R'}<=set(v['proof_status'] for v in rows))

class TestProtocols(unittest.TestCase):
    def test_protocols_all_valid_json(self):
        for p in sorted((R/'protocols').glob('*.json')):
            with self.subTest(name=p.name):self.assertIsInstance(json.loads(p.read_text(encoding='utf8')),dict)
    def test_four_protocols(self):self.assertEqual(len(list((R/'protocols').glob('*.json'))),4)
    def test_no_fabricated_observation(self):
        for p in (R/'protocols').glob('*.json'):
            d=json.loads(p.read_text(encoding='utf8'))
            self.assertIs(d['observation_performed'],False)
    def test_protocol_assumptions(self):
        for p in (R/'protocols').glob('*.json'):
            d=json.loads(p.read_text(encoding='utf8'))
            self.assertTrue(d['controls'])
            self.assertTrue(d['no_claims'])
            self.assertTrue(d['pass_if'])

class TestDatasetProvenance(unittest.TestCase):
    def test_numerical_summary_is_not_observed(self):
        d=json.loads((R/'results/numerical_summary.json').read_text(encoding='utf8'))
        self.assertEqual(d['status'],'THEORY_AND_SYNTHETIC_ONLY')
        self.assertIs(d['G_independently_derived'],False)
        self.assertIs(d['physical_unification_proven'],False)
    def test_synthetic_dataset_marked(self):
        with (R/'data/synthetic_source_switch.csv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),80)
        self.assertEqual({v['provenance'] for v in rows},{'SYNTHETIC'})
    def test_dimensionless_integrals(self):
        x=json.loads((R/'results/independent_integral_check.json').read_text())
        self.assertAlmostEqual(x['normalization'],1,places=12)
        self.assertAlmostEqual(x['gaussian_self_energy_ratio'],1,places=12)
    def test_interactive_html_offline(self):
        x=(R/'web/index.html').read_text(encoding='utf8')
        self.assertNotIn('<script src=',x)
        self.assertIn('非实测',x)
    def test_document_no_proof_claim(self):
        text=(next((R/'book').glob('*.md'))).read_text(encoding='utf8')
        self.assertIn('不宣称解决量子引力',text)
        self.assertIn('没有证明',text)

if __name__=='__main__':unittest.main()
