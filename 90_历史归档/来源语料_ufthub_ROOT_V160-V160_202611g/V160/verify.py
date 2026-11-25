from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
manifest=json.loads((root/'SHA256.json').read_text())
for name,digest in manifest.items():
    assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,name
print(f'{len(manifest)} static files verified')
