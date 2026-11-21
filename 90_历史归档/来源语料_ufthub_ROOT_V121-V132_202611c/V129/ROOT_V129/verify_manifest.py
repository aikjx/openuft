"""Run `python verify_manifest.py` from this archive's ROOT_V129 root."""
from pathlib import Path
import hashlib, sys
root=Path(__file__).resolve().parent
lines=(root/'MANIFEST.sha256').read_text(encoding='utf-8').splitlines()
failed=[]; count=0
for line in lines:
    if not line.strip(): continue
    digest, rel=line.split('  ',1)
    fp=root/rel
    if not fp.is_file() or hashlib.sha256(fp.read_bytes()).hexdigest()!=digest:
        failed.append(rel)
    count+=1
print('SHA256 manifest entries:',count,'failed:',len(failed))
if failed: print('\n'.join(failed));sys.exit(1)
