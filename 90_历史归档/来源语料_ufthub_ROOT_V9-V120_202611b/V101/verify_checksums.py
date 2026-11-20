from pathlib import Path
import hashlib,sys
R=Path(__file__).resolve().parent
items=[line.strip().split('  ',1) for line in (R/'CHECKSUMS.sha256').read_text().splitlines() if line.strip()]
failed=[]
for digest,rel in items:
 p=R/rel
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:
  failed.append(rel)
print(f'CHECKSUMS {len(items)-len(failed)}/{len(items)} PASS')
if failed:
 print('FAILED:',failed)
 sys.exit(1)
