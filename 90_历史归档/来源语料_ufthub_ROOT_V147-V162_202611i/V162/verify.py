from pathlib import Path
import hashlib
p=Path(__file__).resolve().parent
for line in (p/'SHA256SUMS').read_text().splitlines():
    expected,name=line.split('  ',1)
    assert hashlib.sha256((p/name).read_bytes()).hexdigest()==expected,name
print('All static SHA256 checks passed')
