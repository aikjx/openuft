"""SHA-256 checks against CHECKSUMS.sha256. No mutable UI or secret contents."""
import hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def run():
  checks=(ROOT/'CHECKSUMS.sha256').read_text().splitlines()
  for line in checks:
    h,rel=line.split('  ',1)
    p=ROOT/rel
    if not p.is_file():raise FileNotFoundError(p)
    if hashlib.sha256(p.read_bytes()).hexdigest()!=h:raise ValueError('SHA mismatch '+rel)
  print(f'OK: {len(checks)} SHA256 files')
  return len(checks)
if __name__=='__main__':run()
