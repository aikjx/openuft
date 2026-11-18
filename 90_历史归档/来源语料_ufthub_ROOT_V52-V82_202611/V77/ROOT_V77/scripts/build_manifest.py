"""Build a SHA256 manifest of all existing project files except itself.
Note: changing files after running this invalidates the manifest.
"""
from pathlib import Path
import csv,hashlib
BASE=Path(__file__).resolve().parents[1]
files=sorted(x for x in BASE.rglob('*') if x.is_file() and x.name != 'SHA256_MANIFEST.csv' and '__pycache__' not in x.parts and '.pytest_cache' not in x.parts)
with (BASE/'SHA256_MANIFEST.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['relative_path','sha256','size_bytes'])
 for p in files:
  w.writerow([p.relative_to(BASE).as_posix(),hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_size])
print('Manifest hashed',len(files),'files')
