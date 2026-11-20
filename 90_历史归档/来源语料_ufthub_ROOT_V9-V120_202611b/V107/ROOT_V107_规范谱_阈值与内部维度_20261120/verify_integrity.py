"""Verify all listed file hashes, excluding the hash listing and manifest itself."""
from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parent

def main():
    lines=(ROOT/'CHECKSUMS.sha256').read_text(encoding='utf-8').splitlines()
    for row in lines:
        if not row.strip():continue
        h,rel=row.split('  ',1)
        actual=hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()
        assert actual==h,('hash mismatch',rel)
    print('verified',len(lines),'sha256 hashes')
if __name__=='__main__':main()
