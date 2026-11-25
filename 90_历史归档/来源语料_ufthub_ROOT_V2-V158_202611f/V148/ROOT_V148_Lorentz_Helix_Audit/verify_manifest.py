from pathlib import Path
import hashlib
BASE=Path(__file__).resolve().parent

def verify():
    missing=[];bad=[];n=0
    for line in (BASE/'MANIFEST.sha256').read_text(encoding='utf-8').splitlines():
        if not line.strip():continue
        hexdigest,rel=line.split('  ',1)
        p=BASE/rel
        if not p.is_file():missing.append(rel)
        elif hashlib.sha256(p.read_bytes()).hexdigest()!=hexdigest:bad.append(rel)
        n+=1
    if missing or bad:
        raise AssertionError(f'FAIL missing={missing} changed={bad}')
    print(f'MANIFEST OK: {n} files verified')
    return n

if __name__=='__main__':verify()
