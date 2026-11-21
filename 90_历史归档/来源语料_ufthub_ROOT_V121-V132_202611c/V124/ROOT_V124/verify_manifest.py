from pathlib import Path
import hashlib,sys
r=Path(__file__).resolve().parent
p=r/'MANIFEST.sha256'
for line in p.read_text(encoding='utf-8').splitlines():
    digest,rel=line.split('  ',1)
    f=(r/rel).resolve()
    if not f.is_relative_to(r) or not f.is_file():
        raise SystemExit(f'BAD FILE {rel}')
    actual=hashlib.sha256(f.read_bytes()).hexdigest()
    if digest!=actual:raise SystemExit(f'CHECKSUM FAIL {rel}')
print('V124_MANIFEST_OK',len(p.read_text().splitlines()))
