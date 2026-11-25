from pathlib import Path
import hashlib
p=Path(__file__).resolve().parent
for line in (p/'SHA256SUMS').read_text().splitlines():
    digest,name=line.split('  ',1)
    assert hashlib.sha256((p/name).read_bytes()).hexdigest()==digest,name
print('Static SHA-256 checks passed')
