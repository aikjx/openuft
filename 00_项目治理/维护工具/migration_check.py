"""检查中文目录迁移及历史快照；不认证科学结论。"""
from pathlib import Path
import hashlib
import io
import json
import zipfile


def check(root):
    errors = []
    base = root / '90_历史归档/迁移记录/20260909_中文目录与署名'
    manifest = json.loads((base / '迁移清单.json').read_text(encoding='utf-8'))
    mapping = {row['old']: row['new'] for row in manifest['files']}
    counts = []
    with zipfile.ZipFile(base / '原始快照.zip') as original:
        for row in manifest['files']:
            if hashlib.sha256(original.read(row['old'])).hexdigest() != row['sha256_before']:
                errors.append('Localization snapshot mismatch: ' + row['new'])
            target = (root / row['new']).resolve()
            try:
                target.relative_to(root.resolve())
            except ValueError:
                errors.append('Migration path escapes root: ' + row['new'])
                continue
            if not target.is_file():
                errors.append('Lost localized file: ' + row['new'])
        # Original manifests live in the pre-localization snapshot, with their original ZIP names.
        paths = ['90_archive/migrations/' + name for name in ['20260907_full_layout', '20260907_independent_systems']]
        historic = [json.loads(original.read(path + '/manifest.json')) for path in paths]
        latest = {row['old']: row['new'] for row in historic[-1]['files']}
        for index, (path, record) in enumerate(zip(paths, historic)):
            counts.append(len(record['files']))
            original_zip = original.read(path + '/before.zip')
            if (root / mapping[path + '/before.zip']).read_bytes() != original_zip:
                errors.append('Historic ZIP changed: ' + path)
            with zipfile.ZipFile(io.BytesIO(original_zip)) as snapshot:
                for row in record['files']:
                    if hashlib.sha256(snapshot.read(row['old'])).hexdigest() != row['sha256_before']:
                        errors.append('Historic snapshot mismatch: ' + row['old'])
                    old_target = latest.get(row['new'], row['new']) if index == 0 else row['new']
                    if old_target not in mapping or not (root / mapping[old_target]).is_file():
                        errors.append('Lost historical target: ' + old_target)
    return errors, counts
