# -*- coding: utf-8 -*-
"""Contract tests in isolated temporary roots; do not create example research modules."""
import json
from pathlib import Path
import tempfile
import unittest
import module_catalog as catalog

class CatalogContract(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='openuft_catalog_')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.write('00_governance/module_types.json', catalog.read(catalog.ROOT / '00_governance/module_types.json'))
        self.write('00_governance/layout.json', {'systems': [], 'stages': ['00_project'], 'sections': []})
        (self.root / '01_systems').mkdir()

    def write(self, rel, value):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')

    def add(self, sid='s10000_example', kind='candidate_theory'):
        entry = {'id': sid, 'title': 'Isolated test fixture', 'kind': kind, 'status': 'unreviewed',
                 'premise_summary': 'Test only', 'premise_status': 'Not scientific content',
                 'source_records': [], 'postulates': [], 'related_systems': [], 'code_dependencies': []}
        self.write('01_systems/' + sid + '/system.json', entry)
        for rel in ['00_project/README.md', 'claims.csv', '08_data/data_registry.csv', '07_computation/runs/run_template.json']:
            path = self.root / '01_systems' / sid / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('{}', encoding='utf-8')
        self.write('01_systems/' + sid + '/07_computation/runs/run_template.json', {'system_id': sid})
        return entry

    def test_new_module_above_two_digit_range_is_discovered(self):
        self.add()
        self.assertEqual(catalog.refresh(self.root), [])
        self.assertEqual(catalog.check(self.root), [])
        self.assertEqual(catalog.read(self.root / '00_governance/layout.json')['systems'], ['s10000_example'])

    def test_type_change_keeps_id_and_old_module_bytes(self):
        self.add('s01_existing')
        old = (self.root / '01_systems/s01_existing/system.json').read_bytes()
        entry = self.add('p01_direction', 'unformulated_direction')
        self.assertEqual(catalog.refresh(self.root), [])
        entry['kind'] = 'candidate_theory'
        self.write('01_systems/p01_direction/system.json', entry)
        self.assertEqual(catalog.refresh(self.root), [])
        text = (self.root / '01_systems/TYPE_INDEX.md').read_text(encoding='utf-8')
        self.assertIn('| 待建模方向 | 0 |', text)
        self.assertEqual((self.root / '01_systems/s01_existing/system.json').read_bytes(), old)

    def test_unregistered_directory_is_rejected(self):
        (self.root / '01_systems/unknown').mkdir()
        self.assertIn('Unregistered directory: unknown', catalog.discover(self.root)[1])

    def test_unknown_type_refuses_partial_refresh(self):
        self.add()
        self.assertEqual(catalog.refresh(self.root), [])
        before = (self.root / '00_governance/system_registry.json').read_bytes()
        self.add('s02_unknown', 'made_up_type')
        self.assertTrue(catalog.refresh(self.root))
        self.assertEqual((self.root / '00_governance/system_registry.json').read_bytes(), before)

    def test_dangling_related_system_is_rejected(self):
        entry = self.add()
        entry['related_systems'] = ['missing_system']
        self.write('01_systems/s10000_example/system.json', entry)
        self.assertTrue(catalog.discover(self.root)[1])

    def test_reference_escape_is_rejected(self):
        entry = self.add()
        entry['source_records'] = [{'path': '../outside.md', 'locator': 'test'}]
        self.write('01_systems/s10000_example/system.json', entry)
        self.assertTrue(catalog.discover(self.root)[1])
        self.assertFalse(catalog.inside(self.root, 'C:/outside.md'))
        self.assertFalse(catalog.inside(self.root, '/outside.md'))

    def test_derived_view_drift_is_detected(self):
        self.add()
        catalog.refresh(self.root)
        (self.root / '01_systems/TYPE_INDEX.md').write_text('stale', encoding='utf-8')
        self.assertTrue(catalog.check(self.root))

    def test_new_type_requires_only_taxonomy_definition(self):
        taxonomy = catalog.read(self.root / '00_governance/module_types.json')
        taxonomy['types']['experimental_program'] = {'label': '实验计划', 'definition': 'Test', 'boundary': 'Test'}
        self.write('00_governance/module_types.json', taxonomy)
        self.add(kind='experimental_program')
        self.assertEqual(catalog.refresh(self.root), [])
        self.assertEqual(catalog.check(self.root), [])

if __name__ == '__main__':
    unittest.main()
