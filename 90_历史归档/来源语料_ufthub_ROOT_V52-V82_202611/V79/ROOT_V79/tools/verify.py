"""Check manifest SHA-256 of V79 files. ZIP separate CRC checked by packaging driver."""
import csv,hashlib,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'SHA256_MANIFEST.csv'
def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def check():
    entries=[];issues=[]
    with MANIFEST.open(encoding='utf-8-sig',newline='') as f:
        for row in csv.DictReader(f):
            p=ROOT/row['relative_path']
            if not p.is_file():issues.append(f'missing: {row["relative_path"]}')
            elif digest(p)!=row['sha256']:issues.append(f'changed: {row["relative_path"]}')
            entries.append(row)
    status={'files_expected':len(entries),'files_verified':len(entries)-len(issues),'issues':issues,'passed':not issues}
    print(json.dumps(status,ensure_ascii=False,indent=2))
    if issues:raise SystemExit(2)
    return status
if __name__=='__main__':check()
