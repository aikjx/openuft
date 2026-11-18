"""Verify immutable code and documentation; numerical outputs can legitimately change on rerun."""
from pathlib import Path
import json,hashlib,sys
root=Path(__file__).resolve().parent
manifest=json.loads((root/'SOURCE_SHA256_MANIFEST.json').read_text(encoding='utf-8'))
failed=[]
for e in manifest['files']:
    p=root/e['path']
    if not p.is_file(): failed.append({'file':e['path'],'error':'missing'})
    elif hashlib.sha256(p.read_bytes()).hexdigest()!=e['sha256']:failed.append({'file':e['path'],'error':'sha256 changed'})
print(json.dumps({'checked':len(manifest['files']),'status':'PASS' if not failed else 'FAIL','failed':failed},ensure_ascii=False,indent=2))
sys.exit(1 if failed else 0)
