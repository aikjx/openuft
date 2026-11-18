"""Verify frozen source files from SHA256_MANIFEST.csv. Does not validate physical hypotheses."""
from pathlib import Path
from hashlib import sha256
import csv,json
P=Path(__file__).resolve().parent
with (P/'SHA256_MANIFEST.csv').open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
problems=[]
for row in rows:
    file=P/row['path']
    if not file.exists(): problems.append({'file':row['path'],'error':'missing'})
    elif sha256(file.read_bytes()).hexdigest()!=row['sha256']:problems.append({'file':row['path'],'error':'sha256 mismatch'})
    elif file.stat().st_size!=int(row['bytes']):problems.append({'file':row['path'],'error':'byte size mismatch'})
res={'verified':len(rows)-len(problems),'total':len(rows),'problems':problems,
     'statement':'Integrity only; not validation of new physics.'}
print(json.dumps(res,ensure_ascii=False,indent=2))
if problems:raise SystemExit(1)
