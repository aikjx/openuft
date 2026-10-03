"""检查中文目录迁移及历史快照；不认证科学结论。"""
from pathlib import Path
import hashlib
import io
import json
import zipfile


def check(root):
    errors = []
    # 2026-09-23 之后的「毕业迁移与改名登记」：旧位置被有意移除（moved→新位置 / deleted→删除），
    # 由对应 git commit 登记（如 c348058）。migration_check 据此把已毕业/已删除的旧路径视为合法演进，
    # 而不是「丢失」。这与 20260909 历史快照的防篡改校验共存：不改原快照，只补登记当前真实位置。
    grad_map = {}
    grad_deleted = set()
    grad_path = root / '90_历史归档/迁移记录/20261003_毕业迁移与改名/毕业迁移清单.json'
    if grad_path.exists():
        for row in json.loads(grad_path.read_text(encoding='utf-8'))['files']:
            if row.get('kind') == 'moved':
                grad_map[row['old']] = row['new']
            elif row.get('kind') == 'deleted':
                grad_deleted.add(row['old'])

    correction = root / '90_历史归档/迁移记录/20260909_术语与语言'
    corrections = json.loads((correction / '变更清单.json').read_text(encoding='utf-8'))['files'] if (correction / '变更清单.json').exists() else []
    aliases = {row['old']: row['new'] for row in corrections}

    def current(path):
        # 解析优先级：毕业迁移映射 → 术语改名映射 → 原路径。
        return root / grad_map.get(path, aliases.get(path, path))

    if corrections:
        with zipfile.ZipFile(correction / '变更前原件.zip') as snapshot:
            for row in corrections:
                if hashlib.sha256(snapshot.read(row['old'])).hexdigest() != row['sha256_before']:
                    errors.append('Terminology snapshot mismatch: ' + row['old'])
                if row['new'] in grad_deleted:
                    continue  # 有意删除，非丢失
                if not current(row['new']).is_file():
                    errors.append('Lost renamed file: ' + row['new'])
    base = root / '90_历史归档/迁移记录/20260909_中文目录与署名'
    manifest = json.loads((base / '迁移清单.json').read_text(encoding='utf-8'))
    mapping = {row['old']: row['new'] for row in manifest['files']}
    counts = []
    with zipfile.ZipFile(base / '原始快照.zip') as original:
        for row in manifest['files']:
            if hashlib.sha256(original.read(row['old'])).hexdigest() != row['sha256_before']:
                errors.append('Localization snapshot mismatch: ' + row['new'])
            if row['new'] in grad_deleted:
                continue  # 有意删除，非丢失
            target = current(row['new']).resolve()
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
            if current(mapping[path + '/before.zip']).read_bytes() != original_zip:
                errors.append('Historic ZIP changed: ' + path)
            with zipfile.ZipFile(io.BytesIO(original_zip)) as snapshot:
                for row in record['files']:
                    if hashlib.sha256(snapshot.read(row['old'])).hexdigest() != row['sha256_before']:
                        errors.append('Historic snapshot mismatch: ' + row['old'])
                    old_target = latest.get(row['new'], row['new']) if index == 0 else row['new']
                    if old_target in grad_deleted:
                        continue  # 有意删除，非丢失
                    if old_target not in mapping or not current(mapping[old_target]).is_file():
                        errors.append('Lost historical target: ' + old_target)
    return errors, counts
