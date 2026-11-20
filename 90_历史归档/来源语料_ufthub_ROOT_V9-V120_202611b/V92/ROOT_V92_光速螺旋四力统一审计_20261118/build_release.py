"""Publish ROOT V92 research artifact with manifest, SHA256 and ZIP integrity.
Run only after running run_all.py and browser smoke. Bundle outside project dir.
"""
from pathlib import Path
import hashlib,json,zipfile,os
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'ROOT_V92_光速螺旋四力统一_147项问题审计_20261118.zip'

def pack():
    ignore={'MANIFEST.json','CHECKSUMS.sha256'}
    files=sorted([p for p in ROOT.rglob('*') if p.is_file() and not any(x in ('__pycache__','.pytest_cache') for x in p.relative_to(ROOT).parts) and p.suffix not in ('.pyc','.pyo') and p.name not in ignore])
    entries=[]
    for p in files:
        b=p.read_bytes();entries.append({'name':p.relative_to(ROOT).as_posix(),'size_bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
    manifest={'title':'ROOT V92 theoretical audit of luminal helix unification hypothesis','date':'2026-11-18',
              'scope':'MATH_SOFTWARE_ONLY','four_force_unified':False,
              'entries':entries,'n_entries_excluding_manifest_and_checksums':len(entries)}
    (ROOT/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    all_hashes=[(r['sha256'],r['name']) for r in entries]
    all_hashes.append((hashlib.sha256((ROOT/'MANIFEST.json').read_bytes()).hexdigest(),'MANIFEST.json'))
    (ROOT/'CHECKSUMS.sha256').write_text('\n'.join(a+'  '+b for a,b in all_hashes)+'\n',encoding='utf-8')
    with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8,allowZip64=True) as z:
        for p in files+[ROOT/'MANIFEST.json',ROOT/'CHECKSUMS.sha256']:
            z.write(p,arcname=f'{ROOT.name}/{p.relative_to(ROOT).as_posix()}')
    with zipfile.ZipFile(OUT) as z:
        corrupt=z.testzip()
        assert corrupt is None,corrupt
        assert len(z.namelist())==len(all_hashes)+1
    return {'zip':str(OUT),'size_bytes':OUT.stat().st_size,'entries':len(all_hashes)+1,
            'SHA256_zip':hashlib.sha256(OUT.read_bytes()).hexdigest()}
if __name__=='__main__':print(json.dumps(pack(),ensure_ascii=False,indent=2))
