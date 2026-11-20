"""Check every SHA256 entry in the delivered archive; does not alter files."""
from pathlib import Path
import hashlib,csv,sys,json
root=Path(__file__).resolve().parent.parent
manifest=root/'SHA256_MANIFEST.csv'
with manifest.open(encoding='utf-8-sig',newline='') as f: entries=list(csv.DictReader(f))
wrong=[]
for entry in entries:
 f=root/entry['relative_path']
 if not f.is_file():wrong.append([entry['relative_path'],'MISSING']);continue
 digest=hashlib.sha256(f.read_bytes()).hexdigest()
 if digest!=entry['sha256']:wrong.append([entry['relative_path'],'MISMATCH'])
result={'manifest_count':len(entries),'mismatch_count':len(wrong),'mismatches':wrong}
print(json.dumps(result,indent=2,ensure_ascii=False))
if wrong:sys.exit(1)
