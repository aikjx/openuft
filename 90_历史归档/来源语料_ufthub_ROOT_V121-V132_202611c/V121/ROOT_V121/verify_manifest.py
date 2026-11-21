"""Verify pinned SHA256 inventory for the delivered ROOT V121 working tree."""
from pathlib import Path
import hashlib, sys
ROOT=Path(__file__).resolve().parent
MANIFEST=ROOT/'MANIFEST.sha256'

def main():
    if not MANIFEST.exists():
        print('MISSING MANIFEST.sha256');return 2
    rows=[line.strip().split('  ',1) for line in MANIFEST.read_text().splitlines() if line.strip()]
    good=0
    for sha, rel in rows:
        p=ROOT/rel
        if not p.is_file():print('MISSING',rel);return 1
        actual=hashlib.sha256(p.read_bytes()).hexdigest()
        if actual!=sha:print('BAD HASH',rel);return 1
        good+=1
    listed={item[1] for item in rows}
    present={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*')
             if p.is_file() and p.name!='MANIFEST.sha256' and '__pycache__' not in p.parts and '.pytest_cache' not in p.parts}
    if present!=listed:
        print('MANIFEST MISMATCH: unlisted files=',sorted(present-listed),
              '; missing files=',sorted(listed-present));return 1
    print(f'PASS: {good} files verified against SHA256.');return 0

if __name__=='__main__':sys.exit(main())
