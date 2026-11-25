import hashlib,json
from pathlib import Path
p=Path(__file__).resolve().parent
m=json.loads((p/'SHA256.json').read_text())
for name,h in m.items():
    assert hashlib.sha256((p/name).read_bytes()).hexdigest()==h,name
print(f'{len(m)} static files verified')
