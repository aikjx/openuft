"""Verify every distributed file from CHECKSUMS.sha256, excluding the checksum itself."""
from pathlib import Path
import hashlib
BASE=Path(__file__).resolve().parent

def run():
    rows=(BASE/'CHECKSUMS.sha256').read_text(encoding='utf-8').splitlines()
    for line in rows:
        if not line.strip(): continue
        sig,filename=line.split('  ',1)
        p=BASE/filename
        if not p.is_file():raise FileNotFoundError(filename)
        got=hashlib.sha256(p.read_bytes()).hexdigest()
        if got!=sig:raise ValueError('hash mismatch '+filename)
    print(f'CHECKSUM OK: {len(rows)} files')
    return len(rows)

if __name__=='__main__':run()
