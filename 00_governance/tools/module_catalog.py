# -*- coding: utf-8 -*-
"""Discover independent modules, validate identity boundaries, refresh derived views."""
import argparse
import json
from pathlib import Path, PurePosixPath
import re

ROOT = Path(__file__).resolve().parents[2]

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def inside(root, value):
    """Require an existing portable root-relative reference, not a shell/drive path."""
    if not isinstance(value, str) or not value or '\\' in value or ':' in value:
        return False
    path = PurePosixPath(value)
    if path.is_absolute() or '..' in path.parts:
        return False
    try:
        (root / value).resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True

def discover(root):
    errors = []
    taxonomy = read(root / '00_governance/module_types.json')
    types = taxonomy['types']
    layout = read(root / '00_governance/layout.json')
    entries = []
    for base in sorted((root / '01_systems').iterdir()):
        if not base.is_dir() or base.name == '_template':
            continue
        identity = base / 'system.json'
        if not identity.is_file():
            errors.append('Unregistered directory: ' + base.name)
            continue
        try:
            entry = read(identity)
        except (ValueError, OSError) as exc:
            errors.append('Invalid identity {}: {}'.format(base.name, exc))
            continue
        if not isinstance(entry, dict):
            errors.append('Identity must be an object: ' + base.name)
            continue
        sid = entry.get('id')
        if sid != base.name or not re.fullmatch(r'[a-z][a-z0-9]*(?:_[a-z0-9]+)*', str(sid)):
            errors.append('Invalid stable id: ' + base.name)
        for key in ['title', 'premise_summary', 'premise_status']:
            if not isinstance(entry.get(key), str) or not entry[key].strip():
                errors.append('Missing text {}: {}'.format(key, base.name))
        if not isinstance(entry.get('kind'), str) or entry.get('kind') not in types:
            errors.append('Unknown module type: ' + base.name)
        if entry.get('status') not in taxonomy['statuses']:
            errors.append('Unknown lifecycle status: ' + base.name)
        for key in ['source_records', 'related_systems', 'code_dependencies', 'postulates']:
            if not isinstance(entry.get(key), list):
                errors.append('Expected list {}: {}'.format(key, base.name))
        sources = entry.get('source_records', [])
        if isinstance(sources, list):
            for source in sources:
                if not isinstance(source, dict) or not inside(root, source.get('path')):
                    errors.append('Invalid source reference: ' + base.name)
                elif not (root / source['path']).is_file() or not isinstance(source.get('locator'), str) or not source['locator'].strip():
                    errors.append('Missing source or locator: ' + base.name)
        dependencies = entry.get('code_dependencies', [])
        if isinstance(dependencies, list):
            for dep in dependencies:
                if not inside(root, dep) or not (root / dep).exists():
                    errors.append('Invalid code reference: ' + base.name)
        for stage in layout['stages']:
            if not (base / stage / 'README.md').is_file():
                errors.append('Missing lifecycle stage: ' + base.name + '/' + stage)
        for relative in ['claims.csv', '08_data/data_registry.csv', '07_computation/runs/run_template.json']:
            if not (base / relative).is_file():
                errors.append('Missing module record: ' + base.name + '/' + relative)
        run_template = base / '07_computation/runs/run_template.json'
        if run_template.is_file():
            try:
                run = read(run_template)
                if not isinstance(run, dict) or run.get('system_id') != sid:
                    errors.append('Run template belongs to another system: ' + base.name)
            except (ValueError, OSError):
                errors.append('Invalid run template: ' + base.name)
        entries.append(entry)
    ids = {str(entry.get('id')) for entry in entries}
    if len(ids) != len(entries):
        errors.append('Duplicate stable ids')
    for entry in entries:
        relations = entry.get('related_systems', [])
        if isinstance(relations, list):
            for dep in relations:
                if not isinstance(dep, str) or dep not in ids or dep == entry.get('id'):
                    errors.append('Invalid related system: ' + str(entry.get('id')))
    return entries, errors

