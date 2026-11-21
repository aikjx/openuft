from pathlib import Path
import hashlib,sys
root=Path(__file__).resolve().parent
items=(root/'MANIFEST.sha256').read_text(encoding='utf-8').splitlines()
failed=[]
for line in items:
    if not line.strip(): continue
    digest,rel=line.split('  ',1)
    p=root/rel
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest: failed.append(rel)
print(f'manifest verified {len(items)-len(failed)}/{len(items)}')
if failed: print('FAILED:',failed);sys.exit(1)
