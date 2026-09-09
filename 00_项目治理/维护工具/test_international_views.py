"""默认中文、可选语言与未知语言回退的实际行为。"""
import copy
import json
from pathlib import Path
import unittest
import international_views

class LocaleContract(unittest.TestCase):
    def setUp(self):
        self.config = json.loads((Path(__file__).resolve().parents[1] / '国际化配置.json').read_text(encoding='utf-8'))

    def test_default_is_chinese(self):
        self.assertEqual(international_views.entry_for(self.config), 'README.md')

    def test_english_is_explicit_and_optional(self):
        self.assertEqual(international_views.entry_for(self.config, 'en'), '05_全球研究/03_多语种协作/英语/项目介绍.md')

    def test_japanese_has_real_entry(self):
        entry = international_views.entry_for(self.config, 'ja')
        self.assertEqual(entry, '05_全球研究/03_多语种协作/日语/项目介绍.md')
        self.assertTrue((Path(__file__).resolve().parents[2] / entry).is_file())

    def test_unknown_locale_falls_back_to_chinese(self):
        self.assertEqual(international_views.entry_for(self.config, 'unknown-language'), 'README.md')

    def test_non_chinese_default_is_rejected(self):
        self.config['默认语言'] = 'en'
        with self.assertRaises(ValueError): international_views.entry_for(self.config)

    def test_path_escape_is_rejected(self):
        self.config['语言版本'][1]['入口'] = '../outside.md'
        with self.assertRaises(ValueError): international_views.entry_for(self.config, 'en')

if __name__ == '__main__': unittest.main()
