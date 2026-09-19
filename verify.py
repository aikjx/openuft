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

RAW_STAGING_SECTION = '99_待整理资料'
RAW_BATCH_PREFIX = '根目录来料_'


def is_raw_staging(parts) -> bool:
    """根目录来料_* 批次是外部资料的原样转存（目录命名与链接结构均来自上游，
    如 assets/fonts/.github/arxiv 等）。完成整理并入正式目录前，不纳入
    中文目录命名与本地链接治理，避免为迎合规则而破坏来源镜像的完整性。"""
    return bool(parts) and parts[0] == RAW_STAGING_SECTION and any(
        part.startswith(RAW_BATCH_PREFIX) for part in parts)


def main():
    errors = []
    import importlib.util
    spec = importlib.util.spec_from_file_location('module_catalog', ROOT / '00_项目治理/维护工具/module_catalog.py')
    catalog = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(catalog)
    catalog_errors = catalog.check(ROOT)
    if catalog_errors:
        for error in catalog_errors: print(error)
        print('FAIL: identity/type validation; fix before structural checks')
        return True
    layout = json.loads((ROOT / '00_项目治理/layout.json').read_text(encoding='utf-8'))
    for section in layout['sections']:
        if not (ROOT / section / 'README.md').is_file(): errors.append('Missing section: ' + section)
    systems = layout['systems']
    dir_map = layout.get('system_directories', {})
    identities = []
    for model in systems + ['_template']:
        base = ROOT / '01_独立体系' / ('新体系模板' if model == '_template' else dir_map.get(model, model))
        for stage in layout['stages']:
            if not (base / stage / 'README.md').is_file(): errors.append('Missing stage: ' + model + '/' + stage)
        for name in ['system.json', 'claims.csv', '08_研究数据/data_registry.csv', '07_计算复现/运行记录/run_template.json']:
            if not (base / name).is_file(): errors.append('Missing record: ' + model + '/' + name)
        if (base / 'system.json').exists():
            identity = json.loads((base / 'system.json').read_text(encoding='utf-8'))
            identities.append(identity)
            if identity['id'] != model: errors.append('Wrong system id: ' + model)
            expected_dir = ('新体系模板' if model == '_template' else dir_map.get(model, model))
            if identity.get('directory', expected_dir) != expected_dir:
                errors.append('Wrong directory mapping: ' + model)
            for source in identity['source_records']:
                if not (ROOT / source['path']).is_file(): errors.append('Missing provenance: ' + source['path'])
            for dependency in identity['related_systems']:
                if dependency not in systems: errors.append('Unknown related system: ' + dependency)
            for dependency in identity['code_dependencies']:
                if not (ROOT / dependency).is_dir(): errors.append('Missing code dependency: ' + dependency)
    if len(set(systems)) != len(systems): errors.append('Duplicate system ids')
    if (ROOT / '01_models').exists(): errors.append('Obsolete six-route root still active')
    registry = json.loads((ROOT / '00_项目治理/system_registry.json').read_text(encoding='utf-8'))['systems']
    if registry != [entry for entry in identities if entry['id'] != '_template']:
        errors.append('System registry differs from individual identities')
    global_spec = importlib.util.spec_from_file_location('global_catalog', ROOT / '00_项目治理/维护工具/global_catalog.py')
    global_catalog = importlib.util.module_from_spec(global_spec)
    global_spec.loader.exec_module(global_catalog)
    errors.extend(global_catalog.check(ROOT))
    for directory in ROOT.rglob('*'):
        if not directory.is_dir(): continue
        parts = directory.relative_to(ROOT).parts
        if parts[0].startswith('.') or '__pycache__' in parts: continue
        if is_raw_staging(parts): continue
        if not re.search(r'[一-鿿]', directory.name):
            errors.append('Research directory must use Chinese: ' + directory.relative_to(ROOT).as_posix())
    checked = 0
    for p in ROOT.rglob('*.md'):
        if '90_历史归档' in p.relative_to(ROOT).parts: continue
        if is_raw_staging(p.relative_to(ROOT).parts): continue
        body = re.sub(r'```.*?```', '', p.read_text(encoding='utf-8-sig'), flags=re.S)
        for target in re.findall(r'!?\[[^\]\n]*\]\(([^\s)]+)\)', body):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'): continue
            dest = p.parent / unquote(target.split('#', 1)[0].strip('<>'))
            checked += 1
            if not dest.exists(): errors.append('Broken link: ' + p.relative_to(ROOT).as_posix() + ' -> ' + target)
    migration_spec = importlib.util.spec_from_file_location('migration_check', ROOT / '00_项目治理/维护工具/migration_check.py')
    migration_check = importlib.util.module_from_spec(migration_spec)
    migration_spec.loader.exec_module(migration_check)
    migration_errors, snapshot_counts = migration_check.check(ROOT)
    errors.extend(migration_errors)
    for record in json.loads((ROOT / '00_项目治理/chapter_provenance.json').read_text(encoding='utf-8')):
        source = ROOT / record['source']
        if hashlib.sha256(source.read_bytes()).hexdigest() != record['source_sha256']: errors.append('Changed chapter source: ' + record['source'])
        excerpt = ''.join(source.read_text(encoding='utf-8').splitlines(keepends=True)[record['start_line']-1:record['end_line']])
        if excerpt.rstrip() + '\n' != (ROOT / record['derived_path']).read_text(encoding='utf-8'): errors.append('Chapter excerpt mismatch: ' + record['derived_path'])
    print('Systems/directions: {}; lifecycle stages: {}; local links: {}; snapshot originals: {}'.format(len(systems), len(layout['stages']), checked, snapshot_counts))
    for error in errors: print(error)
    print('PASS' if not errors else 'FAIL: {} issues'.format(len(errors)))
    return bool(errors)

if __name__ == '__main__':
    sys.exit(main())
