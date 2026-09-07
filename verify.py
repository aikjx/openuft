# -*- coding: utf-8 -*-
"""Validate research layout, local Markdown links and migration preservation."""
from pathlib import Path
from urllib.parse import unquote
import hashlib
import json
import re
import sys
import zipfile
sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent

def main():
    errors = []
    import importlib.util
    spec = importlib.util.spec_from_file_location('module_catalog', ROOT / '00_governance/tools/module_catalog.py')
    catalog = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(catalog)
    catalog_errors = catalog.check(ROOT)
    if catalog_errors:
        for error in catalog_errors: print(error)
        print('FAIL: identity/type validation; fix before structural checks')
        return True
    layout = json.loads((ROOT / '00_governance/layout.json').read_text(encoding='utf-8'))
    for section in layout['sections']:
        if not (ROOT / section / 'README.md').is_file(): errors.append('Missing section: ' + section)
    systems = layout['systems']
    identities = []
    for model in systems + ['_template']:
        base = ROOT / '01_systems' / model
        for stage in layout['stages']:
            if not (base / stage / 'README.md').is_file(): errors.append('Missing stage: ' + model + '/' + stage)
        for name in ['system.json', 'claims.csv', '08_data/data_registry.csv', '07_computation/runs/run_template.json']:
            if not (base / name).is_file(): errors.append('Missing record: ' + model + '/' + name)
        if (base / 'system.json').exists():
            identity = json.loads((base / 'system.json').read_text(encoding='utf-8'))
            identities.append(identity)
            if identity['id'] != model: errors.append('Wrong system id: ' + model)
            for source in identity['source_records']:
                if not (ROOT / source['path']).is_file(): errors.append('Missing provenance: ' + source['path'])
            for dependency in identity['related_systems']:
                if dependency not in systems: errors.append('Unknown related system: ' + dependency)
            for dependency in identity['code_dependencies']:
                if not (ROOT / dependency).is_dir(): errors.append('Missing code dependency: ' + dependency)
    if len(set(systems)) != len(systems): errors.append('Duplicate system ids')
    if (ROOT / '01_models').exists(): errors.append('Obsolete six-route root still active')
    registry = json.loads((ROOT / '00_governance/system_registry.json').read_text(encoding='utf-8'))['systems']
    if registry != [entry for entry in identities if entry['id'] != '_template']:
        errors.append('System registry differs from individual identities')
    checked = 0
    for p in ROOT.rglob('*.md'):
        if '90_archive' in p.relative_to(ROOT).parts: continue
        body = re.sub(r'```.*?```', '', p.read_text(encoding='utf-8-sig'), flags=re.S)
        for target in re.findall(r'!?\[[^\]\n]*\]\(([^\s)]+)\)', body):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'): continue
            dest = p.parent / unquote(target.split('#', 1)[0].strip('<>'))
            checked += 1
            if not dest.exists(): errors.append('Broken link: ' + p.relative_to(ROOT).as_posix() + ' -> ' + target)
    migrations = [ROOT / '90_archive/migrations' / name for name in ['20260907_full_layout', '20260907_independent_systems']]
    manifests = [json.loads((p / 'manifest.json').read_text(encoding='utf-8')) for p in migrations]
    latest_moves = {row['old']: row['new'] for row in manifests[-1]['files']}
    for index, (migration, manifest) in enumerate(zip(migrations, manifests)):
        with zipfile.ZipFile(migration / 'before.zip') as snapshot:
            for row in manifest['files']:
                if hashlib.sha256(snapshot.read(row['old'])).hexdigest() != row['sha256_before']: errors.append('Snapshot mismatch: ' + row['old'])
                target = latest_moves.get(row['new'], row['new']) if index == 0 else row['new']
                if not (ROOT / target).is_file(): errors.append('Lost migrated file: ' + target)
    for record in json.loads((ROOT / '00_governance/chapter_provenance.json').read_text(encoding='utf-8')):
        source = ROOT / record['source']
        if hashlib.sha256(source.read_bytes()).hexdigest() != record['source_sha256']: errors.append('Changed chapter source: ' + record['source'])
        excerpt = ''.join(source.read_text(encoding='utf-8').splitlines(keepends=True)[record['start_line']-1:record['end_line']])
        if excerpt.rstrip() + '\n' != (ROOT / record['derived_path']).read_text(encoding='utf-8'): errors.append('Chapter excerpt mismatch: ' + record['derived_path'])
    print('Systems/directions: {}; lifecycle stages: {}; local links: {}; snapshot originals: {}'.format(len(systems), len(layout['stages']), checked, [len(m['files']) for m in manifests]))
    for error in errors: print(error)
    print('PASS' if not errors else 'FAIL: {} issues'.format(len(errors)))
    return bool(errors)

if __name__ == '__main__':
    sys.exit(main())