def render_types(entries, taxonomy):
    body = '# 按模块类型浏览\n\n本文件由各体系 system.json 生成；主文件始终保留在独立体系目录。类型改变无需移动路径，ID 前缀不决定类型。\n\n[扩展与最优性分析](../00_governance/SCALABILITY_REVIEW.md) · [独立体系总入口](README.md)。\n\n'
    body += '| 类型 | 数量 | 职责 |\n|---|---:|---|\n'
    for kind, spec in taxonomy['types'].items():
        body += '| {} | {} | {} |\n'.format(spec['label'], sum(e['kind'] == kind for e in entries), spec['definition'])
    for kind, spec in taxonomy['types'].items():
        body += '\n## ' + spec['label'] + '\n\n' + spec['boundary'] + '\n\n'
        members = [e for e in entries if e['kind'] == kind]
        if not members:
            body += '当前没有此类型的活动登记。\n'
        for entry in members:
            body += '- [{}]({}/README.md) · `{}` · {}\n'.format(entry['title'], entry['id'], entry['status'], entry['premise_summary'])
    body += '\n类型描述研究对象，status 描述工作状态，证据类型记录在 claims.csv；三者不能相互替代。\n'
    return body

def check(root):
    entries, errors = discover(root)
    if errors:
        return errors
    layout = read(root / '00_governance/layout.json')
    if layout['systems'] != [e['id'] for e in entries]:
        errors.append('Stale layout systems; run module_catalog.py refresh')
    registry = root / '00_governance/system_registry.json'
    if not registry.is_file() or read(registry) != {'systems': entries}:
        errors.append('Stale system registry; run module_catalog.py refresh')
    index = root / '01_systems/TYPE_INDEX.md'
    expected = render_types(entries, read(root / '00_governance/module_types.json'))
    if not index.is_file() or index.read_text(encoding='utf-8') != expected:
        errors.append('Stale type index; run module_catalog.py refresh')
    overview = root / '01_systems/README.md'
    if not overview.is_file() or overview.read_text(encoding='utf-8') != render_overview(entries, read(root / '00_governance/module_types.json')):
        errors.append('Stale module overview; run module_catalog.py refresh')
    return errors

def render_overview(entries, taxonomy):
    text = '# 独立体系总入口\n\n[按模块类型浏览](TYPE_INDEX.md) · [可持续扩展与最优性分析](../00_governance/SCALABILITY_REVIEW.md) · [原始拆分依据](../00_governance/INDEPENDENT_SYSTEMS_DESIGN.md) · [新体系模板](_template/README.md)。\n\n'
    text += '当前登记 {} 个独立模块。数量不代表已建立理论数量；类型、工作状态和证据分别管理。本表自动生成，不手工维护第二份身份。\n\n'.format(len(entries))
    for kind, spec in taxonomy['types'].items():
        members = [e for e in entries if e['kind'] == kind]
        text += '## {}（{}）\n\n{}\n\n'.format(spec['label'], len(members), spec['boundary'])
        if members:
            text += '| 独立体系 | 状态 | 基础前提 |\n|---|---|---|\n'
            for e in members:
                text += '| [{}]({}/README.md) | {} | {} |\n'.format(e['title'], e['id'], e['status'], e['premise_summary'])
        else:
            text += '尚无登记。\n'
        text += '\n'
    return text

def refresh(root):
    entries, errors = discover(root)
    if errors:
        return errors  # Never generate a partial catalog from invalid identities.
    layout = read(root / '00_governance/layout.json')
    layout['systems'] = [e['id'] for e in entries]
    outputs = {
        root / '00_governance/layout.json': json.dumps(layout, ensure_ascii=False, indent=2) + '\n',
        root / '00_governance/system_registry.json': json.dumps({'systems': entries}, ensure_ascii=False, indent=2) + '\n',
        root / '01_systems/TYPE_INDEX.md': render_types(entries, read(root / '00_governance/module_types.json')),
        root / '01_systems/README.md': render_overview(entries, read(root / '00_governance/module_types.json')),
    }
    for path, body in outputs.items():
        path.write_text(body, encoding='utf-8')
    return []

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['check', 'refresh'])
    args = parser.parse_args()
    errors = refresh(ROOT) if args.command == 'refresh' else check(ROOT)
    for error in errors:
        print(error)
    print('FAIL' if errors else 'PASS: module types, stable ids and generated views')
    return bool(errors)

if __name__ == '__main__':
    raise SystemExit(main())
