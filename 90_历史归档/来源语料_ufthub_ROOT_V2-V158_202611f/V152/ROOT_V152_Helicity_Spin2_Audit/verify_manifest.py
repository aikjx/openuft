"""Verify SHA256 for static reproducible inputs. Auto-generated outputs are excluded."""
from pathlib import Path
import json,hashlib,sys
root=Path(__file__).resolve().parent
manifest_path=root/'manifest.json'
if not manifest_path.exists():
 print('Missing manifest.json');sys.exit(1)
manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
bad=[]
for item in manifest['files']:
    file=root/item['path']
    if not file.exists() or hashlib.sha256(file.read_bytes()).hexdigest()!=item['sha256']:
        bad.append(item['path'])
if bad:
 print('FAILED SHA256:',bad);sys.exit(1)
print(f'PASS SHA256: {len(manifest["files"])} static files.')
