from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parent
lines=(ROOT/'CHECKSUMS.sha256').read_text(encoding='utf-8').splitlines()
for line in lines:
    expected,rel=line.split('  ',1)
    p=ROOT/rel
    assert p.is_file(),f'missing {rel}'
    actual=hashlib.sha256(p.read_bytes()).hexdigest()
    assert actual==expected,f'hash mismatch {rel}'
print('V96 CHECKSUMS PASS',len(lines),'files')
