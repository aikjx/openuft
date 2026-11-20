"""Verify manifest and 1-by-1 SHA-256 checksum. Does not mutate project files."""
from pathlib import Path
import hashlib,json,sys,csv,zipfile
root=Path(__file__).resolve().parent
rows=[]
for line in (root/'CHECKSUMS.sha256').read_text(encoding='utf-8').splitlines():
    if not line.strip():continue
    sha,relative=line.split('  ',1)
    p=root/relative
    if not p.is_file():raise SystemExit(f'MISSING: {relative}')
    got=hashlib.sha256(p.read_bytes()).hexdigest()
    if sha!=got:raise SystemExit(f'HASH MISMATCH: {relative}')
    rows.append(relative)
manifest=json.loads((root/'MANIFEST.json').read_text(encoding='utf-8'))
assert manifest['file_count']==len(rows)-1,(manifest['file_count'],len(rows))
with (root/'ledger/V111_ALL_396_PRESERVED.csv').open(encoding='utf-8-sig') as f:
    ledger=list(csv.DictReader(f))
assert len(ledger)==396 and len({r['canonical_id'] for r in ledger})==396
with zipfile.ZipFile(root/'archive/ROOT_V110_original.zip') as previous:
    assert previous.testzip() is None
print('All checksums PASS:',len(rows),'including manifest. Original nested V110 archive:',(root/'archive/ROOT_V110_original.zip').exists())
