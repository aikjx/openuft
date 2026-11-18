"""Recompute stable artifact SHA-256, after extraction or reruns."""
from pathlib import Path
import json,hashlib,sys
P=Path(__file__).resolve().parent
man=json.loads((P/'SOURCE_SHA256_MANIFEST.json').read_text(encoding='utf-8'))
fail=[]
for name,meta in man['files'].items():
    q=P/name
    if not q.exists() or q.stat().st_size!=meta['bytes'] or hashlib.sha256(q.read_bytes()).hexdigest()!=meta['sha256']:
        fail.append(name)
print(json.dumps({'project':'ROOT V69','files_checked':len(man['files']),'failures':fail,'status':'PASS' if not fail else 'FAIL'},ensure_ascii=False,indent=2))
sys.exit(1 if fail else 0)
