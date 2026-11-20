from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parent
manifest=ROOT/'CHECKSUMS.sha256'
if not manifest.exists():raise SystemExit('checksum manifest absent')
checks=manifest.read_text(encoding='utf-8').splitlines()
for line in checks:
 sha,rel=line.split('  ',1)
 p=ROOT/rel
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=sha:
  raise SystemExit('HASH MISMATCH: '+rel)
print(f'PASS SHA256: {len(checks)} files')
