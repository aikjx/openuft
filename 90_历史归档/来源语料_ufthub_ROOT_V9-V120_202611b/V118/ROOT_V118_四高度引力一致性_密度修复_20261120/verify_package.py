"""Verify archived file hashes; run before modifying/re-generating any outputs."""
import hashlib,json,sys
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text(encoding='utf-8'))
fail=[]
for item in manifest['files']:
    p=root/item['path']
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:
        fail.append(item['path'])
print(f"ROOT V118 hashes: {len(manifest['files'])-len(fail)}/{len(manifest['files'])}")
if fail: print('HASH MISMATCH: ',fail)
sys.exit(1 if fail else 0)
