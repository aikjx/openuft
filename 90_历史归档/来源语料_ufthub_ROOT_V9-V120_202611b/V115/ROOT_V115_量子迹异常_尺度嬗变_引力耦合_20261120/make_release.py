"""Build SHA manifest and complete distribution ZIP. Exclude runtime pycache."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent
ZIP=ROOT.parent/'ROOT_V115_量子迹异常_强弱电磁引力_396项科研总集_20261120.zip'

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

ignore={'.pytest_cache','__pycache__','.git'}
paths=sorted([p for p in ROOT.rglob('*') if p.is_file() and not any(x in ignore for x in p.relative_to(ROOT).parts)
              and p.name not in ('MANIFEST.json','CHECKSUMS.sha256')])
manifest={
 'project':'ROOT V115 quantum trace anomaly RG and induced-gravity audit',
 'research_date':'2026-11-20',
 'five_fundamental_OPEN':'OPEN',
 'historical_issues':396,
 'v115_pytest_tests':115,
 'v114_historical_pytest_tests':90,
 'chromium_e2e_checks':12,
 'model_limits':'one-loop fixed nf, induced-gravity scalar-stabilized assumption; no new G prediction',
 'files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in paths]
}
(ROOT/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
checksum=[sha(ROOT/'MANIFEST.json')+'  MANIFEST.json']
checksum.extend(f"{item['sha256']}  {item['path']}" for item in manifest['files'])
(ROOT/'CHECKSUMS.sha256').write_text('\n'.join(checksum)+'\n',encoding='utf-8')
with zipfile.ZipFile(ZIP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for path in sorted(paths+[ROOT/'MANIFEST.json',ROOT/'CHECKSUMS.sha256']):
        z.write(path,arcname=f'{ROOT.name}/{path.relative_to(ROOT).as_posix()}')
with zipfile.ZipFile(ZIP) as z:
    assert z.testzip() is None
print('ZIP',ZIP)
print('bytes',ZIP.stat().st_size,'members',len(paths)+2,'hash-tracked',len(paths))
