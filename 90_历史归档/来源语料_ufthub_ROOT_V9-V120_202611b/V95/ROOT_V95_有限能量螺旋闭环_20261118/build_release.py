from pathlib import Path
import hashlib,zipfile,json,os
root=Path(__file__).resolve().parent
out=root.parent/'ROOT_V95_有限能量Maxwell螺旋闭环_229项科研包_20261118.zip'

def eligible(p):
    rel=p.relative_to(root)
    if not p.is_file():return False
    if any(x in ('__pycache__','.pytest_cache','.git') for x in rel.parts):return False
    if p.suffix in ('.pyc','.pyo'):return False
    return True
files=[p for p in root.rglob('*') if eligible(p) and p.name not in ('MANIFEST.json','CHECKSUMS.sha256')]
files=sorted(files,key=lambda p:str(p.relative_to(root)))
checksum=''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(root).as_posix()}\n' for p in files)
(root/'CHECKSUMS.sha256').write_text(checksum,encoding='utf-8')
manifest={'project':'ROOT V95 finite energy Maxwell trajectory inverse problem',
          'date':'2026-11-18','science_status':'conditional mathematical construction only; NOT four-force unification',
          'historical_v94_archive_included':True,'ledger_items':229,
          'v95_python_tests_passed':51,'v94_python_tests_passed':39,'v94_subtests_passed':4,
          'browser_checks_passed':7,'num_dimension_equations':24,'dimension_invalid_examples':4,
          'independent_high_precision_digits':65,
          'hashed_file_count_excluding_manifest_and_checksum':len(files),
          'file_hashes':{p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(root/'MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=8) as z:
    for p in sorted([p for p in root.rglob('*') if eligible(p)],key=lambda p:str(p.relative_to(root))):
        z.write(p,(root.name+'/'+p.relative_to(root).as_posix()))
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
print(json.dumps({'zip':str(out),'size_bytes':out.stat().st_size,'zip_entries':len(zipfile.ZipFile(out).namelist()),'sha256_files':len(files),'zip_sha256':hashlib.sha256(out.read_bytes()).hexdigest()},ensure_ascii=False,indent=2))
