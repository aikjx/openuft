"""Build deterministic V94 ZIP, manifest and hashes. No silent changes to V93 archive."""
from pathlib import Path
import hashlib,json,zipfile,os
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'ROOT_V94_从作用量到螺旋闭环_205项科研总集_20261118.zip'

def candidates():
    return sorted(p for p in ROOT.rglob('*') if p.is_file()
        and '__pycache__' not in p.parts and p.suffix not in ['.pyc']
        and p.name not in ['CHECKSUMS.sha256','MANIFEST.json'])

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for block in iter(lambda:f.read(2**20),b''):h.update(block)
    return h.hexdigest()

def build():
    items=candidates()
    metadata={'title':'ROOT V94| Covariant Action and Torus-Knot Inverse Dynamics',
      'date':'2026-11-18','status':'THEORY_AND_NUMERICAL_ONLY_NO_UNIFICATION_PROOF',
      'historical_archive':'archive/ROOT_V93_original.zip',
      'research_issues':205,'tests':{'V94_python':39,'V93_original_regression':36,'Sympy_checks':22},
      'dimension_audit':{'quantities':54,'pairs':1431,'equations':33,'mismatches':7},
      'files':[{'path':str(x.relative_to(ROOT)),'size':x.stat().st_size,'sha256':sha(x)} for x in items]}
    (ROOT/'MANIFEST.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2))
    items=candidates()+[ROOT/'MANIFEST.json']
    (ROOT/'CHECKSUMS.sha256').write_text(''.join(f'{sha(x)}  {x.relative_to(ROOT).as_posix()}\n' for x in sorted(items)))
    items=sorted(items+[ROOT/'CHECKSUMS.sha256'])
    with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
        for p in items:z.write(p,arcname=f'{ROOT.name}/{p.relative_to(ROOT).as_posix()}')
    with zipfile.ZipFile(OUT) as z:
        assert z.testzip() is None
        assert len(z.namelist())==len(items)
    print(json.dumps({'zip':str(OUT),'file_count':len(items),'zip_bytes':OUT.stat().st_size,'validated':True},ensure_ascii=False))
    return OUT
if __name__=='__main__':build()
