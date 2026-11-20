"""Verify shipped archive contents before running any recalculation."""
from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parent

def main():
  lines=(ROOT/'CHECKSUMS.sha256').read_text(encoding='utf-8').splitlines()
  for line in lines:
    if not line:continue
    sha,rel=line.split('  ',1)
    path=(ROOT/rel).resolve()
    if not path.is_relative_to(ROOT):raise RuntimeError('illegal outside path')
    if not path.is_file():raise FileNotFoundError(path)
    actual=hashlib.sha256(path.read_bytes()).hexdigest()
    if sha!=actual:raise ValueError(f'sha mismatch: {rel}')
  print(f'PASS: {len(lines)} files SHA-256 verified (self checksum file excluded)')
if __name__=='__main__':main()
