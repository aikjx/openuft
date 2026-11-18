"""SHA-256 validation for the extracted ROOT V74 project."""
import csv,hashlib,pathlib,sys
root=pathlib.Path(__file__).resolve().parent
manifest=root/'SHA256_MANIFEST.csv'
with manifest.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
problems=[]
for row in rows:
    p=root/row['relative_path']
    if not p.is_file():problems.append('MISSING '+str(p));continue
    digest=hashlib.sha256(p.read_bytes()).hexdigest()
    if digest!=row['sha256']:problems.append('MISMATCH '+str(p))
print('Files checked:',len(rows),'integrity problems:',len(problems))
for p in problems:print(p)
if problems:sys.exit(1)
