#!/usr/bin/env python3
"""Verify frozen static source/docs/history hashes, not regenerated outputs."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
failed=[]
for item in manifest['files']:
    target=root/item['path']
    if not target.is_file():failed.append(f"missing {item['path']}");continue
    digest=hashlib.sha256(target.read_bytes()).hexdigest()
    if digest!=item['sha256']:failed.append(f"SHA mismatch {item['path']}")
if failed:
    raise SystemExit('MANIFEST FAILED: '+', '.join(failed))
print(f"MANIFEST PASS: {len(manifest['files'])} static source/docs/history files")
