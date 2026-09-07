# -*- coding: utf-8 -*-
"""Refresh current file navigation; does not assign scientific ownership."""
from pathlib import Path
import json
import os

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / '00_governance/catalog'

def main():
    files = sorted(p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    entries = [{'path': p.relative_to(ROOT).as_posix(), 'section': p.relative_to(ROOT).parts[0]} for p in files]
    (CATALOG / 'structure_manifest.json').write_text(json.dumps({'purpose': 'Current paths only; not scientific evidence or ownership certification', 'files': entries}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    body = '# 全量文件索引\n\n按实际存放位置生成。归属待审的历史资料不因被索引而获得证据认可。\n\n'
    section = None
    for p in files:
        current = p.relative_to(ROOT).parts[0]
        if current != section:
            body += '\n## ' + current + '\n\n'
            section = current
        target = os.path.relpath(p, CATALOG).replace('\\', '/')
        body += '- [' + p.relative_to(ROOT).as_posix() + '](' + target + ')\n'
    (CATALOG / 'material_catalog.md').write_text(body, encoding='utf-8')
    print('Indexed {} files'.format(len(files)))

if __name__ == '__main__':
    main()
