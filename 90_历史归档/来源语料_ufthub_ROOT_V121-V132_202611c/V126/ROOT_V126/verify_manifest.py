"""Verify ROOT V126 SHA256 file manifest, excluding self and the manifest."""
from pathlib import Path
from hashlib import sha256
ROOT=Path(__file__).resolve().parent
manifest=ROOT/'MANIFEST.sha256'
expected={}
for raw in manifest.read_text(encoding='utf-8').splitlines():
    if not raw:continue
    hashval,rel=raw.split('  ',1)
    assert rel not in expected, f'duplicate manifest path: {rel}'
    p=(ROOT/rel).resolve()
    assert p.is_relative_to(ROOT) and p.is_file(),f'missing/unsafe entry: {rel}'
    assert p.is_symlink() is False,f'symlink disallowed: {rel}'
    actual=sha256(p.read_bytes()).hexdigest()
    assert actual==hashval,f'sha256 mismatch for {rel}'
    expected[rel]=actual
actual_files={str(p.relative_to(ROOT).as_posix()) for p in ROOT.rglob('*') if p.is_file() and not any(part in ('__pycache__','.pytest_cache') for part in p.parts)}
actual_files-={'MANIFEST.sha256','verify_manifest.py'}
assert actual_files==set(expected), f'manifest file-set mismatch: missing {actual_files-set(expected)}, extras {set(expected)-actual_files}'
print(f'V126_MANIFEST_OK {len(expected)} files')
