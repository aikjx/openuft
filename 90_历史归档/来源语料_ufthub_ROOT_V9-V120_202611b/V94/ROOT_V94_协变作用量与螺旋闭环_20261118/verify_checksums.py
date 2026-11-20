from pathlib import Path
import hashlib
root=Path(__file__).resolve().parent
lst=root/'CHECKSUMS.sha256'
if not lst.exists():raise FileNotFoundError('CHECKSUMS.sha256 is not present, use the official distributed ZIP')
checks=[line.strip().split('  ',1) for line in lst.read_text().splitlines() if line.strip()]
failed=[]
for expected,rel in checks:
    path=root/rel
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:failed.append(rel)
if failed:raise ValueError(f'Hash mismatch (possible post-install generated changes): {failed}')
print('SHA-256 verified:',len(checks),'files')
