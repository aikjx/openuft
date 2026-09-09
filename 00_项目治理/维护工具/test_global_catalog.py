"""独立临时目录中检查全球研究登记与生成视图的契约。"""
import json
from pathlib import Path
import tempfile
import unittest
import global_catalog as catalog

class GlobalCatalogContract(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='openuft_global_')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.base = self.root / '05_全球研究'
        self.base.mkdir()
        self.data = json.loads((catalog.ROOT / '05_全球研究/全球研究登记.json').read_text(encoding='utf-8'))
        governance = self.root / '00_项目治理'
        governance.mkdir()
        (governance / '国际化配置.json').write_text((catalog.ROOT / '00_项目治理/国际化配置.json').read_text(encoding='utf-8'),encoding='utf-8')
        self.save()

    def save(self):
        (self.base / '全球研究登记.json').write_text(json.dumps(self.data,ensure_ascii=False),encoding='utf-8')

    def test_drift_is_detected(self):
        catalog.refresh(self.root)
        self.assertEqual(catalog.check(self.root), [])
        path = self.base / '02_全球路线' / self.data['路线'][0]['目录'] / 'README.md'
        path.write_text('过时内容',encoding='utf-8')
        self.assertTrue(catalog.check(self.root))

    def test_duplicate_route_is_rejected_before_writing(self):
        self.data['路线'].append(dict(self.data['路线'][0]))
        self.save()
        with self.assertRaises(ValueError): catalog.refresh(self.root)
        self.assertFalse((self.base / '02_全球路线').exists())

    def test_path_escape_is_rejected(self):
        self.data['路线'][0]['目录'] = '../越界'
        self.save()
        self.assertTrue(catalog.check(self.root))

    def test_changed_source_requires_regeneration(self):
        catalog.refresh(self.root)
        self.data['路线'][0]['核实范围'] = '新的范围说明'
        self.save()
        self.assertTrue(catalog.check(self.root))
        catalog.refresh(self.root)
        self.assertEqual(catalog.check(self.root), [])

if __name__ == '__main__': unittest.main()
