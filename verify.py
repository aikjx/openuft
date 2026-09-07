# -*- coding: utf-8 -*-
"""Validate research layout, local Markdown links and migration preservation."""
from pathlib import Path
from urllib.parse import unquote
import hashlib
import json
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parent

def main():
    errors = []
    layout = json.loads((ROOT / '00_governance/layout.json').read_text(encoding='utf-8'))
    for section in layout['sections']:
        if not (ROOT / section / 'README.md').is_file(): errors.append('Missing section: ' + section)
    for model in layout['models'] + ['_template']:
        base = ROOT / '01_models' / model
        for stage in layout['stages']:
            if not (base / stage / 'README.md').is_file(): errors.append('Missing stage: ' + model + '/' + stage)
        for name in ['model.json', 'claims.csv', '08_data/data_registry.csv', '07_computation/runs/run_template.json']:
            if not (base / name).is_file(): errors.append('Missing record: ' + model + '/' + name)
        if (base / 'model.json').exists():
            if json.loads((base / 'model.json').read_text(encoding='utf-8'))['id'] != model: errors.append('Wrong model id: ' + model)
    checked = 0
    for p in ROOT.rglob('*.md'):
        if '90_archive' in p.relative_to(ROOT).parts: continue
        body = re.sub(r'```.*?```', '', p.read_text(encoding='utf-8-sig'), flags=re.S)
        for target in re.findall(r'!?\[[^\]\n]*\]\(([^\s)]+)\)', body):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'): continue
            dest = p.parent / unquote(target.split('#', 1)[0].strip('<>'))
            checked += 1
            if not dest.exists(): errors.append('Broken link: ' + p.relative_to(ROOT).as_posix() + ' -> ' + target)
    migration = ROOT / '90_archive/migrations/20260907_full_layout'
    manifest = json.loads((migration / 'manifest.json').read_text(encoding='utf-8'))
    with zipfile.ZipFile(migration / 'before.zip') as snapshot:
        for row in manifest['files']:
            if hashlib.sha256(snapshot.read(row['old'])).hexdigest() != row['sha256_before']: errors.append('Snapshot mismatch: ' + row['old'])
            if not (ROOT / row['new']).is_file(): errors.append('Lost migrated file: ' + row['new'])
    print('Models: {}; lifecycle stages per model: {}; local links checked: {}; preserved originals: {}'.format(len(layout['models']), len(layout['stages']), checked, len(manifest['files'])))
    for error in errors: print(error)
    print('PASS' if not errors else 'FAIL: {} issues'.format(len(errors)))
    return bool(errors)

if __name__ == '__main__':
    sys.exit(main())
